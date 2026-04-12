# -------------------------------------------------------------------------
# File: streamlit_helpers.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Streamlit helper functions for the Sorting Algorithm Comparison Tool.
# Provides reusable UI components: header banners, dataset info panels,
# sort-result metric cards, comparison grids, step-trace expanders,
# benchmark tables, in-app charts, and Markdown template rendering.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit UI helpers for the sorting-algorithm comparison tool."""

# ________________
# Imports
#

from __future__ import annotations

import re
from pathlib import Path

import streamlit as st
import pandas as pd
import altair as alt

from models.sort_result import SortResult
from data.dataset_manager import (
    format_dataset_type_label,
    preview_dataset,
    is_sorted_non_decreasing,
)

# __________________________________________________________________________
# Constants
#

# Consistent algorithm color palette (matches report_generator.py)
ALGO_COLORS: dict[str, str] = {
    "Bubble Sort": "#e74c3c",
    "Selection Sort": "#f39c12",
    "Insertion Sort": "#2ecc71",
    "Merge Sort": "#3498db",
}

# Altair-friendly color scale domain/range
_ALGO_NAMES: list[str] = list(ALGO_COLORS.keys())
_ALGO_HEX: list[str] = list(ALGO_COLORS.values())

# Placeholder regex — lines like {{BENCHMARK_RESULTS_TABLE}}
_PLACEHOLDER_RE = re.compile(r"^\{\{([A-Z0-9_]+)\}\}$")
_IMAGE_MARKDOWN_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)$")

# __________________________________________________________________________
# Header
#

# ========================================================================
# Header
# ========================================================================

# --------------------------------------------------------------- render_header()
def render_header() -> None:
    """Render the application title and course information banner."""
    st.title("Sorting Algorithm Performance Comparison Tool")
    st.caption(
        "CSC506 – Design and Analysis of Algorithms | "
        "Professor Dr. Jonathan Vanover | Spring A 2026 | "
        "Student: Alexander Ricciardi"
    )
    st.divider()
# --------------------------------------------------------------- end render_header()

# __________________________________________________________________________
# Dataset Display
#

# ========================================================================
# Dataset Info
# ========================================================================

# --------------------------------------------------------------- render_dataset_info()
def render_dataset_info(
    data: list[int],
    dataset_type: str,
    size: int,
) -> None:
    """Display dataset metadata, preview, sortedness check, and expandable view.

    Args:
        data: The generated dataset.
        dataset_type: Label for the dataset type.
        size: Number of elements.
    """
    col1, col2, col3 = st.columns(3)
    col1.metric("Dataset Type", format_dataset_type_label(dataset_type))
    col2.metric("Size", f"{size:,}")
    is_sorted = is_sorted_non_decreasing(data)
    col3.metric("Sorted?", "Yes" if is_sorted else "No")

    st.markdown("**Preview:**")
    st.code(preview_dataset(data, count=15))

    with st.expander("View Full Dataset", expanded=False):
        df = pd.DataFrame({"Index": range(len(data)), "Value": data})
        st.dataframe(df, height=300, width="stretch", hide_index=True)
# --------------------------------------------------------------- end render_dataset_info()

# __________________________________________________________________________
# Sort Result Display
#

# ========================================================================
# Sort Result Metrics
# ========================================================================

# --------------------------------------------------------------- render_sort_result()
def render_sort_result(result: SortResult) -> None:
    """Render a SortResult as a metrics card with algorithm properties.

    Args:
        result: The SortResult to display.
    """
    color = ALGO_COLORS.get(result.algorithm, "#888888")
    st.markdown(
        f"### <span style='color:{color}'>{result.algorithm}</span>",
        unsafe_allow_html=True,
    )

    # Metrics row 1 — timing and operations
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Time", f"{result.elapsed_time * 1_000:.4f} ms")
    c2.metric("Comparisons", f"{result.comparisons:,}")
    c3.metric("Swaps", f"{result.swaps:,}")
    c4.metric("Writes", f"{result.writes:,}")

    # Metrics row 2 — algorithm properties
    p1, p2, p3 = st.columns(3)
    p1.metric("Stable", "Yes" if result.is_stable else "No")
    p2.metric("In-Place", "Yes" if result.is_in_place else "No")
    p3.metric("Extra Space", result.extra_space)

    # Sorted output preview
    st.markdown("**Sorted output:**")
    st.code(preview_dataset(result.sorted_data, count=15))
    st.markdown("""
**Operation Metric Guide**

- **Comparisons**: The number of times the algorithm compares two values to decide their order.
- **Swaps**: The number of times two values trade places in the dataset during sorting.
- **Writes**: The number of times the algorithm writes or moves values into list positions while building the sorted result.
    """)
