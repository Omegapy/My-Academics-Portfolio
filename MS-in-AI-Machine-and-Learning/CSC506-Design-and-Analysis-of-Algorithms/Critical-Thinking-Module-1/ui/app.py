# -------------------------------------------------------------------------
# File: app.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Main application loop and menus for the CTA-1
# data structures demonstration. Uses Banner and Menu from
# the utilities package.
# -------------------------------------------------------------------------

# --- Functions ---
# - display_welcome_banner(): Show the welcome banner with course info.
# - run_stack_menu(): Interactive sub-menu for Stack operations.
# - run_queue_menu(): Interactive sub-menu for Queue operations.
# - run_linked_list_menu(): Interactive sub-menu for LinkedList operations.
# - _seed_sample_data(): Pre-populate data structures with sample data.
# - run_application(): Main menu loop routing to sub-menus.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - sys for clean exit.
# - colorama.Fore for colored terminal output.
# - utilities: Banner, Menu, validation functions.
# - data_structures: Stack, Queue, LinkedList.
# - ui.display_helpers: visual rendering and explanations.
# -------------------------------------------------------------------------

"""
Main application module for the CTA-1 data structures demonstration.

It is a console UI that lets the user perform Stack,
Queue, and LinkedList operations.
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

import sys

from colorama import Fore

from utilities.menu_banner_utilities import Banner, Menu
from utilities.validation_utilities import (
    validate_prompt_int,
    validate_prompt_string,
    wait_for_enter,
)

from data_structures.stack_ds import Stack
from data_structures.queue_ds import Queue
from data_structures.linked_list_ds import LinkedList

from ui.display_helpers import (
    STRUCTURE_DEFINITIONS,
    display_stack_state,
    display_queue_state,
    display_linked_list_state,
    display_structure_definition,
    display_operation_preview,
    display_operation_result,
    STACK_EXPLANATIONS,
    QUEUE_EXPLANATIONS,
    LINKED_LIST_EXPLANATIONS,
)

# ==============================================================================
# WELCOME BANNER
# ==============================================================================

# -------------------------------------------------------------- display_welcome_banner()
def display_welcome_banner() -> None:
    """Display the welcome banner with course and assignment information."""
    banner = Banner([
        ("CSC506 – Design and Analysis of Algorithms", "center", True),
        ("CTA-1: Data Structures Demo", "center", False),
        ("", "center", False),
        ("Stack | Queue | Linked List", "center", True),
        ("Author: Alexander Ricciardi", "center", False),
        ("Spring A (26SA) – 2026", "center", False),
    ])
    print(Fore.CYAN + banner.render())
    print()
# -------------------------------------------------------------- end display_welcome_banner()

# ==============================================================================
# STACK SUB-MENU
# ==============================================================================

# -------------------------------------------------------------- run_stack_menu()
def run_stack_menu(stack: Stack) -> None:
    """Run the interactive Stack operations sub-menu.

    Args:
        stack: The Stack instance to operate on.

    Logic:
        1. Display the Stack menu with Push, Pop, Peek, Display, Back options.
        2. Route user choice to the appropriate Stack operation.
        3. Show visual state and educational explanation after each operation.
        4. Loop until the user selects Back.
    """
    menu = Menu("Stack Operations", ["Push", "Pop", "Peek", "Display", "Back"])
    show_definition = True

    while True:
        print()
        print(Fore.CYAN + menu.render())
        if show_definition:
            display_structure_definition("Stack", STRUCTURE_DEFINITIONS["Stack"])
            show_definition = False
        choice = validate_prompt_int("Enter choice (1-5): ")

        # --- Push ---
        if choice == 1:
            value = validate_prompt_string("Enter value to push: ")
            display_operation_preview("Push", STACK_EXPLANATIONS["push"].format(value=value))
            stack.push(value)
            display_operation_result("Pushed", value, STACK_EXPLANATIONS["push"].format(value=value))
            print()
            display_stack_state(stack.to_list())

        # --- Pop ---
        elif choice == 2:
            display_operation_preview("Pop", STACK_EXPLANATIONS["pop"])
            try:
                value = stack.pop()
                display_operation_result("Popped", value, STACK_EXPLANATIONS["pop"])
            except IndexError:
                print(Fore.RED + "\n  Error: Cannot pop from an empty stack.")
            print()
            display_stack_state(stack.to_list())

        # --- Peek ---
        elif choice == 3:
            display_operation_preview("Peek", STACK_EXPLANATIONS["peek"])
            try:
                value = stack.peek()
                display_operation_result("Top element", value, STACK_EXPLANATIONS["peek"])
            except IndexError:
                print(Fore.RED + "\n  Error: Cannot peek on an empty stack.")

        # --- Display ---
        elif choice == 4:
            display_operation_preview("Display", STACK_EXPLANATIONS["display"])
            print(Fore.WHITE + f"\n  Stack size: {stack.size()}")
            display_stack_state(stack.to_list())

        # --- Back ---
        elif choice == 5:
            return

        else:
            print(Fore.RED + "  Invalid choice. Please enter 1-5.")

        wait_for_enter()

# -------------------------------------------------------------- end run_stack_menu()

# ==============================================================================
# QUEUE SUB-MENU
# ==============================================================================

# -------------------------------------------------------------- run_queue_menu()
def run_queue_menu(queue: Queue) -> None:
    """Run the interactive Queue operations sub-menu.

    Args:
        queue: The Queue instance to operate on.

    Logic:
        1. Display the Queue menu with Enqueue, Dequeue, Front, Display, Back.
        2. Route user choice to the appropriate Queue operation.
        3. Show visual state and educational explanation after each operation.
        4. Loop until the user selects Back.
    """
    menu = Menu("Queue Operations", ["Enqueue", "Dequeue", "Front", "Display", "Back"])
    show_definition = True

    while True:
        print()
        print(Fore.CYAN + menu.render())
        if show_definition:
            display_structure_definition("Queue", STRUCTURE_DEFINITIONS["Queue"])
            show_definition = False
        choice = validate_prompt_int("Enter choice (1-5): ")

        # --- Enqueue ---
        if choice == 1:
            value = validate_prompt_string("Enter value to enqueue: ")
            display_operation_preview("Enqueue", QUEUE_EXPLANATIONS["enqueue"].format(value=value))
            queue.enqueue(value)
            display_operation_result("Enqueued", value, QUEUE_EXPLANATIONS["enqueue"].format(value=value))
            print()
            display_queue_state(queue.to_list())

        # --- Dequeue ---
        elif choice == 2:
            display_operation_preview("Dequeue", QUEUE_EXPLANATIONS["dequeue"])
            try:
                value = queue.dequeue()
                display_operation_result("Dequeued", value, QUEUE_EXPLANATIONS["dequeue"])
            except IndexError:
                print(Fore.RED + "\n  Error: Cannot dequeue from an empty queue.")
            print()
            display_queue_state(queue.to_list())

        # --- Front ---
        elif choice == 3:
            display_operation_preview("Front", QUEUE_EXPLANATIONS["front"])
            try:
                value = queue.front()
                display_operation_result("Front element", value, QUEUE_EXPLANATIONS["front"])
            except IndexError:
                print(Fore.RED + "\n  Error: Cannot peek front on an empty queue.")

        # --- Display ---
        elif choice == 4:
            display_operation_preview("Display", QUEUE_EXPLANATIONS["display"])
            print(Fore.WHITE + f"\n  Queue size: {queue.size()}")
            display_queue_state(queue.to_list())

        # --- Back ---
        elif choice == 5:
            return

        else:
            print(Fore.RED + "  Invalid choice. Please enter 1-5.")

        wait_for_enter()

# -------------------------------------------------------------- end run_queue_menu()

# ==============================================================================
# LINKED LIST SUB-MENU
# ==============================================================================

# -------------------------------------------------------------- run_linked_list_menu()
def run_linked_list_menu(linked_list: LinkedList) -> None:
    """Run the interactive LinkedList operations sub-menu.

    Args:
        linked_list: The LinkedList instance to operate on.

    Logic:
        1. Display the LinkedList menu with Prepend, Append, Insert After,
           Delete, Search, Display, Back options.
        2. Route user choice to the appropriate LinkedList operation.
        3. Show visual state and educational explanation after each operation.
        4. Loop until the user selects Back.
    """
    menu = Menu(
        "Linked List Operations",
        ["Prepend", "Append", "Insert After", "Delete", "Search", "Display", "Back"],
    )
    show_definition = True

    while True:
        print()
        print(Fore.CYAN + menu.render())
        if show_definition:
            display_structure_definition("Linked List", STRUCTURE_DEFINITIONS["LinkedList"])
            show_definition = False
        choice = validate_prompt_int("Enter choice (1-7): ")

        # --- Prepend ---
        if choice == 1:
            value = validate_prompt_string("Enter value to prepend: ")
            display_operation_preview(
                "Prepend",
                LINKED_LIST_EXPLANATIONS["prepend"].format(value=value),
            )
            linked_list.prepend(value)
            display_operation_result(
                "Prepended",
                value,
                LINKED_LIST_EXPLANATIONS["prepend"].format(value=value),
            )
            print()
            display_linked_list_state(linked_list.to_list())

        # --- Append ---
        elif choice == 2:
            value = validate_prompt_string("Enter value to append: ")
            display_operation_preview(
                "Append",
                LINKED_LIST_EXPLANATIONS["append"].format(value=value),
            )
            linked_list.append(value)
            display_operation_result(
                "Appended",
                value,
                LINKED_LIST_EXPLANATIONS["append"].format(value=value),
            )
            print()
            display_linked_list_state(linked_list.to_list())

        # --- Insert After ---
        elif choice == 3:
            target = validate_prompt_string("Enter target value to insert after: ")
            value = validate_prompt_string("Enter new value to insert: ")
            display_operation_preview(
                "Insert After",
                LINKED_LIST_EXPLANATIONS["insert_after"].format(target=target, value=value),
            )
            if linked_list.insert_after(target, value):
                display_operation_result(
                    f"Inserted '{value}' after '{target}'",
                    value,
                    LINKED_LIST_EXPLANATIONS["insert_after"].format(target=target, value=value),
                )
            else:
                print(Fore.RED + f"\n  Error: Target value '{target}' not found in the list.")
            print()
            display_linked_list_state(linked_list.to_list())

        # --- Delete ---
        elif choice == 4:
            value = validate_prompt_string("Enter value to delete: ")
            display_operation_preview(
                "Delete",
                LINKED_LIST_EXPLANATIONS["delete"].format(value=value),
            )
            if linked_list.delete(value):
                display_operation_result(
                    "Deleted",
                    value,
                    LINKED_LIST_EXPLANATIONS["delete"].format(value=value),
                )
            else:
                print(Fore.RED + f"\n  Error: Value '{value}' not found in the list.")
            print()
            display_linked_list_state(linked_list.to_list())

        # --- Search ---
        elif choice == 5:
            value = validate_prompt_string("Enter value to search for: ")
            display_operation_preview(
                "Search",
                LINKED_LIST_EXPLANATIONS["search"].format(value=value),
            )
            if linked_list.search(value):
                print(Fore.GREEN + f"\n  Found: '{value}' exists in the list.")
            else:
                print(Fore.YELLOW + f"\n  Not Found: '{value}' is not in the list.")

        # --- Display ---
        elif choice == 6:
            display_operation_preview("Display", LINKED_LIST_EXPLANATIONS["display"])
            print(Fore.WHITE + f"\n  List size: {linked_list.size()}")
            display_linked_list_state(linked_list.to_list())

        # --- Back ---
        elif choice == 7:
            return

        else:
            print(Fore.RED + "  Invalid choice. Please enter 1-7.")

        wait_for_enter()

# -------------------------------------------------------------- end run_linked_list_menu()

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

# -------------------------------------------------------------- run_application()
def _seed_sample_data(stack: Stack, queue: Queue, linked_list: LinkedList) -> None:
    """Pre-populate data structures with sample data for immediate demo use.

    Args:
        stack: The Stack instance to populate.
        queue: The Queue instance to populate.
        linked_list: The LinkedList instance to populate.
    """
    for v in ("A", "B", "C"):
        stack.push(v)
    for v in ("X", "Y", "Z"):
        queue.enqueue(v)
    for v in ("10", "20", "30"):
        linked_list.append(v)


def run_application() -> None:
    """Run the main CTA-1 data structures demonstration application.

    Logic:
        1. Display the welcome banner.
        2. Create persistent instances of Stack, Queue, and LinkedList.
        3. Main loop: render main menu, route to menus, repeat.
        4. Exit cleanly when the user selects Exit.
    """
    # Step 1: Display welcome banner
    display_welcome_banner()

    # Step 2: Create persistent data structure instances
    stack = Stack()
    queue = Queue()
    linked_list = LinkedList()

    # Step 3: Pre-populate with sample data for immediate exploration
    _seed_sample_data(stack, queue, linked_list)
    print(Fore.YELLOW + "  Sample data loaded into each data structure:")
    print(Fore.WHITE + f"    Stack (top→bottom): {', '.join(stack.to_list())}")
    print(Fore.WHITE + f"    Queue (front→rear): {', '.join(queue.to_list())}")
    print(Fore.WHITE + f"    Linked List: {linked_list}")
    print()

    # Step 4: Main menu loop
    main_menu = Menu(
        "CTA-1: Data Structures Demo",
        ["Stack", "Queue", "Linked List", "Exit"],
    )

    while True:
        print()
        print(Fore.CYAN + main_menu.render())
        choice = validate_prompt_int("Enter choice (1-4): ")

        # --- Stack ---
        if choice == 1:
            run_stack_menu(stack)

        # --- Queue ---
        elif choice == 2:
            run_queue_menu(queue)

        # --- Linked List ---
        elif choice == 3:
            run_linked_list_menu(linked_list)

        # --- Exit ---
        elif choice == 4:
            print(Fore.GREEN + "\n  Goodbye! Thank you for using the Data Structures Demo.")
            print()
            sys.exit(0)

        else:
            print(Fore.RED + "  Invalid choice. Please enter 1-4.")
# -------------------------------------------------------------- end run_application()

# ==============================================================================
# End of File
# ==============================================================================
