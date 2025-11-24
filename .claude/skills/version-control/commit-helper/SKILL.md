# Commit Helper

You are an expert at writing clear, meaningful Git commit messages.

## Activation

This skill activates when the user needs help with:
- Writing commit messages
- Conventional commits
- Commit organization
- Atomic commits
- Commit history management

## Process

### 1. Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes nor adds
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, etc.
- `ci`: CI/CD changes
- `revert`: Revert previous commit

### 2. Commit Message Examples

**Good Examples:**
```
feat(auth): add OAuth2 login support

Implement Google and GitHub OAuth2 authentication.
Users can now sign in with their existing accounts.

- Add OAuth2 configuration
- Create callback handlers
- Update user model for OAuth profiles

Closes #123

---

fix(api): handle null response from payment service

The payment service occasionally returns null for
pending transactions. Added null check to prevent
500 errors in the order completion flow.

Fixes #456

---

refactor(db): optimize user query performance

Replace N+1 queries in user listing with single
JOIN query. Reduces page load time from 2s to 200ms.

Before: 1 query + N queries for profiles
After: 1 query with LEFT JOIN

---

docs(readme): add installation instructions

- Add prerequisites section
- Document environment variables
- Include troubleshooting guide

---

chore(deps): update dependencies to latest versions

- eslint 8.x → 9.x
- typescript 5.2 → 5.3
- jest 29.x → 30.x

Breaking: ESLint config format changed
```

**Bad Examples (and fixes):**
```
❌ "fixed bug"
✅ "fix(cart): prevent duplicate items when adding quickly"

❌ "WIP"
✅ "feat(search): add basic filtering (WIP)"

❌ "asdfasdf" or "."
✅ "chore: save work in progress"

❌ "Updated code"
✅ "refactor(utils): simplify date formatting logic"

❌ "Changes requested by John"
✅ "fix(form): add email validation per code review"
```

### 3. Commit Message Template

```bash
# Set up commit template
git config --global commit.template ~/.gitmessage

# ~/.gitmessage
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
#
# --- COMMIT GUIDELINES ---
# Type: feat, fix, docs, style, refactor, perf, test, chore, ci
# Scope: component/module affected (optional)
# Subject: imperative mood, no period, max 50 chars
# Body: explain what and why (not how), wrap at 72 chars
# Footer: reference issues, breaking changes
#
# Example:
# feat(auth): add password reset functionality
#
# Users can now reset their password via email link.
# Token expires after 24 hours for security.
#
# Closes #789
```

### 4. Atomic Commits

```markdown
## Atomic Commit Principles

### One Logical Change Per Commit
❌ Bad: "Add feature, fix bug, update docs"
✅ Good: Three separate commits

### Commit Should Be Complete
- Code compiles/runs
- Tests pass
- No broken state

### Splitting Large Changes
Instead of one large commit:
1. Add database schema
2. Add model/entity
3. Add repository layer
4. Add service layer
5. Add API endpoint
6. Add tests
```

### 5. Rewriting Commit History

```bash
# Amend last commit message
git commit --amend -m "New message"

# Amend last commit (add forgotten files)
git add forgotten-file.py
git commit --amend --no-edit

# Interactive rebase to edit multiple commits
git rebase -i HEAD~3

# In editor:
# pick abc123 First commit
# reword def456 Second commit  # Change message
# squash ghi789 Third commit   # Combine with previous

# Split a commit
git rebase -i HEAD~2
# Mark commit as 'edit'
git reset HEAD~
git add file1.py
git commit -m "First logical change"
git add file2.py
git commit -m "Second logical change"
git rebase --continue
```

### 6. Commit Organization

```bash
# Stage specific hunks (partial file)
git add -p file.py
# y = stage this hunk
# n = don't stage
# s = split into smaller hunks
# e = manually edit hunk

# Stage specific lines
git add -i  # Interactive mode

# Check what will be committed
git diff --staged

# Verify commit before pushing
git log -1 --stat
git show HEAD
```

### 7. Commit Message Checklist

```markdown
## Before Committing

Message Quality:
- [ ] Subject line < 50 characters
- [ ] Starts with type (feat, fix, etc.)
- [ ] Uses imperative mood ("add" not "added")
- [ ] No period at end of subject
- [ ] Body explains what and why

Commit Quality:
- [ ] Single logical change
- [ ] All tests pass
- [ ] No debug code
- [ ] No unrelated changes
- [ ] Compiles/runs successfully

References:
- [ ] Issue number included if applicable
- [ ] Breaking changes noted
- [ ] Co-authors credited
```

### 8. Git Hooks for Commit Messages

```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# Check format: type(scope): message
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|ci)(\(.+\))?: .{1,50}"; then
    echo "Error: Commit message doesn't follow convention"
    echo ""
    echo "Format: type(scope): message"
    echo "Types: feat, fix, docs, style, refactor, perf, test, chore, ci"
    echo ""
    echo "Examples:"
    echo "  feat(auth): add login functionality"
    echo "  fix(api): handle null response"
    exit 1
fi

# Check for WIP
if echo "$commit_msg" | grep -qiE "^wip"; then
    echo "Warning: WIP commit detected. Consider completing the work."
fi

exit 0
```

## Output Format

Provide:
1. Formatted commit message
2. Type classification
3. Scope suggestion
4. Body content if needed
5. Footer references
