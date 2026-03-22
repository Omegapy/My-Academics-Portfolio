# -------------------------------------------------------------------------
# File: display_helpers.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Display functions for Stack, Queue, and
# LinkedList states in the console, and provides explanations
# about each data structure's behavior and complexity.
# -------------------------------------------------------------------------

# --- Functions ---
# - display_structure_definition(): Show the introductory explanation for a data structure.
# - display_operation_preview(): Show a pre-execution explanation for an operation.
# - display_stack_state(): Render a vertical stack diagram with TOP arrow.
# - display_queue_state(): Render a horizontal queue with FRONT/REAR labels.
# - display_linked_list_state(): Render a node chain with HEAD label.
# - display_operation_result(): Show a colored operation result confirmation.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - shutil.get_terminal_size for console-aware text wrapping.
# - textwrap.fill for aligned educational text formatting.
# - typing.Any for flexible value types.
# - colorama.Fore for colored terminal output.
# -------------------------------------------------------------------------

"""
Display helpers for data structure state.

Provides ASCII-art diagrams for Stack (vertical), Queue (horizontal),
and LinkedList (chain), as well as colored operation results and
educational explanations.
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from shutil import get_terminal_size
from textwrap import fill
from typing import Any

from colorama import Fore

# ==============================================================================
# CONSTANTS — Educational Explanations
# ==============================================================================

# Structure-level definitions keyed by structure name
STRUCTURE_DEFINITIONS: dict[str, str] = {
    "Stack": (
        "A stack stores items in Last-In, First-Out (LIFO) order.\n"
        "Items are added and removed only from the top.\n"
        "Complexity -> push O(1), pop O(1), peek O(1), and "
        "display O(n) are worst-case estimates.\n\n"
    ),
    "Queue": (
        "A queue stores items in First-In, First-Out (FIFO) order.\n"
        "Items enter at the rear and leave from the front.\n"
        "Complexity -> enqueue O(1), dequeue O(1), front O(1), display O(n).\n\n"
    ),
    "LinkedList": (
        "A linked list stores an ordered list of items in nodes, and each node stores "
        "data plus a pointer to the next node.\n"
        "Access proceeds by following nodes from the head through the chain.\n"
        "Complexity -> prepend O(1), append O(n), insert-after O(n) if the "
        "target must be located first, delete O(n), search O(n), and display O(n).\n\n"
    ),
}

# Stack explanations keyed by operation name
STACK_EXPLANATIONS: dict[str, str] = {
    "push": (
        "Push adds '{value}' to the top of the stack.\n"
        "  Time Complexity: O(1) because only the top pointer changes."
    ),
    "pop": (
        "Pop removes the current top item from the stack.\n"
        "  Time Complexity: O(1) because only the top pointer is advanced."
    ),
    "peek": (
        "Peek reads the current top item without removing it.\n"
        "  Time Complexity: O(1) because the top pointer is accessed directly."
    ),
    "display": (
        "Display traverses the stack from top to bottom.\n"
        "  Time Complexity: O(n) because each node is visited once."
    ),
}

# Queue explanations keyed by operation name
QUEUE_EXPLANATIONS: dict[str, str] = {
    "enqueue": (
        "Enqueue adds '{value}' at the rear of the queue.\n"
        "  Time Complexity: O(1) because only the rear pointer changes."
    ),
    "dequeue": (
        "Dequeue removes the item at the front of the queue.\n"
        "  Time Complexity: O(1) because only the front pointer is advanced."
    ),
    "front": (
        "Front reads the next item to leave the queue without removing it.\n"
        "  Time Complexity: O(1) because the front pointer is accessed directly."
    ),
    "display": (
        "Display traverses the queue from front to rear.\n"
        "  Time Complexity: O(n) because each node is visited once."
    ),
}

# Linked list explanations keyed by operation name
LINKED_LIST_EXPLANATIONS: dict[str, str] = {
    "prepend": (
        "Prepend adds '{value}' before the current head node.\n"
        "  Time Complexity: O(1) because no traversal is needed."
    ),
    "append": (
        "Append adds '{value}' at the end of the linked list.\n"
        "  Time Complexity: O(n) because the list may need to be traversed node by node."
    ),
    "insert_after": (
        "Insert After looks for '{target}' and places '{value}' immediately after it.\n"
        "  Time Complexity: O(n) because the target node must be found first."
    ),
    "delete": (
        "Delete searches for '{value}' and removes the first matching node.\n"
        "  Time Complexity: O(n) in the general case because traversal may be needed."
    ),
    "search": (
        "Search checks nodes one by one for '{value}'.\n"
        "  Time Complexity: O(n) because the list may need a full linear scan."
    ),
    "display": (
        "Display traverses the linked list from head to tail.\n"
        "  Time Complexity: O(n) because each node is visited once."
    ),
}

# ==============================================================================
# DISPLAY FUNCTIONS
# ==============================================================================

# -------------------------------------------------------------- _print_wrapped_text()
def _print_wrapped_text(text: str, color: str, indent: str = "  ") -> None:
    """Print multi-line educational text with consistent indentation and wrapping.

    Args:
        text: Text block that may contain explicit newline separators.
        color: Colorama color prefix to apply to each rendered line.
        indent: Left padding to apply to wrapped lines.
    """
    terminal_width = get_terminal_size(fallback=(80, 24)).columns
    wrap_width = max(40, terminal_width - len(indent))

    for raw_line in text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            print()
            continue
        wrapped_line = fill(
            stripped_line,
            width=wrap_width,
            initial_indent=indent,
            subsequent_indent=indent,
        )
        for output_line in wrapped_line.splitlines():
            print(color + output_line)
# -------------------------------------------------------------- end _print_wrapped_text()

# -------------------------------------------------------------- display_structure_definition()
def display_structure_definition(structure_name: str, definition: str) -> None:
    """Display an introductory explanation for a data structure.

    Args:
        structure_name: Name of the data structure being introduced.
        definition: Multi-line educational description for the structure.
    """
    print(Fore.MAGENTA + f"\n  What Is a {structure_name}?")
    _print_wrapped_text(definition, Fore.WHITE)
# -------------------------------------------------------------- end display_structure_definition()


# -------------------------------------------------------------- display_operation_preview()
def display_operation_preview(operation: str, explanation: str) -> None:
    """Display a pre-execution explanation for an operation.

    Args:
        operation: Name of the operation that is about to run.
        explanation: Multi-line educational description for the operation.
    """
    print(Fore.BLUE + f"\n  Before {operation}:")
    _print_wrapped_text(explanation, Fore.WHITE)
# -------------------------------------------------------------- end display_operation_preview()

# -------------------------------------------------------------- display_stack_state()
def display_stack_state(values: list[Any]) -> None:
    """Render a vertical stack diagram with a TOP arrow.

    Args:
        values: List of values from top to bottom (as returned by Stack.to_list()).

    Example output::

        TOP -> | 30 |
               | 20 |
               | 10 |
               +----+
    """
    if not values:
        print(Fore.YELLOW + "  Stack is empty.")
        return

    # Step 1: Determine cell width based on longest value string
    str_values = [str(v) for v in values]
    width = max(len(s) for s in str_values) + 2  # padding

    # Step 2: Render each row
    for i, s in enumerate(str_values):
        cell = s.center(width)
        if i == 0:
            print(Fore.CYAN + f"  TOP -> | {cell} |")
        else:
            prefix = " " * len("  TOP -> ")
            print(Fore.CYAN + f"{prefix}| {cell} |")

    # Step 3: Render bottom border
    bottom_prefix = " " * len("  TOP -> ")
    print(Fore.CYAN + f"{bottom_prefix}+{'-' * (width + 2)}+")
# -------------------------------------------------------------- end display_stack_state()


# -------------------------------------------------------------- display_queue_state()
def display_queue_state(values: list[Any]) -> None:
    """Render a horizontal queue diagram with FRONT and REAR labels.

    Args:
        values: List of values from front to rear (as returned by Queue.to_list()).

    Example output::

        FRONT -> [10] -> [20] -> [30] <- REAR
    """
    if not values:
        print(Fore.YELLOW + "  Queue is empty.")
        return

    # Step 1: Build the chain of bracketed values
    chain = " -> ".join(f"[{v}]" for v in values)
    print(Fore.CYAN + f"  FRONT -> {chain} <- REAR")
# -------------------------------------------------------------- end display_queue_state()


# -------------------------------------------------------------- display_linked_list_state()
def display_linked_list_state(values: list[Any]) -> None:
    """Render a linked list node chain with HEAD label.

    Args:
        values: List of values from head to tail (as returned by LinkedList.to_list()).

    Example output::

        HEAD -> [10] -> [20] -> [30] -> None
    """
    if not values:
        print(Fore.YELLOW + "  LinkedList is empty.")
        return

    # Step 1: Build the chain of bracketed values ending with None
    chain = " -> ".join(f"[{v}]" for v in values)
    print(Fore.CYAN + f"  HEAD -> {chain} -> None")
# -------------------------------------------------------------- end display_linked_list_state()


# -------------------------------------------------------------- display_operation_result()
def display_operation_result(operation: str, value: Any, explanation: str) -> None:
    """Display a colored operation result confirmation.

    Args:
        operation: Name of the operation performed (e.g., "Push", "Dequeue").
        value: The value involved in the operation.
        explanation: Educational text about the operation's behavior and complexity.
    """
    print(Fore.GREEN + f"\n  {operation}: {value}")
# -------------------------------------------------------------- end display_operation_result()

# ==============================================================================
# End of File
# ==============================================================================
