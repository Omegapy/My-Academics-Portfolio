# -------------------------------------------------------------------------
# File: dataset_manager.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-26
# File Path: Portfolio-Milestone-Module-6/data/dataset_manager.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Generate datasets for integers, strings, and tuple keys.
# - Parse manual dataset input and validate BST-safe comparable keys.
# - Build search workloads for labs and benchmarks.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Global Constants / Variables: dataset-type, insertion-pattern, and size
#   policies shared across Module 6.
# - Function Definitions: key generators, insertion-order helpers, and
#   map-item builders.
# - Function Definitions: manual parsing, validation, workload generation,
#   and dataset preview helpers.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: ast, random, collections
# - Third-Party: none
# - Local Project Modules: none
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the Streamlit app, guided demos, and benchmark pipeline.
# - Acts as the single source of truth for dataset policy and parsing rules.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset generation, parsing, and validation.

This module defines the dataset, including key generation, manual
parsing, comparable type validation, construction, and dataset
preview.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

import ast
import random
from collections import deque


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# DATASET POLICIES AND DEFAULTS
# ========================================================================
# These constants define the only supported key families and insertion
# patterns used across the labs, demos, and benchmark pipeline.
#

DEFAULT_DATASET_SIZE: int = 50
"""Default dataset size used by the Module 6 app."""

DEFAULT_RANDOM_SEED: int = 506
"""Default random seed used for reproducible dataset generation."""

# Constraint: one dataset may contain only one comparable key family.
# Rationale: mixed key types would violate the BST ordering rule.
# Whitelist of comparable key families allowed within one dataset.
# Any key family not listed here is rejected to preserve one BST ordering rule.
DATASET_TYPES: tuple[str, ...] = (
    "integers",  # Numeric keys used by the default BST and benchmark demos
    "strings",  # Lexicographically ordered label keys such as ``item-001``
    "tuples",  # Two-int composite keys for comparable structured-key demos
)
"""Supported comparable key-type groups for one tree instance at a time."""

# Constraint: insertion order is limited to the scenarios used in the
# assignment demos and benchmark comparison views.
# Whitelist of insertion-order scenarios supported across the module.
# Any pattern not listed here is rejected so demos and benchmarks stay consistent.
INSERTION_PATTERNS: tuple[str, ...] = (
    "random",  # Shuffle the canonical keys into an unsorted insertion order
    "sorted",  # Preserve canonical order to demonstrate skewed growth
    "balanced",  # Use median-first order to keep the plain BST relatively short
)
"""Supported insertion-order patterns used by demos and benchmarks."""

# Constraint: benchmark sizes should be large enough to show search trends
# while still remaining fast enough for classroom demos.
# Benchmark sizes escalate from assignment-scale demos to larger trend checks.
# The fixed size ladder keeps charts and summary tables comparable run to run.
BENCHMARK_SIZES: tuple[int, ...] = (
    50,  # Minimum assignment-sized workload and smallest classroom demo
    100,  # Small follow-up size for early scaling comparisons
    500,  # Medium benchmark size that still runs quickly in Streamlit
    1_000,  # Large classroom-sized benchmark workload
    5_000,  # Largest built-in size used to show clearer search trends
)
"""Default benchmark sizes for TreeMap vs ListMap search comparison."""


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# DATASET BUILDERS
# ========================================================================
# These helpers generate canonical comparable key families before a later
# step optionally reorders them for a chosen insertion pattern.
#
# --------------------------------------------------------------- _build_integer_keys()
def _build_integer_keys(size: int) -> list[int]:
    """Build the canonical sorted integer key list.

    Logic:
        This helper creates the baseline integer dataset before any later
        reordering.
        1. Count upward from ``1`` through the requested size.
        2. Return the resulting sorted integer key list.
    """
    return list(range(1, size + 1))
# --------------------------------------------------------------- 

# --------------------------------------------------------------- _build_string_keys()
def _build_string_keys(size: int) -> list[str]:
    """Build the canonical sorted string key list.

    Logic:
        This helper creates the baseline string dataset before any later
        reordering.
        1. Build one stable ``item-###`` label per requested position.
        2. Return the resulting sorted string key list.
    """
    return [f"item-{index:03d}" for index in range(1, size + 1)]
# --------------------------------------------------------------- 

