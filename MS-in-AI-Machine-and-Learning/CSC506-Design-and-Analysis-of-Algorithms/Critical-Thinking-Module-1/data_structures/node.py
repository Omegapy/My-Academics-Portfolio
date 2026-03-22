# -------------------------------------------------------------------------
# File: node.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Provides the shared Node dataclass used as the building block for
# Stack, Queue, and LinkedList data structures.
# -------------------------------------------------------------------------

# --- Classes ---
# - Node: A singly-linked node holding arbitrary data and a next-node pointer.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - dataclasses.dataclass for concise data container declaration.
# - typing.Any to allow storing any data type.
# -------------------------------------------------------------------------

"""
Shared Node dataclass for linked data structures.

The Node class serves as the fundamental building block for the Stack,
Queue, and LinkedList implementations. Each node stores a data value
and a reference to the next node in the chain.
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# ==============================================================================
# DATA CLASSES
# ==============================================================================

# ------------------------------------------------------------------------- class Node
@dataclass(slots=True)
class Node:
    """A singly-linked node that stores data and a reference to the next node.

    This dataclass is the shared building block for Stack, Queue, and
    LinkedList. Using ``next_node`` instead of ``next`` avoids shadowing
    the Python built-in.

    Attributes:
        data: The value stored in this node (any type).
        next_node: Reference to the next Node in the chain, or None if
            this is the last node.
    """

    data: Any
    next_node: Node | None = None

# ------------------------------------------------------------------------- end class Node

# ==============================================================================
# End of File
# ==============================================================================
