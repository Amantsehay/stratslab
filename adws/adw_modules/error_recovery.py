"""Error Recovery Module for ADW - Handle failures and enable recovery.

Provides error classification, retry logic, and state recovery mechanisms
for agentic workflows.
"""

import logging
from enum import Enum
from typing import Optional, Dict, Any, Tuple
from datetime import datetime


class ErrorSeverity(str, Enum):
    """Error severity levels for classification."""

    RECOVERABLE = "recoverable"
    PARTIALLY_RECOVERABLE = "partially_recoverable"
    FATAL = "fatal"


class ErrorType(str, Enum):
    """Classification of error types."""

    # API/Network errors
    API_TIMEOUT = "api_timeout"
    NETWORK_ERROR = "network_error"
    RATE_LIMIT = "rate_limit"

    # GitHub errors
    GITHUB_API_ERROR = "github_api_error"
    GITHUB_AUTH_ERROR = "github_auth_error"
    BRANCH_CONFLICT = "branch_conflict"

    # Claude Code errors
    CLAUDE_CODE_ERROR = "claude_code_error"
    AGENT_TIMEOUT = "agent_timeout"
    INVALID_PERMISSIONS = "invalid_permissions"

    # Git errors
    GIT_CONFLICT = "git_conflict"
    GIT_OPERATION_FAILED = "git_operation_failed"

    # Test errors
    TEST_FAILURE = "test_failure"
    MISSING_DEPENDENCIES = "missing_dependencies"

    # Configuration errors
    MISSING_ENV_VAR = "missing_env_var"
    INVALID_CONFIG = "invalid_config"

    # Unknown errors
    UNKNOWN = "unknown"


class ErrorClassification:
    """Classification of an error with recovery suggestions."""

    def __init__(
        self,
        error_type: ErrorType,
        severity: ErrorSeverity,
        recoverable: bool,
        retry_able: bool,
        recovery_steps: list[str],
    ):
        """Initialize error classification."""
        self.error_type = error_type
        self.severity = severity
        self.recoverable = recoverable
        self.retry_able = retry_able
        self.recovery_steps = recovery_steps


