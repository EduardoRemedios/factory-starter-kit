#!/usr/bin/env bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1
echo "verification-boundary-v2"
echo "DETERMINISTIC_PACKAGED_PRETOOLUSE"
python3 -m unittest tests.test_factory_bmad_enforcement -v
python3 scripts/build_factory_bmad_plugins.py --check
bash scripts/verify_factory_bmad_claude_composition.sh
echo "ADVISORY_MODEL_CHOICE_SMOKE=NOT_AUTHORIZED_NOT_RUN"
