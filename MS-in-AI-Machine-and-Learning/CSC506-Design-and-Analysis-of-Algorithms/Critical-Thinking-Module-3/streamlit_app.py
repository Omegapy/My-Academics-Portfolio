# -------------------------------------------------------------------------
# File: streamlit_app.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Main entry point for the Sorting Algorithm Comparison Tool.
# Provides seven tabs: Overview, Dataset Builder,
# Sort Playground, Compare Algorithms, Benchmark Lab, Written Analysis,
# and Recommendation Guide.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit application - Sorting Algorithm Performance Comparison Tool.

Launch with::

    streamlit run CTA-3/streamlit_app.py
"""

# ________________
# Imports
#

from __future__ import annotations

import sys
from pathlib import Path

# SETUP: add project root so sibling packages are importable
_PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
import pandas as pd

from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from data.dataset_manager import (
    generate_dataset_by_type,
    format_dataset_type_label,
    preview_dataset,
    is_sorted_non_decreasing,
    DATASET_TYPES,
)
from analysis.benchmark_sorts import (
    run_benchmarks,
    save_results_csv,
    load_results_csv,
    compute_scenario_winners,
    estimate_sort_time,
    DEFAULT_SIZES,
    DEFAULT_DATASET_TYPES,
)
from analysis.report_generator import (
    build_comparison_table,
    build_winner_summary,
)
from ui.streamlit_helpers import (
    render_header,
    render_dataset_info,
    render_sort_result,
    render_comparison_grid,
    render_step_trace,
    render_benchmark_table,
    render_benchmark_charts,
    render_analysis_markdown_file,
)

# ======================================================================
# Page Configuration
# ======================================================================

st.set_page_config(
    page_title="CTA-3 — Sorting Comparison",
    layout="wide",
)

# ======================================================================
# Session State Initialization
# ======================================================================

_DEFAULTS: dict[str, object] = {
    "dataset": None,
    "dataset_type": "random",
    "dataset_size": 1000,
    "sort_results": {},
    "benchmark_df": None,
    "scenario_winners_df": None,
}

for _key, _val in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val

# ======================================================================
# Algorithm Registry
# ======================================================================

_ALGO_MAP: dict[str, object] = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
}

# ======================================================================
# App Header
# ======================================================================

render_header()

# ======================================================================
# Tab Layout
# ======================================================================

tab_overview, tab_dataset, tab_playground, tab_compare, tab_benchmark, \
    tab_analysis, tab_guide = st.tabs([
        "Overview",
        "Dataset Builder",
        "Sort Playground",
        "Compare Algorithms",
        "Benchmark Lab",
        "Written Analysis",
        "Recommendation Guide",
    ])

# ======================================================================
# Tab 1: Overview
# ======================================================================

with tab_overview:
    st.header("Project Overview")

    st.markdown("""
**CTA-3 — Sorting Algorithm Performance Comparison Tool** allows you to
explore, compare, and benchmark four classic sorting algorithms:

