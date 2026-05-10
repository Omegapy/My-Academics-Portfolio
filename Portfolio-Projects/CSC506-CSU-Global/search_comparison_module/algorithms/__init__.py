# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-05-05
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Search algorithm implementations for Portfolio Module 8."""

from __future__ import annotations

from search_comparison_module.algorithms.binary_search import binary_search
from search_comparison_module.algorithms.linear_search import linear_search

__all__ = [
    "binary_search",
    "linear_search",
]
