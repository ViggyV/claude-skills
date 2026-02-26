# Pipeline JSON Schema

## Top-Level Structure

```json
{
  "name": "string — kebab-case identifier (e.g. full-stack, quality-gate)",
  "description": "string — what this pipeline produces",
  "mode": "interactive | autonomous",
  "stages": ["array of Stage objects"]
}
```

## Stage Object

```json
{
  "id": "string — unique identifier, used for variable interpolation",
  "type": "skill | skill-chain | parallel",
  "description": "string — human-readable stage purpose",
  "skill": "string — skill path (type: skill only)",
  "skills": ["array of skill paths (type: skill-chain only)"],
  "branches": ["array of Branch objects (type: parallel only)"],
  "inputs": { "key": "value or ${stage_id.outputs.key}" },
  "outputs": { "key": "file path with optional {date}, {name}, {project} vars" },
  "gate": "optional Gate object"
}
```

### Stage Types

| Type | Required Fields | Behavior |
|------|----------------|----------|
| `skill` | `skill` | Invoke single skill, verify outputs |
| `skill-chain` | `skills` | Invoke skills sequentially, share context |
| `parallel` | `branches` | Dispatch branches as concurrent subagents |

## Branch Object (for `parallel` stages)

```json
{
  "id": "string — branch identifier",
  "type": "skill | skill-chain",
  "skill": "string (if type: skill)",
  "skills": ["array (if type: skill-chain)"],
  "inputs": { "key": "value" },
  "outputs": { "key": "file path" }
}
```

## Gate Object

```json
{
  "type": "approval | quality | verification",
  "prompt": "string — displayed to user or used as review context"
}
```

### Gate Types

| Type | Interactive Mode | Autonomous Mode |
|------|-----------------|-----------------|
| `approval` | Pause, ask user to confirm | Skip |
| `quality` | Run code review subagent | Run code review subagent |
| `verification` | Run verification commands | Run verification commands |

## Template Variables

Available in `outputs` paths:

| Variable | Resolves To | Example |
|----------|------------|---------|
| `{date}` | Today's date YYYY-MM-DD | `2025-01-15` |
| `{name}` | Slugified pipeline name or user-provided name | `my-feature` |
| `{project}` | Current directory name | `my-app` |

## Interpolation Variables

Available in `inputs` values:

| Syntax | Resolves To |
|--------|------------|
| `${stage_id.outputs.key}` | File path from a prior stage's outputs |

Example: `${brainstorm.outputs.design_doc}` → `docs/plans/2025-01-15-my-feature-design.md`

## Skill Path Format

Skills are referenced by their relative path under `.claude/skills/`:

```
obra-superpowers/skills/brainstorming
backend-api/api-designer
frameworks/fastapi-builder
code-quality/code-reviewer
business-communication/pitch-coach
anthropics-official/document-skills/pptx
```

## Validation Rules

1. All `id` fields must be unique within a pipeline
2. `${...}` interpolation can only reference stages that appear earlier in the array
3. Parallel branches must not share output file paths
4. At least one stage is required
5. `type` must be one of: `skill`, `skill-chain`, `parallel`
6. Gate `type` must be one of: `approval`, `quality`, `verification`