# --------------------------------------------------------------- _build_tuple_keys()
def _build_tuple_keys(size: int) -> list[tuple[int, int]]:
    """Build the canonical sorted tuple key list.

    Logic:
        This helper creates the baseline tuple dataset before any later
        reordering.
        1. Build one two-integer tuple per requested position.
        2. Return the resulting sorted tuple key list.
    """
    return [(index, index * 10) for index in range(1, size + 1)]
# --------------------------------------------------------------- 

# --------------------------------------------------------------- build_balanced_insertion_order()
def build_balanced_insertion_order(keys: list[object]) -> list[object]:
    """Return a median-first insertion order for a near-balanced BST.

    Logic:
        This helper reorders comparable keys so sequential insertion tends to
        keep the plain BST short.
        1. Sort the provided keys into canonical order.
        2. Process subranges breadth-first and emit each median first.
        3. Return the resulting median-first insertion order.
    """
    # VALIDATION: empty input trivially yields an empty balanced order.
    if not keys:
        return []

    ordered = sorted(keys)
    result: list[object] = []
    pending: deque[tuple[int, int]] = deque([(0, len(ordered) - 1)])

    # MAIN ITERATION LOOP: process one slice at a time in breadth-first order.
    while pending:
        # Step 1: pop the next subrange that still needs a median.
        start, end = pending.popleft()
        if start > end:
            continue
        # Step 2: emit the median key so inserts stay as balanced as possible.
        middle = (start + end) // 2
        result.append(ordered[middle])
        # Step 3: queue the left and right halves for later processing.
        pending.append((start, middle - 1))
        pending.append((middle + 1, end))

    return result
# ----------------------------------------------------------- 

# --------------------------------------------------------------- _apply_insertion_pattern()
def _apply_insertion_pattern(
    keys: list[object],
    insertion_pattern: str,
    seed: int,
) -> list[object]:
    """Return ``keys`` reordered to match the requested insertion pattern.

    Logic:
        This helper centralizes the dataset ordering rules used across the
        module.
        1. Reject unsupported insertion-pattern names.
        2. Return sorted or balanced order for those explicit modes.
        3. Shuffle a copy of the keys for the random mode.
    """
    # VALIDATION: reject unsupported insertion patterns explicitly.
    if insertion_pattern not in INSERTION_PATTERNS:
        raise ValueError(
            f"Unknown insertion pattern {insertion_pattern!r}. "
            f"Choose from {list(INSERTION_PATTERNS)}."
        )

    # DISPATCH: apply the exact ordering strategy requested by the caller.
    if insertion_pattern == "sorted":
        return list(sorted(keys))
    if insertion_pattern == "balanced":
        return build_balanced_insertion_order(list(keys))

    # Step 3: random mode shuffles a copy so callers keep their original key order.
    shuffled = list(keys)
    random.Random(seed).shuffle(shuffled)
    return shuffled
# --------------------------------------------------------------- 

# --------------------------------------------------------------- generate_keys()
def generate_keys(
    size: int,
    dataset_type: str,
    insertion_pattern: str,
    seed: int = DEFAULT_RANDOM_SEED,
) -> list[object]:
    """Generate comparable keys for the requested dataset type and pattern.

    Logic:
        This function builds one comparable dataset that is safe to load into
        a BST or map.
        1. Build the canonical key family for the requested dataset type.
        2. Reorder that key list to match the requested insertion pattern.
        3. Return a comparable dataset that can safely feed the BST or Map.
    """
    # VALIDATION: non-positive sizes produce an empty workload instead of an
    # invalid partially generated dataset.
    if size <= 0:
        return []

    # DISPATCH: build the canonical sorted key family for the requested type.
    if dataset_type == "integers":
        base_keys: list[object] = _build_integer_keys(size)
    elif dataset_type == "strings":
        base_keys = _build_string_keys(size)
    elif dataset_type == "tuples":
        base_keys = _build_tuple_keys(size)
    else:
        raise ValueError(
            f"Unknown dataset type {dataset_type!r}. "
            f"Choose from {list(DATASET_TYPES)}."
        )

    return _apply_insertion_pattern(base_keys, insertion_pattern, seed)
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# MAP WORKLOAD BUILDERS
# ========================================================================
# These helpers pair generated keys with readable values so the same dataset
# can feed both the TreeMap UI and the benchmark pipeline.
#
# --------------------------------------------------------------- _build_value_for_key()
def _build_value_for_key(index: int, key: object) -> object:
    """Build a readable value object paired with ``key`` for map demos.

    Logic:
        This helper builds the consistent value payload used in the map demos
        and benchmarks.
        1. Package the index, label, and source key into one small mapping.
        2. Return that mapping as the value paired with the key.
    """
    # Payload fields echoed by the Map lab and benchmark result renderers.
    return {
        "id": index,  # Stable 1-based position within the generated workload
        "label": f"value-{index:03d}",  # Human-friendly label shown in the UI
        "source_key": key,  # Original key echoed back for traceability
    }
