# -------------------------------------------------------------------------
# File: benchmark_structures.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Benchmarking for the four required ADTs (Stack, Queue, Deque,
# LinkedList). Provides timing using fresh structure instances
# per timed run, a workload registry that defines every benchmark operation,
# CSV save/load helpers, and a winner computation that ranks operations
# within seven operation_group buckets.
# -------------------------------------------------------------------------

# --- Functions ---
# - build_structure()                — create + load a fresh ADT instance
# - benchmark_single()               — time one operation workload
# - run_benchmarks()                 — full benchmark matrix → DataFrame
# - save_results_csv()               — persist benchmark CSV
# - load_results_csv()               — reload saved benchmark CSV
# - compute_operation_winners()      — fastest structure per group/size
# - save_operation_winners_csv()     — persist winner CSV
# -------------------------------------------------------------------------

# --- Apache-2.0 --- 
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Benchmark Functions.

The functions below measures every workload on fresh structure instances
per size. For non-mutating workloads (``peek``, ``search``, ``display``)
it uses :func:`timeit.Timer.autorange` to amortize many calls. For
mutating workloads (``build``, ``drain``, single mutating operations) it
uses a custom timing loop that constructs a fresh structure outside the
timed region for every timed iteration, so the timing reflects the
operation itself rather than the setup cost.

Operations and operation groups:

