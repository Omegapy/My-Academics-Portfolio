# -------------------------------------------------------------------------
# File: benchmark_record.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-21
# File Path: Portfolio-Milestone-Module-6/models/benchmark_record.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Define the immutable timing row used by the benchmark pipeline.
# - Keep CSV, DataFrame, chart, and Markdown summary fields aligned.
# - Carry optional tree-only metadata alongside generic timing fields.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Imports: dataclass support for benchmark result packaging.
# - Class Definitions - Data Classes: ``BenchmarkRecord``.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses
# - Third-Party: none
# - Local Project Modules: none
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the benchmark pipeline before rows are converted to DataFrames.
# - Consumed by CSV export, report generation, and Streamlit benchmark views.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for benchmark timing records"""

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
# One benchmark record maps directly to one timing row that will later be
# written to CSV, summarized in Markdown, and plotted in charts.
#
# ------------------------------------------------------------------------- class BenchmarkRecord
@dataclass(slots=True, kw_only=True)
class BenchmarkRecord:
    """One row of benchmark output.

    Attributes:
        method: Method or structure label, such as ``"TreeMap"``.
        scenario: Dataset-shape scenario, such as ``"random_insertion"``.
        query_mode: Search workload mode, such as ``"hits"`` or ``"misses"``.
        size: Number of items in the structure.
        time_ms: Best measured runtime in milliseconds.
        repeat_count: Number of repeated timing attempts.
        height: Tree height when applicable, else ``None``.
        is_balanced: Tree balance status when applicable, else ``None``.
        notes: Optional explanatory note for the record.
    """

    method: str
    scenario: str
    query_mode: str
    size: int
    time_ms: float
    repeat_count: int
    height: int | None  # Remains ``None`` for ListMap rows that do not have tree height.
    is_balanced: bool | None  # Remains ``None`` for ListMap rows with no tree structure.
    notes: str = ""  # Optional context that explains dataset flavor or caveats.
# -------------------------------------------------------------- end class BenchmarkRecord

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------
