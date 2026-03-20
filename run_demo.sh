#!/usr/bin/env bash
set -euo pipefail

SEED="${SEED:-7}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

export PYTHONHASHSEED=0

echo "Running synthetic demo with SEED=${SEED}"
"${PYTHON_BIN}" -m src.generate_data --seed "${SEED}"
"${PYTHON_BIN}" -m src.train_baseline
"${PYTHON_BIN}" -m src.score_signals
"${PYTHON_BIN}" -m src.evaluate

echo "Demo outputs refreshed under outputs/"
