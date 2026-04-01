# -------------------------------------------------------------------------
# File: streamlit_helpers.py
# Author: Alexander Ricciardi
# Date: 2026-03-29
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Streamlit rendering helpers for the Algorithm Comparison Tool.
# The functions are used for common UI patterns (headers, result cards,
# comparison columns, dataset info, benchmark charts).
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit UI helpers for the search-algorithm UI."""

# ________________
# Imports
#

from __future__ import annotations

from pathlib import Path
import math

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import streamlit as st
import pandas as pd
import altair as alt

import sys
import os
# SETUP: add project root so sibling packages are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.search_result import SearchResult

# __________________________________________________________________________
# Helper Functions
#

ANALYSIS_PLACEHOLDER_PATTERN: str = r"^\{\{([A-Z0-9_]+)\}\}$"

# ========================================================================
# Header
# ========================================================================

# --------------------------------------------------------------- render_header()
def render_header() -> None:
    """Render the application title and course information banner."""
    st.title("Algorithm Comparison Tool")
    st.caption(
        "CSC506 – Design and Analysis of Algorithms | "
        "Professor Dr. Jonathan Vanover | Spring A 2026 | "
        "Student: Alexander Ricciardi"
    )
    st.divider()
# --------------------------------------------------------------- end render_header()

# ========================================================================
# Search Result Display
# ========================================================================

# --------------------------------------------------------------- render_search_result()
def render_search_result(
    result: SearchResult,
    show_explanation: bool = True,
) -> None:
    """Render a single SearchResult as Streamlit metrics and step trace.

    Args:
        result: The SearchResult to display.
        show_explanation: If True, show a Big-O explanation box below
            the step trace (default True).
    """
    st.subheader(result.algorithm)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Found", "Yes" if result.found else "No")
    col2.metric("Index", str(result.index) if result.index is not None else "—")
    col3.metric("Comparisons", f"{result.comparisons:,}")
    col4.metric("Time", f"{result.elapsed_time * 1_000:.4f} ms")

    # Step trace (collapsible)
    if result.step_trace:
        with st.expander("Step Trace", expanded=False):
            for step in result.step_trace:
                st.text(step)

    # Algorithm explanation with Big-O (only in Search Playground)
    if show_explanation:
        if "linear" in result.algorithm.lower():
            st.info(
                "**How Linear Search works — O(n)**\n\n"
                "Scans the list sequentially from index 0 to the end. Each element "
                "is compared to the target one by one. In the **worst case** (target "
                "not found), every element is examined, giving **O(n)** time "
                "complexity. In the **best case** (target at index 0), it finishes "
                "in **O(1)**."
            )
        else:
            st.info(
                "**How Binary Search works — O(log n)**\n\n"
                "Requires a **sorted** list. Computes the midpoint and compares it "
                "to the target: if the target is smaller, the upper half is "
                "discarded; if larger, the lower half is discarded. Each step "
                "**halves** the search space, giving **O(log n)** time complexity "
                "in the worst case. The **best case** is **O(1)** when the target "
                "value is already at the midpoint of the dataset."
            )
# --------------------------------------------------------------- end render_search_result()

# ========================================================================
# Side-by-Side Comparison
# ========================================================================

# --------------------------------------------------------------- render_comparison()
def render_comparison(
    linear: SearchResult,
    binary: SearchResult,
    show_explanation: bool = False,
) -> None:
    """Render linear and binary search results in side-by-side columns.

    Args:
        linear: SearchResult from linear search.
        binary: SearchResult from binary search.
        show_explanation: If True, show Big-O explanation in each column
            (default False — Compare tab omits it).
    """
    left, right = st.columns(2)

    with left:
        render_search_result(linear, show_explanation=show_explanation)

    with right:
        render_search_result(binary, show_explanation=show_explanation)
# --------------------------------------------------------------- end render_comparison()

# ========================================================================
# Dataset Info
# ========================================================================

# --------------------------------------------------------------- _render_expandable_list()
def _render_expandable_list(
    data: list[int],
    label: str,
    preview_count: int = 15,
    expander_key: str = "",
) -> None:
    """Show a short preview and an expandable scrollable view of *data*.

    Args:
        data: The integer list to display.
        label: Column label (e.g. "Original order").
        preview_count: How many leading elements to show inline.
        expander_key: Unique suffix to avoid duplicate widget IDs.
    """
    from data.dataset_manager import preview

    st.markdown(f"**{label}**")
    st.code(preview(data, preview_count))

    with st.expander("View Full Dataset", expanded=False):
        df = pd.DataFrame({"Index": range(len(data)), "Value": data})
        st.dataframe(df, height=300, use_container_width=True, hide_index=True)
# --------------------------------------------------------------- end _render_expandable_list()

# --------------------------------------------------------------- render_dataset_info()
def render_dataset_info(data: list[int], sorted_data: list[int]) -> None:
    """Display dataset size and expandable previews (original and sorted).

    Args:
        data: The original (possibly unsorted) dataset.
        sorted_data: The sorted copy.
    """
    st.markdown(f"**Dataset size:** {len(data):,} element(s)")

    col1, col2 = st.columns(2)
    with col1:
        _render_expandable_list(data, "Original order", expander_key="orig")
    with col2:
        _render_expandable_list(sorted_data, "Sorted order", expander_key="sort")
# --------------------------------------------------------------- end render_dataset_info()

# --------------------------------------------------------------- render_dataset_scrollable()
def render_dataset_scrollable(data: list[int], label: str = "Sorted dataset") -> None:
    """Show dataset size, preview, and expandable scrollable full view.

    Intended for the Search Playground and Compare Algorithms tabs where
    only one dataset column (sorted) is shown.

    Args:
        data: The dataset to display.
        label: Display label (default "Sorted dataset").
    """
    st.markdown(f"**{label}** ({len(data):,} elements)")
    _render_expandable_list(data, "", expander_key=label)
# --------------------------------------------------------------- end render_dataset_scrollable()

# ========================================================================
# Benchmark Charts
# ========================================================================

# --------------------------------------------------------------- render_benchmark_charts()
def render_benchmark_charts(df: pd.DataFrame) -> None:
    """Render benchmark results as a table and line chart.

    Args:
        df: DataFrame with columns ``size``, ``linear_time_ms``,
            ``binary_time_ms``, ``linear_comparisons``,
            ``binary_comparisons``.
    """
    # Results table
    st.subheader("Results Table")
    display_df = df.copy()
    display_df.columns = [
        "Dataset Size",
        "Linear Time (ms)",
        "Binary Time (ms)",
        "Linear Comparisons",
        "Binary Comparisons",
    ]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(
        "Note: This table shows the median execution time (in milliseconds) and total "
        "comparison count for each algorithm at every dataset size. Times are the median "
        "of multiple runs to reduce measurement noise. Comparisons reflect worst-case "
        "behavior (target not in dataset)."
    )

    # Execution-time line chart
    st.subheader("Execution Time vs. Dataset Size")
    chart_df = df[["size", "linear_time_ms", "binary_time_ms"]].copy()
    chart_df = chart_df.rename(columns={
        "size": "Dataset Size",
        "linear_time_ms": "Linear Search",
        "binary_time_ms": "Binary Search",
    })
    time_long = chart_df.melt(
        id_vars="Dataset Size",
        var_name="Algorithm",
        value_name="Time (ms)",
    )
    time_chart = (
        alt.Chart(time_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("Dataset Size:Q", title="Dataset Size"),
            y=alt.Y("Time (ms):Q", title="Execution Time (ms)"),
            color=alt.Color("Algorithm:N", title="Algorithm"),
        )
        .properties(height=400)
    )
    st.altair_chart(time_chart, use_container_width=True)
    st.caption(
        "Note: This line chart plots median execution time against dataset size for both "
        "algorithms. Linear search time grows proportionally with n, O(n), producing a "
        "steep upward slope, while binary search time remains nearly flat, O(log n)."
    )

    # Comparisons bar chart (log scale so binary search bars are visible)
    st.subheader("Comparisons vs. Dataset Size")
    comp_df = df[["size", "linear_comparisons", "binary_comparisons"]].copy()
    comp_df = comp_df.rename(columns={
        "size": "Dataset Size",
        "linear_comparisons": "Linear Search",
        "binary_comparisons": "Binary Search",
    })
    # Melt to long format for Altair grouped bar chart
    comp_long = comp_df.melt(
        id_vars="Dataset Size",
        var_name="Algorithm",
        value_name="Comparisons",
    )
    # SETUP: convert to native types for reliable Altair serialisation
    size_order = [str(s) for s in sorted(comp_df["Dataset Size"].unique())]
    comp_long["Dataset Size"] = comp_long["Dataset Size"].astype(str)
    comp_long["Comparisons"] = comp_long["Comparisons"].astype(float)

    bar = (
        alt.Chart(comp_long)
        .mark_bar()
        .encode(
            x=alt.X("Dataset Size:N", title="Dataset Size",
                     sort=size_order,
                     axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Comparisons:Q", title="Comparisons (log scale)",
                     scale=alt.Scale(type="log"),
                     axis=alt.Axis(values=[1, 10, 100, 1_000, 10_000, 100_000])),
            y2=alt.datum(1),
            color=alt.Color("Algorithm:N", title="Algorithm"),
            xOffset=alt.XOffset("Algorithm:N"),
        )
        .properties(height=400)
    )
    st.altair_chart(bar, use_container_width=True)
    st.caption(
        "Note: This bar chart uses a logarithmic scale to compare the number of element "
        "comparisons each algorithm performed at each dataset size. Linear search compares "
        "every element (n), while "
        "binary search needs only about log2(n) comparisons, illustrating the "
        "fundamental efficiency difference. The log scale makes both algorithms visible "
        "despite the large difference in magnitude."
    )
# --------------------------------------------------------------- end render_benchmark_charts()

# ========================================================================
# Analysis Markdown Rendering
# ========================================================================

# --------------------------------------------------------------- render_analysis_markdown_file()
def render_analysis_markdown_file(
    path: Path,
    benchmark_df: pd.DataFrame | None = None,
) -> None:
    """Render a markdown analysis file with inline visual placeholders.

    Supported placeholders are written on their own line as
    ``{{PLACEHOLDER_NAME}}`` within the markdown file.

    Args:
        path: The markdown file to render.
        benchmark_df: Optional benchmark results DataFrame used by the
            analysis visuals.
    """
    if not path.exists():
        st.error(f"File not found: {path}")
        return

    text = path.read_text(encoding="utf-8")
    render_analysis_markdown_text(text, benchmark_df=benchmark_df)
# --------------------------------------------------------------- end render_analysis_markdown_file()

# --------------------------------------------------------------- render_analysis_markdown_text()
def render_analysis_markdown_text(
    text: str,
    benchmark_df: pd.DataFrame | None = None,
) -> None:
    """Render markdown text and replace placeholder lines with visuals.

    Args:
        text: Markdown source text.
        benchmark_df: Optional benchmark results DataFrame used by the
            analysis visuals.
    """
    import re

    markdown_lines: list[str] = []

    def flush_markdown_block() -> None:
        """Render any accumulated markdown lines as one block."""
        if markdown_lines:
            st.markdown("\n".join(markdown_lines).strip())
            markdown_lines.clear()

    for line in text.splitlines():
        match = re.fullmatch(ANALYSIS_PLACEHOLDER_PATTERN, line.strip())
        if match:
            flush_markdown_block()
            _render_analysis_placeholder(match.group(1), benchmark_df)
        else:
            markdown_lines.append(line)

    flush_markdown_block()
# --------------------------------------------------------------- end render_analysis_markdown_text()

# --------------------------------------------------------------- _render_analysis_placeholder()
def _render_analysis_placeholder(
    placeholder_name: str,
    benchmark_df: pd.DataFrame | None,
) -> None:
    """Render a supported analysis placeholder.

    Args:
        placeholder_name: Placeholder identifier without braces.
        benchmark_df: Optional benchmark results DataFrame.
    """
    if placeholder_name == "BENCHMARK_RESULTS_DATAFRAME":
        _render_benchmark_results_dataframe(benchmark_df)
    elif placeholder_name == "BENCHMARK_RESULTS_SUMMARY":
        _render_benchmark_results_summary(benchmark_df)
    elif placeholder_name == "BENCHMARK_TIME_CHART":
        _render_benchmark_time_chart(benchmark_df)
    elif placeholder_name == "BIG_O_COMPARISON_DIAGRAM":
        _render_big_o_comparison_diagram(benchmark_df)
    elif placeholder_name == "RECOMMENDATION_DECISION_DIAGRAM":
        _render_recommendation_decision_diagram()
    else:
        st.warning(f"Unsupported analysis placeholder: {placeholder_name}")
# --------------------------------------------------------------- end _render_analysis_placeholder()

# --------------------------------------------------------------- _render_benchmark_results_dataframe()
def _render_benchmark_results_dataframe(
    benchmark_df: pd.DataFrame | None,
) -> None:
    """Render the benchmark results as a pandas-backed DataFrame.

    Args:
        benchmark_df: Optional benchmark results DataFrame.
    """
    if benchmark_df is None or benchmark_df.empty:
        return

    display_df = benchmark_df.copy()
    display_df.columns = [
        "Dataset Size",
        "Linear Time (ms)",
        "Binary Time (ms)",
        "Linear Comparisons",
        "Binary Comparisons",
    ]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
# --------------------------------------------------------------- end _render_benchmark_results_dataframe()

# --------------------------------------------------------------- _render_benchmark_results_summary()
def _render_benchmark_results_summary(
    benchmark_df: pd.DataFrame | None,
) -> None:
    """Render a dynamic text summary of benchmark comparison counts.

    Args:
        benchmark_df: Optional benchmark results DataFrame.
    """
    if benchmark_df is None or benchmark_df.empty:
        return

    parts: list[str] = []
    for _, row in benchmark_df.iterrows():
        size = int(row["size"])
        lin = int(row["linear_comparisons"])
        bsn = int(row["binary_comparisons"])
        parts.append(
            f"At `n = {size:,}`, linear search used {lin:,} comparisons "
            f"while binary search used {bsn:,}"
        )

    summary = (
        "The benchmark results show that the difference between the two "
        "algorithms is significant. "
        + ". ".join(parts)
        + ". These results match the theoretical expectations of "
        "`O(n)` and `O(log n)`."
    )
    st.markdown(summary)
# --------------------------------------------------------------- end _render_benchmark_results_summary()

# --------------------------------------------------------------- _render_benchmark_time_chart()
def _render_benchmark_time_chart(
    benchmark_df: pd.DataFrame | None,
) -> None:
    """Render a Matplotlib timing chart from the benchmark results.

    Args:
        benchmark_df: Optional benchmark results DataFrame.
    """
    if benchmark_df is None or benchmark_df.empty:
        return

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(
        benchmark_df["size"],
        benchmark_df["linear_time_ms"],
        marker="o",
        linewidth=2.2,
        color="#C0392B",
        label="Linear Search",
    )
    ax.plot(
        benchmark_df["size"],
        benchmark_df["binary_time_ms"],
        marker="o",
        linewidth=2.2,
        color="#1F618D",
        label="Binary Search",
    )
    ax.set_title("Benchmark Runtime Comparison")
    ax.set_xlabel("Dataset Size (n)")
    ax.set_ylabel("Median Time (ms)")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
# --------------------------------------------------------------- end _render_benchmark_time_chart()

# --------------------------------------------------------------- _render_big_o_comparison_diagram()
def _render_big_o_comparison_diagram(
    benchmark_df: pd.DataFrame | None,
) -> None:
    """Render a conceptual Big O comparison diagram with Matplotlib.

    Args:
        benchmark_df: Optional benchmark results DataFrame used to choose
            sample input sizes.
    """
    if benchmark_df is None or benchmark_df.empty:
        return

    sizes = benchmark_df["size"].tolist()

    linear_values = sizes
    binary_values = [math.ceil(math.log2(size)) for size in sizes]

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(
        sizes,
        linear_values,
        marker="o",
        linewidth=2.4,
        color="#C0392B",
        label="Linear Search: O(n)",
    )
    ax.plot(
        sizes,
        binary_values,
        marker="s",
        linewidth=2.4,
        color="#117A65",
        label="Binary Search: O(log n)",
    )
    ax.set_title("Growth Pattern Diagram: O(n) vs. O(log n)")
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Relative Comparison Growth")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax.annotate(
        "Linear growth rises directly\nwith dataset size.",
        xy=(sizes[-1], linear_values[-1]),
        xytext=(sizes[-2], linear_values[-1] * 0.65),
        arrowprops={"arrowstyle": "->", "color": "#C0392B"},
        color="#922B21",
    )
    ax.annotate(
        "Logarithmic growth increases slowly\nbecause each step halves the range.",
        xy=(sizes[-1], binary_values[-1]),
        xytext=(sizes[-1] * 0.55, linear_values[-1] * 0.12),
        arrowprops={"arrowstyle": "->", "color": "#117A65"},
        color="#0B5345",
        bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "#117A65", "alpha": 0.9},
    )
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption(
        "Conceptual growth diagram comparing the relative comparison counts of "
        "linear and binary search across increasing input sizes."
    )
# --------------------------------------------------------------- end _render_big_o_comparison_diagram()

# --------------------------------------------------------------- _render_recommendation_decision_diagram()
def _render_recommendation_decision_diagram() -> None:
    """Render the recommendation decision diagram with Matplotlib."""
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(0.5, 10.5)
    ax.axis("off")

    # ---- Layout constants ----
    # Row y-positions (top → bottom) with generous spacing
    y_top = 9.0
    y_mid = 6.0
    y_bot = 2.8

    # Column x-positions — symmetric around center (6.0)
    cx = 6.0
    x_root = cx
    x_left_mid = 3.0
    x_right_mid = 9.0
    x_ll = 1.5    # left-left leaf
    x_lr = 4.5    # left-right leaf
    x_rl = 7.5    # right-left leaf
    x_rr = 10.5   # right-right leaf

    # Node dimensions — compact to avoid overlaps
    node_h = 0.85

    # Step 1: draw nodes
    nodes = [
        # (x, y), width, height, label, bg_color
        ((x_root, y_top), 2.4, node_h,
         "Is the data sorted?", "#EAF2F8"),
        ((x_left_mid, y_mid), 2.0, node_h,
         "Is n > ~100?", "#E8F8F5"),
        ((x_right_mid, y_mid), 2.6, node_h * 1.15,
         "Will you search\nmore than a few times?", "#FEF9E7"),
        ((x_ll, y_bot), 2.0, node_h,
         "Binary Search", "#D4EFDF"),
        ((x_lr, y_bot), 2.0, node_h,
         "Either is fine", "#FDEDEC"),
        ((x_rl, y_bot), 2.2, node_h * 1.15,
         "Sort first, then\nBinary Search", "#FCF3CF"),
        ((x_rr, y_bot), 2.0, node_h,
         "Linear Search", "#FADBD8"),
    ]

    for (x, y), width, height, label, color in nodes:
        box = FancyBboxPatch(
            (x - width / 2, y - height / 2),
            width,
            height,
            boxstyle="round,pad=0.18",
            linewidth=1.4,
            edgecolor="#34495E",
            facecolor=color,
        )
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=10)

    # Step 2: connect decision paths
    arrow_style = {
        "arrowstyle": "->",
        "linewidth": 1.5,
        "color": "#34495E",
    }
    
    # Calculate exact vertical edge offsets considering box height and pad
    pad = 0.18
    edge_normal = node_h / 2 + pad
    edge_large = (node_h * 1.15) / 2 + pad

    # Root → mid-level
    ax.annotate("", xy=(x_left_mid, y_mid + edge_normal),
                xytext=(x_root - 0.7, y_top - edge_normal), arrowprops=arrow_style, zorder=1)
    ax.annotate("", xy=(x_right_mid, y_mid + edge_large),
                xytext=(x_root + 0.7, y_top - edge_normal), arrowprops=arrow_style, zorder=1)
    # Left mid → leaves
    ax.annotate("", xy=(x_ll, y_bot + edge_normal),
                xytext=(x_left_mid - 0.5, y_mid - edge_normal), arrowprops=arrow_style, zorder=1)
    ax.annotate("", xy=(x_lr, y_bot + edge_normal),
                xytext=(x_left_mid + 0.5, y_mid - edge_normal), arrowprops=arrow_style, zorder=1)
    # Right mid → leaves
    ax.annotate("", xy=(x_rl, y_bot + edge_large),
                xytext=(x_right_mid - 0.5, y_mid - edge_large), arrowprops=arrow_style, zorder=1)
    ax.annotate("", xy=(x_rr, y_bot + edge_normal),
                xytext=(x_right_mid + 0.5, y_mid - edge_large), arrowprops=arrow_style, zorder=1)

    # Step 3: label the branches
    # Background box to make text readable over arrows
    label_bg = {"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.85}
    text_kwargs = {"fontsize": 10, "fontweight": "bold", "ha": "center", "va": "center", "bbox": label_bg, "zorder": 3}

    # Position text exactly at the midpoints of the arrows
    ax.text((x_root - 0.7 + x_left_mid) / 2, (y_top - edge_normal + y_mid + edge_normal) / 2, 
            "Yes", color="#1B4F72", **text_kwargs)
    ax.text((x_root + 0.7 + x_right_mid) / 2, (y_top - edge_normal + y_mid + edge_large) / 2, 
            "No", color="#7D6608", **text_kwargs)
    
    ax.text((x_left_mid - 0.5 + x_ll) / 2, (y_mid - edge_normal + y_bot + edge_normal) / 2, 
            "Yes", color="#117864", **text_kwargs)
    ax.text((x_left_mid + 0.5 + x_lr) / 2, (y_mid - edge_normal + y_bot + edge_normal) / 2, 
            "No", color="#922B21", **text_kwargs)
            
    ax.text((x_right_mid - 0.5 + x_rl) / 2, (y_mid - edge_large + y_bot + edge_large) / 2, 
            "Yes", color="#7D6608", **text_kwargs)
    ax.text((x_right_mid + 0.5 + x_rr) / 2, (y_mid - edge_large + y_bot + edge_normal) / 2, 
            "No", color="#922B21", **text_kwargs)

    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption(
        "Decision diagram for choosing between linear search and binary search based on "
        "sorting, dataset size, and search frequency."
    )
# --------------------------------------------------------------- end _render_recommendation_decision_diagram()

# __________________________________________________________________________
# End of File
#
