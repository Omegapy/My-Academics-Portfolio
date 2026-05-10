# File: set_operation_result.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Store before/after metadata for one CourseSet playground operation.
# - Preserve returned values, derived result sets, complexity labels, and notes.
# - Support manual history tables and automatic operation demos in Streamlit.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# DATA CLASSES:
#   - Class: SetOperationResult - result from one manual or automatic set operation
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: collections.abc, dataclasses
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Created by the Bubble Quickselect Sets overview page after set operations run.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Result model for one Bubble Quickselect Sets playground operation."""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass, field


# __________________________________________________________________________
# Class Definitions - Data Classes
# ========================================================================
# SET OPERATION RESULT
# ========================================================================
# Contains the typed result model used by manual and automatic CourseSet demos.
#
# DATACLASS CONTENTS:
#   - Class: SetOperationResult - before/after state for one set operation
# -------------------------------------------------------------------------
# Constraint: Optional operand fields are populated only for two-set operations.
# Rationale: The UI can render dynamic and static operations with one result shape.

# ------------------------------------------------------------------------- class SetOperationResult
@dataclass(slots=True, kw_only=True)
class SetOperationResult:
    """Store the outcome of one set playground operation.

    Attributes:
        operation: Operation name such as ``"add"`` or ``"union"``.
        target_set: Primary set label.
        operand_set: Optional secondary operand label.
        input_value: Optional value used for dynamic operations.
        returned_value: Value returned by the operation.
        result_values: Derived result values for static operations.
        size_before: Target set size before the operation.
        size_after: Target set size after the operation.
        elapsed_time: Wall-clock seconds for the operation.
        complexity: Expected Big-O label.
        state_before: Target set state before the operation.
        state_after: Target set state after the operation.
        notes: Human-readable operation notes.
        operand_before: Optional secondary operand state before the operation.
        operand_after: Optional secondary operand state after the operation.
        step_trace: Optional human-readable operation trace entries.

    Logic:
        This dataclass records set operation behavior for consistent rendering.
        1. Store the selected operation, operands, return value, and complexity.
        2. Preserve before/after state so the UI can explain mutations.
        3. Leave optional operand fields empty for single-set dynamic operations.
    """

    operation: str
    target_set: str
    operand_set: str | None  # Populated only for two-set static operations.
    input_value: Hashable | None  # Populated only for dynamic value operations.
    returned_value: object
    result_values: list[Hashable] | None  # Populated when a derived set is returned.
    size_before: int
    size_after: int
    elapsed_time: float
    complexity: str
    state_before: list[Hashable]
    state_after: list[Hashable]
    notes: str
    operand_before: list[Hashable] | None = None  # Two-set operations only.
    operand_after: list[Hashable] | None = None  # Two-set operations only.
    step_trace: list[str] = field(default_factory=list)

# -------------------------------------------------------- end class SetOperationResult

# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
