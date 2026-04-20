# -------------------------------------------------------------------------
# File: queue.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Queue ADT. Items are stored in a Python list whose right
# end is the logical front and whose index 0 is the logical rear. enqueue
# uses list.insert(0, value) and dequeue uses list.pop(); the result is an
# intentionally O(n) enqueue and an O(1) dequeue, which matches the lecture
# point about how list.insert(0) shifts every existing element.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""FIFO Queue implemented on top of a Python list (course-aligned)."""

# ________________
# Imports 
#

from __future__ import annotations

# __________________________________________________________________________
# Queue Class
#

# ========================================================================
# Queue
# ========================================================================
# --------------------------------------------------------------- class Queue
class Queue:
    """FIFO Queue backed by a Python list with the course-aligned orientation.

    Internal storage:

    - logical front = right end of ``self._items``
    - logical rear  = index ``0`` of ``self._items``

    Enqueue is intentionally ``O(n)`` because ``insert(0)`` shifts every
    existing element to the right. Dequeue is ``O(1)``. The empty-state
    policy is to return ``None`` from ``dequeue`` and ``front`` rather than
    raising.
    """

    # --------------------------------------------------------------- __init__()
    def __init__(self, values: list[int] | None = None) -> None:
        """Create a queue, optionally bulk-loaded from *values*.

        The optional *values* are interpreted in logical front-to-rear order
        and enqueued one at a time, so ``Queue([10, 20, 30]).dequeue()``
        returns ``10`` (the first value enqueued).

        Args:
            values: Optional initial values, in logical front-to-rear order.
        """
        self._items: list[int] = []
        if values is not None:
            # Step 1: enqueue each value so the front-of-queue invariant holds
            for value in values:
                self.enqueue(value)
    # --------------------------------------------------------------- end __init__()

    # --------------------------------------------------------------- enqueue()
    def enqueue(self, value: int) -> None:
        """Add *value* to the rear of the queue (course-aligned).

        Uses ``list.insert(0, value)``, which is intentionally ``O(n)``
        because every existing item is shifted right by one position.

        Args:
            value: Integer to enqueue.
        """
        self._items.insert(0, value)
    # --------------------------------------------------------------- end enqueue()

    # --------------------------------------------------------------- dequeue()
    def dequeue(self) -> int | None:
        """Remove and return the value at the front of the queue.

        Uses ``list.pop()`` from the right end, which is ``O(1)``.

        Returns:
            The next FIFO value, or ``None`` if the queue is empty.
        """
        if not self._items:
            return None
        return self._items.pop()
    # --------------------------------------------------------------- end dequeue()

    # --------------------------------------------------------------- front()
    def front(self) -> int | None:
        """Return the value at the front of the queue without removing it.

        Returns:
            The next FIFO value, or ``None`` if the queue is empty.
        """
        if not self._items:
            return None
        return self._items[-1]
    # --------------------------------------------------------------- end front()

    # --------------------------------------------------------------- isEmpty()
    def isEmpty(self) -> bool:
        """Return True iff the queue is empty."""
        return len(self._items) == 0
    # --------------------------------------------------------------- end isEmpty()

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove every value from the queue."""
        self._items.clear()
    # --------------------------------------------------------------- end clear()

    # --------------------------------------------------------------- to_list()
    def to_list(self) -> list[int]:
        """Return a copy of the queue in logical front-to-rear order.

        Returns:
            A new list whose first element is the front of the queue.
        """
        return list(reversed(self._items))
    # --------------------------------------------------------------- end to_list()

    # --------------------------------------------------------------- to_internal_list()
    def to_internal_list(self) -> list[int]:
        """Return a copy of the raw internal storage.

        This exposes the course-aligned orientation for teaching/debugging:
        the front of the queue is the **right end** of the returned list.

        Returns:
            A copy of ``self._items``.
        """
        return list(self._items)
    # --------------------------------------------------------------- end to_internal_list()

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of items currently in the queue."""
        return len(self._items)
    # --------------------------------------------------------------- end __len__()

# --------------------------------------------------------------- end class Queue

# __________________________________________________________________________
# End of File
#
