# Bug Fix: <bug title>

## Metadata
- **Type**: Bug
- **Status**: Planning
- **Created**: <date>
- **Updated**: <date>
- **Agent**: <agent name>
- **Severity**: <Critical/High/Medium/Low>

## Bug Description
<describe the bug in detail, what users are experiencing>

## Reproduction Steps
1. <step 1>
2. <step 2>
3. <step 3>

## Expected Behavior
<describe what should happen>

## Actual Behavior
<describe what actually happens>

## Impact Assessment
- **Severity**: <Critical/High/Medium/Low>
- **Affected Users/Components**: <list affected functionality>
- **Business Impact**: <describe impact to the product>

## Root Cause Analysis
<describe the underlying cause of the bug, not just symptoms>

## Relevant Files
Use these files to fix the bug:

- `stratslabapi/**` - Backend API implementation
- `<other relevant files>` - Describe why they are relevant

## Fix Strategy
### Proposed Solution
<describe the fix approach>

### Alternatives Considered
<describe other approaches that were considered and why they were rejected>

### Safety Safeguards
<describe any precautions to ensure the fix doesn't break other functionality>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: <reproduce and verify>
- <subtask 1>
- <subtask 2>

### Step 2: <implement fix>
- <subtask 1>
- <subtask 2>

### Step 3: <validation and regression testing>
- <subtask 1>
- <subtask 2>

## Testing Strategy

### Reproduction Test
<describe test that reproduces the bug>

### Unit Tests
<describe unit tests for the fix>

### Regression Tests
<describe tests to ensure no related functionality is broken>

### Edge Cases
- <edge case 1>
- <edge case 2>

## Dependencies & Blockers
- **External Dependencies**: <list any new packages needed>
- **Internal Dependencies**: <list dependent fixes or components>
- **Blockers**: <list any blocking issues>

## Rollback Plan
<describe how to safely rollback this fix if new issues occur>

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `poetry run pytest tests/ -v` - Run all tests to validate the bug fix works with zero regressions
- <additional validation commands>

## Notes
<optionally list any additional notes, preventative measures, or context relevant to this bug>
