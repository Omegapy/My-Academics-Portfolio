# File: double_numbers.py | Author: Alexander Ricciardi | Date: 2026-06-03
# Course: CSC507 | Professor: Dr. Joseph Issa | Spring C 2026
# SPDX-License-Identifier: Apache-2.0
# ----------------------------------------

"""Benchmark three Python methods for doubling numbers from file1.txt.

The script reads file1.txt, doubles every integer value, writes the result
to newfile1.txt, verifies correctness, and records benchmark evidence.
The three measured methods match the Module 4 Portfolio Milestone prompt:

1. Read the entire source file into memory before processing.
2. Read and process one source line at a time.
3. Split the source file into two parts and read each part into memory
   separately before processing.
"""

from __future__ import annotations

import argparse
import csv
import os
import platform
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


# ======
# Constants
# ======

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_FILE = SCRIPT_DIR / "file1.txt"
DEFAULT_OUTPUT_FILE = SCRIPT_DIR / "newfile1.txt"
DEFAULT_CSV_FILE = SCRIPT_DIR / "benchmark_results.csv"
DEFAULT_BASH_RESULT_FILE = SCRIPT_DIR / "bash_benchmark_result.csv"
VALID_METHODS = ("full_read", "line_by_line", "split_read")

CSV_FIELDNAMES = [
    "method",
    "input_file",
    "output_file",
    "line_count",
    "elapsed_seconds",
    "elapsed_hms",
    "verified_lines",
    "verified_correct",
    "file_size_bytes",
    "platform_name",
    "platform_release",
    "python_version",
    "cpu_count",
    "notes",
]


# ======
# Data Models
# ======

# ---- class BenchmarkResult
@dataclass(frozen=True)
class BenchmarkResult:
    """Store the measured result for one Python doubling method.

    Args:
        method: Name of the measured processing method.
        input_file: Source file used for the benchmark.
        output_file: Destination file produced by the benchmark.
        line_count: Number of source lines processed.
        elapsed_seconds: Timed runtime in seconds.
        elapsed_hms: Timed runtime formatted as HH:MM:SS.
        verified_lines: Number of output lines found after processing.
        verified_correct: Whether every output line equals input line * 2.
        file_size_bytes: Size of the generated output file in bytes.
        platform_name: Operating-system name reported by Python.
        platform_release: Operating-system release reported by Python.
        python_version: Python version used for the benchmark.
        cpu_count: CPU count reported by Python.
        notes: Short explanation of the measured method.

    Returns:
        None.
    """

    method: str
    input_file: Path
    output_file: Path
    line_count: int
    elapsed_seconds: float
    elapsed_hms: str
    verified_lines: int
    verified_correct: bool
    file_size_bytes: int
    platform_name: str
    platform_release: str
    python_version: str
    cpu_count: int
    notes: str

    # ---- to_csv_row()
    def to_csv_row(self) -> dict[str, str | int]:
        """Convert the benchmark result to a CSV-safe row.

        Args:
            None.

        Returns:
            Dictionary keyed by benchmark CSV column names.
        """
        return {
            "method": self.method,
            "input_file": str(self.input_file),
            "output_file": str(self.output_file),
            "line_count": self.line_count,
            "elapsed_seconds": f"{self.elapsed_seconds:.6f}",
            "elapsed_hms": self.elapsed_hms,
            "verified_lines": self.verified_lines,
            "verified_correct": str(self.verified_correct).lower(),
            "file_size_bytes": self.file_size_bytes,
            "platform_name": self.platform_name,
            "platform_release": self.platform_release,
            "python_version": self.python_version,
            "cpu_count": self.cpu_count,
            "notes": self.notes,
        }

    # ---- end to_csv_row()


# ---- end class BenchmarkResult


# ======
# Timing, Parsing, and Validation Helpers
# ======

