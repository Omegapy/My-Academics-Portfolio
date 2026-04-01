# -------------------------------------------------------------------------
# File: search_result.py
# Author: Alexander Ricciardi
# Date: 2026-03-29
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# SearchResult dataclass that captures the outcome of a
# search algorithm execution, including timing, comparisons, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for search algorithm results.

The SearchResult dataclass stores everything returned (search metrics)
by a search-algorithm. That is, whether the target was found, how many 
comparisons were made, wall-clock time, and a human-readable step trace.
"""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass, field

# __________________________________________________________________________
# SearchResult Dataclass
#

# ========================================================================
# SearchResult
# ========================================================================
# --------------------------------------------------------------- dataclass SearchResult
@dataclass
class SearchResult:
    """Immutable record of one search-algorithm execution.

    Args:
        algorithm: Name of the algorithm (e.g., "Linear Search").
        target: The integer value that was searched for.
        found: True if the target was located in the dataset.
        index: Position of the target, or None if not found.
        comparisons: Total element comparisons performed.
        elapsed_time: Wall-clock seconds (via time.perf_counter()).
        dataset_size: Number of elements in the dataset.
        sorted_required: True if the algorithm requires sorted input.
        step_trace: Human-readable step-by-step explanation strings.
    """

    algorithm: str
    target: int
    found: bool
    index: int | None
    comparisons: int
    elapsed_time: float
    dataset_size: int
    sorted_required: bool
    step_trace: list[str] = field(default_factory=list)

# --------------------------------------------------------------- end dataclass SearchResult

# __________________________________________________________________________
# End of File
#
