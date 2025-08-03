# -------------------------------------------------------------------------
# File: test_parallel_hybrid.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-28
# File Path: tests/unit/test_parallel_hybrid.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Unit tests for the parallel hybrid retrieval module (backend/parallel_hybrid.py).
# Tests ParallelRetrievalEngine class, async execution, performance monitoring,
# confidence scoring, and factory functions. Ensures proper parallel execution
# of VectorRAG and GraphRAG with comprehensive error handling.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Parallel Hybrid Retrieval Unit Tests

Comprehensive testing of the Advanced Parallel Hybrid functionality:
- Parallel execution of VectorRAG and GraphRAG
- Async task management and timeout handling
- Confidence scoring and result evaluation
- Error handling and resilience features
- Performance monitoring and metrics
- Factory functions and singleton pattern
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor

# Import parallel hybrid components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.parallel_hybrid import (
    RetrievalResult, ParallelRetrievalResponse, ParallelRetrievalEngine,
    get_parallel_engine, validate_parallel_retrieval, _parallel_engine
)


# =========================================================================
# Test Fixtures
# =========================================================================

@pytest.fixture
def mock_vector_result():
    """Provide mock vector retrieval result."""
    return "CFR § 30.1 requires safety equipment including hard hats, safety glasses, and protective clothing for all mining operations. Compliance with these requirements is mandatory for underground and surface mining activities."

@pytest.fixture
def mock_graph_result():
    """Provide mock graph retrieval result."""
    return "Based on MSHA regulations, mining operations must maintain specific safety equipment standards. The requirements include personal protective equipment, emergency response equipment, and regular safety inspections."

@pytest.fixture
def mock_vector_tool():
    """Provide mock vector tool functions."""
    with patch('backend.parallel_hybrid.search_regulations_semantic') as mock_search:
        with patch('backend.parallel_hybrid.check_vector_tool_health') as mock_health:
            mock_search.return_value = "Mock vector search result"
            mock_health.return_value = {"status": "healthy"}
            yield mock_search, mock_health

@pytest.fixture
def mock_graph_tool():
    """Provide mock graph tool functions."""
    with patch('backend.parallel_hybrid.query_regulations') as mock_query:
        with patch('backend.parallel_hybrid.check_cypher_tool_health') as mock_health:
            mock_query.return_value = "Mock graph query result"
            mock_health.return_value = {"status": "healthy"}
            yield mock_query, mock_health

@pytest.fixture
def mock_llm():
    """Provide mock LLM for query enhancement."""
    with patch('backend.parallel_hybrid.get_llm') as mock_get_llm:
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.return_value = Mock(content="Enhanced query for MSHA regulations")
        mock_get_llm.return_value = mock_llm_instance
        yield mock_llm_instance

@pytest.fixture
def clean_parallel_engine():
    """Reset global parallel engine instance before each test."""
    global _parallel_engine
    original_engine = _parallel_engine
    _parallel_engine = None
    yield
    _parallel_engine = original_engine

@pytest.fixture
def sample_retrieval_result():
    """Provide sample RetrievalResult for testing."""
    return RetrievalResult(
        content="Sample regulatory content",
        method="vector_rag",
        confidence=0.8,
        response_time_ms=150,
        metadata={"source": "test"}
    )


# =========================================================================
# Unit Tests for Data Classes
# =========================================================================

@pytest.mark.unit
class TestDataClasses:
    """Test data classes for parallel retrieval."""
    
    def test_retrieval_result_creation(self):
        """Test RetrievalResult creation and attributes."""
        result = RetrievalResult(
            content="Test content",
            method="vector_rag",
            confidence=0.75,
            response_time_ms=200,
            error=None,
            metadata={"test": "data"}
        )
        
        assert result.content == "Test content"
        assert result.method == "vector_rag"
        assert result.confidence == 0.75
        assert result.response_time_ms == 200
        assert result.error is None
        assert result.metadata == {"test": "data"}
    
    def test_retrieval_result_with_error(self):
        """Test RetrievalResult with error information."""
        result = RetrievalResult(
            content="Error occurred",
            method="graph_rag",
            confidence=0.0,
            response_time_ms=50,
            error="Connection timeout"
        )
        
        assert result.error == "Connection timeout"
        assert result.confidence == 0.0
    
    def test_parallel_retrieval_response_creation(self, sample_retrieval_result):
        """Test ParallelRetrievalResponse creation."""
        vector_result = sample_retrieval_result
        graph_result = RetrievalResult(
            content="Graph content",
            method="graph_rag",
            confidence=0.6,
            response_time_ms=300
        )
        
        response = ParallelRetrievalResponse(
            vector_result=vector_result,
            graph_result=graph_result,
            query="Test query",
            total_time_ms=500,
            success=True,
            fusion_ready=True
        )
        
        assert response.vector_result == vector_result
        assert response.graph_result == graph_result
        assert response.query == "Test query"
        assert response.total_time_ms == 500
        assert response.success is True
        assert response.fusion_ready is True


