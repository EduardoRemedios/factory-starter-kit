#!/usr/bin/env bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1
python3 scripts/build_factory_bmad_plugins.py --check
SKILL_HOME="${CODEX_HOME:-$HOME/.codex}/skills/.system"
python3 "$SKILL_HOME/plugin-creator/scripts/validate_plugin.py" plugins/factory-bmad >/dev/null
echo "Codex companion plugin validation: PASS"
for skill in plugin-src/factory-bmad/skills/*; do
  python3 "$SKILL_HOME/skill-creator/scripts/quick_validate.py" "$skill"
done
python3 -m unittest \
  tests.test_factory_bmad_plugin_build \
  tests.test_factory_bmad_bootstrap \
  tests.test_factory_bmad_policy \
  tests.test_factory_bmad_promotion \
  tests.test_factory_bmad_preflight \
  tests.test_factory_bmad_output \
  tests.test_factory_bmad_docs_privacy -v
bash scripts/knowledge_lint.sh
git diff --check
