# -------------------------------------------------------------------------
# File: vector.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/tools/vector.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module implements VectorRAG (Vector Retrieval-Augmented Generation) functionality
# for the MRCA Advanced Parallel Hybrid system. It provides semantic similarity search
# capabilities using Gemini embeddings and Neo4j vector indexing for MSHA regulatory
# content retrieval. The module creates and manages vector search chains that combine
# retrieval with LLM processing to provide comprehensive regulatory guidance and
# compliance information based on Title 30 CFR mining safety regulations.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: get_neo4j_vector() - Creates Neo4jVector instance with Gemini embeddings
# - Function: get_vector_retriever() - Creates configured retriever for semantic search
# - Function: create_vector_chain() - Creates complete vector search chain with LLM processing
# - Function: search_regulations_semantic() - Main semantic search function for agent use
# - Function: search_regulations_detailed() - Detailed search with full metadata and sources
# - Function: get_vector_tool() - Creates LangChain tool for semantic vector search
# - Function: test_vector_search() - Test function for development and debugging
# - Function: check_vector_tool_health() - Health check function for vector search system
# - Function: get_vector_tool_safe() - Safe vector tool getter with fallback handling
# - Function: _vector_fallback() - Fallback function when vector search unavailable
# - Constant: VECTOR_SEARCH_INSTRUCTIONS - MSHA-specific retrieval instructions template
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - logging: For vector search operation logging and debugging
#   - time: Performance monitoring and timing operations
# - Third-party:
#   - langchain_neo4j.Neo4jVector: Neo4j vector database integration
#   - langchain.chains.combine_documents.create_stuff_documents_chain: Document processing
#   - langchain.chains.create_retrieval_chain: Retrieval chain creation
#   - langchain_core.prompts.ChatPromptTemplate: Prompt template for LLM processing
#   - langchain.tools.Tool: Tool creation for agent integration
# - Local Project Modules:
#   - ..llm: get_llm, get_embeddings functions for LLM and embedding access
#   - ..graph: get_graph function for Neo4j database connection
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is used by the parallel hybrid system for VectorRAG operations:
# - parallel_hybrid.py: Uses vector search functions for VectorRAG execution
# - main.py: May use vector tools for API endpoint functionality
# - Agent-based systems: Functions designed as tools for agent frameworks
# The vector search capabilities provide semantic similarity-based retrieval
# for regulatory content using advanced embedding techniques.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

VectorRAG Implementation for MRCA Mining Regulatory Search

Provides semantic similarity search capabilities using Gemini embeddings and Neo4j vector
indexing for comprehensive MSHA regulatory content retrieval as part of the Advanced
Parallel Hybrid system's VectorRAG component.

"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging
import time

# Third-party library imports
from langchain_neo4j import Neo4jVector
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# Local application/library specific imports
from ..llm import get_llm, get_embeddings
from ..graph import get_graph

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# MSHA-specific retrieval instructions template for vector search
VECTOR_SEARCH_INSTRUCTIONS = """
You are an expert MSHA regulatory assistant providing information about Title 30 CFR mining safety regulations.

Use the given context from CFR documents to answer questions about mining safety and health compliance.
Always cite specific CFR sections and document sources when available.
Focus on providing accurate regulatory guidance for mining operations.

If you don't know the answer based on the provided context, say you don't know.
Never provide legal advice - only informational guidance about regulations.

Context from CFR Title 30 documents:
{context}
"""

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# ------------------------------------
# --- Core Vector Database Setup ---
# ------------------------------------

