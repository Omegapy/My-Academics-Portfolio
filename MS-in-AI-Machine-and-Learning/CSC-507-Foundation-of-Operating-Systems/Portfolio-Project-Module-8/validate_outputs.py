# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

"""Validate Module 8 summed output files.

Fast validation checks counts, file sizes, and boundary samples. Full
validation streams all three files and verifies every aligned output row.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# ======
# Constants
# ======

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_A = SCRIPT_DIR / "hugefile1.txt" # Default first input file path
DEFAULT_INPUT_B = SCRIPT_DIR / "hugefile2.txt" # Default second input file path
DEFAULT_OUTPUT = SCRIPT_DIR / "totalfile.txt" # Default output file path
DEFAULT_REPORT = SCRIPT_DIR / "verification_report.txt" # Default verification report path
DEFAULT_CSV = SCRIPT_DIR / "validation_results.csv" # Default CSV path
SAMPLE_SIZE = 5 # Default sample size

CSV_FIELDNAMES = [
    "label", # Label for the validation
    "mode", # Mode of validation (fast or full)
    "input_file_a", # First input file path
    "input_file_b", # Second input file path
    "output_file", # Output file path
    "start_timestamp", # Start timestamp of validation
    "end_timestamp", # End timestamp of validation
    "elapsed_seconds", # Elapsed time in seconds
    "elapsed_hms", # Elapsed time in hours, minutes, seconds
    "line_count_a", # Line count for the first input file
    "line_count_b", # Line count for the second input file
    "line_count_output", # Line count for the output file
    "output_byte_count", # Size of the output file in bytes
    "first_five_status", # Status of first-five-row validation
    "last_five_status", # Status of last-five-row validation
    "full_validation_status", # Status of full stream validation
    "overall_status", # Whether the validation passed overall
    "notes", # Notes about the validation
]


# ======
# Data Models
# ======


# ---- class ValidationResult
@dataclass(frozen=True)
class ValidationResult:
    """Store one validation run.

    Args:
        label: Method label associated with the output being validated.
        mode: Validation mode, either fast or full.
        input_file_a: First input file.
        input_file_b: Second input file.
        output_file: Output file being validated.
        start_timestamp: UTC timestamp captured before validation.
        end_timestamp: UTC timestamp captured after validation.
        elapsed_seconds: Validation runtime.
        line_count_a: Line count for the first input file.
        line_count_b: Line count for the second input file.
        line_count_output: Line count for the output file.
        output_byte_count: Output file size in bytes.
        first_five_status: Status of first-five-row validation.
        last_five_status: Status of last-five-row validation.
        full_validation_status: Status of full stream validation.
        overall_status: Whether the validation passed overall.
        notes: Human-readable validation detail.

    Returns:
        None.
    """

    label: str
    mode: str
    input_file_a: Path
    input_file_b: Path
    output_file: Path
    start_timestamp: str
    end_timestamp: str
    elapsed_seconds: float
    line_count_a: int
    line_count_b: int
    line_count_output: int
    output_byte_count: int
    first_five_status: str
    last_five_status: str
    full_validation_status: str
    overall_status: str
    notes: str

    # ---- to_csv_row()
    def to_csv_row(self) -> dict[str, str | int]:
        """Convert the validation result to a CSV-safe dictionary.

        Args:
            None.

        Returns:
            Dictionary keyed by validation CSV columns.
        """
        return {
            "label": self.label,
            "mode": self.mode,
            "input_file_a": str(self.input_file_a),
            "input_file_b": str(self.input_file_b),
            "output_file": str(self.output_file),
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "elapsed_seconds": f"{self.elapsed_seconds:.6f}",
            "elapsed_hms": format_duration(self.elapsed_seconds),
            "line_count_a": self.line_count_a,
            "line_count_b": self.line_count_b,
            "line_count_output": self.line_count_output,
            "output_byte_count": self.output_byte_count,
            "first_five_status": self.first_five_status,
            "last_five_status": self.last_five_status,
            "full_validation_status": self.full_validation_status,
            "overall_status": self.overall_status,
            "notes": self.notes,
        }

    # ---- end to_csv_row()


# ---- end class ValidationResult


# ======
# Timing and CSV Helpers
# ======


# ---- normalize_module_path()
def normalize_module_path(path_value: Path) -> Path:
    """Resolve a path while keeping it inside this Module 8 folder.

    Args:
        path_value: File path supplied by the user or wrapper.

    Returns:
        Absolute path inside the Module 8 project directory.

    Raises:
        ValueError: If the path points outside the Module 8 directory.
    """
    candidate_path = path_value if path_value.is_absolute() else SCRIPT_DIR / path_value
    resolved_path = candidate_path.resolve(strict=False)
    module_root = SCRIPT_DIR.resolve()

    try:
        resolved_path.relative_to(module_root)
    except ValueError as exc:
        raise ValueError(
            "Module 8 validation may only read or write files inside "
            f"{module_root}; rejected path: {path_value}"
        ) from exc

    return resolved_path


# ---- end normalize_module_path()


# ---- timestamp_utc()
def timestamp_utc() -> str:
    """Return the current UTC timestamp in ISO-like form.

    Args:
        None.

    Returns:
        Timestamp string with a trailing Z marker.
    """
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---- end timestamp_utc()


# ---- format_duration()
def format_duration(total_seconds: float) -> str:
    """Format elapsed seconds as HH:MM:SS.

    Args:
        total_seconds: Elapsed runtime in seconds.

    Returns:
        Runtime formatted as HH:MM:SS.
    """
    rounded_seconds = max(0, int(round(total_seconds))) # Round the elapsed time to the nearest second
    hours, remainder = divmod(rounded_seconds, 3600) # Calculate hours and remainder
    minutes, seconds = divmod(remainder, 60) # Calculate minutes and seconds
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" # Return the formatted time


# ---- end format_duration()


# ---- ensure_csv_header()
def ensure_csv_header(csv_file: Path) -> None:
    """Create the validation CSV header when needed.

    Args:
        csv_file: Validation CSV path.

    Returns:
        None.
    """
    csv_file.parent.mkdir(parents=True, exist_ok=True)
    if csv_file.exists() and csv_file.stat().st_size > 0: # Check if the CSV file exists and has a size greater than 0
        return

    with csv_file.open("w", encoding="utf-8", newline="") as handle: # Open the CSV file for writing
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES) # Create a CSV writer
        writer.writeheader() # Write the header row


# ---- end ensure_csv_header()


# ---- append_csv_row()
def append_csv_row(csv_file: Path, result: ValidationResult) -> None:
    """Append one validation row.

    Args:
        csv_file: Validation CSV path.
        result: Validation result to append.

    Returns:
        None.
    """
    ensure_csv_header(csv_file) # Ensure the CSV header exists
    with csv_file.open("a", encoding="utf-8", newline="") as handle: # Open the CSV file for appending
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES) # Create a CSV writer
        writer.writerow(result.to_csv_row()) # Write the result row


# ---- end append_csv_row()


# ======
# File Inspection Helpers
# ======


# ---- require_file()
def require_file(file_path: Path) -> None:
    """Fail clearly if a required file is absent.

    Args:
        file_path: File path to check.

    Returns:
        None.

    Raises:
        FileNotFoundError: If the file is missing.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"required file not found: {file_path}") # Raise a file not found error if the file is missing


