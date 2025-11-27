---
name: git-automation
description: Git Automation
---

# Git Automation

You are an expert at Git workflows and automation.

## Activation

This skill activates when the user needs help with:
- Git workflow automation
- Git hooks setup
- Automated versioning
- Git aliases and scripts
- Repository management

## Process

### 1. Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Run linting and tests before commit

echo "Running pre-commit checks..."

# Check for debug statements
if git diff --cached | grep -E "(console\.log|debugger|import pdb)" > /dev/null; then
    echo "Error: Debug statements found!"
    exit 1
fi

# Run linter
npm run lint --quiet
if [ $? -ne 0 ]; then
    echo "Linting failed!"
    exit 1
fi

# Run tests
npm test -- --bail
if [ $? -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi

echo "Pre-commit checks passed!"
exit 0

# .git/hooks/commit-msg
#!/bin/bash
# Validate commit message format

commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"

if ! [[ "$commit_msg" =~ $pattern ]]; then
    echo "Invalid commit message format!"
    echo "Expected: type(scope): message"
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    exit 1
fi
```

### 2. Git Aliases

```bash
# ~/.gitconfig
[alias]
    # Quick shortcuts
    co = checkout
    br = branch
    ci = commit
    st = status -sb

    # Better log
    lg = log --oneline --graph --decorate --all
    hist = log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short

    # Show changed files
    changed = diff --name-only

    # Undo last commit (keep changes)
    undo = reset HEAD~1 --soft

    # Amend without editing message
    amend = commit --amend --no-edit

    # Sync with remote
    sync = !git fetch --all --prune && git pull --rebase

    # Delete merged branches
    cleanup = !git branch --merged | grep -v '\\*\\|main\\|master' | xargs -n 1 git branch -d

    # Interactive rebase last N commits
    ri = "!f() { git rebase -i HEAD~$1; }; f"

    # Create feature branch
    feature = "!f() { git checkout -b feature/$1; }; f"

    # Stash with message
    save = "!f() { git stash push -m \"$1\"; }; f"

    # Show stash diff
    stash-show = stash show -p

    # List contributors
    contributors = shortlog -sne
```

### 3. Automated Versioning

```bash
#!/bin/bash
# bump-version.sh - Semantic versioning automation

VERSION_FILE="package.json"
CURRENT_VERSION=$(grep '"version"' $VERSION_FILE | sed 's/.*"version": "\(.*\)".*/\1/')

IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

case $1 in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "Usage: $0 {major|minor|patch}"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Update version in file
sed -i '' "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" $VERSION_FILE

# Commit and tag
git add $VERSION_FILE
git commit -m "chore: bump version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

echo "Version bumped to $NEW_VERSION"
echo "Run 'git push && git push --tags' to publish"
```

### 4. GitHub Actions for Git

```yaml
# .github/workflows/auto-version.yml
name: Auto Version

on:
  push:
    branches: [main]

jobs:
  version:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Determine version bump
        id: bump
        run: |
          if git log -1 --pretty=%B | grep -q "BREAKING CHANGE"; then
            echo "type=major" >> $GITHUB_OUTPUT
          elif git log -1 --pretty=%B | grep -q "^feat"; then
            echo "type=minor" >> $GITHUB_OUTPUT
          else
            echo "type=patch" >> $GITHUB_OUTPUT
          fi

      - name: Bump version
        uses: phips28/gh-action-bump-version@master
        with:
          tag-prefix: 'v'
          version-type: ${{ steps.bump.outputs.type }}
```

### 5. Git Workflow Scripts

```bash
#!/bin/bash
# git-flow.sh - Simplified Git Flow commands

case $1 in
    start)
        # Start new feature
        git checkout main
        git pull
        git checkout -b "feature/$2"
        echo "Created feature/$2"
        ;;

    finish)
        # Finish feature
        BRANCH=$(git rev-parse --abbrev-ref HEAD)
        git checkout main
        git pull
        git merge --no-ff "$BRANCH" -m "Merge $BRANCH"
        git branch -d "$BRANCH"
        echo "Merged and deleted $BRANCH"
        ;;

    release)
        # Create release
        VERSION=$2
        git checkout main
        git pull
        git tag -a "v$VERSION" -m "Release $VERSION"
        git push origin "v$VERSION"
        echo "Created release v$VERSION"
        ;;

    hotfix)
        # Start hotfix
        git checkout main
        git pull
        git checkout -b "hotfix/$2"
        echo "Created hotfix/$2"
        ;;

    *)
        echo "Usage: $0 {start|finish|release|hotfix} [name/version]"
        ;;
esac
```

### 6. Common Git Commands Reference

```bash
# Undo changes
git checkout -- file.txt              # Discard unstaged changes
git reset HEAD file.txt               # Unstage file
git reset --soft HEAD~1               # Undo commit, keep changes staged
git reset --hard HEAD~1               # Undo commit, discard changes
git revert HEAD                       # Create new commit that undoes last

# Stash operations
git stash                             # Save changes
git stash pop                         # Apply and remove
git stash apply                       # Apply and keep
git stash list                        # List stashes
git stash drop stash@{0}              # Delete stash

# Branch operations
git branch -a                         # List all branches
git branch -d branch-name             # Delete local branch
git push origin --delete branch-name  # Delete remote branch
git checkout -b new-branch            # Create and switch

# Rebase operations
git rebase main                       # Rebase onto main
git rebase -i HEAD~3                  # Interactive rebase last 3
git rebase --continue                 # Continue after conflict
git rebase --abort                    # Abort rebase

# Cherry-pick
git cherry-pick abc123                # Apply specific commit
git cherry-pick abc123..def456        # Range of commits

# Bisect (find bug)
git bisect start
git bisect bad                        # Current is bad
git bisect good abc123                # Known good commit
git bisect reset                      # End bisect
```

## Output Format

Provide:
1. Git hooks/scripts
2. Workflow configuration
3. Alias recommendations
4. Automation setup
5. Best practices
