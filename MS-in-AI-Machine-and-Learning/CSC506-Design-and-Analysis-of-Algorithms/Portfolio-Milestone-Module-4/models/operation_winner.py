# -------------------------------------------------------------------------
# File: operation_winner.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# OperationWinner dataclass used by the benchmark engine to capture the 
# fastest structure / operation combination for one (operation_group, size) 
# bucket. Used by the Benchmark Lab to surface the operation_winners.csv 
# table and the heatmap chart.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for benchmark operation-winner summaries."""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass

# __________________________________________________________________________
# OperationWinner Dataclass
#

# ========================================================================
# OperationWinner
# ========================================================================
# --------------------------------------------------------------- dataclass OperationWinner
@dataclass
class OperationWinner:
    """Winner record for one (operation_group, size) benchmark bucket.

    Args:
        operation_group: Logical grouping label, e.g. ``"common_build"``,
            ``"deque_ends"``, or ``"linked_list_search"``.
        size: Workload size for the bucket.
        fastest_structure: Name of the structure that wins the bucket.
        fastest_operation: Operation name that wins the bucket.
        fastest_time_ms: Winning time in milliseconds.
        runner_up: Second-place ``"Structure.operation"`` label.
        notes: Human-readable summary sentence used in reports.
    """

    operation_group: str
    size: int
    fastest_structure: str
    fastest_operation: str
    fastest_time_ms: float
    runner_up: str
    notes: str

# --------------------------------------------------------------- end dataclass OperationWinner

# __________________________________________________________________________
# End of File
#
