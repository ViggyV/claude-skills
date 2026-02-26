---
name: pipeline-creator
description: Use when the user wants to create a custom agent pipeline, add a new pipeline to an existing agent, or design a multi-stage workflow that chains skills together - guides through pipeline JSON creation with validation
---

# Pipeline Creator

I'm using the `pipeline-creator` skill to create a custom agent pipeline.

## Process

### 1. Understand the Workflow

Ask the user:
- **What is the end goal?** (e.g., "build a SaaS app", "create training materials")
- **Which agent should own this?** (`coding-agent`, `docs-agent`, `startup-agent`, or a new one)
- **What stages are needed?** List the steps from start to finish

### 2. Map Stages to Skills

For each stage, identify the right skill from the library. Read `QUICK_REFERENCE.md` to find matching skills.

Common skill paths:
```
obra-superpowers/skills/brainstorming
obra-superpowers/skills/writing-plans
obra-superpowers/skills/requesting-code-review
obra-superpowers/skills/verification-before-completion
obra-superpowers/skills/finishing-a-development-branch
backend-api/api-designer
backend-api/database-schema
frameworks/fastapi-builder
frameworks/react-component
devops-infrastructure/docker-composer
code-quality/code-reviewer
code-quality/test-generator
code-quality/security-auditor
business-communication/pitch-coach
business-communication/email-polisher
anthropics-official/document-skills/pptx
data-engineering/analytics-builder
community/d3js-visualization
```

### 3. Determine Stage Types

For each stage, choose:
- **`skill`** — single skill invocation
- **`skill-chain`** — multiple skills in sequence (same context)
- **`parallel`** — independent branches dispatched as subagents

**Parallel rule:** Branches MUST be independent. No shared files. No shared state. If work depends on each other, use sequential stages or a skill-chain instead.

### 4. Design Data Flow

For each stage:
- **Outputs:** What files does this stage produce? Use template vars: `{date}`, `{name}`, `{project}`
- **Inputs:** What does this stage need from earlier stages? Use interpolation: `${stage_id.outputs.key}`

### 5. Add Gates

Decide where to add checkpoints:
- **`approval`** — user reviews before continuing (skipped in autonomous mode)
- **`quality`** — code review subagent runs (always enforced)
- **`verification`** — evidence-based check (always enforced)

**Best practices:**
- Add approval gates after design/planning stages
- Add quality gates after build/parallel stages
- Add verification gates before the final stage

### 6. Generate the JSON

Create the pipeline file at:
```
.claude/skills/agents/<agent>/references/pipelines/<name>.json
```

Validate the JSON:
```bash
python3 -c "import json; json.load(open('path/to/pipeline.json')); print('valid')"
```

### 7. Update the Agent

Add the new pipeline to the agent's SKILL.md routing table:
- Add a row to the "Available Pipelines" table
- Add a routing case in the "Route" section

### 8. Validate

Check against these rules:
- [ ] All `id` fields are unique
- [ ] `${...}` interpolation only references earlier stages
- [ ] Parallel branches have no shared output paths
- [ ] At least one stage exists
- [ ] All skill paths match existing skills in `.claude/skills/`
- [ ] JSON is valid (no trailing commas, proper quoting)

## Pipeline Template

```json
{
  "name": "my-pipeline",
  "description": "What this pipeline produces",
  "mode": "interactive",
  "stages": [
    {
      "id": "stage-1",
      "type": "skill",
      "skill": "category/skill-name",
      "description": "What this stage does",
      "outputs": {
        "output_key": "docs/{date}-{name}-output.md"
      },
      "gate": {
        "type": "approval",
        "prompt": "Stage 1 complete. Continue?"
      }
    },
    {
      "id": "stage-2",
      "type": "skill",
      "skill": "category/another-skill",
      "description": "Next stage",
      "inputs": {
        "input_key": "${stage-1.outputs.output_key}"
      },
      "outputs": {
        "final_output": "output/{name}-result.md"
      }
    }
  ]
}
```

## Integration

- **Invoked by:** User who wants to create a custom pipeline
- **References:** `pipeline-orchestrator/references/pipeline-schema.md` for full schema
- **References:** `pipeline-orchestrator/references/data-contracts.md` for data flow rules
