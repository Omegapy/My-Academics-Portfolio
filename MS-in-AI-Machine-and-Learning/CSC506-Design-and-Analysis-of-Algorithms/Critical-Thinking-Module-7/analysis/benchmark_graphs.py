# File: benchmark_graphs.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Benchmark engine comparing adjacency-list and adjacency-matrix graphs.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Benchmark pipeline for CTA-7 graph representations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import time

import pandas as pd
from algorithms.graph_algorithms import (
    bellman_ford_shortest_path,
    breadth_first_search,
    depth_first_search,
    dijkstra_shortest_path,
)
from algorithms.graph_protocol import WeightedGraph
from data.graph_dataset_manager import (
    DEFAULT_SEED,
    build_graph,
    generate_random_graph_data,
    graph_density,
)
from models.benchmark_record import BenchmarkRecord
from models.graph_edge import GraphEdge


DEFAULT_SIZES: list[int] = [25, 50, 100, 250, 500]
"""Default benchmark vertex counts."""

DEFAULT_GRAPH_KINDS: list[str] = ["sparse", "dense"]
"""Default benchmark density categories."""

DEFAULT_REPEATS: int = 3
"""Default number of timing repetitions."""

REPRESENTATIONS: tuple[str, str] = ("list", "matrix")
"""Representations included in the comparison."""

_REPRESENTATION_NAMES: dict[str, str] = {
    "list": "Adjacency List",
    "matrix": "Adjacency Matrix",
}

_OPERATION_GROUPS: dict[str, str] = {
    "build": "construction",
    "adjacency_check": "adjacency_queries",
    "neighbor_scan": "neighbor_scan",
    "bfs": "traversal",
    "dfs": "traversal",
    "dijkstra": "shortest_path",
    "bellman_ford": "shortest_path",
    "remove_edges": "mutation",
}

ProgressCallback = Callable[[int, int, str], None]
"""Optional callback used by Streamlit to report benchmark progress."""


# ------------------------------------------------------------------------- class BenchmarkDatasetBundle
@dataclass(frozen=True)
class BenchmarkDatasetBundle:
    """Prebuilt deterministic graph workload input.

    Args:
        vertex_count: Number of vertices.
        graph_kind: Sparse or dense workload category.
        directed: Whether generated edges are directed.
        vertices: Vertex labels.
        edges: Weighted edge list.
        adjacency_queries: Source-target pairs for adjacency checks.
        remove_edges: Edges selected for delete workloads.
    """

    vertex_count: int
    graph_kind: str
    directed: bool
    vertices: list[str]
    edges: list[GraphEdge]
    adjacency_queries: list[tuple[str, str]]
    remove_edges: list[GraphEdge]


# ------------------------------------------------------------------------- end class BenchmarkDatasetBundle


# -------------------------------------------------------------------------------- _normalize_ms()
def _normalize_ms(seconds: float) -> float:
    """Convert seconds to rounded milliseconds.

    Args:
        seconds: Elapsed seconds.

    Returns:
        Milliseconds rounded for CSV readability.
    """
    return round(seconds * 1_000.0, 6)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _normalize_avg_us()
def _normalize_avg_us(seconds: float, count: int) -> float:
    """Convert elapsed time to average microseconds per logical operation.

    Args:
        seconds: Elapsed seconds.
        count: Logical operation count.

    Returns:
        Average microseconds.
    """
    if count <= 0:
        return 0.0
    return round((seconds / count) * 1_000_000.0, 6)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _best_of_repeats()
