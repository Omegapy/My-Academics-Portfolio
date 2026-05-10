# -------------------------------------------------------------------------
# File: streamlit_helpers.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-21
# File Path: Portfolio-Milestone-Module-6/ui/streamlit_helpers.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Centralize repeated Streamlit layout, table, chart, and markdown helpers.
# - Render balance, benchmark, guided-result, and analysis-document sections.
# - Keep UI formatting rules consistent across all Module 6 tabs.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Global Constants / Variables: placeholder and image-parsing rules.
# - Function Definitions: shared headers, panels, and lab display helpers.
# - Function Definitions: guided result renderers and benchmark displays.
# - Function Definitions: Markdown analysis rendering with placeholder support.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: re, pathlib
# - Third-Party: altair (optional), pandas, streamlit
# - Local Project Modules:
#   - analysis.report_generator
#   - models.balance_report
#   - models.lab_operation_result
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by ``streamlit_app.py`` to keep tab rendering consistent.
# - Handles both live benchmark rendering and saved analysis-document display.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit UI helper functions."""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations
import re
from pathlib import Path
try:
    import altair as alt
except ImportError:  # pragma: no cover - optional dependency path
    alt = None
import pandas as pd
import streamlit as st
# Analysis imports
from analysis.report_generator import (
    CHART_FILENAMES,
    build_balance_summary_table,
    build_benchmark_table,
    build_speedup_summary_table,
)
# Model imports
from models.balance_report import BalanceReport
from models.lab_operation_result import LabOperationResult


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# MARKDOWN / IMAGE PARSING RULES
# ========================================================================
# These regular expressions define the tiny markdown subset that receives
# special handling when analysis documents are rendered inside Streamlit.
#
# Constraint: only full-line ``{{TOKEN}}`` placeholders trigger substitution.
# Rationale: partial brace text should keep rendering as ordinary markdown.
_PLACEHOLDER_RE = re.compile(r"^\{\{([A-Z0-9_]+)\}\}$")
# Constraint: only standalone markdown image lines are promoted to ``st.image()``.
# Rationale: inline image syntax should stay under normal markdown rendering.
_IMAGE_MARKDOWN_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)$")
"""Detect markdown image lines that should render through ``st.image()``."""


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# HEADER / PANEL RENDERERS
# ========================================================================
# These helpers keep repeated Streamlit layout patterns visually consistent
# across the dataset, BST, map, benchmark, and analysis tabs.
#
# --------------------------------------------------------------- render_header()
def render_header() -> None:
    """Render the page title and course banner.

    Logic:
        This helper draws the shared page header used across the app.
        1. Render the main application title.
        2. Render the course and student caption line.
        3. Separate the header from later content with a divider.
    """
    st.title("Algorithm and Data Structure Comparison Tool")
    st.caption(
        "CSC506 – Design and Analysis of Algorithms | "
        "Professor: Dr. Jonathan Vanover | Spring A 2026 | "
        "Student: Alexander Ricciardi"
    )
    st.divider()
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_section_intro()
def render_section_intro(title: str, body: str) -> None:
    """Render a standard section title and description.

    Logic:
        This helper keeps section introductions visually consistent.
        1. Render the provided title as a Streamlit subheader.
        2. Render the accompanying body text as Markdown.
    """
    st.subheader(title)
    st.markdown(body)
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_lab_quick_start()
def render_lab_quick_start(title: str, steps: list[str]) -> None:
    """Render a short boxed quick-start checklist.

    Logic:
        This helper packages a short instructional checklist into one bordered
        panel.
        1. Open a bordered container and render the checklist title.
        2. Walk the provided steps in order.
        3. Render each step as a numbered Markdown line.
    """
    with st.container(border=True):
        st.markdown(f"**{title}**")
        # MAIN ITERATION LOOP: render each quick-start step as a numbered markdown line.
        for index, step in enumerate(steps, start=1):
            st.markdown(f"{index}. {step}")
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_dataset_info()
def render_dataset_info(
    keys: list[object],
    dataset_type: str,
    insertion_pattern: str,
) -> None:
    """Render dataset metadata and a compact preview.

    Logic:
        This helper summarizes the current dataset selection in one compact UI
        block.
        1. Render the dataset type, insertion pattern, and size as metrics.
        2. Render a preview label for the current key list.
        3. Show a compact preview of the dataset contents.
    """
    col1, col2, col3 = st.columns(3)
    col1.metric("Dataset Type", dataset_type.title())
    col2.metric("Insertion Pattern", insertion_pattern.replace("_", " ").title())
    col3.metric("Size", len(keys))

    st.markdown("**Dataset Preview**")
    st.code(str(keys[:12]) if len(keys) <= 12 else f"{keys[:6]} ... {keys[-6:]}")
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_tree_state_panel()
def render_tree_state_panel(
    *,
    name: str,
    size: int,
    height: int,
    balanced: bool,
    min_key: object | None,
    max_key: object | None,
) -> None:
    """Render a compact row of tree-state metrics.

    Logic:
        This helper summarizes one structure's current tree state in a single
        metric row.
        1. Render the panel heading for the named structure.
        2. Create a five-column metric layout.
        3. Populate the size, height, balance, minimum, and maximum metrics.
    """
    st.markdown(f"**{name} State**")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Size", size)
    col2.metric("Height", height)
    col3.metric("Balanced", "Yes" if balanced else "No")
    col4.metric("Min", min_key if min_key is not None else "None")
    col5.metric("Max", max_key if max_key is not None else "None")
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_tree_ascii_diagram()
def render_tree_ascii_diagram(ascii_text: str, *, title: str = "Tree Diagram") -> None:
    """Render an ASCII tree diagram.

    Logic:
        This helper displays the current tree shape as monospace text.
        1. Render the diagram title.
        2. Render the provided ASCII text or the empty-tree placeholder.
    """
    st.markdown(f"**{title}**")
    st.code(ascii_text or "(empty tree)")
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_balance_summary()
def render_balance_summary(balance_reports: list[BalanceReport]) -> None:
    """Render a balance summary table or an empty-state message.

    Logic:
        This helper converts node-level balance rows into a display table.
        1. Render the balance summary heading.
        2. Show an empty-state message when no rows exist.
        3. Convert the report rows into a DataFrame and display it.
    """
    st.markdown("**Balance Summary**")
    if not balance_reports:
        st.info("No balance-report rows available yet.")
        return

    # Step 1: normalize the dataclass rows into a display-friendly DataFrame.
    # Display-facing column names translated from the node-level report fields.
    report_df = pd.DataFrame(
        {
            "Key": [report.node_key for report in balance_reports],  # Node being analyzed
            "Left Height": [
                report.left_height for report in balance_reports
            ],  # Left subtree height
            "Right Height": [
                report.right_height for report in balance_reports
            ],  # Right subtree height
            "Balance Factor": [report.balance_factor for report in balance_reports],  # Height delta
            "Unbalanced": [
                report.is_unbalanced for report in balance_reports
            ],  # Rule violation flag
        }
    )
    st.dataframe(report_df, width="stretch", hide_index=True)
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_traversal_outputs()
def render_traversal_outputs(
    inorder: list[object],
    preorder: list[object],
    postorder: list[object],
) -> None:
    """Render the three traversal outputs.

    Logic:
        This helper presents the three traversal orders side by side.
        1. Render the traversal section heading.
        2. Create a three-column layout.
        3. Display the in-order, pre-order, and post-order outputs.
    """
    st.markdown("**Traversal Outputs**")
    col1, col2, col3 = st.columns(3)
    col1.markdown("`inorder`")
    col1.code(str(inorder))
    col2.markdown("`preorder`")
    col2.code(str(preorder))
    col3.markdown("`postorder`")
    col3.code(str(postorder))
