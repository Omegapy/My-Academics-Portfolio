# File: benchmark_search.py 
#
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
#
# -------------------------------------------------------------------------
# Module Functionality
# This module is the benchmark engine for the hash-table and
# priority-queue workloads. Produces reproducible timing rows, summary
# tables, and benchmark-linked visualization states for the Streamlit app.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Benchmark engine for the CTA-5 Benchmark Lab."""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from dataclasses import asdict, dataclass
import random
import time
import timeit
from pathlib import Path
from typing import Callable

import pandas as pd

from algorithms.hash_table import HashTable
from algorithms.linear_search import linear_search_by_key
from algorithms.priority_queue import BinaryHeapPriorityQueue
from data.dataset_manager import (
    generate_collision_keys,
    generate_key_value_dataset,
    generate_priority_items,
    generate_search_queries,
)
from models.benchmark_record import BenchmarkRecord
from models.priority_item import PriorityItem

# ______________________________________________________________________________
# Global Constants / Variables
# ==============================================================================
# BENCHMARK CONSTANTS & METHODOLOGY
# ==============================================================================
#
# TIMING METHODOLOGY:
#   Read-only uses``timeit.Timer.autorange`` to handle overhead
#   and the minimum-of-repeats sample to suppress jitter.
#
# WORKLOAD TAXONOMY:
#   _GROUP_SEARCH_COMPARISON  - Hash table vs linear search rows used by the
#                               assignment's headline speedup chart.
#   _GROUP_HASH_CORE          - Hash-table insert/search/delete on normal data.
#   _GROUP_HASH_COLLISION     - Same operations on the forced-collision dataset.
#   _GROUP_PRIORITY_CORE      - Priority-queue insert/peek/extract/search/delete.
#
# REPRODUCIBILITY:
#   Every workload is fed by a deterministic BenchmarkDatasetBundle built once
#   per size from a single seed. Running the matrix twice with the same seed
#   reproduces the same input data even if timings differ.
# ------------------------------------------------------------------------------

# Constraint: dataset sizes covered by the CTA-5 assignment matrix.
# Rationale: matches the rubric's required scaling sweep.
DEFAULT_SIZES: list[int] = [100, 500, 1_000, 5_000, 10_000]
"""Supported CTA-5 benchmark sizes."""

# Constraint: query modes exercised by the search-comparison block.
# Rationale: covers all-hits, all-misses, and an interleaved workload.
DEFAULT_QUERY_MODES: list[str] = ["hits", "misses", "mixed"]
"""Search-comparison query modes."""

# Constraint: number of lookup queries issued per search workload.
# Rationale: large enough to swamp per-call overhead at every size.
DEFAULT_QUERY_COUNT: int = 500
"""Number of lookup queries per search workload."""

# Constraint: ceiling on deterministic delete operations per workload.
# Rationale: keeps mutating runs cheap enough to repeat for stable timings.
DEFAULT_DELETE_SAMPLE_SIZE: int = 250
"""Maximum number of deterministic delete operations per delete workload."""

# Constraint: number of timing repetitions per workload.
# Rationale: smallest sample size that reliably suppresses GC / JIT jitter.
DEFAULT_REPEATS: int = 3
"""Number of timing repetitions used for stable measurements."""

# Constraint: shared random seed for benchmark data generation.
# Rationale: matches the dataset_manager default so demos and benchmarks align.
DEFAULT_RANDOM_SEED: int = 506
"""Default seed for reproducible benchmark data."""

# Constraint: priority-queue heap modes covered by the priority-core matrix.
# Rationale: assignment requires both max-heap and min-heap behavior.
DEFAULT_HEAP_MODES: list[str] = ["max", "min"]
"""Priority-queue benchmark modes."""

# Constraint: fixed bucket count for forced-collision hash-table scenarios.
# Rationale: small prime keeps clustered collisions visible without resizing.
DEFAULT_COLLISION_CAPACITY: int = 53
"""Fixed bucket count for forced-collision hash-table scenarios."""

# Constraint: bucket index targeted by the single-bucket collision generator.
# Rationale: bucket 0 is easy to reason about in lab/demo diagrams.
DEFAULT_COLLISION_TARGET_BUCKET: int = 0
"""Bucket index targeted by forced-collision workloads."""

# Constraint: target buckets used by the clustered-collision benchmark.
# Rationale: spreading collisions across a small set yields informative occupancy charts.
DEFAULT_COLLISION_BENCHMARK_BUCKETS: tuple[int, ...] = (0, 11, 22, 33, 44)
"""Target buckets used by the benchmark's clustered-collision scenario."""

# Group tags wired into BenchmarkRecord.operation_group for downstream filtering.
_GROUP_SEARCH_COMPARISON = "search_comparison"  # Hash vs linear headline rows
_GROUP_HASH_CORE = "hash_core"                  # Hash table on normal data
_GROUP_HASH_COLLISION = "hash_collision"        # Hash table on collision data
_GROUP_PRIORITY_CORE = "priority_queue_core"    # Priority queue workloads

# Method-name and operation-name sets used by validation / reporting helpers.
_SEARCH_COMPARISON_METHODS = {"Hash Table", "Linear Search"}
_PRIORITY_MUTATING_OPERATIONS = {"insert_bulk", "extract_top_drain", "delete_sample"}

# ______________________________________________________________________________
# Class definitions
# ==============================================================================
# INTERNAL DATA MODELS
# ==============================================================================
# Frozen dataclasses that includes deterministic inputs (BenchmarkDatasetBundle)
# and workload metadata (WorkloadSpec) so the runners can iterate
# the benchmark.
# ------------------------------------------------------------------------------

#   ------------------------------------------------  class BenchmarkDatasetBundle
@dataclass(frozen=True)
class BenchmarkDatasetBundle:
    """Prebuilt deterministic inputs reused across one benchmark size.

    Attributes:
        size: Logical record count this bundle was generated for.
        seed: Seed used when generating every dataset in the bundle.
        normal_records: Key/value pairs from the normal generator.
        normal_record_map: Lookup map of normal records for validation.
        collision_records: Key/value pairs whose hashes cluster in hot buckets.
        collision_record_map: Lookup map of collision records for validation.
        priority_items: Deterministic priority items for heap workloads.
        priority_item_map: Label -> item map for priority-queue validation.
        normal_hash_table: Pre-populated hash table over *normal_records*.
        collision_hash_table: Pre-populated hash table over *collision_records*.
        priority_queues: Mode -> pre-populated heap (one per heap mode).
        hash_queries: Query mode -> hash-search query list.
        collision_hit_queries: Hit-only queries against the collision table.
        priority_queries: "hits"/"misses" -> priority-search query list.
        hash_delete_keys: Deterministic delete sample for the normal table.
        collision_delete_keys: Deterministic delete sample for the collision table.
        priority_delete_labels: Deterministic delete sample for priority queues.
    """

    size: int
    seed: int
    normal_records: list[tuple[str, int]]
    normal_record_map: dict[str, int]
    collision_records: list[tuple[str, int]]
    collision_record_map: dict[str, int]
    priority_items: list[PriorityItem]
    priority_item_map: dict[str, PriorityItem]
    normal_hash_table: HashTable
    collision_hash_table: HashTable
    priority_queues: dict[str, BinaryHeapPriorityQueue]
    hash_queries: dict[str, list[str]]
    collision_hit_queries: list[str]
    priority_queries: dict[str, list[str]]
    hash_delete_keys: list[str]
    collision_delete_keys: list[str]
    priority_delete_labels: list[str]
# -------------------------------------------- end class BenchmarkDatasetBundle


# ---------------------------------------------------------- class WorkloadSpec
@dataclass(frozen=True)
class WorkloadSpec:
    """Declarative description of one benchmark workload family.

    Attributes:
        structure: Human-readable structure label ("Hash Table", "Priority Queue", ...).
        operation: Operation name written into the BenchmarkRecord.
        operation_group: Group tag for downstream filtering / charting.
        scenario_kind: Drives _scenario_values to expand the matrix per workload.
        fixed_scenario: Single scenario string for "fixed" scenario_kind workloads.
        runner: Callable that materializes a BenchmarkRecord for one cell.
    """

    structure: str
    operation: str
    operation_group: str
    scenario_kind: str
    fixed_scenario: str | None
    runner: Callable[[BenchmarkDatasetBundle, str, int], BenchmarkRecord]
