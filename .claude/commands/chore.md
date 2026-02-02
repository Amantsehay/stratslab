# Chore Planning

Create a new plan in specs/*.md to resolve the `Chore` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the plan use the `Relevant Files` to focus on the right files.

## Instructions

- You're writing a plan to resolve a chore, it should be simple but we need to be thorough and precise so we don't miss anything or waste time with any second round of changes.
- Create the plan in the `specs/*.md` file. Name it appropriately based on the `Chore`.
- Use the plan format below to create the plan. 
- Research the codebase and put together a plan to accomplish the chore.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to accomplish the chore.
- Use your reasoning model: THINK HARD about the plan and the steps to accomplish the chore.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `stratslabapi/**` - Contains the backend API implementation.
- `tests/**` - Contains the test suite.
- `scripts/**` - Contains development automation scripts.
- `.claude/templates/chore-spec.md` - Chore specification template.

Ignore all other files in the codebase.

## Plan Format

Use the `.claude/templates/chore-spec.md` template as your guide. Key sections:

1. **Chore Description** - Detail what the chore involves
2. **Problem Statement** - Define what improvement it provides
3. **Relevant Files** - List affected files with explanations
4. **Step by Step Tasks** - Detailed ordered steps for completion
5. **Testing Strategy** - How changes will be tested
6. **Validation Commands** - Commands to verify completion with zero regressions

## Important Notes

- Research existing patterns in `stratslabapi/**` before planning
- Keep chores focused and self-contained
- Include validation commands using `poetry run pytest`
- Document the purpose and impact of the chore
- Plan for safe implementation with rollback capability

## Chore
$ARGUMENTS