# --------------------------------------------------------------------------------- get_neo4j_vector()
def get_neo4j_vector():
    """Create and return the Neo4jVector instance using Gemini embeddings.

    This function creates a Neo4jVector instance configured for the MRCA system
    using consistent 768-dimensional Gemini embeddings for both storage and query
    operations. It connects to the existing vector index in Neo4j created by the
    hybrid store builder and provides semantic similarity search capabilities.

    Returns:
        Neo4jVector: Configured Neo4j vector instance for similarity search operations

    Examples:
        >>> vector_db = get_neo4j_vector()
        >>> results = vector_db.similarity_search("safety regulations", k=5)
        >>> print(f"Found {len(results)} relevant documents")
    """
    return Neo4jVector.from_existing_index(
        embedding=get_embeddings(),  # Gemini embeddings from llm.py (768 dimensions)
        graph=get_graph(),          # Neo4j connection from graph.py
        index_name="chunkVector",   # Vector index created by build_hybrid_store.py
        node_label="Chunk",         # Our chunk nodes
        text_node_property="text",  # Property containing the text content
        embedding_node_property="textEmbedding",  # Property containing Gemini embeddings
        retrieval_query="""
        MATCH (node)-[:PART_OF]->(d:Document)
        OPTIONAL MATCH (node)-[:HAS_ENTITY]->(e:Entity)
        RETURN 
            node.text AS text,
            score,
            {
                document: d.id,
                chunk_id: node.id,
                entities: [(node)-[:HAS_ENTITY]->(entity) | {
                    name: entity.name,
                    type: entity.type,
                    id: entity.id
                }],
                source: 'CFR Title 30 - Mining Safety and Health',
                document_type: 'Federal Regulation'
            } AS metadata
        """
    )
# --------------------------------------------------------------------------------- end get_neo4j_vector()

# --------------------------------------------------------------------------------- get_vector_retriever()
def get_vector_retriever():
    """Create and return a retriever for semantic vector search.

    This function creates a configured retriever specifically optimized for
    MSHA regulatory content retrieval with appropriate similarity thresholds
    and result limits. The retriever uses semantic similarity based on Gemini
    embeddings to find the most relevant regulatory content.

    Returns:
        BaseRetriever: Configured retriever for regulatory content search

    Examples:
        >>> retriever = get_vector_retriever()
        >>> docs = retriever.get_relevant_documents("mining safety standards")
        >>> print(f"Retrieved {len(docs)} relevant documents")
    """
    neo4j_vector = get_neo4j_vector()
    
    # Configure retriever for regulatory content
    return neo4j_vector.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 5,  # Return top 5 most similar chunks
            "score_threshold": 0.7  # Minimum similarity threshold
        }
    )
# --------------------------------------------------------------------------------- end get_vector_retriever()

# -----------------------------------
# --- Vector Search Chain Creation ---
# -----------------------------------

# --------------------------------------------------------------------------------- create_vector_chain()
def create_vector_chain():
    """Create the complete vector search chain for MSHA regulations.

    This function creates a comprehensive vector search chain that combines
    retrieval with LLM processing to provide complete answers with proper
    regulatory context and guidance. The chain integrates semantic similarity
    search with language model processing for comprehensive regulatory responses.

    Returns:
        BaseChain: Complete vector search chain ready for question processing

    Examples:
        >>> chain = create_vector_chain()
        >>> result = chain.invoke({"input": "What are the ventilation requirements?"})
        >>> print(result["answer"])
    """
    # Get components
    llm = get_llm()
    retriever = get_vector_retriever()
    
    # Create the prompt for processing retrieved documents
    prompt = ChatPromptTemplate.from_messages([
        ("system", VECTOR_SEARCH_INSTRUCTIONS),
        ("human", "{input}")
    ])
    
    # Create document processing chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create complete retrieval chain
    vector_search_chain = create_retrieval_chain(
        retriever,
        question_answer_chain
    )
    
    return vector_search_chain
# --------------------------------------------------------------------------------- end create_vector_chain()

# --------------------------------------
# --- Main Search Interface Functions ---
# --------------------------------------

# --------------------------------------------------------------------------------- search_regulations_semantic()
def search_regulations_semantic(question: str) -> str:
    """Perform semantic vector search on MSHA regulations using Gemini embeddings.

    This function performs semantic similarity search on MSHA regulations and
    returns a formatted response suitable for agent use. It's designed to be
    used as a tool in agent frameworks, providing comprehensive regulatory
    guidance based on semantic similarity rather than keyword matching.

    Args:
        question (str): Natural language question about MSHA regulations

    Returns:
        str: Comprehensive response suitable for agent use, includes regulatory context

    Examples:
        >>> result = search_regulations_semantic("What are hard hat requirements?")
        >>> print("Safety equipment requirements found:", result[:100])

        >>> result = search_regulations_semantic("Tell me about ventilation standards")
        >>> print(result)
        "Ventilation standards require..."
    """
    try:
        # Get the vector search chain and invoke
        vector_chain = create_vector_chain()
        result = vector_chain.invoke({"input": question})
        
        # Return the answer from the chain
        return result.get("answer", "No relevant regulations found.")
        
    except Exception as e:
        # Return error message for the agent
        return f"Error during semantic search: {str(e)}"
