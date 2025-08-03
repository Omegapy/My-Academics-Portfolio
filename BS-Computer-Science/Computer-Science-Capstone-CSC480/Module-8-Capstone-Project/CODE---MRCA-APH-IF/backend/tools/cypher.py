# -------------------------------------------------------------------------
# File: cypher.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/tools/cypher.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides Cypher query generation and execution functionality for the
# MRCA GraphRAG component of the Advanced Parallel Hybrid system. It translates
# natural language questions about mining safety regulations into structured Cypher
# queries that traverse the Neo4j knowledge graph. The module implements specialized
# prompt templates for MSHA regulatory contexts, handles complex graph relationships,
# and provides comprehensive health monitoring for the GraphRAG system component.
# The Cypher generation enables precise regulatory information retrieval through
# structured graph traversal queries.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Global Template: CYPHER_GENERATION_TEMPLATE - MSHA-specific Cypher generation prompt
# - Global Variable: cypher_prompt - Configured prompt template for regulatory queries
# - Function: get_cypher_qa() - Create Cypher QA chain with lazy loading
# - Function: query_regulations() - Query MSHA regulations using Cypher generation
# - Function: query_regulations_detailed() - Query with detailed response and metadata
# - Function: get_cypher_tool() - Get cypher tool for agent integration
# - Function: check_cypher_tool_health() - Comprehensive health check for cypher tool
# - Function: get_cypher_tool_safe() - Safe cypher tool getter with fallback handling
# - Function: _cypher_fallback() - Fallback function when cypher generation unavailable
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Third-Party:
#   - langchain_neo4j.GraphCypherQAChain: Neo4j graph chain for Cypher QA operations
#   - langchain.prompts.prompt.PromptTemplate: Template engine for prompt formatting
#   - logging: Module-level logging and error tracking
# - Local Project Modules:
#   - ..llm.get_llm: Lazy loading function for LLM initialization
#   - ..graph.get_graph: Lazy loading function for Neo4j graph connection
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is integrated into the MRCA backend as the GraphRAG component of the
# Advanced Parallel Hybrid system. It is used by:
# - main.py: API endpoints for graph-based regulatory queries
# - parallel_hybrid.py: GraphRAG component for hybrid search operations
# - Agent tools: Integrated as a tool for complex regulatory graph traversal
# The module provides both simple query functions for basic usage and detailed
# functions for debugging and metadata extraction. Health monitoring functions
# ensure system reliability and provide fallback mechanisms when graph services
# are unavailable.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

Cypher Query Generation for MRCA Mining Regulatory Graph Traversal

Provides specialized Cypher query generation and execution for mining safety regulations
in the Neo4j knowledge graph, enabling precise regulatory information retrieval through
structured graph traversal as part of the Advanced Parallel Hybrid system's GraphRAG component.

"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging
import time

# Third-party library imports
from langchain_neo4j import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

# Local application/library specific imports
from ..llm import get_llm
from ..graph import get_graph

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# MSHA-specific Cypher generation prompt template for regulatory queries
CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer and MSHA regulatory specialist translating user questions into Cypher queries about mining safety regulations from Title 30 CFR.

Convert the user's question based on the schema, focusing on mining safety and health compliance information.

Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Do not return entire nodes or embedding properties.

MSHA Regulatory Context:
- Focus on mining safety regulations from Title 30 CFR
- Understand regulatory terminology (CFR sections, parts, subparts)
- Handle safety equipment, procedures, violations, and compliance requirements
- Provide specific regulatory citations when possible

Fine Tuning for CFR Documents:
- CFR document titles often contain volume and part information
- Handle queries about specific CFR sections (e.g., "30 CFR 75.400")
- Focus on safety-related entities: equipment, procedures, violations, requirements

Example Cypher Statements for MSHA Regulations:

1. To find chunks related to specific safety equipment:
```
MATCH (c:Chunk)-[:HAS_ENTITY]->(e)
WHERE e.id =~ '(?i).*safety equipment.*' OR e.id =~ '(?i).*respirator.*'
MATCH (c)-[:PART_OF]->(d:Document)
RETURN c.text, d.id, e.id
LIMIT 10
```

