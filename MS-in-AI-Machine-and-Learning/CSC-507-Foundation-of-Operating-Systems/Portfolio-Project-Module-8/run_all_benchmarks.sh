#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

# Run the complete Module 8 benchmark sequence on Ubuntu.

set -euo pipefail


# ======
# Configuration
# ======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" # Sets the script directory.
PYTHON_BIN="${PYTHON_BIN:-python3}" # Sets the python binary.
INPUT_A="$SCRIPT_DIR/hugefile1.txt" # Sets the input file A.
INPUT_B="$SCRIPT_DIR/hugefile2.txt" # Sets the input file B.
OUTPUT_FILE="$SCRIPT_DIR/totalfile.txt" # Sets the output file.
CSV_FILE="$SCRIPT_DIR/benchmark_results.csv" # Sets the CSV file.
VALIDATION_CSV="$SCRIPT_DIR/validation_results.csv" # Sets the validation CSV file.
REPORT_FILE="$SCRIPT_DIR/verification_report.txt" # Sets the verification report file.
RUN_FULL_VALIDATION="${RUN_FULL_VALIDATION:-true}" # Sets the full validation flag.
RESET_RESULTS="${RESET_RESULTS:-true}" # Sets the reset results flag.
LOG_DIR="$SCRIPT_DIR/generated/logs" # Sets the log directory.
LOG_FILE="$LOG_DIR/full_run.log" # Sets the log file.


# ======
# Main Script
# ======

mkdir -p "$LOG_DIR" # Creates the log directory if it does not exist.
exec > >(tee "$LOG_FILE") 2>&1 # Redirects the output to the log file.

echo "Module 8 full benchmark run started: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the start time.

echo "Run full validation after final method: $RUN_FULL_VALIDATION" # Prints the full validation flag.

echo "Reset result CSV files first: $RESET_RESULTS" # Prints the reset results flag.

if [[ "$RESET_RESULTS" == "true" ]]; then # Checks the reset results flag. If true, it will remove the CSV files.
  rm -f "$CSV_FILE" "$VALIDATION_CSV" # Removes the CSV files.
fi

"$SCRIPT_DIR/verify_inputs.sh" # Verifies the inputs.

echo
echo "=== Baseline single-process run ==="
# Run the baseline single-process benchmark.
"$SCRIPT_DIR/run_baseline.sh"
# Validate the outputs of the baseline single-process benchmark.
"$PYTHON_BIN" "$SCRIPT_DIR/validate_outputs.py" \
  --mode fast \
  --label "baseline_single_process" \
  --input-a "$INPUT_A" \
  --input-b "$INPUT_B" \
  --output "$OUTPUT_FILE" \
  --csv "$VALIDATION_CSV" \
  --report "$REPORT_FILE"

echo
echo "=== Two-program half-parallel run ==="
# Run the two-program half-parallel benchmark.
"$SCRIPT_DIR/run_half_parallel.sh"
# Validate the outputs of the two-program half-parallel benchmark.
"$PYTHON_BIN" "$SCRIPT_DIR/validate_outputs.py" \
  --mode fast \
  --label "half_parallel_end_to_end" \
  --input-a "$INPUT_A" \
  --input-b "$INPUT_B" \
  --output "$OUTPUT_FILE" \
  --csv "$VALIDATION_CSV" \
  --report "$REPORT_FILE"

echo
echo "=== Ten-way split and parallel run ==="
# Split the huge files into ten chunks.
"$SCRIPT_DIR/split_hugefiles.sh"
# Run the ten-way parallel benchmark.
"$SCRIPT_DIR/run_ten_parallel.sh"
# Validate the outputs of the ten-way parallel benchmark.
"$PYTHON_BIN" "$SCRIPT_DIR/validate_outputs.py" \
  --mode fast \
  --label "ten_way_end_to_end" \
  --input-a "$INPUT_A" \
  --input-b "$INPUT_B" \
  --output "$OUTPUT_FILE" \
  --csv "$VALIDATION_CSV" \
  --report "$REPORT_FILE"

# Run full validation after final method.
if [[ "$RUN_FULL_VALIDATION" == "true" ]]; then # Checks the full validation flag. If true, it will run the full validation.
  echo
  echo "=== Final full validation ==="
  "$PYTHON_BIN" "$SCRIPT_DIR/validate_outputs.py" \
    --mode full \
    --label "ten_way_final_full_validation" \
    --input-a "$INPUT_A" \
    --input-b "$INPUT_B" \
    --output "$OUTPUT_FILE" \
    --csv "$VALIDATION_CSV" \
    --report "$REPORT_FILE"
else
  echo
  echo "Full validation skipped by RUN_FULL_VALIDATION=$RUN_FULL_VALIDATION"
fi

echo
echo "Module 8 full benchmark run ended: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo
echo "Command summary for evidence collection:"
echo "wc -l hugefile1.txt hugefile2.txt totalfile.txt"
echo "head -5 hugefile1.txt hugefile2.txt totalfile.txt"
echo "tail -5 hugefile1.txt hugefile2.txt totalfile.txt"
echo "cat benchmark_results.csv"
echo "cat validation_results.csv"
echo "cat system_info.txt"
echo "cat verification_report.txt"
