# Feature: Full Agentic Workflow Integration

## Metadata
- **Type**: Feature
- **Status**: Planning
- **Created**: 2026-02-12
- **Agent**: Feature Planning
- **Priority**: High
- **Scope**: Complete agentic automation for GitHub-to-API code generation

## Feature Description

Implement a complete **Agentic Developer Workflow (ADW)** system that automates software development by integrating GitHub issues with the Claude Code CLI. The system will classify issues, generate implementation plans, execute code changes, run tests, and create pull requests entirely through AI agents. This transforms StratsLab into a platform that can autonomously develop features, fix bugs, and maintain itself with minimal human intervention.

The system consists of:
1. **Issue Classification**: Automatically categorize GitHub issues (feature/bug/chore)
2. **Planning Phase**: AI agent generates detailed implementation plans
3. **Implementation Phase**: AI agent executes the plan and creates code
4. **Testing Phase**: Automated test execution and validation
5. **Integration Phase**: Creates git commits and pull requests
6. **API Integration**: REST API endpoints to trigger workflows and track status
7. **Monitoring & Triggers**: Webhook and cron-based automation
8. **Persistence Layer**: Database models to track workflow runs and audit trail

## User Story

As a **development team**
I want to **have GitHub issues automatically implemented by AI agents**
So that **I can focus on strategy and code review while agents handle routine development tasks**

## Problem Statement

Manual software development involves repetitive tasks:
- Manual issue analysis and planning
- Manual code implementation
- Manual testing and validation
- Manual git operations and PR creation

This is time-consuming, error-prone, and limits productivity. Automating the entire workflow from issue to merged PR would significantly accelerate development while maintaining quality through automated testing.

## Solution Statement

Implement a complete agentic workflow system that:
1. **Listens** to GitHub issues (via webhooks or polling)
2. **Classifies** issues to determine type (feature/bug/chore)
3. **Plans** implementation using AI agents with access to codebase
4. **Implements** changes automatically with validated code
5. **Tests** implementations to ensure quality
6. **Integrates** changes via git commits and PRs
7. **Tracks** workflow runs in database for audit and monitoring
8. **Exposes** REST API for programmatic workflow triggers and status queries
9. **Recovers** from failures with detailed error reporting

## Acceptance Criteria

- ✅ ADW system perfectly adapted for StratsLab project structure
- ✅ All existing ADW components (plan, build, test, triggers) working correctly
- ✅ New REST API endpoints for triggering and monitoring workflows
- ✅ Database models to track workflow runs and state
- ✅ Webhook endpoint integrated with FastAPI application
- ✅ GitHub integration working (issue creation, comments, PRs)
- ✅ Complete state persistence and recovery mechanisms
- ✅ Comprehensive logging and error reporting
- ✅ Unit tests for all core workflow operations
- ✅ Integration tests for full pipeline workflows
- ✅ End-to-end test with real GitHub issue
- ✅ All existing tests pass without regression
- ✅ Documentation for running workflows manually and automatically

## Relevant Files

### Core ADW System (Already in place, needs refinement)
- `adws/` - Root directory for agentic developer workflow system
- `adws/adw_plan.py` - Planning phase entry point
- `adws/adw_build.py` - Implementation phase entry point
- `adws/adw_test.py` - Testing phase entry point
- `adws/adw_plan_build.py` - Combined plan + build workflow
- `adws/adw_plan_build_test.py` - Full pipeline (plan + build + test)
- `adws/adw_modules/` - Core modules for workflow operations
- `adws/adw_triggers/` - Webhook and cron triggers

### New Integration Points
- `stratslabapi/routers/workflows.py` - REST API endpoints for ADW workflows
- `stratslabapi/repositories/workflow_models.py` - Database models for workflow tracking
- `stratslabapi/schemas/workflows.py` - Pydantic schemas for workflow API
- `stratslabapi/web_servers/asgi.py` - Integrate webhook endpoint into main app
- `tests/test_workflows.py` - Workflow integration tests

### Configuration & Scripts
- `.env.example` - Add ADW-specific environment variables
- `scripts/run_adw.sh` - Helper script to run ADW workflows
- `scripts/setup_adw.sh` - Setup ADW environment and dependencies

