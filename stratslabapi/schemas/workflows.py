"""Pydantic schemas for Agentic Developer Workflow API endpoints."""

from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field


class WorkflowType(str, Enum):
    """ADW workflow types."""

    PLAN = "adw_plan"
    BUILD = "adw_build"
    TEST = "adw_test"
    PLAN_BUILD = "adw_plan_build"
    PLAN_BUILD_TEST = "adw_plan_build_test"


class WorkflowStatus(str, Enum):
    """Workflow execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowPhaseType(str, Enum):
    """Individual workflow phase types."""

    PLAN = "plan"
    BUILD = "build"
    TEST = "test"


class WorkflowPhaseStatus(str, Enum):
    """Phase execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# Request Schemas


class WorkflowTriggerRequest(BaseModel):
    """Request to trigger a new workflow."""

    issue_number: int = Field(..., description="GitHub issue number to process")
    workflow: WorkflowType = Field(
        ..., description="Type of workflow to execute"
    )


class WorkflowRetryRequest(BaseModel):
    """Request to retry a failed workflow or phase."""

    phase: Optional[WorkflowPhaseType] = Field(
        None, description="Specific phase to retry (optional, retries whole workflow if not specified)"
    )


# Response Schemas


class WorkflowPhaseStatusResponse(BaseModel):
    """Status of a single workflow phase."""

    phase: str = Field(..., description="Phase name (plan, build, test)")
    status: WorkflowPhaseStatus = Field(..., description="Current phase status")
    started_at: Optional[datetime] = Field(..., description="When phase started")
    completed_at: Optional[datetime] = Field(..., description="When phase completed")
    error: Optional[str] = Field(None, description="Error message if phase failed")

    class Config:
        from_attributes = True


class WorkflowRunResponse(BaseModel):
    """Complete workflow run information."""

    adw_id: str = Field(..., description="Unique workflow execution ID")
    issue_number: int = Field(..., description="GitHub issue number")
    workflow_type: WorkflowType = Field(..., description="Type of workflow")
    status: WorkflowStatus = Field(..., description="Current workflow status")

    # Execution details
    branch_name: Optional[str] = Field(None, description="Git branch created for this workflow")
    plan_file: Optional[str] = Field(None, description="Path to generated plan file")

    # Phases
    phases: List[WorkflowPhaseStatusResponse] = Field(
        default_factory=list, description="Status of each phase"
    )

    # Timestamps
    created_at: datetime = Field(..., description="When workflow was created")
    started_at: Optional[datetime] = Field(None, description="When workflow started")
    completed_at: Optional[datetime] = Field(None, description="When workflow completed")

    # Results
    pull_request_url: Optional[str] = Field(None, description="URL to created PR if applicable")
    implementation_summary: Optional[str] = Field(None, description="Summary of implementation changes")

    # Errors
    errors: List[str] = Field(
        default_factory=list, description="List of errors encountered"
    )

    class Config:
        from_attributes = True


class WorkflowListResponse(BaseModel):
    """Paginated list of workflows."""

    items: List[WorkflowRunResponse] = Field(..., description="List of workflow runs")
    total: int = Field(..., description="Total number of workflows matching filters")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")


class WorkflowLogsResponse(BaseModel):
    """Workflow execution logs."""

    logs: List[str] = Field(..., description="List of log lines from workflow execution")
    total_lines: int = Field(..., description="Total number of log lines")


# Pagination


class PaginationParams(BaseModel):
    """Pagination parameters for workflow list queries."""

    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")


# Filter Parameters


class WorkflowFilterParams(BaseModel):
    """Filter parameters for workflow list queries."""

    status: Optional[WorkflowStatus] = Field(None, description="Filter by workflow status")
    issue_number: Optional[int] = Field(None, description="Filter by issue number")
    workflow_type: Optional[WorkflowType] = Field(None, description="Filter by workflow type")
