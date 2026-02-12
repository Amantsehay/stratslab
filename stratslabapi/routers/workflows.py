"""REST API endpoints for Agentic Developer Workflow management.

Provides endpoints for triggering workflows, checking status, and monitoring
workflow execution.
"""

import logging
from typing import Optional, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stratslabapi.repositories.session import get_session
from stratslabapi.repositories.workflow_models import WorkflowRun, WorkflowPhaseRun
from stratslabapi.schemas.workflows import (
    WorkflowTriggerRequest,
    WorkflowRunResponse,
    WorkflowListResponse,
    WorkflowPhaseStatusResponse,
    WorkflowRetryRequest,
    WorkflowLogsResponse,
    WorkflowStatus,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.post("/trigger", response_model=WorkflowRunResponse)
async def trigger_workflow(
    request: WorkflowTriggerRequest,
    session: AsyncSession = Depends(get_session),
) -> WorkflowRunResponse:
    """Trigger a new agentic workflow.

    Args:
        request: Workflow trigger request with issue number and workflow type
        session: Database session

    Returns:
        Created workflow run details

    Raises:
        HTTPException: If workflow cannot be created
    """
    try:
        # Generate unique ADW ID
        adw_id = str(uuid4())[:8]

        # Create workflow run record
        workflow = WorkflowRun(
            adw_id=adw_id,
            issue_number=request.issue_number,
            workflow_type=request.workflow.value,
            status="pending",
        )
        session.add(workflow)
        await session.commit()
        await session.refresh(workflow)

        logger.info(f"Created workflow: {adw_id} for issue #{request.issue_number}")

        return WorkflowRunResponse(
            adw_id=workflow.adw_id,
            issue_number=workflow.issue_number,
            workflow_type=request.workflow,
            status=WorkflowStatus.PENDING,
            created_at=workflow.created_at,
            phases=[],
            errors=[],
        )
    except Exception as e:
        logger.error(f"Failed to trigger workflow: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger workflow")


@router.get("/{adw_id}", response_model=WorkflowRunResponse)
async def get_workflow_status(
    adw_id: str,
    session: AsyncSession = Depends(get_session),
) -> WorkflowRunResponse:
    """Get workflow status and details.

    Args:
        adw_id: Workflow ID
        session: Database session

    Returns:
        Workflow run details

    Raises:
        HTTPException: If workflow not found
    """
    try:
        stmt = select(WorkflowRun).where(WorkflowRun.adw_id == adw_id)
        result = await session.execute(stmt)
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Get phases
        phases_stmt = select(WorkflowPhaseRun).where(
            WorkflowPhaseRun.workflow_run_id == workflow.id
        )
        phases_result = await session.execute(phases_stmt)
        phase_runs = phases_result.scalars().all()

        phases = [
            WorkflowPhaseStatusResponse(
                phase=phase.phase,
                status=phase.status,
                started_at=phase.started_at,
                completed_at=phase.completed_at,
                error=phase.error_message,
            )
            for phase in phase_runs
        ]

        # Collect errors
        errors = []
        if workflow.error_message:
            errors.append(f"[{workflow.error_phase}] {workflow.error_message}")

        return WorkflowRunResponse(
            adw_id=workflow.adw_id,
            issue_number=workflow.issue_number,
            workflow_type=workflow.workflow_type,
            status=workflow.status,
            branch_name=workflow.branch_name,
            plan_file=workflow.plan_file,
            phases=phases,
            created_at=workflow.created_at,
            started_at=workflow.started_at,
            completed_at=workflow.completed_at,
            pull_request_url=workflow.pull_request_url,
            implementation_summary=workflow.implementation_summary,
            errors=errors,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workflow status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow status")


@router.get("", response_model=WorkflowListResponse)
async def list_workflows(
    status: Optional[WorkflowStatus] = Query(None, description="Filter by status"),
    issue_number: Optional[int] = Query(None, description="Filter by issue number"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    session: AsyncSession = Depends(get_session),
) -> WorkflowListResponse:
    """List workflows with optional filtering.

    Args:
        status: Filter by workflow status
        issue_number: Filter by GitHub issue number
        page: Page number for pagination
        page_size: Number of items per page
        session: Database session

    Returns:
        List of workflow runs with pagination info
    """
    try:
        # Build query
        stmt = select(WorkflowRun)

        if status:
            stmt = stmt.where(WorkflowRun.status == status.value)
        if issue_number:
            stmt = stmt.where(WorkflowRun.issue_number == issue_number)

        # Order by created_at descending
        stmt = stmt.order_by(WorkflowRun.created_at.desc())

        # Get total count
        count_stmt = select(WorkflowRun)
        if status:
            count_stmt = count_stmt.where(WorkflowRun.status == status.value)
        if issue_number:
            count_stmt = count_stmt.where(WorkflowRun.issue_number == issue_number)

        count_result = await session.execute(
            select(type(WorkflowRun)).select_entity_from(count_stmt)
        )
        total = len(count_result.all())

        # Apply pagination
        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size)

        result = await session.execute(stmt)
        workflows = result.scalars().all()

        items = []
        for workflow in workflows:
            # Get phases for each workflow
            phases_stmt = select(WorkflowPhaseRun).where(
                WorkflowPhaseRun.workflow_run_id == workflow.id
            )
            phases_result = await session.execute(phases_stmt)
            phase_runs = phases_result.scalars().all()

            phases = [
                WorkflowPhaseStatusResponse(
                    phase=phase.phase,
                    status=phase.status,
                    started_at=phase.started_at,
                    completed_at=phase.completed_at,
                    error=phase.error_message,
                )
                for phase in phase_runs
            ]

            errors = []
            if workflow.error_message:
                errors.append(f"[{workflow.error_phase}] {workflow.error_message}")

            items.append(
                WorkflowRunResponse(
                    adw_id=workflow.adw_id,
                    issue_number=workflow.issue_number,
                    workflow_type=workflow.workflow_type,
                    status=workflow.status,
                    branch_name=workflow.branch_name,
                    plan_file=workflow.plan_file,
                    phases=phases,
                    created_at=workflow.created_at,
                    started_at=workflow.started_at,
                    completed_at=workflow.completed_at,
                    pull_request_url=workflow.pull_request_url,
                    implementation_summary=workflow.implementation_summary,
                    errors=errors,
                )
            )

        return WorkflowListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        logger.error(f"Failed to list workflows: {e}")
        raise HTTPException(status_code=500, detail="Failed to list workflows")


@router.post("/{adw_id}/retry", response_model=WorkflowRunResponse)
async def retry_workflow(
    adw_id: str,
    request: WorkflowRetryRequest,
    session: AsyncSession = Depends(get_session),
) -> WorkflowRunResponse:
    """Retry a failed workflow or specific phase.

    Args:
        adw_id: Workflow ID
        request: Retry request with optional phase to retry
        session: Database session

    Returns:
        Updated workflow status

    Raises:
        HTTPException: If workflow not found or cannot be retried
    """
    try:
        stmt = select(WorkflowRun).where(WorkflowRun.adw_id == adw_id)
        result = await session.execute(stmt)
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Reset status for retry
        if request.phase:
            # Retry specific phase
            phase_stmt = select(WorkflowPhaseRun).where(
                WorkflowPhaseRun.workflow_run_id == workflow.id,
                WorkflowPhaseRun.phase == request.phase.value,
            )
            phase_result = await session.execute(phase_stmt)
            phase = phase_result.scalar_one_or_none()

            if phase:
                phase.status = "pending"
                phase.error_message = None
                phase.started_at = None
                phase.completed_at = None
        else:
            # Retry entire workflow
            workflow.status = "pending"
            workflow.error_message = None
            workflow.error_phase = None
            workflow.started_at = None
            workflow.completed_at = None

        await session.commit()
        await session.refresh(workflow)

        logger.info(f"Retried workflow: {adw_id}")

        # Return updated status
        phases_stmt = select(WorkflowPhaseRun).where(
            WorkflowPhaseRun.workflow_run_id == workflow.id
        )
        phases_result = await session.execute(phases_stmt)
        phase_runs = phases_result.scalars().all()

        phases = [
            WorkflowPhaseStatusResponse(
                phase=phase.phase,
                status=phase.status,
                started_at=phase.started_at,
                completed_at=phase.completed_at,
                error=phase.error_message,
            )
            for phase in phase_runs
        ]

        return WorkflowRunResponse(
            adw_id=workflow.adw_id,
            issue_number=workflow.issue_number,
            workflow_type=workflow.workflow_type,
            status=workflow.status,
            branch_name=workflow.branch_name,
            plan_file=workflow.plan_file,
            phases=phases,
            created_at=workflow.created_at,
            started_at=workflow.started_at,
            completed_at=workflow.completed_at,
            pull_request_url=workflow.pull_request_url,
            implementation_summary=workflow.implementation_summary,
            errors=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retry workflow: {e}")
        raise HTTPException(status_code=500, detail="Failed to retry workflow")


@router.get("/{adw_id}/logs", response_model=WorkflowLogsResponse)
async def get_workflow_logs(
    adw_id: str,
    session: AsyncSession = Depends(get_session),
) -> WorkflowLogsResponse:
    """Get execution logs for a workflow.

    Args:
        adw_id: Workflow ID
        session: Database session

    Returns:
        Workflow execution logs

    Raises:
        HTTPException: If workflow not found
    """
    try:
        stmt = select(WorkflowRun).where(WorkflowRun.adw_id == adw_id)
        result = await session.execute(stmt)
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Get logs
        from stratslabapi.repositories.workflow_models import WorkflowLog

        logs_stmt = select(WorkflowLog).where(
            WorkflowLog.workflow_run_id == workflow.id
        ).order_by(WorkflowLog.created_at.asc())

        logs_result = await session.execute(logs_stmt)
        log_records = logs_result.scalars().all()

        logs = [
            f"[{log.created_at.isoformat()}] [{log.level}] {log.message}"
            for log in log_records
        ]

        return WorkflowLogsResponse(logs=logs, total_lines=len(logs))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workflow logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workflow logs")
