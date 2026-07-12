#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

# Run the two-program parallel half-file benchmark for Module 8.

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
HALF_LINES="${HALF_LINES:-500000000}" # Sets the half lines. 
HALF_DIR="$SCRIPT_DIR/generated/half" # Sets the half directory. 
LOG_DIR="$SCRIPT_DIR/generated/logs" # Sets the log directory. 
LOG_FILE="$LOG_DIR/half_parallel.log" # Sets the log file. 


# ======
# Helper Functions
# ======

# ---- timer_now()
timer_now() {
  "$PYTHON_BIN" -c 'import time; print(f"{time.perf_counter():.9f}")'
}
# ---- end timer_now()


# ---- elapsed_seconds()
elapsed_seconds() {
  "$PYTHON_BIN" -c 'import sys; print(f"{float(sys.argv[2]) - float(sys.argv[1]):.6f}")' "$1" "$2"
}
# ---- end elapsed_seconds()


# ---- require_file()
require_file() {
  # Checks if the file path exists.
  local file_path="$1"
  if [[ ! -f "$file_path" ]]; then # Checks if the file path exists.
    echo "Required file not found: $file_path" >&2 # Prints the required file path.
    exit 1 # Exits with code 1.
  fi
}
# ---- end require_file()


# ---- line_count()
line_count() { 
  # Counts the lines in a file.
  wc -l < "$1" | tr -d ' '
}
# ---- end line_count()


# ---- count_glob()
count_glob() {
  # Counts the number of files that match a pattern.
  local pattern="$1"
  local matches

  matches="$(compgen -G "$pattern" || true)" # Compares the pattern to the glob. 
  if [[ -z "$matches" ]]; then # Checks if the matches are zero.
    printf "0" # Prints zero.
  else
    printf "%s\n" "$matches" | wc -l | tr -d ' '  
  fi
}
# ---- end count_glob()


# ---- split_lines()
split_lines() {
  # Splits the source file into half. 
  local source_file="$1"
  local output_prefix="$2"

  rm -f "${output_prefix}"*.txt "${output_prefix}"[0-9][0-9]

  # Step 1: Use GNU split options on Ubuntu and a suffix rename fallback on macOS.
  if split --version >/dev/null 2>&1; then # Checks if the split version exists. 
    split -l "$HALF_LINES" -d -a 2 --additional-suffix=.txt "$source_file" "$output_prefix" # Splits the source file into half. 
  else 
    split -l "$HALF_LINES" -d -a 2 "$source_file" "$output_prefix" # Splits the source file into half. 
    
    for part_file in "${output_prefix}"[0-9][0-9]; do # Iterates through the part files. 
      [[ -e "$part_file" ]] || continue # Continues if the part file does not exist. 
      mv "$part_file" "${part_file}.txt" # Moves the part file. 
    done
  fi
}
# ---- end split_lines()


# ---- record_event()
record_event() { 
  # Records the event. 
  local method_name="$1" # Sets the method name. 
  local elapsed="$2" # Sets the elapsed time. 
  local processed_lines="$3" # Sets the processed lines. 
  local output_path="$4" # Sets the output path. 
  local status="$5" # Sets the status. 
  local notes="$6" # Sets the notes. 

  # Records the event.
  "$PYTHON_BIN" "$SCRIPT_DIR/bigdata_sum.py" \
    --event-only \
    --method "$method_name" \
    --input-a "$INPUT_A" \
    --input-b "$INPUT_B" \
    --output "$output_path" \
    --csv "$CSV_FILE" \
    --elapsed-seconds "$elapsed" \
    --processed-lines "$processed_lines" \
    --verification-status "$status" \
    --notes "$notes"
}
# ---- end record_event()


# ======
# Main Script
# ======

mkdir -p "$HALF_DIR" "$LOG_DIR" # Creates the half directory and log directory if they do not exist.
exec > >(tee "$LOG_FILE") 2>&1 # Redirects the output to the log file.

echo "Module 8 half-parallel benchmark started: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the start time.
echo "Input A: $INPUT_A" # Prints the input file A.
echo "Input B: $INPUT_B" # Prints the input file B.
echo "Output: $OUTPUT_FILE" # Prints the output file. 
echo "Half split line count: $HALF_LINES" # Prints the half split line count. 

require_file "$INPUT_A" # Verifies the input file A. 
require_file "$INPUT_B" # Verifies the input file B. 
rm -f "$OUTPUT_FILE" "$HALF_DIR"/total_part_*.txt # Removes the output file and the half directory.

overall_start="$(timer_now)"

echo # Prints a blank line.
echo "Creating line-preserving half inputs." # Prints that the half inputs are being created. 
split_start="$(timer_now)" # Starts the timer. 
split_lines "$INPUT_A" "$HALF_DIR/file1_part_" # Splits the input file A. 
split_lines "$INPUT_B" "$HALF_DIR/file2_part_" # Splits the input file B. 
split_end="$(timer_now)" # Stops the timer. 
split_elapsed="$(elapsed_seconds "$split_start" "$split_end")" # Calculates the elapsed time. 