| Algorithm | Best / Average / Worst | Space | Stable | In-Place |
|-----------|------------------------|-------|--------|----------|
| **Bubble Sort** | Ω(n) / Θ(n²) / O(n²) | O(1) | Yes | Yes |
| **Selection Sort** | Ω(n²) / Θ(n²) / O(n²) | O(1) | No | Yes |
| **Insertion Sort** | Ω(n) / Θ(n²) / O(n²) | O(1) | Yes | Yes |
| **Merge Sort** | Ω(n log n) / Θ(n log n) / O(n log n) | O(n) | Yes | No |
    """)

    # ---- Algorithm Descriptions ----

    st.subheader("Bubble Sort")
    st.info(
        "Bubble Sort repeatedly steps through the list, compares adjacent "
        "elements, and swaps them if they are in the wrong order. Each full "
        "pass \"bubbles\" the next-largest value into its final position. "
        "An early-exit optimization stops the algorithm when a complete pass "
        "makes zero swaps, which gives a best-case time of Ω(n) on already-"
        "sorted input. In the average and worst cases the time is O(n²). "
        "Bubble Sort is stable and in-place with O(1) extra space."
    )

    st.subheader("Selection Sort")
    st.info(
        "Selection Sort divides the list into a sorted prefix and an unsorted "
        "suffix. On each pass it scans the unsorted portion for the minimum "
        "value and swaps it into the next position of the sorted prefix. "
        "Because it always scans the full unsorted region, it performs Θ(n²) "
        "comparisons regardless of input order — best, average, and worst "
        "cases are all O(n²). Selection Sort is in-place with O(1) extra "
        "space, but it is not stable because the swap can change the "
        "relative order of equal elements."
    )

    st.subheader("Insertion Sort")
    st.info(
        "Insertion Sort builds the sorted result one element at a time. For "
        "each element it shifts larger values to the right until it finds "
        "the correct insertion position. On already-sorted data each element "
        "needs zero shifts, giving a best-case time of Ω(n). On random or "
        "reverse-sorted data the average and worst cases are O(n²). "
        "Insertion Sort is stable and in-place with O(1) extra space."
    )

    st.subheader("Merge Sort")
    st.info(
        "Merge Sort is a divide-and-conquer algorithm. It recursively splits "
        "the list into halves until each sub-list has one element, then "
        "merges the sub-lists back together in sorted order. Because every "
        "split and merge level does O(n) work across log n levels, the "
        "running time is Θ(n log n) in all cases — best, average, and worst. "
        "Merge Sort is stable but not in-place; it requires O(n) extra "
        "space for the temporary merge arrays."
    )

    # ---- Sorting Concepts ----

    st.subheader("Sorting Concepts")
    st.info(
        "**Space Complexity** describes how much extra memory an algorithm "
        "uses beyond the input itself. O(1) means a constant amount of extra "
        "memory regardless of input size; O(n) means the extra memory grows "
        "proportionally with the number of elements.\n\n"
        "**Stable** — a stable sorting algorithm preserves the relative order "
        "of elements that compare as equal. If two items share the same sort "
        "key, they appear in the output in the same order they appeared in "
        "the input.\n\n"
        "**In-Place** — an in-place sorting algorithm rearranges elements "
        "within the original list without allocating a separate output "
        "structure. It may use a small, constant amount of extra memory for "
        "temporary variables (swaps, indices), but does not create a copy of "
        "the data."
    )

    # ---- Key Concepts: Asymptotic Notation ----

    st.subheader("Key Concepts")
    st.info(
        "**Asymptotic Notation** describes how an algorithm's running time "
        "grows as the input size *n* increases. There are three notations "
        "used to characterize different cases:\n\n"
        "**Big-O (O)** — an upper bound on the running time, used to "
        "describe the **worst case**. For example, Bubble Sort is O(n²) in "
        "the worst case because it may need to compare and swap across every "
        "pair of elements.\n\n"
        "**Big-Theta (Θ)** — a tight bound, used when the running time is "
        "the **same for all cases**. For example, Selection Sort is Θ(n²) "
        "because it always performs roughly n²/2 comparisons regardless of "
        "input order. Merge Sort is Θ(n log n) because its divide-and-merge "
        "structure performs the same amount of work on any input.\n\n"
        "**Big-Omega (Ω)** — a lower bound on the running time, used to "
        "describe the **best case**. For example, Bubble Sort is Ω(n) on "
        "already-sorted input — one pass with zero swaps triggers the "
        "early-exit optimization. Insertion Sort is also Ω(n) on sorted "
        "data, since each element requires only one comparison and no shifts."
    )

    # ---- How to Use / Goals ----

    st.markdown("""
### How to Use This Tool

1. **Dataset Builder** — Generate datasets of various types and sizes
2. **Sort Playground** — Run a single algorithm and view step traces
3. **Compare Algorithms** — Run all 4 algorithms side-by-side
4. **Benchmark Lab** — Full benchmark matrix with timing charts
5. **Written Analysis** — 2–3 page analysis of results
6. **Recommendation Guide** — When to use each algorithm

### Assignment Goals

