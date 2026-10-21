#!/usr/bin/env bash
# Entry point for this benchmark.
#
#   ./run.sh          full run, rewrites results/raw.txt and results/summary.md
#   QUICK=1 ./run.sh  smoke test, finishes in under ten seconds, writes nothing
#
# The thread limits are exported before Python starts because the linear algebra library
# reads them when it loads, and its thread count moves throughput by more than most of the
# effects these benchmarks measure.
set -euo pipefail
cd "$(dirname "$0")"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export PYTHONHASHSEED=0

if [[ "${QUICK:-0}" == "1" ]]; then
  exec python3 bench.py --quick
fi

mkdir -p results
python3 bench.py --write-summary results/summary.md | tee results/raw.txt
