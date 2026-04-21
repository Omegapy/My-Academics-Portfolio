# File: benchmark_record.py 
#
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
#
# -------------------------------------------------------------------------
# Module Functionality
# BenchmarkRecord dataclass for one benchmark row.
# Stores the structure, operation, scenario, timing, correctness, and
# benchmark-specific health metrics needed by the Streamlit Benchmark Lab,
# CSV artifacts, and written-analysis placeholders.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for CTA-5 benchmark timing records."""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from dataclasses import dataclass


# ______________________________________________________________________________
# Class Definitions – Data Classes
# ==============================================================================
# TYPES AND DATA STRUCTURES
# ==============================================================================
# Benchmark-row dataclass from analysis.benchmark_search workloads and
# consumed by the Streamlit Benchmark Lab, CSV exports, and written analysis.
# - Class: BenchmarkRecord (Dataclass) - One timed workload row
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------- class BenchmarkRecord
@dataclass
class BenchmarkRecord:
    """One row in the CTA-5 benchmark results table.

    Attributes:
        structure: Structure or baseline name, such as ``"Hash Table"``.
        operation: Timed operation label such as ``"insert_bulk"``.
        operation_group: Logical workload group such as
            ``"search_comparison"``.
        scenario: Scenario label such as ``"hits"`` or ``"max_heap"``.
        size: Dataset size used for the workload.
        workload_count: Number of underlying operations performed inside the
            timed workload.
        time_ms: Normalized runtime in milliseconds.
        avg_time_us: Average runtime per underlying operation in microseconds.
        complexity: Expected Big-O label for the operation.
        is_correct: True when the workload passed its correctness checks.
        size_before: Structure size before the workload.
        size_after: Structure size after the workload.
        found_count: Number of successful lookups, when applicable.
        deleted_count: Number of successful deletions, when applicable.
        collision_count: Collision count observed for hash-table workloads.
        load_factor: Load factor observed for hash-table workloads.
        heap_valid_after: Heap-validity flag for priority-queue workloads.
        speedup_vs_linear: Speedup ratio for hash-table search rows.
        notes: Human-readable summary for tables and analysis text.

    Logic:
        This dataclass is the canonical benchmark row used across the project.
        1. Carry workload identity (structure, operation, group, scenario, size).
        2. Carry primary timing metrics (time_ms, avg_time_us) for tables/charts.
        3. Carry workload-specific health fields (collision_count, heap_valid_after, etc.)
           that may be None when not applicable to the structure.
    """
    # Workload identity
    structure: str
    operation: str
    operation_group: str
    scenario: str
    size: int
    workload_count: int
    time_ms: float
    avg_time_us: float
    complexity: str
    is_correct: bool
    size_before: int
    size_after: int
    # Optional fields populated only for workloads where the metric is meaningful.
    found_count: int | None
    deleted_count: int | None
    collision_count: int | None
    load_factor: float | None
    heap_valid_after: bool | None
    speedup_vs_linear: float | None
    notes: str


# ------------------------------------------------------------------------- end class BenchmarkRecord

# ==============================================================================
# End of File
# ==============================================================================