# --------------------------------------------------------------- 

# --------------------------------------------------------------- generate_map_items()
def generate_map_items(
    size: int,
    dataset_type: str,
    insertion_pattern: str,
    seed: int = DEFAULT_RANDOM_SEED,
) -> list[tuple[object, object]]:
    """Generate key-value items for TreeMap and ListMap workloads.

    Logic:
        This function converts a generated key dataset into readable map items.
        1. Build the requested key list with the shared dataset generator.
        2. Pair each key with its display-friendly value object.
        3. Return the resulting key-value item list.
    """
    keys = generate_keys(
        size=size,
        dataset_type=dataset_type,
        insertion_pattern=insertion_pattern,
        seed=seed,
    )
    return [
        (key, _build_value_for_key(index, key))
        for index, key in enumerate(keys, start=1)
    ]
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# BENCHMARK QUERY BUILDERS
# ========================================================================
# Query-generation helpers preserve key type compatibility so benchmark hits
# and misses stay valid for the currently selected dataset family.
#
# --------------------------------------------------------------- _generate_missing_int_keys()
def _generate_missing_int_keys(
    keys: list[int],
    query_count: int,
) -> list[int]:
    """Generate integer miss-query keys not found in ``keys``.

    Logic:
        This helper creates integer search misses that stay outside the current
        dataset.
        1. Start one value above the largest existing integer key.
        2. Generate the requested number of consecutive missing integers.
        3. Return the resulting miss-query list.
    """
    start = (max(keys) if keys else 0) + 1
    return list(range(start, start + query_count))
# --------------------------------------------------------------- 

# --------------------------------------------------------------- _generate_missing_string_keys()
def _generate_missing_string_keys(
    keys: list[str],
    query_count: int,
) -> list[str]:
    """Generate string miss-query keys not found in ``keys``.

    Logic:
        This helper creates synthetic string misses that do not collide with
        existing keys.
        1. Track the existing keys in a set for fast membership checks.
        2. Propose numbered ``missing-###`` labels until enough misses exist.
        3. Return the resulting miss-query list.
    """
    existing = set(keys)
    misses: list[str] = []
    counter = 1
    # MAIN ITERATION LOOP: keep proposing synthetic keys until enough misses exist.
    while len(misses) < query_count:
        candidate = f"missing-{counter:03d}"
        if candidate not in existing:
            misses.append(candidate)
        counter += 1
    return misses
# --------------------------------------------------------------- 


# --------------------------------------------------------------- _generate_missing_tuple_keys()
def _generate_missing_tuple_keys(
    keys: list[tuple[int, int]],
    query_count: int,
) -> list[tuple[int, int]]:
    """Generate tuple miss-query keys not found in ``keys``.

    Logic:
        This helper creates tuple misses that stay compatible with the tuple
        dataset family.
        1. Track the existing tuple keys for collision checks.
        2. Advance the leading integer until enough fresh tuple keys are found.
        3. Return the resulting miss-query list.
    """
    existing = set(keys)
    start = (max((item[0] for item in keys), default=0)) + 1
    misses: list[tuple[int, int]] = []
    counter = 0
    # MAIN ITERATION LOOP: advance the leading integer until a fresh tuple key appears.
    while len(misses) < query_count:
        candidate = (start + counter, (start + counter) * 100)
        if candidate not in existing:
            misses.append(candidate)
        counter += 1
    return misses
# ---------------------------------------------------------------   

