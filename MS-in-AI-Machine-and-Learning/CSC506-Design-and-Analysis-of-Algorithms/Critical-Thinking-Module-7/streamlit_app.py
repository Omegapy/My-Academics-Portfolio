# File: streamlit_app.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Streamlit app for CTA-7 graph representations and graph algorithms.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Dataset, structure, traversal, shortest-path, benchmark, and analysis tabs.
# - Session-state helpers keep paired list/matrix graph demos synchronized.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Launch with: streamlit run CTA-7/streamlit_app.py
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit application for the CTA-7 Graph Tool.

Launch with:

    streamlit run CTA-7/streamlit_app.py
"""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from math import isinf
from pathlib import Path
import sys
import time
from collections.abc import Callable

import pandas as pd
import streamlit as st

# SETUP: add CTA-7 root so local packages import correctly from any launcher cwd.
_PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_PROJECT_ROOT))

# ==============================================================================
# ALGORITHMS
# ==============================================================================
from algorithms.graph_algorithms import (
    breadth_first_search,
    depth_first_search,
    format_adjacency_list,
    format_adjacency_matrix,
)

# ==============================================================================
# GRAPH PROTOCOL
# ==============================================================================
from algorithms.graph_protocol import WeightedGraph

# ==============================================================================
# ANALYSIS
# ==============================================================================
from analysis.benchmark_graphs import (
    DEFAULT_GRAPH_KINDS,
    DEFAULT_SEED,
    DEFAULT_SIZES,
    compute_operation_scaling_summary,
    compute_operation_winners,
    load_results_csv,
    run_benchmarks,
    save_operation_winners_csv,
    save_results_csv,
)
from analysis.lab_validation import (
    run_bellman_ford_demo,
    run_benchmark_validation,
    run_positive_shortest_path_comparison,
    run_shortest_path_demo,
    run_traversal_demo,
)
from analysis.report_generator import (
    build_benchmark_table,
    build_operation_scaling_table,
    build_operation_winners_table,
    generate_charts,
)

# ==============================================================================
# DATASET MANAGER
# ==============================================================================
from data.graph_dataset_manager import (
    build_graph,
    generate_classroom_graph_data,
    generate_negative_weight_cost_graph_data,
    generate_positive_distance_graph_data,
    generate_positive_weighted_positive_route_demo_graph_data,
    generate_random_graph_data,
    preview_edges,
)

# ==============================================================================
# MODELS
# ==============================================================================
from models.graph_edge import GraphEdge
from models.lab_operation_result import LabOperationResult
from models.shortest_path_result import ShortestPathResult
from models.traversal_result import TraversalResult

# ==============================================================================
# STREAMLIT HELPERS
# ==============================================================================
from ui.streamlit_helpers import (
    build_graphviz_dot,
    render_adjacency_views,
    render_benchmark_charts,
    render_benchmark_table,
    render_graph_visual,
    render_header,
    render_lab_quick_start,
    render_lab_status_summary,
    render_markdown_file,
    render_operation_history,
    render_paired_adjacency_views,
    render_paired_operation_result,
    render_shortest_path_result,
    render_traversal_result,
    render_validation_results,
)

# ______________________________________________________________________________
#
# ==============================================================================
# PATHS AND PAGE CONFIGURATION
# ==============================================================================

_ANALYSIS_DIR = _PROJECT_ROOT / "analysis"
_CHART_DIR = _ANALYSIS_DIR / "charts"
_CSV_PATH = _ANALYSIS_DIR / "benchmark_results.csv"
_WINNERS_CSV_PATH = _ANALYSIS_DIR / "operation_winners.csv"
_SCALING_CSV_PATH = _ANALYSIS_DIR / "operation_scaling_summary.csv"
_WRITTEN_ANALYSIS_PATH = _ANALYSIS_DIR / "written_analysis.md"
_RECOMMENDATION_GUIDE_PATH = _ANALYSIS_DIR / "recommendation_guide.md"
_TRAVERSAL_DATASET_NAME = "Sample BFS/DFS Graph"
_STRUCTURE_DATASET_NAME = "Positive Weighted Positive Route Demo"
_POSITIVE_DISTANCE_DEMO_NAME = "Positive Distance Route Demo"
_NEGATIVE_WEIGHT_DEMO_NAME = "Negative Weight Cost Demo"
_RANDOM_SPARSE_DATASET_NAME = "Random Sparse Graph"
_RANDOM_DENSE_DATASET_NAME = "Random Dense Graph"
_BUILDER_DATASET_NAMES = (
    _TRAVERSAL_DATASET_NAME,
    _STRUCTURE_DATASET_NAME,
    _NEGATIVE_WEIGHT_DEMO_NAME,
    _RANDOM_SPARSE_DATASET_NAME,
    _RANDOM_DENSE_DATASET_NAME,
)
_SHORTEST_PATH_DEMOS = (
    _POSITIVE_DISTANCE_DEMO_NAME,
    _NEGATIVE_WEIGHT_DEMO_NAME,
)
_DEFAULT_RANDOM_VERTEX_COUNT = 8

# MODULE INITIALIZATION: configure the Streamlit page before rendering widgets.
st.set_page_config(
    page_title="CTA-7 - Graph Tool",
    page_icon=_PROJECT_ROOT / "icon.png",
    layout="wide",
)

# ______________________________________________________________________________
#
# ==============================================================================
# SESSION STATE DEFAULTS
# ==============================================================================

# Constraint: every key is initialized exactly once so reruns preserve user work.
# Rationale: Streamlit reruns the script on interaction, so missing defaults break tabs.
_DEFAULTS: dict[str, object] = {
    "vertices": None,
    "edges": None,
    "dataset_name": "None",
    "directed": False,
    "list_graph": None,
    "matrix_graph": None,
    "list_history": [],
    "matrix_history": [],
    "last_list_operation_result": None,
    "last_matrix_operation_result": None,
    "structure_vertices": None,
    "structure_edges": None,
    "structure_list_graph": None,
    "structure_matrix_graph": None,
    "structure_list_history": [],
    "structure_matrix_history": [],
    "structure_history": [],
    "last_structure_list_operation_result": None,
    "last_structure_matrix_operation_result": None,
    "last_structure_operation_results": None,
    "last_structure_section": None,
    "structure_sync_warning": "",
    "traversal_vertices": None,
    "traversal_edges": None,
    "traversal_list_graph": None,
    "traversal_matrix_graph": None,
    "traversal_result_graph": None,
    "traversal_result": None,
    "traversal_list_result": None,
    "traversal_matrix_result": None,
    "shortest_vertices": None,
    "shortest_edges": None,
    "shortest_list_graph": None,
    "shortest_matrix_graph": None,
    "shortest_graph_config": None,
    "shortest_path_result_graph": None,
    "shortest_path_result": None,
    "shortest_comparison_df": None,
    "traversal_demo_result": None,
    "shortest_demo_result": None,
    "shortest_visual_run_id": 0,
    "list_demo_result": None,
    "matrix_demo_result": None,
    "benchmark_df": None,
    "operation_winners_df": None,
    "scaling_df": None,
    "benchmark_validation": None,
    "chart_paths": [],
    "benchmark_sizes": [25, 50, 100],
    "benchmark_kinds": list(DEFAULT_GRAPH_KINDS),
    "benchmark_repeats": 1,
    "benchmark_directed": False,
    "benchmark_include_bellman_ford": True,
    "builder_vertex_count": _DEFAULT_RANDOM_VERTEX_COUNT,
    "builder_seed": DEFAULT_SEED,
    "shortest_demo_name": _POSITIVE_DISTANCE_DEMO_NAME,
}

# MODULE INITIALIZATION: seed any missing session-state keys without overwriting values.
for _key, _value in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value


# ______________________________________________________________________________
#
# ==============================================================================
# APP HELPERS
# ==============================================================================


# -------------------------------------------------------------------------------- _graph_data_ready()
def _graph_data_ready() -> bool:
    """Return True when graph source data is available.

    Returns:
        Whether graph data exists in session state.
    """
    return st.session_state["vertices"] is not None and st.session_state["edges"] is not None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _active_graph()
def _active_graph(representation: str) -> WeightedGraph | None:
    """Return the active graph for a representation label.

    Args:
        representation: ``"list"`` or ``"matrix"``.

    Returns:
        Active graph or None.
    """
    key = "list_graph" if representation == "list" else "matrix_graph"
    graph = st.session_state[key]
    return graph if graph is not None else None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _load_graphs()
def _load_graphs(vertices: list[str], edges: list[GraphEdge], *, directed: bool) -> None:
    """Build and store both graph representations.

    Args:
        vertices: Vertex labels.
        edges: Weighted edges.
        directed: Whether edges are directed.

    Returns:
        None.
    """
    st.session_state["vertices"] = vertices
    st.session_state["edges"] = edges
    st.session_state["directed"] = directed
    st.session_state["list_graph"] = build_graph("list", vertices, edges, directed=directed)
    st.session_state["matrix_graph"] = build_graph("matrix", vertices, edges, directed=directed)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _graph_for_lab()
def _graph_for_lab(prefix: str, representation: str) -> WeightedGraph | None:
    """Return a lab-owned graph by state prefix and representation.

    Args:
        prefix: Session-state prefix for the lab.
        representation: ``"list"`` or ``"matrix"``.

    Returns:
        Lab graph or None.
    """
    key = f"{prefix}_{representation}_graph"
    graph = st.session_state[key]
    return graph if graph is not None else None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _store_lab_graphs()
def _store_lab_graphs(
    prefix: str,
    vertices: list[str],
    edges: list[GraphEdge],
    *,
    directed: bool = False,
) -> None:
    """Build and store both graph representations for one lab.

    Args:
        prefix: Session-state prefix for the lab.
        vertices: Vertex labels.
        edges: Weighted edges.
        directed: Whether edges are directed.

    Returns:
        None.
    """
    st.session_state[f"{prefix}_vertices"] = vertices
    st.session_state[f"{prefix}_edges"] = edges
    st.session_state[f"{prefix}_list_graph"] = build_graph(
        "list",
        vertices,
        edges,
        directed=directed,
    )
    st.session_state[f"{prefix}_matrix_graph"] = build_graph(
        "matrix",
        vertices,
        edges,
        directed=directed,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _ensure_structure_graphs()
def _ensure_structure_graphs() -> None:
    """Ensure the Graph Structure Lab has its own positive weighted route demo.

    Returns:
        None.
    """
    if (
        st.session_state["structure_list_graph"] is not None
        and st.session_state["structure_matrix_graph"] is not None
    ):
        return
    vertices, edges = generate_positive_weighted_positive_route_demo_graph_data()
    _store_lab_graphs("structure", vertices, edges, directed=False)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _ensure_traversal_graphs()
def _ensure_traversal_graphs() -> None:
    """Ensure the Traversal Lab has its own classroom graph.

    Returns:
        None.
    """
    if (
        st.session_state["traversal_list_graph"] is not None
        and st.session_state["traversal_matrix_graph"] is not None
    ):
        return
    vertices, edges = generate_classroom_graph_data()
    _store_lab_graphs("traversal", vertices, edges, directed=False)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _shortest_demo_graph_data()
def _shortest_demo_graph_data(demo_name: str) -> tuple[list[str], list[GraphEdge], bool]:
    """Return graph data for a guided shortest-path demo.

    Args:
        demo_name: Selected guided demo name.

    Returns:
        Vertices, edges, and direction flag.

    Raises:
        ValueError: If the demo name is unknown.
    """
    if demo_name == _POSITIVE_DISTANCE_DEMO_NAME:
        vertices, edges = generate_positive_distance_graph_data()
        return vertices, edges, False
    if demo_name == _NEGATIVE_WEIGHT_DEMO_NAME:
        vertices, edges = generate_negative_weight_cost_graph_data()
        return vertices, edges, True
    raise ValueError(f"Unknown guided shortest-path demo: {demo_name}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _ensure_shortest_demo_graphs()
def _ensure_shortest_demo_graphs(demo_name: str) -> None:
    """Ensure the Shortest Path Lab has graph data for the selected demo.

    Args:
        demo_name: Selected guided demo name.

    Returns:
        None.
    """
    config = (demo_name,)
    if (
        st.session_state["shortest_graph_config"] == config
        and st.session_state["shortest_list_graph"] is not None
    ):
        return

    vertices, edges, directed = _shortest_demo_graph_data(demo_name)
    _store_lab_graphs("shortest", vertices, edges, directed=directed)
    st.session_state["shortest_graph_config"] = config
    st.session_state["shortest_path_result"] = None
    st.session_state["shortest_path_result_graph"] = None
    st.session_state["shortest_demo_result"] = None
    st.session_state["shortest_comparison_df"] = None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _selected_visual_step_index()
def _selected_visual_step_index(label: str, step_count: int, *, key: str) -> int:
    """Return the selected zero-based visual step index.

    Args:
        label: Slider label.
        step_count: Number of available algorithm trace steps.
        key: Streamlit widget key.

    Returns:
        Zero-based selected step index.
    """
    if step_count <= 1:
        st.caption("Only one visual step is available for this result.")
        return 0
    selected_step_number = st.slider(
        label,
        min_value=1,
        max_value=step_count,
        value=1,
        key=key,
    )
    return int(selected_step_number) - 1
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _bounded_visual_step_number()
def _bounded_visual_step_number(step_number: object, step_count: int) -> int:
    """Return a visual step number clamped to the available trace range.

    Args:
        step_number: Candidate one-based visual step number.
        step_count: Number of available algorithm trace steps.

    Returns:
        One-based visual step number within ``1..step_count``.
    """
    try:
        selected_step = int(step_number)
    except (TypeError, ValueError):
        selected_step = 1
    return min(max(selected_step, 1), max(step_count, 1))
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _move_visual_step()
def _move_visual_step(state_key: str, slider_key: str, delta: int, step_count: int) -> None:
    """Move a stateful visual step control by one bounded delta.

    Args:
        state_key: Session-state key storing the selected visual step.
        slider_key: Session-state key owned by the slider widget.
        delta: Signed step movement.
        step_count: Number of available algorithm trace steps.

    Returns:
        None.
    """
    current_step = _bounded_visual_step_number(
        st.session_state.get(slider_key, st.session_state.get(state_key, 1)),
        step_count,
    )
    next_step = _bounded_visual_step_number(current_step + delta, step_count)
    st.session_state[state_key] = next_step
    st.session_state[slider_key] = next_step
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _selected_visual_step_index_with_stepper()
def _selected_visual_step_index_with_stepper(
    label: str,
    step_count: int,
    *,
    key: str,
    previous_label: str,
    next_label: str,
) -> int:
    """Return a stateful selected visual step index with stepper buttons.

    Args:
        label: Slider label.
        step_count: Number of available algorithm trace steps.
        key: Stable base key for related Streamlit widgets.
        previous_label: Previous-step button label.
        next_label: Next-step button label.

    Returns:
        Zero-based selected step index.
    """
    if step_count <= 1:
        st.caption("Only one visual step is available for this result.")
        return 0

    state_key = f"{key}_state"
    slider_key = f"{key}_slider"
    current_step = _bounded_visual_step_number(
        st.session_state.get(slider_key, st.session_state.get(state_key, 1)),
        step_count,
    )
    st.session_state[state_key] = current_step
    if slider_key not in st.session_state:
        st.session_state[slider_key] = current_step

    previous_col, slider_col, next_col = st.columns([2, 5, 2])
    with previous_col:
        st.button(
            previous_label,
            disabled=current_step <= 1,
            key=f"{key}_previous",
            on_click=_move_visual_step,
            args=(state_key, slider_key, -1, step_count),
        )
    with next_col:
        st.button(
            next_label,
            disabled=current_step >= step_count,
            key=f"{key}_next",
            on_click=_move_visual_step,
            args=(state_key, slider_key, 1, step_count),
        )
    with slider_col:
        selected_step_number = st.slider(
            label,
            min_value=1,
            max_value=step_count,
            key=slider_key,
        )

    selected_step_number = _bounded_visual_step_number(selected_step_number, step_count)
    st.session_state[state_key] = selected_step_number
    return selected_step_number - 1
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _distance_label()
def _distance_label(distance: float) -> str:
    """Return a compact display label for a shortest-path distance.

    Args:
        distance: Numeric distance value.

    Returns:
        Formatted distance label.
    """
    return "inf" if isinf(distance) else f"{distance:g}"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _append_history()
def _append_history(key: str, message: str) -> None:
    """Append one most-recent-first history entry.

    Args:
        key: Session-state history key.
        message: Message to add.

    Returns:
        None.
    """
    history = list(st.session_state[key])
    history.insert(0, message)
    st.session_state[key] = history[:8]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _snapshot_graph()
def _snapshot_graph(graph: WeightedGraph | None) -> list[str]:
    """Return a compact graph snapshot.

    Args:
        graph: Graph to snapshot.

    Returns:
        Text rows for before/after cards.
    """
    if graph is None:
        return ["(no graph loaded)"]
    rows = format_adjacency_list(graph)
    return rows[:10] + ([f"... ({graph.order()} vertices total)"] if len(rows) > 10 else [])
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _edge_signature()
def _edge_signature(graph: WeightedGraph, edge: GraphEdge) -> tuple[str, str, float]:
    """Return a comparable edge signature.

    Args:
        graph: Graph that owns the edge.
        edge: Edge to normalize.

    Returns:
        Comparable ``(source, target, weight)`` tuple.
    """
    if graph.directed:
        return (edge.source, edge.target, edge.weight)
    source, target = sorted((edge.source, edge.target))
    return (source, target, edge.weight)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _graph_signature()
def _graph_signature(graph: WeightedGraph | None) -> tuple[tuple[str, ...], tuple[tuple[str, str, float], ...]]:
    """Return a comparable graph signature.

    Args:
        graph: Graph to inspect.

    Returns:
        Vertex-order tuple and sorted edge-signature tuple.
    """
    if graph is None:
        return ((), ())
    return (
        tuple(graph.vertices()),
        tuple(sorted(_edge_signature(graph, edge) for edge in graph.edges())),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _structure_graphs_in_sync()
def _structure_graphs_in_sync() -> bool:
    """Return whether the Structure Lab graphs have the same logical state.

    Returns:
        True when adjacency list and matrix represent the same graph.
    """
    return _graph_signature(_graph_for_lab("structure", "list")) == _graph_signature(
        _graph_for_lab("structure", "matrix")
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _sync_structure_source_state()
def _sync_structure_source_state() -> None:
    """Refresh Structure Lab source-data state from the adjacency-list graph.

    Returns:
        None.
    """
    graph = _graph_for_lab("structure", "list")
    if graph is None:
        st.session_state["structure_vertices"] = None
        st.session_state["structure_edges"] = None
        return
    st.session_state["structure_vertices"] = graph.vertices()
    st.session_state["structure_edges"] = graph.edges()
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _return_values_match()
def _return_values_match(first: object | None, second: object | None) -> bool:
    """Return whether paired operation return values are equivalent.

    Args:
        first: First return value.
        second: Second return value.

    Returns:
        Whether values should be treated as matching.
    """
    if first == second:
        return True
    if isinstance(first, list) and isinstance(second, list):
        return sorted(str(item) for item in first) == sorted(str(item) for item in second)
    return False
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _show_edge_weights_for_active_dataset()
def _show_edge_weights_for_active_dataset() -> bool:
    """Return True when the active dataset should display edge weights.

    Returns:
        Whether graph visuals should label edge weights.
    """
    return st.session_state["dataset_name"] not in {
        _TRAVERSAL_DATASET_NAME,
        _RANDOM_DENSE_DATASET_NAME,
    }
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _predecessor_edges()
def _predecessor_edges(predecessors: dict[str, str | None]) -> list[tuple[str, str]]:
    """Return predecessor-map edges for shortest-path visual traces.

    Args:
        predecessors: Vertex-to-predecessor mapping.

    Returns:
        Directed predecessor edges.
    """
    return [
        (predecessor, vertex)
        for vertex, predecessor in predecessors.items()
        if predecessor is not None
    ]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_shortest_path_result_section()
def _render_shortest_path_result_section(
    path_result: ShortestPathResult | None,
    display_graph: WeightedGraph | None,
    path_representation: str,
) -> None:
    """Render a shortest-path result, visual trace step, and final graph.

    Args:
        path_result: Shortest-path result to display.
        display_graph: Graph used to render trace and final route visuals.
        path_representation: Active representation key for unique widget keys.

    Returns:
        None.
    """
    # If there are no steps, return
    if path_result is None:
        render_shortest_path_result(path_result)
        return

    result_container = st.container()
    selected_step = None
    shortest_step_index = 0

    # If there are steps, render them
    if path_result.steps:
        shortest_visual_key = (
            f"shortest_visual_step_{path_result.algorithm}_{path_representation}_"
            f"{path_result.start_vertex}_{path_result.end_vertex}_{len(path_result.steps)}_"
            f"{st.session_state['shortest_visual_run_id']}"
        )
        shortest_step_index = _selected_visual_step_index_with_stepper(
            f"{path_result.algorithm} Visual Step",
            len(path_result.steps),
            key=shortest_visual_key,
            previous_label=f"Previous {path_result.algorithm} step",
            next_label=f"Next {path_result.algorithm} step",
        )
        # Get the selected step
        selected_step = path_result.steps[shortest_step_index]

    # Render the result after selecting the step so the trace table can highlight it.
    highlighted_step_number = (
        selected_step.step_number
        if selected_step is not None
        else None
    )
    with result_container:
        render_shortest_path_result(path_result, highlighted_step_number)

    if selected_step is not None:
        # Get the candidate edge and label
        candidate_edge = (selected_step.current_vertex, selected_step.neighbor)
        candidate_label = _distance_label(selected_step.candidate_distance)
        # Get the known label
        known_label = _distance_label(selected_step.known_distance)
        # Get the action label
        action_label = "update" if selected_step.updated else "check"
        # Render the Bellman-Ford step
        if path_result.algorithm == "Bellman-Ford":
            visual_step_number = shortest_step_index + 1
            phase_label = selected_step.phase.lower()
            st.caption(
                f"Bellman-Ford Visual Step {visual_step_number} of {len(path_result.steps)} "
                f"checks {selected_step.current_vertex} -> {selected_step.neighbor} "
                f"during {phase_label} pass {selected_step.pass_number}. "
                f"Candidate distance {candidate_label}; previous known distance {known_label}; "
                f"updated: {'Yes' if selected_step.updated else 'No'}."
            )
            # Render the graph visual
            render_graph_visual(
                display_graph,
                title=(
                    f"Visual Step {visual_step_number} of {len(path_result.steps)} - "
                    f"{selected_step.phase} pass {selected_step.pass_number}: "
                    f"{selected_step.current_vertex} -> {selected_step.neighbor}"
                ),
                highlighted_vertices=[selected_step.neighbor],
                predecessor_edges=_predecessor_edges(selected_step.predecessor_snapshot),
                updated_candidate_edge=candidate_edge if selected_step.updated else None,
                rejected_candidate_edge=candidate_edge if not selected_step.updated else None,
                current_vertex=selected_step.current_vertex,
            )
        # Render the Dijkstra step
        else:
            visual_step_number = shortest_step_index + 1
            title_suffix = (
                f"{action_label} {selected_step.current_vertex} -> {selected_step.neighbor}"
                if selected_step.updated
                else f"{action_label} {selected_step.current_vertex} -> {selected_step.neighbor} (no update)"
            )
            # Render the graph visual
            st.caption(
                f"Dijkstra Visual Step {visual_step_number} of {len(path_result.steps)} "
                f"checks {selected_step.current_vertex} -> {selected_step.neighbor}. "
                f"Candidate distance {candidate_label}; previous known distance {known_label}; "
                f"updated: {'Yes' if selected_step.updated else 'No'}."
            )
            # Render the graph visual
            render_graph_visual(
                display_graph,
                title=(
                    f"Visual Step {visual_step_number} of {len(path_result.steps)} - "
                    f"Dijkstra: {title_suffix}"
                ),
                highlighted_vertices=[selected_step.neighbor],
                predecessor_edges=_predecessor_edges(selected_step.predecessor_snapshot),
                updated_candidate_edge=candidate_edge if selected_step.updated else None,
                rejected_candidate_edge=candidate_edge if not selected_step.updated else None,
                current_vertex=selected_step.current_vertex,
                frontier_vertices=selected_step.queue_snapshot,
            )
    # Render the final graph visual
    if path_result.negative_cycle_detected:
        render_graph_visual(
            display_graph,
            title=f"{path_result.algorithm} Shortest Path Result",
            highlighted_edges=path_result.negative_cycle_edges,
        )
    # Render the final graph visual 
    else:
        render_graph_visual(
            display_graph,
            title=f"{path_result.algorithm} Shortest Path Result",
            highlighted_path=path_result.path,
        )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_traversal_algorithm()
def _run_traversal_algorithm(
    graph: WeightedGraph,
    algorithm_key: str,
    start_vertex: str,
) -> TraversalResult:
    """Run BFS or DFS on one graph.

    Args:
        graph: Graph to traverse.
        algorithm_key: ``"BFS"`` or ``"DFS"``.
        start_vertex: Vertex where traversal begins.

    Returns:
        Traversal result.
    """
    if algorithm_key == "BFS":
        return breadth_first_search(graph, start_vertex)
    return depth_first_search(graph, start_vertex)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _store_paired_traversal_results()
def _store_paired_traversal_results(algorithm_key: str, start_vertex: str) -> None:
    """Run and store traversal results for both graph representations.

    Args:
        algorithm_key: ``"BFS"`` or ``"DFS"``.
        start_vertex: Vertex where traversal begins.

    Returns:
        None.
    """
    list_graph = _graph_for_lab("traversal", "list")
    matrix_graph = _graph_for_lab("traversal", "matrix")
    if list_graph is None or matrix_graph is None:
        return

    list_result = _run_traversal_algorithm(list_graph, algorithm_key, start_vertex)
    matrix_result = _run_traversal_algorithm(matrix_graph, algorithm_key, start_vertex)
    st.session_state["traversal_list_result"] = list_result
    st.session_state["traversal_matrix_result"] = matrix_result
    # BACKWARD COMPATIBILITY: keep the original single-result slots populated.
    st.session_state["traversal_result"] = list_result
    st.session_state["traversal_result_graph"] = list_graph
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_traversal_result_section()
def _render_traversal_result_section(
    title: str,
    result: TraversalResult | None,
    graph: WeightedGraph | None,
) -> None:
    """Render one representation's traversal result and visual step.

    Args:
        title: Representation label.
        result: Traversal result for that representation.
        graph: Graph used to render visual steps.

    Returns:
        None.
    """
    # Render the traversal result   
    st.subheader(title)
    render_traversal_result(result)
    # If there are no steps, return
    if result is None:
        return
    # Select the visual step
    selected_step_index = _selected_visual_step_index(
        f"{title} Visual Step",
        len(result.steps),
        key=f"traversal_visual_step_{result.algorithm}_{title}_{result.start_vertex}_{len(result.steps)}",
    )
    # Get the selected step   
    selected_step = result.steps[selected_step_index]
    # Render the graph visual
    render_graph_visual(
        graph,
        title=f"{title} {result.algorithm} Step {selected_step.step_number}: {selected_step.current_vertex}",
        highlighted_vertices=selected_step.visited,
        highlighted_edges=selected_step.traversed_edges,
        current_vertex=selected_step.current_vertex,
        frontier_vertices=selected_step.frontier,
        discovered_vertices=selected_step.discovered,
        show_edge_weights=False,
    )   
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _format_benchmark_display()
def _format_benchmark_display(df: pd.DataFrame) -> pd.DataFrame:
    """Return a readable benchmark table for Streamlit display.

    Args:
        df: Raw benchmark results DataFrame.

    Returns:
        Formatted DataFrame.
    """
    # Copy the DataFrame
    display = df.copy()
    # Format the operation group
    display["operation_group"] = display["operation_group"].map(
        lambda value: {
            "construction": "Construction",
            "adjacency_queries": "Adjacency Queries",
            "neighbor_scan": "Neighbor Scan",
            "traversal": "Traversal",
            "shortest_path": "Shortest Path",
            "mutation": "Mutation",
        }.get(str(value), str(value))
    )
    # Select the columns to display
    display = display[
        [
            "graph_kind",
            "structure",
            "operation",
            "operation_group",
            "size",
            "edge_count",
            "workload_count",
            "time_ms",
            "avg_time_us",
            "complexity",
            "is_correct",
        ]
    ]
    # Format the column names 
    display.columns = [
        "Graph",
        "Structure",
        "Operation",
        "Group",
        "V",
        "E",
        "Workload",
        "Time (ms)",
        "Avg (us)",
        "Big-O",
        "Correct",
    ]
    # Format the column values
    display["V"] = display["V"].map(lambda value: f"{int(value):,}")
    display["E"] = display["E"].map(lambda value: f"{int(value):,}")
    display["Workload"] = display["Workload"].map(lambda value: f"{int(value):,}")
    display["Time (ms)"] = display["Time (ms)"].map(lambda value: f"{float(value):.4f}")
    display["Avg (us)"] = display["Avg (us)"].map(lambda value: f"{float(value):.4f}")
    display["Correct"] = display["Correct"].map(lambda value: "Yes" if bool(value) else "No")
    return display
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _format_operation_winners_display()
def _format_operation_winners_display(df: pd.DataFrame) -> pd.DataFrame:
    """Return a readable winners table for Streamlit display.

    Args:
        df: Operation winners DataFrame.

    Returns:
        Formatted DataFrame.
    """
    # Copy the DataFrame
    display = df.copy()
    # Format the operation group 
    display["operation_group"] = display["operation_group"].map(
        lambda value: {
            "construction": "Construction",
            "adjacency_queries": "Adjacency Queries",
            "neighbor_scan": "Neighbor Scan",
            "traversal": "Traversal",
            "shortest_path": "Shortest Path",
            "mutation": "Mutation",
        }.get(str(value), str(value))
    )
    # Select the columns to display
    display = display[
        [
            "graph_kind",
            "operation",
            "operation_group",
            "size",
            "fastest_structure",
            "fastest_time_ms",
            "runner_up",
            "runner_up_time_ms",
            "pct_faster_than_runner_up",
        ]
    ]
    # Format the column names
    display.columns = [
        "Graph",
        "Operation",
        "Group",
        "V",
        "Fastest Structure",
        "Fastest Time (ms)",
        "Runner-Up",
        "Runner-Up Time (ms)",
        "Gap",
    ]
    # Format the column values
    display["V"] = display["V"].map(lambda value: f"{int(value):,}")
    display["Fastest Time (ms)"] = display["Fastest Time (ms)"].map(lambda value: f"{float(value):.4f}")
    display["Runner-Up Time (ms)"] = display["Runner-Up Time (ms)"].map(lambda value: f"{float(value):.4f}")
    display["Gap"] = display["Gap"].map(lambda value: f"{float(value):.1f}%")
    return display
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_unweighted_edges()
def _build_unweighted_edges(edges: list[GraphEdge]) -> list[GraphEdge]:
    """Return preview edges with unit weights.

    Args:
        edges: Weighted source edges.

    Returns:
        Edges with the same endpoints and unit weights.
    """
    return [GraphEdge(edge.source, edge.target, 1.0) for edge in edges]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_mixed_weight_preview_edges()
def _build_mixed_weight_preview_edges(edges: list[GraphEdge]) -> list[GraphEdge]:
    """Return preview edges with a few negative illustration weights.

    Args:
        edges: Positive generated source edges.

    Returns:
        Edges with deterministic mixed positive and negative weights.
    """
    mixed_edges: list[GraphEdge] = []
    # For each edge, alternate between positive and negative weights
    for index, edge in enumerate(edges):
        if index % 4 == 1:
            mixed_edges.append(GraphEdge(edge.source, edge.target, -max(1.0, edge.weight / 2.0)))
        else:
            mixed_edges.append(edge)
    return mixed_edges
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_benchmark_graph_gallery()
def _render_benchmark_graph_gallery() -> None:
    """Render compact example graphs for Benchmark Lab context.

    Returns:
        None.
    """
    # Generate random graph data
    sparse_vertices, sparse_weighted_edges = generate_random_graph_data(
        6,
        "sparse",
        directed=False,
        seed=DEFAULT_SEED,
    )
    # Generate random graph data
    dense_vertices, dense_weighted_edges = generate_random_graph_data(
        6,
        "dense",
        directed=False,
        seed=DEFAULT_SEED + 1,
    )
    # Generate random graph data
    directed_sparse_vertices, directed_sparse_edges = generate_random_graph_data(
        5,
        "sparse",
        directed=True,
        seed=DEFAULT_SEED + 2,
    )
    # Generate random graph data
    directed_dense_vertices, directed_dense_edges = generate_random_graph_data(
        5,
        "dense",
        directed=True,
        seed=DEFAULT_SEED + 3,
    )
    # Vertices for a loop graph
    loop_vertices = ["A", "B", "C", "D", "E"]
    # Unweighted edges for a loop graph
    loop_unweighted_edges = [
        GraphEdge("A", "B", 1.0),
        GraphEdge("B", "C", 1.0),
        GraphEdge("C", "C", 1.0),
        GraphEdge("C", "D", 1.0),
        GraphEdge("D", "E", 1.0),
        GraphEdge("E", "B", 1.0),
    ]
    # Weighted edges for a loop graph
    loop_weighted_edges = [
        GraphEdge("A", "B", 4.0),
        GraphEdge("B", "C", -7.0),
        GraphEdge("C", "C", 2.0),
        GraphEdge("C", "D", 5.0),
        GraphEdge("D", "E", -3.0),
        GraphEdge("E", "B", 8.0),
    ]
    # Gallery specifications
    gallery_specs = [
        (
            "Sparse Unweighted Undirected Graph",
            build_graph("list", sparse_vertices, _build_unweighted_edges(sparse_weighted_edges)),
            False,
        ),
        (
            "Sparse Weighted Undirected Graph",
            build_graph("list", sparse_vertices, _build_mixed_weight_preview_edges(sparse_weighted_edges)),
            True,
        ),
        (
            "Dense Unweighted Undirected Graph",
            build_graph("list", dense_vertices, _build_unweighted_edges(dense_weighted_edges)),
            False,
        ),
        (
            "Dense Weighted Undirected Graph",
            build_graph("list", dense_vertices, _build_mixed_weight_preview_edges(dense_weighted_edges)),
            True,
        ),
        (
            "Sparse Unweighted Directed Graph",
            build_graph(
                "list",
                directed_sparse_vertices,
                _build_unweighted_edges(directed_sparse_edges),
                directed=True,
            ),
            False,
        ),
        (
            "Dense Weighted Directed Graph",
            build_graph(
                "list",
                directed_dense_vertices,
                _build_mixed_weight_preview_edges(directed_dense_edges),
                directed=True,
            ),
            True,
        ),
        (
            "Directed Unweighted Self-Loop Graph",
            build_graph("list", loop_vertices, loop_unweighted_edges, directed=True),
            False,
        ),
        (
            "Directed Weighted Self-Loop Graph",
            build_graph("list", loop_vertices, loop_weighted_edges, directed=True),
            True,
        ),
    ]
    # Render the graph gallery
    st.subheader("Benchmark Graph Gallery")
    st.caption(
        "These compact Graphviz previews show the graph shapes used when reading "
        "benchmark density, direction, and weight results. Negative weights in "
        "the weighted examples illustrate credits, discounts, or cost reductions; "
        "the actual benchmark shortest-path workloads still use positive weights "
        "for Dijkstra compatibility."
    )
    # Render the graph gallery
    gallery_columns = st.columns(4)
    for index, (label, graph, show_edge_weights) in enumerate(gallery_specs):
        with gallery_columns[index % 4]:
            st.markdown(f"**{label}**")
            dot_source = build_graphviz_dot(
                graph,
                title=label,
                show_edge_weights=show_edge_weights,
                compact=True,
            )
            st.graphviz_chart(dot_source, width="stretch", height=235)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_compact_benchmark_graph()
def _render_compact_benchmark_graph(
    graph: WeightedGraph,
    *,
    title: str,
    highlighted_path: list[str] | None = None,
    highlighted_vertices: list[str] | None = None,
    show_edge_weights: bool = True,
) -> None:
    """Render a compact Graphviz chart for Benchmark Lab context.

    Args:
        graph: Graph to render.
        title: Graph title.
        highlighted_path: Optional path to highlight.
        highlighted_vertices: Optional vertices to highlight.
        show_edge_weights: Whether to show edge weight labels.

    Returns:
        None.
    """
    dot_source = build_graphviz_dot(
        graph,
        title=title,
        highlighted_path=highlighted_path,
        highlighted_vertices=highlighted_vertices,
        show_edge_weights=show_edge_weights,
        compact=True,
    )
    st.graphviz_chart(dot_source, width="stretch", height=260)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_benchmark_reference_explanation()
def _render_benchmark_reference_explanation() -> None:
    """Render reference-based Benchmark Lab explanations.

    Returns:
        None.
    """
    st.subheader("How to Read the Benchmark")
    st.markdown(
        "- A graph is modeled as `G = (V, E)`: vertices are the items, and edges "
        "are the connections between them.\n"
        "- Undirected edges connect both ways; directed edges use arrows from a "
        "source vertex to a target vertex. A self-loop is an edge from a vertex "
        "back to itself.\n"
        "- Unweighted traversal treats each edge as equal. Weighted shortest-path "
        "workloads use edge costs such as distance, latency, credits, discounts, "
        "or route cost. Negative weights can model a cost reduction, but "
        "Dijkstra remains limited to non-negative weights.\n"
        "- Sparse graphs have far fewer edges than the maximum possible, so "
        "adjacency lists usually save memory with `O(V + E)` storage. Dense "
        "graphs fill more of the possible vertex pairs, making adjacency matrices "
        "more competitive for direct edge checks.\n"
        "- BFS and DFS measure reachability and neighbor scanning. Dijkstra "
        "measures non-negative weighted shortest paths. Bellman-Ford relaxes "
        "edges repeatedly in `O(VE)` and is the safer algorithm when negative "
        "weights or negative-cycle detection matter."
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _save_benchmark_artifacts()
def _save_benchmark_artifacts() -> None:
    """Persist benchmark, winner, and scaling DataFrames to CSV.

    Returns:
        None.
    """
    benchmark_df = st.session_state["benchmark_df"]
    winners_df = st.session_state["operation_winners_df"]
    scaling_df = st.session_state["scaling_df"]
    if benchmark_df is None or winners_df is None or scaling_df is None:
        st.error("No benchmark artifacts are ready. Run the benchmark first.")
        return
    save_results_csv(benchmark_df, _CSV_PATH)
    save_operation_winners_csv(winners_df, _WINNERS_CSV_PATH)
    save_results_csv(scaling_df, _SCALING_CSV_PATH)
    st.success(
        "Saved benchmark_results.csv, operation_winners.csv, and "
        "operation_scaling_summary.csv under CTA-7/analysis/."
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _load_saved_benchmark_artifacts()
def _load_saved_benchmark_artifacts() -> None:
    """Load saved benchmark CSV artifacts into session state.

    Returns:
        None.
    """
    # Load benchmark results
    benchmark_df = load_results_csv(_CSV_PATH)  
    # Check if benchmark results are empty
    if benchmark_df.empty:
        st.error(f"No saved benchmark results found at {_CSV_PATH}.")
        return
    # Load operation winners
    winners_df = load_results_csv(_WINNERS_CSV_PATH)
    # Check if operation winners are empty
    if winners_df.empty:
        winners_df = compute_operation_winners(benchmark_df)
    # Load scaling summary
    scaling_df = load_results_csv(_SCALING_CSV_PATH)
    # Check if scaling summary is empty
    if scaling_df.empty:
        scaling_df = compute_operation_scaling_summary(benchmark_df)
    # Generate charts
    chart_paths = generate_charts(benchmark_df, _CHART_DIR, winners_df=winners_df)
    # Store benchmark artifacts in session state
    st.session_state["benchmark_df"] = benchmark_df
    st.session_state["operation_winners_df"] = winners_df
    st.session_state["scaling_df"] = scaling_df
    st.session_state["chart_paths"] = chart_paths
    st.session_state["benchmark_validation"] = run_benchmark_validation(benchmark_df)
    st.success(f"Loaded {len(benchmark_df)} benchmark rows from saved CSV artifacts.")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_benchmark_context_sections()
def _render_benchmark_context_sections() -> None:
    """Render Benchmark Lab context from the other CTA-7 labs.

    Returns:
        None.
    """
    st.subheader("Benchmark Context From Other Labs")
    structure_vertices, structure_edges = generate_positive_weighted_positive_route_demo_graph_data()
    structure_list_graph = build_graph("list", structure_vertices, structure_edges)
    structure_matrix_graph = build_graph("matrix", structure_vertices, structure_edges)
    context_tabs = st.tabs(["Graph Structure", "Traversal", "Shortest Path"])
    # Render graph structure context
    with context_tabs[0]:
        # Render compact benchmark graph
        st.caption(
            "The benchmark uses the same representation trade-off shown in the "
            "Graph Structure Lab: lists store only neighbors, while matrices "
            "store every possible vertex pair."
        )
        # Render compact benchmark graph
        st.markdown("**Positive Weighted Route Graph**")
        _render_compact_benchmark_graph(
            structure_list_graph,
            title="Graph Structure Context",
            show_edge_weights=True,
        )
        # Render list and matrix snapshots
        list_col, matrix_col = st.columns(2)
        with list_col:
            st.markdown("**Adjacency List Snapshot**")
            list_rows = [
                {
                    "Vertex": row.split(":", 1)[0],
                    "Connections": row.split(":", 1)[1].strip(),
                }
                # Format adjacency list
                for row in format_adjacency_list(structure_list_graph)
            ]
            st.dataframe(pd.DataFrame(list_rows), width="stretch", hide_index=True)
        # Render matrix snapshot
        with matrix_col:
            st.markdown("**Adjacency Matrix Snapshot**")
            st.dataframe(
                pd.DataFrame(format_adjacency_matrix(structure_matrix_graph)).astype(str),
                width="stretch",
                hide_index=True,
            )

    # Render traversal context
    with context_tabs[1]:
        # Generate traversal graph data
        traversal_vertices, traversal_edges = generate_classroom_graph_data()
        traversal_graph = build_graph("list", traversal_vertices, traversal_edges)
        traversal_demo = run_traversal_demo("list", directed=False)
        # Render traversal context caption
        st.caption(
            "BFS and DFS are benchmarked as reachability workloads. The visit "
            "orders below come from the same classroom graph used in the Traversal Lab."
        )
        # Render traversal graph
        st.markdown("**Classroom Traversal Graph**")
        _render_compact_benchmark_graph(
            traversal_graph,
            title="Traversal Context",
            highlighted_vertices=["A"],
            show_edge_weights=False,
        )
        # Display BFS and DFS results
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Algorithm": "BFS",
                        "Visit Order": " -> ".join(traversal_demo.bfs_result.visit_order),
                        "Trace Rows": len(traversal_demo.bfs_result.steps),
                    },
                    {
                        "Algorithm": "DFS",
                        "Visit Order": " -> ".join(traversal_demo.dfs_result.visit_order),
                        "Trace Rows": len(traversal_demo.dfs_result.steps),
                    },
                ]
            ),
            width="stretch",
            hide_index=True,
        )
    # Render shortest path context  
    with context_tabs[2]:
        # Generate shortest path graph data
        path_vertices, path_edges = generate_positive_distance_graph_data()
        path_graph = build_graph("list", path_vertices, path_edges)
        path_result = run_shortest_path_demo("list").result
        # Render shortest path context caption
        st.caption(
            "Dijkstra and Bellman-Ford are benchmarked on positive weighted "
            "graphs so their timings are comparable. Negative-weight behavior "
            "remains in the Shortest Path Lab because Dijkstra is invalid there."
        )
        # Render shortest path graph
        st.markdown("**Positive Distance Shortest-Path Graph**")
        _render_compact_benchmark_graph(
            path_graph,
            title="Shortest Path Context",
            highlighted_path=path_result.path,
            show_edge_weights=True,
        )
        # Display shortest path results
        st.dataframe(
            run_positive_shortest_path_comparison("list", repeats=1),
            width="stretch",
            hide_index=True,
        )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _record_operation()
def _record_operation(
    prefix: str,
    representation: str,
    operation: str,
    *,
    complexity: str,
    summary: str | Callable[[object | None], str],
    input_details: list[str],
    op_callable: Callable[[WeightedGraph], object | None],
    visual_vertices: list[str] | None = None,
    visual_edges: list[tuple[str, str]] | None = None,
) -> object | None:
    """Run, time, and store one manual graph operation.

    Args:
        prefix: Session-state prefix for the owning lab.
        representation: ``"list"`` or ``"matrix"``.
        operation: Operation name.
        complexity: Expected Big-O label.
        summary: Static summary or callable that formats the return value.
        input_details: Input echo lines.
        op_callable: Callable receiving the active graph.
        visual_vertices: Vertices to emphasize in before/after visuals.
        visual_edges: Edges to emphasize in before/after visuals.

    Returns:
        Operation return value.
    """
    # Get the graph from session state
    graph = _graph_for_lab(prefix, representation)
    # Check if graph is None
    if graph is None:
        return None
    # Take snapshot before operation
    before = _snapshot_graph(graph)
    # Build Graphviz dot before operation
    dot_before = build_graphviz_dot(
        graph,
        title=f"Before {operation}",
        highlighted_vertices=visual_vertices,
        highlighted_edges=visual_edges,
        show_edge_weights=True,
    )
    # Record size and order before operation
    size_before = graph.size()
    order_before = graph.order()
    # Measure elapsed time
    start = time.perf_counter()
    returned = op_callable(graph)
    elapsed = time.perf_counter() - start
    # Take snapshot after operation
    after = _snapshot_graph(graph)
    dot_after = build_graphviz_dot(
        graph,
        title=f"After {operation}",
        highlighted_vertices=visual_vertices,
        highlighted_edges=visual_edges,
        show_edge_weights=True,
    )
    # Format the summary text
    summary_text = summary(returned) if callable(summary) else summary
    # Create LabOperationResult object
    result = LabOperationResult(
        structure=graph.representation_name,
        operation=operation,
        returned_value=returned,
        elapsed_time=elapsed,
        complexity=complexity,
        size_before=size_before,
        size_after=graph.size(),
        order_before=order_before,
        order_after=graph.order(),
        summary=summary_text,
        input_details=input_details,
        state_label=graph.representation_name,
        state_before=before,
        state_after=after,
        dot_before=dot_before,
        dot_after=dot_after,
    )
    # Record the result in session state    
    result_key = f"last_{prefix}_{representation}_operation_result"
    st.session_state[result_key] = result
    return returned
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _record_paired_structure_operation()
def _record_paired_structure_operation(
    operation: str,
    *,
    section_id: str = "mutation",
    list_complexity: str,
    matrix_complexity: str,
    summary: str | Callable[[object | None], str],
    input_details: list[str],
    op_callable: Callable[[WeightedGraph], object | None],
    visual_vertices: list[str] | None = None,
    visual_edges: list[tuple[str, str]] | None = None,
) -> tuple[object | None, object | None]:
    """Run one Structure Lab operation on both graph representations.

    Args:
        operation: Operation name.
        section_id: UI section that should render the result.
        list_complexity: Expected Big-O for the adjacency-list graph.
        matrix_complexity: Expected Big-O for the adjacency-matrix graph.
        summary: Static summary or callable that formats the return value.
        input_details: Input echo lines.
        op_callable: Callable receiving the active graph.
        visual_vertices: Vertices to emphasize in before/after visuals.
        visual_edges: Edges to emphasize in before/after visuals.

    Returns:
        Return values from the list and matrix operations.
    """
    # Record the list operation
    list_returned = _record_operation(
        "structure",
        "list",
        operation,
        complexity=list_complexity,
        summary=summary,
        input_details=input_details,
        op_callable=op_callable,
        visual_vertices=visual_vertices,
        visual_edges=visual_edges,
    )
    # Record the matrix operation
    matrix_returned = _record_operation(
        "structure",
        "matrix",
        operation,
        complexity=matrix_complexity,
        summary=summary,
        input_details=input_details,
        op_callable=op_callable,
        visual_vertices=visual_vertices,
        visual_edges=visual_edges,
    )
    # Get the results from session state
    list_result = st.session_state["last_structure_list_operation_result"]
    matrix_result = st.session_state["last_structure_matrix_operation_result"]
    # Record the results in session state
    st.session_state["last_structure_operation_results"] = (list_result, matrix_result)
    st.session_state["last_structure_section"] = section_id
    # Sync the structure source state
    _sync_structure_source_state()
    # Check for warnings
    warnings: list[str] = []
    if not _return_values_match(list_returned, matrix_returned):
        warnings.append(
            "The adjacency-list and adjacency-matrix operations returned different values."
        )
    if not _structure_graphs_in_sync():
        warnings.append(
            "The adjacency-list and adjacency-matrix graphs are out of sync."
        )
    st.session_state["structure_sync_warning"] = " ".join(warnings)
    return (list_returned, matrix_returned)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_structure_section_result()
def _render_structure_section_result(section_id: str) -> None:
    """Render the last paired Structure Lab result for a matching UI section.

    Args:
        section_id: Section identifier to match.

    Returns:
        None.
    """
    # Return if the section ID doesn't match    
    if st.session_state.get("last_structure_section") != section_id:
        return
    # Get the results from session state
    result_pair = st.session_state.get("last_structure_operation_results")
    # Return if the results are None
    if result_pair is None:
        return
    list_result, matrix_result = result_pair
    render_paired_operation_result(list_result, matrix_result)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_structure_lab()
def _render_structure_lab() -> None:
    """Render the synchronized graph-structure playground.

    Returns:
        None.
    """
    # Get the graphs from session state
    list_graph = _graph_for_lab("structure", "list")
    matrix_graph = _graph_for_lab("structure", "matrix")
    controls_disabled = list_graph is None or matrix_graph is None
    # Create columns for controls and view      
    controls_col, view_col = st.columns([2, 3])
    # Render the controls
    with controls_col:
        # Render the vertex operations
        with st.container(border=True):
            st.subheader("Vertex Operations")
            vertex_label = st.text_input(
                "Vertex Label",
                value="Aspen",
                key="structure_vertex_label",
            )
            # Create columns for vertex operations            
            vertex_cols = st.columns(2)
            # Render the add vertex button
            if vertex_cols[0].button("Add Vertex", disabled=controls_disabled):
                # Record the add vertex operation
                returned = _record_paired_structure_operation(
                    "add_vertex",
                    list_complexity="O(1)",
                    matrix_complexity="O(V)",
                    summary=lambda value: f"Vertex {vertex_label} {'added' if value else 'already existed'}.",
                    input_details=[f"vertex={vertex_label}"],
                    op_callable=lambda active: active.add_vertex(vertex_label),
                    visual_vertices=[vertex_label],
                )
                # Append the result to the history
                _append_history(
                    "structure_history",
                    f"Add vertex {vertex_label}: list={returned[0]}, matrix={returned[1]}",
                )
            # Render the remove vertex button
            if vertex_cols[1].button("Remove Vertex", disabled=controls_disabled):
                # Record the remove vertex operation
                returned = _record_paired_structure_operation(
                    "remove_vertex",
                    list_complexity="O(V + E)",
                    matrix_complexity="O(V^2)",
                    summary=lambda value: f"Vertex {vertex_label} {'removed' if value else 'not found'}.",
                    input_details=[f"vertex={vertex_label}"],
                    op_callable=lambda active: active.remove_vertex(vertex_label),
                    visual_vertices=[vertex_label],
                )
                # Append the result to the history
                _append_history(
                    "structure_history",
                    f"Remove vertex {vertex_label}: list={returned[0]}, matrix={returned[1]}",
                )
        # Render the edge operations
        with st.container(border=True):
            st.subheader("Edge Operations")
            # Get the edge source from session state
            edge_source = st.text_input(
                "Edge Source",
                value="Denver",
                key="structure_edge_source",
            )
            # Get the edge target from session state
            edge_target = st.text_input(
                "Edge Target",
                value="Vail",
                key="structure_edge_target",
            )
            # Get the edge weight from session state
            edge_weight = st.number_input(
                "Edge Weight",
                value=101.0,
                step=1.0,
                key="structure_edge_weight",
            )
            # Create columns for edge operations
            edge_cols = st.columns(2)
            # Render the add/update edge button
            if edge_cols[0].button("Add/Update Edge", disabled=controls_disabled):
                returned = _record_paired_structure_operation(
                    "add_edge",
                    list_complexity="O(1)",
                    matrix_complexity="O(1)",
                    summary=lambda value: f"Edge {edge_source}->{edge_target} {'added' if value else 'updated'}.",
                    input_details=[
                        f"source={edge_source}",
                        f"target={edge_target}",
                        f"weight={edge_weight:g}",
                    ],
                    op_callable=lambda active: active.add_edge(edge_source, edge_target, edge_weight),
                    visual_vertices=[edge_source, edge_target],
                    visual_edges=[(edge_source, edge_target)],
                )
                # Append the result to the history
                _append_history(
                    "structure_history",
                    f"Add/update edge {edge_source}->{edge_target}: list={returned[0]}, matrix={returned[1]}",
                )
            # Render the remove edge button
            if edge_cols[1].button("Remove Edge", disabled=controls_disabled):
                # Record the remove edge operation
                returned = _record_paired_structure_operation(
                    "remove_edge",
                    list_complexity="O(1) average",
                    matrix_complexity="O(1)",
                    summary=lambda value: f"Edge {edge_source}->{edge_target} {'removed' if value else 'not found'}.",
                    input_details=[f"source={edge_source}", f"target={edge_target}"],
                    op_callable=lambda active: active.remove_edge(edge_source, edge_target),
                    visual_vertices=[edge_source, edge_target],
                    visual_edges=[(edge_source, edge_target)],
                )
                # Append the result to the history
                _append_history(
                    "structure_history",
                    f"Remove edge {edge_source}->{edge_target}: list={returned[0]}, matrix={returned[1]}",
                )
            # Render a divider
            st.divider()
            st.subheader("Edge Queries")
            # Create columns for edge queries
            query_cols = st.columns(2)
            # Render the has edge query
            with query_cols[0]:
                has_edge_source = st.text_input(
                    "Has Edge Source",
                    value="Denver",
                    key="structure_has_edge_source",
                )
                has_edge_target = st.text_input(
                    "Has Edge Target",
                    value="Vail",
                    key="structure_has_edge_target",
                )
                # Render the has edge button
                if st.button("Has Edge", disabled=controls_disabled):
                    # Record the has edge operation
                    returned = _record_paired_structure_operation(
                        "has_edge",
                        section_id="has_edge",
                        list_complexity="O(deg(V))",
                        matrix_complexity="O(1)",
                        summary=lambda value: f"Edge {has_edge_source}->{has_edge_target} exists: {value}.",
                        input_details=[f"source={has_edge_source}", f"target={has_edge_target}"],
                        op_callable=lambda active: active.has_edge(has_edge_source, has_edge_target),
                        visual_vertices=[has_edge_source, has_edge_target],
                        visual_edges=[(has_edge_source, has_edge_target)],
                    )
                    # Append the result to the history
                    _append_history(
                        "structure_history",
                        f"Has edge {has_edge_source}->{has_edge_target}: list={returned[0]}, matrix={returned[1]}",
                    )
            # Render the get weight query
            with query_cols[1]:
                weight_query_source = st.text_input(
                    "Weight Query Source",
                    value="Denver",
                    key="structure_weight_query_source",
                )
                weight_query_target = st.text_input(
                    "Weight Query Target",
                    value="Vail",
                    key="structure_weight_query_target",
                )
                # Render the get weight button
                if st.button("Get Weight", disabled=controls_disabled):
                    # Record the get weight operation
                    returned = _record_paired_structure_operation(
                        "get_weight",
                        section_id="get_weight",
                        list_complexity="O(deg(V))",
                        matrix_complexity="O(1)",
                        summary=lambda value: f"Weight for {weight_query_source}->{weight_query_target}: {value if value is not None else 'not found'}.",
                        input_details=[f"source={weight_query_source}", f"target={weight_query_target}"],
                        op_callable=lambda active: active.get_weight(weight_query_source, weight_query_target),
                        visual_vertices=[weight_query_source, weight_query_target],
                        visual_edges=[(weight_query_source, weight_query_target)],
                    )
                    # Append the result to the history
                    _append_history(
                        "structure_history",
                        f"Get weight {weight_query_source}->{weight_query_target}: list={returned[0]}, matrix={returned[1]}",
                    )
            # Render query results below both query columns so result cards have room.
            _render_structure_section_result("has_edge")
            _render_structure_section_result("get_weight")
        # Render the neighbor scan
        with st.container(border=True):
            st.subheader("Neighbor Scan")
            # Get the neighbor vertex from session state
            neighbor_vertex = st.text_input(
                "Neighbor Vertex",
                value="Denver",
                key="structure_neighbor_vertex",
            )
            # Render the neighbors button
            if st.button("Neighbors", disabled=controls_disabled):
                # Record the neighbors operation
                returned = _record_paired_structure_operation(
                    "neighbors",
                    section_id="neighbors",
                    list_complexity="O(deg(V))",
                    matrix_complexity="O(V)",
                    summary=lambda value: f"{neighbor_vertex} has {len(value) if isinstance(value, list) else 0} neighbors.",
                    input_details=[f"vertex={neighbor_vertex}"],
                    op_callable=lambda active: active.neighbors(neighbor_vertex),
                    visual_vertices=[neighbor_vertex],
                )
                # Append the result to the history
                _append_history(
                    "structure_history",
                    f"Neighbors {neighbor_vertex}: list={returned[0]}, matrix={returned[1]}",
                )
            # Render the neighbors result
            _render_structure_section_result("neighbors")
    # Render the view column
    with view_col:
        # Render the sync warning
        if st.session_state["structure_sync_warning"]:
            st.warning(st.session_state["structure_sync_warning"])
        # Render the mutation result
        _render_structure_section_result("mutation")
        # Render the operation history
        render_operation_history(
            "Synchronized Operation History",
            st.session_state["structure_history"],
            "No manual operations have been run yet.",
        )
        # Render the paired adjacency views
        render_paired_adjacency_views(list_graph, matrix_graph)
        # Render the graph visualization
        render_graph_visual(
            list_graph,
            title="Synchronized Graph Visualization",
            show_edge_weights=True,
        )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
#
# ==============================================================================
# MAIN APP
# ==============================================================================

render_header()

(
    tab_overview,
    tab_builder,
    tab_structure,
    tab_traversal,
    tab_shortest,
    tab_benchmark,
    tab_analysis,
    tab_guide,
) = st.tabs(
    [
        "Overview",
        "Graph Builder",
        "Graph Structure Lab",
        "Traversal Lab",
        "Shortest Path Lab",
        "Benchmark Lab",
        "Written Analysis",
        "Recommendation Guide",
    ]
)

with tab_overview:
    st.header("Project Overview")
    st.markdown(
        """
