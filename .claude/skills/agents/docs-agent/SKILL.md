---
name: docs-agent
description: Use when the user says /docs or asks for end-to-end documentation workflows like API docs, project scaffolding, content pipelines, or release documentation - routes to the right pipeline and invokes pipeline-orchestrator to execute it
---

# Docs Agent

I'm using the `docs-agent` skill to orchestrate a documentation pipeline.

## Available Pipelines

| Command | Pipeline | What It Does |
|---------|----------|-------------|
| `/docs api` | `api-docs.json` | API documenter → code documenter → examples → OpenAPI spec |
| `/docs project` | `project-docs.json` | Scaffold CLAUDE.md → ARCHITECTURE.md → DEVLOG.md → DOMAIN.md |
| `/docs content` | `content-pipeline.json` | Research → parallel content (Medium, LinkedIn, newsletter) → polish |
| `/docs release` | `release-docs.json` | PR review → commit helper → changelog → release notes |

## Process

### 1. Route

If the user specifies a pipeline (e.g. `/docs api`), load it directly.

If the user says just `/docs` or describes a task without specifying a pipeline, present the options:

Ask the user which pipeline fits their task:
- **API Documentation** — Generate comprehensive API docs with OpenAPI spec
- **Project Documentation** — Scaffold project docs using g4-templates structure
- **Content Pipeline** — Create multi-channel content from research
- **Release Documentation** — Generate changelog and release notes from commits

### 2. Gather Context

Ask the user for:
- **What to document** — the project, API, or topic
- **Project name** — for file naming (default: current directory name)
- **Mode** — interactive (pause at gates) or autonomous (skip approval gates)

### 3. Execute

1. Read the selected pipeline from `references/pipelines/{pipeline}.json`
2. Attach user context to the pipeline object
3. Invoke `pipeline-orchestrator` to execute the pipeline

**REQUIRED SUB-SKILL:** `agents/pipeline-orchestrator`

### 4. Complete

After the orchestrator finishes, summarize:
- What was documented
- Key output files and their locations
- Any gaps or areas needing manual review
- Next steps

## Integration

- **Invoked by:** User via `/docs` or "document this", "write docs", "create changelog"
- **Invokes:** `pipeline-orchestrator` (always), plus skills defined in pipeline JSONs
- **Related stacks:** `content-creation`, `document-processing`