| group                | operations                                                              |
|----------------------|--------------------------------------------------------------------------|
| common_build         | Stack.push, Queue.enqueue, Deque.addRear, LinkedList.insert(rear)        |
| common_drain         | Stack.pop, Queue.dequeue, Deque.removeFront, LinkedList.delete(head)     |
| peek_front           | Stack.peek, Queue.front, Deque.peekFront, Deque.peekRear                 |
| deque_ends           | Deque.addFront, Deque.addRear, Deque.removeFront, Deque.removeRear       |
| linked_list_search   | LinkedList.search(mid), LinkedList.search(missing)                       |
| linked_list_delete   | LinkedList.delete(head/tail/middle/missing)                              |
| linked_list_display  | LinkedList.display(False), LinkedList.display(True)                      |
"""

# ________________
# Imports
#

from __future__ import annotations

import time
import timeit
from pathlib import Path
from typing import Callable

import pandas as pd

from data.dataset_manager import (
    DEFAULT_BENCHMARK_SIZES,
    generate_sequential_dataset,
)
from data_structures import Deque, LinkedList, Node, Queue, Stack
from models.benchmark_record import BenchmarkRecord

# __________________________________________________________________________
# Constants
#

# ========================================================================
# Defaults
# ========================================================================

DEFAULT_SIZES: list[int] = list(DEFAULT_BENCHMARK_SIZES)
"""Required dataset sizes for the assignment benchmark."""

DEFAULT_REPEATS: int = 5
"""Number of timing repetitions per operation/size scenario."""

DEFAULT_RANDOM_SEED: int = 506
"""Seed used by deterministic dataset generation."""

# Categories
_CATEGORY_COMMON: str = "common"
_CATEGORY_SPECIFIC: str = "specific"

# Operation group identifiers
_GROUP_COMMON_BUILD: str = "common_build"
_GROUP_COMMON_DRAIN: str = "common_drain"
_GROUP_PEEK_FRONT: str = "peek_front"
_GROUP_DEQUE_ENDS: str = "deque_ends"
_GROUP_LL_SEARCH: str = "linked_list_search"
_GROUP_LL_DELETE: str = "linked_list_delete"
_GROUP_LL_DISPLAY: str = "linked_list_display"

# Common categories that run when include_specific=False
_COMMON_GROUPS: set[str] = {
    _GROUP_COMMON_BUILD,
    _GROUP_COMMON_DRAIN,
    _GROUP_PEEK_FRONT,
}

# __________________________________________________________________________
# Fast-Build Helpers
#

# ========================================================================
# Internal Fast Loaders
# ========================================================================

# --------------------------------------------------------------- _fast_build_stack()
def _fast_build_stack(values: list[int]) -> Stack:
    """Build a Stack of *values* in ``O(n)`` without re-pushing each item.

    Args:
        values: Bottom-to-top values.

    Returns:
        A populated :class:`Stack` instance.
    """
    s = Stack()
    s._items = list(values)  # noqa: SLF001
    return s
# --------------------------------------------------------------- end _fast_build_stack()


# --------------------------------------------------------------- _fast_build_queue()
def _fast_build_queue(values: list[int]) -> Queue:
    """Build a Queue of *values* in ``O(n)`` regardless of enqueue cost.

    *values* are interpreted in logical front-to-rear order. The Queue's
    course-aligned internal layout stores the front at the right end of
    the internal list, so the values are reversed when assigned.

    Args:
        values: Logical front-to-rear values.

    Returns:
        A populated :class:`Queue` instance.
    """
    q = Queue()
    q._items = list(reversed(values))  # noqa: SLF001
    return q
# --------------------------------------------------------------- end _fast_build_queue()


# --------------------------------------------------------------- _fast_build_deque()
def _fast_build_deque(values: list[int]) -> Deque:
    """Build a Deque of *values* in ``O(n)`` regardless of addRear cost.

    Args:
        values: Logical front-to-rear values.

    Returns:
        A populated :class:`Deque` instance.
    """
    d = Deque()
    d._items = list(reversed(values))  # noqa: SLF001
    return d
# --------------------------------------------------------------- end _fast_build_deque()


# --------------------------------------------------------------- _fast_build_linked_list()
def _fast_build_linked_list(values: list[int]) -> LinkedList:
    """Build a LinkedList of *values* in ``O(n)`` via direct node chaining.

    Bypasses the public ``insert_rear`` API to keep the helper symmetric
    with the other fast loaders.

    Args:
        values: Head-to-tail values.

    Returns:
        A populated :class:`LinkedList` instance.
    """
    ll = LinkedList()
    # If the list is empty, return it
    if not values:
        return ll
    nodes = [Node(data=v) for v in values]
    # Link the nodes together
    for idx in range(len(nodes) - 1):
        nodes[idx].next = nodes[idx + 1]
        nodes[idx + 1].prev = nodes[idx]
    ll.head = nodes[0]
    ll.tail = nodes[-1]
    ll.size = len(nodes)
    return ll
# --------------------------------------------------------------- end _fast_build_linked_list()

# __________________________________________________________________________
# Public Build Helper
#

# ========================================================================
# Public API
# ========================================================================

# --------------------------------------------------------------- build_structure()
def build_structure(structure_name: str, values: list[int]):
    """Create and load a fresh ADT instance using the public constructors.

    This is used by the Streamlit playground and tests to construct the same
    instance type the benchmark engine targets.

    Args:
        structure_name: One of ``"Stack"``, ``"Queue"``, ``"Deque"``, or
            ``"LinkedList"``.
        values: Items to load into the structure.

    Returns:
        A populated structure instance.

    Raises:
        ValueError: If *structure_name* is not recognized.
    """
    if structure_name == "Stack":
        return Stack(values)
    if structure_name == "Queue":
        return Queue(values)
    if structure_name == "Deque":
        return Deque(values)
    if structure_name == "LinkedList":
        return LinkedList(values)
    raise ValueError(f"Unknown structure {structure_name!r}")
# --------------------------------------------------------------- end build_structure()

# __________________________________________________________________________
# Timing Helpers
#

# ========================================================================
# Timing
# ========================================================================

# --------------------------------------------------------------- _time_static_call()
def _time_static_call(
    call: Callable[[], object],
    repeats: int,
) -> tuple[float, object]:
    """Time a non-mutating callable using ``timeit.Timer.autorange``.

    Args:
        call: Zero-argument callable that performs the workload. Must not
            mutate any external state, since the same callable is invoked
            many times.
        repeats: Number of timing repetitions.

    Returns:
        A ``(seconds_per_call, sample_return_value)`` tuple. The sample
        return value comes from a single direct invocation that runs
        outside the timing loop.
    """
    sample = call()  # capture for verification
    timer = timeit.Timer(call)
    loop_count, _ = timer.autorange()
    best_batch = min(timer.repeat(repeat=repeats, number=loop_count))
    return best_batch / loop_count, sample
# --------------------------------------------------------------- end _time_static_call()


# --------------------------------------------------------------- _time_with_setup()
def _time_with_setup(
    setup: Callable[[], object],
    call: Callable[[object], object],
    repeats: int,
) -> tuple[float, object]:
    """Time a mutating callable with a per-iteration fresh setup.

    Each iteration runs ``setup()`` outside the timing window to produce
    a fresh state, then times exactly one ``call(state)`` invocation. The
    minimum across repeated iterations is returned, which approximates
    the lower bound of the operation's runtime under noise.

    Args:
        setup: Zero-argument factory that produces a fresh state object.
        call: Single-argument callable invoked with the state object.
        repeats: Number of fresh-state timing repetitions.

    Returns:
        A ``(seconds_per_call, sample_return_value)`` tuple where the
        sample return value comes from the **last** timed iteration.
    """
    best: float = float("inf")
    sample: object = None
    for _ in range(repeats):
        state = setup()
        start = time.perf_counter()
        sample = call(state)
        elapsed = time.perf_counter() - start
        if elapsed < best:
            best = elapsed
    return best, sample
# --------------------------------------------------------------- end _time_with_setup()

# __________________________________________________________________________
# Workload Registry
#

# ========================================================================
# Workload Definition
# ========================================================================

# Each entry has the columns the BenchmarkRecord needs PLUS a "runner"
# callable. The runner accepts (size, repeats) and returns a tuple
# (time_seconds, sample_return_value, size_before, size_after, is_correct).
#
# The runner is responsible for setup, timing, correctness verification,
# and choosing whether to use _time_static_call or _time_with_setup.

# --------------------------------------------------------------- _runner_build()
def _runner_build(
    structure_name: str,
    push_op: Callable[[object, int], None],
    finalize_size: Callable[[object], int],
):
    """Build a runner that times constructing a fresh structure of size n.

    Args:
        structure_name: Display name for the structure.
        push_op: ``(structure, value) -> None`` add operation under test.
        finalize_size: ``(structure) -> int`` size accessor for verification.

    Returns:
        A runner callable accepted by the workload registry.
    """
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        # Setup the structure based on the structure name
        if structure_name == "Stack":
            def setup(): return Stack()
        elif structure_name == "Queue":
            def setup(): return Queue()
        elif structure_name == "Deque":
            def setup(): return Deque()
        else:
            def setup(): return LinkedList()
        # Call the push operation on the structure
        def call(state):
            for value in values:
                push_op(state, value)
            return state
        # Time the push operation
        elapsed, last_state = _time_with_setup(setup, call, repeats)
        size_after = finalize_size(last_state)
        is_correct = size_after == size
        return elapsed, size, 0, size_after, is_correct

    return runner
# --------------------------------------------------------------- end _runner_build()


# --------------------------------------------------------------- _runner_drain()
def _runner_drain(
    structure_name: str,
    pop_op: Callable[[object], object],
    finalize_size: Callable[[object], int],
):
    """Build a runner that times draining a preloaded structure of size n."""
    # Setup the structure based on the structure name
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        # Setup the structure based on the structure name
        if structure_name == "Stack":
            def setup(): return _fast_build_stack(values)
            expected_first = values[-1]  # LIFO: last pushed pops first
        elif structure_name == "Queue":
            def setup(): return _fast_build_queue(values)
            expected_first = values[0]  # FIFO
        elif structure_name == "Deque":
            def setup(): return _fast_build_deque(values)
            expected_first = values[0]  # removeFront
        else:
            def setup(): return _fast_build_linked_list(values)
            expected_first = values[0]  # delete(head_value)
        # Call the pop operation on the structure
        def call(state):
            first = pop_op(state)
            while finalize_size(state) > 0:
                pop_op(state)
            return first
        # Time the pop operation
        elapsed, first = _time_with_setup(setup, call, repeats)
        is_correct = first == expected_first
        return elapsed, size, size, 0, is_correct

    return runner
# --------------------------------------------------------------- end _runner_drain()


# --------------------------------------------------------------- _runner_static_peek()
def _runner_static_peek(
    structure_name: str,
    peek_op: Callable[[object], object],
    expected_index: int,
):
    """Build a runner for non-mutating peek/front operations."""
    # Setup the structure based on the structure name   
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        # Setup the structure based on the structure name
        if structure_name == "Stack":
            state = _fast_build_stack(values)
        elif structure_name == "Queue":
            state = _fast_build_queue(values)
        elif structure_name == "Deque":
            state = _fast_build_deque(values)
        else:
            state = _fast_build_linked_list(values)

        def call():
            return peek_op(state)
        # Time the peek operation
        elapsed, sample = _time_static_call(call, repeats)
        expected = values[expected_index]
        is_correct = sample == expected
        return elapsed, size, size, size, is_correct

    return runner
# --------------------------------------------------------------- end _runner_static_peek()


# --------------------------------------------------------------- _runner_deque_end_build()
def _runner_deque_end_build(end: str):
    """Build a runner for ``Deque.addFront`` / ``Deque.addRear`` build workloads."""
    # Setup the structure based on the structure name       
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        # Setup the structure based on the structure name
        def setup(): return Deque()
        # Call the addFront or addRear operation on the structure
        if end == "front":
            def call(state):
                for value in values:
                    state.addFront(value)
                return state
        else:
            def call(state):
                for value in values:
                    state.addRear(value)
                return state
        # Time the addFront or addRear operation on the structure
        elapsed, last_state = _time_with_setup(setup, call, repeats)
        is_correct = len(last_state) == size
        return elapsed, size, 0, size, is_correct

    return runner
# --------------------------------------------------------------- end _runner_deque_end_build()


# --------------------------------------------------------------- _runner_deque_end_drain()
def _runner_deque_end_drain(end: str):
    """Build a runner for ``Deque.removeFront`` / ``Deque.removeRear`` drain workloads."""
    # Setup the structure based on the structure name           
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        # Setup the structure based on the structure name
        def setup(): return _fast_build_deque(values)
        # Call the removeFront or removeRear operation on the structure
        if end == "front":
            expected_first = values[0]
            # Call the removeFront operation on the structure
            def call(state):
                first = state.removeFront()
                while len(state) > 0:
                    state.removeFront()
                return first
        else:
            expected_first = values[-1]
            # Call the removeRear operation on the structure
            def call(state):
                first = state.removeRear()
                while len(state) > 0:
                    state.removeRear()
                return first
        # Time the removeFront or removeRear operation on the structure
        elapsed, first = _time_with_setup(setup, call, repeats)
        is_correct = first == expected_first
        return elapsed, size, size, 0, is_correct

    return runner
# --------------------------------------------------------------- end _runner_deque_end_drain()


# --------------------------------------------------------------- _runner_ll_search_static()
def _runner_ll_search_static(target_kind: str):
    """Build a runner that times ``LinkedList.search`` (non-mutating)."""
    # Setup the structure based on the structure name           
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        ll = _fast_build_linked_list(values)
        # Setup the structure based on the structure name
        if target_kind == "middle":
            target = values[size // 2]
            should_find = True
        else:
            target = -1
            should_find = False
        # Call the search operation on the structure    
        def call():
            return ll.search(target)
        # Time the search operation
        elapsed, sample = _time_static_call(call, repeats)
        if should_find:
            is_correct = isinstance(sample, Node) and sample.data == target
        else:
            is_correct = sample is None
        return elapsed, size, size, size, is_correct

    return runner
# --------------------------------------------------------------- end _runner_ll_search_static()


# --------------------------------------------------------------- _runner_ll_delete_single()
def _runner_ll_delete_single(target_kind: str):
    """Build a runner that times a single ``LinkedList.delete`` call."""
    # Setup the structure based on the structure name           
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        # Setup the structure based on the structure name
        if target_kind == "head":
            target = values[0]
            should_find = True
        elif target_kind == "tail":
            target = values[-1]
            should_find = True
        elif target_kind == "middle":
            target = values[size // 2]
            should_find = True
        else:
            target = -1
            should_find = False
        # Setup the structure based on the structure name
        def setup(): return _fast_build_linked_list(values)
        # Call the delete operation on the structure
        def call(state):
            return state.delete(target)
        # Time the delete operation
        elapsed, sample = _time_with_setup(setup, call, repeats)
        is_correct = bool(sample) is should_find
        size_after = size - 1 if should_find else size
        return elapsed, size, size, size_after, is_correct

    return runner
# --------------------------------------------------------------- end _runner_ll_delete_single()


# --------------------------------------------------------------- _runner_ll_display()
def _runner_ll_display(reverse: bool):
    """Build a runner for ``LinkedList.display`` (non-mutating)."""
    # Se    tup the structure based on the structure name           
    def runner(size: int, repeats: int):
        values = generate_sequential_dataset(size)
        ll = _fast_build_linked_list(values)
        # Call the display operation on the structure
        def call():
            return ll.display(reverse=reverse)
        # Time the display operation
        elapsed, sample = _time_static_call(call, repeats)
        expected = list(reversed(values)) if reverse else list(values)
        is_correct = isinstance(sample, list) and sample == expected
        return elapsed, size, size, size, is_correct

    return runner
# --------------------------------------------------------------- end _runner_ll_display()

# __________________________________________________________________________
# Workload Registry Definition
#

# ========================================================================
# Workload Table
# ========================================================================

# Format: list of dicts. Each dict declares one benchmark workload row.
_WORKLOADS: list[dict[str, object]] = [
    # ---- common_build ----
    {
        "structure": "Stack",
        "operation": "push",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_BUILD,
        "complexity": "O(n)",
        "runner": _runner_build(
            "Stack",
            lambda s, v: s.push(v),
            lambda s: len(s),
        ),
    },
    {
        "structure": "Queue",
        "operation": "enqueue",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_BUILD,
        "complexity": "O(n^2)",
        "runner": _runner_build(
            "Queue",
            lambda q, v: q.enqueue(v),
            lambda q: len(q),
        ),
    },
    {
        "structure": "Deque",
        "operation": "addRear",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_BUILD,
        "complexity": "O(n^2)",
        "runner": _runner_build(
            "Deque",
            lambda d, v: d.addRear(v),
            lambda d: len(d),
        ),
    },
    {
        "structure": "LinkedList",
        "operation": "insert_rear",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_BUILD,
        "complexity": "O(n)",
        "runner": _runner_build(
            "LinkedList",
            lambda ll, v: ll.insert_rear(v),
            lambda ll: len(ll),
        ),
    },
    # ---- common_drain ----
    {
        "structure": "Stack",
        "operation": "pop",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_DRAIN,
        "complexity": "O(n)",
        "runner": _runner_drain(
            "Stack",
            lambda s: s.pop(),
            lambda s: len(s),
        ),
    },
    {
        "structure": "Queue",
        "operation": "dequeue",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_DRAIN,
        "complexity": "O(n)",
        "runner": _runner_drain(
            "Queue",
            lambda q: q.dequeue(),
            lambda q: len(q),
        ),
    },
    {
        "structure": "Deque",
        "operation": "removeFront",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_DRAIN,
        "complexity": "O(n)",
        "runner": _runner_drain(
            "Deque",
            lambda d: d.removeFront(),
            lambda d: len(d),
        ),
    },
    {
        "structure": "LinkedList",
        "operation": "delete_head",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_COMMON_DRAIN,
        "complexity": "O(n)",
        "runner": _runner_drain(
            "LinkedList",
            lambda ll: ll.delete(ll.head.data) if ll.head else None,
            lambda ll: len(ll),
        ),
    },
    # ---- peek_front ----
    {
        "structure": "Stack",
        "operation": "peek",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_PEEK_FRONT,
        "complexity": "O(1)",
        "runner": _runner_static_peek("Stack", lambda s: s.peek(), -1),
    },
    {
        "structure": "Queue",
        "operation": "front",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_PEEK_FRONT,
        "complexity": "O(1)",
        "runner": _runner_static_peek("Queue", lambda q: q.front(), 0),
    },
    {
        "structure": "Deque",
        "operation": "peekFront",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_PEEK_FRONT,
        "complexity": "O(1)",
        "runner": _runner_static_peek("Deque", lambda d: d.peekFront(), 0),
    },
    {
        "structure": "Deque",
        "operation": "peekRear",
        "category": _CATEGORY_COMMON,
        "operation_group": _GROUP_PEEK_FRONT,
        "complexity": "O(1)",
        "runner": _runner_static_peek("Deque", lambda d: d.peekRear(), -1),
    },
    # ---- deque_ends ----
    {
        "structure": "Deque",
        "operation": "addFront_build",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_DEQUE_ENDS,
        "complexity": "O(n)",
        "runner": _runner_deque_end_build("front"),
    },
    {
        "structure": "Deque",
        "operation": "addRear_build",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_DEQUE_ENDS,
        "complexity": "O(n^2)",
        "runner": _runner_deque_end_build("rear"),
    },
    {
        "structure": "Deque",
        "operation": "removeFront_drain",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_DEQUE_ENDS,
        "complexity": "O(n)",
        "runner": _runner_deque_end_drain("front"),
    },
    {
        "structure": "Deque",
        "operation": "removeRear_drain",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_DEQUE_ENDS,
        "complexity": "O(n^2)",
        "runner": _runner_deque_end_drain("rear"),
    },
    # ---- linked_list_search ----
    {
        "structure": "LinkedList",
        "operation": "search_middle",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_SEARCH,
        "complexity": "O(n)",
        "runner": _runner_ll_search_static("middle"),
    },
    {
        "structure": "LinkedList",
        "operation": "search_missing",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_SEARCH,
        "complexity": "O(n)",
        "runner": _runner_ll_search_static("missing"),
    },
    # ---- linked_list_delete ----
    {
        "structure": "LinkedList",
        "operation": "delete_head_single",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_DELETE,
        "complexity": "O(1)",
        "runner": _runner_ll_delete_single("head"),
    },
    {
        "structure": "LinkedList",
        "operation": "delete_tail_single",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_DELETE,
        "complexity": "O(n)",
        "runner": _runner_ll_delete_single("tail"),
    },
    {
        "structure": "LinkedList",
        "operation": "delete_middle_single",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_DELETE,
        "complexity": "O(n)",
        "runner": _runner_ll_delete_single("middle"),
    },
    {
        "structure": "LinkedList",
        "operation": "delete_missing_single",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_DELETE,
        "complexity": "O(n)",
        "runner": _runner_ll_delete_single("missing"),
    },
    # ---- linked_list_display ----
    {
        "structure": "LinkedList",
        "operation": "display_forward",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_DISPLAY,
        "complexity": "O(n)",
        "runner": _runner_ll_display(False),
    },
    {
        "structure": "LinkedList",
        "operation": "display_reverse",
        "category": _CATEGORY_SPECIFIC,
        "operation_group": _GROUP_LL_DISPLAY,
        "complexity": "O(n)",
        "runner": _runner_ll_display(True),
    },
]

# __________________________________________________________________________
# Public Benchmark Functions
#

# ========================================================================
# Single workload
# ========================================================================

# --------------------------------------------------------------- benchmark_single()
def benchmark_single(
    operation_name: str,
    structure_name: str,
    size: int,
    repeats: int = DEFAULT_REPEATS,
) -> BenchmarkRecord:
    """Time a single workload by ``(structure, operation)`` and return a record.

    Args:
        operation_name: Operation key from the workload registry, e.g.
            ``"push"``, ``"insert_rear"``, ``"search_middle"``.
        structure_name: Structure key, e.g. ``"Stack"``.
        size: Workload size to time at.
        repeats: Number of timing repetitions.

    Returns:
        A populated :class:`BenchmarkRecord`.

    Raises:
        ValueError: If no workload matches the given names.
    """
    # Iterate through the workload registry to find the matching workload
    for entry in _WORKLOADS:
        # Check if the workload matches the given names
        if entry["operation"] == operation_name and entry["structure"] == structure_name:
            runner = entry["runner"]
            elapsed_sec, size_before, size_before_check, size_after, is_correct = runner(  # type: ignore[misc]
                size, repeats,
            )
            # Convert the elapsed time from seconds to milliseconds and round to 6 decimal places
            time_ms = round(elapsed_sec * 1_000.0, 6)
            # Return the benchmark record
            return BenchmarkRecord(
                structure=str(entry["structure"]),
                operation=str(entry["operation"]),
                category=str(entry["category"]),
                size=int(size_before),
                time_ms=time_ms,
                returned_value=None,
                size_before=int(size_before_check),
                size_after=int(size_after),
                complexity=str(entry["complexity"]),
                is_correct=bool(is_correct),
                operation_group=str(entry["operation_group"]),
            )
    # Raise an error if no workload is found
    raise ValueError(
        f"No workload found for structure={structure_name!r}, "
        f"operation={operation_name!r}"
    )
# --------------------------------------------------------------- end benchmark_single()


# ========================================================================
# Full benchmark matrix
# ========================================================================

# --------------------------------------------------------------- run_benchmarks()
def run_benchmarks(
    sizes: list[int] | None = None,
    repeats: int = DEFAULT_REPEATS,
    include_specific: bool = True,
    progress_callback: Callable[[int, int, str], None] | None = None,
) -> pd.DataFrame:
    """Run the full benchmark matrix and return a DataFrame.

    Args:
        sizes: Workload sizes (default: :data:`DEFAULT_SIZES`).
        repeats: Timing repetitions per workload.
        include_specific: When False, only the common categories
            (``common_build``, ``common_drain``, ``peek_front``) are run.
        progress_callback: Optional ``(current, total, label)`` callback
            invoked after every workload completes.

    Returns:
        A DataFrame with one row per ``(structure, operation, size)``
        combination. Columns: ``structure``, ``operation``, ``category``,
        ``operation_group``, ``size``, ``time_ms``, ``size_before``,
        ``size_after``, ``complexity``, ``is_correct``.
    """
    # Set the sizes to the default sizes if no sizes are provided
    if sizes is None:
        sizes = list(DEFAULT_SIZES)
    # Filter the workloads based on the include_specific flag
    workloads = [
        entry for entry in _WORKLOADS
        if include_specific or entry["operation_group"] in _COMMON_GROUPS
    ]
    # Calculate the total number of workloads
    total = len(workloads) * len(sizes)
    current = 0
    rows: list[dict[str, object]] = []
    # Iterate through the sizes
    for size in sizes:
        # Iterate through the workloads
        for entry in workloads:
            current += 1
            if progress_callback is not None:
                label = (
                    f"{entry['structure']}.{entry['operation']} "
                    f"(n={size:,})"
                )
                progress_callback(current, total, label)
            # Benchmark the single workload
            record = benchmark_single(
                operation_name=str(entry["operation"]),
                structure_name=str(entry["structure"]),
                size=size,
                repeats=repeats,
            )
            # Append the benchmark record to the rows list
            rows.append({
                "structure": record.structure,
                "operation": record.operation,
                "category": record.category,
                "operation_group": record.operation_group,
                "size": record.size,
                "time_ms": record.time_ms,
                "size_before": record.size_before,
                "size_after": record.size_after,
                "complexity": record.complexity,
                "is_correct": record.is_correct,
            })

    return pd.DataFrame(rows)
# --------------------------------------------------------------- end run_benchmarks()

# __________________________________________________________________________
# CSV Persistence
#

# ========================================================================
# CSV
# ========================================================================

# --------------------------------------------------------------- save_results_csv()
def save_results_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Save a benchmark results DataFrame to a CSV file.

    Args:
        df: DataFrame returned by :func:`run_benchmarks`.
        path: Destination CSV path.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
# --------------------------------------------------------------- end save_results_csv()


# --------------------------------------------------------------- load_results_csv()
def load_results_csv(path: str | Path) -> pd.DataFrame:
    """Load benchmark results from a CSV file.

    Args:
        path: CSV path.

    Returns:
        A DataFrame with the saved benchmark data.
    """
    return pd.read_csv(path)
# --------------------------------------------------------------- end load_results_csv()

# __________________________________________________________________________
# Operation Winners
#

# ========================================================================
# Winners
# ========================================================================

# --------------------------------------------------------------- compute_operation_winners()
def compute_operation_winners(df: pd.DataFrame) -> pd.DataFrame:
    """Determine the fastest workload per ``(operation_group, size)`` bucket.

    Args:
        df: Benchmark results DataFrame.

    Returns:
        A DataFrame with columns: ``operation_group``, ``size``,
        ``fastest_structure``, ``fastest_operation``, ``fastest_time_ms``,
        ``runner_up``, ``notes``.
    """
    winners: list[dict[str, object]] = []
    # Group the DataFrame by operation group and size
    for (group, size), bucket in df.groupby(["operation_group", "size"]):
        # Sort the bucket by time_ms and reset the index
        ranked = bucket.sort_values("time_ms").reset_index(drop=True)
        # Get the best workload
        best = ranked.iloc[0]
        # Get the runner-up workload
        runner_up = ranked.iloc[1] if len(ranked) > 1 else best
        # Calculate the percentage faster
        if runner_up["time_ms"] > 0:
            pct_faster = round(
                (runner_up["time_ms"] - best["time_ms"])
                / runner_up["time_ms"] * 100.0,
                1,
            )
            notes = (
                f"For {group} at size {int(size):,}, "
                f"{best['structure']}.{best['operation']} wins at "
                f"{best['time_ms']:.4f} ms "
                f"({pct_faster}% faster than "
                f"{runner_up['structure']}.{runner_up['operation']})."
            )
        else:
            notes = (
                f"For {group} at size {int(size):,}, "
                f"{best['structure']}.{best['operation']} wins at "
                f"{best['time_ms']:.4f} ms."
            )
        # Append the winner to the winners list
        winners.append({
            "operation_group": group,
            "size": int(size),
            "fastest_structure": str(best["structure"]),
            "fastest_operation": str(best["operation"]),
            "fastest_time_ms": float(best["time_ms"]),
            "runner_up": (
                f"{runner_up['structure']}.{runner_up['operation']}"
            ),
            "notes": notes,
        })

    return pd.DataFrame(winners)
# --------------------------------------------------------------- end compute_operation_winners()


# --------------------------------------------------------------- save_operation_winners_csv()
def save_operation_winners_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Save an operation winners DataFrame to CSV.

    Args:
        df: DataFrame returned by :func:`compute_operation_winners`.
        path: Destination CSV path.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
# --------------------------------------------------------------- end save_operation_winners_csv()

# __________________________________________________________________________
# End of File
#
