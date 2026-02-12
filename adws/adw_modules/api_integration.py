"""API Integration Module for ADW Workflow Tracking.

Handles integration with the FastAPI application for workflow persistence,
status tracking, and logging.
"""

import json
import logging
import os
from datetime import datetime
from typing import Optional
from uuid import uuid4

# Try to import from stratslabapi, but make it optional for standalone ADW execution
try:
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False


class WorkflowAPI:
    """Handle workflow tracking and status updates via API or database."""

    def __init__(self, database_url: Optional[str] = None, logger: Optional[logging.Logger] = None):
        """Initialize API integration.

        Args:
            database_url: PostgreSQL connection string (optional)
            logger: Logger instance for messages
        """
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.logger = logger or logging.getLogger(__name__)
        self.engine = None
        self.session_maker = None

        if self.database_url and SQLALCHEMY_AVAILABLE:
            self._setup_database()

    def _setup_database(self) -> None:
        """Set up database connection pool."""
        try:
            self.engine = create_async_engine(
                self.database_url,
                echo=False,
                pool_size=5,
                max_overflow=10,
            )
            self.session_maker = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            self.logger.info("Database connection pool initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize database: {e}")
            self.engine = None
            self.session_maker = None

    async def create_workflow_run(
        self,
        adw_id: str,
        issue_number: int,
        workflow_type: str,
        branch_name: Optional[str] = None,
        plan_file: Optional[str] = None,
    ) -> dict:
        """Create a new workflow run record in the database.

        Args:
            adw_id: Unique workflow ID
            issue_number: GitHub issue number
            workflow_type: Type of workflow (adw_plan, adw_build, etc.)
            branch_name: Git branch name if applicable
            plan_file: Path to plan file if applicable

        Returns:
            Dictionary with workflow run details
        """
        if not self.session_maker:
            self.logger.warning("Database not available, skipping workflow run creation")
            return {"adw_id": adw_id, "status": "pending"}

        try:
            from stratslabapi.repositories.workflow_models import WorkflowRun

            async with self.session_maker() as session:
                workflow = WorkflowRun(
                    adw_id=adw_id,
                    issue_number=issue_number,
                    workflow_type=workflow_type,
                    branch_name=branch_name,
                    plan_file=plan_file,
                    status="pending",
                )
                session.add(workflow)
                await session.commit()
                await session.refresh(workflow)

                self.logger.info(f"Created workflow run: {adw_id}")
                return {
                    "adw_id": adw_id,
                    "status": "pending",
                    "created_at": workflow.created_at.isoformat(),
                }
        except Exception as e:
            self.logger.error(f"Failed to create workflow run: {e}")
            return {"adw_id": adw_id, "status": "pending", "error": str(e)}

    async def update_workflow_status(
        self,
        adw_id: str,
        status: str,
        error_message: Optional[str] = None,
        error_phase: Optional[str] = None,
        pull_request_url: Optional[str] = None,
    ) -> bool:
        """Update workflow run status.

        Args:
            adw_id: Workflow ID
            status: New status (running, completed, failed, etc.)
            error_message: Error message if failed
            error_phase: Which phase failed
            pull_request_url: URL to created PR if applicable

        Returns:
            True if successful, False otherwise
        """
        if not self.session_maker:
            return False

        try:
            from stratslabapi.repositories.workflow_models import WorkflowRun
            from sqlalchemy import select

            async with self.session_maker() as session:
                stmt = select(WorkflowRun).where(WorkflowRun.adw_id == adw_id)
                result = await session.execute(stmt)
                workflow = result.scalar_one_or_none()

                if not workflow:
                    self.logger.warning(f"Workflow not found: {adw_id}")
                    return False

                workflow.status = status
                if error_message:
                    workflow.error_message = error_message
                if error_phase:
                    workflow.error_phase = error_phase
                if pull_request_url:
                    workflow.pull_request_url = pull_request_url

                if status == "running":
                    workflow.started_at = datetime.utcnow()
                elif status in ("completed", "failed", "cancelled"):
                    workflow.completed_at = datetime.utcnow()

                await session.commit()
                self.logger.info(f"Updated workflow status: {adw_id} -> {status}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to update workflow status: {e}")
            return False

    async def add_phase_run(
        self,
        adw_id: str,
        phase: str,
        status: str = "pending",
    ) -> bool:
        """Add a phase run record for a workflow.

        Args:
            adw_id: Workflow ID
            phase: Phase name (plan, build, test)
            status: Initial phase status

        Returns:
            True if successful, False otherwise
        """
        if not self.session_maker:
            return False

        try:
            from stratslabapi.repositories.workflow_models import WorkflowRun, WorkflowPhaseRun
            from sqlalchemy import select

            async with self.session_maker() as session:
                # Get the workflow run
                stmt = select(WorkflowRun).where(WorkflowRun.adw_id == adw_id)
                result = await session.execute(stmt)
                workflow = result.scalar_one_or_none()

                if not workflow:
                    self.logger.warning(f"Workflow not found for phase: {adw_id}")
                    return False

                # Create phase run
                phase_run = WorkflowPhaseRun(
                    workflow_run_id=workflow.id,
                    phase=phase,
                    status=status,
                )
                session.add(phase_run)
                await session.commit()
                self.logger.info(f"Added phase run: {adw_id}:{phase}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to add phase run: {e}")
            return False

    async def add_log(
        self,
        adw_id: str,
        message: str,
        level: str = "INFO",
        context: Optional[dict] = None,
    ) -> bool:
        """Add a log entry for a workflow.

        Args:
            adw_id: Workflow ID
            message: Log message
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            context: Optional structured data for debugging

        Returns:
            True if successful, False otherwise
        """
        if not self.session_maker:
            return False

        try:
            from stratslabapi.repositories.workflow_models import WorkflowRun, WorkflowLog
            from sqlalchemy import select

            async with self.session_maker() as session:
                # Get the workflow run
                stmt = select(WorkflowRun).where(WorkflowRun.adw_id == adw_id)
                result = await session.execute(stmt)
                workflow = result.scalar_one_or_none()

                if not workflow:
                    self.logger.debug(f"Workflow not found for logging: {adw_id}")
                    return False

                # Create log entry
                log_entry = WorkflowLog(
                    workflow_run_id=workflow.id,
                    level=level,
                    message=message,
                    context=context,
                )
                session.add(log_entry)
                await session.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to add log: {e}")
            return False

    async def get_workflow_status(self, adw_id: str) -> Optional[dict]:
        """Get current status of a workflow.

        Args:
            adw_id: Workflow ID

        Returns:
            Dictionary with workflow status or None if not found
        """
        if not self.session_maker:
            return None

        try:
            from stratslabapi.repositories.workflow_models import WorkflowRun
            from sqlalchemy import select

            async with self.session_maker() as session:
                stmt = select(WorkflowRun).where(WorkflowRun.adw_id == adw_id)
                result = await session.execute(stmt)
                workflow = result.scalar_one_or_none()

                if not workflow:
                    return None

                return {
                    "adw_id": workflow.adw_id,
                    "status": workflow.status,
                    "issue_number": workflow.issue_number,
                    "workflow_type": workflow.workflow_type,
                    "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
                    "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
                    "pull_request_url": workflow.pull_request_url,
                    "error_message": workflow.error_message,
                    "error_phase": workflow.error_phase,
                }
        except Exception as e:
            self.logger.error(f"Failed to get workflow status: {e}")
            return None

    async def close(self) -> None:
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            self.logger.info("Database connections closed")


# Global API instance
_api_instance: Optional[WorkflowAPI] = None


def get_workflow_api(database_url: Optional[str] = None) -> WorkflowAPI:
    """Get or create the global WorkflowAPI instance."""
    global _api_instance
    if _api_instance is None:
        _api_instance = WorkflowAPI(database_url)
    return _api_instance
