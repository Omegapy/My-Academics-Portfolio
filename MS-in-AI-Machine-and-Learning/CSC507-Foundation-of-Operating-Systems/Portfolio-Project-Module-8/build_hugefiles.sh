#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

# Verify or rebuild hugefile1.txt and hugefile2.txt from million-line inputs.

set -euo pipefail


# ======
# Configuration
# ======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" # Sets the script directory.
PYTHON_BIN="${PYTHON_BIN:-python3}" # Sets the python binary.
INPUT_A="$SCRIPT_DIR/file1.txt" # Sets the input file A.
INPUT_B="$SCRIPT_DIR/file2.txt" # Sets the input file B.
HUGE_A="$SCRIPT_DIR/hugefile1.txt" # Sets the huge file A.
HUGE_B="$SCRIPT_DIR/hugefile2.txt" # Sets the huge file B.
REPEAT_COUNT="${REPEAT_COUNT:-1000}" # Sets the repeat count.
BUILD_MODE="false" # Sets the build mode.
FORCE_MODE="false" # Sets the force mode.
LOG_DIR="$SCRIPT_DIR/generated/logs" # Sets the log directory.
LOG_FILE="$LOG_DIR/build_hugefiles.log" # Sets the log file.


# ======
# Helper Functions
# ======

# ---- print_usage()
# Prints the usage of the script.
print_usage() {
  cat <<'USAGE'
Usage: ./build_hugefiles.sh [--build] [--force]

Default behavior verifies existing Module 8 hugefile1.txt and hugefile2.txt.
--build appends Module 8 file1.txt and file2.txt REPEAT_COUNT times.
--force permits overwriting existing huge files during --build.
USAGE
}
# ---- end print_usage()


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
  local file_path="$1"
  if [[ ! -f "$file_path" ]]; then
    echo "Required file not found: $file_path" >&2
    exit 1
  fi
}
# ---- end require_file()


# ---- verify_hugefiles()
verify_hugefiles() {
  require_file "$HUGE_A" # Verifies the huge file A.
  require_file "$HUGE_B" # Verifies the huge file B.

  echo "Huge-file line counts:"
  wc -l "$HUGE_A" "$HUGE_B" # Prints the line counts of the huge files.
  echo
  echo "Huge-file byte counts:"
  wc -c "$HUGE_A" "$HUGE_B"
}
# ---- end verify_hugefiles()


# ---- record_build_event()
record_build_event() { 
  local elapsed="$1" # Sets the elapsed time.

  # Calls the python script with the event-only flag, 
  # and sets the method to build_hugefiles_recovery.
  "$PYTHON_BIN" "$SCRIPT_DIR/bigdata_sum.py" \
    --event-only \
    --method "build_hugefiles_recovery" \
    --input-a "$INPUT_A" \
    --input-b "$INPUT_B" \
    --output "$HUGE_A" \
    --elapsed-seconds "$elapsed" \
    --verification-status "recorded" \
    --notes "Recovery build time only; excluded from processing benchmark"
}
# ---- end record_build_event()


# ======
# Main Script
# ======

while [[ $# -gt 0 ]]; do # Checks the arguments.
  case "$1" in # Checks the arguments.
    --build)
      BUILD_MODE="true" # Sets the build mode to true.
      shift # Shifts the arguments.
      ;;
    --force)
      FORCE_MODE="true" # Sets the force mode to true.
      shift # Shifts the arguments.
      ;;
    -h|--help)
      print_usage # Prints the usage.
      exit 0 # Exits with code 0.
      ;;
    *)
      echo "Unknown option: $1" >&2 # Prints the unknown option.
      print_usage >&2 # Prints the usage.
      exit 2 # Exits with code 2.
      ;;
  esac
done

mkdir -p "$LOG_DIR" # Creates the log directory if it does not exist.
exec > >(tee "$LOG_FILE") 2>&1 # Redirects the output to the log file.

echo "Module 8 huge-file helper started: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the start time.
echo "Build mode: $BUILD_MODE" 
echo "Force mode: $FORCE_MODE" 
echo "Repeat count: $REPEAT_COUNT"
echo "Seed input A: $INPUT_A"
echo "Seed input B: $INPUT_B"
echo "Huge output A: $HUGE_A"
echo "Huge output B: $HUGE_B"

if [[ "$BUILD_MODE" != "true" ]]; then # Checks the build mode. If false, the script will verify the existing huge files.
  echo "Default action: verify existing huge files."
  verify_hugefiles
  echo "No build was performed."
  exit 0
fi

require_file "$INPUT_A"
require_file "$INPUT_B"

if [[ -e "$HUGE_A" || -e "$HUGE_B" ]]; then # Checks if the huge files exist. If true, it will check the force mode.
  if [[ "$FORCE_MODE" != "true" ]]; then # Checks the force mode. If false, it will exit with code 1.
    echo "Refusing to overwrite existing huge files without --force." >&2
    echo "Existing path check: $HUGE_A / $HUGE_B" >&2
    exit 1
  fi
  echo "Force mode enabled. Removing existing huge files."
  rm -f "$HUGE_A" "$HUGE_B" # Removes the huge files.
fi

echo "Building huge files inside the Module 8 directory."
echo "This follows the assignment pattern: append file1.txt and file2.txt 1000 times by default."
start_time="$(timer_now)" # Sets the start time.
index=1 # Sets the index.
while [[ "$index" -le "$REPEAT_COUNT" ]]; do # Checks the index.
  cat "$INPUT_A" >> "$HUGE_A" # Appends the input file A to the huge file A.
  cat "$INPUT_B" >> "$HUGE_B" # Appends the input file B to the huge file B.
  if [[ $((index % 50)) -eq 0 ]]; then # Checks the index every 50 iterations.
    echo "Completed append iteration $index of $REPEAT_COUNT" # Prints the completed append iteration.
  fi
  index=$((index + 1))
done
end_time="$(timer_now)" # Sets the end time.
elapsed="$(elapsed_seconds "$start_time" "$end_time")" # Calculates the elapsed time.

echo "Build elapsed seconds: $elapsed" # Prints the elapsed time.
record_build_event "$elapsed" # Records the build event.
verify_hugefiles # Verifies the huge files.
echo "Module 8 huge-file helper ended: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the end time.
