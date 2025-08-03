# -------------------------------------------------------------------------
# File: database.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/database.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides an enhanced Neo4j database layer with comprehensive
# resilience features for the MRCA backend system. It implements connection
# pooling, retry logic, health monitoring, and metrics collection to ensure
# robust database operations. The module serves as the primary interface
# for all Neo4j database interactions in the Advanced Parallel Hybrid system,
# providing both high-level convenience functions and detailed error handling
# for graph database operations supporting regulatory knowledge graph queries.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: DatabaseConfig - Configuration dataclass for database settings
# - Class: DatabaseMetrics - Metrics tracking dataclass for performance monitoring
# - Class: MRCADatabaseError - Base exception class for database errors
# - Class: DatabaseConnectionError - Exception for connection failures
# - Class: DatabaseQueryError - Exception for query execution failures
# - Class: EnhancedNeo4jDatabase - Main database class with resilience features
# - Function: get_database() - Factory function for global database instance
# - Function: get_graph() - Backward compatibility function for legacy code
# - Function: database_health_check() - Standalone health check function
# - Function: reset_database_connection() - Connection reset utility function
# - Global Variables: _database_instance, _database_lock - Thread-safe singleton pattern
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - time: For timing operations and backoff delays
#   - logging: For comprehensive error and operation logging
#   - typing: For type hints (Optional, Dict, Any, List)
#   - dataclasses: For configuration and metrics data structures
#   - threading.Lock: For thread-safe singleton pattern implementation
# - Third-Party:
#   - neo4j.GraphDatabase, Driver, Record: Core Neo4j database connectivity
#   - neo4j.exceptions: Specific Neo4j error handling (ServiceUnavailable, TransientError, DatabaseError)
# - Local Project Modules:
#   - .config.get_config: Configuration management for database connection parameters
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is used throughout the MRCA backend for all Neo4j database operations:
# - tools/cypher.py: Uses enhanced database for Cypher query execution
# - graph.py: Legacy compatibility through get_graph() function
# - Health monitoring systems: Uses database_health_check() for status reporting
# - Application startup: Uses get_database() for singleton database instance
# The enhanced features provide retry logic, connection pooling, and comprehensive
# metrics collection essential for production database operations.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Enhanced Neo4j Database Layer with Resilience Features

Provides connection pooling, retry logic, and comprehensive health monitoring.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import time
import logging
from typing import Optional, Dict, Any, List, cast, LiteralString
from dataclasses import dataclass
from threading import Lock

# Third-party library imports
from neo4j import GraphDatabase, Driver, Record
from neo4j.exceptions import ServiceUnavailable, TransientError, DatabaseError

