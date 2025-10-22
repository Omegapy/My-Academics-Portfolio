# -------------------------------------------------------------------------
# File: course_info.py
# Project:
# Author: Alexander Ricciardi
# Date: 2025-10-26
# File Path: Critical-Thinking-Module-7/course_info.py
# ------------------------------------------------------------------------
# Course: CSS-500 Principles of Programming
# Professor: Dr. Brian Holbert
# Fall C-2025
# Sep-Nov 2025
# ------------------------------------------------------------------------
# Assignment:
# Write a program that creates a dictionary containing course numbers 
# and the room numbers of the rooms where the courses meet. 
# The dictionary should have the following key–value pairs:
#
# Key–Value Pairs: Room Number:
# |---------------------|---------------------|
# | Course Number (key) | Room Number (value) |
# |---------------------|---------------------|
# | CSC101              | 3004                |
# | CSC102              | 4501                |
# | CSC103              | 6755                |
# | NET110              | 1244                |
# | COM241              | 1411                |
# |---------------------|---------------------|
#
# The program should also create a dictionary containing course numbers 
# and the names of the instructors that teach each course. 
# The dictionary should have the following key–value pairs:
#
# Key–Value Pairs: Instructors:
# |---------------------|--------------------|
# | Course Number (key) | Instructor (value) |
# |---------------------|--------------------|
# | CSC101              | Haynes             |
# | CSC102              | Alvarado           |
# | CSC103              | Rich               |
# | NET110              | Burke              |
# | COM241              | Lee                |
# |---------------------|--------------------|
#
# The program should also create a dictionary containing course numbers 
# and the meeting times of each course. 
# The dictionary should have the following key–value pairs:
#
# Key–Value Pairs: Meeting Time:
# |---------------------|----------------------|
# | Course Number (key) | Meeting Time (value) |
# |---------------------|----------------------|
# | CSC101              | 8:00 a.m.            |
# | CSC102              | 9:00 a.m.            |
# | CSC103              | 10:00 a.m.           |
# | NET110              | 11:00 a.m.           |
# | COM241              | 1:00 p.m.            |
# |---------------------|----------------------|
#
# Program Behavior:  
# The program should let the user enter a course number and then display the course’s room number, 
# instructor, and meeting time.
#
# Submission:
#
# Compile and submit your pseudocode, source code, screenshots of the application executing the code, 
# the results and GIT repository in a single document (Word is preferred).
# ------------------------------------------------------------------------

# Project:
# CSC500 Module 7 — Course info
#
# Project description:
# Simple console application that lets a user enter a course number and displays
# it's room, instructor, and meeting time using dictionary info.
# -------------------------------------------------------------------------

# --- Module Functionality ---
#   Provide a way for a user to look up the course room, instructor, and time
#   The program uses dictionaries and a small menu console UI.
# -------------------------------------------------------------------------