- Implement four sorting algorithms (Bubble, Selection, Insertion, Merge Sort)
- Build a reproducible timing system for benchmarking
- Test across four dataset types and multiple sizes
- Analyze results with charts and written interpretation
- Provide practical guidance for algorithm selection
    """)

    st.info(
        "**Start with the Dataset Builder tab** to generate a dataset, "
        "then explore sorting in the Playground or Compare tabs."
    )

# ======================================================================
# Tab 2: Dataset Builder
# ======================================================================

with tab_dataset:
    st.header("Dataset Builder")
    st.markdown("Generate datasets for sorting experiments.")

    # ---- Controls ----
    col_type, col_size, col_seed = st.columns(3)

    with col_type:
        ds_type = st.selectbox(
            "Dataset Type",
            options=DATASET_TYPES,
            format_func=format_dataset_type_label,
            index=DATASET_TYPES.index(st.session_state["dataset_type"]),
            key="ds_type_select",
        )

    with col_size:
        size_presets = [100, 1_000, 5_000, 10_000, 50_000]
        preset = st.selectbox(
            "Size Preset",
            options=["Custom"] + [f"{s:,}" for s in size_presets],
            index=0,
            key="ds_size_preset",
        )
        if preset == "Custom":
            ds_size = st.number_input(
                "Custom Size",
                min_value=1,
                max_value=100_000,
                value=int(st.session_state["dataset_size"]),
                step=100,
                key="ds_size_input",
            )
        else:
            ds_size = int(preset.replace(",", ""))

    with col_seed:
        use_seed = st.checkbox("Use Seed", value=True, key="ds_use_seed")
        if use_seed:
            ds_seed: int | None = st.number_input(
                "Seed",
                min_value=0,
                value=506,
                step=1,
                key="ds_seed_input",
            )
        else:
            ds_seed = None

    # ---- Generate Button ----
    if st.button("Generate Dataset", type="primary", key="ds_generate"):
        with st.spinner("Generating dataset…"):
            data = generate_dataset_by_type(ds_type, ds_size, seed=ds_seed)
            st.session_state["dataset"] = data
            st.session_state["dataset_type"] = ds_type
            st.session_state["dataset_size"] = ds_size
            # Clear stale results
            st.session_state["sort_results"] = {}
        st.success(
            f"Generated {ds_size:,} elements "
            f"({format_dataset_type_label(ds_type)})"
        )

    # ---- Display ----
    if st.session_state["dataset"] is not None:
        render_dataset_info(
            st.session_state["dataset"],
            st.session_state["dataset_type"],
            st.session_state["dataset_size"],
        )
    else:
        st.info("No dataset generated yet. Click **Generate Dataset** above.")

# ======================================================================
# Tab 3: Sort Playground
# ======================================================================

with tab_playground:
    st.header("Sort Playground")
    st.markdown("Run a single sorting algorithm on the current dataset.")
    st.markdown("""
**Algorithm Property Guide**

