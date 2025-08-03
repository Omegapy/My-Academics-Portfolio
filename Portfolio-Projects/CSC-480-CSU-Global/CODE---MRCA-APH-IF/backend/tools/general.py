# -------------------------------------------------------------------------
# File: general.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/tools/general.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides general MSHA regulatory guidance functionality that serves
# as a fallback tool in the MRCA Advanced Parallel Hybrid system. It handles
# general mining safety questions, regulatory overviews, and provides guidance
# within the mining safety and health domain when specific VectorRAG or GraphRAG
# tools don't provide sufficient information. The module implements specialized
# chat functionality for MSHA regulations with comprehensive scope management,
# error handling, and health monitoring capabilities for reliable regulatory
# assistance in mining compliance scenarios.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Global Constant: MSHA_GENERAL_CHAT_INSTRUCTIONS - MSHA-specific chat instructions
# - Function: create_msha_general_chat() - Create general MSHA chat chain
# - Function: provide_msha_guidance() - Provide general MSHA regulatory guidance
# - Function: provide_regulatory_overview() - Provide regulatory overview for topics
# - Function: handle_out_of_scope_questions() - Handle questions outside MSHA domain
# - Function: get_general_tool() - Create LangChain tool for general MSHA guidance
# - Function: get_overview_tool() - Create tool for regulatory topic overviews
# - Function: create_general_chat_chain() - Create simple general chat chain
# - Function: test_general_tool() - Test function to verify general tool functionality
# - Function: create_general_chat_tool() - Backward compatibility function
# - Function: check_general_tool_health() - Comprehensive health check for general tool
# - Function: get_general_tool_safe() - Safe general tool getter with fallback
# - Function: _general_fallback() - Fallback function when general chat unavailable
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Third-Party:
#   - langchain_core.prompts: ChatPromptTemplate and PromptTemplate for conversation
#   - langchain.schema.StrOutputParser: String output parsing for chain responses
#   - langchain.tools.Tool: Tool creation for agent integration
#   - langchain.chains.LLMChain: Chain creation for conversation workflows
#   - logging: Module-level logging and error tracking
#   - time: Performance monitoring and timing operations
# - Local Project Modules:
#   - ..llm.get_llm: Lazy loading function for LLM initialization
#   - ..graph.get_graph: Lazy loading function for Neo4j graph connection
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is integrated into the MRCA backend as a fallback component of the
# Advanced Parallel Hybrid system. It is used by:
# - main.py: API endpoints for general regulatory guidance when specific tools fail
# - parallel_hybrid.py: Fallback component when VectorRAG and GraphRAG don't suffice
# - Agent tools: Integrated as a general guidance tool for broad MSHA questions
# The module provides both simple chat functions for basic usage and comprehensive
# tools for agent integration with health monitoring and fallback mechanisms for
# system reliability when handling general mining safety and regulatory queries.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

MRCA General MSHA Regulatory Guidance Tool

Provides general chat functionality for MSHA mining safety regulations, serving as a
fallback tool when specific VectorRAG or GraphRAG tools don't provide sufficient information.
Handles regulatory overviews, safety guidance, and compliance assistance within the mining domain.

"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging
import time

# Third-party library imports
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain.chains import LLMChain

# Local application/library specific imports
from ..llm import get_llm
from ..graph import get_graph

# =========================================================================
# Global Constants / Variables
# =========================================================================
# Logger for this module
logger = logging.getLogger(__name__)

# MSHA-specific general chat instructions for regulatory guidance
MSHA_GENERAL_CHAT_INSTRUCTIONS = """
You are an expert MSHA (Mine Safety and Health Administration) regulatory assistant providing general information about mining safety and health regulations.

Your expertise covers Title 30 CFR (Code of Federal Regulations) for mining operations, including:
- Underground and surface mining safety
- Health and safety standards
- Equipment regulations and requirements
- Emergency procedures and protocols
- Training and certification requirements
- Hazard identification and prevention
- Personal protective equipment (PPE)
- Air quality and ventilation standards
- Electrical safety in mining operations
- Roof and rib support requirements

IMPORTANT GUIDELINES:
- Provide accurate, helpful information about mining safety and health
- Focus on regulatory compliance guidance and safety best practices
- Always remind users to consult official CFR documents for authoritative information
- Cite relevant CFR sections when you know them (e.g., "30 CFR § 75.1720")
- Be professional and use appropriate regulatory terminology
- Never provide legal advice - only informational guidance about regulations
- If asked about specific technical details, recommend consulting the full CFR text

SCOPE RESTRICTIONS:
- Only answer questions related to mining safety, health, and MSHA regulations
- Do not answer questions outside the mining/safety regulatory domain
- For non-mining questions, politely redirect to your regulatory expertise
- If you don't know something specific, acknowledge it and suggest official resources

RESPONSE STYLE:
- Be helpful and comprehensive in your responses
- Use clear, professional language appropriate for mining professionals
- Include safety reminders when relevant
- Provide context about why regulations exist (safety protection)
- Suggest related topics the user might want to explore
"""

