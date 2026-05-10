# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-05-04
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Public API for the Module 8 Bubble Sort and Quickselect package."""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from bubble_quickselect_module.algorithms import bubble_sort, quickselect
from bubble_quickselect_module.models import QuickSelectResult, SortResult
from bubble_quickselect_module.set_operations import CourseSet, SetOperationResult

__all__: list[str] = [
    "bubble_sort",
    "quickselect",
    "SortResult",
    "QuickSelectResult",
    "CourseSet",
    "SetOperationResult",
]

# __________________________________________________________________________
# End of File
#