# Local application/library specific imports
from .config import get_config

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# Global database instance and thread lock for singleton pattern
_database_instance: Optional['EnhancedNeo4jDatabase'] = None
_database_lock = Lock()

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class DatabaseConfig
@dataclass
class DatabaseConfig:
    """Configuration for enhanced database connection.

    This dataclass defines all configuration parameters for the enhanced
    Neo4j database connection including connection pooling, timeouts,
    and retry behavior settings.

    Class Attributes:
        None

    Instance Attributes:
        pool_size (int): Maximum connections in pool. Defaults to 10.
        max_connection_lifetime (int): Connection lifetime in seconds. Defaults to 300.
        max_connection_pool_size (int): Maximum pool size. Defaults to 50.
        connection_timeout (float): Connection timeout in seconds. Defaults to 5.0.
        max_retry_attempts (int): Maximum retry attempts. Defaults to 3.
        health_check_timeout (float): Health check timeout. Defaults to 5.0.

    Methods:
        None (dataclass with default values)
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    pool_size: int = 10                    # Maximum connections in pool
    max_connection_lifetime: int = 300     # Connection lifetime in seconds
    max_connection_pool_size: int = 50     # Maximum pool size
    connection_timeout: float = 5.0        # Connection timeout in seconds
    max_retry_attempts: int = 3            # Maximum retry attempts
    health_check_timeout: float = 5.0      # Health check timeout
    
# ------------------------------------------------------------------------- end class DatabaseConfig

# ------------------------------------------------------------------------- class DatabaseMetrics
@dataclass 
class DatabaseMetrics:
    """Database operation metrics.

    This dataclass tracks comprehensive metrics for database operations
    including query counts, success rates, and response time analytics.
    It provides methods to update and calculate derived metrics.

    Class Attributes:
        None

    Instance Attributes:
        total_queries (int): Total number of queries executed.
        successful_queries (int): Number of successful queries.
        failed_queries (int): Number of failed queries.
        average_response_time (float): Average query response time.
        total_response_time (float): Cumulative response time for all queries.

    Methods:
        update_response_time(): Updates average response time calculations.
    """
    
    # ----------------------
    # --- Class Variable ---
    # ----------------------
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    average_response_time: float = 0.0
    total_response_time: float = 0.0
    
    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # ------------------------------------------------------------------------- update_response_time()
    def update_response_time(self, response_time: float) -> None:
        """Update average response time.

        This method updates the running average of response times by
        incorporating a new response time measurement into the overall
        statistics.

        Args:
            response_time (float): The response time in seconds to add to metrics.
        """
        self.total_response_time += response_time
        if self.total_queries > 0:
            self.average_response_time = self.total_response_time / self.total_queries
    # ------------------------------------------------------------------------- end update_response_time()

# ------------------------------------------------------------------------- end class DatabaseMetrics

# ------------------------------------------------------------------------- class MRCADatabaseError
class MRCADatabaseError(Exception):
    """Base exception for MRCA database errors.

    This is the base exception class for all database-related errors
    in the MRCA system. It provides a consistent error hierarchy
    for database exception handling.

    Class Attributes:
        None

    Instance Attributes:
        Inherits from Exception

    Methods:
        Inherits from Exception
    """
    pass
# ------------------------------------------------------------------------- end class MRCADatabaseError

# ------------------------------------------------------------------------- class DatabaseConnectionError
class DatabaseConnectionError(MRCADatabaseError):
    """Exception for database connection failures.

    This exception is raised when database connection establishment
    or maintenance fails. It provides specific error handling for
    connection-related issues.

    Class Attributes:
        None

    Instance Attributes:
        Inherits from MRCADatabaseError

    Methods:
        Inherits from MRCADatabaseError
    """
    pass
# ------------------------------------------------------------------------- end class DatabaseConnectionError

# ------------------------------------------------------------------------- class DatabaseQueryError
class DatabaseQueryError(MRCADatabaseError):
    """Exception for database query failures.

    This exception is raised when database query execution fails
    after all retry attempts have been exhausted. It provides
    specific error handling for query-related issues.

    Class Attributes:
        None

    Instance Attributes:
        Inherits from MRCADatabaseError

    Methods:
        Inherits from MRCADatabaseError
    """
    pass
# ------------------------------------------------------------------------- end class DatabaseQueryError

# ------------------------------------------------------------------------- class EnhancedNeo4jDatabase
class EnhancedNeo4jDatabase:
    """Enhanced Neo4j database connection with resilience features.

    This class provides a robust, production-ready interface to Neo4j
    with connection pooling, automatic retry logic, comprehensive health
    monitoring, and detailed metrics collection. It implements a thread-safe
    design with proper resource management for high-availability database operations.

    Class Attributes:
        None

    Instance Attributes:
        config (DatabaseConfig): Configuration settings for database operations.
        metrics (DatabaseMetrics): Performance and operational metrics.
        _driver (Optional[Driver]): Neo4j driver instance.
        _lock (Lock): Thread synchronization lock.
        _is_connected (bool): Connection status flag.

    Methods:
        _create_driver(): Creates Neo4j driver with enhanced configuration.
        connect(): Establishes database connection.
        disconnect(): Closes database connection and cleanup resources.
        execute_query(): Executes Cypher query with retry logic.
        health_check(): Performs comprehensive database health check.
        _get_metrics(): Gets current database metrics.
    """
    
    # -------------------
    # --- Constructor ---
    # -------------------
    
    # --------------------------------------------------------------------------------- __init__()
    def __init__(self, config: Optional[DatabaseConfig] = None) -> None:
        """Initializes the EnhancedNeo4jDatabase instance.

        Creates an enhanced database instance with the specified configuration
        or default settings. Initializes metrics tracking and prepares the
        connection management infrastructure.

        Args:
            config (Optional[DatabaseConfig]): Database configuration settings.
                                             If None, uses default configuration.
        """
        self.config = config or DatabaseConfig()
        self.metrics = DatabaseMetrics()
        self._driver: Optional[Driver] = None
        self._lock = Lock()
        self._is_connected = False
        
        logger.info(f"Enhanced Neo4j database initialized")
    # --------------------------------------------------------------------------------- end __init__()

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # --------------------------------------------------------------------------------- _create_driver()
    def _create_driver(self) -> Driver:
        """Create Neo4j driver with enhanced configuration.

        This internal method creates a Neo4j driver instance with optimized
        settings for production use including connection pooling, timeouts,
        and lifecycle management.

        Returns:
            Driver: Configured Neo4j driver instance.

        Raises:
            DatabaseConnectionError: If configuration is invalid or driver creation fails.
        """
        app_config = get_config()
        
        if not app_config.neo4j_uri:
            raise DatabaseConnectionError("Neo4j URI not configured")
        
        if not app_config.neo4j_username or not app_config.neo4j_password:
            raise DatabaseConnectionError("Neo4j credentials not configured")
        
        driver = GraphDatabase.driver(
            app_config.neo4j_uri,
            auth=(app_config.neo4j_username, app_config.neo4j_password),
            max_connection_lifetime=self.config.max_connection_lifetime,
            max_connection_pool_size=self.config.max_connection_pool_size,
            connection_timeout=self.config.connection_timeout,
        )
        
        logger.info(f"Neo4j driver created")
        return driver
    # --------------------------------------------------------------------------------- end _create_driver()
    
    # --------------------------------------------------------------------------------- _get_metrics()
    def _get_metrics(self) -> Dict[str, Any]:
        """Get current database metrics.

        This internal method compiles current database performance metrics
        including query counts, success rates, and response times into
        a dictionary format for monitoring and reporting.

        Returns:
            Dict[str, Any]: Dictionary containing current database metrics.
        """
        success_rate = 0.0
        if self.metrics.total_queries > 0:
            success_rate = self.metrics.successful_queries / self.metrics.total_queries
        
        return {
            "total_queries": self.metrics.total_queries,
            "successful_queries": self.metrics.successful_queries,
            "failed_queries": self.metrics.failed_queries,
            "success_rate": success_rate,
            "average_response_time": self.metrics.average_response_time,
            "is_connected": self._is_connected,
        }
    # --------------------------------------------------------------------------------- end _get_metrics()

    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # --------------------------------------------------------------------------------- connect()
    def connect(self) -> Driver:
        """Establish database connection.

        This method establishes a connection to the Neo4j database using
        thread-safe singleton pattern. It creates the driver instance if
        it doesn't exist and updates connection status.

        Returns:
            Driver: The connected Neo4j driver instance.

        Raises:
            DatabaseConnectionError: If connection establishment fails.
        """
        try:
            with self._lock:
                if self._driver is None:
                    self._driver = self._create_driver()
                    self._is_connected = True
                    logger.info("Neo4j database connection established")
                return self._driver
                
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j database: {e}")
            self._is_connected = False
            raise DatabaseConnectionError(f"Connection failed: {e}")
    # --------------------------------------------------------------------------------- end connect()
    
    # --------------------------------------------------------------------------------- disconnect()
    def disconnect(self) -> None:
        """Close database connection and cleanup resources.

        This method safely closes the database connection and cleans up
        all associated resources. It uses proper synchronization to ensure
        thread safety during shutdown.
        """
        with self._lock:
            if self._driver:
                try:
                    self._driver.close()
                    logger.info("Neo4j database connection closed")
                except Exception as e:
                    logger.warning(f"Error closing database connection: {e}")
                finally:
                    self._driver = None
                    self._is_connected = False
    # --------------------------------------------------------------------------------- end disconnect()
    
    # --------------------------------------------------------------------------------- execute_query()
    def execute_query(self, query: str, parameters: Optional[Dict] = None) -> List[Record]:
        """Execute a Cypher query with retry logic.

        This method executes Cypher queries with automatic retry logic,
        comprehensive error handling, and metrics tracking. It handles
        transient failures and provides detailed logging.

        Args:
            query (str): The Cypher query to execute.
            parameters (Optional[Dict]): Query parameters. Defaults to None.

        Returns:
            List[Record]: List of Neo4j records returned by the query.

        Raises:
            DatabaseQueryError: If query execution fails after all retry attempts.
            DatabaseConnectionError: If database connection cannot be established.
        """
        start_time = time.time()
        parameters = parameters or {}
        
        retry_count = 0
        last_error = None
        
        while retry_count < self.config.max_retry_attempts:
            try:
                if not self._driver:
                    self.connect()
                
                if self._driver is None:
                    raise DatabaseConnectionError("Failed to establish database connection")
                
                with self._driver.session() as session:
                    result = session.run(cast(LiteralString, query), parameters)
                    records = list(result)
                    
                # Update metrics
                response_time = time.time() - start_time
                self.metrics.total_queries += 1
                self.metrics.successful_queries += 1
                self.metrics.update_response_time(response_time)
                
                logger.debug(f"Query executed successfully in {response_time:.3f}s")
                return records
                
            except (ServiceUnavailable, TransientError) as e:
                last_error = e
                retry_count += 1
                if retry_count < self.config.max_retry_attempts:
                    wait_time = retry_count * 2  # Simple backoff
                    logger.warning(f"Query failed, retrying in {wait_time}s (attempt {retry_count}): {e}")
                    time.sleep(wait_time)
                else:
                    break
            except Exception as e:
                self.metrics.failed_queries += 1
                logger.error(f"Query execution failed: {e}")
                raise DatabaseQueryError(f"Query failed: {e}")
        
        # All retries exhausted
        self.metrics.failed_queries += 1
        logger.error(f"Query failed after {retry_count} attempts: {last_error}")
        raise DatabaseQueryError(f"Query failed after retries: {last_error}")
    # --------------------------------------------------------------------------------- end execute_query()

    # ---------------------------------------------------------------------
    # --- Class Information Methods (Optional, but highly recommended) ---
    # ---------------------------------------------------------------------
    
    # --------------------------------------------------------------------------------- health_check()
    def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive database health check.

        This method executes a comprehensive health check of the database
        connection and performance, returning detailed status information
        including response times, connection status, and current metrics.

        Returns:
            Dict[str, Any]: Dictionary containing comprehensive health status information.
        """
        health_status = {
            "database": "unknown",
            "connection": "unknown",
            "response_time": None,
            "metrics": self._get_metrics(),
            "error": None
        }
        
        start_time = time.time()
        
        try:
            if not self._driver:
                self.connect()
            
            if self._driver is None:
                raise DatabaseConnectionError("Failed to establish database connection")
            
            # Execute simple health check query
            with self._driver.session() as session:
                result = session.run("RETURN 1 as health_check")
                record = result.single()
                
                response_time = time.time() - start_time
                
                if record and record["health_check"] == 1:
                    health_status.update({
                        "database": "healthy",
                        "connection": "active",
                        "response_time": response_time
                    })
                else:
                    health_status.update({
                        "database": "unhealthy",
                        "connection": "failed",
                        "error": "Health check query failed"
                    })
                    
        except Exception as e:
            response_time = time.time() - start_time
            health_status.update({
                "database": "unhealthy",
                "connection": "failed",
                "response_time": response_time,
                "error": str(e)
            })
            logger.warning(f"Database health check failed: {e}")
        
        return health_status
    # --------------------------------------------------------------------------------- end health_check()

