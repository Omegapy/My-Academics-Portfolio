#-------------------------------------------------------------------------
# File: online_shopping_cart_v2.py
# Project:
# Author: Alexander Ricciardi
# Date: 2025-10-15
# File Path: Portfolio-Milestone-Module-6/online_shopping_cart_v2.py
# ------------------------------------------------------------------------
# Course: CSS-500 Principles of Programming
# Professor: Dr. Brian Holbert
# Fall C-2025
# Sep-Nov 2025
# ------------------------------------------------------------------------
# Assignment:
# Portfolio Milestone Module 6
#
# Directions:
# Online Shopping Cart - Continue from Portfolio Milestone Module 4 
# that implemented steps 1 through 3, this module integrates steps 4 through 6
#
# Step 1: Build the ItemToPurchase class with the following specifications:
#  •	Attributes
#  •	item_name (string)
#  •	item_price (float)
#  •	item_quantity (int)
#  •	Default constructor
#  •	Initializes item's name = "none", item's price = 0, item's quantity = 0
#  •	Method
#  •	print_item_cost()
# Example of print_item_cost() output:
# Bottled Water 10 @ $1 = $10
#
# Step 2: In the main section of your code, prompt the user for two items 
# and create two objects of the ItemToPurchase class.
# Example:
#   Item 1
#   Enter the item name:
#   Chocolate Chips
#   Enter the item price:
#   3
#   Enter the item quantity:
#   1
#
#   Item 2
#   Enter the item name:
#   Bottled Water
#   Enter the item price:
#   1
#   Enter the item quantity:
#   10
#
# Step 3: Add the costs of the two items together and output the total cost.
#   Example:
#   TOTAL COST
#   Chocolate Chips 1 @ $3 = $3
#   Bottled Water 10 @ $1 = $10
#   Total: $13
#
# -------------------------------------------------------------------------
# NOTE: Steps 2-3 are NOT included in this version's main() function.
# The program starts with an empty cart and uses the menu system (Steps 5-6) to add items.
# -------------------------------------------------------------------------
#
# Step 4: Build the ShoppingCart class with the following data attributes and related methods. 
# Note: Some can be method stubs (empty methods) initially, to be completed in later steps
#
# Parameterized constructor, which takes the customer name and date as parameters
# Attributes:
# - customer_name (string) - Initialized in default constructor to "none"
# - current_date (string) - Initialized in default constructor to "January 1, 2020"
# - cart_items (list)
#
# Methods:
# - add_item(): 
#   Adds an item to cart_items list. 
#   Has parameter ItemToPurchase. 
#   Does not return anything.
#
# - remove_item():
#   Removes item from cart_items list. 
#   Has a string (an item's name) parameter. 
#   Does not return anything.
#   If item name cannot be found, output this message: 
#      Item not found in cart. Nothing removed.
# - modify_item():
#   Modifies an item's description, price, and/or quantity. 
#   Has parameter ItemToPurchase. Does not return anything.
#   If item can be found (by name) in cart, check if parameter has default values for description, price, 
#   and quantity. If not, modify item in cart.
#   If item cannot be found (by name) in cart, output this message: 
#      Item not found in cart. Nothing modified.
#
# - get_num_items_in_cart()
#   Returns quantity of all items in cart. 
#   Has no parameters.
#
# - get_cost_of_cart()
#   Determines and returns the total cost of items in cart. 
#   Has no parameters.
# - print_total()
#   Outputs total of objects in cart.
#   If cart is empty, output this message: 
#      SHOPPING CART IS EMPTY
#
# - print_descriptions()
#   Outputs each item's description.
#
# Example of print_total() output:
#    John Doe's Shopping Cart - February 1, 2020
#    Number of Items: 8
#    Nike Romaleos 2 @ $189 = $378
#    Chocolate Chips 5 @ $3 = $15
#    Powerbeats 2 Headphones 1 @ $128 = $128
#    Total: $521
#
# Example of print_descriptions() output:
#    John Doe's Shopping Cart - February 1, 2020
#    Item Descriptions
#    Nike Romaleos: Volt color, Weightlifting shoes
#    Chocolate Chips: Semi-sweet
#    Powerbeats 2 Headphones: Bluetooth headphones
#
# Step 5: 
# In the main section of your code, implement 
# - the print_menu() function. 
#   print_menu() has a ShoppingCart parameter and outputs a menu of options to manipulate the shopping cart. 
#   Each option is represented by a single character. Build and output the menu within the function.
#   If an invalid character is entered, continue to prompt for a valid selection. Hint: 
#      Implement Quit before implementing other options. 
#      Call print_menu() in the main() function. 
#      Continue to execute the menu until the user enters q to Quit.
#
# Example:
#   MENU
#   a - Add item to cart
#   r - Remove item from cart
#   c - Change item quantity
#   i - Output items' descriptions
#   o - Output shopping cart
#   q - Quit
#   Choose an option:
#
# Step 6: Implement Output shopping cart menu option. 
# Implement Output item's description menu option.
#
# Example of shopping cart menu option:
#   OUTPUT SHOPPING CART
#   John Doe's Shopping Cart - February 1, 2020
#   Number of Items: 8
#   Nike Romaleos 2 @ $189 = $378
#   Chocolate Chips 5 @ $3 = $15
#   Powerbeats 2 Headphones 1 @ $128 = $128
#   Total: $521
#
# Example of item description menu option.
#   OUTPUT ITEMS' DESCRIPTIONS
#   John Doe's Shopping Cart - February 1, 2020
#   Item Descriptions
#   Nike Romaleos: Volt color, Weightlifting shoes
#   Chocolate Chips: Semi-sweet
#   Powerbeats 2 Headphones: Bluetooth headphones
# ------------------------------------------------------------------------
# Project:
# Online Shopping Cart
#
# Project description:
# The program is a small console app. that implements the functionality of 
# an online shopping cart.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: ItemToPurchase
# - Class: ShoppingCart
# - Function: prompt_for_item_info
# - Function: print_menu
# - Function: main
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: 
#   - dataclasses (data containers and auto-generated init/repr methods)
#   - copy (copies objects for menu/banner templates when needed)
# - Third-Party: 
#   - colorama (console color utilities)
# - Local Project Modules: 
#   - menu_banner_utilities (render ASCII banners and menus)
#   - validation_utilities (input validation functions)
# --- Requirements ---
# - Python 3.13
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
Online Shopping Cart Version 2
The console online shopping cart program is contained in this file
implements the functionality of an online shopping cart,
it displays simple banners and a menu.
This module implements Steps 4-6 (ShoppingCart class and menu system).
It provides a menu for the shopping cart.
Users can add, remove, and modify items through the menu.
"""

# __________________________________________________________________________
# Imports
#
# For annotations (type hints/docstrings)
from __future__ import annotations

# Standard library imports
from dataclasses import dataclass
from copy import deepcopy
# Third party library
from colorama import Fore, Style

# Import utilities from same directory
from menu_banner_utilities import Banner, Menu
from validation_utilities import (
    validate_prompt_string,
    validate_prompt_nonezero_positive_int,
    validate_prompt_nonezero_positive_float,
    validate_prompt_yes_or_no,
    validate_prompt_date,
    wait_for_enter,
)

# ===========================================================================
# ||                                                                       ||
# ||                 Step 1: Build the ItemToPurchase class                ||
# ||                                                                       ||
# ===========================================================================
# ____________________________________________________________________________
# Classes Definitions
#
# =========================================================================
# ItemToPurchase Class Functionality (domain model for line items)
# =========================================================================
# ------------------------------------------------------------------------- class ItemToPurchase
@dataclass
class ItemToPurchase:
    """Represent an item (to be ppurchased) managed by the shopping cart.

    Attributes:
        item_name: Name of the item
        item_price: Price per unit
        item_quantity: Quantity to purchase
        item_description: Description for display (Step 4 requirement)

    Examples:
        >>> item = ItemToPurchase(item_name="Apples", item_price=1.5, item_quantity=2)
        >>> item.item_name, item.item_price, item.item_quantity
        ('Apples', 1.5, 2)
    """

    # Initializes item variables 
    item_name: str = "none"
    item_price: float = 0.0
    item_quantity: int = 0

    # Step 4 requirement (for print_descriptions)
    item_description: str = "none"

   # -------------------------------------------------------------- format_currency() 
   # Used by print_item_cost()
    @staticmethod
    def format_currency(value: float) -> str:
        """Format a numeric value for currency-like display without excess zeros

        Notes:
            Used by menu option o - Output shopping cart

        Args:
            value: Raw numeric value coming from the backend or router layer.

        Returns:
            Currency string trimmed to at most two decimals.
            Ensures CLI and router payloads stay aligned.

        Examples:
            >>> ItemToPurchase.format_currency(2.0)
            '2'
            >>> ItemToPurchase.format_currency(2.5)
            '2.5'
            >>> ItemToPurchase.format_currency(2.75)
            '2.75'
        """
        # if the value is a whole number, it drops the decimal portion
        if value == int(value):
            return str(int(value))
        # else format to the two decimal places and remove trailing zeros
        return f"{value:.2f}".rstrip("0")
    # ------------------------------------------------------------

    # ------------------------------------------------------------ print_item_cost()
    def print_item_cost(self, display_name: str | None = None) -> str:
        """Print and return the formatted cost line for this item.

        Args:
            display_name: Optional capitalized name to display (if None, uses item_name as-is)

        Returns:
            A line-item cost string (for example, "Apples 3 @ $1 = $3")

        Examples:
            >>> ItemToPurchase(item_name="W", item_price=2.0, item_quantity=3).print_item_cost())
            'W 3 @ $2 = $6'
        """
        # Use provided display name or default to item_name
        name_to_display = display_name if display_name is not None else self.item_name

        # compute the item total based on price and quatity
        total_cost = self.item_price * self.item_quantity
        # Format item info into a string to be displayed
        cost_statement = (
            Fore.LIGHTYELLOW_EX +
            f"{name_to_display.title()} {self.item_quantity} @ "
            f"${self.format_currency(self.item_price)} = "
            f"${self.format_currency(total_cost)}"
            + Style.RESET_ALL
        )
        # Echo the formatted cost to the console for immediate feedback.
        print(cost_statement)
        # Return the cost so it can be reuse or used for testing
        return cost_statement
     # ------------------------------------------------------------

# ------------------------------------------------------------------------- end class ItemToPurchase

# ===========================================================================
# ||                                                                       ||
# ||                 Step 4: Build the ShoppingCart class                  ||
# ||                                                                       ||
# ===========================================================================
# =========================================================================
# ShoppingCart Class Functionality 
# =========================================================================
# ------------------------------------------------------------------------- class ShoppingCart
class ShoppingCart:
    """Manage customer shopping cart items (ItemToPurchase instances).

    This class simulates an online shopping cart functionality

    Attributes:
        customer_name: Name of the customer that owns the cart.
        current_date: Date associated with the shopping session.
        cart_items: Mutable list of tracked items.
    """

    # ______________________ 
    # Constructor
    #
    # -------------------------------------------------------------- __init__()
    def __init__(
        self,
        customer_name: str = "none",
        current_date: str = "January 1, 2020"
    ) -> None:
        """Initialize cart with customer info.

        Args:
            customer_name: customer name associated with the cart 
            current_date:  date associated with the cart
        """
        self.customer_name = customer_name
        self.current_date = current_date
        self.cart_items: list[ItemToPurchase] = []
    # --------------------------------------------------------------

    # ______________________ 
    # Getters
    #

    # ------------------------------------------------------------- get_num_items_in_cart()
    def get_num_items_in_cart(self) -> int:
        """Return total quantity of all items.

        Returns:
            Combined quantity count across every tracked item.

        Examples:
            >>> cart = ShoppingCart("User", "February 1, 2020")
            >>> cart.add_item(
            ...     ItemToPurchase(item_name="Tomatos", 
                                    item_description = "fruit"
                                    item_quantity=2,
                                    item_price=1.5
                                )
            ... )
            >>> cart.get_num_items_in_cart()
            2
        """
        return sum(item.item_quantity for item in self.cart_items)
    # -------------------------------------------------------------

    # ------------------------------------------------------------- get_cost_of_cart()
    def get_cost_of_cart(self) -> float:
        """Return total cost of all items.

        Note:
            Used by menu option a - Add item to cart

        Returns:
            Total cost of all the items in the cart

        Examples:
            >>> cart = ShoppingCart("User", "February 1, 2020")
            >>> cart.add_item(
            ...     ItemToPurchase(item_name="Widget", item_price=2.5, item_quantity=2),
            ... )
            >>> cart.get_cost_of_cart()
            5.0
        """
        return sum(item.item_price * item.item_quantity for item in self.cart_items)
    # -------------------------------------------------------------

    # ______________________ 
    # Setters
    #
    
    # -------------------------------------------------------------- add_item()
    def add_item(self, item: ItemToPurchase) -> None:
        """Add item to cart.
        
        Notes:
            Used by menu option a - Add item to cart

        Args:
            item: populated item object to add

        Examples:
            >>> cart = ShoppingCart("User", "February 1, 2020")
            >>> cart.add_item(
            ...     ItemToPurchase(item_name="Orange", item_price=5.0, item_quantity=1),
            ... )
        """
        self.cart_items.append(item)
    # -------------------------------------------------------------

    # ------------------------------------------------------------- modify_item()
    def modify_item(self, item: ItemToPurchase) -> None:
        """Modify an existing item by name, updating only non-default fields.

        Note:
            Used by menu option c - Change item quantity

        Args:
            item: Item containing updated values from the caller.

        Returns:
            None. Updates occur in place so the API routers and CLI menu share the same state.

        Notes: --- Meets the assignment Requirement about the modify_item() method --- 
            Default values to check:
                item_description: "none"
                item_price: 0.0
                item_quantity: 0

            Error message: "Item not found in cart. Nothing modified."
        """

        # Format customer name and date into a colorized string
        print(Fore.LIGHTYELLOW_EX + f"\n{self.customer_name.title()}'s Shopping Cart - {self.current_date}")

        # Loops through all the items present in the cart 
        # to find an item with a name matching the function parameter name value
        # if match is found, modify the item's values from the parameter item object 
        # --- Meets the assignment Requirement about the modify_item() method --- 
        for cart_item in self.cart_items:
            # Compare names if names match, modify values
            if cart_item.item_name == item.item_name:
                # update description in cart item if the given item description 
                # is NOT None - default value
                if item.item_description != "none":
                    cart_item.item_description = item.item_description
                # update price in cart item if the given item price 
                # is NOT equal to 0 - default value
                if item.item_price != 0.0:
                    cart_item.item_price = item.item_price
                # update quantity in cart item if the given item quantity 
                # is NOT equal to 0 - default value
                # to remove item from cart use the ShoppingCart.remove_item()
                if item.item_quantity != 0:
                    # Replace old quantity with new one
                    cart_item.item_quantity = item.item_quantity
                    # Confirm message
                    print(Fore.YELLOW + f"\nThe {cart_item.item_name.title()}'s quantity is now: {cart_item.item_quantity}")
                return # exit functions
        # Error message
        print(Fore.YELLOW + "\nItem not found in cart. Nothing modified.")
    # -------------------------------------------------------------

    # ------------------------------------------------------------- remove_item()
    def remove_item(self, item_name: str) -> None:
        """Remove item by name and report when the lookup fails.

        Args:
            item_name: Name of the item that needs to be removed

        Notes:
            Error message: "Item not found in cart. Nothing removed."
        """

        # Format customer name and date into a colorized string
        print(Fore.LIGHTYELLOW_EX + f"\n{self.customer_name.title()}'s Shopping Cart - {self.current_date}")

        # Loops through all the items present in the cart 
        # to find an item with a name matching the function parameter item name value
        # if match is found, removes items from cart 
        # matching the function parameter item name value
        for i, item in enumerate(self.cart_items):
            # Check if it is the item that needs to be removed
            if item.item_name == item_name.lower():
                # Store item to be removed in a temp var. 
                # to be used by confirmation message
                temp_item = deepcopy(item)
                # Remove item from cart
                self.cart_items.pop(i)
                # Check quantity of the item to be removed
                # to format the confirmation message 
                if (temp_item.item_quantity == 1):
                    print(Fore.YELLOW + f"\n1 {temp_item.item_name.title()} was removed from cart")
                    return # exit function
                # else 
                # Confirm message plural
                print(Fore.YELLOW + f"\n{temp_item.item_quantity} {temp_item.item_name.title()}s were removed from cart")
                return # exit function
        # Error message
        print(Fore.YELLOW + "\nItem not found in cart. Nothing removed.")
    # -------------------------------------------------------------

    # ===========================================================================
    # ||                                                                       ||
    # ||         Step 6: Implement Output item's description menu option       ||
    # ||                                                                       ||
    # ===========================================================================
     

    # ______________________
    # Printers
    #

    # ------------------------------------------------------------- print_total()
    def print_total(self) -> None:
        """Print cart summary or "SHOPPING CART IS EMPTY" (Step 4).

        Notes:
            Used by menu option o - Output shopping cart 

        Format:
            John Doe's Shopping Cart - February 1, 2020
            Number of Items: 8
            Nike Romaleos 2 @ $189 = $378
            Chocolate Chips 5 @ $3 = $15
            Total: $521

        Examples:
            >>> cart = ShoppingCart("User", "February 1, 2020")
            >>> cart.add_item(
            ...     ItemToPurchase(item_name="Widget", item_price=5.0, item_quantity=2),
            ... )
            >>> cart.print_total()
            User Shopping Cart - February 1, 2020
            Number of Items: 2
            Widget 2 @ $5 = $10
            
            Total: $10
        """

        # Format customer name and date into a colorized string
        print(Fore.LIGHTYELLOW_EX + f"\n{self.customer_name.title()}'s Shopping Cart - {self.current_date}")

        #---- Assignment requirement ----
        # Check if cart is empty
        if not self.cart_items:
            print(Fore.YELLOW + "\nSHOPPING CART IS EMPTY")
            return # Exit method

        # ---- Number of items in cart
        # Get and format total with colors
        num_items = Fore.LIGHTYELLOW_EX + f"{self.get_num_items_in_cart()}" + Style.RESET_ALL
        print(f"Number of Items: {num_items}")
        # Print each item total cost, quantity, description
        for item in self.cart_items:
            item.print_item_cost(item.item_name)
        # Format cart total into colorized string
        total = Fore.LIGHTGREEN_EX+ f"${ItemToPurchase.format_currency(self.get_cost_of_cart())}" + Style.RESET_ALL
        print(f"Total: {total}")
    # -------------------------------------------------------------

    # ------------------------------------------------------------- print_descriptions()
    def print_descriptions(self) -> None:
        """Print item descriptions required in Step 4.

        Notes:
            Used by menu option a i - Output items' descriptions

        Returns:
            None. Output is directed to stdout just like router-backed renderers

        Format (with items):
            John Doe's Shopping Cart - February 1, 2020
            Item Descriptions
            Nike Romaleos: Volt color, Weightlifting shoes
            Chocolate Chips: Semi-sweet

        Format 
            John Doe's Shopping Cart - February 1, 2020
            Item Descriptions
            

        Examples:
            >>> cart = ShoppingCart("User", "February 1, 2020")
            >>> cart.add_item(
            ...     ItemToPurchase(
            ...         item_name="Widget",
            ...         item_description="Blue gadget",
            ...         item_price=5.0,
            ...         item_quantity=2,
            ...     )
            ... )
            >>> cart.print_descriptions()
            User Shopping Cart - February 1, 2020
            Item Descriptions
            Widget: Blue gadget
        """

        # Format customer name and date into colorized string
        print(Fore.LIGHTYELLOW_EX + f"\n{self.customer_name.title()}'s Shopping Cart - {self.current_date}")

        #-- Get  and display description
        print("Item Descriptions")
        # Loops through all the items present in the cart
        # and print each item name and description
        for item in self.cart_items:
             # Get item name and description and format with colors
            item_desc = Fore.LIGHTWHITE_EX + item.item_description + Style.RESET_ALL
            print(f"{item.item_name.title()}: {item_desc}")
    # -------------------------------------------------------------

    # ------------------------------------------------------------- print_items_with_quantity()
    def print_items_with_quantity(self) -> None:
        """Print all items in cart with their names and quantities.

        Format (with items):
            Apples: 3
            Bananas: 2
            Orange Juice: 1

        Examples:
            >>> cart = ShoppingCart("User", "February 1, 2020")
            >>> cart.add_item(
            ...     ItemToPurchase(item_name="apples", item_quantity=3, item_price=1.5)
            ... )
            >>> cart.add_item(
            ...     ItemToPurchase(item_name="bananas", item_quantity=2, item_price=0.5)
            ... )
            >>> cart.print_items_with_quantity()
            Apples: 3
            Bananas: 2
        """

        # Format customer name and date into a colorized string
        print(Fore.LIGHTYELLOW_EX + f"\n{self.customer_name.title()}'s Shopping Cart - {self.current_date}")


        # Loop through all items in cart and print name with quantity
        for item in self.cart_items:
            item_name = Fore.LIGHTWHITE_EX + item.item_name.title() + Style.RESET_ALL
            item_qty = Fore.LIGHTYELLOW_EX + str(item.item_quantity) + Style.RESET_ALL
            print(f"{item_name}'s quantity: {item_qty}")
    # -------------------------------------------------------------

# ------------------------------------------------------------------------- end class ShoppingCart

# __________________________________________________________________________
# Helper Functions
#
# =========================================================================
# Item Prompt Function
# =========================================================================
# ------------------------------------------------------------------------- prompt_for_item_info()
def prompt_for_item_info() -> ItemToPurchase:
    """Collects item info

    Returns:
        ItemToPurchase: populated item object

    Notes:
        Used by menu option a - Add item to cart

    Examples:
        >>> item = prompt_for_item_info()  
        >>> item.item_name  # doctest: +SKIP
        'Widget'
    """
    # Prompt user to enter the item info.
    name = validate_prompt_string("Enter the item name:\n").lower()
    
    description = validate_prompt_string("Enter the item description:\n")
    price = validate_prompt_nonezero_positive_float("Enter the item price:\n")
    quantity = validate_prompt_nonezero_positive_int("Enter the item quantity:\n")

    # Create an item with input info and returns it
    return ItemToPurchase(
        item_name=name,
        item_description=description,
        item_price=price,
        item_quantity=quantity,
    )
# ------------------------------------------------------------------------- end prompt_for_item_info()

# ===========================================================================
# ||                                                                       ||
# ||               Step 5-6: Implement print_menu function                 ||
# ||                                                                       ||
# ===========================================================================
# =========================================================================
# Menu Function
# =========================================================================
# ------------------------------------------------------------------------- print_menu()
def print_menu(cart: ShoppingCart) -> None:
    """Display Online Shopping Cart menu (Steps 5-6).

    Args:
        cart: ShoppingCart object

    Menu options:
        a - Add item to cart.
        r - Remove item from cart (shows empty message if cart is empty)
        c - Change item quantity (shows empty message if cart is empty)
        i - Output items' descriptions (shows empty message if cart is empty)
        o - Output shopping cart (shows empty message if cart is empty)
        q - Quit.

    """
    # Create menu with letter-based options using the Menu class
    menu = Menu(
        "MENU",
        [
            "Add item to cart",
            "Remove item from cart",
            "Change item quantity",
            "Output items' descriptions",
            "Output shopping cart",
            "Quit",
        ],
        prefixes=["a", "r", "c", "i", "o", "q"],
    )
    # Render the menu and store it in a string variable to be displayed
    menu_display = Fore.LIGHTCYAN_EX + menu.render()

    # Create a Add Itme banner instance
    add_item_banner = Banner(["Add Itme"])
    # Render the description banner and store it in a string variable to be displayed
    add_item_banner_display = Fore.LIGHTCYAN_EX + add_item_banner.render() 
    
    desc_banner = Banner(["OUTPUT ITEMS' DESCRIPTIONS"])
    # Render the description banner and store it in a string variable to be displayed
    desc_banner_display = Fore.LIGHTCYAN_EX + desc_banner.render()
    
    # Create a cart output banner instance
    cart_output_banner = Banner(["OUTPUT SHOPPING CART"])
    # Render the cart output banner and store it in a string variable to be displayed
    cart_output_banner_display = Fore.LIGHTCYAN_EX + cart_output_banner.render()

    # Create a Remove item banner instance
    remove_banner = Banner(["REMOVE ITEM"])
    # Render the Remove banner and store it in a string variable to be displayed
    remove_banner_display = Fore.LIGHTCYAN_EX + remove_banner.render()

    # Create a Modify Quantity item banner instance
    mod_quantity_banner = Banner(["MODIFY QUANTITY"])
    # Render the Remove banner and store it in a string variable to be displayed
    mod_quantity_banner_display = Fore.LIGHTCYAN_EX + mod_quantity_banner.render()

     # Menu loop
    while True:
        print()
        print(menu_display)

        # Prompt the user for selection and captures it
        selection = input("\nChoose an option: ").strip().lower()

        match selection:
            case 'a': # Launch the add item feature
                print()
                print(add_item_banner_display)
                print()
                # Creat a n item instance and prompt user for item info
                new_item = prompt_for_item_info()
                # Add the new populated item to cart
                cart.add_item(new_item)
                # Confimation message
                print(Fore.LIGHTGREEN_EX + f"\n{new_item.item_quantity} \"{new_item.item_name.title()}\" added to cart.")
                wait_for_enter()

            case 'r': # Launch the remove item feature
                print()
                print(remove_banner_display)
                
                # Check if cart is empty
                if not cart.cart_items:
                    # Format customer name and date into a colorized string
                    print(Fore.LIGHTYELLOW_EX + f"\n{cart.customer_name.title()}'s Shopping Cart - {cart.current_date}")
                    print(Fore.YELLOW + "\nSHOPPING CART IS EMPTY")
                else:
                    # Display items in cart descriptions
                    cart.print_descriptions()
                    print()
                    # Prompt user for the name of the item to remove
                    name = validate_prompt_string("Enter the item name to remove:\n").lower()
                    # Remove item from cart
                    cart.remove_item(name)
                
                wait_for_enter()

            case 'c': # Launch the item change quantity feature
                print()
                print(mod_quantity_banner_display)

                # Check if cart is empty
                if not cart.cart_items:
                    # Format customer name and date into a colorized string
                    print(Fore.LIGHTYELLOW_EX + f"\n{cart.customer_name.title()}'s Shopping Cart - {cart.current_date}")
                    print(Fore.YELLOW + "\nSHOPPING CART IS EMPTY")
                else:
                    # Display the items in cart name and quantity
                    cart.print_items_with_quantity()
                    # Prompt user for the name of the item to change quantity
                    name = validate_prompt_string("\nEnter the item name:\n").lower()
                    new_qty = validate_prompt_nonezero_positive_int("Enter the new quantity: ")
                    # --- Meets the assignment Requirement about the modify_item() method --- 
                    # Create item with only name and quantity set --(others default)--
                    temp_item = ItemToPurchase(item_name=name, item_quantity=new_qty)
                    # Modify item
                    cart.modify_item(temp_item)

                wait_for_enter()

            case 'i': # Launch the item output description feature
                print()
                print(desc_banner_display)

                # Check if cart is empty
                if not cart.cart_items:
                    # Format customer name and date into a colorized string
                    print(Fore.LIGHTYELLOW_EX + f"\n{cart.customer_name.title()}'s Shopping Cart - {cart.current_date}")
                    print(Fore.YELLOW + "\nSHOPPING CART IS EMPTY")
                else:
                    # Output the items' descriptions present in cart
                    cart.print_descriptions()
                
                wait_for_enter()

            case 'o': # Launch the item Output cart feature
                print()
                print(cart_output_banner_display)

                # # Check if cart is empty
                # if not cart.cart_items:
                    #  # Format customer name and date into a colorized string
                    # print(Fore.LIGHTYELLOW_EX + f"\n{cart.customer_name.title()}'s Shopping Cart - {self.current_date}")
                #     print(Fore.YELLOW + "\nSHOPPING CART IS EMPTY")
                # else:

                # Built-in check for empty cart
                # Display the formated cart info and total
                cart.print_total() 
                
                wait_for_enter()

            case 'q': # Launch the item quit feature
                if (validate_prompt_yes_or_no("Are you sure that you want to exist? ")):
                    print("\nThank you for shopping!")
                    # Exits while loop 
                    break

            case _:
                # Invalid input
                print(Fore.LIGHTRED_EX + "\nInvalid selection, please enter a, r, c, i, o, or q.")
                wait_for_enter()
# ------------------------------------------------------------------------- end print_menu()

# __________________________________________________________________________
# -------------- Main Function --------------
#
# =========================================================================
# Main Application Flow Functionality (program entry and user interaction)
# =========================================================================
# ------------------------------------------------------------------------- main()
def main() -> None:
    """Run the shopping cart program (Steps 4-6).

    Program:
        1. Display header.
        2. Prompt for customer name and date
        3. Create ShoppingCart (empty)
        4. Enter menu loop (Steps 5-6)
        5. Display exit message

    Examples:
        >>> main()  

    """
   
    # Display program header
    header = Banner(["Online Shopping Cart"])
    print(Fore.LIGHTCYAN_EX + header.render())
    print()

    #______________
    # Part 4
    #
    # Prompt for customer info
    customer_name = validate_prompt_string("Enter customer's name:\n")
    current_date = validate_prompt_date("Enter today's date:\n")

    # Create shopping cart (empty - no items added initially)
    cart = ShoppingCart(customer_name, current_date)

    #______________
    # Part 5-6
    #
    # The print-menu() function implements
    # the main functionality of the Online Shopping Cart
    print_menu(cart)

    # Exit program message
    print("\nBye! 👋\n")
    
# ------------------------------------------------------------------------- end main()

# __________________________________________________________________________
# Module Initialization / Main Execution Guard
#
# ------------------------------------------------------------------------- main_guard
if __name__ == "__main__":
    main()
# ------------------------------------------------------------------------- end main_guard

# __________________________________________________________________________
# End of File
#
