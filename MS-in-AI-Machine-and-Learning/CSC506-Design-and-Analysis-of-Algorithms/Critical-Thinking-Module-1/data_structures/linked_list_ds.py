# -------------------------------------------------------------------------
# File: linked_list_ds.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Provides a singly linked list data structure with prepend, append,
# insert-after, delete, and search operations.
# -------------------------------------------------------------------------

# --- Classes ---
# - LinkedList: Singly linked list backed by Node objects.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - typing.Any to allow storing any data type.
# - data_structures.node.Node for the shared node class.
# -------------------------------------------------------------------------

"""
Singly linked list data structure.

The LinkedList class uses Node objects to form a chain of elements.
Prepend is O(1), while append, insert-after, delete, and search
require O(n) traversal in the worst case.
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

# ------------------------------------------------------------------------- class LinkedList
class LinkedList:
    """A singly linked list with head pointer.

    Supports insertion (prepend, append, insert-after), deletion, and search.

    Attributes:
        _head: Reference to the first node, or None if the list is empty.
        _size: Number of elements currently in the list.

    Logic:
        1. Prepend inserts at the front by creating a node whose next_node
           points to the current head, then updating head — O(1).
        2. Append traverses to the tail and links a new node — O(n).
        3. Delete traverses with a previous pointer to unlink the target — O(n).
    """

    # ______________________
    # Constructor
    #
    # -------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initialize an empty linked list."""
        self._head: Node | None = None
        self._size: int = 0
    # -------------------------------------------------------------- end __init__()

    # ______________________
    # Mutators
    #

    # -------------------------------------------------------------- prepend()
    def prepend(self, value: Any) -> None:
        """Insert a value at the front of the list — O(1).

        Args:
            value: The data to insert.

        Logic:
            1. Create a new node pointing to the current head.
            2. Update head to the new node.
        """
        # Step 1: Create new node pointing to current head
        new_node = Node(data=value, next_node=self._head)
        # Step 2: Update head
        self._head = new_node
        self._size += 1
    # -------------------------------------------------------------- end prepend()

    # -------------------------------------------------------------- append()
    def append(self, value: Any) -> None:
        """Insert a value at the end of the list — O(n).

        Args:
            value: The data to insert.

        Logic:
            1. Create a new node.
            2. If the list is empty, set head to the new node.
            3. Otherwise, traverse to the last node and link it.
        """
        new_node = Node(data=value)
        # Step 1: Handle empty list
        if self._head is None:
            self._head = new_node
        else:
            # Step 2: Traverse to the last node
            current = self._head
            while current.next_node is not None:
                current = current.next_node
            # Step 3: Link new node at the end
            current.next_node = new_node
        self._size += 1
    # -------------------------------------------------------------- end append()

    # -------------------------------------------------------------- insert_after()
    def insert_after(self, target: Any, value: Any) -> bool:
        """Insert a new value after the first occurrence of target — O(n).

        Args:
            target: The value to search for.
            value: The new value to insert after the target.

        Returns:
            True if the target was found and insertion succeeded, False otherwise.

        Logic:
            1. Traverse the list looking for the target value.
            2. If found, create a new node and splice it in after the target node.
        """
        current = self._head
        # MAIN TRAVERSAL LOOP: Search for target node
        while current is not None:
            if current.data == target:
                # Step 1: Create new node pointing to target's next
                new_node = Node(data=value, next_node=current.next_node)
                # Step 2: Link target to new node
                current.next_node = new_node
                self._size += 1
                return True
            current = current.next_node
        return False
    # -------------------------------------------------------------- end insert_after()

    # -------------------------------------------------------------- delete()
    def delete(self, value: Any) -> bool:
        """Delete the first occurrence of a value from the list — O(n).

        Args:
            value: The value to remove.

        Returns:
            True if the value was found and deleted, False otherwise.

        Logic:
            1. Handle empty list.
            2. Handle head deletion.
            3. Traverse with a previous pointer to find and unlink the node.
        """
        # Step 1: Handle empty list
        if self._head is None:
            return False
        # Step 2: Handle head deletion
        if self._head.data == value:
            self._head = self._head.next_node
            self._size -= 1
            return True
        # Step 3: Traverse to find node, keeping track of previous
        previous = self._head
        current = self._head.next_node
        while current is not None:
            if current.data == value:
                # Unlink the node
                previous.next_node = current.next_node
                self._size -= 1
                return True
            previous = current
            current = current.next_node
        return False
    # -------------------------------------------------------------- end delete()

    # ______________________
    # Getters / Queries
    #

    # -------------------------------------------------------------- search()
    def search(self, value: Any) -> bool:
        """Search for a value in the list — O(n).

        Args:
            value: The value to search for.

        Returns:
            True if the value is found, False otherwise.
        """
        current = self._head
        # MAIN TRAVERSAL LOOP: Search for value
        while current is not None:
            if current.data == value:
                return True
            current = current.next_node
        return False
    # -------------------------------------------------------------- end search()

    # -------------------------------------------------------------- is_empty()
    def is_empty(self) -> bool:
        """Return True if the list contains no elements — O(1)."""
        return self._head is None
    # -------------------------------------------------------------- end is_empty()

    # -------------------------------------------------------------- size()
    def size(self) -> int:
        """Return the number of elements in the list — O(1)."""
        return self._size
    # -------------------------------------------------------------- end size()

    # ______________________
    # Utilities
    #

    # -------------------------------------------------------------- to_list()
    def to_list(self) -> list[Any]:
        """Traverse head-to-tail and return values as a list — O(n).

        Returns:
            A list of values from head to tail.
        """
        result: list[Any] = []
        current = self._head
        # MAIN TRAVERSAL LOOP: Walk from head to tail
        while current is not None:
            result.append(current.data)
            current = current.next_node
        return result
    # -------------------------------------------------------------- end to_list()

    # -------------------------------------------------------------- __str__()
    def __str__(self) -> str:
        """Return a human-readable string showing the node chain.

        Returns:
            A string like ``[10] -> [20] -> [30] -> None``.
        """
        if self.is_empty():
            return "LinkedList: [empty]"
        parts: list[str] = []
        current = self._head
        while current is not None:
            parts.append(f"[{current.data}]")
            current = current.next_node
        return " -> ".join(parts) + " -> None"
    # -------------------------------------------------------------- end __str__()

# ------------------------------------------------------------------------- end class LinkedList

# ==============================================================================
# End of File
# ==============================================================================