2. To find documents containing specific CFR sections:
```
MATCH (d:Document)<-[:PART_OF]-(c:Chunk)-[:HAS_ENTITY]->(e)
WHERE d.id CONTAINS 'CFR-2024-title30' AND e.id =~ '(?i).*ventilation.*'
RETURN d.id, c.text, collect(e.id) as entities
LIMIT 5
```

3. To find related safety procedures and requirements:
```
MATCH (c:Chunk)-[:HAS_ENTITY]->(e1)-[r]-(e2)<-[:HAS_ENTITY]-(c2:Chunk)
WHERE e1.id =~ '(?i).*methane.*' AND type(r) IN ['RELATED_TO', 'REQUIRES', 'USES']
MATCH (c)-[:PART_OF]->(d:Document)
RETURN e1.id, type(r), e2.id, c.text, d.id
LIMIT 10
```

4. To search for compliance requirements:
```
MATCH (c:Chunk)-[:HAS_ENTITY]->(e)
WHERE e.id =~ '(?i).*(requirement|compliance|must|shall).*'
MATCH (c)-[:PART_OF]->(d:Document)
RETURN e.id, c.text, d.id
ORDER BY e.id
LIMIT 15
```

Always use case insensitive matching with =~ '(?i)pattern' for text searches.
Focus on safety-related entities and provide regulatory context in results.

Schema:
{schema}

Question:
{question}

