# -------------------------------------------------------------------------
# File: bubble_sort.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Implements classic bubble sort with an early-exit optimization.
# Returns a SortResult with timing, comparisons, swaps, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Bubble sort algorithm implementation.

Repeatedly steps through the list, compares adjacent elements, and swaps
them if they are in the wrong order. Includes an early-exit optimization
that terminates when a full pass produces zero swaps.

Time complexity:
    Best:    O(n)   — already sorted (with early exit)
    Average: O(n^2)
    Worst:   O(n^2)

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
# Bubble Sort
#

# ========================================================================
# Constants
# ========================================================================

# Maximum dataset size for which step traces are collected
_MAX_TRACE_ITEMS: int = 25

# ========================================================================
# Bubble Sort Function
# ========================================================================

# --------------------------------------------------------------- bubble_sort()
def bubble_sort(
    data: list[int],
    *,
    collect_trace: bool = True,
) -> SortResult:
    """Sort *data* using bubble sort and return a SortResult.

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
            algorithm="Bubble Sort",
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

    # Step 2: bubble sort with early-exit optimization
    for p in range(n - 1):
        swapped: bool = False
        for s in range(n - 1 - p):
            comparisons += 1
            if arr[s] > arr[s + 1]:
                # Swap adjacent elements
                if do_trace:
                    trace.append(
                        f"Pass {p + 1}, Step {s + 1}: compare data[{s}]={arr[s]} "
                        f"vs data[{s + 1}]={arr[s + 1]} → swap"
                    )
                arr[s], arr[s + 1] = arr[s + 1], arr[s]
                swaps += 1
                swapped = True
            else:
                if do_trace:
                    trace.append(
                        f"Pass {p + 1}, Step {s + 1}: compare data[{s}]={arr[s]} "
                        f"vs data[{s + 1}]={arr[s + 1]} → no swap"
                    )

        if do_trace:
            trace.append(f"  End of pass {p + 1}: {arr}")

        # OPTIMIZATION: early exit if no swaps occurred in this pass
        if not swapped:
            if do_trace:
                trace.append(f"  No swaps in pass {p + 1} — list is sorted, exiting early.")
            break

    # Step 3: stop timer
    elapsed: float = time.perf_counter() - start

    return SortResult(
        algorithm="Bubble Sort",
        input_size=n,
        sorted_data=arr,
        comparisons=comparisons,
        swaps=swaps,
        writes=swaps * 2,  # each swap writes two positions
        elapsed_time=elapsed,
        is_stable=True,
        is_in_place=True,
        extra_space="O(1)",
        step_trace=trace,
    )
# --------------------------------------------------------------- end bubble_sort()

# __________________________________________________________________________
# End of File
#
