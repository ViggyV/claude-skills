---
name: coding-agent
description: Use when the user says /code or asks for end-to-end coding workflows like full-stack builds, quality audits, rapid prototypes, or debug chains - routes to the right pipeline and invokes pipeline-orchestrator to execute it
---

# Coding Agent

I'm using the `coding-agent` skill to orchestrate a coding pipeline.

## Available Pipelines

| Command | Pipeline | What It Does |
|---------|----------|-------------|
| `/code full-stack` | `full-stack.json` | Brainstorm → plan → parallel build (backend, frontend, infra) → quality review → finish |
| `/code quality` | `quality-gate.json` | Code review → bug hunt → security audit → tests → performance → verify |
| `/code prototype` | `rapid-prototype.json` | API design → database → FastAPI → React → Docker |
| `/code debug` | `debug-chain.json` | Systematic debugging → root cause → bug hunt → test → verify |

## Process

### 1. Route

If the user specifies a pipeline (e.g. `/code full-stack`), load it directly.

If the user says just `/code` or describes a task without specifying a pipeline, present the options:

Ask the user which pipeline fits their task:
- **Full-Stack Build** — End-to-end feature development with parallel workstreams
- **Quality Gate** — Comprehensive code quality audit and fixes
- **Rapid Prototype** — Fast MVP from idea to containerized app
- **Debug Chain** — Systematic debugging with root cause analysis

### 2. Gather Context

Ask the user for:
- **What to build/fix/review** — brief description of the task
- **Project name** — for file naming (default: current directory name)
- **Mode** — interactive (pause at gates) or autonomous (skip approval gates)

### 3. Execute

1. Read the selected pipeline from `references/pipelines/{pipeline}.json`
2. Attach user context to the pipeline object
3. Invoke `pipeline-orchestrator` to execute the pipeline

**REQUIRED SUB-SKILL:** `agents/pipeline-orchestrator`

### 4. Complete

After the orchestrator finishes, summarize:
- What was built/fixed/reviewed
- Key output files and their locations
- Any issues found during quality gates
- Next steps or follow-up actions

## Integration

- **Invoked by:** User via `/code` or "help me build/debug/review"
- **Invokes:** `pipeline-orchestrator` (always), plus skills defined in pipeline JSONs
- **Related stacks:** `full-stack-ai`, `backend-development`, `code-quality`
