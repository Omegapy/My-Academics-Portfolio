# -------------------------------------------------------------------------
# File: benchmark_record.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# BenchmarkRecord dataclass for one row of timing data emitted by the
# benchmark engine. Each record captures the structure, operation,
# operation category (common vs structure-specific), workload size, best-of-
# repeats normalized time in milliseconds, sample return value, sizes before
# and after the workload, the expected Big-O label, and a correctness flag.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for benchmark timing records."""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass

# __________________________________________________________________________
# BenchmarkRecord Dataclass
#

# ========================================================================
# BenchmarkRecord
# ========================================================================
# --------------------------------------------------------------- dataclass BenchmarkRecord
@dataclass
class BenchmarkRecord:
    """One row in the benchmark results table.

    Args:
        structure: Structure name (e.g. ``"Stack"``).
        operation: Operation name (e.g. ``"push"``, ``"insert_rear"``).
        category: ``"common"`` for cross-structure workloads or
            ``"specific"`` for structure-specific workloads.
        size: Workload size used for the timed run.
        time_ms: Best-of-repeats normalized time, in milliseconds.
        returned_value: Sample return value used for verification.
        size_before: Structure size before the timed workload.
        size_after: Structure size after the timed workload.
        complexity: Expected Big-O label for the operation.
        is_correct: True when the workload behaved as expected.
        operation_group: Logical grouping label used by the operation
            winner computation, e.g. ``"common_build"`` or
            ``"linked_list_search"``.
    """

    structure: str
    operation: str
    category: str
    size: int
    time_ms: float
    returned_value: int | bool | None
    size_before: int
    size_after: int
    complexity: str
    is_correct: bool
    operation_group: str

# --------------------------------------------------------------- end dataclass BenchmarkRecord

# __________________________________________________________________________
# End of File
#
