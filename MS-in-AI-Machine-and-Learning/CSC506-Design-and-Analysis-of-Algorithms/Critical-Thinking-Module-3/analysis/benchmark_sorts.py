# -------------------------------------------------------------------------
# File: benchmark_sorts.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Benchmarking engine for the four sorting algorithms across multiple
# dataset types and sizes. Provides stable timing via repeated batched
# runs on fresh dataset copies, CSV persistence, and scenario-winner
# computation.
# -------------------------------------------------------------------------

# --- Functions ---
# - estimate_sort_time()          — stable per-sort timing on fresh copies
# - benchmark_single()            — time one algorithm on one scenario
# - run_benchmarks()              — full benchmark matrix → DataFrame
# - save_results_csv()            — persist benchmark table to CSV
# - load_results_csv()            — reload saved benchmark results
# - compute_scenario_winners()    — fastest algorithm per (type, size)
# - save_scenario_winners_csv()   — persist winner summaries to CSV
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Sorting-algorithm benchmarking utilities.

Timing infrastructure that runs each sorting algorithm multiple times on
fresh dataset copies, takes the best normalized time to reduce noise, and
generates a ``pandas.DataFrame`` for analysis.

**Fairness rules:**

1. Generate the base dataset once per ``(dataset_type, size)`` scenario.
2. Pass a **new copy** of the base dataset to each algorithm.
3. Every repeated timing run also receives a **fresh copy**.
4. Validate that each algorithm's output equals ``sorted(base_dataset)``.
5. Time only the sort itself — not I/O, chart rendering, or trace collection.
"""

# ________________
# Imports
#

from __future__ import annotations

import timeit
from pathlib import Path
from typing import Callable

import pandas as pd

from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from data.dataset_manager import (
    format_dataset_type_label,
    generate_dataset_by_type,
)
from models.sort_result import SortResult
from models.benchmark_record import BenchmarkRecord
from models.scenario_summary import ScenarioSummary

# __________________________________________________________________________
# Benchmark Constants
#

# ========================================================================
# Defaults
# ========================================================================

DEFAULT_SIZES: list[int] = [1_000, 5_000, 10_000, 50_000]
"""Required dataset sizes for the full assignment benchmark."""

DEFAULT_DATASET_TYPES: list[str] = [
    "random_unsorted",
    "sorted",
    "reverse_sorted",
    "partially_sorted",
]
"""Required dataset types for the full assignment benchmark."""

DEFAULT_REPEATS: int = 3
"""Number of timing repetitions per scenario."""

DEFAULT_RANDOM_SEED: int = 506
"""Seed for reproducible dataset generation."""

# Algorithm registry: name → callable
_ALGORITHMS: dict[str, Callable[..., SortResult]] = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
}

_STORAGE_DATASET_TYPE_ALIASES: dict[str, str] = {
    "random": "random_unsorted",
}
"""Maps legacy/internal dataset type keys to canonical DataFrame values."""

_GENERATION_DATASET_TYPE_ALIASES: dict[str, str] = {
    "random_unsorted": "random",
}
"""Maps canonical DataFrame values back to dataset generator keys."""

# __________________________________________________________________________
# Timing Helpers
#

# ========================================================================
# Stable Sort Timer
# ========================================================================

# --------------------------------------------------------------- _normalize_dataset_type_for_storage()
def _normalize_dataset_type_for_storage(dataset_type: str) -> str:
    """Return the canonical dataset type value stored in benchmark DataFrames.

    Args:
        dataset_type: Dataset type value from UI, tests, or legacy CSVs.

    Returns:
        The normalized dataset type value used in saved benchmark data.
    """
    return _STORAGE_DATASET_TYPE_ALIASES.get(dataset_type, dataset_type)
# --------------------------------------------------------------- end _normalize_dataset_type_for_storage()


# --------------------------------------------------------------- _normalize_dataset_type_for_generation()
def _normalize_dataset_type_for_generation(dataset_type: str) -> str:
    """Return the generator-facing dataset type key for dataset creation.

    Args:
        dataset_type: Canonical or legacy dataset type value.

    Returns:
        The dataset type key accepted by ``generate_dataset_by_type()``.
    """
    return _GENERATION_DATASET_TYPE_ALIASES.get(dataset_type, dataset_type)
# --------------------------------------------------------------- end _normalize_dataset_type_for_generation()

# --------------------------------------------------------------- estimate_sort_time()
def estimate_sort_time(
    sort_func: Callable[..., SortResult],
    data: list[int],
    repeats: int = DEFAULT_REPEATS,
) -> float:
    """Estimate per-sort runtime using batched runs on fresh copies.

    Each timed repetition receives a **fresh copy** of *data* so that
    later repetitions do not accidentally time the algorithm on
    already-sorted output.

    Args:
        sort_func: A sorting function accepting ``(data, *, collect_trace)``.
        data: The base (unsorted) dataset. Not mutated.
        repeats: How many batched timing samples to collect.

    Returns:
        Best normalized time in **seconds** for a single sort execution.
    """
    # IMPORTANT: data[:] inside the lambda ensures every repetition gets
    # a fresh unsorted copy. collect_trace=False avoids measuring
    # presentation overhead.
    timer = timeit.Timer(lambda: sort_func(data[:], collect_trace=False))
    loop_count, _ = timer.autorange()
    best_batch = min(timer.repeat(repeat=repeats, number=loop_count))
    return best_batch / loop_count
# --------------------------------------------------------------- end estimate_sort_time()

# __________________________________________________________________________
# Benchmark Functions
#

# ========================================================================
# Single-Scenario Benchmark
# ========================================================================

# --------------------------------------------------------------- benchmark_single()
def benchmark_single(
    sort_func: Callable[..., SortResult],
    data: list[int],
    dataset_type: str,
    repeats: int = DEFAULT_REPEATS,
) -> BenchmarkRecord:
    """Time one sorting algorithm on one scenario.

    Runs the algorithm once to collect metrics (comparisons, swaps, writes)
    and validates correctness. Then uses :func:`estimate_sort_time` for
    a stable timing measurement.

    Args:
        sort_func: The sorting function to benchmark.
        data: The base dataset (not mutated).
        dataset_type: Label for the dataset type.
        repeats: Timing repetitions.

    Returns:
        A populated BenchmarkRecord.
    """
    # Step 1: run once on a fresh copy to get metrics
    result: SortResult = sort_func(data[:], collect_trace=False)

    # Step 2: validate correctness
    is_correct: bool = result.sorted_data == sorted(data)

    # Step 3: stable timing estimate
    time_sec: float = estimate_sort_time(sort_func, data, repeats)
    time_ms: float = round(time_sec * 1_000, 4)

    return BenchmarkRecord(
        algorithm=result.algorithm,
        dataset_type=_normalize_dataset_type_for_storage(dataset_type),
        size=len(data),
        time_ms=time_ms,
        comparisons=result.comparisons,
        swaps=result.swaps,
        writes=result.writes,
        is_correct=is_correct,
    )
# --------------------------------------------------------------- end benchmark_single()

# ========================================================================
# Full Benchmark Matrix
# ========================================================================

# --------------------------------------------------------------- run_benchmarks()
def run_benchmarks(
    sizes: list[int] | None = None,
    dataset_types: list[str] | None = None,
    repeats: int = DEFAULT_REPEATS,
    seed: int = DEFAULT_RANDOM_SEED,
    progress_callback: Callable[[int, int, str], None] | None = None,
) -> pd.DataFrame:
    """Run the full benchmark matrix and return a DataFrame.

    For each ``(dataset_type, size)`` scenario, generates one base dataset
    and benchmarks all four algorithms on copies of that same data.

    Args:
        sizes: Dataset sizes to benchmark (default: DEFAULT_SIZES).
        dataset_types: Dataset types to benchmark (default: DEFAULT_DATASET_TYPES).
        repeats: Timing repetitions per scenario.
        seed: Random seed for dataset generation.
        progress_callback: Optional ``(current, total, label)`` callback
            for progress reporting (e.g., Streamlit progress bar).

    Returns:
        A DataFrame with one row per ``(algorithm, dataset_type, size)``
        combination. Columns: ``algorithm``, ``dataset_type``, ``size``,
        ``time_ms``, ``comparisons``, ``swaps``, ``writes``, ``is_correct``.
    """
    if sizes is None:
        sizes = DEFAULT_SIZES
    if dataset_types is None:
        dataset_types = DEFAULT_DATASET_TYPES

    total_scenarios: int = len(dataset_types) * len(sizes) * len(_ALGORITHMS)
    current: int = 0
    records: list[dict[str, object]] = []

    for dtype in dataset_types:
        for size in sizes:
            # Step 1: generate one base dataset per (type, size) scenario
            generator_dtype = _normalize_dataset_type_for_generation(dtype)
            storage_dtype = _normalize_dataset_type_for_storage(dtype)
            base_data: list[int] = generate_dataset_by_type(
                generator_dtype,
                size,
                seed=seed,
            )

            for algo_name, algo_func in _ALGORITHMS.items():
                current += 1
                if progress_callback is not None:
                    progress_callback(
                        current, total_scenarios,
                        f"{algo_name} on "
                        f"{format_dataset_type_label(storage_dtype)} "
                        f"(n={size:,})",
                    )

                # Step 2: benchmark on a fresh copy
                rec: BenchmarkRecord = benchmark_single(
                    algo_func, base_data, storage_dtype, repeats,
                )
                records.append({
                    "algorithm": rec.algorithm,
                    "dataset_type": rec.dataset_type,
                    "size": rec.size,
                    "time_ms": rec.time_ms,
                    "comparisons": rec.comparisons,
                    "swaps": rec.swaps,
                    "writes": rec.writes,
                    "is_correct": rec.is_correct,
                })

    return pd.DataFrame(records)
# --------------------------------------------------------------- end run_benchmarks()

# ========================================================================
# CSV Persistence
# ========================================================================

# --------------------------------------------------------------- save_results_csv()
def save_results_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Save benchmark results to a CSV file.

    Args:
        df: DataFrame returned by :func:`run_benchmarks`.
        path: Destination file path.
    """
    output_df = df.copy()
    if "dataset_type" in output_df.columns:
        output_df["dataset_type"] = output_df["dataset_type"].apply(
            lambda value: _normalize_dataset_type_for_storage(str(value))
        )
    output_df.to_csv(path, index=False)
