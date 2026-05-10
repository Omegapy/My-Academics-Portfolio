# -------------------------------------------------------------------------
# File: traversal_result.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-21
# File Path: Portfolio-Milestone-Module-6/models/traversal_result.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Define the immutable traversal summary record used by display helpers.
# - Keep traversal order, node count, and empty-state metadata together.
# - Support traversal-focused summaries in UI and validation code.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Imports: dataclass support for traversal summary packaging.
# - Class Definitions - Data Classes: ``TraversalResult``.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses
# - Third-Party: none
# - Local Project Modules: none
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Intended for traversal-focused helpers, summaries, and UI displays.
# - Provides a lightweight container for traversal output metadata.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for traversal-output summaries in Module 6.

This dataclass packages traversal order metadata, returned keys, and empty
state information so traversal-focused helpers and UI renderers can pass one
display-ready summary object instead of several parallel values.
"""

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
# Traversal results are small, display-friendly summaries that can move
# between analysis helpers, UI renderers, and tests without recomputation.
#
# ------------------------------------------------------------------------- class TraversalResult
@dataclass(slots=True, kw_only=True)
class TraversalResult:
    """Summary of one traversal output.

    Attributes:
        order_name: Traversal name such as ``"inorder"``.
        keys: Keys visited in traversal order.
        node_count: Number of keys returned.
        is_empty: True when the traversal result is empty.
    """

    order_name: str
    keys: list[object]
    node_count: int
    is_empty: bool

# -------------------------------------------------------------- end class TraversalResult

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------
