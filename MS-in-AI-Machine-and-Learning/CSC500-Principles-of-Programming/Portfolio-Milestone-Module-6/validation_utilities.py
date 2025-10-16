# -------------------------------------------------------------------------
# File: validation_utilities.py
# Author: Alexander Ricciardi
# Date: 2025-10-05
# -------------------------------------------------------------------------
# Course: CSS-500 Principles of Programming
# Professor: Dr. Brian Holbert
# Fall C-2025
# Sep.-Nov. 2025

# --- Module Functionality ---
# The file provides user input validation utility functions.
# -------------------------------------------------------------------------

# --- Functions ---
# - validate_prompt_yes_or_no(): request a yes/no confirmation, until a valid input is entered
# - wait_for_enter(): pause program until the user presses Enter
# - validate_prompt_int(): prompt user until a valid integer is entered
# - validate_prompt_positive_int(): prompt user until a valid positive integer is entered
# - validate_prompt_nonezer_positive_int(): prompt user until a valid none positive integer is entered
# - validate_prompt_float(): prompt user until a valid float is entered
# - validate_prompt_positive_float(): prompt user until a valid positive float is entered
# - validate_prompt_nonezero_positive_float(): prompt user until a valid nonezero positive float is entered.
# - validate_prompt_string(): prompt user until a non-empty string is entered
# - validate_prompt_date(): prompt user until a valid date is entered

# --- Imports ---
# - __future__.annotations to simplify forward typing references.
# - colorama (Fore, init) for cross-platform colored terminal
# - datetime for date parsing and validation 
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
The file provides input validation utility functions.

