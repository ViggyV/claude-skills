# Agent Pipelines — Complete Guide

## What Are Agent Pipelines?

Agent pipelines are automated multi-stage workflows that chain existing Claude Code skills together. Instead of manually invoking skills one by one, you say `/code full-stack` and the system automatically:

1. Brainstorms your idea into a design
2. Writes an implementation plan
3. Builds backend, frontend, and infrastructure in parallel
4. Runs a quality review
5. Finishes the branch (merge, PR, keep, or discard)

Each stage passes its outputs to the next via files on disk, so context survives even across long sessions.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                    User                          │
│         "/code full-stack my-app"                │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│              Super-Agent (Router)                │
│                                                  │
│  coding-agent / docs-agent / startup-agent       │
│                                                  │
│  1. Parse command → select pipeline              │
│  2. Gather context (what, name, mode)            │
│  3. Load pipeline JSON                           │
│  4. Invoke pipeline-orchestrator                 │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│           Pipeline Orchestrator                  │
│                                                  │
│  1. Resolve template variables                   │
│  2. Create task list                             │
│  3. Execute stages in order:                     │
│     ┌──────────┐                                 │
│     │  skill   │ → invoke single skill           │
│     └──────────┘                                 │
│     ┌──────────────┐                             │
│     │ skill-chain  │ → invoke skills in sequence │
│     └──────────────┘                             │
│     ┌──────────┐                                 │
│     │ parallel │ → dispatch subagents            │
│     └──────────┘                                 │
│  4. Enforce gates between stages                 │
│  5. Pass data via file outputs                   │
└─────────────────────────────────────────────────┘
```

---

## The Four Skills

### 1. Pipeline Orchestrator

**What it is:** The execution engine. Never called directly by users.

**What it does:**
- Reads a pipeline JSON definition
- Resolves `{date}`, `{name}`, `{project}` variables in output paths
- Executes stages in order (sequential, chained, or parallel)
- Interpolates `${stage_id.outputs.key}` to pass data between stages
- Enforces quality gates (approval, code review, verification)
- Stops on failure with a clear error report

**Key rule:** No stage advances without verified outputs from the previous stage.

### 2. Coding Agent (`/code`)

**What it is:** Router for coding workflows.

**Pipelines:**

| Pipeline | Stages | Best For |
|----------|--------|----------|
| `full-stack` | brainstorm → plan → parallel(backend, frontend, infra) → review → finish | Building complete features from scratch |
| `quality-gate` | code-review → bug-hunt → security → tests → performance → verify | Auditing existing code quality |
| `rapid-prototype` | api-design → database → FastAPI → React → Docker | Fast MVPs with a working prototype |
| `debug-chain` | systematic-debug → root-cause → bug-hunt → test → verify | Fixing bugs you can't figure out |

**Example usage:**
```
/code                     → shows all 4 pipelines, asks which one
/code full-stack          → jumps straight to full-stack pipeline
/code quality             → starts quality audit
/code debug               → starts systematic debugging
/code prototype           → starts rapid prototype
```

### 3. Docs Agent (`/docs`)

**What it is:** Router for documentation workflows.

**Pipelines:**

| Pipeline | Stages | Best For |
|----------|--------|----------|
| `api-docs` | api-documenter → code-documenter → examples → OpenAPI | Documenting REST/GraphQL APIs |
| `project-docs` | CLAUDE.md → ARCHITECTURE.md → DEVLOG.md → DOMAIN.md | Scaffolding project documentation |
| `content-pipeline` | research → parallel(Medium, LinkedIn, newsletter) → polish | Creating multi-channel content |
| `release-docs` | PR-review → commits → changelog → release-notes | Generating release documentation |

**Example usage:**
```
/docs                     → shows all 4 pipelines, asks which one
/docs api                 → generate API documentation
/docs project             → scaffold project docs
/docs content             → create multi-channel content
/docs release             → generate changelog and release notes
```

### 4. Startup Agent (`/startup`)

**What it is:** Router for startup/business workflows.

**Pipelines:**

| Pipeline | Stages | Best For |
|----------|--------|----------|
| `mvp-builder` | brainstorm → Hormozi pitch → plan → parallel build → deploy | Going from idea to deployed product |
| `gtm-launch` | research → pitch → parallel(LinkedIn, Medium, newsletter, video) → email | Multi-channel go-to-market launch |
| `pitch-deck` | Hormozi pitch → pitch coach → PPTX → outreach email | Investor pitch with presentation |
| `product-analytics` | analytics spec → data pipeline → D3.js → PPTX report | Setting up analytics dashboards |

**Example usage:**
```
/startup                  → shows all 4 pipelines, asks which one
/startup mvp              → build MVP from scratch
/startup gtm              → create go-to-market content
/startup pitch            → create pitch deck
/startup analytics        → set up analytics dashboards
```

---

## Pipeline JSON Format

Each pipeline is a declarative JSON file. Here's the anatomy:

```json
{
  "name": "pipeline-name",
  "description": "What this pipeline produces",
  "mode": "interactive",
  "stages": [...]
}
```

### Stage Types

#### `skill` — Invoke a single skill

```json
{
  "id": "brainstorm",
  "type": "skill",
  "skill": "obra-superpowers/skills/brainstorming",
  "description": "Refine the idea into a design",
  "outputs": {
    "design_doc": "docs/plans/{date}-{name}-design.md"
  }
}
```

#### `skill-chain` — Invoke skills in sequence

```json
{
  "id": "backend",
  "type": "skill-chain",
  "skills": [
    "backend-api/api-designer",
    "backend-api/database-schema",
    "frameworks/fastapi-builder"
  ],
  "description": "Build the backend API stack"
}
```

#### `parallel` — Dispatch concurrent branches

```json
{
  "id": "build",
  "type": "parallel",
  "branches": [
    { "id": "backend", "type": "skill-chain", "skills": [...] },
    { "id": "frontend", "type": "skill-chain", "skills": [...] },
    { "id": "infra", "type": "skill", "skill": "..." }
  ],
  "description": "Build all components in parallel"
}
```

### Gates

Gates are checkpoints between stages:

| Gate Type | Interactive Mode | Autonomous Mode |
|-----------|-----------------|-----------------|
| `approval` | Pause, ask user to confirm | Skip |
| `quality` | Run code-review subagent | Run code-review subagent |
| `verification` | Require evidence before proceeding | Require evidence before proceeding |

```json
{
  "gate": {
    "type": "approval",
    "prompt": "Design complete. Review before planning?"
  }
}
```

### Data Flow

Stages declare outputs and consume inputs from prior stages:

```json
// Stage 1 declares outputs
{ "id": "brainstorm", "outputs": { "design_doc": "docs/plans/{date}-{name}-design.md" } }

