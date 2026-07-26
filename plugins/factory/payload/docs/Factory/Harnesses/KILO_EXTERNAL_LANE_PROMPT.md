# Kilo External Lane Mode Prompt

Use this prompt in Codex or another non-Kilo orchestrator when you want Kilo Code CLI to run selected Factory stages with explicit model routing.

```text
Run this Factory planning run using Kilo External Lane Mode.

Repository:
<ABSOLUTE_REPO_PATH>

Run:
<RUN_ID>

Rules:
- You are the orchestrator.
- Do not open an interactive Kilo session.
- Do not ask Kilo to launch nested Kilo processes.
- For each Kilo-routed stage, call `./scripts/factoryctl kilo-stage`.
- Wait for each Kilo subprocess to exit before starting the next stage.
- Run `./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>` after each stage.
- If `kilo-stage` fails, inspect its JSON evidence under `docs/Factory/runs/<RUN_ID>/kilo_stage_runs/` and stop unless the fix is deterministic and bounded.

Model routing:
- Stage B Red Team: kilo/anthropic/claude-opus-4.8, variant high
- Stage C Blue Team: kilo/openai/gpt-5.5, variant high
- Stage D Purple Gate: kilo/z-ai/glm-5.2, variant high
- Stage I Envelope Red/Blue: choose the route specified in the pack or ask me before continuing.

Command shape:
./scripts/factoryctl kilo-stage --run <RUN_ID> --stage <STAGE> --model <KILO_MODEL_ID> --variant high --auto --timeout-seconds 900

Continue only while stage-lint passes and the run remains within the locked Factory scope.
```
