# Agent Pipelines

Super-agents that chain multiple skills into automated, multi-stage pipelines. Say `/code full-stack` and watch it brainstorm, plan, build in parallel, review, and finish — automatically passing outputs between stages.

## Architecture

```
User → Super-Agent (router) → Pipeline JSON → Pipeline Orchestrator → Skills
```

1. **Super-agent** (coding/docs/startup) presents pipeline options to the user
2. User selects a pipeline → agent loads the JSON definition
3. Agent invokes **pipeline-orchestrator** as a sub-skill
4. Orchestrator resolves variables, creates task list, executes stages
5. At gates: pause for approval / run code review / require verification
6. On completion: summarize outputs and next steps

## Skills

### Pipeline Orchestrator

**Location:** `agents/pipeline-orchestrator/`

The execution engine. Never invoked directly by users — always called by a super-agent.

**What it does:**
- Reads pipeline JSON definitions
- Resolves template variables (`{date}`, `{name}`, `{project}`)
- Executes stages sequentially: `skill`, `skill-chain`, `parallel`
- Manages data flow between stages via `${stage_id.outputs.key}` interpolation
- Enforces quality gates (approval, quality review, verification)
- Stops immediately on failure with a clear error report

**Reference files:**
- `references/pipeline-schema.md` — JSON schema documentation
- `references/data-contracts.md` — How stages pass data via files on disk

**When to use:** You don't invoke this directly. The coding/docs/startup agents call it.

---

### Coding Agent

**Location:** `agents/coding-agent/`
**Trigger:** `/code` or `/code <pipeline>`

Routes coding tasks to the right pipeline.

| Pipeline | Command | Description |
|----------|---------|-------------|
| **full-stack** | `/code full-stack` | End-to-end feature: brainstorm → plan → parallel build (backend + frontend + infra) → code review → finish |
| **quality-gate** | `/code quality` | Comprehensive audit: code review → bug hunt → security → tests → performance → verify |
| **rapid-prototype** | `/code prototype` | Fast MVP: API design → database → FastAPI → React → Docker |
| **debug-chain** | `/code debug` | Systematic fix: debugging → root cause → bug hunt → regression tests → verify |

**How to use:**
```
/code                    # Shows all pipelines, asks which one
/code full-stack         # Jumps straight to full-stack pipeline
/code debug              # Starts systematic debugging chain
```

**What it chains:**
- obra/superpowers skills (brainstorming, planning, code review, verification)
- Backend skills (api-designer, database-schema, fastapi-builder)
- Frontend skills (react-component, ui-builder)
- DevOps skills (docker-composer, ci-cd-builder)
- Quality skills (code-reviewer, bug-hunter, security-auditor, test-generator, performance-profiler)

---

### Docs Agent

**Location:** `agents/docs-agent/`
**Trigger:** `/docs` or `/docs <pipeline>`

Routes documentation tasks to the right pipeline.

| Pipeline | Command | Description |
|----------|---------|-------------|
| **api-docs** | `/docs api` | API docs: documenter → code docs → usage examples → OpenAPI spec |
| **project-docs** | `/docs project` | Project scaffold: CLAUDE.md → ARCHITECTURE.md → DEVLOG.md → DOMAIN.md |
| **content-pipeline** | `/docs content` | Multi-channel: research → parallel (Medium + LinkedIn + newsletter) → polish |
| **release-docs** | `/docs release` | Release: PR review → commit analysis → CHANGELOG → release notes |

**How to use:**
```
/docs                    # Shows all pipelines, asks which one
/docs api                # Generate API documentation
/docs content            # Create multi-channel content from research
```

**What it chains:**
- API skills (api-documenter, endpoint-tester, api-designer)
- Code quality skills (code-documenter)
- Content skills (medium-post, linkedin-post-formatter, newsletter, content-trend-researcher)
- Version control skills (pr-reviewer, commit-helper)
- Document skills (pptx for project docs scaffold reference)

---

### Startup Agent

**Location:** `agents/startup-agent/`
**Trigger:** `/startup` or `/startup <pipeline>`

Routes startup/business tasks to the right pipeline.