# ---- end require_file()


# ---- count_lines()
def count_lines(file_path: Path) -> int:
    """Count lines using the operating system wc utility.

    Args:
        file_path: File to count.

    Returns:
        Integer line count.
    """
    result = subprocess.run( 
        ["wc", "-l", str(file_path)], # Run the wc utility to count the lines
        check=True, # Raise an error if the command fails
        capture_output=True, # Capture the output
        text=True, # Decode the output as text
    )
    return int(result.stdout.strip().split()[0]) # Return the line count


# ---- end count_lines()


# ---- read_first_lines()
def read_first_lines(file_path: Path, limit: int = SAMPLE_SIZE) -> list[str]:
    """Read the first lines from a file.

    Args:
        file_path: File to inspect.
        limit: Maximum number of lines to return.

    Returns:
        List of stripped line values.
    """
    rows: list[str] = []
    with file_path.open("r", encoding="utf-8") as handle:
        for _ in range(limit): # Read the first 'limit' lines
            line = handle.readline() # Read a single line
            if not line: # If the line is empty, break the loop
                break
            rows.append(line.strip()) # Strip whitespace from the line and append it to the list
    return rows


# ---- end read_first_lines()


# ---- read_last_lines()
def read_last_lines(file_path: Path, limit: int = SAMPLE_SIZE) -> list[str]:
    """Read the last lines from a file.

    Args:
        file_path: File to inspect.
        limit: Maximum number of lines to return.

    Returns:
        List of stripped line values.
    """
    rows: deque[str] = deque(maxlen=limit) # Create a deque with a maximum length of 'limit'
    with file_path.open("r", encoding="utf-8") as handle: 
        for line in handle: # Iterate through each line in the file
            rows.append(line.strip()) # Strip whitespace from the line and append it to the deque
    return list(rows) # Convert the deque to a list and return it


