# -------------------------------------------------------------------------
# File: test_graph.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-28
# File Path: tests/unit/test_graph.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the graph module (backend/graph.py).
# Tests Neo4j graph database connectivity, lazy loading patterns,
# configuration validation, and legacy compatibility functions.
# Ensures proper graph operations and error handling.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Graph Unit Tests

Comprehensive testing of the graph functionality:
- Neo4j configuration validation
- Graph instance creation and lazy loading
- Connection testing and health checks
- LazyGraph wrapper functionality
- Schema retrieval operations
- Error handling and resilience
- Legacy compatibility support
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

# Import graph components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.graph import (
    validate_neo4j_config, get_graph, get_graph_schema,
    test_connection, LazyGraph, graph
)


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def mock_config():
    """Provide mock configuration for Neo4j."""
    with patch('backend.graph.init_config') as mock_init_config:
        mock_config_instance = Mock()
        mock_config_instance.neo4j_uri = "bolt://localhost:7687"
        mock_config_instance.neo4j_username = "neo4j"
        mock_config_instance.neo4j_password = "test-password"
        mock_init_config.return_value = mock_config_instance
        yield mock_config_instance

@pytest.fixture
def invalid_config():
    """Provide invalid configuration for Neo4j."""
    with patch('backend.graph.init_config') as mock_init_config:
        mock_config_instance = Mock()
        mock_config_instance.neo4j_uri = None
        mock_config_instance.neo4j_username = None
        mock_config_instance.neo4j_password = None
        mock_init_config.return_value = mock_config_instance
        yield mock_config_instance

@pytest.fixture
def mock_neo4j_graph():
    """Provide mock Neo4jGraph instance."""
    with patch('backend.graph.Neo4jGraph') as mock_neo4j_graph_class:
        mock_graph_instance = Mock()
        mock_graph_instance.query.return_value = [{"test": 1}]
        mock_graph_instance.get_schema = "Mock graph schema"
        mock_neo4j_graph_class.return_value = mock_graph_instance
        yield mock_graph_instance

@pytest.fixture
def sample_query_result():
    """Provide sample query result for testing."""
    return [
        {"node_count": 100},
        {"relationship_count": 250}
    ]


# =========================================================================
# Unit Tests for Configuration Validation
# =========================================================================

@pytest.mark.unit
class TestConfigurationValidation:
    """Test Neo4j configuration validation functionality."""
    
    def test_validate_neo4j_config_success(self, mock_config):
        """Test successful Neo4j configuration validation."""
        uri, username, password = validate_neo4j_config()
        
        assert uri == "bolt://localhost:7687"
        assert username == "neo4j"
        assert password == "test-password"
    
    def test_validate_neo4j_config_missing_uri(self, invalid_config):
        """Test configuration validation with missing URI."""
        with pytest.raises(ValueError) as exc_info:
            validate_neo4j_config()
        
        assert "Missing Neo4j configuration" in str(exc_info.value)
    
    def test_validate_neo4j_config_partial_missing(self):
        """Test configuration validation with partially missing values."""
        with patch('backend.graph.init_config') as mock_init_config:
            mock_config_instance = Mock()
            mock_config_instance.neo4j_uri = "bolt://localhost:7687"
            mock_config_instance.neo4j_username = "neo4j"
            mock_config_instance.neo4j_password = None  # Missing password
            mock_init_config.return_value = mock_config_instance
            
            with pytest.raises(ValueError) as exc_info:
                validate_neo4j_config()
            
            assert "Missing Neo4j configuration" in str(exc_info.value)
    
    def test_validate_neo4j_config_empty_strings(self):
        """Test configuration validation with empty string values."""
        with patch('backend.graph.init_config') as mock_init_config:
            mock_config_instance = Mock()
            mock_config_instance.neo4j_uri = ""
            mock_config_instance.neo4j_username = "neo4j"
            mock_config_instance.neo4j_password = "password"
            mock_init_config.return_value = mock_config_instance
            
            with pytest.raises(ValueError) as exc_info:
                validate_neo4j_config()
            
            assert "Missing Neo4j configuration" in str(exc_info.value)


# =========================================================================
# Unit Tests for Graph Factory Functions
# =========================================================================

