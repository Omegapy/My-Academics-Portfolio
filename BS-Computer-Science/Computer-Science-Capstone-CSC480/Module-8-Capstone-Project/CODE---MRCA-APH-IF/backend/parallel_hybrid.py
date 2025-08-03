# -------------------------------------------------------------------------
# File: parallel_hybrid.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/parallel_hybrid.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module implements the core Advanced Parallel Hybrid retrieval engine for the MRCA system.
# It provides simultaneous execution of VectorRAG and GraphRAG techniques as described in research
# literature on hybrid retrieval-augmented generation. The engine executes both retrieval methods
# in parallel instead of using sequential agent-based selection, maximizing information coverage
# and providing comprehensive regulatory compliance information from both semantic similarity
# and graph traversal approaches.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: RetrievalResult - Data container for individual retrieval results with metadata
# - Class: ParallelRetrievalResponse - Container for complete parallel retrieval response
# - Class: ParallelRetrievalEngine - Main parallel retrieval engine implementing Advanced Parallel Hybrid
# - Function: get_parallel_engine() - Factory function for global engine instance
# - Function: test_parallel_retrieval() - Development testing function for engine validation
# - Various private methods for confidence calculation, query enhancement, and error handling
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - asyncio: For asynchronous parallel execution of retrieval operations
#   - time: For performance timing and response time measurements
#   - logging: For comprehensive debugging and operation tracking
#   - typing: For type hints (Dict, List, Any, Optional, Tuple, cast)
#   - dataclasses: For data container definitions (RetrievalResult, ParallelRetrievalResponse)
#   - concurrent.futures: For thread pool execution and parallel processing
# - Third-Party: None
# - Local Project Modules:
#   - .tools.vector: VectorRAG implementation with semantic similarity search
#   - .tools.cypher: GraphRAG implementation with Cypher query generation
#   - .tools.general: General tool safety mechanisms and fallbacks
#   - .llm: LLM access for processing and enhancement
#   - .utils: Session management and utility functions
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is the core component used by the MRCA Advanced Parallel Hybrid system:
# - main.py: Uses parallel engine for API endpoint processing of regulatory queries
# - context_fusion.py: Receives parallel retrieval results for advanced fusion processing
# - Frontend UI: Indirectly uses through API endpoints for dual AI processing modes
# The engine provides the foundational parallel retrieval capability that distinguishes
# MRCA's Advanced Parallel Hybrid approach from traditional sequential RAG systems.
# It enables simultaneous VectorRAG and GraphRAG execution for comprehensive regulatory coverage.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import asyncio
import time
import logging
from typing import Dict, List, Any, Optional, Tuple, cast
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party library imports
# (None for this module)

# Local application/library specific imports
try:
    # Try relative imports first (when run as module)
    from .tools.vector import search_regulations_semantic, check_vector_tool_health
    from .tools.cypher import query_regulations, check_cypher_tool_health
    from .tools.general import get_general_tool_safe
    from .llm import get_llm
    from .utils import get_session_id