# --------------------------------------------------------------- end render_sort_result()

# ========================================================================
# Comparison Grid
# ========================================================================

# --------------------------------------------------------------- render_comparison_grid()
def render_comparison_grid(results: dict[str, SortResult]) -> None:
    """Render a 2×2 grid of algorithm result cards for side-by-side comparison.

    Args:
        results: Mapping of algorithm name → SortResult.
    """
    items = list(results.items())

    # Row 1: first two algorithms
    if len(items) >= 2:
        col_a, col_b = st.columns(2)
        with col_a:
            render_sort_result(items[0][1])
        with col_b:
            render_sort_result(items[1][1])

    # Row 2: next two algorithms
    if len(items) >= 4:
        col_c, col_d = st.columns(2)
        with col_c:
            render_sort_result(items[2][1])
        with col_d:
            render_sort_result(items[3][1])

    # Quick comparison table
    st.divider()
    st.subheader("Quick Comparison")
    rows = []
    best_time = min(r.elapsed_time for r in results.values())
    for name, r in results.items():
        is_fastest = r.elapsed_time == best_time
        rows.append({
            "Algorithm": f"🏆 {name}" if is_fastest else name,
            "Time (ms)": f"{r.elapsed_time * 1_000:.4f}",
            "Comparisons": f"{r.comparisons:,}",
            "Swaps": f"{r.swaps:,}",
            "Writes": f"{r.writes:,}",
        })
    st.table(pd.DataFrame(rows))
# --------------------------------------------------------------- end render_comparison_grid()

# __________________________________________________________________________
# Step Trace
#

# ========================================================================
# Step Trace
# ========================================================================

# --------------------------------------------------------------- render_step_trace()
def render_step_trace(trace: list[str]) -> None:
    """Render a step trace inside a collapsible expander.

    Hidden entirely if the trace is empty.

    Args:
        trace: Human-readable walkthrough strings.
    """
    if not trace:
        return
    with st.expander(f"Step Trace ({len(trace)} steps)", expanded=False):
        for step in trace:
            st.text(step)
# --------------------------------------------------------------- end render_step_trace()

# __________________________________________________________________________
# Benchmark Table & Charts
#

# ========================================================================
# Benchmark Table
# ========================================================================

# --------------------------------------------------------------- render_benchmark_table()
def render_benchmark_table(df: pd.DataFrame) -> None:
    """Render benchmark results as a formatted, scrollable table.

    Args:
        df: Benchmark results DataFrame with columns ``algorithm``,
            ``dataset_type``, ``size``, ``time_ms``, ``comparisons``,
            ``swaps``, ``writes``, ``is_correct``.
    """
    display = df.copy()
    display["dataset_type"] = display["dataset_type"].apply(
        format_dataset_type_label
    )
    display.columns = [
        "Algorithm", "Dataset Type", "Size", "Time (ms)",
        "Comparisons", "Swaps", "Writes", "Correct",
    ]
    # Format numeric columns for readability
    display["Size"] = display["Size"].apply(lambda x: f"{x:,}")
    display["Time (ms)"] = display["Time (ms)"].apply(lambda x: f"{x:.2f}")
    display["Comparisons"] = display["Comparisons"].apply(lambda x: f"{x:,}")
    display["Swaps"] = display["Swaps"].apply(lambda x: f"{x:,}")
    display["Writes"] = display["Writes"].apply(lambda x: f"{x:,}")
    display["Correct"] = display["Correct"].apply(
        lambda x: "✅" if x else "❌"
    )
    st.dataframe(display, width="stretch", hide_index=True, height=500)
# --------------------------------------------------------------- end render_benchmark_table()

# ========================================================================
# Benchmark Charts
# ========================================================================

