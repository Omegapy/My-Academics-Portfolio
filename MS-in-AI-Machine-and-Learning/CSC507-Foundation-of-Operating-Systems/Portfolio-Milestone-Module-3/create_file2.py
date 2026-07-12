# File: create_file2.py
# Author: Alexander Ricciardi
# Date: 2026-05-25
# Course: CSC507
# Professor: Dr. Joseph Issa
# Term: Spring C 2026
#----------------------------------------

"""Benchmark Python methods for creating file2.txt.

The program is a small standalone Python script that creates one 
random integer per line, matching Bash's $RANDOM
range of 0 through 32767. 
It runs one or more Python generation methods,
it also records elapsed time with time.perf_counter(), 
verifies the generated line count, 
and writes a CSV timing file.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import os
import platform
import random
import time
from dataclasses import dataclass
from pathlib import Path


# ======
# Constants
# ======

DEFAULT_LINE_COUNT = 1_000_000
DEFAULT_CHUNK_SIZE = 50_000
DEFAULT_CSV_FILE = Path("benchmark_results.csv")
OUTPUT_FILE = Path("file2.txt")
MAX_BASH_RANDOM = 32_767
VALID_METHODS = ("sequential", "buffered", "threaded", "multiprocessing")


# ======
# Data Models
# ======

# ---- class BenchmarkResult
# data class to store the timing measurements and other data
@dataclass(frozen=True)
class BenchmarkResult:
    """Store the measured result for one generation method.

    Args:
        method: Name of the generation method.
        line_count: Number of requested output lines.
        chunk_size: Chunk size used for buffered and parallel methods.
        workers: Worker count used for threaded and multiprocessing methods.
        elapsed_seconds: Measured elapsed runtime in seconds.
        elapsed_hms: Measured elapsed runtime formatted as HH:MM:SS.
        verified_lines: Number of newline-terminated lines found in the output.
        file_size_bytes: Size of the generated output file in bytes.
        platform_name: Operating-system name reported by Python.
        platform_release: Operating-system release reported by Python.
        python_version: Python version used for the benchmark.
        cpu_count: CPU count reported by Python.

    Returns:
        None.
    """

    method: str
    line_count: int
    chunk_size: int
    workers: int
    elapsed_seconds: float
    elapsed_hms: str
    verified_lines: int
    file_size_bytes: int
    platform_name: str
    platform_release: str
    python_version: str
    cpu_count: int

    # ---- to_csv_row()
    def to_csv_row(self) -> dict[str, str | int]:
        """Convert the benchmark result to a CSV-safe dictionary.

        Args:
            None.

        Returns:
            Dictionary containing CSV column names.
        """
        return {
            "method": self.method,  # string method name
            "line_count": self.line_count,  # integer line count
            "chunk_size": self.chunk_size,  # integer chunk size
            "workers": self.workers,  # integer worker count
            "elapsed_seconds": f"{self.elapsed_seconds:.6f}",  # float elapsed seconds
            "elapsed_hms": self.elapsed_hms,  # string elapsed time in HH:MM:SS format
            "verified_lines": self.verified_lines,   # integer verified lines
            "file_size_bytes": self.file_size_bytes,  # integer file size
            "platform_name": self.platform_name,  # string platform name
            "platform_release": self.platform_release,  # string platform release
            "python_version": self.python_version,  # string python version
            "cpu_count": self.cpu_count,  # integer cpu count
        }

    # ---- end to_csv_row()


# ---- end class BenchmarkResult


# ======
# Timing and Validation Helpers
# ======

# ---- positive_int()
def positive_int(value: str) -> int:
    """Positive integer command-line value.

    Args:
        value: Raw command-line value.

    Returns:
        Positive integer value.

    Raises:
        argparse.ArgumentTypeError: If the value is not a positive integer.
    """
    try:
        parsed_value = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("value must be an integer") from exc

    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")

    return parsed_value

# ---- end positive_int()


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
    """Validate the comma-separated method list.

    Args:
        methods_value: Comma-separated method names or the word "all".

    Returns:
        Ordered list of benchmark method names.

    Raises:
        ValueError: If no valid methods are supplied.
    """
    # Clean the input string and convert to lowercase
    cleaned_value = methods_value.strip().lower()
    # Check if the user wants to run all methods
    if cleaned_value == "all":
        return list(VALID_METHODS)

    # Split the string into a list of methods
    methods = [
        method.strip().lower()
        for method in cleaned_value.split(",")
        if method.strip()
    ]

    # Check for invalid methods
    invalid_methods = sorted(set(methods) - set(VALID_METHODS))
    if invalid_methods:
        valid_methods = ", ".join(VALID_METHODS)
        raise ValueError(
            f"invalid method(s): {', '.join(invalid_methods)}; "
            f"valid methods are: {valid_methods}"
        )

    # Check if at least one method is provided
    if not methods:
        raise ValueError("at least one method is required")

    return methods

# ---- end parse_method_list()


# ---- count_lines()
def count_lines(output_path: Path) -> int:
    """Count newline-terminated lines.

    Args:
        output_path: Path to the generated text file.

    Returns:
        Number of lines found in the file.
    """
    line_total = 0
    # Open the file in binary read mode
    with output_path.open("rb") as file_handle:
        # Iterate through the file in chunks
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            # Count the number of newline characters in the chunk
            line_total += chunk.count(b"\n")
    return line_total

# ---- end count_lines()


# ======
# Random Number Generation
# ======

# ---- build_random_chunk()
def build_random_chunk(line_count: int, seed: int) -> str:
    """Build a text chunk containing random-number lines.

    Args:
        line_count: Number of lines to generate for this chunk.
        seed: Seed for this chunk's local pseudo-random generator.

    Returns:
        String containing one random integer per line.
    """
    local_random = random.Random(seed)
    return "".join(
        f"{local_random.randint(0, MAX_BASH_RANDOM)}\n"
        for _ in range(line_count)
    )

# ---- end build_random_chunk()


# ---- build_random_chunk_from_spec()
def build_random_chunk_from_spec(chunk_spec: tuple[int, int]) -> str:
    """Build a random-number chunk from a worker-safe tuple.

    Args:
        chunk_spec: Tuple containing chunk line count and random seed.

    Returns:
        String containing one random integer per line.
    """
    chunk_line_count, seed = chunk_spec
    return build_random_chunk(chunk_line_count, seed)

# ---- end build_random_chunk_from_spec()


# ---- build_chunk_specs()
def build_chunk_specs(line_count: int, chunk_size: int) -> list[tuple[int, int]]:
    """Create chunk sizes and seeds for buffered or parallel generation.

    Args:
        line_count: Total number of output lines requested.
        chunk_size: Maximum number of lines per generated chunk.

    Returns:
        List of worker-safe chunk specifications.
    """
    specs: list[tuple[int, int]] = []
    remaining_lines = line_count
    # Use system random for better randomness
    seed_source = random.SystemRandom()
    # Loop until all lines are accounted for
    while remaining_lines > 0:
        # Determine the number of lines for the current chunk
        current_chunk_size = min(chunk_size, remaining_lines)
        # Use system random for better randomness
        seed = seed_source.randrange(1, 2**63)
        # Append the chunk specification to the list
        specs.append((current_chunk_size, seed))
        # Decrement the remaining lines count
        remaining_lines -= current_chunk_size

    return specs

# ---- end build_chunk_specs()


# ======
# Generation Methods
# ======

# ---- write_sequential()
def write_sequential(output_path: Path, line_count: int) -> None:
    """Write random-number lines with one direct Python loop.

    Args:
        output_path: Path to the output text file.
        line_count: Number of random-number lines to write.

    Returns:
        None.
    """
    # Create a local random number generator
    local_random = random.Random()
    # Open the output file for writing
    with output_path.open("w", encoding="utf-8") as file_handle:
        # Iterate through line count and write generated random numbers to the file
        for _ in range(line_count):
            file_handle.write(f"{local_random.randint(0, MAX_BASH_RANDOM)}\n")

# ---- end write_sequential()


# ---- write_buffered()
def write_buffered(output_path: Path, line_count: int, chunk_size: int) -> None:
    """Write random-number lines in larger generated chunks.

    Args:
        output_path: Path to the output text file.
        line_count: Number of random-number lines to write.
        chunk_size: Maximum number of lines per generated chunk.

    Returns:
        None.
    """
    chunk_specs = build_chunk_specs(line_count, chunk_size)
    # Open the output file for writing
    with output_path.open("w", encoding="utf-8") as file_handle:
        # Iterate through chunk specs and write generated chunks to the file
        for chunk_spec in chunk_specs:
            file_handle.write(build_random_chunk_from_spec(chunk_spec))

# ---- end write_buffered()


# ---- write_threaded()
def write_threaded(
    output_path: Path,
    line_count: int,
    chunk_size: int,
    workers: int,
) -> None:
    """Generate chunks with threads and write them in deterministic order.

    Args:
        output_path: Path to the output text file.
        line_count: Number of random-number lines to write.
        chunk_size: Maximum number of lines per generated chunk.
        workers: Number of worker threads.

    Returns:
        None.
    """
    chunk_specs = build_chunk_specs(line_count, chunk_size)
    # Use ThreadPoolExecutor for parallel execution with threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # Open the output file for writing
        with output_path.open("w", encoding="utf-8") as file_handle:
            # Map the build_random_chunk_from_spec function to the chunk specs
            for chunk in executor.map(build_random_chunk_from_spec, chunk_specs):
                # Write the generated chunk to the file
                file_handle.write(chunk)

# ---- end write_threaded()


# ---- write_multiprocessing()
def write_multiprocessing(
    output_path: Path,
    line_count: int,
    chunk_size: int,
    workers: int,
) -> None:
    """Generate chunks with worker processes and write them in order.

    Args:
        output_path: Path to the output text file.
        line_count: Number of random-number lines to write.
        chunk_size: Maximum number of lines per generated chunk.
        workers: Number of worker processes.

    Returns:
        None.
    """
    chunk_specs = build_chunk_specs(line_count, chunk_size)

    # Use ProcessPoolExecutor for true parallel execution
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        # Open the output file for writing
        with output_path.open("w", encoding="utf-8") as file_handle:
            for chunk in executor.map(
                build_random_chunk_from_spec,
                chunk_specs,
                chunksize=1,
            ):
                file_handle.write(chunk)

# ---- end write_multiprocessing()


# ======
# Benchmark Orchestration
# ======

# ---- run_benchmark()
def run_benchmark(
    method: str,
    output_path: Path,
    line_count: int,
    chunk_size: int,
    workers: int,
) -> BenchmarkResult:
    """Run one benchmark method and verify the generated output.

    Args:
        method: Benchmark method name.
        output_path: Path to the output text file.
        line_count: Number of random-number lines to write.
        chunk_size: Maximum number of lines per generated chunk.
        workers: Number of worker threads or processes.

    Returns:
        Benchmark result for the completed method.

    Raises:
        RuntimeError: If the generated file has the wrong line count.
    """
    start_time = time.perf_counter()

    if method == "sequential":
        write_sequential(output_path, line_count)
    elif method == "buffered":
        write_buffered(output_path, line_count, chunk_size)
    elif method == "threaded":
        write_threaded(output_path, line_count, chunk_size, workers)
    elif method == "multiprocessing":
        write_multiprocessing(output_path, line_count, chunk_size, workers)
    else:
        raise RuntimeError(f"unsupported benchmark method: {method}")

    elapsed_seconds = time.perf_counter() - start_time
    verified_lines = count_lines(output_path)

    # VALIDATION: Stop immediately if a method creates incomplete evidence.
    if verified_lines != line_count:
        raise RuntimeError(
            f"{method} generated {verified_lines} lines; "
            f"expected {line_count} lines"
        )

    return BenchmarkResult(
        method=method, # method name
        line_count=line_count, # number of lines
        chunk_size=chunk_size, # number of lines per chunk
        workers=workers if method in {"threaded", "multiprocessing"} else 1, # number of workers
        elapsed_seconds=elapsed_seconds, # elapsed seconds
        elapsed_hms=format_duration(elapsed_seconds), # elapsed hms
        verified_lines=verified_lines, # verified lines
        file_size_bytes=output_path.stat().st_size, # file size in bytes
        platform_name=platform.system(), # platform name
        platform_release=platform.release(), # platform release
        python_version=platform.python_version(), # python version
        cpu_count=os.cpu_count() or 1, # cpu count
    )

# ---- end run_benchmark()


# ---- write_results_csv()
def write_results_csv(results: list[BenchmarkResult], csv_path: Path) -> None:
    """Write benchmark results to a CSV file.

    Args:
        results: Benchmark results to write.
        csv_path: Destination CSV path.

    Returns:
        None.
    """
    fieldnames = [
        "method", # method name
        "line_count", # number of lines
        "chunk_size", # number of lines per chunk
        "workers", # number of workers
        "elapsed_seconds", # elapsed seconds
        "elapsed_hms", # elapsed hms
        "verified_lines", # verified lines
        "file_size_bytes", # file size in bytes
        "platform_name", # platform name
        "platform_release", # platform release
        "python_version", # python version
        "cpu_count", # cpu count
    ]

    # Create the directory for the CSV file if it doesn't exist
    if csv_path.parent != Path("."):
        csv_path.parent.mkdir(parents=True, exist_ok=True)
    # Open the CSV file for writing 
    with csv_path.open("w", encoding="utf-8", newline="") as file_handle:
        # Create a CSV writer
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        # Write the header
        writer.writeheader()
        # Write the results
        for result in results:
            writer.writerow(result.to_csv_row())

# ---- end write_results_csv()


# ---- build_parser()
def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    Args:
        None.

    Returns:
        Configured argument parser.
    """
    # Default to the number of CPUs on the host
    default_workers = os.cpu_count() or 1
    parser = argparse.ArgumentParser(
        description="Create file2.txt and benchmark Python generation methods."
    )
    # Add command line arguments
    parser.add_argument(
        "--line-count",
        type=positive_int,
        default=DEFAULT_LINE_COUNT,
        help=f"number of random-number lines to write (default: {DEFAULT_LINE_COUNT})",
    )
    # comma separated methods to run or 'all'
    parser.add_argument(
        "--methods",
        default=",".join(VALID_METHODS),
        help=(
            "comma-separated methods to run or 'all' "
            f"(default: {','.join(VALID_METHODS)})"
        ),
    )
    # Number of threads or processes for parallel methods
    parser.add_argument(
        "--workers",
        type=positive_int,
        default=default_workers,
        help=f"threads/processes for parallel methods (default: {default_workers})",
    )
    # Lines per generated chunk
    parser.add_argument(
        "--chunk-size",
        type=positive_int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"lines per generated chunk (default: {DEFAULT_CHUNK_SIZE})",
    )
    # Benchmark CSV output path
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV_FILE,
        help=f"benchmark CSV output path (default: {DEFAULT_CSV_FILE})",
    )
    return parser

