# -------------------------------------------------------------------------
# File: developer_builder.py
# Project: CTA-Module-4
# Author: Alexander Ricciardi
# Date: 2025-12-06
# p:\CSU-projects\CSC-505-Programs\CTA-Module-4\developer_builder.py
# ------------------------------------------------------------------------
# Course: CSC-505 Principles of Software Development
# Professor: Dr. Brian Holbert
# Winter W-2025
# Nov.-Jan. 2025
# ------------------------------------------------------------------------
# Assignment:
# Critical Thinking Assignment Module 4
#
# Directions:
#
# Write a Python Script:
# - Develop a Python program (developer_builder.py) that:
#   - Defines a Developer class with attributes for each selected trait
#   - Uses a builder or fluent interface to construct the developer object
#   - Prints a formatted output including:
#     - The trait names
#     - A brief description of each trait
#     - The number of traits represented
#
# Example output:
#   Building your ideal developer...
#   Trait: Curiosity – Drives exploration of new tools and techniques
#   Trait: Empathy – Enhances team communication and user understanding
#   Trait: Adaptability – Enables flexibility in changing environments
#   Total traits included: 3
# ------------------------------------------------------------------------
# Project:
# CTA-Module-4
#
# Project description:
# The program is a small python script tjat runs in the console program.
# It creates Developer objects listing desire developer personality traits (Resilience,
# Awareness, Pragmatism).
# ------------------------------------------------------------------------

# --- File Contents Overview ---
# - Class: Developer
# - Class: Builder (Interface)
# - Class: DeveloperBuilder (Concrete Builder)
# - Class: DeveloperManager (Director)
# - Function: main
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: os, sys, dataclasses, typing, abc
# - Third-Party: colorama (for terminal colors)
# - Local Project Modules:
#   - utilities.menu_banner_utilities.Banner
# --- Requirements ---
# - Python 3.x
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0
# -------------------------------------------------------------------------

"""
The program is a small python script tjat runs in the console program.
It creates Developer objects listing desire developer personality traits (Resilience,
Awareness, Pragmatism).
"""

# __________________________________________________________________________
# Imports

from __future__ import annotations

import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar

# UI - Local utility modules (for Banner) and color 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from colorama import Fore, Style, init
from utilities.menu_banner_utilities import Banner

# ____________________________________________________________________________
# Class Definitions

# =========================================================================
# Developer Data Class
# =========================================================================
# ------------------------------------------------------------------------- class Developer
@dataclass(slots=True, kw_only=True)
class Developer:
    """ Software developer with specific personality traits (Product pattern element)

    This class uses @dataclass to auto-generate:
        - __init__ from annotated fields,
        - __repr__ (developer-friendly),
        - __eq__ (equality).

    Attributes:
        resilience: Description of the resilience trait
        awareness: Description of the awareness trait
        pragmatism: Description of the pragmatism trait
    """

    # ______________________
    #  Constant Class Variable 
    # (excluded from dataclass constructor/compare via ClassVar)
    #
    _INSTANCE_COUNT: ClassVar[int] = 0

    # ______________________
    #  Instance Fields
    #
    resilience: str | None = None
    awareness: str | None = None
    pragmatism: str | None = None

    # ______________________
    # Post-Initialization 
    #
    # --------------------------------------------------------------------------------- __post_init__()
    def __post_init__(self) -> None:
        """Validate inputs and compute derived fields."""
        type(self)._INSTANCE_COUNT += 1
    # --------------------------------------------------------------------------------- 

    # ______________________
    # Class Information Methods
    #
    # --------------------------------------------------------------------------------- __str__()
    def __str__(self) -> str:
        """Return Developer traits as a formatted string.

        Returns:
            Formatted developer's traits string with colors.
        """
        return (
            f"{Style.BRIGHT}{Fore.GREEN}Developer Traits:{Style.RESET_ALL}\n"
            f"{Fore.CYAN}Trait: Resilience Under Pressure{Style.RESET_ALL} – {self.resilience}\n"
            f"{Fore.CYAN}Trait: Acute Awareness{Style.RESET_ALL} – {self.awareness}\n"
            f"{Fore.CYAN}Trait: Pragmatism{Style.RESET_ALL} – {self.pragmatism}"
        )
    # --------------------------------------------------------------------------------- 

# ------------------------------------------------------------------------- end class Developer

# =========================================================================
# Builder Interface
# =========================================================================
# ------------------------------------------------------------------------- class Builder
class Builder(ABC):
    """Abstract interface for Developer builders.

    Defines the steps required to build a Developer object.
    """

    # ______________________
    # Abstract Methods
    #
    # --------------------------------------------------------------------------------- build_resilience()
    @abstractmethod
    def build_resilience(self, description: str) -> None:
        """Setter for the resilience trait description.

        Args:
            description: The description of the resilience trait.
        """
        pass
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- build_awareness()
    @abstractmethod
    def build_awareness(self, description: str) -> None:
        """Setter for the acute awareness trait description.

        Args:
            description: The description of the acute awareness trait.
        """
        pass
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- build_pragmatism()
    @abstractmethod
    def build_pragmatism(self, description: str) -> None:
        """Setter for the pragmatism trait description.

        Args:
            description: The description of the pragmatism trait.
        """
        pass
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- reset()
    @abstractmethod
    def reset(self) -> None:
        """Reset the builder state to start a new build."""
        pass
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- get_result()
    @abstractmethod
    def get_result(self) -> Developer:
        """Return the the Developer object.

        Returns:
            The Developer object.
        """
        pass
    # --------------------------------------------------------------------------------- 

