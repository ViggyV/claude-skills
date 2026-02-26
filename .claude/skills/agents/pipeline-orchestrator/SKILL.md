---
name: pipeline-orchestrator
description: Use when a super-agent (coding-agent, docs-agent, startup-agent) needs to execute a multi-stage pipeline defined in JSON - resolves template variables, manages sequential/parallel/chain stage execution, enforces quality gates, and passes data between stages via file outputs
---

# Pipeline Orchestrator

I'm using the `pipeline-orchestrator` skill to execute a multi-stage pipeline.

## Iron Law

```
NO STAGE ADVANCES WITHOUT VERIFIED OUTPUTS FROM THE PREVIOUS STAGE.
```

## Input Contract

Receive a pipeline JSON object with:
- `name` — pipeline identifier
- `description` — what this pipeline produces
- `mode` — `interactive` (all gates active) or `autonomous` (skip approval gates)
- `stages` — ordered array of stage definitions
- `context` — user's original request/description (passed by the calling agent)

## Execution Protocol

### 1. Initialize

1. Read the pipeline JSON (passed inline or from a `references/pipelines/*.json` file)
2. Resolve template variables in all `outputs` paths:
   - `{date}` → `YYYY-MM-DD` (today)
   - `{name}` → slugified pipeline name or user-provided name
   - `{project}` → current directory name
3. Create a task list from stages using TodoWrite
4. Announce: "Executing pipeline: **{name}** — {description}"
5. List all stages with descriptions for the user

### 2. Execute Stages (sequential order)

For each stage in `stages`:

#### Type: `skill`
1. Announce: "Stage {id}: {description}"
2. Resolve `inputs` — interpolate `${stage_id.outputs.key}` from prior stage outputs
3. Invoke the skill via the Skill tool (path format: `category/skill-name`)
4. Verify declared `outputs` exist on disk (Read or Glob)
5. Record outputs for downstream interpolation

#### Type: `skill-chain`
1. Announce: "Stage {id}: {description} ({n} skills in sequence)"
2. For each skill in `skills` array:
   - Invoke via Skill tool
   - Pass context from the previous skill in the chain
3. Verify final outputs exist

#### Type: `parallel`
1. Announce: "Stage {id}: {description} — dispatching {n} parallel branches"
2. Validate branches are independent (no shared output paths)
3. Dispatch each branch as a subagent using the Task tool:
   - Each branch gets its own resolved inputs
   - Branch prompt includes: skill(s) to invoke, inputs, expected outputs
   - Follow `dispatching-parallel-agents` constraints: focused, self-contained, specific
4. Wait for all branches to complete
5. Review branch results for conflicts
6. Verify all declared outputs exist

### 3. Enforce Gates

When a stage has a `gate`:

#### `approval` gate
- **Interactive mode:** Present the gate prompt to the user via AskUserQuestion. Options: "Continue" / "Review changes" / "Abort pipeline"
- **Autonomous mode:** Skip, log "Gate skipped (autonomous mode)"

#### `quality` gate
- Dispatch a code-reviewer subagent using `requesting-code-review` pattern
- Review feedback: fix Critical issues immediately, fix Important before proceeding
- Both modes: always enforce quality gates

#### `verification` gate
- Use `verification-before-completion` pattern: run verification commands, require evidence
- Both modes: always enforce verification gates

### 4. Handle Failures

If any stage fails:
1. Stop the pipeline immediately
2. Report: "Pipeline **{name}** failed at stage **{stage_id}**: {error}"
3. List completed stages and their outputs
4. List remaining stages that were not executed
5. Do NOT attempt to continue past a failed stage

### 5. Complete

After all stages succeed:
1. Announce: "Pipeline **{name}** completed successfully"
2. List all outputs with their file paths
3. If the pipeline context suggests finishing a branch, offer `finishing-a-development-branch`

## Variable Interpolation

Outputs from prior stages are available via `${stage_id.outputs.key}`:
```
${brainstorm.outputs.design_doc}  → resolves to the actual file path
${plan.outputs.plan_file}         → resolves to the plan's file path
```

If a referenced variable doesn't exist, fail the stage with a clear error message.

## Integration

- **Called by:** `coding-agent`, `docs-agent`, `startup-agent`
- **Uses:** `requesting-code-review`, `verification-before-completion`, `finishing-a-development-branch`, `dispatching-parallel-agents`
- **Never called directly by users** — always invoked by a super-agent

## Red Flags

- Never skip a `quality` or `verification` gate, even in autonomous mode
- Never advance past a stage whose outputs don't exist
- Never run parallel branches that share output files
- Never guess output paths — always verify with Glob or Read