- **Stable**: A stable sorting algorithm keeps equal values in the same relative order they appeared in the original dataset.
- **In-Place**: An in-place sorting algorithm organizes the data using very little extra memory beyond the original list.
- **Extra Space**: This shows the additional memory the algorithm typically needs while sorting, such as `O(1)` for constant extra memory or `O(n)` for memory that grows with the dataset size.
    """)

    if st.session_state["dataset"] is None:
        st.warning("⚠️ No dataset available. Go to **Dataset Builder** first.")
    else:
        data = st.session_state["dataset"]
        dataset_type = str(st.session_state["dataset_type"])
        dataset_descriptions: dict[str, str] = {
            "random": (
                "This is an unsorted random dataset, so values appear in no "
                "predictable order."
            ),
            "sorted": (
                "This dataset is already sorted in non-decreasing order."
            ),
            "reverse_sorted": (
                "This dataset is in reverse-sorted order, from largest to smallest."
            ),
            "partially_sorted": (
                "This dataset is mostly sorted, but it includes a small amount "
                "of disorder from swapped values."
            ),
        }

        st.markdown("**Original Dataset:**")
        st.code(preview_dataset(data, count=15))
        st.markdown(
            f"**Dataset Pattern:** {format_dataset_type_label(dataset_type)}  \n"
            f"{dataset_descriptions.get(dataset_type, 'Dataset type description unavailable.')}"
        )

        # ---- Controls ----
        algo_name = st.selectbox(
            "Algorithm",
            options=list(_ALGO_MAP.keys()),
            key="pg_algo_select",
        )

        ds_size = len(data)
        collect_trace = ds_size <= 25

        if not collect_trace:
            st.caption(
                f"Step trace disabled for large datasets "
                f"(n = {ds_size:,} > 25)."
            )

        if st.button("Run Sort", type="primary", key="pg_run"):
            with st.spinner(f"Running {algo_name}…"):
                sort_func = _ALGO_MAP[algo_name]

                # Run once with trace for display
                result = sort_func(data[:], collect_trace=collect_trace)

                # Get stable batched timing estimate
                stable_time = estimate_sort_time(sort_func, data, repeats=3)
                # Replace one-shot time with stable estimate
                result = result.__class__(
                    algorithm=result.algorithm,
                    input_size=result.input_size,
                    sorted_data=result.sorted_data,
                    comparisons=result.comparisons,
                    swaps=result.swaps,
                    writes=result.writes,
                    elapsed_time=stable_time,
                    is_stable=result.is_stable,
                    is_in_place=result.is_in_place,
                    extra_space=result.extra_space,
                    step_trace=result.step_trace,
                )

                st.session_state["sort_results"][algo_name] = result

            st.success(f"{algo_name} completed in {stable_time * 1_000:.4f} ms")

        # ---- Display result ----
        if algo_name in st.session_state["sort_results"]:
            result = st.session_state["sort_results"][algo_name]
            render_sort_result(result)
            render_step_trace(result.step_trace)

# ======================================================================
# Tab 4: Compare Algorithms
# ======================================================================

with tab_compare:
    st.header("Compare Algorithms")
    st.markdown("Run all 4 sorting algorithms on the same dataset.")

    if st.session_state["dataset"] is None:
        st.warning("⚠️ No dataset available. Go to **Dataset Builder** first.")
    else:
        data = st.session_state["dataset"]
        ds_size = len(data)

        if ds_size > 10_000:
            st.warning(
                f"⚠️ Dataset size is {ds_size:,}. O(n²) algorithms may "
                "take a long time. Consider using a smaller dataset."
            )

        if st.button("Compare All", type="primary", key="cmp_run"):
            results: dict[str, object] = {}
            progress = st.progress(0, text="Starting comparison…")

            for idx, (name, func) in enumerate(_ALGO_MAP.items()):
                progress.progress(
                    (idx) / len(_ALGO_MAP),
                    text=f"Running {name}…",
                )
                # Run with trace only for tiny datasets
                collect_trace = ds_size <= 25
                result = func(data[:], collect_trace=collect_trace)

                # Stable timing estimate
                stable_time = estimate_sort_time(func, data, repeats=3)
                result = result.__class__(
                    algorithm=result.algorithm,
                    input_size=result.input_size,
                    sorted_data=result.sorted_data,
                    comparisons=result.comparisons,
                    swaps=result.swaps,
                    writes=result.writes,
                    elapsed_time=stable_time,
                    is_stable=result.is_stable,
                    is_in_place=result.is_in_place,
                    extra_space=result.extra_space,
                    step_trace=result.step_trace,
                )
                results[name] = result

            progress.progress(1.0, text="Comparison complete!")
            st.session_state["sort_results"] = results
            st.success("All 4 algorithms compared successfully!")

        # ---- Display ----
        current_results = st.session_state["sort_results"]
        if len(current_results) == 4:
            render_comparison_grid(current_results)

# ======================================================================
# Tab 5: Benchmark Lab
# ======================================================================

with tab_benchmark:
    st.header("Benchmark Lab")
    st.markdown(
        "Run the full benchmark matrix across multiple dataset types and sizes."
    )

    # ---- Controls ----
    col_bm_types, col_bm_sizes, col_bm_opts = st.columns(3)

    with col_bm_types:
        bm_types = st.multiselect(
            "Dataset Types",
            options=DEFAULT_DATASET_TYPES,
            default=DEFAULT_DATASET_TYPES,
            format_func=format_dataset_type_label,
            key="bm_types",
        )

    with col_bm_sizes:
        bm_sizes = st.multiselect(
            "Sizes",
            options=[500] + DEFAULT_SIZES + [75_000, 100_000],
            default=DEFAULT_SIZES,
            format_func=lambda x: f"{x:,}",
            key="bm_sizes",
        )

    with col_bm_opts:
        bm_repeats = st.number_input(
            "Repeats", min_value=1, max_value=10, value=3, key="bm_repeats",
        )

    # Cost warning
    total_scenarios = len(bm_types) * len(bm_sizes) * 4
    has_large_quadratic = any(s >= 10_000 for s in bm_sizes)
    if has_large_quadratic:
        st.warning(
            f"⚠️ **{total_scenarios} scenarios selected.** "
            "Sizes ≥ 10,000 with O(n²) algorithms may take several minutes. "
            "Consider running the full matrix offline."
        )

    # ---- Run / Load ----
    col_run, col_load = st.columns(2)

    with col_run:
        if st.button(
            "Run Benchmark", type="primary", key="bm_run",
            disabled=not bm_types or not bm_sizes,
        ):
            progress = st.progress(0, text="Starting benchmark…")

            def _progress_cb(current: int, total: int, label: str) -> None:
                progress.progress(
                    current / total,
                    text=f"({current}/{total}) {label}",
                )

            bm_df = run_benchmarks(
                sizes=sorted(bm_sizes),
                dataset_types=bm_types,
                repeats=bm_repeats,
                progress_callback=_progress_cb,
            )
            progress.progress(1.0, text="Benchmark complete!")

            winners_df = compute_scenario_winners(bm_df)
            st.session_state["benchmark_df"] = bm_df
            st.session_state["scenario_winners_df"] = winners_df
            st.success(
                f"Benchmark complete — {len(bm_df)} results, "
                f"{len(winners_df)} scenario winners."
            )

    with col_load:
        csv_path = _PROJECT_ROOT / "analysis" / "benchmark_results.csv"
        if csv_path.exists():
            if st.button("Load Saved Results", key="bm_load"):
                loaded_df = load_results_csv(csv_path)
                loaded_winners = compute_scenario_winners(loaded_df)
                st.session_state["benchmark_df"] = loaded_df
                st.session_state["scenario_winners_df"] = loaded_winners
                st.success(f"Loaded {len(loaded_df)} results from CSV.")

    # ---- Save button ----
    if st.session_state["benchmark_df"] is not None:
        if st.button("Save Results to CSV", key="bm_save"):
            save_path = _PROJECT_ROOT / "analysis" / "benchmark_results.csv"
            save_results_csv(st.session_state["benchmark_df"], save_path)
            st.success(f"Saved to `{save_path.name}`")

    # ---- Display ----
    if st.session_state["benchmark_df"] is not None:
        bm_display_df = st.session_state["benchmark_df"]
        st.divider()
        st.subheader("Results Table")
        render_benchmark_table(bm_display_df)
        st.divider()
        render_benchmark_charts(bm_display_df)
    else:
        st.info(
            "No benchmark data yet. Click **Run Benchmark** or "
            "**Load Saved Results**."
        )

# ======================================================================
# Tab 6: Written Analysis
# ======================================================================

with tab_analysis:
    st.header("Written Analysis")

    bm_df = st.session_state.get("benchmark_df")
    winners_df = st.session_state.get("scenario_winners_df")

    if bm_df is None:
        st.warning(
            "⚠️ No benchmark data available. Please run a benchmark in the "
            "**Benchmark Lab** tab first, or load previously saved results below."
        )
        csv_path = _PROJECT_ROOT / "analysis" / "benchmark_results.csv"
        if csv_path.exists():
            if st.button("Load Saved Results", key="wa_load"):
                loaded_df = load_results_csv(csv_path)
                loaded_winners = compute_scenario_winners(loaded_df)
                st.session_state["benchmark_df"] = loaded_df
                st.session_state["scenario_winners_df"] = loaded_winners
                st.success(f"Loaded {len(loaded_df)} results from CSV.")
                st.rerun()
        else:
            st.info(
                "No saved benchmark CSV found. Go to the **Benchmark Lab** "
                "tab and run a benchmark first."
            )
    else:
        # Build placeholder content from session state
        analysis_placeholders: dict[str, str] = {}

        analysis_placeholders["BENCHMARK_RESULTS_TABLE"] = (
            build_comparison_table(bm_df)
        )
        if winners_df is not None:
            analysis_placeholders["SCENARIO_WINNERS_TABLE"] = (
                build_winner_summary(winners_df)
            )
        # Runtime chart placeholder — point to the PNG
        chart_path = _PROJECT_ROOT / "analysis" / "charts" / "runtime_by_size.png"
        if chart_path.exists():
            analysis_placeholders["RUNTIME_CHART"] = (
                f"![Runtime by Size]({chart_path})"
            )

        render_analysis_markdown_file(
            _PROJECT_ROOT / "analysis" / "written_analysis.md",
            placeholders=analysis_placeholders,
        )

# ======================================================================
# Tab 7: Recommendation Guide
# ======================================================================

with tab_guide:
    st.header("Recommendation Guide")

    guide_placeholders: dict[str, str] = {}

    heatmap_path = (
        _PROJECT_ROOT / "analysis" / "charts" / "scenario_winner_heatmap.png"
    )
    if heatmap_path.exists():
        guide_placeholders["WINNER_HEATMAP"] = (
            f"![Scenario Winner Heatmap]({heatmap_path})"
        )

    render_analysis_markdown_file(
        _PROJECT_ROOT / "analysis" / "recommendation_guide.md",
        placeholders=guide_placeholders,
    )

# __________________________________________________________________________
# End of File
#
