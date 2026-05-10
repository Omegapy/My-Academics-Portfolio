# File: lab_operation_result.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Dataclass used by manual Streamlit graph labs to show operation results.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - LabOperationResult captures before/after snapshots for UI graph actions.
# - The model keeps action labels, success flags, return values, and notes together.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Returned by Streamlit lab helpers and displayed by paired operation renderers.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Manual lab operation result model."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from dataclasses import dataclass, field


# ______________________________________________________________________________
# Class Definitions - Data Classes
# ==============================================================================
# LAB OPERATION DATA MODELS
# ==============================================================================
# Immutable lab results keep UI before/after comparisons reproducible.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class LabOperationResult
@dataclass(frozen=True)
class LabOperationResult:
    """Capture one manual graph-lab operation.

    Args:
        structure: Structure name shown in the UI.
        operation: Operation name.
        returned_value: Value returned by the operation.
        elapsed_time: Wall-clock time in seconds.
        complexity: Expected Big-O label.
        size_before: Edge count before the operation.
        size_after: Edge count after the operation.
        order_before: Optional vertex count before the operation.
        order_after: Optional vertex count after the operation.
        summary: User-facing operation summary.
        input_details: Optional input echo lines.
        state_label: Label for before/after snapshots.
        state_before: Compact snapshot before the operation.
        state_after: Compact snapshot after the operation.
        dot_before: Graphviz DOT snapshot before the operation.
        dot_after: Graphviz DOT snapshot after the operation.

    Logic:
        This dataclass mirrors CTA-5's operation-result cards while carrying
        graph-specific snapshots.
    """

    structure: str
    operation: str
    returned_value: object | None
    elapsed_time: float
    complexity: str
    size_before: int
    size_after: int
    summary: str
    order_before: int | None = None
    order_after: int | None = None
    input_details: list[str] = field(default_factory=list)
    state_label: str = "Graph Snapshot"
    state_before: list[str] = field(default_factory=list)
    state_after: list[str] = field(default_factory=list)
    dot_before: str = ""
    dot_after: str = ""


# ------------------------------------------------------------------------- end class LabOperationResult

# ==============================================================================
# End of File
# ==============================================================================