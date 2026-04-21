# -------------------------------------------------------------------------
# File: hash_table_stats.py
# 
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# HashTableStats dataclass capturing the current state of the hash table
# for UI display and analysis reporting.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for hash table statistics.

HashTableStats provides a snapshot of hash table health including
load factor, collision counts, and bucket distribution.
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
# Snapshot dataclass produced by HashTable.get_stats() and consumed by the
# Streamlit UI plus the written-analysis pipeline.
# - Class: HashTableStats (Dataclass) - Read-only snapshot of bucket health
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class HashTableStats
@dataclass
class HashTableStats:
    """Snapshot of hash table statistics.

    Attributes:
        size: Number of stored entries.
        capacity: Number of buckets.
        load_factor: Ratio of size to capacity.
        used_buckets: Buckets containing at least one entry.
        empty_buckets: Buckets with no entries.
        collision_buckets: Buckets with more than one entry.
        longest_bucket_length: Length of the largest bucket chain.
        total_collisions: Count of insertions that landed in a non-empty bucket.

    Logic:
        This dataclass is a flat read-only summary of bucket-level health metrics.
        1. Carry counts and ratios computed by HashTable.get_stats().
        2. Stay decoupled from HashTable so UI/reporting code can pass it freely.
        3. Provide all fields required by the Streamlit dashboard and CSV exports.
    """

    size: int
    capacity: int
    load_factor: float
    used_buckets: int
    empty_buckets: int
    collision_buckets: int
    longest_bucket_length: int
    total_collisions: int

# ------------------------------------------------------------------------- end class HashTableStats

# ==============================================================================
# End of File
# ==============================================================================