Each function contains a validation loop for prompting user, capturing input,
and validating input (ints, floats, or strings). The loop will loop until a valid
input is entered, and then the function will validate the input.
"""

# ________________
# Imports
#

from __future__ import annotations

from datetime import datetime

from colorama import Fore, init
# Initialize colorama primarily to make it work on Windows
init(autoreset=True)

# ____________________________________________________________________________
#  Miscellaneous user-input validation functions
#

# --------------------------------------------------------------------------------- validate_prompt_yes_or_no()
def validate_prompt_yes_or_no(prompt: str) -> bool:
    """Prompt the user until a valid yes/no answer is provided.

    Args:
        prompt: text to display before the "[Y/N]".

    Returns:
        True if the user selects yes ("y"/"yes"); False if no ("n"/"no").

    Examples:
        user input shown after [prompts]:

            >>> result = validate_prompt_yes_or_no("Continue?")
            Continue? [Y/N]: maybe
            Invalid input. Please enter 'Y' or 'N'.
            Continue? [Y/N]: y
            >>> result
            True
    """
    # Loop until a yes/no input is provided.
    while True:
        choice = input(f"{prompt} [Y/N]: ").strip().lower()
        # confirmations
        if choice in ("y", "yes"):
            return True
        # reinforce confirmations
        if choice in ("n", "no"):
            return False
        # invalid input message
        print(Fore.LIGHTRED_EX + "Invalid input. Please enter 'Y' or 'N'.")
# --------------------------------------------------------------------------------- end validate_prompt_yes_or_no()

# -------------------------------------------------------------- wait_for_enter()
def wait_for_enter() -> None:
    """Pause execution until the user presses Enter.

    Examples:
            >>> wait_for_enter()
            
            Press Enter to continue...
            <user presses Enter>
    """
    input("\nPress Enter to continue...")
# -------------------------------------------------------------- 

# ____________________________________________________________________________
# Integer validation functions
#

# -------------------------------------------------------------- validate_prompt_int()
def validate_prompt_int(prompt: str) -> int:
    """Ask the user until a valid integer is entered.

    Args:
        prompt: text to display to the user

    Returns:
        The validated integer value

    Behavior:
        - Re-prompts when the input cannot be validated as an integer

    Examples:
       user input shown after [prompts]:

            >>> value = validate_prompt_int("Enter an integer:")
            Enter an integer:
            three
            Invalid input. Please enter an integer (e.g., 2).
            Enter the integer entered is: 2
            >>> value
            2
    """
    # Keep asking until a valid int is entered
    while True:
        raw = input(f"{prompt}").strip()
        try:
            return int(raw)
        except ValueError:
            # Invalid input error message
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter an integer (e.g., 2).")
# -------------------------------------------------------------- end validate_prompt_int()

# -------------------------------------------------------------- validate_prompt_positive_int()
def validate_prompt_positive_int(prompt: str) -> int:
    """Ask the user until a valid positive integer is entered.

    Args:
        prompt: text to display to the user

    Returns:
        The validated positive integer value

    Behavior:
        - Re-prompts when the input cannot be validated as a positive integer

    Examples:
       user input shown after [prompts]:

            >>> value = validate_prompt_positive_int("Enter the item quantity:")
            Enter the item quantity:
            three
            Invalid input. Please enter a positive integer (e.g., 2).
            Enter the item quantity: 2
            >>> value
            2
    """
    # Keep asking until a valid positive int is entered
    while True:
        raw = input(f"{prompt}").strip()
        try:
            if int(raw) >= 0: # 0 is both + and -
                return int(raw) 
            raise  ValueError
        except ValueError:
            # Invalid input error message
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a positive integer (e.g., 2).")
# -------------------------------------------------------------- end validate_prompt_positive_int()

# -------------------------------------------------------------- validate_prompt_nonezero_positive_int()
def validate_prompt_nonezero_positive_int(prompt: str) -> int:
    """Ask the user until a valid nonezero positive integer is entered.

    Args:
        prompt: text to display to the user

    Returns:
        The validated nonezero positive integer value

    Behavior:
        - Re-prompts when the input cannot be validated as a nonezero positive integer

    Examples:
       user input shown after [prompts]:

            >>> value = validate_prompt_positive_int("Enter the item quantity:")
            Enter the item quantity:
            three
            Invalid input. Please enter a positive integer (e.g., 2).
            Enter the item quantity: 2
            >>> value
            2
    """
    # Keep asking until a valid positive int is entered
    while True:
        raw = input(f"{prompt}").strip()
        try:
            if int(raw) > 0: 
                return int(raw) 
            raise  ValueError
        except ValueError:
            # Invalid input error message
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a nonezero positive integer (e.g., 2).")
# -------------------------------------------------------------- end validate_prompt_nonezero_positive_int()

# ____________________________________________________________________________
# Float validation functions
#

# -------------------------------------------------------------- validate_prompt_float()
def validate_prompt_float(prompt: str) -> float:
    """Asks the user until a valid float is entered.

    Args:
        prompt: text to display to the user

    Returns:
        The validated float value

    Behavior:
        - Re-prompts when the input cannot be validated as a float

    Examples:
        user input shown after [prompts]:

            >>> price = validate_prompt_float("Enter the item price:")
            Enter the item price:
            price
            Invalid input. Please enter a valid float (e.g., 12.99).
            Enter the item price: 12.99
            >>> price
            12.99
    """
    # Keep asking until valid float is entered
    while True:
        raw = input(f"{prompt}").strip()
        try:
            return float(raw)
        except ValueError:
            # Invalid input error message
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a valid float (e.g., 12.99).")
# -------------------------------------------------------------- end validate_prompt_float()

# -------------------------------------------------------------- validate_prompt_positive_float()
def validate_prompt_positive_float(prompt: str) -> float:
    """Ask the user until a valid positive integer is entered.

    Args:
        prompt: text to display to the user

    Returns:
        The validated positive float value

    Behavior:
        - Re-prompts when the input cannot be validated as a positive integer

    Examples:
       user input shown after [prompts]:

             >>> price = validate_prompt_float("Enter the item price:")
            Enter the item price:
            price
            Invalid input. Please enter a valid float (e.g., 12.99).
            Enter the item price: 12.99
            >>> price
            12.99
    """
    # Keep asking until a valid positive int is entered
    while True:
        raw = input(f"{prompt}").strip()
        try:
            if float(raw) >= 0.0: # 0.0 is both + and -
                return float(raw) 
            raise  ValueError
        except ValueError:
            # Invalid input error message
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a positive float (e.g., 12.99).")
# -------------------------------------------------------------- end validate_prompt_positive_float()

# -------------------------------------------------------------- validate_prompt_nonezero_positive_float()
def validate_prompt_nonezero_positive_float(prompt: str) -> float:
    """Ask the user until a valid nonezero positive float is entered.

    Args:
        prompt: text to display to the user

    Returns:
        The validated positive float value

    Behavior:
        - Re-prompts when the input cannot be validated as a nonzero positive float

    Examples:
       user input shown after [prompts]:

             >>> price = validate_prompt_float("Enter the item price:")
            Enter the item price:
            price
            Invalid input. Please enter a valid float (e.g., 12.99).
            Enter the item price: 12.99
            >>> price
            12.99
    """
    # Keep asking until a valid nonezero positive float is entered
    while True:
        raw = input(f"{prompt}").strip()
        try:
            if float(raw) > 0.0: 
                return float(raw) 
            raise  ValueError
        except ValueError:
            # Invalid input error message
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a nonezero positive float (e.g., 12.99).")
# -------------------------------------------------------------- end validate_prompt_nonezero_positive_float()

# ____________________________________________________________________________
# String validation functions
#

# -------------------------------------------------------------- validate_prompt_string()
def validate_prompt_string(prompt: str) -> str:
    """Ask the user until a non-empty string is entered.

    Args:
        prompt: text to display to the user

    Returns:
        A validated string value 

    Behavior:
        - when the input cannot be validated as a non-empty string 

    Examples:
        user input shown after [prompts]:

            >>> name = validate_prompt_string("Enter the item name:")
            Enter the item name:
            
            Invalid input. Please enter a string (e.g., Hello).
            Enter the item name:
            Apples
            >>> name
            'Apples'
    """
    # Keep asking until a non-empty string is entered
    while True:
        raw = input(f"{prompt}").strip()
        try:
            if raw == "":
                # raise error if input string is empty
                raise ValueError()
            return str(raw)
        except ValueError:
            # Keep asking until a none-empty is entered
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a string (e.g., Hello).")
# -------------------------------------------------------------- end validate_prompt_string()

# ____________________________________________________________________________
# Date validation functions
#

# -------------------------------------------------------------- validate_prompt_date()
def validate_prompt_date(
    prompt: str,
    *,
    formats: list[str] | None = None,
    normalize_format: str = "%B %d, %Y"
) -> str:
    """Prompt user until valid date is entered.

    Args:
        prompt: Text to display to the user
        formats: List of accepted input formats -> (default: ["%B %d, %Y", "%m/%d/%Y", "%Y-%m-%d"])
        normalize_format: Output format for the date string (default: "%B %d, %Y")

    Returns:
        Date string in normalize_format (e.g., "February 1, 2020")

    Examples:
        user input shown after [prompts]:

            >>> date = validate_prompt_date("Enter date:\\n")
            Enter date:
            2/1/2020
            >>> date
            'February 1, 2020'

            >>> date = validate_prompt_date("Enter date:\\n")
            Enter date:
            February 1, 2020
            >>> date
            'February 1, 2020'

            >>> date = validate_prompt_date("Enter date:\\n")
            Enter date:
            2020-02-01
            >>> date
            'February 1, 2020'

            >>> date = validate_prompt_date("Enter date:\\n")
            Enter date:
            invalid
            Invalid input. Please enter a valid date (e.g., February 1, 2020 or 2/1/2020 or 2020-02-01).
            Enter date:
            2/1/2020
            >>> date
            'February 1, 2020'
    """
    # Default formats if none provided
    if formats is None:
        formats = ["%B %d, %Y", "%m/%d/%Y", "%Y-%m-%d"]

    # Build example string from formats
    examples = []
    try:
        example_date = datetime(2020, 2, 1)
        for fmt in formats[:3]:  # Show up to 3 examples
            examples.append(example_date.strftime(fmt))
    except Exception:
        examples = ["February 1, 2020", "2/1/2020", "2020-02-01"]

    example_str = " or ".join(examples)

    while True:
        raw = input(f"{prompt}").strip()

        # Try each format until one works
        date_obj = None
        for fmt in formats:
            try:
                date_obj = datetime.strptime(raw, fmt)
                break
            except ValueError:
                continue

        if date_obj is not None:
            # Successfully parsed - return normalized format
            # Use %-d for non-zero-padded day on Unix/Mac, %#d on Windows
            # But %B %d, %Y with manual formatting is more portable
            formatted = date_obj.strftime(normalize_format)
            # Remove leading zero from day if present (e.g., "February 01" -> "February 1")
            parts = formatted.split()
            if len(parts) >= 2 and parts[1].endswith(',') and parts[1][:-1].startswith('0'):
                parts[1] = parts[1][1:]  # Remove leading zero
            return ' '.join(parts)
        else:
            # No format matched - show error
            print(Fore.LIGHTRED_EX + f"Invalid input. Please enter a valid date (e.g., {example_str}).")
# -------------------------------------------------------------- end validate_prompt_date()

# __________________________________________________________________________
# End of File
#