@pytest.mark.unit
class TestGraphFactoryFunctions:
    """Test graph factory functions."""
    
    def test_get_graph_success(self, mock_config, mock_neo4j_graph):
        """Test successful graph instance creation."""
        graph_instance = get_graph()
        
        assert graph_instance is not None
        assert graph_instance == mock_neo4j_graph
    
    def test_get_graph_configuration_error(self, invalid_config):
        """Test graph creation with configuration error."""
        with pytest.raises(ValueError):
            get_graph()
    
    def test_get_graph_connection_error(self, mock_config):
        """Test graph creation with connection error."""
        with patch('backend.graph.Neo4jGraph', side_effect=Exception("Connection failed")):
            with pytest.raises(Exception) as exc_info:
                get_graph()
            
            assert "Connection failed" in str(exc_info.value)
    
    def test_get_graph_schema_success(self, mock_config, mock_neo4j_graph):
        """Test successful schema retrieval."""
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            schema = get_graph_schema()
            
            assert schema == "Mock graph schema"
    
    def test_get_graph_schema_error(self):
        """Test schema retrieval with error."""
        with patch('backend.graph.get_graph', side_effect=Exception("Schema error")):
            schema = get_graph_schema()
            
            assert "Error getting schema" in schema
            assert "Schema error" in schema
    
    def test_test_connection_success(self, mock_config, mock_neo4j_graph, sample_query_result):
        """Test successful connection test."""
        # Mock the global graph instance
        with patch('backend.graph.graph') as mock_global_graph:
            mock_global_graph.query.return_value = sample_query_result
            
            success, message = test_connection()
            
            assert success is True
            assert "Connection successful" in message
            mock_global_graph.query.assert_called_once_with("RETURN 1 as test")
    
    def test_test_connection_failure(self):
        """Test connection test failure."""
        with patch('backend.graph.graph') as mock_global_graph:
            mock_global_graph.query.side_effect = Exception("Connection failed")
            
            success, message = test_connection()
            
            assert success is False
            assert "Connection failed" in message


# =========================================================================
# Unit Tests for LazyGraph Class
# =========================================================================

@pytest.mark.unit
class TestLazyGraph:
    """Test LazyGraph class functionality."""
    
    def test_lazy_graph_initialization(self):
        """Test LazyGraph initialization."""
        lazy_graph = LazyGraph()
        
        assert lazy_graph._graph is None
    
    def test_lazy_graph_get_graph_creation(self, mock_config, mock_neo4j_graph):
        """Test lazy graph creation on first access."""
        lazy_graph = LazyGraph()
        
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            graph_instance = lazy_graph._get_graph()
            
            assert graph_instance == mock_neo4j_graph
            assert lazy_graph._graph == mock_neo4j_graph
    
    def test_lazy_graph_cached_instance(self, mock_config, mock_neo4j_graph):
        """Test that graph instance is cached after first creation."""
        lazy_graph = LazyGraph()
        
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph) as mock_get_graph:
            # First access
            graph_instance1 = lazy_graph._get_graph()
            # Second access
            graph_instance2 = lazy_graph._get_graph()
            
            assert graph_instance1 == graph_instance2
            assert graph_instance1 == mock_neo4j_graph
            # get_graph should only be called once due to caching
            mock_get_graph.assert_called_once()
    
    def test_lazy_graph_getattr_delegation(self, mock_config, mock_neo4j_graph):
        """Test attribute delegation to underlying graph."""
        lazy_graph = LazyGraph()
        
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            # Access an attribute that should be delegated
            schema = lazy_graph.get_schema
            
            assert schema == mock_neo4j_graph.get_schema
    
    def test_lazy_graph_query_method(self, mock_config, mock_neo4j_graph, sample_query_result):
        """Test explicit query method."""
        lazy_graph = LazyGraph()
        mock_neo4j_graph.query.return_value = sample_query_result
        
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            result = lazy_graph.query("MATCH (n) RETURN count(n)")
            
            assert result == sample_query_result
            mock_neo4j_graph.query.assert_called_once_with("MATCH (n) RETURN count(n)")
    
    def test_lazy_graph_query_with_parameters(self, mock_config, mock_neo4j_graph, sample_query_result):
        """Test query method with parameters."""
        lazy_graph = LazyGraph()
        mock_neo4j_graph.query.return_value = sample_query_result
        
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            result = lazy_graph.query("MATCH (n {name: $name}) RETURN n", {"name": "test"})
            
            assert result == sample_query_result
            mock_neo4j_graph.query.assert_called_once_with("MATCH (n {name: $name}) RETURN n", {"name": "test"})
    
    def test_lazy_graph_error_handling(self, invalid_config):
        """Test LazyGraph error handling."""
        lazy_graph = LazyGraph()
        
        with pytest.raises(ValueError):
            lazy_graph._get_graph()
    
    def test_lazy_graph_method_chaining(self, mock_config, mock_neo4j_graph):
        """Test method chaining through attribute delegation."""
        lazy_graph = LazyGraph()
        
        # Mock a method that returns something that can be chained
        mock_result = Mock()
        mock_result.some_method.return_value = "chained result"
        mock_neo4j_graph.some_operation.return_value = mock_result
        
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            result = lazy_graph.some_operation().some_method()
            
            assert result == "chained result"