# ---- end read_last_lines()


# ---- sample_status()
def sample_status(
    sample_a: Iterable[str],
    sample_b: Iterable[str],
    sample_output: Iterable[str],
) -> tuple[str, str]:
    """Check whether sampled output rows equal input sums.

    Args:
        sample_a: Sample rows from first input.
        sample_b: Sample rows from second input.
        sample_output: Sample rows from output file.

    Returns:
        Tuple containing status and detail text.
    """
    rows_a = list(sample_a) # Convert the sample to a list
    rows_b = list(sample_b) # Convert the sample to a list
    rows_output = list(sample_output) # Convert the sample to a list

    if not (len(rows_a) == len(rows_b) == len(rows_output)): # Check if the sample lengths are equal
        return "failed", "sample lengths differ" # Return a failed status with a message

    for offset, (raw_a, raw_b, raw_output) in enumerate(
        zip(rows_a, rows_b, rows_output), start=1 # Iterate through the samples with an offset
    ):
        try:
            expected_value = int(raw_a) + int(raw_b) # Calculate the expected value
            observed_value = int(raw_output) # Get the observed value
        except ValueError:
            return "failed", f"non-integer sample value at sample row {offset}" # Return a failed status with a message

        if observed_value != expected_value: # Check if the observed value equals the expected value
            return (
                "failed",
                f"sample row {offset} expected {expected_value} got {observed_value}", # Return a failed status with a message
            )

    return "passed", f"{len(rows_output)} sampled rows matched" # Return a passed status with a message


# ---- end sample_status()


# ---- full_stream_status()
def full_stream_status(input_file_a: Path, input_file_b: Path, output_file: Path) -> str:
    """Verify every output line against both input files.

    Args:
        input_file_a: First input file.
        input_file_b: Second input file.
        output_file: Output file to validate.

    Returns:
        Passed status or a failure explanation.
    """
    checked_lines = 0
    with input_file_a.open("r", encoding="utf-8") as handle_a, input_file_b.open(
        "r", encoding="utf-8"
    ) as handle_b, output_file.open("r", encoding="utf-8") as output_handle: # Open the input files and output file for reading
       # Process both input files line-by-line
       while True:
            line_a = handle_a.readline() # Read a line from the first input file
            line_b = handle_b.readline() # Read a line from the second input file
            line_output = output_handle.readline() # Read a line from the output file

            if not line_a and not line_b and not line_output: # Check if all files are exhausted
                return f"passed:{checked_lines}" # Return a passed status with the line count

            checked_lines += 1 # Increment the line counter
            if not line_a or not line_b or not line_output: # Check if any files are not exhausted
                return f"failed:line-count-mismatch-at-{checked_lines}" # Return a failed status with the line count

            try:
                expected_value = int(line_a.strip()) + int(line_b.strip()) # Calculate the expected value
                observed_value = int(line_output.strip()) # Get the observed value
            except ValueError:
                return f"failed:non-integer-at-{checked_lines}" # Return a failed status with the line count

            if observed_value != expected_value: # Check if the observed value equals the expected value
                return (
                    f"failed:mismatch-at-{checked_lines}:" # Return a failed status with the line count
                    f"expected-{expected_value}:got-{observed_value}" # Return the expected and observed values
                ) # Return a failed status with the line count and values


