# -------------------------------------------------------------------------
# File: shopping_list_prototype.py
# Project: CSC-505-Programs
# Author: Alexander Ricciardi
# Date: 2025-11-30
# CTA-Module-3/shopping_list_prototype.py
# ------------------------------------------------------------------------
# Course: CSS-505 Principal of Software Development
# Professor: Dr. Joseph Issa
# Winter W-2025
# Nov.-jav. 2025
# ------------------------------------------------------------------------
# Assignement:
# Critical Thinking Assignment Module 3
#
# Directions:
# Step 3: Python Script to Describe Prototype
# Create a Python script (shopping_list_prototype.py) that:
#
# Defines the screen names
# Prints the total number of screens
# Prints the navigation flow (e.g., "Home → Add Item → Save → View List")
# Optionally includes descriptions of what each screen does
# Sample Output:
#
# Screens: Home, Add Item, View List, Edit Item, Settings
# Total Screens: 5
# Flow:
# Home → Add Item
# Add Item → View List
# View List → Edit Item
# Home → Settings
#
# Keep the code simple and use lists or dictionaries to model screens and navigation.
# -------------------------------------------------------------------------

# --- Program Description ---
# The program is a small console program that 
# summarizes a mobile shopping app UI flow.
# -------------------------------------------------------------------------

# --- File Contents ---
# -- Data
# - Global: SCENE_LIST
# - Global: SCENE_DESCRIPTIONS
# - Global: NAVIGATION_GROUPS
# -- Functions
# - Function: supports_color
# - Function: colorize
# - Function: safe_render
# - Function: render_banner
# - Function: main
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: decimal (currency math), sys (stdout encoding handling)
# - Local Project Modules:
#   - utilities.menu_banner_utilities.Banner
# --- Requirements ---
# - Python Python 3.12
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Ac 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
The program is a small console program that summarizes a mobile shopping app UI flow.

