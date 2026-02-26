# Skill Index — All Skills Used Across All Pipelines

Complete reference of every skill invoked by agent pipelines, organized by pipeline.

## Coding Agent Pipelines

### full-stack.json (5 stages, 9 skills)

```
Stage 1: brainstorm          → obra-superpowers/skills/brainstorming
Stage 2: plan                → obra-superpowers/skills/writing-plans
Stage 3: build (parallel)
  ├── backend (chain)        → backend-api/api-designer
  │                          → backend-api/database-schema
  │                          → frameworks/fastapi-builder
  ├── frontend (chain)       → frameworks/react-component
  │                          → frameworks/ui-builder
  └── infra (chain)          → devops-infrastructure/docker-composer
                             → devops-infrastructure/ci-cd-builder
Stage 4: review              → obra-superpowers/skills/requesting-code-review
Stage 5: finish              → obra-superpowers/skills/finishing-a-development-branch
```

### quality-gate.json (6 stages, 6 skills)

```
Stage 1: code-review         → code-quality/code-reviewer
Stage 2: bug-hunt            → code-quality/bug-hunter
Stage 3: security            → code-quality/security-auditor
Stage 4: tests               → code-quality/test-generator
Stage 5: performance         → code-quality/performance-profiler
Stage 6: verify              → obra-superpowers/skills/verification-before-completion
```

### rapid-prototype.json (5 stages, 5 skills)

```
Stage 1: api-design          → backend-api/api-designer
Stage 2: database            → backend-api/database-schema
Stage 3: backend             → frameworks/fastapi-builder
Stage 4: frontend            → frameworks/react-component
Stage 5: containerize        → devops-infrastructure/docker-composer
```

### debug-chain.json (5 stages, 5 skills)

```
Stage 1: debug               → obra-superpowers/skills/systematic-debugging
Stage 2: root-cause          → obra-superpowers/skills/root-cause-tracing
Stage 3: fix                 → code-quality/bug-hunter
Stage 4: test                → code-quality/test-generator
Stage 5: verify              → obra-superpowers/skills/verification-before-completion
```

---

## Docs Agent Pipelines

### api-docs.json (4 stages, 4 skills)

```
Stage 1: api-doc             → backend-api/api-documenter
Stage 2: code-doc            → code-quality/code-documenter
Stage 3: examples            → backend-api/endpoint-tester
Stage 4: openapi             → backend-api/api-designer
```

### project-docs.json (4 stages, 4 skills)

```
Stage 1: claude-md           → anthropics-official/skill-creator
Stage 2: architecture        → backend-api/api-designer
Stage 3: devlog              → version-control/commit-helper
Stage 4: domain              → code-quality/code-documenter
```

### content-pipeline.json (3 stages, 5 skills)

```
Stage 1: research            → business-communication/content-trend-researcher
Stage 2: content (parallel)
  ├── medium                 → business-communication/medium-post
  ├── linkedin               → business-communication/linkedin-post-formatter
  └── newsletter             → business-communication/newsletter
Stage 3: polish              → business-communication/email-polisher
```

### release-docs.json (4 stages, 4 skills)

```
Stage 1: pr-review           → version-control/pr-reviewer
Stage 2: commits             → version-control/commit-helper
Stage 3: changelog           → code-quality/code-documenter
Stage 4: release-notes       → business-communication/email-polisher
```

---

## Startup Agent Pipelines

### mvp-builder.json (5 stages, 10 skills)

```
Stage 1: brainstorm          → obra-superpowers/skills/brainstorming
Stage 2: offer               → business-communication/alex-hormozi-pitch
Stage 3: plan                → obra-superpowers/skills/writing-plans
Stage 4: build (parallel)
  ├── backend (chain)        → backend-api/api-designer
  │                          → backend-api/database-schema
  │                          → frameworks/fastapi-builder
  ├── frontend (chain)       → frameworks/react-component
  │                          → frameworks/ui-builder
  └── infra                  → devops-infrastructure/docker-composer
Stage 5: deploy              → devops-infrastructure/ci-cd-builder
```

### gtm-launch.json (4 stages, 8 skills)

```
Stage 1: research            → business-communication/content-trend-researcher
Stage 2: pitch               → business-communication/pitch-coach
Stage 3: content (parallel)
  ├── linkedin               → business-communication/linkedin-post-formatter
  ├── medium                 → business-communication/medium-post
  ├── newsletter             → business-communication/newsletter
  └── video                  → business-communication/video-script
Stage 4: email               → business-communication/email-polisher
```

### pitch-deck.json (4 stages, 4 skills)

```
Stage 1: offer               → business-communication/alex-hormozi-pitch
Stage 2: pitch               → business-communication/pitch-coach
Stage 3: deck                → anthropics-official/document-skills/pptx
Stage 4: email               → business-communication/email-polisher
```

### product-analytics.json (4 stages, 4 skills)

```
Stage 1: analytics           → data-engineering/analytics-builder
Stage 2: pipeline            → data-engineering/data-pipeline
Stage 3: dashboard           → community/d3js-visualization
Stage 4: report              → anthropics-official/document-skills/pptx
```

---

## Unique Skills Used (deduplicated)

### obra/superpowers (6)
- `brainstorming`
- `writing-plans`
- `requesting-code-review`
- `verification-before-completion`
- `finishing-a-development-branch`
- `systematic-debugging`
- `root-cause-tracing`

### Backend & API (4)
- `api-designer`
- `api-documenter`
- `database-schema`
- `endpoint-tester`

### Code Quality (5)
- `bug-hunter`
- `code-documenter`
- `code-reviewer`
- `performance-profiler`
- `security-auditor`
- `test-generator`

### Frameworks (3)
- `fastapi-builder`
- `react-component`
- `ui-builder`

### DevOps (2)
- `ci-cd-builder`
- `docker-composer`

### Business Communication (7)
- `alex-hormozi-pitch`
- `content-trend-researcher`
- `email-polisher`
- `linkedin-post-formatter`
- `medium-post`
- `newsletter`
- `pitch-coach`
- `video-script`

### Data Engineering (2)
- `analytics-builder`
- `data-pipeline`

### Version Control (2)
- `commit-helper`
- `pr-reviewer`

### Anthropic Official (2)
- `document-skills/pptx`
- `skill-creator`

### Community (1)
- `d3js-visualization`

**Total: 38 unique skills across 12 pipelines**
