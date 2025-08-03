#!/usr/bin/env python3

# -------------------------------------------------------------------------
# File: launch_app.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: launch_app.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module serves as the application launcher for the MRCA Advanced Parallel Hybrid system.
# It provides automated deployment functionality that handles dependency management,
# process cleanup, and coordinated startup of both frontend and backend services.
# The launcher is specifically designed to work in development container environments
# and handles relative import issues by running the backend as a module.
# It also provides comprehensive health checking and monitoring for service readiness.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: check_dependencies() - Verifies required Python packages are installed
# - Function: install_dependencies() - Installs missing dependencies from requirements
# - Function: launch_backend() - Starts FastAPI backend server with proper module handling
# - Function: launch_frontend() - Starts Streamlit frontend server with dev container configuration
# - Function: wait_for_services() - Monitors service health and readiness
# - Function: cleanup_existing_processes() - Terminates existing MRCA processes
# - Function: main() - Main orchestration function for application launch
# - Module Execution Guard: Handles direct script execution
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: 
#   - subprocess: For launching and managing external processes (uvicorn, streamlit)
#   - sys: For system-specific parameters and exit codes
#   - time: For sleep operations and timing control
#   - os: For environment variable management
#   - pathlib.Path: For cross-platform path operations
# - Third-Party: 
#   - requests: For HTTP health check requests (imported dynamically)
#   - fastapi, streamlit, uvicorn: Checked for availability (imported dynamically)
# - Local Project Modules: None (this is the entry point launcher)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is the primary entry point for launching the complete MRCA system.
# It should be executed directly from the project root directory using:
# - python3 launch_app.py (recommended for dev containers)
# - ./launch.sh (shell script wrapper)
# The launcher coordinates startup of both frontend and backend services,
# handles dependency installation, and provides dev container specific configuration
# for proper port forwarding and accessibility.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
MRCA Application Launcher - Fixed Version
Handles the relative import issue by running backend as a module
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import subprocess
import sys
import time
import os
from pathlib import Path

# Third-party library imports
# (Imported dynamically as needed for dependency checking)

# Local application/library specific imports
# (None - this is the entry point launcher)

# =========================================================================
# Global Constants / Variables
# =========================================================================
# No global constants defined in this module

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# --------------------------
# --- Utility Functions ---
# --------------------------

# ------------------------------------------------------------------------- check_dependencies()
def check_dependencies() -> bool:
    """Check if required dependencies are installed.

    This function verifies that core dependencies (fastapi, streamlit, uvicorn)
    are available in the current Python environment. It performs dynamic imports
    to test availability without causing import errors.

    Returns:
        bool: True if all core dependencies are available, False otherwise.

    Examples:
        >>> check_dependencies()
        ✅ Core dependencies available
        True
    """
    try:
        import fastapi
        import streamlit
        import uvicorn
        print("✅ Core dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
# ------------------------------------------------------------------------- end check_dependencies()

# ------------------------------------------------------------------------- install_dependencies()
def install_dependencies() -> bool:
    """Install backend dependencies from requirements.txt files.

    This function installs missing dependencies by reading from backend/requirements.txt
    and also ensures streamlit is installed for the frontend. It uses pip subprocess
    calls to perform the installations.

    Returns:
        bool: True if all dependencies were installed successfully, False otherwise.

    Examples:
        >>> install_dependencies()
        Installing dependencies...
        ✅ Backend dependencies installed
        ✅ Streamlit installed
        True
    """
    print("📦 Installing dependencies...")
    backend_requirements = Path("backend/requirements.txt")
    
    if backend_requirements.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(backend_requirements)
            ], check=True)
            print("✅ Backend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install backend dependencies")
            return False
    
    # Install streamlit for frontend
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"], check=True)
        print("✅ Streamlit installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install streamlit")
        return False
    
    return True
# ------------------------------------------------------------------------- end install_dependencies()

