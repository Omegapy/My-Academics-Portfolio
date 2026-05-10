# File: benchmark_record.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - BenchmarkRecord stores one flat, CSV-ready benchmark observation.
# - as_dict() converts the immutable model into a pandas-friendly mapping.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Produced by benchmark_graphs.py and consumed by reports, charts, and Streamlit.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Benchmark record data model."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from dataclasses import asdict, dataclass


# ______________________________________________________________________________
# Class Definitions - Data Classes
# ==============================================================================
# BENCHMARK DATA MODELS
# ==============================================================================
# Immutable records keep timing results stable after measurement.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class BenchmarkRecord
@dataclass(frozen=True)
class BenchmarkRecord:
    """Represent one graph benchmark workload result.

    Args:
        structure: Graph representation name.
        operation: Operation name.
        operation_group: Group used by reports and charts.
        graph_kind: Sparse or dense workload label.
        size: Vertex count.
        edge_count: Edge count.
        workload_count: Number of logical operations timed.
        time_ms: Best elapsed time in milliseconds.
        avg_time_us: Average microseconds per logical operation.
        complexity: Expected Big-O label.
        is_correct: Correctness flag for the workload.
        density: Edge density for the graph.
        notes: Human-readable summary.

    Logic:
        Each row is intentionally flat so it can be written directly to CSV
        and displayed in Streamlit tables.
    """

    structure: str
    operation: str
    operation_group: str
    graph_kind: str
    size: int
    edge_count: int
    workload_count: int
    time_ms: float
    avg_time_us: float
    complexity: str
    is_correct: bool
    density: float
    notes: str

    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return a dictionary representation.

        Returns:
            Dictionary suitable for pandas DataFrame construction.
        """
        return asdict(self)
    # ---------------------------------------------------------------


# ------------------------------------------------------------------------- end class BenchmarkRecord

# ==============================================================================
# End of File
# ==============================================================================