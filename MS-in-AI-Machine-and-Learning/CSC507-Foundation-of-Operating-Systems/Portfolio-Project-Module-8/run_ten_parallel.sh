#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

# Run the ten-way parallel chunk benchmark for Module 8.

set -euo pipefail


# ======
# Configuration
# ======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" # Sets the script directory. 
PYTHON_BIN="${PYTHON_BIN:-python3}" # Sets the python binary. 
INPUT_A="$SCRIPT_DIR/hugefile1.txt" # Sets the input A file. 
INPUT_B="$SCRIPT_DIR/hugefile2.txt" # Sets the input B file. 
OUTPUT_FILE="$SCRIPT_DIR/totalfile.txt" # Sets the output file. 
CSV_FILE="$SCRIPT_DIR/benchmark_results.csv" # Sets the CSV file. 
EXPECTED_CHUNKS="${EXPECTED_CHUNKS:-10}" # Sets the expected chunks to 10. 
CHUNK_DIR="$SCRIPT_DIR/generated/chunks" # Sets the chunk directory. 
LOG_DIR="$SCRIPT_DIR/generated/logs" # Sets the log directory. 
LOG_FILE="$LOG_DIR/ten_parallel.log" # Sets the log file.


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
require_file() { # Checks if the file path exists.
  local file_path="$1" # Sets the file path. 
  if [[ ! -f "$file_path" ]]; then # Checks if the file path exists. If not, it will exit with code 1. 
    echo "Required file not found: $file_path" >&2 # Prints the file path. 
    exit 1 # Exits with code 1. 
  fi
}
# ---- end require_file()


# ---- line_count()
line_count() {
  wc -l < "$1" | tr -d ' ' # Counts the lines in the file. 
}
# ---- end line_count()


