# File: graph_edge.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - GraphEdge stores source, target, weight, and directed display metadata.
# - label() formats one edge consistently for tables, charts, and visual legends.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Shared by graph implementations, dataset generators, Streamlit UI, and reports.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Graph edge data model."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from dataclasses import dataclass


# ______________________________________________________________________________
# Class Definitions - Data Classes
# ==============================================================================
# GRAPH DATA MODELS
# ==============================================================================
# Immutable edges provide a shared input/output shape for graph workflows.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class GraphEdge
@dataclass(frozen=True)
class GraphEdge:
    """Represent one weighted graph edge.

    Args:
        source: Source vertex label.
        target: Target vertex label.
        weight: Numeric edge weight.

    Logic:
        This dataclass is intentionally tiny and immutable.
        1. Carry the source and target endpoint labels.
        2. Carry the numeric edge weight used by shortest-path algorithms.
    """

    source: str
    target: str
    weight: float = 1.0

    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return a table-friendly dictionary.

        Returns:
            Dictionary representation of the edge.
        """
        return {
            "Source": self.source,
            "Target": self.target,
            "Weight": self.weight,
        }
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class GraphEdge

# ==============================================================================
# End of File
# ==============================================================================