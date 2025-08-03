# -------------------------------------------------------------------------
# File: bot.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-07-11 
# Last Modified: 2025-07-11
# File Path: frontend/bot.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module implements the Streamlit-based user interface for the MRCA
# (Mining Regulatory Compliance Assistant) application. 
# Users can configure search parameters, and view performance metrics.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Global Constant: BACKEND_URL
# - Function: get_session_id()
# - Function: write_message()
# - Function: display_parallel_hybrid_metrics()
# - Function: display_header()
# - Function: display_disclaimer()
# - Function: display_parallel_hybrid_config()
# - Function: display_sidebar()
# - Function: display_system_health()
# - Function: get_welcome_message()
# - Function: call_parallel_hybrid_api()
# - Function: handle_submit()
# - Function: process_template_response()
# - Function: display_post_processing_feedback()
# - Function: get_confidence_level()
# - Function: get_quality_assessment()
# - Function: handle_processing_error()
# - Function: initialize_session()
# - Function: main()
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# This file relies on several standard and third-party libraries for its
# functionality, as well as an environment variable for backend configuration.
# - Standard Library: datetime (for timestamps), os (for environment variables),
#                     json (for data serialization), uuid (for session IDs)
# - Third-Party: streamlit (for UI framework), requests (for HTTP communication)
# - Local Project Modules: None (this is a standalone script communicating via HTTP)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is the primary entry point for the MRCA frontend application.
# It is designed to be run directly as a Streamlit application (e.g., `streamlit run bot.py`).
# It integrates with the `backend` FastAPI service by making HTTP requests to its
# `/generate_parallel_hybrid` endpoint. It handles user input, displays responses,
# manages session state, and provides configuration options for the Advanced Parallel Hybrid RAG.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Streamlit-based User Interface for MRCA Advanced Parallel Hybrid System

Provides an interactive web interface for the Mining Regulatory Compliance Assistant
with real-time configuration options, performance metrics, and Advanced Parallel
Hybrid RAG technology for mining safety regulation queries.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
from datetime import datetime  # Used for displaying current date in sidebar.
import os  # Used to retrieve environment variables like BACKEND_URL.

import uuid  # Used for generating unique session IDs.

# Third-party library imports
import streamlit as st  # The core framework for building the web UI.
import requests  # Used for making HTTP requests to the backend API.


# =========================================================================
# Global Constants / Variables
# =========================================================================
# Backend API configuration URL.
# Supports both BACKEND_URL (direct URL) and BACKEND_HOST (Render host injection)
def get_backend_url():
    """Get the backend URL from environment variables.
    
    Returns:
        str: The complete backend URL
    """
    # Check for direct URL first (local development, docker-compose)
    backend_url = os.getenv("BACKEND_URL")
    if backend_url:
        return backend_url
    
    # Check for host-only (Render deployment)
    backend_host = os.getenv("BACKEND_HOST")
    if backend_host:
        # Construct full URL with HTTPS for Render
        return f"https://{backend_host}"
    
    # Default fallback for local development
    return "http://localhost:8000"

BACKEND_URL = get_backend_url()


# =========================================================================
# Standalone Function Definitions
# =========================================================================
# These are functions that are not methods of any specific class within this module.

# --------------------------
# --- Utility Functions ---
# --------------------------

# --------------------------------------------------------------------------------- get_session_id()
def get_session_id() -> str:
    """Generates or retrieves a unique session ID for conversation tracking.

    This function ensures that each user session has a consistent, unique
    identifier stored in Streamlit's session state, which is then used
    for tracking conversations with the backend.

    Returns:
        str: A unique session identifier (UUID).
    """
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id
# --------------------------------------------------------------------------------- end get_session_id()

# --------------------------------------------------------------------------------- write_message()
def write_message(role: str, content: str, save: bool = True, metadata: dict | None = None) -> None:
    """Writes a message to the Streamlit UI and optionally saves it to session state.

    This function formats the message based on the role ('user' or 'assistant')
    and can display additional metadata, particularly for Advanced Parallel Hybrid
    responses, which include performance metrics and fusion analysis.

    Args:
        role (str): The role of the message sender ('user' or 'assistant').
        content (str): The text content of the message.
        save (bool, optional): If True, the message is appended to the
                                Streamlit session state history. Defaults to True.
        metadata (dict, optional): Optional dictionary containing metadata
                                   (e.g., processing times, confidence scores)
                                   for assistant messages. Defaults to None.
    """
    if save:
        message_data: dict = {"role": role, "content": content}
        if metadata:
            message_data["metadata"] = metadata
        st.session_state.messages.append(message_data)

    with st.chat_message(role):
        st.markdown(content)

        # Display parallel hybrid metadata if available and if the message is from the assistant
        if metadata and role == "assistant":
            display_parallel_hybrid_metrics(metadata)
            
            # Display processing summary if we have the necessary metadata
            if metadata.get('metadata', {}).get('context_fusion'):
                fusion_data = metadata.get('metadata', {}).get('context_fusion', {})
                config = metadata.get('config', {})
                fusion_strategy = config.get('fusion_strategy', 'advanced_hybrid')
                template_type = config.get('template_type', 'regulatory_compliance')
                display_post_processing_feedback(fusion_strategy, template_type, metadata)
