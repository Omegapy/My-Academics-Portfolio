# -------------------------------------------------------------------------
# File: linear_search.py
# Author: Alexander Ricciardi
# Date: 2026-04-14
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Linear search baseline for the hash-table-vs-linear-search benchmark.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Linear search over a list of key-value pairs.

Provides the O(n) baseline comparison for the hash table search benchmark.
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# SEARCH ALGORITHM - LINEAR BASELINE
# ==============================================================================
# Provides the O(n) baseline used by the Benchmark Lab to contrast the hash
# table's average-case O(1) search against an unsorted-list scan.
#
# COMPLEXITY OVERVIEW:
#   - Worst case  : O(n) — target absent or last element
#   - Average case: O(n/2) → O(n)
#   - Best case   : O(1)  — target is the first element
#
# - Function: linear_search_by_key() - Sequential scan returning matching value
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- linear_search_by_key()
def linear_search_by_key(
    records: list[tuple[str, object]],
    key: str,
) -> object | None:
    """Scan *records* left-to-right and return the value matching *key*.

    Logic:
        This function performs an unsorted-list linear search baseline.
        1. Iterate the records list in insertion order.
        2. Compare each tuple's key against the target key.
        3. Return the value on the first exact match (early exit).
        4. Return None if the loop exhausts the list without a match.
    """
    # MAIN ITERATION LOOP: scan every (key, value) pair until first match
    for k, v in records:
        # Step 1: Check convergence criteria
        # Converged if: stored key equals the target key
        if k == key:
            return v
    # If we exit the loop, the key is absent from the records list
    # Return None to signal "not found" (matches HashTable.search semantics)
    return None
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
