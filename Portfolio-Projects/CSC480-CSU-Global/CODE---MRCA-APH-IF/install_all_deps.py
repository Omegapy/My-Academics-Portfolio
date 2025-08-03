#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: install_all_deps.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-19 (Creation Date)
# Last Modified: 2025-01-19
# File Path: install_all_deps.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Automated dependency installer for the MRCA Advanced Parallel Hybrid system.
# Installs all required dependencies from multiple requirements files across
# the project structure, including backend, frontend, and testing dependencies.
# Provides a single command to set up the complete development environment.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: install_requirements - Install dependencies from a specific requirements file
# - Function: main - Orchestrate installation of all MRCA dependencies
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: subprocess (for running pip commands), sys (for Python executable)
# - Standard Library: pathlib.Path (for file system operations and path handling)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This script should be run once during initial setup or when dependencies change.
# It automatically finds and installs from all requirements.txt files in the project.
# Run with: python3 install_all_deps.py
# Integrates with the development container setup and deployment processes.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF) System
# -------------------------------------------------------------------------

"""
MRCA Dependency Installer

Automated installation script for all MRCA Advanced Parallel Hybrid dependencies.
Installs packages from multiple requirements files across the project structure.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import subprocess
import sys
from pathlib import Path

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ---------------------------------------------------------------------------------
def install_requirements(req_file, description):
    """Install dependencies from a requirements file.
    
    Attempts to install Python packages from a specified requirements file
    using pip. Provides feedback on installation success or failure.
    
    Args:
        req_file (str): Path to the requirements.txt file
        description (str): Human-readable description of the dependency set
        
    Returns:
        bool: True if installation successful, False if failed or file not found
    """
    if Path(req_file).exists():
        print(f"Installing {description}...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", req_file
            ], check=True)
            print(f"{description} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to install {description}")
            return False
    else:
        print(f"{req_file} not found, skipping {description}")
        return True
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def main():
    """Orchestrate installation of all MRCA dependencies.
    
    Main function that coordinates the installation of dependencies from all
    requirements files in the MRCA project. Updates pip first, then installs
    from root, backend, frontend, and testing requirements files.
    
    Returns:
        int: 0 if all installations successful, 1 if any installation failed
    """
    print("Installing all MRCA dependencies...")
    
    # Update pip first
    print("Updating pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    success = True
    
    # Install from all requirements files
    requirements_files = [
        ("requirements.txt", "Root dependencies (dev container)"),
        ("backend/requirements.txt", "Backend dependencies"),
        ("frontend/requirements.txt", "Frontend dependencies"),
        ("requirements-test.txt", "Testing dependencies (optional)")
    ]
    
    for req_file, description in requirements_files:
        if not install_requirements(req_file, description):
            success = False
    
    if success:
        print("\nAll dependencies installed successfully!")
        print("You can now run: python3 launch_app.py")
    else:
        print("\nSome dependencies failed to install")
        return 1
    
    return 0
# ---------------------------------------------------------------------------------

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================

# ---------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Execute the dependency installation when script is run directly.
    
    This block runs only when the file is executed directly, not when imported.
    Executes the main installation process and exits with appropriate status code.
    """
    exit(main())
# ---------------------------------------------------------------------------------

# =========================================================================
# End of File
# =========================================================================