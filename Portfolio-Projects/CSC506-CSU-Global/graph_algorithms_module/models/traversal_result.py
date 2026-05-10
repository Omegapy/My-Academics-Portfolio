# File: traversal_result.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Dataclasses for BFS and DFS step-by-step traversal output.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - TraversalStep stores one row in the BFS/DFS classroom trace.
# - TraversalResult stores the complete visit order and representation label.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Returned by traversal algorithms and displayed by Streamlit/report components.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Traversal result models for BFS and DFS."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from dataclasses import dataclass, field


# ______________________________________________________________________________
# Class Definitions - Data Classes
# ==============================================================================
# TRAVERSAL DATA MODELS
# ==============================================================================
# Trace rows and final results keep BFS/DFS output readable in tables.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class TraversalStep
@dataclass(frozen=True)
class TraversalStep:
    """Represent one BFS or DFS trace row.

    Args:
        step_number: One-based step counter.
        action: Short explanation of the action performed.
        current_vertex: Vertex being processed, if any.
        frontier: Queue or stack snapshot after the action.
        visited: Ordered visited vertices after the action.
        discovered: Discovered vertices after the action.

    Logic:
        This row captures enough state for the Streamlit app to render a
        classroom-style traversal trace.
    """

    step_number: int
    action: str
    current_vertex: str
    frontier: list[str] = field(default_factory=list)
    visited: list[str] = field(default_factory=list)
    discovered: list[str] = field(default_factory=list)
    traversed_edges: list[tuple[str, str]] = field(default_factory=list)

    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return a table-friendly dictionary.

        Returns:
            Dictionary representation of the traversal step.
        """
        return {
            "Step": self.step_number,
            "Action": self.action,
            "Current": self.current_vertex,
            "Frontier": ", ".join(self.frontier) if self.frontier else "-",
            "Visited": ", ".join(self.visited) if self.visited else "-",
            "Discovered": ", ".join(self.discovered) if self.discovered else "-",
            "Traversal Edges": ", ".join(
                f"{source}->{target}" for source, target in self.traversed_edges
            )
            if self.traversed_edges
            else "-",
        }
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class TraversalStep


# ------------------------------------------------------------------------- class TraversalResult
@dataclass(frozen=True)
class TraversalResult:
    """Represent a completed graph traversal.

    Args:
        algorithm: Traversal algorithm name.
        start_vertex: Starting vertex label.
        visit_order: Ordered list of visited vertices.
        steps: Step-by-step trace rows.
        representation: Human-readable graph representation name.

    Logic:
        This result bundles the final visit order with the trace rows used by
        the UI and validation tests.
    """

    algorithm: str
    start_vertex: str
    visit_order: list[str]
    steps: list[TraversalStep]
    representation: str

    # --------------------------------------------------------------- steps_as_dicts()
    def steps_as_dicts(self) -> list[dict[str, object]]:
        """Return traversal steps as dictionaries.

        Returns:
            List of table-friendly step dictionaries.
        """
        return [step.as_dict() for step in self.steps]
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class TraversalResult


# ==============================================================================
# End of File
# ==============================================================================
