# File: quickselect_result.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Store the complete result of one Quickselect run.
# - Preserve partition metadata, kth-rank details, operation counts, and traces.
# - Provide a serializable result object for validation, charts, and UI display.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# DATA CLASSES:
#   - Class: QuickSelectResult - complete result from one Quickselect execution
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by the Quickselect algorithm, benchmark pipeline, and Streamlit page.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Quickselect result model for Portfolio Module 8.

The ``QuickSelectResult`` dataclass stores the selected kth-smallest value,
partition metadata, operation counts, timing data, and optional trace lines
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
# ``QuickSelectResult`` records both the untouched original input and the final
# partitioned working copy so the UI can explain what Quickselect changed.
#
# DATACLASS CONTENTS:
#   - Class: QuickSelectResult - complete output from one Quickselect execution
# -------------------------------------------------------------------------
# Constraint: ``k`` remains user-facing and ``zero_based_rank`` remains internal.
#
# ------------------------------------------------------------------------- class QuickSelectResult
@dataclass(slots=True, kw_only=True)
class QuickSelectResult:
    """Store the complete result of one Quickselect execution.

    Attributes:
        algorithm: Display name for the selection algorithm.
        input_size: Number of input values provided by the caller.
        original_data: Copy of the caller's input before partitioning.
        partitioned_data: Final working-list order after Quickselect stops.
        k: User-facing 1-based kth-smallest position.
        zero_based_rank: Internal target rank equal to ``k - 1``.
        selected_value: Value found at the kth-smallest position.
        comparisons: Number of pivot comparisons.
        swaps: Number of different-index exchanges.
        writes: Number of list-position writes, counted as two per swap.
        elapsed_time: Wall-clock seconds measured with ``time.perf_counter()``.
        is_correct: Whether the selected value matches sorted-order checking.
        step_trace: Human-readable partition trace entries for visualization.

    Logic:
        This dataclass captures Quickselect output without rerunning selection.
        1. Store the original input and final partitioned working copy.
        2. Preserve rank, selected value, operation counters, and correctness.
        3. Keep trace lines optional through a safe list default factory.
    """

    algorithm: str
    input_size: int
    original_data: list[int]
    partitioned_data: list[int]
    k: int
    zero_based_rank: int
    selected_value: int
    comparisons: int
    swaps: int
    writes: int
    elapsed_time: float
    is_correct: bool
    step_trace: list[str] = field(default_factory=list)

# --------------------------------------------------------- end class QuickSelectResult

# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
