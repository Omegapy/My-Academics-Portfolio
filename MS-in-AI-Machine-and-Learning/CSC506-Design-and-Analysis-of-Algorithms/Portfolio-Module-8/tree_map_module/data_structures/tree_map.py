# -------------------------------------------------------------------------
# File: tree_map.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-26
# File Path: Portfolio-Milestone-Module-6/data_structures/tree_map.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026

# -------------------------------------------------------------------------
# --- Module Functionality ---
# - Expose map-style put/get/delete behavior through BST composition.
# - Reuse BST traversal, min/max, and balance helpers for key-value storage.
# - Provide the tree-backed mapping surface used by labs and benchmarks.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Class Definitions - Regular Classes: ``Map`` wraps a backing
#   ``BinarySearchTree`` and exposes key-value operations.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: none beyond ``__future__`` annotations
# - Third-Party: none
# - Local Project Modules:
#   - data_structures.binary_search_tree
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the Streamlit map lab, guided validation demos, and benchmarks.
# - Serves as the tree-backed mapping interface for Module 6.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""BST-backed Map implementation.

This module wraps the binary search tree in a map-style interface so the
labs, validation helpers, and benchmark pipeline can store key-value pairs
while still reusing BST traversal, balance, and rendering behavior.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from tree_map_module.data_structures.binary_search_tree import BinarySearchTree


# __________________________________________________________________________
# Class Definitions - Regular Classes
# ========================================================================
# CLASS DEFINITIONS
# ========================================================================
# ``Map`` exposes familiar key-value behavior while delegating ordering,
# traversal, and balance reporting to the plain binary search tree.
#
# ------------------------------------------------------------------------- class Map
class Map:
    """Map abstraction backed by a plain binary search tree.

    Attributes:
        _tree: Backing binary search tree that stores all key-value pairs.

    Logic:
        1. Delegate storage and ordering to the backing binary search tree.
        2. Expose map-style put/get/delete helpers on top of that tree.
        3. Reuse traversal, balance, and display helpers for the Module 6 labs.
    """

    # ________________________________________________
    # Construction
    #
    # --------------------------------------------------------------- __init__()
    def __init__(
        self,
        items: list[tuple[object, object]] | None = None,
    ) -> None:
        """Initialize the map with optional key-value pairs.

        Logic:
            This method creates the BST-backed mapping surface for Module 6.
            1. Build the backing binary search tree.
            2. Preload any provided key-value pairs through the tree
               constructor.
        """
        self._tree: BinarySearchTree = BinarySearchTree(items)
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Mutation Helpers
    #
    # --------------------------------------------------------------- put()
    def put(self, key: object, value: object) -> None:
        """Insert or update ``key`` with ``value``.

        Logic:
            This method delegates map-style writes to the backing BST.
            1. Pass the provided key and value into the tree insert helper.
            2. Let the tree decide whether to add a new node or update an
               existing one.
        """
        self._tree.insert(key, value)
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- get()
    def get(self, key: object, default: object | None = None) -> object | None:
        """Return the value for ``key`` or the provided default.

        Logic:
            This method preserves normal mapping lookup behavior on top of the
            BST node search.
            1. Search the backing tree for the requested key.
            2. Return the caller-provided default when the key is absent.
            3. Return the node payload when the key is present.
        """
        node = self._tree.search(key)
        # VALIDATION: preserve mapping semantics by returning the caller's
        # default when the tree does not contain the requested key.
        if node is None:
            return default
        return node.value
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- delete()
    def delete(self, key: object) -> bool:
        """Delete ``key`` from the map when present.

        Logic:
            This method forwards deletion responsibility to the backing BST.
            1. Ask the tree to remove the requested key.
            2. Return the tree's success flag to the caller.
        """
        return self._tree.delete(key)
    # --------------------------------------------------------------- 

    # ________________________________________________
    # Read-Only Views
    #
    # --------------------------------------------------------------- contains_key()
    def contains_key(self, key: object) -> bool:
        """Return whether ``key`` exists in the map.

        Logic:
            This method exposes tree membership through a map-style name.
            1. Delegate the membership check to the backing BST.
            2. Return the resulting boolean status.
        """
        return self._tree.contains(key)
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- min_key()
    def min_key(self) -> object | None:
        """Return the minimum key or ``None`` when the map is empty.

        Logic:
            This method exposes the backing tree's smallest stored key.
            1. Ask the tree for its minimum key.
            2. Return that key or ``None`` when no nodes exist.
        """
        return self._tree.min_key()
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- max_key()
    def max_key(self) -> object | None:
        """Return the maximum key or ``None`` when the map is empty.

        Logic:
            This method exposes the backing tree's largest stored key.
            1. Ask the tree for its maximum key.
            2. Return that key or ``None`` when no nodes exist.
        """
        return self._tree.max_key()
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- keys()
    def keys(self, order: str = "inorder") -> list[object]:
        """Return keys in the requested traversal order.

        Logic:
            This method projects only keys from the tree's ordered item view.
            1. Request the ordered key-value pairs from the backing tree.
            2. Extract each key in traversal order.
            3. Return the resulting key list.
        """
        return [key for key, _ in self._tree.items(order)]
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- values()
    def values(self, order: str = "inorder") -> list[object]:
        """Return values in the requested traversal order.

        Logic:
            This method projects only values from the tree's ordered item view.
            1. Request the ordered key-value pairs from the backing tree.
            2. Extract each value in traversal order.
            3. Return the resulting value list.
        """
        return [value for _, value in self._tree.items(order)]
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- items()
    def items(self, order: str = "inorder") -> list[tuple[object, object]]:
        """Return key-value pairs in the requested traversal order.

        Logic:
            This method exposes the tree's ordered mapping contents as plain
            tuple pairs.
            1. Request the ordered items from the backing BST.
            2. Rebuild them into a fresh list of key-value tuples.
            3. Return the copied traversal result.
        """
        # DISPATCH: defer ordering policy to the backing BST traversal helper.
        return [
            (key, value)
            for key, value in self._tree.items(order)
        ]
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- height()
    def height(self) -> int:
        """Return the height of the backing tree.

        Logic:
            This method forwards the tree-height query through the map
            interface.
            1. Ask the backing BST for its current height.
            2. Return that height value.
        """
        return self._tree.height()
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- is_balanced()
    def is_balanced(self) -> bool:
        """Return whether the backing tree is balanced.

        Logic:
            This method exposes the BST balance check through the map surface.
            1. Ask the backing tree whether its balance condition holds.
            2. Return that boolean result.
        """
        return self._tree.is_balanced()
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- render_ascii()
    def render_ascii(self) -> str:
        """Return an ASCII diagram of the backing tree.

        Logic:
            This method exposes the tree's display helper for the map lab.
            1. Ask the backing BST to render its current structure.
            2. Return the resulting ASCII diagram string.
        """
        return self._tree.render_ascii()
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- clear()
    def clear(self) -> None:
        """Remove all key-value pairs from the map.

        Logic:
            This method resets the map by clearing the backing tree.
            1. Delegate the clear operation to the BST.
            2. Leave the map ready for fresh insertions.
        """
        self._tree.clear()
    # --------------------------------------------------------------- 

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of stored key-value pairs.

        Logic:
            This method reports the current mapping size from the backing tree.
            1. Ask the tree for its current node count.
            2. Return that count to the caller.
        """
        return len(self._tree)
    # --------------------------------------------------------------- 

# ------------------------------------------------------------------------- end class Map

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------
