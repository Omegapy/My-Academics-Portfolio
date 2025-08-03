# -------------------------------------------------------------------------
# File: graph.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/graph.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides centralized Neo4j graph database connectivity and management
# for the MRCA backend system. It implements lazy loading patterns for Neo4j
# connections to ensure proper resource management and resilience. The module
# handles configuration validation, connection setup, and provides factory functions
# for creating graph database instances used throughout the Advanced Parallel Hybrid
# system for GraphRAG operations and regulatory knowledge graph queries.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: validate_neo4j_config() - Validates Neo4j database configuration
# - Function: get_graph() - Factory function for Neo4j graph instance
# - Function: get_graph_schema() - Retrieves current graph schema for debugging
# - Function: test_connection() - Tests Neo4j database connectivity
# - Class: LazyGraph - Lazy loading wrapper for graph instance with query handling
# - Global Variable: graph - Lazy-loaded graph instance for backwards compatibility
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - logging: For error logging and debugging
# - Third-Party:
#   - langchain_neo4j.Neo4jGraph: Neo4j graph database integration for GraphRAG
# - Local Project Modules:
#   - .config.init_config: Configuration management for Neo4j connection settings
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is imported by various components requiring graph database functionality:
# - tools/cypher.py: Uses graph for executing Cypher queries in GraphRAG operations
# - parallel_hybrid.py: Uses graph for knowledge graph retrieval
# - Any component needing access to the regulatory knowledge graph
# The lazy loading pattern ensures connections are only created when needed,
# improving startup performance and error resilience for database connectivity.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Centralized Neo4j Graph Database Connectivity for MRCA Backend

Provides lazy loading Neo4j connections and graph database management for
the Advanced Parallel Hybrid system, supporting GraphRAG operations and
regulatory knowledge graph queries with proper resource management.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging

# Third-party library imports
from langchain_neo4j import Neo4jGraph

# Local application/library specific imports
from .config import init_config

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# --------------------------
# --- Utility Functions ---
# --------------------------

# ------------------------------------------------------------------------- validate_neo4j_config()
def validate_neo4j_config() -> tuple:
    """Validate Neo4j configuration and provide helpful error messages.

    This function checks that all required Neo4j connection parameters are
    properly configured including URI, username, and password. It validates
    the presence of these values to prevent runtime errors during graph
    database connection initialization.

    Returns:
        tuple: A tuple containing (uri, username, password) if validation succeeds.

    Raises:
        ValueError: If any required Neo4j configuration parameter is missing.

    Examples:
        >>> uri, username, password = validate_neo4j_config()
        >>> print(f"Connecting to: {uri}")
        Connecting to: bolt://localhost:7687
    """
    config = init_config()
    
    if not config.neo4j_uri or not config.neo4j_username or not config.neo4j_password:
        error_msg = "Missing Neo4j configuration in backend config"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    return config.neo4j_uri, config.neo4j_username, config.neo4j_password
# ------------------------------------------------------------------------- end validate_neo4j_config()

# ------------------------------------------------------------------------- get_graph_schema()
def get_graph_schema() -> str:
    """Get the current graph schema for debugging.

    This function retrieves the current Neo4j graph schema which is useful
    for debugging, development, and understanding the structure of the
    regulatory knowledge graph.

    Returns:
        str: The graph schema information or error message if retrieval fails.

    Examples:
        >>> schema = get_graph_schema()
        >>> print("Current graph structure:", schema)
    """
    try:
        graph_instance = get_graph()
        schema = graph_instance.get_schema
        return schema
    except Exception as e:
        return f"Error getting schema: {str(e)}"
# ------------------------------------------------------------------------- end get_graph_schema()

# ------------------------------------------------------------------------- test_connection()
def test_connection() -> tuple:
    """Test Neo4j connection.

    This function performs a simple connectivity test to the Neo4j database
    by executing a basic query. It's useful for health checks and verifying
    that the database connection is working properly.

    Returns:
        tuple: A tuple containing (success_bool, message_string) indicating
               the result of the connection test.

    Examples:
        >>> success, message = test_connection()
        >>> print(f"Connection test: {'PASSED' if success else 'FAILED'} - {message}")
        Connection test: PASSED - Connection successful
    """
    try:
        # Use the lazy graph instance for testing
        result = graph.query("RETURN 1 as test")
        return True, "Connection successful"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
