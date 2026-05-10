# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-05-05
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Portfolio Module 8 search comparison package."""

from __future__ import annotations

from search_comparison_module.algorithms import binary_search, linear_search
from search_comparison_module.models import SearchResult

__all__ = [
    "SearchResult",
    "binary_search",
    "linear_search",
]
