# -------------------------------------------------------------------------
# File: dataset_manager.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Dataset generation, validation, and preview helpers for the four required
# sorting scenarios: random, sorted, reverse sorted, and partially sorted.
# -------------------------------------------------------------------------

# --- Functions ---
# - generate_random_dataset()            — random integers (may contain duplicates)
# - generate_sorted_dataset()            — ascending integers
# - generate_reverse_sorted_dataset()    — descending integers
# - generate_partially_sorted_dataset()  — mostly ascending with random swaps
# - generate_dataset_by_type()           — dispatcher mapping string to generator
# - preview_dataset()                    — short string representation
# - validate_dataset()                   — non-empty + all-ints check
# - is_sorted_non_decreasing()           — correctness helper
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset generation and validation.

All generators accept an optional ``seed`` for reproducibility.
"""

# ________________
# Imports
#

from __future__ import annotations

import random

# __________________________________________________________________________
# Dataset Generation Functions
#

# ========================================================================
# Generation
# ========================================================================

# --------------------------------------------------------------- generate_random_dataset()
def generate_random_dataset(
    size: int,
    low: int = 1,
    high: int = 1_000_000,
    seed: int | None = None,
) -> list[int]:
    """Generate a list of *size* random integers in [low, high].

    Duplicates are allowed so the function works for any *size* without
    requiring the range to be larger than the list.

    Args:
        size: Number of elements to generate.
        low: Minimum value (inclusive).
        high: Maximum value (inclusive).
        seed: Optional random seed for reproducibility.

    Returns:
        A list of random integers in arbitrary order.
    """
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(size)]
# --------------------------------------------------------------- end generate_random_dataset()


# --------------------------------------------------------------- generate_sorted_dataset()
def generate_sorted_dataset(
    size: int,
    seed: int | None = None,
) -> list[int]:
    """Generate a sorted (ascending) list of *size* random integers.

    Args:
        size: Number of elements to generate.
        seed: Optional random seed for reproducibility.

    Returns:
        A list of integers in non-decreasing order.
    """
    data = generate_random_dataset(size, seed=seed)
    data.sort()
    return data
# --------------------------------------------------------------- end generate_sorted_dataset()


# --------------------------------------------------------------- generate_reverse_sorted_dataset()
def generate_reverse_sorted_dataset(
    size: int,
    seed: int | None = None,
) -> list[int]:
    """Generate a reverse-sorted (descending) list of *size* random integers.

    Args:
        size: Number of elements to generate.
        seed: Optional random seed for reproducibility.

    Returns:
        A list of integers in non-increasing order.
    """
    data = generate_random_dataset(size, seed=seed)
    data.sort(reverse=True)
    return data
# --------------------------------------------------------------- end generate_reverse_sorted_dataset()


# --------------------------------------------------------------- generate_partially_sorted_dataset()
def generate_partially_sorted_dataset(
    size: int,
    disorder_ratio: float = 0.10,
    seed: int | None = None,
) -> list[int]:
    """Generate a mostly-sorted list with a small number of random swaps.

    Starts with an ascending list, then performs
    ``max(1, int(size * disorder_ratio))`` random pair swaps to introduce
    controlled disorder.

    Args:
        size: Number of elements to generate.
        disorder_ratio: Fraction of the list size to use as the swap count
            (default 0.10, i.e. 10%).
        seed: Optional random seed for reproducibility.

    Returns:
        A list that is mostly sorted but contains some out-of-order pairs.
    """
    # Step 1: build ascending base
    data = generate_sorted_dataset(size, seed=seed)

    # Step 2: introduce disorder via random swaps
    rng = random.Random(seed if seed is None else seed + 1)
    swap_count = max(1, int(size * disorder_ratio))
    for _ in range(swap_count):
        i = rng.randrange(size)
        j = rng.randrange(size)
        data[i], data[j] = data[j], data[i]

    return data
# --------------------------------------------------------------- end generate_partially_sorted_dataset()

# ========================================================================
# Dispatcher
# ========================================================================

# VALIDATION: maps user-facing dataset type strings to generator functions
_GENERATORS: dict[str, object] = {
    "random": generate_random_dataset,
    "sorted": generate_sorted_dataset,
    "reverse_sorted": generate_reverse_sorted_dataset,
    "partially_sorted": generate_partially_sorted_dataset,
}

DATASET_TYPES: list[str] = list(_GENERATORS.keys())
"""Valid dataset type strings accepted by :func:`generate_dataset_by_type`."""

DATASET_TYPE_LABELS: dict[str, str] = {
    "random": "Random - Unsorted",
    "sorted": "Sorted",
    "reverse_sorted": "Reverse Sorted",
    "partially_sorted": "Partially Sorted",
}
"""User-facing labels for dataset type values."""


# --------------------------------------------------------------- generate_dataset_by_type()
def generate_dataset_by_type(
    dataset_type: str,
    size: int,
    seed: int | None = None,
) -> list[int]:
    """Generate a dataset of the given *dataset_type* and *size*.

    Args:
        dataset_type: One of ``"random"``, ``"sorted"``,
            ``"reverse_sorted"``, or ``"partially_sorted"``.
        size: Number of elements.
        seed: Optional random seed.

    Returns:
        A list of integers matching the requested scenario.

    Raises:
        ValueError: If *dataset_type* is not recognized.
    """
    generator = _GENERATORS.get(dataset_type)
    if generator is None:
        raise ValueError(
            f"Unknown dataset type {dataset_type!r}. "
            f"Choose from {DATASET_TYPES}."
        )
    return generator(size, seed=seed)  # type: ignore[operator]
# --------------------------------------------------------------- end generate_dataset_by_type()


# --------------------------------------------------------------- format_dataset_type_label()
def format_dataset_type_label(dataset_type: str) -> str:
    """Return the user-facing label for a dataset type value.

    Args:
        dataset_type: Internal dataset type key such as ``"random"``.

    Returns:
        A friendly label for UI and report display.
    """
    return DATASET_TYPE_LABELS.get(
        dataset_type,
        dataset_type.replace("_", " ").title(),
    )
# --------------------------------------------------------------- end format_dataset_type_label()

# ========================================================================
# Preview & Validation
# ========================================================================

# --------------------------------------------------------------- preview_dataset()
def preview_dataset(data: list[int], count: int = 15) -> str:
    """Return a short string showing the first and last elements of *data*.

    Args:
        data: The list to preview.
        count: Maximum number of leading/trailing elements to show
            (default 15 total: first 10 + last 5).

    Returns:
        A compact string representation of *data*.
    """
    if not data:
        return "[]"
    if len(data) <= count:
        return str(data)
    head = ", ".join(str(v) for v in data[:10])
    tail = ", ".join(str(v) for v in data[-5:])
    return f"[{head}, ..., {tail}]  ({len(data)} items)"
# --------------------------------------------------------------- end preview_dataset()


# --------------------------------------------------------------- validate_dataset()
def validate_dataset(data: list[int]) -> tuple[bool, str]:
    """Validate that *data* is a non-empty list of integers.

    Args:
        data: The dataset to validate.

    Returns:
        A ``(is_valid, message)`` tuple. ``is_valid`` is True when the
        dataset passes all checks; *message* describes the first failure
        or a success confirmation.
    """
    if not data:
        return False, "Dataset is empty."
    if not all(isinstance(v, int) for v in data):
        return False, "Dataset contains non-integer values."
    return True, f"Dataset OK — {len(data)} integer(s)."
# --------------------------------------------------------------- end validate_dataset()


# --------------------------------------------------------------- is_sorted_non_decreasing()
def is_sorted_non_decreasing(data: list[int]) -> bool:
    """Return True if *data* is sorted in non-decreasing order.

    Args:
        data: The list to check.

    Returns:
        True if every adjacent pair satisfies ``data[i] <= data[i+1]``.
    """
    return all(data[i] <= data[i + 1] for i in range(len(data) - 1))
# --------------------------------------------------------------- end is_sorted_non_decreasing()

# __________________________________________________________________________
# End of File
#
