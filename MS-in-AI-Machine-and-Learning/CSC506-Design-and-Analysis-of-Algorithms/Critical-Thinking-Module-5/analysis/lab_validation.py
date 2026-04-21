# File: lab_validation.py 
#
# Author: Alexander Ricciardi 
# Date: 2026-04-19
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026

# -------------------------------------------------------------------------
# Module Functionality
# Validation helpers for the CTA-5 Streamlit labs.
# These helpers keep validation logic out of the UI so the app can offer
# one-click demos for the hash table, priority queue, and benchmark labs.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Validation helpers for the CTA-5 Streamlit labs.

These helpers provide deterministic, structured demo flows for:

- the hash table lab
- the priority queue lab
- the benchmark lab

Each function returns step-by-step validation results that the Streamlit
interface can render as screenshot-friendly tables.
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Callable

import pandas as pd

from algorithms.hash_table import HashTable
from algorithms.priority_queue import BinaryHeapPriorityQueue
from analysis.benchmark_search import (
    DEFAULT_HEAP_MODES,
    DEFAULT_QUERY_COUNT,
    DEFAULT_QUERY_MODES,
    DEFAULT_RANDOM_SEED,
    DEFAULT_REPEATS,
    DEFAULT_SIZES,
    compute_operation_scaling_summary,
    compute_speedup_summary,
    run_benchmarks,
)
from data.dataset_manager import (
    generate_collision_keys,
    generate_key_value_dataset,
    generate_priority_items,
)
from models.hash_table_stats import HashTableStats
from models.lab_operation_result import LabOperationResult
from models.priority_item import PriorityItem


# ______________________________________________________________________________
# Class Definitions – Data Classes
# ==============================================================================
# TYPES AND DATA STRUCTURES
# ==============================================================================
# Dataclasses used by the lab helpers to bundle step-by-step
# validation rows, demo operation traces, and benchmark summaries for the
# Streamlit UI.
#
# - Class: ValidationStepResult       (Dataclass) - One PASS/CHECK validation row
# - Class: HashTableDemoResult        (Dataclass) - Hash-table lab demo result
# - Class: PriorityQueueDemoResult    (Dataclass) - Priority-queue lab demo result
# - Class: BenchmarkValidationResult  (Dataclass) - Benchmark lab validation result
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------- class ValidationStepResult
@dataclass
class ValidationStepResult:
    """One pass/fail validation row for a guided demo.

    Attributes:
        step_name: Short label for the validation step.
        expected: The expected outcome.
        actual: The observed outcome.
        passed: Whether the step succeeded.
        notes: Optional supporting note.

    Logic:
        This dataclass packages one row of a guided-demo validation table.
        1. Carry the step identity (name) and the expected/actual values.
        2. Carry a boolean pass flag plus an optional notes string.
        3. Provide as_dict() to convert to a UI-friendly dictionary.
    """

    step_name: str
    expected: str
    actual: str
    passed: bool
    notes: str = ""

    # --------------------------------------------------------------- as_dict()
    def as_dict(self) -> dict[str, object]:
        """Return the step as a dictionary for DataFrame rendering.

        Logic:
            This helper renders the row as a UI-friendly dictionary.
            1. Map step fields to display column names.
            2. Convert the boolean pass flag to "PASS" or "CHECK" text.
            3. Return the resulting dictionary for DataFrame ingestion.
        """
        return {
            "Step": self.step_name,
            "Expected": self.expected,
            "Actual": self.actual,
            "Passed": "PASS" if self.passed else "CHECK",
            "Notes": self.notes,
        }
    # ---------------------------------------------------------------

# ------------------------------------------------------------------------- end class ValidationStepResult


# ------------------------------------------------------------------------- class HashTableDemoResult
@dataclass
class HashTableDemoResult:
    """Structured results for the hash table lab demo.

    Attributes:
        dataset_size: Number of records used in the demo.
        collision_demo: True when forced-collision keys were used.
        steps: Ordered validation step rows.
        operation_results: Ordered (label, LabOperationResult) trace.
        stats: Final HashTableStats snapshot.
        summary_lines: Bullet-style summary lines for UI rendering.

    Logic:
        This dataclass bundles every artifact produced by the hash-table demo.
        1. Carry the dataset size and whether collision-mode was used.
        2. Carry the validation rows and the per-operation traces.
        3. Carry the final stats snapshot and summary lines for display.
    """

    dataset_size: int
    collision_demo: bool
    steps: list[ValidationStepResult]
    operation_results: list[tuple[str, LabOperationResult]]
    stats: HashTableStats
    summary_lines: list[str]

# ------------------------------------------------------------------------- end class HashTableDemoResult


# ------------------------------------------------------------------------- class PriorityQueueDemoResult
@dataclass
class PriorityQueueDemoResult:
    """Structured results for the priority queue lab demo.

    Attributes:
        dataset_size: Number of items used in the demo.
        mode: Heap mode ("max" or "min") used for the demo.
        steps: Ordered validation step rows.
        operation_results: Ordered (label, LabOperationResult) trace.
        extraction_preview: Compact preview of upcoming extractions.
        summary_lines: Bullet-style summary lines for UI rendering.

    Logic:
        This dataclass bundles every artifact produced by the priority-queue demo.
        1. Carry dataset size, mode, validation rows, and per-operation traces.
        2. Carry an extraction preview (next-N peek) for UI display.
        3. Carry summary lines that explain the heap state after the demo.
    """

    dataset_size: int
    mode: str
    steps: list[ValidationStepResult]
    operation_results: list[tuple[str, LabOperationResult]]
    extraction_preview: list[str]
    summary_lines: list[str]

# ------------------------------------------------------------------------- end class PriorityQueueDemoResult