# ------------------------------------------------------------------------- end class EnhancedNeo4jDatabase

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# --------------------------------------------------------------------------------- get_database()
def get_database() -> EnhancedNeo4jDatabase:
    """Get or create the global enhanced database instance.

    This function implements a thread-safe singleton pattern to provide
    a global enhanced database instance. It ensures only one database
    connection manager exists throughout the application lifecycle.

    Returns:
        EnhancedNeo4jDatabase: The global enhanced database instance.

    Examples:
        >>> db = get_database()
        >>> result = db.execute_query("MATCH (n) RETURN count(n)")
        >>> print(f"Total nodes: {result[0]['count(n)']}")
    """
    global _database_instance
    
    with _database_lock:
        if _database_instance is None:
            _database_instance = EnhancedNeo4jDatabase()
            logger.info("Global enhanced database instance created")
        return _database_instance
# --------------------------------------------------------------------------------- end get_database()

# --------------------------------------------------------------------------------- get_graph()
def get_graph():
    """Backward compatibility function to get database instance.

    This function provides backward compatibility with existing code
    that expects a simple graph interface. It wraps the enhanced database
    functionality in a simplified interface matching legacy expectations.

    Returns:
        GraphWrapper: A simplified wrapper providing backward compatibility.

    Examples:
        >>> graph = get_graph()
        >>> result = graph.query("MATCH (n) RETURN count(n)")
        >>> schema = graph.get_schema()
    """
    database = get_database()
    
    # Create a simplified wrapper for backward compatibility
    class GraphWrapper:
        def __init__(self, db: EnhancedNeo4jDatabase):
            self._db = db
        
        def query(self, query: str, parameters: Optional[Dict] = None) -> List[Record]:
            """Execute query with enhanced error handling"""
            return self._db.execute_query(query, parameters)
        
        def get_schema(self) -> str:
            """Get database schema information"""
            try:
                # Get node labels
                labels_result = self._db.execute_query("CALL db.labels()")
                labels = [record["label"] for record in labels_result]
                
                # Get relationship types
                rel_types_result = self._db.execute_query("CALL db.relationshipTypes()")
                rel_types = [record["relationshipType"] for record in rel_types_result]
                
                schema = f"Node Labels: {', '.join(labels)}\n"
                schema += f"Relationship Types: {', '.join(rel_types)}"
                
                return schema
            except Exception as e:
                logger.warning(f"Failed to get schema: {e}")
                return "Schema information unavailable"
    
    return GraphWrapper(database)
