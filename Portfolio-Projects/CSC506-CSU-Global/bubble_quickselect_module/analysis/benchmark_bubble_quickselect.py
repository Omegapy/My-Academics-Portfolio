# File: benchmark_bubble_quickselect.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Run repeatable Bubble Sort, Quickselect, and Python baseline benchmarks.
# - Convert timing and operation-count measurements into stable CSV rows.
# - Support Streamlit progress callbacks during benchmark execution.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# BENCHMARK POLICIES:
#   - Constants: DEFAULT_QUICK_SIZES, DEFAULT_FULL_SIZES, BENCHMARK_COLUMNS
#   - Type: ProgressCallback - Streamlit-compatible progress callback
#
# DATA CLASSES:
#   - Class: BenchmarkRecord - CSV-ready benchmark result row
#
# FUNCTIONS:
#   - Timing helpers: _to_ms(), _best_of_repeats(), _dataset_seed()
#   - Workload recorders: Bubble Sort, Python sorted, Quickselect baselines
#   - Public API: run_benchmarks(), save_results_csv(), load_results_csv()
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: collections.abc, dataclasses, pathlib, time
# - Third-Party: pandas
# - Local Project Modules: bubble_quickselect_module.algorithms, data helpers
# --- Requirements ---
# - Python 3.12+
# - pandas
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by the Benchmark Lab tab and test suite; may also be run by reports.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Benchmark pipeline for Module 8 Bubble Sort and Quickselect."""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import time

import pandas as pd

from bubble_quickselect_module.algorithms import bubble_sort, quickselect
from bubble_quickselect_module.data import (
    DEFAULT_RANDOM_SEED,
    generate_dataset_by_type,
)


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# BENCHMARK POLICIES
# ========================================================================
# These defaults keep classroom benchmark runs small enough for Streamlit while
# still showing how quadratic, linear-average, and Timsort baselines diverge.
#
# BENCHMARK CONFIGURATION OVERVIEW:
# Sizes, dataset types, CSV columns, repeat counts, and deterministic seed
# offsets are centralized here so the benchmark UI and tests share one policy.
#
# -------------------------------------------------------------------------

DEFAULT_QUICK_SIZES: list[int] = [25, 100, 250]
"""Small classroom-friendly benchmark sizes."""

DEFAULT_FULL_SIZES: list[int] = [25, 100, 500, 1_000]
"""Larger benchmark profile sizes."""

DEFAULT_BENCHMARK_DATASET_TYPES: list[str] = [
    "random",  # unordered average-case style workload
    "sorted",  # best-case Bubble Sort early-exit workload
    "reverse_sorted",  # descending order stress workload
    "duplicate_heavy",  # repeated-value workload for equality handling
    "partially_sorted",  # mostly ordered workload with controlled disorder
]
"""Dataset scenarios used by the benchmark lab."""

# Stable CSV schema used by saved benchmark artifacts and Streamlit tables.
# Any column not listed here is intentionally rejected by the export order.
BENCHMARK_COLUMNS: list[str] = [
    # Workload identity
    "dataset_type",  # generated workload family
    "size",  # input size used for the run
    "operation",  # algorithm or baseline display name
    "selected_rank",  # 1-based rank for kth-selection workloads

    # Measured values
    "elapsed_time_ms",  # best elapsed sample in milliseconds
    "comparisons",  # algorithm comparison count when available
    "swaps",  # algorithm swap count when available
    "writes",  # list-position write count when available

    # Validation and reporting
    "is_correct",  # validation flag against Python baseline behavior
    "complexity",  # expected Big-O label for the workload
    "notes",  # short recommendation/reporting context
]
"""Stable benchmark CSV column order."""

DEFAULT_REPEATS: int = 1
"""Default number of timing repetitions."""

ProgressCallback = Callable[[int, int, str], None]
"""Optional callback used by Streamlit to report benchmark progress."""

# Deterministic offsets avoid giving every dataset type the same random stream.
# Constraint: keys must match generated dataset type names used by the benchmark UI.
_DATASET_SEED_OFFSETS: dict[str, int] = {
    "random": 11,  # uniform pseudo-random workload
    "sorted": 23,  # Bubble Sort early-exit workload
    "reverse_sorted": 37,  # Bubble Sort worst-case order
    "duplicate_heavy": 53,  # equality-heavy partition/sort workload
    "partially_sorted": 71,  # nearly ordered mixed workload
}
"""Deterministic seed offsets for each workload type."""


# __________________________________________________________________________
# Class Definitions - Data Classes
# ========================================================================
# BENCHMARK RECORD
# ========================================================================
# Contains the typed result row used by every benchmark workload.
#
# DATACLASS CONTENTS:
#   - Class: BenchmarkRecord - stable CSV/UI row for one measured workload
# -------------------------------------------------------------------------

# ------------------------------------------------------------------------- class BenchmarkRecord
@dataclass(slots=True, kw_only=True)
class BenchmarkRecord:
    """Store one benchmark result row.

    Attributes:
        dataset_type: Dataset scenario key.
        size: Dataset size.
        operation: Operation display name.
        selected_rank: One-based rank for selection workloads.
        elapsed_time_ms: Elapsed time in milliseconds.
        comparisons: Algorithm comparison count when available.
        swaps: Algorithm swap count when available.
        writes: Algorithm write count when available.
        is_correct: Whether the operation result matched Python checking.
        complexity: Expected Big-O label.
        notes: Human-readable workload summary.

    Logic:
        This dataclass keeps benchmark rows stable for CSV export and Streamlit tables.
        1. Store the measured workload context and validation metadata.
        2. Preserve operation counts when the algorithm exposes them.
        3. Convert to the configured column order through ``as_dict()``.
    """

    dataset_type: str
    size: int
    operation: str
    selected_rank: int | None  # Populated only for kth-selection workloads.
    elapsed_time_ms: float
    comparisons: int | None  # None when the baseline does not expose this count.
    swaps: int | None  # None when the baseline does not expose this count.
    writes: int | None  # None when the baseline does not expose this count.
    is_correct: bool
    complexity: str
    notes: str

    # ________________________________________________
    # Utilities
    #
    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return this benchmark record as a CSV-ready dictionary.

        Returns:
            Dictionary using the stable benchmark column names.

        Logic:
            This utility maps dataclass fields to benchmark CSV columns.
            1. Read each stored field without mutating the record.
            2. Return a dictionary whose keys match ``BENCHMARK_COLUMNS``.
        """
        return {
            "dataset_type": self.dataset_type,
            "size": self.size,
            "operation": self.operation,
            "selected_rank": self.selected_rank,
            "elapsed_time_ms": self.elapsed_time_ms,
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "writes": self.writes,
            "is_correct": self.is_correct,
            "complexity": self.complexity,
            "notes": self.notes,
        }
    # --------------------------------------------------------------- end as_dict()