# ---- record_event()
record_event() { # Records the event in the CSV file.
  local method_name="$1" # Sets the method name.
  local elapsed="$2" # Sets the elapsed time. 
  local processed_lines="$3" # Sets the processed lines. 
  local status="$4" # Sets the status. 
  local notes="$5" # Sets the notes. 
  
  # Calls the bigdata_sum.py script with the given arguments. 
  "$PYTHON_BIN" "$SCRIPT_DIR/bigdata_sum.py" \
    --event-only \
    --method "$method_name" \
    --input-a "$INPUT_A" \
    --input-b "$INPUT_B" \
    --output "$OUTPUT_FILE" \
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

mkdir -p "$CHUNK_DIR" "$LOG_DIR" # Creates the chunk and log directories. 
exec > >(tee "$LOG_FILE") 2>&1 # Redirects the output to the log file. 

echo "Module 8 ten-way parallel benchmark started: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the start time. 
echo "Input A: $INPUT_A" # Prints the input A file. 
echo "Input B: $INPUT_B" # Prints the input B file. 
echo "Output: $OUTPUT_FILE" # Prints the output file. 
echo "Expected chunks: $EXPECTED_CHUNKS" # Prints the expected chunks. 

require_file "$INPUT_A" # Checks if the input A file exists. 
require_file "$INPUT_B" # Checks if the input B file exists. 
rm -f "$OUTPUT_FILE" "$CHUNK_DIR"/total_part_*.txt # Removes the output file and the chunk files.

overall_start="$(timer_now)" # Gets the start time. 

echo # Prints a newline. 
echo "Verifying input chunks before worker launch." # Prints the message. 
index=0 # Sets the index to 0. 
while [[ "$index" -lt "$EXPECTED_CHUNKS" ]]; do # Loops through the expected chunks. 
  suffix="$(printf "%02d" "$index")" # Formats the index as a two-digit number. 
  require_file "$CHUNK_DIR/file1_part_${suffix}.txt" # Checks if the input file exists. 
  require_file "$CHUNK_DIR/file2_part_${suffix}.txt" # Checks if the input file exists. 
  index=$((index + 1)) # Increments the index. 
done

echo 
echo "Launching ten chunk workers through the operating system." # Prints the message. 
process_start="$(timer_now)" # Gets the start time. 
pids=() # Creates an array to store the process IDs. 
index=0 # Sets the index to 0. 
while [[ "$index" -lt "$EXPECTED_CHUNKS" ]]; do # Loops through the expected chunks. 
  suffix="$(printf "%02d" "$index")" # Formats the index as a two-digit number. 
  # Calls the sum_chunk.py script with the given arguments. 
  "$PYTHON_BIN" "$SCRIPT_DIR/sum_chunk.py" \
    --chunk-index "$suffix" \
    --input-a "$CHUNK_DIR/file1_part_${suffix}.txt" \
    --input-b "$CHUNK_DIR/file2_part_${suffix}.txt" \
    --output "$CHUNK_DIR/total_part_${suffix}.txt" \
    --csv "$CSV_FILE" &
  pids[$index]=$!
  index=$((index + 1))
done

worker_status=0 # Sets the worker status to 0. 
for pid in "${pids[@]}"; do # Loops through the process IDs. 
  if ! wait "$pid"; then # Checks if the process ID is valid. 
    worker_status=1 # Sets the worker status to 1. 
  fi
done

if [[ "$worker_status" -ne 0 ]]; then # Checks if the worker status is not 0. 
  echo "At least one chunk worker failed." >&2 # Prints the message. 
  exit 1
fi
process_end="$(timer_now)" # Gets the end time. 
process_elapsed="$(elapsed_seconds "$process_start" "$process_end")" # Calculates the elapsed time. 

echo # Prints a newline. 
echo "Concatenating chunk outputs in numeric order." # Prints the message. 
concat_start="$(timer_now)" # Gets the start time. 
: > "$OUTPUT_FILE" # Empties the output file. 
index=0 # Sets the index to 0. 

while [[ "$index" -lt "$EXPECTED_CHUNKS" ]]; do # Loops through the expected chunks. 
  suffix="$(printf "%02d" "$index")" # Formats the index as a two-digit number. 
  output_chunk="$CHUNK_DIR/total_part_${suffix}.txt" # Sets the output chunk file. 
  require_file "$output_chunk" # Checks if the output chunk file exists. 
  cat "$output_chunk" >> "$OUTPUT_FILE" # Concatenates the output chunk file to the output file. 
  index=$((index + 1)) 
done
concat_end="$(timer_now)" # Gets the end time. 
concat_elapsed="$(elapsed_seconds "$concat_start" "$concat_end")" # Calculates the elapsed time. 

overall_end="$(timer_now)" # Gets the end time. 
overall_elapsed="$(elapsed_seconds "$overall_start" "$overall_end")" # Calculates the elapsed time. 

input_lines="$(line_count "$INPUT_A")" # Counts the lines in the input file. 
output_lines="$(line_count "$OUTPUT_FILE")" # Counts the lines in the output file. 
if [[ "$input_lines" != "$output_lines" ]]; then # Checks if the input lines are not equal to the output lines. 
  echo "Verification failed: input lines $input_lines != output lines $output_lines" >&2 # Prints the message. 
  exit 1 
fi

record_event "ten_way_processing_total" "$process_elapsed" "$output_lines" "passed" "Processing-only time for chunk workers"
record_event "ten_way_concatenate" "$concat_elapsed" "$output_lines" "recorded" "Concatenation time for ten output chunks"
record_event "ten_way_end_to_end" "$overall_elapsed" "$output_lines" "passed" "Processing plus concatenation after pre-splitting"

echo
echo "Line-count verification passed: $output_lines lines"
echo "Processing-only seconds: $process_elapsed"
echo "Concatenation seconds: $concat_elapsed"
echo "End-to-end seconds after pre-splitting: $overall_elapsed"
echo "Module 8 ten-way parallel benchmark ended: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
