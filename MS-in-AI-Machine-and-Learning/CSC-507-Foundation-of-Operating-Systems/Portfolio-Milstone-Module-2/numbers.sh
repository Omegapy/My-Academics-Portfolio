#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-05-24
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Spring C 2026


set -euo pipefail

OUTPUT_FILE="file1.txt"
LINE_COUNT=1000

# Generate a random number and display it
echo "$RANDOM"

# Output a random number into file1.txt
echo "$RANDOM" > "$OUTPUT_FILE"

# Append another random number to file1.txt
echo "$RANDOM" >> "$OUTPUT_FILE"

# Remove file1.txt before creating the final assignment output
rm "$OUTPUT_FILE"

# Create file1.txt with 1,000 random-number lines using a for loop
for i in $(seq 1 "$LINE_COUNT")
do
  echo "$RANDOM" >> "$OUTPUT_FILE"
done

echo "Created $OUTPUT_FILE with $(wc -l < "$OUTPUT_FILE" | tr -d ' ') lines."
