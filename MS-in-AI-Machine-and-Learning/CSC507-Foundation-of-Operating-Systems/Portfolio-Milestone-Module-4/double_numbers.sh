#!/usr/bin/env bash
# File: double_numbers.sh | Author: Alexander Ricciardi | Date: 2026-06-03
# Course: CSC507 | Professor: Dr. Joseph Issa | Spring C 2026
# SPDX-License-Identifier: Apache-2.0
# ----------------------------------------

# Benchmark the required Bash line-by-line doubling process.

set -euo pipefail

# ======
# Configuration
# ======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_FILE="${INPUT_FILE:-$SCRIPT_DIR/file1.txt}"
OUTPUT_FILE="${OUTPUT_FILE:-$SCRIPT_DIR/newfile1.txt}"
BASH_RESULT_FILE="${BASH_RESULT_FILE:-$SCRIPT_DIR/bash_benchmark_result.csv}"


# ======
# Helper Functions
# ======

# ---- format_duration()
format_duration() {
  local total_seconds="$1"
  local hours=$((total_seconds / 3600))
  local minutes=$(((total_seconds % 3600) / 60))
  local seconds=$((total_seconds % 60))

  printf "%02d:%02d:%02d" "$hours" "$minutes" "$seconds"
}
# ---- end format_duration()


# ---- detect_cpu_count()
detect_cpu_count() {
  if command -v getconf >/dev/null 2>&1; then
    getconf _NPROCESSORS_ONLN 2>/dev/null && return 0
  fi

  if command -v sysctl >/dev/null 2>&1; then
    sysctl -n hw.ncpu 2>/dev/null && return 0
  fi

  printf "unknown"
}
# ---- end detect_cpu_count()


# ---- verify_output()
verify_output() {
  local input_path="$1"
  local output_path="$2"

  paste "$input_path" "$output_path" |
    awk '{ if ($2 != $1 * 2) { exit 1 } }'
}
# ---- end verify_output()


# ======
# Main Script
# ======

# SAFETY CHECK: Fail before timing if the source file is missing.
if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Input file not found: $INPUT_FILE" >&2
  exit 1
fi

echo "Bash line-by-line doubling started: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Input file: $INPUT_FILE"
echo "Output file: $OUTPUT_FILE"

# Step 1: Remove prior output so each run produces a clean newfile1.txt.
rm -f "$OUTPUT_FILE"

# Step 2: Reset Bash's integer SECONDS timer immediately before the measured loop.
SECONDS=0

# Step 3: Read one number at a time, double it, and append it to newfile1.txt.
while IFS= read -r number || [[ -n "$number" ]]
do
  doubled_number=$((number * 2))
  printf "%s\n" "$doubled_number" >> "$OUTPUT_FILE"
done < "$INPUT_FILE"

# Step 4: Capture elapsed time and verify output after the timed work completes.
elapsed_seconds="$SECONDS"
elapsed_hms="$(format_duration "$elapsed_seconds")"
input_lines="$(wc -l < "$INPUT_FILE" | tr -d ' ')"
verified_lines="$(wc -l < "$OUTPUT_FILE" | tr -d ' ')"
file_size_bytes="$(wc -c < "$OUTPUT_FILE" | tr -d ' ')"
verified_correct="false"

if [[ "$input_lines" == "$verified_lines" ]] && verify_output "$INPUT_FILE" "$OUTPUT_FILE"; then
  verified_correct="true"
else
  echo "Verification failed: output does not match doubled input." >&2
  exit 1
fi

# Step 5: Persist one CSV row so the Python benchmark can include the Bash baseline.
{
  echo "method,input_file,output_file,line_count,elapsed_seconds,elapsed_hms,verified_lines,verified_correct,file_size_bytes,platform_name,platform_release,python_version,cpu_count,notes"
  printf "bash_line_by_line,%s,%s,%s,%.6f,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" \
    "$INPUT_FILE" \
    "$OUTPUT_FILE" \
    "$input_lines" \
    "$elapsed_seconds" \
    "$elapsed_hms" \
    "$verified_lines" \
    "$verified_correct" \
    "$file_size_bytes" \
    "$(uname -s)" \
    "$(uname -r)" \
    "n/a" \
    "$(detect_cpu_count)" \
    "Bash SECONDS integer timing"
} > "$BASH_RESULT_FILE"

echo "Bash line-by-line doubling ended: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Elapsed seconds: $elapsed_seconds"
echo "Elapsed HH:MM:SS: $elapsed_hms"
echo "Verified lines: $verified_lines"
echo "Verified correct: $verified_correct"
echo "CSV row written: $BASH_RESULT_FILE"
