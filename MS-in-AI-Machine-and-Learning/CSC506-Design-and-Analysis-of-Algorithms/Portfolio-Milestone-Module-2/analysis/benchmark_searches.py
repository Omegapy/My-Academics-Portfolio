# -------------------------------------------------------------------------
# File: benchmark_searches.py
# Author: Alexander Ricciardi
# Date: 2026-03-29
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Benchmarking linear and binary search across
# multiple dataset sizes, collecting median timing results, and
# saving / loading those results as CSV.
# -------------------------------------------------------------------------

# --- Functions ---
# - benchmark_single()  — run one algorithm N times, return median time
# - run_benchmarks()    — benchmark both algorithms across multiple sizes
# - save_results_csv()  — persist results to CSV
# - load_results_csv()  — load CSV into a pandas DataFrame
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Search-algorithm benchmarking utilities.

Timing infrastructure that runs each algorithm multiple times per
dataset size, takes the median to reduce noise, and generates a
``pandas.DataFrame``.
"""

# ________________
# Imports
#

from __future__ import annotations

from functools import partial
from pathlib import Path
import timeit
from typing import Callable

import pandas as pd

import sys
import os
# SETUP: add project root so sibling packages are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.linear_search import linear_search
from algorithms.binary_search import binary_search
from data.dataset_manager import generate_random_dataset, sorted_copy
from models.search_result import SearchResult

# __________________________________________________________________________
# Benchmark Constants
#

# Default dataset sizes for benchmarking
DEFAULT_SIZES: list[int] = [100, 1_000, 5_000, 10_000, 50_000]

# Default number of repeated benchmark samples per size
DEFAULT_REPEATS: int = 5

# __________________________________________________________________________
# Benchmark Functions
#

# ========================================================================
# Single-Algorithm Benchmark
# ========================================================================

# --------------------------------------------------------------- benchmark_single()
def benchmark_single(
    algorithm_func: Callable[[list[int], int], SearchResult],
    data: list[int],
    target: int,
    repeats: int = DEFAULT_REPEATS,
) -> tuple[float, int]:
    """Benchmark one search algorithm using ``timeit`` style batching.

    Args:
        algorithm_func: A search function with signature
            ``(data: list[int], target: int) -> SearchResult``.
        data: The dataset to search.
        target: The value to search for.
        repeats: How many repeated batch samples to collect.

    Returns:
        A ``(best_time_seconds, comparisons)`` tuple.
    """
    result = algorithm_func(data, target)
    comparisons: int = result.comparisons

    timer = timeit.Timer(lambda: algorithm_func(data, target))
    loop_count, _ = timer.autorange()
    best_batch_time = min(timer.repeat(repeat=repeats, number=loop_count))
    return best_batch_time / loop_count, comparisons
# --------------------------------------------------------------- end benchmark_single()

# ========================================================================
# Full Benchmark Suite
# ========================================================================

# --------------------------------------------------------------- run_benchmarks()
def run_benchmarks(
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
) -> pd.DataFrame:
    """Benchmark linear and binary search across multiple dataset sizes.

    For each size a random dataset is generated, sorted, and both
    algorithms are tested with a worst-case target (a value guaranteed
    not to be in the dataset) so that every run the full
    search path.

    Args:
        sizes: List of dataset sizes to test (default: DEFAULT_SIZES).
        repeats: Repetitions per algorithm per size (default 10).

    Returns:
        A ``pandas.DataFrame`` with columns:
        ``size``, ``linear_time_ms``, ``binary_time_ms``,
        ``linear_comparisons``, ``binary_comparisons``.
    """
    if sizes is None:
        sizes = DEFAULT_SIZES

    rows: list[dict[str, int | float]] = []

    for size in sizes:
        # Step 1: generate sorted dataset
        raw = generate_random_dataset(size)
        data = sorted_copy(raw)

        # Step 2: choose worst-case target (not in dataset)
        worst_target = max(data) + 1

        # SETUP: benchmark the search logic itself. The dataset is already
        # sorted, so binary-search validation is redundant here, and the
        # benchmark does not need UI step traces.
        linear_benchmark = partial(linear_search, collect_trace=False)
        binary_benchmark = partial(
            binary_search,
            validate_sorted=False,
            collect_trace=False,
        )

        # Step 3: benchmark linear search
        lin_time, lin_comps = benchmark_single(
            linear_benchmark,
            data,
            worst_target,
            repeats,
        )

        # Step 4: benchmark binary search
        bin_time, bin_comps = benchmark_single(
            binary_benchmark,
            data,
            worst_target,
            repeats,
        )

        rows.append({
            "size": size,
            "linear_time_ms": round(lin_time * 1_000, 4),
            "binary_time_ms": round(bin_time * 1_000, 4),
            "linear_comparisons": lin_comps,
            "binary_comparisons": bin_comps,
        })

    return pd.DataFrame(rows)
# --------------------------------------------------------------- end run_benchmarks()

# ========================================================================
# CSV Persistence
# ========================================================================

# --------------------------------------------------------------- save_results_csv()
def save_results_csv(results: pd.DataFrame, path: str | Path) -> None:
    """Save benchmark results to a CSV file.

    Args:
        results: DataFrame returned by ``run_benchmarks()``.
        path: Destination file path.
    """
    results.to_csv(path, index=False)
# --------------------------------------------------------------- end save_results_csv()

# --------------------------------------------------------------- load_results_csv()
def load_results_csv(path: str | Path) -> pd.DataFrame:
    """Load benchmark results from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        A ``pandas.DataFrame`` with the saved benchmark data.
    """
    return pd.read_csv(path)
# --------------------------------------------------------------- end load_results_csv()

# __________________________________________________________________________
# End of File
#
