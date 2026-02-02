# Claude Commands Reference

This directory contains command templates for the agentic workflow system. Each command is a specialized agent that helps with specific tasks in the development lifecycle.

## Quick Start

### First Time Setup
```bash
/install          # Install dependencies and setup environment
```

### Understanding the Codebase
```bash
/prime            # Understand the project structure and codebase
/research "topic" # Deep dive research on specific topics
```

### Planning Work
```bash
/feature "description"    # Plan a new feature
/chore "description"      # Plan a maintenance task
/bug "description"        # Plan a bug fix
/refactor "description"   # Plan a refactoring task
/test "code"              # Plan test generation
```

### Implementing Work
```bash
/implement specs/features/feature-name.md    # Execute a feature plan
/implement specs/bugs/bug-name.md            # Execute a bug fix plan
/review stratslabapi/module.py               # Review code quality
```

## Commands

### 1. Prime (`prime.md`)
Understand the codebase structure and patterns.

**Use when:**
- Starting work on the project
- You need an overview of the architecture
- Understanding existing patterns before planning new work

**Output:** Summary of project structure, technology stack, and key components

**Example:**
```bash
/prime
```

### 2. Install (`install.md`)
Set up the development environment and install dependencies.

**Use when:**
- First time setting up the project
- Dependencies need to be refreshed
- Environment configuration needs to be updated

**What it does:**
- Installs project dependencies via poetry
- Sets up .env file from template
- Verifies installation

**Example:**
```bash
/install
```

### 3. Start (`start.md`)
Launch the development server with auto-reload.

**Use when:**
- You want to start the backend API server
- Testing endpoints locally
- Developing new features

**What it does:**
- Starts FastAPI server on http://0.0.0.0:8000
- Enables auto-reload for development
- Timeout: 300 seconds

**Example:**
```bash
/start
```

### 4. Feature (`feature.md`)
Plan the implementation of a new feature.

**Use when:**
- Adding new functionality to the application
- Need a detailed implementation plan before coding
- Want to ensure feature design is solid

**Output:** Feature specification in `specs/features/`

**Example:**
```bash
/feature "Add user authentication with JWT tokens"
/feature "Implement real-time notifications via WebSockets"
```

**Creates:** `specs/features/user-auth-jwt-tokens.md`

**Template:** `.claude/templates/feature-spec.md`

### 5. Chore (`chore.md`)
Plan maintenance tasks and improvements.

**Use when:**
- Updating dependencies
- Refactoring for better code quality
- Fixing technical debt
- Improving documentation

**Output:** Chore specification in `specs/chores/`

**Example:**
```bash
/chore "Update Python dependencies to latest versions"
/chore "Add comprehensive API documentation"
```

**Creates:** `specs/chores/update-python-dependencies.md`

**Template:** `.claude/templates/chore-spec.md`

### 6. Bug (`bug.md`)
Diagnose and plan the fix for a reported bug.

**Use when:**
- A bug has been reported
- Need to understand the root cause
- Planning a fix with comprehensive testing

**Output:** Bug fix specification in `specs/bugs/`

**Example:**
```bash
/bug "Login endpoint returns 500 error with valid credentials"
/bug "Database connection pool exhausts under load"
```

**Creates:** `specs/bugs/login-500-error.md`

**Template:** `.claude/templates/bug-spec.md`

**Process:**
1. Reproduce the bug
2. Analyze root cause
3. Plan fix strategy
4. Design regression tests

### 7. Refactor (`refactor.md`)
Design and plan refactoring work.

**Use when:**
- Code needs structural improvements
- Architectural changes are needed
- Consolidating duplicated code
- Improving maintainability

**Output:** Refactoring specification in `specs/refactors/`

**Example:**
```bash
/refactor "Extract database layer into separate module"
/refactor "Consolidate authentication logic across endpoints"
```

**Creates:** `specs/refactors/extract-database-layer.md`

