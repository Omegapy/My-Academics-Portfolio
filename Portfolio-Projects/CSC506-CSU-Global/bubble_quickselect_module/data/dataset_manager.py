# File: dataset_manager.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Generate deterministic integer datasets for sorting and selection labs.
# - Parse and validate manual integer input from Streamlit controls.
# - Provide shared preview and integrated dataset helpers for portfolio tabs.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# DATASET POLICIES:
#   - Constants: DEFAULT_DATASET_SIZE, DEFAULT_RANDOM_SEED, DATASET_TYPES
#
# DATASET GENERATORS:
#   - Functions: random, sorted, reverse-sorted, partial, and duplicate-heavy
#
# PARSING / VALIDATION:
#   - Functions: parse_manual_input(), generate_dataset_by_type()
#   - Functions: validate_dataset(), preview_dataset()
#
# INTEGRATED HELPERS:
#   - Functions: comparable keys, records, graph presets, and preview helpers
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: random, typing
# - Local Project Modules: graph/hash model annotations during type checking
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by algorithm labs, benchmark pipelines, and cross-module data demos.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Integer dataset helpers for Portfolio Module 8 Phase 1.

This module provides reproducible integer-list generators, manual parsing,
validation, and compact previews for the Bubble Sort and Quickselect foundation
and for later Streamlit dataset-builder integration.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

# TYPE CHECKING: imported models are needed only for annotations.
if TYPE_CHECKING:
    from graph_algorithms_module.models import GraphEdge
    from hash_priority_module.models import PriorityItem


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# DATASET POLICIES
# ========================================================================
# These constants define the supported integer dataset scenarios for the
# sorting, selection, set, search, and linked-structure labs.
#
# DATASET POLICY OVERVIEW:
# The generated dataset keys are shared by Streamlit controls, benchmark loops,
# and tests, so the accepted names live in one central section.
#
# Constraint: Dataset type keys are used by Streamlit controls and benchmark CSVs.
#

DEFAULT_DATASET_SIZE: int = 25
"""Default dataset size used by the Module 8 Phase 1 helpers."""

DEFAULT_RANDOM_SEED: int = 506
"""Default seed used for reproducible classroom examples."""

