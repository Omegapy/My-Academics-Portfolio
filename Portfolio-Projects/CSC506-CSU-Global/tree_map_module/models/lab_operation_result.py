# -------------------------------------------------------------------------
# File: lab_operation_result.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-26
# File Path: Portfolio-Milestone-Module-6/models/lab_operation_result.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Define the immutable before-and-after result card used across the labs.
# - Keep operation metadata, structure state, and display text together.
# - Support guided demos, manual actions, and regression-test expectations.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Imports: dataclass support for operation result packaging.
# - Class Definitions - Data Classes: ``LabOperationResult``.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses
# - Third-Party: none
# - Local Project Modules: none
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by validation helpers and Streamlit app state packaging.
# - Rendered by Streamlit UI helpers as manual and guided result cards.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for guided and manual lab operation results"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from dataclasses import dataclass


# __________________________________________________________________________
# Data Classes
# ========================================================================
# TYPES AND DATA STRUCTURES
# ========================================================================
# This immutable record keeps the before/after state needed by the Module 6
# labs, validation demos, and Streamlit status panels.
#
# ------------------------------------------------------------------------- class LabOperationResult
@dataclass(slots=True, kw_only=True)
class LabOperationResult:
    """Immutable record of one BST or Map lab operation.

    Attributes:
        section: UI or validation section label.
        operation: Operation name, such as ``"insert"`` or ``"delete"``.
        input_key: Optional submitted key for the operation.
        input_value: Optional submitted value for the operation.
        returned_value: Value returned by the operation.
        success: True when the action completed successfully.
        size_before: Size before the operation.
        size_after: Size after the operation.
        height_before: Tree height before the operation, if applicable.
        height_after: Tree height after the operation, if applicable.
        balanced_before: Tree balance status before the operation.
        balanced_after: Tree balance status after the operation.
        tree_before_ascii: Text snapshot before the operation.
        tree_after_ascii: Text snapshot after the operation.
        message: Short user-facing summary of the result.
    """

    section: str
    operation: str
    input_key: object | None  # Remains ``None`` for summary-style or bulk operations.
    input_value: object | None  # Remains ``None`` for read-only operations.
    returned_value: object | None  # Remains ``None`` when the operation reports only status.
    success: bool
    size_before: int
    size_after: int
    height_before: int | None  # Remains ``None`` when a result does not track tree height.
    height_after: int | None  # Remains ``None`` when a result does not track tree height.
    balanced_before: bool | None  # Remains ``None`` when balance state is not applicable.
    balanced_after: bool | None  # Remains ``None`` when balance state is not applicable.
    tree_before_ascii: str
    tree_after_ascii: str
    message: str

# ----------------------------------------------------------- end class LabOperationResult

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------