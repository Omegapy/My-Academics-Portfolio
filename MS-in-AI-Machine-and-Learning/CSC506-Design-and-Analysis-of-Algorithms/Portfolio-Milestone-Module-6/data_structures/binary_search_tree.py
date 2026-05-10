# -------------------------------------------------------------------------
# File: binary_search_tree.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-26
# File Path: Portfolio-Milestone-Module-6/data_structures/binary_search_tree.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
# Assignment:
# Portfolio Milestone Module 6 - Trees
#
# Directions:
# - Implement a Binary Search Tree with insert, delete, search, and
#   traversal support.
# - Build a BST-backed Map, detect unbalanced trees, and test with at
#   least 50 comparable items.
# - Compare TreeMap search behavior against a list-backed baseline and
#   report the results.
#
# --- Module Contents Overview ---
# - Class Definitions - Data Classes: ``TreeNode`` stores comparable keys and
#   optional payloads.
# - Class Definitions - Regular Classes: ``BinarySearchTree`` exposes the
#   assignment operations and balance-report helpers.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses
# - Third-Party: none
# - Local Project Modules:
#   - models.balance_report
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported directly by the Streamlit BST lab and guided validation helpers.
# - Imported indirectly by ``Map`` to provide ordered key-value storage.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Binary search tree implementation.

It provides the ordered tree structure used by the BST lab and by the
BST-backed ``Map`` abstraction, including traversal output, balance detection,
and ASCII rendering that feed the Streamlit UI and automated tests.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations
from dataclasses import dataclass
from models.balance_report import BalanceReport

# __________________________________________________________________________
# Data Classes
# ========================================================================
# TYPES AND DATA STRUCTURES
# ========================================================================
# ``TreeNode`` stores the comparable key and optional payload used by the
# plain BST. The node itself does not enforce ordering; the tree does.
#
# ------------------------------------------------------------------------- class TreeNode
@dataclass(slots=True, kw_only=True, eq=False)
class TreeNode:
    """Node stored inside the binary search tree.

    Attributes:
        key: Comparable key used to position the node in the tree.
        value: Optional payload associated with the key.
        left: Left-child node.
        right: Right-child node.
    """

    key: object
    value: object | None = None  # Remains ``None`` for plain key-only BST usage.
    left: TreeNode | None = None  # Stays ``None`` until a smaller child is inserted.
    right: TreeNode | None = None  # Stays ``None`` until a larger child is inserted

# ------------------------------------------------------------------------- end class TreeNode