# ---- end full_stream_status()


# ======
# Validation Workflow
# ======


# ---- validate_outputs()
def validate_outputs(
    input_file_a: Path,
    input_file_b: Path,
    output_file: Path,
    *,
    mode: str,
    label: str,
) -> ValidationResult:
    """Validate output files in fast or full mode.

    Args:
        input_file_a: First input file.
        input_file_b: Second input file.
        output_file: Output file to validate.
        mode: Validation mode, either fast or full.
        label: Method label for the validation row.

    Returns:
        ValidationResult with measured evidence.
    """
    require_file(input_file_a) # Require the first input file
    require_file(input_file_b) # Require the second input file
    require_file(output_file) # Require the output file

    start_timestamp = timestamp_utc() # Record the start timestamp
    start_counter = time.perf_counter() # Record the start counter

    line_count_a = count_lines(input_file_a) # Count the number of lines in the first input file
    line_count_b = count_lines(input_file_b) # Count the number of lines in the second input file
    line_count_output = count_lines(output_file) # Count the number of lines in the output file
    output_byte_count = output_file.stat().st_size # Get the size of the output file

    # Check the first lines of each file for matching sums
    first_status, first_notes = sample_status(
        read_first_lines(input_file_a),
        read_first_lines(input_file_b),
        read_first_lines(output_file),
    )
    
    # Check the last lines of each file for matching sums
    last_status, last_notes = sample_status(
        read_last_lines(input_file_a),
        read_last_lines(input_file_b),
        read_last_lines(output_file),
    )

    full_status = "not_run" # Default status to not_run
    if mode == "full": # Check if the mode is full
        full_status = full_stream_status(input_file_a, input_file_b, output_file) # Get the full status

    count_status = line_count_a == line_count_b == line_count_output # Check if the line counts match
    sample_passed = first_status == "passed" and last_status == "passed" # Check if the samples passed
    full_passed = mode == "fast" or full_status.startswith("passed:") # Check if the full status is passed
    overall_status = "passed" if count_status and sample_passed and full_passed else "failed" # Get the overall status

    elapsed_seconds = time.perf_counter() - start_counter # Calculate the elapsed time
    end_timestamp = timestamp_utc() # Get the end timestamp
    notes = (
        f"line_counts_match={str(count_status).lower()}; " # Get the line count status
        f"first={first_notes}; last={last_notes}"
    )
    if mode == "full": # Check if the mode is full
        notes = f"{notes}; full={full_status}" # Get the full status

    return ValidationResult(
        label=label, # Get the method label
        mode=mode, # Get the validation mode
        input_file_a=input_file_a, # Get the first input file
        input_file_b=input_file_b, # Get the second input file
        output_file=output_file, # Get the output file
        start_timestamp=start_timestamp, # Get the start timestamp
        end_timestamp=end_timestamp, # Get the end timestamp
        elapsed_seconds=elapsed_seconds, # Get the elapsed time
        line_count_a=line_count_a, # Get the number of lines in the first input file
        line_count_b=line_count_b, # Get the number of lines in the second input file
        line_count_output=line_count_output, # Get the number of lines in the output file
        output_byte_count=output_byte_count, # Get the size of the output file
        first_five_status=first_status, # Get the first five status
        last_five_status=last_status, # Get the last five status
        full_validation_status=full_status, # Get the full validation status
        overall_status=overall_status, # Get the overall status
        notes=notes, # Get the notes
    )


# ---- end validate_outputs()


