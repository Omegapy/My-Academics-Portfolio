# File: graph_algorithms.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Traversal helpers: BFS, DFS, deterministic neighbor ordering, and trace rows.
# - Shortest-path helpers: Dijkstra, Bellman-Ford, and adjacency display formatting.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Called by Streamlit labs, validation helpers, report generation, and benchmarks.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Graph traversal and shortest-path algorithms."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from collections import deque
import heapq
from math import inf, isinf

from algorithms.graph_protocol import WeightedGraph
from models.shortest_path_result import BellmanFordStep, DijkstraStep, ShortestPathResult
from models.traversal_result import TraversalResult, TraversalStep


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# GRAPH ALGORITHM HELPERS
# ==============================================================================
# Shared helper functions validate vertices and enforce deterministic edge order.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _validate_start()
def _validate_start(graph: WeightedGraph, vertex: str) -> str:
    """Validate a start vertex.

    Args:
        graph: Graph to inspect.
        vertex: Start vertex label.

    Returns:
        Cleaned vertex label.

    Raises:
        ValueError: If the graph does not contain the vertex.
    """
    cleaned = str(vertex).strip()
    # VALIDATION: traversal algorithms need an existing start vertex
    if cleaned not in graph.vertices():
        raise ValueError(f"Unknown start vertex: {cleaned}")
    return cleaned
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- sorted_neighbors()
def sorted_neighbors(graph: WeightedGraph, vertex: str) -> list[tuple[str, float]]:
    """Return neighbors sorted by label for deterministic algorithms.

    Args:
        graph: Graph to inspect.
        vertex: Vertex label.

    Returns:
        Alphabetically sorted neighbor pairs.
    """
    return sorted(graph.neighbors(vertex), key=lambda item: item[0])
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _relaxation_edges()
def _relaxation_edges(graph: WeightedGraph) -> list[tuple[str, str, float]]:
    """Return directed edge rows for shortest-path relaxation.

    Args:
        graph: Graph to inspect.

    Returns:
        ``(source, target, weight)`` rows in deterministic order.

    Logic:
        Undirected graph objects expose mirrored neighbors, so Bellman-Ford
        correctly relaxes both directions for an undirected edge.
    """
    rows: list[tuple[str, str, float]] = []
    # MAIN ITERATION LOOP: keep source order stable and neighbor order sorted
    for source in graph.vertices():
        # MAIN ITERATION LOOP: scan the row in vertex display order
        for target, weight in sorted_neighbors(graph, source):
            # get the indices of the source and target vertices
            rows.append((source, target, weight))
    return rows
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# TRAVERSAL ALGORITHMS
# ==============================================================================
# BFS explores level-by-level, while DFS follows each branch before backtracking.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- breadth_first_search()
def breadth_first_search(graph: WeightedGraph, start_vertex: str) -> TraversalResult:
    """Traverse a graph with breadth-first search.

    Args:
        graph: Graph to traverse.
        start_vertex: Starting vertex label.

    Returns:
        TraversalResult containing visit order and trace steps.

    Raises:
        ValueError: If the start vertex is unknown.
    """
    # VALIDATION: ensure the start vertex exists in the graph
    start = _validate_start(graph, start_vertex)
    # initialize the frontier queue with the start vertex
    frontier: deque[str] = deque([start])
    # initialize the set of discovered vertices with the start vertex
    discovered: set[str] = {start}
    # initialize the list of visited vertices
    visited: list[str] = []
    # initialize the list of traversal steps
    steps: list[TraversalStep] = [
        TraversalStep(
            1,
            f"Enqueue start vertex {start}.",
            start,
            list(frontier),
            list(visited),
            sorted(discovered),
        )
    ]
    step_number = 2
    traversed_edges: list[tuple[str, str]] = []

    # MAIN ITERATION LOOP: process vertices level by level from the queue
    while frontier:
        # remove the next oldest discovered vertex from the frontier.
        current = frontier.popleft()
        # add the current vertex to the list of visited vertices
        visited.append(current)
        # enqueue each undiscovered neighbor in deterministic label order.
        for neighbor, _weight in sorted_neighbors(graph, current):
            # VALIDATION: ensure the neighbor has not been discovered before
            if neighbor not in discovered:
                discovered.add(neighbor)
                frontier.append(neighbor)
                traversed_edges.append((current, neighbor))
        # snapshot the queue, visit order, and discovered set for the UI trace.
        steps.append(
            TraversalStep(
                step_number,
                f"Visit {current}; enqueue undiscovered neighbors.",
                current,
                list(frontier),
                list(visited),
                sorted(discovered),
                list(traversed_edges),
            )
        )
        step_number += 1

    return TraversalResult(
        algorithm="BFS",
        start_vertex=start,
        visit_order=visited,
        steps=steps,
        representation=graph.representation_name,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- depth_first_search()
def depth_first_search(graph: WeightedGraph, start_vertex: str) -> TraversalResult:
    """Traverse a graph with recursive depth-first search.

    Args:
        graph: Graph to traverse.
        start_vertex: Starting vertex label.

    Returns:
        TraversalResult containing visit order and trace steps.

    Raises:
        ValueError: If the start vertex is unknown.
    """
    start = _validate_start(graph, start_vertex)
    visited_set: set[str] = set()
    visited_order: list[str] = []
    steps: list[TraversalStep] = []
    call_stack: list[str] = []
    traversed_edges: list[tuple[str, str]] = []

    # -------------------------------------------------------------------------------- _visit()
    def _visit(vertex: str, inbound_edge: tuple[str, str] | None = None) -> None:
        """Visit one vertex and recursively visit undiscovered neighbors.

        Args:
            vertex: Vertex currently being visited.
            inbound_edge: Tree edge used to reach the vertex.

        Returns:
            None.
        """
        # add the inbound edge to the list of traversed edges
        if inbound_edge is not None:
            traversed_edges.append(inbound_edge)
        # record the current vertex and the active recursive call stack.
        visited_set.add(vertex)
        visited_order.append(vertex)
        call_stack.append(vertex)
        # append the traversal step to the list of steps
        steps.append(
            # Parameters: step_number, description, current_vertex, call_stack, visit_order, visited_set, traversed_edges
            TraversalStep(
                len(steps) + 1,
                f"Visit {vertex}; recursively explore unvisited neighbors.",
                vertex,
                list(call_stack),
                list(visited_order),
                sorted(visited_set),
                list(traversed_edges),
            )
        )
        # MAIN ITERATION LOOP: descend into each neighbor in deterministic order
        for neighbor, _weight in sorted_neighbors(graph, vertex):
            # VALIDATION: ensure the neighbor has not been discovered before
            if neighbor not in visited_set:
                # recurse only into undiscovered neighbors to avoid cycles.
                _visit(neighbor, (vertex, neighbor))
        # pop after descendants complete so the stack mirrors recursion.
        call_stack.pop()
    # --------------------------------------------------------------------------------

    # start the traversal
    _visit(start)
    return TraversalResult(
        algorithm="DFS",
        start_vertex=start,
        visit_order=visited_order,
        steps=steps,
        representation=graph.representation_name,
    )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# SHORTEST-PATH ALGORITHMS
# ==============================================================================
# Dijkstra handles non-negative weights; Bellman-Ford supports negative weights.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _ensure_non_negative_edges()
def _ensure_non_negative_edges(graph: WeightedGraph) -> None:
    """Raise when the graph contains a negative edge.

    Args:
        graph: Graph to inspect.

    Returns:
        None.

    Raises:
        ValueError: If a negative edge exists.
    """
    # MAIN ITERATION LOOP: Dijkstra cannot safely run on negative edge weights
    for edge in graph.edges():
        # VALIDATION: ensure the edge weight is non-negative
        if edge.weight < 0:
            raise ValueError("Dijkstra's algorithm requires non-negative edge weights.")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- dijkstra_shortest_path()
def dijkstra_shortest_path(
    graph: WeightedGraph,
    start_vertex: str,
    end_vertex: str,
) -> ShortestPathResult:
    """Find a shortest path with Dijkstra's algorithm.

    Args:
        graph: Graph to search.
        start_vertex: Source vertex label.
        end_vertex: Destination vertex label.

    Returns:
        ShortestPathResult containing the route, distance, and trace steps.

    Raises:
        ValueError: If either endpoint is unknown or a negative edge exists.
    """
    # VALIDATION: ensure the start and end vertices exist in the graph
    start = _validate_start(graph, start_vertex)
    end = _validate_start(graph, end_vertex)
    # VALIDATION: ensure the graph contains only non-negative edge weights
    _ensure_non_negative_edges(graph)

    # Get all vertices from the graph
    vertices = graph.vertices()
    # initialize distances to infinity
    distances: dict[str, float] = {vertex: inf for vertex in vertices}
    # initialize predecessors to None
    predecessors: dict[str, str | None] = {vertex: None for vertex in vertices}
    # set the distance of the start vertex to 0
    distances[start] = 0.0
    # initialize the priority queue with the start vertex
    queue: list[tuple[float, str]] = [(0.0, start)]
    visited: set[str] = set()
    steps: list[DijkstraStep] = []

    # MAIN ITERATION LOOP: repeatedly relax edges from the closest unvisited vertex
    while queue:
        # choose the unvisited vertex with the smallest known distance.
        current_distance, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        # stop early once the destination leaves the priority queue.
        if current == end:
            break
        # relax each outgoing edge from the current vertex.
        for neighbor, weight in sorted_neighbors(graph, current):
            if neighbor in visited:
                continue
            known_distance = distances[neighbor]
            candidate_distance = current_distance + weight
            updated = candidate_distance < known_distance
            if updated:
                # store the shorter distance and queue the neighbor.
                distances[neighbor] = candidate_distance
                predecessors[neighbor] = current
                heapq.heappush(queue, (candidate_distance, neighbor))
            # snapshot the queue and predecessor map for the trace table.
            queue_snapshot = [
                vertex
                for _distance, vertex in sorted(queue, key=lambda item: (item[0], item[1]))
                if vertex not in visited
            ]
            # append the traversal step to the list of steps    
            steps.append(
                DijkstraStep(
                    len(steps) + 1,
                    current,
                    neighbor,
                    candidate_distance,
                    known_distance,
                    updated,
                    queue_snapshot,
                    dict(predecessors),
                )
            )
    
    # reconstruct the path from the end vertex to the start vertex
    path: list[str] = []
    # VALIDATION: ensure the end vertex is reachable from the start vertex
    if not isinf(distances[end]):
        cursor: str | None = end
        # MAIN ITERATION LOOP: reconstruct by following predecessor pointers backward
        while cursor is not None:
            path.append(cursor)
            cursor = predecessors[cursor]
        path.reverse()
    # return the shortest path result
    return ShortestPathResult(
        start_vertex=start,
        end_vertex=end,
        path=path,
        distance=distances[end],
        steps=steps,
        distances=distances,
        predecessors=predecessors,
        representation=graph.representation_name,
        algorithm="Dijkstra",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- bellman_ford_shortest_path()
def bellman_ford_shortest_path(
    # Parameters: graph, start_vertex, end_vertex, max_trace_steps
    graph: WeightedGraph,
    start_vertex: str,
    end_vertex: str,
    *,
    max_trace_steps: int | None = None,
) -> ShortestPathResult:
    """Find a shortest path with Bellman-Ford's algorithm.

    Args:
        graph: Graph to search.
        start_vertex: Source vertex label.
        end_vertex: Destination vertex label.
        max_trace_steps: Optional cap for stored trace rows. The algorithm
            still computes the full result when the trace is capped.

    Returns:
        ShortestPathResult containing the route, distance, and trace steps.

    Raises:
        ValueError: If either endpoint is unknown.
    """
    # VALIDATION: ensure the start and end vertices exist in the graph
    start = _validate_start(graph, start_vertex)
    end = _validate_start(graph, end_vertex)
    # Get all vertices and edges from the graph
    vertices = graph.vertices()
    edges = _relaxation_edges(graph)
    # Initialize distances to infinity
    distances: dict[str, float] = {vertex: inf for vertex in vertices}
    predecessors: dict[str, str | None] = {vertex: None for vertex in vertices}
    # set the distance of the start vertex to 0
    distances[start] = 0.0
    # store the trace steps
    steps: list[BellmanFordStep] = []
    # flag to indicate if the trace was truncated
    trace_truncated = False
    # counter for the logical step
    logical_step = 0

    # -------------------------------------------------------------------------------- _append_step()
    def _append_step(
        # Parameters: pass_number, phase, source, target, weight, candidate_distance, known_distance, updated
        *,
        pass_number: int,
        phase: str,
        source: str,
        target: str,
        weight: float,
        candidate_distance: float,
        known_distance: float,
        updated: bool,
    ) -> None:
        """Store one Bellman-Ford trace row when within the trace cap.

        Args:
            pass_number: Main-loop or final-check pass number.
            phase: Trace phase label.
            source: Edge source.
            target: Edge target.
            weight: Edge weight.
            candidate_distance: Candidate distance through ``source``.
            known_distance: Previous target distance.
            updated: Whether relaxation changed the target.

        Returns:
            None.
        """
        nonlocal trace_truncated
        if max_trace_steps is not None and len(steps) >= max_trace_steps:
            trace_truncated = True
            return
        steps.append(
            BellmanFordStep(
                logical_step,
                pass_number,
                phase,
                source,
                target,
                weight,
                candidate_distance,
                known_distance,
                updated,
                dict(distances),
                dict(predecessors),
            )
        )
    # --------------------------------------------------------------------------------

    # MAIN ITERATION LOOP: relax every edge up to V - 1 times
    for pass_number in range(1, max(len(vertices), 1)):
        changed = False
        # Step 1: scan every directed relaxation edge for this pass.
        for source, target, weight in edges:
            known_distance = distances[target]
            candidate_distance = distances[source] + weight
            updated = not isinf(distances[source]) and candidate_distance < known_distance
            if updated:
                # Step 2: keep the shorter path and predecessor when relaxation succeeds.
                distances[target] = candidate_distance
                predecessors[target] = source
                changed = True
            logical_step += 1
            # Step 3: append the trace row, respecting the optional cap.
            _append_step(
                pass_number=pass_number,
                phase="Relax",
                source=source,
                target=target,
                weight=weight,
                candidate_distance=candidate_distance,
                known_distance=known_distance,
                updated=updated,
            )
        # OPTIMIZATION: stop once a full pass produces no shorter paths
        if not changed:
            break

    negative_cycle_edges: list[tuple[str, str]] = []
    final_check_pass = max(len(vertices), 1)
    # SAFETY CHECK: one more edge scan detects reachable negative-weight cycles
    for source, target, weight in edges:
        # Step 1: a still-improving edge means a reachable negative cycle exists.
        known_distance = distances[target]
        candidate_distance = distances[source] + weight
        updated = not isinf(distances[source]) and candidate_distance < known_distance
        if updated:
            negative_cycle_edges.append((source, target))
        logical_step += 1
        # Step 2: store cycle-check trace state for explanation in the UI.
        _append_step(
            # Parameters: pass_number, phase, source, target, weight, candidate_distance, known_distance, updated
            pass_number=final_check_pass,
            phase="Cycle Check",
            source=source,
            target=target,
            weight=weight,
            candidate_distance=candidate_distance,
            known_distance=known_distance,
            updated=updated,
        )

    path: list[str] = []
    distance = inf if negative_cycle_edges else distances[end]
    if not negative_cycle_edges and not isinf(distances[end]):
        cursor: str | None = end
        seen: set[str] = set()
        # MAIN ITERATION LOOP: reconstruct by following predecessor pointers backward
        while cursor is not None and cursor not in seen:
            seen.add(cursor)
            path.append(cursor)
            cursor = predecessors[cursor]
        # reverse the path
        path.reverse()
    # return the shortest path result
    return ShortestPathResult(
        start_vertex=start,
        end_vertex=end,
        path=path,
        distance=distance,
        steps=steps,
        distances=distances,
        predecessors=predecessors,
        representation=graph.representation_name,
        algorithm="Bellman-Ford",
        negative_cycle_detected=bool(negative_cycle_edges),
        negative_cycle_edges=negative_cycle_edges,
        trace_truncated=trace_truncated,
    )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# ADJACENCY DISPLAY FORMATTERS
# ==============================================================================
# Convert graph structure into table-friendly rows without mutating the graph.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_adjacency_list()
def format_adjacency_list(graph: WeightedGraph) -> list[str]:
    """Format graph connections as adjacency-list text rows.

    Args:
        graph: Graph to format.

    Returns:
        List of display rows.
    """
    rows: list[str] = []
    # MAIN ITERATION LOOP: render one vertex and its neighbors per row
    for vertex in graph.vertices():
        # get the neighbors of the current vertex
        neighbors = graph.neighbors(vertex)
        if not neighbors:
            rows.append(f"{vertex}: (none)")
        else:
            # MAIN ITERATION LOOP: format each neighbor and its weight
            links = ", ".join(f"{neighbor} ({weight:g})" for neighbor, weight in neighbors)
            rows.append(f"{vertex}: {links}")
    return rows
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- format_adjacency_matrix()
def format_adjacency_matrix(graph: WeightedGraph) -> list[dict[str, object]]:
    """Format graph connections as adjacency-matrix rows.

    Args:
        graph: Graph to format.

    Returns:
        List of row dictionaries.
    """
    vertices = graph.vertices()
    rows: list[dict[str, object]] = []
    # MAIN ITERATION LOOP: build one dictionary per matrix row
    for source in vertices:
        # get the weight of the edge between source and target
        row: dict[str, object] = {"Vertex": source}
        # MAIN ITERATION LOOP: get the weight of the edge between source and target
        for target in vertices:
            weight = graph.get_weight(source, target)
            row[target] = "-" if weight is None else weight
        rows.append(row)
    return rows
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