# --- Module Contents Overview ---
# - Constants: COURSE_TO_ROOM, COURSE_TO_INSTRUCTOR, COURSE_TO_TIME
# - Functions: validate_dictionaries, info_course, print_menu, main
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: 
#   - sys
# - Third-Party: 
#   - colorama (console color utilities)
# - Local Project Modules: 
#   - menu_banner_utilities (render ASCII banners and menus)
#   - validation_utilities (input validation functions)
# --- Requirements ---
# - Python 3.13
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is imported by `main.py` to run the Course info menu-based CLI.
# It can also be executed directly as a script to launch the same interface.
#
# Example integrations:
# - Import `print_menu` in a larger console app to embed the info feature.
# - Import `info_course` to trigger a single info from another flow.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
The program is a small terminal app that allows a user to view 
an ‘university’ course(s) information (course number, room, instructor, and time) 
by entering a course number. 
The course information (data) is stored in three dictionaries, 
and the course numbers are used as keys within the dictionaries.
"""
# __________________________________________________________________________
# Imports
#
# ________________
# Future annotations for simplified type hints 
from __future__ import annotations
# ________________
# Imports
#
# Standard library
import sys # For 

# Third-party
from colorama import Fore, Style

# Local project modules
from menu_banner_utilities import Banner, Menu
from validation_utilities import (
    validate_prompt_string,
    validate_prompt_yes_or_no,
    wait_for_enter,
)

# __________________________________________________________________________
# Global Constants / Variables
#

# Room Number
COURSE_TO_ROOM: dict[str, str] = {
    "CSC101": "3004",
    "CSC102": "4501",
    "CSC103": "6755",
    "NET110": "1244",
    "COM241": "1411",
}

# Instructors
COURSE_TO_INSTRUCTOR: dict[str, str] = {
    "CSC101": "Haynes",
    "CSC102": "Alvarado",
    "CSC103": "Rich",
    "NET110": "Burke",
    "COM241": "Lee",
}

# Meeting Time
COURSE_TO_TIME: dict[str, str] = {
    "CSC101": "8:00 a.m.",
    "CSC102": "9:00 a.m.",
    "CSC103": "10:00 a.m.",
    "NET110": "11:00 a.m.",
    "COM241": "1:00 p.m.",
}


# __________________________________________________________________________
# Standalone Function Definitions
#
# ______________________
# Helper Functions
#
# =========================================================================
# Program logic function, user interface and query
# =========================================================================

# --------------------------------------------------------------------------------- info_course()
def info_course() -> None:
    """Prompt the user to enter a course number 
       and display the course number and associated room, instructor, and time.

    Returns:
        None

    Examples:
        >>> info_course()  
        Enter course number (e.g., CSC101):
        CSC101
        Course: CSC101
        Room: 3004
        Instructor: Haynes
        Time: 8:00 a.m.
    """
    # Prompt user and validate user a string
    user_input = validate_prompt_string("Enter course number (e.g., CSC101):\n").strip().upper()

    # Check if course exists
    if user_input not in COURSE_TO_ROOM:
        print(Fore.LIGHTRED_EX + "\nCourse not found." + Style.RESET_ALL)
        wait_for_enter()
        return # return None if the inputted course does not exist

    # get course info
    room = COURSE_TO_ROOM[user_input]
    instructor = COURSE_TO_INSTRUCTOR[user_input]
    time = COURSE_TO_TIME[user_input]

    # Create a Course Information banner instance
    results_banner = Banner(["Course Information"])
    print()
    # Render and display banner
    print(Fore.LIGHTCYAN_EX + results_banner.render())

    # Display course number using colors
    print(
        Fore.LIGHTYELLOW_EX
        + "\nCourse: "
        + Fore.LIGHTWHITE_EX
        + user_input
        + Style.RESET_ALL,
    )
    # Display course room number using colors
    print(
        Fore.LIGHTYELLOW_EX + "Room: " + Fore.LIGHTWHITE_EX + room + Style.RESET_ALL,
    )
    # Display course instructor last name using colors
    print(
        Fore.LIGHTYELLOW_EX
        + "Instructor: "
        + Fore.LIGHTWHITE_EX
        + instructor
        + Style.RESET_ALL,
    )
    # Display course meeting time using colors
    print(
        Fore.LIGHTYELLOW_EX + "Time: " + Fore.LIGHTWHITE_EX + time + Style.RESET_ALL,
    )

    wait_for_enter()
# --------------------------------------------------------------------------------- 

#---- Menu ----
# --------------------------------------------------------------------------------- print_menu()
def print_menu() -> None:
    """Render the menu

    Menu options:
        l - Look Up Course: Execute course info
        q - Quit: Exit program with confirmation

    Returns:
        None

    Examples:
        >>> print_menu()  # doctest: +SKIP
        ╔══════════════════════╗
        ║         MENU         ║
        ╠══════════════════════╣
        ║ l - Look Up Course   ║
        ║ q - Quit             ║
        ╚══════════════════════╝

        Choose an option:
    """
    # Create menu instance using the Menu class
    menu = Menu(
        "MENU",
        [
            "Lookup Course Information",
            "Quit",
        ],
        prefixes=["l", "q"],
    )
    # Render main menu and store it in a string variable to be displayed
    # to be used in the program main while loop
    menu_display = Fore.LIGHTCYAN_EX + menu.render()

    # Create info banner instance
    info_banner = Banner(["COURSE INFORMATION"])
    # Render the course info banner and store it in a string variable to be displayed
    # to be used in the program main while loop
    info_banner_display = Fore.LIGHTCYAN_EX + info_banner.render()

    # Main program Menu loop
    while True:
        print()
        print(menu_display)

        # Prompt and capture the user for selection (l or q)
        selection = input("\nChoose an option: ").strip().lower()

        match selection:
            # Launch the course info feature
            case "l":  
                print()
                print(info_banner_display)
                print()
                # Launch course info query functionality
                info_course()
            # Launch the quit/existing program feature
            case "q":  
                if validate_prompt_yes_or_no("Are you sure you want to exit?"):
                    print("\nThank you for using Course info System!")
                    # Exit while loop/program
                    break

            case _:
                # Invalid selection input message
                print(
                    Fore.LIGHTRED_EX + "\nInvalid selection. Please enter 'l' or 'q'.",
                )
                wait_for_enter()

# --------------------------------------------------------------------------------- 

# ______________________
# Program Entrypoint 
# Main function
# --------------------------------------------------------------------------------- main()
def main() -> None:
    """Run the course info program

    Program Flow:
        1. UTF-8 encoding (Windows compatibility)
        2. header banner
        4. menu loop (user can info courses or quit)
           program logic

    Examples:
        >>> main() 
        ╔════════════════════════╗
        ║   Course info System   ║
        ╚════════════════════════╝
        ...menu loop...
            user interaction
            program logic
        Goodbye! 👋
    """
    # Configure UTF-8 encoding for console (Windows compatibility)
    sys.stdout.reconfigure(encoding="utf-8")

    # Display program header banner
    header = Banner(["Course info System"])
    print(Fore.LIGHTCYAN_EX + header.render())
    print()

    # Enter menu loop - contain program logic
    print_menu()

    # Exit message (after menu loop ends)
    print("\nGoodbye! 👋\n")
# --------------------------------------------------------------------------------- 

# __________________________________________________________________________
# Module Initialization / Main Execution Guard (if applicable)
#
if __name__ == "__main__":
    main()
# __________________________________________________________________________
# End of File
#
