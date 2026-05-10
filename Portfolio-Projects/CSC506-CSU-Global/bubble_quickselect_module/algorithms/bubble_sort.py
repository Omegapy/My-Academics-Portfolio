# File: bubble_sort.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Implement native Bubble Sort without relying on Python's built-in sort.
# - Count comparisons, swaps, writes, elapsed time, and early-exit behavior.
# - Collect readable trace lines for small classroom datasets.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# GLOBAL CONSTANTS:
#   - Constant: _MAX_TRACE_ITEMS - Trace collection size threshold
#
# BUBBLE SORT:
#   - Function: bubble_sort() - Sort integers and return a SortResult
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: time
# - Local Project Modules: bubble_quickselect_module.models.sort_result
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Called by Streamlit labs, benchmark recorders, and Bubble Sort unit tests.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Native Bubble Sort implementation for Portfolio Module 8.

Bubble Sort repeatedly compares adjacent values and swaps out-of-order pairs
until the list is sorted. This version includes the standard early-exit
optimization: if a full pass makes no swaps, the algorithm stops immediately.

Complexity:
    Best case: ``O(n)`` with early exit for already sorted input.
    Average case: ``O(n^2)``.
    Worst case: ``O(n^2)``.
    Space: ``O(1)`` auxiliary space for the conceptual in-place algorithm.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

import time

from bubble_quickselect_module.models.sort_result import SortResult


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# TRACE POLICY
# ========================================================================
# Small datasets receive human-readable trace lines for visualization; larger
# datasets skip tracing so benchmarks and app demos stay responsive.
#
# TRACE OVERVIEW:
# Bubble Sort can emit one trace line per adjacent comparison, so the trace
# threshold keeps classroom examples readable while protecting larger runs.
#
# Constraint: Larger inputs skip trace collection to avoid huge session output.
#

_MAX_TRACE_ITEMS: int = 25


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# BUBBLE SORT
# ========================================================================
# Contains the native adjacent-comparison sorting implementation used by the
# Module 8 Bubble Sort lab and benchmark pipeline.
#
# BUBBLE SORT OVERVIEW:
# Each pass compares adjacent values, swaps out-of-order pairs, and moves the
# largest remaining value toward the right side of the working list.
#
# STOPPING RULES:
#   1. Empty and one-item datasets return immediately as already sorted.
#   2. A no-swap pass triggers the early-exit optimization.
#   3. Otherwise, passes continue until the unsorted region is exhausted.
# =========================================================================
# - Function: bubble_sort()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- bubble_sort()
def bubble_sort(
    data: list[int],
    *,
    collect_trace: bool = True,
) -> SortResult:
    """Sort an integer list using Bubble Sort.

    Args:
        data: List of integers to sort.
        collect_trace: Whether to collect human-readable trace entries for
            small datasets.

    Returns:
        A ``SortResult`` containing sorted data, operation counts, timing,
        algorithm metadata, and optional trace entries.
    """
    original_data: list[int] = data[:]
    arr: list[int] = data[:]
    input_size: int = len(arr)
    comparisons: int = 0
    swaps: int = 0
    writes: int = 0
    early_exit_used: bool = False
    step_trace: list[str] = []
    do_trace: bool = collect_trace and input_size <= _MAX_TRACE_ITEMS

    # VALIDATION: empty and one-item lists are already sorted.
    # Returning before timing keeps the zero-work case easy to explain.
    if input_size <= 1:
        return SortResult(
            algorithm="Bubble Sort",
            input_size=input_size,
            original_data=original_data,
            sorted_data=arr,
            comparisons=0,
            swaps=0,
            writes=0,
            elapsed_time=0.0,
            is_stable=True,
            is_in_place=True,
            extra_space="O(1)",
            early_exit_used=False,
            step_trace=[],
        )

    start_time: float = time.perf_counter()

    # MAIN ITERATION LOOP: each pass moves the largest remaining value right.
    for pass_index in range(input_size - 1):
        # Step 1: assume this pass is sorted until a swap proves otherwise.
        swapped_this_pass: bool = False

        # Step 2: compare adjacent unsorted pairs.
        for compare_index in range(input_size - 1 - pass_index):
            left_index: int = compare_index
            right_index: int = compare_index + 1
            left_value: int = arr[left_index]
            right_value: int = arr[right_index]
            comparisons += 1

            # Step 3: swap only when the adjacent pair is out of order.
            if left_value > right_value:
                # TRACE: record the swap decision before mutating the working copy.
                if do_trace:
                    step_trace.append(
                        f"Pass {pass_index + 1}, compare indices "
                        f"{left_index} and {right_index}: {left_value} > "
                        f"{right_value}; swap."
                    )

                arr[left_index], arr[right_index] = arr[right_index], arr[left_index]
                swaps += 1
                writes += 2
                swapped_this_pass = True
            else:
                # TRACE: record stable no-swap decisions for small demonstrations.
                if do_trace:
                    step_trace.append(
                        f"Pass {pass_index + 1}, compare indices "
                        f"{left_index} and {right_index}: {left_value} <= "
                        f"{right_value}; no swap."
                    )

        if do_trace:
            step_trace.append(f"End of pass {pass_index + 1}: {arr}")

        # OPTIMIZATION: one no-swap pass proves the remaining data is sorted.
        if not swapped_this_pass:
            early_exit_used = True
            # Step 4: stop because this pass proved global sorted order.
            if do_trace:
                step_trace.append(
                    f"No swaps in pass {pass_index + 1}; list is sorted, "
                    "exiting early."
                )
            break

    elapsed_time: float = time.perf_counter() - start_time

    # Step 5: package algorithm metadata and operation counts for the UI.
    return SortResult(
        algorithm="Bubble Sort",
        input_size=input_size,
        original_data=original_data,
        sorted_data=arr,
        comparisons=comparisons,
        swaps=swaps,
        writes=writes,
        elapsed_time=elapsed_time,
        is_stable=True,
        is_in_place=True,
        extra_space="O(1)",
        early_exit_used=early_exit_used,
        step_trace=step_trace,
    )
# --------------------------------------------------------------- end bubble_sort()

# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
