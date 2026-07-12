# Student: Alexander Ricciardi 
# Date: 2026-06-21
# Course: CSC507 
# Professor: Dr. Joseph Issa | 
# Spring C 2026
# ----------------------------------------

"""Benchmark real-time and non-real-time file-processing methods.

The program creates or reuses a large input file containing one integer per
line, doubles every integer, writes the result to output files, verifies the
outputs, and records timing results in CSV format.

The first five benchmark methods match the CAT-6 assignment prompt. The final
five methods are practical efficiency alternatives that can be discussed in
the written analysis.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import os
import platform
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


# ======
# Constants
# ======

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "benchmark_output" # directory where output files will be stored
DEFAULT_LINE_COUNT = 10_000_000 # number of lines to process
DEFAULT_REAL_TIME_PRIORITY = 10 # default real-time priority
DEFAULT_BUFFER_SIZE = 1024 * 1024 # default buffer size
LARGE_BUFFER_SIZE = 16 * 1024 * 1024 # larger buffer size
MAX_RANDOM_VALUE = 32_767 # maximum value for random numbers
# column headers for the CSV file
CSV_FIELDNAMES = [ 
    "method_number",
    "method_name",
    "description",
    "input_file",
    "output_file",
    "line_count",
    "part_count",
    "worker_count",
    "scheduler_requested",
    "scheduler_enabled_workers",
    "scheduler_status",
    "elapsed_seconds",
    "elapsed_hms",
    "split_seconds",
    "process_seconds",
    "combine_seconds",
    "verified_lines",
    "verified_correct",
    "file_size_bytes",
    "platform_name",
    "platform_release",
    "python_version",
    "cpu_count",
    "notes",
]
# Naming for the mode
MethodMode = Literal[
    "single",
    "split_process",
    "split_process_auto",
    "split_thread",
    "awk",
]


# ======
# Data Models
# ======


# ---- class MethodSpec
@dataclass(frozen=True)
class MethodSpec:
    """Describe one benchmark method.

    Args:
        number: Assignment method number used in reports.
        name: Stable method name used in output files and CSV rows.
        description: Short explanation of the method.
        mode: Processing mode used by the benchmark harness.
        part_count: Number of file pieces for split methods.
        request_realtime: Whether worker processes should request real-time scheduling.
        buffer_size: File buffer size in bytes.

    Returns:
        None.
    """

    number: int
    name: str
    description: str
    mode: MethodMode
    part_count: int
    request_realtime: bool
    buffer_size: int = DEFAULT_BUFFER_SIZE


# ---- end class MethodSpec


# ---- class WorkerResult
@dataclass(frozen=True)
class WorkerResult:
    """Store the outcome of one worker process or thread.

    Args:
        input_file: Chunk input file processed by the worker.
        output_file: Chunk output file created by the worker.
        processed_lines: Number of lines processed.
        scheduler_requested: Whether real-time scheduling was requested.
        scheduler_enabled: Whether real-time scheduling was actually enabled.
        scheduler_status: Short status message about scheduling.

    Returns:
        None.
    """

    input_file: str
    output_file: str
    processed_lines: int
    scheduler_requested: bool
    scheduler_enabled: bool
    scheduler_status: str


# ---- end class WorkerResult


# ---- class BenchmarkResult
@dataclass(frozen=True)
class BenchmarkResult:
    """Store the measured result for one benchmark method.

    Args:
        method_spec: Method definition.
        input_file: Source file path.
        output_file: Destination file path.
        line_count: Number of source lines processed.
        part_count: Number of parts actually used.
        worker_count: Number of workers actually used.
        scheduler_enabled_workers: Count of workers that entered real-time scheduling.
        scheduler_status: Short scheduler status summary.
        elapsed_seconds: Total elapsed method time.
        split_seconds: Time spent splitting the input file.
        process_seconds: Time spent processing data.
        combine_seconds: Time spent combining chunk outputs.
        verified_lines: Number of verified output lines.
        verified_correct: Whether the output matched the expected doubled values.
        file_size_bytes: Size of the method output file.
        notes: Additional observation about the method.

    Returns:
        None.
    """

    method_spec: MethodSpec
    input_file: Path
    output_file: Path
    line_count: int
    part_count: int
    worker_count: int
    scheduler_enabled_workers: int
    scheduler_status: str
    elapsed_seconds: float
    split_seconds: float
    process_seconds: float
    combine_seconds: float
    verified_lines: int
    verified_correct: bool
    file_size_bytes: int
    notes: str

    # ---- to_csv_row()
    def to_csv_row(self) -> dict[str, str | int]:
        """Convert the benchmark result to a CSV-safe dictionary.

        Args:
            None.

        Returns:
            Dictionary containing one CSV row.
        """
        return {
            "method_number": self.method_spec.number,
            "method_name": self.method_spec.name,
            "description": self.method_spec.description,
            "input_file": str(self.input_file),
            "output_file": str(self.output_file),
            "line_count": self.line_count,
            "part_count": self.part_count,
            "worker_count": self.worker_count,
            "scheduler_requested": str(self.method_spec.request_realtime).lower(),
            "scheduler_enabled_workers": self.scheduler_enabled_workers,
            "scheduler_status": self.scheduler_status,
            "elapsed_seconds": f"{self.elapsed_seconds:.6f}",
            "elapsed_hms": format_duration(self.elapsed_seconds),
            "split_seconds": f"{self.split_seconds:.6f}",
            "process_seconds": f"{self.process_seconds:.6f}",
            "combine_seconds": f"{self.combine_seconds:.6f}",
            "verified_lines": self.verified_lines,
            "verified_correct": str(self.verified_correct).lower(),
            "file_size_bytes": self.file_size_bytes,
            "platform_name": platform.system(),
            "platform_release": platform.release(),
            "python_version": platform.python_version(),
            "cpu_count": os.cpu_count() or 1,
            "notes": self.notes,
        }

    # ---- end to_csv_row()


# ---- end class BenchmarkResult


# ======
# Method Definitions
# ======

# list of method specifications
METHOD_SPECS = ( 
    MethodSpec( # one normal process on the full larger file
        1,
        "m01_single_normal",
        "Run one normal-scheduler process on the full larger file.",
        "single",
        1,
        False,
    ),
    MethodSpec( # 10 files with real-time scheduling
        2,
        "m02_split10_realtime",
        "Split into 10 files, process each with real-time scheduling, then combine.",
        "split_process",
        10,
        True,
    ),
    MethodSpec( # 2 files with real-time scheduling
        3,
        "m03_split2_realtime",
        "Split into 2 files, process each with real-time scheduling, then combine.",
        "split_process",
        2,
        True,
    ),
    MethodSpec( # 5 files with real-time scheduling
        4,
        "m04_split5_realtime",
        "Split into 5 files, process each with real-time scheduling, then combine.",
        "split_process",
        5,
        True,
    ),
    MethodSpec( # 20 files with real-time scheduling
        5,
        "m05_split20_realtime",
        "Split into 20 files, process each with real-time scheduling, then combine.",
        "split_process",
        20,
        True,
    ),
    MethodSpec( # 10 files with normal scheduling
        6,
        "m06_split10_normal",
        "Split into 10 files with normal scheduling to isolate the real-time effect.",
        "split_process",
        10,
        False,
    ),
    MethodSpec(
        7,
        "m07_split_auto_normal",
        "Split by available logical CPUs with normal scheduling.",
        "split_process_auto",
        0,
        False,
    ),
    MethodSpec( # one normal process with a larger file buffer
        8,
        "m08_single_large_buffer",
        "Run one normal process with a larger file buffer.",
        "single",
        1,
        False,
        LARGE_BUFFER_SIZE,
    ),
    MethodSpec( # 10 files with normal scheduling but using Python threads instead of processes
        9,
        "m09_split10_threads",
        "Split into 10 files and process chunks with Python threads.",
        "split_thread",
        10,
        False,
    ),
    MethodSpec( # Unix awk stream processor as a compact optimized pipeline
        10,
        "m10_awk_stream",
        "Use the Unix awk stream processor as a compact optimized pipeline.",
        "awk",
        1,
        False,
    ),
)
METHODS_BY_NAME = {method.name: method for method in METHOD_SPECS}


# ======
# Parsing and Formatting Helpers
# ======


# ---- positive_int()
def positive_int(value: str) -> int:
    """Parse a positive integer command-line argument.

    Args:
        value: Raw command-line value.

    Returns:
        Parsed positive integer.

    Raises:
        argparse.ArgumentTypeError: If the value is not positive.
    """
    try:
        parsed_value = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("value must be an integer") from exc

    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")

    return parsed_value


# ---- end positive_int()


# ---- parse_methods()
def parse_methods(methods_value: str) -> list[MethodSpec]:
    """Parse a comma-separated method list.

    Args:
        methods_value: Comma-separated method names or "all".

    Returns:
        Ordered list of selected MethodSpec objects.

    Raises:
        ValueError: If an unknown method name is supplied.
    """

    # ---- parse the method list
    cleaned_value = methods_value.strip().lower()
    if cleaned_value == "all":
        return list(METHOD_SPECS)

    # ---- create a list of selected method names
    selected_names = [
        method_name.strip().lower()
        for method_name in cleaned_value.split(",")
        if method_name.strip()
    ]
    invalid_names = sorted(set(selected_names) - set(METHODS_BY_NAME))

    # ---- raise ValueError if any invalid method names are found
    if invalid_names:
        valid_names = ", ".join(METHODS_BY_NAME)
        raise ValueError(
            f"invalid method(s): {', '.join(invalid_names)}; "
            f"valid methods are: {valid_names}"
        )

    # ---- raise ValueError if no methods are selected
    if not selected_names:
        raise ValueError("at least one method must be selected")

    # ---- return the list of selected method specifications
    return [METHODS_BY_NAME[method_name] for method_name in selected_names]


# ---- end parse_methods()


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


# ---- summarize_scheduler_status()
def summarize_scheduler_status(worker_results: list[WorkerResult]) -> str:
    """Summarize scheduler messages from workers.

    Args:
        worker_results: Results returned by worker processes or threads.

    Returns:
        Compact scheduler status string.
    """
    if not worker_results:
        return "not requested"

    messages = sorted({worker.scheduler_status for worker in worker_results})
    return "; ".join(messages)


# ---- end summarize_scheduler_status()


# ======
# File Generation and Verification
# ======


# ---- deterministic_number()
def deterministic_number(line_number: int) -> int:
    """Return a repeatable integer in the Bash RANDOM range.

    Args:
        line_number: One-based line number.

    Returns:
        Deterministic pseudo-random integer between 0 and 32767.
    """
    return (line_number * 1_103_515_245 + 12_345) % (MAX_RANDOM_VALUE + 1)


# ---- end deterministic_number()


# ---- generate_input_file()
def generate_input_file(input_path: Path, line_count: int, force: bool) -> None:
    """Create the benchmark input file if needed.

    Args:
        input_path: Destination input file path.
        line_count: Number of integer lines to generate.
        force: Whether to replace an existing file.

    Returns:
        None.
    """

    # ---- create input file if it doesn't exist
    if input_path.exists() and not force:
        print(f"Input file already exists: {input_path}")
        return

    # ---- create parent directory if needed
    temp_path = input_path.with_name(f"{input_path.name}.tmp")
    print(f"Creating input file: {input_path}")
    print(f"Line count: {line_count}")

    with temp_path.open("w", encoding="utf-8", buffering=LARGE_BUFFER_SIZE) as file_handle:
        batch: list[str] = []
        for line_number in range(1, line_count + 1):
            batch.append(f"{deterministic_number(line_number)}\n")
            if len(batch) >= 100_000:
                file_handle.writelines(batch)
                batch.clear()

        if batch:
            file_handle.writelines(batch)

    # ---- move the temp file to the final destination
    temp_path.replace(input_path)


# ---- end generate_input_file()


# ---- count_lines()
def count_lines(path: Path) -> int:
    """Count newline-terminated lines in a file.

    Args:
        path: File path to count.

    Returns:
        Number of newline characters found in the file.
    """

    # ---- count newline characters in the file
    line_total = 0
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(LARGE_BUFFER_SIZE), b""):
            line_total += chunk.count(b"\n")
    return line_total


# ---- end count_lines()


# ---- parse_integer_line()
def parse_integer_line(line: str, line_number: int, path: Path) -> int:
    """Parse one integer line.

    Args:
        line: Raw line text.
        line_number: One-based line number.
        path: File path used in error messages.

    Returns:
        Parsed integer value.

    Raises:
        ValueError: If the line is blank or not an integer.
    """

    # ---- strip whitespace and check for blank lines
    stripped_line = line.strip()
    if not stripped_line:
        raise ValueError(f"blank line found in {path} at line {line_number}")

    # ---- convert to integer and raise ValueError if not an integer
    try:
        return int(stripped_line)
    except ValueError as exc:
        raise ValueError(
            f"non-integer value found in {path} at line {line_number}: "
            f"{stripped_line!r}"
        ) from exc


# ---- end parse_integer_line()


# ---- verify_output()
def verify_output(input_path: Path, output_path: Path) -> tuple[int, bool]:
    """Verify that every output line equals the input line doubled.

    Args:
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        Tuple containing output line count and correctness flag.
    """

    # ---- count output lines
    output_lines = 0

    # ---- open both files and iterate through them line by line
    with input_path.open("r", encoding="utf-8", buffering=LARGE_BUFFER_SIZE) as input_handle:

        # ---- open the output file
        with output_path.open("r", encoding="utf-8", buffering=LARGE_BUFFER_SIZE) as output_handle:

            # ---- iterate through the input file line by line
            for line_number, source_line in enumerate(input_handle, start=1):

                # ---- read the output file line by line
                output_line = output_handle.readline()

                # ---- check if the output file is empty
                if output_line == "":
                    return output_lines, False

                # ---- parse the source and output values
                source_value = parse_integer_line(source_line, line_number, input_path)
                output_value = parse_integer_line(output_line, line_number, output_path)
                
                # ---- increment output line count
                output_lines += 1

                # ---- check if the output value is correct
                if output_value != source_value * 2:
                    return output_lines, False
            
            # ---- check if there are any extra output lines
            extra_output = output_handle.readline()
            if extra_output != "":
                return output_lines + 1, False

    return output_lines, True


# ---- end verify_output()


# ======
# Scheduling and Processing Helpers
# ======


# ---- request_realtime_scheduler()
def request_realtime_scheduler(priority: int) -> tuple[bool, str]:
    """Attempt to put the current process into Linux real-time scheduling.

    Args:
        priority: SCHED_RR priority to request.

    Returns:
        Tuple of enabled flag and status message.
    """
    if not hasattr(os, "sched_setscheduler") or not hasattr(os, "SCHED_RR"):
        return False, "real-time scheduler not available on this OS"

    try:
        os.sched_setscheduler(0, os.SCHED_RR, os.sched_param(priority))
    except PermissionError:
        return False, "permission denied; run with CAP_SYS_NICE or sudo for real-time"
    except OSError as exc:
        return False, f"real-time request failed: {exc}"

    return True, f"SCHED_RR priority {priority}"


# ---- end request_realtime_scheduler()


# ---- process_part_worker()
def process_part_worker(
    input_file: str,
    output_file: str,
    request_realtime: bool,
    real_time_priority: int,
    buffer_size: int,
) -> WorkerResult:
    """Process one file or file chunk.

    Args:
        input_file: Source file path as a string for multiprocessing.
        output_file: Destination file path as a string for multiprocessing.
        request_realtime: Whether to request real-time scheduling.
        real_time_priority: Linux SCHED_RR priority.
        buffer_size: File buffer size in bytes.

    Returns:
        WorkerResult with processing and scheduler details.
    """

    # ---- convert input and output file paths to Path objects
    input_path = Path(input_file)
    output_path = Path(output_file)
    scheduler_enabled = False
    scheduler_status = "not requested"
    
    # ---- request real-time scheduling if requested
    if request_realtime:
        scheduler_enabled, scheduler_status = request_realtime_scheduler(real_time_priority)

    # ---- count lines that were processed
    processed_lines = 0

    # ---- open the input file for reading
    with input_path.open("r", encoding="utf-8", buffering=buffer_size) as input_handle:
        
        # ---- open the output file for writing
        with output_path.open("w", encoding="utf-8", buffering=buffer_size) as output_handle:
            
            # ---- iterate through the input file line by line
            for line_number, line in enumerate(input_handle, start=1):

                # ---- parse the input value
                value = parse_integer_line(line, line_number, input_path)

                # ---- write the output value
                output_handle.write(f"{value * 2}\n")
                processed_lines += 1

    return WorkerResult(
        input_file=input_file,
        output_file=output_file,
        processed_lines=processed_lines,
        scheduler_requested=request_realtime,
        scheduler_enabled=scheduler_enabled,
        scheduler_status=scheduler_status,
    )


# ---- end process_part_worker()


# ---- run_awk_stream()
def run_awk_stream(input_path: Path, output_path: Path) -> None:
    """Run the awk streaming method.

    Args:
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        None.

    Raises:
        RuntimeError: If awk is unavailable or returns a failure code.
    """

    # ---- ensure awk is available on PATH
    if shutil.which("awk") is None:
        raise RuntimeError("awk was not found on PATH")
    
    # ---- open the output file for writing
    with output_path.open("w", encoding="utf-8", buffering=LARGE_BUFFER_SIZE) as output_handle:
        
        # ---- run awk to process the input file
        completed_process = subprocess.run(
            ["awk", "{print $1 * 2}", str(input_path)],
            check=False,
            stdout=output_handle,
            stderr=subprocess.PIPE,
            text=True,
        )

    # ---- check if awk failed
    if completed_process.returncode != 0:
        raise RuntimeError(completed_process.stderr.strip() or "awk failed")


# ---- end run_awk_stream()


# ======
# Split and Combine Helpers
# ======


# ---- build_part_sizes()
def build_part_sizes(line_count: int, part_count: int) -> list[int]:
    """Build balanced line counts for split files.

    Args:
        line_count: Total source line count.
        part_count: Desired number of parts.

    Returns:
        List of line counts, one per part.
    """
    actual_part_count = min(part_count, line_count)
    base_size, remainder = divmod(line_count, actual_part_count)
    return [
        base_size + (1 if part_index < remainder else 0)
        for part_index in range(actual_part_count)
    ]


# ---- end build_part_sizes()


# ---- split_input_file()
def split_input_file(
    input_path: Path,
    temp_dir: Path,
    line_count: int,
    part_count: int,
    buffer_size: int,
) -> list[Path]:
    """Split the source file into ordered chunk files.

    Args:
        input_path: Source file path.
        temp_dir: Temporary directory for chunk files.
        line_count: Total source line count.
        part_count: Desired number of parts.
        buffer_size: File buffer size in bytes.

    Returns:
        Ordered list of chunk input paths.
    """
    
    # ---- build balanced line counts for each part
    part_sizes = build_part_sizes(line_count, part_count)
    part_paths: list[Path] = []

    # ---- open the input file for reading
    with input_path.open("r", encoding="utf-8", buffering=buffer_size) as input_handle:
        
        # ---- iterate through the part sizes
        for part_index, part_size in enumerate(part_sizes, start=1):
            
            # ---- create the part path
            part_path = temp_dir / f"input_part_{part_index:03d}.txt"
            part_paths.append(part_path)
            
            # ---- open the part file for writing
            with part_path.open("w", encoding="utf-8", buffering=buffer_size) as part_handle:
                
                # ---- write the part data
                for _ in range(part_size):
                    line = input_handle.readline()
                    if line == "":
                        raise RuntimeError("input ended before split completed")
                    part_handle.write(line)

    return part_paths


# ---- end split_input_file()


# ---- combine_output_files()
def combine_output_files(part_output_paths: list[Path], output_path: Path) -> None:
    """Combine ordered chunk outputs into one final output file.

    Args:
        part_output_paths: Ordered chunk output paths.
        output_path: Final output path.

    Returns:
        None.
    """
    # ---- open the output file for writing
    with output_path.open("wb") as output_handle:
        # ---- iterate through the part output paths
        for part_output_path in part_output_paths:
            # ---- open the part output file for reading
            with part_output_path.open("rb") as part_handle:
                # ---- copy the part output file to the output file
                shutil.copyfileobj(part_handle, output_handle, length=LARGE_BUFFER_SIZE)


# ---- end combine_output_files()


# ======
# Benchmark Orchestration
# ======


# ---- run_single_method()
def run_single_method(
    method_spec: MethodSpec,
    input_path: Path,
    output_path: Path,
    real_time_priority: int,
) -> tuple[float, float, float, list[WorkerResult]]:
    """Run a one-process Python method.

    Args:
        method_spec: Method definition.
        input_path: Source file path.
        output_path: Output file path.
        real_time_priority: Linux SCHED_RR priority.

    Returns:
        Tuple containing split seconds, process seconds, combine seconds, and worker results.
    """
    process_start = time.perf_counter()
    worker_result = process_part_worker(
        str(input_path),
        str(output_path),
        method_spec.request_realtime,
        real_time_priority,
        method_spec.buffer_size,
    )
    process_seconds = time.perf_counter() - process_start
    return 0.0, process_seconds, 0.0, [worker_result]


# ---- end run_single_method()


# ---- run_split_method()
def run_split_method(
    method_spec: MethodSpec,
    input_path: Path,
    output_path: Path,
    temp_dir: Path,
    line_count: int,
    real_time_priority: int,
    max_auto_parts: int,
) -> tuple[float, float, float, list[WorkerResult]]:
    """Run a split/process/combine method.

    Args:
        method_spec: Method definition.
        input_path: Source file path.
        output_path: Output file path.
        temp_dir: Temporary directory for this method.
        line_count: Total source line count.
        real_time_priority: Linux SCHED_RR priority.
        max_auto_parts: Upper bound for auto-selected part counts.

    Returns:
        Tuple containing split seconds, process seconds, combine seconds, and worker results.
    """
    
    # ---- create temp dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)
    
    # ---- auto-select part count
    if method_spec.mode == "split_process_auto":
        requested_parts = min(os.cpu_count() or 1, max_auto_parts, line_count)
    else:
        requested_parts = min(method_spec.part_count, line_count)
    
    # ---- split the input file
    split_start = time.perf_counter()
    # ---- split the input file into chunks
    part_input_paths = split_input_file(
        input_path,
        temp_dir,
        line_count,
        requested_parts,
        method_spec.buffer_size,
    )
    
    # ---- record split time
    split_seconds = time.perf_counter() - split_start
    # ---- create output paths
    part_output_paths = [
        temp_dir / f"output_part_{part_index:03d}.txt"
        for part_index in range(1, len(part_input_paths) + 1)
    ]
    
    # ---- set executor class based on mode
    executor_class: type[
        concurrent.futures.ProcessPoolExecutor | concurrent.futures.ThreadPoolExecutor
    ]
    
    # ---- set executor class based on mode
    if method_spec.mode == "split_thread":
        executor_class = concurrent.futures.ThreadPoolExecutor
    else:
        executor_class = concurrent.futures.ProcessPoolExecutor
    
    # ---- record process time
    process_start = time.perf_counter()
    worker_results: list[WorkerResult] = []
    # ---- run workers
    with executor_class(max_workers=len(part_input_paths)) as executor:
        # ---- submit workers
        futures = [
            # ---- submit a worker for each part
            executor.submit(
                process_part_worker,
                str(part_input_path),
                str(part_output_path),
                method_spec.request_realtime,
                real_time_priority,
                method_spec.buffer_size,
            )
            # ---- pair the input and output paths
            for part_input_path, part_output_path in zip(part_input_paths, part_output_paths)
        ]
        
        # ---- collect results as they complete
        for future in concurrent.futures.as_completed(futures):
            worker_results.append(future.result())
    
    process_seconds = time.perf_counter() - process_start
    # ---- record combine time
    combine_start = time.perf_counter()
    # ---- combine the part output files
    combine_output_files(part_output_paths, output_path)
    combine_seconds = time.perf_counter() - combine_start

    return split_seconds, process_seconds, combine_seconds, worker_results


# ---- end run_split_method()


# ---- run_awk_method()
def run_awk_method(
    input_path: Path,
    output_path: Path,
) -> tuple[float, float, float, list[WorkerResult]]:
    """Run the awk method.

    Args:
        input_path: Source file path.
        output_path: Output file path.

    Returns:
        Tuple containing split seconds, process seconds, combine seconds, and worker results.
    """
    process_start = time.perf_counter()
    run_awk_stream(input_path, output_path)
    process_seconds = time.perf_counter() - process_start
    return 0.0, process_seconds, 0.0, []


# ---- end run_awk_method()


# ---- run_method()
def run_method(
    method_spec: MethodSpec,
    input_path: Path,
    output_dir: Path,
    temp_root: Path,
    line_count: int,
    real_time_priority: int,
    max_auto_parts: int,
) -> BenchmarkResult:
    """Run, time, and verify one method.

    Args:
        method_spec: Method definition.
        input_path: Source file path.
        output_dir: Directory for method outputs.
        temp_root: Directory for temporary chunk files.
        line_count: Total source line count.
        real_time_priority: Linux SCHED_RR priority.
        max_auto_parts: Upper bound for auto-selected part counts.

    Returns:
        BenchmarkResult for the completed method.
    """
    output_path = output_dir / f"{method_spec.name}_output.txt"
    temp_dir = temp_root / method_spec.name
    
    # ---- remove output if exists
    if output_path.exists():
        output_path.unlink()
    
    # ---- print method info
    print(f"\nRunning {method_spec.number}. {method_spec.name}")
    print(method_spec.description)

    total_start = time.perf_counter()

    # ---- run the appropriate method
    try:
        # ---- single-threaded method
        if method_spec.mode == "single":
            split_seconds, process_seconds, combine_seconds, worker_results = run_single_method(
                method_spec,
                input_path,
                output_path,
                real_time_priority,
            )
        # ---- split/process/combine methods
        elif method_spec.mode in {"split_process", "split_process_auto", "split_thread"}:
            split_seconds, process_seconds, combine_seconds, worker_results = run_split_method(
                method_spec,
                input_path,
                output_path,
                temp_dir,
                line_count,
                real_time_priority,
                max_auto_parts,
            )
        # ---- awk method
        elif method_spec.mode == "awk":
            split_seconds, process_seconds, combine_seconds, worker_results = run_awk_method(
                input_path,
                output_path,
            )
        # ---- raise error if method not supported
        else:
            raise RuntimeError(f"unsupported method mode: {method_spec.mode}")
    finally:
        # ---- cleanup temp files
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
    # ---- compute elapsed time
    elapsed_seconds = time.perf_counter() - total_start
    # ---- verify output
    verified_lines, verified_correct = verify_output(
        input_path,
        output_path,
    )

    # ---- raise error if output is incorrect
    if not verified_correct:
        raise RuntimeError(f"{method_spec.name} produced incorrect output")

    # ---- count workers that had scheduler enabled
    scheduler_enabled_workers = sum(
        1 for worker_result in worker_results if worker_result.scheduler_enabled
    )
    
    actual_part_count = max(1, len(worker_results))
    worker_count = actual_part_count
    # ---- summarize scheduler status
    scheduler_status = summarize_scheduler_status(worker_results)
    # ---- notes
    notes = "verified output equals input value multiplied by 2"

    # ---- update notes if real-time scheduling was requested but not enabled
    if method_spec.request_realtime and scheduler_enabled_workers == 0:
        notes = (
            "verified output; real-time scheduling was requested but not enabled. "
            "Linux usually requires CAP_SYS_NICE or sudo."
        )
    # ---- create benchmark result
    result = BenchmarkResult(
        method_spec=method_spec,
        input_file=input_path,
        output_file=output_path,
        line_count=line_count,
        part_count=actual_part_count,
        worker_count=worker_count,
        scheduler_enabled_workers=scheduler_enabled_workers,
        scheduler_status=scheduler_status,
        elapsed_seconds=elapsed_seconds,
        split_seconds=split_seconds,
        process_seconds=process_seconds,
        combine_seconds=combine_seconds,
        verified_lines=verified_lines,
        verified_correct=verified_correct,
        file_size_bytes=output_path.stat().st_size,
        notes=notes,
    )

    print(
        f"Completed {method_spec.name}: "
        f"{elapsed_seconds:.3f}s, verified_lines={verified_lines}, "
        f"real_time_workers={scheduler_enabled_workers}/{actual_part_count}"
    )
    return result


# ---- end run_method()


# ---- write_csv()
def write_csv(csv_path: Path, results: list[BenchmarkResult]) -> None:
    """Write benchmark results to CSV.

    Args:
        csv_path: Destination CSV path.
        results: Benchmark results to write.

    Returns:
        None.
    """
    with csv_path.open("w", encoding="utf-8", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(result.to_csv_row() for result in results)


# ---- end write_csv()


# ---- print_summary()
def print_summary(results: list[BenchmarkResult], csv_path: Path) -> None:
    """Print a compact terminal summary.

    Args:
        results: Benchmark results to summarize.
        csv_path: CSV output path.

    Returns:
        None.
    """
    print("\nBenchmark summary")
    print("-----------------")

    # ---- print results sorted by elapsed time
    for result in sorted(results, key=lambda item: item.elapsed_seconds):
        print(
            f"{result.method_spec.number:02d} {result.method_spec.name}: "
            f"{result.elapsed_seconds:.3f}s "
            f"(split={result.split_seconds:.3f}s, "
            f"process={result.process_seconds:.3f}s, "
            f"combine={result.combine_seconds:.3f}s, "
            f"verified={result.verified_correct})"
        )

    print(f"\nCSV results written: {csv_path}")


# ---- end print_summary()


# ======
# Command Line Interface
# ======


# ---- build_parser()
def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser.

    Args:
        None.

    Returns:
        Configured ArgumentParser instance.
    """
    # ---- build argument parser
    parser = argparse.ArgumentParser(
        description="Run CAT-6 real-time scheduling file-processing benchmarks.",
    )
    # ---- add arguments
    # ---- add line count argument
    parser.add_argument(
        "--line-count",
        type=positive_int,
        default=DEFAULT_LINE_COUNT,
        help="number of input lines to generate when the input file is missing",
    )
    # ---- add input file argument
    parser.add_argument(
        "--input-file",
        type=Path,
        default=None,
        help="input file path; default is benchmark_output/cat6_input_<lines>.txt",
    )
    # ---- add output directory argument
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="directory for input, outputs, and CSV results",
    )
    # ---- add methods argument
    parser.add_argument(
        "--methods",
        default="all",
        help="comma-separated method names or 'all'",
    )
    # ---- add results CSV argument
    parser.add_argument(
        "--results-csv",
        type=Path,
        default=None,
        help="CSV result path; default is output-dir/cat6_realtime_results.csv",
    )
    # ---- add force generate argument
    parser.add_argument(
        "--force-generate",
        action="store_true",
        help="replace the generated input file before running benchmarks",
    )
    # ---- add real-time priority argument
    parser.add_argument(
        "--real-time-priority",
        type=positive_int,
        default=DEFAULT_REAL_TIME_PRIORITY,
        help="SCHED_RR priority requested by real-time worker processes",
    )
    # ---- add max auto parts argument
    parser.add_argument(
        "--max-auto-parts",
        type=positive_int,
        default=32,
        help="maximum part count for method 7",
    )
    
    return parser