This Graph Representation and Algorithm Tool compares the following CTA-7
structures and behaviors:

- **Adjacency List** - a graph representation that stores each vertex with its
  actual neighbors, making it useful for sparse relationship data.
- **Adjacency Matrix** - a graph representation that stores a full
  vertex-by-vertex table, making direct edge checks easy to inspect.
- **BFS and DFS** - traversal algorithms that show how the same graph can be
  explored by layers or by deep path exploration.
- **Dijkstra's algorithm** - a shortest-path algorithm for graphs with
  non-negative edge weights.
- **Bellman-Ford** - a shortest-path algorithm that can handle negative edge
  weights and detect reachable negative cycles.

Use the tabs above to build deterministic graph datasets, compare graph
structures, run guided traversal and shortest-path operations, benchmark sparse
and dense workloads, and read the written analysis and recommendation guide.

### Assignment Goals

- Implement adjacency-list and adjacency-matrix graph representations
- Demonstrate vertex, edge, neighbor, and adjacency-check operations
- Implement BFS and DFS traversal algorithms
- Implement Dijkstra and Bellman-Ford shortest-path algorithms
- Compare sparse and dense graph performance across key operation groups
        """
    )

    # overview of adjacency-list graph
    st.subheader("Adjacency List")
    st.info(
        "An adjacency list stores each vertex with the vertices connected to "
        "it. That makes the structure naturally suited for sparse graphs "
        "because it stores real relationships instead of reserving space for "
        "missing edges. In this project, adjacency-list behavior is especially "
        "useful for neighbor scans, BFS, DFS, and sparse shortest-path "
        "workloads."
    )

    # overview of adjacency-matrix graph
    st.subheader("Adjacency Matrix")
    st.info(
        "An adjacency matrix stores graph connections in a square table where "
        "each row and column represents a vertex. That makes direct adjacency "
        "checks easy to reason about because the program can look up one "
        "source-target cell. The trade-off is that the matrix reserves space "
        "for every possible vertex pair, so it is best suited for dense or "
        "stable graphs where that full table is useful."
    )

    # overview of traversal algorithms
    st.subheader("BFS and DFS")
    st.info(
        "BFS and DFS both explore reachable vertices, but they organize the "
        "search differently. BFS expands outward from the start vertex in "
        "layers, which makes it useful for unweighted fewest-edge paths and "
        "level-by-level reachability. DFS follows one path deeply before "
        "backtracking, which makes it useful for connected-component "
        "exploration, dependency reasoning, and path exploration."
    )

    # overview of shortest-path algorithms
    st.subheader("Dijkstra and Bellman-Ford")
    st.info(
        "Dijkstra is the practical default when every edge weight is "
        "non-negative, such as distance, travel time, or network latency. "
        "Bellman-Ford is slower, but it is the better choice when negative "
        "edge weights can appear or when the program must detect reachable "
        "negative cycles. In this tool, shortest-path demos use edge weights "
        "to find the lowest-cost route."
    )

    # complexity overview
    st.subheader("Complexity Overview")
    st.markdown(
        """
