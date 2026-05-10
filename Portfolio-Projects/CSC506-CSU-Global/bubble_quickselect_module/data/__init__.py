# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-05-04
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset helper exports for the Bubble Sort and Quickselect package."""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from bubble_quickselect_module.data.dataset_manager import (
    DATASET_TYPES,
    DEFAULT_DATASET_SIZE,
    DEFAULT_RANDOM_SEED,
    generate_comparable_keys,
    generate_dataset_by_type,
    generate_duplicate_heavy_dataset,
    generate_graph_preset,
    generate_key_value_records,
    generate_partially_sorted_dataset,
    generate_priority_records,
    generate_random_dataset,
    generate_reverse_sorted_dataset,
    generate_sorted_dataset,
    parse_manual_input,
    preview_dataset,
    preview_edges,
    preview_records,
    validate_dataset,
)

__all__: list[str] = [
    "DEFAULT_DATASET_SIZE",
    "DEFAULT_RANDOM_SEED",
    "DATASET_TYPES",
    "generate_random_dataset",
    "generate_sorted_dataset",
    "generate_reverse_sorted_dataset",
    "generate_duplicate_heavy_dataset",
    "generate_partially_sorted_dataset",
    "generate_comparable_keys",
    "generate_key_value_records",
    "generate_priority_records",
    "generate_graph_preset",
    "parse_manual_input",
    "generate_dataset_by_type",
    "validate_dataset",
    "preview_dataset",
    "preview_records",
    "preview_edges",
]

# __________________________________________________________________________
# End of File
#