### Documentation
- `adws/README.md` - Already exists, may need updates
- `docs/AGENTIC_WORKFLOW.md` - Complete workflow documentation

### New Files
- `adws/adw_modules/api_integration.py` - Integration with FastAPI
- `adws/adw_modules/database_ops.py` - Database operations for workflow tracking
- `adws/adw_modules/error_recovery.py` - Error handling and recovery
- `.claude/commands/adw.md` - Claude Code command for running workflows

## Design Decisions

### Alternatives Considered

1. **External ADW Service vs Integrated System**
   - **Rejected**: External service would add operational complexity
   - **Selected**: Integrate into project, simpler deployment and state management

2. **Webhook Only vs Webhook + Cron**
   - **Rejected**: Webhook only misses issues without events
   - **Selected**: Both webhooks (instant) and cron (backup/polling)

3. **Synchronous vs Asynchronous Workflow**
   - **Rejected**: Synchronous blocks API responses
   - **Selected**: Asynchronous with background task execution via subprocess

4. **State Storage (File-based vs Database)**
   - **Rejected**: File-based only limits scalability and auditability
   - **Selected**: Primary database storage with file-based caching for working state

5. **Claude Code CLI vs Direct API**
   - **Rejected**: Direct API requires reimplementing agent logic
   - **Selected**: Claude Code CLI via subprocess, uses proven agent system

### Selected Approach

**Distributed Workflow System with Multiple Entry Points**:
- Multiple trigger mechanisms (webhook, cron, API)
- Modular phases (plan, build, test) callable independently or chained
- Persistent state tracking in database
- File-based working state for chaining workflows
- REST API for programmatic access and monitoring
- Comprehensive error handling and recovery

### Key Architectural Decisions

1. **Modular Phase Architecture**: Each phase (plan/build/test) can run independently or be chained, allowing flexibility and recovery
2. **State Management**: Dual storage (database for persistence, files for working state) enables recovery and auditability
3. **GitHub Integration**: Direct gh CLI integration avoids auth complexity
4. **Claude Code CLI Integration**: Uses existing Claude Code infrastructure rather than reimplementing
5. **Asynchronous Execution**: Background task execution prevents blocking API requests
6. **Database Audit Trail**: All workflow executions tracked for monitoring, debugging, and compliance
7. **Error Recovery**: Detailed state preservation enables retry and manual intervention points

## API Contracts & Data Models

### New REST Endpoints

```
POST /api/workflows/trigger
  - Trigger a workflow manually
  - Body: { issue_number: int, workflow: "adw_plan" | "adw_build" | "adw_test" | "adw_plan_build" | "adw_plan_build_test" }
  - Response: { adw_id: str, status: str, created_at: datetime }

GET /api/workflows/{adw_id}
  - Get workflow status and details
  - Response: { adw_id: str, status: str, issue_number: int, workflow_type: str, phases: [...], errors: [...], created_at, started_at, completed_at }

GET /api/workflows?status=running&limit=10
  - List workflows with filtering
  - Response: { items: [...], total: int, page: int }

POST /api/workflows/{adw_id}/retry
  - Retry failed workflow or phase
  - Body: { phase?: "plan" | "build" | "test" }
  - Response: { adw_id: str, status: str }

GET /api/workflows/{adw_id}/logs
  - Get workflow execution logs
  - Response: { logs: string[] }
```

### Database Models

```python
# WorkflowRun - Track each ADW execution
class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: UUID = Column(UUID, primary_key=True)
    adw_id: str = Column(String(8), unique=True, index=True)
    issue_number: int = Column(Integer, index=True)
    workflow_type: str = Column(String(50))  # plan, build, test, plan_build, plan_build_test
    status: str = Column(String(20))  # pending, running, completed, failed

    # Execution details
    branch_name: Optional[str]
    plan_file: Optional[str]

    # Tracking
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    # Error tracking
    error_message: Optional[str]
    error_phase: Optional[str]  # Which phase failed

    # Results
    pull_request_url: Optional[str]
    implementation_summary: Optional[str]

# WorkflowPhaseRun - Track individual phase executions
class WorkflowPhaseRun(Base):
    __tablename__ = "workflow_phase_runs"

    id: UUID
    workflow_run_id: UUID = ForeignKey(WorkflowRun.id)
    phase: str = Column(String(20))  # plan, build, test
    status: str = Column(String(20))

    started_at: datetime
    completed_at: Optional[datetime]

    output_file: Optional[str]
    error_message: Optional[str]

# WorkflowLog - Detailed execution logs
class WorkflowLog(Base):
    __tablename__ = "workflow_logs"

    id: UUID
    workflow_run_id: UUID = ForeignKey(WorkflowRun.id)
    timestamp: datetime
    level: str  # DEBUG, INFO, WARNING, ERROR
    message: str
    context: Optional[dict]
```