# ---- end build_parser()


# ---- main()
def main() -> None:
    """Run the benchmark program.

    Args:
        None.

    Returns:
        None.
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        methods = parse_method_list(args.methods)
    except ValueError as exc:
        parser.error(str(exc))

    print("Python random-number generation benchmark")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Line count: {args.line_count}")
    print(f"Methods: {', '.join(methods)}")
    print(f"Chunk size: {args.chunk_size}")
    print(f"Workers: {args.workers}")

    # Benchmark loop
    results: list[BenchmarkResult] = [] 
    for method in methods:
        print(f"\nRunning method: {method}")
        result = run_benchmark(
            method=method,
            output_path=OUTPUT_FILE,
            line_count=args.line_count,
            chunk_size=args.chunk_size,
            workers=args.workers,
        )
        # append the result to the results list
        results.append(result)
        # Print the result
        print(
            f"{method}: {result.elapsed_seconds:.6f} seconds "
            f"({result.elapsed_hms}); verified {result.verified_lines} lines"
        )
    
    # Write the results to a CSV file
    write_results_csv(results, args.csv)
    # Print the final result
    print(f"\nWrote benchmark results to {args.csv}")
    print(f"Final {OUTPUT_FILE} line count: {count_lines(OUTPUT_FILE)}")

# ---- end main()


if __name__ == "__main__":
    main()