# --------------------------------------------------------------------------------- end write_message()

# --------------------------------------------------------------------------------- display_parallel_hybrid_metrics()
def display_parallel_hybrid_metrics(metadata: dict) -> None:
    """Displays detailed metrics for Advanced Parallel Hybrid responses in an expandable section.

    This function visually presents key performance indicators and analytical insights
    from the backend's Advanced Parallel Hybrid processing, including total processing
    time, confidence scores, quality scores, and the contribution of VectorRAG and GraphRAG.

    Args:
        metadata (dict): A dictionary containing the processing metadata from the
                         backend API response. Expected to contain keys like
                         'processing_time' and nested 'metadata' for 'context_fusion'
                         and 'hybrid_template'.
    """
    if not metadata:
        return

    # Create expandable metrics section
    with st.expander("🔬 Advanced Parallel HybridRAG Metrics", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Processing Time",
                f"{metadata.get('processing_time', 0):.2f}s"
            )

        with col2:
            fusion_data = metadata.get('metadata', {}).get('context_fusion', {})
            st.metric(
                "Confidence Score",
                f"{fusion_data.get('final_confidence', 0)*100:.1f}%",
                help="Algorithm's confidence level in the accuracy and reliability of the response, combining vector and graph search results through advanced fusion techniques"
            )

        with col3:
            fusion_data = metadata.get('metadata', {}).get('context_fusion', {})
            st.metric(
                "Quality Score",
                f"{fusion_data.get('quality_score', 0)*100:.1f}%",
                help="Content quality assessment based on regulatory terminology density (40%), technical specificity (30%), linguistic complexity (20%), and response length appropriateness (10%)"
            )

        # Detailed breakdown of fusion analysis
        st.markdown("**Fusion Analysis:**")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"**Strategy:** {fusion_data.get('strategy', 'N/A')}")
            st.markdown(f"**Vector Contribution:** {fusion_data.get('vector_contribution', 0):.1%}")
            st.markdown(f"**Graph Contribution:** {fusion_data.get('graph_contribution', 0):.1%}")

        with col_b:
            template_data = metadata.get('metadata', {}).get('hybrid_template', {})
            st.markdown(f"**Template Type:** {template_data.get('type', 'N/A')}")
            st.markdown(f"**Processing Mode:** Advanced Parallel Hybrid")
# --------------------------------------------------------------------------------- end display_parallel_hybrid_metrics()

# --------------------------------------------------------------------------------- display_header()
def display_header() -> None:
    """Displays the main MRCA application header with branding.

    This function inserts a custom HTML/CSS block to render a stylized header
    at the top of the Streamlit application, emphasizing its role as a
    Mining Regulatory Compliance Assistant powered by Advanced Parallel Hybrid RAG.
    """
    st.markdown("""
    <div class="main-header">
        <h1>⛏️ MRCA - Mining Regulatory Compliance Assistant</h1>
        <p>AI-Powered Access to MSHA Title 30 CFR Regulations | Advanced Parallel HybridRAG - Intelligent Fusion</p>
    </div>
    """, unsafe_allow_html=True)
# --------------------------------------------------------------------------------- end display_header()

# --------------------------------------------------------------------------------- display_disclaimer()
def display_disclaimer() -> None:
    """Displays an important legal disclaimer regarding the use of MRCA.

    This function adds a prominent disclaimer to the UI, clarifying that MRCA
    provides informational guidance only and is not a substitute for legal
    or health advice, or official MSHA interpretations.
    """
    st.markdown("""
    <div class="disclaimer">
        <h4>⚠️ Important Legal Disclaimer</h4>
        <p><strong>MRCA provides information and guidance only - It does not provide legal or health advice.</strong>
        Always consult the official Code of Federal Regulations (CFR) and qualified legal counsel for
        authoritative regulatory interpretation. MRCA is a research tool to help understand mining safety
        regulations but does not replace official MSHA guidance or legal consultation.</p>
    </div>
    """, unsafe_allow_html=True)
# --------------------------------------------------------------------------------- end display_disclaimer()