Cypher Query:
"""

# Create the configured prompt template for regulatory Cypher generation
cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# -------------------------------
# --- Core Cypher Generation ---
# -------------------------------

# --------------------------------------------------------------------------------- get_cypher_qa()
def get_cypher_qa():
    """Create and return the Cypher QA chain with lazy loading and MSHA configuration.

    Initializes the GraphCypherQAChain with specialized settings for mining regulatory
    queries. Uses centralized lazy loading functions to establish connections to the
    LLM and Neo4j graph database. Configures the chain with MSHA-specific prompts,
    validation settings, and safety parameters for regulatory compliance queries.

    Returns:
        GraphCypherQAChain: Configured chain for MSHA regulatory Cypher generation

    Examples:
        >>> cypher_qa = get_cypher_qa()
        >>> result = cypher_qa.invoke({"query": "What are ventilation requirements?"})
        >>> print(result["result"])
    """
    return GraphCypherQAChain.from_llm(
        llm=get_llm(),  # OpenAI GPT-4o from llm.py (lazy loaded)
        graph=get_graph(),  # Neo4j connection from graph.py (lazy loaded)
        verbose=True,
        cypher_prompt=cypher_prompt,
        allow_dangerous_requests=True,  # Required for Cypher generation
        return_intermediate_steps=True,  # For debugging and transparency
        top_k=5,  # Limit results to avoid token overflow
        exclude_types=["textEmbedding"],  # Exclude embedding properties
        validate_cypher=True,  # Validate generated Cypher
        handle_parsing_errors=True,  # Handle LLM parsing errors gracefully
    )
# --------------------------------------------------------------------------------- end get_cypher_qa()

# --------------------------------------------------------------------------------- query_regulations()
def query_regulations(question: str) -> str:
    """Query MSHA regulations using Cypher generation for agent integration.

    Translates natural language questions about mining safety regulations into
    Cypher queries and executes them against the Neo4j knowledge graph. Designed
    for use as a tool in agent workflows, providing clean string responses
    suitable for further processing or direct user presentation.

    Args:
        question (str): Natural language question about MSHA regulations

    Returns:
        str: Formatted response with regulatory information or error message

    Examples:
        >>> response = query_regulations("What are the methane detection requirements?")
        >>> print(response)
        "Methane detection requirements include..."

        >>> response = query_regulations("Show me safety equipment regulations")
        >>> print(response)
        "Safety equipment regulations specify..."
    """
    try:
        # Get the chain and invoke with the question
        cypher_qa = get_cypher_qa()
        result = cypher_qa.invoke({"query": question})
        
        # Return the result string for the agent
        return result.get("result", "No answer found.")
        
    except Exception as e:
        # Return error message for the agent
        return f"Error processing query: {str(e)}"
# --------------------------------------------------------------------------------- end query_regulations()

# --------------------------------------------------------------------------------- query_regulations_detailed()
def query_regulations_detailed(question: str) -> dict:
    """Query MSHA regulations with detailed response including metadata and debugging info.

    Performs comprehensive regulatory queries with full metadata extraction including
    intermediate processing steps, generated Cypher queries, and context information.
    Designed for debugging, system monitoring, and detailed analysis of regulatory
    query processing workflows.

    Args:
        question (str): Natural language question about MSHA regulations

    Returns:
        dict: Comprehensive response containing:
            - answer (str): Formatted regulatory information
            - intermediate_steps (list): Processing steps and transformations
            - cypher_query (str): Generated Cypher query for transparency
            - context (list): Additional context and metadata

    Examples:
        >>> result = query_regulations_detailed("What are ventilation standards?")
        >>> print(result["answer"])
        "Ventilation standards require..."
        >>> print(result["cypher_query"])
        "MATCH (c:Chunk)-[:HAS_ENTITY]->(e)..."
    """
    try:
        # Get the chain and invoke with the question
        cypher_qa = get_cypher_qa()
        result = cypher_qa.invoke({"query": question})
        
        # Extract Cypher query from intermediate steps if available
        cypher_query = None
        if result.get("intermediate_steps"):
            for step in result["intermediate_steps"]:
                if isinstance(step, dict) and "query" in step:
                    cypher_query = step["query"]
                    break
        
        return {
            "answer": result.get("result", "No answer found"),
            "intermediate_steps": result.get("intermediate_steps", []),
            "cypher_query": cypher_query,
            "context": result.get("context", [])
        }
    except Exception as e:
        return {
            "answer": f"Error processing query: {str(e)}",
            "intermediate_steps": [],
            "cypher_query": None,
            "context": []
        }
# --------------------------------------------------------------------------------- end query_regulations_detailed()

# -------------------------------
# --- Agent Integration Tools ---
# -------------------------------

# --------------------------------------------------------------------------------- get_cypher_tool()
def get_cypher_tool():
    """Get the cypher tool function for agent integration.

    Returns the query_regulations function configured for direct use as an agent tool.
    Provides the core GraphRAG functionality for the Advanced Parallel Hybrid system's
    agent-based regulatory assistance workflows.

    Returns:
        function: query_regulations function ready for agent tool integration

    Examples:
        >>> cypher_tool = get_cypher_tool()
        >>> # Use in agent.py:
        >>> tools = [
        ...     Tool.from_function(
        ...         name="Regulation Queries",
        ...         description="For complex regulatory questions requiring graph traversal",
        ...         func=cypher_tool,
        ...     )
        ... ]
    """
    return query_regulations
# --------------------------------------------------------------------------------- end get_cypher_tool()

# --------------------------------------------------------------------------------- get_cypher_tool_safe()
def get_cypher_tool_safe():
    """Safe cypher tool getter with comprehensive fallback handling.

    Provides a robust tool getter that performs health checks before returning
    the cypher query function. If the GraphRAG system is unavailable or unhealthy,
    returns a fallback function that provides appropriate error messaging to users.

    Returns:
        function: query_regulations function or fallback function based on system health

    Examples:
        >>> safe_tool = get_cypher_tool_safe()
        >>> response = safe_tool("What are safety requirements?")
        >>> # Returns either regulatory info or fallback message
    """
    try:
        # Test tool health first
        health = check_cypher_tool_health()
        if health["status"] in ["healthy", "degraded"]:
            return query_regulations
        else:
            logger.warning(f"Cypher tool unhealthy: {health['errors']}")
            return _cypher_fallback
    except Exception as e:
        logger.error(f"Cypher tool initialization failed: {str(e)}")
        return _cypher_fallback
# --------------------------------------------------------------------------------- end get_cypher_tool_safe()

# ---------------------------
# --- Health Monitoring ---
# ---------------------------

# --------------------------------------------------------------------------------- check_cypher_tool_health()
def check_cypher_tool_health() -> dict:
    """Comprehensive health check for the cypher generation tool and GraphRAG system.

    Performs detailed health monitoring of all GraphRAG components including Neo4j
    connectivity, graph schema validation, LLM connectivity, and end-to-end Cypher
    generation functionality. Provides metrics, error details, and component-specific
    status information for system monitoring and debugging.

    Returns:
        dict: Detailed health status containing:
            - tool_name (str): Identifier for the tool being monitored
            - status (str): Overall health status (healthy/degraded/error)
            - components (dict): Individual component health statuses
            - metrics (dict): Performance and data metrics
            - errors (list): Detailed error messages for failed components

    Examples:
        >>> health = check_cypher_tool_health()
        >>> print(f"GraphRAG Status: {health['status']}")
        >>> if health['errors']:
        ...     print(f"Errors: {health['errors']}")
    """
    health_status = {
        "tool_name": "cypher_generation", 
        "status": "unknown",
        "components": {
            "neo4j_connection": "unknown",
            "graph_schema": "unknown",
            "llm_connection": "unknown", 
            "cypher_generation": "unknown"
        },
        "metrics": {
            "last_check": None,
            "response_time_ms": 0,
            "node_count": 0,
            "relationship_count": 0
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
            
        # Test graph schema and data availability
        try:
            # Check for basic node types
            node_query = "MATCH (n) RETURN labels(n) as labels, count(n) as count ORDER BY count DESC LIMIT 5"
            node_result = graph.query(node_query)
            
            # Check for relationships
            rel_query = "MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count ORDER BY count DESC LIMIT 5"
            rel_result = graph.query(rel_query)
            
            total_nodes = sum(record["count"] for record in node_result)
            total_rels = sum(record["count"] for record in rel_result)
            
            health_status["metrics"]["node_count"] = total_nodes
            health_status["metrics"]["relationship_count"] = total_rels
            
            if total_nodes > 0 and total_rels > 0:
                health_status["components"]["graph_schema"] = "healthy"
            elif total_nodes > 0:
                health_status["components"]["graph_schema"] = "partial"
                health_status["errors"].append("Graph has nodes but no relationships")
            else:
                health_status["components"]["graph_schema"] = "empty"
                health_status["errors"].append("Graph database is empty")
                
        except Exception as e:
            health_status["components"]["graph_schema"] = "error"
            health_status["errors"].append(f"Graph schema: {str(e)}")
            
        # Test LLM connection
        try:
            llm = get_llm()
            # Simple test - this might still fail due to the type annotation issue
            health_status["components"]["llm_connection"] = "healthy"
        except Exception as e:
            health_status["components"]["llm_connection"] = "error"
            health_status["errors"].append(f"LLM connection: {str(e)}")
            
        # Test Cypher generation (only if other components are working)
        try:
            if (health_status["components"]["neo4j_connection"] == "healthy" and 
                health_status["components"]["graph_schema"] in ["healthy", "partial"]):
                
                # Simple test query
                test_result = query_regulations("test query about safety")
                if "Error" not in test_result:
                    health_status["components"]["cypher_generation"] = "healthy"
                else:
                    health_status["components"]["cypher_generation"] = "error"
                    health_status["errors"].append(f"Cypher generation test failed: {test_result}")
            else:
                health_status["components"]["cypher_generation"] = "dependency_failed"
                health_status["errors"].append("Cypher generation skipped due to dependency failures")
                
        except Exception as e:
            health_status["components"]["cypher_generation"] = "error"
            health_status["errors"].append(f"Cypher generation: {str(e)}")
            
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
# --------------------------------------------------------------------------------- end check_cypher_tool_health()

# ----------------------------
# --- Fallback Mechanisms ---
# ----------------------------

# --------------------------------------------------------------------------------- _cypher_fallback()
def _cypher_fallback(question: str) -> str:
    """Fallback function when cypher generation system is unavailable.

    Provides informative responses when the GraphRAG component of the Advanced
    Parallel Hybrid system is temporarily unavailable. Guides users toward
    alternative query methods and preserves the user's original question for
    context and potential retry scenarios.

    Args:
        question (str): User's original regulatory question

    Returns:
        str: Fallback response indicating system unavailability and alternatives

    Examples:
        >>> fallback_response = _cypher_fallback("What are methane limits?")
        >>> print(fallback_response)
        "I'm currently unable to perform complex graph queries..."
    """
    return (
        f"I'm currently unable to perform complex graph queries on the MSHA regulations database. "
        f"The graph traversal system may be temporarily unavailable. "
        f"Please try asking a simpler question or use semantic search instead. "
        f"Your question was: {question}"
    )
# --------------------------------------------------------------------------------- end _cypher_fallback()

# =========================================================================
# End of File
# ========================================================================= 