# =========================================================================
# Unit Tests for ParallelRetrievalEngine Class
# =========================================================================

@pytest.mark.unit
class TestParallelRetrievalEngine:
    """Test ParallelRetrievalEngine class functionality."""
    
    def test_initialization_default(self):
        """Test engine initialization with default parameters."""
        engine = ParallelRetrievalEngine()
        
        assert engine.timeout_seconds == 30
        assert isinstance(engine.executor, ThreadPoolExecutor)
        assert engine.executor._max_workers == 4
    
    def test_initialization_custom_timeout(self):
        """Test engine initialization with custom timeout."""
        engine = ParallelRetrievalEngine(timeout_seconds=60)
        
        assert engine.timeout_seconds == 60
    
    def test_calculate_vector_confidence_high_quality(self):
        """Test vector confidence calculation for high-quality results."""
        engine = ParallelRetrievalEngine()
        
        high_quality_result = "CFR § 30.1 requires safety equipment including hard hats and safety glasses. Mining operations must maintain compliance with these requirements for underground and surface activities."
        
        confidence = engine._calculate_vector_confidence(high_quality_result)
        
        assert confidence > 0.8  # Should be high confidence
        assert confidence <= 1.0
    
    def test_calculate_vector_confidence_low_quality(self):
        """Test vector confidence calculation for low-quality results."""
        engine = ParallelRetrievalEngine()
        
        low_quality_result = "Error: No results found"
        
        confidence = engine._calculate_vector_confidence(low_quality_result)
        
        assert confidence == 0.0
    
    def test_calculate_vector_confidence_medium_quality(self):
        """Test vector confidence calculation for medium-quality results."""
        engine = ParallelRetrievalEngine()
        
        medium_quality_result = "Mining safety requirements include protective equipment and regular inspections."
        
        confidence = engine._calculate_vector_confidence(medium_quality_result)
        
        assert 0.4 < confidence < 0.8
    
    def test_calculate_graph_confidence_high_quality(self):
        """Test graph confidence calculation for high-quality results."""
        engine = ParallelRetrievalEngine()

        high_quality_result = "Based on MSHA regulations, mining operations must maintain specific safety equipment standards including personal protective equipment."

        confidence = engine._calculate_graph_confidence(high_quality_result)

        assert confidence >= 0.5  # Base confidence for valid content
        assert confidence <= 1.0
    
    def test_calculate_graph_confidence_unknown_response(self):
        """Test graph confidence calculation for 'I don't know' responses."""
        engine = ParallelRetrievalEngine()
        
        unknown_result = "I don't know about that specific regulation."
        
        confidence = engine._calculate_graph_confidence(unknown_result)
        
        assert confidence == 0.0
    
    def test_enhance_query_for_graph(self, mock_llm):
        """Test query enhancement for graph retrieval."""
        engine = ParallelRetrievalEngine()
        
        original_query = "safety equipment"
        enhanced_query = engine._enhance_query_for_graph(original_query)
        
        assert "MSHA" in enhanced_query or "mining" in enhanced_query.lower()
        assert len(enhanced_query) > len(original_query)
    
    def test_enhance_query_for_graph_error_handling(self):
        """Test query enhancement error handling."""
        engine = ParallelRetrievalEngine()
        
        with patch('backend.parallel_hybrid.get_llm', side_effect=Exception("LLM error")):
            original_query = "safety equipment"
            enhanced_query = engine._enhance_query_for_graph(original_query)
            
            # Should fall back to original query with MSHA context
            assert "safety equipment" in enhanced_query
            assert "MSHA" in enhanced_query

    @pytest.mark.asyncio
    async def test_async_vector_retrieve_success(self, mock_vector_tool, mock_vector_result):
        """Test successful async vector retrieval."""
        mock_search, mock_health = mock_vector_tool
        mock_search.return_value = mock_vector_result

        engine = ParallelRetrievalEngine()

        result = await engine._async_vector_retrieve("safety equipment")

        assert result.method == "vector_rag"
        assert result.error is None
        assert result.confidence > 0.0
        assert result.response_time_ms >= 0  # Can be 0 for mocked functions
        assert mock_vector_result in result.content
        mock_search.assert_called_once_with("safety equipment")

    @pytest.mark.asyncio
    async def test_async_vector_retrieve_error(self, mock_vector_tool):
        """Test async vector retrieval with error."""
        mock_search, mock_health = mock_vector_tool
        mock_search.side_effect = Exception("Vector search failed")

        engine = ParallelRetrievalEngine()

        result = await engine._async_vector_retrieve("safety equipment")

        assert result.method == "vector_rag"
        assert result.error == "Vector search failed"
        assert result.confidence == 0.0
        assert "Vector retrieval failed" in result.content

    @pytest.mark.asyncio
    async def test_async_graph_retrieve_success(self, mock_graph_tool, mock_graph_result):
        """Test successful async graph retrieval."""
        mock_query, mock_health = mock_graph_tool
        mock_query.return_value = mock_graph_result

        engine = ParallelRetrievalEngine()

        with patch.object(engine, '_enhance_query_for_graph', return_value="enhanced query"):
            result = await engine._async_graph_retrieve("safety equipment")

        assert result.method == "graph_rag"
        assert result.error is None
        assert result.confidence > 0.0
        assert result.response_time_ms >= 0  # Can be 0 for mocked functions
        assert mock_graph_result in result.content
        mock_query.assert_called_once_with("enhanced query")

    @pytest.mark.asyncio
    async def test_async_graph_retrieve_with_alternatives(self, mock_graph_tool):
        """Test async graph retrieval with alternative queries."""
        mock_query, mock_health = mock_graph_tool
        mock_query.return_value = "I don't know"

        engine = ParallelRetrievalEngine()

        with patch.object(engine, '_enhance_query_for_graph', return_value="enhanced query"):
            with patch.object(engine, '_try_alternative_graph_queries', return_value="Alternative result"):
                result = await engine._async_graph_retrieve("safety equipment")

        assert result.method == "graph_rag"
        assert result.error is None
        assert "Alternative result" in result.content

    @pytest.mark.asyncio
    async def test_async_graph_retrieve_error(self, mock_graph_tool):
        """Test async graph retrieval with error."""
        mock_query, mock_health = mock_graph_tool
        mock_query.side_effect = Exception("Graph query failed")

        engine = ParallelRetrievalEngine()

        with patch.object(engine, '_enhance_query_for_graph', return_value="enhanced query"):
            result = await engine._async_graph_retrieve("safety equipment")

        assert result.method == "graph_rag"
        assert result.error == "Graph query failed"
        assert result.confidence == 0.0
        assert "Graph retrieval failed" in result.content

    @pytest.mark.asyncio
    async def test_retrieve_parallel_success(self, mock_vector_tool, mock_graph_tool, mock_vector_result, mock_graph_result):
        """Test successful parallel retrieval."""
        mock_vector_search, _ = mock_vector_tool
        mock_graph_query, _ = mock_graph_tool

        mock_vector_search.return_value = mock_vector_result
        mock_graph_query.return_value = mock_graph_result

        engine = ParallelRetrievalEngine(timeout_seconds=10)

        with patch.object(engine, '_enhance_query_for_graph', return_value="enhanced query"):
            response = await engine.retrieve_parallel("safety equipment requirements")

        assert response.success is True
        assert response.fusion_ready is True
        assert response.query == "safety equipment requirements"
        assert response.total_time_ms >= 0  # Can be 0 for mocked functions

        assert response.vector_result.method == "vector_rag"
        assert response.vector_result.error is None
        assert response.vector_result.confidence > 0.0

        assert response.graph_result.method == "graph_rag"
        assert response.graph_result.error is None
        assert response.graph_result.confidence > 0.0

    @pytest.mark.asyncio
    async def test_retrieve_parallel_vector_failure(self, mock_vector_tool, mock_graph_tool, mock_graph_result):
        """Test parallel retrieval with vector failure."""
        mock_vector_search, _ = mock_vector_tool
        mock_graph_query, _ = mock_graph_tool

        mock_vector_search.side_effect = Exception("Vector failed")
        mock_graph_query.return_value = mock_graph_result

        engine = ParallelRetrievalEngine()

        with patch.object(engine, '_enhance_query_for_graph', return_value="enhanced query"):
            response = await engine.retrieve_parallel("safety equipment")

        assert response.success is True  # Graph succeeded
        assert response.vector_result.error == "Vector failed"
        assert response.graph_result.error is None

    @pytest.mark.asyncio
    async def test_retrieve_parallel_graph_failure(self, mock_vector_tool, mock_graph_tool, mock_vector_result):
        """Test parallel retrieval with graph failure."""
        mock_vector_search, _ = mock_vector_tool
        mock_graph_query, _ = mock_graph_tool

        mock_vector_search.return_value = mock_vector_result
        mock_graph_query.side_effect = Exception("Graph failed")

        engine = ParallelRetrievalEngine()

        with patch.object(engine, '_enhance_query_for_graph', return_value="enhanced query"):
            response = await engine.retrieve_parallel("safety equipment")

        assert response.success is True  # Vector succeeded
        assert response.vector_result.error is None
        assert response.graph_result.error == "Graph failed"

    @pytest.mark.asyncio
    async def test_retrieve_parallel_both_failures(self, mock_vector_tool, mock_graph_tool):
        """Test parallel retrieval with both failures."""
        mock_vector_search, _ = mock_vector_tool
        mock_graph_query, _ = mock_graph_tool

        mock_vector_search.side_effect = Exception("Vector failed")
        mock_graph_query.side_effect = Exception("Graph failed")

        engine = ParallelRetrievalEngine()

        with patch.object(engine, '_enhance_query_for_graph', return_value="enhanced query"):
            response = await engine.retrieve_parallel("safety equipment")

        assert response.success is False
        assert response.fusion_ready is False
        assert response.vector_result.error == "Vector failed"
        assert response.graph_result.error == "Graph failed"

    @pytest.mark.asyncio
    async def test_retrieve_parallel_timeout(self, mock_vector_tool, mock_graph_tool):
        """Test parallel retrieval with timeout."""
        mock_vector_search, _ = mock_vector_tool
        mock_graph_query, _ = mock_graph_tool

        # Simulate slow operations
        async def slow_vector(*args):
            await asyncio.sleep(2)
            return "Vector result"

        async def slow_graph(*args):
            await asyncio.sleep(2)
            return "Graph result"

        engine = ParallelRetrievalEngine(timeout_seconds=1)  # Short timeout

        with patch.object(engine, '_async_vector_retrieve', side_effect=slow_vector):
            with patch.object(engine, '_async_graph_retrieve', side_effect=slow_graph):
                # The engine catches TimeoutError and returns a response, so test the response
                result = await engine.retrieve_parallel("safety equipment")

                assert result.success is False
                assert result.vector_result.method == "timeout"
                assert result.graph_result.method == "timeout"
                assert result.vector_result.error == "Timeout"

    @pytest.mark.asyncio
    async def test_health_check_all_healthy(self, mock_vector_tool, mock_graph_tool):
        """Test health check with all components healthy."""
        mock_vector_search, mock_vector_health = mock_vector_tool
        mock_graph_query, mock_graph_health = mock_graph_tool

        mock_vector_health.return_value = {"status": "healthy", "response_time": 50}
        mock_graph_health.return_value = {"status": "healthy", "response_time": 75}

        engine = ParallelRetrievalEngine()

        health = await engine.health_check()

        assert health["engine_status"] == "healthy"
        assert health["vector_tool"]["status"] == "healthy"
        assert health["graph_tool"]["status"] == "healthy"
        assert health["parallel_capable"] is True

    @pytest.mark.asyncio
    async def test_health_check_partial_failure(self, mock_vector_tool, mock_graph_tool):
        """Test health check with partial component failure."""
        mock_vector_search, mock_vector_health = mock_vector_tool
        mock_graph_query, mock_graph_health = mock_graph_tool

        mock_vector_health.return_value = {"status": "healthy"}
        mock_graph_health.side_effect = Exception("Graph tool unavailable")

        engine = ParallelRetrievalEngine()

        health = await engine.health_check()

        assert health["engine_status"] == "healthy"  # Still healthy because vector is working
        assert health["vector_tool"]["status"] == "healthy"
        assert health["graph_tool"]["status"] == "unhealthy"
        assert "Graph tool unavailable" in health["graph_tool"]["error"]

    @pytest.mark.asyncio
    async def test_health_check_all_failed(self, mock_vector_tool, mock_graph_tool):
        """Test health check with all components failed."""
        mock_vector_search, mock_vector_health = mock_vector_tool
        mock_graph_query, mock_graph_health = mock_graph_tool

        mock_vector_health.side_effect = Exception("Vector tool failed")
        mock_graph_health.side_effect = Exception("Graph tool failed")

        engine = ParallelRetrievalEngine()

        health = await engine.health_check()

        assert health["engine_status"] == "error"
        assert health["vector_tool"]["status"] == "unhealthy"
        assert health["graph_tool"]["status"] == "unhealthy"

    def test_destructor_cleanup(self):
        """Test that destructor properly cleans up thread pool."""
        engine = ParallelRetrievalEngine()
        executor = engine.executor

        # Mock the shutdown method
        with patch.object(executor, 'shutdown') as mock_shutdown:
            engine.__del__()
            mock_shutdown.assert_called_once_with(wait=False)