# ------------------------------------------------------------ end class BenchmarkRecord


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# TIMING HELPERS
# ========================================================================
# Contains small helpers that normalize timing and deterministic seeding before
# benchmark workloads are recorded.
#
# TIMING HELPER OVERVIEW:
# Timings are measured in seconds by ``time.perf_counter()`` and converted to
# rounded milliseconds for chart and CSV readability.
# =========================================================================
# - Function: _to_ms()
# - Function: _best_of_repeats()
# - Function: _dataset_seed()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- _to_ms()
def _to_ms(seconds: float) -> float:
    """Convert seconds to rounded milliseconds.

    Args:
        seconds: Elapsed seconds.

    Returns:
        Milliseconds rounded for CSV readability.
    """
    return round(seconds * 1_000.0, 6)
# --------------------------------------------------------------- end _to_ms()


# --------------------------------------------------------------- _best_of_repeats()
def _best_of_repeats(workload: Callable[[], object], repeats: int) -> float:
    """Return the fastest elapsed time from repeated runs.

    Args:
        workload: Callable workload.
        repeats: Number of timing repetitions.

    Returns:
        Fastest elapsed seconds.
    """
    best_elapsed: float = float("inf")

    # MAIN ITERATION LOOP: choose the lowest timing sample to reduce noise.
    for _ in range(max(1, repeats)):
        start_time: float = time.perf_counter()
        workload()
        elapsed: float = time.perf_counter() - start_time
        best_elapsed = min(best_elapsed, elapsed)

    return best_elapsed
# --------------------------------------------------------------- end _best_of_repeats()


# --------------------------------------------------------------- _dataset_seed()
def _dataset_seed(dataset_type: str, size: int, seed: int) -> int:
    """Build a deterministic seed for one workload.

    Args:
        dataset_type: Dataset scenario key.
        size: Dataset size.
        seed: Base seed.

    Returns:
        Derived deterministic seed.
    """
    return seed + (size * 31) + _DATASET_SEED_OFFSETS.get(dataset_type, 0)
