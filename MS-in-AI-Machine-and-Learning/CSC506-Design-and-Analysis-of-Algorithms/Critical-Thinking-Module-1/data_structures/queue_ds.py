# -------------------------------------------------------------------------
# File: queue_ds.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Provides a linked-node-backed Queue (FIFO) data structure with enqueue,
# dequeue, and front operations — all running in O(1) time.
# Unlike a Python-list-based queue where dequeue (pop(0)) is O(n),
# this linked-node implementation achieves O(1) for both enqueue and dequeue.
# -------------------------------------------------------------------------

# --- Classes ---
# - Queue: FIFO queue backed by singly-linked Nodes with front and rear pointers.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - typing.Any to allow storing any data type.
# - data_structures.node.Node for the shared node class.
# -------------------------------------------------------------------------

"""
Linked-node-backed Queue (FIFO) data structure.

The Queue class uses singly-linked Node objects with front and rear
pointers so that both enqueue and dequeue operate in O(1) time.
This is superior to a Python-list-based queue where ``list.pop(0)``
requires O(n) time to shift elements.
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

# ------------------------------------------------------------------------- class Queue
class Queue:
    """A First-In-First-Out (FIFO) queue backed by singly-linked nodes.

    Maintains front and rear pointers for O(1) enqueue and dequeue.

    Attributes:
        _front: Reference to the front node (dequeue end), or None if empty.
        _rear: Reference to the rear node (enqueue end), or None if empty.
        _size: Number of elements currently in the queue.

    Logic:
        1. Enqueue creates a new node and appends it at the rear.
        2. Dequeue removes and returns the node at the front.
        3. When the queue becomes empty, both front and rear are reset to None.
    """

    # ______________________
    # Constructor
    #
    # -------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initialize an empty queue."""
        self._front: Node | None = None
        self._rear: Node | None = None
        self._size: int = 0
    # -------------------------------------------------------------- end __init__()

    # ______________________
    # Mutators
    #

    # -------------------------------------------------------------- enqueue()
    def enqueue(self, value: Any) -> None:
        """Add a value to the rear of the queue — O(1).

        Args:
            value: The data to enqueue.

        Logic:
            1. Create a new node with the given value.
            2. If the queue is empty, both front and rear point to the new node.
            3. Otherwise, link the current rear's next_node to the new node
               and advance rear.
        """
        new_node = Node(data=value)
        # Step 1: Handle empty queue
        if self._rear is None:
            self._front = new_node
            self._rear = new_node
        else:
            # Step 2: Link current rear to new node and advance rear
            self._rear.next_node = new_node
            self._rear = new_node
        # Step 3: Increment size
        self._size += 1
    # -------------------------------------------------------------- end enqueue()

    # -------------------------------------------------------------- dequeue()
    def dequeue(self) -> Any:
        """Remove and return the front value from the queue — O(1).

        Returns:
            The data from the front node.

        Raises:
            IndexError: If the queue is empty.

        Logic:
            1. Check that the queue is not empty.
            2. Save the front node's data.
            3. Advance front to the next node.
            4. If front becomes None, also reset rear to None.
        """
        # VALIDATION: Ensure queue is not empty
        if self._front is None:
            raise IndexError("Dequeue from an empty queue.")
        # Step 1: Save front value
        value = self._front.data
        # Step 2: Advance front pointer
        self._front = self._front.next_node
        # Step 3: If queue is now empty, reset rear
        if self._front is None:
            self._rear = None
        # Step 4: Decrement size
        self._size -= 1
        return value
    # -------------------------------------------------------------- end dequeue()

    # ______________________
    # Getters / Queries
    #

    # -------------------------------------------------------------- front()
    def front(self) -> Any:
        """Return the front value without removing it — O(1).

        Returns:
            The data from the front node.

        Raises:
            IndexError: If the queue is empty.
        """
        # VALIDATION: Ensure queue is not empty
        if self._front is None:
            raise IndexError("Front on an empty queue.")
        return self._front.data
    # -------------------------------------------------------------- end front()

    # -------------------------------------------------------------- is_empty()
    def is_empty(self) -> bool:
        """Return True if the queue contains no elements — O(1)."""
        return self._front is None
    # -------------------------------------------------------------- end is_empty()

    # -------------------------------------------------------------- size()
    def size(self) -> int:
        """Return the number of elements in the queue — O(1)."""
        return self._size
    # -------------------------------------------------------------- end size()

    # ______________________
    # Utilities
    #

    # -------------------------------------------------------------- to_list()
    def to_list(self) -> list[Any]:
        """Traverse the queue front-to-rear and return values as a list — O(n).

        Returns:
            A list of values from front to rear.
        """
        result: list[Any] = []
        current = self._front
        # MAIN TRAVERSAL LOOP: Walk from front to rear
        while current is not None:
            result.append(current.data)
            current = current.next_node
        return result
    # -------------------------------------------------------------- end to_list()

    # -------------------------------------------------------------- __str__()
    def __str__(self) -> str:
        """Return a human-readable string representation of the queue.

        Returns:
            A string showing the queue contents from front to rear.
        """
        if self.is_empty():
            return "Queue: [empty]"
        values = self.to_list()
        items = " -> ".join(str(v) for v in values)
        return f"Queue (front -> rear): {items}"
    # -------------------------------------------------------------- end __str__()

# ------------------------------------------------------------------------- end class Queue

# ==============================================================================
# End of File
# ==============================================================================
