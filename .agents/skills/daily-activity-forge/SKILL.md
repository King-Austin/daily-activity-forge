```markdown
# daily-activity-forge Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the development patterns and conventions used in the `daily-activity-forge` TypeScript codebase. You'll learn how to structure files, write imports and exports, and follow the project's testing patterns. This guide also provides suggested commands for common workflows, helping you contribute efficiently and consistently.

## Coding Conventions

### File Naming
- Use **snake_case** for all file names.
  - Example:  
    ```
    user_activity.ts
    daily_report_generator.ts
    ```

### Import Style
- Use **relative imports** for referencing other modules.
  - Example:  
    ```typescript
    import { calculateSteps } from './step_utils';
    import { User } from '../models/user';
    ```

### Export Style
- Use **named exports** for all exported functions, types, or constants.
  - Example:  
    ```typescript
    // In activity_utils.ts
    export function summarizeActivity(data: ActivityData[]): Summary { ... }
    export const ACTIVITY_THRESHOLD = 10000;
    ```

### Commit Messages
- Commit messages are **freeform** (no enforced prefixes).
- Typical length is short (~17 characters).
  - Example:  
    ```
    add daily summary
    fix step counter bug
    update user model
    ```

## Workflows

### Adding a New Feature
**Trigger:** When you want to introduce new functionality  
**Command:** `/add-feature`

1. Create a new file using snake_case in the appropriate directory.
2. Implement your feature using TypeScript.
3. Use relative imports to include any dependencies.
4. Export your functions/types using named exports.
5. Write corresponding tests in a `*.test.*` file.
6. Commit your changes with a concise message.

### Fixing a Bug
**Trigger:** When you need to resolve a defect  
**Command:** `/fix-bug`

1. Locate the relevant file(s) using snake_case naming.
2. Make the necessary code changes.
3. Update or add tests in the matching `*.test.*` file.
4. Commit with a short, descriptive message.

### Writing Tests
**Trigger:** When adding or updating tests  
**Command:** `/write-test`

1. Create or update a test file matching the pattern `*.test.*` (e.g., `activity_utils.test.ts`).
2. Write test cases for your functions or modules.
3. Use the project's preferred (unknown) testing framework.
4. Run the tests to ensure correctness.

## Testing Patterns

- Test files follow the `*.test.*` naming convention.
  - Example:  
    ```
    activity_utils.test.ts
    user_activity.test.ts
    ```
- The specific testing framework is **unknown**; check existing test files for patterns.
- Each test file should cover the corresponding module's functionality.

## Commands
| Command       | Purpose                                   |
|---------------|-------------------------------------------|
| /add-feature  | Start the workflow for adding a new feature|
| /fix-bug      | Start the workflow for fixing a bug        |
| /write-test   | Start the workflow for writing or updating tests |
```