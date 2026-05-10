# File: streamlit_helpers.py |
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Reusable Streamlit rendering helpers for CTA-7 graph labs.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Rendering helpers cover headers, adjacency tables, histories, and charts.
# - Markdown/image helpers keep written-analysis artifacts visible inside Streamlit.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by streamlit_app.py to keep tab code focused on lab workflows.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit rendering helpers for the CTA-7 graph tool."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

import re
from math import isinf
from pathlib import Path

import pandas as pd
import streamlit as st

# Algorithm formatting functions  
from algorithms.graph_algorithms import format_adjacency_list, format_adjacency_matrix
# Graph protocol and data models
from algorithms.graph_protocol import WeightedGraph
from models.lab_operation_result import LabOperationResult
from models.shortest_path_result import ShortestPathResult
from models.traversal_result import TraversalResult
from ui.graphviz_visuals import (
    _graphviz_chart_height,
    build_graph_legend_html,
    build_graphviz_dot,
)

# ______________________________________________________________________________
#
# ==============================================================================
# STREAMLIT RENDERING CONSTANTS
# ==============================================================================

_MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
"""Markdown image pattern used to render local images through Streamlit media."""

_REMOTE_IMAGE_PREFIXES = ("http://", "https://", "data:")
"""Image references that are not local filesystem paths."""

_MARKDOWN_FIGURE_COLUMNS: tuple[int, int, int] = (1, 4, 1)
"""Column ratios used to center Markdown report figures at a smaller width."""

_PAIRED_RESULT_TABLE_HEIGHT = 112
"""Fixed height for compact paired-operation result tables."""