### Pydantic Schemas

```python
class WorkflowTriggerRequest(BaseModel):
    issue_number: int
    workflow: Literal["adw_plan", "adw_build", "adw_test", "adw_plan_build", "adw_plan_build_test"]

class WorkflowPhaseStatus(BaseModel):
    phase: str
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error: Optional[str]

class WorkflowRunResponse(BaseModel):
    adw_id: str
    issue_number: int
    workflow_type: str
    status: str
    phases: List[WorkflowPhaseStatus]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    pull_request_url: Optional[str]
    errors: List[str]

class WorkflowListResponse(BaseModel):
    items: List[WorkflowRunResponse]
    total: int
    page: int
    page_size: int
```

## Dependencies & Blockers

### External Dependencies
- **Existing**: Claude Code CLI (required)
- **Existing**: GitHub CLI (required)
- **Existing**: Python 3.12+ with Poetry
- **Existing**: PostgreSQL (for database)
- **New**: `python-dotenv` (already in adws, may add to main project)
- **New**: `uvicorn` (for webhook server, may be integrated into main app)

### Internal Dependencies
- ✅ FastAPI application structure (already exists)
- ✅ SQLAlchemy models and repositories (already exists)
- ✅ Pydantic schemas (already exists)
- ✅ PostgreSQL database (already exists)
- ✅ Authentication system (already exists)

### Blockers
- None identified - all required infrastructure exists

## Implementation Plan

### Phase 1: Foundation & Adaptation
Ensure ADW system is perfectly adapted for StratsLab architecture:
- Review and validate all ADW modules for StratsLab compatibility
- Set up ADW environment variables in project configuration
- Create database models for workflow tracking and persistence
- Implement state persistence layer (database integration)

### Phase 2: Core Integration
Integrate ADW into main FastAPI application:
- Create REST API endpoints for workflow management
- Implement webhook endpoint in FastAPI
- Add async task queue for background workflow execution
- Create database operations module
- Implement error recovery and logging

### Phase 3: Enhancement & Safety
Add production-ready features:
- Comprehensive error handling and recovery mechanisms
- Detailed logging and audit trail
- State validation and consistency checks
- Rate limiting for workflow triggers
- User authentication and authorization for API endpoints

### Phase 4: Testing & Validation
Ensure quality and reliability:
- Unit tests for all workflow components
- Integration tests for full pipeline
- End-to-end tests with real GitHub interaction
- Performance and load testing
- Security validation

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom. Each step builds on previous ones.

### Step 1: Validate and Adapt ADW Core
- [ ] Review all ADW modules for project-specific adaptations needed
- [ ] Verify environment variables are properly documented
- [ ] Test each ADW script independently (plan, build, test)
- [ ] Ensure all dependencies are compatible with project Python version
- [ ] Create/update .env.example with ADW-specific variables
- [ ] Test chaining workflows (plan | build, plan | build | test)

### Step 2: Create Database Models
- [ ] Create `stratslabapi/repositories/workflow_models.py` with WorkflowRun model
- [ ] Create WorkflowPhaseRun model for phase-level tracking
- [ ] Create WorkflowLog model for detailed execution logs
- [ ] Add database migration for new tables using Alembic
- [ ] Create repository class for workflow operations
- [ ] Write unit tests for model creation and queries

### Step 3: Create Pydantic Schemas
- [ ] Create `stratslabapi/schemas/workflows.py`
- [ ] Implement WorkflowTriggerRequest schema
- [ ] Implement WorkflowRunResponse schema
- [ ] Implement WorkflowListResponse schema
- [ ] Implement WorkflowPhaseStatus schema
- [ ] Write validation tests for schemas