# --------------------------------------------------------------------------------- display_parallel_hybrid_config()
def display_parallel_hybrid_config() -> None:
    """Displays the configuration options for the Advanced Parallel Hybrid RAG mode.

    This function provides interactive select boxes for users to choose
    the desired 'Fusion Strategy' and 'Template Type', along with
    dynamic descriptions for each option to aid user understanding.
    These selections influence how the backend processes queries.
    """
    st.markdown("### Search Configuration - Advanced Parallel HybridRAG Settings")

    col1, col2 = st.columns(2)

    with col1:
        fusion_strategy = st.selectbox(
            "Fusion Strategy",
            options=["advanced_hybrid", "weighted_linear", "max_confidence", "adaptive_fusion"],
            index=0,
            key="fusion_strategy",
            help="Algorithm for combining VectorRAG and GraphRAG results"
        )

    with col2:
        template_type = st.selectbox(
            "Template Type",
            options=["regulatory_compliance", "basic_hybrid", "research_based", "comparative_analysis", "confidence_weighted"],
            index=0,
            key="template_type",
            help="Specialized prompt template for response generation"
        )

    # Display strategy descriptions
    strategy_descriptions = {
        "advanced_hybrid": "**Advanced Hybrid**: Research-based fusion with complementarity analysis",
        "weighted_linear": "**Weighted Linear**: Confidence-based linear combination",
        "max_confidence": "**Max Confidence**: Select highest confidence result with context",
        "adaptive_fusion": "**Adaptive**: Dynamic strategy selection based on content"
    }

    template_descriptions = {
        "regulatory_compliance": "**Regulatory Compliance**: Mine-type specific regulations and regulations urgency assessment",
        "research_based": "**Research-Based**: Research-based template with methodology notes",
        "basic_hybrid": "**Basic Hybrid**: Simple combination template",
        "comparative_analysis": "**Comparative Analysis**: Shows source complementarity",
        "confidence_weighted": "**Confidence Weighted**: Adjusts based on information quality"
    }

    # Display descriptions in column format
    desc_col1, desc_col2 = st.columns(2)

    with desc_col1:
        st.markdown(strategy_descriptions.get(fusion_strategy or "advanced_hybrid", ""))

    with desc_col2:
        st.markdown(template_descriptions.get(template_type or "regulatory_compliance", ""))
# --------------------------------------------------------------------------------- end display_parallel_hybrid_config()

