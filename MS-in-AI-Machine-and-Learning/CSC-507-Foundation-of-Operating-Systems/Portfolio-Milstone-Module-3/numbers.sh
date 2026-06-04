#!/usr/bin/env bash
# Author: Alexander Ricciardi
# Date: 2026-05-30
# Course: CSC507
# Professor: Dr. Joseph Issa
# Spring C 2026

# Set shell options
set -euo pipefail

# Output file name, default = file1.txt
OUTPUT_FILE="${OUTPUT_FILE:-file1.txt}"
# Number of lines to generate, default = 1,000,000
LINE_COUNT="${LINE_COUNT:-1000000}"

# Validate LINE_COUNT is a positive integer
if ! [[ "$LINE_COUNT" =~ ^[0-9]+$ ]] || ((LINE_COUNT <= 0)); then
  echo "LINE_COUNT must be a positive integer." >&2
  exit 1
fi

# Function to format seconds into HH:MM:SS
format_duration() {
  local total_seconds="$1"
  local hours=$((total_seconds / 3600))
  local minutes=$(((total_seconds % 3600) / 60))
  local seconds=$((total_seconds % 60))

  printf "%02d:%02d:%02d" "$hours" "$minutes" "$seconds"
}

echo "Bash random-number generation started: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Output file: $OUTPUT_FILE"
echo "Line count: $LINE_COUNT"

#  Remove file1.txt from the previous exercise before creating the Module 3 output.
rm -f "$OUTPUT_FILE"

# Reset the Bash SECONDS timer immediately before the measured process starts.
SECONDS=0

# Create file1.txt with 1,000,000 random-number lines using a Bash for loop.
for ((i = 1; i <= LINE_COUNT; i++))
do
  echo "$RANDOM" >> "$OUTPUT_FILE"
done

# Calculate elapsed time and verify line count
elapsed_seconds="$SECONDS"
verified_lines="$(wc -l < "$OUTPUT_FILE" | tr -d ' ')"

# Print the results
echo "Bash random-number generation ended: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Elapsed seconds: $elapsed_seconds"
echo "Elapsed HH:MM:SS: $(format_duration "$elapsed_seconds")"
echo "Created $OUTPUT_FILE with $verified_lines lines."
