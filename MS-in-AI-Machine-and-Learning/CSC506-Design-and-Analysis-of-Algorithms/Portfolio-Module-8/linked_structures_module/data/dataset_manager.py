# -------------------------------------------------------------------------
# File: dataset_manager.py
# Author: Alexander Ricciardi
# Date: 2026-04-06
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Dataset generation manager, parsing, validation, and preview helpers used by the
# Algorithm and Data Structure Comparison Tool. Provides three deterministic generators (sequential,
# random with optional seed, reverse), a manual comma-separated parser, a
# dispatcher mapping a dataset type string to a generator, a compact preview
# string for the UI, and an integer-only validator.
# -------------------------------------------------------------------------

# --- Functions ---
# - generate_sequential_dataset()  — ascending integers from start
# - generate_random_dataset()      — random integers in [low, high]
# - generate_reverse_dataset()     — descending integers
# - parse_manual_input()           — parse comma-separated integers
# - generate_dataset_by_type()     — dispatcher mapping type string to generator
# - preview_dataset()              — short string for UI display
# - validate_dataset()             — non-empty + all-integers check
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset generation, parsing, and validation for the Algorithm and Data Structure Comparison Tool."""

# ________________
# Imports
#

from __future__ import annotations

import random

# __________________________________________________________________________
# Constants
#

# ========================================================================
# Defaults
# ========================================================================

DEFAULT_DATASET_SIZE: int = 25
"""Default user-generated dataset size for the Dataset Builder tab."""

DEFAULT_BENCHMARK_SIZES: list[int] = [1_000, 5_000, 10_000, 50_000]
"""Required benchmark sizes for the assignment."""

DEFAULT_RANDOM_SEED: int = 506
"""Default seed used by the random generator for reproducibility."""

DATASET_TYPES: list[str] = ["sequential", "random", "reverse", "manual"]
"""Valid dataset type strings recognized by the UI."""

# __________________________________________________________________________
# Dataset Generators
#

# ========================================================================
# Generators
# ========================================================================

# --------------------------------------------------------------- generate_sequential_dataset()
def generate_sequential_dataset(
    size: int = DEFAULT_DATASET_SIZE,
    start: int = 1,
) -> list[int]:
    """Generate an ascending sequential dataset.

    Produces ``[start, start+1, ..., start+size-1]``. Useful for benchmarks
    that need a deterministic, predictable input so the workload's expected
    return values can be verified.

    Args:
        size: Number of elements to generate.
        start: First value in the sequence.

    Returns:
        A list of *size* ascending integers starting at *start*.
    """
    # SAFETY CHECK: clamp negative or zero sizes to an empty list
    if size <= 0:
        return []
    return list(range(start, start + size))
# --------------------------------------------------------------- end generate_sequential_dataset()


# --------------------------------------------------------------- generate_random_dataset()
def generate_random_dataset(
    size: int = DEFAULT_DATASET_SIZE,
    low: int = 1,
    high: int = 1_000_000,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Generate a random dataset of integers in ``[low, high]``.

    Duplicates are allowed, so the function works for any size without
    requiring the value range to be larger than the list. The optional
    ``seed`` is fed to a private :class:`random.Random` instance so that
    seeded calls are reproducible.

    Args:
        size: Number of elements to generate.
        low: Minimum value, inclusive.
        high: Maximum value, inclusive.
        seed: Optional random seed for reproducibility.

    Returns:
        A list of *size* random integers in arbitrary order.
    """
    if size <= 0:
        return []
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(size)]
# --------------------------------------------------------------- end generate_random_dataset()


# --------------------------------------------------------------- generate_reverse_dataset()
def generate_reverse_dataset(
    size: int = DEFAULT_DATASET_SIZE,
    start: int = 1,
) -> list[int]:
    """Generate a strictly descending dataset.

    Produces a list whose first element is ``start + size - 1`` and whose
    last element is ``start``. The values are spaced by 1.

    Args:
        size: Number of elements to generate.
        start: Minimum value of the sequence (used as the last element).

    Returns:
        A list of *size* descending integers.
    """
    if size <= 0:
        return []
    return list(range(start + size - 1, start - 1, -1))
# --------------------------------------------------------------- end generate_reverse_dataset()