class ErrorRecovery:
    """Handle error recovery and retry logic."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize error recovery.

        Args:
            logger: Logger instance for messages
        """
        self.logger = logger or logging.getLogger(__name__)
        self.max_retries = 3
        self.retry_delay_seconds = 5

    def classify_error(self, error_message: str, phase: str) -> ErrorClassification:
        """Classify an error and provide recovery suggestions.

        Args:
            error_message: The error message to classify
            phase: Which phase the error occurred in (plan, build, test)

        Returns:
            ErrorClassification with recovery information
        """
        error_lower = error_message.lower()

        # API/Network errors
        if "timeout" in error_lower or "timed out" in error_lower:
            return ErrorClassification(
                ErrorType.API_TIMEOUT,
                ErrorSeverity.RECOVERABLE,
                True,
                True,
                ["Wait and retry the workflow", "Check network connectivity", "Check API status"],
            )

        if "connection" in error_lower or "refused" in error_lower:
            return ErrorClassification(
                ErrorType.NETWORK_ERROR,
                ErrorSeverity.RECOVERABLE,
                True,
                True,
                ["Check network connectivity", "Verify database is running", "Retry workflow"],
            )

        if "rate limit" in error_lower or "429" in error_lower:
            return ErrorClassification(
                ErrorType.RATE_LIMIT,
                ErrorSeverity.PARTIALLY_RECOVERABLE,
                True,
                True,
                ["Wait before retrying (GitHub rate limit)", "Check API quotas"],
            )

        # GitHub errors
        if "github" in error_lower:
            if "auth" in error_lower or "token" in error_lower or "permission" in error_lower:
                return ErrorClassification(
                    ErrorType.GITHUB_AUTH_ERROR,
                    ErrorSeverity.FATAL,
                    False,
                    False,
                    [
                        "Verify GITHUB_PAT token is valid",
                        "Check token has required permissions",
                        "Run: gh auth login",
                    ],
                )

            if "conflict" in error_lower or "merge" in error_lower:
                return ErrorClassification(
                    ErrorType.BRANCH_CONFLICT,
                    ErrorSeverity.PARTIALLY_RECOVERABLE,
                    True,
                    True,
                    [
                        "Manually resolve branch conflict",
                        "Rebase branch on main",
                        "Retry workflow after resolving conflict",
                    ],
                )

            return ErrorClassification(
                ErrorType.GITHUB_API_ERROR,
                ErrorSeverity.RECOVERABLE,
                True,
                True,
                ["Check GitHub status page", "Retry workflow"],
            )

        # Claude Code errors
        if "claude" in error_lower:
            if "permission" in error_lower or "permission" in error_lower:
                return ErrorClassification(
                    ErrorType.INVALID_PERMISSIONS,
                    ErrorSeverity.FATAL,
                    False,
                    False,
                    ["Grant Claude Code CLI required permissions", "Check clauses/security settings"],
                )

            if "timeout" in error_lower:
                return ErrorClassification(
                    ErrorType.AGENT_TIMEOUT,
                    ErrorSeverity.PARTIALLY_RECOVERABLE,
                    True,
                    True,
                    ["Increase ADW_TIMEOUT environment variable", "Simplify the task", "Retry workflow"],
                )

            return ErrorClassification(
                ErrorType.CLAUDE_CODE_ERROR,
                ErrorSeverity.RECOVERABLE,
                True,
                True,
                ["Check Claude Code CLI is installed", "Update Claude Code CLI", "Retry workflow"],
            )

        # Git errors
        if "git" in error_lower:
            if "conflict" in error_lower:
                return ErrorClassification(
                    ErrorType.GIT_CONFLICT,
                    ErrorSeverity.PARTIALLY_RECOVERABLE,
                    True,
                    True,
                    ["Resolve git conflicts manually", "Run: git status", "Retry workflow after fixing"],
                )

            return ErrorClassification(
                ErrorType.GIT_OPERATION_FAILED,
                ErrorSeverity.RECOVERABLE,
                True,
                True,
                ["Check git repository state", "Verify branch exists", "Retry workflow"],
            )

        # Test errors
        if phase == "test":
            if "test" in error_lower or "failed" in error_lower:
                return ErrorClassification(
                    ErrorType.TEST_FAILURE,
                    ErrorSeverity.PARTIALLY_RECOVERABLE,
                    True,
                    True,
                    [
                        "Review test failure details",
                        "Check if implementation is correct",
                        "Fix implementation and retry test phase",
                    ],
                )

            if "import" in error_lower or "module" in error_lower:
                return ErrorClassification(
                    ErrorType.MISSING_DEPENDENCIES,
                    ErrorSeverity.RECOVERABLE,
                    True,
                    True,
                    [
                        "Install missing dependencies: poetry install",
                        "Check pyproject.toml",
                        "Retry test phase",
                    ],
                )

        # Configuration errors
        if "environment" in error_lower or "env" in error_lower:
            return ErrorClassification(
                ErrorType.MISSING_ENV_VAR,
                ErrorSeverity.FATAL,
                False,
                False,
                ["Check .env file is configured", "Review .env.example for required variables", "Set missing variables"],
            )

        # Unknown error
        return ErrorClassification(
            ErrorType.UNKNOWN,
            ErrorSeverity.PARTIALLY_RECOVERABLE,
            True,
            True,
            [
                "Review error message carefully",
                "Check logs for more details",
                "Try retrying the workflow",
                "If persistent, report issue",
            ],
        )

    def should_retry(
        self, error_classification: ErrorClassification, attempt: int
    ) -> Tuple[bool, Optional[str]]:
        """Determine if a workflow should be retried.

        Args:
            error_classification: Classification of the error
            attempt: Current attempt number (1-indexed)

        Returns:
            Tuple of (should_retry, reason)
        """
        if not error_classification.retry_able:
            return False, "Error type is not retryable"

        if attempt >= self.max_retries:
            return False, f"Max retries ({self.max_retries}) exceeded"

        return True, f"Will retry (attempt {attempt + 1}/{self.max_retries})"

    def get_recovery_instructions(
        self, error_classification: ErrorClassification
    ) -> str:
        """Get human-readable recovery instructions.

        Args:
            error_classification: Classification of the error

        Returns:
            Formatted recovery instructions
        """
        lines = [
            f"Error Type: {error_classification.error_type.value}",
            f"Severity: {error_classification.severity.value}",
            f"Recoverable: {'Yes' if error_classification.recoverable else 'No'}",
            "",
            "Recovery Steps:",
        ]

        for i, step in enumerate(error_classification.recovery_steps, 1):
            lines.append(f"{i}. {step}")

        return "\n".join(lines)


# Global instance
_error_recovery_instance: Optional[ErrorRecovery] = None


def get_error_recovery(logger: Optional[logging.Logger] = None) -> ErrorRecovery:
    """Get or create the global ErrorRecovery instance."""
    global _error_recovery_instance
    if _error_recovery_instance is None:
        _error_recovery_instance = ErrorRecovery(logger)
    return _error_recovery_instance
