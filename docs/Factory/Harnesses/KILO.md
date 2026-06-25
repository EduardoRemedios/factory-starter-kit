# Kilo Code CLI Harness Adapter

## Version
v0.3

## Change Log
- v0.3 (2026-06-25): Made Kilo External Lane Mode the supported optional pattern for reliable Kilo routing and clarified the Codex/shell orchestration workflow.
- v0.2 (2026-06-25): Added nested-Kilo guard, per-run stage lock guidance, and timeout guidance after field testing.
- v0.1 (2026-06-25): Initial Kilo Code CLI adapter for model-routed Factory stage lanes.

## Purpose

Use this adapter when running Factory stages through Kilo Code CLI.

This adapter may define model routing, Kilo command shape, permission posture, and evidence capture. It must not change Factory Core stage contracts, required artifacts, validator semantics, or human Go requirements.

## Kilo External Lane Mode

Supported optional pattern:

```text
Codex or neutral shell = orchestrator
factoryctl kilo-stage = bounded stage launcher
Kilo Code CLI = model-routed worker subprocess
Factory artifacts = source of truth
stage-lint / pack-lint = deterministic gates
```

Kilo should be the worker lane, not the parent orchestrator, for this adapter.

Recommended:
- Run `factoryctl kilo-stage` from a neutral shell, Codex, or another non-Kilo orchestrator.
- Let `factoryctl kilo-stage` invoke exactly one `kilo run` process for the selected Factory stage.
- Wait for that command to exit before starting the next stage.

Avoid:
- Running `factoryctl kilo-stage` from inside an active Kilo Code session.
- Asking a Kilo agent to launch more `kilo run` processes.
- Starting the next stage while a prior Kilo lane is still running or unclear.

The runner refuses nested Kilo by default. Override only for deliberate debugging:

```bash
./scripts/factoryctl kilo-stage \
  --run <RUN_ID> \
  --stage B \
  --model kilo/anthropic/claude-opus-4.8 \
  --allow-nested-kilo
```

Kilo Native Mode, where an interactive Kilo session owns the whole Factory run and switches active models in-session, is a different harness pattern. It is not implemented by `factoryctl kilo-stage`.

## Model Routing

Recommended starting lanes:

| Factory Work | Kilo Model | Notes |
|---|---|---|
| Red Team stages B and I | `kilo/anthropic/claude-opus-4.8` | Strong adversarial review lane. |
| Blue Team synthesis and hardening | `kilo/openai/gpt-5.5` | Use for synthesis, conflict resolution, and final hardening. |
| Third-opinion or alternate critique | `kilo/z-ai/glm-5.2` | Useful as a variance check before Purple Gate. |

Use the exact model IDs returned by:

```bash
kilo models --refresh --verbose
```

Model availability depends on the configured Kilo account, organization, gateway, and provider access.

## Factory Runner Command

The starter kit includes a conservative Kilo lane runner:

```bash
./scripts/factoryctl kilo-stage \
  --run <RUN_ID> \
  --stage B \
  --model kilo/anthropic/claude-opus-4.8 \
  --variant high \
  --timeout-seconds 900 \
  --auto
```

From Codex or a neutral shell, the orchestration loop is:

```bash
./scripts/factoryctl kilo-stage --run <RUN_ID> --stage B --model kilo/anthropic/claude-opus-4.8 --variant high --auto --timeout-seconds 900
./scripts/factoryctl stage-lint --run <RUN_ID> --stage B

./scripts/factoryctl kilo-stage --run <RUN_ID> --stage C --model kilo/openai/gpt-5.5 --variant high --auto --timeout-seconds 900
./scripts/factoryctl stage-lint --run <RUN_ID> --stage C
```

Dry-run the generated command and prompt without invoking Kilo:

```bash
./scripts/factoryctl kilo-stage \
  --run <RUN_ID> \
  --stage B \
  --model kilo/anthropic/claude-opus-4.8 \
  --dry-run
```

The runner:
1. generates a stage-bounded prompt
2. passes the selected Kilo model with `kilo run --model`
3. snapshots repo files before and after the Kilo process
4. fails if Kilo changes files outside the stage's allowed output artifacts and handoff
5. uses a per-run lock file so overlapping stage runs fail closed
6. records timeout failures instead of leaving ambiguous state
7. writes a JSON run record under `docs/Factory/runs/<RUN_ID>/kilo_stage_runs/`

The generated worker prompt also tells Kilo not to launch `kilo`, `kilocode`, or `factoryctl kilo-stage` from inside the worker lane.

Run `stage-lint` after a successful Kilo lane:

```bash
./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>
```

## Permission Posture

Prefer explicit Kilo permission config over broad auto-approval.

For planning-only Factory stages, Kilo should be allowed to read the repo and write only the run artifacts for the current stage. The `factoryctl kilo-stage` runner checks this after the process exits, but it is not a sandbox.

Do not use `--dangerously-skip-permissions` for Factory-governed work.

Use `--auto` only when:
1. the run is `PLANNING_ONLY`, or execution has explicit authorization
2. allowed write paths are stage-bounded
3. the runner's post-run boundary check is enabled
4. a human will review pack evidence before Go or merge

Use `--timeout-seconds` for every non-dry run. The default command path uses 900 seconds. If a stage times out, inspect the JSON evidence and active processes before retrying.

## Example Red / Blue / Third-Opinion Cycle

Stage B Red Team:

```bash
./scripts/factoryctl kilo-stage \
  --run RUN_YYYYMMDD_HHMM_factory \
  --stage B \
  --model kilo/anthropic/claude-opus-4.8 \
  --variant high \
  --auto
./scripts/factoryctl stage-lint --run RUN_YYYYMMDD_HHMM_factory --stage B
```

Stage C Blue Team:

```bash
./scripts/factoryctl kilo-stage \
  --run RUN_YYYYMMDD_HHMM_factory \
  --stage C \
  --model kilo/openai/gpt-5.5 \
  --variant high \
  --auto
./scripts/factoryctl stage-lint --run RUN_YYYYMMDD_HHMM_factory --stage C
```

Optional third-opinion review before Purple Gate:

```bash
kilo run \
  --dir . \
  --model kilo/z-ai/glm-5.2 \
  --variant high \
  --format json \
  "Review docs/Factory/runs/RUN_YYYYMMDD_HHMM_factory/pack/intent.md and intent_redteam.md. Do not edit files. Return only blocking concerns for Purple Gate."
```

## Guardrails

- Keep Factory artifacts on disk as source of truth.
- Do not treat Kilo session history, Kilo Gateway state, or chat text as approval authority.
- Do not nest Kilo inside Kilo for normal Factory work.
- Do not start Stage C until the Stage B `factoryctl kilo-stage` process has exited and `stage-lint --stage B` passes.
- Do not let one model lane overwrite another model lane's artifact outside the stage contract.
- If Kilo asks a follow-up question in autonomous mode, the stage prompt must require a FAIL handoff rather than scope guessing.
- If model access, provider identity, or organization routing is unclear, run `kilo models --refresh --verbose` and record the resolved model ID in run metrics.
