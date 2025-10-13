# File: average_rain_and_csu_book.py
# Project:
# Author: Alexander Ricciardi
# Date: 2025-10-12
# File Path: Critical-Thinking-Module-5/average_rain_and_csu_book.py
# ------------------------------------------------------------------------
# Course: CSS-500 Principles of Programming
# Professor: Dr. Brian Holbert
# Fall C-2025
# Sep-Nov 2025
# ------------------------------------------------------------------------
# Assignment:
# Critical Thinking Module 5
#
# Directions:
# Part 1:
# Write a program that uses nested loops to collect data
# and calculate the average rainfall over a period of years.
# The program should first ask for the number of years.
# The outer loop will iterate once for each year.
# The inner loop will iterate twelve times, once for each month.
# Each iteration of the inner loop will ask the user for the inches of rainfall for that month.
# After all iterations, the program should display the number of months,
# the total inches of rainfall, and the average rainfall per month for the entire period.
#
# Part 2:
# The CSU Global Bookstore has a book club that awards points
# to its students based on the number of books purchased each month. The points are awarded as follows:
#
# If a customer purchases 0 books, they earn 0 points.
# If a customer purchases 2 books, they earn 5 points.
# If a customer purchases 4 books, they earn 15 points.
# If a customer purchases 6 books, they earn 30 points.
# If a customer purchases 8 or more books, they earn 60 points.
# Write a program that asks the user to enter the number of books that they have purchased this month
# and then display the number of points awarded.
# -------------------------------------------------------------------------

# --- Program Description ---
# The program is a small console-based program consisting of 2 parts.
# Part 1 implements Rainfall Average Calculator 
# Pert 2 implements Bookstore Points calculates
# -------------------------------------------------------------------------

# --- Imports ---
# - Standard Library: dataclasses (data containers), decimal.Decimal (currency)
# - Typing Utilities: typing (Any and related hints)
# - Third-Party: numpy (array math), colorama (console color)
# - Project Utility Modules:
#   - menu_banner_utilities (ASCII banner and menu)
#   - validation_utilities (input prompt and validation)
# --- Requirements ---
# - Python 3.12
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
The program is a small console-based program consisting of 2 parts.

-	Part 1 - Rainfall Average Calculator captures rainfall data from user inputs 
    and calculates the rainfall average from the inputted per-month rainfall for the inputted number of years. 
    Then display the results in the console.
-	Part 2 - Bookstore Points calculates the Bookstore club points based on a tier system 
    from the user inputted number of books purchased and displays the results.