# __________________________________________________________________________
# Class Definitions - Regular Classes
# ========================================================================
# CLASS DEFINITIONS
# ========================================================================
# ``BinarySearchTree`` preserves the BST ordering rule while exposing the
# assignment operations: insert, delete, search, traversals, min/max, height,
# balance detection, and ASCII rendering.
#
# ------------------------------------------------------------------------- class BinarySearchTree
class BinarySearchTree:
    """Plain binary search tree with balance detection but no rebalancing.

    Attributes:
        _root: Root node for the tree, or ``None`` when the tree is empty.
        _size: Number of stored nodes currently in the tree.

    Logic:
        This class preserves the binary-search-tree ordering rule without
        automatic rebalancing.
        1. Store mutually comparable keys so left children remain smaller and
           right children remain larger than each parent.
        2. Build higher-level operations such as traversal, deletion, and
           balance reporting on top of that ordering rule.
        3. Expose display and analysis helpers without changing the underlying
           tree structure.
    """

    # ________________________________________________
    # Construction and Key Policy
    #
    # --------------------------------------------------------------- __init__()
    def __init__(
        self,
        items: list[tuple[object, object]] | None = None,
    ) -> None:
        """Initialize an empty BST and optionally preload key-value items.

        Logic:
            This method prepares the tree storage and optionally seeds it with
            initial entries.
            1. Start with an empty root reference and zero size.
            2. Reinsert any provided items through ``insert()`` so normal key
               validation and duplicate handling stay consistent.
        """
        self._root: TreeNode | None = None
        self._size: int = 0

        # Step 1: preload through ``insert()`` so duplicate-key and
        # comparability rules stay identical to the normal public path.
        if items:
            for key, value in items:
                self.insert(key, value)
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- _compare_keys()
    def _compare_keys(self, left: object, right: object) -> int:
        """Compare two keys and return ``-1``, ``0``, or ``1``.

        Logic:
            This method centralizes BST key ordering for every search and
            update path.
            1. Compare the left key against the right key using normal Python
               ordering.
            2. Return ``-1``, ``0``, or ``1`` to represent the ordering
               result.
            3. Raise ``TypeError`` when the keys cannot be compared safely.
        """
        try:
            if left < right:
                return -1
            if left > right:
                return 1
            return 0
        except TypeError as exc:
            raise TypeError(
                "All keys in one BinarySearchTree must be mutually comparable "
                "and from one compatible type family."
            ) from exc
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- _ensure_key_compatibility()
    def _ensure_key_compatibility(self, key: object) -> None:
        """Validate that ``key`` is comparable with existing tree keys.

        Logic:
            This method rejects incompatible key families before traversal or
            mutation continues.
            1. Return immediately when the tree is empty.
            2. Compare the candidate key against the current root key.
            3. Let the shared comparison helper raise when the key family is
               incompatible.
        """
        # VALIDATION: an empty tree has no existing key family to compare against.
        if self._root is None:
            return
        self._compare_keys(key, self._root.key)
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Core BST Operations
    #
    # --------------------------------------------------------------- insert()
    def insert(self, key: object, value: object | None = None) -> bool:
        """Insert or update a key in the BST.

        Logic:
            This method preserves BST ordering while inserting new keys or
            updating existing ones.
            1. Handle the empty-tree case by creating the root node.
            2. Descend the tree using key comparisons until the insert/update
               location is found.
            3. Update an existing key in place or attach a new child node.
        """
        # Step 1: the empty-tree case becomes the root insert.
        if self._root is None:
            self._root = TreeNode(key=key, value=value)
            self._size = 1
            return True

        # VALIDATION: every inserted key must remain comparable with the
        # existing key family already stored in the tree.
        self._ensure_key_compatibility(key)

        parent: TreeNode | None = None
        current = self._root

        # MAIN ITERATION LOOP: descend until we find the insert/update spot.
        while current is not None:
            parent = current
            comparison = self._compare_keys(key, current.key)
            # Step 2: update in place when the key already exists.
            if comparison == 0:
                current.value = value
                return False
            # Step 3: otherwise follow the BST ordering rule downward.
            if comparison < 0:
                current = current.left
            else:
                current = current.right

        # Step 4: attach the new node beneath the last visited parent.
        new_node = TreeNode(key=key, value=value)
        if parent is None:
            self._root = new_node
        elif self._compare_keys(key, parent.key) < 0:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1
        return True
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- search()
    def search(self, key: object) -> TreeNode | None:
        """Search for ``key`` and return its node when present.

        Logic:
            This method follows the BST ordering rule to locate one key.
            1. Validate that the requested key belongs to the current key
               family.
            2. Walk left or right according to each comparison result.
            3. Return the matching node or ``None`` when the search falls off
               the tree.
        """
        # VALIDATION: reject incomparable key families before traversal starts.
        self._ensure_key_compatibility(key)
        current = self._root
        # MAIN ITERATION LOOP: follow the BST ordering rule until the key is found
        # or the search falls off the tree.
        while current is not None:
            comparison = self._compare_keys(key, current.key)
            if comparison == 0:
                return current
            current = current.left if comparison < 0 else current.right
        return None
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- contains()
    def contains(self, key: object) -> bool:
        """Return whether ``key`` exists in the BST.

        Logic:
            This method exposes membership as a boolean-only lookup.
            1. Delegate the lookup to ``search()``.
            2. Return ``True`` when a node is found.
            3. Return ``False`` when the search result is ``None``.
        """
        return self.search(key) is not None
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- min_key()
    def min_key(self) -> object | None:
        """Return the minimum key in the BST or ``None`` when empty.

        Logic:
            This method finds the smallest stored key by walking the left edge
            of the tree.
            1. Stop early when the tree is empty.
            2. Move left until no smaller descendant remains.
            3. Return the key stored in the left-most node.
        """
        current = self._root
        # VALIDATION: an empty tree has no minimum key.
        if current is None:
            return None
        # MAIN ITERATION LOOP: the minimum key is the left-most descendant.
        while current.left is not None:
            current = current.left
        return current.key
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- max_key()
    def max_key(self) -> object | None:
        """Return the maximum key in the BST or ``None`` when empty.

        Logic:
            This method finds the largest stored key by walking the right edge
            of the tree.
            1. Stop early when the tree is empty.
            2. Move right until no larger descendant remains.
            3. Return the key stored in the right-most node.
        """
        current = self._root
        # VALIDATION: an empty tree has no maximum key.
        if current is None:
            return None
        # MAIN ITERATION LOOP: the maximum key is the right-most descendant.
        while current.right is not None:
            current = current.right
        return current.key
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove all nodes from the tree.

        Logic:
            This method resets the BST to its empty state.
            1. Clear the root reference.
            2. Reset the stored node count to zero.
        """
        self._root = None
        self._size = 0
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of nodes in the tree.

        Logic:
            This method reports the current BST size.
            1. Read the stored node-count field.
            2. Return that count to the caller.
        """
        return self._size
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Traversal Helpers
    #
    # --------------------------------------------------------------- _traversal_nodes()
    def _traversal_nodes(self, order: str) -> list[TreeNode]:
        """Return nodes in the requested traversal order.

        Logic:
            This method centralizes the tree's non-recursive traversal
            strategies.
            1. Stop early when the tree is empty.
            2. Execute the requested in-order, pre-order, or post-order walk
               using an explicit stack.
            3. Return the visited nodes in the requested order or raise for an
               unsupported traversal name.
        """
        # VALIDATION: empty trees produce an empty traversal regardless of order.
        if self._root is None:
            return []

        # DISPATCH: choose the explicit-stack traversal that matches the requested order.
        if order == "inorder":
            result: list[TreeNode] = []
            stack: list[TreeNode] = []
            current: TreeNode | None = self._root
            # MAIN ITERATION LOOP: walk left, visit, then walk right.
            while stack or current is not None:
                # Step 1: keep descending left until the current branch ends.
                while current is not None:
                    stack.append(current)
                    current = current.left
                # Step 2: visit the next node whose left subtree is complete.
                current = stack.pop()
                result.append(current)
                # Step 3: continue with the right subtree after the visit.
                current = current.right
            return result

        if order == "preorder":
            result = []
            stack = [self._root]
            # MAIN ITERATION LOOP: visit node, then queue right and left children.
            while stack:
                # Step 1: visit the next node scheduled for pre-order output.
                current = stack.pop()
                result.append(current)
                # Step 2: queue the right child first so the left child is processed next.
                if current.right is not None:
                    stack.append(current.right)
                # Step 3: queue the left child so it appears before the right subtree.
                if current.left is not None:
                    stack.append(current.left)
            return result

        if order == "postorder":
            result = []
            stack: list[tuple[TreeNode, bool]] = [(self._root, False)]
            # MAIN ITERATION LOOP: revisit nodes after both subtrees have been seen.
            while stack:
                # Step 1: recover the next node together with its visit-state flag.
                current, visited = stack.pop()
                if visited:
                    # Step 2: append the node only after both children were already handled.
                    result.append(current)
                    continue
                # Step 3: schedule the node for its later post-order visit.
                stack.append((current, True))
                # Step 4: push children so they are fully processed before the revisit.
                if current.right is not None:
                    stack.append((current.right, False))
                if current.left is not None:
                    stack.append((current.left, False))
            return result

        raise ValueError("Order must be 'inorder', 'preorder', or 'postorder'.")
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- inorder()
    def inorder(self) -> list[object]:
        """Return keys visited in in-order traversal.

        Logic:
            This method exposes the BST's sorted key traversal.
            1. Request the in-order node sequence from the shared traversal
               helper.
            2. Extract each node key in visit order.
            3. Return the resulting key list.
        """
        return [node.key for node in self._traversal_nodes("inorder")]
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- preorder()
    def preorder(self) -> list[object]:
        """Return keys visited in pre-order traversal.

        Logic:
            This method exposes the BST's root-left-right key traversal.
            1. Request the pre-order node sequence from the shared traversal
               helper.
            2. Extract each node key in visit order.
            3. Return the resulting key list.
        """
        return [node.key for node in self._traversal_nodes("preorder")]
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- postorder()
    def postorder(self) -> list[object]:
        """Return keys visited in post-order traversal.

        Logic:
            This method exposes the BST's left-right-root key traversal.
            1. Request the post-order node sequence from the shared traversal
               helper.
            2. Extract each node key in visit order.
            3. Return the resulting key list.
        """
        return [node.key for node in self._traversal_nodes("postorder")]
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- items()
    def items(self, order: str = "inorder") -> list[tuple[object, object | None]]:
        """Return ``(key, value)`` pairs in the requested traversal order.

        Logic:
            This method exposes the tree contents as ordered key-value tuples.
            1. Request the node sequence for the selected traversal order.
            2. Rebuild each visited node as a ``(key, value)`` pair.
            3. Return the resulting list of pairs.
        """
        return [(node.key, node.value) for node in self._traversal_nodes(order)]
    # ---------------------------------------------------------------   

    # --------------------------------------------------------------- delete()
    def delete(self, key: object) -> bool:
        """Delete *key* from the BST when present.

        Logic:
            This method removes one key while preserving BST ordering.
            1. Search for the requested node and track its parent.
            2. Replace two-child deletions with the in-order successor.
            3. Reconnect the surviving child subtree and shrink the size.
        """
        # VALIDATION: the requested key must belong to the tree's comparable type family.
        self._ensure_key_compatibility(key)

        parent: TreeNode | None = None
        current = self._root

        # MAIN ITERATION LOOP: descend until the target node and its parent are located.
        while current is not None:
            # Step 1: compare the requested key against the current node.
            comparison = self._compare_keys(key, current.key)
            if comparison == 0:
                break
            # Step 2: remember the parent and keep searching down the matching side.
            parent = current
            current = current.left if comparison < 0 else current.right

        # VALIDATION: stop early when the requested key is not present.
        if current is None:
            return False

        # Step 2: when two children exist, swap with the in-order successor.
        if current.left is not None and current.right is not None:
            successor_parent = current
            successor = current.right
            # MAIN ITERATION LOOP: move left through the right subtree until the
            # smallest replacement key is found.
            while successor.left is not None:
                # Step 2a: keep descending left to find the in-order successor.
                successor_parent = successor
                successor = successor.left
            # Step 2b: copy the successor payload into the target node.
            current.key = successor.key
            current.value = successor.value
            parent = successor_parent
            current = successor

        # Step 3: delete the node that now has at most one child.
        child = current.left if current.left is not None else current.right

        # Step 4: reconnect the parent to the surviving child subtree.
        if parent is None:
            self._root = child
        elif parent.left is current:
            parent.left = child
        else:
            parent.right = child

        self._size -= 1
        return True
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Balance Analysis
    #
    # --------------------------------------------------------------- balance_report()
    def balance_report(self) -> list[BalanceReport]:
        """Return one :class:`BalanceReport` per node in post-order.

        Logic:
            This method computes node-level balance diagnostics for the whole
            tree.
            1. Walk the tree bottom-up so child heights are known first.
            2. Compute each node's balance factor from its left/right heights.
            3. Store a report row and the node's derived height for reuse.
        """
        # VALIDATION: empty trees have no node-level balance rows to report.
        if self._root is None:
            return []

        reports: list[BalanceReport] = []
        heights: dict[TreeNode, int] = {}
        stack: list[tuple[TreeNode, bool]] = [(self._root, False)]

        # MAIN ITERATION LOOP: compute subtree heights bottom-up.
        while stack:
            # Step 1: recover the next node together with its visit-state flag.
            current, visited = stack.pop()
            if visited:
                # Step 2: recover already-computed child heights.
                left_height = heights.get(current.left, -1)
                right_height = heights.get(current.right, -1)
                balance_factor = left_height - right_height
                # Step 3: capture the node-level report row before storing height.
                reports.append(
                    BalanceReport(
                        node_key=current.key,
                        left_height=left_height,
                        right_height=right_height,
                        balance_factor=balance_factor,
                        is_unbalanced=abs(balance_factor) > 1,
                    )
                )
                # Step 4: store the current node height for its parent calculations.
                heights[current] = 1 + max(left_height, right_height)
                continue

            # DISPATCH: first-visit nodes must schedule both children before revisiting.
            stack.append((current, True))
            if current.right is not None:
                stack.append((current.right, False))
            if current.left is not None:
                stack.append((current.left, False))

        return reports
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- height()
    def height(self) -> int:
        """Return the height of the tree using the Module 6 convention.

        Logic:
            This method computes tree height bottom-up using the Module 6
            convention.
            1. Return ``-1`` immediately when the tree is empty.
            2. Walk the tree bottom-up with an explicit stack so child heights
               are computed first.
            3. Return the stored height for the root node.
        """
        # VALIDATION: the Module 6 height convention uses ``-1`` for empty trees.
        if self._root is None:
            return -1

        heights: dict[TreeNode, int] = {}
        stack: list[tuple[TreeNode, bool]] = [(self._root, False)]

        # MAIN ITERATION LOOP: compute heights bottom-up without recursion.
        while stack:
            # Step 1: recover the next node together with its visit-state flag.
            current, visited = stack.pop()
            if visited:
                # Step 2: combine the previously computed child heights.
                left_height = heights.get(current.left, -1)
                right_height = heights.get(current.right, -1)
                heights[current] = 1 + max(left_height, right_height)
                continue
            # DISPATCH: first-visit nodes must revisit themselves after both children.
            stack.append((current, True))
            if current.right is not None:
                stack.append((current.right, False))
            if current.left is not None:
                stack.append((current.left, False))

        return heights[self._root]
    # --------------------------------------------------------------- end height()

    # --------------------------------------------------------------- is_balanced()
    def is_balanced(self) -> bool:
        """Return whether every node satisfies the balance rule.

        Logic:
            This method summarizes the node-level balance report into one
            boolean result.
            1. Build the current balance report for the tree.
            2. Check whether every reported node remains within the allowed
               balance threshold.
            3. Return the resulting boolean status.
        """
        return all(not report.is_unbalanced for report in self.balance_report())
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- worst_balance_factor()
    def worst_balance_factor(self) -> int:
        """Return the largest absolute balance factor in the tree.

        Logic:
            This method identifies the most extreme node imbalance currently
            present.
            1. Build the node-level balance report.
            2. Return ``0`` when the tree has no reported nodes.
            3. Return the maximum absolute balance factor across all reports.
        """
        reports = self.balance_report()
        if not reports:
            return 0
        return max(abs(report.balance_factor) for report in reports)
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- unbalanced_keys()
    def unbalanced_keys(self) -> list[object]:
        """Return the list of keys whose nodes are unbalanced.

        Logic:
            This method extracts only the keys that violate the balance rule.
            1. Build the current balance report.
            2. Filter the report rows to only the unbalanced nodes.
            3. Return the corresponding node keys.
        """
        return [
            report.node_key
            for report in self.balance_report()
            if report.is_unbalanced
        ]
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Display Helpers
    #
    # --------------------------------------------------------------- render_ascii()
    def render_ascii(self) -> str:
        """Render the tree as a simple ASCII diagram.

        Logic:
            1. Traverse the tree in pre-order using an explicit stack.
            2. Emit one connector-prefixed line per visited node.
            3. Push children in reverse display order so the left subtree
               renders above the right subtree.
        """
        # VALIDATION: empty trees use a stable placeholder string in the UI and tests.
        if self._root is None:
            return "(empty tree)"

        lines: list[str] = []
        stack: list[tuple[TreeNode, str, bool]] = [(self._root, "", True)]

        # MAIN ITERATION LOOP: walk the tree in pre-order and emit connectors.
        while stack:
            current, prefix, is_tail = stack.pop()
            # Step 1: emit the current node with the connector that matches its branch role.
            connector = "\\-- " if is_tail else "|-- "
            lines.append(f"{prefix}{connector}{current.key!r}")

            # Step 2: collect real children in logical left/right order.
            children = [child for child in (current.left, current.right) if child]
            child_prefix = prefix + ("    " if is_tail else "|   ")

            # Step 3: push children in reverse so the left child renders first.
            for index in range(len(children) - 1, -1, -1):
                child = children[index]
                child_is_tail = index == len(children) - 1
                stack.append((child, child_prefix, child_is_tail))

        return "\n".join(lines)
    # --------------------------------------------------------------- 

# -------------------------------------------------------------- end class BinarySearchTree

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------