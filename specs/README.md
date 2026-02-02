# Specifications & Plans

This directory contains all implementation specs and plans for the StratsLab project. Specs serve as the single source of truth for planned work and guide implementation.

## Directory Structure

- **`features/`** - Feature specifications for new functionality
- **`chores/`** - Maintenance tasks and improvements
- **`bugs/`** - Bug fix plans with root cause analysis
- **`refactors/`** - Refactoring plans for code improvements
- **`research/`** - Research findings and codebase exploration

## Spec Lifecycle

### 1. Planning Phase
- Use `/feature`, `/chore`, `/bug`, `/refactor`, or `/research` commands
- Creates detailed spec in appropriate subdirectory
- Spec defines problem, solution, and acceptance criteria

### 2. Review Phase
- Review the generated spec for completeness
- Identify any blockers or dependencies
- Ensure acceptance criteria are measurable

### 3. Implementation Phase
- Use `/implement <spec-file>` to start implementation
- Follow the step-by-step tasks in the spec
- Execute validation commands to verify completion

### 4. Validation Phase
- Run all validation commands from the spec
- Ensure no regressions
- Mark spec as complete

## Creating a Spec

### Using a Command

**Feature:**
```bash
/feature "Add user authentication system"
```

**Bug:**
```bash
/bug "Login endpoint returns 500 error"
```

**Chore:**
```bash
/chore "Update dependencies to latest versions"
```

**Refactor:**
```bash
/refactor "Extract database logic into separate module"
```

**Research:**
```bash
/research "How is error handling currently implemented?"
```

### Spec Templates

Each spec type has a template available in `.claude/templates/`:
- `feature-spec.md` - Feature implementation template
- `bug-spec.md` - Bug fix template
- `chore-spec.md` - Maintenance task template
- `refactor-spec.md` - Refactoring template
- `test-spec.md` - Testing template
- `research-spec.md` - Research template

## Spec Structure

All specs follow a consistent structure:

### Metadata
- Type (features/chores/bugs/refactors/research)
- Status (planning/in-progress/completed)
- Created and updated dates
- Agent name

### Problem & Solution
- Problem statement explaining what needs to be done
- Solution approach and design decisions
- Acceptance criteria for completion

### Implementation Details
- Relevant files to modify or create
- Step-by-step tasks in order
- Testing strategy
- Validation commands

### Risk Management
- Dependencies and blockers
- Rollback plan
- Safety considerations

## Best Practices

### Writing Good Specs

1. **Be Specific**: Specs should be detailed enough to implement without asking questions
2. **Define Success**: Acceptance criteria must be measurable and testable
3. **Plan for Failure**: Include rollback plans and risk assessment
4. **Research First**: Use `/research` before planning to understand the codebase
5. **Break Down Work**: Complex specs should have multiple phases
6. **Consider Edge Cases**: Testing section should cover edge cases and error scenarios

### Implementing Specs

1. **Read Carefully**: Understand the entire spec before starting
2. **Follow Order**: Execute step-by-step tasks in the order specified
3. **Validate Frequently**: Run validation commands after each phase
4. **Report Progress**: Use git commits to track implementation progress
5. **Adapt When Needed**: Update spec if you discover new information

### Using Specs in Workflows

**Sequential Workflow:**
1. Create feature spec: `/feature "User profiles"`
2. Implement feature: `/implement specs/features/user-profiles.md`
3. Generate tests: `/test stratslabapi/routers/profile.py`
4. Review code: `/review stratslabapi/routers/profile.py`

**Parallel Workflow:**
1. Create main feature spec with multiple components
2. Create sub-specs for each component
3. Multiple agents implement in parallel
4. Integrate and test together

**Iterative Workflow:**
1. Research current implementation: `/research "How auth works"`
2. Plan refactoring: `/refactor "Standardize auth"`
3. Implement: `/implement specs/refactors/standardize-auth.md`
4. Repeat for improvements

## File Naming

Use descriptive names for spec files:
- Good: `specs/features/user-authentication-system.md`
- Good: `specs/bugs/login-endpoint-500-error.md`
- Avoid: `specs/features/feature1.md`

Use hyphens to separate words, keep names concise but clear.

## Viewing Specs

List all specs by type:
```bash
ls specs/features/        # View all feature specs
ls specs/bugs/            # View all bug specs
ls specs/chores/          # View all chore specs
ls specs/refactors/       # View all refactor specs
ls specs/research/        # View all research findings
```

Find specs by keyword:
```bash
grep -r "user auth" specs/     # Find specs related to user auth
grep -r "database" specs/      # Find specs related to database
```

## Integration with .claude

The `.claude/` directory contains command templates that create specs:
- `.claude/commands/feature.md` - Feature planning command
- `.claude/commands/chore.md` - Chore planning command
- `.claude/commands/bug.md` - Bug fix command
- `.claude/commands/refactor.md` - Refactoring command
- `.claude/commands/research.md` - Research command
- `.claude/commands/implement.md` - Implementation executor

See `.claude/commands/README.md` for complete documentation.

## Examples

### Example Feature Spec

```markdown
# Feature: User Profile Management

## Metadata
- **Type**: Feature
- **Status**: Planning
- **Created**: 2024-01-15
- **Agent**: feature-planner

## Feature Description
Allow users to create, read, update, and delete their profiles...

## Acceptance Criteria
- Users can view their complete profile
- Users can update their information
- Avatar upload works with image validation
- Changes are persisted to database
```

### Example Bug Spec

```markdown
# Bug Fix: Login Endpoint Returns 500 Error

## Bug Description
When users attempt to login with valid credentials, they receive a 500 error instead of a session token...

## Reproduction Steps
1. Navigate to /api/login
2. Enter valid credentials
3. Observe 500 response

## Root Cause Analysis
Database connection pool is exhausted due to unclosed connections in auth handler...
```

## Questions?

Refer to:
- `.claude/commands/README.md` - Available commands and workflows
- Individual spec templates in `.claude/templates/` - Template structure
- Project README.md - Overall project documentation
