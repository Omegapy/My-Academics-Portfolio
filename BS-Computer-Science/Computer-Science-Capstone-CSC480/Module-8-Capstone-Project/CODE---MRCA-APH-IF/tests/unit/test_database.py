# -------------------------------------------------------------------------
# File: test_database.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-28
# File Path: tests/unit/test_database.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the enhanced database module (backend/database.py).
# Tests EnhancedNeo4jDatabase class, connection management, query execution,
# health checks, metrics tracking, and factory functions. Ensures proper
# database operations with resilience features and error handling.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Enhanced Database Unit Tests

Comprehensive testing of the database layer functionality:
- Database configuration and initialization
- Connection management and pooling
- Query execution with retry logic
- Health checks and metrics tracking
- Factory functions and singleton pattern
- Error handling and resilience features
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List
from threading import Thread

# Import database components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.database import (
    DatabaseConfig, DatabaseMetrics,
    MRCADatabaseError, DatabaseConnectionError, DatabaseQueryError,
    EnhancedNeo4jDatabase, get_database, get_graph,
    database_health_check, reset_database_connection,
    _database_instance, _database_lock
)


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def mock_config():
    """Provide mock application configuration."""
    config = Mock()
    config.neo4j_uri = "neo4j+s://test.databases.neo4j.io"
    config.neo4j_username = "neo4j"
    config.neo4j_password = "test-password"
    return config

@pytest.fixture
def invalid_config():
    """Provide invalid application configuration."""
    config = Mock()
    config.neo4j_uri = None
    config.neo4j_username = None
    config.neo4j_password = None
    return config

@pytest.fixture
def database_config():
    """Provide database configuration for testing."""
    return DatabaseConfig(
        pool_size=5,
        max_connection_lifetime=60,
        max_connection_pool_size=10,
        connection_timeout=2.0,
        max_retry_attempts=2,
        health_check_timeout=3.0
    )

@pytest.fixture
def mock_driver():
    """Provide mock Neo4j driver."""
    driver = Mock()
    session = Mock()
    result = Mock()
    
    # Mock session context manager
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=None)
    
    # Mock query result
    result.data.return_value = [{"count": 100}]
    session.run.return_value = result
    
    driver.session.return_value = session
    driver.close = Mock()
    
    return driver

@pytest.fixture
def mock_records():
    """Provide mock Neo4j records."""
    record1 = Mock()
    record1.__getitem__ = Mock(side_effect=lambda key: {"count": 100}[key])
    record1.get = Mock(side_effect=lambda key, default=None: {"count": 100}.get(key, default))
    
    record2 = Mock()
    record2.__getitem__ = Mock(side_effect=lambda key: {"label": "TestNode"}[key])
    record2.get = Mock(side_effect=lambda key, default=None: {"label": "TestNode"}.get(key, default))
    
    return [record1, record2]

@pytest.fixture
def clean_database_instance():
    """Reset global database instance before each test."""
    global _database_instance
    original_instance = _database_instance
    _database_instance = None
    yield
    _database_instance = original_instance


# =========================================================================
# Unit Tests for Configuration Classes
# =========================================================================

@pytest.mark.unit
class TestDatabaseConfig:
    """Test DatabaseConfig dataclass."""
    
    def test_default_configuration(self):
        """Test default configuration values."""
        config = DatabaseConfig()
        
        assert config.pool_size == 10
        assert config.max_connection_lifetime == 300
        assert config.max_connection_pool_size == 50
        assert config.connection_timeout == 5.0
        assert config.max_retry_attempts == 3
        assert config.health_check_timeout == 5.0
    
    def test_custom_configuration(self):
        """Test custom configuration values."""
        config = DatabaseConfig(
            pool_size=20,
            max_connection_lifetime=600,
            max_connection_pool_size=100,
            connection_timeout=10.0,
            max_retry_attempts=5,
            health_check_timeout=8.0
        )
        
        assert config.pool_size == 20
        assert config.max_connection_lifetime == 600
        assert config.max_connection_pool_size == 100
        assert config.connection_timeout == 10.0
        assert config.max_retry_attempts == 5
        assert config.health_check_timeout == 8.0


