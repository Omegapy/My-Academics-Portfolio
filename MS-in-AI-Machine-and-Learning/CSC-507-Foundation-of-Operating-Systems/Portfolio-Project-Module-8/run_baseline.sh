#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

# Run the single-process streaming baseline for Module 8.

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
LOG_DIR="$SCRIPT_DIR/generated/logs" # Sets the log directory.
LOG_FILE="$LOG_DIR/baseline.log" # Sets the log file.


# ======
# Helper Functions
# ======

# ---- require_file()
require_file() {
  local file_path="$1"
  if [[ ! -f "$file_path" ]]; then
    echo "Required file not found: $file_path" >&2
    exit 1
  fi
}
# ---- end require_file()


# ---- line_count()
line_count() {
  wc -l < "$1" | tr -d ' '
}
# ---- end line_count()


# ======
# Main Script
# ======

mkdir -p "$LOG_DIR" # Creates the log directory if it does not exist.
exec > >(tee "$LOG_FILE") 2>&1 # Redirects the output to the log file.

echo "Module 8 baseline started: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the start time.
echo "Input A: $INPUT_A" # Prints the input file A.
echo "Input B: $INPUT_B" # Prints the input file B.
echo "Output: $OUTPUT_FILE" # Prints the output file.

require_file "$INPUT_A" # Verifies the input file A.
require_file "$INPUT_B" # Verifies the input file B.
rm -f "$OUTPUT_FILE" # Removes the output file.

"$PYTHON_BIN" "$SCRIPT_DIR/bigdata_sum.py" \
  --method "baseline_single_process" \
  --input-a "$INPUT_A" \
  --input-b "$INPUT_B" \
  --output "$OUTPUT_FILE" \
  --csv "$CSV_FILE" \
  --notes "Single Python process streaming two aligned files"

input_lines="$(line_count "$INPUT_A")" # Counts the lines in the input file A.
output_lines="$(line_count "$OUTPUT_FILE")" # Counts the lines in the output file.

if [[ "$input_lines" != "$output_lines" ]]; then # Checks if the input lines equal the output lines. If not, it will exit with code 1.
  echo "Verification failed: input lines $input_lines != output lines $output_lines" >&2
  exit 1
fi

echo
echo "Line-count verification passed: $output_lines lines"
echo
echo "First five rows from input A:"
head -5 "$INPUT_A"
echo
echo "First five rows from input B:"
head -5 "$INPUT_B"
echo
echo "First five rows from output:"
head -5 "$OUTPUT_FILE"
echo
echo "Module 8 baseline ended: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
