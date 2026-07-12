# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

"""Stream two integer files and write line-aligned sums.

The Module 8 assignment requires processing very large files without loading
the full inputs into memory. This module provides one shared implementation for
the baseline, two-program parallel, and ten-way parallel scripts.
"""

from __future__ import annotations

import argparse # Used to parse command line arguments
import csv # Used to write CSV files
import os # Used to get CPU count
import platform # Used to get platform information
import sys # Used to exit the program
import time # Used to measure time
from dataclasses import dataclass # Used to create data classes
from pathlib import Path # Used to work with file paths


# ======
# Constants
# ======

SCRIPT_DIR = Path(__file__).resolve().parent # Used to get the directory of the script
DEFAULT_INPUT_A = SCRIPT_DIR / "hugefile1.txt" # Default input file A
DEFAULT_INPUT_B = SCRIPT_DIR / "hugefile2.txt" # Default input file B
DEFAULT_OUTPUT = SCRIPT_DIR / "totalfile.txt" # Default output file
DEFAULT_CSV = SCRIPT_DIR / "benchmark_results.csv" # Default CSV file
DEFAULT_BUFFER_SIZE = 1024 * 1024 # Default buffer size
DEFAULT_BATCH_LINES = 8192 # Default number of lines to process at a time

CSV_FIELDNAMES = [ # Used to define the columns in the CSV file
    "method",
    "input_file_a",
    "input_file_b",
    "output_file",
    "start_timestamp",
    "end_timestamp",
    "elapsed_seconds",
    "elapsed_hms",
    "processed_line_count",
    "output_byte_count",
    "python_version",
    "platform_name",
    "platform_release",
    "cpu_count",
    "verification_status",
    "notes",
]


# ======
# Data Models
# ======


# ---- class SumResult
@dataclass(frozen=True)
class SumResult:
    """Store the measured result for one summation run.

    Args:
        method: Stable benchmark method name.
        input_file_a: First input file.
        input_file_b: Second input file.
        output_file: Output file containing one sum per line.
        start_timestamp: UTC timestamp captured before processing.
        end_timestamp: UTC timestamp captured after processing.
        elapsed_seconds: Processing time measured with time.perf_counter().
        processed_line_count: Number of line pairs processed.
        output_byte_count: Size of the output file in bytes.
        verification_status: Short correctness status.
        notes: Additional benchmark notes.

    Returns:
        None.
    """

    method: str # Stable benchmark method name
    input_file_a: Path # First input file
    input_file_b: Path # Second input file
    output_file: Path # Output file
    start_timestamp: str # Start timestamp
    end_timestamp: str # End timestamp
    elapsed_seconds: float # Elapsed time
    processed_line_count: int # Number of lines processed
    output_byte_count: int # Size of output file in bytes
    verification_status: str # Verification status
    notes: str # Additional benchmark notes

    # ---- to_csv_row()
    def to_csv_row(self) -> dict[str, str | int]:
        """Convert the result to a CSV-safe dictionary.

        Args:
            None.

        Returns:
            Dictionary keyed by the stable benchmark CSV columns.
        """
        return {
            "method": self.method, # Stable benchmark method name
            "input_file_a": str(self.input_file_a), # First input file
            "input_file_b": str(self.input_file_b), # Second input file
            "output_file": str(self.output_file), # Output file
            "start_timestamp": self.start_timestamp, # Start timestamp
            "end_timestamp": self.end_timestamp, # End timestamp
            "elapsed_seconds": f"{self.elapsed_seconds:.6f}",
            "elapsed_hms": format_duration(self.elapsed_seconds), # Elapsed time in hours, minutes, seconds
            "processed_line_count": self.processed_line_count, # Number of lines processed
            "output_byte_count": self.output_byte_count, # Size of output file in bytes
            "python_version": platform.python_version(), # Python version
            "platform_name": platform.system(), # Platform name
            "platform_release": platform.release(), # Platform release
            "cpu_count": os.cpu_count() or 0, # CPU count
            "verification_status": self.verification_status, # Verification status
            "notes": self.notes, # Additional benchmark notes
        }

    # ---- end to_csv_row()


