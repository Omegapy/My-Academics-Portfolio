"""
MRCA Frontend Package - Advanced Parallel Hybrid UI

This package contains the frontend components for the Mining Regulatory Compliance Assistant (MRCA).
It provides a Streamlit-based web interface for interacting with the Advanced Parallel Hybrid backend system.

Components:
- bot.py: Main Streamlit chat interface with advanced configuration options
- utils.py: Frontend-specific utilities for session management and formatting

Communication:
- HTTP client for backend API communication
- Real-time configuration for fusion strategies and templates  
- Performance analytics display
- Session management and chat history

Architecture:
- Streamlit web application (port 8501)
- Containerized deployment with Dockerfile.frontend
- Independent service that communicates with backend via HTTP API

Version: 2.0.0 (Advanced Parallel Hybrid UI)
"""

__version__ = "2.0.0"
__title__ = "MRCA Frontend - Advanced Parallel Hybrid UI" 