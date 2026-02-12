# Agentic Developer Workflow (ADW) - Complete Guide

## Overview

The Agentic Developer Workflow (ADW) is a complete automation system that transforms GitHub issues into implemented, tested, and merged pull requests through AI agents. The system integrates with the Claude Code CLI to automatically plan, implement, test, and integrate software changes.

## Architecture

```
GitHub Issue Event
    ↓
Webhook/API Trigger
    ↓
ADW Pipeline
├── Phase 1: Planning
│   └── AI agent generates implementation plan
├── Phase 2: Implementation
│   └── AI agent creates code changes
├── Phase 3: Testing
│   └── Runs test suite validation
└── Phase 4: Integration
    └── Creates git commits and PR
    ↓
Database Audit Trail
↓
GitHub PR + Comments
```

## Core Components

### 1. REST API Endpoints

```
POST   /api/workflows/trigger           - Start a new workflow
GET    /api/workflows/{adw_id}          - Get workflow status
GET    /api/workflows                   - List all workflows (with filters)
POST   /api/workflows/{adw_id}/retry    - Retry failed workflow
GET    /api/workflows/{adw_id}/logs     - Get execution logs
```

### 2. GitHub Webhook

```
POST   /gh-webhook                      - Receive GitHub issue events
GET    /webhook/status                  - Check webhook configuration
```

### 3. Database Models

- **WorkflowRun** - Main workflow execution record
- **WorkflowPhaseRun** - Individual phase execution tracking
- **WorkflowLog** - Detailed execution logs

### 4. ADW Modules

- `adw_plan.py` - Planning phase entry point
- `adw_build.py` - Implementation phase entry point
- `adw_test.py` - Testing phase entry point
- `adw_plan_build.py` - Plan + Build combined
- `adw_plan_build_test.py` - Full pipeline
- `adws/adw_modules/` - Core modules for operations
- `adws/adw_triggers/` - Webhook and cron triggers

### 5. API Integration

- **api_integration.py** - Database persistence layer
- **database_ops.py** - Synchronous database operations
- **error_recovery.py** - Error classification and recovery logic

## Running Workflows

### Via Helper Script

```bash
# Full pipeline (plan + build + test)
./scripts/run_adw.sh 42

# Plan only
./scripts/run_adw.sh 42 plan

# Plan and build
./scripts/run_adw.sh 42 plan-build

# Full pipeline with testing
./scripts/run_adw.sh 42 plan-build-test
```

### Via Claude Command

```bash
/adw <issue-number>
```

### Via REST API

```bash
curl -X POST http://localhost:8000/api/workflows/trigger \
  -H "Content-Type: application/json" \
  -d '{"issue_number": 42, "workflow": "adw_plan_build_test"}'
```

### Via GitHub

1. Create an issue on GitHub
2. Webhook automatically triggers ADW workflow
3. Check issue comments for status updates

## Environment Configuration

Required environment variables in `.env`:

```bash
# GitHub Configuration
GITHUB_REPO_URL=https://github.com/owner/repository
GITHUB_PAT=ghp_xxxx...  # Optional, for different account

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_CODE_PATH=claude  # or full path

# Database (optional, for workflow tracking)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db

# ADW Configuration
ADW_DEBUG=false          # Enable debug logging
ADW_TIMEOUT=1800         # Timeout in seconds
ADW_MODEL=sonnet         # Model to use (sonnet or opus)
WEBHOOK_SECRET=...       # GitHub webhook secret
WEBHOOK_PORT=8001        # Webhook server port
```

## Database Setup

Run migrations to create workflow tables:

```bash
poetry run alembic upgrade head
```

This creates:
- `workflow_runs` - Workflow execution records
- `workflow_phase_runs` - Phase execution tracking
- `workflow_logs` - Detailed execution logs

## API Examples

### Trigger a Workflow

```bash
curl -X POST http://localhost:8000/api/workflows/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "issue_number": 42,
    "workflow": "adw_plan_build_test"
  }'

# Response:
{
  "adw_id": "a1b2c3d4",
  "status": "pending",
  "issue_number": 42,
  "workflow_type": "adw_plan_build_test",
  "created_at": "2026-02-12T10:30:00Z",
  ...
}
```

### Get Workflow Status

```bash
curl http://localhost:8000/api/workflows/a1b2c3d4

# Response:
{
  "adw_id": "a1b2c3d4",
  "status": "completed",
  "phases": [
    {
      "phase": "plan",
      "status": "completed",
      "started_at": "2026-02-12T10:30:05Z",
      "completed_at": "2026-02-12T10:35:10Z"
    },
    {
      "phase": "build",
      "status": "completed",
      "started_at": "2026-02-12T10:35:15Z",
      "completed_at": "2026-02-12T10:40:20Z"
    },
    ...
  ],
  "pull_request_url": "https://github.com/owner/repo/pull/123",
  ...
}
```

### List Workflows

```bash
curl "http://localhost:8000/api/workflows?status=completed&limit=10"

# Response:
{
  "items": [...],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

### Get Workflow Logs

```bash
curl http://localhost:8000/api/workflows/a1b2c3d4/logs