# ---- format_duration()
def format_duration(total_seconds: float) -> str:
    """Format elapsed seconds as HH:MM:SS.

    Args:
        total_seconds: Elapsed runtime in seconds.

    Returns:
        Runtime formatted as HH:MM:SS.
    """
    rounded_seconds = max(0, int(round(total_seconds)))
    hours, remainder = divmod(rounded_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# ---- end format_duration()


# ---- parse_method_list()
def parse_method_list(methods_value: str) -> list[str]:
    """Parse and validate a comma-separated method list.

    Args:
        methods_value: Comma-separated method names or the word "all".

    Returns:
        Ordered list of method names.

    Raises:
        ValueError: If an unknown method name is supplied.
    """
    cleaned_value = methods_value.strip().lower()
    if cleaned_value == "all":
        return list(VALID_METHODS)

    methods = [
        method.strip().lower()
        for method in cleaned_value.split(",")
        if method.strip()
    ]
    invalid_methods = sorted(set(methods) - set(VALID_METHODS))

    if invalid_methods:
        valid_methods = ", ".join(VALID_METHODS)
        raise ValueError(
            f"invalid method(s): {', '.join(invalid_methods)}; "
            f"valid methods are: {valid_methods}"
        )

    if not methods:
        raise ValueError("at least one method is required")

    return methods


# ---- end parse_method_list()


# ---- parse_integer_line()
def parse_integer_line(line: str, line_number: int) -> int:
    """Convert one source line to an integer.

    Args:
        line: Raw text line from the source file.
        line_number: One-based line number used in error messages.

    Returns:
        Integer value parsed from the line.

    Raises:
        ValueError: If the line is blank or not an integer.
    """
    stripped_line = line.strip()

    if not stripped_line:
        raise ValueError(f"blank line found at source line {line_number}")

    try:
        return int(stripped_line)
    except ValueError as exc:
        raise ValueError(
            f"non-integer value found at source line {line_number}: "
            f"{stripped_line!r}"
        ) from exc


# ---- end parse_integer_line()


# ---- build_doubled_text()
def build_doubled_text(lines: Iterable[str], start_line_number: int = 1) -> str:
    """Build doubled-number text from an iterable of source lines.

    Args:
        lines: Source lines containing one integer value each.
        start_line_number: One-based line number of the first supplied line.

    Returns:
        Newline-terminated text containing doubled integer values.
    """
    return "".join(
        f"{parse_integer_line(line, line_number) * 2}\n"
        for line_number, line in enumerate(lines, start=start_line_number)
    )


# ---- end build_doubled_text()


# ---- count_lines()
def count_lines(path: Path) -> int:
    """Count text lines in a file.

    Args:
        path: File path to count.

    Returns:
        Number of lines found in the file.
    """
    with path.open("r", encoding="utf-8") as file_handle:
        return sum(1 for _ in file_handle)


# ---- end count_lines()


# ---- verify_output()
def verify_output(input_path: Path, output_path: Path) -> tuple[int, int, bool]:
    """Verify that every output line is double the matching input line.

    Args:
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        Tuple of source line count, output line count, and correctness flag.
    """
    source_lines = count_lines(input_path)
    output_lines = count_lines(output_path)

    if source_lines != output_lines:
        return source_lines, output_lines, False

    with input_path.open("r", encoding="utf-8") as input_handle:
        with output_path.open("r", encoding="utf-8") as output_handle:
            for line_number, (source_line, output_line) in enumerate(
                zip(input_handle, output_handle),
                start=1,
            ):
                source_value = parse_integer_line(source_line, line_number)
                output_value = parse_integer_line(output_line, line_number)

                if output_value != source_value * 2:
                    return source_lines, output_lines, False

    return source_lines, output_lines, True


# ---- end verify_output()


# ======
# Processing Methods
# ======

# ---- process_full_read()
def process_full_read(input_path: Path, output_path: Path) -> None:
    """Double numbers after reading the entire source file into memory.

    Args:
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        None.
    """
    with input_path.open("r", encoding="utf-8") as input_handle:
        lines = input_handle.readlines()

    output_path.write_text(build_doubled_text(lines), encoding="utf-8")


# ---- end process_full_read()


# ---- process_line_by_line()
def process_line_by_line(input_path: Path, output_path: Path) -> None:
    """Double numbers while reading and writing one row at a time.

    Args:
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        None.
    """
    with input_path.open("r", encoding="utf-8") as input_handle:
        with output_path.open("w", encoding="utf-8") as output_handle:
            for line_number, line in enumerate(input_handle, start=1):
                doubled_value = parse_integer_line(line, line_number) * 2
                output_handle.write(f"{doubled_value}\n")


# ---- end process_line_by_line()


# ---- process_split_read()
def process_split_read(input_path: Path, output_path: Path) -> None:
    """Double numbers by processing two separately loaded file halves.

    Args:
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        None.
    """
    total_lines = count_lines(input_path)
    first_part_count = total_lines // 2

    with input_path.open("r", encoding="utf-8") as input_handle:
        with output_path.open("w", encoding="utf-8") as output_handle:
            # Step 1: Load and process the first half of the source file.
            first_part = [
                input_handle.readline()
                for _ in range(first_part_count)
            ]
            output_handle.write(build_doubled_text(first_part, 1))
            del first_part

            # Step 2: Load and process the remaining half of the source file.
            second_start_line = first_part_count + 1
            second_part = input_handle.readlines()
            output_handle.write(
                build_doubled_text(second_part, second_start_line)
            )


# ---- end process_split_read()


# ======
# Benchmark Orchestration
# ======

PROCESSORS: dict[str, Callable[[Path, Path], None]] = {
    "full_read": process_full_read,
    "line_by_line": process_line_by_line,
    "split_read": process_split_read,
}

METHOD_NOTES = {
    "full_read": "Read entire file into memory before processing",
    "line_by_line": "Read and write one line at a time",
    "split_read": "Read first half and second half into memory separately",
}


# ---- run_method()
def run_method(method: str, input_path: Path, output_path: Path) -> BenchmarkResult:
    """Run, time, and verify one processing method.

    Args:
        method: Method name from VALID_METHODS.
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        BenchmarkResult for the completed method.

    Raises:
        RuntimeError: If the generated output fails verification.
    """
    if output_path.exists():
        output_path.unlink()

    start_time = time.perf_counter()
    PROCESSORS[method](input_path, output_path)
    elapsed_seconds = time.perf_counter() - start_time

    source_lines, verified_lines, verified_correct = verify_output(
        input_path,
        output_path,
    )

    if not verified_correct:
        raise RuntimeError(f"{method} produced incorrect output")

    return BenchmarkResult(
        method=method,
        input_file=input_path,
        output_file=output_path,
        line_count=source_lines,
        elapsed_seconds=elapsed_seconds,
        elapsed_hms=format_duration(elapsed_seconds),
        verified_lines=verified_lines,
        verified_correct=verified_correct,
        file_size_bytes=output_path.stat().st_size,
        platform_name=platform.system(),
        platform_release=platform.release(),
        python_version=platform.python_version(),
        cpu_count=os.cpu_count() or 1,
        notes=METHOD_NOTES[method],
    )


# ---- end run_method()


# ---- read_bash_result_rows()
def read_bash_result_rows(bash_result_file: Path) -> list[dict[str, str]]:
    """Read a previously captured Bash benchmark CSV row.

    Args:
        bash_result_file: CSV file produced by double_numbers.sh.

    Returns:
        List of Bash result rows, or an empty list if no file exists.
    """
    if not bash_result_file.exists():
        return []

    with bash_result_file.open("r", encoding="utf-8", newline="") as file_handle:
        return list(csv.DictReader(file_handle))


# ---- end read_bash_result_rows()


# ---- write_csv()
def write_csv(csv_path: Path, rows: list[dict[str, str | int]]) -> None:
    """Write benchmark rows to a CSV file.

    Args:
        csv_path: Destination CSV path.
        rows: Benchmark result rows to write.

    Returns:
        None.
    """
    with csv_path.open("w", encoding="utf-8", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


# ---- end write_csv()


# ---- build_parser()
def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    Args:
        None.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Benchmark three Python methods for doubling file1.txt.",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help="source file containing one integer per line",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help="destination file for doubled values",
    )
    parser.add_argument(
        "--csv-file",
        type=Path,
        default=DEFAULT_CSV_FILE,
        help="destination CSV file for benchmark results",
    )
    parser.add_argument(
        "--methods",
        default="all",
        help="comma-separated methods to run, or 'all'",
    )
    parser.add_argument(
        "--include-bash-result",
        action="store_true",
        help="include the row captured by double_numbers.sh in the CSV",
    )
    parser.add_argument(
        "--bash-result-file",
        type=Path,
        default=DEFAULT_BASH_RESULT_FILE,
        help="CSV row file produced by double_numbers.sh",
    )
    return parser


# ---- end build_parser()


# ---- main()
def main() -> None:
    """Run the selected benchmark methods.

    Args:
        None.

    Returns:
        None.
    """
    parser = build_parser()
    args = parser.parse_args()

    input_path = args.input_file.resolve()
    output_path = args.output_file.resolve()
    csv_path = args.csv_file.resolve()
    bash_result_file = args.bash_result_file.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(f"input file not found: {input_path}")

    methods = parse_method_list(args.methods)
    csv_rows: list[dict[str, str | int]] = []

    if args.include_bash_result:
        csv_rows.extend(read_bash_result_rows(bash_result_file))

    print("Python doubling benchmark started")
    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Methods: {', '.join(methods)}")

    for method in methods:
        result = run_method(method, input_path, output_path)
        csv_rows.append(result.to_csv_row())
        print(
            f"{result.method}: {result.elapsed_seconds:.6f} seconds; "
            f"verified_lines={result.verified_lines}; "
            f"verified_correct={result.verified_correct}"
        )

    write_csv(csv_path, csv_rows)

    print(f"Benchmark CSV written: {csv_path}")
    print("Python doubling benchmark ended")


# ---- end main()


if __name__ == "__main__":
    main()