// Stage 2 consumes them via interpolation
{ "id": "plan", "inputs": { "design_doc": "${brainstorm.outputs.design_doc}" } }
```

Template variables resolved at pipeline start:
- `{date}` → today's date (YYYY-MM-DD)
- `{name}` → pipeline name or user-provided name
- `{project}` → current directory name

---

## Modes

### Interactive Mode (Default)

All gates are active. The pipeline pauses at each gate and asks the user to confirm before continuing. Best for:
- First time running a pipeline
- Important production work
- When you want to review each stage's output

### Autonomous Mode

Approval gates are skipped, but quality and verification gates still run. Best for:
- Familiar workflows you've run before
- Batch processing
- When you trust the pipeline and want speed

---

## How Agents Build on obra/superpowers

These agents orchestrate existing skills — they don't replace them:

| Pattern | obra Skill Used | How Agents Use It |
|---------|----------------|-------------------|
| Design refinement | `brainstorming` | First stage in full-stack and MVP pipelines |
| Implementation plans | `writing-plans` | Plan stage, saves to `docs/plans/YYYY-MM-DD-<name>.md` |
| Code review | `requesting-code-review` | Quality gates dispatch code-reviewer subagent |
| Verification | `verification-before-completion` | Verification gates require evidence, not claims |
| Branch completion | `finishing-a-development-branch` | Final stage offers merge/PR/keep/discard |
| Parallel dispatch | `dispatching-parallel-agents` | Parallel stages follow independent-work-only constraint |

---

## Creating Custom Pipelines

You can create your own pipeline by adding a JSON file to any agent's `references/pipelines/` directory.

### Step 1: Create the JSON file

```bash
# Example: add a "microservices" pipeline to the coding agent
touch .claude/skills/agents/coding-agent/references/pipelines/microservices.json
```

### Step 2: Define stages

```json
{
  "name": "microservices",
  "description": "Design and build a microservices architecture",
  "mode": "interactive",
  "stages": [
    {
      "id": "design",
      "type": "skill",
      "skill": "backend-api/microservices-architect",
      "description": "Design the microservices architecture",
      "outputs": { "arch_doc": "docs/plans/{date}-{name}-architecture.md" },
      "gate": { "type": "approval", "prompt": "Architecture ready. Build services?" }
    },
    {
      "id": "services",
      "type": "parallel",
      "branches": [
        { "id": "auth", "type": "skill", "skill": "backend-api/oauth-implementer" },
        { "id": "api", "type": "skill", "skill": "frameworks/fastapi-builder" },
        { "id": "gateway", "type": "skill", "skill": "backend-api/api-designer" }
      ],
      "inputs": { "arch_doc": "${design.outputs.arch_doc}" }
    },
    {
      "id": "infra",
      "type": "skill-chain",
      "skills": [
        "devops-infrastructure/docker-composer",
        "devops-infrastructure/kubernetes-helper"
      ],
      "gate": { "type": "verification", "prompt": "Verify K8s manifests are valid" }
    }
  ]
}
```

### Step 3: Update the agent's SKILL.md

Add the new pipeline to the agent's routing table.

### Validation Rules

- All stage `id` fields must be unique
- `${...}` interpolation can only reference earlier stages
- Parallel branches must not share output file paths
- At least one stage required
- Skill paths match the format: `category/skill-name`

---

## Troubleshooting

### Pipeline fails at a stage

The orchestrator stops and reports which stage failed. Check:
1. Does the skill exist at the referenced path?
2. Are input files from prior stages present on disk?
3. Did a quality gate reject the output?

### Parallel branches conflict

Branches in a `parallel` stage must be independent. If you see conflicts:
1. Ensure branches write to different output paths
2. Ensure branches don't modify the same source files
3. Split dependent work into sequential stages instead

### Gate blocks progress

- **Approval gate:** Choose "Continue", "Review changes", or "Abort pipeline"
- **Quality gate:** Fix Critical issues immediately, fix Important before proceeding
- **Verification gate:** Run the verification command and provide evidence

### Pipeline doesn't start

1. Check that the agent's SKILL.md exists at `.claude/skills/agents/<agent>/SKILL.md`
2. Check that the pipeline JSON is valid (run `python3 -c "import json; json.load(open('path'))"`)
3. Restart your Claude Code session

---

## File Locations

```
.claude/skills/agents/
├── pipeline-orchestrator/
│   ├── SKILL.md                          # Execution engine
│   └── references/
│       ├── pipeline-schema.md            # JSON schema docs
│       └── data-contracts.md             # Data flow docs
│
├── coding-agent/
│   ├── SKILL.md                          # /code router
│   └── references/pipelines/
│       ├── full-stack.json               # 5-stage build pipeline
│       ├── quality-gate.json             # 6-stage quality audit
│       ├── rapid-prototype.json          # 5-stage MVP pipeline
│       └── debug-chain.json              # 5-stage debug pipeline
│
├── docs-agent/
│   ├── SKILL.md                          # /docs router
│   └── references/pipelines/
│       ├── api-docs.json                 # 4-stage API docs
│       ├── project-docs.json             # 4-stage project scaffold
│       ├── content-pipeline.json         # 3-stage content creation
│       └── release-docs.json             # 4-stage release docs
│
├── startup-agent/
│   ├── SKILL.md                          # /startup router
│   └── references/pipelines/
│       ├── mvp-builder.json              # 5-stage MVP pipeline
│       ├── gtm-launch.json              # 4-stage GTM launch
│       ├── pitch-deck.json               # 4-stage pitch pipeline
│       └── product-analytics.json        # 4-stage analytics
│
├── GUIDE.md                              # This file
└── README.md                             # Quick reference
```
