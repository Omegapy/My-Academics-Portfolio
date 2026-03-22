# -------------------------------------------------------------------------
# File: complexity_analyzer.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Provides rules-based complexity lookup for Stack, Queue, and LinkedList.
# Provides Big-O predictions for time and space complexity along with
# explanations and use-case guidance.
# -------------------------------------------------------------------------

# --- Functions ---
# - get_complexity(): Single lookup for one (structure, operation) pair.
# - complexity_table(): All operations for a given structure.
# - comparison_table(): Cross-structure comparison for a logical task.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# -------------------------------------------------------------------------

"""
Provides rules-based complexity analysis for Stack, Queue, and LinkedList.

``COMPLEXITY_RULES`` are maped to a ``(structure, operation)`` tuple
to its predicted Big-O time complexity (average and worst case), space
complexity, a brief explanation of *why*, and a real-world use case.
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

# ==============================================================================
# CONSTANTS
# ==============================================================================

# ---- Complexity Rules Dictionary ----
# Keys: (structure_name, operation_name)
# Values: dict with time_avg, time_worst, space, explanation, use_case
COMPLEXITY_RULES: dict[tuple[str, str], dict[str, str]] = {
    # -----------------------------------------------------------------
    # Stack operations
    # -----------------------------------------------------------------
    ("Stack", "push"): {
        "time_avg": "O(1)",
        "time_worst": "O(1)",
        "space": "O(1)",
        "explanation": (
            "Creates a new node and updates the top pointer. "
            "No traversal required."
        ),
        "use_case": "Undo/redo systems, expression evaluation, backtracking.",
    },
    ("Stack", "pop"): {
        "time_avg": "O(1)",
        "time_worst": "O(1)",
        "space": "O(1)",
        "explanation": (
            "Saves the top node's data and advances the top pointer. "
            "No traversal required."
        ),
        "use_case": "Processing items in reverse order, balanced parentheses.",
    },
    ("Stack", "peek"): {
        "time_avg": "O(1)",
        "time_worst": "O(1)",
        "space": "O(1)",
        "explanation": "Returns the top node's data without modifying the stack.",
        "use_case": "Checking the most recent item without consuming it.",
    },
    ("Stack", "display"): {
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(n)",
        "explanation": (
            "Traverses every node from top to bottom to collect values."
        ),
        "use_case": "Debugging and visualizing stack contents.",
    },
    # -----------------------------------------------------------------
    # Queue operations
    # -----------------------------------------------------------------
    ("Queue", "enqueue"): {
        "time_avg": "O(1)",
        "time_worst": "O(1)",
        "space": "O(1)",
        "explanation": (
            "Creates a new node and updates the rear pointer. "
            "Front and rear pointers eliminate the need for traversal."
        ),
        "use_case": "Task scheduling, BFS, print job queues.",
    },
    ("Queue", "dequeue"): {
        "time_avg": "O(1)",
        "time_worst": "O(1)",
        "space": "O(1)",
        "explanation": (
            "Saves the front node's data and advances the front pointer. "
            "Resets rear to None if the queue becomes empty."
        ),
        "use_case": "Processing tasks in arrival order.",
    },
    ("Queue", "front"): {
        "time_avg": "O(1)",
        "time_worst": "O(1)",
        "space": "O(1)",
        "explanation": "Returns the front node's data without modifying the queue.",
        "use_case": "Peeking at the next item to be processed.",
    },
    ("Queue", "display"): {
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(n)",
        "explanation": (
            "Traverses every node from front to rear to collect values."
        ),
        "use_case": "Debugging and visualizing queue contents.",
    },
    # -----------------------------------------------------------------
    # LinkedList operations
    # -----------------------------------------------------------------
    ("LinkedList", "prepend"): {
        "time_avg": "O(1)",
        "time_worst": "O(1)",
        "space": "O(1)",
        "explanation": (
            "Creates a new node pointing to the current head, then updates "
            "head. No traversal required."
        ),
        "use_case": "Building a list when insertion order does not matter.",
    },
    ("LinkedList", "append"): {
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(1)",
        "explanation": (
            "Must traverse the entire list to find the tail node because "
            "this implementation has no tail pointer."
        ),
        "use_case": "Maintaining insertion order when appending is infrequent.",
    },
    ("LinkedList", "insert_after"): {
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(1)",
        "explanation": (
            "Searches for the target node (O(n) traversal), then splices "
            "in the new node (O(1))."
        ),
        "use_case": "Inserting at a known position within a chain of records.",
    },
    ("LinkedList", "delete"): {
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(1)",
        "explanation": (
            "Traverses with a previous pointer to find and unlink the node. "
            "Best case O(1) if deleting head, but worst/average is O(n)."
        ),
        "use_case": "Removing a specific record from an ordered collection.",
    },
    ("LinkedList", "search"): {
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(1)",
        "explanation": (
            "Linear scan from head to tail comparing each node's data. "
            "No indexing or binary search is possible."
        ),
        "use_case": "Checking membership in a small, unsorted collection.",
    },
    ("LinkedList", "display"): {
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(n)",
        "explanation": (
            "Traverses every node from head to tail to collect values."
        ),
        "use_case": "Debugging and visualizing list contents.",
    },
}

# ---- Cross-structure comparison mappings ----
# Maps a logical task name to the (structure, operation) keys to compare.
_COMPARISON_MAP: dict[str, list[tuple[str, str]]] = {
    "primary_insert": [
        ("Stack", "push"),
        ("Queue", "enqueue"),
        ("LinkedList", "prepend"),
    ],
    "insert_front": [
        ("Stack", "push"),
        ("LinkedList", "prepend"),
    ],
    "insert_back": [
        ("Queue", "enqueue"),
        ("LinkedList", "append"),
    ],
    "search": [
        ("LinkedList", "search"),
    ],
    "peek": [
        ("Stack", "peek"),
        ("Queue", "front"),
    ],
    "display": [
        ("Stack", "display"),
        ("Queue", "display"),
        ("LinkedList", "display"),
    ],
}

# ==============================================================================
# FUNCTIONS
# ==============================================================================

# -------------------------------------------------------------- get_complexity()
def get_complexity(structure: str, operation: str) -> dict[str, str]:
    """Look up the complexity info for a single (structure, operation) pair.

    Args:
        structure: Data structure name (e.g., ``"Stack"``, ``"Queue"``,
            ``"LinkedList"``). Case-sensitive.
        operation: Operation name (e.g., ``"push"``, ``"append"``).

    Returns:
        A dict with keys ``time_avg``, ``time_worst``, ``space``,
        ``explanation``, and ``use_case``.

    Raises:
        KeyError: If the (structure, operation) pair is not in the rules.
    """
    key = (structure, operation)
    if key not in COMPLEXITY_RULES:
        raise KeyError(
            f"No complexity rule for ({structure!r}, {operation!r}). "
            f"Available structures: Stack, Queue, LinkedList."
        )
    return COMPLEXITY_RULES[key]
# -------------------------------------------------------------- end get_complexity()


# -------------------------------------------------------------- complexity_table()
def complexity_table(structure: str) -> list[dict[str, str]]:
    """Return complexity info for all operations of a given structure.

    Args:
        structure: Data structure name (``"Stack"``, ``"Queue"``, or
            ``"LinkedList"``).

    Returns:
        A list of dicts, each containing ``operation`` plus the standard
        complexity fields.
    """
    rows: list[dict[str, str]] = []
    for (struct, op), info in COMPLEXITY_RULES.items():
        if struct == structure:
            row = {"operation": op}
            row.update(info)
            rows.append(row)
    return rows
# -------------------------------------------------------------- end complexity_table()


# -------------------------------------------------------------- comparison_table()
def comparison_table(operation_type: str) -> list[dict[str, str]]:
    """Cross-structure comparison for a logical operation type.

    Args:
        operation_type: One of ``"primary_insert"``, ``"insert_front"``,
            ``"insert_back"``, ``"search"``, ``"peek"``, or ``"display"``.

    Returns:
        A list of dicts, each with ``structure``, ``operation``, and
        the standard complexity fields.

    Raises:
        KeyError: If the operation_type is not recognized.
    """
    if operation_type not in _COMPARISON_MAP:
        raise KeyError(
            f"Unknown operation type {operation_type!r}. "
            f"Available: {list(_COMPARISON_MAP.keys())}"
        )
    rows: list[dict[str, str]] = []
    for struct, op in _COMPARISON_MAP[operation_type]:
        info = COMPLEXITY_RULES[(struct, op)]
        row = {"structure": struct, "operation": op}
        row.update(info)
        rows.append(row)
    return rows
# -------------------------------------------------------------- end comparison_table()

# ==============================================================================
# End of File
# ==============================================================================
