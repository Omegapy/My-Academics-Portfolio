#!/usr/bin/env bash
# Author: Alexander Ricciardi
# Date: 2026-05-25
# Course: CSC507
# Professor: Dr. Joseph Issa
# Spring C 2026

set -euo pipefail

OUTPUT_FILE="${OUTPUT_FILE:-file1.txt}"
LINE_COUNT="${LINE_COUNT:-1000000}"

if ! [[ "$LINE_COUNT" =~ ^[0-9]+$ ]] || ((LINE_COUNT <= 0)); then
  echo "LINE_COUNT must be a positive integer." >&2
  exit 1
fi

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

# Remove file1.txt from the previous exercise before creating the Module 3 output.
rm -f "$OUTPUT_FILE"

# Reset the Bash SECONDS timer immediately before the measured process starts.
SECONDS=0

# Create file1.txt with 1,000,000 random-number lines using a Bash for loop.
for ((i = 1; i <= LINE_COUNT; i++))
do
  echo "$RANDOM" >> "$OUTPUT_FILE"
done

elapsed_seconds="$SECONDS"
verified_lines="$(wc -l < "$OUTPUT_FILE" | tr -d ' ')"

echo "Bash random-number generation ended: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Elapsed seconds: $elapsed_seconds"
echo "Elapsed HH:MM:SS: $(format_duration "$elapsed_seconds")"
echo "Created $OUTPUT_FILE with $verified_lines lines."