# --------------------------------------------------------------- generate_search_queries()
def generate_search_queries(
    keys: list[object],
    query_mode: str,
    seed: int = DEFAULT_RANDOM_SEED,
    query_count: int | None = None,
) -> list[object]:
    """Generate hit, miss, or mixed search queries for a comparable key list.

    Logic:
        This function builds benchmark query workloads that stay compatible
        with the current key family.
        1. Validate the requested workload mode and derive a query count.
        2. Build hit-only, miss-only, or mixed queries that stay compatible
           with the current key family.
        3. Return a query list suitable for repeated benchmark searches.
    """
    count = query_count if query_count is not None else max(len(keys), 10)
    rng = random.Random(seed)

    # VALIDATION: benchmark views are defined only for hit, miss, and mixed workloads.
    if query_mode not in ("hits", "misses", "mixed"):
        raise ValueError(
            f"Unknown query mode {query_mode!r}. "
            "Choose from ['hits', 'misses', 'mixed']."
        )

    # DISPATCH: hit-only workloads sample directly from existing keys.
    if query_mode == "hits":
        # VALIDATION: hit-only workloads cannot sample from an empty key set.
        if not keys:
            return []
        return [rng.choice(keys) for _ in range(count)]

    # Step 1: build the miss-only query set using a type-matched generator.
    if keys:
        sample = keys[0]
        # DISPATCH: infer the miss generator from the first key so the
        # resulting queries stay compatible with the active dataset family.
        if isinstance(sample, int):
            misses = _generate_missing_int_keys(keys, count)  # type: ignore[arg-type]
        elif isinstance(sample, str):
            misses = _generate_missing_string_keys(keys, count)  # type: ignore[arg-type]
        elif isinstance(sample, tuple):
            misses = _generate_missing_tuple_keys(keys, count)  # type: ignore[arg-type]
        else:
            # VALIDATION: unsupported key families cannot produce safe miss queries.
            raise TypeError(f"Unsupported key type for queries: {type(sample)!r}")
    else:
        misses = _generate_missing_int_keys([], count)

    # DISPATCH: miss-only workloads can return the generated misses directly.
    if query_mode == "misses":
        return misses

    # Step 2: interleave hits and misses for the mixed workload.
    # VALIDATION: without source keys, a mixed workload collapses to miss-only queries.
    if not keys:
        return misses
    hits = [rng.choice(keys) for _ in range(count)]
    mixed: list[object] = []
    # MAIN ITERATION LOOP: alternate hit and miss keys to create a balanced mixed workload.
    for index in range(count):
        # Step 3: alternate between existing and missing keys by index parity.
        mixed.append(hits[index] if index % 2 == 0 else misses[index])
    return mixed
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# MANUAL INPUT PARSING AND VALIDATION
# ========================================================================
# These helpers keep user-provided datasets inside the same type-family and
# uniqueness rules enforced by the automatically generated datasets.
#
# --------------------------------------------------------------- parse_manual_keys()
def parse_manual_keys(raw_text: str, dataset_type: str) -> list[object]:
    """Parse user-supplied keys for the requested dataset type.

    Integer and string datasets accept comma-separated input. Tuple datasets
    accept either a Python-list literal such as ``[(1, 2), (3, 4)]`` or a
    semicolon-separated form such as ``(1, 2); (3, 4)``.

    Logic:
        1. Reject empty input before attempting any parsing.
        2. Dispatch to the parser expected by the chosen dataset type.
        3. Normalize and validate tuple input so only 2-item int tuples pass.
    """
    # VALIDATION: reject empty or whitespace-only input up front.
    if raw_text is None or not raw_text.strip():
        raise ValueError("Manual input cannot be empty.")

    cleaned = raw_text.strip()

    # DISPATCH: integer and string datasets use straightforward comma parsing.
    if dataset_type == "integers":
        return [int(token.strip()) for token in cleaned.split(",") if token.strip()]

    if dataset_type == "strings":
        parsed = [token.strip() for token in cleaned.split(",") if token.strip()]
        if not parsed:
            raise ValueError("At least one string key is required.")
        return parsed

    if dataset_type != "tuples":
        raise ValueError(
            f"Unknown dataset type {dataset_type!r}. Choose from {list(DATASET_TYPES)}."
        )

    # Step 1: normalize semicolon-separated tuple input into a list literal.
    normalized = cleaned
    if not cleaned.startswith("["):
        tuple_parts = [part.strip() for part in cleaned.split(";") if part.strip()]
        normalized = "[" + ", ".join(tuple_parts) + "]"

    # Step 2: safely parse the tuple-literal list.
    try:
        parsed_value = ast.literal_eval(normalized)
    except (SyntaxError, ValueError) as exc:
        raise ValueError(
            "Tuple input must look like [(1, 2), (3, 4)] "
            "or (1, 2); (3, 4)."
        ) from exc

    if not isinstance(parsed_value, list):
        raise ValueError("Tuple input must evaluate to a list of 2-item tuples.")

    parsed_tuples: list[tuple[int, int]] = []
    # MAIN ITERATION LOOP: verify every user-supplied tuple keeps the required
    # two-int shape used by the Module 6 tuple dataset option.
    for item in parsed_value:
        if (
            not isinstance(item, tuple)
            or len(item) != 2
            or not all(isinstance(part, int) for part in item)
        ):
            raise ValueError("Every tuple key must contain exactly two integers.")
        parsed_tuples.append(item)

    if not parsed_tuples:
        raise ValueError("At least one tuple key is required.")

    return parsed_tuples