# ---- end class SumResult


# ======
# Timing and CSV Helpers
# ======


# ---- normalize_module_path()
def normalize_module_path(path_value: Path) -> Path:
    """Resolve a path while keeping it inside this Module 8 folder.

    Args:
        path_value: File or directory path supplied by the user or wrapper.

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
            "Module 8 scripts may only read or write files inside "
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
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) # Format current UTC time as ISO-like string


# ---- end timestamp_utc()


# ---- format_duration()
def format_duration(total_seconds: float) -> str:
    """Format elapsed seconds as HH:MM:SS.

    Args:
        total_seconds: Elapsed runtime in seconds.

    Returns:
        Runtime formatted as HH:MM:SS.
    """
    rounded_seconds = max(0, int(round(total_seconds))) # Round total seconds to nearest integer, ensuring non-negative value
    hours, remainder = divmod(rounded_seconds, 3600) # Calculate hours and remaining seconds
    minutes, seconds = divmod(remainder, 60) # Calculate minutes and remaining seconds
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" # Format as HH:MM:SS


# ---- end format_duration()


# ---- ensure_csv_header()
def ensure_csv_header(csv_file: Path) -> None:
    """Create the benchmark CSV header when needed.

    Args:
        csv_file: Benchmark CSV path.

    Returns:
        None.
    """
    csv_file.parent.mkdir(parents=True, exist_ok=True) # Create the benchmark CSV directory if it doesn't exist
    if csv_file.exists() and csv_file.stat().st_size > 0: # Check if the CSV file already exists and has content
        return

    with csv_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES) # Create a CSV DictWriter with the stable field order
        writer.writeheader() # Write the header row to the CSV file


# ---- end ensure_csv_header()


# ---- append_csv_row()
def append_csv_row(csv_file: Path, row: dict[str, str | int]) -> None:
    """Append one benchmark row using the stable field order.

    Args:
        csv_file: Benchmark CSV path.
        row: CSV row data.

    Returns:
        None.
    """
    ensure_csv_header(csv_file) # Ensure the CSV file has a header row
    with csv_file.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES) # Create a CSV DictWriter with the stable field order
        writer.writerow(row) # Write the row to the CSV file


# ---- end append_csv_row()


# ======
# Streaming Processing
# ======


# ---- parse_integer_line()
def parse_integer_line(raw_line: str, file_path: Path, line_number: int) -> int:
    """Parse one integer line and produce useful errors.

    Args:
        raw_line: Raw line read from the input file.
        file_path: Source file path used in error messages.
        line_number: One-based line number.

    Returns:
        Parsed integer value.

    Raises:
        ValueError: If the line is blank or not an integer.
    """
    stripped_line = raw_line.strip() # Strip leading/trailing whitespace from the line
    if not stripped_line: # Check if the line is empty after stripping whitespace
        raise ValueError(f"blank line in {file_path} at line {line_number}")

    try:
        return int(stripped_line) # Attempt to convert the stripped line to an integer
    except ValueError as exc:
        raise ValueError(
            f"non-integer value in {file_path} at line {line_number}: " # Format the non-integer value for the error message
            f"{stripped_line!r}"  # Format the non-integer value for the error message
        ) from exc


# ---- end parse_integer_line()


# ---- stream_sum_files()
def stream_sum_files(
    input_file_a: Path, # First input file
    input_file_b: Path, # Second input file
    output_file: Path, # Output file
    *,
    method: str, # Stable benchmark method name
    notes: str = "", # Optional notes written to the benchmark CSV
    buffer_size: int = DEFAULT_BUFFER_SIZE, # File I/O buffer size in bytes
    batch_lines: int = DEFAULT_BATCH_LINES, # Number of output rows to batch before writing
) -> SumResult:
    """Stream two aligned input files and write summed output lines.

    Args:
        input_file_a: First integer input file.
        input_file_b: Second integer input file.
        output_file: Output file to create.
        method: Stable benchmark method name.
        notes: Optional notes written to the benchmark CSV.
        buffer_size: File I/O buffer size in bytes.
        batch_lines: Number of output rows to batch before writing.

    Returns:
        SumResult containing timing and verification metadata.

    Raises:
        FileNotFoundError: If either input file is missing.
        ValueError: If inputs have mismatched lengths or invalid integers.
    """
    # SAFETY CHECK: Fail before truncating an output when inputs are absent.
    if not input_file_a.is_file(): # Check if the first input file exists
        raise FileNotFoundError(f"input file not found: {input_file_a}") # Raise FileNotFoundError if the first input file is not found
    if not input_file_b.is_file(): # Check if the second input file exists
        raise FileNotFoundError(f"input file not found: {input_file_b}") # Raise FileNotFoundError if the second input file is not found
    if batch_lines < 1: # Check if batch_lines is less than 1
        raise ValueError("batch_lines must be at least 1") # Raise ValueError if batch_lines is less than 1

    output_file.parent.mkdir(parents=True, exist_ok=True) # Create the benchmark CSV directory if it doesn't exist
    start_timestamp = timestamp_utc() # Record the start timestamp
    start_counter = time.perf_counter() # Record the start time
    processed_line_count = 0 # Initialize the number of lines processed
    pending_output: list[str] = [] # Initialize the list of output rows

    with input_file_a.open(
        "r", encoding="utf-8", buffering=buffer_size # Open the first input file for reading with UTF-8 encoding and specified buffer size
    ) as handle_a, input_file_b.open(
        "r", encoding="utf-8", buffering=buffer_size # Open the second input file for reading with UTF-8 encoding and specified buffer size
    ) as handle_b, output_file.open(
        "w", encoding="utf-8", buffering=buffer_size, newline="\n" # Open the output file for writing with UTF-8 encoding and specified buffer size
    ) as output_handle:
        while True: # Loop until both files are read completely
            line_a = handle_a.readline() # Read a line from the first input file
            line_b = handle_b.readline() # Read a line from the second input file

            # VALIDATION: Both files must end at the same logical row.
            if not line_a and not line_b: # Check if both files are read completely
                break # Exit the loop
            if not line_a or not line_b: # Check if one file is read completely but the other is not
                next_line = processed_line_count + 1 # Calculate the next line number
                raise ValueError(
                    "input line count mismatch at aligned line "
                    f"{next_line}: {input_file_a} and {input_file_b}" # Format the input line count mismatch error message
                )

            processed_line_count += 1 # Increment the number of lines processed
            value_a = parse_integer_line(line_a, input_file_a, processed_line_count) # Parse the first input file line
            value_b = parse_integer_line(line_b, input_file_b, processed_line_count) # Parse the second input file line
            pending_output.append(f"{value_a + value_b}\n") # Append the summed value to the pending output list

            if len(pending_output) >= batch_lines: # Check if the pending output list has reached the batch size
                output_handle.writelines(pending_output) # Write the pending output list to the output file
                pending_output.clear() # Clear the pending output list

        if pending_output: # Check if there is any pending output
            output_handle.writelines(pending_output) # Write the pending output list to the output file

    elapsed_seconds = time.perf_counter() - start_counter # Calculate the elapsed time
    end_timestamp = timestamp_utc() # Record the end timestamp
    output_byte_count = output_file.stat().st_size # Get the size of the output file in bytes

    return SumResult(
        method=method, # Stable benchmark method name
        input_file_a=input_file_a, # First input file path
        input_file_b=input_file_b, # Second input file path
        output_file=output_file, # Output file path
        start_timestamp=start_timestamp, # Start timestamp
        end_timestamp=end_timestamp, # End timestamp
        elapsed_seconds=elapsed_seconds, # Elapsed time in seconds
        processed_line_count=processed_line_count, # Number of lines processed
        output_byte_count=output_byte_count, # Size of the output file in bytes
        verification_status="passed", # Verification status
        notes=notes, # Optional notes written to the benchmark CSV
    )


# ---- end stream_sum_files()


# ======
# Command-Line Interface
# ======


# ---- build_parser()
def build_parser(
    *,
    default_method: str,
    default_input_a: Path,
    default_input_b: Path,
    default_output: Path,
    default_csv: Path,
) -> argparse.ArgumentParser:
    """Build the command-line parser.

    Args:
        default_method: Default benchmark method name.
        default_input_a: Default first input file.
        default_input_b: Default second input file.
        default_output: Default output file.
        default_csv: Default benchmark CSV file.

    Returns:
        Configured ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        description="Stream two integer files and write line-aligned sums."
    )
    parser.add_argument("--method", default=default_method) # Default benchmark method name
    parser.add_argument("--input-a", type=Path, default=default_input_a) # Default first input file path
    parser.add_argument("--input-b", type=Path, default=default_input_b) # Default second input file path
    parser.add_argument("--output", type=Path, default=default_output) # Default output file path
    parser.add_argument("--csv", type=Path, default=default_csv) # Default benchmark CSV file path
    parser.add_argument("--notes", default="") # Optional notes written to the benchmark CSV
    parser.add_argument("--buffer-size", type=int, default=DEFAULT_BUFFER_SIZE) # File I/O buffer size in bytes
    parser.add_argument("--batch-lines", type=int, default=DEFAULT_BATCH_LINES) # Number of output rows to batch before writing
    parser.add_argument(
        "--event-only",
        action="store_true",
        help="append a timing-only benchmark row without processing files", # Append a timing-only benchmark row without processing files
    )
    parser.add_argument("--elapsed-seconds", type=float, default=0.0) # Elapsed time in seconds
    parser.add_argument("--start-timestamp", default="") # Start timestamp
    parser.add_argument("--end-timestamp", default="") # End timestamp
    parser.add_argument("--processed-lines", type=int, default=0) # Number of lines processed
    parser.add_argument("--verification-status", default="recorded") # Verification status
    return parser # Configured ArgumentParser


