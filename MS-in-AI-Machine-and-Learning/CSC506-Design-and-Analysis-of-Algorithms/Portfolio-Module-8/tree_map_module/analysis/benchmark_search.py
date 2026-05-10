# -------------------------------------------------------------------------
# File: benchmark_search.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-21
# File Path: Portfolio-Milestone-Module-6/analysis/benchmark_search.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Build matched TreeMap and ListMap benchmark cases from shared datasets.
# - Time search workloads under multiple insertion-shape scenarios.
# - Save and summarize benchmark results for Streamlit and report artifacts.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Global Constants / Variables: benchmark defaults used across the module.
# - Function Definitions: benchmark-case builders and timing helpers.
# - Function Definitions: CSV artifact I/O and summary-table derivation.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: time, dataclasses, pathlib, typing
# - Third-Party: pandas
# - Local Project Modules:
#   - data.dataset_manager
#   - data_structures.list_map
#   - data_structures.tree_map
#   - models.benchmark_record
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the Streamlit benchmark tab to run matched timing workloads.
# - Imported by the report-generation layer to reload and summarize CSV data.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Benchmark search performance for TreeMap versus ListMap."""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

import time
from dataclasses import asdict
from pathlib import Path
from typing import Callable

import pandas as pd
# Data modules
from tree_map_module.data.dataset_manager import (
    BENCHMARK_SIZES,
    DEFAULT_RANDOM_SEED,
    generate_map_items,
    generate_search_queries,
)
# Data structure modules
from tree_map_module.data_structures.list_map import ListMap
from tree_map_module.data_structures.tree_map import Map
# Record modules
from tree_map_module.models.benchmark_record import BenchmarkRecord


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# BENCHMARK DEFAULTS
# ========================================================================
# These defaults define the scenarios surfaced in the Streamlit benchmark
# lab, CSV exports, and written analysis placeholders.
#
DEFAULT_SIZES: list[int] = list(BENCHMARK_SIZES)
"""Default benchmark sizes used by the Module 6 benchmark lab."""

DEFAULT_REPEATS: int = 5
"""Default number of repeated timing attempts per benchmark case."""

# Whitelist of benchmark query workloads supported by the Module 6 UI.
# Any query mode not listed here is rejected to keep the workload rules explicit.
DEFAULT_QUERY_MODES: list[str] = [
    "hits",  # Every query targets a key that already exists in the structure
    "misses",  # Every query targets a comparable key that is absent
    "mixed",  # The workload alternates between hits and misses
]
"""Supported query modes for the benchmark lab."""

# Whitelist of insertion scenarios surfaced by the benchmark lab.
# Any scenario not listed here is rejected so the UI and reports stay aligned.
DEFAULT_SCENARIOS: list[str] = [
    "random_insertion",  # Shuffled insertion order for a more typical tree shape
    "sorted_insertion",  # Ordered insertion path used to expose skewed growth
]
"""Supported insertion-shape scenarios for TreeMap/ListMap benchmarks."""


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# BENCHMARK BUILDERS
# ========================================================================
# These helpers keep TreeMap and ListMap workloads synchronized so timing
# differences reflect the data structures, not mismatched datasets.
#
# --------------------------------------------------------------- _scenario_to_pattern()
def _scenario_to_pattern(scenario: str) -> str:
    """Map a scenario label to a dataset-manager insertion pattern.

    Logic:
        This helper keeps benchmark scenario names aligned with dataset
        generation inputs.
        1. Match the supported scenario labels to their insertion patterns.
        2. Return the matching dataset-manager pattern string.
        3. Raise ``ValueError`` for unsupported scenario names.
    """
    # DISPATCH: benchmark scenario labels map directly to dataset-manager patterns.
    if scenario == "random_insertion":
        return "random"
    if scenario == "sorted_insertion":
        return "sorted"
    raise ValueError(
        f"Unknown scenario {scenario!r}. Choose from {DEFAULT_SCENARIOS}."
    )
# --------------------------------------------------------------- 

# --------------------------------------------------------------- _build_structures()
def _build_structures(
    size: int,
    dataset_type: str,
    scenario: str,
    seed: int,
) -> tuple[Map, ListMap]:
    """Build matched TreeMap and ListMap instances for one benchmark case.

    Logic:
        This helper ensures both structures receive the exact same workload.
        1. Translate the scenario name into one insertion pattern.
        2. Generate one shared key-value item list for that case.
        3. Build both structures from the same generated items.
    """
    insertion_pattern = _scenario_to_pattern(scenario)
    items = generate_map_items(
        size=size,
        dataset_type=dataset_type,
        insertion_pattern=insertion_pattern,
        seed=seed,
    )
    return Map(items), ListMap(items)
# ---------------------------------------------------------------