# ------------------------------------------------------ end class WorkloadSpec

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# TIMING HELPERS
# ==============================================================================
# Low-level helpers that normalize elapsed times into reporting units and
# wrap the actual ``time.perf_counter`` / ``timeit`` calls used by every
# workload runner.
#
# - Function: _normalize_ms()                 - Seconds -> rounded milliseconds
# - Function: _normalize_avg_us()             - Seconds -> avg microseconds/op
# - Function: _autorange_normalized_time()    - timeit.autorange + min repeats
# - Function: _time_search_loop()             - Wall-clock timing for search batch
# - Function: estimate_search_time()          - Public read-only timing helper
# - Function: benchmark_hash_table_search()   - Convenience wrapper for hash search
# - Function: benchmark_linear_search()       - Convenience wrapper for linear search
# - Function: _best_mutating_run()            - Min-of-repeats for mutating runs
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _normalize_ms()
def _normalize_ms(elapsed_seconds: float) -> float:
    """Convert elapsed seconds to rounded milliseconds.

    Logic:
        1. Multiply seconds by 1_000 to land in milliseconds.
        2. Round to 6 decimal places so CSV output stays compact.
    """
    return round(elapsed_seconds * 1_000.0, 6)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _normalize_avg_us()
def _normalize_avg_us(elapsed_seconds: float, workload_count: int) -> float:
    """Convert elapsed seconds to average microseconds per operation.

    Logic:
        1. SAFETY CHECK: return 0.0 when workload_count is non-positive.
        2. Divide seconds by workload count, scale to microseconds, and round.
    """
    # SAFETY CHECK: guard against division by zero or negative work counts
    if workload_count <= 0:
        return 0.0
    return round((elapsed_seconds / workload_count) * 1_000_000.0, 6)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _autorange_normalized_time()
def _autorange_normalized_time(
    callable_: Callable[[], object | None],
    repeats: int = DEFAULT_REPEATS,
) -> float:
    """Measure a read-only callable using ``timeit.Timer.autorange``.

    Logic:
        1. Wrap *callable_* in a timeit.Timer so it can be measured repeatedly.
        2. Use autorange() to choose a loop count that smooths per-call overhead.
        3. Repeat *repeats* trials and return the per-call minimum (best sample).
    """
    timer = timeit.Timer(callable_)
    loops, _ = timer.autorange()
    samples = timer.repeat(repeat=max(repeats, 1), number=loops)
    return min(samples) / loops
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _time_search_loop()
def _time_search_loop(
    search_func: Callable[[str], object | None],
    queries: list[str],
) -> tuple[float, int]:
    """Time one full search-query batch and count successful lookups.

    Logic:
        1. Initialize the success counter and capture a perf_counter start time.
        2. MAIN ITERATION LOOP: invoke *search_func* on every query and count hits.
        3. Return the wall-clock elapsed seconds and the success count.
    """
    found = 0
    start_time = time.perf_counter()
    # MAIN ITERATION LOOP: issue each query and count non-None results as hits
    for query in queries:
        if search_func(query) is not None:
            found += 1
    elapsed_seconds = time.perf_counter() - start_time
    return elapsed_seconds, found
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- estimate_search_time()
def estimate_search_time(
    search_func: Callable[[str], object | None],
    queries: list[str],
    repeats: int = DEFAULT_REPEATS,
) -> tuple[float, int]:
    """Benchmark a read-only search workload using autorange normalization.

    Logic:
        1. Run a single uninstrumented batch to capture the success count.
        2. Build a closure that issues every query without counting (timing only).
        3. Hand the closure to _autorange_normalized_time and return both values.
    """
    # Step 1: warm-up pass also captures the expected found count
    _, found_count = _time_search_loop(search_func, queries)

    # Step 2: closure batches all queries into one timed unit
    def _batched_search() -> None:
        for query in queries:
            search_func(query)

    # Step 3: autorange normalization smooths per-call overhead
    elapsed_seconds = _autorange_normalized_time(_batched_search, repeats)
    return elapsed_seconds, found_count
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- benchmark_hash_table_search()
def benchmark_hash_table_search(
    hash_table: HashTable,
    queries: list[str],
    repeats: int = DEFAULT_REPEATS,
) -> tuple[float, int]:
    """Benchmark the hash table's search method.

    Logic:
        1. Delegate to estimate_search_time, supplying ``hash_table.search``.
    """
    return estimate_search_time(hash_table.search, queries, repeats)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- benchmark_linear_search()
def benchmark_linear_search(
    records: list[tuple[str, object]],
    queries: list[str],
    repeats: int = DEFAULT_REPEATS,
) -> tuple[float, int]:
    """Benchmark the linear-search baseline.

    Logic:
        1. Wrap linear_search_by_key in a closure that captures *records*.
        2. Delegate to estimate_search_time using the closure as the search callable.
    """

    def _search(key: str) -> object | None:
        return linear_search_by_key(records, key)

    return estimate_search_time(_search, queries, repeats)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _best_mutating_run()