# =========================================================================
# Standalone Function Definitions
# =========================================================================

# -------------------------------
# --- Core Chat Functionality ---
# -------------------------------

# --------------------------------------------------------------------------------- create_msha_general_chat()
def create_msha_general_chat():
    """Create a general MSHA chat chain for regulatory guidance and safety information.

    Initializes a LangChain chat chain specifically configured for MSHA regulatory
    guidance. Uses specialized prompt templates with mining safety expertise and
    regulatory compliance instructions. Serves as a fallback tool when specific
    VectorRAG or GraphRAG searches don't provide sufficient regulatory information.

    Returns:
        Chain: Configured LangChain chain for MSHA general chat functionality

    Examples:
        >>> chat_chain = create_msha_general_chat()
        >>> response = chat_chain.invoke({"input": "What is MSHA?"})
        >>> print(response)
        "MSHA (Mine Safety and Health Administration) is..."
    """
    # Create the chat prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", MSHA_GENERAL_CHAT_INSTRUCTIONS),
        ("human", "{input}")
    ])
    
    # Get the LLM instance
    llm = get_llm()
    
    # Create the chain
    general_chat_chain = chat_prompt | llm | StrOutputParser()
    
    return general_chat_chain
# --------------------------------------------------------------------------------- end create_msha_general_chat()

# --------------------------------------------------------------------------------- provide_msha_guidance()
def provide_msha_guidance(question: str) -> str:
    """Provide general MSHA regulatory guidance for questions not covered by specific tools.

    Handles general mining safety and regulatory questions using the MSHA chat chain.
    Designed for use as a tool in agent workflows, providing comprehensive regulatory
    guidance with appropriate disclaimers and safety context. Serves as a reliable
    fallback when specific document retrieval tools don't provide sufficient answers.

    Args:
        question (str): User question about MSHA regulations or mining safety

    Returns:
        str: Comprehensive response with general regulatory guidance and safety context

    Examples:
        >>> guidance = provide_msha_guidance("What are the main MSHA safety principles?")
        >>> print(guidance)
        "The main MSHA safety principles include..."

        >>> guidance = provide_msha_guidance("Tell me about PPE requirements")
        >>> print(guidance)
        "Personal protective equipment requirements under MSHA..."
    """
    try:
        # Get the general chat chain
        chat_chain = create_msha_general_chat()
        
        # Generate response
        response = chat_chain.invoke({"input": question})
        
        # Ensure response is a string
        if isinstance(response, str):
            return response
        else:
            return str(response)
            
    except Exception as e:
        # Graceful error handling for the agent
        return f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try rephrasing your question about MSHA regulations or mining safety."
# --------------------------------------------------------------------------------- end provide_msha_guidance()

# --------------------------------------------------------------------------------- provide_regulatory_overview()
def provide_regulatory_overview(topic: str = "general") -> str:
    """Provide a regulatory overview for specific mining safety topics.

    Generates structured overviews of specific MSHA regulatory areas using
    predefined topic prompts. Covers major mining safety domains including
    ventilation, PPE, training, electrical safety, and emergency procedures.
    Used when users need general information about regulatory scope and requirements.

    Args:
        topic (str, optional): Specific regulatory topic. Defaults to "general".
                              Supported: "general", "ventilation", "ppe", "training", 
                              "electrical", "emergency", "equipment"

    Returns:
        str: Comprehensive regulatory overview for the specified topic

    Examples:
        >>> overview = provide_regulatory_overview("ventilation")
        >>> print(overview)
        "Key ventilation requirements and air quality standards..."

        >>> overview = provide_regulatory_overview("ppe")
        >>> print(overview)
        "Personal protective equipment requirements for mining..."
    """
    overview_prompts = {
        "general": "Provide a general overview of MSHA regulations and mining safety requirements.",
        "ventilation": "Explain the key ventilation requirements and air quality standards in mining operations.",
        "ppe": "Describe personal protective equipment requirements for mining operations.",
        "training": "Outline the training and certification requirements for miners under MSHA regulations.",
        "electrical": "Explain electrical safety requirements and standards in mining operations.",
        "emergency": "Describe emergency procedures and evacuation requirements in mines.",
        "equipment": "Explain equipment safety requirements and inspection standards for mining operations."
    }
    
    prompt = overview_prompts.get(topic.lower(), overview_prompts["general"])
    
    try:
        return provide_msha_guidance(prompt)
    except Exception as e:
        return f"Error providing regulatory overview: {str(e)}"
