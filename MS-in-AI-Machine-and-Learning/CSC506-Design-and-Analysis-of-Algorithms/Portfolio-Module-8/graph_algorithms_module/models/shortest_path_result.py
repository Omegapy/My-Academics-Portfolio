# File: shortest_path_result.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Helper functions compact distances and predecessor maps for trace tables.
# - Dataclasses store Dijkstra steps, Bellman-Ford steps, and final path results.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Returned by shortest-path algorithms and rendered by Streamlit/report helpers.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Shortest-path result models for CTA-7 graph algorithms."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from dataclasses import dataclass, field
from math import isinf


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# SHORTEST-PATH DISPLAY HELPERS
# ==============================================================================
# Compact values keep algorithm trace tables readable in Streamlit.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _format_distance()
def _format_distance(value: float) -> float | str:
    """Return a table-friendly distance value.

    Args:
        value: Numeric distance.

    Returns:
        Distance or ``"inf"`` when the value is infinite.
    """
    return "inf" if isinf(value) else value
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _compact_predecessors()
def _compact_predecessors(predecessors: dict[str, str | None]) -> str:
    """Return a readable predecessor-map label.

    Args:
        predecessors: Vertex-to-predecessor mapping.

    Returns:
        Compact string for display tables.
    """
    compact = {
        vertex: predecessor
        for vertex, predecessor in predecessors.items()
        if predecessor is not None
    }
    return str(compact) if compact else "-"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _compact_distances()
def _compact_distances(distances: dict[str, float]) -> str:
    """Return a readable finite-distance label.

    Args:
        distances: Vertex-to-distance mapping.

    Returns:
        Compact string for display tables.
    """
    compact = {
        vertex: _format_distance(distance)
        for vertex, distance in distances.items()
        if not isinf(distance)
    }
    return str(compact) if compact else "-"
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Class Definitions - Data Classes
# ==============================================================================
# SHORTEST-PATH DATA MODELS
# ==============================================================================
# Trace rows and final results preserve classroom algorithm state.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class DijkstraStep
@dataclass(frozen=True)
class DijkstraStep:
    """Represent one Dijkstra trace row.

    Args:
        step_number: One-based step counter.
        current_vertex: Vertex currently removed from the priority queue.
        neighbor: Neighbor being relaxed, if any.
        candidate_distance: Distance through the current vertex.
        known_distance: Neighbor distance before relaxation.
        updated: Whether the relaxation updated distance/predecessor.
        queue_snapshot: Priority queue labels after the action.
        predecessor_snapshot: Current predecessor map.

    Logic:
        This row mirrors the classroom explanation of Dijkstra: dequeue the
        nearest vertex, compute an alternate path, then update when shorter.
    """

    step_number: int
    current_vertex: str
    neighbor: str
    candidate_distance: float
    known_distance: float
    updated: bool
    queue_snapshot: list[str] = field(default_factory=list)
    predecessor_snapshot: dict[str, str | None] = field(default_factory=dict)

    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return a table-friendly dictionary.

        Returns:
            Dictionary representation of the Dijkstra step.
        """
        return {
            "Step": self.step_number,
            "Current": self.current_vertex,
            "Neighbor": self.neighbor,
            "Candidate": _format_distance(self.candidate_distance),
            "Previous": _format_distance(self.known_distance),
            "Updated": "Yes" if self.updated else "No",
            "Queue": ", ".join(self.queue_snapshot) if self.queue_snapshot else "-",
            "Predecessors": _compact_predecessors(self.predecessor_snapshot),
        }
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class DijkstraStep


# ------------------------------------------------------------------------- class BellmanFordStep
@dataclass(frozen=True)
class BellmanFordStep:
    """Represent one Bellman-Ford relaxation or cycle-check row.

    Args:
        step_number: One-based trace counter.
        pass_number: Main-loop pass, or final check pass.
        phase: ``"Relax"`` or ``"Cycle Check"``.
        current_vertex: Edge source being inspected.
        neighbor: Edge target being inspected.
        edge_weight: Weight on the inspected edge.
        candidate_distance: Distance through ``current_vertex``.
        known_distance: Target distance before relaxation.
        updated: Whether the step updated distance/predecessor.
        distance_snapshot: Current source-to-vertex distances.
        predecessor_snapshot: Current predecessor map.

    Logic:
        Bellman-Ford repeatedly relaxes every edge, then performs one extra
        edge scan to detect a reachable negative-weight cycle.
    """

    step_number: int
    pass_number: int
    phase: str
    current_vertex: str
    neighbor: str
    edge_weight: float
    candidate_distance: float
    known_distance: float
    updated: bool
    distance_snapshot: dict[str, float] = field(default_factory=dict)
    predecessor_snapshot: dict[str, str | None] = field(default_factory=dict)

    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return a table-friendly dictionary.

        Returns:
            Dictionary representation of the Bellman-Ford step.
        """
        return {
            "Step": self.step_number,
            "Phase": self.phase,
            "Pass": self.pass_number,
            "Edge": f"{self.current_vertex} -> {self.neighbor}",
            "Weight": self.edge_weight,
            "Candidate": _format_distance(self.candidate_distance),
            "Previous": _format_distance(self.known_distance),
            "Updated": "Yes" if self.updated else "No",
            "Distances": _compact_distances(self.distance_snapshot),
            "Predecessors": _compact_predecessors(self.predecessor_snapshot),
        }
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class BellmanFordStep


# ------------------------------------------------------------------------- class ShortestPathResult
@dataclass(frozen=True)
class ShortestPathResult:
    """Represent a completed source-to-target shortest path query.

    Args:
        start_vertex: Source vertex label.
        end_vertex: Destination vertex label.
        path: Ordered source-to-target path, or empty when unreachable.
        distance: Total path distance, or infinity when unreachable.
        steps: Step-by-step shortest-path trace rows.
        distances: Final distance map from the source.
        predecessors: Final predecessor map.
        representation: Human-readable graph representation name.
        algorithm: Algorithm display name.
        negative_cycle_detected: Whether Bellman-Ford found a reachable
            negative-weight cycle.
        negative_cycle_edges: Edges that still relax during Bellman-Ford's
            final cycle-check pass.
        trace_truncated: Whether trace rows were capped for UI readability.

    Logic:
        This result packages both the route answer and the trace state needed
        to explain how the selected shortest-path algorithm found the route.
    """

    start_vertex: str
    end_vertex: str
    path: list[str]
    distance: float
    steps: list[DijkstraStep | BellmanFordStep]
    distances: dict[str, float]
    predecessors: dict[str, str | None]
    representation: str
    algorithm: str = "Dijkstra"
    negative_cycle_detected: bool = False
    negative_cycle_edges: list[tuple[str, str]] = field(default_factory=list)
    trace_truncated: bool = False

    # --------------------------------------------------------------- steps_as_dicts()
    def steps_as_dicts(self) -> list[dict[str, object]]:
        """Return trace steps as dictionaries.

        Returns:
            List of table-friendly step dictionaries.
        """
        return [step.as_dict() for step in self.steps]
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- path_label()
    def path_label(self) -> str:
        """Return a readable path label.

        Returns:
            Arrow-separated path text, or ``"No route"``.
        """
        if not self.path:
            return "No route"
        return " -> ".join(self.path)
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class ShortestPathResult

# ==============================================================================
# End of File
# ==============================================================================