# --------------------------------------------------------------- end _dataset_seed()


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# WORKLOAD RECORDERS
# ========================================================================
# Contains one recorder per algorithm or baseline workload in the comparison.
#
# WORKLOAD OVERVIEW:
# Each recorder runs a workload, validates it against Python behavior where
# possible, then packages the result into ``BenchmarkRecord``.
# =========================================================================
# - Function: _benchmark_bubble_sort()
# - Function: _benchmark_python_sorted()
# - Function: _benchmark_quickselect()
# - Function: _benchmark_python_sorted_selection()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- _benchmark_bubble_sort()
def _benchmark_bubble_sort(
    data: list[int],
    dataset_type: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark Bubble Sort full sorting.

    Args:
        data: Dataset values.
        dataset_type: Dataset scenario key.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord for Bubble Sort.
    """
    # Step 1: run the timed workload with the best-of-repeats helper.
    elapsed = _best_of_repeats(lambda: bubble_sort(data, collect_trace=False), repeats)
    # Step 2: run once more to capture operation counts for reporting.
    result = bubble_sort(data, collect_trace=False)
    # Step 3: package timing, counts, correctness, and complexity metadata.
    return BenchmarkRecord(
        dataset_type=dataset_type,
        size=len(data),
        operation="Bubble Sort full sort",
        selected_rank=None,
        elapsed_time_ms=_to_ms(elapsed),
        comparisons=result.comparisons,
        swaps=result.swaps,
        writes=result.writes,
        is_correct=result.sorted_data == sorted(data),
        complexity="O(n^2)",
        notes="Adjacent comparison sorting with early exit for sorted data.",
    )
# --------------------------------------------------------------- end _benchmark_bubble_sort()


# --------------------------------------------------------------- _benchmark_python_sorted()
def _benchmark_python_sorted(
    data: list[int],
    dataset_type: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark Python's built-in full sort.

    Args:
        data: Dataset values.
        dataset_type: Dataset scenario key.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord for Python sorted.
    """
    # Step 1: time Python's built-in sorted baseline.
    elapsed = _best_of_repeats(lambda: sorted(data), repeats)
    # Step 2: produce the sorted result for correctness validation.
    sorted_data = sorted(data)
    # Step 3: package baseline timing and metadata.
    return BenchmarkRecord(
        dataset_type=dataset_type,
        size=len(data),
        operation="Python sorted full sort",
        selected_rank=None,
        elapsed_time_ms=_to_ms(elapsed),
        comparisons=None,
        swaps=None,
        writes=None,
        is_correct=sorted_data == sorted(data),
        complexity="O(n log n)",
        notes="Built-in Timsort baseline for full sorted order.",
    )
# --------------------------------------------------------------- end _benchmark_python_sorted()


# --------------------------------------------------------------- _benchmark_quickselect()
def _benchmark_quickselect(
    data: list[int],
    dataset_type: str,
    repeats: int,
    selected_rank: int,
) -> BenchmarkRecord:
    """Benchmark Quickselect kth-smallest selection.

    Args:
        data: Dataset values.
        dataset_type: Dataset scenario key.
        repeats: Timing repetitions.
        selected_rank: One-based selected rank.

    Returns:
        BenchmarkRecord for Quickselect.
    """
    # Step 1: time partition-based kth selection.
    elapsed = _best_of_repeats(
        lambda: quickselect(data, selected_rank, collect_trace=False),
        repeats,
    )
    # Step 2: run once more to capture operation counts and selected value.
    result = quickselect(data, selected_rank, collect_trace=False)
    # Step 3: validate the selected value against sorted-order checking.
    expected = sorted(data)[selected_rank - 1]
    # Step 4: package timing, counts, correctness, and complexity metadata.
    return BenchmarkRecord(
        dataset_type=dataset_type,
        size=len(data),
        operation="Quickselect kth selection",
        selected_rank=selected_rank,
        elapsed_time_ms=_to_ms(elapsed),
        comparisons=result.comparisons,
        swaps=result.swaps,
        writes=result.writes,
        is_correct=result.selected_value == expected and result.is_correct,
        complexity="O(n) average, O(n^2) worst",
        notes="Partition-based selection without fully sorting the dataset.",
    )
# --------------------------------------------------------------- end _benchmark_quickselect()


# --------------------------------------------------- _benchmark_python_sorted_selection()
def _benchmark_python_sorted_selection(
    data: list[int],
    dataset_type: str,
    repeats: int,
    selected_rank: int,
) -> BenchmarkRecord:
    """Benchmark kth selection by fully sorting with Python.

    Args:
        data: Dataset values.
        dataset_type: Dataset scenario key.
        repeats: Timing repetitions.
        selected_rank: One-based selected rank.

    Returns:
        BenchmarkRecord for full-sort selection.
    """
    # Step 1: time full-sort kth selection as a baseline.
    elapsed = _best_of_repeats(lambda: sorted(data)[selected_rank - 1], repeats)
    # Step 2: capture the selected value for correctness reporting.
    selected_value = sorted(data)[selected_rank - 1]
    # Step 3: package baseline timing and metadata.
    return BenchmarkRecord(
        dataset_type=dataset_type,
        size=len(data),
        operation="Python sorted kth selection",
        selected_rank=selected_rank,
        elapsed_time_ms=_to_ms(elapsed),
        comparisons=None,
        swaps=None,
        writes=None,
        is_correct=selected_value == sorted(data)[selected_rank - 1],
        complexity="O(n log n)",
        notes="Full-sort baseline used to validate kth-smallest selection.",
    )
# ----------------------------------------------- end _benchmark_python_sorted_selection()


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# PUBLIC BENCHMARK API
# ========================================================================
# Contains the functions imported by the Streamlit benchmark tab and tests.
#
# PUBLIC API OVERVIEW:
# The public layer expands selected sizes and dataset types into a workload
# matrix, saves benchmark output, and reloads prior CSV artifacts.
# =========================================================================
# - Function: run_benchmarks()
# - Function: save_results_csv()
# - Function: load_results_csv()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- run_benchmarks()
def run_benchmarks(
    *,
    sizes: list[int] | None = None,
    dataset_types: list[str] | None = None,
    repeats: int = DEFAULT_REPEATS,
    seed: int = DEFAULT_RANDOM_SEED,
    progress_callback: ProgressCallback | None = None,
) -> pd.DataFrame:
    """Run Bubble Sort, Python sorted, Quickselect, and selection baselines.

    Args:
        sizes: Dataset sizes to benchmark.
        dataset_types: Dataset scenarios to include.
        repeats: Timing repetitions for each workload.
        seed: Base random seed.
        progress_callback: Optional callback receiving completed count, total
            count, and a workload label.

    Returns:
        Benchmark results DataFrame with stable columns.
    """
    selected_sizes = sizes or DEFAULT_QUICK_SIZES
    selected_dataset_types = dataset_types or DEFAULT_BENCHMARK_DATASET_TYPES
    total_workloads: int = len(selected_sizes) * len(selected_dataset_types) * 4
    completed: int = 0
    records: list[BenchmarkRecord] = []

    # --------------------------------------------------------------- _append_record()
    def _append_record(record: BenchmarkRecord) -> None:
        """Append one benchmark row and report progress.

        Args:
            record: Completed benchmark record.

        Returns:
            None.
        """
        nonlocal completed
        records.append(record)
        completed += 1
        # DISPATCH: Streamlit passes a callback, command-line/report callers may not.
        if progress_callback is not None:
            progress_callback(
                completed,
                total_workloads,
                f"{record.dataset_type} {record.operation} n={record.size}",
            )
    # --------------------------------------------------------------- end _append_record()

    # MAIN ITERATION LOOP: expand dataset type, size, and operation matrix.
    for size in selected_sizes:
        for dataset_type in selected_dataset_types:
            # Step 1: derive a stable dataset for this size/type pair.
            data = generate_dataset_by_type(
                dataset_type,
                size=size,
                seed=_dataset_seed(dataset_type, size, seed),
            )
            selected_rank = (len(data) + 1) // 2
            # Step 2: benchmark full-sort algorithms on the same dataset.
            _append_record(_benchmark_bubble_sort(data, dataset_type, repeats))
            _append_record(_benchmark_python_sorted(data, dataset_type, repeats))
            # Step 3: benchmark kth-selection algorithms at the median rank.
            _append_record(
                _benchmark_quickselect(
                    data,
                    dataset_type,
                    repeats,
                    selected_rank,
                )
            )
            _append_record(
                _benchmark_python_sorted_selection(
                    data,
                    dataset_type,
                    repeats,
                    selected_rank,
                )
            )

    # Step 4: emit a DataFrame with a stable column order for CSV and UI use.
    return pd.DataFrame([record.as_dict() for record in records], columns=BENCHMARK_COLUMNS)
# --------------------------------------------------------------- end run_benchmarks()


# --------------------------------------------------------------- save_results_csv()
def save_results_csv(df: pd.DataFrame, path: Path) -> None:
    """Save benchmark results to CSV.

    Args:
        df: Benchmark DataFrame.
        path: Destination CSV path.

    Returns:
        None.
    """
    # SETUP: create the analysis directory when the Streamlit benchmark saves CSV.
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
# --------------------------------------------------------------- end save_results_csv()


# --------------------------------------------------------------- load_results_csv()
def load_results_csv(path: Path) -> pd.DataFrame:
    """Load benchmark results from CSV when present.

    Args:
        path: Source CSV path.

    Returns:
        Loaded DataFrame or an empty DataFrame with stable columns.
    """
    # VALIDATION: missing CSVs return an empty table that still has expected columns.
    if not path.exists():
        return pd.DataFrame(columns=BENCHMARK_COLUMNS)
    return pd.read_csv(path)
# --------------------------------------------------------------- end load_results_csv()


# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
