# -------------------------------------------------------------------------
# File: deque.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Deque ADT with the same orientation as Queue: the right end of the internal list is the logical
# front and index 0 is the logical rear. addFront/removeFront use append/pop
# (O(1)), while addRear/removeRear use insert(0)/pop(0) (O(n)). The empty-
# state policy is to return None from removeFront/removeRear/peekFront/
# peekRear instead of raising.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved. 
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Double-ended queue implemented on top of a Python list (course-aligned)."""

# ________________
# Imports
#

from __future__ import annotations

# __________________________________________________________________________
# Deque Class
#

# ========================================================================
# Deque
# ========================================================================
# --------------------------------------------------------------- class Deque
class Deque:
    """List-backed Deque using the course-aligned orientation.

    Internal storage:

    - logical front = right end of ``self._items``
    - logical rear  = index ``0`` of ``self._items``

    Cost summary:

    | Operation     | List op       | Cost                |
    |---------------|---------------|---------------------|
    | ``addFront``  | ``append``    | amortized ``O(1)``  |
    | ``addRear``   | ``insert(0)`` | ``O(n)``            |
    | ``removeFront`` | ``pop()``   | ``O(1)``            |
    | ``removeRear``  | ``pop(0)``  | ``O(n)``            |

    Empty-state policy: ``removeFront``, ``removeRear``, ``peekFront``, and
    ``peekRear`` all return ``None`` when the deque is empty.
    """

    # --------------------------------------------------------------- __init__()
    def __init__(self, values: list[int] | None = None) -> None:
        """Create a deque, optionally bulk-loaded from *values*.

        Bulk-loaded values are added with ``addFront`` in iteration order so
        that the first iterated value ends up at the rear of the deque.
        This matches the convention used by ``Queue.__init__``.

        Args:
            values: Optional initial values, interpreted in logical
                front-to-rear order.
        """
        self._items: list[int] = []
        if values is not None:
            # Step 1: addFront in iteration order so iteration order
            #         matches logical front-to-rear order
            for value in reversed(values):
                self.addFront(value)
    # --------------------------------------------------------------- end __init__()

    # --------------------------------------------------------------- addFront()
    def addFront(self, value: int) -> None:
        """Add *value* at the logical front of the deque.

        Uses ``list.append`` because the right end of the internal list
        is the logical front. Cost: amortized ``O(1)``.

        Args:
            value: Integer to add at the front.
        """
        self._items.append(value)
    # --------------------------------------------------------------- end addFront()

    # --------------------------------------------------------------- addRear()
    def addRear(self, value: int) -> None:
        """Add *value* at the logical rear of the deque.

        Uses ``list.insert(0, value)``, which is intentionally ``O(n)``
        because every existing item is shifted right by one position.

        Args:
            value: Integer to add at the rear.
        """
        self._items.insert(0, value)
    # --------------------------------------------------------------- end addRear()

    # --------------------------------------------------------------- removeFront()
    def removeFront(self) -> int | None:
        """Remove and return the logical front value.

        Returns:
            The front value, or ``None`` if the deque is empty.
        """
        if not self._items:
            return None
        return self._items.pop()
    # --------------------------------------------------------------- end removeFront()

    # --------------------------------------------------------------- removeRear()
    def removeRear(self) -> int | None:
        """Remove and return the logical rear value.

        Uses ``list.pop(0)``, which is ``O(n)``.

        Returns:
            The rear value, or ``None`` if the deque is empty.
        """
        if not self._items:
            return None
        return self._items.pop(0)
    # --------------------------------------------------------------- end removeRear()

    # --------------------------------------------------------------- peekFront()
    def peekFront(self) -> int | None:
        """Return the logical front without removing it.

        Returns:
            The front value, or ``None`` if the deque is empty.
        """
        if not self._items:
            return None
        return self._items[-1]
    # --------------------------------------------------------------- end peekFront()

    # --------------------------------------------------------------- peekRear()
    def peekRear(self) -> int | None:
        """Return the logical rear without removing it.

        Returns:
            The rear value, or ``None`` if the deque is empty.
        """
        if not self._items:
            return None
        return self._items[0]
    # --------------------------------------------------------------- end peekRear()

    # --------------------------------------------------------------- isEmpty()
    def isEmpty(self) -> bool:
        """Return True iff the deque is empty."""
        return len(self._items) == 0
    # --------------------------------------------------------------- end isEmpty()

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove every value from the deque."""
        self._items.clear()
    # --------------------------------------------------------------- end clear()

    # --------------------------------------------------------------- to_list()
    def to_list(self) -> list[int]:
        """Return a copy of the deque in logical front-to-rear order.

        Returns:
            A new list whose first element is the front of the deque.
        """
        return list(reversed(self._items))
    # --------------------------------------------------------------- end to_list()

    # --------------------------------------------------------------- to_internal_list()
    def to_internal_list(self) -> list[int]:
        """Return a copy of the raw internal storage (rear-to-front)."""
        return list(self._items)
    # --------------------------------------------------------------- end to_internal_list()

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of items currently in the deque."""
        return len(self._items)
    # --------------------------------------------------------------- end __len__()

# --------------------------------------------------------------- end class Deque

# __________________________________________________________________________
# End of File
#
