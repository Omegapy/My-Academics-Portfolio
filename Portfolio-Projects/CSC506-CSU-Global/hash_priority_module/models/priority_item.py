# -------------------------------------------------------------------------
# File: priority_item.py
# 
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
# ---------------------------------------------

# --- Module Functionality ---
# PriorityItem dataclass representing one item in the binary heap
# priority queue, with a sequence number for deterministic tie-breaking.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for priority queue items.

Each PriorityItem holds a label, numeric priority, optional payload,
and a sequence number for stable ordering when priorities are equal.
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
# Contains the per-item dataclass used by the BinaryHeapPriorityQueue.
# - Class: PriorityItem (Dataclass) - Heap element with deterministic ordering
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class PriorityItem
@dataclass
class PriorityItem:
    """One item stored in the binary heap priority queue.

    Attributes:
        label: Human-readable identifier (e.g., "task-001").
        priority: Numeric priority value.
        payload: Optional description or value.
        sequence_number: Tie-breaker to preserve insertion order for equal priorities.

    Logic:
        This dataclass carries the data the heap orders on plus a stable tie-breaker.
        1. Store identifying label and arbitrary payload for UI display.
        2. Order primarily by numeric priority (min-heap by default).
        3. Break ties with sequence_number to keep insertion order deterministic.
    """

    label: str
    priority: int
    payload: str
    sequence_number: int

    # --------------------------------------------------------------- __lt__()
    def __lt__(self, other: PriorityItem) -> bool:
        """Compare by (priority, sequence_number) for deterministic heap ordering.

        Logic:
            This comparator powers the binary heap's sift operations.
            1. Compare priorities first; lower priority wins (min-heap behaviour).
            2. If priorities are equal, fall back to the sequence_number tie-breaker.
            3. Return the boolean result the heap uses to decide swaps.
        """
        # Step 1: primary key comparison on priority
        if self.priority != other.priority:
            return self.priority < other.priority
        # Step 2: stable tie-breaker preserves insertion order
        return self.sequence_number < other.sequence_number
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __eq__()
    def __eq__(self, other: object) -> bool:
        """Check equality by (priority, sequence_number).

        Logic:
            This equality check mirrors __lt__ so heap invariants stay consistent.
            1. VALIDATION: reject non-PriorityItem comparisons via NotImplemented.
            2. Compare the (priority, sequence_number) tuple for exact equality.
            3. Return the boolean equality result.
        """
        # VALIDATION: only compare against other PriorityItem instances
        if not isinstance(other, PriorityItem):
            return NotImplemented
        return (self.priority, self.sequence_number) == (
            other.priority,
            other.sequence_number,
        )
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __repr__()
    def __repr__(self) -> str:
        """Return a compact display string for UI and debugging.

        Logic:
            This method renders the item in a UI/log-friendly format.
            1. Format the label with repr() to preserve quoting.
            2. Include priority and abbreviated sequence number.
            3. Return the combined single-line representation.
        """
        return (
            f"PriorityItem({self.label!r}, priority={self.priority}, "
            f"seq={self.sequence_number})"
        )
    # ---------------------------------------------------------------

# ------------------------------------------------------------------------- end class PriorityItem

# ==============================================================================
# End of File
# ==============================================================================
