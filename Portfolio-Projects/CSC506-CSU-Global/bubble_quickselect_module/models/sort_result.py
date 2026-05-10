# File: sort_result.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Store the complete result of one Bubble Sort run.
# - Preserve algorithm metadata, operation counts, timing, and optional traces.
# - Provide a small serializable object for tests, benchmarks, and Streamlit UI.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# DATA CLASSES:
#   - Class: SortResult - complete result from one Bubble Sort execution
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by the Bubble Sort algorithm, the benchmark pipeline, and the
# Bubble Quickselect Sets Streamlit page.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Bubble Sort result model for Portfolio Module 8.

The ``SortResult`` dataclass captures the original input, sorted output,
operation counts, algorithm properties, timing data, and optional trace lines
needed by tests, benchmarks, and future Streamlit visualizations.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from dataclasses import dataclass, field


# __________________________________________________________________________
# Class Definitions - Data Classes
# ========================================================================
# RESULT MODEL
# ========================================================================
# ``SortResult`` is intentionally small and serializable so later UI and
# benchmark layers can convert it into tables without extra adapter logic.
#
# DATACLASS CONTENTS:
#   - Class: SortResult - complete output from one Bubble Sort execution
# -------------------------------------------------------------------------
# Constraint: Field names match benchmark/UI expectations and should remain stable.
#
# ------------------------------------------------------------------------- class SortResult
@dataclass(slots=True, kw_only=True)
class SortResult:
    """Store the complete result of one Bubble Sort execution.

    Attributes:
        algorithm: Display name for the sorting algorithm.
        input_size: Number of input values provided by the caller.
        original_data: Copy of the caller's input before sorting.
        sorted_data: Sorted output produced by the algorithm.
        comparisons: Number of adjacent value comparisons.
        swaps: Number of adjacent element exchanges.
        writes: Number of list-position writes, counted as two per swap.
        elapsed_time: Wall-clock seconds measured with ``time.perf_counter()``.
        is_stable: Whether equal items keep their relative order.
        is_in_place: Conceptual in-place property of Bubble Sort.
        extra_space: Auxiliary-space complexity label.
        early_exit_used: Whether a no-swap pass ended the algorithm.
        step_trace: Human-readable trace entries for visualization.

    Logic:
        This dataclass captures Bubble Sort output without recomputing anything.
        1. Store original and sorted data for side-by-side UI display.
        2. Preserve operation counters and algorithm properties from the run.
        3. Keep trace lines optional through a safe list default factory.
    """

    algorithm: str
    input_size: int
    original_data: list[int]
    sorted_data: list[int]
    comparisons: int
    swaps: int
    writes: int
    elapsed_time: float
    is_stable: bool
    is_in_place: bool
    extra_space: str
    early_exit_used: bool
    step_trace: list[str] = field(default_factory=list)

# ------------------------------------------------------------------------- end class SortResult

# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
