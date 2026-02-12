# ADW - Agentic Developer Workflow

Run the full agentic developer workflow to automatically plan, implement, test, and create a PR for a GitHub issue.

## Instructions

Run the full ADW pipeline to automatically solve a GitHub issue:

```bash
./scripts/run_adw.sh <issue-number> [workflow-type]
```

Where:
- `<issue-number>` - GitHub issue number to process (required)
- `[workflow-type]` - Type of workflow to run (optional, default: plan-build)

## Workflow Types

- **plan** - Planning phase only (generates implementation plan)
- **build** - Building phase only (requires existing plan)
- **test** - Testing phase only (validates implementation)
- **plan-build** - Plan + Build (default)
- **plan-build-test** - Plan + Build + Test (full pipeline)

## Examples

```bash
# Full workflow (plan + build + test)
./scripts/run_adw.sh 42

# Just planning
./scripts/run_adw.sh 42 plan

# Plan and build (create PR but don't test)
./scripts/run_adw.sh 42 plan-build

# Full pipeline with testing
./scripts/run_adw.sh 42 plan-build-test
```

## Environment Setup

First time setup:

```bash
./scripts/setup_adw.sh
```

Then configure your `.env` file with:
- `GITHUB_REPO_URL` - Your GitHub repository URL
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `CLAUDE_CODE_PATH` - Path to Claude Code CLI (usually "claude")

## How It Works

The ADW workflow:

1. **Plan** - AI analyzes the issue and creates an implementation plan
2. **Build** - AI executes the plan, making code changes
3. **Test** - Runs tests to validate the implementation
4. **Integrate** - Creates git commits and pull request

Each phase can be run independently or chained together.

## Monitoring

Check workflow status via API:

```bash
curl http://localhost:8000/api/workflows/
curl http://localhost:8000/api/workflows/{adw_id}
curl http://localhost:8000/api/workflows/{adw_id}/logs
```

Or check GitHub issue comments for status updates.

## Troubleshooting

If a workflow fails:

1. Check GitHub issue comments for error details
2. Review logs: `/adws/logs/<adw_id>/`
3. Retry the failed phase: `./scripts/run_adw.sh <issue> <phase>`

## Requirements

- GitHub CLI (`gh`) - Installed and authenticated
- Claude Code CLI - Installed
- uv package manager - For running Python scripts
- Anthropic API key - For accessing Claude API
- GitHub repository URL - Set in `.env`

## Advanced Usage

### Using Different Models

By default, workflows use the Sonnet model (fast, lower cost). To use a more capable model:

```bash
export ADW_MODEL=opus
./scripts/run_adw.sh 42
```

### Enabling Debug Logging

For detailed debug output:

```bash
export ADW_DEBUG=true
./scripts/run_adw.sh 42
```

### Manual Workflow Phases

Run individual phases manually:

```bash
cd adws/
uv run adw_plan.py 42                    # Planning only
uv run adw_plan.py 42 | uv run adw_build.py  # Chain plan and build
```

## API Integration

Trigger workflows via REST API:

```bash
# Trigger workflow
curl -X POST http://localhost:8000/api/workflows/trigger \
  -H "Content-Type: application/json" \
  -d '{"issue_number": 42, "workflow": "adw_plan_build_test"}'

# Get status
curl http://localhost:8000/api/workflows/{adw_id}

# Retry failed workflow
curl -X POST http://localhost:8000/api/workflows/{adw_id}/retry
```

## Learn More

- See `adws/README.md` for detailed ADW documentation
- See `docs/AGENTIC_WORKFLOW.md` for architecture and design decisions
- See `.env.example` for all available configuration options
