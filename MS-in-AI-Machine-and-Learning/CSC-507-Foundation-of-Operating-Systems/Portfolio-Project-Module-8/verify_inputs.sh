#!/usr/bin/env bash
# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

# Capture Module 8 input and system evidence before benchmarking.

set -euo pipefail


# ======
# Configuration
# ======

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" # Sets the script directory.
SYSTEM_INFO_FILE="$SCRIPT_DIR/system_info.txt" # Sets the system info file.
VERIFICATION_REPORT="$SCRIPT_DIR/verification_report.txt" # Sets the verification report.
ALLOW_SMALL_INPUTS="false" # Sets whether to allow small inputs.


# ======
# Helper Functions
# ======

# ---- print_usage()
print_usage() {
  cat <<'USAGE' # Prints the usage information.
Usage: ./verify_inputs.sh [--allow-small]

Default behavior requires hugefile1.txt and hugefile2.txt. Use --allow-small
only for local smoke tests where the billion-line files are not present.
USAGE
}
# ---- end print_usage()


# ---- log_line()
log_line() {
  printf "%s\n" "$*" | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Logs the line to the system info file and the verification report.
}
# ---- end log_line()


# ---- log_command()
log_command() {
  local label="$1" # Sets the label.
  shift # Removes the label from the arguments.

  log_line "" # Prints a blank line.
  log_line "$label" # Prints the label.
  if "$@" >>"$SYSTEM_INFO_FILE" 2>&1; then # Checks if the command is available and successful.
    "$@" >>"$VERIFICATION_REPORT" 2>&1 || true # Redirects the output to the verification report.
  else # If the command is not available or successful.
    printf "Command unavailable or failed: %s\n" "$*" | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Prints an error message.
  fi
}
# ---- end log_command()


# ---- detect_cpu_count()
detect_cpu_count() {
  if command -v nproc >/dev/null 2>&1; then # Checks if nproc is available.
    nproc # Returns the number of processors.
    return 0 # Returns 0 if successful.
  fi

  if command -v getconf >/dev/null 2>&1; then # Checks if getconf is available.
    getconf _NPROCESSORS_ONLN 2>/dev/null && return 0 # Returns 0 if successful.
  fi

  if command -v sysctl >/dev/null 2>&1; then # Checks if sysctl is available.
    sysctl -n hw.ncpu 2>/dev/null && return 0 # Returns 0 if successful.
  fi

  printf "unknown"
}
# ---- end detect_cpu_count()


# ---- describe_file()
describe_file() {
  local file_path="$1" # Sets the file path.
  local label="$2" # Sets the label.

  log_line "" # Prints a blank line.
  log_line "File: $label" # Prints the label.
  log_line "Path: $file_path" # Prints the file path.

  if [[ ! -f "$file_path" ]]; then # Checks if the file is present.
    log_line "Status: MISSING" # Prints that the file is missing.
    return 1 # Returns 1 if the file is missing.
  fi

  log_line "Status: present" # Prints that the file is present.
  log_line "Line count: $(wc -l < "$file_path" | tr -d ' ')" # Prints the line count.
  log_line "Byte count: $(wc -c < "$file_path" | tr -d ' ')" # Prints the byte count.
  log_line "Long listing: $(ls -lh "$file_path")" # Prints the long listing.
  return 0 # Returns 0 if the file is present.
}
# ---- end describe_file()


# ======
# Main Script
# ======

while [[ $# -gt 0 ]]; do # Loops through the arguments.
  case "$1" in # Checks the arguments.
    --allow-small)
      ALLOW_SMALL_INPUTS="true"
      shift
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_usage >&2
      exit 2
      ;;
  esac
done

: > "$SYSTEM_INFO_FILE" # Clears the system info file.
: > "$VERIFICATION_REPORT" # Clears the verification report.

log_line "Module 8 Input and Environment Verification" # Prints the module 8 input and environment verification header.
log_line "Timestamp UTC: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" # Prints the timestamp.
log_line "Working directory: $SCRIPT_DIR" # Prints the working directory.
log_line "Allow small inputs: $ALLOW_SMALL_INPUTS" # Prints whether small inputs are allowed.

log_line "" # Prints a blank line.
log_line "CPU count: $(detect_cpu_count)" # Prints the CPU count.

log_line "" # Prints a blank line.
log_line "Disk space for project directory:" # Prints the disk space for the project directory.
df -h "$SCRIPT_DIR" | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Prints the disk space for the project directory.

log_line "" # Prints a blank line.
log_line "Kernel information:" # Prints the kernel information.
uname -a | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Prints the kernel information.

log_line "" # Prints a blank line.
log_line "Operating-system release information:" # Prints the operating system release information.
if command -v lsb_release >/dev/null 2>&1; then # Checks if lsb_release is available.
  lsb_release -a 2>&1 | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Prints the operating system release information.
elif command -v sw_vers >/dev/null 2>&1; then # Checks if sw_vers is available.
  sw_vers 2>&1 | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Prints the operating system release information.
else
  log_line "lsb_release and sw_vers are not available."
fi

log_line "" # Prints a blank line.
log_line "Memory information:" # Prints the memory information.
if command -v free >/dev/null 2>&1; then # Checks if free is available.
  free -h | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Prints the memory information.
elif command -v vm_stat >/dev/null 2>&1; then # Checks if vm_stat is available.
  vm_stat | tee -a "$SYSTEM_INFO_FILE" "$VERIFICATION_REPORT" # Prints the memory information.
else
  log_line "free and vm_stat are not available."
fi

missing_required=0 # Sets the required file count to 0.
describe_file "$SCRIPT_DIR/file1.txt" "file1.txt" || missing_required=$((missing_required + 1)) # Checks if file1.txt is present.
describe_file "$SCRIPT_DIR/file2.txt" "file2.txt" || missing_required=$((missing_required + 1)) # Checks if file2.txt is present.

missing_huge=0 # Sets the huge file count to 0.
describe_file "$SCRIPT_DIR/hugefile1.txt" "hugefile1.txt" || missing_huge=$((missing_huge + 1)) # Checks if hugefile1.txt is present.
describe_file "$SCRIPT_DIR/hugefile2.txt" "hugefile2.txt" || missing_huge=$((missing_huge + 1)) # Checks if hugefile2.txt is present.

if [[ "$missing_required" -gt 0 ]]; then # Checks if the required file count is greater than 0.
  log_line ""
  log_line "Conclusion: required seed input files are missing."
  exit 1
fi

if [[ "$missing_huge" -gt 0 && "$ALLOW_SMALL_INPUTS" != "true" ]]; then # Checks if the huge file count is greater than 0 and if small inputs are not allowed.
  log_line ""
  log_line "Conclusion: hugefile1.txt and/or hugefile2.txt are missing."
  log_line "The Ubuntu benchmark requires both billion-line files before timing."
  log_line "Run ./build_hugefiles.sh --build only if the files must be regenerated."
  exit 1
fi

if [[ "$missing_huge" -gt 0 ]]; then
  log_line ""
  log_line "Conclusion: local small-input verification mode completed with missing huge files."
else
  log_line ""
  log_line "Conclusion: all required Module 8 input files are present."
fi