# --------------------------------------------------------------------------------- end get_graph()

# ------------------------
# --- Helper Functions ---
# ------------------------

# --------------------------------------------------------------------------------- database_health_check()
def database_health_check() -> Dict[str, Any]:
    """Perform database health check.

    This standalone function provides a convenient interface for performing
    database health checks without requiring direct database instance management.
    It's useful for health monitoring systems and API endpoints.

    Returns:
        Dict[str, Any]: Dictionary containing comprehensive health status information.

    Examples:
        >>> health = database_health_check()
        >>> print(f"Database status: {health['database']}")
        Database status: healthy
    """
    database = get_database()
    return database.health_check()
# --------------------------------------------------------------------------------- end database_health_check()

# --------------------------------------------------------------------------------- reset_database_connection()
def reset_database_connection() -> None:
    """Reset database connection (useful for testing).

    This function resets the global database connection, which is primarily
    useful for testing scenarios where a fresh connection state is needed.
    It safely disconnects and clears the global database instance.

    Examples:
        >>> reset_database_connection()
        >>> # Fresh database connection will be created on next access
    """
    global _database_instance
    
    with _database_lock:
        if _database_instance:
            _database_instance.disconnect()
            _database_instance = None
        logger.info("Database connection reset")
# --------------------------------------------------------------------------------- end reset_database_connection()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This module is designed to be imported, not executed directly.
# No main execution guard is needed.

# =========================================================================
# End of File
# =========================================================================