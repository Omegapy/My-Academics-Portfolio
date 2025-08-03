#!/usr/bin/env python3

# -------------------------------------------------------------------------
# File: launch_devcontainer.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25 
# File Path: launch_devcontainer.py
# ------------------------------------------------------------------------

# --- Module Objective ---
#   This module provides a comprehensive launcher for the MRCA Advanced Parallel Hybrid
#   application specifically optimized for VS Code Dev Containers. It handles automated
#   service startup, health monitoring, graceful shutdown, and provides detailed access
#   information for both frontend and backend services. The launcher ensures proper
#   process management and port forwarding compatibility within containerized environments.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: DevContainerLauncher (Main launcher orchestrator)
# - Function: main execution guard with launcher instantiation
# - Signal handling for graceful shutdown
# - Service health monitoring and status reporting
# - VS Code Dev Container specific optimizations
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: os, sys, time, signal, subprocess, pathlib (system operations and process management)
# - Third-Party: requests (HTTP health check requests)
# - Local Project Modules: None (standalone launcher module)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is designed as a standalone launcher script executed directly from the
# project root directory. It should be called via `python3 launch_devcontainer.py`
# from VS Code Dev Containers or similar containerized development environments.
# The launcher handles all service dependencies automatically and provides real-time
# status feedback for the MRCA application stack.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
MRCA Dev Container Launcher

Optimized launcher for VS Code Dev Containers with proper port forwarding,
health monitoring, and graceful service management for the MRCA Advanced
Parallel Hybrid application stack.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from typing import Optional

# Third-party library imports
import requests