The script lists screens, counts, descriptions, and navigation screen UI flow paths.
"""

from __future__ import annotations

# __________________________________________________________________________
# Imports
#
from decimal import Decimal
import sys
from typing import Any, Dict, List, Tuple

from utilities.menu_banner_utilities import Banner

# __________________________________________________________________________
# Global Constants / Variables
#

SEPARATOR = "-" * 30  # Console screen divider "-------"
ARROW = " -> "  # directionarrow used within rendered flow path

ScreenPath = List[str]
# List of tuples containing -> (group name, list of navigation flow paths)
FlowGroup = Tuple[str, List[ScreenPath]] 

# Console Screen text ANSI color 
COLOR_RESET = "\033[0m"  # Reset ANSI color 
COLOR_TITLE = "\033[96m"  # Bright cyan - banner headers
COLOR_HEADING = "\033[94m"  # Blue - section headings
COLOR_LABEL = "\033[92m"  # Green - labels and indices
COLOR_TEXT = "\033[97m"  # White - general text

# __________________________________________________________________________
# Global Data Definitions
#

# List of UI screens
SCREENS: List[str] = [
    "Home Screen",
    "Search/Browse Screen",
    "Add Item Screen",
    "Item List Screen",
    "Edit/Remove Screen",
    "Checkout Screen",
]

# Screen descriptions, it mappes the screen names to thier descriptions
SCREEN_DESCRIPTIONS: Dict[str, str] = {
    "Home Screen": "Home landing view with UI button linking to browse, add, edit, and checkout screens.",
    "Search/Browse Screen": "Search functionality allows users to search items by category or/and price, and it displays the search results.",
    "Add Item Screen": "Allow users to add a new item and the item list (shopping Cart) and set the quantity wanted",
    "Item List Screen": "Display the shopping cart list.",
    "Edit/Remove Screen": "Allows user to update an item quantity or remove the item from the shopping cart list.",
    "Checkout Screen": "Display totals and allow user to proceed to payment.",
}

# Navigation UI flows grouped, List[Tuple[str, List[str]]]
NAVIGATION_GROUPS: List[FlowGroup] = [
    # -----------------------------
    ( # -- Group 1: Home to Search/Browse
        "The Home Screen -> Search/Browse Screen flows:",
        [
            ["Home Screen", "Search/Browse Screen", "Home Screen"],
            ["Home Screen", "Search/Browse Screen", "Checkout Screen", "Home Screen"],
            ["Home Screen", "Search/Browse Screen", "Checkout Screen", "External UI"],
            ["Home Screen", "Search/Browse Screen", "Add Item Screen", "Home Screen"],
            [
                "Home Screen",
                "Search/Browse Screen",
                "Add Item Screen",
                "Checkout Screen",
                "Home Screen",
            ],
            [
                "Home Screen",
                "Search/Browse Screen",
                "Add Item Screen",
                "Checkout Screen",
                "External UI",
            ],
            [
                "Home Screen",
                "Search/Browse Screen",
                "Add Item Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Home Screen",
            ],
            [
                "Home Screen",
                "Search/Browse Screen",
                "Add Item Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Home Screen",
            ],
            [
                "Home Screen",
                "Search/Browse Screen",
                "Add Item Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "External UI",
            ],
        ],
    ),
    # -----------------------------
    ( # -- # Group 2: Home to Add Item
        "The Home Screen -> Add Item Screen flows:",
        [
            ["Home Screen", "Add Item Screen", "Home Screen"],
            ["Home Screen", "Add Item Screen", "Checkout Screen", "Home Screen"],
            ["Home Screen", "Add Item Screen", "Checkout Screen", "External UI"],
        ],
    ),
    # -----------------------------
    ( # -- Group 3: Home to Item List
        "The Home Screen -> Item List Screen flows:",
        [
            ["Home Screen", "Item List Screen", "Home Screen"],
            ["Home Screen", "Item List Screen", "Checkout Screen", "Home Screen"],
            ["Home Screen", "Item List Screen", "Checkout Screen", "External UI"],
            ["Home Screen", "Item List Screen", "Edit/Remove Screen", "Home Screen"],
            [
                "Home Screen",
                "Item List Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Home Screen",
            ],
            [
                "Home Screen",
                "Item List Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "External UI",
            ],
            [
                "Home Screen",
                "Item List Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Home Screen",
            ],
            [
                "Home Screen",
                "Item List Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Home Screen",
            ],
            [
                "Home Screen",
                "Item List Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "External UI",
            ],
        ],
    ),
    # -----------------------------
    ( # -- Group 4: Home directly to Edit/Remove
        "The Home Screen -> Edit/Remove Screen flows:",
        [
            ["Home Screen", "Edit/Remove Screen", "Home Screen"],
            ["Home Screen", "Edit/Remove Screen", "Checkout Screen", "Home Screen"],
            ["Home Screen", "Edit/Remove Screen", "Checkout Screen", "External UI"],
        ],
    ),
    # -----------------------------
    ( # -- Group 5: Home to Checkout
        "The Home Screen -> Checkout Screen flows:",
        [
            ["Home Screen", "Checkout Screen", "Home Screen"],
            ["Home Screen", "Checkout Screen", "External UI"],
            [
                "Home Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Home Screen",
            ],
            [
                "Home Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "Edit/Remove Screen",
                "Checkout Screen",
                "External UI",
            ],
        ],
    ),
    # -----------------------------
]

# __________________________________________________________________________
# Utility Helper Functions
#

# ---------------------------------------------------------------------------------
def supports_color() -> bool:
    """Check if the platform stdout used supports ANSI colors

    Returns:
        True when stdout is a TTY (Teletypewriter) and supports ANSI escape sequences
    """
    return sys.stdout.isatty()
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def colorize(text: str, color: str) -> str:
    """Wrap text with ANSI color codes

    Args:
        text: The text to colorize
        color: ANSI color to apply

    Returns:
        The colored text when supported -> otherwise the original text.
    """
    if not supports_color():
        return text
    
    return f"{color}{text}{COLOR_RESET}"
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def safe_render(text: str) -> str:
    """Render text safely for Windows OS console   

    It allows any characters unsupported by the console’s encoding 
    to become replacement glyphs instead of raising/printing garbage.
    In this application is used to safely render banners.

    Args:
        text: Text to encode and decode safely

    Returns:
        A rendered safe text by replacing error with '?'
    """
    # grabs the current stdout encoding (falls back to "utf-8" if missing)
    encoding = sys.stdout.encoding or "utf-8"  
    # If error occur the text is replaced with '?'
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def render_banner(title: str) -> str:
    """Render the app banner using the utlity module

    Args:
        title: The banner text

    Returns:
        The formatted banner string with color
    """
    banner = Banner([(title, "center")])
    return colorize(safe_render(banner.render()), COLOR_TITLE)
# ---------------------------------------------------------------------------------

# __________________________________________________________________________
# Main Function
#
def main() -> None:
    """Main execution function to print the UI flow"""
    
    # --------------------------------------------------------------------------
    # 1. Print Banner
    # --------------------------------------------------------------------------
    print(f"\n{render_banner('Shopping App User Flow')}")

    # --------------------------------------------------------------------------
    # 2. Print Screens and Descriptions
    # --------------------------------------------------------------------------
    # Display the colorize list of screen names and the total count
    print(colorize(f"\nScreens:", COLOR_HEADING))
    print(colorize(f"{'\n'.join(SCREENS)}", COLOR_LABEL))
    print(colorize(f"\nTotal Screens: {len(SCREENS)}\n", COLOR_LABEL))
    
    # Print section separator and Screen description header
    print(colorize(SEPARATOR, COLOR_HEADING))
    print(colorize("Screen Descriptions:", COLOR_HEADING))

    # Iterate through the list of screen names (SCREENS)
    # retrieves each screen description from the SCREEN_DESCRIPTIONS dictionary
    # and print them in a formatted colorize line.
    for screen in SCREENS:
        description = SCREEN_DESCRIPTIONS.get(screen, "")
        print(f" - {colorize(screen, COLOR_LABEL)}: {description}")

    # Print a separator 
    print(colorize(SEPARATOR, COLOR_HEADING))

    # --------------------------------------------------------------------------
    # 3. Print Navigation UI Flow
    # --------------------------------------------------------------------------
    # User UI Flow Header
    print(colorize("\nUser UI Flow:", COLOR_HEADING))
    print("")

    # Iterates through the grouped navigation flows (NAVIGATION_GROUPS)
    # 'enumerate' group_index starting at 1, 
    # inner loop adds a path_index for each paths (e.g., 1.1, 1.2)
    # each printed group consists of a 'title' for the group and a list of 'paths'.
    for group_index, (title, paths) in enumerate(NAVIGATION_GROUPS, start=1):
        
        # Create and print the group header (e.g., "1. Home Screen -> Search/Browse Screen flows:").
        group_label = colorize(f"{group_index}.", COLOR_LABEL)
        header_line = f"{group_label} {title}"
        print(colorize(header_line, COLOR_HEADING))
        
        # Print a separator under the group header
        print(colorize(SEPARATOR, COLOR_HEADING))

        # Inner Loop -> iterates through the group paths
        # 'enumerate' adds a path_index for each paths (e.g., 1.1, 1.2)
        for path_index, path in enumerate(paths, start=1):
            
            # Format add index to path (e.g., "1.1").
            path_label = colorize(f"{group_index}.{path_index}", COLOR_LABEL)
            
            # Join the list of screens wthin the path with an arrow " -> "
            formatted_path = ARROW.join(path)
            
            # Print the formated path
            print(f"{path_label}: {formatted_path}")
            
        # Print a separator below group before the next
        print(colorize(SEPARATOR, COLOR_HEADING))
        print("")


# __________________________________________________________________________
# Module Initialization / Main Execution Guard 
#
if __name__ == "__main__":
    main()
# __________________________________________________________________________
# End of File
#