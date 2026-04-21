# File: lab_operation_result.py 
#
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
# -------------------------------------------------------------------------
# Module Functionality
# Dataclass used by the anual lab sections to capture one operation's
# returned value, timing, size change, summary text, and compact before/after
# structure snapshots for inline Streamlit display.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for a manual CTA-5 lab operation result."""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from dataclasses import dataclass, field


# ______________________________________________________________________________
# Class Definitions – Data Classes
# ==============================================================================
# TYPES AND DATA STRUCTURES
# ==============================================================================
# Manual-lab result dataclass produced by analysis.lab_validation helpers and
# consumed by the Streamlit Hash Table / Priority Queue lab tabs.
# - Class: LabOperationResult (Dataclass) - One manual operation snapshot
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------- class LabOperationResult
@dataclass
class LabOperationResult:
    """Immutable record of one manual CTA-5 lab operation.

    Attributes:
        structure: Structure or lab name shown in the UI.
        operation: Operation name such as ``"insert"`` or ``"peek"``.
        returned_value: Value returned by the underlying operation.
        elapsed_time: Wall-clock time for the single operation in seconds.
        complexity: Expected Big-O label for the operation.
        size_before: Structure size before the operation.
        size_after: Structure size after the operation.
        summary: Short user-facing description of the outcome.
        input_details: Optional display lines describing submitted inputs.
        state_label: Label used for the before/after snapshot panels.
        state_before: Compact pre-operation structure snapshot.
        state_after: Compact post-operation structure snapshot.
        state_before_highlight_idx: Optional row index to highlight in the
            before snapshot.
        state_after_highlight_idx: Optional row index to highlight in the
            after snapshot.

    Logic:
        This dataclass packages everything the Streamlit lab tabs render per op.
        1. Capture the operation identity (structure, operation, complexity).
        2. Capture the timing and size-change metrics for inline display.
        3. Carry compact before/after snapshots and optional highlight indices.
    """

    structure: str
    operation: str
    returned_value: object | None
    elapsed_time: float
    complexity: str
    size_before: int
    size_after: int
    summary: str
    # Optional input echo lines populated only when inputs are user-visible.
    input_details: list[str] = field(default_factory=list)
    state_label: str = "State Snapshot"
    # Snapshot lists default to empty when no before/after rendering is needed.
    state_before: list[str] = field(default_factory=list)
    state_after: list[str] = field(default_factory=list)
    # Highlight indices become non-None only when the UI should mark a row.
    state_before_highlight_idx: int | None = None
    state_after_highlight_idx: int | None = None


# ------------------------------------------------------------------------- end class LabOperationResult

# ==============================================================================
# End of File
# ==============================================================================