# --------------------------------------------------------------- _time_search_workload()
def _time_search_workload(
    search_callable: Callable[[object], object | None],
    queries: list[object],
    repeats: int,
) -> float:
    """Time one search workload repeatedly and return the best runtime in ms.

    Logic:
        1. Run the same query workload repeatedly for the requested repeat count.
        2. Measure each attempt with ``perf_counter``.
        3. Keep the best observed runtime as the benchmark result.
    """
    best_seconds: float | None = None
    # MAIN ITERATION LOOP: keep the best observed runtime so transient slow runs
    # do not dominate the reported benchmark case.
    for _ in range(repeats):
        start = time.perf_counter()
        # Step 1: execute the full search workload for this timing attempt.
        for key in queries:
            search_callable(key)
        elapsed = time.perf_counter() - start
        best_seconds = elapsed if best_seconds is None else min(best_seconds, elapsed)
    return (best_seconds or 0.0) * 1_000.0
# ---------------------------------------------------------------

# --------------------------------------------------------------- _build_records_for_case()
def _build_records_for_case(
    *,
    size: int,
    dataset_type: str,
    scenario: str,
    query_mode: str,
    repeats: int,
    seed: int,
) -> list[BenchmarkRecord]:
    """Build benchmark records for one ``(size, scenario, query_mode)`` case.

    Logic:
        This helper packages one matched benchmark case into CSV-ready rows.
        1. Build both structures from the same generated dataset.
        2. Time the same query workload against each structure.
        3. Return one benchmark record per structure for the case.
    """
    # Step 1: build matched structures from the same dataset and insertion order.
    tree_map, list_map = _build_structures(size, dataset_type, scenario, seed)
    items = tree_map.items()
    keys = [key for key, _ in items]
    queries = generate_search_queries(keys, query_mode, seed=seed, query_count=size)

    # Step 2: time the identical query workload against both structures.
    tree_time = _time_search_workload(tree_map.get, queries, repeats)
    list_time = _time_search_workload(list_map.get, queries, repeats)

    # Step 3: package the timings into CSV-ready dataclass rows.
    return [
        # Return one row for the TreeMap measurement.
        BenchmarkRecord(
            method="TreeMap",
            scenario=scenario,
            query_mode=query_mode,
            size=size,
            time_ms=tree_time,
            repeat_count=repeats,
            height=tree_map.height(),
            is_balanced=tree_map.is_balanced(),
            notes=f"{dataset_type} dataset",
        ),
        # Return one row for the ListMap measurement.
        BenchmarkRecord(
            method="ListMap",
            scenario=scenario,
            query_mode=query_mode,
            size=size,
            time_ms=list_time,
            repeat_count=repeats,
            height=None,
            is_balanced=None,
            notes=f"{dataset_type} dataset",
        ),
    ]
# --------------------------------------------------------------- 