except ImportError:
    # Fall back to absolute imports (when run directly from backend directory)
    from tools.vector import search_regulations_semantic, check_vector_tool_health
    from tools.cypher import query_regulations, check_cypher_tool_health
    from tools.general import get_general_tool_safe
    from llm import get_llm
    from utils import get_session_id

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# Global parallel engine instance for singleton pattern
_parallel_engine = None

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class RetrievalResult
@dataclass
class RetrievalResult:
    """Container for retrieval results with metadata.

    This dataclass encapsulates the results from individual retrieval operations
    (VectorRAG or GraphRAG) including the retrieved content, performance metrics,
    confidence scoring, and error handling information. It provides a standardized
    format for both successful and failed retrieval attempts.

    Class Attributes:
        None

    Instance Attributes:
        content (str): Retrieved regulatory content or error message.
        method (str): Retrieval method identifier ('vector_rag', 'graph_rag', etc.).
        confidence (float): Confidence score between 0.0 and 1.0 for result quality.
        response_time_ms (int): Response time in milliseconds for performance tracking.
        error (Optional[str]): Error message if retrieval failed. Defaults to None.
        metadata (Optional[Dict[str, Any]]): Additional metadata about the retrieval. Defaults to None.

    Methods:
        None (dataclass with automatic methods)
    """
    content: str
    method: str
    confidence: float
    response_time_ms: int
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
@dataclass
class ParallelRetrievalResponse:
    """Container for parallel retrieval response.

    This dataclass aggregates the results from simultaneous VectorRAG and GraphRAG
    operations, providing comprehensive metadata about the parallel retrieval process
    including timing, success status, and fusion readiness assessment for downstream
    context fusion processing.

    Class Attributes:
        None

    Instance Attributes:
        vector_result (RetrievalResult): Result from VectorRAG semantic similarity search.
        graph_result (RetrievalResult): Result from GraphRAG knowledge graph traversal.
        query (str): Original user query that triggered the parallel retrieval.
        total_time_ms (int): Total time for parallel retrieval operation in milliseconds.
        success (bool): Overall success status (true if at least one retrieval succeeded).
        fusion_ready (bool): Whether results are suitable for context fusion processing.

    Methods:
        None (dataclass with automatic methods)
    """
    vector_result: RetrievalResult
    graph_result: RetrievalResult
    query: str
    total_time_ms: int
    success: bool
    fusion_ready: bool
# ------------------------------------------------------------------------- end class ParallelRetrievalResponse

