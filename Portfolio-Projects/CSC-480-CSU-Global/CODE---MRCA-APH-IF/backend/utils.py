# -------------------------------------------------------------------------
# File: utils.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/utils.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides utility functions and session management capabilities
# for the MRCA backend system. It handles conversation session tracking,
# message storage, and response formatting for regulatory queries. The module
# implements a simple in-memory session storage system (suitable for development)
# and provides helper functions for formatting regulatory information responses
# with proper disclaimers and query details.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: get_session_id() - Generate or retrieve unique session identifiers
# - Function: get_session_data() - Retrieve session data dictionary for a given session
# - Function: save_message() - Store conversation messages in session data
# - Function: format_regulatory_response() - Format Cypher query results for display
# - Global Variable: _backend_sessions - In-memory session storage dictionary
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - uuid: For generating unique session identifiers
#   - logging: For debug logging and session tracking
#   - typing.Optional: For type hints with optional parameters
# - Third-Party: None
# - Local Project Modules: None
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is imported by various backend components requiring session management:
# - main.py: Uses session utilities for conversation tracking in API endpoints
# - parallel_hybrid.py: Uses session management for request tracking
# - Any component needing conversation state management or regulatory response formatting
# The session storage is currently in-memory for development but designed for
# easy migration to Redis or database storage in production environments.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

Utility Functions and Session Management for MRCA Backend System

Provides conversation session tracking, message storage, and response formatting 
for regulatory queries. Implements in-memory session storage with helper functions
for formatting regulatory information responses with proper disclaimers and query details.

"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import uuid
import logging
from typing import Optional

# Third-party library imports
# (None for this module)

# Local application/library specific imports
# (None for this module)

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# Backend session storage (in production, use Redis or database)
# Dictionary storing session data keyed by session ID
_backend_sessions = {}

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# --------------------------
# --- Utility Functions ---
# --------------------------

# --------------------------------------------------------------------------------- get_session_id()
def get_session_id(session_id: Optional[str] = None) -> str:
    """Generate or retrieve session ID for conversation tracking.

    This function provides session ID management for conversation tracking.
    If a session ID is provided, it returns that ID. If no session ID is
    provided, it generates a new UUID-based session identifier and logs
    the creation for debugging purposes.

    Args:
        session_id (Optional[str]): Existing session ID to validate and return.
                                  If None, generates a new session ID.

    Returns:
        str: Valid session ID for conversation tracking.

    Examples:
        >>> new_session = get_session_id()
        >>> print(f"New session: {new_session[:8]}...")
        New session: a1b2c3d4...
        
        >>> existing_session = get_session_id("existing-id-123")
        >>> print(existing_session)
        existing-id-123
    """
    if session_id is None:
        session_id = str(uuid.uuid4())
        logger.info(f"Generated new session ID: {session_id[:8]}")
    return session_id
# --------------------------------------------------------------------------------- end get_session_id()

# --------------------------------------------------------------------------------- get_session_data()
def get_session_data(session_id: str) -> dict:
    """Get session data for a given session ID.

    This function retrieves session data from the in-memory storage,
    creating a new session entry if one doesn't exist. Each session
    contains a messages list for conversation history and metadata.

    Args:
        session_id (str): The session identifier to retrieve data for.

    Returns:
        dict: Session data dictionary containing messages and metadata.
              Structure: {"messages": [], "created": timestamp}

    Examples:
        >>> session_data = get_session_data("session-123")
        >>> print(len(session_data["messages"]))
        0
        >>> session_data["messages"].append({"role": "user", "content": "Hello"})
    """
    if session_id not in _backend_sessions:
        _backend_sessions[session_id] = {
            "messages": [],
            "created": str(uuid.uuid4())  # Timestamp placeholder
        }
    return _backend_sessions[session_id]
# --------------------------------------------------------------------------------- end get_session_data()

# --------------------------------------------------------------------------------- save_message()
def save_message(session_id: str, role: str, content: str) -> None:
    """Save a message to the session data.

    This function stores a conversation message in the session data structure,
    maintaining the conversation history for a given session. It automatically
    creates the session if it doesn't exist and logs the operation.

    Args:
        session_id (str): The session identifier to save the message to.
        role (str): The role of the message sender (e.g., "user", "assistant").
        content (str): The message content to store.

    Examples:
        >>> save_message("session-123", "user", "What is Title 30 CFR?")
        >>> save_message("session-123", "assistant", "Title 30 CFR contains...")
        >>> session_data = get_session_data("session-123")
        >>> print(len(session_data["messages"]))
        2
    """
    session_data = get_session_data(session_id)
    session_data["messages"].append({"role": role, "content": content})
    logger.debug(f"Saved {role} message to session {session_id[:8]}")
# --------------------------------------------------------------------------------- end save_message()

# ------------------------
# --- Helper Functions ---
# ------------------------

# --------------------------------------------------------------------------------- format_regulatory_response()
def format_regulatory_response(result_dict: dict) -> str:
    """Format the Cypher query results for regulatory context.

    This function takes the raw results from regulatory database queries
    and formats them into a user-friendly response with proper structure,
    query details, and regulatory disclaimers.

    Args:
        result_dict (dict): Dictionary from query_regulations() containing
                          'answer' and optionally 'cypher_query' keys.

    Returns:
        str: Formatted string ready for display with regulatory information,
             query details, and compliance disclaimers.

    Examples:
        >>> result = {
        ...     "answer": "Safety regulations require...",
        ...     "cypher_query": "MATCH (n:Regulation) RETURN n"
        ... }
        >>> formatted = format_regulatory_response(result)
        >>> print("**Regulatory Information:**" in formatted)
        True
    """
    answer = result_dict.get("answer", "No answer found")
    cypher_query = result_dict.get("cypher_query")
    
    formatted = f"**Regulatory Information:**\n\n{answer}\n\n"
    
    if cypher_query:
        formatted += f"**Query Details:**\n```cypher\n{cypher_query}\n```\n\n"
    
    formatted += "**Disclaimer:** This information is for guidance only. Always consult official CFR documentation for compliance requirements."
    
    return formatted
# --------------------------------------------------------------------------------- end format_regulatory_response()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This module is designed to be imported, not executed directly.
# No main execution guard is needed.

# =========================================================================
# End of File
# =========================================================================