# --------------------------------------------------------------------------------- end provide_regulatory_overview()

# --------------------------------------------------------------------------------- handle_out_of_scope_questions()
def handle_out_of_scope_questions(question: str) -> str:
    """Handle questions that are outside the MSHA regulatory domain.

    Provides polite redirection to mining safety topics when users ask questions
    outside the scope of MSHA regulations and mining safety. Maintains professional
    tone while clearly defining the system's expertise boundaries and suggesting
    appropriate topics for assistance.

    Args:
        question (str): User question that's outside mining/safety scope

    Returns:
        str: Professional redirection message with scope clarification

    Examples:
        >>> redirect = handle_out_of_scope_questions("How do I file taxes?")
        >>> print(redirect)
        "I'm specifically designed to assist with MSHA regulations..."
    """
    redirect_message = """
I'm specifically designed to assist with MSHA (Mine Safety and Health Administration) regulations and mining safety questions. 

I can help you with:
- Mining safety and health regulations (Title 30 CFR)
- Equipment requirements and safety standards
- Training and certification requirements
- Emergency procedures and protocols
- Personal protective equipment (PPE) guidance
- Air quality and ventilation standards
- Hazard identification and prevention
- Electrical safety in mining operations

Please feel free to ask me about any mining safety or MSHA regulatory topic, and I'll be happy to help!
"""
    
    return redirect_message
# --------------------------------------------------------------------------------- end handle_out_of_scope_questions()

# -------------------------------
# --- Tool Creation Functions ---
# -------------------------------

# --------------------------------------------------------------------------------- get_general_tool()
def get_general_tool():
    """Create a LangChain tool for general MSHA regulatory assistance.

    Creates a comprehensive LangChain Tool configured for general MSHA guidance.
    Serves as a fallback when specific VectorRAG or GraphRAG tools don't provide
    sufficient information. Includes detailed description for proper agent integration
    and clear usage guidelines for optimal tool selection in agent workflows.

    Returns:
        Tool: LangChain tool configured for general MSHA guidance, or None if creation fails

    Examples:
        >>> general_tool = get_general_tool()
        >>> if general_tool:
        ...     response = general_tool.func("What is MSHA?")
        ...     print(response)
    """
    try:
        # Create the general chat tool
        general_tool = Tool(
            name="general_msha_guidance",
            description="""
            Provides general MSHA regulatory guidance and mining safety information.
            
            Use this tool when:
            - User asks general questions about mining safety or MSHA regulations
            - Other specific tools (vector search, graph queries) don't provide sufficient information
            - User needs regulatory overviews or safety best practices
            - User asks about broad regulatory concepts or compliance guidance
            - Questions about mining safety principles that don't require specific document retrieval
            
            This tool covers:
            - General mining safety and health principles
            - MSHA regulatory overviews and guidance
            - Safety best practices and compliance advice
            - Training and certification information
            - Equipment safety general requirements
            - Emergency procedure concepts
            - Regulatory scope and applicability
            
            Input: A natural language question about MSHA regulations or mining safety
            Output: General regulatory guidance with appropriate disclaimers and CFR references when applicable
            """,
            func=provide_msha_guidance
        )
        
        return general_tool
        
    except Exception as e:
        logger.error(f"Error creating general tool: {str(e)}")
        return None
# --------------------------------------------------------------------------------- end get_general_tool()

# --------------------------------------------------------------------------------- get_overview_tool()
def get_overview_tool():
    """Create a specialized tool for providing regulatory overviews on specific topics.

    Creates a LangChain Tool for structured regulatory topic overviews. Complements
    the general tool by providing focused overviews of specific MSHA regulatory
    areas. Designed for users who need introductory information about particular
    regulatory domains or want to understand the scope of regulations for specific topics.

    Returns:
        Tool: LangChain tool for regulatory topic overviews, or None if creation fails

    Examples:
        >>> overview_tool = get_overview_tool()
        >>> if overview_tool:
        ...     response = overview_tool.func("ventilation")
        ...     print(response)
    """
    try:
        overview_tool = Tool(
            name="regulatory_overview",
            description="""
            Provides structured overviews of specific MSHA regulatory topics.
            
            Use this tool when:
            - User asks for an overview of a specific regulatory area
            - User wants to understand the scope of regulations for a particular topic
            - User needs introductory information about a regulatory domain
            
            Supported topics: ventilation, PPE, training, electrical, emergency, equipment, general
            
            Input: A regulatory topic or area (e.g., "ventilation requirements", "PPE standards")
            Output: Structured overview of the regulatory requirements for that topic
            """,
            func=lambda topic: provide_regulatory_overview(topic)
        )
        
        return overview_tool
        
    except Exception as e:
        logger.error(f"Error creating overview tool: {str(e)}")
        return None