# --------------------------------------------------------------- 

# --------------------------------------------------------------- validate_unique_keys()
def validate_unique_keys(keys: list[object]) -> tuple[bool, str]:
    """Validate that ``keys`` is non-empty and contains no duplicates.

    Logic:
        This helper enforces the minimum dataset constraints used throughout
        Module 6.
        1. Reject empty datasets.
        2. Reject datasets that contain duplicate keys.
        3. Return a status flag with a user-facing validation message.
    """
    # VALIDATION: empty datasets are not useful for the assignment demos.
    if not keys:
        return False, "Dataset cannot be empty."

    # VALIDATION: duplicate keys would hide update-vs-insert behavior in the BST.
    if len(set(keys)) != len(keys):
        return False, "Dataset keys must be unique for predictable BST behavior."

    return True, "Dataset is valid and contains unique keys."
# --------------------------------------------------------------- 

# --------------------------------------------------------------- validate_dataset()
def validate_dataset(
    keys: list[object],
    dataset_type: str,
) -> tuple[bool, str]:
    """Validate dataset shape, type family, and uniqueness.

    Logic:
        1. Reuse the uniqueness validator for emptiness and duplicate checks.
        2. Confirm the declared dataset type is supported.
        3. Enforce the exact key shape required by that dataset family.
    """
    is_unique, message = validate_unique_keys(keys)
    if not is_unique:
        return False, message

    # VALIDATION: callers must choose one supported dataset family.
    if dataset_type not in DATASET_TYPES:
        return False, f"Unknown dataset type: {dataset_type!r}."

    # DISPATCH: enforce the exact key shape expected by the chosen dataset type.
    if dataset_type == "integers" and not all(isinstance(key, int) for key in keys):
        return False, "Integer datasets must contain only int keys."
    if dataset_type == "strings" and not all(isinstance(key, str) for key in keys):
        return False, "String datasets must contain only str keys."
    if dataset_type == "tuples":
        if not all(
            isinstance(key, tuple)
            and len(key) == 2
            and all(isinstance(part, int) for part in key)
            for key in keys
        ):
            return False, "Tuple datasets must contain only 2-item int tuples."

    return True, "Dataset passed validation."
# --------------------------------------------------------------- 

# --------------------------------------------------------------- preview_dataset()
def preview_dataset(keys: list[object], count: int = 10) -> str:
    """Return a compact head-and-tail preview string for the UI.

    Logic:
        This helper keeps dataset previews readable across small and large
        workloads.
        1. Return a stable placeholder for empty datasets.
        2. Return the full list when it already fits inside the preview budget.
        3. Return a head-and-tail summary string for larger datasets.
    """
    # VALIDATION: empty datasets render as a stable placeholder string.
    if not keys:
        return "[]"
    if len(keys) <= count:
        return str(keys)
    # Step 1: split the preview budget between the head and tail so users can
    # see both the beginning and end of large datasets.
    head_count = count // 2
    tail_count = count - head_count
    return (
        f"{keys[:head_count]} ... {keys[-tail_count:]} "
        f"(total={len(keys)})"
    )
# --------------------------------------------------------------- 

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------