# --------------------------------------------------------------------------------- end search_regulations_semantic()

# --------------------------------------------------------------------------------- search_regulations_detailed()
def search_regulations_detailed(question: str) -> dict:
    """Perform detailed semantic vector search with full metadata and source documents.

    This function provides comprehensive search results including full metadata,
    source documents, entity information, and search analytics. Use this for
    debugging, system monitoring, or when complete context information is needed
    for detailed analysis of search results and system performance.

    Args:
        question (str): Natural language question about MSHA regulations

    Returns:
        dict: Comprehensive dictionary containing:
            - answer (str): Formatted regulatory information
            - question (str): Original user question
            - sources (list): Source documents with metadata
            - entities_found (list): Extracted entities from results
            - num_sources (int): Number of source documents
            - search_type (str): Type of search performed

    Examples:
        >>> result = search_regulations_detailed("ventilation standards")
        >>> print(f"Found {len(result['sources'])} source documents")
        >>> print(f"Entities: {result['entities_found']}")
        >>> print(f"Answer: {result['answer']}")
    """
    try:
        # Get the vector chain and invoke it for detailed results
        vector_chain = create_vector_chain()
        result = vector_chain.invoke({"input": question})
        
        # Extract answer
        answer = result.get("answer", "No relevant regulations found.")
        
        # Get the retrieval context for detailed information
        context_docs = result.get("context", [])
        
        sources = []
        entities_found = []
        
        for doc in context_docs:
            # Extract metadata
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
            
            sources.append({
                "document": metadata.get("document", "Unknown"),
                "chunk_id": metadata.get("chunk_id", "Unknown"),
                "source": metadata.get("source", "CFR Title 30"),
                "content_preview": content[:200] + "..." if len(content) > 200 else content,
                "entities": metadata.get("entities", [])
            })
            
            # Collect entities
            doc_entities = metadata.get("entities", [])
            if isinstance(doc_entities, list):
                entities_found.extend([entity.get("name", entity) if isinstance(entity, dict) else entity for entity in doc_entities])
        
        return {
            "answer": answer,
            "question": question,
            "sources": sources,
            "entities_found": entities_found[:10],  # Limit to top 10 entities
            "num_sources": len(sources),
            "search_type": "semantic_vector_search"
        }
        
    except Exception as e:
        return {
            "answer": f"Error during semantic vector search: {str(e)}",
            "question": question,
            "sources": [],
            "entities_found": [],
            "num_sources": 0,
            "search_type": "semantic_vector_search",
            "error": str(e)
        }
# --------------------------------------------------------------------------------- end search_regulations_detailed()

# -------------------------------
# --- Agent Integration Tools ---
# -------------------------------

# --------------------------------------------------------------------------------- get_vector_tool()
def get_vector_tool():
    """Create a LangChain tool for semantic vector search of MSHA regulations.

    This tool integrates with the ReAct agent to provide regulatory information using 
    Gemini embeddings for true similarity search. It provides the VectorRAG component
    for the Advanced Parallel Hybrid system with comprehensive tool description for
    optimal agent integration and tool selection.

    Returns:
        Tool: LangChain tool configured for MSHA regulatory vector search, or None if creation fails

    Examples:
        >>> vector_tool = get_vector_tool()
        >>> if vector_tool:
        ...     response = vector_tool.func("What are safety equipment requirements?")
        ...     print(response)
    """
    try:
        from langchain.tools import Tool
        
        # Create tool using the enhanced vector search function
        vector_tool = Tool(
            name="search_regulations_semantic",
            description="""
            Searches MSHA safety regulations using semantic vector similarity search with Gemini embeddings.
            
            This tool performs true similarity search using 768-dimensional Gemini embeddings
            to find the most relevant regulatory content based on semantic meaning.
            
            Use this tool when the user asks about:
            - Safety equipment and requirements
            - Mining procedures and protocols  
            - Air quality and ventilation standards
            - Emergency procedures and evacuation
            - Personal protective equipment (PPE)
            - Electrical safety in mines
            - Roof and rib support requirements
            - Hazard identification and reporting
            - Training and certification requirements
            - General mining safety questions
            
            Input: A natural language question about MSHA regulations
            Output: Detailed regulatory information with specific CFR citations and entity context
            """,
            func=search_regulations_semantic
        )
        
        return vector_tool
        
    except Exception as e:
        logger.error(f"Error creating vector tool: {str(e)}")
        return None
