# -------------------------------------------------------------------------
# File: operation_result.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# OperationResult dataclass used by the benchmark engine to capture the 
# outcome of a single playground operation against one of the four required 
# data structures (Stack, Queue, Deque, LinkedList). Stores the structure name, 
# operation, inputs, return value, sizes before/after, elapsed wall-clock time, 
# expected Big-O label, and an optional human-readable step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for one playground operation result."""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass, field

# __________________________________________________________________________
# OperationResult Dataclass
#

# ========================================================================
# OperationResult
# ========================================================================
# --------------------------------------------------------------- dataclass OperationResult
@dataclass
class OperationResult:
    """Immutable record of one Structure Playground operation.

    Args:
        structure: Structure name (``"Stack"``, ``"Queue"``, ``"Deque"``,
            ``"LinkedList"``).
        operation: Operation name (``"push"``, ``"dequeue"``, ``"insert_before"``...).
        input_value: Optional value passed to the operation.
        anchor_value: Optional anchor value used by ``insert_before`` /
            ``insert_after``.
        returned_value: Whatever the operation returned: an integer, a
            boolean, a list of ints, or ``None``.
        size_before: Structure size before the operation.
        size_after: Structure size after the operation.
        elapsed_time: Wall-clock seconds for the single operation.
        complexity: Expected Big-O label, e.g. ``"O(1)"`` or ``"O(n)"``.
        state_before: Logical state snapshot taken before the operation.
        state_after: Logical state snapshot taken after the operation.
        step_trace: Optional human-readable walkthrough strings.
    """

    structure: str
    operation: str
    input_value: int | None
    anchor_value: int | None
    returned_value: int | bool | list[int] | None
    size_before: int
    size_after: int
    elapsed_time: float
    complexity: str
    state_before: list[int]
    state_after: list[int]
    step_trace: list[str] = field(default_factory=list)

# --------------------------------------------------------------- end dataclass OperationResult

# __________________________________________________________________________
# End of File
#