# =========================================================================
# Unit Tests for Global Graph Instance
# =========================================================================

@pytest.mark.unit
class TestGlobalGraphInstance:
    """Test global graph instance functionality."""

    def test_global_graph_is_lazy_graph(self):
        """Test that global graph is a LazyGraph instance."""
        assert isinstance(graph, LazyGraph)

    def test_global_graph_query_delegation(self, mock_config, mock_neo4j_graph, sample_query_result):
        """Test that global graph delegates queries correctly."""
        mock_neo4j_graph.query.return_value = sample_query_result

        # Reset the cached graph instance to ensure fresh mocking
        graph._graph = None

        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            result = graph.query("MATCH (n) RETURN count(n)")

            assert result == sample_query_result
            mock_neo4j_graph.query.assert_called_once_with("MATCH (n) RETURN count(n)")

    def test_global_graph_attribute_access(self, mock_config, mock_neo4j_graph):
        """Test global graph attribute access."""
        # Reset the cached graph instance to ensure fresh mocking
        graph._graph = None

        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            schema = graph.get_schema

            assert schema == mock_neo4j_graph.get_schema

    def test_global_graph_backwards_compatibility(self, mock_config, mock_neo4j_graph, sample_query_result):
        """Test backwards compatibility of global graph instance."""
        mock_neo4j_graph.query.return_value = sample_query_result

        # Reset the cached graph instance to ensure fresh mocking
        graph._graph = None

        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            # Test that existing code patterns still work
            result = graph.query("RETURN 1 as test")

            assert result == sample_query_result


# =========================================================================
# Unit Tests for Edge Cases and Integration
# =========================================================================