# ------------------------------------------------------------------------- class BenchmarkValidationResult
@dataclass
class BenchmarkValidationResult:
    """Structured results for the benchmark lab validation summary.

    Attributes:
        benchmark_df: Raw benchmark results DataFrame.
        speedup_df: Per-scenario speedup summary DataFrame.
        operation_scaling_df: Per-operation scaling summary DataFrame.
        checks: Ordered rubric-style validation rows.
        summary_lines: Bullet-style summary lines for UI rendering.
        correct_rows: Count of benchmark rows that passed correctness.
        total_rows: Total number of benchmark rows produced.
        hash_faster_scenarios: Count of (size, mode) scenarios where hash beat linear.
        total_search_scenarios: Count of all search-comparison scenarios.
        meets_assignment_requirement: True when every rubric check passes.

    Logic:
        This dataclass bundles every artifact produced by the benchmark validation.
        1. Carry the three benchmark DataFrames for downstream rendering.
        2. Carry the rubric checks plus aggregate count summaries.
        3. Expose meets_assignment_requirement as the final pass/fail rollup.
    """

    benchmark_df: pd.DataFrame
    speedup_df: pd.DataFrame
    operation_scaling_df: pd.DataFrame
    checks: list[ValidationStepResult]
    summary_lines: list[str]
    correct_rows: int
    total_rows: int
    hash_faster_scenarios: int
    total_search_scenarios: int
    meets_assignment_requirement: bool

# ------------------------------------------------------------------------- end class BenchmarkValidationResult


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# SHARED HELPERS
# ==============================================================================
# Helpers used by the guided demos and the benchmark validator.
# Kept private (underscore prefix) so the public surface stays small.
#
# - Function: _count_passed()                  - Count passing rows
# - Function: _build_collision_records()       - Forced-collision (key, value) pairs
# - Function: _build_demo_insert_key()         - Pick a guaranteed-unique demo key
# - Function: _build_priority_insert_item()    - Build an extreme-priority demo item
# - Function: _build_extraction_preview()      - Preview next-N extractions
# - Function: _validate_scenario_pairing()     - Hash/linear pairing check
# - Function: _bulk_load_hash_records()        - Batch insert into a HashTable
# - Function: _bulk_load_priority_items()      - Batch insert into a queue
# - Function: _snapshot_hash_table()           - Render bucket snapshot rows
# - Function: _snapshot_priority_queue()       - Render heap-array snapshot rows
# - Function: _first_snapshot_diff()           - Locate first differing snapshot row
# - Function: _find_snapshot_row()             - Locate snapshot row by token
# - Function: _resolve_snapshot_highlights()   - Choose before/after highlight indices
# - Function: _capture_hash_operation()        - Wrap a hash op as LabOperationResult
# - Function: _capture_priority_operation()    - Wrap a queue op as LabOperationResult
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _count_passed()
def _count_passed(steps: list[ValidationStepResult]) -> int:
    """Return the number of passing steps.

    Logic:
        This helper counts how many step rows have passed=True.
        1. Iterate the step list with a generator expression.
        2. Sum 1 per row whose passed attribute is truthy.
    """
    return sum(1 for step in steps if step.passed)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_collision_records()
def _build_collision_records(
    count: int,
    capacity: int,
    target_bucket: int,
    seed: int,
) -> list[tuple[str, int]]:
    """Generate deterministic key-value records that collide by design.

    Logic:
        This helper pairs forced-collision keys with deterministic int values.
        1. Generate `count` keys that all hash to `target_bucket`.
        2. Generate a deterministic integer-value dataset.
        3. Zip them so every record uses a colliding key.
    """
    collision_keys = generate_collision_keys(
        count=count,
        capacity=capacity,
        target_bucket=target_bucket,
    )
    base_records = generate_key_value_dataset(count, seed=seed)
    return [
        (collision_key, value)
        for collision_key, (_, value) in zip(collision_keys, base_records)
    ]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_demo_insert_key()
