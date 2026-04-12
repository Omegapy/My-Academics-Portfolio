# -------------------------------------------------------------------------
# File: sort_result.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# SortResult dataclass that captures the outcome of a sorting algorithm
# execution, including timing, comparisons, swaps, writes, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for sorting algorithm results.

The SortResult dataclass stores everything returned by a sorting algorithm:
the sorted output, operation counts (comparisons, swaps, writes),
wall-clock time, algorithm properties, and an optional step trace.
"""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass, field

# __________________________________________________________________________
# SortResult Dataclass
#

# ========================================================================
# SortResult
# ========================================================================
# --------------------------------------------------------------- dataclass SortResult
@dataclass
class SortResult:
    """Immutable record of one sorting-algorithm execution.

    Args:
        algorithm: Name of the algorithm (e.g., "Bubble Sort").
        input_size: Number of items sorted.
        sorted_data: The sorted output list.
        comparisons: Total value comparisons performed.
        swaps: Swap count (0 for non-swap algorithms like insertion/merge).
        writes: Data writes or moves (shifts, merge writes).
        elapsed_time: Wall-clock seconds (via time.perf_counter()).
        is_stable: Whether the algorithm preserves relative order of equal elements.
        is_in_place: Whether the algorithm sorts in place conceptually.
        extra_space: Space label, e.g. "O(1)" or "O(n)".
        step_trace: Human-readable walkthrough strings (default empty).
    """

    algorithm: str
    input_size: int
    sorted_data: list[int]
    comparisons: int
    swaps: int
    writes: int
    elapsed_time: float
    is_stable: bool
    is_in_place: bool
    extra_space: str
    step_trace: list[str] = field(default_factory=list)

# --------------------------------------------------------------- end dataclass SortResult

# __________________________________________________________________________
# End of File
#
