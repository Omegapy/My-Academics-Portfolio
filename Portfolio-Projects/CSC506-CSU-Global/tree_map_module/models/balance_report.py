# -------------------------------------------------------------------------
# File: balance_report.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-21
# File Path: Portfolio-Milestone-Module-6/models/balance_report.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Define the node-level balance record returned by the BST analysis helpers.
# - Keep balance-report rows immutable and display-friendly.
# - Move per-node height and balance information between tree and UI layers.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Imports: dataclass support for the lightweight balance record.
# - Class Definitions - Data Classes: ``BalanceReport``.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses
# - Third-Party: none
# - Local Project Modules: none
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the BST implementation when building node-level balance rows.
# - Imported by Streamlit helpers to render balance summary tables.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for BST balance-report """

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
# Lightweight record used to explain how one BST node contributes to the
# tree's overall balance state.
#
# ------------------------------------------------------------------------- class BalanceReport
@dataclass(slots=True, kw_only=True)
class BalanceReport:
    """Summary of one node's left/right subtree height balance.

    Attributes:
        node_key: Key stored in the node being reported.
        left_height: Height of the left subtree rooted beneath the node.
        right_height: Height of the right subtree rooted beneath the node.
        balance_factor: ``left_height - right_height`` for the node.
        is_unbalanced: True when ``abs(balance_factor) > 1``.
    """

    node_key: object
    left_height: int
    right_height: int
    balance_factor: int
    is_unbalanced: bool

# ------------------------------------------------------------------------- end class BalanceReport

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------
