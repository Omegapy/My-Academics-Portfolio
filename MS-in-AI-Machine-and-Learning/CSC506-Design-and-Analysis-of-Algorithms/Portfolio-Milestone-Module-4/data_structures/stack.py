# -------------------------------------------------------------------------
# File: stack.py
# Author: Alexander Ricciardi
# Date: 2026-04-06
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Stack ADT. The right end of the internal list is the top of the stack, 
# so push uses list.append and pop uses list.pop, both of which are amortized O(1).
# All operations that touch an empty stack return None instead of raising, 
# matching the empty-state policy used across the Module 4 playground.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""LIFO Stack implemented on top of a Python list."""

# ________________
# Imports
#

from __future__ import annotations

# __________________________________________________________________________
# Stack Class
#

# ========================================================================
# Stack
# ========================================================================
# --------------------------------------------------------------- class Stack
class Stack:
    """LIFO Stack backed by a Python list.

    The top of the stack is the right end of the internal list. Push uses
    ``list.append`` and pop uses ``list.pop``, both of which are amortized
    ``O(1)``. The empty-state policy is to return ``None`` from ``pop`` and
    ``peek`` rather than raising, which keeps the playground UI friendly.
    """

    # --------------------------------------------------------------- __init__()
    def __init__(self, values: list[int] | None = None) -> None:
        """Create a new stack, optionally pre-loaded with values.

        The optional values iterable is copied so the caller's list is
        never aliased. Values are pushed in order, so the last element of
        values becomes the top of the stack.

        Args:
            values: Optional initial values to push, bottom-to-top.
        """
        self._items: list[int] = []
        if values is not None:
            # Step 1: copy values so external mutation cannot affect the stack
            self._items = list(values)
    # --------------------------------------------------------------- end __init__()

    # --------------------------------------------------------------- push()
    def push(self, value: int) -> None:
        """Push *value* on top of the stack.

        Args:
            value: Integer to push onto the stack.
        """
        self._items.append(value)
    # --------------------------------------------------------------- end push()

    # --------------------------------------------------------------- pop()
    def pop(self) -> int | None:
        """Remove and return the top of the stack.

        Returns:
            The most recently pushed value, or ``None`` if the stack is
            empty (no exception raised).
        """
        if not self._items:
            return None
        return self._items.pop()
    # --------------------------------------------------------------- end pop()

    # --------------------------------------------------------------- peek()
    def peek(self) -> int | None:
        """Return the top of the stack without removing it.

        Returns:
            The top value, or ``None`` if the stack is empty.
        """
        if not self._items:
            return None
        return self._items[-1]
    # --------------------------------------------------------------- end peek()

    # --------------------------------------------------------------- isEmpty()
    def isEmpty(self) -> bool:
        """Return True iff the stack is empty.

        Returns:
            ``True`` when the stack contains zero items.
        """
        return len(self._items) == 0
    # --------------------------------------------------------------- end isEmpty()

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove every value from the stack."""
        self._items.clear()
    # --------------------------------------------------------------- end clear()

    # --------------------------------------------------------------- to_list()
    def to_list(self) -> list[int]:
        """Return a copy of the stack contents in bottom-to-top order.

        Returns:
            A new list whose first element is the bottom of the stack and
            whose last element is the top.
        """
        return list(self._items)
    # --------------------------------------------------------------- end to_list()

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of items currently on the stack."""
        return len(self._items)
    # --------------------------------------------------------------- end __len__()

# --------------------------------------------------------------- end class Stack

# __________________________________________________________________________
# End of File
#
 