# ---- end build_parser()


# ---- main()
def main() -> None:
    """Run the CAT-6 benchmark program.

    Args:
        None.

    Returns:
        None.
    """
    # ---- build parser
    parser = build_parser()
    # ---- parse arguments
    args = parser.parse_args()

    try:
        # ---- parse methods
        selected_methods = parse_methods(args.methods)
    except ValueError as exc:
        parser.error(str(exc))

    # ---- set up output directory
    output_dir: Path = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir = output_dir / "method_outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    temp_root = output_dir / "temp_parts"
    temp_root.mkdir(parents=True, exist_ok=True)

    # ---- set up input file path
    input_path = args.input_file
    if input_path is None:
        input_path = output_dir / f"cat6_input_{args.line_count}.txt"
    else:
        input_path = input_path.resolve()

    csv_path = args.results_csv
    if csv_path is None:
        csv_path = output_dir / "cat6_realtime_results.csv"
    else:
        csv_path = csv_path.resolve()

    # ---- generate input file
    generate_input_file(input_path, args.line_count, args.force_generate)
    # ---- count lines
    line_count = count_lines(input_path)
    # ---- check if line count is positive
    if line_count <= 0:
        raise RuntimeError(f"input file has no lines: {input_path}")

    print(f"Measured input line count: {line_count}")
    print(f"Selected methods: {', '.join(method.name for method in selected_methods)}")

    # ---- run benchmarks
    results = [
        run_method(
            method,
            input_path,
            outputs_dir,
            temp_root,
            line_count,
            args.real_time_priority,
            args.max_auto_parts,
        )
        for method in selected_methods
    ]
    # ---- write csv results
    write_csv(csv_path, results)
    # ---- print summary
    print_summary(results, csv_path)


# ---- end main()


if __name__ == "__main__":
    main()