# --------------------------------------------------------------------------------- end get_vector_tool()

# ---------------------------
# --- Testing and Validation ---
# ---------------------------

# --------------------------------------------------------------------------------- test_vector_search()
def test_vector_search():
    """Test function to verify vector search is working correctly.

    Comprehensive testing function that verifies VectorRAG component functionality
    with various types of mining safety questions. Provides detailed logging of
    test results and response quality for system validation and debugging purposes.
    Run this to check the VectorRAG component health and performance.

    Examples:
        >>> test_vector_search()
        # Runs comprehensive test suite with logging output
    """
    logger.info("Testing MRCA VectorRAG Component...")
    
    test_questions = [
        "What safety equipment is required in underground mines?",
        "Tell me about ventilation requirements",
        "What are the methane monitoring requirements?"
    ]
    
    for question in test_questions:
        logger.info(f"\nTesting: {question}")
        try:
            result = search_regulations_semantic(question)
            logger.info(f"Result: {result[:100]}...")
        except Exception as e:
            logger.error(f"Error: {e}")
    
    logger.info("\nVectorRAG testing complete!")
# --------------------------------------------------------------------------------- end test_vector_search()

# ---------------------------
# --- Health Monitoring ---
# ---------------------------

# --------------------------------------------------------------------------------- check_vector_tool_health()
def check_vector_tool_health() -> dict:
    """Comprehensive health check for the vector search tool and VectorRAG system.

    Performs detailed health monitoring of all VectorRAG components including Neo4j
    vector index status, embedding functionality, retrieval operations, and end-to-end
    search capabilities. Provides metrics, error details, and component-specific
    status information for system monitoring and debugging.

    Returns:
        dict: Detailed health status containing:
            - tool_name (str): Identifier for the tool being monitored
            - status (str): Overall health status (healthy/degraded/error)
            - components (dict): Individual component health statuses
            - metrics (dict): Performance and data metrics
            - errors (list): Detailed error messages for failed components

    Examples:
        >>> health = check_vector_tool_health()
        >>> print(f"VectorRAG Status: {health['status']}")
        >>> if health['errors']:
        ...     print(f"Errors: {health['errors']}")
    """
    health_status = {
        "tool_name": "vector_search",
        "status": "unknown",
        "components": {
            "neo4j_connection": "unknown",
            "vector_index": "unknown", 
            "embeddings": "unknown",
            "retrieval": "unknown"
        },
        "metrics": {
            "last_check": None,
            "response_time_ms": 0,
            "index_node_count": 0
        },
        "errors": []
    }
    
    start_time = time.time()
    
    try:
        # Test Neo4j connection
        try:
            graph = get_graph()
            health_status["components"]["neo4j_connection"] = "healthy"
        except Exception as e:
            health_status["components"]["neo4j_connection"] = "error"
            health_status["errors"].append(f"Neo4j connection: {str(e)}")
            
        # Test vector index existence and status
        try:
            neo4j_vector = get_neo4j_vector()
            
            # Test vector index by counting nodes
            query = "MATCH (n:Chunk) RETURN count(n) as chunk_count"
            result = graph.query(query)
            chunk_count = result[0]["chunk_count"] if result else 0
            
            health_status["components"]["vector_index"] = "healthy" if chunk_count > 0 else "empty"
            health_status["metrics"]["index_node_count"] = chunk_count
            
        except Exception as e:
            health_status["components"]["vector_index"] = "error"
            health_status["errors"].append(f"Vector index: {str(e)}")
            
        # Test embeddings
        try:
            embeddings = get_embeddings()
            # Test with a simple phrase
            test_embedding = embeddings.embed_query("test query")
            health_status["components"]["embeddings"] = "healthy" if len(test_embedding) > 0 else "error"
        except Exception as e:
            health_status["components"]["embeddings"] = "error"
            health_status["errors"].append(f"Embeddings: {str(e)}")
            
        # Test retrieval functionality
        try:
            retriever = get_vector_retriever()
            # Test retrieval with a simple query
            test_docs = retriever.get_relevant_documents("safety equipment", k=1)
            health_status["components"]["retrieval"] = "healthy" if len(test_docs) > 0 else "no_results"
        except Exception as e:
            health_status["components"]["retrieval"] = "error"
            health_status["errors"].append(f"Retrieval: {str(e)}")
            
        # Calculate response time
        health_status["metrics"]["response_time_ms"] = int((time.time() - start_time) * 1000)
        health_status["metrics"]["last_check"] = time.time()
        
        # Determine overall status
        component_statuses = list(health_status["components"].values())
        if all(status == "healthy" for status in component_statuses):
            health_status["status"] = "healthy"
        elif any(status == "healthy" for status in component_statuses):
            health_status["status"] = "degraded"
        else:
            health_status["status"] = "error"
            
    except Exception as e:
        health_status["status"] = "error"
        health_status["errors"].append(f"Health check failed: {str(e)}")
        health_status["metrics"]["response_time_ms"] = int((time.time() - start_time) * 1000)
    
    return health_status