### Step 4: Create API Integration Module
- [ ] Create `adws/adw_modules/api_integration.py`
- [ ] Implement workflow trigger function
- [ ] Implement status query function
- [ ] Implement workflow logging function
- [ ] Add error reporting to API
- [ ] Write unit tests

### Step 5: Create Database Operations Module
- [ ] Create `adws/adw_modules/database_ops.py`
- [ ] Implement workflow persistence functions
- [ ] Implement phase tracking functions
- [ ] Implement log insertion functions
- [ ] Add database connection management
- [ ] Write unit tests

### Step 6: Create Error Recovery Module
- [ ] Create `adws/adw_modules/error_recovery.py`
- [ ] Implement error classification logic
- [ ] Implement retry mechanisms
- [ ] Implement state recovery procedures
- [ ] Add error reporting and notifications
- [ ] Write unit tests

### Step 7: Create REST API Endpoints
- [ ] Create `stratslabapi/routers/workflows.py`
- [ ] Implement POST /api/workflows/trigger endpoint
- [ ] Implement GET /api/workflows/{adw_id} endpoint
- [ ] Implement GET /api/workflows endpoint (with filtering/pagination)
- [ ] Implement POST /api/workflows/{adw_id}/retry endpoint
- [ ] Implement GET /api/workflows/{adw_id}/logs endpoint
- [ ] Add request validation and error handling
- [ ] Add authentication/authorization checks
- [ ] Write integration tests for each endpoint

### Step 8: Integrate Webhook into FastAPI
- [ ] Create separate webhook handler in `stratslabapi/routers/webhooks.py`
- [ ] Move webhook logic from trigger_webhook.py to router
- [ ] Integrate into main FastAPI application
- [ ] Add webhook verification (GitHub signature validation)
- [ ] Implement async background task execution
- [ ] Add webhook event filtering and routing
- [ ] Write integration tests

### Step 9: Implement Async Task Execution
- [ ] Set up background task queue (using APScheduler or Celery)
- [ ] Implement async workflow trigger function
- [ ] Add task progress tracking
- [ ] Implement task timeout and retry logic
- [ ] Add worker monitoring
- [ ] Write integration tests

### Step 10: Update Main FastAPI Application
- [ ] Import new workflow routers in `stratslabapi/apps/fastapi.py`
- [ ] Register workflow endpoints
- [ ] Register webhook endpoint
- [ ] Add database migrations to startup
- [ ] Add workflow background task startup
- [ ] Test full application startup

### Step 11: Create Helper Scripts
- [ ] Create `scripts/run_adw.sh` for manual workflow execution
- [ ] Create `scripts/setup_adw.sh` for ADW environment setup
- [ ] Create `scripts/test_adw_workflow.sh` for end-to-end testing
- [ ] Make scripts executable and documented

### Step 12: Add ADW Claude Command
- [ ] Create `.claude/commands/adw.md` for easy workflow triggering
- [ ] Document command usage and examples
- [ ] Test command integration with Claude Code

### Step 13: Comprehensive Testing
- [ ] Write unit tests for all new modules
- [ ] Write integration tests for workflow chain
- [ ] Write end-to-end test (GitHub issue → PR)
- [ ] Test error scenarios and recovery
- [ ] Test rate limiting and throttling
- [ ] Test concurrent workflow execution
- [ ] Verify all existing tests still pass

### Step 14: Documentation
- [ ] Create `docs/AGENTIC_WORKFLOW.md` with complete guide
- [ ] Document API endpoints with examples
- [ ] Document database schema
- [ ] Document error codes and recovery procedures
- [ ] Update main README.md with ADW section
- [ ] Create troubleshooting guide

### Step 15: Validation & Cleanup
- [ ] Run full test suite with zero failures
- [ ] Validate all API endpoints manually
- [ ] Test complete workflow end-to-end
- [ ] Check code quality and coverage
- [ ] Clean up debug code and logging
- [ ] Final documentation review

## Testing Strategy

### Unit Tests

