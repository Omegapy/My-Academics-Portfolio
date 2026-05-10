# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-05-05
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset generation, parsing, and validation utilities."""

from __future__ import annotations

from search_comparison_module.data.dataset_manager import (
    generate_random_dataset,
    generate_sample_dataset,
    parse_manual_input,
    preview,
    remove_duplicates,
    sorted_copy,
    validate_dataset,
)

__all__ = [
    "generate_random_dataset",
    "generate_sample_dataset",
    "parse_manual_input",
    "preview",
    "remove_duplicates",
    "sorted_copy",
    "validate_dataset",
]