# ------------------------------------------------------------------------- end class Builder

# =========================================================================
# DeveloperBuilder Class (Concrete Builder)
# =========================================================================
# ------------------------------------------------------------------------- class DeveloperBuilder
class DeveloperBuilder(Builder):
    """ Construct a Developer object (Concrete Builder pattern element)

    Instance Attributes:
        _developer (Developer): The Developer instance.
        count (int): The number of traits added.
    """

    # ______________________
    # Constructor
    #
    # --------------------------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initialize the builder with a Developer instance."""
        self._developer: Developer = Developer()
        self.count: int = 0
    # --------------------------------------------------------------------------------- 

    # ______________________
    # Builder Methods
    #
    # --------------------------------------------------------------------------------- reset()
    def reset(self) -> None:
        """Reset the builder to start a new build."""
        self._developer = Developer()
        self.count = 0
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- build_resilience()
    def build_resilience(self, description: str) -> None:
        """Setter for the resilience trait description.

        Args:
            description: The description of the resilience trait.
        """
        self._developer.resilience = description
        self.count += 1
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- build_awareness()
    def build_awareness(self, description: str) -> None:
        """Setter for the acute awareness trait description.

        Args:
            description: The description of the acute awareness trait.
        """
        self._developer.awareness = description
        self.count += 1
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- build_pragmatism()
    def build_pragmatism(self, description: str) -> None:
        """Setter for the pragmatism trait description.

        Args:
            description: The description of the pragmatism trait.
        """
        self._developer.pragmatism = description
        self.count += 1
    # --------------------------------------------------------------------------------- 

    # --------------------------------------------------------------------------------- get_result()
    def get_result(self) -> Developer:
        """Return the constructed Developer object.

        Returns:
            The constructed Developer object.
        """
        # Note: In a real implementation, one might reset here or require manual reset.
        # We return the object and let the client decide.
        return self._developer
    # --------------------------------------------------------------------------------- 

# ------------------------------------------------------------------------- end class DeveloperBuilder

# =========================================================================
# DeveloperManager Class (Director)
# =========================================================================
# ------------------------------------------------------------------------- class DeveloperManager
class DeveloperManager:
    """Controls (manages) the construction steps (Director pattern element)

    Instance Attributes:
        _builder (Builder): The builder instance to use for construction.
    """

    # ______________________
    # Constructor
    #
    # --------------------------------------------------------------------------------- __init__()
    def __init__(self, builder: Builder) -> None:
        """Initialize the Manager with a builder.

        Args:
            builder: The Builder instance to control.
        """
        self._builder: Builder = builder
    # --------------------------------------------------------------------------------- 

    # ______________________
    # Construction Methods
    #
    # --------------------------------------------------------------------------------- construct()
    def construct(self) -> None:
        """Execute the construction sequence to build an 'Ideal Developer'.

        Calls the builder methods in the predefined order with specific content.
        """
        self._builder.build_resilience("Maintains performance and morale despite chaos")
        self._builder.build_awareness("Understands needs of peers and stakeholders")
        self._builder.build_pragmatism("Adapts rules to fit specific project circumstances")
    # ---------------------------------------------------------------------------------             

# ------------------------------------------------------------------------- end class DeveloperManager

# __________________________________________________________________________
# Standalone Function Definitions
#

# ______________________
# Main Execution
#
# --------------------------------------------------------------------------------- main()
def main() -> None:
    """Execute the developer builder demonstration (Client pattern element)

    Initializes the environment, prints a banner, and builds a Developer
    using the Director (Manager) and Builder.
    """
    # Initialize colorama
    init(autoreset=True)

    # Create and print banner
    banner = Banner([("Building your ideal developer...", "center")])
    print(Fore.YELLOW + banner.render() + Style.RESET_ALL)
    print()  # detailed spacing

    # Create the concrete builder
    builder: DeveloperBuilder = DeveloperBuilder()

    # 2. Create the director and pass the builder to it
    manager: DeveloperManager = DeveloperManager(builder)

    # Director constructs the product
    manager.construct()

    # Store the result from the builder
    developer: Developer = builder.get_result()
    trait_count: int = builder.count

    # Print the result
    print(developer)
    print(f"\n{Fore.MAGENTA}Total traits included: {trait_count}{Style.RESET_ALL}")
# --------------------------------------------------------------------------------- end main()

# __________________________________________________________________________
# Module Initialization / Main Execution Guard #
# --------------------------------------------------------------------------------- main_guard
if __name__ == "__main__":
    main()
# --------------------------------------------------------------------------------- 

# __________________________________________________________________________
# End of File