# --------------------------------------------------------------------------------- display_sidebar()
def display_sidebar() -> None:
    """Displays the enhanced Streamlit sidebar with system status, query examples,
    research features, knowledge base statistics, and application information.

    This function consolidates various informational and interactive elements
    into the sidebar, providing quick access to system health, pre-defined queries,
    and details about MRCA's core capabilities and data.
    """
    with st.sidebar:
        # Display Advanced Parallel Hybrid header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a2d1a 0%, #2d3a2d 100%);
                            border: 1px solid #4a904a; border-radius: 8px; padding: 1rem;
                            text-align: center; margin-bottom: 1rem;">
                <h3 style="color: #4a904a; margin: 0; font-size: 1.2rem;"> ⛏️ MRCA - Advanced Parallel HybridRAG</h3>
                <p style="color: #b3d9b3; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                    Title 30 CFR - MSHA Regulations
                </p>
        </div>
        """, unsafe_allow_html=True)

        # System status
        st.markdown("### System Status:")
        display_system_health()

        st.markdown("---")
        st.markdown("### Query Examples:")
        example_queries = [
            "What safety equipment is required in underground mines?",
            "Tell me about methane monitoring requirements",
            "What are the ventilation standards for coal mines?",
            "Explain MSHA inspection procedures",
            "What are the requirements for mine rescue teams?"
        ]

        for query in example_queries:
            if st.button(f"📃 {query[:35]}...", key=f"example_{hash(query)}",
                         help=query, use_container_width=True):
                st.session_state.example_query = query

        st.markdown("---")
        st.markdown("### 🔬 Research Features:")
        st.markdown("""
        <div class="feature-highlight">
        <strong>Advanced Parallel HybridRAG:</strong><br>
        •  Simultaneous Retrieval<br>
        •  Research-Based Fusion<br>
        •  4 Fusion Strategies<br>
        •  5 Template Types<br>
        •  Performance Analytics
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Knowledge Base:")
        st.markdown("""
        <div class="stats-box">
        <strong>Database Contents:</strong><br>
        • 26,429 total nodes<br>
        • 20,851 regulatory entities<br>
        • 5,575 text chunks<br>
        • 3 CFR volumes processed
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ℹ️ About MRCA")
        st.markdown("""
        **Version:** Beta 2.0.1 (Advanced Parallel Hybrid Only)
        **Technology:** Research-Grade HybridRAG
        **Data Source:** Title 30 CFR
        **Last Updated:** {}
        """.format(datetime.now().strftime("%Y-%m-%d")))

        # Clear conversation button
        st.markdown("---")
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": get_welcome_message()}
            ]
            st.rerun()
# --------------------------------------------------------------------------------- end display_sidebar()

# --------------------------------------------------------------------------------- display_system_health()
def display_system_health() -> None:
    """Displays the real-time health status of the backend services.

    This function checks the health endpoint of the backend's Advanced Parallel Hybrid
    service and displays a visual indicator (Healthy, Degraded, Error) to the user.
    """
    try:
        # Check parallel hybrid health only
        try:
            parallel_health = requests.get(f"{BACKEND_URL}/parallel_hybrid/health", timeout=60)
            if parallel_health.status_code == 200:
                parallel_status = "🟢 Healthy"
            elif parallel_health.status_code == 503:
                parallel_status = "🟡 Degraded"
            else:
                parallel_status = "🔴 Error"
        except requests.exceptions.ConnectionError: # Catch specific connection error for clearer message
            parallel_status = "🔴 Error (Backend Not Reachable)"
        except requests.exceptions.Timeout: # Catch timeout specifically for clearer message
            parallel_status = "🔴 Error (Health Check Timeout)"
        except Exception: # General catch for other unexpected errors during health check
            parallel_status = "🔴 Error (Health Check Failed)"

    except Exception: # This outer try-except might be redundant given the inner one for health check
        parallel_status = "🔴 Error (General Issue)"

    st.markdown(f"""
    **Parallel Hybrid:** {parallel_status}
    """)
# --------------------------------------------------------------------------------- end display_system_health()

# --------------------------------------------------------------------------------- get_welcome_message()
def get_welcome_message() -> str:
    """Returns the welcome message for the Advanced Parallel Hybrid mode.

    This message introduces the MRCA system, highlights its core capabilities,
    explains how to get started, and emphasizes its research-grade features,
    while also including an important legal disclaimer.

    Returns:
        str: A formatted string containing the welcome message.
    """
    return """**MRCA - APH-IF Beta v2.0**

I'm your research-grade AI assistant for navigating **Title 30 CFR mining safety regulations**. This system uses advanced Advanced Parallel Hybrid technology for superior performance:

**What I can help you with:**
- **Regulatory Search** - Find specific safety requirements and procedures
- **Compliance Guidance** - Understand regulatory obligations and standards
- **Mining Safety** - Equipment, ventilation, monitoring, and inspection requirements
- **CFR Navigation** - Locate specific sections and understand regulatory structure

**How to get started:**
- Ask me about any MSHA regulation or mining safety topic
- Try the example questions in the sidebar
- Be specific for the best results (e.g., "underground coal mine ventilation requirements")

**This is research grade tool and it has the following Features:**
- **4 Fusion Strategies** - Advanced hybrid, weighted linear, max confidence, adaptive
- **5 Template Types** - Research-based, regulatory compliance, comparative analysis, and more
- **Performance Metrics** - Detailed processing analytics and confidence scores
- **Quality Analysis** - Fusion readiness, contribution ratios, and complementarity scores

**Remember:** I provide informational guidance based on CFR Title 30. Always consult official MSHA resources and qualified professionals for authoritative regulatory interpretation.

What would you like to know about mining safety regulations?"""
# --------------------------------------------------------------------------------- end get_welcome_message()

# --------------------------------------------------------------------------------- call_parallel_hybrid_api()
def call_parallel_hybrid_api(user_input: str, session_id: str, fusion_strategy: str, template_type: str) -> tuple:
    """Calls the parallel hybrid backend API to generate a response.

    This function constructs an HTTP POST request to the backend service,
    sending the user's query along with the selected fusion strategy and
    template type. It handles API responses, including successful data
    retrieval and various error conditions (timeout, connection, API errors).

    Args:
        user_input (str): The natural language query from the user.
        session_id (str): The unique identifier for the current user session.
        fusion_strategy (str): The chosen algorithm for combining VectorRAG
                               and GraphRAG results (e.g., "advanced_hybrid").
        template_type (str): The chosen specialized prompt template for
                             generating the final response (e.g., "regulatory_compliance").

    Returns:
        tuple: A tuple containing:
               - str: The generated response text or an error message.
               - dict | None: A dictionary of metadata if the call was successful,
                              otherwise None.
    """
    try:
        payload = {
            "user_input": user_input,
            "session_id": session_id,
            "fusion_strategy": fusion_strategy,
            "template_type": template_type
        }

        headers = {
            "Content-Type": "application/json",
            "X-Session-ID": session_id
        }

        response = requests.post(
            f"{BACKEND_URL}/generate_parallel_hybrid",
            json=payload,
            headers=headers,
            timeout=None # No timeout - allow unlimited processing time for active sessions
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response received from backend"), {
                "processing_time": data.get("processing_time", 0),
                "mode": "parallel_hybrid",
                "metadata": data.get("metadata", {})
            }
        else:
            return f"Parallel hybrid API error (status {response.status_code}): {response.text}", None

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again with a shorter question.", None
    except requests.exceptions.ConnectionError:
        return f"Could not connect to backend service at {BACKEND_URL}. Please ensure the backend is running.", None
    except Exception as e:
        return f"Error calling parallel hybrid API: {str(e)}", None
# --------------------------------------------------------------------------------- end call_parallel_hybrid_api()

# --------------------------------------------------------------------------------- handle_submit()
def handle_submit(message: str) -> None:
    """Handles the user's message submission, orchestrating the request to the
    backend and managing the display of responses and associated metrics.

    This function acts as the central logic for processing user input. It
    validates the selected fusion strategy and template type, displays
    processing information, calls the backend API, and then formats and
    displays the assistant's response, including detailed metrics and feedback.

    Args:
        message (str): The user's input message to be processed.
    """
    # Display user message
    write_message('user', message)

    # Get and validate configuration parameters
    fusion_strategy = st.session_state.get("fusion_strategy", "advanced_hybrid")
    template_type = st.session_state.get("template_type", "regulatory_compliance")

    # Validate fusion strategy
    valid_fusion_strategies = ["advanced_hybrid", "weighted_linear", "max_confidence", "adaptive_fusion"]
    if fusion_strategy not in valid_fusion_strategies:
        st.warning(f"⚠️ Invalid fusion strategy '{fusion_strategy}'. Using default 'advanced_hybrid'.")
        fusion_strategy = "advanced_hybrid"

    # Validate template type
    valid_template_types = ["regulatory_compliance", "basic_hybrid", "research_based", "comparative_analysis", "confidence_weighted"]
    if template_type not in valid_template_types:
        st.warning(f"⚠️ Invalid template type '{template_type}'. Using default 'regulatory_compliance'.")
        template_type = "regulatory_compliance"

    # Display processing information with current configuration
    processing_info = f"""
    🔬 **Processing with Advanced Parallel Hybrid**

    **Configuration:**
    • Fusion Strategy: `{fusion_strategy.replace('_', ' ').title()}`
    • Template Type: `{template_type.replace('_', ' ').title()}`
    • Mode: Simultaneous VectorRAG + GraphRAG
    """

    # Generate response using Advanced Parallel Hybrid
    with st.spinner(f'🔬 Be patient! Processing with {fusion_strategy.replace("_", " ").title()} fusion and {template_type.replace("_", " ").title()} template...'):
        try:
            session_id = get_session_id()

            # Show brief processing info
            with st.expander("Current Processing Configuration", expanded=False):
                st.markdown(processing_info)

            # Call API with selected configuration
            response, metadata = call_parallel_hybrid_api(message, session_id, fusion_strategy, template_type)

            # Enhanced response handling based on template type
            if metadata:
                # Add configuration info to metadata for display
                metadata['config'] = {
                    'fusion_strategy': fusion_strategy,
                    'template_type': template_type,
                    'processing_mode': 'advanced_parallel_hybrid'
                }

                # Template-specific response processing
                response = process_template_response(response, template_type, metadata)

            # Display assistant response with enhanced metadata
            write_message('assistant', response, metadata=metadata)

        except Exception as e:
            error_message = handle_processing_error(e, fusion_strategy, template_type)
            write_message('assistant', error_message)
# --------------------------------------------------------------------------------- end handle_submit()

# --------------------------------------------------------------------------------- process_template_response()
def process_template_response(response: str, template_type: str, metadata: dict) -> str:
    """Processes the raw API response by adding template-specific headers and footers.

    This function enhances the readability and context of the AI's response
    based on the chosen template type, adding appropriate introductory text
    and a footer that includes the confidence level of the generated response.

    Args:
        response (str): The raw response text received from the backend API.
        template_type (str): The type of template used for response generation
                             (e.g., "regulatory_compliance", "research_based").
        metadata (dict): The metadata associated with the API response, used
                         to extract confidence scores.

    Returns:
        str: The processed response string with added headers and footers.
    """
    # Template-specific response enhancements
    template_enhancements = {
        "regulatory_compliance": "**Regulatory Compliance Analysis**\n\n",
        "research_based": "**Research-Based Analysis**\n\n",
        "basic_hybrid": "**Basic Hybrid Analysis**\n\n",
        "comparative_analysis": "**Comparative Source Analysis**\n\n",
        "confidence_weighted": "**Confidence-Weighted Analysis**\n\n"
    }

    # Add template-specific header if not already present
    enhancement = template_enhancements.get(template_type, "")
    if enhancement and not any(marker in response for marker in ["**Regulatory Compliance", "**Research-Based", "**Basic Hybrid", "**Comparative", "**Confidence-Weighted"]):
        response = enhancement + response

    # Add template-specific footer information
    fusion_data = metadata.get('metadata', {}).get('context_fusion', {})
    confidence = fusion_data.get('final_confidence', 0)

    template_footers = {
        "regulatory_compliance": f"\n\n*This compliance analysis uses enhanced regulatory focus with mine-type awareness and urgency assessment (Confidence: {confidence*100:.1f}%)*",
        "research_based": f"\n\n*This analysis incorporates research-based methodology notes and source attribution (Confidence: {confidence*100:.1f}%)*",
        "comparative_analysis": f"\n\n*This analysis shows complementarity between vector and graph sources (Confidence: {confidence*100:.1f}%)*",
        "confidence_weighted": f"\n\n*Response tone and certainty calibrated to information confidence level: {confidence*100:.1f}%*",
        "basic_hybrid": f"\n\n*Simple hybrid combination of vector and graph sources (Confidence: {confidence*100:.1f}%)*"
    }

    footer = template_footers.get(template_type, f"\n\n🔬 *Advanced Parallel Hybrid analysis (Confidence: {confidence*100:.1f}%)*")
    response += footer

    return response
# --------------------------------------------------------------------------------- end process_template_response()

# --------------------------------------------------------------------------------- display_post_processing_feedback()
def display_post_processing_feedback(fusion_strategy: str, template_type: str, metadata: dict) -> None:
    """Displays a summary of the processing performed, including details about
    the fusion strategy and template type used, and an overall quality assessment.

    This function provides transparent feedback to the user on how their query
    was processed by the Advanced Parallel Hybrid RAG system, reinforcing
    the configurable nature of the AI.

    Args:
        fusion_strategy (str): The fusion strategy that was applied for the current query.
        template_type (str): The template type that was used for the response.
        metadata (dict): The complete metadata from the backend response, containing
                         confidence and quality scores.
    """
    if not metadata:
        return

    fusion_data = metadata.get('metadata', {}).get('context_fusion', {})
    confidence = fusion_data.get('final_confidence', 0)
    quality_score = fusion_data.get('quality_score', 0)

    # Strategy-specific feedback messages with detailed process descriptions
    vector_contrib = fusion_data.get('vector_contribution', 0)
    graph_contrib = fusion_data.get('graph_contribution', 0)
    
    strategy_feedback = {
        "advanced_hybrid": f"Advanced Parallel Hybrid executed simultaneous VectorRAG ({vector_contrib:.0%}) and GraphRAG ({graph_contrib:.0%}) with multi-factor fusion: complementarity analysis, quality assessment ({quality_score*100:.0f}%), and semantic coherence optimization achieving {confidence*100:.1f}% confidence",
        "weighted_linear": f"Weighted linear fusion combined VectorRAG ({vector_contrib:.0%}) and GraphRAG ({graph_contrib:.0%}) using confidence-based dynamic weighting achieving {confidence*100:.1f}% confidence with {quality_score*100:.0f}% content quality",
        "max_confidence": f"Max confidence selection chose the highest-scoring source ({('VectorRAG' if vector_contrib > graph_contrib else 'GraphRAG')}) with context enrichment achieving {confidence*100:.1f}% confidence and {quality_score*100:.0f}% quality",
        "adaptive_fusion": f"Adaptive fusion analyzed content complexity and dynamically selected optimal strategy, processing VectorRAG ({vector_contrib:.0%}) and GraphRAG ({graph_contrib:.0%}) to achieve {confidence*100:.1f}% confidence with {quality_score*100:.0f}% quality"
    }

    # Template-specific feedback messages
    template_feedback = {
        "regulatory_compliance": "Specialized for compliance queries with mine-type awareness and urgency assessment",
        "research_based": "Research methodology with source attribution and complementarity analysis",
        "comparative_analysis": "Detailed source comparison showing vector vs graph contribution breakdown",
        "confidence_weighted": f"Response tone calibrated to {get_confidence_level(confidence)} confidence level ({confidence*100:.1f}%)",
        "basic_hybrid": "Simple combination optimized for clear, direct responses"
    }

    # Display feedback in expandable section
    with st.expander("📋 Processing Summary", expanded=False):
        st.markdown("**Fusion Strategy Results:**")
        st.info(strategy_feedback.get(fusion_strategy, f"Strategy: {fusion_strategy}"))
        # Overall quality assessment
        quality_assessment = get_quality_assessment(confidence, quality_score)
        st.markdown(f"**Overall Quality:** {quality_assessment}")
# --------------------------------------------------------------------------------- end display_post_processing_feedback()

# --------------------------------------------------------------------------------- get_confidence_level()
def get_confidence_level(confidence: float) -> str:
    """Returns a descriptive string for a given numerical confidence score.

    This utility function categorizes a float confidence score into
    human-readable levels (e.g., "High", "Medium-High", "Low"),
    aiding in the interpretation of the AI's certainty.

    Args:
        confidence (float): The numerical confidence score (0.0 to 1.0).

    Returns:
        str: A descriptive string representing the confidence level.
    """
    if confidence >= 0.8:
        return "High"
    elif confidence >= 0.6:
        return "Medium-High"
    elif confidence >= 0.4:
        return "Medium"
    elif confidence >= 0.2:
        return "Low-Medium"
    else:
        return "Low"
# --------------------------------------------------------------------------------- end get_confidence_level()

# --------------------------------------------------------------------------------- get_quality_assessment()
def get_quality_assessment(confidence: float, quality_score: float) -> str:
    """Provides an overall quality assessment based on combined confidence and quality scores.

    This function calculates an average score from the confidence and quality
    metrics and provides a concise, colored assessment of the response's
    overall reliability and completeness.

    Args:
        confidence (float): The system's confidence in the response (0.0 to 1.0).
        quality_score (float): The content's quality assessment score (0.0 to 1.0).

    Returns:
        str: A string with an emoji indicating the overall quality level.
    """
    avg_score = (confidence + quality_score) / 2

    if avg_score >= 0.8:
        return "🟢 Excellent - High confidence with strong source agreement"
    elif avg_score >= 0.6:
        return "🟡 Good - Reliable information with minor uncertainties"
    elif avg_score >= 0.4:
        return "🟠 Fair - Adequate information with some limitations"
    else:
        return "🔴 Limited - Additional verification recommended"
# --------------------------------------------------------------------------------- end get_quality_assessment()

# --------------------------------------------------------------------------------- handle_processing_error()
def handle_processing_error(error: Exception, fusion_strategy: str, template_type: str) -> str:
    """Generates a user-friendly error message with troubleshooting suggestions
    and context about the configuration that led to the error.

    This function aims to guide the user towards resolving issues by providing
    actionable advice and indicating the specific processing settings that
    were in use when the error occurred.

    Args:
        error (Exception): The exception object that was caught.
        fusion_strategy (str): The fusion strategy that was attempted.
        template_type (str): The template type that was attempted.

    Returns:
        str: A formatted error message containing details and suggestions.
    """
    error_message = f"""I apologize, but I encountered an issue while processing your question with the current configuration:

**Configuration Used:**
• Fusion Strategy: `{fusion_strategy.replace('_', ' ').title()}`
• Template Type: `{template_type.replace('_', ' ').title()}`

**Error Details:** {str(error)}

**Troubleshooting Suggestions:**
• Try a different fusion strategy (Advanced Hybrid is most robust)
• Switch to Basic Hybrid template for simpler processing
• Rephrase your question to be more specific
• Use the example questions in the sidebar
• Check that the backend service is running properly

**Alternative Configurations to Try:**
• Fusion Strategy: `Advanced Hybrid` (most reliable)
• Template Type: `Basic Hybrid` (fastest processing)

If the issue persists, please check your connection and try again with a simpler configuration."""

    return error_message
# --------------------------------------------------------------------------------- end handle_processing_error()

# --------------------------------------------------------------------------------- initialize_session()
def initialize_session() -> None:
    """Initializes necessary Streamlit session state variables.

    This function ensures that 'messages' (for conversation history) and
    'example_query' (for pre-filled sidebar queries) are set up at the
    beginning of each session, preventing key errors and ensuring continuity.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": get_welcome_message()}
        ]

    if "example_query" not in st.session_state:
        st.session_state.example_query = None
