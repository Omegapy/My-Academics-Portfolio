# -------------------------------------------------------------------------
# File: benchmark_record.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# BenchmarkRecord dataclass representing one timed benchmark scenario row.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data model for benchmark timing records.

Each BenchmarkRecord captures one algorithm's performance on one
(dataset_type, size) scenario.
"""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass

# __________________________________________________________________________
# BenchmarkRecord Dataclass
#

# ========================================================================
# BenchmarkRecord
# ========================================================================
# --------------------------------------------------------------- dataclass BenchmarkRecord
@dataclass
class BenchmarkRecord:
    """One row in the benchmark results table.

    Args:
        algorithm: Algorithm name (e.g., "Merge Sort").
        dataset_type: One of "random", "sorted", "reverse_sorted", "partially_sorted".
        size: Dataset size.
        time_ms: Median or best normalized time in milliseconds.
        comparisons: Comparisons used during the sort.
        swaps: Swap count.
        writes: Write/move count.
        is_correct: Whether the output matches Python's sorted().
    """

    algorithm: str
    dataset_type: str
    size: int
    time_ms: float
    comparisons: int
    swaps: int
    writes: int
    is_correct: bool

# --------------------------------------------------------------- end dataclass BenchmarkRecord

# __________________________________________________________________________
# End of File
#
