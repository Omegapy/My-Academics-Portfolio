# -------------------------------------------------------------------------
# File: benchmark_utils.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Provides repeatable benchmarking for Stack, Queue, and
# LinkedList. Each benchmark builds a fresh data structure
# before each repetition, then times a specific operation.
# -------------------------------------------------------------------------

# --- Functions ---
# - benchmark_operation(): Generic timer for a single operation + sizes.
# - benchmark_stack(): Benchmark push and pop.
# - benchmark_queue(): Benchmark enqueue and dequeue.
# - benchmark_linked_list(): Benchmark prepend, append, search, delete.
# - run_all_benchmarks(): Execute all benchmarks and collect results.
# - save_results_csv(): Write results list to a CSV file.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - time for high-resolution operation timing.
# - csv for writing results.
# - sys and os for import-path setup.
# - data_structures package for Stack, Queue, LinkedList.
# -------------------------------------------------------------------------

"""
Benchmarking utilities for Stack, Queue, and LinkedList.

Functions populate fresh data structures to the target size for each
repetition, then time only the requested operation using a
high-resolution timer. Results are collected as lists of dicts that
can be used by DataFrames or CSV export.
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

import csv
import os
import sys
from time import perf_counter
from typing import Any, Callable

# SETUP - CTA-1 is on sys.path so data_structures can be imported
_CTA1_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CTA1_DIR not in sys.path:
    sys.path.insert(0, _CTA1_DIR)

from data_structures import Stack, Queue, LinkedList

# ==============================================================================
# CONSTANTS
# ==============================================================================

# Default input sizes 
DEFAULT_SIZES: list[int] = [10, 100, 1_000, 5_000, 10_000]

# Default number of repeats per timing run
DEFAULT_REPEATS: int = 50

# ==============================================================================
# FUNCTIONS
# ==============================================================================

# -------------------------------------------------------------- benchmark_operation()
def benchmark_operation(
    setup_fn: Callable[[int], Any],
    operation_fn: Callable[[Any], None],
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
    structure: str = "",
    operation: str = "",
) -> list[dict[str, Any]]:
    """Time a single operation across multiple input sizes.

    Args:
        setup_fn: Callable that takes an input size ``n`` and returns a
            pre-populated data structure (or any state needed by the op).
        operation_fn: Callable that takes the state returned by
            ``setup_fn`` and executes the operation to be timed.
        sizes: List of input sizes to test. Defaults to ``DEFAULT_SIZES``.
        repeats: Number of times to execute the operation per size.
        structure: Name label for the data structure (for result dicts).
        operation: Name label for the operation (for result dicts).

    Returns:
        A list of dicts with keys: ``structure``, ``operation``, ``n``,
        ``repeats``, ``total_time``, ``avg_time``.

    Notes:
        A fresh state is created for every repetition before the timer
        starts. This keeps setup and restore work outside the measured
        interval so the recorded time reflects only the target
        operation.
    """
    if sizes is None:
        sizes = DEFAULT_SIZES

    results: list[dict[str, Any]] = []
    for n in sizes:
        total = 0.0
        for _ in range(repeats):
            # Step 1: Build fresh data structure before timing begins
            state = setup_fn(n)
            # Step 2: Time only the requested operation
            start = perf_counter()
            operation_fn(state)
            total += perf_counter() - start
        avg = total / repeats
        results.append({
            "structure": structure,
            "operation": operation,
            "n": n,
            "repeats": repeats,
            "total_time": round(total, 8),
            "avg_time": round(avg, 8),
        })
    return results
# -------------------------------------------------------------- end benchmark_operation()


# -------------------------------------------------------------- benchmark_stack()
def benchmark_stack(
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
) -> list[dict[str, Any]]:
    """Benchmark Stack push and pop operations.

    Args:
        sizes: Input sizes to test.
        repeats: Number of timing repetitions.

    Returns:
        Combined results for push and pop.
    """
    results: list[dict[str, Any]] = []

    # ---- Push benchmark ----
    # Setup: build a stack of size n, then time one additional push.
    def setup_push(n: int) -> Stack:
        s = Stack()
        for i in range(n):
            s.push(i)
        return s

    def op_push(s: Stack) -> None:
        s.push(0)

    results.extend(benchmark_operation(
        setup_push, op_push, sizes, repeats, "Stack", "push",
    ))

    # ---- Pop benchmark ----
    # Setup: build a stack of size n, then time a single pop.
    def setup_pop(n: int) -> Stack:
        s = Stack()
        for i in range(n):
            s.push(i)
        return s

    def op_pop(s: Stack) -> None:
        s.pop()

    results.extend(benchmark_operation(
        setup_pop, op_pop, sizes, repeats, "Stack", "pop",
    ))

    return results
# -------------------------------------------------------------- end benchmark_stack()


# -------------------------------------------------------------- benchmark_queue()
def benchmark_queue(
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
) -> list[dict[str, Any]]:
    """Benchmark Queue enqueue and dequeue operations.

    Args:
        sizes: Input sizes to test.
        repeats: Number of timing repetitions.

    Returns:
        Combined results for enqueue and dequeue.
    """
    results: list[dict[str, Any]] = []

    # ---- Enqueue benchmark ----
    def setup_enqueue(n: int) -> Queue:
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        return q

    def op_enqueue(q: Queue) -> None:
        q.enqueue(0)

    results.extend(benchmark_operation(
        setup_enqueue, op_enqueue, sizes, repeats, "Queue", "enqueue",
    ))

    # ---- Dequeue benchmark ----
    def setup_dequeue(n: int) -> Queue:
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        return q

    def op_dequeue(q: Queue) -> None:
        q.dequeue()

    results.extend(benchmark_operation(
        setup_dequeue, op_dequeue, sizes, repeats, "Queue", "dequeue",
    ))

    return results
# -------------------------------------------------------------- end benchmark_queue()


# -------------------------------------------------------------- benchmark_linked_list()
def benchmark_linked_list(
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
) -> list[dict[str, Any]]:
    """Benchmark LinkedList prepend, append, search, and delete operations.

    Args:
        sizes: Input sizes to test.
        repeats: Number of timing repetitions.

    Returns:
        Combined results for prepend, append, search, and delete.

    Logic:
        - Prepend: O(1) — insert at head.
        - Append: O(n) — traverse to tail every time.
        - Search: O(n) — search for the last element (worst case).
        - Delete: O(n) — delete the last element (worst-case traversal).
    """
    results: list[dict[str, Any]] = []

    # ---- Prepend benchmark ----
    def setup_prepend(n: int) -> LinkedList:
        ll = LinkedList()
        for i in range(n):
            ll.prepend(i)
        return ll

    def op_prepend(ll: LinkedList) -> None:
        ll.prepend(-1)

    results.extend(benchmark_operation(
        setup_prepend, op_prepend, sizes, repeats, "LinkedList", "prepend",
    ))

    # ---- Append benchmark ----
    # Append is O(n) because it traverses to the tail.
    def setup_append(n: int) -> LinkedList:
        ll = LinkedList()
        for i in range(n):
            ll.prepend(i)  # Build with prepend (fast) for setup
        return ll

    def op_append(ll: LinkedList) -> None:
        ll.append(-1)

    results.extend(benchmark_operation(
        setup_append, op_append, sizes, repeats, "LinkedList", "append",
    ))

    # ---- Search benchmark (worst case: search for last element) ----
    def setup_search(n: int) -> tuple[LinkedList, int]:
        ll = LinkedList()
        for i in range(n):
            ll.prepend(i)  # 0 will be the last element (tail)
        return (ll, 0)  # Search for 0 — the tail node

    def op_search(state: tuple[LinkedList, int]) -> None:
        ll, target = state
        ll.search(target)

    results.extend(benchmark_operation(
        setup_search, op_search, sizes, repeats, "LinkedList", "search",
    ))

    # ---- Delete benchmark (worst case: delete last element) ----
    def setup_delete(n: int) -> LinkedList:
        ll = LinkedList()
        # Build list: prepend 0..n-1, then append a sentinel at the tail
        for i in range(n):
            ll.prepend(i)
        ll.append(-1)  # -1 is at the tail
        return ll

    def op_delete(ll: LinkedList) -> None:
        ll.delete(-1)   # Traverses to tail — O(n)

    results.extend(benchmark_operation(
        setup_delete, op_delete, sizes, repeats, "LinkedList", "delete",
    ))

    return results
# -------------------------------------------------------------- end benchmark_linked_list()


# -------------------------------------------------------------- run_all_benchmarks()
def run_all_benchmarks(
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
) -> list[dict[str, Any]]:
    """Execute all benchmarks and return combined results.

    Args:
        sizes: Input sizes to test.
        repeats: Number of timing repetitions.

    Returns:
        A list of result dicts from all structure benchmarks.
    """
    results: list[dict[str, Any]] = []
    results.extend(benchmark_stack(sizes, repeats))
    results.extend(benchmark_queue(sizes, repeats))
    results.extend(benchmark_linked_list(sizes, repeats))
    return results
# -------------------------------------------------------------- end run_all_benchmarks()


# -------------------------------------------------------------- save_results_csv()
def save_results_csv(
    results: list[dict[str, Any]],
    path: str,
) -> None:
    """Write benchmark results to a CSV file.

    Args:
        results: List of result dicts as returned by ``run_all_benchmarks``.
        path: File path for the output CSV.
    """
    if not results:
        return
    fieldnames = ["structure", "operation", "n", "repeats", "total_time", "avg_time"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
# -------------------------------------------------------------- end save_results_csv()

# ==============================================================================
# End of File
# ==============================================================================