@pytest.mark.unit
class TestDatabaseMetrics:
    """Test DatabaseMetrics dataclass."""
    
    def test_default_metrics(self):
        """Test default metrics values."""
        metrics = DatabaseMetrics()
        
        assert metrics.total_queries == 0
        assert metrics.successful_queries == 0
        assert metrics.failed_queries == 0
        assert metrics.average_response_time == 0.0
        assert metrics.total_response_time == 0.0
    
    def test_update_response_time_single(self):
        """Test updating response time with single measurement."""
        metrics = DatabaseMetrics()
        metrics.total_queries = 1
        
        metrics.update_response_time(2.5)
        
        assert metrics.total_response_time == 2.5
        assert metrics.average_response_time == 2.5
    
    def test_update_response_time_multiple(self):
        """Test updating response time with multiple measurements."""
        metrics = DatabaseMetrics()
        metrics.total_queries = 3
        
        metrics.update_response_time(1.0)
        metrics.update_response_time(2.0)
        metrics.update_response_time(3.0)
        
        assert metrics.total_response_time == 6.0
        assert metrics.average_response_time == 2.0
    
    def test_update_response_time_zero_queries(self):
        """Test updating response time with zero queries."""
        metrics = DatabaseMetrics()
        metrics.total_queries = 0
        
        metrics.update_response_time(1.5)
        
        assert metrics.total_response_time == 1.5
        assert metrics.average_response_time == 0.0  # Should remain 0 when no queries


# =========================================================================
# Unit Tests for Exception Classes
# =========================================================================

@pytest.mark.unit
class TestExceptionClasses:
    """Test database exception classes."""
    
    def test_mrca_database_error(self):
        """Test MRCADatabaseError exception."""
        error = MRCADatabaseError("Test database error")
        
        assert str(error) == "Test database error"
        assert isinstance(error, Exception)
    
    def test_database_connection_error(self):
        """Test DatabaseConnectionError exception."""
        error = DatabaseConnectionError("Connection failed")
        
        assert str(error) == "Connection failed"
        assert isinstance(error, MRCADatabaseError)
        assert isinstance(error, Exception)
    
    def test_database_query_error(self):
        """Test DatabaseQueryError exception."""
        error = DatabaseQueryError("Query execution failed")
        
        assert str(error) == "Query execution failed"
        assert isinstance(error, MRCADatabaseError)
        assert isinstance(error, Exception)


# =========================================================================
# Unit Tests for EnhancedNeo4jDatabase Class
# =========================================================================

