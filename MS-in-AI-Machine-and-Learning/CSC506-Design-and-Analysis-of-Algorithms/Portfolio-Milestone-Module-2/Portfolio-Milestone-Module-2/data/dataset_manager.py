# -------------------------------------------------------------------------
# File: dataset_manager.py
# Author: Alexander Ricciardi
# Date: 2026-03-29
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Dataset generation, parsing, sorting, preview, and validation
# used by the Streamlit UI and the benchmarking module.
# -------------------------------------------------------------------------

# --- Functions ---
# - generate_sample_dataset() — predictable small dataset
# - generate_random_dataset() — random unique integers
# - parse_manual_input()      — comma-separated string → list[int]
# - sorted_copy()             — non-mutating sort
# - preview()                 — short string representation
# - validate_dataset()        — non-empty + all-ints check
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset generation, parsing, and validation helpers.

All functions operate on ``list[int]`` and never mutate the input list.
"""

# ________________
# Imports
#

from __future__ import annotations

import random

# __________________________________________________________________________
# Dataset Functions
#

# ========================================================================
# Generation
# ========================================================================

# --------------------------------------------------------------- generate_sample_dataset()
def generate_sample_dataset(size: int = 20) -> list[int]:
    """Return a predictable sample dataset of *size* integers.

    The values are drawn from a fixed seed so results are reproducible
    across runs.

    Args:
        size: Number of elements to generate (default 20).

    Returns:
        A list of unique integers in arbitrary order.
    """
    return random.sample(range(1, max(size * 10, 100)), size)
# --------------------------------------------------------------- end generate_sample_dataset()

# --------------------------------------------------------------- generate_random_dataset()
def generate_random_dataset(
    size: int,
    low: int = 1,
    high: int = 100_000,
) -> list[int]:
    """Generate a list of *size* unique random integers in [low, high].

    Args:
        size: Number of elements to generate.
        low: Minimum value (inclusive).
        high: Maximum value (inclusive).

    Returns:
        A list of unique integers in arbitrary order.

    Raises:
        ValueError: If the requested size exceeds the available range.
    """
    if size > (high - low + 1):
        raise ValueError(
            f"Cannot sample {size} unique values from range [{low}, {high}]."
        )
    return random.sample(range(low, high + 1), size)
# --------------------------------------------------------------- end generate_random_dataset()

# ========================================================================
# Parsing & Sorting
# ========================================================================

# --------------------------------------------------------------- parse_manual_input()
def parse_manual_input(raw: str) -> list[int]:
    """Parse a comma-separated string of integers into a list.

    Args:
        raw: User-entered string (e.g., ``"5, 3, 8, 1, 9"``).

    Returns:
        A list of integers parsed from *raw*.

    Raises:
        ValueError: If any token cannot be converted to an integer.
    """
    tokens = [token.strip() for token in raw.split(",") if token.strip()]
    if not tokens:
        raise ValueError("Input is empty — please enter at least one integer.")
    return [int(token) for token in tokens]
# --------------------------------------------------------------- end parse_manual_input()

# --------------------------------------------------------------- sorted_copy()
def sorted_copy(data: list[int]) -> list[int]:
    """Return a sorted copy of *data* without mutating the original.

    Args:
        data: The list to sort.

    Returns:
        A new list with the same elements in ascending order.
    """
    return sorted(data)
# --------------------------------------------------------------- end sorted_copy()

# ========================================================================
# Duplicate Removal
# ========================================================================

# --------------------------------------------------------------- remove_duplicates()
def remove_duplicates(data: list[int]) -> tuple[list[int], list[int]]:
    """Remove duplicate values from *data*, keeping first occurrences.

    Args:
        data: The list to deduplicate.

    Returns:
        A tuple ``(unique, removed)`` where *unique* is the deduplicated
        list (original order preserved) and *removed* contains each value
        that was dropped (one entry per extra occurrence).
    """
    seen: set[int] = set()
    unique: list[int] = []
    removed: list[int] = []
    for value in data:
        if value in seen:
            removed.append(value)
        else:
            seen.add(value)
            unique.append(value)
    return unique, removed
# --------------------------------------------------------------- end remove_duplicates()

# ========================================================================
# Preview & Validation
# ========================================================================

# --------------------------------------------------------------- preview()
def preview(data: list[int], n: int = 10) -> str:
    """Return a short string showing the first *n* values of *data*.

    Args:
        data: The list to preview.
        n: Maximum number of leading elements to show (default 10).

    Returns:
        A string like ``"[3, 7, 1, 9, 12, ...]"`` if truncated,
        or the full list representation if len(data) <= n.
    """
    if len(data) <= n:
        return str(data)
    head = ", ".join(str(v) for v in data[:n])
    return f"[{head}, ...]"
# --------------------------------------------------------------- end preview()

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

# __________________________________________________________________________
# End of File
#
