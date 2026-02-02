# Feature Planning

Create a new plan in specs/*.md to implement the `Feature` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the plan use the `Relevant Files` to focus on the right files.

## Instructions

- You're writing a plan to implement a net new feature that will add value to the application.
- Create the plan in the `specs/*.md` file. Name it appropriately based on the `Feature`.
- Use the `Plan Format` below to create the plan. 
- Research the codebase to understand existing patterns, architecture, and conventions before planning the feature.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to implement the feature successfully.
- Use your reasoning model: THINK HARD about the feature requirements, design, and implementation approach.
- Follow existing patterns and conventions in the codebase. Don't reinvent the wheel.
- Design for extensibility and maintainability.
- If you need a new library, use `poetry add` and be sure to report it in the `Notes` section of the `Plan Format`.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `stratslabapi/**` - Contains the backend API implementation.
- `tests/**` - Contains the test suite.
- `scripts/**` - Contains development automation scripts.
- `.claude/templates/feature-spec.md` - Feature specification template.

Ignore all other files in the codebase.

## Plan Format

Use the `.claude/templates/feature-spec.md` template as your guide. Key sections:

1. **Feature Description** - Detail the feature, its purpose, and value
2. **User Story** - Frame as "As a <user>, I want <action>, so that <benefit>"
3. **Problem & Solution** - Define the problem and proposed solution
4. **Acceptance Criteria** - Specific, measurable completion criteria
5. **Relevant Files** - List affected files with explanations
6. **Design Decisions** - Explain architectural choices and alternatives
7. **Implementation Plan** - Phased approach (Foundation → Core → Integration)
8. **Step by Step Tasks** - Detailed ordered steps (must include testing)
9. **Testing Strategy** - Unit, integration, and edge case tests
10. **Validation Commands** - Commands to verify implementation with zero regressions

## Important Notes

- Research existing patterns in `stratslabapi/**` before planning
- Use `poetry add <package>` for new dependencies (not uv)
- Create spec file in `specs/features/` with descriptive name
- Include validation commands using `poetry run pytest`
- Plan for extensibility and maintainability
- Document design decisions and alternatives considered

## Feature
$ARGUMENTS