# -------------------------------------------------------------------------
# File: __init__.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

"""Data structures package — exports Node, Stack, Queue, and LinkedList."""

from data_structures.node import Node
from data_structures.stack_ds import Stack
from data_structures.queue_ds import Queue
from data_structures.linked_list_ds import LinkedList

__all__ = ["Node", "Stack", "Queue", "LinkedList"]