**Template:** `.claude/templates/refactor-spec.md`

**Key aspects:**
- Maintains behavior (not a feature)
- Comprehensive test coverage beforehand
- Safe migration strategy
- Clear rollback plan

### 8. Test (`test.md`)
Plan and generate comprehensive tests.

**Use when:**
- Need to increase test coverage
- Writing tests for new code
- Planning test strategy before implementation

**Output:** Test specification in `specs/research/`

**Example:**
```bash
/test "stratslabapi/routers/users.py"
/test "Authentication middleware"
```

**Template:** `.claude/templates/test-spec.md`

**Includes:**
- Unit tests
- Integration tests
- Edge cases
- Test fixtures and data

### 9. Review (`review.md`)
Perform comprehensive code review.

**Use when:**
- Need feedback on code quality
- Checking adherence to conventions
- Validating implementation before merge
- Looking for improvements

**Output:** Detailed code review report

**Example:**
```bash
/review stratslabapi/routers/users.py
/review stratslabapi/models/user.py
```

**Checks:**
- Code quality and readability
- Design and architecture
- Security vulnerabilities
- Performance issues
- Test coverage
- Adherence to conventions

### 10. Research (`research.md`)
Explore and document codebase patterns.

**Use when:**
- Understanding how something works
- Learning codebase conventions
- Documenting architecture decisions
- Exploring implementation patterns

**Output:** Research findings in `specs/research/`

**Example:**
```bash
/research "How is user authentication currently implemented?"
/research "What database patterns are used for relationships?"
/research "How are API errors handled?"
```

**Creates:** `specs/research/auth-implementation-patterns.md`

**Template:** `.claude/templates/research-spec.md`

**Produces:**
- Architecture patterns found
- Conventions and standards
- Strengths and weaknesses
- Recommendations for future work

### 11. Implement (`implement.md`)
Execute a specification and implement the planned work.

**Use when:**
- You have a completed spec (from /feature, /bug, /chore, /refactor)
- Ready to write code based on the plan
- Want to execute planned work step-by-step

**Requires:** Spec file as argument (path to .md file)

**Example:**
```bash
/implement specs/features/user-authentication.md
/implement specs/bugs/login-500-error.md
/implement specs/refactors/extract-database-layer.md
```

**Process:**
1. Read and understand the spec
2. Execute step-by-step tasks in order
3. Run validation commands after each phase
4. Report completed work with git diff

### 12. Tools (`tools.md`)
List all available built-in tools and capabilities.

**Use when:**
- Exploring available tools
- Understanding tool capabilities
- Looking for specific functionality

**Example:**
```bash
/tools
```

## Workflow Patterns

### Sequential Workflow (Classic)
```bash
# 1. Plan the work
/feature "Add user profiles"

# 2. Implement based on plan
/implement specs/features/user-profiles.md

# 3. Generate comprehensive tests
/test stratslabapi/routers/profiles.py

# 4. Review the implementation
/review stratslabapi/routers/profiles.py
```

### Research-First Workflow
```bash
# 1. Research current implementation
/research "How are endpoints currently authenticated?"

# 2. Plan refactoring based on findings
/refactor "Standardize authentication across endpoints"

# 3. Implement the refactor
/implement specs/refactors/standardize-auth.md
```

### Bug Fix Workflow
```bash
# 1. Plan the fix
/bug "Login returns 500 with valid credentials"

# 2. Implement the fix
/implement specs/bugs/login-500-error.md

# 3. Verify with comprehensive tests
/test stratslabapi/routers/auth.py

# 4. Review the fix
/review stratslabapi/routers/auth.py
```

