"""GitHub Webhook endpoint for Agentic Developer Workflow integration.

Receives GitHub issue events and triggers ADW workflows.
"""

import json
import logging
import os
import subprocess
from typing import Optional

from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter(tags=["webhooks"])

# GitHub webhook secret for signature verification
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


def verify_github_signature(request_body: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature.

    Args:
        request_body: Raw request body
        signature: X-Hub-Signature-256 header value

    Returns:
        True if signature is valid
    """
    if not WEBHOOK_SECRET:
        # If no secret configured, skip verification for development
        logger.warning("WEBHOOK_SECRET not configured, skipping signature verification")
        return True

    import hmac
    import hashlib

    # GitHub sends signature as "sha256=<hex_digest>"
    if not signature.startswith("sha256="):
        return False

    expected_signature = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        request_body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


@router.post("/gh-webhook")
async def github_webhook(request: Request) -> dict:
    """Handle GitHub webhook events.

    Supports issue creation and comments with ADW trigger commands.

    Args:
        request: FastAPI request object

    Returns:
        Acknowledgment response
    """
    try:
        # Get raw body for signature verification
        body = await request.body()

        # Verify signature if secret is configured
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not verify_github_signature(body, signature):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")

        # Parse payload
        payload = json.loads(body)
        event_type = request.headers.get("X-GitHub-Event", "")

        logger.info(f"Received webhook: event={event_type}")

        # Only handle issue events
        if event_type != "issues":
            return {"status": "ignored", "reason": "Only issue events are supported"}

        action = payload.get("action")
        issue = payload.get("issue", {})
        issue_number = issue.get("number")

        if not issue_number:
            return {"status": "error", "reason": "No issue number found"}

        logger.info(f"Issue #{issue_number} event: {action}")

        # Determine if we should trigger ADW
        should_trigger = False
        workflow_type = None

        if action == "opened":
            # Trigger on new issues (plan + build + test)
            should_trigger = True
            workflow_type = "adw_plan_build_test"
            logger.info(f"Issue #{issue_number} opened, triggering {workflow_type}")

        elif action == "synchronize" or action == "labeled":
            # Check if latest comment is "adw" or issue has "adw" label
            comments = issue.get("comments", [])
            if isinstance(comments, int):
                # GitHub API sometimes returns comment count as integer
                # Would need separate API call to get actual comments
                pass
            elif comments and isinstance(comments, list):
                latest_comment = comments[-1] if comments else None
                if latest_comment and latest_comment.get("body", "").strip() == "adw":
                    should_trigger = True
                    workflow_type = "adw_plan_build"

            # Check for adw label
            labels = issue.get("labels", [])
            label_names = [label.get("name") for label in labels] if isinstance(labels, list) else []
            if "adw" in label_names or "agentic" in label_names:
                should_trigger = True
                if not workflow_type:
                    workflow_type = "adw_plan_build"

        if not should_trigger:
            return {"status": "ignored", "reason": "No ADW trigger detected"}

        # Trigger ADW workflow in background
        try:
            trigger_adw_workflow(issue_number, workflow_type)
            logger.info(f"Triggered {workflow_type} for issue #{issue_number}")
            return {"status": "success", "workflow": workflow_type, "issue": issue_number}
        except Exception as e:
            logger.error(f"Failed to trigger workflow: {e}")
            return {"status": "error", "reason": str(e)}

    except json.JSONDecodeError:
        logger.error("Invalid JSON in webhook payload")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def trigger_adw_workflow(issue_number: int, workflow_type: str) -> None:
    """Trigger ADW workflow in background process.

    Args:
        issue_number: GitHub issue number
        workflow_type: Type of workflow to run

    Raises:
        RuntimeError: If workflow cannot be triggered
    """
    try:
        # Get ADW script path
        adw_script = get_adw_script_path(workflow_type)

        # Trigger in background
        cmd = ["uv", "run", adw_script, str(issue_number)]

        logger.info(f"Running: {' '.join(cmd)}")

        # Run in background without blocking
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=get_adws_directory(),
        )

        logger.info(f"Background workflow triggered: {workflow_type} for issue #{issue_number}")
    except Exception as e:
        logger.error(f"Failed to trigger background workflow: {e}")
        raise


def get_adw_script_path(workflow_type: str) -> str:
    """Get the path to ADW script for given workflow type.

    Args:
        workflow_type: Type of workflow

    Returns:
        Filename of ADW script

    Raises:
        ValueError: If workflow type is not recognized
    """
    script_map = {
        "adw_plan": "adw_plan.py",
        "adw_build": "adw_build.py",
        "adw_test": "adw_test.py",
        "adw_plan_build": "adw_plan_build.py",
        "adw_plan_build_test": "adw_plan_build_test.py",
    }

    if workflow_type not in script_map:
        raise ValueError(f"Unknown workflow type: {workflow_type}")

    return script_map[workflow_type]


def get_adws_directory() -> str:
    """Get the path to adws directory.

    Returns:
        Absolute path to adws directory
    """
    import pathlib

    # This file is at stratslabapi/routers/webhooks.py
    # We need to go up to project root, then into adws/
    project_root = pathlib.Path(__file__).parent.parent.parent
    return str(project_root / "adws")


@router.get("/webhook/status")
async def webhook_status() -> dict:
    """Check webhook status and configuration.

    Returns:
        Webhook configuration status
    """
    return {
        "status": "ready",
        "webhook_secret_configured": bool(WEBHOOK_SECRET),
        "adws_directory": get_adws_directory(),
    }
