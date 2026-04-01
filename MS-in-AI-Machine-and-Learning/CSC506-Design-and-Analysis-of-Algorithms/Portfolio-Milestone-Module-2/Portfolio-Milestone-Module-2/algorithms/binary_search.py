# -------------------------------------------------------------------------
# File: binary_search.py
# Author: Alexander Ricciardi
# Date: 2026-03-20
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Implements an iterative binary search over a sorted list of integers.
# Returns a SearchResult with timing, comparison count, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Binary search algorithm implementation.

Binary search halves the search data space on each
step. Requires the list to be sorted in ascending order. Returns a
SearchResult of the outcome, number of comparisons, elapsed
time, and step trace.
"""

# ________________
# Imports
#

from __future__ import annotations

import time

import sys
import os
# SETUP: add project root so sibling packages are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.search_result import SearchResult

# __________________________________________________________________________
# Binary Search
#

# ========================================================================
# Binary Search Function
# ========================================================================

# Maximum number of step-trace entries to keep
_MAX_TRACE_STEPS: int = 20

# --------------------------------------------------------------- binary_search()
def binary_search(
    data: list[int],
    target: int,
    *,
    validate_sorted: bool = True,
    collect_trace: bool = True,
) -> SearchResult:
    """Perform binary search for a target value (serached value) in a sorted list.

    The input list must be sorted in ascending order. If the list is
    not sorted, a ``ValueError`` is raised.

    Args:
        data: A sorted list of integers to search.
        target: The integer value to find.
        validate_sorted: If True, verify that *data* is sorted before
            searching. Callers that already guarantee sorted input can
            disable this check.
        collect_trace: If True, collect the step-by-step trace strings
            used by the UI. Benchmarking can disable this to avoid
            measuring presentation overhead.

    Returns:
        A SearchResult populated with algorithm name, outcome, comparisons,
        timing, and step trace.

    Raises:
        ValueError: If data is not sorted in ascending order.
    """
    trace: list[str] = []
    comparisons: int = 0
    dataset_size: int = len(data)

    # EDGE CASE: empty list
    if dataset_size == 0:
        return SearchResult(
            algorithm="Binary Search",
            target=target,
            found=False,
            index=None,
            comparisons=0,
            elapsed_time=0.0,
            dataset_size=0,
            sorted_required=True,
            step_trace=["Dataset is empty — nothing to search."] if collect_trace else [],
        )

    # Step 1: start timer
    start: float = time.perf_counter()

    # VALIDATION: ensure input is sorted when the caller has not already
    # guaranteed the precondition.
    if validate_sorted and any(data[i] > data[i + 1] for i in range(dataset_size - 1)):
        raise ValueError(
            "Binary search requires a sorted list. "
            "Please sort the dataset before calling binary_search()."
        )

    # Step 2: iterative binary search
    low: int = 0
    high: int = dataset_size - 1
    found_index: int | None = None

    while low <= high:
        mid: int = (low + high) // 2
        mid_value: int = data[mid]
        comparisons += 1

        # Build step trace (capped for large datasets)
        if collect_trace and len(trace) < _MAX_TRACE_STEPS:
            trace.append(
                f"Step {comparisons}: low={low}, high={high}, mid={mid}, "
                f"data[{mid}] = {mid_value}"
            )

        if mid_value == target:
            found_index = mid
            if collect_trace and len(trace) <= _MAX_TRACE_STEPS:
                trace.append(f"  → {mid_value} == {target}  → FOUND at index {mid}")
            break
        elif mid_value < target:
            if collect_trace and len(trace) <= _MAX_TRACE_STEPS:
                trace.append(f"  → {mid_value} < {target}  → search right half")
            low = mid + 1
        else:
            if collect_trace and len(trace) <= _MAX_TRACE_STEPS:
                trace.append(f"  → {mid_value} > {target}  → search left half")
            high = mid - 1

    # Step 3: stop timer
    elapsed: float = time.perf_counter() - start

    # Step 4: build summary line
    if collect_trace:
        if found_index is not None:
            trace.append(
                f"Target {target} found at index {found_index} after {comparisons} comparison(s)."
            )
        else:
            trace.append(
                f"Target {target} not found after {comparisons} comparison(s)."
            )

    return SearchResult(
        algorithm="Binary Search",
        target=target,
        found=found_index is not None,
        index=found_index,
        comparisons=comparisons,
        elapsed_time=elapsed,
        dataset_size=dataset_size,
        sorted_required=True,
        step_trace=trace if collect_trace else [],
    )
# --------------------------------------------------------------- end binary_search()

# __________________________________________________________________________
# End of File
#