@pytest.mark.unit
class TestEnhancedNeo4jDatabase:
    """Test EnhancedNeo4jDatabase class functionality."""

    def test_initialization_default_config(self):
        """Test database initialization with default configuration."""
        db = EnhancedNeo4jDatabase()

        assert isinstance(db.config, DatabaseConfig)
        assert isinstance(db.metrics, DatabaseMetrics)
        assert db._driver is None
        assert db._is_connected is False
        assert db.config.pool_size == 10  # Default value

    def test_initialization_custom_config(self, database_config):
        """Test database initialization with custom configuration."""
        db = EnhancedNeo4jDatabase(database_config)

        assert db.config == database_config
        assert db.config.pool_size == 5  # Custom value
        assert db.config.max_retry_attempts == 2  # Custom value

    @patch('backend.database.GraphDatabase.driver')
    def test_create_driver_success(self, mock_graph_database, mock_config, mock_driver):
        """Test successful driver creation."""
        mock_graph_database.return_value = mock_driver

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()
            driver = db._create_driver()

            assert driver == mock_driver
            mock_graph_database.assert_called_once_with(
                "neo4j+s://test.databases.neo4j.io",
                auth=("neo4j", "test-password"),
                max_connection_lifetime=300,
                max_connection_pool_size=50,
                connection_timeout=5.0
            )

    def test_create_driver_missing_uri(self, invalid_config):
        """Test driver creation failure with missing URI."""
        with patch('backend.database.get_config', return_value=invalid_config):
            db = EnhancedNeo4jDatabase()

            with pytest.raises(DatabaseConnectionError) as exc_info:
                db._create_driver()

            assert "Neo4j URI not configured" in str(exc_info.value)

    def test_create_driver_missing_credentials(self):
        """Test driver creation failure with missing credentials."""
        config = Mock()
        config.neo4j_uri = "neo4j+s://test.databases.neo4j.io"
        config.neo4j_username = None
        config.neo4j_password = "password"

        with patch('backend.database.get_config', return_value=config):
            db = EnhancedNeo4jDatabase()

            with pytest.raises(DatabaseConnectionError) as exc_info:
                db._create_driver()

            assert "Neo4j credentials not configured" in str(exc_info.value)

    @patch('backend.database.GraphDatabase.driver')
    def test_connect_success(self, mock_graph_database, mock_config, mock_driver):
        """Test successful database connection."""
        mock_graph_database.return_value = mock_driver

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()
            db.connect()

            assert db._driver == mock_driver
            assert db._is_connected is True

    @patch('backend.database.GraphDatabase.driver')
    def test_connect_failure(self, mock_graph_database, mock_config):
        """Test database connection failure."""
        mock_graph_database.side_effect = Exception("Connection failed")

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()

            with pytest.raises(DatabaseConnectionError):
                db.connect()

            assert db._driver is None
            assert db._is_connected is False

    def test_disconnect_success(self, mock_driver):
        """Test successful database disconnection."""
        db = EnhancedNeo4jDatabase()
        db._driver = mock_driver
        db._is_connected = True

        db.disconnect()

        mock_driver.close.assert_called_once()
        assert db._driver is None
        assert db._is_connected is False

    def test_disconnect_with_error(self, mock_driver):
        """Test database disconnection with error."""
        mock_driver.close.side_effect = Exception("Close error")

        db = EnhancedNeo4jDatabase()
        db._driver = mock_driver
        db._is_connected = True

        # Should not raise exception
        db.disconnect()

        assert db._driver is None
        assert db._is_connected is False

    def test_disconnect_no_driver(self):
        """Test disconnection when no driver exists."""
        db = EnhancedNeo4jDatabase()

        # Should not raise exception
        db.disconnect()

        assert db._driver is None
        assert db._is_connected is False

    def test_get_metrics(self):
        """Test getting database metrics."""
        db = EnhancedNeo4jDatabase()
        db.metrics.total_queries = 10
        db.metrics.successful_queries = 8
        db.metrics.failed_queries = 2
        db.metrics.average_response_time = 1.5

        metrics = db._get_metrics()

        assert metrics["total_queries"] == 10
        assert metrics["successful_queries"] == 8
        assert metrics["failed_queries"] == 2
        assert metrics["average_response_time"] == 1.5
        assert metrics["success_rate"] == 0.8

    @patch('backend.database.GraphDatabase.driver')
    def test_execute_query_success(self, mock_graph_database, mock_config, mock_driver, mock_records):
        """Test successful query execution."""
        mock_graph_database.return_value = mock_driver

        # Mock session and result
        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        result = Mock()
        result.__iter__ = Mock(return_value=iter(mock_records))
        session.run.return_value = result

        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()

            records = db.execute_query("MATCH (n) RETURN count(n)")

            assert len(records) == 2
            assert db.metrics.total_queries == 1
            assert db.metrics.successful_queries == 1
            assert db.metrics.failed_queries == 0
            assert db.metrics.average_response_time > 0

    @patch('backend.database.GraphDatabase.driver')
    def test_execute_query_with_parameters(self, mock_graph_database, mock_config, mock_driver):
        """Test query execution with parameters."""
        mock_graph_database.return_value = mock_driver

        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        result = Mock()
        result.__iter__ = Mock(return_value=iter([]))
        session.run.return_value = result

        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()

            parameters = {"name": "test"}
            db.execute_query("MATCH (n {name: $name}) RETURN n", parameters)

            session.run.assert_called_once()
            call_args = session.run.call_args
            assert call_args[0][1] == parameters  # Check parameters were passed as second positional argument

    @patch('backend.database.GraphDatabase.driver')
    def test_execute_query_auto_connect(self, mock_graph_database, mock_config, mock_driver):
        """Test query execution with automatic connection."""
        mock_graph_database.return_value = mock_driver

        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        result = Mock()
        result.__iter__ = Mock(return_value=iter([]))
        session.run.return_value = result

        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()
            # Don't call connect() explicitly

            db.execute_query("MATCH (n) RETURN count(n)")

            # Should have auto-connected
            assert db._driver == mock_driver
            assert db._is_connected is True

    def test_execute_query_connection_failure(self, database_config):
        """Test query execution with connection failure."""
        db = EnhancedNeo4jDatabase(database_config)

        with patch.object(db, 'connect', side_effect=DatabaseConnectionError("Connection failed")):
            with pytest.raises(DatabaseQueryError):
                db.execute_query("MATCH (n) RETURN count(n)")

            assert db.metrics.failed_queries == 1

    @patch('backend.database.GraphDatabase.driver')
    def test_execute_query_with_retry_success(self, mock_graph_database, mock_config, mock_driver, database_config):
        """Test query execution with retry logic success."""
        from neo4j.exceptions import ServiceUnavailable

        mock_graph_database.return_value = mock_driver

        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        # First call fails, second succeeds
        result = Mock()
        result.__iter__ = Mock(return_value=iter([]))
        session.run.side_effect = [ServiceUnavailable("Service down"), result]

        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            with patch('time.sleep'):  # Mock sleep to speed up test
                db = EnhancedNeo4jDatabase(database_config)

                records = db.execute_query("MATCH (n) RETURN count(n)")

                assert len(records) == 0
                assert db.metrics.total_queries == 1
                assert db.metrics.successful_queries == 1
                assert session.run.call_count == 2  # One retry

    @patch('backend.database.GraphDatabase.driver')
    def test_execute_query_retry_exhausted(self, mock_graph_database, mock_config, mock_driver, database_config):
        """Test query execution with retry exhaustion."""
        from neo4j.exceptions import ServiceUnavailable

        mock_graph_database.return_value = mock_driver

        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        # Always fail
        session.run.side_effect = ServiceUnavailable("Service down")
        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            with patch('time.sleep'):  # Mock sleep to speed up test
                db = EnhancedNeo4jDatabase(database_config)

                with pytest.raises(DatabaseQueryError) as exc_info:
                    db.execute_query("MATCH (n) RETURN count(n)")

                assert "Query failed after retries" in str(exc_info.value)
                assert db.metrics.failed_queries == 1
                assert session.run.call_count == 2  # max_retry_attempts = 2

    @patch('backend.database.GraphDatabase.driver')
    def test_execute_query_non_transient_error(self, mock_graph_database, mock_config, mock_driver):
        """Test query execution with non-transient error."""
        mock_graph_database.return_value = mock_driver

        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        # Non-transient error should not retry
        session.run.side_effect = Exception("Syntax error")
        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()

            with pytest.raises(DatabaseQueryError) as exc_info:
                db.execute_query("INVALID QUERY")

            assert "Query failed: Syntax error" in str(exc_info.value)
            assert db.metrics.failed_queries == 1
            assert session.run.call_count == 1  # No retry for non-transient errors

    @patch('backend.database.GraphDatabase.driver')
    def test_health_check_success(self, mock_graph_database, mock_config, mock_driver):
        """Test successful health check."""
        mock_graph_database.return_value = mock_driver

        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        # Mock the record returned by result.single()
        mock_record = Mock()
        mock_record.__getitem__ = Mock(return_value=1)  # record["health_check"] returns 1

        result = Mock()
        result.single.return_value = mock_record
        session.run.return_value = result

        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()

            health = db.health_check()

            assert health["database"] == "healthy"
            assert health["connection"] == "active"
            assert "response_time" in health
            assert "metrics" in health

    def test_health_check_failure(self):
        """Test health check with connection failure."""
        db = EnhancedNeo4jDatabase()

        # Mock the driver to raise an exception when creating a session
        with patch.object(db, '_driver') as mock_driver:
            mock_driver.session.side_effect = Exception("Connection failed")

            health = db.health_check()

            assert health["database"] == "unhealthy"
            assert health["connection"] == "failed"
            assert "error" in health


