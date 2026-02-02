# Test Generation & Execution

Create a new plan in `specs/research/*.md` to generate comprehensive tests for existing or new code. Follow the `Instructions` to create the plan.

## Instructions

- You're writing a plan to generate thorough tests for the specified code/feature
- Create the plan in the `specs/research/*.md` file or update `specs/test.md` with details
- Use the `.claude/templates/test-spec.md` template as your guide
- Research the code to understand what needs to be tested
- Plan comprehensive test coverage including unit, integration, and edge cases
- Identify gaps in existing test coverage
- Design tests that are maintainable, clear, and follow project conventions
- Consider edge cases, error conditions, and boundary values
- Plan for test data, fixtures, and factories as needed
- Ensure tests validate both success and failure paths

## Relevant Files

Focus on the following files:
- `stratslabapi/**` - Code to be tested
- `tests/**` - Test suite structure and patterns
- `.claude/templates/test-spec.md` - Test specification template

## Plan Format

Use the `.claude/templates/test-spec.md` template as your guide. Key sections:

1. **Test Description** - Describe what is being tested and why
2. **Scope** - Define what is included and excluded
3. **Test Strategy** - Unit, integration, end-to-end, edge cases
4. **Test Data & Fixtures** - Data, fixtures, and factories needed
5. **Coverage Goals** - Target coverage percentage and critical paths
6. **Step by Step Tasks** - Detailed ordered test implementation steps
7. **Validation Commands** - Commands to run tests and check coverage

## Important Notes

- Write clear, descriptive test names that explain what is being tested
- Test both success and failure paths
- Use fixtures and factories to keep tests DRY
- Aim for high coverage of critical code paths
- Tests should be maintainable and easy to understand
- Consider edge cases and boundary conditions

## Code to Test

$ARGUMENTS
