#!/usr/bin/env bash
set -euo pipefail

export FACTORY_BMAD_LIVE_INSTALLER=1
export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest tests.test_factory_bmad_single_repo_pilot -v