| Operation | Adjacency List | Adjacency Matrix |
|---|---:|---:|
| Space | O(V + E) | O(V^2) |
| Add vertex | O(1) | O(V) |
| Add edge | O(1) | O(1) |
| Check adjacency | O(deg(V)) | O(1) |
| Scan neighbors | O(deg(V)) | O(V) |
| BFS / DFS | O(V + E) | O(V^2) |
| Dijkstra | O((V + E) log V) | O(V^2 log V) |
| Bellman-Ford | O(VE) | O(VE) |
        """
    )

    # key concepts
    st.subheader("Key Concepts")
    st.info(
        "**Graph density** explains why sparse graphs often favor adjacency "
        "lists, while dense graphs can make adjacency matrices more "
        "competitive.\n\n"
        "**Representation choice** means deciding whether the graph should "
        "store only real edges or reserve a full vertex-by-vertex table.\n\n"
        "**Traversal order** explains why BFS and DFS can visit the same "
        "vertices in different sequences.\n\n"
        "**Edge-weight rules** determine whether Dijkstra is valid or "
        "Bellman-Ford is required for correctness."
    )

    # how to use this tool
    st.subheader("How to Use This Tool")
    st.info(
        "Use Graph Builder to preview deterministic datasets and compare the "
        "two representations. Use Graph Structure Lab to inspect vertex, edge, "
        "adjacency, and neighbor operations. Use Traversal Lab to compare BFS "
        "and DFS visit order. Use Shortest Path Lab to compare Dijkstra and "
        "Bellman-Ford behavior. Use Benchmark Lab to measure sparse and dense "
        "performance, then read the Written Analysis and Recommendation Guide "
        "tabs to connect the results to the assignment requirements."
    )

# Build the graph
with tab_builder:
    # Render the header
    st.header("Graph Builder")
    # Render the description
    st.markdown("Create deterministic graph data and load both representations at the same time.")
    col_a, col_b = st.columns(2)
    # Render the dataset and vertex count
    with col_a:
        dataset_kind = st.selectbox(
            "Dataset",
            _BUILDER_DATASET_NAMES,
        )
    # Render the vertex count and seed
    with col_b:
        vertex_count = st.number_input(
            "Random Vertex Count",
            min_value=2,
            max_value=500,
            value=int(st.session_state["builder_vertex_count"]),
            step=1,
        )
        seed = st.number_input(
            "Random Seed",
            min_value=0,
            value=int(st.session_state["builder_seed"]),
            step=1,
        )
    # Render the generate graph button
    if st.button("Generate Graph", type="primary"):
        st.session_state["builder_vertex_count"] = int(vertex_count)
        st.session_state["builder_seed"] = int(seed)
        if dataset_kind == _TRAVERSAL_DATASET_NAME:
            vertices, edges = generate_classroom_graph_data()
            selected_directed = False
        elif dataset_kind == _STRUCTURE_DATASET_NAME:
            vertices, edges = generate_positive_weighted_positive_route_demo_graph_data()
            selected_directed = False
        elif dataset_kind == _NEGATIVE_WEIGHT_DEMO_NAME:
            vertices, edges = generate_negative_weight_cost_graph_data()
            selected_directed = True
        elif dataset_kind == _RANDOM_SPARSE_DATASET_NAME:
            vertices, edges = generate_random_graph_data(int(vertex_count), "sparse", directed=False, seed=int(seed))
            selected_directed = False
        else:
            vertices, edges = generate_random_graph_data(int(vertex_count), "dense", directed=False, seed=int(seed))
            selected_directed = False
        _load_graphs(vertices, edges, directed=selected_directed)
        st.session_state["dataset_name"] = dataset_kind
        st.success(f"Generated {dataset_kind} with {len(vertices)} vertices and {len(edges)} edges.")
    # Render the lab status summary
    render_lab_status_summary(
        [
            ("Dataset", str(st.session_state["dataset_name"])),
            ("Data Ready", "Yes" if _graph_data_ready() else "No"),
        ]
    )
    # Render the graph data preview
    if _graph_data_ready():
        st.subheader("Source Data Preview")
        st.code(preview_edges(st.session_state["edges"], count=12))
        render_adjacency_views(_active_graph("list"))
        render_graph_visual(
            _active_graph("list"),
            title="Generated Graph",
            show_edge_weights=_show_edge_weights_for_active_dataset(),
        )
    # Render the info message
    else:
        st.info("No graph generated yet. Use Generate Graph to load both representations.")

# -------------------------------------------------------------------------
# STRUCTURE TAB
# -------------------------------------------------------------------------
with tab_structure:
    # Render the header
    st.header("Graph Structure Lab")
    # Ensure the structure graphs are loaded
    _ensure_structure_graphs()
    # Render the quick start guide
    render_lab_quick_start(
        "Quick Start",
        [
            "Use the auto-loaded Positive Weighted Positive Route Demo",
            "Use one control set to update both representations",
            "Inspect paired results, adjacency tables, and the shared graph visual",
        ],
    )
    # Get the structure graph
    structure_graph = _graph_for_lab("structure", "list")
    # Render the lab status summary
    render_lab_status_summary(
        [
            ("Dataset", _STRUCTURE_DATASET_NAME),
            ("Vertices", f"{structure_graph.order():,}" if structure_graph is not None else "0"),
            ("Edges", f"{structure_graph.size():,}" if structure_graph is not None else "0"),
            ("Mode", "List + Matrix"),
        ],
        title="Structure Graph",
    )
    # Render the structure lab
    _render_structure_lab()
# -------------------------------------------------------------------------
# TRAVERSAL LAB
# -------------------------------------------------------------------------
with tab_traversal:
    # Render the header
    st.header("Traversal Lab")
    # Ensure the traversal graphs are loaded
    _ensure_traversal_graphs()
    # Render the quick start guide
    render_lab_quick_start(
        "Quick Start",
        [
            "Use the auto-loaded sample graph",
            "Choose Breadth-First Search (BFS) or Depth-First Search (DFS)",
            "Run traversal and inspect the frontier trace",
        ],
    )
    # Render the caption
    st.caption(
        "Breadth-First Search (BFS) and Depth-First Search (DFS) use reachability, "
        "not edge cost; traversal visuals omit unit-weight labels for the sample BFS/DFS graph."
    )
    # Get the traversal graphs
    list_graph = _graph_for_lab("traversal", "list")
    matrix_graph = _graph_for_lab("traversal", "matrix")
    # Get the vertices
    vertices = list_graph.vertices() if list_graph is not None else []
    # Get the traversal algorithm
    algorithm = st.radio(
        "Traversal Algorithm",
        ["BFS (Breadth-First Search)", "DFS (Depth-First Search)"],
        horizontal=True,
    )
    algorithm_key = "BFS" if algorithm.startswith("BFS") else "DFS"
    # Render the lab status summary
    render_lab_status_summary(
        [
            ("Dataset", _TRAVERSAL_DATASET_NAME),
            ("Vertices", f"{len(vertices):,}"),
            ("Edges", f"{list_graph.size():,}" if list_graph is not None else "0"),
            ("Mode", "List + Matrix"),
        ],
        title="Traversal Graph",
    )
    # Get the start vertex
    start_vertex = (
        st.selectbox("Start Vertex", vertices, key="traversal_start_paired")
        if vertices
        else ""
    )
    # Get the run button and demo button columns
    col_run, col_demo = st.columns(2)
    
    # Render the run button
    with col_run:
        if st.button(
            "Run Traversal",
            disabled=list_graph is None or matrix_graph is None,
            key="run_traversal_btn",
        ):
            _store_paired_traversal_results(algorithm_key, start_vertex)
            st.success(f"{algorithm_key} traversal complete. Both representations updated.")
    
    # Render the demo button
    with col_demo:
        if st.button("Run Guided Traversal Demo", key="run_guided_traversal_demo_btn"):
            demo = run_traversal_demo("list", directed=False)
            matrix_demo = run_traversal_demo("matrix", directed=False)
            st.session_state["traversal_demo_result"] = demo
            st.session_state["traversal_list_result"] = demo.bfs_result
            st.session_state["traversal_matrix_result"] = matrix_demo.bfs_result
            st.session_state["traversal_result"] = demo.bfs_result
            st.session_state["traversal_result_graph"] = list_graph
            st.success("Guided traversal demo complete.")

    st.divider()
    st.subheader("Traversal Graph Data Structures")
    # Render the paired adjacency views
    render_paired_adjacency_views(list_graph, matrix_graph)
    # Get the demo result
    demo_result = st.session_state["traversal_demo_result"]
    # Render the validation results
    if demo_result is not None:
        render_validation_results("Traversal Demo Results", demo_result.steps)
        for line in demo_result.summary_lines:
            st.info(line)

    # Get the result columns
    result_cols = st.columns(2)
    # Render the result in the first column
    with result_cols[0]:
        _render_traversal_result_section(
            "Adjacency List Representation",
            st.session_state["traversal_list_result"],
            list_graph,
        )
    # Render the result in the second column
    with result_cols[1]:
        _render_traversal_result_section(
            "Adjacency Matrix Representation",
            st.session_state["traversal_matrix_result"],
            matrix_graph,
        )

# -------------------------------------------------------------------------
# SHORTEST PATH LAB
# -------------------------------------------------------------------------
with tab_shortest:
    # Render the header
    st.header("Shortest Path Lab")
    # Render the quick start guide
    render_lab_quick_start(
        "Quick Start",
        ["Choose a graph representation", "Choose a guided shortest-path demo", "Run the guided demo and inspect relaxations"],
    )
    # Render the caption
    st.caption(
        "Guided demos show Dijkstra on positive route distances and Bellman-Ford "
        "on a directed cost graph with a negative edge."
    )
    # Get the representation and demo columns
    path_rep_col, path_demo_col = st.columns(2)
    # Get the graph choice
    with path_rep_col:
        path_graph_choice = st.radio("Representation", ["Adjacency List", "Adjacency Matrix"], horizontal=True, key="path_representation")
    # Get the representation
    path_representation = "list" if path_graph_choice == "Adjacency List" else "matrix"
    # Get the demo name
    if st.session_state["shortest_demo_name"] not in _SHORTEST_PATH_DEMOS:
        st.session_state["shortest_demo_name"] = _POSITIVE_DISTANCE_DEMO_NAME
    # Get the demo
    with path_demo_col:
        path_demo_name = st.selectbox(
            "Guided Shortest Path Demo",
            _SHORTEST_PATH_DEMOS,
            key="shortest_demo_name",
        )
    # Get the algorithm
    path_algorithm = "Dijkstra + Bellman-Ford" if path_demo_name == _POSITIVE_DISTANCE_DEMO_NAME else "Bellman-Ford"
    
    # Get the info
    if path_demo_name == _NEGATIVE_WEIGHT_DEMO_NAME:
        st.info(
            "Weights are checkout cost changes in dollars: product costs, fees, "
            "discounts, and credits. Directed means each arrow is one checkout "
            "step forward, not a Python data type. Purchase math: "
            "Start Purchase->Item Added 80 + Item Added->Cart Review 2 + "
            "Cart Review->Coupon Applied -15 + Coupon Applied->Store Credit -10 + "
            "Store Credit->Standard Shipping 6 + Standard Shipping->Payment 5 + "
            "Payment->Order Complete 1 = 69. Dijkstra requires non-negative "
            "edge weights, so this demo uses Bellman-Ford."
        )
    # Ensure the demo graphs are loaded
    _ensure_shortest_demo_graphs(str(path_demo_name))
    # Get the graph
    path_graph = _graph_for_lab("shortest", path_representation)
    path_vertices = path_graph.vertices() if path_graph is not None else []
    # Render the lab status summary
    render_lab_status_summary(
        [
            ("Demo", str(path_demo_name)),
            ("Vertices", f"{len(path_vertices):,}"),
            ("Edges", f"{path_graph.size():,}" if path_graph is not None else "0"),
            ("Algorithm", path_algorithm),
        ],
        title="Shortest Path Graph",
    )
    # Get the run button
    if st.button("Run Guided Shortest Path Demo", disabled=path_graph is None, key="run_guided_shortest_path_demo_btn"):
        # Check if the demo is the negative weight demo
        if path_demo_name == _NEGATIVE_WEIGHT_DEMO_NAME:
            demo = run_bellman_ford_demo(path_representation)
            st.session_state["shortest_comparison_df"] = None
        # Otherwise, run the demo
        else:
            demo = run_shortest_path_demo(path_representation)
            st.session_state["shortest_comparison_df"] = run_positive_shortest_path_comparison(path_representation)
        st.session_state["shortest_demo_result"] = demo
        st.session_state["shortest_path_result"] = demo.result
        st.session_state["shortest_path_result_graph"] = path_graph
        st.session_state["shortest_visual_run_id"] += 1
        st.success("Guided shortest path demo complete.")
    
    # Get the demo result
    shortest_demo = st.session_state["shortest_demo_result"]
    # Render the validation results
    if shortest_demo is not None:
        render_validation_results("Shortest Path Demo Results", shortest_demo.steps)
        for line in shortest_demo.summary_lines:
            st.info(line)
    # Get the comparison dataframe
    shortest_comparison_df = st.session_state["shortest_comparison_df"]
    # Render the comparison dataframe
    if shortest_comparison_df is not None:
        st.subheader("Positive Sparse Algorithm Comparison")
        st.caption(
            "Bellman-Ford is timed only on the positive distance graph so its "
            "runtime can be compared directly with Dijkstra."
        )
        # Render the comparison dataframe
        st.dataframe(shortest_comparison_df, width="stretch", hide_index=True)
    # Get the primary path result
    primary_path_result = st.session_state["shortest_path_result"]
    # Get the secondary path result
    secondary_path_result = shortest_demo.secondary_result if shortest_demo is not None else None
    # Get the display graph
    display_graph = st.session_state["shortest_path_result_graph"] or path_graph
    # Render the primary path result
    _render_shortest_path_result_section(primary_path_result, display_graph, path_representation)
    # Render the secondary path result
    if secondary_path_result is not None:
        _render_shortest_path_result_section(secondary_path_result, display_graph, path_representation)

# -------------------------------------------------------------------------
# BENCHMARK LAB
# -------------------------------------------------------------------------
with tab_benchmark:
    st.header("Benchmark Lab")
    # Render the quick start guide
    render_lab_quick_start(
        "Quick Start",
        [
            "Choose a preset or custom size and density set",
            "Run the representation benchmark with Dijkstra and Bellman-Ford",
            "Review winners, scaling, charts, and lab context",
        ],
    )
    # Render the caption
    st.caption(
        "Benchmark graphs are deterministic weighted sparse/dense workloads. "
        "BFS and DFS ignore weights; Dijkstra and Bellman-Ford use positive weights "
        "so their shortest-path timings are comparable."
    )
    # Render the benchmark graph gallery
    _render_benchmark_graph_gallery()
    _render_benchmark_reference_explanation()
    st.divider()
    
    # Render the preset columns
    preset_col_a, preset_col_b, preset_col_c = st.columns(3)
    # Render the preview button
    if preset_col_a.button("Preview [25, 50]", key="preview_benchmark_btn"):
        st.session_state["benchmark_sizes"] = [25, 50]
        st.session_state["benchmark_kinds"] = ["sparse"]
        st.info("Preview preset selected: sparse graphs at V=25 and V=50.")
    if preset_col_b.button("Report [25, 50, 100]", key="report_benchmark_btn"):
        st.session_state["benchmark_sizes"] = [25, 50, 100]
        st.session_state["benchmark_kinds"] = list(DEFAULT_GRAPH_KINDS)
        st.info("Report preset selected: sparse and dense graphs at V=25, V=50, and V=100.")
    if preset_col_c.button("Extended [25, 50, 100, 250, 500]", key="extended_benchmark_btn"):
        st.session_state["benchmark_sizes"] = list(DEFAULT_SIZES)
        st.session_state["benchmark_kinds"] = list(DEFAULT_GRAPH_KINDS)
        st.info("Extended preset selected. Dense shortest-path workloads may take longer.")

    # Get the configuration columns
    config_col, action_col = st.columns([3, 2])
    with config_col:
        # Get the benchmark sizes
        sizes = st.multiselect(
            "Benchmark Sizes",
            DEFAULT_SIZES,
            default=st.session_state["benchmark_sizes"],
        )
        # Get the graph kinds
        kinds = st.multiselect(
            "Graph Kinds",
            DEFAULT_GRAPH_KINDS,
            default=st.session_state["benchmark_kinds"],
        )
        # Get the number of repeats
        repeats = st.number_input(
            "Repeats per workload",
            min_value=1,
            max_value=5,
            value=int(st.session_state["benchmark_repeats"]),
            step=1,
        )
        # Get the directed benchmark
        directed_bench = st.checkbox(
            "Directed Benchmark",
            value=bool(st.session_state["benchmark_directed"]),
        )
        # Get the include bellman ford
        include_bellman_ford = st.checkbox(
            "Include Bellman-Ford shortest-path workload",
            value=bool(st.session_state["benchmark_include_bellman_ford"]),
        )
    # Get the action column
    with action_col:
        # Get the warning
        # Get the warning
        if 250 in sizes or 500 in sizes:
            st.warning(
                "Extended dense graphs can take longer because Bellman-Ford is O(VE). "
                "Use the Preview or Report preset for quick classroom runs."
            )
        # Get the run button
        run_clicked = st.button("Run Benchmark", type="primary")
        # Get the save button
        save_clicked = st.button("Save Results to CSV")
        # Get the load button
        load_clicked = st.button("Load saved CSV")
    
    # Check if the run button was clicked
    if run_clicked:
        # Get the selected sizes
        selected_sizes = sizes or [25]
        # Get the selected kinds
        selected_kinds = kinds or ["sparse"]
        # Set the session state
        st.session_state["benchmark_sizes"] = selected_sizes
        st.session_state["benchmark_kinds"] = selected_kinds
        st.session_state["benchmark_repeats"] = int(repeats)
        st.session_state["benchmark_directed"] = bool(directed_bench)
        st.session_state["benchmark_include_bellman_ford"] = bool(include_bellman_ford)
        progress = st.progress(0.0, text="Starting benchmark...")

        # -------------------------------------------------------------------------------- _benchmark_progress()
        def _benchmark_progress(done: int, total: int, label: str) -> None:
            """Update the Streamlit progress bar for benchmark workloads.

            Args:
                done: Completed workload count.
                total: Total workload count.
                label: Current workload label.

            Returns:
                None.
            """
            progress.progress(done / total, text=f"{label} ({done}/{total})")
        # --------------------------------------------------------------------------------

        # Run the benchmark
        benchmark_df = run_benchmarks(
            sizes=selected_sizes,
            graph_kinds=selected_kinds,
            repeats=int(repeats),
            seed=DEFAULT_SEED,
            directed=directed_bench,
            include_bellman_ford=include_bellman_ford,
            progress_callback=_benchmark_progress,
        )
        # Compute the scaling summary
        scaling_df = compute_operation_scaling_summary(benchmark_df)
        # Compute the winners dataframe
        winners_df = compute_operation_winners(benchmark_df)
        # Generate the charts
        chart_paths = generate_charts(benchmark_df, _CHART_DIR, winners_df=winners_df)
        # Clear the progress bar
        progress.empty()
        # Set the session state
        st.session_state["benchmark_df"] = benchmark_df
        st.session_state["operation_winners_df"] = winners_df
        st.session_state["scaling_df"] = scaling_df
        st.session_state["chart_paths"] = chart_paths
        st.session_state["benchmark_validation"] = run_benchmark_validation(benchmark_df)
        # Success message
        st.success(f"Benchmark complete. Generated {len(benchmark_df)} rows.")
    
    # Check if the save button was   clicked
    # Save the benchmark artifacts
    if save_clicked:
        _save_benchmark_artifacts()
    
    # Load the benchmark artifacts
    if load_clicked:
        _load_saved_benchmark_artifacts()   
    
    # Get the validation
    validation = st.session_state["benchmark_validation"]
    if validation is not None:
        # Render the validation results
        render_validation_results("Benchmark Validation", validation.checks)
        # Render the summary lines
        for line in validation.summary_lines:
            st.info(line)
    
    # Get the benchmark dataframe
    benchmark_df = st.session_state["benchmark_df"]
    # Get the winners dataframe
    winners_df = st.session_state["operation_winners_df"]
    # Get the scaling dataframe
    scaling_df = st.session_state["scaling_df"]
    # Render the benchmark results
    if benchmark_df is not None and not benchmark_df.empty:
        st.subheader("Benchmark Results")
        st.caption(
            "Raw timed workloads for each graph kind, representation, operation, "
            "vertex count, and edge count."
        )
        st.dataframe(_format_benchmark_display(benchmark_df), width="stretch", hide_index=True)
    # If the benchmark dataframe is empty, render the benchmark table
    else:
        render_benchmark_table(benchmark_df)

    # Render the winners dataframe
    if winners_df is not None and not winners_df.empty:
        st.subheader("Operation Winners")
        st.caption(
            "Fastest representation for each operation and size, with the runtime "
            "gap compared with the runner-up."
        )
        st.dataframe(_format_operation_winners_display(winners_df), width="stretch", hide_index=True)

    # Render the scaling dataframe
    if scaling_df is not None and not scaling_df.empty:
        st.subheader("Operation Scaling Table")
        st.caption(
            "Smallest-to-largest runtime growth for each representation and "
            "operation group."
        )
        # Render the scaling dataframe
        st.dataframe(scaling_df, width="stretch", hide_index=True)
    # Render the benchmark charts
    render_benchmark_charts(st.session_state["chart_paths"])
    # Render the benchmark context sections
    _render_benchmark_context_sections()
    # Render the benchmark table
    if benchmark_df is not None:
        # Expand the benchmark table
        with st.expander("Markdown Benchmark Table"):
            # Render the benchmark table
            st.markdown(build_benchmark_table(benchmark_df))
        # Expand the winners dataframe
        if winners_df is not None:
            # Expand the winners dataframe
            with st.expander("Markdown Operation Winners Table"):
                # Render the winners dataframe
                st.markdown(build_operation_winners_table(winners_df))
        # Expand the scaling dataframe
        if scaling_df is not None:
            # Expand the scaling dataframe
            with st.expander("Markdown Scaling Table"):
                # Render the scaling dataframe
                st.markdown(build_operation_scaling_table(scaling_df))

# Set the analysis tab
with tab_analysis:
    # Set the header
    st.header("Written Analysis")
    # Render the markdown file
    render_markdown_file(_WRITTEN_ANALYSIS_PATH)

# Set the guide tab
with tab_guide:
    st.header("Recommendation Guide")
    render_markdown_file(_RECOMMENDATION_GUIDE_PATH)

# ==============================================================================
# End of File
# ==============================================================================