# ------------------------------------------------------------------------- wait_for_services()
def wait_for_services() -> None:
    """Wait for services to be ready and perform health checks.

    This function implements a waiting period for services to start up and then
    performs health checks on both backend API and frontend Streamlit service
    to ensure they're responding correctly.

    Examples:
        >>> wait_for_services()
        Waiting for services to start...
        ✅ Backend is healthy
        ✅ Frontend is healthy
        ✅ Services should be ready!
    """
    print("Waiting for services to start...")
    time.sleep(8)  # Give more time for services to start
    
    try:
        import requests
        
        # Check backend health
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                print("Backend is healthy")
            else:
                print("⚠️ Backend may not be fully ready")
        except Exception as e:
            print(f"⚠️ Could not check backend health: {e}")
        
        # Check frontend health (Streamlit health endpoint)
        try:
            # Give Streamlit extra time to start
            time.sleep(3)
            response = requests.get("http://localhost:8501/_stcore/health", timeout=10)
            if response.status_code == 200:
                print("✅ Frontend is healthy")
            else:
                print("⚠️ Frontend may not be fully ready")
        except Exception as e:
            print(f"⚠️ Could not check frontend health: {e}")
            
    except ImportError:
        print("⚠️ Requests module not available for health checks")
    
    print("✅ Services should be ready!")
# ------------------------------------------------------------------------- end wait_for_services()

# ------------------------
# --- Helper Functions ---
# ------------------------

# ------------------------------------------------------------------------- launch_backend()
def launch_backend():
    """Launch FastAPI backend using module approach to handle relative imports.

    This function starts the FastAPI backend server using uvicorn with proper
    module execution to resolve relative import issues. It configures the
    PYTHONPATH environment variable and uses subprocess to start the server
    in a separate process.

    Returns:
        subprocess.Popen: Backend process object if successful, None if failed.

    Examples:
        >>> backend_proc = launch_backend()
        Starting backend server...
        ✅ Backend server starting on http://localhost:8000
    """
    print("Starting backend server...")
    
    try:
        # Set PYTHONPATH to include the project root
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())
        
        # Run backend as a module to handle relative imports
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "backend.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--timeout-keep-alive", "3600",
            "--timeout-graceful-shutdown", "30",
            "--access-log"
        ], env=env)
        
        print("✅ Backend server starting on http://localhost:8000")
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None
# ------------------------------------------------------------------------- end launch_backend()