# Local application/library specific imports
# None - standalone launcher module

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Default service ports for MRCA application
BACKEND_PORT = 8000  # FastAPI backend service port
FRONTEND_PORT = 8501  # Streamlit frontend service port
HEALTH_CHECK_TIMEOUT = 5  # Timeout for health check requests in seconds
SERVICE_STARTUP_DELAY = 5  # Initial delay for service startup in seconds
HEALTH_CHECK_RETRIES = 10  # Maximum retries for health checks

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- DevContainerLauncher
class DevContainerLauncher:
    """Comprehensive launcher for MRCA services in Dev Container environments.

    This class orchestrates the startup, monitoring, and shutdown of both frontend
    and backend services for the MRCA Advanced Parallel Hybrid application. It provides
    specialized handling for VS Code Dev Container environments with proper port
    forwarding, health monitoring, and graceful process management.

    Class Attributes:
        None

    Instance Attributes:
        backend_process (subprocess.Popen): Process handle for the FastAPI backend service
        frontend_process (subprocess.Popen): Process handle for the Streamlit frontend service  
        project_root (Path): Absolute path to the MRCA project root directory

    Methods:
        cleanup_processes(): Terminates any existing MRCA service processes
        start_backend(): Launches the FastAPI backend server with proper configuration
        start_frontend(): Launches the Streamlit frontend server with Dev Container optimizations
        wait_for_services(): Monitors service health and confirms successful startup
        print_access_info(): Displays comprehensive access information and URLs
        signal_handler(): Handles graceful shutdown on interrupt signals
        launch(): Main orchestration method for complete service startup
    """

    # -------------------
    # --- Constructor ---
    # -------------------
    
    # --------------------------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initializes the DevContainerLauncher with default state.

        Sets up process handles and determines the project root directory for
        relative path resolution during service startup.
        """
        self.backend_process = None
        self.frontend_process = None
        self.project_root = Path(__file__).parent.absolute()
    # --------------------------------------------------------------------------------- end __init__()

    # ---------------------------
    # --- Process Management ---
    # ---------------------------

    # --------------------------------------------------------------------------------- cleanup_processes()
    def cleanup_processes(self) -> None:
        """Terminates any existing MRCA service processes.

        Performs a comprehensive cleanup of any running Streamlit or Uvicorn processes
        that might conflict with the new service instances. Uses pkill for reliable
        process termination and includes a delay for complete cleanup.
        """
        print("Cleaning up existing processes...")
        try:
            subprocess.run(["pkill", "-f", "streamlit"], check=False, capture_output=True)
            subprocess.run(["pkill", "-f", "uvicorn"], check=False, capture_output=True)
            time.sleep(2)
        except Exception as e:
            print(f"Note: {e}")
        print("Process cleanup complete")
    # --------------------------------------------------------------------------------- end cleanup_processes()

    # --------------------------------------------------------------------------------- start_backend()
    def start_backend(self) -> bool:
        """Launches the FastAPI backend server with proper configuration.

        Starts the Uvicorn ASGI server hosting the MRCA backend API with reload
        capability and proper host binding for container environments.

        Returns:
            bool: True if backend process started successfully, False otherwise
        """
        print("Starting backend server...")
        
        backend_cmd = [
            sys.executable, "-m", "uvicorn", 
            "backend.main:app",
            "--host", "0.0.0.0",
            "--port", str(BACKEND_PORT), 
            "--reload",
            "--timeout-keep-alive", "3600",
            "--timeout-graceful-shutdown", "30",
            "--access-log"
        ]
        
        # Create a detached process that survives launcher termination
        self.backend_process = subprocess.Popen(
            backend_cmd,
            cwd=self.project_root,
            stdout=subprocess.DEVNULL,  # Detach stdout to prevent blocking
            stderr=subprocess.DEVNULL,  # Detach stderr to prevent blocking
            stdin=subprocess.DEVNULL,   # Detach stdin for complete independence
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None,  # Create new process group (Unix)
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0  # Windows equivalent
        )
        
        print(f"Backend server starting on http://0.0.0.0:{BACKEND_PORT}")
        return True
    # --------------------------------------------------------------------------------- end start_backend()


    # --------------------------------------------------------------------------------- start_frontend()
    def start_frontend(self) -> bool:
        """Launches the Streamlit frontend server with Dev Container optimizations.

        Configures Streamlit with proper host binding, CORS settings, and security
        configurations optimized for VS Code Dev Container port forwarding.

        Returns:
            bool: True if frontend process started successfully, False otherwise
        """
        print("Starting frontend server...")
        
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
        
        # Create a detached process that survives launcher termination
        self.frontend_process = subprocess.Popen(
            frontend_cmd,
            cwd=self.project_root,
            stdout=subprocess.DEVNULL,  # Detach stdout to prevent blocking
            stderr=subprocess.DEVNULL,  # Detach stderr to prevent blocking
            stdin=subprocess.DEVNULL,   # Detach stdin for complete independence
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None,  # Create new process group (Unix)
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0  # Windows equivalent
        )
        
        print(f"Frontend server starting on http://0.0.0.0:{FRONTEND_PORT}")
        return True
    # --------------------------------------------------------------------------------- end start_frontend()

    # -------------------------
    # --- Health Monitoring ---
    # -------------------------

    # --------------------------------------------------------------------------------- wait_for_services()
    def wait_for_services(self) -> bool:
        """Monitors service health and confirms successful startup.

        Performs comprehensive health checks on both backend and frontend services
        using their respective health endpoints. Implements retry logic with
        configurable timeouts to ensure services are fully operational.

        Returns:
            bool: True if both services are healthy, False if any service fails health checks
        """
        print("Waiting for services to start...")
        time.sleep(SERVICE_STARTUP_DELAY)  # Give services time to start
        
        # Check backend health
        backend_healthy = False
        for i in range(HEALTH_CHECK_RETRIES):
            try:
                response = requests.get(f"http://localhost:{BACKEND_PORT}/health", timeout=HEALTH_CHECK_TIMEOUT)
                if response.status_code == 200:
                    print("✅ Backend is healthy")
                    backend_healthy = True
                    break
            except Exception:
                time.sleep(1)
        
        # Check frontend health  
        frontend_healthy = False
        for i in range(HEALTH_CHECK_RETRIES):
            try:
                response = requests.get(f"http://localhost:{FRONTEND_PORT}/_stcore/health", timeout=HEALTH_CHECK_TIMEOUT)
                if response.status_code == 200:
                    print("✅ Frontend is healthy") 
                    frontend_healthy = True
                    break
            except Exception:
                time.sleep(1)
                
        return backend_healthy and frontend_healthy
    # --------------------------------------------------------------------------------- end wait_for_services()

    # -----------------------------
    # --- Information Display ---
    # -----------------------------

    # --------------------------------------------------------------------------------- print_access_info()
    def print_access_info(self) -> None:
        """Displays comprehensive access information for Dev Container environments.

        Provides detailed URLs, VS Code Dev Container specific instructions, and
        feature information for the MRCA Advanced Parallel Hybrid application.
        Includes port forwarding guidance and service capabilities overview.
        """
        print("\n" + "="*80)
        print("MRCA Application Launched Successfully!")
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
        print("Port Forwarding URLs (if available):")
        print("   Check the PORTS tab for forwarded URLs")
        print("")
        print("Advanced Parallel Hybrid Technology Ready!")
        print("   - Dual AI processing modes")
        print("   - 4 fusion strategies available") 
        print("   - Neo4j knowledge graph integration")
        print("")
        print("Press Ctrl+C to stop all services")
        print("="*80)
    # --------------------------------------------------------------------------------- end print_access_info()

    # ---------------------------
    # --- Signal Handling ---
    # ---------------------------

    # --------------------------------------------------------------------------------- signal_handler()
    def signal_handler(self, signum: Optional[int] = None, frame = None) -> None:
        """Handles interrupt signals for graceful service shutdown with user choice.

        Provides options for service management when receiving interrupt signals.
        Users can choose to stop services or let them continue running detached.

        Args:
            signum (Optional[int]): Signal number received. Defaults to None for manual shutdown.
            frame: Current stack frame (unused). Defaults to None.
        """
        print("\n🛑 Launcher interrupted...")
        print("\nServices are running as detached processes and will continue running.")
        print("Access URLs:")
        print(f"  Frontend: http://localhost:{FRONTEND_PORT}")
        print(f"  Backend:  http://localhost:{BACKEND_PORT}")
        print(f"  API Docs: http://localhost:{BACKEND_PORT}/docs")
        print("\nTo stop services manually later, run:")
        print("  pkill -f streamlit && pkill -f uvicorn")
        print("\n✅ Launcher terminated - services continue running")
        sys.exit(0)
    # --------------------------------------------------------------------------------- end signal_handler()

    # -----------------------------
    # --- Main Orchestration ---
    # -----------------------------

    # --------------------------------------------------------------------------------- launch()
    def launch(self) -> None:
        """Main orchestration method for complete MRCA service startup.

        Coordinates the entire service launch sequence including cleanup, service
        startup, health monitoring, and user information display. Implements proper
        error handling and maintains the launcher process for continuous monitoring.

        Raises:
            KeyboardInterrupt: Handled gracefully through signal_handler
            Exception: Any other errors during service startup are caught and reported
        """
        print("MRCA Dev Container Launcher")
        print("="*50)
        
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            # Cleanup and start services
            self.cleanup_processes()
            self.start_backend()
            time.sleep(2)
            self.start_frontend()
            
            # Wait for services to be ready
            if self.wait_for_services():
                self.print_access_info()
                
                print("\n🔗 Services are now running as detached processes.")
                print("   They will continue running even if this launcher is closed.")
                print("   Press Ctrl+C to exit launcher (services will keep running)")
                print("   Or use 'pkill -f streamlit && pkill -f uvicorn' to stop services")
                
                # Keep the launcher running for monitoring (optional)
                try:
                    while True:
                        time.sleep(10)
                        # Optional: Add health monitoring here
                except KeyboardInterrupt:
                    # Gracefully handle Ctrl+C
                    self.signal_handler(signal.SIGINT, None)
                    
            else:
                print("❌ Services failed to start properly")
                self.signal_handler(None, None)
                
        except KeyboardInterrupt:
            self.signal_handler(None, None)
        except Exception as e:
            print(f"❌ Error launching application: {e}")
            self.signal_handler(None, None)
    # --------------------------------------------------------------------------------- end launch()

# ------------------------------------------------------------------------- end DevContainerLauncher

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.
# Provides the main entry point for the MRCA Dev Container launcher application.

if __name__ == "__main__":
    # --- Main Launcher Execution ---
    print("Initializing MRCA Dev Container Launcher...")
    
    try:
        # Create and execute the launcher
        launcher = DevContainerLauncher()
        launcher.launch()
    except Exception as e:
        print(f"❌ Fatal error in launcher initialization: {e}")
        sys.exit(1)
# ---------------------------------------------------------------------------------

# =========================================================================
# End of File
# ========================================================================= 