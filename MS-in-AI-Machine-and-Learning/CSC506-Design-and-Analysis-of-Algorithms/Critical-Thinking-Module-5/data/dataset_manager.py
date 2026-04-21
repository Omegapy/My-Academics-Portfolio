# -------------------------------------------------------------------------
# File: dataset_manager.py
# Author: Alexander Ricciardi
# Date: 2026-04-14
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Dataset generation for hash table key-value
# records, priority queue items, benchmark query lists, and forced
# collision scenarios.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset generation, validation, and preview utilities.

Provides deterministic generators for key-value datasets, priority items,
search queries, and forced-collision demo keys.
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

import random

from models.priority_item import PriorityItem

# ______________________________________________________________________________
# Global Constants / Variables
# ==============================================================================
# DATASET CONSTRAINTS & DETERMINISM
# ==============================================================================
#
# DETERMINISM POLICY:
#   Every generator accepts an explicit seed and uses random.Random(seed) to
#   isolate state from the global RNG. This makes lab demos and benchmark
#   runs byte-reproducible across machines and re-runs.
#
# KEY/LABEL CONVENTIONS:
#   - key-value records use "item-NNN" keys (3-digit zero-padded ids).
#   - priority items use "task-NNN" labels with sequential sequence_numbers.
#   - missed/absent search queries use "missing-NNNNNN" so collisions with
#     real keys are impossible by construction.
#
# COLLISION KEYS:
#   generate_collision_keys() replicates HashTable._hash_code + _compress so
#   the produced keys land in the requested bucket without depending on
#   HashTable's internals at import time.
# ------------------------------------------------------------------------------

# Constraint: deterministic seed used by every generator when no seed is provided.
# Rationale: keeps lab demos and benchmark snapshots reproducible across runs.
DEFAULT_SEED: int = 506
"""Default random seed for reproducible dataset generation."""

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# DATASET GENERATORS
# ==============================================================================
# Datasets generator that generates datasets used by the Streamlit UI and the
# benchmark engine. Each call returns a fresh list so callers can mutate
# safely.
#
# - Function: generate_key_value_dataset() - (key, int) pairs for hash workloads
# - Function: generate_priority_items()    - PriorityItem list for heap workloads
# - Function: generate_search_queries()    - Hits / misses / mixed query lists
# - Function: generate_collision_keys()    - Force-bucket keys for chaining demos
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- generate_key_value_dataset()
def generate_key_value_dataset(
    size: int,
    seed: int | None = None,
) -> list[tuple[str, int]]:
    """Generate a deterministic list of (string-key, int-value) pairs.

    Keys are formatted as ``"item-001"``, ``"item-002"``, etc.
    Values are random integers in the range [1, 10_000].

    Logic:
        This generator builds the canonical hash-workload dataset.
        1. Seed a local Random instance to keep generation deterministic.
        2. Build "item-NNN" keys with zero-padded ids for stable sort order.
        3. Pair each key with a random integer value in [1, 10_000].
    """
    rng = random.Random(seed)
    return [(f"item-{i + 1:03d}", rng.randint(1, 10_000)) for i in range(size)]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_priority_items()
def generate_priority_items(
    size: int,
    seed: int | None = None,
) -> list[PriorityItem]:
    """Generate a deterministic list of PriorityItem instances.

    Labels are formatted as ``"task-001"``, ``"task-002"``, etc.
    Priorities are random integers in the range [1, 1_000].

    Logic:
        This generator builds the canonical heap-workload dataset.
        1. Seed a local Random instance to keep generation deterministic.
        2. Build "task-NNN" labels with zero-padded ids.
        3. Assign random priorities and an increasing sequence_number for tie-breaking.
    """
    rng = random.Random(seed)
    return [
        PriorityItem(
            label=f"task-{i + 1:03d}",
            priority=rng.randint(1, 1_000),
            payload=f"payload for task {i + 1}",
            sequence_number=i,
        )
        for i in range(size)
    ]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_search_queries()
def generate_search_queries(
    records: list[tuple[str, int]],
    mode: str,
    query_count: int,
    seed: int | None = None,
) -> list[str]:
    """Build a list of search-query keys for benchmarking.

    Logic:
        This function builds query lists tailored to a benchmark scenario.
        1. Seed a local Random instance and snapshot the existing keys.
        2. DISPATCH on mode: "hits" returns sampled real keys, "misses" returns
           guaranteed-missing keys, "mixed" interleaves them.
        3. Raise ValueError when mode is not one of the supported values.
    """
    rng = random.Random(seed)
    existing_keys = [k for k, _ in records]

    # DISPATCH: every query is guaranteed to be a present key
    if mode == "hits":
        return [rng.choice(existing_keys) for _ in range(query_count)]

    # DISPATCH: every query is constructed to never collide with a real key
    if mode == "misses":
        return [f"missing-{i + 1:06d}" for i in range(query_count)]

    # DISPATCH: alternate hits and misses for a balanced workload
    if mode == "mixed":
        queries: list[str] = []
        # MAIN ITERATION LOOP: alternate between guaranteed hits and misses
        for i in range(query_count):
            if i % 2 == 0:
                queries.append(rng.choice(existing_keys))
            else:
                queries.append(f"missing-{i + 1:06d}")
        return queries

    # VALIDATION: any other mode is unsupported and rejected loudly
    raise ValueError(f"Unknown query mode: {mode!r}. Use 'hits', 'misses', or 'mixed'.")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_collision_keys()
