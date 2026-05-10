# File: quickselect.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Implement deterministic Quickselect for kth-smallest selection.
# - Count partition comparisons, swaps, writes, elapsed time, and correctness.
# - Collect readable partition traces for small classroom datasets.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# GLOBAL CONSTANTS:
#   - Constant: _MAX_TRACE_ITEMS - Trace collection size threshold
#
# QUICKSELECT:
#   - Function: quickselect() - Select the 1-based kth-smallest integer
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: time
# - Local Project Modules: bubble_quickselect_module.models.quickselect_result
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Called by Streamlit labs, benchmark recorders, and Quickselect unit tests.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Native Quickselect implementation for Portfolio Module 8.

Quickselect finds the kth-smallest value without fully sorting the dataset. This
implementation uses an iterative Lomuto partition with the rightmost active
value as the deterministic pivot, making classroom traces reproducible.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

import time

from bubble_quickselect_module.models.quickselect_result import QuickSelectResult


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# TRACE POLICY
# ========================================================================
# Small datasets receive partition traces for visualization; larger datasets
# skip tracing to keep interactive runs and benchmarks lightweight.
#
# TRACE OVERVIEW:
# Quickselect can produce multiple partition narration lines per loop, so the
# trace threshold keeps small demonstrations explainable without flooding UI.
#
# Constraint: Trace output is limited so worst-case partition runs remain usable.
#

_MAX_TRACE_ITEMS: int = 25


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# QUICKSELECT
# ========================================================================
# Contains the native partition-based selection algorithm used by the Module 8
# Quickselect lab and benchmark pipeline.
#
# QUICKSELECT OVERVIEW:
# Quickselect finds one rank by partitioning around a pivot and continuing only
# into the side that can still contain the requested kth-smallest value.
#
# STOPPING RULES:
#   1. Invalid empty data or out-of-range k raises ValueError before timing.
#   2. A pivot landing on the target rank returns the selected value.
#   3. The active bounds shrink until the target rank is isolated.
# =========================================================================
# - Function: quickselect()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- quickselect()
def quickselect(
    data: list[int],
    k: int,
    *,
    collect_trace: bool = True,
) -> QuickSelectResult:
    """Find the 1-based kth-smallest value using iterative Quickselect.

    Args:
        data: List of integers to search.
        k: User-facing 1-based kth-smallest position.
        collect_trace: Whether to collect human-readable trace entries for
            small datasets.

    Returns:
        A ``QuickSelectResult`` containing the selected value, final partitioned
        data, operation counts, timing, correctness metadata, and trace entries.

    Raises:
        ValueError: If the dataset is empty or ``k`` is outside the valid range.
    """
    # VALIDATION: fail before timing so invalid calls do not produce results.
    if not data:
        raise ValueError("Quickselect requires at least one value.")
    # VALIDATION: user-facing k must map to an existing zero-based rank.
    if k < 1 or k > len(data):
        raise ValueError("k must be between 1 and the dataset size.")

    original_data: list[int] = data[:]
    arr: list[int] = data[:]
    input_size: int = len(arr)
    zero_based_rank: int = k - 1
    comparisons: int = 0
    swaps: int = 0
    writes: int = 0
    step_trace: list[str] = []
    do_trace: bool = collect_trace and input_size <= _MAX_TRACE_ITEMS

    start_time: float = time.perf_counter()
    left: int = 0
    right: int = input_size - 1
    selected_value: int | None = None

    # MAIN ITERATION LOOP: narrow the active partition until the rank is found.
    while left <= right:
        # Step 1: choose a deterministic pivot at the right edge.
        pivot_value: int = arr[right]
        store_index: int = left

        # TRACE: show the active partition bounds before rearranging values.
        if do_trace:
            step_trace.append(
                f"Search bounds {left}-{right}; pivot index {right}, "
                f"pivot value {pivot_value}."
            )

        # Step 1: partition values less than or equal to the pivot to the left.
        for scan_index in range(left, right):
            comparisons += 1

            # Step 2: move values on the left side when they belong before pivot.
            if arr[scan_index] <= pivot_value:
                # OPTIMIZATION: avoid counting a swap when the item is already placed.
                if scan_index != store_index:
                    if do_trace:
                        step_trace.append(
                            f"  Move {arr[scan_index]} <= {pivot_value}: "
                            f"swap indices {scan_index} and {store_index}."
                        )
                    arr[scan_index], arr[store_index] = (
                        arr[store_index],
                        arr[scan_index],
                    )
                    swaps += 1
                    writes += 2
                else:
                    # TRACE: keep equal/smaller values in place when no swap is needed.
                    if do_trace:
                        step_trace.append(
                            f"  Keep {arr[scan_index]} at index {scan_index}; "
                            f"it is <= pivot {pivot_value}."
                        )
                store_index += 1
            else:
                # TRACE: values greater than the pivot stay in the right partition.
                if do_trace:
                    step_trace.append(
                        f"  Leave {arr[scan_index]} on the right side; "
                        f"it is > pivot {pivot_value}."
                    )

        # Step 2: place the pivot after the <= partition.
        if store_index != right:
            # MUTATION: put the pivot in its final sorted-order position.
            if do_trace:
                step_trace.append(
                    f"Place pivot {pivot_value}: swap indices {store_index} "
                    f"and {right}."
                )
            arr[store_index], arr[right] = arr[right], arr[store_index]
            swaps += 1
            writes += 2
        else:
            # TRACE: the pivot is already positioned after the left partition.
            if do_trace:
                step_trace.append(
                    f"Pivot {pivot_value} already belongs at index {store_index}."
                )

        pivot_index: int = store_index

        if do_trace:
            step_trace.append(
                f"Pivot final position {pivot_index}; current data: {arr}"
            )

        # Step 3: choose the next active side or finish.
        if pivot_index == zero_based_rank:
            selected_value = arr[pivot_index]
            # CONVERGENCE: the pivot landed exactly on the requested rank.
            if do_trace:
                step_trace.append(
                    f"Target rank {zero_based_rank} found with value "
                    f"{selected_value}."
                )
            break

        # DISPATCH: search only the side that can still contain the target rank.
        if pivot_index < zero_based_rank:
            if do_trace:
                step_trace.append(
                    f"Target rank {zero_based_rank} is right of pivot; "
                    f"search {pivot_index + 1}-{right} next."
                )
            left = pivot_index + 1
        else:
            if do_trace:
                step_trace.append(
                    f"Target rank {zero_based_rank} is left of pivot; "
                    f"search {left}-{pivot_index - 1} next."
                )
            right = pivot_index - 1

    elapsed_time: float = time.perf_counter() - start_time

    # SAFETY CHECK: the loop must find a value for every validated input.
    if selected_value is None:
        selected_value = arr[zero_based_rank]

    expected: int = sorted(original_data)[zero_based_rank]
    is_correct: bool = selected_value == expected

    # Step 4: package the selected value, final partition state, and metadata.
    return QuickSelectResult(
        algorithm="Quickselect",
        input_size=input_size,
        original_data=original_data,
        partitioned_data=arr,
        k=k,
        zero_based_rank=zero_based_rank,
        selected_value=selected_value,
        comparisons=comparisons,
        swaps=swaps,
        writes=writes,
        elapsed_time=elapsed_time,
        is_correct=is_correct,
        step_trace=step_trace,
    )
# --------------------------------------------------------------- end quickselect()

# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
