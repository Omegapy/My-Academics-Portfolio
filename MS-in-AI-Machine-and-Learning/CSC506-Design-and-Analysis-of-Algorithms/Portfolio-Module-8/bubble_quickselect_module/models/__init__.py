# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-05-04
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Shared result models for the Bubble Sort and Quickselect package."""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from bubble_quickselect_module.models.quickselect_result import QuickSelectResult
from bubble_quickselect_module.models.sort_result import SortResult

__all__: list[str] = ["SortResult", "QuickSelectResult"]

# __________________________________________________________________________
# End of File
#