# --------------------------------------------------------------- parse_manual_input()
def parse_manual_input(raw: str) -> list[int]:
    """Parse a comma-separated string of integers.

    Whitespace around tokens is stripped, negative values are accepted, and
    any non-integer token raises ``ValueError``. Empty input is rejected
    explicitly so the UI can show a clean message.

    Args:
        raw: User-provided text from the manual input field.

    Returns:
        A list of integers parsed from *raw*.

    Raises:
        ValueError: If *raw* is empty or contains a non-integer token.
    """
    # VALIDATION: reject empty / whitespace-only input up front
    if raw is None or not raw.strip():
        raise ValueError("Manual input cannot be empty")

    # Step 1: split on commas and strip whitespace from each token
    tokens = [token.strip() for token in raw.split(",")]

    # Step 2: drop trailing empty tokens that come from "1, 2, 3,"
    tokens = [token for token in tokens if token != ""]

    if not tokens:
        raise ValueError("Manual input cannot be empty")

    # Step 3: convert each token, raising on the first invalid one
    parsed: list[int] = []
    # Iterate through the tokens and convert them to integers
    for token in tokens:
        try:
            parsed.append(int(token))
        except ValueError as exc:
            raise ValueError(
                f"Invalid integer token: {token!r}"
            ) from exc

    return parsed
# --------------------------------------------------------------- end parse_manual_input()


# --------------------------------------------------------------- generate_dataset_by_type()
def generate_dataset_by_type(
    dataset_type: str,
    size: int = DEFAULT_DATASET_SIZE,
    seed: int | None = DEFAULT_RANDOM_SEED,
) -> list[int]:
    """Dispatch to the matching dataset generator.

    Manual input is intentionally not handled here — it flows through
    :func:`parse_manual_input` directly from the UI because it cannot be
    generated from a size alone.

    Args:
        dataset_type: One of ``"sequential"``, ``"random"``, or ``"reverse"``.
        size: Number of elements to generate.
        seed: Random seed (only used for the random generator).

    Returns:
        A list of integers matching the requested dataset type.

    Raises:
        ValueError: If *dataset_type* is not recognized.
    """
    # Dispatch to the matching dataset generator
    if dataset_type == "sequential":
        return generate_sequential_dataset(size)
    if dataset_type == "random":
        return generate_random_dataset(size, seed=seed)
    if dataset_type == "reverse":
        return generate_reverse_dataset(size)
    raise ValueError(
        f"Unknown dataset type {dataset_type!r}. "
        f"Choose from {['sequential', 'random', 'reverse']}."
    )
# --------------------------------------------------------------- end generate_dataset_by_type()

# __________________________________________________________________________
# Preview & Validation
#

# ========================================================================
# Preview
# ========================================================================

# --------------------------------------------------------------- preview_dataset()
def preview_dataset(data: list[int], count: int = 15) -> str:
    """Return a compact string preview of *data* for UI display.

    For lists shorter than *count* the full list is shown. For longer lists
    the first 10 and last 5 elements are shown together with the total
    length.

    Args:
        data: The list to preview.
        count: Total number of elements to show before switching to the
            head/tail summary form (default 15).

    Returns:
        A short string representation of *data*.
    """
    # Return the full list if it is shorter than the count
    if not data:
        return "[]"
    if len(data) <= count:
        return str(data)
    # Return the head and tail of the list if it is longer than the count
    head = ", ".join(str(v) for v in data[:10])
    tail = ", ".join(str(v) for v in data[-5:])
    return f"[{head}, ..., {tail}]  ({len(data)} items)"
# --------------------------------------------------------------- end preview_dataset()


# ========================================================================
# Validation
# ========================================================================

# --------------------------------------------------------------- validate_dataset()
def validate_dataset(data: list[int]) -> tuple[bool, str]:
    """Validate that *data* is a non-empty list of integers.

    Booleans are rejected as well, since ``bool`` is a subclass of ``int``
    in Python and we want strictly integer values for the playground.

    Args:
        data: The dataset to validate.

    Returns:
        A ``(is_valid, message)`` tuple. *is_valid* is True only when the
        dataset passes every check; *message* describes the first failure
        or a success confirmation.
    """
    # Check if the dataset is empty
    if data is None or len(data) == 0:
        return False, "Dataset is empty."
    # Check if the dataset contains non-integer values
    for value in data:
        # SAFETY CHECK: bool is a subclass of int — exclude it explicitly
        if isinstance(value, bool) or not isinstance(value, int):
            return False, "Dataset contains non-integer values."
    return True, f"Dataset OK — {len(data)} integer(s)." 
# --------------------------------------------------------------- end validate_dataset()

# __________________________________________________________________________
# End of File
#
