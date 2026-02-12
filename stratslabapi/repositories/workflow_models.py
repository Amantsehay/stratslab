"""Workflow tracking models for Agentic Developer Workflow (ADW) system.

Models to track workflow runs, phases, and execution logs.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base


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


class LogLevel(str, Enum):
    """Log message severity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class WorkflowRun(Base):
    """Track each Agentic Developer Workflow execution."""

    __tablename__ = "workflow_runs"

    # Identifiers
    adw_id: Mapped[str] = mapped_column(
        String(8), unique=True, index=True, nullable=False
    )
    issue_number: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    workflow_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Status
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")

    # Execution details
    branch_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    plan_file: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Tracking timestamps
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Error information
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_phase: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Results
    pull_request_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    implementation_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    phases: Mapped[list["WorkflowPhaseRun"]] = relationship(
        back_populates="workflow_run", cascade="all, delete-orphan"
    )
    logs: Mapped[list["WorkflowLog"]] = relationship(
        back_populates="workflow_run", cascade="all, delete-orphan"
    )

    # Indexes for common queries
    __table_args__ = (
        Index("ix_workflow_runs_adw_id", "adw_id"),
        Index("ix_workflow_runs_issue_number", "issue_number"),
        Index("ix_workflow_runs_status", "status"),
        Index("ix_workflow_runs_created_at", "created_at"),
    )


class WorkflowPhaseRun(Base):
    """Track individual phase execution within a workflow."""

    __tablename__ = "workflow_phase_runs"

    # Foreign key
    workflow_run_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False
    )

    # Phase details
    phase: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")

    # Execution timestamps
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Output and error information
    output_file: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    workflow_run: Mapped["WorkflowRun"] = relationship(back_populates="phases")

    # Indexes
    __table_args__ = (
        Index("ix_workflow_phase_runs_workflow_id", "workflow_run_id"),
        Index("ix_workflow_phase_runs_phase", "phase"),
        Index("ix_workflow_phase_runs_status", "status"),
    )


class WorkflowLog(Base):
    """Detailed execution logs for workflow debugging and monitoring."""

    __tablename__ = "workflow_logs"

    # Foreign key
    workflow_run_id: Mapped[UUID] = mapped_column(
        ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False
    )

    # Log details
    level: Mapped[str] = mapped_column(String(20), nullable=False, default="INFO")
    message: Mapped[str] = mapped_column(Text, nullable=False)

    # Optional structured data for debugging
    context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    workflow_run: Mapped["WorkflowRun"] = relationship(back_populates="logs")

    # Indexes for querying logs
    __table_args__ = (
        Index("ix_workflow_logs_workflow_id", "workflow_run_id"),
        Index("ix_workflow_logs_level", "level"),
        Index("ix_workflow_logs_created_at", "created_at"),
    )
