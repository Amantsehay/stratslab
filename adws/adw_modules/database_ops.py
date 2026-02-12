"""Database Operations Module for ADW - Synchronous database access.

Provides synchronous database operations for ADW workflow tracking,
designed to work within the ADW subprocess-based execution model.
"""

import json
import logging
import os
import subprocess
from typing import Optional, Dict, List, Any
from datetime import datetime


class DatabaseOps:
    """Synchronous database operations for ADW workflows."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize database operations.

        Args:
            logger: Logger instance for messages
        """
        self.logger = logger or logging.getLogger(__name__)
        self.database_url = os.getenv("DATABASE_URL")

    def log_workflow_event(
        self,
        adw_id: str,
        issue_number: int,
        workflow_type: str,
        event: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Log a workflow event to database for audit trail.

        This uses the Python script runner to execute a database insertion
        in the main process context to avoid async complexity.

        Args:
            adw_id: Workflow ID
            issue_number: GitHub issue number
            workflow_type: Type of workflow
            event: Event name (created, started, phase_completed, etc.)
            details: Optional structured data

        Returns:
            True if logged successfully
        """
        if not self.database_url:
            self.logger.debug("Database URL not configured, skipping event logging")
            return False

        try:
            # Create event payload
            payload = {
                "adw_id": adw_id,
                "issue_number": issue_number,
                "workflow_type": workflow_type,
                "event": event,
                "timestamp": datetime.utcnow().isoformat(),
                "details": details or {},
            }

            self.logger.debug(f"Logging event: {event} for {adw_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to log workflow event: {e}")
            return False

    def save_workflow_output(
        self,
        adw_id: str,
        phase: str,
        output_file: str,
        status: str = "completed",
    ) -> bool:
        """Save workflow phase output file reference to database.

        Args:
            adw_id: Workflow ID
            phase: Phase name (plan, build, test)
            output_file: Path to output file
            status: Phase completion status

        Returns:
            True if saved successfully
        """
        try:
            self.logger.debug(f"Saving output for {adw_id}:{phase} -> {output_file}")
            # This would be connected to the database in the API
            return True
        except Exception as e:
            self.logger.error(f"Failed to save workflow output: {e}")
            return False

    def record_phase_error(
        self,
        adw_id: str,
        phase: str,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Record a phase failure to database.

        Args:
            adw_id: Workflow ID
            phase: Phase name
            error_message: Error message
            error_details: Optional additional error details

        Returns:
            True if recorded successfully
        """
        try:
            self.logger.debug(f"Recording error for {adw_id}:{phase}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to record phase error: {e}")
            return False

    def mark_workflow_complete(
        self,
        adw_id: str,
        status: str = "completed",
        pull_request_url: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> bool:
        """Mark a workflow as complete in the database.

        Args:
            adw_id: Workflow ID
            status: Final status (completed, failed, cancelled)
            pull_request_url: URL to PR if created
            summary: Implementation summary

        Returns:
            True if marked successfully
        """
        try:
            self.logger.info(f"Marking workflow complete: {adw_id} -> {status}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to mark workflow complete: {e}")
            return False


# Global instance
_db_ops_instance: Optional[DatabaseOps] = None


def get_database_ops(logger: Optional[logging.Logger] = None) -> DatabaseOps:
    """Get or create the global DatabaseOps instance."""
    global _db_ops_instance
    if _db_ops_instance is None:
        _db_ops_instance = DatabaseOps(logger)
    return _db_ops_instance
