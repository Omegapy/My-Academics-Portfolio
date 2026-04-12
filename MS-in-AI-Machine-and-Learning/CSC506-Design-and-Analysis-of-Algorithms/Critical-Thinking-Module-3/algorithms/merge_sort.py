# -------------------------------------------------------------------------
# File: merge_sort.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Implements recursive divide-and-conquer merge sort.
# Returns a SortResult with timing, comparisons, writes, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Merge sort algorithm implementation.

Recursively divides the list in half, sorts each half, and merges the
sorted halves back together.

Time complexity:
    Best:    O(n log n)
    Average: O(n log n)
    Worst:   O(n log n)

Space: O(n) auxiliary (merge buffer).
Stable: Yes.
"""

# ________________
# Imports
#

from __future__ import annotations

import time

from models.sort_result import SortResult

# __________________________________________________________________________
# Merge Sort
#

# ========================================================================
# Constants
# ========================================================================

_MAX_TRACE_ITEMS: int = 25
_MAX_TRACE_ENTRIES: int = 50  # cap trace lines for small datasets

# ========================================================================
# Internal Helpers
# ========================================================================

# --------------------------------------------------------------- _merge()
def _merge(
    arr: list[int],
    left: int,
    mid: int,
    right: int,
    metrics: dict[str, int],
    trace: list[str] | None,
) -> None:
    """Merge two sorted sub-arrays arr[left..mid] and arr[mid+1..right].

    Args:
        arr: The working array (mutated in place).
        left: Start index of the left sub-array.
        mid: End index of the left sub-array.
        right: End index of the right sub-array.
        metrics: Shared mutable dict with ``"comparisons"`` and ``"writes"``
            keys, accumulated across all recursion frames.
        trace: If not None, append high-level merge descriptions.
    """
    # Step 1: create temporary copies of the two halves
    left_half: list[int] = arr[left:mid + 1]
    right_half: list[int] = arr[mid + 1:right + 1]

    i: int = 0  # index into left_half
    j: int = 0  # index into right_half
    k: int = left  # index into arr

    # Step 2: merge elements from both halves in sorted order
    while i < len(left_half) and j < len(right_half):
        metrics["comparisons"] += 1
        if left_half[i] <= right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        metrics["writes"] += 1
        k += 1

    # Step 3: copy remaining elements from left half
    while i < len(left_half):
        arr[k] = left_half[i]
        metrics["writes"] += 1
        i += 1
        k += 1

    # Step 4: copy remaining elements from right half
    while j < len(right_half):
        arr[k] = right_half[j]
        metrics["writes"] += 1
        j += 1
        k += 1

    # Step 5: trace the merge operation
    if trace is not None and len(trace) < _MAX_TRACE_ENTRIES:
        merged_preview = arr[left:right + 1]
        if len(merged_preview) > 10:
            preview = str(merged_preview[:5])[:-1] + ", ...]"
        else:
            preview = str(merged_preview)
        trace.append(
            f"Merge [{left}..{mid}] + [{mid + 1}..{right}] → {preview}"
        )
# --------------------------------------------------------------- end _merge()


# --------------------------------------------------------------- _merge_sort_recursive()
def _merge_sort_recursive(
    arr: list[int],
    left: int,
    right: int,
    metrics: dict[str, int],
    trace: list[str] | None,
) -> None:
    """Recursively divide and merge-sort arr[left..right].

    Args:
        arr: The working array (mutated in place).
        left: Start index.
        right: End index.
        metrics: Shared mutable metrics dict.
        trace: Trace list or None.
    """
    if left < right:
        mid: int = (left + right) // 2
        _merge_sort_recursive(arr, left, mid, metrics, trace)
        _merge_sort_recursive(arr, mid + 1, right, metrics, trace)
        _merge(arr, left, mid, right, metrics, trace)
# --------------------------------------------------------------- end _merge_sort_recursive()

# ========================================================================
# Merge Sort Public Function
# ========================================================================

# --------------------------------------------------------------- merge_sort()
def merge_sort(
    data: list[int],
    *,
    collect_trace: bool = True,
) -> SortResult:
    """Sort *data* using merge sort and return a SortResult.

    Works on a **copy** of *data* — the caller's list is never mutated.

    Args:
        data: The list of integers to sort.
        collect_trace: If True and the dataset is small enough, collect
            higher-level merge trace strings.

    Returns:
        A fully populated SortResult.
    """
    n: int = len(data)
    arr: list[int] = data[:]  # SAFETY CHECK: work on a copy
    metrics: dict[str, int] = {"comparisons": 0, "writes": 0}
    trace: list[str] | None = [] if (collect_trace and n <= _MAX_TRACE_ITEMS) else None

    # EDGE CASE: trivial input
    if n <= 1:
        return SortResult(
            algorithm="Merge Sort",
            input_size=n,
            sorted_data=arr,
            comparisons=0,
            swaps=0,
            writes=0,
            elapsed_time=0.0,
            is_stable=True,
            is_in_place=False,
            extra_space="O(n)",
            step_trace=[],
        )

    # Step 1: start timer
    start: float = time.perf_counter()

    # Step 2: recursive merge sort
    _merge_sort_recursive(arr, 0, n - 1, metrics, trace)

    # Step 3: stop timer
    elapsed: float = time.perf_counter() - start

    return SortResult(
        algorithm="Merge Sort",
        input_size=n,
        sorted_data=arr,
        comparisons=metrics["comparisons"],
        swaps=0,  # merge sort does not swap in place
        writes=metrics["writes"],
        elapsed_time=elapsed,
        is_stable=True,
        is_in_place=False,
        extra_space="O(n)",
        step_trace=trace if trace is not None else [],
    )
# --------------------------------------------------------------- end merge_sort()

# __________________________________________________________________________
# End of File
#