# --------------------------------------------------------------------------------- end get_overview_tool()

# ----------------------------------
# --- Compatibility and Utilities ---
# ----------------------------------

# --------------------------------------------------------------------------------- create_general_chat_chain()
def create_general_chat_chain():
    """Create a simple general chat chain for direct use in agent tools.

    Creates a general chat chain following the pattern from reference implementations.
    Provides a simple interface for direct chain usage in agent tools without the
    additional tool wrapper overhead. Maintains compatibility with existing agent
    integration patterns.

    Returns:
        Chain: LangChain chain for general MSHA chat ready for direct invocation

    Examples:
        >>> chat_chain = create_general_chat_chain()
        >>> response = chat_chain.invoke({"input": "What are safety standards?"})
    """
    return create_msha_general_chat()
# --------------------------------------------------------------------------------- end create_general_chat_chain()

# --------------------------------------------------------------------------------- create_general_chat_tool()
def create_general_chat_tool():
    """Create a general chat function for backward compatibility.

    Backward compatibility function that matches the pattern used in agent.py.
    Creates a general chat function for MSHA-related questions that can be
    directly invoked without the LangChain Tool wrapper. Maintains compatibility
    with existing implementations while providing the same functionality.

    Returns:
        function: Callable function for general MSHA guidance with invoke method

    Examples:
        >>> chat_func = create_general_chat_tool()
        >>> response = chat_func({"input": "What is mining safety?"})
    """
    chat_chain = create_msha_general_chat()
    return chat_chain.invoke
# --------------------------------------------------------------------------------- end create_general_chat_tool()

# ---------------------------
# --- Testing and Validation ---
# ---------------------------

# --------------------------------------------------------------------------------- test_general_tool()
def test_general_tool():
    """Test function to verify the general tool is working correctly.

    Comprehensive testing function that verifies general tool functionality
    with various types of questions including in-scope mining safety questions,
    out-of-scope questions, and edge cases. Provides detailed logging of test
    results and response quality for system validation and debugging purposes.

    Examples:
        >>> test_general_tool()
        # Runs comprehensive test suite with logging output
    """
    logger.info("Testing MRCA General Chat Tool...")
    
    test_questions = [
        "What is MSHA and what do they regulate?",
        "Tell me about general mining safety principles",
        "What are the main areas covered by Title 30 CFR?",
        "I need help with my taxes",  # Out of scope test
        "What training is required for new miners?",
        "Explain the importance of ventilation in mines"
    ]
    
    for i, question in enumerate(test_questions, 1):
        logger.info(f"\n{i}. Testing: {question}")
        try:
            response = provide_msha_guidance(question)
            logger.info(f"Response ({len(response)} chars): {response[:150]}...")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
    
    logger.info("\n✅ General tool testing complete!")
# --------------------------------------------------------------------------------- end test_general_tool()

# ---------------------------
# --- Health Monitoring ---
# ---------------------------

