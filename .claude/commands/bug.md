# Bug Fix Planning

Create a new plan in `specs/bugs/*.md` to diagnose and fix the reported `Bug` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the plan.

## Instructions

- You're writing a plan to diagnose and fix a bug that is impacting the application
- Create the plan in the `specs/bugs/*.md` file with a descriptive name
- Use the `.claude/templates/bug-spec.md` template as your guide
- Research the codebase to reproduce the bug and understand the root cause
- Focus on understanding the problem before planning the fix
- Include reproduction steps that clearly demonstrate the issue
- Provide root cause analysis explaining why the bug occurs
- Design a fix that addresses the root cause, not just symptoms
- Plan comprehensive testing to prevent regression
- Include a rollback plan for safe deployment
- Document all changes and lessons learned

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions
- `stratslabapi/**` - Backend API implementation where the bug likely exists
- `tests/**` - Test suite where regression tests will be added
- `.claude/templates/bug-spec.md` - Bug specification template

## Plan Format

Use the `.claude/templates/bug-spec.md` template as your guide. Key sections:

1. **Bug Description** - Describe what users are experiencing
2. **Reproduction Steps** - Clear steps to reproduce the bug
3. **Expected vs Actual Behavior** - Define what should happen vs what does
4. **Impact Assessment** - Severity, affected users/components
5. **Root Cause Analysis** - Explain why the bug occurs
6. **Fix Strategy** - Proposed solution with alternatives considered
7. **Safety Safeguards** - Precautions to prevent breaking other code
8. **Step by Step Tasks** - Detailed ordered implementation steps
9. **Testing Strategy** - Tests to verify fix and prevent regression
10. **Rollback Plan** - How to safely rollback if issues occur
11. **Validation Commands** - Commands to verify fix with zero regressions

## Important Notes

- Always reproduce the bug before planning the fix
- Look for the root cause, not just symptoms
- Consider edge cases and error scenarios
- Add tests that would have caught this bug initially
- Document the investigation process
- Plan for safe deployment and rollback

## Bug Description

$ARGUMENTS