**Workflow Operations** (`tests/test_workflow_operations.py`)
- Test each workflow operation function independently
- Test state creation and persistence
- Test git operations (branch creation, commits)
- Test GitHub API interactions
- Test issue classification logic

**Database Operations** (`tests/test_workflow_database.py`)
- Test WorkflowRun creation and updates
- Test WorkflowPhaseRun tracking
- Test WorkflowLog insertion and retrieval
- Test query filtering and pagination
- Test error handling and rollback

**Error Recovery** (`tests/test_error_recovery.py`)
- Test error classification
- Test retry logic
- Test state recovery
- Test partial failure scenarios

**API Integration** (`tests/test_workflow_api.py`)
- Test trigger function
- Test status query
- Test logging
- Test error reporting

### Integration Tests

**Workflow Chaining** (`tests/test_workflow_chaining.py`)
- Test plan → build → test pipeline
- Test state passing between phases
- Test failure handling across phases
- Test recovery from mid-phase failures

**API Endpoints** (`tests/test_workflow_endpoints.py`)
- Test workflow trigger endpoint
- Test status query endpoint
- Test workflow list endpoint with filters
- Test retry endpoint
- Test authentication and authorization
- Test rate limiting

**GitHub Integration** (`tests/test_github_integration.py`)
- Test issue comment creation
- Test PR creation
- Test branch management
- Test webhook event handling

**Database Integration** (`tests/test_workflow_persistence.py`)
- Test full workflow persistence
- Test log retrieval
- Test filtering and searching

### End-to-End Tests

**Complete Workflow** (`tests/test_e2e_workflow.py`)
- Create test GitHub issue
- Run full ADW pipeline (plan → build → test)
- Verify PR created and comments added
- Clean up test issue

**Error Recovery** (`tests/test_e2e_recovery.py`)
- Simulate failure in build phase
- Test retry mechanism
- Verify workflow completes successfully

### Edge Cases

- **No changes needed** - Issue already resolved
- **Merge conflicts** - Branch conflicts with main
- **Test failures** - Implementation breaks existing tests
- **API timeouts** - Claude Code CLI timeout
- **GitHub rate limits** - Too many API calls
- **Concurrent workflows** - Multiple ADW runs for same issue
- **Invalid issue format** - Malformed issue content
- **Missing environment variables** - Incomplete configuration
- **Database connection failures** - Database unavailable during execution
- **Webhook signature validation** - Invalid webhook requests

## Security & Performance Considerations

### Security

**Threat Model**
- Malicious issue content could inject commands
- GitHub webhook could be spoofed
- State files could contain sensitive data
- Database could be accessed by unauthorized users

**Mitigations**
- Validate all GitHub issue content before processing
- Verify GitHub webhook signatures using X-Hub-Signature
- Encrypt sensitive data in state files
- Use database authentication and row-level security
- Implement API authentication (JWT tokens)
- Run workflows in isolated subprocess environment
- Limit Claude Code CLI permissions via environment
- Audit all workflow executions in database
- Set up rate limiting on API endpoints
- Use fine-grained GitHub tokens with minimal scopes

**Compliance**
- Log all workflow executions for audit trail
- Implement data retention policies
- Support workflow cancellation for user control
- Track who triggered workflows (if API authenticated)

### Performance

**Scalability**
- Use async task queue for parallel workflow execution
- Implement result caching for frequently run workflows
- Add database indexes on commonly filtered columns
- Paginate API list responses
- Set reasonable timeouts for Claude Code execution

**Optimization**
- Cache compiled codebase analysis between phases
- Parallelize independent workflow triggers
- Use connection pooling for database
- Implement incremental testing (run only affected tests)
- Cache GitHub API responses where possible

**Monitoring**
- Track workflow execution time by phase
- Monitor success/failure rates
- Alert on high failure rates
- Track API response times
- Monitor background task queue depth

## Migration Strategy

### Initial Deployment

1. **Deploy database schema** (migration step)
2. **Deploy API endpoints** (backward compatible)
3. **Enable webhook** (in project settings)
4. **Enable cron trigger** (or manual testing)
5. **Monitor workflow execution** (in logs and database)

### Rollback Plan

