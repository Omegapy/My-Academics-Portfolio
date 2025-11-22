# -------------------------------------------------------------------------
# File: menu_banner_utilities.py
# Author: Alexander Ricciardi
# Date: 2025-10-05
# -------------------------------------------------------------------------
# Course: CSS-500 Principles of Programming
# Professor: Dr. Brian Holbert
# Fall C-2025
# Sep.-Nov. 2025

# --- Module Functionality ---
# Provides console UI classes that render bordered banners and numbered menus.
# -------------------------------------------------------------------------

# --- Classes ---
# - Banner: Creates an ASCII-styled boxes with alignment, dividers, and sizing functionality.
# - Menu: Creates a console menus using Banner.
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - typing (Literal, Sequence, TypeAlias) to annotate alignment options and content.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
The file provides a console banner and a menu console-based UI.

The Banner and Menu use ASCII formatting to display UI on the console.
The Banner renders banner-style titles, and the Menu class uses the Banner class
to render menus.
"""
# ________________
# Imports
#

from __future__ import annotations

from typing import Literal, Sequence, TypeAlias

# __________________________________________________________________________
# Utility Classe Banner
#
# =========================================================================
# Banner Class (box headers)
# =========================================================================
# ------------------------------------------------------------------------- class Banner
class Banner:
    """Instantiate box banner for the console from one or more text lines

    The banner consists of a top border, one header line 
    and maybe more text lines with alignment (left/center/right), and a bottom border. 
    The inner_width of the box automatically expands to fit the text length.

    
    Examples:
                ╔══════════════╗
                ║  First line  ║ 
                ╚══════════════╝
        
    """
    
    Alignment: TypeAlias = Literal["left", "center", "right"]

    # ______________________ 
    #  Class constants 
    #
    # Default title text when no content is provided
    DEFAULT_TEXT = "Banner"
    # Default alignment 
    DEFAULT_ALIGNMENT = "center"
    # Whether divider is applied to the line
    DEFAULT_ISDIVIDER = False
    # Default banner content tuple
    DEFAULT_CONTENT: list[tuple[str, Alignment, bool]] = [(DEFAULT_TEXT, DEFAULT_ALIGNMENT, DEFAULT_ISDIVIDER)]
    # Minimum Banner inner width 
    MINIUM_WIDTH: int = 10

    # ______________________ 
    # Constructor
    #
    # -------------------------------------------------------------- __init__()
    def __init__(
        self,
        content: Sequence[object] = DEFAULT_CONTENT,
        inner_width: int = MINIUM_WIDTH,
    ) -> None:
        """Construct and initialize a new banner with default values if none are entered

        Args:
            text: text lines inside the banner 
            alignment: Alignment of text lines ("left", "center", or "right")
            inner_width: the minimum inner width of the banner (auto-expands for longer text)
        
        example:
             >>> banner_1 = Banner([("First line"), 
                                    (), 
                                    ("Third Line", "left", True), 
                                    ("Fourth Line", "Right") 
                                ])
            >>> print(banner_1.render())

                ╔══════════════╗
                ║  First line  ║ # Default alignment and isDivider
                ║              ║ # Second Line empty
                ║ Third Line   ║ # Aligns to the left and adds a divider
                ╠══════════════╣
                ║ Fourth Line  ║ # Aligns to the right and default isDividerr
                ╚══════════════╝
        
        """
        # Initialize the banner lines to default content
        self._lines: list[object] = list(content)
        # Check if the first line tuple is a default to string, 
        # as a tuple with just one element, and if the element is a string defaults to a string type
        # if the line tuple is a string, the inner width is the maximum comparison between inner_width and the string length
        if isinstance(self._lines[0], str): 
            # Compare and return the largest value + 4
            self.inner_width = max( 
                                    len(self._lines[0]),inner_width
                                ) + 4 # inner padding
        else: 
            # Compare lines text elements and return the text element largest lenght value + 4
            self.inner_width = max( 
                                    # Compare and return the largest value
                                    max(# if the line tuple is empty it returns 0
                                        # else it iterates through all the line tuple text elements
                                        # and return the length of each line tuple text element
                                        (0 if not t else len(t[0])) for t in self._lines
                                    ), 
                                    self.MINIUM_WIDTH
                                ) + 4
    # -------------------------------------------------------------- end __init__()

    # ______________________ 
    # Banner render helper methods
    
    # -----------------
    # line render helper method
    def _text_line(self, text: str, alignment: Alignment) -> str:
        """Build a text line, aligned inside the banner borders

        Examples:
            ║  First line (Header)  ║
        """
        # Left align the text by adding spaces to the right of the text
        if alignment == "left":
            return f"║ {text.ljust(self.inner_width -2)} ║"
        # Right align the text by adding spaces to the left of the text
        if alignment == "right":
            return f"║ {text.rjust(self.inner_width -2)} ║"
        # Center align the text by adding spaces on both sides of the text
        return f"║ {text.center(self.inner_width - 2)} ║"

    # -----------------
    # Banner borders render helper methods

    # -------------------------------------------------------------- _top()
    # Top border line for the banner
    def _top(self) -> str:
        """Build top banner border.

        Examples:
            ╔═══════════════════════╗
        """
        
        return f"╔{'═' * self.inner_width}╗"
    # --------------------------------------------------------------

    # -------------------------------------------------------------- _divider()
    def _divider(self) -> str:
        """Build borderline divider after the first text line.

        Notes: if the Banner has one line it gets replaced by 
            the Banner bottom line in the render method

        Examples:
            ╠═══════════════════════╣
        """
        return f"╠{'═' * self.inner_width}╣"
    # --------------------------------------------------------------

    # -------------------------------------------------------------- _bottom()
    def _bottom(self) -> str:
        """Return the bottom border line for the banner.

        Examples:
            ╚═══════════════════════╝
        """
        return f"╚{'═' * self.inner_width}╝"
    # --------------------------------------------------------------

    # ______________________ 
    # Render banner to one string
    #
    # -------------------------------------------------------------- render()
    def render(self) -> str:
        """Render the full banner as a single string, including first lines, other line if any, 
            border elements.

        Example:
                ╔══════════════╗
                ║  First line  ║ # Default alignment and isDivider
                ║              ║ # Second Line empty
                ║ Third Line   ║ # Aligns to the left and adds a divider
                ╠══════════════╣
                ║ Fourth Line  ║ # Aligns to the right and default isDivider
                ╚══════════════╝
        """
        # Add top border (e.g., "╔════╗") banner string
        banner = [self._top()]
        # For each Loop, loops over the line tuple list (_lines)
        for line in self._lines: 
            # Empty line tuple e.g., ()    
            if not line: 
                txt = ""
                align = self.DEFAULT_ALIGNMENT 
                isDiv = self.DEFAULT_ISDIVIDER
            # Check if the line tuple has defaulted to string, 
            # as a tuple with just one element, and if the element is string, defaults to a string type
            # ("Option")
            elif isinstance(line, str):
                txt = line
                align = self.DEFAULT_ALIGNMENT 
                isDiv = self.DEFAULT_ISDIVIDER              
            # Line tuple with more than one element set
            # e.g. ("Option", "left") or ("Option", "left", True)
            else:
                txt = line[0]
                align = line[1]
                # set the divider flag to the default value if no flag value was set, else to the set value
                isDiv = self.DEFAULT_ISDIVIDER if len(line) < 3 else line[2]
            # add text line (e.g., "║  First line  ║" ) to banner string
            banner.append(self._text_line(txt, align))
            # add border divider (e.g., "╠═════╣") if flag is true to banner string 
            if isDiv: banner.append(self._divider())
        # add bottom (e.g.,"╚══════╝") border to banner string
        banner.append(self._bottom())
        return "\n".join(banner) # add a return in the front of banner string 
    # -------------------------------------------------------------- end render()

# ------------------------------------------------------------------------- end class Banner

# __________________________________________________________________________
# Utility Classe Menu
#
# =========================================================================
# Menu Class Functionality (uses the Banner class)
# =========================================================================
# ------------------------------------------------------------------------- class Menu
class Menu:
    """The menu class renders a console menu using the Banner class.

    Examples:
        >>> menu = Menu("Menu Example", ["Option", "Option", "Option"])
        >>> print(menu.render())
            ╔══════════════════════╗
            ║     Menu Example     ║
            ╠══════════════════════╣
            ║ 1. Option            ║
            ║ 2. Option            ║
            ║ 3. Option            ║
            ╚══════════════════════╝
    """
    # ______________________ 
    # Constructor
    #
    # -------------------------------------------------------------- __init__()
    def __init__(
        self,
        title: str = "Menu",
        options: Sequence[str] = ["Option", "Option", "Option"],
        inner_width: int = 10,
        prefixes: Sequence[str] | None = None,
    ) -> None:
        """Create a new menu.

        Args:
            title: title text displayed in the menu header
            options: option lines
            inner_width: the minimum inner banner width
            prefixes: optional custom prefixes for options (e.g., ['a', 'r', 'c'])
                     If None, uses numbered prefixes (1, 2, 3...)

        Examples:
            >>> menu = Menu("Menu", ["Start", "Exit"], inner_width=25)
            >>> menu_custom = Menu("MENU", ["Add", "Remove"], prefixes=['a', 'r'])
        """
        # Validate we have at least one option; otherwise selection makes no sense
        if not options:
            raise ValueError("Menu requires at least one option.")

        # Validate prefixes length matches options length if provided
        if prefixes is not None and len(prefixes) != len(options):
            raise ValueError("Number of prefixes must match number of options.")

        # Initialize Variables with entered values
        self._title = title
        self._options = list(options)
        self._inner_width = inner_width
        self._prefixes = list(prefixes) if prefixes is not None else None

        # Build formatted options based on prefix type
        if self._prefixes is None:
            # Use numbered prefixes (1, 2, 3...) with ". " separator
            self._formatted_options = [
                f"{index}. {text}" for index, text in enumerate(self._options, start=1)
            ]
        else:
            # Use custom prefixes with " - " separator
            self._formatted_options = [
                f"{prefix} - {text}" for prefix, text in zip(self._prefixes, self._options)
            ]

        # Initialize banner first line by adding the menu header
        self._menu_lines = [ # First line of the Banner object
                (self._title, "center", True)
            ]
        # Initialize banner additional line by adding the menu options
        for option in self._formatted_options:
            self._menu_lines.append((option, "left"))

        # Instantiate the menu as a Banner object
        self._menu = Banner(self._menu_lines)
    # -------------------------------------------------------------- end __init__()

    # ______________________ 
    # Menu constructor helper methods
    #
    # -------------------------------------------------------------- _choices()
    def _choices(self) -> list[str]:
        """Return available choice indices as strings (e.g., ["1", "2"]) 

        Examples:
            >>> Menu("Menu Range", ["Option-1", "Obtion-2"])._choices()
            ['1', '2']
        """
        return [str(index) for index in range(1, len(self._options) + 1)]
    # -------------------------------------------------------------- 

    # -------------------------------------------------------------- _choice_index_range()
    def _choice_index_range(self) -> str:
        """Return a string of the index range (e.g., "1-3" or "1")

        Can be used to prompt user to enter a number related to the wanted option

        Examples:
            >>> Menu("Menu List", ["Option"])._choice_index_range()
            "1"
            >>> Menu("Menu List", ["Option-1", "Obtion-2"])._choice_index_range()
            "1-3"
        """
        options = self._choices() # List of choice indices
        # If there is only one option
        if len(options) == 1:
            return options[0] # "1"
        # Else range (e.g., "1-3")
        return f"{options[0]}-{options[-1]}"  
    # -------------------------------------------------------------- 

    # -------------------------------------------------------------- _choice_index_list()
    def _choice_index_list(self) -> str:
        """Return a list of choices based on option indices (e.g., "1, 2, or 3")
        
        Can be used to prompt to enter a number related to the wanted option

        Examples:
            >>> menu = Menu("Menu list", ["Option"])._choice_index_list()
            "1"
            >>> Menu("Pair", ["First", "Second"])._choice_index_list()
            "1, or 2"
        """
        options = self._choices() # List of choice indices
        # only one choice index exists
        if len(options) == 1:
            return options[0] # "1"
        # Else list (e.g., "1, 2, or 3")
        return ", ".join(options[:-1]) + f", or {options[-1]}"
    # -------------------------------------------------------------- 

    # -------------------------------------------------------------- render()
    def render(self) -> "Banner Rendered":
        """Render the menu, including title and numbered options

        Examples:
            >>> menu = Menu("Menu Example", ["Option", "Option", "Option"])
            >>> print(menu.render())
            ╔══════════════════════╗
            ║     Menu Example     ║
            ╠══════════════════════╣
            ║ 1. Option            ║
            ║ 2. Option            ║
            ║ 3. Option            ║
            ╚══════════════════════╝
        """
        return self._menu.render()        
    # -------------------------------------------------------------- 
    
# ------------------------------------------------------------------------- end class Menu
