# -------------------------------------------------------------------------
# File: linear_search.py
# Author: Alexander Ricciardi
# Date: 2026-03-29
# # -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Implements a linear (sequential) search over a list of integers.
# Returns a SearchResult with timing, comparison count, and step trace.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Linear search algorithm implementation.

Sequentially scan from index 0 through the end of the list,
returning a SearchResult of the outcome, number of comparisons,
elapsed time, and step trace.
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
# Linear Search
#

# ========================================================================
# Linear Search Function
# ========================================================================

# Maximum number of step-trace entries to keep (prevents huge traces)
_MAX_TRACE_STEPS: int = 20

# --------------------------------------------------------------- linear_search()
def linear_search(
    data: list[int],
    target: int,
    *,
    collect_trace: bool = True,
) -> SearchResult:
    """Perform a linear (sequential) search for *target* in *data*.

    Scans every element from index 0 to the end. Works on both sorted
    and unsorted lists.

    Args:
        data: The list of integers to search.
        target: The integer value to find.
        collect_trace: If True, collect the step-by-step trace strings
            used by the UI. Benchmarking can disable this to avoid
            measuring presentation overhead.

    Returns:
        A SearchResult populated with algorithm name, outcome, comparisons,
        timing, and step trace.
    """
    trace: list[str] = []
    comparisons: int = 0
    dataset_size: int = len(data)

    # EDGE CASE: empty list
    if dataset_size == 0:
        return SearchResult(
            algorithm="Linear Search",
            target=target,
            found=False,
            index=None,
            comparisons=0,
            elapsed_time=0.0,
            dataset_size=0,
            sorted_required=False,
            step_trace=["Dataset is empty — nothing to search."] if collect_trace else [],
        )

    # Step 1: start timer
    start: float = time.perf_counter()

    # Step 2: sequential scan
    found_index: int | None = None
    for i, value in enumerate(data):
        comparisons += 1

        # Build step trace (capped for large datasets)
        if collect_trace:
            if len(trace) < _MAX_TRACE_STEPS:
                if value == target:
                    trace.append(f"Step {comparisons}: data[{i}] = {value} == {target}  → FOUND")
                else:
                    trace.append(f"Step {comparisons}: data[{i}] = {value} != {target}")
            elif len(trace) == _MAX_TRACE_STEPS:
                trace.append("... (remaining steps omitted for brevity)")

        if value == target:
            found_index = i
            break

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
                f"Target {target} not found after scanning all {comparisons} element(s)."
            )

    return SearchResult(
        algorithm="Linear Search",
        target=target,
        found=found_index is not None,
        index=found_index,
        comparisons=comparisons,
        elapsed_time=elapsed,
        dataset_size=dataset_size,
        sorted_required=False,
        step_trace=trace if collect_trace else [],
    )
# --------------------------------------------------------------- end linear_search()

# __________________________________________________________________________
# End of File
#