def _best_mutating_run(
    runner: Callable[[], dict[str, object]],
    repeats: int = DEFAULT_REPEATS,
) -> dict[str, object]:
    """Run a mutating workload repeatedly and keep the fastest valid result.

    Logic:
        1. Initialize a running "best" slot and clamp repeats to at least one.
        2. REPETITION LOOP: invoke *runner*, comparing elapsed_seconds to the best.
        3. SAFETY CHECK: raise if no result was produced (defensive guard).
        4. Return the fastest result dict.
    """
    best_result: dict[str, object] | None = None
    # REPETITION LOOP: keep the run with the lowest elapsed_seconds
    for _ in range(max(repeats, 1)):
        result = runner()
        if best_result is None or float(result["elapsed_seconds"]) < float(best_result["elapsed_seconds"]):
            best_result = result
    # SAFETY CHECK: at least one repeat must have executed
    if best_result is None:
        raise RuntimeError("Mutating workload did not produce any timing result.")
    return best_result
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# DATASET BUILDERS
# ==============================================================================
# Helpers that build deterministic input datasets and pre-populated structures
# reused by every workload runner. Lives here (not in dataset_manager) because
# they encode benchmark-specific shapes (clustered collisions, query bundles).
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _build_collision_records()
def _build_collision_records(
    size: int,
    seed: int,
    *,
    capacity: int = DEFAULT_COLLISION_CAPACITY,
    target_buckets: tuple[int, ...] = DEFAULT_COLLISION_BENCHMARK_BUCKETS,
) -> list[tuple[str, int]]:
    """Build deterministic records whose keys collide in several buckets.

    The benchmark uses a clustered-collision pattern rather than forcing every
    key into one bucket. This keeps collisions visible while producing a more
    informative occupancy chart across a small set of hot buckets.

    Logic:
        1. VALIDATION: filter target_buckets to indices inside [0, capacity).
        2. Distribute *size* keys evenly across the valid buckets (remainder front-loaded).
        3. Generate per-bucket collision keys via dataset_manager.generate_collision_keys.
        4. Interleave keys round-robin so the Streamlit charts show all buckets growing.
        5. Pair each interleaved key with the next value from the normal dataset.
    """
    # VALIDATION: only buckets inside the capacity window are usable
    valid_buckets = tuple(
        bucket for bucket in target_buckets
        if 0 <= bucket < capacity
    )
    if not valid_buckets:
        raise ValueError("target_buckets must contain at least one valid bucket index.")

    # Step 2: even distribution + front-loaded remainder so totals match *size*
    per_bucket_counts = [size // len(valid_buckets)] * len(valid_buckets)
    for idx in range(size % len(valid_buckets)):
        per_bucket_counts[idx] += 1

    # Step 3: one collision-key list per target bucket
    collision_key_groups = [
        generate_collision_keys(
            count=count,
            capacity=capacity,
            target_bucket=bucket,
        )
        for bucket, count in zip(valid_buckets, per_bucket_counts)
    ]

    # Step 4: round-robin interleave so each bucket grows in lockstep
    collision_keys: list[str] = []
    max_group_len = max((len(group) for group in collision_key_groups), default=0)
    for key_index in range(max_group_len):
        for group in collision_key_groups:
            if key_index < len(group):
                collision_keys.append(group[key_index])

    # Step 5: borrow values from the normal generator so every record is a 2-tuple
    base_records = generate_key_value_dataset(size, seed=seed)
    return [
        (collision_key, value)
        for collision_key, (_, value) in zip(collision_keys, base_records)
    ]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_hash_table()
def _build_hash_table(
    records: list[tuple[str, int]],
    *,
    initial_capacity: int = DEFAULT_COLLISION_CAPACITY,
    max_load_factor: float = 0.75,
) -> HashTable:
    """Create and populate a hash table from deterministic records.

    Logic:
        1. Construct a HashTable with the requested capacity and load factor.
        2. MAIN ITERATION LOOP: insert every record in input order.
    """
    hash_table = HashTable(
        initial_capacity=initial_capacity,
        max_load_factor=max_load_factor,
    )
    # MAIN ITERATION LOOP: replay the dataset into the new table
    for key, value in records:
        hash_table.insert(key, value)
    return hash_table
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_collision_benchmark_state()
def build_collision_benchmark_state(
    size: int,
    seed: int = DEFAULT_RANDOM_SEED,
) -> HashTable:
    """Rebuild the forced-collision hash-table state for UI diagrams.

    Logic:
        1. Regenerate the clustered-collision records for *size* and *seed*.
        2. Re-load them into a fresh hash table with the collision capacity
           and a 0.0 load factor (resizing disabled to keep collisions visible).
    """
    collision_records = _build_collision_records(size, seed)
    return _build_hash_table(
        collision_records,
        initial_capacity=DEFAULT_COLLISION_CAPACITY,
        max_load_factor=0.0,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_priority_queue_benchmark_state()
def build_priority_queue_benchmark_state(
    size: int,
    mode: str = "max",
    seed: int = DEFAULT_RANDOM_SEED,
) -> BinaryHeapPriorityQueue:
    """Rebuild a representative priority-queue benchmark state for the UI.

    Logic:
        1. Construct a fresh BinaryHeapPriorityQueue in the requested *mode*.
        2. Insert every priority item generated for *size* / *seed* in order.
    """
    queue = BinaryHeapPriorityQueue(mode=mode)
    for item in generate_priority_items(size, seed=seed):
        queue.insert(item)
    return queue
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_priority_queries()
def _build_priority_queries(
    items: list[PriorityItem],
    query_count: int,
    seed: int,
) -> dict[str, list[str]]:
    """Build deterministic hit/miss label queries for priority-queue search.

    Logic:
        1. Seed a local Random instance for reproducible label sampling.
        2. Build "hits" by sampling existing labels and "misses" using a
           prefix that cannot collide with real "task-NNN" labels.
    """
    rng = random.Random(seed)
    labels = [item.label for item in items]
    return {
        "hits": [rng.choice(labels) for _ in range(query_count)],
        "misses": [f"missing-task-{index + 1:06d}" for index in range(query_count)],
    }
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _select_delete_samples()
def _select_delete_samples(values: list[str], sample_size: int) -> list[str]:
    """Return a deterministic delete sample from the front of *values*.

    Logic:
        1. Slice the first ``min(len(values), sample_size)`` entries.
    """
    return values[: min(len(values), sample_size)]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_priority_queue()
def _build_priority_queue(
    items: list[PriorityItem],
    mode: str,
) -> BinaryHeapPriorityQueue:
    """Build a deterministic priority queue for one mode.

    Logic:
        1. Construct a BinaryHeapPriorityQueue in *mode*.
        2. MAIN ITERATION LOOP: insert every item in input order.
    """
    queue = BinaryHeapPriorityQueue(mode=mode)
    # MAIN ITERATION LOOP: replay the items into the new queue
    for item in items:
        queue.insert(item)
    return queue
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _prepare_bundle()
def _prepare_bundle(
    size: int,
    query_count: int,
    seed: int,
    heap_modes: list[str],
) -> BenchmarkDatasetBundle:
    """Prepare deterministic inputs reused by all workloads for one size.

    Logic:
        1. Generate the normal, collision, and priority datasets for *size*/*seed*.
        2. Build lookup maps (key/label -> value) used by validators.
        3. Pre-populate the normal and collision hash tables and per-mode heaps.
        4. Build hash and priority query bundles via dataset_manager helpers.
        5. Pick deterministic delete samples for both hash and priority workloads.
        6. Pack everything into a frozen BenchmarkDatasetBundle.
    """
    # Step 1: regenerate the canonical datasets for this size
    normal_records = generate_key_value_dataset(size, seed=seed)
    collision_records = _build_collision_records(size, seed)
    priority_items = generate_priority_items(size, seed=seed)

    # Step 2: lookup maps used by validation helpers
    normal_record_map = {key: value for key, value in normal_records}
    collision_record_map = {key: value for key, value in collision_records}
    priority_item_map = {item.label: item for item in priority_items}

    # Step 3: pre-populated structures shared across read-only workloads
    normal_hash_table = _build_hash_table(normal_records)
    collision_hash_table = _build_hash_table(
        collision_records,
        initial_capacity=DEFAULT_COLLISION_CAPACITY,
        max_load_factor=0.0,
    )
    priority_queues = {
        mode: _build_priority_queue(priority_items, mode)
        for mode in heap_modes
    }

    # Step 4: query bundles for hash and priority searches
    hash_queries = {
        mode: generate_search_queries(
            normal_records,
            mode,
            query_count,
            seed=seed,
        )
        for mode in DEFAULT_QUERY_MODES
    }
    collision_hit_queries = generate_search_queries(
        collision_records,
        "hits",
        query_count,
        seed=seed,
    )
    priority_queries = _build_priority_queries(priority_items, query_count, seed)

    # Step 6: pack the deterministic bundle
    return BenchmarkDatasetBundle(
        size=size,
        seed=seed,
        normal_records=normal_records,
        normal_record_map=normal_record_map,
        collision_records=collision_records,
        collision_record_map=collision_record_map,
        priority_items=priority_items,
        priority_item_map=priority_item_map,
        normal_hash_table=normal_hash_table,
        collision_hash_table=collision_hash_table,
        priority_queues=priority_queues,
        hash_queries=hash_queries,
        collision_hit_queries=collision_hit_queries,
        priority_queries=priority_queries,
        # Step 5: deterministic delete samples drawn from the front of each list
        hash_delete_keys=_select_delete_samples(
            [key for key, _ in normal_records],
            DEFAULT_DELETE_SAMPLE_SIZE,
        ),
        collision_delete_keys=_select_delete_samples(
            [key for key, _ in collision_records],
            DEFAULT_DELETE_SAMPLE_SIZE,
        ),
        priority_delete_labels=_select_delete_samples(
            [item.label for item in priority_items],
            DEFAULT_DELETE_SAMPLE_SIZE,
        ),
    )
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# VALIDATION HELPERS
# ==============================================================================
# Recompute the outcome of a workload so the
# runners can mark each BenchmarkRecord as is_correct=True/False. Logic-free
# from the perspective of the workload — they only inspect post-state.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _hash_stats_metadata()
def _hash_stats_metadata(hash_table: HashTable) -> tuple[int, float]:
    """Return ``(collision_count, load_factor)`` for a hash table.

    Logic:
        1. Snapshot the table's stats and unpack the two reporting fields.
    """
    stats = hash_table.get_stats()
    return stats.total_collisions, stats.load_factor
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _priority_sort_key()
def _priority_sort_key(item: PriorityItem, mode: str) -> tuple[int, int]:
    """Return a deterministic ordering key for one priority item.

    Logic:
        1. DISPATCH on *mode*: max-heaps use negative priority for descending order.
        2. Tie-break on sequence_number to mirror the heap's stable ordering.
    """
    # DISPATCH: max-heap orders by descending priority
    if mode == "max":
        return (-item.priority, item.sequence_number)
    return (item.priority, item.sequence_number)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _expected_priority_top()
def _expected_priority_top(items: list[PriorityItem], mode: str) -> PriorityItem:
    """Return the item expected at the root of a deterministic heap.

    Logic:
        1. Sort *items* with the mode-aware sort key and return the first entry.
    """
    return sorted(items, key=lambda item: _priority_sort_key(item, mode))[0]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _expected_search_found_count()
def _expected_search_found_count(
    keys_or_labels: set[str],
    queries: list[str],
) -> int:
    """Count the number of queries expected to succeed.

    Logic:
        1. Sum 1 for every query that is present in *keys_or_labels*.
    """
    return sum(1 for query in queries if query in keys_or_labels)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _remaining_hash_records_ok()
def _remaining_hash_records_ok(
    hash_table: HashTable,
    record_map: dict[str, int],
    deleted_keys: set[str],
) -> bool:
    """Verify that deleted keys are gone and undeleted keys remain intact.

    Logic:
        1. MAIN ITERATION LOOP: walk every (key, expected_value) entry.
        2. DISPATCH: deleted keys must return None; surviving keys must match.
        3. Return False on the first mismatch; True only when the whole table is consistent.
    """
    # MAIN ITERATION LOOP: every record must match its post-delete expectation
    for key, expected_value in record_map.items():
        actual_value = hash_table.search(key)
        # DISPATCH: deleted vs surviving keys are checked differently
        if key in deleted_keys:
            if actual_value is not None:
                return False
        elif actual_value != expected_value:
            return False
    return True
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _remaining_priority_state_ok()
def _remaining_priority_state_ok(
    queue: BinaryHeapPriorityQueue,
    items: list[PriorityItem],
    deleted_labels: set[str],
    mode: str,
) -> bool:
    """Verify that deleted labels are gone and the root stays correct.

    Logic:
        1. SAFETY CHECK: heap invariant must still hold after deletion.
        2. SAFETY CHECK: every deleted label must be unreachable via search().
        3. Recompute the surviving items and confirm the queue size matches.
        4. SAFETY CHECK: empty queues short-circuit; otherwise compare the new root.
    """
    # SAFETY CHECK: heap property must survive every delete sequence
    if not queue.is_valid_heap():
        return False
    # SAFETY CHECK: deleted labels must no longer be findable
    if any(queue.search(label) is not None for label in deleted_labels):
        return False

    remaining_items = [
        item for item in items
        if item.label not in deleted_labels
    ]
    if len(queue) != len(remaining_items):
        return False
    # SAFETY CHECK: empty post-state collapses to is_empty()
    if not remaining_items:
        return queue.is_empty()
    return queue.peek().label == _expected_priority_top(remaining_items, mode).label
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _extraction_order_ok()
def _extraction_order_ok(
    extracted_items: list[PriorityItem],
    source_items: list[PriorityItem],
    mode: str,
) -> bool:
    """Return True when extraction order matches the expected heap order.

    Logic:
        1. Compute the expected label sequence by sorting *source_items*.
        2. Compare label-for-label against *extracted_items*.
    """
    expected_labels = [
        item.label
        for item in sorted(source_items, key=lambda item: _priority_sort_key(item, mode))
    ]
    actual_labels = [item.label for item in extracted_items]
    return actual_labels == expected_labels
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_record()
def _build_record(
    *,
    structure: str,
    operation: str,
    operation_group: str,
    scenario: str,
    size: int,
    workload_count: int,
    elapsed_seconds: float,
    complexity: str,
    is_correct: bool,
    size_before: int,
    size_after: int,
    found_count: int | None = None,
    deleted_count: int | None = None,
    collision_count: int | None = None,
    load_factor: float | None = None,
    heap_valid_after: bool | None = None,
    speedup_vs_linear: float | None = None,
    notes: str,
) -> BenchmarkRecord:
    """Build a populated benchmark record with normalized timing fields.

    Logic:
        1. Convert *elapsed_seconds* into both rounded ms and avg microseconds.
        2. Forward every other field straight onto the BenchmarkRecord dataclass.
    """
    return BenchmarkRecord(
        structure=structure,
        operation=operation,
        operation_group=operation_group,
        scenario=scenario,
        size=size,
        workload_count=workload_count,
        time_ms=_normalize_ms(elapsed_seconds),
        avg_time_us=_normalize_avg_us(elapsed_seconds, workload_count),
        complexity=complexity,
        is_correct=is_correct,
        size_before=size_before,
        size_after=size_after,
        found_count=found_count,
        deleted_count=deleted_count,
        collision_count=collision_count,
        load_factor=load_factor,
        heap_valid_after=heap_valid_after,
        speedup_vs_linear=speedup_vs_linear,
        notes=notes,
    )
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# WORKLOAD RUNNERS
# ==============================================================================
# One runner per workload cell. Each takes a BenchmarkDatasetBundle plus the
# scenario string and returns a fully populated BenchmarkRecord. The runners
# are wired into _WORKLOADS below so the matrix expander can iterate them
# uniformly across sizes and scenarios.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _run_hash_search_comparison()
def _run_hash_search_comparison(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark hash-table search for the assignment comparison block.

    Logic:
        1. Pick the matching query bundle and time the hash-table search.
        2. Capture collision/load metadata for downstream charts.
        3. Validate the actual hit count against the expected count.
    """
    queries = bundle.hash_queries[scenario]
    elapsed_seconds, found_count = benchmark_hash_table_search(
        bundle.normal_hash_table,
        queries,
        repeats,
    )
    collision_count, load_factor = _hash_stats_metadata(bundle.normal_hash_table)
    expected_found = _expected_search_found_count(set(bundle.normal_record_map), queries)
    return _build_record(
        structure="Hash Table",
        operation="search",
        operation_group=_GROUP_SEARCH_COMPARISON,
        scenario=scenario,
        size=bundle.size,
        workload_count=len(queries),
        elapsed_seconds=elapsed_seconds,
        complexity="Avg O(1)",
        is_correct=found_count == expected_found,
        size_before=bundle.size,
        size_after=bundle.size,
        found_count=found_count,
        collision_count=collision_count,
        load_factor=load_factor,
        notes=(
            f"Hash table search processed {len(queries)} {scenario} queries "
            f"at n={bundle.size:,}."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_linear_search_comparison()
def _run_linear_search_comparison(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark linear search for the assignment comparison block.

    Logic:
        1. Pick the matching query bundle and time the linear search baseline.
        2. Validate the actual hit count against the expected count.
    """
    queries = bundle.hash_queries[scenario]
    elapsed_seconds, found_count = benchmark_linear_search(
        bundle.normal_records,
        queries,
        repeats,
    )
    expected_found = _expected_search_found_count(set(bundle.normal_record_map), queries)
    return _build_record(
        structure="Linear Search",
        operation="search",
        operation_group=_GROUP_SEARCH_COMPARISON,
        scenario=scenario,
        size=bundle.size,
        workload_count=len(queries),
        elapsed_seconds=elapsed_seconds,
        complexity="O(n)",
        is_correct=found_count == expected_found,
        size_before=bundle.size,
        size_after=bundle.size,
        found_count=found_count,
        notes=(
            f"Linear search processed {len(queries)} {scenario} queries "
            f"at n={bundle.size:,}."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_hash_insert_bulk()
def _run_hash_insert_bulk(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark bulk insertion into a fresh normal hash table.

    Logic:
        1. Define a per-repeat closure that builds a fresh table and times inserts.
        2. Run the closure via _best_mutating_run to pick the fastest valid trial.
        3. Materialize the BenchmarkRecord with collision/load metadata from the win.
    """

    def _repeat() -> dict[str, object]:
        hash_table = HashTable()
        start_time = time.perf_counter()
        for key, value in bundle.normal_records:
            hash_table.insert(key, value)
        elapsed_seconds = time.perf_counter() - start_time
        collision_count, load_factor = _hash_stats_metadata(hash_table)
        return {
            "elapsed_seconds": elapsed_seconds,
            "size_after": len(hash_table),
            "collision_count": collision_count,
            "load_factor": load_factor,
            "is_correct": (
                len(hash_table) == bundle.size
                and all(hash_table.search(key) == value for key, value in bundle.normal_records)
            ),
        }

    best = _best_mutating_run(_repeat, repeats)
    return _build_record(
        structure="Hash Table",
        operation="insert_bulk",
        operation_group=_GROUP_HASH_CORE,
        scenario=scenario,
        size=bundle.size,
        workload_count=bundle.size,
        elapsed_seconds=float(best["elapsed_seconds"]),
        complexity="Avg O(1)",
        is_correct=bool(best["is_correct"]),
        size_before=0,
        size_after=int(best["size_after"]),
        collision_count=int(best["collision_count"]),
        load_factor=float(best["load_factor"]),
        notes=f"Inserted {bundle.size:,} normal records into a fresh hash table.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_hash_search_normal()
def _run_hash_search_normal(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark normal hash-table hit/miss search workloads.

    Logic:
        1. DISPATCH on scenario suffix to pick the hits or misses query bundle.
        2. Time the hash-table search and capture collision/load metadata.
        3. Validate the actual hit count against the expected count.
    """
    # DISPATCH: scenario string selects the query bundle
    mode = "hits" if scenario == "normal_hits" else "misses"
    queries = bundle.hash_queries[mode]
    elapsed_seconds, found_count = estimate_search_time(
        bundle.normal_hash_table.search,
        queries,
        repeats,
    )
    collision_count, load_factor = _hash_stats_metadata(bundle.normal_hash_table)
    expected_found = _expected_search_found_count(set(bundle.normal_record_map), queries)
    operation = "search_hits" if mode == "hits" else "search_misses"
    return _build_record(
        structure="Hash Table",
        operation=operation,
        operation_group=_GROUP_HASH_CORE,
        scenario="normal",
        size=bundle.size,
        workload_count=len(queries),
        elapsed_seconds=elapsed_seconds,
        complexity="Avg O(1)",
        is_correct=found_count == expected_found,
        size_before=bundle.size,
        size_after=bundle.size,
        found_count=found_count,
        collision_count=collision_count,
        load_factor=load_factor,
        notes=f"Hash-table {mode} search workload on normal data at n={bundle.size:,}.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_hash_delete_sample()
def _run_hash_delete_sample(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark deterministic deletes on normal hash-table data.

    Logic:
        1. Capture the deleted-key set up front for validation.
        2. Define a per-repeat closure that rebuilds the table and times deletes.
        3. Run via _best_mutating_run; verify size + remaining-record consistency.
    """
    deleted_keys = set(bundle.hash_delete_keys)
    # --- Delete sample from normal data ---
    def _repeat() -> dict[str, object]:
        hash_table = _build_hash_table(bundle.normal_records)
        start_time = time.perf_counter()
        deleted_count = sum(
            1 for key in bundle.hash_delete_keys
            if hash_table.delete(key) is not None
        )
        # --- Calculate elapsed time and collision/load metadata ---
        elapsed_seconds = time.perf_counter() - start_time
        collision_count, load_factor = _hash_stats_metadata(hash_table)
        # --- Return the results ---
        return {
            "elapsed_seconds": elapsed_seconds,
            "deleted_count": deleted_count,
            "size_after": len(hash_table),
            "collision_count": collision_count,
            "load_factor": load_factor,
            "is_correct": (
                deleted_count == len(bundle.hash_delete_keys)
                and len(hash_table) == bundle.size - len(bundle.hash_delete_keys)
                and _remaining_hash_records_ok(
                    hash_table,
                    bundle.normal_record_map,
                    deleted_keys,
                )
            ),
        }
    # --- Run the benchmark ---
    best = _best_mutating_run(_repeat, repeats)
    return _build_record(
        structure="Hash Table",
        operation="delete_sample",
        operation_group=_GROUP_HASH_CORE,
        scenario=scenario,
        size=bundle.size,
        workload_count=len(bundle.hash_delete_keys),
        elapsed_seconds=float(best["elapsed_seconds"]),
        complexity="Avg O(1)",
        is_correct=bool(best["is_correct"]),
        size_before=bundle.size,
        size_after=int(best["size_after"]),
        deleted_count=int(best["deleted_count"]),
        collision_count=int(best["collision_count"]),
        load_factor=float(best["load_factor"]),
        notes=(
            f"Deleted {len(bundle.hash_delete_keys):,} deterministic keys "
            f"from a normal hash table at n={bundle.size:,}."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_hash_collision_insert_bulk()
def _run_hash_collision_insert_bulk(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark bulk insertion into a forced-collision hash table.

    Logic:
        1. Define a closure that builds a 0.0-load-factor table (no resize)
           and times collision-key inserts so chaining stays visible.
        2. Run via _best_mutating_run; require collision_count > 0 to mark valid.
    """
    # --- Define the repeat function ---
    def _repeat() -> dict[str, object]:
        hash_table = HashTable(
            initial_capacity=DEFAULT_COLLISION_CAPACITY,
            max_load_factor=0.0,
        )
        start_time = time.perf_counter()
        for key, value in bundle.collision_records:
            hash_table.insert(key, value)
        elapsed_seconds = time.perf_counter() - start_time
        collision_count, load_factor = _hash_stats_metadata(hash_table)
        # --- Return the results ---
        return {
            "elapsed_seconds": elapsed_seconds,
            "size_after": len(hash_table),
            "collision_count": collision_count,
            "load_factor": load_factor,
            "is_correct": (
                len(hash_table) == bundle.size
                and collision_count > 0
                and all(hash_table.search(key) == value for key, value in bundle.collision_records)
            ),
        }
    # --- Run the benchmark ---
    best = _best_mutating_run(_repeat, repeats) 
    return _build_record(
        structure="Hash Table",
        operation="collision_insert_bulk",
        operation_group=_GROUP_HASH_COLLISION,
        scenario=scenario,
        size=bundle.size,
        workload_count=bundle.size,
        elapsed_seconds=float(best["elapsed_seconds"]),
        complexity="Avg O(1)",
        is_correct=bool(best["is_correct"]),
        size_before=0,
        size_after=int(best["size_after"]),
        collision_count=int(best["collision_count"]),
        load_factor=float(best["load_factor"]),
        notes=(
            f"Inserted {bundle.size:,} colliding records into a fixed-capacity "
            "hash table."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_hash_collision_search_hits()
def _run_hash_collision_search_hits(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark forced-collision hit searches.

    Logic:
        1. Reuse the pre-populated collision table and its hit-only query bundle.
        2. Validate the actual hit count and require collision_count > 0.
    """
    elapsed_seconds, found_count = estimate_search_time(
        bundle.collision_hash_table.search,
        bundle.collision_hit_queries,
        repeats,
    )   
    # --- Calculate collision/load metadata ---
    collision_count, load_factor = _hash_stats_metadata(bundle.collision_hash_table)
    expected_found = _expected_search_found_count(
        set(bundle.collision_record_map),
        bundle.collision_hit_queries,
    )
    # --- Return the results ---
    return _build_record(
        structure="Hash Table",
        operation="collision_search_hits",
        operation_group=_GROUP_HASH_COLLISION,
        scenario=scenario,
        size=bundle.size,
        workload_count=len(bundle.collision_hit_queries),
        elapsed_seconds=elapsed_seconds,
        complexity="Avg O(1)",
        is_correct=(found_count == expected_found) and collision_count > 0,
        size_before=bundle.size,
        size_after=bundle.size,
        found_count=found_count,
        collision_count=collision_count,
        load_factor=load_factor,
        notes=(
            f"Hash-table hit searches against the forced-collision dataset "
            f"at n={bundle.size:,}."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_hash_collision_delete_sample()
def _run_hash_collision_delete_sample(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark deterministic deletes from a forced-collision hash table.

    Logic:
        1. Capture the deleted-key set up front for validation.
        2. Define a closure that rebuilds the collision table and times deletes.
        3. Validate that every targeted delete succeeded and the remainder is intact.
    """
    deleted_keys = set(bundle.collision_delete_keys)
    # --- Define the repeat function ---
    def _repeat() -> dict[str, object]:
        hash_table = _build_hash_table(
            bundle.collision_records,
            initial_capacity=DEFAULT_COLLISION_CAPACITY,
            max_load_factor=0.0,
        )
        # --- Calculate elapsed time and collision/load metadata ---
        start_time = time.perf_counter()
        deleted_count = sum(
            1 for key in bundle.collision_delete_keys
            if hash_table.delete(key) is not None
        )
        # --- Calculate elapsed time and collision/load metadata ---
        elapsed_seconds = time.perf_counter() - start_time
        collision_count, load_factor = _hash_stats_metadata(hash_table)
        return {
            "elapsed_seconds": elapsed_seconds,
            "deleted_count": deleted_count,
            "size_after": len(hash_table),
            "collision_count": collision_count,
            "load_factor": load_factor,
            "is_correct": (
                deleted_count == len(bundle.collision_delete_keys)
                and collision_count > 0
                and _remaining_hash_records_ok(
                    hash_table,
                    bundle.collision_record_map,
                    deleted_keys,
                )
            ),
        }
    # --- Run the benchmark ---
    best = _best_mutating_run(_repeat, repeats)
    return _build_record(
        structure="Hash Table",
        operation="collision_delete_sample",
        operation_group=_GROUP_HASH_COLLISION,
        scenario=scenario,
        size=bundle.size,
        workload_count=len(bundle.collision_delete_keys),
        elapsed_seconds=float(best["elapsed_seconds"]),
        complexity="Avg O(1)",
        is_correct=bool(best["is_correct"]),
        size_before=bundle.size,
        size_after=int(best["size_after"]),
        deleted_count=int(best["deleted_count"]),
        collision_count=int(best["collision_count"]),
        load_factor=float(best["load_factor"]),
        notes=(
            f"Deleted {len(bundle.collision_delete_keys):,} keys from the "
            "forced-collision dataset."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_priority_insert_bulk()
def _run_priority_insert_bulk(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark bulk insertion into a fresh priority queue.

    Logic:
        1. Define a closure that builds a fresh queue in *scenario* mode
           and times insertion of every priority item.
        2. Validate post-state: heap invariant + correct root for the mode.
    """
    # --- Define the repeat function ---
    def _repeat() -> dict[str, object]:
        queue = BinaryHeapPriorityQueue(mode=scenario)
        start_time = time.perf_counter()
        # --- Calculate elapsed time and collision/load metadata ---
        for item in bundle.priority_items:
            queue.insert(item)
        elapsed_seconds = time.perf_counter() - start_time
        expected_top = _expected_priority_top(bundle.priority_items, scenario)
        actual_top = queue.peek() if not queue.is_empty() else None
        heap_valid = queue.is_valid_heap()
        # --- Return the results ---
        return {
            "elapsed_seconds": elapsed_seconds,
            "size_after": len(queue),
            "heap_valid_after": heap_valid,
            "is_correct": (
                len(queue) == bundle.size
                and heap_valid
                and actual_top is not None
                and actual_top.label == expected_top.label
            ),
        }
    # --- Run the benchmark ---
    best = _best_mutating_run(_repeat, repeats)
    return _build_record(
        structure="Priority Queue",
        operation="insert_bulk",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario=scenario,
        size=bundle.size,
        workload_count=bundle.size,
        elapsed_seconds=float(best["elapsed_seconds"]),
        complexity="O(log n)",
        is_correct=bool(best["is_correct"]),
        size_before=0,
        size_after=int(best["size_after"]),
        heap_valid_after=bool(best["heap_valid_after"]),
        notes=(
            f"Inserted {bundle.size:,} items into a fresh {scenario}-heap "
            "priority queue."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_priority_peek()
def _run_priority_peek(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark read-only priority-queue peek.

    Logic:
        1. Reuse the pre-populated queue for *scenario*.
        2. Time queue.peek via _autorange_normalized_time.
        3. Validate the peeked label matches the expected root.
    """
    queue = bundle.priority_queues[scenario]
    expected_top = _expected_priority_top(bundle.priority_items, scenario)
    elapsed_seconds = _autorange_normalized_time(queue.peek, repeats)
    actual_top = queue.peek()
    heap_valid = queue.is_valid_heap()
    # --- Return the results ---
    return _build_record(
        structure="Priority Queue",
        operation="peek",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario=scenario,
        size=bundle.size,
        workload_count=1,
        elapsed_seconds=elapsed_seconds,
        complexity="O(1)",
        is_correct=heap_valid and actual_top.label == expected_top.label,
        size_before=bundle.size,
        size_after=bundle.size,
        heap_valid_after=heap_valid,
        notes=f"Peek inspected the root of the {scenario}-heap priority queue.",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_priority_extract_drain()
def _run_priority_extract_drain(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark repeated root extraction until the priority queue is empty.

    Logic:
        1. Define a closure that builds a fresh queue and drains every root.
        2. Validate: total extracted == size, queue empty, order matches sort.
    """
    # --- Define the repeat function ---
    def _repeat() -> dict[str, object]:
        queue = _build_priority_queue(bundle.priority_items, scenario)
        extracted_items: list[PriorityItem] = []
        start_time = time.perf_counter()
        # MAIN ITERATION LOOP: pop the root until the queue is empty
        while not queue.is_empty():
            extracted_items.append(queue.extract_top())
        elapsed_seconds = time.perf_counter() - start_time
        heap_valid = queue.is_valid_heap()
        # --- Return the results ---
        return {
            "elapsed_seconds": elapsed_seconds,
            "size_after": len(queue),
            "heap_valid_after": heap_valid,
            "is_correct": (
                len(extracted_items) == bundle.size
                and len(queue) == 0
                and heap_valid
                and _extraction_order_ok(extracted_items, bundle.priority_items, scenario)
            ),
        }
    # --- Run the benchmark ---
    best = _best_mutating_run(_repeat, repeats)
    return _build_record(
        structure="Priority Queue",
        operation="extract_top_drain",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario=scenario,
        size=bundle.size,
        workload_count=bundle.size,
        elapsed_seconds=float(best["elapsed_seconds"]),
        complexity="O(log n)",
        is_correct=bool(best["is_correct"]),
        size_before=bundle.size,
        size_after=int(best["size_after"]),
        heap_valid_after=bool(best["heap_valid_after"]),
        notes=(
            f"Extracted every item from a fresh {scenario}-heap priority queue."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_priority_search()
def _run_priority_search(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark read-only priority-queue label search.

    Logic:
        1. Split *scenario* on ":" into (mode, search_kind) - e.g., "max:hits".
        2. Time queue.search across the matching query bundle.
        3. Validate the actual hit count against the expected count.
    """
    # Step 1: scenario carries both heap mode and query kind ("max:hits")
    mode, search_kind = scenario.split(":", maxsplit=1)
    queue = bundle.priority_queues[mode]
    queries = bundle.priority_queries[search_kind]
    elapsed_seconds, found_count = estimate_search_time(queue.search, queries, repeats)
    expected_found = _expected_search_found_count(set(bundle.priority_item_map), queries)
    heap_valid = queue.is_valid_heap()
    operation = "search_hits" if search_kind == "hits" else "search_misses"
    # --- Return the results ---
    return _build_record(
        structure="Priority Queue",
        operation=operation,
        operation_group=_GROUP_PRIORITY_CORE,
        scenario=mode,
        size=bundle.size,
        workload_count=len(queries),
        elapsed_seconds=elapsed_seconds,
        complexity="O(n)",
        is_correct=heap_valid and found_count == expected_found,
        size_before=bundle.size,
        size_after=bundle.size,
        found_count=found_count,
        heap_valid_after=heap_valid,
        notes=(
            f"Priority-queue {search_kind} search workload for the "
            f"{mode}-heap scenario."
        ),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _run_priority_delete_sample()
def _run_priority_delete_sample(
    bundle: BenchmarkDatasetBundle,
    scenario: str,
    repeats: int,
) -> BenchmarkRecord:
    """Benchmark deterministic label deletes on a fresh priority queue.

    Logic:
        1. Capture the deleted-label set up front for validation.
        2. Define a closure that rebuilds the queue and times labeled deletes.
        3. Validate via _remaining_priority_state_ok (heap valid + root correct).
    """
    deleted_labels = set(bundle.priority_delete_labels)

    def _repeat() -> dict[str, object]:
        queue = _build_priority_queue(bundle.priority_items, scenario)
        start_time = time.perf_counter()
        deleted_count = sum(
            1 for label in bundle.priority_delete_labels
            if queue.delete(label) is not None
        )
        elapsed_seconds = time.perf_counter() - start_time
        heap_valid = queue.is_valid_heap()
        return {
            "elapsed_seconds": elapsed_seconds,
            "deleted_count": deleted_count,
            "size_after": len(queue),
            "heap_valid_after": heap_valid,
            "is_correct": (
                deleted_count == len(bundle.priority_delete_labels)
                and _remaining_priority_state_ok(
                    queue,
                    bundle.priority_items,
                    deleted_labels,
                    scenario,
                )
            ),
        }

    best = _best_mutating_run(_repeat, repeats)
    return _build_record(
        structure="Priority Queue",
        operation="delete_sample",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario=scenario,
        size=bundle.size,
        workload_count=len(bundle.priority_delete_labels),
        elapsed_seconds=float(best["elapsed_seconds"]),
        complexity="O(n)",
        is_correct=bool(best["is_correct"]),
        size_before=bundle.size,
        size_after=int(best["size_after"]),
        deleted_count=int(best["deleted_count"]),
        heap_valid_after=bool(best["heap_valid_after"]),
        notes=(
            f"Deleted {len(bundle.priority_delete_labels):,} labels from a "
            f"fresh {scenario}-heap priority queue."
        ),
    )
# --------------------------------------------------------------------------------

# ==============================================================================
#
# Declarative benchmark matrix - runners above are wired into one cell each.
_WORKLOADS: list[WorkloadSpec] = [
    # --- Hash Table Benchmarks ---
    WorkloadSpec(
        structure="Hash Table",
        operation="search",
        operation_group=_GROUP_SEARCH_COMPARISON,
        scenario_kind="query_mode",
        fixed_scenario=None,
        runner=_run_hash_search_comparison,
    ),
    # --- Linear Search Benchmarks ---
    WorkloadSpec(
        structure="Linear Search",
        operation="search",
        operation_group=_GROUP_SEARCH_COMPARISON,
        scenario_kind="query_mode",
        fixed_scenario=None,
        runner=_run_linear_search_comparison,
    ),
    # --- Hash Table Core Benchmarks ---
    WorkloadSpec(
        structure="Hash Table",
        operation="insert_bulk",
        operation_group=_GROUP_HASH_CORE,
        scenario_kind="fixed",
        fixed_scenario="normal",
        runner=_run_hash_insert_bulk,
    ),
    # --- Hash Table Search Benchmarks ---
    WorkloadSpec(
        structure="Hash Table",
        operation="search_hits",
        operation_group=_GROUP_HASH_CORE,
        scenario_kind="fixed",
        fixed_scenario="normal_hits",
        runner=_run_hash_search_normal,
    ),
    # --- Hash Table Search Misses Benchmarks ---
    WorkloadSpec(
        structure="Hash Table",
        operation="search_misses",
        operation_group=_GROUP_HASH_CORE,
        scenario_kind="fixed",
        fixed_scenario="normal_misses",
        runner=_run_hash_search_normal,
    ),
    # --- Hash Table Delete Sample Benchmarks ---
    WorkloadSpec(
        structure="Hash Table",
        operation="delete_sample",
        operation_group=_GROUP_HASH_CORE,
        scenario_kind="fixed",
        fixed_scenario="normal",
        runner=_run_hash_delete_sample,
    ),
    WorkloadSpec(
        structure="Hash Table",
        operation="collision_insert_bulk",
        operation_group=_GROUP_HASH_COLLISION,
        scenario_kind="fixed",
        fixed_scenario="forced_collision",
        runner=_run_hash_collision_insert_bulk,
    ),
    # --- Hash Table Collision Search Hits Benchmarks ---
    WorkloadSpec(
        structure="Hash Table",
        operation="collision_search_hits",
        operation_group=_GROUP_HASH_COLLISION,
        scenario_kind="fixed",
        fixed_scenario="forced_collision",
        runner=_run_hash_collision_search_hits,
    ),
    # --- Hash Table Collision Delete Sample Benchmarks ---
    WorkloadSpec(
        structure="Hash Table",
        operation="collision_delete_sample",
        operation_group=_GROUP_HASH_COLLISION,
        scenario_kind="fixed",
        fixed_scenario="forced_collision",
        runner=_run_hash_collision_delete_sample,
    ),
    # --- Priority Queue Insert Bulk Benchmarks ---
    WorkloadSpec(
        structure="Priority Queue",
        operation="insert_bulk",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario_kind="heap_mode",
        fixed_scenario=None,
        runner=_run_priority_insert_bulk,
    ),
    # --- Priority Queue Peek Benchmarks ---
    WorkloadSpec(
        structure="Priority Queue",
        operation="peek",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario_kind="heap_mode",
        fixed_scenario=None,
        runner=_run_priority_peek,
    ),
    # --- Priority Queue Extract Drain Benchmarks ---
    WorkloadSpec(
        structure="Priority Queue",
        operation="extract_top_drain",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario_kind="heap_mode",
        fixed_scenario=None,
        runner=_run_priority_extract_drain,
    ),
    # --- Priority Queue Search Hits Benchmarks ---
    WorkloadSpec(
        structure="Priority Queue",
        operation="search_hits",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario_kind="heap_mode_search_hits",
        fixed_scenario=None,
        runner=_run_priority_search,
    ),
    WorkloadSpec(
        structure="Priority Queue",
        operation="search_misses",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario_kind="heap_mode_search_misses",
        fixed_scenario=None,
        runner=_run_priority_search,
    ),
    # --- Priority Queue Delete Sample Benchmarks ---
    WorkloadSpec(
        structure="Priority Queue",
        operation="delete_sample",
        operation_group=_GROUP_PRIORITY_CORE,
        scenario_kind="heap_mode",
        fixed_scenario=None,
        runner=_run_priority_delete_sample,
    ),
]

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# BENCHMARK MATRIX
# ==============================================================================
# Top-level driver that expands the WorkloadSpec table into concrete cells,
# runs each cell, annotates the rows with hash-vs-linear speedup ratios, and
# returns a sorted DataFrame consumed by the Streamlit Benchmark Lab tab.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _scenario_values()
def _scenario_values(
    workload: WorkloadSpec,
    query_modes: list[str],
    heap_modes: list[str],
) -> list[str]:
    """Return the scenario values that should be run for one workload.

    Logic:
        1. DISPATCH on workload.scenario_kind to pick the right expansion.
        2. "query_mode" / "heap_mode" return the input mode lists directly.
        3. "heap_mode_search_*" formats build "{mode}:hits" / "{mode}:misses".
        4. "fixed" workloads return their pre-declared single-scenario list.
        5. VALIDATION: missing fixed_scenario for "fixed" raises ValueError.
    """
    # DISPATCH: each scenario_kind has its own expansion strategy
    if workload.scenario_kind == "query_mode":
        return list(query_modes)
    if workload.scenario_kind == "heap_mode":
        return list(heap_modes)
    if workload.scenario_kind == "heap_mode_search_hits":
        return [f"{mode}:hits" for mode in heap_modes]
    if workload.scenario_kind == "heap_mode_search_misses":
        return [f"{mode}:misses" for mode in heap_modes]
    # VALIDATION: fixed-scenario workloads must declare their scenario
    if workload.fixed_scenario is None:
        raise ValueError(f"Workload {workload.operation!r} is missing a fixed scenario.")
    return [workload.fixed_scenario]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _annotate_speedup_vs_linear()
def _annotate_speedup_vs_linear(df: pd.DataFrame) -> pd.DataFrame:
    """Fill raw benchmark rows with the search-comparison speedup ratios.

    Logic:
        1. Copy *df* and zero out the speedup_vs_linear column.
        2. Compute the per-(size, query_mode) speedup table via compute_speedup_summary.
        3. Build a lookup dict keyed by (size, query_mode) -> speedup float.
        4. Apply the dict to hash-table rows; pin linear rows to 1.0.
    """
    annotated = df.copy()
    annotated["speedup_vs_linear"] = None

    speedup_df = compute_speedup_summary(annotated)
    speedup_map = {
        (int(row["dataset_size"]), str(row["query_mode"])): float(row["speedup"])
        for _, row in speedup_df.iterrows()
    }

    # Step 4a: hash-table search rows pull their speedup from the map
    hash_mask = (
        (annotated["operation_group"] == _GROUP_SEARCH_COMPARISON)
        & (annotated["structure"] == "Hash Table")
    )
    # hash-table search rows pull their speedup from the map
    annotated.loc[hash_mask, "speedup_vs_linear"] = annotated.loc[hash_mask].apply(
        lambda row: speedup_map.get((int(row["size"]), str(row["scenario"]))),
        axis=1,
    )
    # linear rows are the baseline (1.0x by definition)
    linear_mask = (
        (annotated["operation_group"] == _GROUP_SEARCH_COMPARISON)
        & (annotated["structure"] == "Linear Search")
    )
    # linear rows are the baseline (1.0x by definition)
    annotated.loc[linear_mask, "speedup_vs_linear"] = 1.0
    return annotated
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_benchmarks()
def run_benchmarks(
    sizes: list[int] | None = None,
    query_modes: list[str] | None = None,
    query_count: int = DEFAULT_QUERY_COUNT,
    repeats: int = DEFAULT_REPEATS,
    seed: int = DEFAULT_RANDOM_SEED,
    progress_callback: Callable[[int, int, str], None] | None = None,
    heap_modes: list[str] | None = None,
) -> pd.DataFrame:
    """Run the full CTA-5 benchmark matrix.

    Logic:
        1. Resolve overrides for sizes, query modes, and heap modes (defaults otherwise).
        2. Pre-compute the *total* number of cells for progress reporting.
        3. MAIN ITERATION LOOP: for each size, build the bundle once and run
           every (workload, scenario) cell against it.
        4. Convert the collected dataclass rows into a DataFrame.
        5. Annotate hash-vs-linear speedup ratios and sort the rows for stability.
    """
    # Step 1: resolve overrides for the matrix dimensions
    selected_sizes = list(sizes) if sizes is not None else list(DEFAULT_SIZES)
    selected_query_modes = list(query_modes) if query_modes is not None else list(DEFAULT_QUERY_MODES)
    selected_heap_modes = list(heap_modes) if heap_modes is not None else list(DEFAULT_HEAP_MODES)

    # compute the total cell count so progress callbacks can report progress
    total = 0
    for workload in _WORKLOADS:
        total += len(_scenario_values(workload, selected_query_modes, selected_heap_modes))
    total *= len(selected_sizes)

    current = 0
    rows: list[dict[str, object]] = []

    # MAIN ITERATION LOOP - one prepared bundle per size, every workload runs against it
    for size in selected_sizes:
        bundle = _prepare_bundle(size, query_count, seed, selected_heap_modes)
        for workload in _WORKLOADS:
            for scenario in _scenario_values(workload, selected_query_modes, selected_heap_modes):
                current += 1
                if progress_callback is not None:
                    progress_callback(
                        current,
                        total,
                        f"{workload.structure}.{workload.operation} [{scenario}] (n={size:,})",
                    )
                rows.append(asdict(workload.runner(bundle, scenario, repeats)))

    # materialize the rows as a DataFrame
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # annotate speedup ratios + stable sort for deterministic output
    df = _annotate_speedup_vs_linear(df)
    return df.sort_values(
        by=["size", "operation_group", "scenario", "structure", "operation"],
        kind="stable",
    ).reset_index(drop=True)
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# CSV PERSISTENCE
# ==============================================================================
# Tiny round-trip helpers so the Streamlit UI can persist benchmark results
# (or summary tables) to disk and re-load them later.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- save_results_csv()
def save_results_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Save benchmark or summary results to CSV.

    Logic:
        1. Coerce *path* to a Path and ensure the parent directory exists.
        2. Write the DataFrame to disk without the pandas integer index.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target, index=False)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- load_results_csv()
def load_results_csv(path: str | Path) -> pd.DataFrame:
    """Load previously saved benchmark results.

    Logic:
        1. Delegate to ``pandas.read_csv`` on *path*.
    """
    return pd.read_csv(path)
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# SUMMARY BUILDERS
# ==============================================================================
# Aggregations applied on top of the raw benchmark DataFrame. These power the
# headline tables in the Streamlit Benchmark Lab tab and the report exports.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- compute_speedup_summary()
def compute_speedup_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute hash-table search speedup over linear search.

    Logic:
        1. Filter *df* down to the search-comparison rows; return empty schema if none.
        2. Group by (size, scenario) and pair the matching hash + linear rows.
        3. Compute speedup = linear_time / hash_time (infinite when hash_time is 0).
        4. Build a tidy DataFrame, sort by (size, query_mode), and reset the index.
    """
    search_df = df[df["operation_group"] == _GROUP_SEARCH_COMPARISON].copy()
    # SAFETY CHECK: empty input still returns the expected column schema
    if search_df.empty:
        return pd.DataFrame(
            columns=[
                "dataset_size",
                "query_mode",
                "hash_time_ms",
                "linear_time_ms",
                "speedup",
                "notes",
            ]
        )

    summary_rows: list[dict[str, object]] = []
    # MAIN ITERATION LOOP: one (size, query_mode) cell at a time
    for (size, query_mode), group in search_df.groupby(["size", "scenario"]):
        hash_row = group[group["structure"] == "Hash Table"]
        linear_row = group[group["structure"] == "Linear Search"]
        # SAFETY CHECK: skip cells that are missing one of the two methods
        if hash_row.empty or linear_row.empty:
            continue
        hash_time_ms = float(hash_row["time_ms"].iloc[0])
        linear_time_ms = float(linear_row["time_ms"].iloc[0])
        speedup = round(linear_time_ms / hash_time_ms, 4) if hash_time_ms > 0 else float("inf")
        summary_rows.append(
            {
                "dataset_size": int(size),
                "query_mode": str(query_mode),
                "hash_time_ms": hash_time_ms,
                "linear_time_ms": linear_time_ms,
                "speedup": speedup,
                "notes": (
                    f"Hash table search is {speedup:.2f}x faster than linear search "
                    f"for {query_mode} queries at n={int(size):,}."
                ),
            }
        )
    # return a tidy DataFrame sorted by (size, query_mode)
    return pd.DataFrame(summary_rows).sort_values(
        by=["dataset_size", "query_mode"],
        kind="stable",
    ).reset_index(drop=True)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- compute_operation_scaling_summary()
def compute_operation_scaling_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize scaling from the smallest to largest tested size.

    Logic:
        1. SAFETY CHECK: empty input still returns the expected column schema.
        2. Group by (operation_group, structure, operation, scenario) series.
        3. Sort each series by size, then take the smallest and largest rows.
        4. Compute growth_factor = largest_time / smallest_time (inf when 0).
        5. Build a tidy DataFrame, sort it stably, and reset the index.
    """
    # SAFETY CHECK: empty input still returns the expected column schema
    if df.empty:
        return pd.DataFrame(
            columns=[
                "operation_group",
                "structure",
                "operation",
                "scenario",
                "smallest_size",
                "largest_size",
                "smallest_time_ms",
                "largest_time_ms",
                "growth_factor",
                "notes",
            ]
        )
    # build a list of summary rows
    rows: list[dict[str, object]] = []
    grouped = df.groupby(["operation_group", "structure", "operation", "scenario"])
    # MAIN ITERATION LOOP: one benchmark series at a time
    for (operation_group, structure, operation, scenario), group in grouped:
        ordered = group.sort_values("size", kind="stable")
        smallest = ordered.iloc[0]
        largest = ordered.iloc[-1]
        smallest_time = float(smallest["time_ms"])
        largest_time = float(largest["time_ms"])
        growth_factor = round(largest_time / smallest_time, 4) if smallest_time > 0 else float("inf")
        rows.append(
            {
                "operation_group": operation_group,
                "structure": structure,
                "operation": operation,
                "scenario": scenario,
                "smallest_size": int(smallest["size"]),
                "largest_size": int(largest["size"]),
                "smallest_time_ms": smallest_time,
                "largest_time_ms": largest_time,
                "growth_factor": growth_factor,
                "notes": (
                    f"{structure}.{operation} ({scenario}) grew {growth_factor:.2f}x "
                    f"from n={int(smallest['size']):,} to n={int(largest['size']):,}."
                ),
            }
        )
    # return a tidy DataFrame sorted by (operation_group, scenario, structure, operation)
    return pd.DataFrame(rows).sort_values(
        by=["operation_group", "scenario", "structure", "operation"],
        kind="stable",
    ).reset_index(drop=True)
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
