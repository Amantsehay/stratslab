"""Add workflow tracking tables for Agentic Developer Workflow system.

Revision ID: 002
Revises: 001
Create Date: 2026-02-12

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create workflow_runs table
    op.create_table(
        "workflow_runs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("adw_id", sa.String(8), nullable=False),
        sa.Column("issue_number", sa.Integer(), nullable=False),
        sa.Column("workflow_type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("branch_name", sa.String(255), nullable=True),
        sa.Column("plan_file", sa.String(255), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("error_phase", sa.String(20), nullable=True),
        sa.Column("pull_request_url", sa.String(255), nullable=True),
        sa.Column("implementation_summary", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
        sa.UniqueConstraint("adw_id"),
    )
    op.create_index("ix_workflow_runs_adw_id", "workflow_runs", ["adw_id"])
    op.create_index("ix_workflow_runs_issue_number", "workflow_runs", ["issue_number"])
    op.create_index("ix_workflow_runs_status", "workflow_runs", ["status"])
    op.create_index("ix_workflow_runs_created_at", "workflow_runs", ["created_at"])

    # Create workflow_phase_runs table
    op.create_table(
        "workflow_phase_runs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("workflow_run_id", sa.UUID(), nullable=False),
        sa.Column("phase", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("output_file", sa.String(255), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_index("ix_workflow_phase_runs_workflow_id", "workflow_phase_runs", ["workflow_run_id"])
    op.create_index("ix_workflow_phase_runs_phase", "workflow_phase_runs", ["phase"])
    op.create_index("ix_workflow_phase_runs_status", "workflow_phase_runs", ["status"])

    # Create workflow_logs table
    op.create_table(
        "workflow_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("workflow_run_id", sa.UUID(), nullable=False),
        sa.Column("level", sa.String(20), nullable=False, server_default="INFO"),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("context", postgresql.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_index("ix_workflow_logs_workflow_id", "workflow_logs", ["workflow_run_id"])
    op.create_index("ix_workflow_logs_level", "workflow_logs", ["level"])
    op.create_index("ix_workflow_logs_created_at", "workflow_logs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_workflow_logs_created_at", "workflow_logs")
    op.drop_index("ix_workflow_logs_level", "workflow_logs")
    op.drop_index("ix_workflow_logs_workflow_id", "workflow_logs")
    op.drop_table("workflow_logs")

    op.drop_index("ix_workflow_phase_runs_status", "workflow_phase_runs")
    op.drop_index("ix_workflow_phase_runs_phase", "workflow_phase_runs")
    op.drop_index("ix_workflow_phase_runs_workflow_id", "workflow_phase_runs")
    op.drop_table("workflow_phase_runs")

    op.drop_index("ix_workflow_runs_created_at", "workflow_runs")
    op.drop_index("ix_workflow_runs_status", "workflow_runs")
    op.drop_index("ix_workflow_runs_issue_number", "workflow_runs")
    op.drop_index("ix_workflow_runs_adw_id", "workflow_runs")
    op.drop_table("workflow_runs")
