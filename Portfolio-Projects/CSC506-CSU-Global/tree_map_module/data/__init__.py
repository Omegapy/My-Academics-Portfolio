# -------------------------------------------------------------------------
# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-04-21
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# Module Functionality
# Package exports for dataset generation and validation helpers.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Dataset exports for Portfolio Milestone Module 6."""

from __future__ import annotations

from tree_map_module.data.dataset_manager import (
    BENCHMARK_SIZES,
    DATASET_TYPES,
    DEFAULT_DATASET_SIZE,
    DEFAULT_RANDOM_SEED,
    INSERTION_PATTERNS,
    build_balanced_insertion_order,
    generate_keys,
    generate_map_items,
    generate_search_queries,
    parse_manual_keys,
    preview_dataset,
    validate_dataset,
    validate_unique_keys,
)

__all__ = [
    "BENCHMARK_SIZES",
    "DATASET_TYPES",
    "DEFAULT_DATASET_SIZE",
    "DEFAULT_RANDOM_SEED",
    "INSERTION_PATTERNS",
    "build_balanced_insertion_order",
    "generate_keys",
    "generate_map_items",
    "generate_search_queries",
    "parse_manual_keys",
    "preview_dataset",
    "validate_dataset",
    "validate_unique_keys",
]