### Multi-Agent Parallel Workflow
```bash
# 1. Create main feature spec
/feature "Add payment processing system"
# Spec includes multiple components

# 2. Create sub-specs for each component
/chore "Implement Stripe integration"
/chore "Add payment models to database"
/chore "Create payment endpoints"

# 3. Multiple agents implement in parallel
# Agent 1: /implement specs/chores/stripe-integration.md
# Agent 2: /implement specs/chores/payment-models.md
# Agent 3: /implement specs/chores/payment-endpoints.md

# 4. Integration testing after all components complete
```

## Spec Templates

All specs use templates in `.claude/templates/`:

| Template | Used By | Purpose |
|----------|---------|---------|
| `feature-spec.md` | /feature | Complete feature implementation plans |
| `chore-spec.md` | /chore | Maintenance and improvement tasks |
| `bug-spec.md` | /bug | Bug diagnosis and fix plans |
| `refactor-spec.md` | /refactor | Code refactoring and restructuring |
| `test-spec.md` | /test | Test planning and generation |
| `research-spec.md` | /research | Codebase exploration findings |

## Specifications Directory

All specs are stored in organized directories:

```
specs/
├── features/       # Feature implementation plans
├── chores/         # Maintenance task plans
├── bugs/           # Bug fix plans
├── refactors/      # Refactoring plans
├── research/       # Research findings
└── README.md       # Guide to specs
```

See `specs/README.md` for detailed guidance on specs.

## Helper Scripts

The `.claude` system uses scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `start.sh` | Start development server |
| `copy_dot_env.sh` | Setup environment file |
| `test.sh` | Run tests with coverage |
| `validate.sh` | Full validation pipeline |

## Best Practices

### Planning Phase
1. **Research First**: Use `/research` before planning complex work
2. **Be Specific**: Write detailed specs, not vague requirements
3. **Consider Alternatives**: Document why your approach was chosen
4. **Plan for Testing**: Include testing strategy in every spec
5. **Plan for Rollback**: Always have a backup plan

### Implementation Phase
1. **Follow the Spec**: Implement exactly what was planned
2. **Test as You Go**: Run validation commands frequently
3. **Make Small Commits**: Break work into logical chunks
4. **Document Changes**: Write clear commit messages
5. **Handle Errors**: Fix issues as they arise, don't skip ahead

### Review Phase
1. **Check Against Spec**: Ensure implementation matches plan
2. **Run All Tests**: Validate with zero regressions
3. **Review Code Quality**: Use `/review` for comprehensive feedback
4. **Test Edge Cases**: Verify robustness

## Troubleshooting

### Command Not Found
Make sure you're using `/command-name` format (with leading slash)

### Spec Not Created
Check that you used proper punctuation and description:
```bash
# Good
/feature "Add user authentication"

# Bad
/feature Add user authentication     # Missing quotes
```

### Implementation Failed
1. Read the spec completely
2. Check current state with `git status`
3. Review error messages
4. Fix issues and continue
5. Re-run validation commands

### Tests Failing
1. Review test output carefully
2. Check what changed since last passing test
3. Update spec if approach needs to change
4. Re-run tests to verify fix

## Documentation

- **Project README**: `README.md` - Overview and setup
- **Specs Guide**: `specs/README.md` - How to create and use specs
- **Commands**: `.claude/commands/` - This directory with command templates
- **Templates**: `.claude/templates/` - Spec templates
- **Settings**: `.claude/settings.json` - Permissions and configuration

## Getting Help

For help with:
- **Claude Code CLI**: Use `/help`
- **Bug Reports**: Report issues at https://github.com/anthropics/claude-code/issues
- **Codebase Questions**: Use `/research` to explore and understand

## Key Principles

1. **Single Source of Truth**: Specs are the plans; implementation follows specs
2. **Progressive Disclosure**: Research → Plan → Implement → Test → Review
3. **Clear Responsibility**: Each agent has a specific role and scope
4. **Safety First**: Plans include rollback strategies and comprehensive testing
5. **Documentation**: Findings and decisions are recorded in specs
6. **Efficiency**: Parallel workflows where possible, sequential where needed