file1_parts="$(count_glob "$HALF_DIR/file1_part_*.txt")" # Counts the number of files that match the pattern. 
file2_parts="$(count_glob "$HALF_DIR/file2_part_*.txt")" # Counts the number of files that match the pattern. 
if [[ "$file1_parts" != "2" || "$file2_parts" != "2" ]]; then # Checks if the file parts equal two. If not, it will exit with code 1. 
  echo "Expected exactly 2 half chunks for each input, found $file1_parts and $file2_parts." >&2 # Prints the expected half chunks. 
  echo "For small tests, set HALF_LINES to half the test file line count." >&2 # Prints the half split line count. 
  exit 1 # Exits with code 1. 
fi

for suffix in 00 01; do # Iterates through the suffixes. 
  count_a="$(line_count "$HALF_DIR/file1_part_${suffix}.txt")" # Counts the lines in the file. 
  count_b="$(line_count "$HALF_DIR/file2_part_${suffix}.txt")" # Counts the lines in the file. 
  if [[ "$count_a" != "$count_b" ]]; then # Checks if the line counts are equal. If not, it will exit with code 1. 
    echo "Chunk line-count mismatch for suffix $suffix: $count_a vs $count_b" >&2 # Prints the chunk line-count mismatch. 
    exit 1 # Exits with code 1. 
  fi
  echo "Half chunk $suffix line count: $count_a" # Prints the half chunk line count. 
done

record_event "half_parallel_split" "$split_elapsed" 0 "$OUTPUT_FILE" "recorded" "Line-preserving split time only" # Records the event. 

echo # Prints a blank line. 
echo "Launching both half workers through the operating system." # Prints that the half workers are being launched. 
process_start="$(timer_now)" # Starts the timer. 

# Launches the first half worker. 
"$PYTHON_BIN" "$SCRIPT_DIR/sum_first_half.py" \
  --input-a "$HALF_DIR/file1_part_00.txt" \
  --input-b "$HALF_DIR/file2_part_00.txt" \
  --output "$HALF_DIR/total_part_00.txt" \
  --csv "$CSV_FILE" &
pid_first=$!

# Launches the second half worker. 
"$PYTHON_BIN" "$SCRIPT_DIR/sum_second_half.py" \
  --input-a "$HALF_DIR/file1_part_01.txt" \
  --input-b "$HALF_DIR/file2_part_01.txt" \
  --output "$HALF_DIR/total_part_01.txt" \
  --csv "$CSV_FILE" &
pid_second=$!

# Checks if the workers failed. 
worker_status=0
if ! wait "$pid_first"; then # Checks if the first worker failed. 
  worker_status=1 # Sets the worker status to 1. 
fi
if ! wait "$pid_second"; then # Checks if the second worker failed. 
  worker_status=1 # Sets the worker status to 1. 
fi

if [[ "$worker_status" -ne 0 ]]; then # Checks if the worker status is not equal to zero. If not, it will exit with code 1. 
  echo "At least one half worker failed." >&2 # Prints the worker status. 
  exit 1 # Exits with code 1. 
fi
process_end="$(timer_now)" # Stops the timer. 
process_elapsed="$(elapsed_seconds "$process_start" "$process_end")" # Calculates the elapsed time. 

echo # Prints a blank line. 
echo "Concatenating half outputs in numeric order." # Prints that the half outputs are being concatenated. 
concat_start="$(timer_now)" # Starts the timer. 
cat "$HALF_DIR/total_part_00.txt" "$HALF_DIR/total_part_01.txt" > "$OUTPUT_FILE" # Concatenates the half outputs. 
concat_end="$(timer_now)" # Stops the timer. 
concat_elapsed="$(elapsed_seconds "$concat_start" "$concat_end")" # Calculates the elapsed time. 

overall_end="$(timer_now)" # Stops the timer. 
overall_elapsed="$(elapsed_seconds "$overall_start" "$overall_end")" # Calculates the elapsed time. 

input_lines="$(line_count "$INPUT_A")" # Counts the lines in the input file A. 
output_lines="$(line_count "$OUTPUT_FILE")" # Counts the lines in the output file. 
if [[ "$input_lines" != "$output_lines" ]]; then # Checks if the line counts are equal. If not, it will exit with code 1. 
  echo "Verification failed: input lines $input_lines != output lines $output_lines" >&2
  exit 1
fi

# Records the events. 
record_event "half_parallel_processing_total" "$process_elapsed" "$output_lines" "$OUTPUT_FILE" "passed" "Processing-only time for two simultaneous Python workers"
record_event "half_parallel_concatenate" "$concat_elapsed" "$output_lines" "$OUTPUT_FILE" "recorded" "Concatenation time for two output halves"
record_event "half_parallel_end_to_end" "$overall_elapsed" "$output_lines" "$OUTPUT_FILE" "passed" "Split plus processing plus concatenation"

echo # Prints a blank line. 
echo "Line-count verification passed: $output_lines lines" # Prints the line count verification. 
echo "Split seconds: $split_elapsed" # Prints the split time. 
echo "Processing-only seconds: $process_elapsed" # Prints the processing time. 
echo "Concatenation seconds: $concat_elapsed" # Prints the concatenation time. 
echo "End-to-end seconds: $overall_elapsed" # Prints the end-to-end time. 
echo "Module 8 half-parallel benchmark ended: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the end time.