If issues occur:
1. **Stop webhook** - Disable in GitHub settings
2. **Stop cron** - Terminate trigger process
3. **Disable API** - Comment out router registration
4. **Keep database** - Preserve audit trail
5. **Revert code** - Checkout previous version
6. **Manual recovery** - Use git to fix issues if needed

### Data Migration

No data migration needed - new tables are additive and don't affect existing schema.

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

```bash
# 1. Run full test suite (all existing tests must pass)
poetry run pytest tests/ -v --tb=short

# 2. Run workflow-specific tests
poetry run pytest tests/test_workflow_operations.py -v
poetry run pytest tests/test_workflow_database.py -v
poetry run pytest tests/test_workflow_endpoints.py -v

# 3. Start API server and test endpoints manually
poetry run uvicorn stratslabapi.web_servers.asgi:app --reload &
sleep 2

# 4. Test workflow trigger endpoint
curl -X POST http://localhost:8000/api/workflows/trigger \
  -H "Content-Type: application/json" \
  -d '{"issue_number": 999, "workflow": "adw_plan"}'

# 5. Test workflow status endpoint (replace {adw_id} with actual ID)
curl http://localhost:8000/api/workflows/{adw_id}

# 6. Test workflow list endpoint
curl "http://localhost:8000/api/workflows?status=running&limit=10"

# 7. Manual end-to-end workflow test
cd adws/
export GITHUB_REPO_URL="<your-repo-url>"
export ANTHROPIC_API_KEY="<your-key>"
# Create a test issue on GitHub, then:
uv run adw_plan_build_test.py <issue-number>

# 8. Test webhook endpoint (create test webhook server)
python -m pytest tests/test_workflow_endpoints.py::test_webhook -v

# 9. Code quality checks
poetry run black stratslabapi/ tests/ adws/ --check
poetry run isort stratslabapi/ tests/ adws/ --check
poetry run mypy stratslabapi/ adws/ --ignore-missing-imports

# 10. Coverage check
poetry run pytest tests/ --cov=stratslabapi --cov=adws --cov-report=html
# Open htmlcov/index.html to view coverage

# 11. Kill the background API server
pkill -f "uvicorn stratslabapi"
```

## Notes

### Dependencies Added
- None new required - existing project dependencies are sufficient
- `python-dotenv` used in ADW, should add to main project if not present
- `uvicorn` for webhook server (if not already available)

### Future Enhancements
1. **Web Dashboard** - UI for monitoring workflows and triggering manually
2. **Slack Integration** - Send workflow status updates to Slack
3. **Performance Optimization** - Parallelize independent tasks
4. **Advanced Routing** - Route issues to different agents based on labels
5. **Custom Workflows** - Allow users to define custom workflow chains
6. **Model Selection** - Per-issue model selection (sonnet vs opus)
7. **Cost Tracking** - Track API costs per workflow
8. **Workflow Templates** - Create reusable workflow configurations
9. **Team Collaboration** - Multi-user workflow management with approvals

### Configuration Guide
```bash
# Required environment variables
export GITHUB_REPO_URL="https://github.com/owner/repo"
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_CODE_PATH="/path/to/claude"  # or just "claude" if in PATH

# Optional
export GITHUB_PAT="ghp_..."  # If using different GitHub account
export ADW_DEBUG="true"      # For verbose logging
export WEBHOOK_SECRET="..."  # For GitHub webhook verification
```

### Project Structure Notes
- ADW is intentionally separate from main application for modularity
- Can run ADW independently or integrated via API
- State files stored in `agents/` directory (add to .gitignore)
- Database tracks all executions for audit and monitoring
- Logging available both in files and database

### Testing Notes
- Use test GitHub account for E2E tests
- Mock GitHub API in unit tests to avoid rate limiting
- Use SQLite for tests to avoid database setup
- Run tests in isolation (each test creates its own state)
- Clean up test artifacts (state files, branches)

### Known Limitations & Future Work
- Claude Code CLI must be installed separately
- Cannot run workflows on Windows natively (requires WSL)
- GitHub webhook requires public URL with HTTPS
- Rate limited by GitHub API (5000 requests/hour for authenticated)
- Cannot run multiple simultaneous workflows on same issue (by design)
- No built-in approval workflow (could add in future)

