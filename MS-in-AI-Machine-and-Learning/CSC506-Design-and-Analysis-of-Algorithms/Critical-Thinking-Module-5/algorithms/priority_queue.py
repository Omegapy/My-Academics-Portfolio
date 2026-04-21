# -------------------------------------------------------------------------
# File: priority_queue.py
# Author: Alexander Ricciardi
# Date: 2026-04-14
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# BinaryHeapPriorityQueue backed by an array-based binary heap.
# Supports max-heap and min-heap modes, insert, peek, extract-top,
# arbitrary search by label (O(n)), and arbitrary delete by label.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Binary-heap-backed priority queue.

Stores PriorityItem instances in a Python list.  Supports both
``"max"`` and ``"min"`` modes with O(log n) insert/extract and O(n)
arbitrary search/delete.
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from models.priority_item import PriorityItem

# ______________________________________________________________________________
# Class Definitions - Regular Classes
# ==============================================================================
# CLASS DEFINITIONS
# ==============================================================================
#
# BINARY HEAP OVERVIEW:
#   The queue stores items in a Python list using the standard array-based
#   binary heap layout. For an item at index i:
#       parent(i) = (i - 1) // 2
#       left(i)   = 2*i + 1
#       right(i)  = 2*i + 2
#
# HEAP INVARIANT:
#   Every parent has higher effective priority than its children, where
#   "higher" depends on mode:
#     - mode="max" → larger priority value wins
#     - mode="min" → smaller priority value wins
#   Ties are broken by sequence_number (lower wins) to keep insertion order
#   stable across both modes.
#
# COMPLEXITY SUMMARY:
#   - insert / extract_top : O(log n) — one sift up or sift down
#   - peek                 : O(1)     — top is always at index 0
#   - search / delete      : O(n)     — linear scan to locate by label,
#                                       then O(log n) reheap on delete
#
# - Class: BinaryHeapPriorityQueue - Array-backed min/max binary heap
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class BinaryHeapPriorityQueue
class BinaryHeapPriorityQueue:
    """Priority queue backed by a binary heap.

    Logic:
        This class is a regular class (not a dataclass) because __init__ validates
        the mode argument and owns mutable internal heap state across operations.
        1. Validate the mode and store it for use by the priority comparator.
        2. Maintain the heap invariant via _sift_up / _sift_down on every mutation.
        3. Expose insert/peek/extract_top plus O(n) search and delete by label.
    """

    # --------------------------------------------------------------- __init__()
    def __init__(self, mode: str = "max") -> None:
        """Initialize an empty priority queue in max- or min-heap mode.

        Logic:
            This initializer validates the mode and prepares an empty heap list.
            1. VALIDATION: reject any mode other than "max" or "min".
            2. Store the validated mode for use by the comparator.
            3. Allocate an empty list to back the binary heap.
        """
        # VALIDATION: only "max" and "min" are supported heap modes
        if mode not in ("max", "min"):
            raise ValueError(f"mode must be 'max' or 'min', got {mode!r}")
        self._mode: str = mode
        self._heap: list[PriorityItem] = []
    # ---------------------------------------------------------------

    # ________________________________________________
    #  Utilities
    #
    # --------------------------------------------------------------- _parent()
    @staticmethod
    def _parent(index: int) -> int:
        """Return the parent index of *index*.

        Logic:
            This helper computes the standard array-heap parent index.
            1. Apply the formula (index - 1) // 2.
            2. Return the resulting parent index.
        """
        return (index - 1) // 2
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _left()
    @staticmethod
    def _left(index: int) -> int:
        """Return the left-child index of *index*.

        Logic:
            This helper computes the standard array-heap left-child index.
            1. Apply the formula 2*index + 1.
            2. Return the resulting left-child index.
        """
        return 2 * index + 1
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _right()
    @staticmethod
    def _right(index: int) -> int:
        """Return the right-child index of *index*.

        Logic:
            This helper computes the standard array-heap right-child index.
            1. Apply the formula 2*index + 2.
            2. Return the resulting right-child index.
        """
        return 2 * index + 2
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _has_higher_priority()
    def _has_higher_priority(self, a: PriorityItem, b: PriorityItem) -> bool:
        """Return True if *a* should be closer to the root than *b*.

        In max-heap mode, higher priority wins.
        In min-heap mode, lower priority wins.
        Ties are broken by sequence_number (lower wins in both modes)
        to preserve insertion order for equal priorities.

        Logic:
            This comparator centralizes mode-aware ordering for the sift routines.
            1. DISPATCH: branch on self._mode to pick the correct ordering.
            2. Compare priorities first (max wins for "max", min wins for "min").
            3. On equal priority, fall back to sequence_number (lower wins).
        """
        # DISPATCH: max-heap branch
        if self._mode == "max":
            if a.priority != b.priority:
                return a.priority > b.priority
            return a.sequence_number < b.sequence_number
        # DISPATCH: min-heap branch (mode validated to be "min" here)
        if a.priority != b.priority:
            return a.priority < b.priority
        return a.sequence_number < b.sequence_number
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _swap()
    def _swap(self, i: int, j: int) -> None:
        """Swap elements at indices *i* and *j*.

        Logic:
            This helper performs an in-place swap inside the heap list.
            1. Use Python tuple-assignment to swap _heap[i] and _heap[j].
        """
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _sift_up()
    def _sift_up(self, index: int) -> None:
        """Move the item at *index* upward until heap order is restored.

        Logic:
            This helper restores the heap invariant after an append at the bottom.
            1. Compute the parent index for the current position.
            2. If the current item out-prioritizes the parent, swap and continue.
            3. Stop when the root is reached or the parent already wins.
        """
        # MAIN ITERATION LOOP: bubble the new item up toward the root
        while index > 0:
            # Step 1: compute the parent index
            parent = self._parent(index)
            # Step 2: compare and swap when the child wins the priority test
            if self._has_higher_priority(self._heap[index], self._heap[parent]):
                self._swap(index, parent)
                index = parent
            else:
                # Step 3: heap invariant restored — stop sifting
                break
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _sift_down()
    def _sift_down(self, index: int) -> None:
        """Move the item at *index* downward until heap order is restored.

        Logic:
            This helper restores the heap invariant after a root replacement.
            1. Pick the better of (current, left, right) using the comparator.
            2. Swap with that child if it out-prioritizes the current node.
            3. Stop when neither child outranks the current position.
        """
        size = len(self._heap)
        # MAIN ITERATION LOOP: push the (possibly out-of-place) item down toward leaves
        while True:
            best = index
            left = self._left(index)
            right = self._right(index)

            # Step 1: see if left child should outrank the current best
            if left < size and self._has_higher_priority(self._heap[left], self._heap[best]):
                best = left
            # Step 2: see if right child should outrank the current best
            if right < size and self._has_higher_priority(self._heap[right], self._heap[best]):
                best = right

            # Step 3: Check convergence criteria
            # Converged if: neither child outranks the current node
            if best == index:
                break
            # Step 4: swap with the winning child and continue from its index
            self._swap(index, best)
            index = best
    # ---------------------------------------------------------------

    # ________________________________________________
    # Setters
    #
    # --------------------------------------------------------------- insert()
    def insert(self, item: PriorityItem) -> None:
        """Insert *item* into the priority queue.

        Time complexity: O(log n).

        Logic:
            This public mutation inserts at the bottom and restores heap order.
            1. Append the item at the next free slot (end of the list).
            2. Sift it up until the heap invariant is satisfied.
        """
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- extract_top()
    def extract_top(self) -> PriorityItem:
        """Remove and return the highest-priority item.

        Time complexity: O(log n).

        Logic:
            This public mutation removes the root and restores heap order.
            1. VALIDATION: raise IndexError when the heap is empty.
            2. Capture the root item to return at the end.
            3. Pop the last list element and overwrite the root, then sift down.
        """
        # VALIDATION: cannot extract from an empty heap
        if not self._heap:
            raise IndexError("extract from an empty priority queue")
        top = self._heap[0]
        last = self._heap.pop()
        # SAFETY CHECK: only restore root + sift down if heap is still non-empty
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return top
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- delete()
    def delete(self, label: str) -> PriorityItem | None:
        """Remove and return the item with the given *label*.

        Time complexity: O(n) to find + O(log n) to restore heap order.

        Logic:
            This method removes an arbitrary item identified by its label.
            1. Step 1 — locate the item's index via a linear scan.
            2. Step 2 — swap with the last element and pop to remove the slot.
            3. Step 3 — restore heap order at the swapped-in slot via sift up + down.
        """
        # Step 1: find the item's index
        target_idx: int | None = None
        # MAIN ITERATION LOOP: linear scan over the heap list to locate the label
        for i, item in enumerate(self._heap):
            if item.label == label:
                target_idx = i
                break
        if target_idx is None:
            return None

        removed = self._heap[target_idx]

        # Step 2: swap with last element and pop
        last_idx = len(self._heap) - 1
        # SAFETY CHECK: removing the last slot needs no reheaping
        if target_idx == last_idx:
            self._heap.pop()
            return removed

        self._swap(target_idx, last_idx)
        self._heap.pop()

        # Step 3: restore heap order — may need sift up or sift down
        if target_idx < len(self._heap):
            self._sift_up(target_idx)
            self._sift_down(target_idx)

        return removed
    # ---------------------------------------------------------------

    # ________________________________________________
    # Getters
    #
    # --------------------------------------------------------------- peek()
    def peek(self) -> PriorityItem:
        """Return the highest-priority item without removing it.

        Time complexity: O(1).

        Logic:
            This O(1) accessor returns the heap root without mutation.
            1. VALIDATION: raise IndexError when the heap is empty.
            2. Return _heap[0] which always holds the highest-priority item.
        """
        # VALIDATION: cannot peek into an empty heap
        if not self._heap:
            raise IndexError("peek from an empty priority queue")
        return self._heap[0]
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- search()
    def search(self, label: str) -> PriorityItem | None:
        """Find and return the item with the given *label*.

        Time complexity: O(n) — the heap property does not support
        efficient label-based lookup.

        Logic:
            This method exposes a linear-scan label lookup into the heap.
            1. Walk the heap list in order.
            2. Return the first item whose label matches.
            3. Return None if the loop finishes without a match.
        """
        # MAIN ITERATION LOOP: scan heap entries until label match
        for item in self._heap:
            if item.label == label:
                return item
        return None
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- to_list()
    def to_list(self) -> list[PriorityItem]:
        """Return a copy of the internal heap array.

        Logic:
            This accessor returns a shallow copy to protect internal state.
            1. Slice _heap to produce a fresh list with the same items.
            2. Return the copy so callers can iterate without mutating the heap.
        """
        return self._heap[:]
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- is_empty()
    def is_empty(self) -> bool:
        """Return True if the queue contains no items.

        Logic:
            This predicate exposes a simple emptiness check.
            1. Compare the heap length to zero.
            2. Return the boolean result.
        """
        return len(self._heap) == 0
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- is_valid_heap()
    def is_valid_heap(self) -> bool:
        """Verify that the heap property holds for all parent-child pairs.

        Logic:
            This validator confirms the heap invariant across the whole array.
            1. Walk every parent index in the heap.
            2. Reject when a left or right child outranks its parent under the comparator.
            3. Return True only when no violation is found.
        """
        # MAIN ITERATION LOOP: check the heap invariant at every parent index
        for i in range(len(self._heap)):
            left = self._left(i)
            right = self._right(i)
            # SAFETY CHECK: child must out-rank parent under comparator => violation
            if left < len(self._heap):
                if self._has_higher_priority(self._heap[left], self._heap[i]):
                    return False
            if right < len(self._heap):
                if self._has_higher_priority(self._heap[right], self._heap[i]):
                    return False
        return True
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- mode()
    @property
    def mode(self) -> str:
        """Return the heap mode (``"max"`` or ``"min"``).

        Logic:
            This property exposes the validated mode chosen at construction.
            1. Return the cached _mode attribute.
        """
        return self._mode
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of items in the queue.

        Logic:
            This dunder mirrors len() against the heap list.
            1. Return len(self._heap).
        """
        return len(self._heap)
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __repr__()
    def __repr__(self) -> str:
        """Return a compact summary string.

        Logic:
            This dunder produces a one-line UI/log summary.
            1. Format mode and current size into a BinaryHeapPriorityQueue(...) string.
            2. Return the formatted result.
        """
        return f"BinaryHeapPriorityQueue(mode={self._mode!r}, size={len(self._heap)})"
    # ---------------------------------------------------------------

# ------------------------------------------------------------------------- end class BinaryHeapPriorityQueue

# ==============================================================================
# End of File
# ==============================================================================