| Pipeline | Command | Description |
|----------|---------|-------------|
| **mvp-builder** | `/startup mvp` | Idea to product: brainstorm → Hormozi offer → plan → parallel build → deploy |
| **gtm-launch** | `/startup gtm` | Go-to-market: research → pitch → parallel content (5 channels) → email |
| **pitch-deck** | `/startup pitch` | Investor pitch: Hormozi offer → pitch coach → PPTX deck → outreach email |
| **product-analytics** | `/startup analytics` | Analytics: KPI spec → data pipeline → D3.js dashboards → PPTX report |

**How to use:**
```
/startup                 # Shows all pipelines, asks which one
/startup mvp             # Build an MVP from scratch
/startup pitch           # Create a pitch deck
```

**What it chains:**
- obra/superpowers skills (brainstorming, planning)
- Business skills (alex-hormozi-pitch, pitch-coach, email-polisher, content-trend-researcher)
- Content skills (linkedin-post-formatter, medium-post, newsletter, video-script)
- Data skills (analytics-builder, data-pipeline)
- Visualization skills (d3js-visualization)
- Document skills (pptx)
- Build skills (api-designer, database-schema, fastapi-builder, react-component, docker-composer)

---

## Pipeline JSON Format

Each pipeline is a declarative JSON file in `references/pipelines/`:

```json
{
  "name": "pipeline-name",
  "description": "What this pipeline produces",
  "mode": "interactive",
  "stages": [
    {
      "id": "stage-id",
      "type": "skill",
      "skill": "category/skill-name",
      "description": "What this stage does",
      "inputs": { "key": "${prior_stage.outputs.key}" },
      "outputs": { "key": "path/to/{date}-{name}-file.md" },
      "gate": { "type": "approval", "prompt": "Review before continuing?" }
    }
  ]
}
```

**Stage types:**
- `skill` — Invoke a single skill
- `skill-chain` — Invoke skills sequentially, sharing context
- `parallel` — Dispatch branches as concurrent subagents

**Gate types:**
- `approval` — User confirms (skipped in autonomous mode)
- `quality` — Code review subagent runs (always enforced)
- `verification` — Evidence-based check (always enforced)

**Template variables:** `{date}`, `{name}`, `{project}`
**Interpolation:** `${stage_id.outputs.key}` resolves to file paths from prior stages

---

## Modes

| Mode | Approval Gates | Quality Gates | Verification Gates |
|------|---------------|---------------|-------------------|
| **Interactive** (default) | Pause & ask | Run review | Run verification |
| **Autonomous** | Skip | Run review | Run verification |

---

## How to Download and Install

1. Clone or copy the `agents/` directory into your `.claude/skills/` folder:
   ```bash
   cp -r agents/ .claude/skills/agents/
   ```

2. Add the agent stacks to your `.claude/skill-stacks.json` (see entries for `coding-agent`, `docs-agent`, `startup-agent`)

3. Restart your Claude Code session

4. Use `/code`, `/docs`, or `/startup` to invoke

---

## Builds On (Doesn't Replace)

These agents orchestrate existing skills — they don't duplicate them:

- **Plans** follow obra's `docs/plans/YYYY-MM-DD-<name>.md` format
- **Code review** uses obra's `requesting-code-review` template
- **Verification** uses `verification-before-completion` (evidence, not claims)
- **Finish** uses `finishing-a-development-branch` (4 options: merge/PR/keep/discard)
- **Parallel dispatch** follows `dispatching-parallel-agents` constraints (independent work only)

---

## Additional Documentation

| Document | What It Covers |
|----------|---------------|
| [`GUIDE.md`](GUIDE.md) | Complete guide: architecture diagrams, all pipelines, JSON format tutorial, custom pipeline creation, troubleshooting |
| [`agent-help/SKILL.md`](agent-help/SKILL.md) | Quick-reference skill — activated when users ask about agent commands |
| [`pipeline-creator/SKILL.md`](pipeline-creator/SKILL.md) | Skill for creating custom pipelines step-by-step |
| [`pipeline-orchestrator/references/pipeline-schema.md`](pipeline-orchestrator/references/pipeline-schema.md) | Full JSON schema specification |
| [`pipeline-orchestrator/references/data-contracts.md`](pipeline-orchestrator/references/data-contracts.md) | How stages pass data via files on disk |
| [`pipeline-orchestrator/references/skill-index.md`](pipeline-orchestrator/references/skill-index.md) | Every skill used across all 12 pipelines (38 unique skills) |