def _build_demo_insert_key(records: list[tuple[str, object]]) -> str:
    """Return a unique key for guided hash-table insert tests.

    Logic:
        This helper finds a "demo-item-NNN" key that does not already exist.
        1. Build a set of existing keys for O(1) membership checks.
        2. Walk candidate ids starting just past the dataset size.
        3. Return the first candidate that is not already present.
    """
    existing_keys = {key for key, _ in records}
    candidate_id = len(records) + 1
    # MAIN ITERATION LOOP: try candidate ids until a free key is found
    while True:
        candidate = f"demo-item-{candidate_id:03d}"
        if candidate not in existing_keys:
            return candidate
        candidate_id += 1
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_priority_insert_item()
def _build_priority_insert_item(
    items: list[PriorityItem],
    mode: str,
) -> PriorityItem:
    """Build an extreme-priority demo item for heap validation.

    Logic:
        This helper crafts a guaranteed-root item for the heap demo.
        1. Read the existing priority distribution.
        2. DISPATCH on heap mode: max-heap uses max+1000, min-heap uses min-1000.
        3. Assign a sequence_number greater than every existing one for stability.
    """
    priorities = [item.priority for item in items]
    # DISPATCH: pick a priority that is guaranteed to dominate the chosen mode
    if mode == "max":
        new_priority = max(priorities) + 1_000
    else:
        new_priority = min(priorities) - 1_000
    return PriorityItem(
        label=f"demo-{mode}-priority",
        priority=new_priority,
        payload="guided demo item",
        sequence_number=max(item.sequence_number for item in items) + 1,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_extraction_preview()
def _build_extraction_preview(
    queue: BinaryHeapPriorityQueue,
    preview_count: int = 5,
) -> list[str]:
    """Return a short preview of upcoming heap extractions.

    Logic:
        This helper previews the next extractions without mutating the queue.
        1. Clone the queue by inserting every item into a fresh heap.
        2. Extract up to preview_count items from the clone.
        3. Format each extraction as "label (priority=n)" for the UI.
    """
    # Step 1: clone the queue so the live heap stays untouched
    clone = BinaryHeapPriorityQueue(mode=queue.mode)
    for item in queue.to_list():
        clone.insert(item)

    preview: list[str] = []
    # MAIN ITERATION LOOP: drain up to preview_count items from the clone
    while not clone.is_empty() and len(preview) < preview_count:
        item = clone.extract_top()
        preview.append(f"{item.label} (priority={item.priority})")
    return preview
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _validate_scenario_pairing()
def _validate_scenario_pairing(df: pd.DataFrame) -> tuple[bool, str]:
    """Check that each search-comparison scenario includes both methods.

    Logic:
        This validator confirms hash/linear pairing across every (size, mode).
        1. Filter df to the search_comparison rows.
        2. VALIDATION: reject when there are no search-comparison rows.
        3. For each (size, scenario), require both methods and matching query counts.
    """
    search_df = df[df["operation_group"] == "search_comparison"].copy()
    # VALIDATION: no rows means the search-comparison block did not run
    if search_df.empty:
        return False, "No search-comparison rows were recorded."

    required_methods = {"Hash Table", "Linear Search"}
    # MAIN ITERATION LOOP: every (size, scenario) must have the required pairing
    for (size, mode), group in search_df.groupby(["size", "scenario"]):
        group_methods = set(str(value) for value in group["structure"].unique())
        query_count_values = set(int(value) for value in group["workload_count"].tolist())
        # VALIDATION: pairing missing or query-count mismatch is a failure
        if group_methods != required_methods or len(query_count_values) != 1:
            return (
                False,
                f"Mismatch at size={size}, mode={mode}: methods={sorted(group_methods)}, "
                f"query_counts={sorted(query_count_values)}",
            )
    return True, "Every search-comparison scenario includes both methods with matching query counts."
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _bulk_load_hash_records()
def _bulk_load_hash_records(
    hash_table: HashTable,
    records: list[tuple[str, int]],
) -> None:
    """Insert each record into the provided hash table.

    Logic:
        This helper performs the bulk-load step of the hash-table demo.
        1. Iterate every (key, value) pair in records.
        2. Call hash_table.insert(key, value) for each pair.
    """
    # MAIN ITERATION LOOP: insert every record into the hash table
    for key, value in records:
        hash_table.insert(key, value)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _bulk_load_priority_items()
def _bulk_load_priority_items(
    queue: BinaryHeapPriorityQueue,
    items: list[PriorityItem],
) -> None:
    """Insert each item into the provided priority queue.

    Logic:
        This helper performs the bulk-load step of the priority-queue demo.
        1. Iterate every PriorityItem in items.
        2. Call queue.insert(item) for each one.
    """
    # MAIN ITERATION LOOP: insert every item into the heap
    for item in items:
        queue.insert(item)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _snapshot_hash_table()
def _snapshot_hash_table(table: HashTable) -> list[str]:
    """Return all non-empty bucket rows for a hash table snapshot.

    Logic:
        This helper renders one snapshot row per non-empty bucket.
        1. Walk the bucket array via get_buckets().
        2. Format every non-empty bucket as a chained "(key: value)" string.
        3. Return the list of bucket-display rows.
    """
    rows: list[str] = []
    # MAIN ITERATION LOOP: emit one row per non-empty bucket
    for bucket_index, bucket in enumerate(table.get_buckets()):
        if bucket:
            chain = " -> ".join(f"({entry.key}: {entry.value})" for entry in bucket)
            rows.append(f"bucket[{bucket_index}]: {chain}")
    return rows
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _snapshot_priority_queue()
def _snapshot_priority_queue(queue: BinaryHeapPriorityQueue) -> list[str]:
    """Return all heap-array rows for a priority queue snapshot.

    Logic:
        This helper renders the heap as one row per array slot.
        1. Walk the heap list via to_list() (already a copy).
        2. Format every entry as "[index] label (priority=, seq=)".
        3. Return the list of heap-display rows.
    """
    return [
        (
            f"[{index}] {item.label} "
            f"(priority={item.priority}, seq={item.sequence_number})"
        )
        for index, item in enumerate(queue.to_list())
    ]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _first_snapshot_diff()
def _first_snapshot_diff(before_lines: list[str], after_lines: list[str]) -> int | None:
    """Return the first differing row between two snapshots.

    Logic:
        This helper locates the first index where two snapshots disagree.
        1. Scan the shared prefix and return the first differing index.
        2. SAFETY CHECK: if lengths differ, return the shorter length as the diff index.
        3. Return None when the two snapshots are identical.
    """
    min_len = min(len(before_lines), len(after_lines))
    # MAIN ITERATION LOOP: walk the shared prefix looking for the first divergence
    for index in range(min_len):
        if before_lines[index] != after_lines[index]:
            return index
    # SAFETY CHECK: snapshots of unequal lengths diverge at min_len
    if len(before_lines) != len(after_lines):
        return min_len
    return None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _find_snapshot_row()
def _find_snapshot_row(lines: list[str], token: str) -> int | None:
    """Return the first snapshot row containing *token*.

    Logic:
        This helper performs a substring scan over snapshot rows.
        1. Walk the snapshot rows in order.
        2. Return the first row index whose content contains the token.
        3. Return None when no row matches.
    """
    # MAIN ITERATION LOOP: scan rows for the requested token
    for index, line in enumerate(lines):
        if token in line:
            return index
    return None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _resolve_snapshot_highlights()
def _resolve_snapshot_highlights(
    before_lines: list[str],
    after_lines: list[str],
    *,
    match_token: str | None = None,
) -> tuple[int | None, int | None]:
    """Choose before/after highlight rows for a snapshot pair.

    Logic:
        This helper decides which rows to highlight in the UI snapshots.
        1. When a match_token is provided, prefer token-based highlight rows.
        2. Otherwise, fall back to the first differing row from _first_snapshot_diff.
        3. Adjust highlights for cases where the after snapshot grew or shrank.
    """
    # Step 1: prefer the explicit match_token search when provided
    if match_token:
        before_idx = _find_snapshot_row(before_lines, match_token)
        after_idx = _find_snapshot_row(after_lines, match_token)
        if before_idx is not None or after_idx is not None:
            return before_idx, after_idx

    diff_idx = _first_snapshot_diff(before_lines, after_lines)
    # SAFETY CHECK: identical snapshots produce no highlight rows
    if diff_idx is None:
        return None, None

    # DISPATCH: choose highlight side based on whether the snapshot grew or shrank
    if len(after_lines) > len(before_lines):
        return None, diff_idx
    if len(before_lines) > len(after_lines):
        return diff_idx, None
    return diff_idx, diff_idx
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _capture_hash_operation()
def _capture_hash_operation(
    hash_table: HashTable,
    *,
    operation: str,
    complexity: str,
    summary: str,
    input_details: list[str] | None = None,
    match_key: str | None = None,
    op_callable: Callable[[], object | None],
) -> LabOperationResult:
    """Capture a guided hash-table operation as a LabOperationResult.

    Logic:
        This helper wraps a single hash-table op with timing + before/after state.
        1. Snapshot the bucket state and size before invoking op_callable.
        2. Time the operation using perf_counter for sub-microsecond precision.
        3. Snapshot the bucket state after, and resolve highlight rows.
        4. Build and return a LabOperationResult bundle for the UI.
    """
    before_state = _snapshot_hash_table(hash_table)
    size_before = len(hash_table)
    # Step 1: time the underlying operation
    start_time = time.perf_counter()
    returned_value = op_callable()
    elapsed_time = time.perf_counter() - start_time
    after_state = _snapshot_hash_table(hash_table)
    before_idx, after_idx = _resolve_snapshot_highlights(
        before_state,
        after_state,
        match_token=f"({match_key}:" if match_key else None,
    )
    # Return the LabOperationResult bundle for the UI
    return LabOperationResult(
        structure="Hash Table",
        operation=operation,
        returned_value=returned_value,
        elapsed_time=elapsed_time,
        complexity=complexity,
        size_before=size_before,
        size_after=len(hash_table),
        summary=summary,
        input_details=input_details or [],
        state_label="Bucket Snapshot",
        state_before=before_state,
        state_after=after_state,
        state_before_highlight_idx=before_idx,
        state_after_highlight_idx=after_idx,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _capture_priority_operation()
def _capture_priority_operation(
    queue: BinaryHeapPriorityQueue,
    *,
    operation: str,
    complexity: str,
    summary: str,
    input_details: list[str] | None = None,
    match_label: str | None = None,
    op_callable: Callable[[], object | None],
) -> LabOperationResult:
    """Capture a guided priority-queue operation as a LabOperationResult.

    Logic:
        This helper wraps a single priority-queue op with timing + before/after state.
        1. Snapshot the heap state and size before invoking op_callable.
        2. Time the operation using perf_counter for sub-microsecond precision.
        3. If the result is a PriorityItem and match_label is unset, use its label.
        4. Snapshot the heap state after, resolve highlights, and return the bundle.
    """
    before_state = _snapshot_priority_queue(queue)
    size_before = len(queue)
    # time the underlying operation
    start_time = time.perf_counter()
    returned_value = op_callable()
    elapsed_time = time.perf_counter() - start_time
    after_state = _snapshot_priority_queue(queue)
    resolved_label = match_label

    # derive a highlight label from the returned PriorityItem when possible
    if resolved_label is None and isinstance(returned_value, PriorityItem):
        resolved_label = returned_value.label
    before_idx, after_idx = _resolve_snapshot_highlights(
        before_state,
        after_state,
        match_token=f"] {resolved_label} " if resolved_label else None,
    )
    # Return the LabOperationResult bundle for the UI
    return LabOperationResult(
        structure="Priority Queue",
        operation=operation,
        returned_value=returned_value,
        elapsed_time=elapsed_time,
        complexity=complexity,
        size_before=size_before,
        size_after=len(queue),
        summary=summary,
        input_details=input_details or [],
        state_label="Heap Array",
        state_before=before_state,
        state_after=after_state,
        state_before_highlight_idx=before_idx,
        state_after_highlight_idx=after_idx,
    )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# HASH TABLE GUIDED DEMO
# ==============================================================================
# Top-level orchestrator that drives the Streamlit hash-table lab demo.
#
# - Function: run_hash_table_demo() - End-to-end guided demo + validation
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_hash_table_demo()
def run_hash_table_demo(
    records: list[tuple[str, int]] | None = None,
    *,
    dataset_size: int = 100,
    seed: int = DEFAULT_RANDOM_SEED,
    initial_capacity: int = 53,
    max_load_factor: float = 0.75,
    force_collisions: bool = False,
    collision_target_bucket: int = 0,
) -> tuple[HashTable, HashTableDemoResult]:
    """Run the guided hash-table demo used by the Streamlit lab.

    Logic:
        This orchestrator runs the full guided hash-table demo and returns its bundle.
        1. Step 1: pick the working dataset (caller-supplied or generated).
        2. Step 2: build a fresh HashTable and bulk-load it with the dataset.
        3. Step 3-7: insert/search/delete with rubric-aligned validation rows.
        4. Aggregate stats and summary lines into a HashTableDemoResult.
    """
    # VALIDATION: prefer caller-supplied data when available
    if records is None:
        # DISPATCH: collision-mode generates forced-collision keys instead of normal ones
        if force_collisions:
            working_records = _build_collision_records(
                count=dataset_size,
                capacity=initial_capacity,
                target_bucket=collision_target_bucket,
                seed=seed,
            )
        else:
            working_records = generate_key_value_dataset(dataset_size, seed=seed)
    else:
        working_records = records[:dataset_size]

    hash_table = HashTable(
        initial_capacity=initial_capacity,
        max_load_factor=max_load_factor,
    )

    # Initialize step and operation result lists
    steps: list[ValidationStepResult] = []
    operation_results: list[tuple[str, LabOperationResult]] = []

    # Bulk-load the hash table with the working records
    bulk_load_result = _capture_hash_operation(
        hash_table,
        operation="bulk_load",
        complexity="O(n)",
        summary=f"Loaded {len(working_records)} records into a fresh hash table.",
        input_details=[
            f"records = {len(working_records)}",
            f"initial_capacity = {initial_capacity}",
        ],
        op_callable=lambda: _bulk_load_hash_records(hash_table, working_records),
    )

    operation_results.append(("Bulk Load", bulk_load_result))

    # bulk-load validation
    loaded_correctly = len(hash_table) == len(working_records)
    steps.append(
        ValidationStepResult(
            step_name="Bulk Load 100+ Items" if len(working_records) >= 100 else "Bulk Load",
            expected=f"{len(working_records)} records inserted successfully",
            actual=f"size={len(hash_table)}",
            passed=loaded_correctly,
            notes="Demonstrates the required large-data insert path.",
        )
    )

    # insert a new key-value pair
    demo_insert_key = _build_demo_insert_key(working_records)
    demo_insert_value = 999_999
    insert_result = _capture_hash_operation(
        hash_table,
        operation="insert",
        complexity="Avg O(1)",
        summary=f"Inserted guided-demo key '{demo_insert_key}' into the active hash table.",
        input_details=[
            f"key = {demo_insert_key}",
            f"value = {demo_insert_value}",
        ],
        match_key=demo_insert_key,
        op_callable=lambda: hash_table.insert(demo_insert_key, demo_insert_value),
    )
    # Append the insert operation result
    operation_results.append(("Insert New Pair", insert_result))
    inserted_value = hash_table.search(demo_insert_key)
    steps.append(
        ValidationStepResult(
            step_name="Insert New Pair",
            expected=f"{demo_insert_key} -> {demo_insert_value}",
            actual=f"{demo_insert_key} -> {inserted_value}",
            passed=inserted_value == demo_insert_value,
            notes="Uses a key that is guaranteed not to already exist.",
        )
    )

    # Step 3: successful search on an existing key
    search_key, search_expected = working_records[min(10, len(working_records) - 1)]
    search_result = _capture_hash_operation(
        hash_table,
        operation="search",
        complexity="Avg O(1)",
        summary=f"Search checked that existing key '{search_key}' returns its stored value.",
        input_details=[f"key = {search_key}"],
        match_key=search_key,
        op_callable=lambda: hash_table.search(search_key),
    )
    operation_results.append(("Search Existing Key", search_result))
    search_actual = search_result.returned_value
    steps.append(
        ValidationStepResult(
            step_name="Search Existing Key",
            expected=f"{search_key} -> {search_expected}",
            actual=f"{search_key} -> {search_actual}",
            passed=search_actual == search_expected,
        )
    )

    # unsuccessful search
    missing_key = "missing-hash-key"
    missing_result = _capture_hash_operation(
        hash_table,
        operation="search",
        complexity="Avg O(1)",
        summary=f"Search confirmed that missing key '{missing_key}' is not present.",
        input_details=[f"key = {missing_key}"],
        match_key=missing_key,
        op_callable=lambda: hash_table.search(missing_key),
    )
    operation_results.append(("Search Missing Key", missing_result))
    missing_actual = missing_result.returned_value
    steps.append(
        ValidationStepResult(
            step_name="Search Missing Key",
            expected=f"{missing_key} -> None",
            actual=f"{missing_key} -> {missing_actual}",
            passed=missing_actual is None,
        )
    )

    # delete an existing key
    delete_key, delete_expected = working_records[min(25, len(working_records) - 1)]
    delete_result = _capture_hash_operation(
        hash_table,
        operation="delete",
        complexity="Avg O(1)",
        summary=f"Deleted existing guided-demo key '{delete_key}' from the active table.",
        input_details=[f"key = {delete_key}"],
        match_key=delete_key,
        op_callable=lambda: hash_table.delete(delete_key),
    )
    # Append the delete operation result
    operation_results.append(("Delete Existing Key", delete_result))
    deleted_value = delete_result.returned_value
    delete_verified = hash_table.search(delete_key) is None
    steps.append(
        ValidationStepResult(
            step_name="Delete Existing Key",
            expected=f"delete({delete_key}) -> {delete_expected}, then search -> None",
            actual=f"delete -> {deleted_value}, search -> {hash_table.search(delete_key)}",
            passed=(deleted_value == delete_expected) and delete_verified,
            notes="Validates deletion from the active table state.",
        )
    )

    # delete a missing key
    missing_delete_key = "missing-delete-key"
    missing_delete_result = _capture_hash_operation(
        hash_table,
        operation="delete",
        complexity="Avg O(1)",
        summary=f"Delete confirmed that missing key '{missing_delete_key}' is absent.",
        input_details=[f"key = {missing_delete_key}"],
        match_key=missing_delete_key,
        op_callable=lambda: hash_table.delete(missing_delete_key),
    )
    # Append the delete operation result
    operation_results.append(("Delete Missing Key", missing_delete_result))
    missing_delete_actual = missing_delete_result.returned_value
    steps.append(
        ValidationStepResult(
            step_name="Delete Missing Key",
            expected=f"delete({missing_delete_key}) -> None",
            actual=f"delete -> {missing_delete_actual}",
            passed=missing_delete_actual is None,
        )
    )

    # Get hash table statistics
    stats = hash_table.get_stats()
    summary_lines = [
        f"{_count_passed(steps)}/{len(steps)} guided checks passed.",
        f"Final table size: {len(hash_table)} items after insert/delete validation.",
        f"Load factor: {stats.load_factor:.4f} with {stats.total_collisions} total collisions.",
        (
            "Forced-collision mode was used to make separate chaining visible."
            if force_collisions
            else "Standard dataset mode was used for the general 100-item validation."
        ),
    ]
    # Return the hash table demo result
    return (
        hash_table,
        HashTableDemoResult(
            dataset_size=len(working_records),
            collision_demo=force_collisions,
            steps=steps,
            operation_results=operation_results,
            stats=stats,
            summary_lines=summary_lines,
        ),
    )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# PRIORITY QUEUE GUIDED DEMO
# ==============================================================================
# Top-level orchestrator that drives the Streamlit priority-queue lab demo.
#
# - Function: run_priority_queue_demo() - End-to-end guided demo + validation
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_priority_queue_demo()
def run_priority_queue_demo(
    items: list[PriorityItem] | None = None,
    *,
    dataset_size: int = 100,
    seed: int = DEFAULT_RANDOM_SEED,
    mode: str = "max",
) -> tuple[BinaryHeapPriorityQueue, PriorityQueueDemoResult]:
    """Run the guided priority-queue demo used by the Streamlit lab.

    Logic:
        This orchestrator runs the full guided priority-queue demo.
        1. Step 1: pick the working items (caller-supplied or generated).
        2. Step 2: build a fresh BinaryHeapPriorityQueue and bulk-load it.
        3. Step 3-9: exercise insert/peek/search/delete/extract with rubric rows.
        4. Aggregate the extraction preview and summary lines into the result bundle.
    """
    working_items = items[:dataset_size] if items is not None else generate_priority_items(
        dataset_size,
        seed=seed,
    )
    # Create a new priority queue
    queue = BinaryHeapPriorityQueue(mode=mode)
    steps: list[ValidationStepResult] = []
    operation_results: list[tuple[str, LabOperationResult]] = []

    # Bulk-load the priority queue with the working items
    bulk_load_result = _capture_priority_operation(
        queue,
        operation="bulk_load",
        complexity="O(n log n)",
        summary=f"Loaded {len(working_items)} items into a fresh {mode}-heap queue.",
        input_details=[
            f"items = {len(working_items)}",
            f"mode = {mode.upper()}",
        ],
        op_callable=lambda: _bulk_load_priority_items(queue, working_items),
    )
    # Append the bulk-load operation result
    operation_results.append(("Bulk Load", bulk_load_result))

    # bulk-load validation
    bulk_valid = len(queue) == len(working_items) and queue.is_valid_heap()
    steps.append(
        ValidationStepResult(
            step_name="Bulk Load 100+ Items" if len(working_items) >= 100 else "Bulk Load",
            expected=f"{len(working_items)} items inserted and heap valid",
            actual=f"size={len(queue)}, heap_valid={queue.is_valid_heap()}",
            passed=bulk_valid,
        )
    )

    # insert a new top-priority item
    demo_item = _build_priority_insert_item(working_items, mode)
    insert_result = _capture_priority_operation(
        queue,
        operation="insert",
        complexity="O(log n)",
        summary=f"Inserted guided-demo item '{demo_item.label}' into the active heap.",
        input_details=[
            f"label = {demo_item.label}",
            f"priority = {demo_item.priority}",
            f"mode = {mode.upper()}",
        ],
        match_label=demo_item.label,
        op_callable=lambda: queue.insert(demo_item),
    )
    # Append the insert operation result
    operation_results.append(("Insert Priority Item", insert_result))
    inserted_ok = (queue.search(demo_item.label) is not None) and queue.is_valid_heap()
    steps.append(
        ValidationStepResult(
            step_name="Insert Priority Item",
            expected=f"{demo_item.label} inserted and heap remains valid",
            actual=f"present={queue.search(demo_item.label) is not None}, heap_valid={queue.is_valid_heap()}",
            passed=inserted_ok,
        )
    )

    # peek
    peek_result = _capture_priority_operation(
        queue,
        operation="peek",
        complexity="O(1)",
        summary="Peek confirmed that the guided-demo item moved to the heap root.",
        input_details=[f"mode = {mode.upper()}"],
        match_label=demo_item.label,
        op_callable=lambda: queue.peek(),
    )
    # Append the peek operation result
    operation_results.append(("Peek Top Item", peek_result))
    top_item = peek_result.returned_value
    steps.append(
        ValidationStepResult(
            step_name="Peek Top Item",
            expected=f"peek() -> {demo_item.label}",
            actual=f"peek() -> {top_item.label}",
            passed=top_item.label == demo_item.label,
        )
    )

    # search for an existing label
    search_label = working_items[min(30, len(working_items) - 1)].label
    search_operation = _capture_priority_operation(
        queue,
        operation="search",
        complexity="O(n)",
        summary=f"Search checked that existing label '{search_label}' is still present.",
        input_details=[
            f"label = {search_label}",
            f"mode = {mode.upper()}",
        ],
        match_label=search_label,
        op_callable=lambda: queue.search(search_label),
    )
    # Append the search operation result
    operation_results.append(("Search Existing Label", search_operation))
    search_result = search_operation.returned_value
    steps.append(
        ValidationStepResult(
            step_name="Search Existing Label",
            expected=f"search({search_label}) returns an item",
            actual=f"search -> {search_result.label if search_result else None}",
            passed=search_result is not None and search_result.label == search_label,
        )
    )

    # search miss
    missing_label = "no-such-task"
    missing_operation = _capture_priority_operation(
        queue,
        operation="search",
        complexity="O(n)",
        summary=f"Search confirmed that missing label '{missing_label}' is absent.",
        input_details=[
            f"label = {missing_label}",
            f"mode = {mode.upper()}",
        ],
        match_label=missing_label,
        op_callable=lambda: queue.search(missing_label),
    )
    # Append the search operation result
    operation_results.append(("Search Missing Label", missing_operation))
    missing_result = missing_operation.returned_value
    steps.append(
        ValidationStepResult(
            step_name="Search Missing Label",
            expected=f"search({missing_label}) -> None",
            actual=f"search -> {missing_result}",
            passed=missing_result is None,
        )
    )

    # delete an existing label
    delete_label = working_items[min(10, len(working_items) - 1)].label
    delete_result = _capture_priority_operation(
        queue,
        operation="delete",
        complexity="O(n) + O(log n)",
        summary=f"Deleted existing label '{delete_label}' and repaired the heap.",
        input_details=[
            f"label = {delete_label}",
            f"mode = {mode.upper()}",
        ],
        match_label=delete_label,
        op_callable=lambda: queue.delete(delete_label),
    )
    # Append the delete operation result
    operation_results.append(("Delete Existing Label", delete_result))
    deleted_item = delete_result.returned_value
    deleted_verified = queue.search(delete_label) is None and queue.is_valid_heap()
    steps.append(
        ValidationStepResult(
            step_name="Delete Existing Label",
            expected=f"delete({delete_label}) removes the item and preserves heap validity",
            actual=(
                f"delete -> {deleted_item.label if deleted_item else None}, "
                f"heap_valid={queue.is_valid_heap()}"
            ),
            passed=(deleted_item is not None) and deleted_verified,
        )
    )

    # extract the root item
    extract_result = _capture_priority_operation(
        queue,
        operation="extract_top",
        complexity="O(log n)",
        summary="Extract removed the guided-demo root item and preserved heap validity.",
        input_details=[f"mode = {mode.upper()}"],
        match_label=demo_item.label,
        op_callable=lambda: queue.extract_top(),
    )
    # Append the extract operation result
    operation_results.append(("Extract Top Item", extract_result))
    extracted_item = extract_result.returned_value
    extract_valid = extracted_item.label == demo_item.label and queue.is_valid_heap()
    steps.append(
        ValidationStepResult(
            step_name="Extract Top Item",
            expected=f"extract_top() -> {demo_item.label}",
            actual=f"extract_top() -> {extracted_item.label}",
            passed=extract_valid,
            notes="Confirms the heap returns the highest-priority root item.",
        )
    )
    # Build the extraction preview
    extraction_preview = _build_extraction_preview(queue)
    summary_lines = [
        f"{_count_passed(steps)}/{len(steps)} guided checks passed in {mode}-heap mode.",
        f"Heap valid after scripted operations: {queue.is_valid_heap()}.",
        f"Current queue size: {len(queue)} items.",
        (
            "Next extractions: " + ", ".join(extraction_preview)
            if extraction_preview
            else "The queue is empty after the guided demo."
        ),
    ]
    # Return the queue and the demo result
    return (
        queue,
        PriorityQueueDemoResult(
            dataset_size=len(working_items),
            mode=mode,
            steps=steps,
            operation_results=operation_results,
            extraction_preview=extraction_preview,
            summary_lines=summary_lines,
        ),
    )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# BENCHMARK VALIDATION SUITE
# ==============================================================================
# Validation that runs the benchmark engine and rolls the results into a
# rubric-style pass/fail summary used by the Streamlit Benchmark Lab.
#
# - Function: _validate_operation_coverage() - Coverage check for an op group
# - Function: summarize_benchmark_validation() - Roll DataFrames into rubric checks
# - Function: run_benchmark_validation()     - Run benchmarks + summarize
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _validate_operation_coverage()
def _validate_operation_coverage(
    benchmark_df: pd.DataFrame,
    *,
    operation_group: str,
    expected_operations: list[str],
    expected_scenarios: list[str],
) -> tuple[bool, str]:
    """Check that every expected operation/scenario appears at each size.

    Logic:
        This validator confirms an operation group covers every required combo.
        1. Filter benchmark_df to the requested operation_group.
        2. VALIDATION: reject when the group has no rows.
        3. For each (size, scenario, operation), ensure at least one row is present.
    """
    group_df = benchmark_df[benchmark_df["operation_group"] == operation_group].copy()
    # VALIDATION: missing the entire group is a hard fail
    if group_df.empty:
        return False, "No rows were recorded for this operation group."

    sizes = sorted(int(value) for value in group_df["size"].unique())
    missing_rows: list[str] = []
    # MAIN ITERATION LOOP: check coverage for every (size, scenario, operation) combo
    for size in sizes:
        size_df = group_df[group_df["size"] == size]
        for scenario in expected_scenarios:
            for operation in expected_operations:
                mask = (
                    (size_df["scenario"] == scenario)
                    & (size_df["operation"] == operation)
                )
                if size_df[mask].empty:
                    missing_rows.append(f"n={size}, scenario={scenario}, op={operation}")

    # VALIDATION: any missing combo is reported as a coverage failure
    if missing_rows:
        preview = ", ".join(missing_rows[:4])
        if len(missing_rows) > 4:
            preview += ", ..."
        return False, f"Missing rows: {preview}"

    return (
        True,
        f"Sizes={', '.join(str(size) for size in sizes)} | "
        f"Scenarios={', '.join(expected_scenarios)} | "
        f"Operations={', '.join(expected_operations)}",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- summarize_benchmark_validation()
def summarize_benchmark_validation(
    benchmark_df: pd.DataFrame,
    speedup_df: pd.DataFrame,
    operation_scaling_df: pd.DataFrame,
) -> BenchmarkValidationResult:
    """Build a rubric-friendly validation summary from benchmark tables.

    Logic:
        This summarizer rolls every benchmark artifact into the rubric checks.
        1. Compute aggregate counts (correct rows, faster scenarios, etc.).
        2. Run coverage validators for each operation_group.
        3. Build the ordered list of ValidationStepResult rows.
        4. Compute headline summary lines and the meets_assignment_requirement rollup.
    """
    dataset_sizes = sorted(int(value) for value in benchmark_df["size"].unique())
    correct_rows = int(benchmark_df["is_correct"].sum()) if not benchmark_df.empty else 0
    total_rows = int(len(benchmark_df))
    size_requirement_passed = any(size >= 100 for size in dataset_sizes)
    scenario_pairing_passed, scenario_pairing_actual = _validate_scenario_pairing(
        benchmark_df
    )
    # Hash core validation
    hash_core_passed, hash_core_actual = _validate_operation_coverage(
        benchmark_df,
        operation_group="hash_core",
        expected_operations=["insert_bulk", "search_hits", "search_misses", "delete_sample"],
        expected_scenarios=["normal"],
    )
    # Hash collision validation
    hash_collision_passed, hash_collision_actual = _validate_operation_coverage(
        benchmark_df,
        operation_group="hash_collision",
        expected_operations=[
            "collision_insert_bulk",
            "collision_search_hits",
            "collision_delete_sample",
        ],
        expected_scenarios=["forced_collision"],
    )
    # Priority queue core validation
    priority_core_passed, priority_core_actual = _validate_operation_coverage(
        benchmark_df,
        operation_group="priority_queue_core",
        expected_operations=[
            "insert_bulk",
            "peek",
            "extract_top_drain",
            "search_hits",
            "search_misses",
            "delete_sample",
        ],
        expected_scenarios=list(DEFAULT_HEAP_MODES),
    )
    # Collision metrics validation
    collision_rows = benchmark_df[benchmark_df["operation_group"] == "hash_collision"]
    collision_metrics_passed = (
        not collision_rows.empty
        and collision_rows["collision_count"].map(
            lambda value: int(value) if pd.notna(value) else 0
        ).gt(0).all()
    )
    # Priority queue mutating rows validation   
    priority_mutating_rows = benchmark_df[
        (benchmark_df["operation_group"] == "priority_queue_core")
        & (benchmark_df["operation"].isin(["insert_bulk", "extract_top_drain", "delete_sample"]))
    ]
    # Heap validity validation
    heap_validity_passed = (
        not priority_mutating_rows.empty
        and priority_mutating_rows["heap_valid_after"].map(
            lambda value: bool(value) if pd.notna(value) else False
        ).all()
    )
    #    Hash faster scenarios
    hash_faster_scenarios = int((speedup_df["speedup"] > 1.0).sum()) if not speedup_df.empty else 0
    # Total search scenarios
    total_search_scenarios = int(len(speedup_df))
    # Build the checks list
    checks = [
        # Dataset size coverage
        # Dataset size coverage
        ValidationStepResult(
            step_name="Dataset Size Coverage",
            expected="At least one benchmark uses 100 or more items",
            actual=f"Sizes tested: {', '.join(str(size) for size in dataset_sizes)}",
            passed=size_requirement_passed,
        ),
        # Search comparison pairing
        ValidationStepResult(
            step_name="Search Comparison Pairing",
            expected="Each search-comparison scenario includes Hash Table and Linear Search with matching query counts",
            actual=scenario_pairing_actual,
            passed=scenario_pairing_passed,
        ),
        # Hash core coverage
        ValidationStepResult(
            step_name="Hash Core Coverage",
            expected="Hash core workloads cover insert, hit search, miss search, and delete on every size",
            actual=hash_core_actual,
            passed=hash_core_passed,
        ),
        # Hash collision coverage
        ValidationStepResult(
            step_name="Hash Collision Coverage",
            expected="Collision workloads cover insert, hit search, and delete on every size",
            actual=hash_collision_actual,
            passed=hash_collision_passed,
        ),
        # Priority queue coverage
        ValidationStepResult(
            step_name="Priority Queue Coverage",
            expected="Priority queue workloads cover all required operations in both heap modes",
            actual=priority_core_actual,
            passed=priority_core_passed,
        ),
        # All rows correct
        ValidationStepResult(
            step_name="All Rows Correct",
            expected="Every raw benchmark row passes its correctness checks",
            actual=f"{correct_rows}/{total_rows} rows passed",
            passed=correct_rows == total_rows and total_rows > 0,
        ),
        # Collision metrics recorded
        ValidationStepResult(
            step_name="Collision Metrics Recorded",
            expected="Forced-collision rows record one or more collisions",
            actual=(
                "All collision rows recorded positive collision counts."
                if collision_metrics_passed
                else "One or more collision rows reported zero collisions."
            ),
            passed=collision_metrics_passed,
        ),
        # Priority heap validity
        ValidationStepResult(
            step_name="Priority Heap Validity",
            expected="All mutating priority-queue workloads preserve heap validity",
            actual=(
                "All mutating priority-queue rows reported heap_valid_after=True."
                if heap_validity_passed
                else "One or more mutating priority-queue rows reported invalid heap state."
            ),
            passed=heap_validity_passed,
        ),
        # Observed speedup
        ValidationStepResult(
            step_name="Observed Speedup",
            expected="Hash table search is faster than linear search in at least one scenario",
            actual=f"{hash_faster_scenarios}/{total_search_scenarios} scenarios faster",
            passed=hash_faster_scenarios > 0,
        ),
    ]
    
    # Build the summary lines
    fastest_line = "No speedup data available."
    if not speedup_df.empty:
        fastest_row = speedup_df.sort_values("speedup", ascending=False).iloc[0]
        fastest_line = (
            f"Best observed speedup: {fastest_row['speedup']:.2f}x at "
            f"size={int(fastest_row['dataset_size'])}, mode={fastest_row['query_mode']}."
        )
    # Build the scaling line
    scaling_line = "No scaling summary is available."
    if not operation_scaling_df.empty:
        largest_growth_row = operation_scaling_df.sort_values(
            "growth_factor",
            ascending=False,
        ).iloc[0]
        scaling_line = (
            f"Largest growth factor: {largest_growth_row['structure']}."
            f"{largest_growth_row['operation']} ({largest_growth_row['scenario']}) "
            f"grew {largest_growth_row['growth_factor']:.2f}x across the tested sizes."
        )
    # Build the summary lines
    summary_lines = [
        f"{_count_passed(checks)}/{len(checks)} benchmark validation checks passed.",
        f"Correct benchmark rows: {correct_rows}/{total_rows}.",
        f"Observed hash table speedup in {hash_faster_scenarios} of {total_search_scenarios} search scenarios.",
        fastest_line,
        scaling_line,
    ]
    # Return the validation result
    return BenchmarkValidationResult(
        benchmark_df=benchmark_df,
        speedup_df=speedup_df,
        operation_scaling_df=operation_scaling_df,
        checks=checks,
        summary_lines=summary_lines,
        correct_rows=correct_rows,
        total_rows=total_rows,
        hash_faster_scenarios=hash_faster_scenarios,
        total_search_scenarios=total_search_scenarios,
        meets_assignment_requirement=all(check.passed for check in checks),
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- run_benchmark_validation()
def run_benchmark_validation(
    *,
    sizes: list[int] | None = None,
    query_modes: list[str] | None = None,
    query_count: int = DEFAULT_QUERY_COUNT,
    repeats: int = DEFAULT_REPEATS,
    seed: int = DEFAULT_RANDOM_SEED,
    progress_callback: Callable[[int, int, str], None] | None = None,
) -> BenchmarkValidationResult:
    """Run the full benchmark suite and return a validation summary.

    Logic:
        This entry point chains the benchmark engine with the validation summary.
        1. Run the benchmark sweep with the requested sizes/modes/repeats.
        2. Compute the speedup and operation-scaling summary tables.
        3. Hand all three DataFrames to summarize_benchmark_validation().
    """
    # Run the benchmark sweep
    benchmark_df = run_benchmarks(
        sizes=sizes if sizes is not None else DEFAULT_SIZES,
        query_modes=query_modes if query_modes is not None else DEFAULT_QUERY_MODES,
        query_count=query_count,
        repeats=repeats,
        seed=seed,
        progress_callback=progress_callback,
    )
    # Compute the speedup and operation-scaling summary tables
    speedup_df = compute_speedup_summary(benchmark_df)
    operation_scaling_df = compute_operation_scaling_summary(benchmark_df)
    # Return the validation result
    return summarize_benchmark_validation(
        benchmark_df,
        speedup_df,
        operation_scaling_df,
    )
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
