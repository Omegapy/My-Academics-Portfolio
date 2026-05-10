# File: adjacency_list_graph.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Weighted graph implementation backed by adjacency dictionaries.
#
# --- Module Contents Overview ---
# - Helper functions normalize vertex labels and numeric edge weights.
# - AdjacencyListGraph implements the shared graph interface with sparse storage.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by dataset builders, graph algorithms, Streamlit labs, and benchmarks.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Adjacency-list graph implementation."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from models.graph_edge import GraphEdge


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# GRAPH VALIDATION HELPERS
# ==============================================================================
# Normalize labels and weights before graph operations touch internal storage.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _clean_label()
def _clean_label(label: str) -> str:
    """Normalize and validate a vertex label.

    Args:
        label: Input vertex label.

    Returns:
        Stripped vertex label.

    Raises:
        ValueError: If the label is blank.
    """
    cleaned = str(label).strip()
    # VALIDATION: blank vertex names cannot be shown clearly in tables or traces
    if not cleaned:
        raise ValueError("Vertex labels must be non-empty.")
    return cleaned
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _clean_weight()
def _clean_weight(weight: float) -> float:
    """Normalize and validate an edge weight.

    Args:
        weight: Input edge weight.

    Returns:
        Edge weight as a float.

    Raises:
        ValueError: If the weight is not numeric.
    """
    return float(weight)
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Class Definitions - Regular Classes
# ==============================================================================
# GRAPH REPRESENTATION CLASSES
# ==============================================================================
# Adjacency-list storage keeps only present edges, favoring sparse graph workloads.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class AdjacencyListGraph
class AdjacencyListGraph:
    """Weighted graph backed by adjacency dictionaries.

    Args:
        directed: True for directed edges, False for undirected edges.

    Logic:
        This representation stores each vertex once and only stores present
        edges, making it memory-efficient for sparse graphs.
    """

    representation_name = "Adjacency List"

    # --------------------------------------------------------------- __init__()
    def __init__(self, *, directed: bool = False) -> None:
        """Initialize an empty adjacency-list graph.

        Args:
            directed: Whether edges should be treated as one-way.
        """
        self.directed = directed
        self._adjacency: dict[str, dict[str, float]] = {}
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- add_vertex()
    def add_vertex(self, label: str) -> bool:
        """Add a vertex.

        Args:
            label: Vertex label.

        Returns:
            True when a new vertex was added, otherwise False.
        """
        vertex = _clean_label(label)
        # VALIDATION: existing vertices are left unchanged
        if vertex in self._adjacency:
            return False
        self._adjacency[vertex] = {}
        return True
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- remove_vertex()
    def remove_vertex(self, label: str) -> bool:
        """Remove a vertex and all incident edges.

        Args:
            label: Vertex label.

        Returns:
            True when the graph changed, otherwise False.
        """
        vertex = _clean_label(label)
        # VALIDATION: absent vertices do not change the graph
        if vertex not in self._adjacency:
            return False
        del self._adjacency[vertex]
        # MAIN ITERATION LOOP: remove inbound references from every neighbor map
        for neighbor_map in self._adjacency.values():
            neighbor_map.pop(vertex, None)
        return True
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- add_edge()
    def add_edge(self, source: str, target: str, weight: float = 1.0) -> bool:
        """Add or update an edge.

        Args:
            source: Source vertex label.
            target: Target vertex label.
            weight: Numeric edge weight. Negative values are allowed for
                Bellman-Ford demos; Dijkstra validates its own inputs.

        Returns:
            True when a new edge was created, False when an existing edge was updated.
        """
        # VALIDATION: normalize labels and weights before using them.
        src = _clean_label(source)
        dst = _clean_label(target)
        edge_weight = _clean_weight(weight)
        # MAIN LOOP: ensure both endpoints exist before setting the edge
        self.add_vertex(src)
        self.add_vertex(dst)
        # determine if the edge is new or just an update
        created = dst not in self._adjacency[src]
        # MAIN LOOP: record outgoing edge
        self._adjacency[src][dst] = edge_weight
        # MAIN LOOP: if undirected, mirror the edge
        if not self.directed:
            self._adjacency[dst][src] = edge_weight
        return created
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- remove_edge()
    def remove_edge(self, source: str, target: str) -> bool:
        """Remove an edge.

        Args:
            source: Source vertex label.
            target: Target vertex label.

        Returns:
            True when the graph changed, otherwise False.
        """
        # VALIDATION: normalize labels and weights before using them.
        src = _clean_label(source)
        dst = _clean_label(target)
        changed = False
        # MAIN LOOP: delete outgoing edge
        if src in self._adjacency and dst in self._adjacency[src]:
            del self._adjacency[src][dst]
            changed = True
        # MAIN LOOP: if undirected, mirror the edge
        if not self.directed and dst in self._adjacency and src in self._adjacency[dst]:
            del self._adjacency[dst][src]
        return changed
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- has_edge()
    def has_edge(self, source: str, target: str) -> bool:
        """Return True when an edge exists.

        Args:
            source: Source vertex label.
            target: Target vertex label.

        Returns:
            Whether the edge exists.
        """
        # VALIDATION: normalize labels and weights before using them.
        src = _clean_label(source)
        dst = _clean_label(target)
        # MAIN LOOP: check for outgoing edge
        return src in self._adjacency and dst in self._adjacency[src]
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
        # VALIDATION: normalize labels and weights before using them.
        src = _clean_label(source)
        dst = _clean_label(target)
        # MAIN LOOP: safely retrieve outgoing edge weight
        return self._adjacency.get(src, {}).get(dst)
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- neighbors()
    def neighbors(self, label: str) -> list[tuple[str, float]]:
        """Return neighbors in insertion order.

        Args:
            label: Vertex label.

        Returns:
            List of ``(neighbor, weight)`` pairs.

        Raises:
            KeyError: If the vertex is unknown.
        """
        # VALIDATION: normalize labels and weights before using them.
        vertex = _clean_label(label)
        # MAIN LOOP: fail when the vertex does not exist
        if vertex not in self._adjacency:
            raise KeyError(f"Unknown vertex: {vertex}")
        return list(self._adjacency[vertex].items())
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- vertices()
    def vertices(self) -> list[str]:
        """Return vertices in insertion order.

        Returns:
            Vertex labels.
        """
        # MAIN LOOP: return vertex labels in insertion order
        return list(self._adjacency.keys())
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- edges()
    def edges(self) -> list[GraphEdge]:
        """Return graph edges.

        Returns:
            Edge objects in display order.
        """
        edges: list[GraphEdge] = []
        seen: set[frozenset[str]] = set()
        # MAIN ITERATION LOOP: walk vertices and neighbor maps in insertion order
        for source, neighbor_map in self._adjacency.items():
            # get neighbor and edge weight for the current source
            for target, weight in neighbor_map.items():
                # MAIN LOOP: skip already-seen edges in undirected graphs
                if not self.directed:
                    key = frozenset((source, target))
                    if key in seen:
                        continue
                    seen.add(key)
                edges.append(GraphEdge(source, target, weight))
        return edges
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- order()
    def order(self) -> int:
        """Return vertex count.

        Returns:
            Number of vertices.
        """
        # MAIN LOOP: return the number of vertices
        return len(self._adjacency)
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- size()
    def size(self) -> int:
        """Return edge count.

        Returns:
            Number of graph edges.
        """
        # MAIN LOOP: return the number of edges
        return len(self.edges())
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove all vertices and edges.

        Returns:
            None.
        """
        # MAIN LOOP: clear all vertices and edges
        self._adjacency.clear()
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- adjacency_dict()
    def adjacency_dict(self) -> dict[str, dict[str, float]]:
        """Return a shallow copy of the adjacency mapping.

        Returns:
            Vertex-to-neighbor mapping copy.
        """
        # MAIN LOOP: return a shallow copy of the adjacency mapping
        return {vertex: dict(neighbors) for vertex, neighbors in self._adjacency.items()}
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return vertex count.

        Returns:
            Number of vertices.
        """
        # MAIN LOOP: return the number of vertices
        return self.order()
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class AdjacencyListGraph

# ==============================================================================
# End of File
# ==============================================================================