# --------------------------------------------------------------- 

# --------------------------------------------------------------- render_manual_operation_result()
def render_manual_operation_result(result: LabOperationResult | None) -> None:
    """Render one operation result card for a manual action.

    Logic:
        1. Show an empty-state message until an operation result exists.
        2. Render the operation summary and before/after metrics in a bordered container.
        3. Display returned values and ASCII snapshots when present.
    """
    # VALIDATION: show a placeholder message until the user runs an action.
    if result is None:
        st.info("No manual operation has been run yet.")
        return

    with st.container(border=True):
        st.markdown(f"**{result.section} - {result.operation}**")
        st.markdown(result.message)
        col1, col2, col3 = st.columns(3)
        col1.metric("Size Before", result.size_before)
        col2.metric("Size After", result.size_after)
        col3.metric("Success", "Yes" if result.success else "No")

        if result.returned_value is not None:
            st.markdown("**Returned Value**")
            st.code(str(result.returned_value))

        st.markdown("**Before**")
        st.code(result.tree_before_ascii)
        st.markdown("**After**")
        st.code(result.tree_after_ascii)
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# GUIDED RESULT RENDERERS
# ========================================================================
# These helpers render guided validation workflows as stacked result cards so
# the labs can narrate each operation step-by-step.
#
# --------------------------------------------------------------- render_guided_operation_results()
def render_guided_operation_results(
    title: str,
    results: list[LabOperationResult],
) -> None:
    """Render a sequence of guided operation result cards.

    Logic:
        This helper displays one guided workflow as a stack of result cards.
        1. Render the subsection title.
        2. Show an empty-state message when no results exist.
        3. Render each result through the shared manual-result card helper.
    """
    st.subheader(title)
    if not results:
        st.info("No guided results available yet.")
        return
    for result in results:
        render_manual_operation_result(result)
