# -------------------------------------------------------------------------
# File: insertion_sort.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Implements classic shift-based insertion sort.
# Returns a SortResult with timing, comparisons, writes, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Insertion sort algorithm implementation.

Builds the sorted portion one element at a time by shifting larger
elements to the right and inserting the current key into its correct
position.

Time complexity:
    Best:    O(n)   — already sorted
    Average: O(n^2)
    Worst:   O(n^2) — reverse sorted

Space: O(1) auxiliary.
Stable: Yes.
"""

# ________________
# Imports
#

from __future__ import annotations

import time

from models.sort_result import SortResult

# __________________________________________________________________________
# Insertion Sort
#

# ========================================================================
# Constants
# ========================================================================

_MAX_TRACE_ITEMS: int = 25

# ========================================================================
# Insertion Sort Function
# ========================================================================

# --------------------------------------------------------------- insertion_sort()
def insertion_sort(
    data: list[int],
    *,
    collect_trace: bool = True,
) -> SortResult:
    """Sort *data* using insertion sort and return a SortResult.

    Uses shift-based insertion (not swap-based). The ``swaps`` field in the
    result is always 0 because insertion sort shifts elements rather than
    performing pairwise swaps.

    Works on a **copy** of *data* — the caller's list is never mutated.

    Args:
        data: The list of integers to sort.
        collect_trace: If True and the dataset is small enough, collect
            human-readable step-by-step trace strings.

    Returns:
        A fully populated SortResult.
    """
    n: int = len(data)
    arr: list[int] = data[:]  # SAFETY CHECK: work on a copy
    comparisons: int = 0
    writes: int = 0
    trace: list[str] = []
    do_trace: bool = collect_trace and n <= _MAX_TRACE_ITEMS

    # EDGE CASE: trivial input
    if n <= 1:
        return SortResult(
            algorithm="Insertion Sort",
            input_size=n,
            sorted_data=arr,
            comparisons=0,
            swaps=0,
            writes=0,
            elapsed_time=0.0,
            is_stable=True,
            is_in_place=True,
            extra_space="O(1)",
            step_trace=[],
        )

    # Step 1: start timer
    start: float = time.perf_counter()

    # Step 2: insertion sort — shift elements right, insert key
    for i in range(1, n):
        key: int = arr[i]
        j: int = i - 1
        shifts: int = 0

        # Shift elements that are greater than key
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            writes += 1  # each shift is one write
            j -= 1
            shifts += 1

        # Count the final comparison that ended the while loop
        if j >= 0:
            comparisons += 1  # comparison that evaluated to False

        # Insert the key into its correct position
        arr[j + 1] = key
        writes += 1  # the insertion write

        if do_trace:
            trace.append(
                f"Step {i}: insert key={key} at position {j + 1} "
                f"(shifted {shifts} element(s))"
            )

    # Step 3: stop timer
    elapsed: float = time.perf_counter() - start

    return SortResult(
        algorithm="Insertion Sort",
        input_size=n,
        sorted_data=arr,
        comparisons=comparisons,
        swaps=0,  # insertion sort shifts, not swaps
        writes=writes,
        elapsed_time=elapsed,
        is_stable=True,
        is_in_place=True,
        extra_space="O(1)",
        step_trace=trace,
    )
# --------------------------------------------------------------- end insertion_sort()

# __________________________________________________________________________
# End of File
#