# ---- end build_parser()


# ---- record_event_row()
def record_event_row(args: argparse.Namespace) -> None:
    """Record a timing-only event row in the benchmark CSV.

    Args:
        args: Parsed command-line arguments.

    Returns:
        None.
    """
    input_file_a = normalize_module_path(Path(args.input_a)) if args.input_a else None # Normalize the first input file path
    input_file_b = normalize_module_path(Path(args.input_b)) if args.input_b else None # Normalize the second input file path
    output_path = normalize_module_path(Path(args.output)) if args.output else None # Normalize the output file path
    csv_file = normalize_module_path(Path(args.csv)) # Normalize the benchmark CSV file path
    output_byte_count = 0 # Initialize the output file byte count
    if output_path and output_path.is_file(): # Check if the output file exists
        output_byte_count = output_path.stat().st_size # Get the size of the output file in bytes

    row = {
        "method": args.method, # Stable benchmark method name
        "input_file_a": str(input_file_a) if input_file_a else "", # First input file path
        "input_file_b": str(input_file_b) if input_file_b else "", # Second input file path
        "output_file": str(output_path) if output_path else "", # Output file path
        "start_timestamp": args.start_timestamp or timestamp_utc(), # Start timestamp
        "end_timestamp": args.end_timestamp or timestamp_utc(), # End timestamp
        "elapsed_seconds": f"{args.elapsed_seconds:.6f}", # Elapsed time in seconds
        "elapsed_hms": format_duration(args.elapsed_seconds), # Elapsed time in hours, minutes, seconds
        "processed_line_count": args.processed_lines, # Number of lines processed
        "output_byte_count": output_byte_count, # Size of the output file in bytes
        "python_version": platform.python_version(), # Python version
        "platform_name": platform.system(), # Operating system name
        "platform_release": platform.release(), # Operating system release
        "cpu_count": os.cpu_count() or 0, # Number of CPU cores
        "verification_status": args.verification_status, # Verification status
        "notes": args.notes, # Optional notes written to the benchmark CSV
    }
    append_csv_row(csv_file, row) # Append the benchmark row to the CSV file