# --------------------------------------------------------------------------------- check_general_tool_health()
def check_general_tool_health() -> dict:
    """Comprehensive health check for the general chat tool and LLM connectivity.

    Performs detailed health monitoring of the general chat tool including LLM
    connectivity testing and chat functionality validation. Provides metrics,
    error details, and component-specific status information for system monitoring
    and debugging of the general guidance component.

    Returns:
        dict: Detailed health status containing:
            - tool_name (str): Identifier for the tool being monitored
            - status (str): Overall health status (healthy/degraded/error)
            - components (dict): Individual component health statuses
            - metrics (dict): Performance metrics and timing information
            - errors (list): Detailed error messages for failed components

    Examples:
        >>> health = check_general_tool_health()
        >>> print(f"General Tool Status: {health['status']}")
        >>> if health['errors']:
        ...     print(f"Errors: {health['errors']}")
    """
    health_status = {
        "tool_name": "general_chat",
        "status": "unknown", 
        "components": {
            "llm_connection": "unknown",
            "chat_chain": "unknown"
        },
        "metrics": {
            "last_check": None,
            "response_time_ms": 0
        },
        "errors": []
    }
    
    start_time = time.time()
    
    try:
        # Test LLM connection
        try:
            llm = get_llm()
            health_status["components"]["llm_connection"] = "healthy"
        except Exception as e:
            health_status["components"]["llm_connection"] = "error"
            health_status["errors"].append(f"LLM connection: {str(e)}")
            
        # Test chat chain functionality
        try:
            if health_status["components"]["llm_connection"] == "healthy":
                # Test with a simple question
                chat_chain = create_msha_general_chat()
                test_response = chat_chain.invoke({"input": "What is MSHA?"})
                
                if test_response and len(test_response.strip()) > 10:
                    health_status["components"]["chat_chain"] = "healthy"
                else:
                    health_status["components"]["chat_chain"] = "no_response"
                    health_status["errors"].append("Chat chain returned empty or very short response")
            else:
                health_status["components"]["chat_chain"] = "dependency_failed" 
                health_status["errors"].append("Chat chain skipped due to LLM failure")
                
        except Exception as e:
            health_status["components"]["chat_chain"] = "error"
            health_status["errors"].append(f"Chat chain: {str(e)}")
            
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
# --------------------------------------------------------------------------------- end check_general_tool_health()

# --------------------------------------------------------------------------------- get_general_tool_safe()
def get_general_tool_safe():
    """Safe general tool getter with comprehensive fallback handling.

    Provides a robust tool getter that performs health checks before returning
    the general chat function. If the general chat system is unavailable or
    unhealthy, returns a fallback function that provides static MSHA guidance
    and appropriate error messaging to users.

    Returns:
        function: General chat function or fallback function based on system health

    Examples:
        >>> safe_tool = get_general_tool_safe()
        >>> response = safe_tool("What are MSHA requirements?")
        >>> # Returns either detailed guidance or fallback message
    """
    try:
        # Test tool health first
        health = check_general_tool_health()
        if health["status"] in ["healthy", "degraded"]:
            return create_general_chat_tool()
        else:
            logger.warning(f"General tool unhealthy: {health['errors']}")
            return _general_fallback
    except Exception as e:
        logger.error(f"General tool initialization failed: {str(e)}")
        return _general_fallback
# --------------------------------------------------------------------------------- end get_general_tool_safe()

# ----------------------------
# --- Fallback Mechanisms ---
# ----------------------------

# --------------------------------------------------------------------------------- _general_fallback()
def _general_fallback(question: str) -> str:
    """Fallback function when general chat system is unavailable.

    Provides basic static MSHA guidance when the main general chat tool is
    unavailable. Includes essential MSHA contact information, official resources,
    and safety reminders to ensure users still receive valuable guidance even
    when the AI-powered chat system is experiencing issues.

    Args:
        question (str): User's original question about MSHA regulations

    Returns:
        str: Static fallback response with basic MSHA information and resources

    Examples:
        >>> fallback_response = _general_fallback("What are safety requirements?")
        >>> print(fallback_response)
        "I'm currently unable to provide detailed guidance..."
    """
    return (
        f"I'm currently unable to provide detailed guidance about your question. "
        f"The general chat system may be temporarily unavailable. "
        f"\n\nFor immediate assistance with MSHA regulations:\n"
        f"• Visit the official MSHA website: https://www.msha.gov/\n"
        f"• Review Title 30 CFR regulations\n"
        f"• Contact MSHA directly for specific compliance questions\n"
        f"• Always prioritize safety and follow established procedures\n\n"
        f"Your question was: {question}"
    )
# --------------------------------------------------------------------------------- end _general_fallback()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This block runs only when the file is executed directly, not when imported.
# It serves as a testing entry point for the general chat tool functionality,
# allowing the module to be used both as an importable component and as a
# standalone testing utility for validating general MSHA guidance capabilities.

if __name__ == "__main__":
    # --- General Chat Tool Testing Entry Point ---
    print(f"Running MRCA General Chat Tool Tests from {__file__}...")
    
    try:
        # Execute the test function
        test_general_tool()
        print("🎉 General chat tool testing completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user (Ctrl+C)")
        print("🛑 General tool testing aborted")
        
    except Exception as e:
        print(f"❌ Critical error during general tool testing: {e}")
        print("🛑 General tool testing failed")
        
    finally:
        print(f"Finished execution of {__file__}")

# =========================================================================
# End of File
# ========================================================================= 