# =========================================================================
# Unit Tests for Factory Functions
# =========================================================================

@pytest.mark.unit
class TestFactoryFunctions:
    """Test factory functions and global instance management."""

    def test_get_parallel_engine_singleton(self, clean_parallel_engine):
        """Test that get_parallel_engine implements singleton pattern."""
        engine1 = get_parallel_engine()
        engine2 = get_parallel_engine()

        assert engine1 is engine2
        assert isinstance(engine1, ParallelRetrievalEngine)

    def test_get_parallel_engine_thread_safety(self, clean_parallel_engine):
        """Test thread safety of get_parallel_engine."""
        import threading

        engines = []

        def create_engine():
            engines.append(get_parallel_engine())

        threads = [threading.Thread(target=create_engine) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All instances should be the same
        assert len(set(id(engine) for engine in engines)) == 1

    @pytest.mark.asyncio
    async def test_test_parallel_retrieval_function(self, mock_vector_tool, mock_graph_tool):
        """Test the test_parallel_retrieval function."""
        mock_vector_search, mock_vector_health = mock_vector_tool
        mock_graph_query, mock_graph_health = mock_graph_tool

        mock_vector_search.return_value = "Test vector result"
        mock_graph_query.return_value = "Test graph result"

        with patch('backend.parallel_hybrid.get_parallel_engine') as mock_get_engine:
            mock_engine = Mock()
            mock_response = Mock()
            mock_response.total_time_ms = 500
            mock_response.vector_result.confidence = 0.8
            mock_response.graph_result.confidence = 0.7
            mock_response.fusion_ready = True
            mock_response.vector_result.error = None
            mock_response.graph_result.error = None

            mock_engine.retrieve_parallel = AsyncMock(return_value=mock_response)
            mock_get_engine.return_value = mock_engine

            # Should not raise any exceptions
            await validate_parallel_retrieval()

            # Should have called retrieve_parallel multiple times (for test queries)
            assert mock_engine.retrieve_parallel.call_count >= 3


# =========================================================================
# Unit Tests for Edge Cases and Integration
# =========================================================================

@pytest.mark.unit
class TestEdgeCasesAndIntegration:
    """Test edge cases and integration scenarios."""

    def test_fusion_ready_logic_vector_only(self):
        """Test fusion ready logic with only vector results."""
        vector_result = RetrievalResult(
            content="High quality CFR § 30.1 safety equipment requirements with detailed compliance information and comprehensive regulatory guidance for mining operations",
            method="vector_rag",
            confidence=0.9,
            response_time_ms=200,
            error=None
        )

        graph_result = RetrievalResult(
            content="I don't know",
            method="graph_rag",
            confidence=0.0,
            response_time_ms=100,
            error="No results found"
        )

        # Simulate the fusion ready logic from retrieve_parallel
        vector_viable = (vector_result.error is None and
                        len(vector_result.content) > 100 and
                        vector_result.confidence > 0.3)

        graph_viable = (graph_result.error is None and
                       len(graph_result.content) > 50 and
                       graph_result.confidence > 0.2 and
                       "I don't know" not in graph_result.content.lower())

        fusion_ready = vector_viable or graph_viable or (
            vector_result.confidence > 0.6 and graph_result.error is None
        )

        assert vector_viable is True
        assert graph_viable is False
        assert fusion_ready is True

    def test_fusion_ready_logic_graph_only(self):
        """Test fusion ready logic with only graph results."""
        vector_result = RetrievalResult(
            content="Error: Vector search failed",
            method="vector_rag",
            confidence=0.0,
            response_time_ms=50,
            error="Connection timeout"
        )

        graph_result = RetrievalResult(
            content="Based on MSHA regulations, mining operations must maintain specific safety equipment standards",
            method="graph_rag",
            confidence=0.7,
            response_time_ms=300
        )

        # Simulate the fusion ready logic
        vector_viable = (vector_result.error is None and
                        len(vector_result.content) > 100 and
                        vector_result.confidence > 0.3)

        graph_viable = (graph_result.error is None and
                       len(graph_result.content) > 50 and
                       graph_result.confidence > 0.2 and
                       "I don't know" not in graph_result.content.lower())

        fusion_ready = vector_viable or graph_viable

        assert vector_viable is False
        assert graph_viable is True
        assert fusion_ready is True

    def test_confidence_calculation_edge_cases(self):
        """Test confidence calculation with edge cases."""
        engine = ParallelRetrievalEngine()

        # Empty content
        assert engine._calculate_vector_confidence("") == 0.0
        assert engine._calculate_graph_confidence("") == 0.0

        # Very short content
        assert engine._calculate_vector_confidence("No") == 0.0
        assert engine._calculate_graph_confidence("No") == 0.0

        # Error messages
        assert engine._calculate_vector_confidence("Error: Failed") == 0.0
        assert engine._calculate_graph_confidence("I don't know anything") == 0.0

        # Maximum confidence bounds
        very_long_content = "CFR § 30.1 " * 100 + "requirements shall must compliance safety"
        vector_conf = engine._calculate_vector_confidence(very_long_content)
        assert vector_conf <= 1.0

        graph_conf = engine._calculate_graph_confidence(very_long_content)
        assert graph_conf <= 1.0

    @pytest.mark.asyncio
    async def test_alternative_graph_queries(self, mock_graph_tool):
        """Test alternative graph query strategies."""
        mock_query, mock_health = mock_graph_tool

        engine = ParallelRetrievalEngine()

        # Mock the query_regulations to return "I don't know" for all strategies
        with patch('backend.parallel_hybrid.query_regulations') as mock_query_regs:
            mock_query_regs.return_value = "I don't know"  # All strategies fail

            result = await engine._try_alternative_graph_queries("safety equipment")

            # Should return the default fallback message
            expected_message = "While I couldn't find specific graph data for 'safety equipment', this appears to be related to mining safety regulations under MSHA's jurisdiction. Consider checking the vector search results or consulting Title 30 CFR directly."
            assert result == expected_message

    @pytest.mark.asyncio
    async def test_alternative_graph_queries_failure(self):
        """Test alternative graph queries with failure."""
        engine = ParallelRetrievalEngine()

        with patch('backend.parallel_hybrid.get_general_tool_safe', side_effect=Exception("General tool failed")):
            with patch('backend.parallel_hybrid.query_regulations', side_effect=Exception("Graph query failed")):
                result = await engine._try_alternative_graph_queries("safety equipment")

                # Should return a fallback message, not None
                assert "Alternative search strategies encountered an error" in result