# ------------------------------------------------------------------------- class ParallelRetrievalEngine
class ParallelRetrievalEngine:
    """Advanced Parallel Hybrid Retrieval Engine for MRCA system.

    This class implements the core Advanced Parallel Hybrid retrieval approach that
    simultaneously executes VectorRAG and GraphRAG techniques as described in research
    literature on hybrid retrieval-augmented generation. Unlike sequential agent-based
    approaches, this engine runs both retrieval methods in parallel to maximize
    information coverage and provide comprehensive regulatory compliance information.

    Class Attributes:
        None

    Instance Attributes:
        timeout_seconds (int): Maximum time to wait for retrieval operations.
        executor (ThreadPoolExecutor): Thread pool for parallel retrieval execution.

    Methods:
        retrieve_parallel(): Main method for parallel VectorRAG and GraphRAG execution.
        health_check(): Comprehensive health check for retrieval components.
        _async_vector_retrieve(): Asynchronous VectorRAG execution.
        _async_graph_retrieve(): Asynchronous GraphRAG execution.
        _calculate_vector_confidence(): Confidence scoring for vector results.
        _calculate_graph_confidence(): Confidence scoring for graph results.
        _enhance_query_for_graph(): Query enhancement for GraphRAG optimization.
        _try_alternative_graph_queries(): Fallback strategies for failed graph queries.
        _create_timeout_response(): Response creation for timeout scenarios.
        _create_error_response(): Response creation for error scenarios.
    """
    
    # -------------------
    # --- Constructor ---
    # -------------------
    
    # --------------------------------------------------------------------------------- function __init__
    def __init__(self, timeout_seconds: int = 30) -> None:
        """Initialize the parallel retrieval engine.

        Creates a parallel retrieval engine with configurable timeout and thread pool
        for simultaneous VectorRAG and GraphRAG execution. The engine is optimized
        for regulatory compliance queries requiring comprehensive information coverage.

        Args:
            timeout_seconds (int): Maximum time to wait for retrieval operations. Defaults to 30.
        """
        self.timeout_seconds = timeout_seconds
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ParallelRAG")
    # ---------------------------------------------------------------------------------

    # ---------------------------
    # --- Setters / Mutators ---
    # ---------------------------
    
    # --------------------------------------------------------------------------------- function retrieve_parallel
    async def retrieve_parallel(self, query: str) -> ParallelRetrievalResponse:
        """Execute VectorRAG and GraphRAG simultaneously using advanced parallel approach.

        This is the core method of the Advanced Parallel Hybrid system that executes
        both VectorRAG (semantic similarity) and GraphRAG (knowledge graph traversal)
        simultaneously to maximize information coverage for regulatory compliance queries.

        Args:
            query (str): User's natural language question about MSHA regulations.

        Returns:
            ParallelRetrievalResponse: Complete response with results from both retrieval methods,
                                     including timing, confidence scores, and fusion readiness.

        Examples:
            >>> engine = ParallelRetrievalEngine()
            >>> result = await engine.retrieve_parallel("What safety equipment is required?")
            >>> print(f"Fusion ready: {result.fusion_ready}")
        """
        start_time = time.time()
        logger.info(f"Starting parallel retrieval for query: {query[:50]}...")
        
        try:
            # Create async tasks for parallel execution
            vector_task = asyncio.create_task(self._async_vector_retrieve(query))
            graph_task = asyncio.create_task(self._async_graph_retrieve(query))
            
            # Wait for both tasks with timeout
            vector_result, graph_result = await asyncio.wait_for(
                asyncio.gather(vector_task, graph_task, return_exceptions=True),
                timeout=self.timeout_seconds
            )
            
            # Handle potential exceptions and ensure proper typing
            final_vector_result: RetrievalResult
            final_graph_result: RetrievalResult
            
            if isinstance(vector_result, Exception):
                final_vector_result = RetrievalResult(
                    content=f"Vector retrieval failed: {str(vector_result)}",
                    method="vector_rag",
                    confidence=0.0,
                    response_time_ms=0,
                    error=str(vector_result)
                )
            else:
                final_vector_result = cast(RetrievalResult, vector_result)
                
            if isinstance(graph_result, Exception):
                final_graph_result = RetrievalResult(
                    content=f"Graph retrieval failed: {str(graph_result)}",
                    method="graph_rag", 
                    confidence=0.0,
                    response_time_ms=0,
                    error=str(graph_result)
                )
            else:
                final_graph_result = cast(RetrievalResult, graph_result)
            
            total_time = int((time.time() - start_time) * 1000)
            
            # Determine if we have sufficient content for fusion
            # Advanced Parallel Hybrid should use available results even if one component fails
            vector_viable = (final_vector_result.error is None and 
                           len(final_vector_result.content) > 100 and 
                           final_vector_result.confidence > 0.3)
            
            graph_viable = (final_graph_result.error is None and 
                          len(final_graph_result.content) > 50 and 
                          final_graph_result.confidence > 0.2 and
                          "I don't know" not in final_graph_result.content.lower())
            
            # Fusion ready if we have at least one strong result OR good vector with any graph attempt
            fusion_ready = vector_viable or graph_viable or (
                final_vector_result.confidence > 0.6 and final_graph_result.error is None
            )
            
            # Success if at least one retrieval succeeded
            success = final_vector_result.error is None or final_graph_result.error is None
            
            logger.info(f"✅ Parallel retrieval completed in {total_time}ms")
            logger.info(f"   Vector viable: {vector_viable} ({len(final_vector_result.content)} chars)")
            logger.info(f"   Graph viable: {graph_viable} ({len(final_graph_result.content)} chars)")
            logger.info(f"   Fusion ready: {fusion_ready}")
            
            # 🔍 DEBUGGING: Show actual search results
            logger.info(f"\n" + "="*80)
            logger.info(f"DEBUGGING - SEARCH RESULTS FOR: {query}")
            logger.info(f"="*80)
            
            logger.info(f"\nVECTOR SEARCH RESULT (Confidence: {final_vector_result.confidence:.2f}):")
            logger.info(f"{'─'*60}")
            if final_vector_result.error:
                logger.info(f"❌ ERROR: {final_vector_result.error}")
            else:
                logger.info(f"{final_vector_result.content}")
            
            logger.info(f"\nGRAPH SEARCH RESULT (Confidence: {final_graph_result.confidence:.2f}):")
            logger.info(f"{'─'*60}")
            if final_graph_result.error:
                logger.info(f"❌ ERROR: {final_graph_result.error}")
            else:
                logger.info(f"{final_graph_result.content}")
            
            logger.info(f"\n" + "="*80)
            
            return ParallelRetrievalResponse(
                vector_result=final_vector_result,
                graph_result=final_graph_result,
                query=query,
                total_time_ms=total_time,
                success=success,
                fusion_ready=fusion_ready
            )
            
        except asyncio.TimeoutError:
            logger.error(f"❌ Parallel retrieval timeout after {self.timeout_seconds}s")
            return self._create_timeout_response(query, start_time)
        except Exception as e:
            logger.error(f"❌ Parallel retrieval failed: {str(e)}")
            return self._create_error_response(query, start_time, str(e))
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # ---------------------------------------------------------------------------------
    async def _async_vector_retrieve(self, query: str) -> RetrievalResult:
        """Execute vector retrieval asynchronously.

        This internal method performs VectorRAG retrieval using semantic similarity
        search in a thread pool to avoid blocking the async event loop. It includes
        confidence calculation and comprehensive error handling.

        Args:
            query (str): User's natural language question for semantic search.

        Returns:
            RetrievalResult: Vector retrieval result with content, confidence, and timing.
        """
        start_time = time.time()
        
        try:
            # Run vector search in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                search_regulations_semantic, 
                query
            )
            
            response_time = int((time.time() - start_time) * 1000)
            
            # Calculate confidence based on result quality
            confidence = self._calculate_vector_confidence(result)
            
            return RetrievalResult(
                content=result,
                method="vector_rag",
                confidence=confidence,
                response_time_ms=response_time,
                metadata={"retrieval_type": "semantic_similarity"}
            )
            
        except Exception as e:
            response_time = int((time.time() - start_time) * 1000)
            logger.error(f"Vector retrieval error: {str(e)}")
            return RetrievalResult(
                content=f"Vector retrieval failed: {str(e)}",
                method="vector_rag",
                confidence=0.0,
                response_time_ms=response_time,
                error=str(e)
            )
    # ---------------------------------------------------------------------------------
    
    # ---------------------------------------------------------------------------------
    async def _async_graph_retrieve(self, query: str) -> RetrievalResult:
        """Execute graph retrieval asynchronously.

        This internal method performs GraphRAG retrieval using knowledge graph traversal
        in a thread pool to avoid blocking the async event loop. It includes query
        enhancement, alternative query strategies, and confidence calculation.

        Args:
            query (str): User's natural language question for graph traversal.

        Returns:
            RetrievalResult: Graph retrieval result with content, confidence, and timing.
        """
        start_time = time.time()
        
        try:
            # Enhance the query with MSHA regulatory context like the ReAct agent does
            enhanced_query = self._enhance_query_for_graph(query)
            
            # Run graph query in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                query_regulations,
                enhanced_query
            )
            
            response_time = int((time.time() - start_time) * 1000)
            
            # If we get "I don't know", try alternative query strategies
            if "I don't know" in result or len(result) < 50:
                logger.info(f"Graph retrieval got minimal result, trying alternative approaches...")
                alternative_result = await self._try_alternative_graph_queries(query)
                if alternative_result and len(alternative_result) > len(result):
                    result = alternative_result
            
            # Calculate confidence based on result quality
            confidence = self._calculate_graph_confidence(result)
            
            return RetrievalResult(
                content=result,
                method="graph_rag",
                confidence=confidence,
                response_time_ms=response_time,
                metadata={"retrieval_type": "graph_traversal", "enhanced_query": enhanced_query}
            )
            
        except Exception as e:
            response_time = int((time.time() - start_time) * 1000)
            logger.error(f"Graph retrieval error: {str(e)}")
            return RetrievalResult(
                content=f"Graph retrieval failed: {str(e)}",
                method="graph_rag",
                confidence=0.0,
                response_time_ms=response_time,
                error=str(e)
            )
    # ---------------------------------------------------------------------------------
    
    # ---------------------------------------------------------------------------------
    def _calculate_vector_confidence(self, result: str) -> float:
        """Calculate confidence score for vector retrieval result.

        This internal method evaluates the quality of VectorRAG retrieval results
        using heuristic analysis including content length, regulatory terminology,
        and CFR citation presence to generate a confidence score.

        Args:
            result (str): Retrieved content from vector similarity search.

        Returns:
            float: Confidence score between 0.0 and 1.0 indicating result quality.
        """
        if not result or "Error" in result or len(result) < 50:
            return 0.0
        
        # Basic heuristics for confidence
        confidence = 0.5  # Base confidence
        
        # Higher confidence if CFR sections are cited
        if "CFR" in result and "§" in result:
            confidence += 0.3
            
        # Higher confidence for longer, detailed responses
        if len(result) > 200:
            confidence += 0.1
            
        # Higher confidence if specific regulations mentioned
        regulatory_terms = ["requirement", "shall", "must", "compliance", "safety"]
        term_count = sum(1 for term in regulatory_terms if term.lower() in result.lower())
        confidence += min(0.1, term_count * 0.02)
        
        return min(1.0, confidence)
    # ---------------------------------------------------------------------------------
    
    # ---------------------------------------------------------------------------------
    def _calculate_graph_confidence(self, result: str) -> float:
        """Calculate confidence score for graph retrieval result.

        This internal method evaluates the quality of GraphRAG retrieval results
        using heuristic analysis including content analysis, entity presence,
        and "I don't know" response detection to generate a confidence score.

        Args:
            result (str): Retrieved content from graph traversal search.

        Returns:
            float: Confidence score between 0.0 and 1.0 indicating result quality.
        """
        if not result or "Error" in result or len(result) < 50:
            return 0.0
            
        # Check for "I don't know" responses which indicate no data found
        if "I don't know" in result.lower():
            return 0.1  # Very low confidence but not zero
            
        # Basic heuristics for confidence
        confidence = 0.5  # Base confidence
        
        # Higher confidence if structured information is present
        if "CFR" in result and "§" in result:
            confidence += 0.3
            
        # Higher confidence for entity-rich responses
        if any(keyword in result.lower() for keyword in ["entity", "relationship", "related to"]):
            confidence += 0.1
            
        # Higher confidence for longer responses
        if len(result) > 200:
            confidence += 0.1
            
        return min(1.0, confidence)
    
    def _enhance_query_for_graph(self, query: str) -> str:
        """
        Enhance user query with context that helps GraphCypherQAChain generate better Cypher.
        This mimics the context the ReAct agent provides.
        """
        # Add MSHA regulatory context to help with Cypher generation
        enhanced_query = f"""
MSHA Regulatory Query: {query}

Context: This is a question about mining safety and health regulations under Title 30 CFR. 
Focus on finding specific regulatory requirements, safety equipment, procedures, compliance standards, or related entities in the mining regulatory knowledge graph.

Key areas to search:
- Safety equipment and procedures
- Regulatory requirements and compliance
- Mining operations and ventilation
- Equipment standards and specifications
- Emergency procedures and rescue operations

Query: {query}
"""
        return enhanced_query.strip()
    
    async def _try_alternative_graph_queries(self, original_query: str) -> str:
        """
        Try alternative query strategies when the primary GraphRAG query fails.
        This provides fallback approaches similar to what a ReAct agent might try.
        """
        try:
            # Strategy 1: Broader entity search
            broad_query = f"Find any entities or information related to: {original_query}"
            
            loop = asyncio.get_event_loop()
            result1 = await loop.run_in_executor(
                self.executor,
                query_regulations,
                broad_query
            )
            
            if result1 and "I don't know" not in result1 and len(result1) > 50:
                return f"Related regulatory information: {result1}"
            
            # Strategy 2: Keyword-based search
            # Extract key terms from the query
            key_terms = []
            mining_terms = ["mine", "mining", "underground", "surface", "coal", "metal", "safety", 
                          "equipment", "ventilation", "methane", "rescue", "emergency", "compliance"]
            
            for term in mining_terms:
                if term.lower() in original_query.lower():
                    key_terms.append(term)
            
            if key_terms:
                keyword_query = f"Find information about mining safety regulations related to: {', '.join(key_terms)}"
                
                result2 = await loop.run_in_executor(
                    self.executor,
                    query_regulations,
                    keyword_query
                )
                
                if result2 and "I don't know" not in result2 and len(result2) > 50:
                    return f"Mining safety regulations related to {', '.join(key_terms)}: {result2}"
            
            # Strategy 3: General MSHA guidance
            general_query = f"Provide general MSHA guidance about: {original_query}"
            
            result3 = await loop.run_in_executor(
                self.executor,
                query_regulations, 
                general_query
            )
            
            if result3 and "I don't know" not in result3 and len(result3) > 50:
                return f"General MSHA guidance: {result3}"
                
            # If all strategies fail, return a helpful message
            return f"While I couldn't find specific graph data for '{original_query}', this appears to be related to mining safety regulations under MSHA's jurisdiction. Consider checking the vector search results or consulting Title 30 CFR directly."
            
        except Exception as e:
            logger.error(f"Alternative graph query strategies failed: {str(e)}")
            return f"Alternative search strategies encountered an error for '{original_query}'. Please try rephrasing your question."
    
    def _create_timeout_response(self, query: str, start_time: float) -> ParallelRetrievalResponse:
        """Create response for timeout scenarios"""
        total_time = int((time.time() - start_time) * 1000)
        
        timeout_result = RetrievalResult(
            content="Retrieval operation timed out",
            method="timeout",
            confidence=0.0,
            response_time_ms=total_time,
            error="Timeout"
        )
        
        return ParallelRetrievalResponse(
            vector_result=timeout_result,
            graph_result=timeout_result,
            query=query,
            total_time_ms=total_time,
            success=False,
            fusion_ready=False
        )
    
    def _create_error_response(self, query: str, start_time: float, error: str) -> ParallelRetrievalResponse:
        """Create response for error scenarios"""
        total_time = int((time.time() - start_time) * 1000)
        
        error_result = RetrievalResult(
            content=f"Retrieval failed: {error}",
            method="error",
            confidence=0.0,
            response_time_ms=total_time,
            error=error
        )
        
        return ParallelRetrievalResponse(
            vector_result=error_result,
            graph_result=error_result,
            query=query,
            total_time_ms=total_time,
            success=False,
            fusion_ready=False
        )
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # --- Class Information Methods (Optional, but highly recommended) ---
    # ---------------------------------------------------------------------
    
    # ---------------------------------------------------------------------------------
    async def health_check(self) -> Dict[str, Any]:
        """Check health of parallel retrieval components.

        This method performs comprehensive health checks on both VectorRAG and
        GraphRAG components to ensure the parallel retrieval engine is operating
        correctly and capable of handling regulatory queries.

        Returns:
            Dict[str, Any]: Health status dictionary containing engine status,
                          individual tool health, and operational metrics.

        Examples:
            >>> engine = ParallelRetrievalEngine()
            >>> health = await engine.health_check()
            >>> print(f"Engine status: {health['engine_status']}")
        """
        logger.info("Checking parallel retrieval engine health...")

        # Check individual tool health with exception handling
        try:
            vector_health = check_vector_tool_health()
        except Exception as e:
            vector_health = {"status": "unhealthy", "error": str(e)}

        try:
            graph_health = check_cypher_tool_health()
        except Exception as e:
            graph_health = {"status": "unhealthy", "error": str(e)}

        # Overall engine health
        engine_healthy = (vector_health["status"] in ["healthy", "degraded"] or
                         graph_health["status"] in ["healthy", "degraded"])

        return {
            "engine_status": "healthy" if engine_healthy else "error",
            "vector_tool": vector_health,
            "graph_tool": graph_health,
            "parallel_capable": engine_healthy,
            "timeout_seconds": self.timeout_seconds,
            "thread_pool_size": self.executor._max_workers
        }
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    # --- Destructor (Use only if absolutely necessary for external resource cleanup) -
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    def __del__(self) -> None:
        """Cleanup thread pool on deletion.

        Performs cleanup operations when the ParallelRetrievalEngine object is destroyed.
        Ensures proper shutdown of the thread pool executor to prevent resource leaks
        and handle graceful termination of background retrieval operations.
        """
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
    # ---------------------------------------------------------------------------------
    