# ---- end record_event_row()


# ---- main()
def main(
    argv: list[str] | None = None,
    *,
    default_method: str = "baseline_single_process",
    default_input_a: Path = DEFAULT_INPUT_A,
    default_input_b: Path = DEFAULT_INPUT_B,
    default_output: Path = DEFAULT_OUTPUT,
    default_csv: Path = DEFAULT_CSV,
) -> int:
    """Run the summation command-line interface.

    Args:
        argv: Optional command-line argument list.
        default_method: Default method name for wrapper scripts.
        default_input_a: Default first input file for wrapper scripts.
        default_input_b: Default second input file for wrapper scripts.
        default_output: Default output file for wrapper scripts.
        default_csv: Default benchmark CSV path for wrapper scripts.

    Returns:
        Process exit code.
    """
    parser = build_parser(
        default_method=default_method, # Default benchmark method name
        default_input_a=default_input_a, # Default first input file path
        default_input_b=default_input_b, # Default second input file path
        default_output=default_output, # Default output file path
        default_csv=default_csv, # Default benchmark CSV file path
    )
    args = parser.parse_args(argv) # Parse the command-line arguments

    try:
        if args.event_only: # Check if the event-only flag is set
            record_event_row(args) # Record the event-only benchmark row
            return 0 # Return 0 to indicate successful execution

        input_file_a = normalize_module_path(Path(args.input_a)) # Normalize the first input file path
        input_file_b = normalize_module_path(Path(args.input_b)) # Normalize the second input file path
        output_file = normalize_module_path(Path(args.output)) # Normalize the output file path
        csv_file = normalize_module_path(Path(args.csv)) # Normalize the benchmark CSV file path

        result = stream_sum_files(
            input_file_a, # First input file path
            input_file_b, # Second input file path
            output_file, # Output file path
            method=args.method, # Stable benchmark method name
            notes=args.notes, # Optional notes written to the benchmark CSV
            buffer_size=args.buffer_size, # File I/O buffer size in bytes
            batch_lines=args.batch_lines, # Number of output rows to batch before writing
        )
        append_csv_row(csv_file, result.to_csv_row()) # Append the benchmark row to the CSV file
    except (OSError, ValueError) as exc: # Catch OS and value errors
        print(f"ERROR: {exc}", file=sys.stderr) # Print the error message
        return 1 # Return 1 to indicate an error

    print(f"Method: {result.method}") # Print the benchmark method name
    print(f"Input A: {result.input_file_a}") # Print the first input file path
    print(f"Input B: {result.input_file_b}") # Print the second input file path
    print(f"Output: {result.output_file}") # Print the output file path
    print(f"Processed lines: {result.processed_line_count}") # Print the number of lines processed
    print(f"Elapsed seconds: {result.elapsed_seconds:.6f}") # Print the elapsed time in seconds
    print(f"Elapsed HH:MM:SS: {format_duration(result.elapsed_seconds)}") # Print the elapsed time in hours, minutes, seconds
    print(f"Output bytes: {result.output_byte_count}") # Print the size of the output file in bytes
    print(f"Verification status: {result.verification_status}") # Print the verification status
    print(f"CSV row appended: {csv_file}") # Print the benchmark CSV file path
    return 0 # Return 0 to indicate successful execution


# ---- end main()


if __name__ == "__main__":
    raise SystemExit(main())
