# -------------------------------------------------------------------------
# File: main.py
# Author: Alexander Ricciardi
# Date: 2026-03-16
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Entry point for the CTA-1 Data Structures Demonstration app
# -------------------------------------------------------------------------

# --- Assignment Description ---
# CTA-1 (Critical Thinking 1) requires implementing three
# data structures — Stack, Queue, and Linked List — with a
# interface demonstrating how each works, including visual displays
# and educational explanations.
# -------------------------------------------------------------------------

# --- Usage ---
# Run from the project root:
#   python CTA-1/main.py
# -------------------------------------------------------------------------

# --- Imports ---
# - __future__.annotations for postponed evaluation of type hints.
# - sys for adding the parent directory to the module search path.
# - pathlib.Path for cross-platform path manipulation.
# - colorama.init for cross-platform colored terminal initialization.
# - ui.app.run_application for the main application loop.
# -------------------------------------------------------------------------

"""
Entry point for the CTA-1 Data Structures Demonstration.

"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

import sys
from pathlib import Path

from colorama import init

# Add the project root (parent of CTA-1/) to the module search path
# so that both `utilities` and `data_structures` packages can be imported.
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Add the CTA-1 directory itself so local packages resolve correctly.
_cta1_dir = str(Path(__file__).resolve().parent)
if _cta1_dir not in sys.path:
    sys.path.insert(0, _cta1_dir)

from ui.app import run_application  # noqa: E402

# ==============================================================================
# MAIN FUNCTION – Entry Point
# ==============================================================================

# -------------------------------------------------------------- main()
def main() -> None:
    """Entry point for CTA-1 data structures demonstration.

    Logic:
        1. Initialize colorama with autoreset for clean color handling.
        2. Launch the interactive application.
    """
    # Step 1: Initialize colorama
    init(autoreset=True)
    # Step 2: Run the application
    run_application()
# -------------------------------------------------------------- end main()

# ==============================================================================
# MODULE INITIALIZATION
# ==============================================================================

if __name__ == "__main__":
    main()

# ==============================================================================
# End of File
# ==============================================================================
