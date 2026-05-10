# -------------------------------------------------------------------------
# File: list_map.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-26
# File Path: Portfolio-Milestone-Module-6/data_structures/list_map.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# - Provide the simple list-backed mapping baseline for search comparisons.
# - Preserve insertion order while performing linear scans for lookup work.
# - Give TreeMap benchmarks a deliberately non-tree comparison structure.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Class Definitions - Regular Classes: ``ListMap`` implements the linear
#   search baseline used by the labs and benchmark pipeline.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: none beyond ``__future__`` annotations
# - Third-Party: none
# - Local Project Modules: none
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the benchmark engine and Streamlit map lab as the O(n) baseline.
# - Used only for comparison workloads, not for tree-shape analysis.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""List-backed map baseline for search comparisons.

It provides the intentionally simple linear-search mapping structure
used to contrast TreeMap behavior in the benchmark lab, validation demos, and
analysis summaries without introducing any tree-specific balancing behavior.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations


# __________________________________________________________________________
# Class Definitions - Regular Classes
# ========================================================================
# CLASS DEFINITIONS
# ========================================================================
# ``ListMap`` is intentionally simple: it preserves insertion order and uses
# linear scans so TreeMap has a fair baseline for search-performance analysis.
#
# ------------------------------------------------------------------------- class ListMap
class ListMap:
    """Simple list-backed map with linear-search lookup.

    Attributes:
        _items: Stored ``(key, value)`` pairs in insertion order.

    Logic:
        1. Preserve insertion order in a plain Python list.
        2. Use linear scans for put/get/delete operations.
        3. Provide the comparison baseline for TreeMap benchmarks.
    """

    # ________________________________________________
    # Construction
    #
    # --------------------------------------------------------------- __init__()
    def __init__(
        self,
        items: list[tuple[object, object]] | None = None,
    ) -> None:
        """Initialize the baseline map with optional items.

        Logic:
            This method prepares the list-backed storage and optionally preloads
            the provided items.
            1. Start with an empty insertion-order list.
            2. Reinsert any provided items through ``put()`` so duplicate-key
               handling matches the normal public path.
        """
        self._items: list[tuple[object, object]] = []
        # Step 1: preload items through ``put()`` so duplicate-key behavior
        # matches the normal public insertion path.
        if items:
            for key, value in items:
                self.put(key, value)
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Mutation Helpers
    #
    # --------------------------------------------------------------- put()
    def put(self, key: object, value: object) -> None:
        """Insert or update ``key`` with ``value``.

        Logic:
            This method preserves insertion order while replacing duplicates in
            place.
            1. Scan the stored pairs until a matching key is found.
            2. Replace the existing pair in place when the key already exists.
            3. Append a new pair when the key is not present.
        """
        # MAIN ITERATION LOOP: scan the insertion-order list for a key match.
        for index, (existing_key, _) in enumerate(self._items):
            if existing_key == key:
                self._items[index] = (key, value)
                return
        self._items.append((key, value))
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- get()
    def get(self, key: object, default: object | None = None) -> object | None:
        """Return the value for ``key`` or the provided default.

        Logic:
            This method performs a linear lookup over the stored key-value
            pairs.
            1. Scan each stored pair in insertion order.
            2. Return the paired value as soon as the requested key matches.
            3. Fall back to the caller-provided default when no key matches.
        """
        # MAIN ITERATION LOOP: search each stored pair until a matching key appears.
        for existing_key, value in self._items:
            if existing_key == key:
                return value
        # VALIDATION: fall back to the caller's default when the key is absent.
        return default
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- delete()
    def delete(self, key: object) -> bool:
        """Delete ``key`` when present and report whether removal occurred.

        Logic:
            This method removes at most one matching key-value pair from the
            insertion-order list.
            1. Scan the list until the first matching key is found.
            2. Delete that pair immediately when found.
            3. Return ``False`` when no matching key exists.
        """
        # MAIN ITERATION LOOP: find the first matching key so only one entry is removed.
        for index, (existing_key, _) in enumerate(self._items):
            if existing_key == key:
                del self._items[index]
                return True
        return False
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Read-Only Views
    #
    # --------------------------------------------------------------- contains_key()
    def contains_key(self, key: object) -> bool:
        """Return whether ``key`` exists in the map.

        Logic:
            This method checks membership without exposing stored values.
            1. Compare the requested key against each stored key.
            2. Return ``True`` when any stored key matches.
            3. Return ``False`` when the scan completes without a match.
        """
        return any(existing_key == key for existing_key, _ in self._items)
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- items()
    def items(self) -> list[tuple[object, object]]:
        """Return stored key-value pairs in insertion order.

        Logic:
            This method exposes a safe snapshot of the current list-backed map
            contents.
            1. Copy the internal insertion-order list.
            2. Return the copied list so callers do not mutate internal state.
        """
        return list(self._items)
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove every key-value pair from the map.

        Logic:
            This method resets the list-backed map to its empty state.
            1. Clear the internal insertion-order list.
            2. Leave the instance ready for fresh insertions.
        """
        self._items.clear()
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of stored items.

        Logic:
            This method reports the current map size from the backing list.
            1. Read the current length of the stored pair list.
            2. Return that count to the caller.
        """
        return len(self._items)
    # --------------------------------------------------------------- 

# ------------------------------------------------------------------------- end class ListMap

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------