def generate_collision_keys(
    count: int,
    capacity: int,
    target_bucket: int = 0,
) -> list[str]:
    """Create string keys that intentionally collide in a hash table.

    Uses the same position-weighted hash function as the HashTable class
    (multiply running value by 31, add ord(ch), compress with modulo) to
    find keys that map to *target_bucket*.

    Logic:
        This function brute-force searches for keys that hash to one bucket.
        1. Iterate "collide-NNNNN" candidates in order.
        2. Recompute the HashTable hash inline so the helper has no import cycle.
        3. Append a candidate when its compressed hash equals target_bucket.
        4. Stop when the requested *count* of colliding keys has been produced.
    """
    # STRATEGY: brute-force search through candidate keys
    colliding: list[str] = []
    candidate_id = 0
    # MAIN ITERATION LOOP: keep producing candidates until we have *count* hits
    while len(colliding) < count:
        # Step 1: build the next candidate key
        key = f"collide-{candidate_id:05d}"
        # Step 2: replicate the HashTable._hash_code + _compress logic
        h = 0
        for ch in key:
            h = h * 31 + ord(ch)
        # Step 3: keep the candidate when it lands in the requested bucket
        if h % capacity == target_bucket:
            colliding.append(key)
        # Step 4: advance to the next candidate id for the next iteration
        candidate_id += 1
    return colliding
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# PREVIEW AND VALIDATION
# ==============================================================================
# Helpers used by the Streamlit Dataset Builder tab and by tests.
# Validators return a (bool, message) pair so the UI can surface user-friendly
# diagnostics without raising.
#
# - Function: preview_records()              - Compact "head" preview of records
# - Function: validate_key_value_dataset()   - Shape check for KV records
# - Function: validate_priority_items()      - Type check for priority items
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- preview_records()
def preview_records(
    records: list[tuple[str, int]],
    count: int = 10,
) -> str:
    """Return a compact preview string of key-value records.

    Shows the first *count* records and a trailing count summary.

    Logic:
        This helper renders a short head-of-list preview for UI display.
        1. VALIDATION: return an "(empty dataset)" placeholder when records is empty.
        2. Slice the first *count* records and format each as "key -> value".
        3. Append a summary line when the dataset has more entries than shown.
    """
    # VALIDATION: empty datasets get a clear placeholder string
    if not records:
        return "(empty dataset)"
    shown = records[:count]
    lines = [f"  {k} -> {v}" for k, v in shown]
    # Append a trailing summary when more rows exist than were displayed
    if len(records) > count:
        lines.append(f"  ... ({len(records)} items total)")
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- validate_key_value_dataset()
def validate_key_value_dataset(
    records: list[tuple[str, int]],
) -> tuple[bool, str]:
    """Check that a key-value dataset is non-empty and well-formed.

    Logic:
        This validator confirms the shape contract of a KV dataset.
        1. VALIDATION: reject empty input lists with a descriptive message.
        2. Walk each record and verify it is a 2-tuple with a string key.
        3. Return (True, summary) when every record is well-formed.
    """
    # VALIDATION: empty datasets are never considered valid
    if not records:
        return False, "Dataset is empty."
    # MAIN ITERATION LOOP: type-check each record's shape and key type
    for i, item in enumerate(records):
        # VALIDATION: each record must be a 2-tuple
        if not isinstance(item, tuple) or len(item) != 2:
            return False, f"Record {i} is not a 2-tuple: {item!r}"
        # VALIDATION: the first element must be a string key
        if not isinstance(item[0], str):
            return False, f"Record {i} key is not a string: {item[0]!r}"
    return True, f"Valid dataset with {len(records)} records."
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- validate_priority_items()
def validate_priority_items(
    items: list[PriorityItem],
) -> tuple[bool, str]:
    """Check that a priority-item list is non-empty and well-formed.

    Logic:
        This validator confirms the type contract of a priority-item list.
        1. VALIDATION: reject empty input lists with a descriptive message.
        2. Walk every item and confirm its concrete type is PriorityItem.
        3. Return (True, summary) when every item is the expected type.
    """
    # VALIDATION: empty lists are never considered valid
    if not items:
        return False, "Priority item list is empty."
    # MAIN ITERATION LOOP: type-check each item against PriorityItem
    for i, item in enumerate(items):
        if not isinstance(item, PriorityItem):
            return False, f"Item {i} is not a PriorityItem: {item!r}"
    return True, f"Valid priority item list with {len(items)} items."
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
