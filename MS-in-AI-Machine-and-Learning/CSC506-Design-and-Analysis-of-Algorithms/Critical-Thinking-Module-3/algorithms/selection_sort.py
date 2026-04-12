# -------------------------------------------------------------------------
# File: selection_sort.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Implements classic selection sort with minimum-selection passes.
# Returns a SortResult with timing, comparisons, swaps, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Selection sort algorithm implementation.

Repeatedly finds the minimum element from the unsorted portion and places
it at the beginning of the unsorted region.

Time complexity:
    Best:    O(n^2)
    Average: O(n^2)
    Worst:   O(n^2)

Space: O(1) auxiliary.
Stable: No (swapping can change relative order of equal elements).
"""

# ________________
# Imports
#

from __future__ import annotations

import time

from models.sort_result import SortResult

# __________________________________________________________________________
# Selection Sort
#

# ========================================================================
# Constants
# ========================================================================

_MAX_TRACE_ITEMS: int = 25

# ========================================================================
# Selection Sort Function
# ========================================================================

# --------------------------------------------------------------- selection_sort()
def selection_sort(
    data: list[int],
    *,
    collect_trace: bool = True,
) -> SortResult:
    """Sort *data* using selection sort and return a SortResult.

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
    swaps: int = 0
    trace: list[str] = []
    do_trace: bool = collect_trace and n <= _MAX_TRACE_ITEMS

    # EDGE CASE: trivial input
    if n <= 1:
        return SortResult(
            algorithm="Selection Sort",
            input_size=n,
            sorted_data=arr,
            comparisons=0,
            swaps=0,
            writes=0,
            elapsed_time=0.0,
            is_stable=False,
            is_in_place=True,
            extra_space="O(1)",
            step_trace=[],
        )

    # Step 1: start timer
    start: float = time.perf_counter()

    # Step 2: selection sort — find minimum, swap into place
    for i in range(n - 1):
        min_idx: int = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Swap only if the minimum is not already in position
        if min_idx != i:
            if do_trace:
                trace.append(
                    f"Pass {i + 1}: find min={arr[min_idx]} at index {min_idx}, "
                    f"swap with data[{i}]={arr[i]}"
                )
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
        else:
            if do_trace:
                trace.append(
                    f"Pass {i + 1}: min={arr[i]} already at index {i}, no swap needed"
                )

    # Step 3: stop timer
    elapsed: float = time.perf_counter() - start

    return SortResult(
        algorithm="Selection Sort",
        input_size=n,
        sorted_data=arr,
        comparisons=comparisons,
        swaps=swaps,
        writes=swaps * 2,  # each swap writes two positions
        elapsed_time=elapsed,
        is_stable=False,
        is_in_place=True,
        extra_space="O(1)",
        step_trace=trace,
    )
# --------------------------------------------------------------- end selection_sort()

# __________________________________________________________________________
# End of File
#
