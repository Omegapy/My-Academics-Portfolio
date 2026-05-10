# File: lab_validation.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Guided validation helpers for CTA-7 Streamlit labs.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Validation dataclasses store expected/actual lab outcomes.
# - Demo functions exercise traversal, shortest-path, and benchmark workflows.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by Streamlit tabs to show ready-made validation and correctness checks.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Guided demo and validation helpers for CTA-7."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from collections.abc import Callable
from dataclasses import dataclass
import time

import pandas as pd
# Import graph algorithms
from algorithms.graph_algorithms import (
    bellman_ford_shortest_path,
    breadth_first_search,
    depth_first_search,
    dijkstra_shortest_path,
)
# Import graph dataset manager
from data.graph_dataset_manager import (
    build_graph,
    generate_classroom_graph_data,
    generate_negative_weight_cost_graph_data,
    generate_positive_distance_graph_data,
)
# Import shortest path result
from models.shortest_path_result import ShortestPathResult
# Import traversal result
from models.traversal_result import TraversalResult


# ______________________________________________________________________________
# Class Definitions - Data Classes
# ==============================================================================
# VALIDATION RESULT DATA MODELS
# ==============================================================================
# Immutable models keep demo outputs consistent between Streamlit and tests.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class ValidationStepResult
@dataclass(frozen=True)
class ValidationStepResult:
    """One validation table row.

    Args:
        step_name: Short validation label.
        expected: Expected result.
        actual: Observed result.
        passed: Whether the check passed.
        notes: Optional supporting text.
    """

    step_name: str
    expected: str
    actual: str
    passed: bool
    notes: str = ""

    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return a table-friendly dictionary.

        Returns:
            Dictionary representation of the validation step.
        """
        return {
            "Step": self.step_name,
            "Expected": self.expected,
            "Actual": self.actual,
            "Passed": "PASS" if self.passed else "CHECK",
            "Notes": self.notes,
        }
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class ValidationStepResult


# ------------------------------------------------------------------------- class TraversalDemoResult
@dataclass(frozen=True)
class TraversalDemoResult:
    """Guided traversal demo result.

    Args:
        bfs_result: BFS trace result.
        dfs_result: DFS trace result.
        steps: Validation rows.
        summary_lines: Summary bullets.
    """

    bfs_result: TraversalResult
    dfs_result: TraversalResult
    steps: list[ValidationStepResult]
    summary_lines: list[str]


# ------------------------------------------------------------------------- end class TraversalDemoResult


# ------------------------------------------------------------------------- class ShortestPathDemoResult
@dataclass(frozen=True)
class ShortestPathDemoResult:
    """Guided shortest-path demo result.

    Args:
        result: Shortest-path result.
        steps: Validation rows.
        summary_lines: Summary bullets.
        secondary_result: Optional second shortest-path result for demos that
            compare algorithms on the same graph.
    """

    result: ShortestPathResult
    steps: list[ValidationStepResult]
    summary_lines: list[str]
    secondary_result: ShortestPathResult | None = None


# ------------------------------------------------------------------------- end class ShortestPathDemoResult


# ------------------------------------------------------------------------- class BenchmarkValidationResult
@dataclass(frozen=True)
class BenchmarkValidationResult:
    """Benchmark validation result.

    Args:
        checks: Validation rows.
        summary_lines: Summary bullets.
        meets_assignment_requirement: Whether all checks passed.
    """

    checks: list[ValidationStepResult]
    summary_lines: list[str]
    meets_assignment_requirement: bool


# ------------------------------------------------------------------------- end class BenchmarkValidationResult


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# GUIDED LAB DEMOS
# ==============================================================================
# Build rubric-friendly demo data for traversal and shortest-path Streamlit tabs.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- run_traversal_demo()
def run_traversal_demo(representation: str = "list", *, directed: bool = False) -> TraversalDemoResult:
    """Run the guided BFS/DFS classroom demo.

    Args:
        representation: Graph representation label.
        directed: Whether to use directed edges.

    Returns:
        TraversalDemoResult.
    """
    vertices, edges = generate_classroom_graph_data()
    graph = build_graph(representation, vertices, edges, directed=directed)
    bfs_result = breadth_first_search(graph, "A")
    dfs_result = depth_first_search(graph, "A")
    # Validation steps for BFS/DFS
    steps = [
        ValidationStepResult("BFS starts at A", "A", bfs_result.visit_order[0], bfs_result.visit_order[0] == "A"),
        ValidationStepResult("BFS reaches all vertices", "8", str(len(bfs_result.visit_order)), len(bfs_result.visit_order) == 8),
        ValidationStepResult("DFS starts at A", "A", dfs_result.visit_order[0], dfs_result.visit_order[0] == "A"),
        ValidationStepResult("DFS reaches all vertices", "8", str(len(dfs_result.visit_order)), len(dfs_result.visit_order) == 8),
    ]
    # Return the traversal demo result
    return TraversalDemoResult(
        bfs_result=bfs_result,
        dfs_result=dfs_result,
        steps=steps,
        summary_lines=[
            f"BFS order: {', '.join(bfs_result.visit_order)}",
            f"DFS order: {', '.join(dfs_result.visit_order)}",
        ],
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_shortest_path_demo()
def run_shortest_path_demo(
    representation: str = "list",
    *,
    graph_kind: str = "positive",
    directed: bool = False,
) -> ShortestPathDemoResult:
    """Run the guided positive-distance Dijkstra route demo.

    Args:
        representation: Graph representation label.
        graph_kind: Compatibility argument; the guided demo always uses the
            positive sparse distance graph.
        directed: Whether to use directed edges.

    Returns:
        ShortestPathDemoResult.
    """
    _ = graph_kind
    vertices, edges = generate_positive_distance_graph_data()
    graph = build_graph(representation, vertices, edges, directed=directed)
    result = dijkstra_shortest_path(graph, "Denver", "Vail")
    bellman_result = bellman_ford_shortest_path(graph, "Denver", "Vail")
    # Validation steps for Dijkstra/Bellman-Ford
    steps = [
        ValidationStepResult("Path starts correctly", "Denver", result.path[0] if result.path else "None", bool(result.path) and result.path[0] == "Denver"),
        ValidationStepResult("Path ends correctly", "Vail", result.path[-1] if result.path else "None", bool(result.path) and result.path[-1] == "Vail"),
        ValidationStepResult("Optimal distance", "139", f"{result.distance:g}", result.distance == 139.0),
        ValidationStepResult("Bellman-Ford path matches", result.path_label(), bellman_result.path_label(), bellman_result.path == result.path),
        ValidationStepResult("Bellman-Ford distance matches", f"{result.distance:g}", f"{bellman_result.distance:g}", bellman_result.distance == result.distance),
    ]
    # Return the shortest path demo result
    return ShortestPathDemoResult(
        result=result,
        steps=steps,
        summary_lines=[
            "Positive sparse distance graph",
            "Route: Denver to Vail",
            f"Shortest path: {result.path_label()}",
            f"Total distance: {result.distance:g}",
            f"Bellman-Ford path: {bellman_result.path_label()}",
            f"Bellman-Ford distance: {bellman_result.distance:g}",
        ],
        secondary_result=bellman_result,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_bellman_ford_demo()
def run_bellman_ford_demo(representation: str = "list") -> ShortestPathDemoResult:
    """Run the guided Bellman-Ford negative-weight cost demo.

    Args:
        representation: Graph representation label.

    Returns:
        ShortestPathDemoResult.
    """
    vertices, edges = generate_negative_weight_cost_graph_data()
    graph = build_graph(representation, vertices, edges, directed=True)
    result = bellman_ford_shortest_path(graph, "Start Purchase", "Order Complete")
    # Validation steps for Bellman-Ford
    steps = [
        ValidationStepResult("Path starts correctly", "Start Purchase", result.path[0] if result.path else "None", bool(result.path) and result.path[0] == "Start Purchase"),
        ValidationStepResult("Path ends correctly", "Order Complete", result.path[-1] if result.path else "None", bool(result.path) and result.path[-1] == "Order Complete"),
        ValidationStepResult("Optimal purchase cost", "69", f"{result.distance:g}", result.distance == 69.0),
        ValidationStepResult("Negative cycle check", "No cycle", str(result.negative_cycle_detected), not result.negative_cycle_detected),
    ]
    # Return the shortest path demo result
    return ShortestPathDemoResult(
        result=result,
        steps=steps,
        summary_lines=[
            "Purchase cost graph",
            "Weights are checkout cost changes in dollars.",
            "Directed edges follow the one-way checkout sequence.",
            "Bellman-Ford computes product costs, fees, discounts, and credits.",
            f"Bellman-Ford path: {result.path_label()}",
            "Cost math: Start Purchase->Item Added 80 + Item Added->Cart Review 2 + Cart Review->Coupon Applied -15 + Coupon Applied->Store Credit -10 + Store Credit->Standard Shipping 6 + Standard Shipping->Payment 5 + Payment->Order Complete 1 = 69",
            f"Total purchase cost: ${result.distance:g}",
        ],
    )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# TIMING AND COMPARISON HELPERS
# ==============================================================================
# Compare shortest-path algorithms while keeping timing noise low.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _best_shortest_path_timing()
def _best_shortest_path_timing(
    runner: Callable[[], ShortestPathResult],
    repeats: int,
) -> tuple[ShortestPathResult, float]:
    """Return a shortest-path result and fastest elapsed runtime.

    Args:
        runner: Zero-argument shortest-path callable.
        repeats: Number of timing attempts.

    Returns:
        Shortest-path result and best elapsed milliseconds.
    """
    result = runner()
    best_elapsed = float("inf")
    # MAIN ITERATION LOOP: use the fastest sample to reduce UI timing noise
    for _index in range(max(repeats, 1)):
        # Step 1: run the shortest-path callable once.
        start = time.perf_counter()
        result = runner()
        elapsed = time.perf_counter() - start
        # Step 2: keep the best elapsed sample for the comparison table.
        best_elapsed = min(best_elapsed, elapsed)
    return result, round(best_elapsed * 1_000.0, 6)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_positive_shortest_path_comparison()
def run_positive_shortest_path_comparison(
    representation: str = "list",
    *,
    repeats: int = 3,
) -> pd.DataFrame:
    """Compare Dijkstra and Bellman-Ford on the positive distance graph.

    Args:
        representation: Graph representation label.
        repeats: Number of timing attempts per algorithm.

    Returns:
        DataFrame with algorithm, route, distance, trace, timing, and correctness.
    """
    vertices, edges = generate_positive_distance_graph_data()
    graph = build_graph(representation, vertices, edges, directed=False)
    expected_path = "Denver -> Boulder -> Vail"
    expected_distance = 139.0
    # Run the timing loop for each algorithm
    dijkstra_result, dijkstra_ms = _best_shortest_path_timing(
        lambda: dijkstra_shortest_path(graph, "Denver", "Vail"),
        repeats,
    )
    # Run the timing loop for each algorithm
    bellman_result, bellman_ms = _best_shortest_path_timing(
        lambda: bellman_ford_shortest_path(graph, "Denver", "Vail"),
        repeats,
    )
    # Create the comparison table
    rows = [
        # Compare Dijkstra and Bellman-Ford on the positive distance graph
        {
            "Algorithm": "Dijkstra",
            "Path": dijkstra_result.path_label(),
            "Distance": dijkstra_result.distance,
            "Trace Rows": len(dijkstra_result.steps),
            "Best Time (ms)": dijkstra_ms,
            "Correct": dijkstra_result.path_label() == expected_path and dijkstra_result.distance == expected_distance,
        },
        # Compare Dijkstra and Bellman-Ford on the positive distance graph
        {
            "Algorithm": "Bellman-Ford",
            "Path": bellman_result.path_label(),
            "Distance": bellman_result.distance,
            "Trace Rows": len(bellman_result.steps),
            "Best Time (ms)": bellman_ms,
            "Correct": bellman_result.path_label() == expected_path and bellman_result.distance == expected_distance,
        },
    ]
    return pd.DataFrame(rows)
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# BENCHMARK VALIDATION
# ==============================================================================
# Translate benchmark DataFrames into simple pass/check rows for the UI.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- run_benchmark_validation()
def run_benchmark_validation(df: pd.DataFrame) -> BenchmarkValidationResult:
    """Validate benchmark results for rubric-friendly output.

    Args:
        df: Benchmark DataFrame.

    Returns:
        BenchmarkValidationResult.
    """
    checks = [
        ValidationStepResult("Benchmark rows", "At least one row", str(len(df)), len(df) > 0),
        ValidationStepResult("Representations", "List and Matrix", ", ".join(sorted(df["structure"].unique())) if not df.empty else "-", {"Adjacency List", "Adjacency Matrix"}.issubset(set(df["structure"].unique())) if not df.empty else False),
        ValidationStepResult("Operations", "Core operations including Bellman-Ford", str(df["operation"].nunique()) if not df.empty else "0", df["operation"].nunique() >= 8 if not df.empty else False),
        ValidationStepResult("Correctness", "All rows correct", str(bool(df["is_correct"].all())) if not df.empty else "False", bool(df["is_correct"].all()) if not df.empty else False),
    ]
    return BenchmarkValidationResult(
        checks=checks,
        summary_lines=[
            f"Generated {len(df)} benchmark rows.",
            "Adjacency list and adjacency matrix workloads were both included.",
        ],
        meets_assignment_requirement=all(check.passed for check in checks),
    )
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