_PAIRED_RESULT_SNAPSHOT_HEIGHT = 170
"""Fixed height for scrollable before/after graph snapshots."""


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# STREAMLIT LAYOUT AND LAB RENDERERS
# ==============================================================================
# Render reusable page sections, tables, histories, charts, and algorithm traces.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_header()
def render_header() -> None:
    """Render the CTA-7 page header.

    Returns:
        None.
    """
    st.title("Graph Representation & Algorithm Tool")
    st.caption(
        "CSC506 - Design and Analysis of Algorithms | "
        "Professor Dr. Jonathan Vanover | Spring A 2026 | "
        "Student: Alexander Ricciardi"
    )
    st.divider()
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_lab_quick_start()
def render_lab_quick_start(title: str, steps: list[str]) -> None:
    """Render a compact lab workflow.

    Args:
        title: Workflow title.
        steps: Ordered workflow steps.

    Returns:
        None.
    """
    with st.container(border=True):
        st.markdown(f"**{title}**")
        for index, step in enumerate(steps, start=1):
            st.markdown(f"{index}. {step}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_lab_status_summary()
def render_lab_status_summary(
    items: list[tuple[str, str]],
    *,
    title: str = "Current State",
) -> None:
    """Render status metrics.

    Args:
        items: ``(label, value)`` pairs.
        title: Section title.

    Returns:
        None.
    """
    st.markdown(f"**{title}**")
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        column.metric(label, value)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_adjacency_views()
def render_adjacency_views(graph: WeightedGraph | None) -> None:
    """Render adjacency list and matrix views.

    Args:
        graph: Graph to render.

    Returns:
        None.
    """
    if graph is None:
        st.info("Generate or load a graph first.")
        return
    list_col, matrix_col = st.columns(2)
    with list_col:
        st.subheader("Adjacency List")
        rows = [{"Vertex": row.split(":", 1)[0], "Connections": row.split(":", 1)[1].strip()} for row in format_adjacency_list(graph)]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    with matrix_col:
        st.subheader("Adjacency Matrix")
        st.dataframe(pd.DataFrame(format_adjacency_matrix(graph)).astype(str), width="stretch", hide_index=True)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_paired_adjacency_views()
def render_paired_adjacency_views(
    list_graph: WeightedGraph | None,
    matrix_graph: WeightedGraph | None,
) -> None:
    """Render synchronized adjacency-list and adjacency-matrix views.

    Args:
        list_graph: Adjacency-list graph used for the list table.
        matrix_graph: Adjacency-matrix graph used for the matrix table.

    Returns:
        None.
    """
    if list_graph is None or matrix_graph is None:
        st.info("Generate or load a graph first.")
        return

    list_col, matrix_col = st.columns(2)
    with list_col:
        st.subheader("Adjacency List")
        rows = [
            {
                "Vertex": row.split(":", 1)[0],
                "Connections": row.split(":", 1)[1].strip(),
            }
            for row in format_adjacency_list(list_graph)
        ]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    with matrix_col:
        st.subheader("Adjacency Matrix")
        st.dataframe(
            pd.DataFrame(format_adjacency_matrix(matrix_graph)).astype(str),
            width="stretch",
            hide_index=True,
        )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _format_graph_returned()
def _format_graph_returned(value: object | None) -> str:
    """Format graph operation return values for compact result tables.

    Args:
        value: Operation return value.

    Returns:
        Human-readable value summary.
    """
    # Handle None
    if value is None:
        return "None"
    # Handle Booleans
    if isinstance(value, bool):
        return "True" if value else "False"
    # Handle Floats (with 'g' format for nice printing)
    if isinstance(value, float):
        return f"{value:g}"
    # Handle Lists
    if isinstance(value, list):
        # Empty list case
        if not value:
            return "[]"
        # Truncate long lists for display
        formatted_items: list[str] = []
        # Format list items
        for item in value[:5]:
            if isinstance(item, tuple) and len(item) == 2:
                formatted_items.append(f"{item[0]} ({float(item[1]):g})")
            else:
                formatted_items.append(str(item))
        # Show suffix for long lists
        suffix = f", ... (+{len(value) - 5})" if len(value) > 5 else ""
        return f"[{', '.join(formatted_items)}{suffix}]"
    # Handle other types by converting to string
    return str(value)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _count_change()
def _count_change(before: int | None, after: int | None) -> str:
    """Format before/after counts for paired operation tables.

    Args:
        before: Count before the operation.
        after: Count after the operation.

    Returns:
        Count change label.
    """
    if before is None or after is None:
        return "-"
    return f"{before:,} -> {after:,}"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_paired_operation_result()
def render_paired_operation_result(
    list_result: LabOperationResult | None,
    matrix_result: LabOperationResult | None,
) -> None:
    """Render synchronized operation results for both graph representations.

    Args:
        list_result: Result captured from the adjacency-list graph.
        matrix_result: Result captured from the adjacency-matrix graph.

    Returns:
        None.
    """
    if list_result is None or matrix_result is None:
        return
    # Container for the paired result
    with st.container(border=True):
        st.markdown(f"**Last Operation - {list_result.operation}**")
        st.success(list_result.summary)
        if list_result.input_details:
            st.caption(" | ".join(list_result.input_details))
        # Prepare rows for the results table
        rows = [
            {
                "Representation": result.structure,
                "Returned": _format_graph_returned(result.returned_value),
                "Vertices": _count_change(result.order_before, result.order_after),
                "Edges": _count_change(result.size_before, result.size_after),
                "Time (ms)": f"{result.elapsed_time * 1000:.4f}",
                "Big-O": result.complexity,
            }
            for result in (list_result, matrix_result)
        ]
        # Display the results table
        st.dataframe(
            pd.DataFrame(rows),
            width="stretch",
            height=_PAIRED_RESULT_TABLE_HEIGHT,
            hide_index=True,
        )
        # Expandable section for Before/After Snapshots
        with st.expander("Before / After Snapshots", expanded=False):
            list_col, matrix_col = st.columns(2)
            # Render Before/After snapshots for Adjacency List
            with list_col:
                st.markdown("**Adjacency List**")
                st.caption("Before")
                st.code(
                    "\n".join(list_result.state_before) or "(empty)",
                    wrap_lines=True,
                    height=_PAIRED_RESULT_SNAPSHOT_HEIGHT,
                )
                st.caption("After")
                st.code(
                    "\n".join(list_result.state_after) or "(empty)",
                    wrap_lines=True,
                    height=_PAIRED_RESULT_SNAPSHOT_HEIGHT,
                )
            # Render Before/After snapshots for Adjacency Matrix
            with matrix_col:
                st.markdown("**Adjacency Matrix**")
                st.caption("Before")
                st.code(
                    "\n".join(matrix_result.state_before) or "(empty)",
                    wrap_lines=True,
                    height=_PAIRED_RESULT_SNAPSHOT_HEIGHT,
                )
                st.caption("After")
                st.code(
                    "\n".join(matrix_result.state_after) or "(empty)",
                    wrap_lines=True,
                    height=_PAIRED_RESULT_SNAPSHOT_HEIGHT,
                )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_graph_visual()
def render_graph_visual(
    graph: WeightedGraph | None,
    *,
    title: str,
    highlighted_vertices: list[str] | None = None,
    highlighted_path: list[str] | None = None,
    highlighted_edges: list[tuple[str, str]] | None = None,
    predecessor_edges: list[tuple[str, str]] | None = None,
    updated_candidate_edge: tuple[str, str] | None = None,
    rejected_candidate_edge: tuple[str, str] | None = None,
    current_vertex: str | None = None,
    frontier_vertices: list[str] | None = None,
    discovered_vertices: list[str] | None = None,
    show_edge_weights: bool = True,
) -> None:
    """Render a Graphviz graph visualization.

    Args:
        graph: Graph to draw.
        title: Figure title.
        highlighted_vertices: Vertices to emphasize.
        highlighted_path: Path to emphasize.
        highlighted_edges: Edges to emphasize.
        predecessor_edges: Current predecessor-tree edges to emphasize.
        updated_candidate_edge: Candidate edge that improved a distance.
        rejected_candidate_edge: Candidate edge that did not improve a distance.
        current_vertex: Vertex currently being processed.
        frontier_vertices: Queue/stack vertices waiting to be processed.
        discovered_vertices: Vertices discovered by the algorithm.
        show_edge_weights: Whether to draw weight labels on edges.

    Returns:
        None.
    """ 
    # If the graph is empty, display a message
    if graph is None:
        st.info("Generate or load a graph first.")
        return
        
    # Build the Graphviz dot source
    dot_source = build_graphviz_dot(
        graph,
        title=title,
        highlighted_vertices=highlighted_vertices,
        highlighted_path=highlighted_path,
        highlighted_edges=highlighted_edges,
        predecessor_edges=predecessor_edges,
        updated_candidate_edge=updated_candidate_edge,
        rejected_candidate_edge=rejected_candidate_edge,
        current_vertex=current_vertex,
        frontier_vertices=frontier_vertices,
        discovered_vertices=discovered_vertices,
        show_edge_weights=show_edge_weights,
    )
    # Render the graph visualization
    st.graphviz_chart(dot_source, width="stretch", height=_graphviz_chart_height(graph))
    # Add a legend for the graph visualization
    st.markdown(build_graph_legend_html(), unsafe_allow_html=True)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_operation_history()
def render_operation_history(title: str, entries: list[str], empty_message: str) -> None:
    """Render a recent-operation history panel.

    Args:
        title: Section title.
        entries: History entries.
        empty_message: Message shown when the history is empty.

    Returns:
        None.
    """
    # Container for the operation history
    with st.container(border=True):
        st.markdown(f"**{title}**")
        # If the operation history is empty, display a message
        if not entries:
            st.info(empty_message)
            return
        for entry in entries:
            st.markdown(f"- {entry}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_validation_results()
def render_validation_results(title: str, steps: list[object]) -> None:
    """Render validation steps as a table.

    Args:
        title: Section title.
        steps: Objects exposing ``as_dict()``.

    Returns:
        None.
    """
    # Subheader for the validation results
    st.subheader(title)
    # Display the validation results as a table
    st.dataframe(pd.DataFrame([step.as_dict() for step in steps]), width="stretch", hide_index=True)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_traversal_result()
def render_traversal_result(result: TraversalResult | None) -> None:
    """Render BFS/DFS output.

    Args:
        result: Traversal result.

    Returns:
        None.
    """
    # If the traversal result is None, display a message
    if result is None:
        st.info("Run a traversal to see step-by-step output.")
        return
    # Subheader for the traversal result
    st.subheader(f"{result.algorithm} Traversal Result")
    # Success message with the visit order
    st.success(f"Visit order: {', '.join(result.visit_order)}")
    # Display the traversal result as a table
    st.dataframe(pd.DataFrame(result.steps_as_dicts()), width="stretch", hide_index=True)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_shortest_path_result()
def render_shortest_path_result(
    result: ShortestPathResult | None,
    highlighted_step_number: int | None = None,
) -> None:
    """Render shortest-path output.

    Args:
        result: Shortest path result.
        highlighted_step_number: Optional trace step number to highlight.

    Returns:
        None.
    """
    # If the shortest path result is None, display a message
    if result is None:
        st.info("Run a guided shortest-path demo to see the route and trace.")
        return
    # Subheader for the shortest path result
    st.subheader(f"{result.algorithm} Shortest Path Result")
    # Display the shortest path result
    distance = "inf" if isinf(result.distance) else f"{result.distance:g}"
    # If a negative cycle is detected, display an error message
    if result.negative_cycle_detected:
        cycle_edges = ", ".join(
            f"{source}->{target}" for source, target in result.negative_cycle_edges
        )
        # Error message for negative cycle detection
        st.error(
            "Reachable negative edge-weight cycle detected; "
            "a shortest path is undefined."
        )
        # Warning message for cycle-check edges still relaxing
        st.warning(f"Cycle-check edges still relaxing: {cycle_edges}")
    elif result.path:
        # Success message with the path label and distance
        st.success(f"{result.path_label()} | distance = {distance}")
    else:
        # Warning message for no route found
        st.warning(f"No route from {result.start_vertex} to {result.end_vertex}.")
    if result.trace_truncated:
        # Caption for truncated trace
        st.caption("Trace table capped for readability; final distances were still fully computed.")
    # Display the shortest path result as a table
    steps_df = pd.DataFrame(result.steps_as_dicts())
    if highlighted_step_number is not None and not steps_df.empty and "Step" in steps_df.columns:
        # Highlight the selected visual row so the table and graph stay aligned.
        highlighted_steps = steps_df.style.apply(
            lambda row: [
                "background-color: rgba(255, 75, 75, 0.22); font-weight: 700;"
                if int(row["Step"]) == highlighted_step_number
                else ""
                for _column in row
            ],
            axis=1,
        )
        st.dataframe(highlighted_steps, width="stretch", hide_index=True)
    else:
        st.dataframe(steps_df, width="stretch", hide_index=True)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_benchmark_table()
def render_benchmark_table(df: pd.DataFrame | None) -> None:
    """Render benchmark results.

    Args:
        df: Benchmark results DataFrame.

    Returns:
        None.
    """
    # If the benchmark DataFrame is None or empty, display a message
    if df is None or df.empty:
        st.info("Run the benchmark to generate comparison results.")
        return
    # Subheader for the benchmark results
    st.subheader("Benchmark Results")
    # Display the benchmark results as a table
    st.dataframe(df, width="stretch", hide_index=True)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_benchmark_charts()
_BENCHMARK_CONTEXT_CHART_NAMES: set[str] = {
    "benchmark_context_route_graph.png",
    "benchmark_context_traversal_graph.png",
}
"""Static context figures that should not appear in Runtime Charts."""


# -------------------------------------------------------------------------------- _runtime_chart_paths()
def _runtime_chart_paths(chart_paths: list[Path]) -> list[Path]:
    """Return existing runtime chart paths, excluding static context figures.

    Args:
        chart_paths: Candidate PNG paths.

    Returns:
        Existing runtime chart paths.
    """
    return [
        Path(path)
        for path in chart_paths
        if Path(path).exists() and Path(path).name not in _BENCHMARK_CONTEXT_CHART_NAMES
    ]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_benchmark_charts()
def render_benchmark_charts(chart_paths: list[Path]) -> None:
    """Render benchmark charts from disk.

    Args:
        chart_paths: PNG paths.

    Returns:
        None.
    """
    # If no chart paths are provided, display a message
    if not chart_paths:
        st.info("No charts have been generated yet.")
        return
    # Get existing chart paths
    existing_paths = _runtime_chart_paths(chart_paths)
    # If no existing chart paths, display a message
    if not existing_paths:
        st.info("No chart image files are available yet.")
        return
    # Subheader for the benchmark charts
    st.subheader("Runtime Charts")
    # Caption for the benchmark charts
    st.caption(
        "These compact figures summarize measured runtime trends; use the "
        "tables above for exact values."
    )
    # Create two columns for the charts
    chart_columns = st.columns(2)
    # Display each chart in the appropriate column
    for index, path in enumerate(existing_paths):
        with chart_columns[index % 2]:
            st.image(str(path), caption=path.name, width="stretch")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_markdown_file()
def _clean_markdown_image_reference(reference: str) -> str:
    """Return the image target from a Markdown image reference.

    Args:
        reference: Raw target text from ``![alt](target)``.

    Returns:
        Cleaned image target.
    """
    cleaned = reference.strip()
    if cleaned.startswith("<") and ">" in cleaned:
        return cleaned[1:cleaned.index(">")].strip()
    return cleaned.split(" ", maxsplit=1)[0].strip().strip("\"'")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _resolve_markdown_image_path()
def _resolve_markdown_image_path(reference: str, markdown_path: Path) -> Path | None:
    """Resolve a local Markdown image reference.

    Args:
        reference: Markdown image target.
        markdown_path: Markdown file that contains the image reference.

    Returns:
        Resolved local image path, or None for remote images.
    """
    target = _clean_markdown_image_reference(reference)
    # If the target starts with a remote image prefix, return None
    if target.lower().startswith(_REMOTE_IMAGE_PREFIXES):
        return None
    # Create a Path object from the target
    target_path = Path(target)
    # If the target is absolute, return it
    if target_path.is_absolute():
        return target_path
    # Get the candidate bases for the image path
    candidate_bases = [markdown_path.parent, *markdown_path.parents, Path.cwd()]
    # Check each candidate base for the image path
    for base_path in candidate_bases:
        candidate = base_path / target_path
        # If the candidate exists, return it
        if candidate.exists():
            return candidate
    # Return the target path relative to the markdown path
    return markdown_path.parent / target_path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_markdown_chunk()
def _render_markdown_chunk(markdown_text: str) -> None:
    """Render non-empty Markdown text.

    Args:
        markdown_text: Markdown text chunk.

    Returns:
        None.
    """
    if markdown_text.strip():
        st.markdown(markdown_text)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_report_image()
def _render_report_image(image_source: str, caption: str | None) -> None:
    """Render a Markdown report image at a smaller responsive width.

    Args:
        image_source: Local image path or remote image URL.
        caption: Optional image caption.

    Returns:
        None.
    """
    _, figure_column, _ = st.columns(list(_MARKDOWN_FIGURE_COLUMNS))
    with figure_column:
        st.image(image_source, caption=caption, width="stretch")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_markdown_image()
def _render_markdown_image(
    alt_text: str,
    image_reference: str,
    markdown_path: Path,
) -> None:
    """Render a Markdown image through Streamlit media handling.

    Args:
        alt_text: Markdown image alt text.
        image_reference: Raw Markdown image target.
        markdown_path: Markdown file that contains the image reference.

    Returns:
        None.
    """
    # Resolve the image path
    resolved_path = _resolve_markdown_image_path(image_reference, markdown_path)
    
    # If the image path is None, render the image with the alt text as a caption
    if resolved_path is None:
        _render_report_image(
            _clean_markdown_image_reference(image_reference),
            caption=alt_text or None,
        )
    elif resolved_path.exists():
        _render_report_image(str(resolved_path), caption=alt_text or None)
    else:
        st.warning(f"Missing image file: {image_reference.strip()}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_markdown_file()
def render_markdown_file(path: Path) -> None:
    """Render a Markdown file or an empty-state message.

    Args:
        path: Markdown file path.

    Returns:
        None.
    """
    # If the markdown path doesn't exist, display a warning message
    if not path.exists():
        st.warning(f"Missing Markdown file: {path.name}")
        return
    # Read the markdown text
    markdown_text = path.read_text(encoding="utf-8")
    # Iterate through the markdown text and render images
    cursor = 0
    for match in _MARKDOWN_IMAGE_PATTERN.finditer(markdown_text):
        _render_markdown_chunk(markdown_text[cursor:match.start()])
        _render_markdown_image(
            match.group(1).strip(),
            match.group(2),
            path,
        )
        cursor = match.end()
    _render_markdown_chunk(markdown_text[cursor:])
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