# ---- write_report()
def write_report(report_file: Path, result: ValidationResult) -> None:
    """Append a human-readable validation report.

    Args:
        report_file: Report file path.
        result: Validation result to append.

    Returns:
        None.
    """
    report_file.parent.mkdir(parents=True, exist_ok=True) # Create the report directory if it doesn't exist
    with report_file.open("a", encoding="utf-8") as handle: # Open the report file for appending
        handle.write("\n") # Add a newline
        handle.write("## Module 8 Output Validation\n") # Add a section header
        handle.write(f"Label: {result.label}\n") # Add the method label
        handle.write(f"Mode: {result.mode}\n") # Add the validation mode
        handle.write(f"Start: {result.start_timestamp}\n") # Add the start timestamp
        handle.write(f"End: {result.end_timestamp}\n") # Add the end timestamp
        handle.write(f"Elapsed seconds: {result.elapsed_seconds:.6f}\n") # Add the elapsed time
        handle.write(f"Input A lines: {result.line_count_a}\n") # Add the number of lines in the first input file
        handle.write(f"Input B lines: {result.line_count_b}\n") # Add the number of lines in the second input file
        handle.write(f"Output lines: {result.line_count_output}\n") # Add the number of lines in the output file
        handle.write(f"Output bytes: {result.output_byte_count}\n") # Add the size of the output file
        handle.write(f"First five status: {result.first_five_status}\n") # Add the first five status
        handle.write(f"Last five status: {result.last_five_status}\n") # Add the last five status
        handle.write(f"Full validation status: {result.full_validation_status}\n") # Add the full validation status
        handle.write(f"Overall status: {result.overall_status}\n") # Add the overall status
        handle.write(f"Notes: {result.notes}\n") # Add the notes


# ---- end write_report()


# ======
# Command-Line Interface
# ======


# ---- build_parser()
def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    Args:
        None.

    Returns:
        Configured ArgumentParser.
    """
    parser = argparse.ArgumentParser(description="Validate Module 8 output files.") # Create an argument parser
    parser.add_argument("--mode", choices=("fast", "full"), default="fast") # Add a mode argument with choices for fast or full
    parser.add_argument("--label", default="manual_validation") # Add a label argument with a default value
    parser.add_argument("--input-a", type=Path, default=DEFAULT_INPUT_A) # Add an input-a argument with a default value
    parser.add_argument("--input-b", type=Path, default=DEFAULT_INPUT_B) # Add an input-b argument with a default value
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT) # Add an output argument with a default value
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT) # Add a report argument with a default value
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV) # Add a csv argument with a default value
    return parser


# ---- end build_parser()


# ---- main()
def main(argv: list[str] | None = None) -> int:
    """Run the validation command-line interface.

    Args:
        argv: Optional command-line argument list.

    Returns:
        Process exit code.
    """
    parser = build_parser() # Build the command-line parser
    args = parser.parse_args(argv) # Parse the command-line arguments

    try:
        input_file_a = normalize_module_path(Path(args.input_a)) # Normalize the first input file path
        input_file_b = normalize_module_path(Path(args.input_b)) # Normalize the second input file path
        output_file = normalize_module_path(Path(args.output)) # Normalize the output file path
        csv_file = normalize_module_path(Path(args.csv)) # Normalize the CSV file path
        report_file = normalize_module_path(Path(args.report)) # Normalize the report file path

        result = validate_outputs(
            input_file_a,
            input_file_b,
            output_file,
            mode=args.mode,
            label=args.label,
        ) # Validate the outputs
        append_csv_row(csv_file, result) # Append the validation result to the CSV file
        write_report(report_file, result) # Append the validation result to the report file
    except (OSError, ValueError, subprocess.CalledProcessError) as exc: # Handle errors
        print(f"ERROR: {exc}", file=sys.stderr) # Print the error
        return 1

    print(f"Validation label: {result.label}") # Print the validation label
    print(f"Validation mode: {result.mode}") # Print the validation mode
    print(f"Overall status: {result.overall_status}") # Print the overall status
    print(f"Elapsed seconds: {result.elapsed_seconds:.6f}") # Print the elapsed time
    print(f"Validation CSV row appended: {csv_file}") # Print the CSV file path
    print(f"Verification report updated: {report_file}") # Print the report file path
    return 0 if result.overall_status == "passed" else 1 # Return 0 if the overall status is passed, 1 otherwise


# ---- end main()


if __name__ == "__main__":
    raise SystemExit(main())