# Response:
{
  "logs": [
    "[2026-02-12T10:30:00Z] [INFO] Starting planning phase",
    "[2026-02-12T10:30:05Z] [DEBUG] Fetching issue details",
    ...
  ],
  "total_lines": 125
}
```

### Retry Failed Workflow

```bash
curl -X POST http://localhost:8000/api/workflows/a1b2c3d4/retry \
  -H "Content-Type: application/json" \
  -d '{"phase": "test"}'  # Optional: retry specific phase
```

## Workflow Execution Flow

### 1. Planning Phase

- Fetch issue from GitHub
- Classify issue type (feature/bug/chore)
- Generate implementation plan using AI
- Commit plan to feature branch
- Create/update PR with plan

### 2. Implementation Phase

- Load existing plan
- Implement changes based on plan
- Create code commits
- Update PR with implementation

### 3. Testing Phase

- Run test suite
- Report test results
- Update PR with test status
- Create final commit with test results

### 4. Integration Phase

- Squash/organize commits
- Push to remote
- Finalize PR
- Update issue comments

## Monitoring & Troubleshooting

### Check Webhook Status

```bash
curl http://localhost:8000/webhook/status
```

### View Workflow Logs

```bash
# Via API
curl http://localhost:8000/api/workflows/{adw_id}/logs

# Via files
cat agents/{adw_id}/*/raw_output.jsonl
```

### Debug Failed Workflow

1. Check GitHub issue comments for error details
2. Get logs via API: `/api/workflows/{adw_id}/logs`
3. Review error phase and message
4. Fix issue and retry: `POST /api/workflows/{adw_id}/retry`

### Common Issues

**"Claude Code CLI not found"**
- Install from: https://docs.anthropic.com/en/docs/claude-code
- Set CLAUDE_CODE_PATH if not in PATH

**"GitHub authentication failed"**
- Run: `gh auth login`
- Or set GITHUB_PAT in .env

**"Timeout during workflow"**
- Increase ADW_TIMEOUT environment variable
- Check if Claude Code CLI is responsive
- Try simpler issue

**"Test failures"**
- Review test output in PR comments
- Fix implementation or tests manually
- Retry test phase

## Architecture Decisions

### Modular Phases

Each phase (plan, build, test) can run independently or chained. This enables:
- Recovery from failures at specific phases
- Testing individual components
- Flexible workflow customization

### Dual State Storage

- **File-based**: Working state during workflow execution
- **Database**: Persistent audit trail for monitoring

This combination provides:
- Fast local execution
- Long-term auditability
- Query capability for monitoring

### Subprocess-Based Execution

ADW runs Claude Code CLI via subprocess instead of direct API calls. Benefits:
- Uses proven Claude Code agent infrastructure
- Avoids reimplementing agent logic
- Maintains compatibility with future updates

### Background Execution

Webhook triggers run ADW in background processes:
- Responds immediately to GitHub (no timeout issues)
- Prevents blocking API requests
- Allows concurrent workflow execution

## Security Considerations

### GitHub Webhook Verification

- Signature verification using HMAC-SHA256
- Configurable webhook secret
- Request filtering by event type

### Environment Variables

- API keys never committed to git
- Stored in .env file (add to .gitignore)
- Can be set as environment variables

### Database Security

- All workflow data persisted to database
- Audit trail of all executions
- Read-only API keys for monitoring

### Execution Isolation

- Each workflow runs in subprocess
- Environment variables passed explicitly
- Claude Code permissions apply

## Performance Characteristics

- **Planning Phase**: 2-5 minutes (depends on issue complexity)
- **Implementation Phase**: 3-10 minutes (depends on code changes)
- **Testing Phase**: 1-5 minutes (depends on test suite size)
- **Total Pipeline**: 6-20 minutes for typical issue

Database query performance:
- Workflow status queries: <100ms
- Workflow list queries: <500ms
- Log retrieval: <1s for 1000 entries

## Future Enhancements

1. **Web Dashboard** - UI for monitoring and triggering workflows
2. **Slack Integration** - Workflow status notifications
3. **Advanced Routing** - Route issues based on labels/assignees
4. **Approval Workflows** - Human review checkpoints
5. **Custom Workflows** - User-defined workflow chains
6. **Cost Tracking** - Monitor API usage and costs
7. **Performance Analytics** - Track success rates and timings

## Support & Troubleshooting

For issues or questions:

1. Check logs: `/adws/logs/{adw_id}/`
2. Review GitHub issue comments for error details
3. Check database logs: `workflow_logs` table
4. Enable debug mode: `export ADW_DEBUG=true`
5. Review plan in `specs/issue-{number}-*.md`

## Learning Resources

- `adws/README.md` - ADW system documentation
- `specs/features/full-agentic-workflow.md` - Detailed feature specification
- `script/run_adw.sh` - Example workflow execution
- `.claude/commands/adw.md` - Claude command documentation