def _best_of_repeats(callable_: Callable[[], object], repeats: int) -> float:
    """Return the fastest elapsed time from repeated runs.

    Args:
        callable_: Zero-argument workload callable.
        repeats: Number of runs.

    Returns:
        Fastest elapsed seconds.
    """
    best = float("inf")
    # MAIN ITERATION LOOP: choose the lowest timing sample to reduce noise
    for _ in range(max(repeats, 1)):
        start = time.perf_counter()
        callable_()
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    return best
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _make_bundle()
def _make_bundle(
    vertex_count: int,
    graph_kind: str,
    *,
    directed: bool,
    seed: int,
) -> BenchmarkDatasetBundle:
    """Build deterministic inputs for one benchmark size and density.

    Args:
        vertex_count: Number of vertices.
        graph_kind: Sparse or dense workload category.
        directed: Whether generated edges are directed.
        seed: Random seed.

    Returns:
        BenchmarkDatasetBundle.
    """
    vertices, edges = generate_random_graph_data(
        vertex_count,
        graph_kind,
        directed=directed,
        seed=seed + vertex_count + (17 if graph_kind == "dense" else 0),
    )
    existing_queries = [
        (edge.source, edge.target)
        for edge in edges[: max(1, min(100, len(edges)))]
    ]
    missing_queries: list[tuple[str, str]] = []
    # MAIN ITERATION LOOP: create deterministic absent self-avoiding checks
    for index in range(min(100, max(vertex_count, 1))):
        source = vertices[index % len(vertices)]
        target = vertices[(index + max(vertex_count // 2, 1)) % len(vertices)]
        if source != target and (source, target) not in existing_queries:
            missing_queries.append((source, target))
    adjacency_queries = existing_queries + missing_queries
    remove_edges = edges[: min(50, len(edges))]
    return BenchmarkDatasetBundle(
        vertex_count,
        graph_kind,
        directed,
        vertices,
        edges,
        adjacency_queries,
        remove_edges,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build()
def _build(representation: str, bundle: BenchmarkDatasetBundle) -> WeightedGraph:
    """Build a graph for a benchmark workload.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.

    Returns:
        Populated graph.
    """
    return build_graph(representation, bundle.vertices, bundle.edges, directed=bundle.directed)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _record()
def _record(
    *,
    representation: str,
    operation: str,
    graph_kind: str,
    vertex_count: int,
    edge_count: int,
    workload_count: int,
    elapsed_seconds: float,
    complexity: str,
    is_correct: bool,
    density: float,
    notes: str,
) -> BenchmarkRecord:
    """Create one benchmark record.

    Args:
        representation: Internal representation label.
        operation: Workload operation.
        graph_kind: Sparse or dense workload category.
        vertex_count: Number of vertices.
        edge_count: Number of edges.
        workload_count: Logical operation count.
        elapsed_seconds: Elapsed seconds.
        complexity: Expected Big-O label.
        is_correct: Correctness flag.
        density: Edge density.
        notes: Human-readable summary.

    Returns:
        BenchmarkRecord.
    """
    return BenchmarkRecord(
        structure=_REPRESENTATION_NAMES[representation],
        operation=operation,
        operation_group=_OPERATION_GROUPS[operation],
        graph_kind=graph_kind,
        size=vertex_count,
        edge_count=edge_count,
        workload_count=workload_count,
        time_ms=_normalize_ms(elapsed_seconds),
        avg_time_us=_normalize_avg_us(elapsed_seconds, workload_count),
        complexity=complexity,
        is_correct=is_correct,
        density=density,
        notes=notes,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _benchmark_build()
def _benchmark_build(
    representation: str,
    bundle: BenchmarkDatasetBundle,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark graph construction.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord.
    """
    elapsed = _best_of_repeats(lambda: _build(representation, bundle), repeats)
    graph = _build(representation, bundle)
    complexity = "O(V + E)" if representation == "list" else "O(V^2 + E)"
    return _record(
        representation=representation,
        operation="build",
        graph_kind=bundle.graph_kind,
        vertex_count=bundle.vertex_count,
        edge_count=len(bundle.edges),
        workload_count=bundle.vertex_count + len(bundle.edges),
        elapsed_seconds=elapsed,
        complexity=complexity,
        is_correct=graph.order() == bundle.vertex_count and graph.size() == len(bundle.edges),
        density=graph_density(bundle.vertex_count, len(bundle.edges), directed=bundle.directed),
        notes=f"Built {bundle.graph_kind} graph with {bundle.vertex_count} vertices.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _benchmark_adjacency()
def _benchmark_adjacency(
    representation: str,
    bundle: BenchmarkDatasetBundle,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark adjacency checks.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord.
    """
    graph = _build(representation, bundle)

    # -------------------------------------------------------------------------------- workload()
    def workload() -> int:
        """Count successful adjacency checks across the sampled query set.

        Returns:
            Number of source-target queries that exist in the graph.
        """
        found = 0
        # MAIN ITERATION LOOP: run the same source-target checks for each repeat
        for source, target in bundle.adjacency_queries:
            if graph.has_edge(source, target):
                found += 1
        return found
    # --------------------------------------------------------------------------------

    expected_found = sum(
        1
        for source, target in bundle.adjacency_queries
        if graph.has_edge(source, target)
    )
    elapsed = _best_of_repeats(workload, repeats)
    complexity = "O(deg(V))" if representation == "list" else "O(1)"
    return _record(
        representation=representation,
        operation="adjacency_check",
        graph_kind=bundle.graph_kind,
        vertex_count=bundle.vertex_count,
        edge_count=graph.size(),
        workload_count=len(bundle.adjacency_queries),
        elapsed_seconds=elapsed,
        complexity=complexity,
        is_correct=workload() == expected_found,
        density=graph_density(bundle.vertex_count, graph.size(), directed=bundle.directed),
        notes=f"Checked {len(bundle.adjacency_queries)} source-target pairs.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _benchmark_neighbor_scan()
def _benchmark_neighbor_scan(
    representation: str,
    bundle: BenchmarkDatasetBundle,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark scanning every vertex's neighbors.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord.
    """
    graph = _build(representation, bundle)

    # -------------------------------------------------------------------------------- workload()
    def workload() -> int:
        """Count neighbor rows returned while scanning all vertices.

        Returns:
            Total number of neighbor entries observed.
        """
        total = 0
        # MAIN ITERATION LOOP: scan each vertex's adjacency collection once
        for vertex in graph.vertices():
            total += len(graph.neighbors(vertex))
        return total
    # --------------------------------------------------------------------------------

    expected = graph.size() if graph.directed else graph.size() * 2
    elapsed = _best_of_repeats(workload, repeats)
    complexity = "O(V + E)" if representation == "list" else "O(V^2)"
    return _record(
        representation=representation,
        operation="neighbor_scan",
        graph_kind=bundle.graph_kind,
        vertex_count=bundle.vertex_count,
        edge_count=graph.size(),
        workload_count=graph.order(),
        elapsed_seconds=elapsed,
        complexity=complexity,
        is_correct=workload() == expected,
        density=graph_density(bundle.vertex_count, graph.size(), directed=bundle.directed),
        notes="Scanned all adjacency rows.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _benchmark_traversal()
def _benchmark_traversal(
    representation: str,
    bundle: BenchmarkDatasetBundle,
    repeats: int,
    *,
    algorithm: str,
) -> BenchmarkRecord:
    """Benchmark BFS or DFS traversal.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.
        repeats: Timing repetitions.
        algorithm: ``"bfs"`` or ``"dfs"``.

    Returns:
        BenchmarkRecord.
    """
    graph = _build(representation, bundle)
    start = graph.vertices()[0]
    runner = breadth_first_search if algorithm == "bfs" else depth_first_search
    elapsed = _best_of_repeats(lambda: runner(graph, start), repeats)
    result = runner(graph, start)
    complexity = "O(V + E)" if representation == "list" else "O(V^2)"
    return _record(
        representation=representation,
        operation=algorithm,
        graph_kind=bundle.graph_kind,
        vertex_count=bundle.vertex_count,
        edge_count=graph.size(),
        workload_count=len(result.visit_order),
        elapsed_seconds=elapsed,
        complexity=complexity,
        is_correct=len(result.visit_order) >= 1 and result.visit_order[0] == start,
        density=graph_density(bundle.vertex_count, graph.size(), directed=bundle.directed),
        notes=f"Visited {len(result.visit_order)} reachable vertices with {algorithm.upper()}.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _benchmark_dijkstra()
def _benchmark_dijkstra(
    representation: str,
    bundle: BenchmarkDatasetBundle,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark Dijkstra shortest path.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord.
    """
    graph = _build(representation, bundle)
    start = graph.vertices()[0]
    end = graph.vertices()[-1]
    elapsed = _best_of_repeats(lambda: dijkstra_shortest_path(graph, start, end), repeats)
    result = dijkstra_shortest_path(graph, start, end)
    complexity = "O((V + E) log V)" if representation == "list" else "O(V^2 log V)"
    is_correct = bool(result.path) and result.path[0] == start and result.path[-1] == end
    return _record(
        representation=representation,
        operation="dijkstra",
        graph_kind=bundle.graph_kind,
        vertex_count=bundle.vertex_count,
        edge_count=graph.size(),
        workload_count=graph.order() + graph.size(),
        elapsed_seconds=elapsed,
        complexity=complexity,
        is_correct=is_correct,
        density=graph_density(bundle.vertex_count, graph.size(), directed=bundle.directed),
        notes=f"Shortest path from {start} to {end} has distance {result.distance:g}.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _benchmark_bellman_ford()
def _benchmark_bellman_ford(
    representation: str,
    bundle: BenchmarkDatasetBundle,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark Bellman-Ford shortest path on positive weighted graphs.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord.
    """
    graph = _build(representation, bundle)
    start = graph.vertices()[0]
    end = graph.vertices()[-1]
    elapsed = _best_of_repeats(
        lambda: bellman_ford_shortest_path(
            graph,
            start,
            end,
            max_trace_steps=0,
        ),
        repeats,
    )
    result = bellman_ford_shortest_path(
        graph,
        start,
        end,
        max_trace_steps=0,
    )
    is_correct = (
        bool(result.path)
        and result.path[0] == start
        and result.path[-1] == end
        and not result.negative_cycle_detected
    )
    return _record(
        representation=representation,
        operation="bellman_ford",
        graph_kind=bundle.graph_kind,
        vertex_count=bundle.vertex_count,
        edge_count=graph.size(),
        workload_count=graph.order() * max(graph.size(), 1),
        elapsed_seconds=elapsed,
        complexity="O(VE)",
        is_correct=is_correct,
        density=graph_density(bundle.vertex_count, graph.size(), directed=bundle.directed),
        notes=f"Bellman-Ford path from {start} to {end} has distance {result.distance:g}.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _benchmark_remove()
def _benchmark_remove(
    representation: str,
    bundle: BenchmarkDatasetBundle,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark edge removals.

    Args:
        representation: Graph representation label.
        bundle: Benchmark input bundle.
        repeats: Timing repetitions.

    Returns:
        BenchmarkRecord.
    """

    # -------------------------------------------------------------------------------- workload()
    def workload() -> int:
        """Rebuild the graph and remove the sampled edge subset.

        Returns:
            Number of sampled edges removed from the rebuilt graph.
        """
        graph = _build(representation, bundle)
        removed = 0
        # MAIN ITERATION LOOP: remove each sampled edge from a fresh graph copy
        for edge in bundle.remove_edges:
            if graph.remove_edge(edge.source, edge.target):
                removed += 1
        return removed
    # --------------------------------------------------------------------------------

    elapsed = _best_of_repeats(workload, repeats)
    removed_count = workload()
    complexity = "O(1) average" if representation == "list" else "O(1)"
    return _record(
        representation=representation,
        operation="remove_edges",
        graph_kind=bundle.graph_kind,
        vertex_count=bundle.vertex_count,
        edge_count=len(bundle.edges),
        workload_count=max(len(bundle.remove_edges), 1),
        elapsed_seconds=elapsed,
        complexity=complexity,
        is_correct=removed_count == len(bundle.remove_edges),
        density=graph_density(bundle.vertex_count, len(bundle.edges), directed=bundle.directed),
        notes=f"Removed {removed_count} sampled edges from a rebuilt graph.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_benchmarks()
def run_benchmarks(
    *,
    sizes: list[int] | None = None,
    graph_kinds: list[str] | None = None,
    repeats: int = DEFAULT_REPEATS,
    seed: int = DEFAULT_SEED,
    directed: bool = False,
    include_bellman_ford: bool = True,
    progress_callback: ProgressCallback | None = None,
) -> pd.DataFrame:
    """Run the graph representation benchmark suite.

    Args:
        sizes: Vertex counts to benchmark.
        graph_kinds: Density categories to include.
        repeats: Timing repetitions.
        seed: Random seed.
        directed: Whether generated graphs are directed.
        include_bellman_ford: Whether to time Bellman-Ford shortest paths.
        progress_callback: Optional callback receiving completed count, total
            count, and a workload label.

    Returns:
        Benchmark results DataFrame.
    """
    selected_sizes = sizes or DEFAULT_SIZES
    selected_kinds = graph_kinds or DEFAULT_GRAPH_KINDS
    records: list[BenchmarkRecord] = []
    operations_per_representation = 8 if include_bellman_ford else 7
    total_workloads = (
        len(selected_sizes)
        * len(selected_kinds)
        * len(REPRESENTATIONS)
        * operations_per_representation
    )
    completed = 0

    # -------------------------------------------------------------------------------- _append_record()
    def _append_record(record: BenchmarkRecord) -> None:
        """Append one benchmark row and report progress.

        Args:
            record: Completed benchmark record.

        Returns:
            None.
        """
        nonlocal completed
        records.append(record)
        completed += 1
        if progress_callback is not None:
            progress_callback(
                completed,
                total_workloads,
                f"{record.graph_kind} {record.structure} {record.operation}",
            )
    # --------------------------------------------------------------------------------

    # MAIN ITERATION LOOP: expand size, density, representation, operation matrix
    for size in selected_sizes:
        for graph_kind in selected_kinds:
            bundle = _make_bundle(size, graph_kind, directed=directed, seed=seed)
            for representation in REPRESENTATIONS:
                _append_record(_benchmark_build(representation, bundle, repeats))
                _append_record(_benchmark_adjacency(representation, bundle, repeats))
                _append_record(_benchmark_neighbor_scan(representation, bundle, repeats))
                _append_record(_benchmark_traversal(representation, bundle, repeats, algorithm="bfs"))
                _append_record(_benchmark_traversal(representation, bundle, repeats, algorithm="dfs"))
                _append_record(_benchmark_dijkstra(representation, bundle, repeats))
                if include_bellman_ford:
                    _append_record(_benchmark_bellman_ford(representation, bundle, repeats))
                _append_record(_benchmark_remove(representation, bundle, repeats))

    return pd.DataFrame([record.as_dict() for record in records])
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- compute_operation_scaling_summary()
def compute_operation_scaling_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize smallest-to-largest runtime growth per operation.

    Args:
        df: Benchmark results DataFrame.

    Returns:
        Scaling summary DataFrame.
    """
    rows: list[dict[str, object]] = []
    grouped = df.groupby(["graph_kind", "structure", "operation"], sort=True)
    # MAIN ITERATION LOOP: compare smallest and largest size per group
    for (graph_kind, structure, operation), group in grouped:
        sorted_group = group.sort_values("size", kind="stable")
        first = sorted_group.iloc[0]
        last = sorted_group.iloc[-1]
        smallest_time = float(first["time_ms"])
        largest_time = float(last["time_ms"])
        rows.append(
            {
                "graph_kind": graph_kind,
                "structure": structure,
                "operation": operation,
                "smallest_size": int(first["size"]),
                "largest_size": int(last["size"]),
                "smallest_time_ms": smallest_time,
                "largest_time_ms": largest_time,
                "growth_factor": round(largest_time / smallest_time, 4)
                if smallest_time > 0
                else 0.0,
            }
        )
    return pd.DataFrame(rows)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- compute_operation_winners()
def compute_operation_winners(df: pd.DataFrame) -> pd.DataFrame:
    """Determine the fastest representation for each graph and operation.

    Args:
        df: Benchmark results DataFrame.

    Returns:
        DataFrame with one winner per graph kind, operation, and size.
    """
    if df.empty:
        return pd.DataFrame(
            columns=[
                "graph_kind",
                "operation_group",
                "operation",
                "size",
                "fastest_structure",
                "fastest_time_ms",
                "runner_up",
                "runner_up_time_ms",
                "pct_faster_than_runner_up",
                "notes",
            ]
        )
    winners: list[dict[str, object]] = []
    grouped = df.groupby(["graph_kind", "operation", "size"], sort=True)
    # MAIN ITERATION LOOP: pick the lowest runtime in each operation bucket
    for (graph_kind, operation, size), bucket in grouped:
        ranked = bucket.sort_values(["time_ms", "structure"], kind="stable").reset_index(drop=True)
        best = ranked.iloc[0]
        runner_up = ranked.iloc[1] if len(ranked) > 1 else best
        runner_up_time = float(runner_up["time_ms"])
        best_time = float(best["time_ms"])
        pct_faster = (
            round((runner_up_time - best_time) / runner_up_time * 100.0, 1)
            if runner_up_time > 0
            else 0.0
        )
        notes = (
            f"For {graph_kind} {operation} at V={int(size):,}, "
            f"{best['structure']} is fastest at {best_time:.4f} ms "
            f"({pct_faster:.1f}% faster than {runner_up['structure']})."
        )
        winners.append(
            {
                "graph_kind": str(graph_kind),
                "operation_group": str(best["operation_group"]),
                "operation": str(operation),
                "size": int(size),
                "fastest_structure": str(best["structure"]),
                "fastest_time_ms": best_time,
                "runner_up": str(runner_up["structure"]),
                "runner_up_time_ms": runner_up_time,
                "pct_faster_than_runner_up": pct_faster,
                "notes": notes,
            }
        )
    return pd.DataFrame(winners)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- save_results_csv()
def save_results_csv(df: pd.DataFrame, path: Path) -> None:
    """Save benchmark results to CSV.

    Args:
        df: Benchmark DataFrame.
        path: Destination path.

    Returns:
        None.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- save_operation_winners_csv()
def save_operation_winners_csv(df: pd.DataFrame, path: Path) -> None:
    """Save operation-winner rows to CSV.

    Args:
        df: Operation winners DataFrame.
        path: Destination path.

    Returns:
        None.
    """
    save_results_csv(df, path)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- load_results_csv()
def load_results_csv(path: Path) -> pd.DataFrame:
    """Load benchmark results from CSV.

    Args:
        path: Source path.

    Returns:
        Loaded DataFrame or an empty DataFrame when missing.
    """
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
# --------------------------------------------------------------------------------