# ---------------------------------------------------------------

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# BENCHMARK RENDERERS
# ========================================================================
# Benchmark helpers first prefer live Altair charts, then gracefully fall back
# to saved PNG artifacts when optional plotting dependencies are unavailable.
#
# --------------------------------------------------------------- render_benchmark_table()
def render_benchmark_table(results_df: pd.DataFrame) -> None:
    """Render the benchmark results table.

    Logic:
        This helper displays the benchmark summary table in the UI.
        1. Render the benchmark table heading.
        2. Build the normalized display table from the raw results.
        3. Show either an empty-state message or the rendered DataFrame.
    """
    st.subheader("Benchmark Results")
    table_df = build_benchmark_table(results_df)
    if table_df.empty:
        st.info("Run the benchmark suite to populate this table.")
        return
    st.dataframe(table_df, width="stretch", hide_index=True)
# --------------------------------------------------------------- end render_benchmark_table()


# --------------------------------------------------------------- render_benchmark_charts()
def render_benchmark_charts(
    results_df: pd.DataFrame,
    chart_dir: str | Path | None = None,
) -> None:
    """Render benchmark charts using Altair when available, or saved PNGs.

    Logic:
        1. Stop early when no benchmark data exists.
        2. Prefer interactive Altair charts when the optional dependency is installed.
        3. Fall back to saved PNG artifacts when Altair is unavailable.
    """
    st.subheader("Benchmark Charts")
    # VALIDATION: there is nothing to chart until at least one benchmark run exists.
    if results_df.empty:
        st.info("Run the benchmark suite to populate the charts.")
        return

    # DISPATCH: prefer interactive Altair charts when the optional dependency exists.
    if alt is not None:
        chart_df = build_benchmark_table(results_df)
        chart_df["series"] = chart_df["method"] + " - " + chart_df["scenario"]
        # Step 1: build the hit-query runtime chart used as the primary comparison view.
        runtime_chart = (
            alt.Chart(chart_df[chart_df["query_mode"] == "hits"])
            .mark_line(point=True)
            .encode(
                x=alt.X("size:Q", title="Dataset Size"),
                y=alt.Y("time_ms:Q", title="Best Runtime (ms)"),
                color=alt.Color("series:N", title="Series"),
                tooltip=["method", "scenario", "size", "time_ms"],
            )
            .properties(height=320)
        )
        st.altair_chart(runtime_chart, use_container_width=True)

        speedup_df = build_speedup_summary_table(results_df)
        # VALIDATION: skip the speedup chart until the derived summary has rows.
        if not speedup_df.empty:
            # Step 2: render the speedup chart when summary rows exist.
            speedup_chart = (
                alt.Chart(speedup_df)
                .mark_line(point=True)
                .encode(
                    x=alt.X("size:Q", title="Dataset Size"),
                    y=alt.Y("speedup_vs_list:Q", title="Speedup (ListMap / TreeMap)"),
                    color=alt.Color("scenario:N", title="Scenario"),
                    tooltip=["scenario", "query_mode", "size", "speedup_vs_list"],
                )
                .properties(height=320)
            )
            st.altair_chart(speedup_chart, use_container_width=True)
        return

    # SAFETY CHECK: when Altair is unavailable, fall back to pre-rendered PNG charts.
    if chart_dir is not None:
        base = Path(chart_dir)
        rendered_any = False
        # MAIN ITERATION LOOP: try each saved artifact listed in the shared filename map.
        for filename in CHART_FILENAMES.values():
            target = base / filename
            if target.exists():
                st.image(str(target), width="stretch")
                rendered_any = True
        if rendered_any:
            return

    st.info("Altair is unavailable and no saved chart images were found.")
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# ANALYSIS DOCUMENT RENDERING
# ========================================================================
# The analysis renderer performs light placeholder substitution and promotes
# local markdown image lines into real Streamlit images for nicer presentation.
#
# --------------------------------------------------------------- render_analysis_markdown_file()
def render_analysis_markdown_file(
    markdown_path: str | Path,
    placeholders: dict[str, str] | None = None,
) -> None:
    """Render analysis markdown with placeholder substitution and local images.

    Logic:
        1. Load the target Markdown artifact and placeholder map.
        2. Walk the file line-by-line so placeholders and image lines can be
           rendered with special handling.
        3. Flush ordinary paragraph content back through ``st.markdown()``.
    """
    path = Path(markdown_path)
    # VALIDATION: stop early when the requested Markdown artifact is missing.
    if not path.exists():
        st.error(f"Markdown file not found: {path}")
        return

    text = path.read_text(encoding="utf-8")
    if placeholders is None:
        # VALIDATION: default to an empty placeholder map so ordinary markdown still renders.
        placeholders = {}

    markdown_buffer: list[str] = []

    # --------------------------------------------------------------- _render_content()
    def _render_content(content: str) -> None:
        """Render markdown content, promoting local image lines to ``st.image()``.

        Logic:
            This nested helper decides whether a Markdown block should render
            as text or as a local image.
            1. Check whether the content is a standalone Markdown image line.
            2. Render the local image directly when the target file exists.
            3. Fall back to ``st.markdown()`` for normal content.
        """
        # DISPATCH: standalone image lines render through ``st.image()`` when
        # the referenced local artifact exists.
        image_match = _IMAGE_MARKDOWN_RE.fullmatch(content.strip())
        if image_match:
            alt_text, image_target = image_match.groups()
            image_path = path.parent / image_target
            if image_path.exists():
                st.image(str(image_path), caption=alt_text or None)
                return
        st.markdown(content)
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- _flush()
    def _flush() -> None:
        """Render the currently buffered markdown block when present.

        Logic:
            This nested helper emits buffered Markdown paragraphs at the right
            time.
            1. Check whether any buffered lines are waiting to render.
            2. Render the joined content through the shared content helper.
            3. Clear the buffer after rendering.
        """
        if markdown_buffer:
            _render_content("\n".join(markdown_buffer))
            markdown_buffer.clear()
    # --------------------------------------------------------------- 

    # MAIN ITERATION LOOP: walk the Markdown file line by line so placeholders,
    # local images, and normal paragraphs can be rendered with the right tool.
    for line in text.splitlines():
        match = _PLACEHOLDER_RE.fullmatch(line.strip())
        # DISPATCH: placeholder lines render substituted analysis fragments when available.
        if match:
            _flush()
            key = match.group(1)
            if key in placeholders:
                _render_content(placeholders[key])
            else:
                st.info(
                    f"Placeholder `{key}` — data not yet available. "
                    "Run a benchmark to populate."
                )
            continue

        image_match = _IMAGE_MARKDOWN_RE.fullmatch(line.strip())
        # DISPATCH: standalone markdown image lines render immediately as images.
        if image_match:
            _flush()
            _render_content(line)
            continue

        markdown_buffer.append(line)

    _flush()
# --------------------------------------------------------------- 

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------
