# -------------------------------------------------------------------------
# File: linked_list.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Doubly LinkedList ADT. Each value is stored in a Node dataclass that has prev and next pointers. 
# The LinkedList tracks head, tail, and size, and supports four insert modes (front, rear, before, after). 
# Search and delete operate on the first matching node, 
# and display can traverse forward (head -> tail) or backward (tail -> head).
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code 
# -------------------------------------------------------------------------

"""Doubly LinkedList ADT with bidirectional traversal."""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass

# __________________________________________________________________________
# Node Dataclass
#

# ========================================================================
# Node
# ========================================================================
# --------------------------------------------------------------- dataclass Node
@dataclass
class Node:
    """One node in a doubly-linked list.

    Args:
        data: Integer value stored in the node.
        prev: Reference to the previous node, or ``None`` if this is the head.
        next: Reference to the next node, or ``None`` if this is the tail.
    """

    data: int
    prev: "Node | None" = None
    next: "Node | None" = None

# --------------------------------------------------------------- end dataclass Node

# __________________________________________________________________________
# LinkedList Class
#

# ========================================================================
# LinkedList
# ========================================================================
# --------------------------------------------------------------- class LinkedList
class LinkedList:
    """Doubly-linked list with head, tail, and size tracking.

    Empty-state policy: ``search`` returns ``None``; ``delete`` returns
    ``False`` when the value is not found; insertion methods return ``True``
    on success and ``False`` only when the requested anchor cannot be found
    (``before`` / ``after`` modes).
    """

    # --------------------------------------------------------------- __init__()
    def __init__(self, values: list[int] | None = None) -> None:
        """Create a list, optionally bulk-loaded by repeated rear inserts.

        Args:
            values: Optional initial values, inserted in order at the rear
                so that ``LinkedList([10, 20, 30]).display() == [10, 20, 30]``.
        """
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size: int = 0
        if values is not None:
            for value in values:
                self.insert_rear(value)
    # --------------------------------------------------------------- end __init__()

    # ====================================================================
    # Insert
    # ====================================================================

    # --------------------------------------------------------------- insert()
    def insert(
        self,
        value: int,
        *,
        mode: str = "rear",
        anchor: int | None = None,
    ) -> bool:
        """Primary insert dispatcher.

        Args:
            value: Integer value to insert.
            mode: Insertion mode — ``"front"``, ``"rear"``, ``"before"``,
                or ``"after"``.
            anchor: Required for ``"before"`` and ``"after"`` modes; the
                value of the existing node next to which *value* is inserted.

        Returns:
            ``True`` on successful insertion, ``False`` only when an anchor
            mode is requested but the anchor value is not found in the list.

        Raises:
            ValueError: If *mode* is unknown, or if an anchor mode is used
                without an *anchor* argument.
        """
        if mode == "rear":
            return self.insert_rear(value)
        if mode == "front":
            return self.insert_front(value)
        if mode == "before":
            if anchor is None:
                raise ValueError("insert(mode='before') requires anchor")
            return self.insert_before(anchor, value)
        if mode == "after":
            if anchor is None:
                raise ValueError("insert(mode='after') requires anchor")
            return self.insert_after(anchor, value)
        raise ValueError(
            f"Unknown insert mode {mode!r}. "
            "Use 'front', 'rear', 'before', or 'after'."
        )
    # --------------------------------------------------------------- end insert()

    # --------------------------------------------------------------- insert_front()
    def insert_front(self, value: int) -> bool:
        """Insert *value* at the front (head) of the list.

        Args:
            value: Integer to insert.

        Returns:
            Always ``True`` (insert at the head cannot fail).
        """
        new_node = Node(data=value)
        if self.head is None:
            # EDGE CASE: empty list - new node becomes head and tail
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
        return True
    # --------------------------------------------------------------- end insert_front()

    # --------------------------------------------------------------- insert_rear()
    def insert_rear(self, value: int) -> bool:
        """Insert *value* at the rear (tail) of the list.

        Args:
            value: Integer to insert.

        Returns:
            Always ``True`` (insert at the tail cannot fail).
        """
        new_node = Node(data=value)
        if self.tail is None:
            # EDGE CASE: empty list
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        return True
    # --------------------------------------------------------------- end insert_rear()

    # --------------------------------------------------------------- insert_before()
    def insert_before(self, anchor: int, value: int) -> bool:
        """Insert *value* immediately before the first node whose data == *anchor*.

        Args:
            anchor: Value of the existing node to insert before.
            value: Integer to insert.

        Returns:
            ``True`` if the anchor was found and the insert succeeded;
            ``False`` if no node holds *anchor* (the list is unchanged).
        """
        target = self._find_node(anchor)
        if target is None:
            return False

        # SAFETY CHECK: inserting before head reduces to insert_front
        if target is self.head:
            return self.insert_front(value)

        # General case: target has a previous node
        new_node = Node(data=value)
        prev_node = target.prev
        new_node.prev = prev_node
        new_node.next = target
        # prev_node is non-None because target is not head
        prev_node.next = new_node  # type: ignore[union-attr]
        target.prev = new_node
        self.size += 1
        return True
    # --------------------------------------------------------------- end insert_before()

    # --------------------------------------------------------------- insert_after()
    def insert_after(self, anchor: int, value: int) -> bool:
        """Insert *value* immediately after the first node whose data == *anchor*.

        Args:
            anchor: Value of the existing node to insert after.
            value: Integer to insert.

        Returns:
            ``True`` if the anchor was found and the insert succeeded;
            ``False`` if no node holds *anchor* (the list is unchanged).
        """
        target = self._find_node(anchor)
        if target is None:
            return False

        # SAFETY CHECK: inserting after tail reduces to insert_rear
        if target is self.tail:
            return self.insert_rear(value)

        new_node = Node(data=value)
        next_node = target.next
        new_node.prev = target
        new_node.next = next_node
        target.next = new_node
        # next_node is non-None because target is not tail
        next_node.prev = new_node  # type: ignore[union-attr]
        self.size += 1
        return True
    # --------------------------------------------------------------- end insert_after()

    # ====================================================================
    # Delete / Search
    # ====================================================================

    # --------------------------------------------------------------- delete()
    def delete(
        self,
        value: int | None = None,
        *,
        mode: str = "value",
        anchor: int | None = None,
    ) -> bool:
        """Primary delete dispatcher (mirrors :meth:`insert`).

        Args:
            value: Integer value to remove (required for ``mode="value"``,
                the default — kept positional so legacy callers like
                ``ll.delete(42)`` still work).
            mode: Delete mode — ``"value"`` (default), ``"front"``,
                ``"rear"``, ``"before"``, or ``"after"``.
            anchor: Required for ``"before"`` and ``"after"`` modes; the
                value of the existing node next to the one being removed.

        Returns:
            ``True`` if a node was removed, ``False`` for empty list /
            missing value / missing anchor / out-of-range neighbor.

        Raises:
            ValueError: If *mode* is unknown, if ``mode="value"`` is used
                without a *value*, or if an anchor mode is used without an
                *anchor* argument.
        """
        if mode == "value":
            if value is None:
                raise ValueError("delete(mode='value') requires a value")
            target = self._find_node(value)
            if target is None:
                return False
            return self._delete_node(target)
        if mode == "front":
            return self.delete_front()
        if mode == "rear":
            return self.delete_rear()
        if mode == "before":
            if anchor is None:
                raise ValueError("delete(mode='before') requires an anchor")
            return self.delete_before(anchor)
        if mode == "after":
            if anchor is None:
                raise ValueError("delete(mode='after') requires an anchor")
            return self.delete_after(anchor)
        raise ValueError(
            f"Unknown delete mode {mode!r}. "
            "Use 'value', 'front', 'rear', 'before', or 'after'."
        )
    # --------------------------------------------------------------- end delete()

    # --------------------------------------------------------------- delete_front()
    def delete_front(self) -> bool:
        """Remove the head node. O(1).

        Returns:
            ``True`` if a node was removed, ``False`` when the list is
            empty.
        """
        if self.head is None:
            return False
        return self._delete_node(self.head)
    # --------------------------------------------------------------- end delete_front()

    # --------------------------------------------------------------- delete_rear()
    def delete_rear(self) -> bool:
        """Remove the tail node. O(1).

        Returns:
            ``True`` if a node was removed, ``False`` when the list is
            empty.
        """
        if self.tail is None:
            return False
        return self._delete_node(self.tail)
    # --------------------------------------------------------------- end delete_rear()

    # --------------------------------------------------------------- delete_before()
    def delete_before(self, anchor: int) -> bool:
        """Remove the node immediately before the first node holding *anchor*.

        Args:
            anchor: Value of the existing node whose predecessor is removed.

        Returns:
            ``True`` if a node was removed, ``False`` if *anchor* is not
            found OR if the matching node is the head (no predecessor).
        """
        target = self._find_node(anchor)
        if target is None or target.prev is None:
            return False
        return self._delete_node(target.prev)
    # --------------------------------------------------------------- end delete_before()

    # --------------------------------------------------------------- delete_after()
    def delete_after(self, anchor: int) -> bool:
        """Remove the node immediately after the first node holding *anchor*.

        Args:
            anchor: Value of the existing node whose successor is removed.

        Returns:
            ``True`` if a node was removed, ``False`` if *anchor* is not
            found OR if the matching node is the tail (no successor).
        """
        target = self._find_node(anchor)
        if target is None or target.next is None:
            return False
        return self._delete_node(target.next)
    # --------------------------------------------------------------- end delete_after()

    # --------------------------------------------------------------- _delete_node()
    def _delete_node(self, node: "Node") -> bool:
        """Internal helper that unlinks *node* and updates head/tail/size.

        Handles every case: head, tail, middle, and only-node.

        Args:
            node: The node to unlink. Must already be a member of this list.

        Returns:
            Always ``True`` (the public callers gate on existence first).
        """
        prev_node = node.prev
        next_node = node.next
        # Handle the edge cases
        if prev_node is None and next_node is None:
            # EDGE CASE: only node in the list
            self.head = None
            self.tail = None
        elif prev_node is None:
            # CASE: head removal
            self.head = next_node
            next_node.prev = None  # type: ignore[union-attr]
        elif next_node is None:
            # CASE: tail removal
            self.tail = prev_node
            prev_node.next = None
        else:
            # CASE: middle removal
            prev_node.next = next_node
            next_node.prev = prev_node

        # Help GC by detaching the removed node
        node.prev = None
        node.next = None

        self.size -= 1
        return True
    # --------------------------------------------------------------- end _delete_node()

    # --------------------------------------------------------------- search()
    def search(self, value: int) -> Node | None:
        """Return the first node whose data equals *value*, or ``None``.

        Args:
            value: Integer value to search for.

        Returns:
            The matching :class:`Node`, or ``None`` if not found.
        """
        return self._find_node(value)
    # --------------------------------------------------------------- end search()

    # --------------------------------------------------------------- _find_node()
    def _find_node(self, value: int) -> Node | None:
        """Internal helper that returns the first matching node, or ``None``.

        Args:
            value: Integer value to find.

        Returns:
            The first :class:`Node` whose ``data`` equals *value*, else
            ``None``.
        """
        current = self.head
        # Iterate through the list and return the first node that matches the value
        while current is not None:
            if current.data == value:
                return current
            current = current.next
        return None
    # --------------------------------------------------------------- end _find_node()

    # ====================================================================
    # Display / Utility
    # ====================================================================

    # --------------------------------------------------------------- display()
    def display(self, reverse: bool = False) -> list[int]:
        """Return the list contents as a Python ``list[int]``.

        Args:
            reverse: When ``True``, traverse from ``tail`` to ``head``.

        Returns:
            A list of values in either head-to-tail (default) or tail-to-head
            order.
        """
        values: list[int] = []
        # Handle the edge cases
        if reverse:
            current = self.tail
            while current is not None:
                values.append(current.data)
                current = current.prev
        else:
            current = self.head
            while current is not None:
                values.append(current.data)
                current = current.next
        return values
    # --------------------------------------------------------------- end display()

    # --------------------------------------------------------------- isEmpty()
    def isEmpty(self) -> bool:
        """Return True iff the list contains no nodes."""
        return self.size == 0
    # --------------------------------------------------------------- end isEmpty()

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove every node by resetting head, tail, and size."""
        self.head = None
        self.tail = None
        self.size = 0
    # --------------------------------------------------------------- end clear()

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of nodes currently in the list."""
        return self.size
    # --------------------------------------------------------------- end __len__()

# --------------------------------------------------------------- end class LinkedList

# __________________________________________________________________________
# End of File
#
