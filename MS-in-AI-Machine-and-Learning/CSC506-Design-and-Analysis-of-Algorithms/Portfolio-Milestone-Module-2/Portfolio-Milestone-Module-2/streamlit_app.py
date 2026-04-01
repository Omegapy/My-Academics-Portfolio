# -------------------------------------------------------------------------
# File: streamlit_app.py
# Author: Alexander Ricciardi
# Date: 2026-03-24
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Main entry point for the Streamlit-based Algorithm Comparison Tool.
# Provides seven tabs: Overview, Dataset Builder, Search Playground,
# Compare Algorithms, Benchmark Lab, Big-O Analysis, and Analysis Guide.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit application - Algorithm Comparison Tool.

Launch with::

    streamlit run Portfolio-Milestone-Module-2/streamlit_app.py
"""

# ________________
# Imports
#

from __future__ import annotations

import gc
import sys
import os
import time
from functools import partial
from pathlib import Path

# SETUP: add project root so sibling packages are importable
_PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
import pandas as pd

from typing import Callable

from algorithms.linear_search import linear_search
from algorithms.binary_search import binary_search
from models.search_result import SearchResult
from data.dataset_manager import (
    generate_sample_dataset,
    generate_random_dataset,
    parse_manual_input,
    remove_duplicates,
    sorted_copy,
    validate_dataset,
)
from analysis.benchmark_searches import run_benchmarks, save_results_csv
from ui.streamlit_helpers import (
    render_header,
    render_search_result,
    render_comparison,
    render_dataset_info,
    render_dataset_scrollable,
    render_benchmark_charts,
    render_analysis_markdown_file,
)

# __________________________________________________________________________
# Page Configuration
#

st.set_page_config(
    page_title="Algorithm Comparison Tool",
    page_icon="🔍",
    layout="wide",
)

# __________________________________________________________________________
# Session State Initialization
#

if "dataset" not in st.session_state:
    st.session_state.dataset = []
if "sorted_dataset" not in st.session_state:
    st.session_state.sorted_dataset = []
if "target" not in st.session_state:
    st.session_state.target = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "benchmark_df" not in st.session_state:
    st.session_state.benchmark_df = None

# __________________________________________________________________________
# Stable Search Helper
#

_TIMING_BATCH_TARGET_NS: int = 20_000_000
_TIMING_REPEATS: int = 5
_SORTED_BINARY_SEARCH = partial(binary_search, validate_sorted=False)

# --------------------------------------------------------------- _estimate_elapsed_time()
def _estimate_elapsed_time(
    algorithm_func: Callable[[list[int], int], SearchResult],
    data: list[int],
    target: int,
) -> float:
    """Estimate per-search wall time using batched runs.

    Very small searches complete in only a few microseconds, so a single
    timer reading is dominated by scheduling noise and timer overhead.
    This helper follows the same general idea as ``timeit``: run the
    callable repeatedly until the batch is large enough to measure
    reliably, then keep the fastest repeated batch as the per-search
    estimate.

    Args:
        algorithm_func: ``linear_search`` or ``binary_search``.
        data: The dataset to search.
        target: The value to search for.

    Returns:
        Estimated elapsed time in seconds for one search.
    """
    loop_count: int = 1
    gc_was_enabled: bool = gc.isenabled()

    if gc_was_enabled:
        gc.disable()

    try:
        # Step 1: choose a loop count large enough for stable timing.
        while True:
            start_ns = time.perf_counter_ns()
            for _ in range(loop_count):
                algorithm_func(data, target)
            elapsed_ns = time.perf_counter_ns() - start_ns

            if elapsed_ns >= _TIMING_BATCH_TARGET_NS:
                break

            loop_count *= 2

        # Step 2: repeat the batch and keep the best timing, matching the
        # timeit guidance for short-running code.
        batch_times_ns: list[int] = []
        for _ in range(_TIMING_REPEATS):
            start_ns = time.perf_counter_ns()
            for _ in range(loop_count):
                algorithm_func(data, target)
            batch_times_ns.append(time.perf_counter_ns() - start_ns)
    finally:
        if gc_was_enabled:
            gc.enable()

    best_batch_ns = min(batch_times_ns)
    return best_batch_ns / loop_count / 1_000_000_000
# --------------------------------------------------------------- end _estimate_elapsed_time()

# --------------------------------------------------------------- stable_search()
def stable_search(
    algorithm_func: Callable[[list[int], int], SearchResult],
    data: list[int],
    target: int,
) -> SearchResult:
    """Run a search and replace its raw timing with a batched estimate.

    Args:
        algorithm_func: ``linear_search`` or ``binary_search``.
        data: The dataset to search.
        target: The value to search for.

    Returns:
        A SearchResult with ``elapsed_time`` replaced by a more stable
        estimate from repeated batched timing.
    """
    result = algorithm_func(data, target)
    if result.dataset_size == 0:
        return result

    result.elapsed_time = _estimate_elapsed_time(algorithm_func, data, target)
    return result
# --------------------------------------------------------------- end stable_search()

# __________________________________________________________________________
# Header
#

render_header()

# __________________________________________________________________________
# Tabs
#

(
    tab_overview,
    tab_dataset,
    tab_playground,
    tab_compare,
    tab_bench,
    tab_big_o,
    tab_analysis,
) = st.tabs([
    "Overview",
    "Dataset Builder",
    "Search Playground",
    "Compare Algorithms",
    "Benchmark Lab",
    "Big-O Analysis",
    "Recommendation Guide",
])

# ========================================================================
# Tab 1 — Overview
# ========================================================================

with tab_overview:
    st.header("Project Overview")
    st.markdown(
        """
        This Algorithm Comparison Tool that compares the following search algorithms:

        * Linear Search, with an O(n) time complexity, it scans every element sequentially.
        * Binary Search, with an O(log n) time complexity, halves the data 
        that needs to be scanned each step (requires sorted data).

        Use the tabs above to build datasets, run individual searches, compare
        their time complexity, benchmark them, and read an overview of the Big-O analysis.
        """
    )

    st.subheader("Dataset Rules")
    st.info(
        "All datasets in this project are sorted and contain no duplicate "
        "values. Binary search relies on sorted data, and it eliminates half the "
        "search space at every step; if the data were unsorted, the algorithm "
        "could discard the portion that actually contains the value being searched for, "
        "producing incorrect results. Additionally, the datasets do not contain duplicate values because "
        "duplicate values add additional complexity, such as deciding which occurrence "
        "to return or return all occurrences of the searched value. This is outside the scope of this milestone. "
        "Futhermore, enforcing sorted keeps with no duplicates keeps the focus on comparing the "
        "O(n) vs. O(log n) performance of the linear and binary search algorithms."
    )

    st.subheader("Linear Search")
    st.info(
        "O(n) worst-case. Searches each element from index 0 to the end. "
        "Works on any sorted or unsorted list. Returns as soon as the target value"
        "is found, or after scanning every element, if the target is not found."
    )

    st.subheader("Binary Search")
    st.info(
        "O(log n) worst-case. Requires a sorted list. Searches the "
        "midpoint, compares it to the searched value, and eliminates half the search data space"
        "each step. It is significantly faster than linear search for large "
        "datasets, but does not work on unsorted data."
    )

    st.subheader("Key Concepts")
    st.info(
        "Big-O Notation describes how an algorithm's running time grows as "
        "the input size increases. O(n) means the time grows linearly; O(log n) "
        "means the time grows logarithmically, which is much more slowly, usually resulting in "
        "significantly faster search times for large datasets."
    )

# ========================================================================
# Tab 2 — Dataset Builder
# ========================================================================

with tab_dataset:
    st.header("Dataset Builder")
    st.markdown("Create a dataset to use in the Search Playground and Compare tabs.")

    source = st.radio(
        "Data source",
        ["Sample (20 items)", "Random (custom size)", "Manual entry"],
        horizontal=True,
    )

    if source == "Sample (20 items)":
        if st.button("Generate Sample Dataset", key="btn_sample"):
            data = generate_sample_dataset(20)
            st.session_state.dataset = data
            st.session_state.sorted_dataset = sorted_copy(data)
            st.session_state.last_result = None
            st.success(f"Sample dataset loaded — {len(data)} elements.")

    elif source == "Random (custom size)":
        size = st.number_input(
            "Dataset size", min_value=10, max_value=100_000, value=1_000, step=100
        )
        if st.button("Generate Random Dataset", key="btn_random"):
            data = generate_random_dataset(int(size))
            st.session_state.dataset = data
            st.session_state.sorted_dataset = sorted_copy(data)
            st.session_state.last_result = None
            st.success(f"Random dataset generated — {len(data)} elements.")

    else:  # Manual entry
        raw = st.text_input(
            "Enter comma-separated integers", placeholder="5, 3, 8, 1, 9"
        )
        if st.button("Parse Manual Input", key="btn_manual"):
            try:
                data = parse_manual_input(raw)
                # VALIDATION: strip duplicate values and warn the user
                data, removed = remove_duplicates(data)
                if removed:
                    st.warning(
                        f"⚠️ Duplicate values removed: "
                        f"{', '.join(str(v) for v in removed)}. "
                        f"This project uses unique-value datasets only."
                    )
                valid, msg = validate_dataset(data)
                if valid:
                    st.session_state.dataset = data
                    st.session_state.sorted_dataset = sorted_copy(data)
                    st.session_state.last_result = None
                    st.success(msg)
                else:
                    st.error(msg)
            except ValueError as exc:
                st.error(str(exc))

    # Show current dataset if available
    if st.session_state.dataset:
        st.divider()
        render_dataset_info(st.session_state.dataset, st.session_state.sorted_dataset)

# ========================================================================
# Tab 3 — Search Playground
# ========================================================================

with tab_playground:
    st.header("Search Playground")

    if not st.session_state.dataset:
        st.warning("Please build a dataset first in the **Dataset Builder** tab.")
    else:
        render_dataset_scrollable(st.session_state.sorted_dataset)
        st.divider()

        with st.form("search_playground_form"):
            algo_choice = st.radio(
                "Algorithm",
                ["Linear Search", "Binary Search"],
                horizontal=True,
                key="playground_algo",
            )

            target_val = st.number_input(
                "Target value",
                value=0,
                step=1,
                key="playground_target",
            )

            run_search = st.form_submit_button("Run Search")

        if run_search:
            if algo_choice == "Linear Search":
                result = stable_search(linear_search, st.session_state.sorted_dataset, int(target_val))
            else:
                result = stable_search(
                    _SORTED_BINARY_SEARCH,
                    st.session_state.sorted_dataset,
                    int(target_val),
                )

            st.session_state.last_result = result

        if st.session_state.last_result is not None:
            st.caption(
                "Timing is estimated from repeated batched runs so very small searches "
                "are less affected by microsecond-level measurement noise."
            )
            render_search_result(st.session_state.last_result)

# ========================================================================
# Tab 4 — Compare Algorithms
# ========================================================================

with tab_compare:
    st.header("Compare Algorithms")

    if not st.session_state.dataset:
        st.warning("Please build a dataset first in the **Dataset Builder** tab.")
    else:
        render_dataset_scrollable(st.session_state.sorted_dataset)
        st.divider()

        st.info(
            "Both algorithms run on the sorted dataset to keep the comparison "
            "fair. Binary search requires sorted data; linear search works "
            "on sorted data too (just without the logarithmic advantage)."
        )

        # Quick Compare — First / Mid / Last
        st.subheader("Quick Compare: First / Mid / Last")
        st.markdown(
            "Run both algorithms on three positions to see how "
            "element location affects performance."
        )

        if st.button("Run Quick Compare", key="btn_quick_compare"):
            sorted_data = st.session_state.sorted_dataset
            n = len(sorted_data)
            binary_mid_index = (n - 1) // 2
            targets = {
                "First Element": sorted_data[0],
                "Middle Element": sorted_data[binary_mid_index],
                "Last Element": sorted_data[-1],
                "Not In Dataset (worst case)": max(sorted_data) + 1,
            }

            for label, target in targets.items():
                st.markdown(f"### {label} — target = `{target}`")
                lin = stable_search(linear_search, sorted_data, target)
                bsn = stable_search(_SORTED_BINARY_SEARCH, sorted_data, target)
                render_comparison(lin, bsn)

        # Manual compare
        st.divider()
        st.subheader("Manual Compare")

        with st.form("compare_form"):
            compare_target = st.number_input(
                "Target value",
                value=0,
                step=1,
                key="compare_target",
            )
            compare_clicked = st.form_submit_button("Compare")

        if compare_clicked:
            sorted_data = st.session_state.sorted_dataset
            lin_result = stable_search(linear_search, sorted_data, int(compare_target))
            bin_result = stable_search(
                _SORTED_BINARY_SEARCH,
                sorted_data,
                int(compare_target),
            )
            render_comparison(lin_result, bin_result)

# ========================================================================
# Tab 5 — Benchmark Lab
# ========================================================================

with tab_bench:
    st.header("Benchmark Lab")
    st.markdown(
        "Run timed benchmarks across multiple dataset sizes to observe "
        "how linear search and binary search scale."
    )
    st.info(
        "Each benchmark uses a worst-case target value (`max(dataset) + 1`) that is "
        "guaranteed not to exist in the dataset. This forces linear search to scan "
        "every element and binary search to exhaust all halvings, ensuring both "
        "algorithms perform their maximum number of comparisons."
    )
    st.caption(
        "Benchmark timings measure the search calls on data that is already sorted. "
        "The benchmark skips step-trace generation and redundant binary-search "
        "sortedness checks so the results reflect the search algorithms themselves. "
        "Each timing is measured with repeated batched runs to reduce microsecond-level noise."
    )

    default_sizes = [100, 1_000, 5_000, 10_000, 50_000]
    sizes = st.multiselect(
        "Dataset sizes",
        options=[100, 500, 1_000, 2_000, 5_000, 10_000, 25_000, 50_000, 100_000],
        default=default_sizes,
    )

    repeats = st.slider("Timing Samples per Size", min_value=5, max_value=50, value=10)
    st.caption(
        "This controls how many repeated timing samples are collected for each dataset size. "
        "Within each sample, the benchmark uses batched runs to make very small timings more reliable."
    )

    if st.button("Run Benchmarks", key="btn_bench"):
        if not sizes:
            st.error("Select at least one dataset size.")
        else:
            with st.spinner(
                "Running benchmarks with repeated batched timing. "
                "This can take a moment because each algorithm is executed many times "
                "at each dataset size so the results are more reliable."
                "`timeit.autorange()` automatically decides how many search calls belong "
                "inside each sample so the timing is long enough to be trustworthy."
            ):
                df = run_benchmarks(sorted(sizes), repeats)
                st.session_state.benchmark_df = df

    if st.session_state.benchmark_df is not None:
        render_benchmark_charts(st.session_state.benchmark_df)

        # CSV export
        csv_path = _PROJECT_ROOT / "analysis" / "benchmark_results.csv"
        if st.button("Save Results to CSV", key="btn_save_csv"):
            save_results_csv(st.session_state.benchmark_df, csv_path)
            st.success(f"Saved to `{csv_path}`")

# ========================================================================
# Tab 6 — Big-O Analysis
# ========================================================================

with tab_big_o:

    analysis_dir = _PROJECT_ROOT / "analysis"
    analysis_benchmark_df = st.session_state.benchmark_df

    if analysis_benchmark_df is None:
        st.info(
            "Please run the **Benchmark Lab** first to generate the Big-O analysis."
        )
    else:
        big_o_path = analysis_dir / "big_o_analysis.md"
        render_analysis_markdown_file(big_o_path, benchmark_df=analysis_benchmark_df)

# ========================================================================
# Tab 7 — Recommendation Guide
# ========================================================================

with tab_analysis:

    rec_path = _PROJECT_ROOT / "analysis" / "recommendation_guide.md"
    render_analysis_markdown_file(rec_path, benchmark_df=analysis_benchmark_df)

# __________________________________________________________________________
# End of File
#
