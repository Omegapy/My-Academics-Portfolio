#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

# Split Module 8 huge files into line-preserving ten-way chunks.

set -euo pipefail


# ======
# Configuration
# ======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" # Sets the script directory.
PYTHON_BIN="${PYTHON_BIN:-python3}" # Sets the Python binary to python3.
INPUT_A="$SCRIPT_DIR/hugefile1.txt" # Sets the input A file.
INPUT_B="$SCRIPT_DIR/hugefile2.txt" # Sets the input B file.
CSV_FILE="$SCRIPT_DIR/benchmark_results.csv" # Sets the CSV file.
CHUNK_LINES="${CHUNK_LINES:-100000000}" # Sets the chunk lines.
EXPECTED_CHUNKS="${EXPECTED_CHUNKS:-10}" # Sets the expected chunks.
CHUNK_DIR="$SCRIPT_DIR/generated/chunks" # Sets the chunk directory.
LOG_DIR="$SCRIPT_DIR/generated/logs" # Sets the log directory.
LOG_FILE="$LOG_DIR/split_hugefiles.log" # Sets the log file.


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
require_file() { # Checks if the file exists.
  local file_path="$1" # Sets the file path.
  if [[ ! -f "$file_path" ]]; then # Checks if the file exists.
    echo "Required file not found: $file_path" >&2 # Prints the message.
    exit 1 
  fi
}
# ---- end require_file()


# ---- line_count()
line_count() { # Counts the lines in the file.
  wc -l < "$1" | tr -d ' ' # Removes the leading spaces.
}
# ---- end line_count()


# ---- count_glob()
count_glob() {
  local pattern="$1" # Sets the pattern.
  local matches
  matches="$(compgen -G "$pattern" || true)"
  if [[ -z "$matches" ]]; then # Checks if the pattern is empty.
    printf "0"
  else # Returns the number of matches.
    printf "%s\n" "$matches" | wc -l | tr -d ' '
  fi
}
# ---- end count_glob()


# ---- split_lines()
split_lines() { # Splits the files into chunks.
  local source_file="$1" # Sets the source file.
  local output_prefix="$2" # Sets the output prefix.

  rm -f "${output_prefix}"*.txt "${output_prefix}"[0-9][0-9] # Removes the output files.

  # Step 1: Use the required GNU form on Ubuntu and a portable fallback on macOS.
  if split --version >/dev/null 2>&1; then # Checks if the split command is available.
    split -l "$CHUNK_LINES" -d -a 2 --additional-suffix=.txt "$source_file" "$output_prefix" # Splits the files into chunks.
  else # Uses the fallback command.
    split -l "$CHUNK_LINES" -d -a 2 "$source_file" "$output_prefix" # Splits the files into chunks.
    for part_file in "${output_prefix}"[0-9][0-9]; do # Iterates through the output files.
      [[ -e "$part_file" ]] || continue # Skips if the file does not exist.
      mv "$part_file" "${part_file}.txt" # Renames the output files.
    done
  fi
}
# ---- end split_lines()


# ---- record_event()
record_event() {
  local elapsed="$1" # Sets the elapsed time.
  # Record the event in the CSV file.
  "$PYTHON_BIN" "$SCRIPT_DIR/bigdata_sum.py" \
    --event-only \
    --method "ten_way_split" \
    --input-a "$INPUT_A" \
    --input-b "$INPUT_B" \
    --output "$CHUNK_DIR" \
    --csv "$CSV_FILE" \
    --elapsed-seconds "$elapsed" \
    --verification-status "passed" \
    --notes "Line-preserving split into ten benchmark chunks"
}
# ---- end record_event()


# ======
# Main Script
# ======

mkdir -p "$CHUNK_DIR" "$LOG_DIR" # Creates the output directories.
exec > >(tee "$LOG_FILE") 2>&1 # Redirects the output to the log file.

echo "Module 8 ten-way split started: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "Input A: $INPUT_A" # Prints the input A file.
echo "Input B: $INPUT_B" # Prints the input B file.
echo "Chunk lines: $CHUNK_LINES" # Prints the chunk lines.
echo "Expected chunks: $EXPECTED_CHUNKS" # Prints the expected chunks.

require_file "$INPUT_A" # Requires the input A file.
require_file "$INPUT_B" # Requires the input B file.
rm -f "$CHUNK_DIR"/file1_part_*.txt "$CHUNK_DIR"/file2_part_*.txt "$CHUNK_DIR"/total_part_*.txt # Removes the output files.

split_start="$(timer_now)" # Sets the start time.
split_lines "$INPUT_A" "$CHUNK_DIR/file1_part_" # Splits the files into chunks.
split_lines "$INPUT_B" "$CHUNK_DIR/file2_part_" # Splits the files into chunks.
split_end="$(timer_now)" # Sets the end time.
split_elapsed="$(elapsed_seconds "$split_start" "$split_end")" # Calculates the elapsed time.

file1_parts="$(count_glob "$CHUNK_DIR/file1_part_*.txt")" # Counts the number of chunks.
file2_parts="$(count_glob "$CHUNK_DIR/file2_part_*.txt")" # Counts the number of chunks.
if [[ "$file1_parts" != "$EXPECTED_CHUNKS" || "$file2_parts" != "$EXPECTED_CHUNKS" ]]; then # Checks if the number of chunks is correct.
  echo "Expected $EXPECTED_CHUNKS chunks for each input, found $file1_parts and $file2_parts." >&2 # Prints an error message.
  exit 1
fi

index=0
while [[ "$index" -lt "$EXPECTED_CHUNKS" ]]; do # Loops through the chunks.
  suffix="$(printf "%02d" "$index")" # Formats the index with leading zeros.
  chunk_a="$CHUNK_DIR/file1_part_${suffix}.txt" # Sets the chunk A file.
  chunk_b="$CHUNK_DIR/file2_part_${suffix}.txt" # Sets the chunk B file.
  require_file "$chunk_a" # Requires the chunk A file.
  require_file "$chunk_b" # Requires the chunk B file.

  count_a="$(line_count "$chunk_a")" # Counts the number of lines in chunk A.
  count_b="$(line_count "$chunk_b")" # Counts the number of lines in chunk B.
  if [[ "$count_a" != "$count_b" ]]; then # Checks if the number of lines is correct.
    echo "Chunk line-count mismatch for suffix $suffix: $count_a vs $count_b" >&2 # Prints an error message.
    exit 1
  fi
  echo "Chunk $suffix line count: $count_a" # Prints the number of lines in the chunk.
  index=$((index + 1)) # Increments the index.
done

record_event "$split_elapsed" # Records the event.
echo "Ten-way split seconds: $split_elapsed" # Prints the elapsed time.
echo "Module 8 ten-way split ended: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
