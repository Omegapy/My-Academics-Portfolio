# -------------------------------------------------------------------------
# File: ricciardi_model.py
# Project: Ricciardi Display  Model 
# Author: Alexander Ricciardi
# Date: 2025-23-17
# CTA-Module-2/ricciardi_model.py
# -------------------------------------------------------------------------
# Course: CSC-505 Principal of Software Development
# Professor: Dr. Joseph Issa
# Winter A term - 25WA
# Nov.-Jan. 2025
# -------------------------------------------------------------------------
# Assignment:
# Critical Thinking Assignment 2
#
# Directions (script portion only):
# Develop a Python Script:
# Implement a script named yourlastname_model.py that:
# Prompts the user for each phase name and a short description.
# Outputs a well-formatted summary of the model’s phases and structure.
# Example output:
# Phase 1: Discovery - Understand user needs and priorities
# Phase 2: Iterative Design - Develop, test, and refine features
# -------------------------------------------------------------------------

# --- File Contents Overview ---
# - Types/Constants: Phase, BANNER_WIDTH, MAIN_BANNER, SUMMARY_BANNER
# - Functions:
#       prompt_number_of_phases, prompt_user_for_phase_info,
#       format_phase_info, display_phases_info, main

# -------------------------------------------------------------------------
# --- Dependencies / Imports ---
# - Standard Library: typing (Final, TypeAlias)
# - Local Project Modules utilities:
#       utilities.menu_banner_utilities (Banner)
#       utilities.validation_utilities (
#           validate_prompt_nonezero_positive_int,
#           validate_prompt_string,
#       )
# -------------------------------------------------------------------------

# --- Requirements ---
# - Python 3.12+
# ------------------------------------------------------------------------

# --- Apache-2.0 ---
# Ac 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
The script is a console program that:
    1. Prompts users for how many phases their model has
    2. Prompts users for the name and a short description of each phase in their model
    3. Prints a well formatted summary:

           Phase 1: Discovery - Understand user needs and priorities
           Phase 2: Iterative Design - Develop, test, and refine features
"""

# __________________________________________________________________________
# Imports
#

# For annotations (type hints/docstrings)
from __future__ import annotations
from typing import Final, TypeAlias

# Import my utilities from same directory use for UI console
from utilities.menu_banner_utilities import Banner
from utilities.validation_utilities import (
    validate_prompt_nonezero_positive_int,
    validate_prompt_string,
)

# __________________________________________________________________________
# Global Constants / Variables
#

Phase: TypeAlias = tuple[str, str]

# Banners
BANNER_WIDTH: Final[int] = 72
# Main main nanner
MAIN_BANNER: Final[Banner] = Banner(
    [
        ("Ricciardi Display Model", "center", True),
        ("Phase Definition Tool", "center", False),
    ],
    inner_width=BANNER_WIDTH,
)
# Main main nanner
PHASES_SUMMARY_BANNER: Final[Banner] = Banner(
    [
        ("Model Summary", "center", False),
    ],
    inner_width=BANNER_WIDTH,
)


# __________________________________________________________________________
# Input functions
#

# # -------------------------------------------------------------------------
# def prompt_number_of_phases() -> int:
#     """Prompt the user to enter the number of phases in their model"""

#     return validate_prompt_nonezero_positive_int(
#         "How many phases are in your model have? ",
#     )
# # -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def prompt_user_for_phase_info(num_phases: int) -> list[Phase]:
    """Prompt the users for each phase name and description of their model

    Args:
        num_phases: Number of phases in the model

    Returns:
        A list of phases (name, description) -> List of tuples 
    """

    phases: list[Phase] = []

    # Collects the name and name of each phase
    for index in range(1, num_phases + 1):
        print(f"\n--- Phase {index} ---")
        # Prompt user for Phase name
        name: str = validate_prompt_string(
            f"Enter the name of Phase {index}: ",
        )
        # Prompt user for Phase description
        description: str = validate_prompt_string(
            f"Enter a short description for '{name}': ",
        )
        phases.append((name, description))

    return phases
# -------------------------------------------------------------------------

# __________________________________________________________________________
# Display Functions
#

# -------------------------------------------------------------------------
def format_phase_info(phases: list[Phase]) -> list[str]:
    """Format phase inputes into printable lines (phase info)

    Args:
        phases: List of (name, description) -> tuples.

    Returns:
        A list of formatted of phases info 
    """

    formatted_phases: list[str] = []

    # Fromat each phase info into lines and stores it in a list
    for index, (name, description) in enumerate(phases, start=1):
        # concatenate pahe num + name + description
        if description:
            formatted_phase = f"Phase {index}: {name} - {description}"
        else: # just in case no descript exist
            formatted_phase = f"Phase {index}: {name}"
        formatted_phases.append(formatted_phase)

    return formatted_phases
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def display_phases_info(phases: list[Phase]) -> None:
    """Display a well-formatted summary of the model’s phases and structure"""

    # Banner
    print() 
    print(PHASES_SUMMARY_BANNER.render())
    print()

    for phase_info in format_phase_info(phases):
        print(phase_info)
        print()
# -------------------------------------------------------------------------

# __________________________________________________________________________
# Main Function
#
# -------------------------------------------------------------------------
def main() -> None:
    """Run Ricciardi Display Model program"""

    # Banner
    print(MAIN_BANNER.render())
    print()
    # Display directions 
    print(
        "Please define the phases of your model by entering a name",
        "and a short description for each phase.",
    )
    print()
    
    # Prompt users to enter the number of phases of their model
    num_phases: int = validate_prompt_nonezero_positive_int(
        "How many phases are in your model have? ",
    )
    
    # Prompt the users for each phase name and description of their model
    phases: list[Phase] = prompt_user_for_phase_info(num_phases)

    # Display well-formatted summary of the model’s phases and structure
    display_phases_info(phases)

    print()
    print("Thank you for using ricciardi_model.py!")
# -------------------------------------------------------------------------

# __________________________________________________________________________
# Module Initialization / Main Execution Guard
#
if __name__ == "__main__":
    main()

# __________________________________________________________________________
# End of File
#