# --------------------------------------------------------------------------------- end check_vector_tool_health()

# --------------------------------------------------------------------------------- get_vector_tool_safe()
def get_vector_tool_safe():
    """Safe vector tool getter with comprehensive fallback handling.

    Provides a robust tool getter that performs health checks before returning
    the vector search function. If the VectorRAG system is unavailable or unhealthy,
    returns a fallback function that provides appropriate error messaging to users
    while maintaining system stability.

    Returns:
        function: Vector search function or fallback function based on system health

    Examples:
        >>> safe_tool = get_vector_tool_safe()
        >>> response = safe_tool("What are safety requirements?")
        >>> # Returns either search results or fallback message
    """
    try:
        # Test tool health first
        health = check_vector_tool_health()
        if health["status"] in ["healthy", "degraded"]:
            return search_regulations_semantic
        else:
            logger.warning(f"Vector tool unhealthy: {health['errors']}")
            return _vector_fallback
    except Exception as e:
        logger.error(f"Vector tool initialization failed: {str(e)}")
        return _vector_fallback
# --------------------------------------------------------------------------------- end get_vector_tool_safe()

# ----------------------------
# --- Fallback Mechanisms ---
# ----------------------------

# --------------------------------------------------------------------------------- _vector_fallback()
def _vector_fallback(question: str) -> str:
    """Fallback function when vector search system is unavailable.

    Provides informative responses when the VectorRAG component of the Advanced
    Parallel Hybrid system is temporarily unavailable. Guides users toward
    alternative query methods and preserves the user's original question for
    context and potential retry scenarios.

    Args:
        question (str): User's original question about MSHA regulations

    Returns:
        str: Fallback response indicating system unavailability and alternatives

    Examples:
        >>> fallback_response = _vector_fallback("What are safety standards?")
        >>> print(fallback_response)
        "I'm currently unable to perform semantic search..."
    """
    return (
        f"I'm currently unable to perform semantic search on the MSHA regulations database. "
        f"The vector search system may be temporarily unavailable. "
        f"Please try asking a more general question, or contact support if this issue persists. "
        f"Your question was: {question}"
    )
# --------------------------------------------------------------------------------- end _vector_fallback()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.
# It serves as a testing entry point for the VectorRAG functionality, allowing
# the module to be used both as an importable component and as a standalone
# testing utility for validating vector search capabilities.

if __name__ == "__main__":
    # --- VectorRAG Component Testing Entry Point ---
    print(f"Running MRCA VectorRAG Component Tests from {__file__}...")
    
    try:
        # Execute the test function
        test_vector_search()
        print("VectorRAG component testing completed successfully!")
        
    except KeyboardInterrupt:
        print("\nTesting interrupted by user (Ctrl+C)")
        print("VectorRAG testing aborted")
        
    except Exception as e:
        print(f"Critical error during VectorRAG testing: {e}")
        print("VectorRAG testing failed")
        
    finally:
        print(f"Finished execution of {__file__}")

# =========================================================================
# End of File
# ========================================================================= 