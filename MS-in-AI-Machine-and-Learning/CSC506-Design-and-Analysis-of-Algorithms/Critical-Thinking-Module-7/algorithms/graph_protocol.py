# File: graph_protocol.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Protocol shared by adjacency-list and adjacency-matrix graph classes.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - WeightedGraph declares the graph operations expected by algorithms and UI code.
# - Concrete representations stay interchangeable through this structural contract.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Used for type hints across algorithms, datasets, visualization, and benchmarks.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Shared graph protocol used by algorithms, UI, and benchmarks."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from typing import Protocol

from models.graph_edge import GraphEdge


# ______________________________________________________________________________
# Class Definitions - Protocol Classes
# ==============================================================================
# GRAPH INTERFACE CONTRACT
# ==============================================================================
# Defines the methods both graph representations must expose to shared callers.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class WeightedGraph
class WeightedGraph(Protocol):
    """Protocol for weighted graph representations.

    Logic:
        The Streamlit app and algorithms depend on this shared behavior rather
        than on one concrete representation.
    """

    directed: bool
    representation_name: str

    # --------------------------------------------------------------- add_vertex()
    def add_vertex(self, label: str) -> bool:
        """Add a vertex.

        Args:
            label: Vertex label.

        Returns:
            True when the graph changed.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- remove_vertex()
    def remove_vertex(self, label: str) -> bool:
        """Remove a vertex.

        Args:
            label: Vertex label.

        Returns:
            True when the graph changed.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- add_edge()
    def add_edge(self, source: str, target: str, weight: float = 1.0) -> bool:
        """Add or update an edge.

        Args:
            source: Source vertex label.
            target: Target vertex label.
            weight: Numeric edge weight.

        Returns:
            True when a new edge was created.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- remove_edge()
    def remove_edge(self, source: str, target: str) -> bool:
        """Remove an edge.

        Args:
            source: Source vertex label.
            target: Target vertex label.

        Returns:
            True when the graph changed.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- has_edge()
    def has_edge(self, source: str, target: str) -> bool:
        """Return whether an edge exists.

        Args:
            source: Source vertex label.
            target: Target vertex label.

        Returns:
            True when the edge exists.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- get_weight()
    def get_weight(self, source: str, target: str) -> float | None:
        """Return an edge weight.

        Args:
            source: Source vertex label.
            target: Target vertex label.

        Returns:
            Edge weight, or None when no edge exists.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- neighbors()
    def neighbors(self, label: str) -> list[tuple[str, float]]:
        """Return adjacent vertices and weights.

        Args:
            label: Vertex label.

        Returns:
            Neighbor label and edge-weight pairs.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- vertices()
    def vertices(self) -> list[str]:
        """Return vertex labels in display order.

        Returns:
            Ordered vertex labels.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- edges()
    def edges(self) -> list[GraphEdge]:
        """Return graph edges.

        Returns:
            GraphEdge records.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- order()
    def order(self) -> int:
        """Return the vertex count.

        Returns:
            Number of vertices.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- size()
    def size(self) -> int:
        """Return the edge count.

        Returns:
            Number of stored edges.
        """
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove all vertices and edges.

        Returns:
            None.
        """
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class WeightedGraph

# ==============================================================================
# End of File
# ==============================================================================