# --------------------------------------------------------------- render_benchmark_charts()
def render_benchmark_charts(df: pd.DataFrame) -> None:
    """Render interactive Altair charts from benchmark results.

    Displays a line chart (runtime vs size) and a grouped bar chart
    (runtime by dataset type).

    Args:
        df: Benchmark results DataFrame.
    """
    display_df = df.copy()
    display_df["dataset_type"] = display_df["dataset_type"].apply(
        format_dataset_type_label
    )
    color_scale = alt.Scale(domain=_ALGO_NAMES, range=_ALGO_HEX)

    # ---- Chart 1: Runtime by Dataset Size (line chart, faceted) ----
    st.subheader("Runtime by Dataset Size")
    line = (
        alt.Chart(display_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("size:Q", title="Dataset Size"),
            y=alt.Y("time_ms:Q", title="Time (ms)"),
            color=alt.Color(
                "algorithm:N", title="Algorithm",
                scale=color_scale,
            ),
        )
        .properties(height=300)
        .facet(
            facet=alt.Facet("dataset_type:N", title="Dataset Type"),
        )
        .properties(columns=2)
    )
    st.altair_chart(line, width="stretch")
    st.caption(
        "Each panel shows runtime scaling for one dataset type. "
        "O(n²) algorithms exhibit steep growth; Merge Sort stays nearly flat."
    )

    # ---- Chart 2: Runtime by Dataset Type (grouped bar) ----
    st.subheader("Runtime by Dataset Type")
    bar = (
        alt.Chart(display_df)
        .mark_bar()
        .encode(
            x=alt.X("dataset_type:N", title="Dataset Type",
                     axis=alt.Axis(labelAngle=0)),
            y=alt.Y("time_ms:Q", title="Time (ms)"),
            color=alt.Color(
                "algorithm:N", title="Algorithm",
                scale=color_scale,
            ),
            xOffset="algorithm:N",
        )
        .properties(height=300)
        .facet(
            facet=alt.Facet("size:N", title="Size"),
        )
        .properties(columns=2)
    )
    st.altair_chart(bar, width="stretch")
    st.caption(
        "Grouped bars compare all four algorithms within each dataset type, "
        "faceted by dataset size."
    )
# --------------------------------------------------------------- end render_benchmark_charts()

# __________________________________________________________________________
# Markdown Template Rendering
#

# ========================================================================
# Analysis Markdown
# ========================================================================

# --------------------------------------------------------------- render_analysis_markdown_file()
def render_analysis_markdown_file(
    path: Path,
    placeholders: dict[str, str] | None = None,
) -> None:
    """Read a Markdown file, replace ``{{PLACEHOLDER}}`` tokens, and render.

    Placeholders are replaced with the corresponding value from the
    *placeholders* dict. If a placeholder is not found, a warning is shown.

    Args:
        path: Path to the Markdown file.
        placeholders: Mapping of placeholder name (without braces) → content.
    """
    if not path.exists():
        st.error(f"File not found: {path}")
        return

    text = path.read_text(encoding="utf-8")

    if placeholders is None:
        placeholders = {}

    md_buffer: list[str] = []

    def render_content(content: str) -> None:
        """Render markdown content, promoting local image lines to st.image()."""
        image_match = _IMAGE_MARKDOWN_RE.fullmatch(content.strip())
        if image_match:
            alt_text, image_target = image_match.groups()
            image_path = Path(image_target)
            if image_path.exists():
                st.image(str(image_path), caption=alt_text or None)
                return
        st.markdown(content)

    def flush() -> None:
        """Emit any accumulated markdown lines as one block."""
        if md_buffer:
            render_content("\n".join(md_buffer))
            md_buffer.clear()

    for line in text.splitlines():
        match = _PLACEHOLDER_RE.fullmatch(line.strip())
        if match:
            flush()
            key = match.group(1)
            if key in placeholders:
                render_content(placeholders[key])
            else:
                st.info(f"Placeholder `{key}` — data not yet available. "
                        "Run a benchmark to populate.")
        else:
            md_buffer.append(line)

    flush()
# --------------------------------------------------------------- end render_analysis_markdown_file()

# __________________________________________________________________________
# End of File
#