# --------------------------------------------------------------------------------- end initialize_session()

# --------------------------------------------------------------------------------- main()
def main() -> None:
    """Main application function for the Streamlit UI.

    This function orchestrates the display of all UI components,
    manages the conversation flow, handles user input, and triggers
    the processing pipeline by interacting with the backend. It also
    integrates the custom CSS styling for the application.
    """
    # MRCA Configuration - Set page_config at the very top.
    # Note: st.set_page_config must be the first Streamlit command.
    st.set_page_config(
        page_title="MRCA",  
        page_icon="⛏️",
        layout="wide",
        initial_sidebar_state="auto"  # Auto-collapse on mobile devices
    )

    # Enhanced CSS for parallel hybrid with mobile responsiveness
    st.markdown("""
<style>
    /* Enhanced dark theme styling */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        /* Fix main content positioning on mobile only */
        .main .block-container {
            padding-top: 4rem !important;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Better button sizing on mobile */
        .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
        
        /* Adjust text input on mobile */
        .stTextArea textarea {
            min-height: 100px;
        }
        
        /* Compact sidebar content on mobile */
        .css-1lcbmhc {
            padding: 1rem 0.5rem;
        }
        
        /* Make sidebar header more compact on mobile */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
    }

    /* Navigation bar title */
    .stApp > header {
        background-color: #1a1a2e;
        border-bottom: 1px solid #333;
    }

    .stApp > header::before {
        content: "⛏️ MRCA - Mining Regulatory Compliance Assistant";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #fafafa;
        font-weight: 400;
        font-size: 1.1rem;
        z-index: 999;
        pointer-events: none;
    }

    /* Mobile responsive title - short version for mobile devices */
    @media (max-width: 768px) {
        .stApp > header::before {
            content: "⛏️ MRCA";
        }
    }

    /* Main header with advanced gradient */
    .main-header {
        background: linear-gradient(135deg, #1a2d1a 0%, #16213e 50%, #0f1419 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: -1rem;
        margin-bottom: 2rem;
        border: 1px solid #4a904a;
        box-shadow: 0 4px 6px rgba(74, 144, 74, 0.3);
    }
    .main-header h1 {
        color: #fafafa;
        margin: 0;
        text-align: center;
        font-weight: 600;
        font-size: 2.2rem;
    }
    .main-header p {
        color: #b3d9b3;
        margin: 0.8rem 0 0 0;
        text-align: center;
        font-size: 1.1rem;
    }

    /* Configuration panel styling */
    .config-panel {
        background: linear-gradient(135deg, #1a2d1a 0%, #2d3a2d 100%);
        border: 1px solid #4a904a;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Modern disclaimer styling */
    .disclaimer {
        background: linear-gradient(135deg, #2d1b1b 0%, #3d2626 100%);
        border: 1px solid #5d3a3a;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .disclaimer h4 {
        color: #ff9999;
        margin-top: 0;
        font-weight: 600;
    }
    .disclaimer p {
        color: #e6cccc;
        margin-bottom: 0;
        line-height: 1.5;
    }

    /* Stats box with modern dark styling */
    .stats-box {
        background: linear-gradient(135deg, #262730 0%, #2d2d3a 100%);
        border: 1px solid #3d3d4d;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        color: #fafafa;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Feature highlight with accent */
    .feature-highlight {
        background: linear-gradient(135deg, #1a2d1a 0%, #2d3a2d 100%);
        border-left: 4px solid #4a904a;
        border-radius: 0 8px 8px 0;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #e6f3e6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Selectbox and input styling */
    .stSelectbox > div > div {
        background-color: #262730;
        border: 1px solid #4a904a;
        border-radius: 6px;
    }

    .stTextInput > div > div > input {
        background-color: #262730;
        border: 1px solid #4a904a;
        border-radius: 6px;
        color: #fafafa;
    }

    /* Metric containers */
    .metric-container {
        background: linear-gradient(135deg, #262730 0%, #2d2d3a 100%);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #3d3d4d;
        margin: 0.5rem 0;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #262730;
        border-radius: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #b3b3b3;
        background-color: transparent;
        border-radius: 6px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4a904a;
        color: white;
    }

    /* Button styling improvements */
    .stButton > button {
        background: linear-gradient(135deg, #262730 0%, #2d2d3a 100%);
        color: #fafafa;
        border: 1px solid #4a904a;
        border-radius: 66px;
        transition: all 0.3s ease;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 12px !important;
        display: flex !important;
        align-items: center !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4a904a 0%, #5ba05b 100%);
        border-color: #6bb06b;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(106, 176, 106, 0.2);
    }

    /* Sidebar improvements */
    section[data-testid="stSidebar"] {
        background-color: #1a1a2e;
        border-right: 1px solid #333;
    }

    /* Chat message improvements */
    .stChatMessage {
        background-color: #262730;
        border: 1px solid #3d3d4d;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
    """, unsafe_allow_html=True)


    # Initialize session
    initialize_session()

    # Display header and sidebar
    display_header()
    display_sidebar()
    display_disclaimer()

    # Configuration panel
    display_parallel_hybrid_config()
    

    
    # Display conversation history in main area
    for message in st.session_state.messages:
        metadata = message.get("metadata")
        
        # Special handling for welcome message - display in expandable container
        if (message['role'] == 'assistant' and
            message['content'].startswith("**MRCA - APH-IF Beta v2.0**")):

            with st.chat_message("assistant"):
                with st.expander("Welcome to MRCA Beta v2.0 - Advanced Parallel Hybrid - Intelligent Fusion!", expanded=False):
                    st.markdown(message['content'])
        else:
            write_message(message['role'], message['content'], save=False, metadata=metadata)

    # Handle example query from sidebar
    if st.session_state.example_query:
        handle_submit(st.session_state.example_query)
        st.session_state.example_query = None
        st.rerun()

    # Chat input with mobile-friendly placeholder
    placeholder_text = "Ask me about MSHA regulations and mining safety..."
    if question := st.chat_input(placeholder_text):
        handle_submit(question)
# --------------------------------------------------------------------------------- end main()

# =========================================================================
# Module Initialization 
# =========================================================================
# This block runs only when the file is executed directly, not when imported.

if __name__ == "__main__":
    # --- Streamlit Application Entry Point ---
    # The main function encapsulates the Streamlit app logic.
    # When this script is run with 'streamlit run', Streamlit takes over execution.
    main()

# =========================================================================
# End of File
# =========================================================================