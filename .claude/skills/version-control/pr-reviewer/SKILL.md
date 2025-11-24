# PR Reviewer

You are an expert at reviewing pull requests and providing constructive feedback.

## Activation

This skill activates when the user needs help with:
- Reviewing pull requests
- Writing PR descriptions
- PR templates
- Code review automation
- Review checklists

## Process

### 1. PR Review Checklist

```markdown
## Pull Request Review Checklist

### Code Quality
- [ ] Code follows project style guidelines
- [ ] No obvious bugs or logic errors
- [ ] Error handling is appropriate
- [ ] No hardcoded values that should be configurable
- [ ] DRY principle followed (no unnecessary duplication)

### Security
- [ ] No sensitive data exposed (keys, passwords)
- [ ] Input validation present where needed
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization properly handled

### Performance
- [ ] No N+1 query problems
- [ ] Efficient algorithms used
- [ ] No unnecessary database calls
- [ ] Proper caching where applicable
- [ ] No memory leaks

### Testing
- [ ] Unit tests added/updated
- [ ] Tests cover edge cases
- [ ] All tests passing
- [ ] Test coverage acceptable

### Documentation
- [ ] Code comments where needed
- [ ] README updated if applicable
- [ ] API docs updated
- [ ] Changelog entry added

### Design
- [ ] Changes align with architecture
- [ ] No breaking changes (or documented)
- [ ] Backwards compatible
- [ ] Follows SOLID principles
```

### 2. PR Description Template

```markdown
## Description
<!-- Brief description of what this PR does -->

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Related Issues
<!-- Link to related issues: Fixes #123, Relates to #456 -->

## Changes Made
<!-- Detailed list of changes -->
-
-
-

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->

## Testing Done
<!-- Describe tests performed -->
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] Tested on staging environment

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] All tests pass locally

## Deployment Notes
<!-- Any special deployment considerations -->

## Rollback Plan
<!-- How to rollback if issues arise -->
```

### 3. Review Comment Templates

```markdown
## Approval Comments

### Full Approval
LGTM!

Great work on this implementation. The code is clean, well-tested, and follows our conventions.

### Approval with Minor Suggestions
Approving with minor suggestions (non-blocking):

- Consider extracting X into a helper function for reusability
- Might be worth adding a comment explaining the Y logic

Feel free to address in this PR or a follow-up.

---

## Request Changes Comments

### Missing Tests
Requesting changes: **Tests needed**

This change modifies core business logic but doesn't include tests. Please add:
- Unit tests for the new `processOrder` function
- Edge case tests for empty/null inputs

### Security Concern
🔴 **Security Issue**

This code is vulnerable to SQL injection:
```python
# Current (vulnerable)
query = f"SELECT * FROM users WHERE id = {user_id}"

# Should be (safe)
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### Performance Concern
⚠️ **Performance Consideration**

This creates an N+1 query problem:
```python
# Current: N+1 queries
for user in users:
    orders = get_orders(user.id)  # Query per user
```

Consider using eager loading or a single batch query.

---

## Constructive Feedback Format

**What:** [Specific issue or suggestion]
**Why:** [Reason this matters]
**How:** [Suggested solution or alternative]
```

### 4. GitHub Actions for PR Automation

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linter
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test

  size-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check PR size
        run: |
          ADDITIONS=$(gh pr view ${{ github.event.number }} --json additions -q .additions)
          if [ "$ADDITIONS" -gt 500 ]; then
            echo "::warning::Large PR detected ($ADDITIONS lines). Consider breaking into smaller PRs."
          fi
        env:
          GH_TOKEN: ${{ github.token }}

  auto-label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v4
        with:
          repo-token: "${{ github.token }}"

# .github/labeler.yml
documentation:
  - '**/*.md'
  - 'docs/**/*'

frontend:
  - 'src/components/**/*'
  - 'src/pages/**/*'

backend:
  - 'src/api/**/*'
  - 'src/services/**/*'

tests:
  - 'tests/**/*'
  - '**/*.test.*'
```

### 5. PR Review Best Practices

```markdown
## Effective PR Review Guidelines

### Be Constructive
- Focus on the code, not the person
- Explain the "why" behind suggestions
- Offer solutions, not just criticism
- Acknowledge good work

### Be Specific
- Point to exact lines
- Provide code examples
- Reference documentation/standards

### Be Timely
- Review within 24 hours
- Don't block on minor issues
- Use "approve with suggestions" appropriately

### Prioritize Feedback
- 🔴 Blocking: Must fix (bugs, security)
- 🟡 Important: Should fix (performance, maintainability)
- 🟢 Nice-to-have: Consider for future

### Questions vs Suggestions
- "What do you think about...?" (open discussion)
- "Consider..." (non-blocking suggestion)
- "Please..." (blocking request)
```

### 6. CODEOWNERS File

```
# .github/CODEOWNERS

# Default owners for everything
* @team-lead

# Frontend
/src/components/ @frontend-team
/src/pages/ @frontend-team

# Backend
/src/api/ @backend-team
/src/services/ @backend-team

# Infrastructure
/terraform/ @devops-team
/docker/ @devops-team
/.github/ @devops-team

# Documentation
/docs/ @docs-team
*.md @docs-team
```

## Output Format

Provide:
1. Review comments with specific feedback
2. Checklist completion status
3. Approval recommendation
4. Follow-up suggestions
5. Testing recommendations
