---
name: startup-agent
description: Use when the user says /startup or asks for end-to-end startup workflows like MVP builds, go-to-market launches, pitch decks, or product analytics - routes to the right pipeline and invokes pipeline-orchestrator to execute it
---

# Startup Agent

I'm using the `startup-agent` skill to orchestrate a startup pipeline.

## Available Pipelines

| Command | Pipeline | What It Does |
|---------|----------|-------------|
| `/startup mvp` | `mvp-builder.json` | Brainstorm → Hormozi pitch → plan → parallel build → deploy |
| `/startup gtm` | `gtm-launch.json` | Research → pitch coaching → parallel content (LinkedIn, Medium, newsletter, video, email) |
| `/startup pitch` | `pitch-deck.json` | Hormozi pitch → pitch coach → PPTX → email polish |
| `/startup analytics` | `product-analytics.json` | Analytics builder → data pipeline → D3.js dashboards → PPTX report |

## Process

### 1. Route

If the user specifies a pipeline (e.g. `/startup mvp`), load it directly.

If the user says just `/startup` or describes a task without specifying a pipeline, present the options:

Ask the user which pipeline fits their task:
- **MVP Builder** — Go from idea to deployed product with Hormozi-style offer design
- **GTM Launch** — Create multi-channel go-to-market content from a single brief
- **Pitch Deck** — Build investor pitch with presentation and outreach email
- **Product Analytics** — Set up analytics dashboards and investor-ready reports

### 2. Gather Context

Ask the user for:
- **What to build/launch/pitch** — brief description of the product or idea
- **Project name** — for file naming (default: current directory name)
- **Mode** — interactive (pause at gates) or autonomous (skip approval gates)

### 3. Execute

1. Read the selected pipeline from `references/pipelines/{pipeline}.json`
2. Attach user context to the pipeline object
3. Invoke `pipeline-orchestrator` to execute the pipeline

**REQUIRED SUB-SKILL:** `agents/pipeline-orchestrator`

### 4. Complete

After the orchestrator finishes, summarize:
- What was built/created/launched
- Key output files and their locations
- Revenue/growth recommendations from the pipeline
- Next steps

## Integration

- **Invoked by:** User via `/startup` or "build MVP", "create pitch deck", "launch product"
- **Invokes:** `pipeline-orchestrator` (always), plus skills defined in pipeline JSONs
- **Related stacks:** `business-pitch`, `rapid-poc`, `full-stack-ai`