# --------------------------------------------------------------- run_benchmarks()
def run_benchmarks(
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
    dataset_type: str = "integers",
    scenarios: list[str] | None = None,
    query_modes: list[str] | None = None,
    seed: int = DEFAULT_RANDOM_SEED,
    progress_callback: Callable[[int, int, str], None] | None = None,
) -> pd.DataFrame:
    """Run the full TreeMap vs ListMap search benchmark suite.

    Logic:
        1. Expand default sizes, scenarios, and query modes when callers omit them.
        2. Benchmark every requested case with matched TreeMap and ListMap inputs.
        3. Assemble the dataclass rows into a DataFrame and annotate TreeMap
           rows with derived speedup values.
    """
    # DISPATCH: expand omitted benchmark selections to the shared module defaults.
    selected_sizes = list(sizes) if sizes is not None else list(DEFAULT_SIZES)
    # Expand scenario selections.
    selected_scenarios = (
        list(scenarios) if scenarios is not None else list(DEFAULT_SCENARIOS)
    )
    # Expand query mode selections.
    selected_query_modes = (
        list(query_modes) if query_modes is not None else list(DEFAULT_QUERY_MODES)
    )

    # Compute the total number of benchmark cases to run.
    total_steps = (
        len(selected_sizes) * len(selected_scenarios) * len(selected_query_modes)
    )
    # Initialize the completed steps counter.
    completed_steps = 0
    # Initialize the list to store benchmark records.
    records: list[BenchmarkRecord] = []

    # MAIN ITERATION LOOP: benchmark every requested scenario/query-mode/size combination.
    for scenario in selected_scenarios:
        # Iterate over query modes.
        for query_mode in selected_query_modes:
            # Iterate over sizes.
            for size in selected_sizes:
                # Step 1: build and record one matched benchmark case.
                records.extend(
                    _build_records_for_case(
                        size=size,
                        dataset_type=dataset_type,
                        scenario=scenario,
                        query_mode=query_mode,
                        repeats=repeats,
                        seed=seed,
                    )
                )
                # Step 2: advance optional progress reporting after the case finishes.
                completed_steps += 1
                if progress_callback is not None:
                    progress_callback(
                        completed_steps,
                        total_steps,
                        f"{scenario}:{query_mode}:{size}",
                    )

    # Step 3: collapse the collected dataclass rows into one benchmark DataFrame.
    df = pd.DataFrame(asdict(record) for record in records)
    # Step 4: annotate TreeMap rows with the derived ListMap speedup summary.
    if not df.empty:
        df["speedup_vs_list"] = None
        speedup_lookup = compute_speedup_summary(df)
        # MAIN ITERATION LOOP: align each TreeMap row with its derived speedup value.
        for _, row in speedup_lookup.iterrows():
            # Step 5: build the exact TreeMap row mask for one benchmark case.
            mask = (
                (df["method"] == "TreeMap")
                & (df["scenario"] == row["scenario"])
                & (df["query_mode"] == row["query_mode"])
                & (df["size"] == row["size"])
            )
            # Step 6: write the derived speedup back onto the matching TreeMap row.
            df.loc[mask, "speedup_vs_list"] = row["speedup_vs_list"]

    return df
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# RESULT ARTIFACT I/O AND SUMMARIES
# ========================================================================
# These helpers persist benchmark outputs and derive summary tables that other
# analysis and UI layers reuse directly.
#
# --------------------------------------------------------------- save_results_csv()
def save_results_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Save benchmark results to CSV.

    Logic:
        This helper persists raw benchmark rows for later analysis reuse.
        1. Resolve the target path as a ``Path`` object.
        2. Create the parent directory when needed.
        3. Write the DataFrame to CSV without an index column.
    """
    target = Path(path)
    # SAFETY CHECK: create the parent directory before writing the CSV artifact.
    target.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target, index=False)
# --------------------------------------------------------------- end save_results_csv()


# --------------------------------------------------------------- load_results_csv()
def load_results_csv(path: str | Path) -> pd.DataFrame:
    """Load benchmark results from CSV.

    Logic:
        This helper reloads previously saved benchmark artifacts from disk.
        1. Resolve the requested path as a ``Path`` object.
        2. Read the CSV file into a DataFrame.
        3. Return the loaded benchmark rows.
    """
    return pd.read_csv(Path(path))
# --------------------------------------------------------------- 

# --------------------------------------------------------------- compute_speedup_summary()
def compute_speedup_summary(results_df: pd.DataFrame) -> pd.DataFrame:
    """Compute ListMap-to-TreeMap search speedup factors.

    Logic:
        1. Pivot the raw benchmark rows so ListMap and TreeMap timings align.
        2. Rename the timing columns into analysis-friendly names.
        3. Compute the ListMap/TreeMap ratio for each benchmark case.
    """
    # VALIDATION: empty benchmark inputs produce an empty summary with a stable schema.
    if results_df.empty:
        return pd.DataFrame(
            columns=[
                "scenario",
                "query_mode",
                "size",
                "tree_time_ms",
                "list_time_ms",
                "speedup_vs_list",
            ]
        )

    pivot = results_df.pivot_table(
        index=["scenario", "query_mode", "size"],
        columns="method",
        values="time_ms",
        aggfunc="min",
    ).reset_index()

    # VALIDATION: both structures must be present before a speedup can be computed.
    if "TreeMap" not in pivot.columns or "ListMap" not in pivot.columns:
        return pd.DataFrame(
            columns=[
                "scenario",
                "query_mode",
                "size",
                "tree_time_ms",
                "list_time_ms",
                "speedup_vs_list",
            ]
        )

    summary = pivot.rename(
        columns={
            "TreeMap": "tree_time_ms",
            "ListMap": "list_time_ms",
        }
    )
    summary["speedup_vs_list"] = summary["list_time_ms"] / summary["tree_time_ms"]
    return summary.sort_values(["scenario", "query_mode", "size"]).reset_index(drop=True)
# --------------------------------------------------------------- 

# --------------------------------------------------------------- compute_balance_summary()
def compute_balance_summary(results_df: pd.DataFrame) -> pd.DataFrame:
    """Return a compact summary of TreeMap height and balance by scenario/size.

    Logic:
        This function reduces raw TreeMap benchmark rows into one balance
        summary per scenario and size.
        1. Filter the benchmark rows down to TreeMap results only.
        2. Return a stable empty schema when no TreeMap rows exist.
        3. Aggregate minimum height and balance state by scenario and size.
    """
    tree_rows = results_df[results_df["method"] == "TreeMap"].copy()
    # VALIDATION: non-TreeMap-only inputs cannot yield a balance summary.
    if tree_rows.empty:
        return pd.DataFrame(columns=["scenario", "size", "height", "is_balanced"])

    summary = (
        tree_rows.groupby(["scenario", "size"], as_index=False)
        .agg({"height": "min", "is_balanced": "min"})
        .sort_values(["scenario", "size"])
        .reset_index(drop=True)
    )
    return summary
# --------------------------------------------------------------- 

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------