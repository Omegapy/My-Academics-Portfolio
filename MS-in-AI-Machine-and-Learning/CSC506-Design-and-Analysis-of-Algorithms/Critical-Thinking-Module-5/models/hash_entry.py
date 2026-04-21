# -------------------------------------------------------------------------
# File: hash_entry.py
# 
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# HashEntry dataclass representing one key-value pair stored in the
# hash table.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for hash table key-value entries.

Each HashEntry stores one key-value pair inside a hash table bucket.
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from dataclasses import dataclass

# ______________________________________________________________________________
# Class Definitions – Data Classes
# ==============================================================================
# TYPES AND DATA STRUCTURES
# ==============================================================================
# Contains the bucket-entry dataclass used by the HashTable implementation.
# - Class: HashEntry (Dataclass) - One key-value pair stored in a bucket chain
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class HashEntry
@dataclass
class HashEntry:
    """One key-value pair stored in a hash table bucket.

    Attributes:
        key: The lookup key (string).
        value: The stored payload (any object).

    Logic:
        This dataclass is a minimal data container for hash table bucket chains.
        1. Accept a string key and an arbitrary value via the generated __init__.
        2. Provide a compact __repr__ that surfaces both fields for UI/debugging.
        3. Stay intentionally lean — collision handling and ordering live in HashTable.
    """

    key: str
    value: object

    # --------------------------------------------------------------- __repr__()
    def __repr__(self) -> str:
        """Return a compact display string for UI and debugging.

        Logic:
            This method renders the entry in a format suitable for tables/logs.
            1. Format the key using repr() to preserve quoting for strings.
            2. Format the value using repr() so all payload types display safely.
            3. Return the combined "HashEntry(key, value)" string.
        """
        return f"HashEntry({self.key!r}, {self.value!r})"
    # ---------------------------------------------------------------

# ------------------------------------------------------------------------- end class HashEntry

# ==============================================================================
# End of File
# ==============================================================================
