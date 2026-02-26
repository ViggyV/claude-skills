---
name: agent-help
description: Use when the user asks about agent pipelines, how to use /code /docs /startup commands, how to create custom pipelines, or needs help troubleshooting agent workflows - explains the agent orchestrator system and guides pipeline creation
---

# Agent Help

I'm using the `agent-help` skill to explain the agent pipeline system.

## Quick Reference

### Available Commands

| Command | Agent | What It Does |
|---------|-------|-------------|
| `/code` | Coding Agent | Full-stack builds, quality audits, prototypes, debugging |
| `/code full-stack` | Coding Agent | brainstorm → plan → parallel build → review → finish |
| `/code quality` | Coding Agent | code-review → bugs → security → tests → perf → verify |
| `/code prototype` | Coding Agent | api → db → FastAPI → React → Docker |
| `/code debug` | Coding Agent | debug → root-cause → fix → test → verify |
| `/docs` | Docs Agent | API docs, project scaffolding, content, releases |
| `/docs api` | Docs Agent | documenter → code-docs → examples → OpenAPI |
| `/docs project` | Docs Agent | CLAUDE.md → ARCHITECTURE → DEVLOG → DOMAIN |
| `/docs content` | Docs Agent | research → parallel(Medium, LinkedIn, newsletter) → polish |
| `/docs release` | Docs Agent | PRs → commits → changelog → release-notes |
| `/startup` | Startup Agent | MVPs, go-to-market, pitch decks, analytics |
| `/startup mvp` | Startup Agent | brainstorm → Hormozi → plan → parallel build → deploy |
| `/startup gtm` | Startup Agent | research → pitch → parallel(5 channels) → email |
| `/startup pitch` | Startup Agent | Hormozi → coach → PPTX → outreach email |
| `/startup analytics` | Startup Agent | metrics → pipeline → D3.js → PPTX report |

### How It Works

1. Say `/code`, `/docs`, or `/startup` (optionally with a pipeline name)
2. The super-agent asks what you want to build and which mode to use
3. It loads the pipeline JSON and invokes the pipeline-orchestrator
4. The orchestrator runs each stage, passing outputs between them
5. Gates pause for approval, run code review, or require verification
6. On completion, you get a summary of all outputs and next steps

### Modes

- **Interactive** (default): Pauses at every gate for your approval
- **Autonomous**: Skips approval gates, still enforces quality and verification

### Creating Custom Pipelines

Read the full guide: `agents/GUIDE.md`

1. Create a JSON file in `agents/<agent>/references/pipelines/<name>.json`
2. Define stages with `skill`, `skill-chain`, or `parallel` types
3. Add gates (`approval`, `quality`, `verification`) between stages
4. Declare `outputs` and `inputs` for data passing
5. Update the agent's SKILL.md routing table

### Troubleshooting

- **Pipeline won't start:** Check SKILL.md exists, JSON is valid, restart session
- **Stage fails:** Check skill path exists, verify input files are on disk
- **Parallel conflict:** Ensure branches write to different output paths
- **Gate blocks:** Fix Critical issues from quality gate, provide evidence for verification

For the complete guide with architecture diagrams, JSON schema, examples, and custom pipeline tutorial, read `agents/GUIDE.md`.