# =========================================================================
# Unit Tests for Factory Functions
# =========================================================================

@pytest.mark.unit
class TestFactoryFunctions:
    """Test database factory functions."""

    def test_get_database_singleton(self, clean_database_instance):
        """Test that get_database implements singleton pattern."""
        db1 = get_database()
        db2 = get_database()

        assert db1 is db2
        assert isinstance(db1, EnhancedNeo4jDatabase)

    def test_get_database_thread_safety(self, clean_database_instance):
        """Test thread safety of get_database."""
        instances = []

        def create_database():
            instances.append(get_database())

        threads = [Thread(target=create_database) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All instances should be the same
        assert len(set(id(instance) for instance in instances)) == 1

    @patch('backend.database.get_database')
    def test_get_graph_wrapper(self, mock_get_database):
        """Test get_graph wrapper functionality."""
        mock_db = Mock()
        mock_db.execute_query.return_value = [Mock()]
        mock_get_database.return_value = mock_db

        graph = get_graph()

        # Test query method
        result = graph.query("MATCH (n) RETURN count(n)")
        mock_db.execute_query.assert_called_once_with("MATCH (n) RETURN count(n)", None)

        # Test query with parameters
        graph.query("MATCH (n {name: $name}) RETURN n", {"name": "test"})
        mock_db.execute_query.assert_called_with("MATCH (n {name: $name}) RETURN n", {"name": "test"})

    @patch('backend.database.get_database')
    def test_get_graph_schema_success(self, mock_get_database):
        """Test get_graph schema retrieval success."""
        mock_db = Mock()

        # Mock labels query
        labels_record = Mock()
        labels_record.__getitem__ = Mock(return_value="TestNode")

        # Mock relationship types query
        rel_types_record = Mock()
        rel_types_record.__getitem__ = Mock(return_value="TEST_RELATIONSHIP")

        mock_db.execute_query.side_effect = [
            [labels_record],  # Labels query
            [rel_types_record]  # Relationship types query
        ]

        mock_get_database.return_value = mock_db

        graph = get_graph()
        schema = graph.get_schema()

        assert "Node Labels:" in schema
        assert "Relationship Types:" in schema
        assert mock_db.execute_query.call_count == 2

    @patch('backend.database.get_database')
    def test_get_graph_schema_failure(self, mock_get_database):
        """Test get_graph schema retrieval failure."""
        mock_db = Mock()
        mock_db.execute_query.side_effect = Exception("Schema query failed")
        mock_get_database.return_value = mock_db

        graph = get_graph()
        schema = graph.get_schema()

        assert schema == "Schema information unavailable"

    @patch('backend.database.get_database')
    def test_database_health_check_function(self, mock_get_database):
        """Test standalone database_health_check function."""
        mock_db = Mock()
        mock_health = {"database": "healthy", "connected": True}
        mock_db.health_check.return_value = mock_health
        mock_get_database.return_value = mock_db

        health = database_health_check()

        assert health == mock_health
        mock_db.health_check.assert_called_once()

    def test_reset_database_connection(self, clean_database_instance):
        """Test reset_database_connection function."""
        # Set up a mock database instance in the global variable
        mock_db = Mock()

        # Directly set the global instance (not using patch context manager)
        import backend.database
        backend.database._database_instance = mock_db

        # Call reset function
        reset_database_connection()

        # Verify disconnect was called
        mock_db.disconnect.assert_called_once()

        # After reset, global instance should be None
        assert backend.database._database_instance is None


# =========================================================================
# Unit Tests for Edge Cases and Integration
# =========================================================================

@pytest.mark.unit
class TestEdgeCasesAndIntegration:
    """Test edge cases and integration scenarios."""

    def test_metrics_calculation_edge_cases(self):
        """Test metrics calculation with edge cases."""
        # Test division by zero protection
        metrics = DatabaseMetrics()
        metrics.total_queries = 0
        metrics.update_response_time(1.0)
        assert metrics.average_response_time == 0.0

        # Test with single query (reset metrics first)
        metrics = DatabaseMetrics()
        metrics.total_queries = 1
        metrics.update_response_time(2.0)
        assert metrics.average_response_time == 2.0

    def test_database_config_immutability(self):
        """Test that database config behaves as expected."""
        config1 = DatabaseConfig()
        config2 = DatabaseConfig(pool_size=20)

        # Original should not be affected
        assert config1.pool_size == 10
        assert config2.pool_size == 20

    @patch('backend.database.GraphDatabase.driver')
    def test_concurrent_query_execution(self, mock_graph_database, mock_config, mock_driver):
        """Test concurrent query execution."""
        mock_graph_database.return_value = mock_driver

        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        result = Mock()
        result.__iter__ = Mock(return_value=iter([]))
        session.run.return_value = result

        mock_driver.session.return_value = session

        with patch('backend.database.get_config', return_value=mock_config):
            db = EnhancedNeo4jDatabase()

            results = []

            def execute_query():
                try:
                    result = db.execute_query("MATCH (n) RETURN count(n)")
                    results.append(result)
                except Exception as e:
                    results.append(e)

            threads = [Thread(target=execute_query) for _ in range(3)]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            # All queries should succeed
            assert len(results) == 3
            assert all(isinstance(result, list) for result in results)
            assert db.metrics.total_queries == 3
            assert db.metrics.successful_queries == 3
