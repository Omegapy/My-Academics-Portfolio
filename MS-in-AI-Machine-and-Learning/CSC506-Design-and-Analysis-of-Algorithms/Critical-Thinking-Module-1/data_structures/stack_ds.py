# -------------------------------------------------------------------------
# File: stack_ds.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Provides a linked-node-backed Stack (LIFO) data structure with push,
# pop, peek, and traversal operations — all running in O(1) time
# (except traversal which is O(n)).
# -------------------------------------------------------------------------

# --- Classes ---
# - Stack: LIFO stack backed by singly-linked Nodes.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - typing.Any to allow storing any data type.
# - data_structures.node.Node for the shared node class.
# -------------------------------------------------------------------------

"""
Linked-node-backed Stack (LIFO) data structure.

The Stack class uses singly-linked Node objects so that push and pop
operate in O(1) time without requiring array resizing.
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from typing import Any

from data_structures.node import Node

# ==============================================================================
# CLASSES
# ==============================================================================

# ------------------------------------------------------------------------- class Stack
class Stack:
    """A Last-In-First-Out (LIFO) stack backed by singly-linked nodes.

    All primary operations — push, pop, peek — run in O(1) time.
    The stack maintains an internal size counter to provide O(1) size queries.

    Attributes:
        _top: Reference to the top node, or None if the stack is empty.
        _size: Number of elements currently in the stack.

    Logic:
        1. Push creates a new node whose next_node points to the current top,
           then updates top to the new node.
        2. Pop saves the top node's data, advances top to the next node,
           and returns the saved data.
        3. Peek returns the top node's data without modifying the stack.
    """

    # ______________________
    # Constructor
    #
    # -------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._top: Node | None = None
        self._size: int = 0
    # -------------------------------------------------------------- end __init__()

    # ______________________
    # Mutators
    #

    # -------------------------------------------------------------- push()
    def push(self, value: Any) -> None:
        """Push a value onto the top of the stack — O(1).

        Args:
            value: The data to push onto the stack.

        Logic:
            1. Create a new node with the given value.
            2. Link the new node to the current top.
            3. Update top to the new node and increment size.
        """
        # Step 1: Create new node pointing to current top
        new_node = Node(data=value, next_node=self._top)
        # Step 2: Update top to new node
        self._top = new_node
        # Step 3: Increment size
        self._size += 1
    # -------------------------------------------------------------- end push()

    # -------------------------------------------------------------- pop()
    def pop(self) -> Any:
        """Remove and return the top value from the stack — O(1).

        Returns:
            The data from the top node.

        Raises:
            IndexError: If the stack is empty.

        Logic:
            1. Check that the stack is not empty.
            2. Save the top node's data.
            3. Advance top to the next node and decrement size.
        """
        # VALIDATION: Ensure stack is not empty
        if self._top is None:
            raise IndexError("Pop from an empty stack.")
        # Step 1: Save top value
        value = self._top.data
        # Step 2: Advance top pointer
        self._top = self._top.next_node
        # Step 3: Decrement size
        self._size -= 1
        return value
    # -------------------------------------------------------------- end pop()

    # ______________________
    # Getters / Queries
    #

    # -------------------------------------------------------------- peek()
    def peek(self) -> Any:
        """Return the top value without removing it — O(1).

        Returns:
            The data from the top node.

        Raises:
            IndexError: If the stack is empty.
        """
        # VALIDATION: Ensure stack is not empty
        if self._top is None:
            raise IndexError("Peek on an empty stack.")
        return self._top.data
    # -------------------------------------------------------------- end peek()

    # -------------------------------------------------------------- is_empty()
    def is_empty(self) -> bool:
        """Return True if the stack contains no elements — O(1)."""
        return self._top is None
    # -------------------------------------------------------------- end is_empty()

    # -------------------------------------------------------------- size()
    def size(self) -> int:
        """Return the number of elements in the stack — O(1)."""
        return self._size
    # -------------------------------------------------------------- end size()

    # ______________________
    # Utilities
    #

    # -------------------------------------------------------------- to_list()
    def to_list(self) -> list[Any]:
        """Traverse the stack top-to-bottom and return values as a list — O(n).

        Returns:
            A list of values from top to bottom.
        """
        result: list[Any] = []
        current = self._top
        # MAIN TRAVERSAL LOOP: Walk from top to bottom
        while current is not None:
            result.append(current.data)
            current = current.next_node
        return result
    # -------------------------------------------------------------- end to_list()

    # -------------------------------------------------------------- __str__()
    def __str__(self) -> str:
        """Return a human-readable string representation of the stack.

        Returns:
            A string showing the stack contents from top to bottom.
        """
        if self.is_empty():
            return "Stack: [empty]"
        values = self.to_list()
        items = " -> ".join(str(v) for v in values)
        return f"Stack (top -> bottom): {items}"
    # -------------------------------------------------------------- end __str__()

# ------------------------------------------------------------------------- end class Stack

# ==============================================================================
# End of File
# ==============================================================================