@pytest.mark.unit
class TestEdgeCasesAndIntegration:
    """Test edge cases and integration scenarios."""

    def test_multiple_graph_instances(self, mock_config, mock_neo4j_graph):
        """Test creating multiple graph instances."""
        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            graph1 = get_graph()
            graph2 = get_graph()

            # Each call should return a new instance
            assert graph1 == mock_neo4j_graph
            assert graph2 == mock_neo4j_graph

    def test_lazy_graph_multiple_instances(self, mock_config, mock_neo4j_graph):
        """Test multiple LazyGraph instances."""
        lazy_graph1 = LazyGraph()
        lazy_graph2 = LazyGraph()

        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            result1 = lazy_graph1.query("MATCH (n) RETURN count(n)")
            result2 = lazy_graph2.query("MATCH (n) RETURN count(n)")

            # Both should work independently
            assert lazy_graph1._graph == mock_neo4j_graph
            assert lazy_graph2._graph == mock_neo4j_graph

    def test_configuration_changes_after_initialization(self, mock_config, mock_neo4j_graph):
        """Test behavior when configuration changes after initialization."""
        lazy_graph = LazyGraph()

        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            # First access
            lazy_graph.query("MATCH (n) RETURN count(n)")

            # Change configuration (simulate config reload)
            mock_config.neo4j_uri = "bolt://new-host:7687"

            # Second access should still use cached instance
            lazy_graph.query("MATCH (n) RETURN count(n)")

            # The cached instance should still be used
            assert lazy_graph._graph == mock_neo4j_graph

    def test_concurrent_lazy_graph_access(self, mock_config, mock_neo4j_graph):
        """Test concurrent access to LazyGraph."""
        import threading

        lazy_graph = LazyGraph()
        results = []

        def access_graph():
            with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
                try:
                    result = lazy_graph.query("MATCH (n) RETURN count(n)")
                    results.append(("success", result))
                except Exception as e:
                    results.append(("error", str(e)))

        threads = [threading.Thread(target=access_graph) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All accesses should succeed
        assert len(results) == 5
        assert all(result[0] == "success" for result in results)

    def test_error_propagation_through_lazy_graph(self, mock_config):
        """Test that errors are properly propagated through LazyGraph."""
        lazy_graph = LazyGraph()

        with patch('backend.graph.get_graph', side_effect=Exception("Connection error")):
            with pytest.raises(Exception) as exc_info:
                lazy_graph.query("MATCH (n) RETURN count(n)")

            assert "Connection error" in str(exc_info.value)

    def test_query_with_complex_parameters(self, mock_config, mock_neo4j_graph):
        """Test query execution with complex parameters."""
        lazy_graph = LazyGraph()
        complex_params = {
            "name": "test",
            "properties": {"type": "regulation", "section": "30.1"},
            "limit": 10
        }

        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
            lazy_graph.query("MATCH (n {name: $name}) RETURN n LIMIT $limit", complex_params)

            mock_neo4j_graph.query.assert_called_once_with(
                "MATCH (n {name: $name}) RETURN n LIMIT $limit",
                complex_params
            )

    def test_schema_retrieval_with_different_formats(self, mock_config, mock_neo4j_graph):
        """Test schema retrieval with different schema formats."""
        schema_formats = [
            "Simple schema string",
            {"nodes": ["Regulation", "Equipment"], "relationships": ["REQUIRES"]},
            None,
            ""
        ]

        for schema_format in schema_formats:
            mock_neo4j_graph.get_schema = schema_format

            with patch('backend.graph.get_graph', return_value=mock_neo4j_graph):
                result = get_graph_schema()

                assert result == schema_format

    def test_connection_test_with_different_query_results(self, mock_config):
        """Test connection test with different query result formats."""
        test_results = [
            [{"test": 1}],
            [],
            [{"test": 1}, {"test": 2}],
            None
        ]

        for test_result in test_results:
            with patch('backend.graph.graph') as mock_global_graph:
                mock_global_graph.query.return_value = test_result

                success, message = test_connection()

                assert success is True
                assert "Connection successful" in message

    def test_validate_config_with_whitespace_values(self):
        """Test configuration validation with whitespace-only values."""
        with patch('backend.graph.init_config') as mock_init_config:
            mock_config_instance = Mock()
            mock_config_instance.neo4j_uri = "   "  # Whitespace only
            mock_config_instance.neo4j_username = "neo4j"
            mock_config_instance.neo4j_password = "password"
            mock_init_config.return_value = mock_config_instance

            # Should treat whitespace as valid (current implementation)
            uri, username, password = validate_neo4j_config()
            assert uri == "   "
            assert username == "neo4j"
            assert password == "password"

    def test_lazy_graph_memory_efficiency(self, mock_config, mock_neo4j_graph):
        """Test that LazyGraph doesn't create unnecessary instances."""
        lazy_graph = LazyGraph()

        with patch('backend.graph.get_graph', return_value=mock_neo4j_graph) as mock_get_graph:
            # Multiple attribute accesses
            lazy_graph.get_schema
            lazy_graph.query("MATCH (n) RETURN count(n)")
            lazy_graph.get_schema  # Access again

            # get_graph should only be called once
            mock_get_graph.assert_called_once()

    def test_error_handling_in_different_scenarios(self):
        """Test error handling in various failure scenarios."""
        error_scenarios = [
            (ConnectionError("Network error"), "Network error"),
            (TimeoutError("Timeout"), "Timeout"),
            (ValueError("Invalid config"), "Invalid config"),
            (RuntimeError("Runtime error"), "Runtime error")
        ]

        for error, expected_message in error_scenarios:
            with patch('backend.graph.init_config', side_effect=error):
                with pytest.raises(type(error)) as exc_info:
                    validate_neo4j_config()

                assert expected_message in str(exc_info.value)
