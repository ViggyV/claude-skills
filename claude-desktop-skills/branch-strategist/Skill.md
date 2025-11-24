---
name: "Branch Strategist"
description: "You are an expert at Git branching strategies and workflows."
---

# Branch Strategist

You are an expert at Git branching strategies and workflows.

## Activation

This skill activates when the user needs help with:
- Branching strategies
- Git Flow implementation
- Trunk-based development
- Release management
- Branch naming conventions

## Process

### 1. Branching Models

```
┌─────────────────────────────────────────────────────────────────┐
│                    GIT FLOW                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  main     ●───────●───────────────●───────●───────● (releases)  │
│            \     /               /         \                     │
│  release    ●───●───────────●───●           \                   │
│              \   \         /                 \                   │
│  develop  ●───●───●───●───●───●───●───●───●───●───● (integration)│
│            \         \   /   /                                   │
│  feature    ●─●─●─●   ●─●   \                                   │
│                               ●─●─●─●  (feature branches)       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    TRUNK-BASED                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  main     ●───●───●───●───●───●───●───●───●───● (single trunk)  │
│            \   \ / \   \ /   \ /                                 │
│  feature    ●   ●   ●   ●     ●  (short-lived, < 1 day)         │
│                                                                  │
│  Releases via tags: v1.0, v1.1, v2.0                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB FLOW                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  main     ●───●───●───●───●───●───●───● (always deployable)     │
│            \     /   \     /   \     /                           │
│  feature    ●─●─●     ●─●─●     ●─●─● (PR-based merge)          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Branch Naming Conventions

```bash
# Feature branches
feature/add-user-authentication
feature/JIRA-123-payment-integration
feat/oauth-login

# Bug fixes
fix/login-timeout-error
bugfix/cart-total-calculation
fix/JIRA-456-null-pointer

# Hotfixes (urgent production fixes)
hotfix/security-vulnerability
hotfix/v2.1.1-payment-crash

# Release branches
release/v2.0.0
release/2024-01

# Other common patterns
chore/update-dependencies
docs/api-documentation
refactor/user-service-cleanup
test/add-integration-tests

# Personal/experimental
user/john/experiment-new-cache
spike/evaluate-redis
```

### 3. Git Flow Implementation

```bash
# Initialize (one-time setup)
git flow init
# Or manually:
git checkout -b develop main

# Start feature
git checkout develop
git checkout -b feature/new-feature
# ... work on feature ...
git checkout develop
git merge --no-ff feature/new-feature
git branch -d feature/new-feature

# Start release
git checkout develop
git checkout -b release/v1.0.0
# ... final testing, version bump ...
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git checkout develop
git merge --no-ff release/v1.0.0
git branch -d release/v1.0.0

# Hotfix
git checkout main
git checkout -b hotfix/critical-fix
# ... fix the issue ...
git checkout main
git merge --no-ff hotfix/critical-fix
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git checkout develop
git merge --no-ff hotfix/critical-fix
git branch -d hotfix/critical-fix
```

### 4. Trunk-Based Development

```bash
# Always start from main
git checkout main
git pull

# Create short-lived feature branch
git checkout -b feature/small-change

# Work in small increments
# ... make minimal changes ...
git commit -m "feat: part 1 of feature"

# ... continue ...
git commit -m "feat: complete feature"

# Rebase before merging
git fetch origin
git rebase origin/main

# Merge via PR (squash recommended)
# Or direct merge for trusted contributors
git checkout main
git merge --squash feature/small-change
git commit -m "feat: add small change"

# Deploy main frequently (CI/CD)

# Use feature flags for incomplete features
if (featureFlags.isEnabled('new-checkout')):
    return newCheckoutFlow()
else:
    return oldCheckoutFlow()
```

### 5. Strategy Selection Guide

```markdown
## When to Use Each Strategy

### Git Flow
Best for:
- Scheduled releases
- Multiple versions in production
- Large teams
- Enterprise software

Challenges:
- Complex branching
- Merge overhead
- Long-lived branches

### Trunk-Based Development
Best for:
- Continuous deployment
- Small, experienced teams
- Web applications
- Microservices

Requirements:
- Strong CI/CD
- Feature flags
- High test coverage
- Code review discipline

### GitHub Flow
Best for:
- SaaS applications
- Continuous delivery
- Medium-sized teams
- Simpler projects

Benefits:
- Simple to understand
- Encourages small PRs
- Quick feedback loop
```

### 6. Branch Protection Rules

```yaml
# GitHub branch protection (via API or UI)
protection_rules:
  main:
    required_reviews: 2
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
    require_signed_commits: false
    require_linear_history: true
    allow_force_pushes: false
    allow_deletions: false
    required_status_checks:
      - "ci/test"
      - "ci/lint"
      - "ci/security"
    required_conversation_resolution: true

  develop:
    required_reviews: 1
    required_status_checks:
      - "ci/test"
```

### 7. Release Workflow

```bash
#!/bin/bash
# release.sh - Automated release workflow

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh <version>"
    exit 1
fi

# Ensure on develop and up to date
git checkout develop
git pull origin develop

# Create release branch
git checkout -b "release/$VERSION"

# Update version files
sed -i '' "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml
npm version "$VERSION" --no-git-tag-version

# Generate changelog
git-cliff --tag "$VERSION" > CHANGELOG.md

# Commit version bump
git add -A
git commit -m "chore: bump version to $VERSION"

# Merge to main
git checkout main
git pull origin main
git merge --no-ff "release/$VERSION" -m "Release $VERSION"

# Tag release
git tag -a "v$VERSION" -m "Release $VERSION"

# Merge back to develop
git checkout develop
git merge --no-ff "release/$VERSION" -m "Merge release $VERSION back to develop"

# Cleanup
git branch -d "release/$VERSION"

echo "Release $VERSION complete!"
echo "Run: git push origin main develop --tags"
```

## Output Format

Provide:
1. Recommended strategy
2. Branch naming scheme
3. Workflow steps
4. Protection rules
5. CI/CD integration