# -------------------------------------------------------------------------

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# ---------------------------------------------------------------------------------
def get_parallel_engine() -> ParallelRetrievalEngine:
    """Get or create the global parallel retrieval engine instance.

    This function implements a singleton pattern to provide global access to the
    parallel retrieval engine instance. It ensures only one engine exists throughout
    the application lifecycle for optimal resource management.

    Returns:
        ParallelRetrievalEngine: The global parallel retrieval engine instance.

    Examples:
        >>> engine = get_parallel_engine()
        >>> result = await engine.retrieve_parallel("safety equipment requirements")
        >>> print(f"Retrieved in {result.total_time_ms}ms")
    """
    global _parallel_engine
    if _parallel_engine is None:
        _parallel_engine = ParallelRetrievalEngine()
    return _parallel_engine
# ---------------------------------------------------------------------------------

# ------------------------
# --- Helper Functions ---
# ------------------------

# ---------------------------------------------------------------------------------
async def validate_parallel_retrieval() -> None:
    """Validate the parallel retrieval engine functionality.

    This development and validation function validates the parallel retrieval engine
    by executing test queries and reporting performance metrics, confidence scores,
    and error handling capabilities.

    Examples:
        >>> await validate_parallel_retrieval()
        Testing Parallel Retrieval Engine...
        All tests completed successfully
    """
    logger.info("Testing Parallel Retrieval Engine...")
    
    engine = get_parallel_engine()
    
    test_queries = [
        "What safety equipment is required in underground mines?",
        "Tell me about mine rescue team requirements",
        "What are ventilation standards for mining operations?"
    ]
    
    for query in test_queries:
        logger.info(f"\nTesting parallel retrieval: {query}")
        
        result = await engine.retrieve_parallel(query)
        
        logger.info(f"Total time: {result.total_time_ms}ms")
        logger.info(f"Vector confidence: {result.vector_result.confidence:.2f}")
        logger.info(f"Graph confidence: {result.graph_result.confidence:.2f}")
        logger.info(f"Fusion ready: {result.fusion_ready}")
        
        if result.vector_result.error:
            logger.warning(f"⚠️ Vector error: {result.vector_result.error}")
        if result.graph_result.error:
            logger.warning(f"⚠️ Graph error: {result.graph_result.error}")
    
    logger.info("\nParallel retrieval testing complete!")
# ---------------------------------------------------------------------------------

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.
# It provides testing capabilities for the parallel retrieval engine during development.

if __name__ == "__main__":
    # --- Parallel Retrieval Engine Testing ---
    print("Starting MRCA Advanced Parallel Hybrid Engine Testing...")
    
    # Execute parallel retrieval testing function
    asyncio.run(test_parallel_retrieval())
    
    print("Parallel retrieval engine testing completed.")
    
# --------------------------------------------------------------------------------- 