# --------------------------------------------------------------- end save_results_csv()


# --------------------------------------------------------------- load_results_csv()
def load_results_csv(path: str | Path) -> pd.DataFrame:
    """Load benchmark results from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        A DataFrame with the saved benchmark data.
    """
    df = pd.read_csv(path)
    if "dataset_type" in df.columns:
        df["dataset_type"] = df["dataset_type"].apply(
            lambda value: _normalize_dataset_type_for_storage(str(value))
        )
    return df
# --------------------------------------------------------------- end load_results_csv()

# ========================================================================
# Scenario Winner Computation
# ========================================================================

# --------------------------------------------------------------- compute_scenario_winners()
def compute_scenario_winners(df: pd.DataFrame) -> pd.DataFrame:
    """Determine the fastest algorithm for each (dataset_type, size) scenario.

    Args:
        df: Benchmark results DataFrame (from :func:`run_benchmarks`).

    Returns:
        A DataFrame with columns: ``dataset_type``, ``size``,
        ``fastest_algorithm``, ``fastest_time_ms``,
        ``runner_up_algorithm``, ``notes``.
    """
    winners: list[dict[str, object]] = []

    for (dtype, size), group in df.groupby(["dataset_type", "size"]):
        ranked = group.sort_values("time_ms").reset_index(drop=True)
        best = ranked.iloc[0]
        runner_up = ranked.iloc[1] if len(ranked) > 1 else best

        # Compute percent lead for commentary
        if runner_up["time_ms"] > 0:
            pct_faster = round(
                (runner_up["time_ms"] - best["time_ms"])
                / runner_up["time_ms"] * 100,
                1,
            )
            notes = (
                f"For {format_dataset_type_label(str(dtype))} data at size {size:,}, "
                f"{best['algorithm']} "
                f"wins at {best['time_ms']:.2f} ms "
                f"({pct_faster}% faster than {runner_up['algorithm']})."
            )
        else:
            notes = (
                f"For {format_dataset_type_label(str(dtype))} data at size {size:,}, "
                f"{best['algorithm']} "
                f"wins at {best['time_ms']:.2f} ms."
            )

        winners.append({
            "dataset_type": dtype,
            "size": size,
            "fastest_algorithm": best["algorithm"],
            "fastest_time_ms": best["time_ms"],
            "runner_up_algorithm": runner_up["algorithm"],
            "notes": notes,
        })

    return pd.DataFrame(winners)
# --------------------------------------------------------------- end compute_scenario_winners()


# --------------------------------------------------------------- save_scenario_winners_csv()
def save_scenario_winners_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Save scenario winner summaries to a CSV file.

    Args:
        df: DataFrame returned by :func:`compute_scenario_winners`.
        path: Destination file path.
    """
    output_df = df.copy()
    if "dataset_type" in output_df.columns:
        output_df["dataset_type"] = output_df["dataset_type"].apply(
            lambda value: _normalize_dataset_type_for_storage(str(value))
        )
    output_df.to_csv(path, index=False)
# --------------------------------------------------------------- end save_scenario_winners_csv()

# __________________________________________________________________________
# End of File
#
