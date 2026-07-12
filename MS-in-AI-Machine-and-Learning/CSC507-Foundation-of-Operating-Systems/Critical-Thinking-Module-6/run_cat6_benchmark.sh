#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-06-21
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# ----------------------------------------

# Run the CAT-6 real-time scheduling benchmark on Ubuntu.

set -euo pipefail


# ======
# Configuration
# ======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
LINE_COUNT="${LINE_COUNT:-10000000}"
METHODS="${METHODS:-all}"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/benchmark_output}"
REAL_TIME_PRIORITY="${REAL_TIME_PRIORITY:-10}"
MAX_AUTO_PARTS="${MAX_AUTO_PARTS:-32}"
SYSTEM_INFO_FILE="$OUTPUT_DIR/cat6_system_info.txt"


# ======
# Helper Functions
# ======

# ---- show_usage()
show_usage() {
  cat <<'USAGE'
CAT-6 Benchmark Runner

Environment variables:
  LINE_COUNT            Input row count. Default: 10000000
  METHODS               Comma-separated methods or all. Default: all
  OUTPUT_DIR            Output directory. Default: CTAs/CAT-6/benchmark_output
  REAL_TIME_PRIORITY    Linux SCHED_RR priority. Default: 10
  MAX_AUTO_PARTS        Max split count for method 7. Default: 32
  PYTHON_BIN            Python command. Default: python3

Examples:
  ./run_cat6_benchmark.sh
  LINE_COUNT=10000 METHODS=m01_single_normal,m03_split2_realtime ./run_cat6_benchmark.sh

Real-time note:
  Linux normally requires CAP_SYS_NICE or sudo before a process can enter
  SCHED_RR real-time scheduling. The Python CSV records whether each worker
  actually received real-time scheduling.
USAGE
}
# ---- end show_usage()


# ---- collect_system_info()
collect_system_info() {
  mkdir -p "$OUTPUT_DIR"

  {
    echo "CAT-6 Ubuntu Benchmark System Information"
    echo "Captured: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo

    echo "===== uname -a ====="
    uname -a || true
    echo

    echo "===== lsb_release -a ====="
    lsb_release -a 2>/dev/null || true
    echo

    echo "===== lscpu summary ====="
    if command -v lscpu >/dev/null 2>&1; then
      lscpu | grep -E "Architecture|Model name|CPU\\(s\\)|Thread\\(s\\) per core|Core\\(s\\) per socket|Socket\\(s\\)|CPU max MHz|CPU min MHz" || true
    else
      echo "lscpu not available"
    fi
    echo

    echo "===== memory ====="
    if command -v free >/dev/null 2>&1; then
      free -h || true
    else
      echo "free not available"
    fi
    echo

    echo "===== storage ====="
    if command -v lsblk >/dev/null 2>&1; then
      lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL || true
    else
      echo "lsblk not available"
    fi
    echo

    echo "===== scheduler tools ====="
    command -v chrt || true
    if ulimit -r >/dev/null 2>&1; then
      echo "ulimit -r: $(ulimit -r)"
    else
      echo "ulimit -r: not available"
    fi
    echo "current user: $(id -un || true)"
  } > "$SYSTEM_INFO_FILE"
}
# ---- end collect_system_info()


# ======
# Main Script
# ======

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  show_usage
  exit 0
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python command not found: $PYTHON_BIN" >&2
  exit 1
fi

collect_system_info

echo "System information written: $SYSTEM_INFO_FILE"
echo "Running CAT-6 benchmark with LINE_COUNT=$LINE_COUNT METHODS=$METHODS"

"$PYTHON_BIN" "$SCRIPT_DIR/cat6_realtime_scheduling_benchmark.py" \
  --line-count "$LINE_COUNT" \
  --methods "$METHODS" \
  --output-dir "$OUTPUT_DIR" \
  --real-time-priority "$REAL_TIME_PRIORITY" \
  --max-auto-parts "$MAX_AUTO_PARTS"