"""

from __future__ import annotations

# __________________________________________________________________________
# Imports
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

import numpy as np
from colorama import Fore, Style

# ======================================================= Added Utilities
from menu_banner_utilities import Menu, Banner
from validation_utilities import (
    validate_prompt_int,
    validate_prompt_positive_float,
    validate_prompt_positive_int,
    validate_prompt_yes_or_no,
    wait_for_enter,
)

# ======================================================= Assignment

# =============================================================
# ||                                                         || 
# ||      Part 1: Rainfall Average Calculator                ||
# ||                                                         ||
# =============================================================
# ____________________________________________________________________________
# Classes Definitions
#

# ------------------------------------------------------------------------- class RainfallAvgCalculator
@dataclass()
class RainfallAvgCalculator:
    """Store rainfall data and compute average.

    Attributes:
        years: int, number of years 
        data: Numpy array, stores rainfall by year (rows) and month (columns)

    Example:
        >>> rain_avg = RainfallAvgCalculator(years=2)
        >>> rain_avg.record(0, 0, 2.5)
        >>> rain_avg.data.shape
        (2, 12)
    """

    years: int
    data: np.ndarray = field(init=False, repr=False) # Used to store rainfall by year and month

    #______________________________________
    # constructor setup
    # --------------------------------------------------------------  __post_init__()
    def __post_init__(self) -> None:
        """Initialize the two-dimensional rainfall array, year (rows) and month (columns)"""
    
        # Populate the array with zeros, year = num. (rows) of years and month = 12 (columns)
        self.data = np.zeros((self.years, 12), dtype=float)
    # --------------------------------------------------------------

    #______________________________________
    # Attribute functions
    #

    # --------------------------------------------------------------  total_months()
    @property
    def total_months(self) -> int:
        """Return the total number of months"""
        return self.years * 12
    # --------------------------------------------------------------

    # --------------------------------------------------------------  total_inches()
    @property
    def total_inches(self) -> float:
        """Return the total rainfall based on all recorded months"""
        return float(np.sum(self.data))
    # --------------------------------------------------------------

    #______________________________________
    # Attribute functions
    #

    # -------------------------------------------------------------- record()
    def record(self, year_index: int, month_index: int, value: float) -> bool:
        """Store a single month's rainfall data in array

        Args:
            year_index: year index corresponding to the year
            month_index: month index corresponding to the month
            value: Rainfall in inches

        Returns:
        none

        raise:
        IndexError and ValueError            

        Example:
            >>> rain_avg = RainfallAvgCalculator(years=1)
            >>> rain_avg.record(0, 0, 1.25)
            >>> rain_avg.data[0, 0]
            1.25
        """
        # Safe guard, just in case..
        try:
            if not 0 <= year_index < self.years:
                raise IndexError("year_index is out of range for the configured years")
            if not 0 <= month_index < 12:
                raise IndexError("month_index must be between 0 and 11 inclusive")
            if value < 0:
                raise ValueError("value must be non-negative")
        except (IndexError, ValueError) as exc:
            print(f"Invalid rainfall entry: {exc}")
            raise
        
        # Record the rainfall value in array
        self.data[year_index, month_index] = value 
    # -------------------------------------------------------------- 

    # -------------------------------------------------------------- average()
    def average(self) -> float:
        """Calculate the average rainfall from stored data.

        Returns:
            Average rainfall in inches.

        Example:
            >>> rain_avg = RainfallAvgCalculator(years=1)
            >>> rain_avg.record(0, 0, 3.0)
            >>> round(rain_avg.average(), 2)
            0.25
        """

        # safeguard, check if it is no data recorded
        if self.data.size == 0: 
            return 0.0 
        # computes the mean from the data and returns it
        return float(np.mean(self.data))
    # -------------------------------------------------------------- 

    # -------------------------------------------------------------- summary()
    def summary(self) -> str:
        """Compute formatted rainfall statistics for display.

        Returns:
            Formatted string storing the total months, total inches, and per-month average.

        Example:
            >>> rainfall_avg = RainfallAvgCalculator(years=1)
            >>> rainfall_avg.record(0, 0, 12.0)
            >>> "Average rainfall per month" in rainfall_avg.summary()
            True
        """

        # Format computed data values into colorized string
        total_inches = Fore.LIGHTMAGENTA_EX + f"{self.total_inches:.2f}" + Style.RESET_ALL
        total_months = Fore.LIGHTMAGENTA_EX + f"{self.total_months}" + Style.RESET_ALL
        avg = Fore.LIGHTMAGENTA_EX + f"{self.average():.2f}" + Style.RESET_ALL

        # Return a formatted string with computed results
        return (
            f"Number of months: {total_months}\n"
            f"Total inches of rainfall: {total_inches}\n"
            f"Average rainfall per month: {avg}"
        )
    # --------------------------------------------------------------

# -------------------------------------------------------------- end class RainfallAvgCalculator

# -------------------------------------------------------------- run_rainfall_avg_calculator()
def run_rainfall_avg_calculator() -> None:
    """Collect rainfall data across years and display aggregate statistics.

    Returns:
        None.

    Example:
        >>> run_rainfall_avg_calculator()  
    """
    
    while True:
        # Prompt user to enter the number of years
        years = validate_prompt_positive_int("Enter the number of years to analyze: ")
        # if the positive value of years is equal to 0, it displays an error message
        if years == 0:
            print("years must be a nonzero positive integer")
        else:
            break # exits while loop, years is a nonzero positive integer
    
    # Create a RainfallAvgCalculator object to store rainfall inputted data 
    # based on the inputted num. of years
    rain_avg = RainfallAvgCalculator(years=years)

    # --- Assignment requirement, nested loops to collect data 
    # and calculate the average rainfall over a period of years ---
    # Number of years loop
    for year_index in range(1, years + 1):
        # Months loop capture monthly rainfall input (12 months)
        print(f"\n---- Year {year_index} ----")
        for month_index in range(1, 13):
            # Format year and month values into colorize strings
            year_display = Fore.LIGHTMAGENTA_EX + f"{year_index}" + Style.RESET_ALL
            month_display = Fore.LIGHTMAGENTA_EX + f"{month_index}" + Style.RESET_ALL
            rainfall_prompt = (
                "Enter rainfall (in inches) for "
                f"Year {year_display}, Month {month_display}: "
            )
            # Prompt user to enter rainfall amount in inches for a given month in a given year
            # validate and capture rainfall input
            rainfall = validate_prompt_positive_float(rainfall_prompt)
            # Store each month's inputted data for a given year
            rain_avg.record(year_index - 1, month_index - 1, rainfall)
    
    # Computer average rainfall from the rainfall data and display results
    print()
    print(rain_avg.summary())
    wait_for_enter()
# -------------------------------------------------------------- end run_rainfall_avg_calculator()

# -------------------------------------------------------------- run_rainfall_menu()
def run_rainfall_menu() -> None:
    """Render a Rainfall Average Calculator submenu 
    
    Example:
        >>> run_rainfall_menu() 
        ╔════════════════════════════════════════════════╗
        ║          Rainfall Average Calculator           ║
        ╠════════════════════════════════════════════════╣
        ║ 1. Enter rainfall and show summary             ║
        ║ 2. Back                                        ║
        ╚════════════════════════════════════════════════╝

    Returns:
        None.
    """

    options = [
        "Enter rainfall and show summary",
        "Back",
    ]
    # Create a Menu object for the Rainfall Average Calculator menu
    menu_rainfall = Menu("Rainfall Average Calculator", options)
    # Render the menu and store it in a string variable to be displayed
    menu_rainfall_display = Fore.LIGHTCYAN_EX + menu_rainfall.render()

    print(menu_rainfall_display)

    # Menu loop
    while True:
        # Prompt the user for selection and captures it
        selection = validate_prompt_positive_int("Please enter your selection: ") 
        print()
        match selection:
            case 1: # Launch the Rainfall Average Calculator, Part 1 of the assignment
                run_rainfall_avg_calculator() 
                print()
                print(menu_rainfall_display)
            case 2:
                return # Ends run_rainfall_menu() - back to main menu
            case _:
                 # the input was not a recognized menu choice; guide the user
                print(
                    Fore.LIGHTRED_EX
                    + f"Invalid selection. Please enter {menu_rainfall._choice_index_list()}."
                )

# -------------------------------------------------------------- end run_rainfall_menu()

# =============================================================
# ||                                                         || 
# ||                 Part 2: Bookstore Points                ||
# ||                                                         ||
# =============================================================

# -------------------------------------------------------------- run_bookstore_points()
def run_bookstore_points() -> None:
    """Prompt for books purchased and report the awarded points.

    Returns:
        None.

    Example:
        >>> # Requires interactive input; launch within a console session.
        >>> run_bookstore_points()  # doctest: +SKIP
    """

    points = 0


    # Prompt user to enter the number of books purchases
    # validate and capture num. books input
    books = validate_prompt_positive_int("\nThe number of books: ")

    # -- Assignment requirement -- 
    # If a customer purchases 0 books, they earn 0 points
    # next tier is trigged when the customer purshases 2 books 
    # so if the customer purchases 1 book they also earns 0 points
    # The tiers are:
    # - Tier-1 = 0 to 1 books -> 0 points
    # - Tier-2 = 2 to 3 books -> 5 points
    # - Tier-3 = 4 to 5 books -> 15 points
    # - Tier-4 = 6 to 7 books -> 30 points
    # - Tier-5 = 8 or more books -> 60 points
    if books <=1: # Tier-1 
        points = 0
    elif books <= 3: # Tier-2
        points = 5
    elif books <= 5: # Tier-3
        points = 15
    elif books <= 7: # Tier-4 
        points = 30
    else:            # Tier-5
        points = 60

    # Format the number of books and points values into colorize strings
    books_str = Fore.LIGHTMAGENTA_EX + f"{books}" + Style.RESET_ALL
    points_str = Fore.LIGHTMAGENTA_EX + f"{points}" + Style.RESET_ALL
    
   # Display the num. of books and the related points earn
    print(f"\nBooks purchased: {books_str}")
    print(f"Points awarded: {points_str}")
    wait_for_enter()
# -------------------------------------------------------------- end run_bookstore_points()

# -------------------------------------------------------------- run_bookstore_menu()
def run_bookstore_menu() -> None:
    """Render a Bookstore Points submenu 
    
    Example:
        >>> run_bookstore_menu() 
        ╔═════════════════════════════════════════╗
        ║             Bookstore Points            ║
        ╠═════════════════════════════════════════╣
        ║ 1. Compute points for books purchased   ║
        ║ 2. Back                                 ║
        ╚═════════════════════════════════════════╝

    Returns:
        None.
    """

    options = [
        "Compute points for books purchased",
        "Back",
    ]
    # Create a Menu object for the Bookstore Points menu
    menu_bookstore = Menu("Bookstore Points", options)
    # Render the menu a store it in a string variable to be displayed
    menu_bookstore_display = Fore.LIGHTCYAN_EX + menu_bookstore.render()
   
    print(menu_bookstore_display)

    # Menu loop
    while True:
         # Prompt the user for selection and captures it
        selection = validate_prompt_positive_int("Please enter your selection: ")
        match selection:
            case 1: # Launch the Bookstore Points calculator, Part 2 of the assignment
                run_bookstore_points()
                print()
                print(menu_bookstore_display)
            case 2:
                return # Ends run_bookstore_menu() - back to main menu
            case _:
                 # the input was not a recognized menu choice; guide the user
                print(
                    Fore.LIGHTRED_EX
                    + f"Invalid selection. Please enter {menu_bookstore._choice_index_list()}."
                )
# -------------------------------------------------------------- end run_bookstore_menu()

# __________________________________________________________________________
# -------------- Main Function --------------
#__________________________________________________________________________
# =========================================================================
# Main Application Flow Functionality (program entry and user interaction)
# =========================================================================

# -------------------------------------------------------------- main()
def main() -> None:
    """Program entry point runs the program, display the main menu

    Example:
        ╔══════════════════════════════════════════╗
        ║                 Main Menu                ║
        ╠══════════════════════════════════════════╣
        ║ 1. Part 1: Rainfall Average Calculator   ║
        ║ 2. Part 2: Bookstore Points              ║
        ║ 3. Exit                                  ║
        ╚══════════════════════════════════════════╝

    Returns:
        None.
    """
    
    # Create the program banner
    main_banner = Banner([("Rainfall Average Calculator & Book Points")])
    # Render the banner and store it in a string variable to be displayed
    main_banner_display = Fore.LIGHTGREEN_EX + main_banner.render()
    
    options = [
        "Part 1: Rainfall Average Calculator",
        "Part 2: Bookstore Points",
        "Exit",
    ]

    # Create a Menu object for the Main Menu menu
    menu_main = Menu("Main Menu", options)
    # Render the menu a store it in a string variable to be displayed
    menu_main_display = Fore.YELLOW + menu_main.render()
    
    
    print(main_banner_display)
    print()
    print(menu_main_display)
    
    # Main menu loop
    while True:
        # Prompt the user for selection and captures it
        selection = validate_prompt_positive_int("Please enter your selection: ")
        print()
        match selection:
            # =============================================================
            # ||                Part 1: Rainfall Average Calculator                ||
            # =============================================================
            case 1: # Launch the Rainfall Average Calculator, Part 1 of the assignement
                run_rainfall_menu()
                print(menu_main_display)
            # =============================================================
            # ||                 Part 2: Bookstore Points                ||
            # =============================================================
            case 2: # Launch the Bookstore Points caculator, Part 2 of the assignmemt
                run_bookstore_menu()
                print(menu_main_display)
            case 3:
                if (validate_prompt_yes_or_no("Are you sure that you want to exist? ")):
                    print("\nBye! 👋\n")
                    return # Ends main() function - exits program
            case _:
                 # the input was not a recognized menu choice; guide the user
                print(
                    Fore.LIGHTRED_EX
                    + f"Invalid selection. Please enter {menu_main._choice_index_list()}."
                )
# -------------------------------------------------------------- end main()

# __________________________________________________________________________
# Module Initialization / Main Execution Guard
# -------------------------------------------------------------------------

# -------------------------------------------------------------- main_guard
if __name__ == "__main__":
    main()
# -------------------------------------------------------------- 

# __________________________________________________________________________
# End of File
# 
