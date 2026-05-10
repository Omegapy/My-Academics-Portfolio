# File: graph_dataset_manager.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Factory helpers create list-backed or matrix-backed graph instances.
# - Dataset helpers provide classroom, route, negative-weight, and random graphs.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by Streamlit tabs, validation demos, report charts, and benchmarks.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset generation and graph construction helpers."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

import random

from graph_algorithms_module.algorithms.adjacency_list_graph import AdjacencyListGraph
from graph_algorithms_module.algorithms.adjacency_matrix_graph import AdjacencyMatrixGraph
from graph_algorithms_module.algorithms.graph_protocol import WeightedGraph
from graph_algorithms_module.models.graph_edge import GraphEdge

# ______________________________________________________________________________
#
# ==============================================================================
# DATASET CONSTANTS
# ==============================================================================

DEFAULT_SEED: int = 506
"""Default deterministic seed used by graph generators."""

REPRESENTATION_LABELS: tuple[str, str] = ("list", "matrix")
"""Supported internal representation labels."""


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# GRAPH FACTORY HELPERS
# ==============================================================================
# Build concrete graph objects behind the shared WeightedGraph protocol.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- create_graph()
def create_graph(representation: str, *, directed: bool = False) -> WeightedGraph:
    """Create an empty graph by representation label.

    Args:
        representation: ``"list"`` or ``"matrix"``.
        directed: Whether to build a directed graph.

    Returns:
        Empty graph instance.

    Raises:
        ValueError: If the representation label is unknown.
    """
    normalized = representation.strip().lower()
    # DISPATCH: pick the requested graph representation
    if normalized in {"list", "adjacency list", "adjacency_list"}:
        return AdjacencyListGraph(directed=directed)
    if normalized in {"matrix", "adjacency matrix", "adjacency_matrix"}:
        return AdjacencyMatrixGraph(directed=directed)
    raise ValueError(f"Unknown graph representation: {representation!r}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_graph()
def build_graph(
    representation: str,
    vertices: list[str],
    edges: list[GraphEdge],
    *,
    directed: bool = False,
) -> WeightedGraph:
    """Build a graph from vertices and edges.

    Args:
        representation: ``"list"`` or ``"matrix"``.
        vertices: Vertex labels to add in display order.
        edges: Weighted edges to add.
        directed: Whether to build a directed graph.

    Returns:
        Populated graph instance.
    """
    graph = create_graph(representation, directed=directed)
    # MAIN ITERATION LOOP: add vertices first to preserve display order
    for vertex in vertices:
        graph.add_vertex(vertex)
    # MAIN ITERATION LOOP: add edges to build the graph structure
    for edge in edges:
        graph.add_edge(edge.source, edge.target, edge.weight)
    return graph
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# DETERMINISTIC CLASSROOM DATASETS
# ==============================================================================
# Curated graph fixtures support traversal, routing, and negative-weight demos.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- generate_classroom_graph_data()
def generate_classroom_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return the small A-H traversal graph from the course examples.

    Returns:
        Tuple of vertices and weighted edges.
    """
    vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
    edges = [
        GraphEdge("A", "B", 1.0),
        GraphEdge("A", "D", 1.0),
        GraphEdge("B", "E", 1.0),
        GraphEdge("B", "F", 1.0),
        GraphEdge("C", "F", 1.0),
        GraphEdge("C", "G", 1.0),
        GraphEdge("E", "F", 1.0),
        GraphEdge("G", "H", 1.0),
    ]
    return vertices, edges
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_sparse_city_graph_data()
def generate_sparse_city_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return a sparse weighted Colorado city graph for distance demos.

    Returns:
        Tuple of vertices and weighted edges.
    """
    vertices = [
        "Denver",
        "Boulder",
        "Fort Collins",
        "Colorado Springs",
        "Pueblo",
        "Vail",
        "Glenwood Springs",
        "Grand Junction",
    ]
    edges = [
        GraphEdge("Denver", "Boulder", 29.0),
        GraphEdge("Boulder", "Fort Collins", 58.0),
        GraphEdge("Denver", "Fort Collins", 65.0),
        GraphEdge("Denver", "Colorado Springs", 70.0),
        GraphEdge("Colorado Springs", "Pueblo", 45.0),
        GraphEdge("Denver", "Vail", 97.0),
        GraphEdge("Boulder", "Vail", 110.0),
        GraphEdge("Vail", "Fort Collins", 142.0),
        GraphEdge("Pueblo", "Vail", 190.0),
        GraphEdge("Vail", "Glenwood Springs", 60.0),
        GraphEdge("Glenwood Springs", "Grand Junction", 87.0),
        GraphEdge("Grand Junction", "Pueblo", 280.0),
    ]
    return vertices, edges
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_positive_distance_graph_data()
def generate_positive_distance_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return the positive-weight sparse distance graph for shortest paths.

    Returns:
        Tuple of vertices and non-negative weighted edges.
    """
    vertices, edges = generate_sparse_city_graph_data()
    positive_edges = [
        edge
        # MAIN ITERATION LOOP: filter out negative weight edges for Dijkstra's algorithm
        for edge in edges
        if not (
            edge.source == "Denver"
            and edge.target == "Vail"
            and edge.weight == 97.0
        )
    ]
    return vertices, positive_edges
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_dense_city_graph_data()
def generate_dense_city_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return a dense weighted Colorado city graph for Dijkstra demos.

    Returns:
        Tuple of vertices and weighted edges.
    """
    vertices, sparse_edges = generate_sparse_city_graph_data()
    dense_edges = [
        GraphEdge("Boulder", "Colorado Springs", 95.0),
        GraphEdge("Boulder", "Grand Junction", 225.0),
        GraphEdge("Colorado Springs", "Fort Collins", 125.0),
        GraphEdge("Colorado Springs", "Grand Junction", 260.0),
        GraphEdge("Colorado Springs", "Glenwood Springs", 210.0),
        GraphEdge("Denver", "Glenwood Springs", 175.0),
        GraphEdge("Fort Collins", "Glenwood Springs", 205.0),
        GraphEdge("Fort Collins", "Grand Junction", 260.0),
        GraphEdge("Grand Junction", "Vail", 150.0),
        GraphEdge("Pueblo", "Boulder", 145.0),
        GraphEdge("Pueblo", "Fort Collins", 175.0),
        GraphEdge("Pueblo", "Glenwood Springs", 230.0),
    ]
    return vertices, sparse_edges + dense_edges
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_positive_weighted_positive_route_demo_graph_data()
def generate_positive_weighted_positive_route_demo_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return the positive weighted Colorado route demo graph.

    Returns:
        Tuple of vertices and weighted edges.
    """
    return generate_sparse_city_graph_data()
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_negative_weight_cost_graph_data()
def generate_negative_weight_cost_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return a directed purchase cost graph with discount edges.

    Returns:
        Tuple of vertices and weighted directed edges.
    """
    vertices = [
        "Start Purchase",
        "Item Added",
        "Cart Review",
        "Coupon Applied",
        "Store Credit",
        "Standard Shipping",
        "Payment",
        "Order Complete",
    ]
    edges = [
        GraphEdge("Start Purchase", "Item Added", 80.0),
        GraphEdge("Item Added", "Cart Review", 2.0),
        GraphEdge("Cart Review", "Coupon Applied", -15.0),
        GraphEdge("Coupon Applied", "Store Credit", -10.0),
        GraphEdge("Store Credit", "Standard Shipping", 6.0),
        GraphEdge("Standard Shipping", "Payment", 5.0),
        GraphEdge("Payment", "Order Complete", 1.0),
        GraphEdge("Cart Review", "Standard Shipping", 6.0),
        GraphEdge("Coupon Applied", "Standard Shipping", 6.0),
        GraphEdge("Item Added", "Standard Shipping", 18.0),
    ]
    return vertices, edges
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_bellman_ford_graph_data()
def generate_bellman_ford_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return a directed negative-edge graph for Bellman-Ford demos.

    Returns:
        Tuple of vertices and weighted directed edges.
    """
    return generate_negative_weight_cost_graph_data()
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_negative_cycle_graph_data()
def generate_negative_cycle_graph_data() -> tuple[list[str], list[GraphEdge]]:
    """Return a directed graph with a reachable negative-weight cycle.

    Returns:
        Tuple of vertices and weighted directed edges.
    """
    vertices = ["A", "B", "C", "D"]
    edges = [
        GraphEdge("A", "B", 8.0),
        GraphEdge("B", "C", 2.0),
        GraphEdge("C", "D", -6.0),
        GraphEdge("D", "B", 1.0),
    ]
    return vertices, edges
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# RANDOM GRAPH GENERATION HELPERS
# ==============================================================================
# Deterministic pseudo-random datasets support sparse/dense benchmark scenarios.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _max_edge_count()
def _max_edge_count(vertex_count: int, *, directed: bool) -> int:
    """Return the maximum simple-graph edge count.

    Args:
        vertex_count: Number of vertices.
        directed: Whether the graph is directed.

    Returns:
        Maximum possible edge count without self-loops.
    """
    if directed:
        return vertex_count * max(vertex_count - 1, 0)
    return vertex_count * max(vertex_count - 1, 0) // 2
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _edge_key()
def _edge_key(source: str, target: str, *, directed: bool) -> tuple[str, str]:
    """Return the duplicate-check key for an edge.

    Args:
        source: Source vertex label.
        target: Target vertex label.
        directed: Whether edge direction is part of identity.

    Returns:
        Normalized two-label edge key.
    """
    if directed:
        return (source, target)
    first, second = sorted((source, target))
    return (first, second)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_random_graph_data()
def generate_random_graph_data(
    vertex_count: int,
    graph_kind: str,
    *,
    directed: bool = False,
    seed: int | None = DEFAULT_SEED,
) -> tuple[list[str], list[GraphEdge]]:
    """Generate a deterministic sparse or dense weighted graph.

    Args:
        vertex_count: Number of vertices to generate.
        graph_kind: ``"sparse"`` or ``"dense"``.
        directed: Whether edge directions matter.
        seed: Random seed.

    Returns:
        Tuple of vertices and weighted edges.

    Raises:
        ValueError: If vertex count or graph kind is invalid.
    """
    # VALIDATION: benchmarks and UI controls use positive graph sizes
    if vertex_count < 1:
        raise ValueError("vertex_count must be at least 1.")
    kind = graph_kind.strip().lower()
    # VALIDATION: graph kind must be 'sparse' or 'dense'
    if kind not in {"sparse", "dense"}:
        raise ValueError("graph_kind must be 'sparse' or 'dense'.")
    # set the random seed for reproducibility
    rng = random.Random(seed)
    # generate the vertices
    vertices = [f"V{i + 1:03d}" for i in range(vertex_count)]
    max_edges = _max_edge_count(vertex_count, directed=directed)
    # MAIN ITERATION LOOP: return vertices if max_edges is 0    
    if max_edges == 0:
        return vertices, []
    
    # calculate the number of edges to generate based on graph kind
    sparse_extra_edges = max(1, vertex_count // 4)
    target_edges = min(max_edges, max(vertex_count - 1, (vertex_count - 1) + sparse_extra_edges))
    # adjust target_edges for dense graphs
    if kind == "dense":
        dense_floor = (max_edges * 3 + 4) // 5
        target_edges = min(max_edges, max(vertex_count - 1, target_edges + 1, dense_floor))

    edges: list[GraphEdge] = []
    used_edges: set[tuple[str, str]] = set()

    # Step 1: add a deterministic backbone so V001 can reach every later vertex.
    for index in range(vertex_count - 1):
        source = vertices[index]
        target = vertices[index + 1]
        used_edges.add(_edge_key(source, target, directed=directed))
        edges.append(GraphEdge(source, target, float(rng.randint(1, 25))))

    candidates: list[tuple[str, str]] = []
    # MAIN ITERATION LOOP: enumerate every allowed simple edge candidate
    for source_index, source in enumerate(vertices):
        # MAIN ITERATION LOOP: iterate through target vertices
        for target_index, target in enumerate(vertices):
            if source == target:
                continue
            if not directed and target_index <= source_index:
                continue
            if _edge_key(source, target, directed=directed) in used_edges:
                continue
            candidates.append((source, target))
    rng.shuffle(candidates)

    # Step 2: add shuffled extra edges until the sparse/dense target is reached.
    for source, target in candidates[: max(target_edges - len(edges), 0)]:
        used_edges.add(_edge_key(source, target, directed=directed))
        edges.append(GraphEdge(source, target, float(rng.randint(1, 25))))
    return vertices, edges
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# DATASET DISPLAY AND METRIC HELPERS
# ==============================================================================
# Summaries and density calculations keep UI and reports consistent.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- preview_edges()
def preview_edges(edges: list[GraphEdge], *, count: int = 10) -> str:
    """Return a compact edge preview string.

    Args:
        edges: Edges to preview.
        count: Maximum rows to include before the summary.

    Returns:
        Multi-line preview string.
    """
    # VALIDATION: empty edge sets get an explicit placeholder
    if not edges:
        return "(no edges)"
    lines = [
        f"  {edge.source} -> {edge.target} (weight={edge.weight:g})"
        for edge in edges[:count]
    ]
    if len(edges) > count:
        lines.append(f"  ... ({len(edges)} edges total)")
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- graph_density()
def graph_density(vertex_count: int, edge_count: int, *, directed: bool) -> float:
    """Compute graph edge density.

    Args:
        vertex_count: Number of vertices.
        edge_count: Number of edges.
        directed: Whether the graph is directed.

    Returns:
        Density in the range 0.0 to 1.0.
    """
    max_edges = _max_edge_count(vertex_count, directed=directed)
    if max_edges == 0:
        return 0.0
    return round(edge_count / max_edges, 6)
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
