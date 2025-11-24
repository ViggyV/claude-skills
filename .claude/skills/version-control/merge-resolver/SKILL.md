# Merge Resolver

You are an expert at resolving Git merge conflicts and managing complex merges.

## Activation

This skill activates when the user needs help with:
- Resolving merge conflicts
- Understanding conflict markers
- Merge strategies
- Rebase conflicts
- Complex merge scenarios

## Process

### 1. Understanding Conflicts

```
<<<<<<< HEAD
Your changes (current branch)
=======
Their changes (incoming branch)
>>>>>>> feature-branch
```

### 2. Conflict Resolution Strategies

```bash
# Strategy 1: Keep ours
git checkout --ours file.txt
git add file.txt

# Strategy 2: Keep theirs
git checkout --theirs file.txt
git add file.txt

# Strategy 3: Manual resolution
# Edit the file, remove markers, keep desired code
git add file.txt

# Strategy 4: Use merge tool
git mergetool

# Strategy 5: Abort and start over
git merge --abort
git rebase --abort
```

### 3. Common Conflict Scenarios

**Scenario 1: Same Line Modified**
```python
# <<<<<<< HEAD
def calculate_total(items):
    return sum(item.price * item.qty for item in items)
# =======
def calculate_total(items):
    total = sum(item.price * item.quantity for item in items)
    return round(total, 2)
# >>>>>>> feature-branch

# Resolution: Combine both changes
def calculate_total(items):
    total = sum(item.price * item.qty for item in items)
    return round(total, 2)
```

**Scenario 2: File Deleted vs Modified**
```bash
# One branch deleted file, another modified it
git status
# both deleted:    config.py
# deleted by them: config.py

# Keep file
git checkout --ours config.py
git add config.py

# Or accept deletion
git rm config.py
```

**Scenario 3: Different Changes to Same Function**
```javascript
// <<<<<<< HEAD
function processUser(user) {
    validateUser(user);
    saveUser(user);
    return user.id;
}
// =======
function processUser(user) {
    if (!user) throw new Error('Invalid user');
    saveUser(user);
    sendNotification(user);
}
// >>>>>>> feature-branch

// Resolution: Merge logic from both
function processUser(user) {
    if (!user) throw new Error('Invalid user');
    validateUser(user);
    saveUser(user);
    sendNotification(user);
    return user.id;
}
```

### 4. Rebase Conflict Resolution

```bash
# Start rebase
git checkout feature-branch
git rebase main

# When conflict occurs:
# 1. Fix conflicts in files
# 2. Stage resolved files
git add resolved-file.py

# 3. Continue rebase
git rebase --continue

# If multiple commits have conflicts, repeat for each

# To see progress
git status
# You are currently rebasing branch 'feature' on 'abc123'.
# (fix conflicts and then run "git rebase --continue")

# Skip a commit if needed
git rebase --skip

# Abort if it gets messy
git rebase --abort
```

### 5. Merge Strategy Options

```bash
# Recursive (default) - handles most cases
git merge feature-branch

# Ours - keep our version on conflicts
git merge -X ours feature-branch

# Theirs - keep their version on conflicts
git merge -X theirs feature-branch

# No fast-forward - always create merge commit
git merge --no-ff feature-branch

# Squash - combine all commits into one
git merge --squash feature-branch
git commit -m "Merged feature-branch"

# Octopus - merge multiple branches
git merge branch1 branch2 branch3
```

### 6. Advanced Conflict Tools

```bash
# Configure merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Use merge tool
git mergetool

# See differences during merge
git diff --base    # Common ancestor
git diff --ours    # Our changes
git diff --theirs  # Their changes

# Three-way diff
git diff HEAD...feature-branch

# Check for conflicts before merge
git merge --no-commit feature-branch
git diff --check  # Shows conflict markers
git merge --abort
```

### 7. Prevention Strategies

```markdown
## Preventing Merge Conflicts

### Regular Syncing
- Pull from main frequently
- Rebase feature branches regularly
- Keep branches short-lived

### Communication
- Coordinate on shared files
- Use CODEOWNERS for ownership
- Discuss large refactors

### Architecture
- Separate concerns into different files
- Use feature flags for parallel work
- Minimize shared state

### Tooling
- Use git hooks to enforce rebasing
- Automated conflict detection in CI
- Lock files for critical configs
```

### 8. Conflict Resolution Checklist

```markdown
## Resolution Checklist

Before resolving:
- [ ] Understand both changes
- [ ] Know which behavior is correct
- [ ] Consider if both changes needed

During resolution:
- [ ] Remove all conflict markers
- [ ] Verify code syntax is valid
- [ ] Ensure logic is correct
- [ ] Preserve all necessary changes

After resolution:
- [ ] Run tests
- [ ] Run linter
- [ ] Verify functionality
- [ ] Commit with clear message
```

## Output Format

Provide:
1. Conflict analysis
2. Recommended resolution
3. Resolved code
4. Verification steps
5. Prevention advice
