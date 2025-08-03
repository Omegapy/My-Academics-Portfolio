#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: start_services.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-25 (Creation Date)
# Last Modified: 2025-01-25 
# File Path: start_services.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Simple standalone launcher for MRCA services that starts both backend and 
# frontend as completely detached background processes. Services will continue
# running even after this script exits, preventing connection issues.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: cleanup_existing_processes - Clean up any existing MRCA processes
# - Function: start_backend - Start the FastAPI backend as a detached process
# - Function: start_frontend - Start the Streamlit frontend as a detached process
# - Function: wait_for_services - Wait for both services to become healthy
# - Function: print_access_info - Print service access information
# - Function: main - Main launcher function
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: os, sys (for system operations and process management)
# - Standard Library: time, subprocess (for timing and process control)
# - Third-Party: requests (for health checking HTTP endpoints)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This script starts the MRCA backend and frontend services as detached processes.
# Services continue running even after the script terminates, making it ideal
# for development container environments. Run with: python3 start_services.py
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF) System
# -------------------------------------------------------------------------

"""
MRCA Simple Service Launcher

Starts the MRCA Advanced Parallel Hybrid backend and frontend services as
completely detached background processes that survive script termination.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import os
import sys
import time
import subprocess

# Third-party library imports
import requests

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Configuration
BACKEND_PORT = 8000
FRONTEND_PORT = 8501
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ---------------------------------------------------------------------------------
def cleanup_existing_processes():
    """Clean up any existing MRCA processes.
    
    Terminates any running streamlit or uvicorn processes to ensure clean startup.
    Uses pkill to find and terminate processes by name pattern matching.
    """
    print("🧹 Cleaning up existing processes...")
    try:
        # Kill existing processes
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
        subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True)
        time.sleep(2)
        print("✅ Cleanup complete")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def start_backend():
    """Start the FastAPI backend as a detached process.
    
    Launches the MRCA backend server using uvicorn with proper configuration
    for development container environments. The process runs completely detached
    and survives script termination.
    """
    print("🚀 Starting backend server...")
    
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", str(BACKEND_PORT),
        "--reload"
    ]
    
    # Start as completely detached background process
    subprocess.Popen(
        backend_cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        preexec_fn=os.setsid if hasattr(os, 'setsid') else None,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    
    print(f"✅ Backend starting on http://localhost:{BACKEND_PORT}")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def start_frontend():
    """Start the Streamlit frontend as a detached process.
    
    Launches the MRCA frontend using Streamlit with proper configuration
    for development container environments. The process runs completely detached
    and survives script termination.
    """
    print("🎨 Starting frontend server...")
    
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run",
        "frontend/bot.py",
        "--server.address=0.0.0.0",
        f"--server.port={FRONTEND_PORT}",
        "--server.headless=true",
        "--browser.serverAddress=localhost",
        f"--browser.serverPort={FRONTEND_PORT}",
        "--server.enableXsrfProtection=false",
        "--server.enableCORS=false"
    ]
    
    # Start as completely detached background process
    subprocess.Popen(
        frontend_cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        preexec_fn=os.setsid if hasattr(os, 'setsid') else None,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    
    print(f"✅ Frontend starting on http://localhost:{FRONTEND_PORT}")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def wait_for_services():
    """Wait for both services to become healthy.
    
    Polls the health endpoints of both backend and frontend services until
    they respond successfully or maximum attempts are reached.
    
    Returns:
        bool: True if both services are healthy, False if timeout reached
    """
    print("⏳ Waiting for services to start...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            # Check backend
            backend_response = requests.get(f"http://localhost:{BACKEND_PORT}/health", timeout=2)
            frontend_response = requests.get(f"http://localhost:{FRONTEND_PORT}/_stcore/health", timeout=2)
            
            if backend_response.status_code == 200 and frontend_response.status_code == 200:
                print("✅ Both services are healthy!")
                return True
                
        except requests.RequestException:
            pass
        
        time.sleep(2)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    print("⚠️  Services may still be starting...")
    return False
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def print_access_info():
    """Print service access information.
    
    Displays comprehensive information about how to access the running MRCA
    services, including URLs, development container specific instructions,
    and system capabilities.
    """
    print("\n" + "="*80)
    print("🎉 MRCA Advanced Parallel Hybrid Services Started!")
    print("="*80)
    print("Service URLs:")
    print(f"    Frontend: http://localhost:{FRONTEND_PORT}")
    print(f"    Backend:  http://localhost:{BACKEND_PORT}")
    print(f"    API Docs: http://localhost:{BACKEND_PORT}/docs")
    print("")
    print("VS Code Dev Container Access:")
    print("   1. Open the 'PORTS' tab in VS Code (bottom panel)")
    print(f"   2. Find ports {FRONTEND_PORT} and {BACKEND_PORT}")
    print(f"   3. Right-click port {FRONTEND_PORT} → 'Open in Browser'")
    print(f"   4. If ports not visible, click 'Add Port' and add {FRONTEND_PORT}")
    print("")
    print("Advanced Parallel Hybrid Technology Ready!")
    print("   - Dual AI processing modes")
    print("   - 4 fusion strategies available")
    print("   - Neo4j knowledge graph integration")
    print("")
    print("🔗 Services are running as detached background processes")
    print("   They will continue running even after closing this terminal")
    print("")
    print("To stop services later, run:")
    print("   pkill -f streamlit && pkill -f uvicorn")
    print("="*80)
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def main():
    """Main launcher function.
    
    Orchestrates the complete service startup process including cleanup,
    backend startup, frontend startup, health checking, and access information
    display. Handles errors gracefully with appropriate exit codes.
    """
    print("MRCA Simple Service Launcher")
    print("="*50)
    
    try:
        cleanup_existing_processes()
        start_backend()
        time.sleep(3)  # Give backend time to start
        start_frontend()
        
        # Wait for services
        wait_for_services()
        print_access_info()
        
        print("\n✅ Launch complete! Services are running in the background.")
        print("   This script can now be safely closed.")
        
    except Exception as e:
        print(f"❌ Error starting services: {e}")
        sys.exit(1)
# ---------------------------------------------------------------------------------

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================

# ---------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Execute the service launcher when script is run directly.
    
    This block runs only when the file is executed directly, not when imported.
    Executes the main launcher function to start all MRCA services.
    """
    main()
# ---------------------------------------------------------------------------------

# =========================================================================
# End of File
# ========================================================================= 