# ------------------------------------------------------------------------- launch_frontend()
def launch_frontend():
    """Launch Streamlit frontend with automatic browser opening.

    This function starts the Streamlit frontend server and automatically opens
    the application in the default browser. It configures the server to bind
    to 0.0.0.0 for proper port forwarding while enabling browser auto-opening.

    Returns:
        subprocess.Popen: Frontend process object if successful, None if failed.

    Examples:
        >>> frontend_proc = launch_frontend()
        Starting frontend server...
        Frontend server starting on http://localhost:8501
        Opening browser automatically...
    """
    print("Starting frontend server...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return None
    
    try:
        # Set environment variables to enable browser opening
        env = os.environ.copy()
        # Remove any browser-disabling environment variables if they exist
        env.pop('STREAMLIT_BROWSER_DISABLE', None)
        env.pop('STREAMLIT_SERVER_HEADLESS', None)
        
        # Use streamlit with browser opening enabled
        frontend_process = subprocess.Popen([
            "streamlit", "run", "bot.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",  # CRITICAL: Must bind to 0.0.0.0 for dev containers
            "--server.headless", "true",  # Run in headless mode for dev containers
            "--browser.gatherUsageStats", "false",
            "--client.toolbarMode", "viewer",
            "--server.enableCORS", "false",  # Disable CORS for dev container access
            "--server.enableXsrfProtection", "false"  # Disable XSRF for dev container access
        ], cwd=frontend_dir, env=env)
        
        print("✅ Frontend server starting on http://localhost:8501")
        print("Browser should open automatically...")
        return frontend_process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None
# ------------------------------------------------------------------------- end launch_frontend()

# ------------------------------------------------------------------------- cleanup_existing_processes()
def cleanup_existing_processes() -> None:
    """Kill any existing MRCA backend or frontend processes.

    This function performs cleanup of existing uvicorn (backend) and streamlit (frontend)
    processes that might be running from previous launches. It uses pkill to terminate
    processes and provides appropriate feedback about the cleanup results.

    Examples:
        >>> cleanup_existing_processes()
        Cleaning up existing processes...
        Stopped existing backend processes
        Stopped existing frontend processes
        Process cleanup complete
    """
    print("🧹 Cleaning up existing processes...")
    
    try:
        # Kill existing uvicorn processes (backend)
        result_uvicorn = subprocess.run(['pkill', '-f', 'uvicorn'], 
                                       capture_output=True, text=True)
        if result_uvicorn.returncode == 0:
            print("  Stopped existing backend processes")
        
        # Kill existing streamlit processes (frontend)  
        result_streamlit = subprocess.run(['pkill', '-f', 'streamlit'], 
                                         capture_output=True, text=True)
        if result_streamlit.returncode == 0:
            print("  Stopped existing frontend processes")
            
        # Wait a moment for processes to fully terminate
        time.sleep(2)
        
        print("Process cleanup complete")
        
    except Exception as e:
        print(f"⚠️  Process cleanup warning: {e}")
        print("  Continuing with launch...")
# ------------------------------------------------------------------------- end cleanup_existing_processes()

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# ------------------------------------------------------------------------- main()
def main() -> int:
    """Main launcher function for the MRCA Advanced Parallel Hybrid system.

    This function orchestrates the complete application launch process including
    dependency checking, process cleanup, service startup, and health monitoring.
    It provides comprehensive status reporting and dev container specific instructions
    for accessing the application.

    Returns:
        int: Exit code (0 for success, 1 for failure).

    Examples:
        >>> main()
        MRCA Advanced Parallel Hybrid Application Launcher (Fixed)
        =================================================================
        MRCA Application Launched Successfully!
        0
    """
    print("MRCA Advanced Parallel Hybrid Application Launcher (Fixed)")
    print("=" * 65)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the MRCA project root directory")
        return 1
    
    # Clean up any existing processes first
    cleanup_existing_processes()
    
    # Check and install dependencies if needed
    if not check_dependencies():
        print("Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return 1
    
    processes = []
    
    try:
        # Launch backend with proper module handling
        backend_process = launch_backend()
        if backend_process:
            processes.append(backend_process)
        
        # Give backend more time to start
        time.sleep(5)
        
        # Launch frontend
        frontend_process = launch_frontend()
        if frontend_process:
            processes.append(frontend_process)
        
        # Wait for services
        wait_for_services()
        
        print("\nMRCA Application Launched Successfully!")
        print("=" * 65)
        print("Frontend UI (Primary Access): http://localhost:8501")
        print("Backend API: http://localhost:8000")
        print("API Documentation: http://localhost:8000/docs")
        print("Health Check: http://localhost:8000/health")
        print("=" * 65)
        
        # Browser opening instructions
        print("BROWSER ACCESS:")
        print("   Browser should open automatically!")
        print("   If browser doesn't open, manually visit: http://localhost:8501")
        print("   For dev containers: Use the PORTS tab or port forwarding")
        
        print("\nBrowser auto-opening enabled for immediate access")
        
        print("\nAdvanced Parallel Hybrid Technology Ready!")
        print("   - Dual AI processing modes")
        print("   - 4 fusion strategies available") 
        print("   - 5 template types for regulatory compliance")
        print("   - Real-time performance analytics")
        print("   - Neo4j knowledge graph integration")
        print("\nPress Ctrl+C to stop all services")
        
        # Monitor processes and wait for user to stop
        try:
            while True:
                # Check if processes are still running
                for i, process in enumerate(processes):
                    if process and process.poll() is not None:
                        print(f"⚠️ Process {i} (PID {process.pid}) has stopped unexpectedly")
                        # Try to restart the process
                        if i == 0:  # Backend process
                            print("Attempting to restart backend...")
                            new_process = launch_backend()
                            if new_process:
                                processes[i] = new_process
                        elif i == 1:  # Frontend process
                            print("Attempting to restart frontend...")
                            new_process = launch_frontend()
                            if new_process:
                                processes[i] = new_process
                time.sleep(5)  # Check every 5 seconds
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            
    except Exception as e:
        print(f"❌ Error during launch: {e}")
        
    finally:
        # Clean up processes
        for process in processes:
            if process and process.poll() is None:
                print(f"🔌 Stopping process {process.pid}")
                process.terminate()
                time.sleep(2)
                if process.poll() is None:
                    process.kill()
        
        print("✅ All services stopped")
        return 0
# ------------------------------------------------------------------------- end main()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.
# It serves as the entry point for the MRCA application launcher.

if __name__ == "__main__":
    # --- MRCA Application Launch ---
    print("Starting MRCA Advanced Parallel Hybrid Application...")
    
    # Execute main launcher function and exit with appropriate code
    sys.exit(main())

# =========================================================================
# End of File
# =========================================================================