# ------------------------------------------------------------------------- end test_connection()

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# ------------------------------------------------------------------------- get_graph()
def get_graph():
    """Lazy loading function to get Neo4j graph connection.

    Creates connection only when needed for better resilience.
    This function provides a factory pattern for creating Neo4jGraph instances
    with proper configuration for the MRCA regulatory knowledge graph.

    Returns:
        Neo4jGraph: Connected Neo4j graph instance ready for Cypher queries.

    Raises:
        Exception: If graph connection fails due to configuration or network issues.

    Examples:
        >>> graph_instance = get_graph()
        >>> result = graph_instance.query("MATCH (n) RETURN count(n) as node_count")
        >>> print(f"Total nodes: {result[0]['node_count']}")
    """
    try:
        uri, username, password = validate_neo4j_config()
        return Neo4jGraph(
            url=uri,
            username=username,
            password=password,
        )
    except Exception as e:
        logger.error(f"Neo4j connection error: {str(e)}")
        raise
# ------------------------------------------------------------------------- end get_graph()

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class LazyGraph
class LazyGraph:
    """Lazy loading wrapper for graph instance.

    This class implements a lazy loading pattern that delays Neo4j graph connection
    initialization until the instance is actually used. This improves startup
    performance and provides better error handling by deferring potential
    connection issues until the graph is actually needed. It also provides
    explicit query method handling for better error management.

    Class Attributes:
        None

    Instance Attributes:
        _graph (Neo4jGraph): The underlying graph instance, initialized on first access.

    Methods:
        _get_graph(): Internal method to get or create the graph instance.
        __getattr__(): Proxies attribute access to the underlying graph instance.
        query(): Explicit query method with enhanced error handling.
    """
    
    # -------------------
    # --- Constructor ---
    # -------------------
    
    # ------------------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initializes the LazyGraph wrapper.

        Creates a wrapper instance without immediately initializing the underlying
        Neo4j graph connection. The actual connection creation is deferred until
        first attribute access or query execution.
        """
        self._graph = None
    # ------------------------------------------------------------------------- end __init__()

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # ------------------------------------------------------------------------- _get_graph()
    def _get_graph(self):
        """Get the graph instance, creating it if needed.

        This internal method implements the lazy loading logic by checking if
        the graph instance exists and creating it if necessary. It's called
        by other methods that need access to the underlying graph.

        Returns:
            Neo4jGraph: The initialized graph database connection.
        """
        if self._graph is None:
            self._graph = get_graph()
        return self._graph
    # ------------------------------------------------------------------------- end _get_graph()
    
    # ------------------------------------------------------------------------- __getattr__()
    def __getattr__(self, name):
        """Proxies attribute access to the underlying graph instance.

        This method implements the lazy loading by creating the graph instance
        on first attribute access and then delegating all subsequent calls
        to the actual Neo4jGraph object.

        Args:
            name (str): The attribute or method name being accessed.

        Returns:
            Any: The result of the attribute access on the underlying graph instance.
        """
        return getattr(self._get_graph(), name)
    # ------------------------------------------------------------------------- end __getattr__()

    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # ------------------------------------------------------------------------- query()
    def query(self, *args, **kwargs):
        """Handle query method explicitly for better error handling.

        This method provides explicit handling of the query operation with
        enhanced error handling and logging. It ensures that database queries
        are executed through the lazy-loaded graph instance.

        Args:
            *args: Variable length argument list passed to the underlying query method.
            **kwargs: Arbitrary keyword arguments passed to the underlying query method.

        Returns:
            Any: The result of the query execution from the Neo4j database.
        """
        return self._get_graph().query(*args, **kwargs)
    # ------------------------------------------------------------------------- end query()

# ------------------------------------------------------------------------- end class LazyGraph

# =========================================================================
# Module Initialization / Global Variables
# =========================================================================
# Backwards compatibility - create graph instance when accessed
# This allows existing code to work while providing lazy loading benefits

# Global lazy-loaded graph instance for module-level access
graph = LazyGraph()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This module is designed to be imported, not executed directly.
# No main execution guard is needed.

# =========================================================================
# End of File
# =========================================================================