#!/bin/bash

# Helper script to run ADW workflows
# Usage: ./scripts/run_adw.sh <issue-number> [workflow-type]

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADW_DIR="$SCRIPT_DIR/adws"

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <issue-number> [workflow-type]"
    echo ""
    echo "Workflow types:"
    echo "  plan            - Planning phase only"
    echo "  build           - Building phase only"
    echo "  test            - Testing phase only"
    echo "  plan-build      - Plan + Build (default)"
    echo "  plan-build-test - Plan + Build + Test"
    exit 1
fi

ISSUE_NUMBER=$1
WORKFLOW_TYPE=${2:-plan-build}

# Map workflow type to script
case $WORKFLOW_TYPE in
    plan)
        SCRIPT="adw_plan.py"
        ;;
    build)
        SCRIPT="adw_build.py"
        ;;
    test)
        SCRIPT="adw_test.py"
        ;;
    plan-build)
        SCRIPT="adw_plan_build.py"
        ;;
    plan-build-test)
        SCRIPT="adw_plan_build_test.py"
        ;;
    *)
        echo "Unknown workflow type: $WORKFLOW_TYPE"
        echo "Supported types: plan, build, test, plan-build, plan-build-test"
        exit 1
        ;;
esac

# Check if in adws directory
if [ ! -f "$ADW_DIR/$SCRIPT" ]; then
    echo "Error: ADW script not found at $ADW_DIR/$SCRIPT"
    echo "Current directory: $(pwd)"
    echo "Script directory: $SCRIPT_DIR"
    exit 1
fi

# Load environment
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Loading environment from .env..."
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
else
    echo "Warning: .env file not found at $SCRIPT_DIR/.env"
fi

# Verify required environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY not set"
    echo "Please configure it in .env or set it as an environment variable"
    exit 1
fi

if [ -z "$GITHUB_REPO_URL" ]; then
    echo "Error: GITHUB_REPO_URL not set"
    echo "Please configure it in .env or set it as an environment variable"
    exit 1
fi

echo "========================================="
echo "ADW Workflow Runner"
echo "========================================="
echo "Issue Number: $ISSUE_NUMBER"
echo "Workflow Type: $WORKFLOW_TYPE"
echo "Script: $SCRIPT"
echo "ADW Directory: $ADW_DIR"
echo ""

# Run the workflow
cd "$ADW_DIR"
echo "Running: uv run $SCRIPT $ISSUE_NUMBER"
echo ""

uv run "$SCRIPT" "$ISSUE_NUMBER"

RESULT=$?

echo ""
echo "========================================="
if [ $RESULT -eq 0 ]; then
    echo "✅ Workflow completed successfully"
else
    echo "❌ Workflow failed with exit code $RESULT"
fi
echo "========================================="

exit $RESULT
