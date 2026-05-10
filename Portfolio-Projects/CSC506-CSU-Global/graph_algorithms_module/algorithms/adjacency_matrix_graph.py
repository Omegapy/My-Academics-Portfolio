# File: adjacency_matrix_graph.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Weighted graph implementation backed by an adjacency matrix.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - AdjacencyMatrixGraph stores vertex indexes and a square weighted matrix.
# - Methods mirror the adjacency-list graph so benchmarks can compare both fairly.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by graph factories, visual labs, shortest-path demos, and benchmarks.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Adjacency-matrix graph implementation."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from graph_algorithms_module.algorithms.adjacency_list_graph import _clean_label, _clean_weight
from graph_algorithms_module.models.graph_edge import GraphEdge


# ______________________________________________________________________________
# Class Definitions - Regular Classes
# ==============================================================================
# GRAPH REPRESENTATION CLASSES
# ==============================================================================
# Adjacency-matrix storage reserves every vertex pair for constant-time checks.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class AdjacencyMatrixGraph
class AdjacencyMatrixGraph:
    """Weighted graph backed by a square adjacency matrix.

    Args:
        directed: True for directed edges, False for undirected edges.

    Logic:
        This representation reserves a row and column for every vertex pair,
        making adjacency checks O(1) but memory cost O(V^2).
    """

    representation_name = "Adjacency Matrix"

    # --------------------------------------------------------------- __init__()
    def __init__(self, *, directed: bool = False) -> None:
        """Initialize an empty adjacency-matrix graph.

        Args:
            directed: Whether edges should be treated as one-way.
        """
        self.directed = directed
        self._vertices: list[str] = []
        self._index: dict[str, int] = {}
        self._matrix: list[list[float | None]] = []
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
        if vertex in self._index:
            return False
        # MAIN LOOP: add the new vertex to the graph
        self._index[vertex] = len(self._vertices)
        self._vertices.append(vertex)
        # Step 1: add one new empty column to every existing row
        for row in self._matrix:
            row.append(None)
        # Step 2: append the new row for the new vertex
        self._matrix.append([None for _ in self._vertices])
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
        if vertex not in self._index:
            return False
        # MAIN LOOP: remove the vertex from the graph
        remove_idx = self._index[vertex]
        del self._vertices[remove_idx]
        del self._matrix[remove_idx]
        # MAIN ITERATION LOOP: remove the matching column from each remaining row
        for row in self._matrix:
            del row[remove_idx]
        self._index = {item: index for index, item in enumerate(self._vertices)}
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
        # MAIN LOOP: add the source and target vertices to the graph if they don't exist
        self.add_vertex(src)
        self.add_vertex(dst)
        # get the indices of the source and target vertices
        src_idx = self._index[src]
        dst_idx = self._index[dst]
        # check if the edge already exists
        created = self._matrix[src_idx][dst_idx] is None
        # MAIN LOOP: add the edge to the graph
        self._matrix[src_idx][dst_idx] = edge_weight
        # add the edge to the graph if it's undirected
        if not self.directed:
            self._matrix[dst_idx][src_idx] = edge_weight
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
            # VALIDATION: absent vertices do not change the graph
        if src not in self._index or dst not in self._index:
            return False
        # get the indices of the source and target vertices
        src_idx = self._index[src]
        dst_idx = self._index[dst]
        # check if the edge already exists
        changed = self._matrix[src_idx][dst_idx] is not None
        # MAIN LOOP: remove the edge from the graph
        self._matrix[src_idx][dst_idx] = None
        if not self.directed:
            self._matrix[dst_idx][src_idx] = None
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
        # get the indices of the source and target vertices
        if src not in self._index or dst not in self._index:
            return False
        return self._matrix[self._index[src]][self._index[dst]] is not None
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
        # get the indices of the source and target vertices
        if src not in self._index or dst not in self._index:
            return None
        return self._matrix[self._index[src]][self._index[dst]]
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- neighbors()
    def neighbors(self, label: str) -> list[tuple[str, float]]:
        """Return neighbors in vertex-order.

        Args:
            label: Vertex label.

        Returns:
            List of ``(neighbor, weight)`` pairs.

        Raises:
            KeyError: If the vertex is unknown.
        """
        # VALIDATION: normalize labels and weights before using them.
        vertex = _clean_label(label)
        if vertex not in self._index:
            raise KeyError(f"Unknown vertex: {vertex}")
        # get the row for the vertex
        row = self._matrix[self._index[vertex]]
        neighbors: list[tuple[str, float]] = []
        # MAIN ITERATION LOOP: scan the row in vertex display order
        for index, weight in enumerate(row):
            if weight is not None:
                neighbors.append((self._vertices[index], weight))
        return neighbors
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- vertices()
    def vertices(self) -> list[str]:
        """Return vertices in insertion order.

        Returns:
            Vertex labels.
        """
        # Return a copy of the vertices
        return list(self._vertices)
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- edges()
    def edges(self) -> list[GraphEdge]:
        """Return graph edges.

        Returns:
            Edge objects in display order.
        """
        edges: list[GraphEdge] = []
        # MAIN ITERATION LOOP: scan every matrix cell in row/column order
        for row_index, source in enumerate(self._vertices):
            # MAIN ITERATION LOOP: scan the row in vertex display order
            for col_index, target in enumerate(self._vertices):
                weight = self._matrix[row_index][col_index]
                # Skip if no edge exists
                if weight is None:
                    continue
                # Skip if it's an undirected graph and the edge is a duplicate
                if not self.directed and col_index < row_index:
                    continue
                # Add the edge to the list
                edges.append(GraphEdge(source, target, weight))
        return edges
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- order()
    def order(self) -> int:
        """Return vertex count.

        Returns:
            Number of vertices.
        """
        # Return the number of vertices
        return len(self._vertices)
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- size()
    def size(self) -> int:
        """Return edge count.

        Returns:
            Number of graph edges.
        """
        # Return the number of edges
        return len(self.edges())
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove all vertices and edges.

        Returns:
            None.
        """
        # Clear all vertices and edges
        self._vertices.clear()
        self._index.clear()
        self._matrix.clear()
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- matrix()
    def matrix(self) -> list[list[float | None]]:
        """Return a copy of the adjacency matrix.

        Returns:
            Matrix copy.
        """
        # Return a copy of the matrix
        return [list(row) for row in self._matrix]
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return vertex count.

        Returns:
            Number of vertices.
        """
        # Return the number of vertices
        return self.order()
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class AdjacencyMatrixGraph

# ==============================================================================
# End of File
# ==============================================================================