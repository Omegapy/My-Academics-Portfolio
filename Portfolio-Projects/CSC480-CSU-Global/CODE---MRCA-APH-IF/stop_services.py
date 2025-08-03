#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: stop_services.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-19 (Creation Date)
# Last Modified: 2025-01-19
# File Path: stop_services.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Simple script to stop all running MRCA services (backend and frontend).
# Provides a clean way to terminate detached processes started by start_services.py.
# Includes health verification to confirm services have been properly stopped.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: stop_services - Stop all MRCA services and verify termination
# - Function: main - Main execution function
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: subprocess (for process termination), time (for delays)
# - Third-Party: requests (for health check verification)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This script provides a clean way to stop all MRCA services that were started
# as detached background processes. Run with: python3 stop_services.py
# Complements start_services.py for complete service lifecycle management.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF) System
# -------------------------------------------------------------------------

"""
MRCA Service Stopper

Stops all running MRCA Advanced Parallel Hybrid services.
Provides clean termination with verification of service shutdown.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import subprocess
import time

# Third-party library imports
import requests

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ---------------------------------------------------------------------------------
def stop_services():
    """Stop all MRCA services.
    
    Terminates all running streamlit and uvicorn processes, then verifies
    that the services have stopped by attempting to connect to their health
    endpoints. Provides feedback on the termination status.
    """
    print("🛑 Stopping MRCA services...")
    
    try:
        # Kill all streamlit and uvicorn processes
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True, check=False)
        subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True, check=False)
        
        print("Waiting for processes to terminate...")
        time.sleep(3)
        
        # Verify services are stopped
        try:
            backend_response = requests.get("http://localhost:8000/health", timeout=2)
            print("⚠️  Backend may still be running")
        except requests.RequestException:
            print("✅ Backend stopped")
            
        try:
            frontend_response = requests.get("http://localhost:8501/_stcore/health", timeout=2)
            print("⚠️  Frontend may still be running")
        except requests.RequestException:
            print("✅ Frontend stopped")
            
        print("\n✅ MRCA services have been stopped")
        
    except Exception as e:
        print(f"❌ Error stopping services: {e}")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def main():
    """Main function.
    
    Entry point for the service stopper script. Provides a title banner
    and executes the service stopping process.
    """
    print("MRCA Service Stopper")
    print("="*30)
    stop_services()
# ---------------------------------------------------------------------------------

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================

# ---------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Execute the service stopper when script is run directly.
    
    This block runs only when the file is executed directly, not when imported.
    Executes the main function to stop all MRCA services.
    """
    main()
# ---------------------------------------------------------------------------------

# =========================================================================
# End of File
# ========================================================================= 