DATASET_TYPES: list[str] = [
    "random",  # uniform pseudo-random integers
    "sorted",  # non-decreasing best-case Bubble Sort workload
    "reverse_sorted",  # descending worst-case Bubble Sort workload
    "duplicate_heavy",  # repeated values for equality-heavy traces
    "partially_sorted",  # mostly ordered data with controlled disorder
    "manual",  # caller-provided comma-separated input
]
"""Supported dataset type keys for generated and manually parsed datasets."""


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# DATASET GENERATORS
# ========================================================================
# Contains deterministic integer-list builders for the sorting and selection
# demonstrations.
#
# GENERATOR OVERVIEW:
# Each generator returns a new list and uses a local random seed when randomness
# is needed, keeping benchmark and UI examples reproducible.
# =========================================================================
# - Function: generate_random_dataset()
# - Function: generate_sorted_dataset()
# - Function: generate_reverse_sorted_dataset()
# - Function: generate_partially_sorted_dataset()
# - Function: generate_duplicate_heavy_dataset()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- generate_random_dataset()
def generate_random_dataset(
    size: int,
    low: int = 1,
    high: int = 1_000,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Generate a reproducible random integer dataset.

    Args:
        size: Number of integers to generate.
        low: Minimum random value, inclusive.
        high: Maximum random value, inclusive.
        seed: Optional seed for deterministic generation.

    Returns:
        A list of random integers. Duplicate values are allowed.
    """
    # SETUP: local RNG keeps dataset generation deterministic and side-effect free.
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(size)]
# --------------------------------------------------------------- end generate_random_dataset()


# --------------------------------------------------------------- generate_sorted_dataset()
def generate_sorted_dataset(
    size: int,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Generate a non-decreasing integer dataset.

    Args:
        size: Number of integers to generate.
        seed: Optional seed for deterministic generation.

    Returns:
        A sorted list of integers.
    """
    data: list[int] = generate_random_dataset(size, seed=seed)
    # Step 1: sort in place to create the best-case Bubble Sort workload.
    data.sort()
    return data
# --------------------------------------------------------------- end generate_sorted_dataset()


# --------------------------------------------------------------- generate_reverse_sorted_dataset()
def generate_reverse_sorted_dataset(
    size: int,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Generate a non-increasing integer dataset.

    Args:
        size: Number of integers to generate.
        seed: Optional seed for deterministic generation.

    Returns:
        A reverse-sorted list of integers.
    """
    data: list[int] = generate_sorted_dataset(size, seed=seed)
    # Step 1: reverse sorted data to create a descending stress case.
    data.reverse()
    return data
# ---------------------------------------------------------- end generate_reverse_sorted_dataset()


# ------------------------------------------------------------- generate_partially_sorted_dataset()
def generate_partially_sorted_dataset(
    size: int,
    disorder_ratio: float = 0.10,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Generate a mostly sorted dataset with deterministic pair swaps.

    Args:
        size: Number of integers to generate.
        disorder_ratio: Fraction of the dataset size used to calculate the
            pair-swap count.
        seed: Optional seed for deterministic generation.

    Returns:
        A mostly sorted list with controlled disorder.
    """
    data: list[int] = generate_sorted_dataset(size, seed=seed)

    # VALIDATION: empty and one-item datasets cannot be meaningfully disordered.
    if size <= 1:
        return data

    rng = random.Random(seed)
    swap_count: int = max(1, int(size * disorder_ratio))

    # MAIN ITERATION LOOP: introduce small, reproducible disruptions.
    for _ in range(swap_count):
        left_index: int = rng.randrange(size)
        right_index: int = rng.randrange(size)
        data[left_index], data[right_index] = data[right_index], data[left_index]

    return data
# ------------------------------------------------------- end generate_partially_sorted_dataset()


# --------------------------------------------------------------- generate_duplicate_heavy_dataset()
def generate_duplicate_heavy_dataset(
    size: int,
    unique_value_count: int = 5,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Generate a deterministic dataset with many repeated values.

    Args:
        size: Number of integers to generate.
        unique_value_count: Maximum number of distinct values to sample from.
        seed: Optional seed for deterministic generation.

    Returns:
        A list of integers where duplicate values are intentionally common.
    """
    # VALIDATION: at least one unique source value is required for sampling.
    source_count: int = max(1, unique_value_count)
    # SETUP: sample from a small deterministic source pool to force duplicates.
    rng = random.Random(seed)
    source_values: list[int] = list(range(1, source_count + 1))
    return [rng.choice(source_values) for _ in range(size)]
# --------------------------------------------------------- end generate_duplicate_heavy_dataset()


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# PARSING AND DISPATCH
# ========================================================================
# Contains manual-input parsing and dataset-type dispatch used by Streamlit
# dataset controls.
#
# PARSING OVERVIEW:
# Manual text is validated token by token, while generated dataset requests are
# routed through the supported type keys.
# =========================================================================
# - Function: parse_manual_input()
# - Function: generate_dataset_by_type()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- parse_manual_input()
def parse_manual_input(raw: str) -> list[int]:
    """Parse comma-separated integer text into a list.

    Args:
        raw: User-provided comma-separated integer text.

    Returns:
        Parsed integer values in the original user-provided order.

    Raises:
        ValueError: If input is blank or contains a non-integer token.
    """
    # VALIDATION: blank input cannot produce a useful dataset.
    if not raw or not raw.strip():
        raise ValueError("Manual dataset input cannot be blank.")

    values: list[int] = []
    tokens: list[str] = raw.split(",")

    # MAIN ITERATION LOOP: parse one comma-separated token at a time.
    for token in tokens:
        cleaned_token: str = token.strip()
        # VALIDATION: consecutive commas or trailing commas create blank tokens.
        if not cleaned_token:
            raise ValueError("Manual dataset input contains a blank value.")
        try:
            # Step 1: preserve user order while normalizing each token to int.
            values.append(int(cleaned_token))
        except ValueError as exc:
            raise ValueError(
                f"Manual dataset value {cleaned_token!r} is not an integer."
            ) from exc

    return values
# --------------------------------------------------------------- end parse_manual_input()


# --------------------------------------------------------------- generate_dataset_by_type()
def generate_dataset_by_type(
    dataset_type: str,
    size: int = DEFAULT_DATASET_SIZE,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Generate an integer dataset for a supported generated type.

    Args:
        dataset_type: Dataset type key such as ``"random"`` or ``"sorted"``.
        size: Number of integers to generate.
        seed: Optional seed for deterministic generation.

    Returns:
        A generated integer dataset.

    Raises:
        ValueError: If the dataset type is ``"manual"`` or unsupported.
    """
    # VALIDATION: manual datasets require raw text and cannot be generated.
    if dataset_type == "manual":
        raise ValueError("Manual datasets must be parsed from raw input text.")

    # DISPATCH: choose the generator that matches the supported dataset key.
    if dataset_type == "random":
        return generate_random_dataset(size=size, seed=seed)
    if dataset_type == "sorted":
        return generate_sorted_dataset(size=size, seed=seed)
    if dataset_type == "reverse_sorted":
        return generate_reverse_sorted_dataset(size=size, seed=seed)
    if dataset_type == "duplicate_heavy":
        return generate_duplicate_heavy_dataset(size=size, seed=seed)
    if dataset_type == "partially_sorted":
        return generate_partially_sorted_dataset(size=size, seed=seed)

    # VALIDATION: unsupported keys cannot be generated safely.
    raise ValueError(
        f"Unknown dataset type {dataset_type!r}. Choose from {DATASET_TYPES}."
    )
# --------------------------------------------------------------- end generate_dataset_by_type()


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# VALIDATION AND PREVIEW
# ========================================================================
# Contains lightweight helpers that validate integer datasets and render compact
# previews for Streamlit tables, captions, and trace panels.
# =========================================================================
# - Function: validate_dataset()
# - Function: preview_dataset()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- validate_dataset()
def validate_dataset(data: list[int]) -> tuple[bool, str]:
    """Validate that a dataset is non-empty and integer-only.

    Args:
        data: Dataset values to validate.

    Returns:
        A tuple containing a validity flag and explanatory message.
    """
    # VALIDATION: algorithms in this phase need at least one value for demos.
    if not data:
        return False, "Dataset is empty."

    # VALIDATION: Phase 1 algorithms are specified for integer lists.
    if not all(isinstance(value, int) for value in data):
        return False, "Dataset contains non-integer values."

    return True, f"Dataset OK: {len(data)} integer value(s)."
# --------------------------------------------------------------- end validate_dataset()


# --------------------------------------------------------------- preview_dataset()
def preview_dataset(data: list[int], count: int = 15) -> str:
    """Return a compact dataset preview string.

    Args:
        data: Dataset values to preview.
        count: Maximum number of leading values to show before truncating.

    Returns:
        A compact string representation suitable for UI display.
    """
    if not data:
        return "[]"
    # VALIDATION: short datasets can be rendered in full without truncation.
    if len(data) <= count:
        return str(data)

    shown_values: str = ", ".join(str(value) for value in data[:count])
    return f"[{shown_values}, ...] ({len(data)} items)"
# --------------------------------------------------------------- end preview_dataset()


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# MODULE 8 INTEGRATED DATASET HELPERS
# ========================================================================
# Contains shared data builders used by the broader integrated portfolio app.
#
# INTEGRATION OVERVIEW:
# These helpers provide comparable keys, key-value records, priority records,
# graph presets, and compact previews for modules beyond Bubble/Quickselect.
# =========================================================================
# - Function: generate_comparable_keys()
# - Function: _balanced_insertion_order()
# - Function: generate_key_value_records()
# - Function: generate_priority_records()
# - Function: generate_graph_preset()
# - Function: preview_records()
# - Function: preview_edges()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- generate_comparable_keys()
def generate_comparable_keys(
    size: int,
    *,
    key_type: str = "integers",
    pattern: str = "random",
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[Any]:
    """Generate comparable keys for tree and map demonstrations.

    Args:
        size: Number of keys to generate.
        key_type: ``"integers"``, ``"strings"``, or ``"tuples"``.
        pattern: ``"random"``, ``"sorted"``, ``"reverse_sorted"``, or
            ``"balanced"``.
        seed: Optional deterministic seed.

    Returns:
        Comparable key values.
    """
    rng = random.Random(seed)
    normalized_type = key_type.strip().lower()
    normalized_pattern = pattern.strip().lower()

    # DISPATCH: build comparable values that match the selected key family.
    if normalized_type == "strings":
        values: list[Any] = [f"K{index + 1:03d}" for index in range(size)]
    elif normalized_type == "tuples":
        values = [(index + 1, (index * 7) % max(size, 1)) for index in range(size)]
    else:
        values = list(range(1, size + 1))

    # DISPATCH: reshape insertion order to demonstrate tree/map behavior.
    if normalized_pattern == "random":
        rng.shuffle(values)
        return values
    if normalized_pattern == "reverse_sorted":
        return list(reversed(values))
    if normalized_pattern == "balanced":
        return _balanced_insertion_order(values)
    # FALLBACK: unknown patterns keep the natural sorted insertion order.
    return values
# --------------------------------------------------------------- end generate_comparable_keys()


# --------------------------------------------------------------- _balanced_insertion_order()
def _balanced_insertion_order(values: list[Any]) -> list[Any]:
    """Return values in median-first order for less-skewed BST insertion.

    Args:
        values: Sorted comparable values.

    Returns:
        Median-first insertion order.
    """
    # VALIDATION: recursion bottoms out when a slice has no values.
    if not values:
        return []
    middle = len(values) // 2
    return [
        values[middle],
        *_balanced_insertion_order(values[:middle]),
        *_balanced_insertion_order(values[middle + 1 :]),
    ]
# --------------------------------------------------------------- end _balanced_insertion_order()


# --------------------------------------------------------------- generate_key_value_records()
def generate_key_value_records(size: int, *, prefix: str = "key") -> list[tuple[str, object]]:
    """Generate deterministic string-key records.

    Args:
        size: Number of records.
        prefix: Key prefix.

    Returns:
        Key-value rows.
    """
    # MAIN ITERATION LOOP: create deterministic string keys with simple payloads.
    return [(f"{prefix}-{index + 1:04d}", {"score": (index * 37) % 101}) for index in range(size)]
# --------------------------------------------------------------- end generate_key_value_records()


# --------------------------------------------------------------- generate_priority_records()
def generate_priority_records(size: int, *, seed: int | None = DEFAULT_RANDOM_SEED) -> list[PriorityItem]:
    """Generate deterministic priority queue rows.

    Args:
        size: Number of records.
        seed: Optional deterministic seed.

    Returns:
        PriorityItem rows.
    """
    from hash_priority_module.models import PriorityItem

    rng = random.Random(seed)
    # MAIN ITERATION LOOP: create stable task labels with deterministic priorities.
    return [
        PriorityItem(
            label=f"task-{index + 1:03d}",
            priority=rng.randint(1, 100),
            payload=f"Generated task {index + 1}",
            sequence_number=index,
        )
        for index in range(size)
    ]
# --------------------------------------------------------------- end generate_priority_records()


# --------------------------------------------------------------- generate_graph_preset()
def generate_graph_preset(
    preset: str,
    *,
    vertex_count: int = 25,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> dict[str, object]:
    """Generate graph preset data for the integrated app.

    Args:
        preset: Preset key such as ``"classroom"``, ``"sparse"``, ``"dense"``,
            or ``"weighted"``.
        vertex_count: Vertex count for generated sparse/dense presets.
        seed: Optional deterministic seed.

    Returns:
        Dictionary containing name, directed flag, vertices, and edges.
    """
    from graph_algorithms_module.data import (
        generate_classroom_graph_data,
        generate_dense_city_graph_data,
        generate_random_graph_data,
        generate_sparse_city_graph_data,
    )

    normalized = preset.strip().lower()
    # DISPATCH: select a graph dataset family for integrated comparisons.
    if normalized == "classroom":
        vertices, edges = generate_classroom_graph_data()
        name = "Small classroom graph"
    elif normalized == "dense":
        vertices, edges = generate_dense_city_graph_data()
        name = "Dense weighted city graph"
    elif normalized == "weighted":
        vertices, edges = generate_sparse_city_graph_data()
        name = "Weighted Dijkstra graph"
    else:
        # FALLBACK: unknown presets use a generated sparse graph.
        vertices, edges = generate_random_graph_data(vertex_count, "sparse", seed=seed)
        name = "Sparse generated graph"
    return {
        "name": name,
        "directed": False,
        "vertices": vertices,
        "edges": edges,
    }
# --------------------------------------------------------------- end generate_graph_preset()


# --------------------------------------------------------------- preview_records()
def preview_records(rows: list[object], count: int = 8) -> str:
    """Return a compact preview for non-integer dataset rows.

    Args:
        rows: Values or records to preview.
        count: Maximum leading rows.

    Returns:
        Preview string.
    """
    if not rows:
        return "[]"
    # VALIDATION: short previews can show the complete row list.
    if len(rows) <= count:
        return str(rows)
    return f"{rows[:count]!r} ... ({len(rows)} items)"
# --------------------------------------------------------------- end preview_records()


# --------------------------------------------------------------- preview_edges()
def preview_edges(edges: list[GraphEdge], count: int = 8) -> str:
    """Return a compact graph-edge preview.

    Args:
        edges: Edge rows.
        count: Maximum edge rows.

    Returns:
        Multi-line preview text.
    """
    if not edges:
        return "(no edges)"
    # MAIN ITERATION LOOP: format the leading edge rows for compact display.
    lines = [f"{edge.source} -> {edge.target} ({edge.weight:g})" for edge in edges[:count]]
    # VALIDATION: append a count note only when rows were truncated.
    if len(edges) > count:
        lines.append(f"... ({len(edges)} edges total)")
    return "\n".join(lines)
# --------------------------------------------------------------- end preview_edges()

# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
