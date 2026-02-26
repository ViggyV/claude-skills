# Data Contracts: How Stages Pass Data

## Principle

Stages communicate through files on disk, not through in-memory state. This survives context loss, enables parallel branches, and follows the obra plan-file pattern.

## Output Declaration

Each stage declares what files it produces:

```json
{
  "outputs": {
    "design_doc": "docs/plans/{date}-{name}-design.md",
    "api_spec": "docs/api/{name}-openapi.yaml"
  }
}
```

The orchestrator resolves template variables at pipeline start and tracks resolved paths.

## Input Resolution

Downstream stages reference upstream outputs:

```json
{
  "inputs": {
    "plan_file": "${plan.outputs.plan_file}",
    "design_doc": "${brainstorm.outputs.design_doc}"
  }
}
```

The orchestrator resolves `${stage_id.outputs.key}` to the actual file path after the referenced stage completes.

## Resolution Flow

```
1. Pipeline starts
2. Resolve all template vars ({date}, {name}, {project}) in output paths
3. For each stage:
   a. Resolve input interpolation (${...}) using completed stage outputs
   b. Execute stage
   c. Verify output files exist on disk
   d. Store resolved output paths for downstream use
```

## Contract Rules

### Producers (output stages)
- MUST create files at the declared output paths
- File format is determined by the skill (markdown for plans, JSON for configs, etc.)
- The orchestrator verifies file existence after stage completion
- If an output file is missing, the stage is considered failed

### Consumers (input stages)
- Receive resolved file paths, not file contents
- Must Read the file themselves to use the content
- If an input references a non-existent stage or output key, the pipeline fails before execution

### Parallel Branches
- Each branch has independent output paths — no overlaps allowed
- The orchestrator validates no output path conflicts before dispatching
- Branch outputs are merged into the stage's output namespace after all branches complete
- Access pattern: `${build.outputs.backend_api}`, `${build.outputs.frontend_app}`

## Common Output Patterns

| Stage Type | Typical Output | Path Convention |
|------------|---------------|-----------------|
| Brainstorming | Design document | `docs/plans/{date}-{name}-design.md` |
| Planning | Implementation plan | `docs/plans/{date}-{name}.md` |
| Code generation | Source files | Created by the skill in project directories |
| Code review | Review report | `docs/reviews/{date}-{name}-review.md` |
| Documentation | Doc files | `docs/{name}/` or project root |
| Presentations | PPTX file | `output/{name}-deck.pptx` |

## Error Cases

| Error | Behavior |
|-------|----------|
| Output file missing after stage | Stage fails, pipeline stops |
| Input references unknown stage | Pipeline fails at validation (before execution) |
| Input references unknown output key | Pipeline fails at stage start |
| Parallel branches share output path | Pipeline fails at validation |
| Template variable unresolvable | Pipeline fails at initialization |
