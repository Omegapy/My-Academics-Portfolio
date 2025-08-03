# -------------------------------------------------------------------------
# File: llm.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/llm.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module provides centralized LLM (Large Language Model) and embeddings management
# for the MRCA backend system. It implements lazy loading patterns for OpenAI GPT-4o
# and Google Gemini embeddings to ensure proper resource management and resilience.
# The module handles configuration validation, environment setup, and provides
# factory functions for creating LLM and embeddings instances used throughout
# the Advanced Parallel Hybrid system.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: validate_openai_config() - Validates OpenAI API configuration
# - Function: get_llm() - Factory function for OpenAI ChatGPT instance
# - Function: validate_gemini_config() - Validates Gemini API configuration
# - Function: get_embeddings() - Factory function for Gemini embeddings instance
# - Class: LazyLLM - Lazy loading wrapper for LLM instance
# - Class: LazyEmbeddings - Lazy loading wrapper for embeddings instance
# - Global Variable: llm - Lazy-loaded LLM instance for backwards compatibility
# - Global Variable: embeddings - Lazy-loaded embeddings instance for backwards compatibility
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - logging: For error logging and debugging
#   - os: For environment variable management (imported dynamically)
# - Third-Party:
#   - langchain_openai.ChatOpenAI: OpenAI GPT integration for LLM functionality
#   - langchain_google_genai.GoogleGenerativeAIEmbeddings: Google Gemini embeddings
# - Local Project Modules:
#   - .config.init_config: Configuration management for API keys and model settings
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This module is imported by various components requiring LLM or embeddings functionality:
# - parallel_hybrid.py: Uses LLM for response generation
# - tools/cypher.py: Uses LLM for Cypher query generation
# - tools/vector.py: Uses embeddings for semantic similarity search
# - tools/general.py: Uses LLM for general query processing
# The lazy loading pattern ensures instances are only created when needed,
# improving startup performance and error resilience.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""

Centralized LLM and Embeddings Management for MRCA Advanced Parallel Hybrid System

Provides lazy loading patterns and factory functions for OpenAI GPT-4o and Google Gemini
embeddings to ensure proper resource management, configuration validation, and resilience
across the Mining Regulatory Compliance Assistant backend system.

"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import logging
import os

# Third-party library imports
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

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

# ------------------------------------------------------------------------- validate_openai_config()
def validate_openai_config() -> tuple:
    """Validate OpenAI configuration and provide helpful error messages.

    This function checks that the OpenAI API key is properly configured and
    follows the expected format. It validates both the presence and format
    of the API key to prevent runtime errors during LLM initialization.

    Returns:
        tuple: A tuple containing (api_key, model) if validation succeeds.

    Raises:
        ValueError: If API key is missing or has invalid format.

    Examples:
        >>> api_key, model = validate_openai_config()
        >>> print(f"Using model: {model}")
        Using model: gpt-4o
    """
    config = init_config()
    
    if not config.openai_api_key:
        error_msg = "Missing OpenAI API key in configuration"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    if not config.openai_api_key.startswith("sk-"):
        error_msg = "Invalid OpenAI API key format"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    return config.openai_api_key, config.openai_model
# ------------------------------------------------------------------------- end validate_openai_config()

# ------------------------------------------------------------------------- validate_gemini_config()
def validate_gemini_config() -> str:
    """Validate Gemini configuration for embeddings.

    This function checks that the Google Gemini API key is properly configured
    for use with the embeddings functionality. It ensures the API key is
    available before attempting to create embeddings instances.

    Returns:
        str: The validated Gemini API key.

    Raises:
        ValueError: If API key is missing or invalid.

    Examples:
        >>> api_key = validate_gemini_config()
        >>> print("Gemini API key validated successfully")
        Gemini API key validated successfully
    """
    config = init_config()
    
    if not config.gemini_api_key:
        error_msg = "GEMINI_API_KEY not found in configuration"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    if not config.gemini_api_key:
        error_msg = "Invalid Gemini API key"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    return config.gemini_api_key
# ------------------------------------------------------------------------- end validate_gemini_config()

# ---------------------------------------------
# --- Callable Functions from other modules ---
# ---------------------------------------------

# ------------------------------------------------------------------------- get_llm()
def get_llm():
    """Lazy loading function to get OpenAI LLM.

    Creates LLM instance only when needed for better resilience.
    This function provides a factory pattern for creating ChatOpenAI instances
    with optimized settings for the MRCA system's query processing needs.

    Returns:
        ChatOpenAI: Configured OpenAI LLM instance with GPT-4o model.

    Raises:
        Exception: If LLM initialization fails due to configuration or network issues.

    Examples:
        >>> llm_instance = get_llm()
        >>> response = llm_instance.invoke("What is Title 30 CFR?")
        >>> print(response.content)
    """
    try:
        api_key, model = validate_openai_config()
        # Set environment variable for OpenAI
        os.environ["OPENAI_API_KEY"] = api_key
        
        return ChatOpenAI(
            model=model,  # Should be "gpt-4o"
            temperature=0,  # Low temperature for consistent Cypher generation
            max_completion_tokens=4096,  # Limit output tokens
            timeout=60,  # Increase timeout for complex queries
        )
    except Exception as e:
        logger.error(f"OpenAI LLM initialization error: {str(e)}")
        raise
# ------------------------------------------------------------------------- end get_llm()

# ------------------------------------------------------------------------- get_embeddings()
def get_embeddings():
    """Lazy loading function to get Gemini embeddings.

    Creates embeddings instance only when needed for better resilience.
    Uses same model as graph building for consistency.
    This function provides consistent embeddings for semantic similarity operations
    across the vector search components.

    Returns:
        GoogleGenerativeAIEmbeddings: Configured Gemini embeddings instance (768 dimensions).

    Raises:
        Exception: If embeddings initialization fails due to configuration or network issues.

    Examples:
        >>> embeddings_instance = get_embeddings()
        >>> vectors = embeddings_instance.embed_documents(["safety regulations"])
        >>> print(f"Vector dimension: {len(vectors[0])}")
        Vector dimension: 768
    """
    try:
        api_key = validate_gemini_config()

        # Set environment variable for Google AI models
        os.environ["GOOGLE_API_KEY"] = api_key
        
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"  # Same as used in build_hybrid_store.py (768 dimensions)
        )
    except Exception as e:
        logger.error(f"Gemini embeddings initialization error: {str(e)}")
        raise
# ------------------------------------------------------------------------- end get_embeddings()

# =========================================================================
# Class Definitions
# =========================================================================

# ------------------------------------------------------------------------- class LazyLLM
class LazyLLM:
    """Lazy loading wrapper for LLM instance.

    This class implements a lazy loading pattern that delays LLM initialization
    until the instance is actually used. This improves startup performance and
    provides better error handling by deferring potential connection issues
    until the LLM is actually needed.

    Class Attributes:
        None

    Instance Attributes:
        _llm (ChatOpenAI): The underlying LLM instance, initialized on first access.

    Methods:
        __getattr__(): Proxies attribute access to the underlying LLM instance.
    """
    
    # -------------------
    # --- Constructor ---
    # -------------------
    
    # ------------------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initializes the LazyLLM wrapper.

        Creates a wrapper instance without immediately initializing the underlying
        LLM. The actual LLM creation is deferred until first attribute access.
        """
        self._llm = None
    # ------------------------------------------------------------------------- end __init__()

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # ------------------------------------------------------------------------- __getattr__()
    def __getattr__(self, name):
        """Proxies attribute access to the underlying LLM instance.

        This method implements the lazy loading by creating the LLM instance
        on first attribute access and then delegating all subsequent calls
        to the actual LLM object.

        Args:
            name (str): The attribute or method name being accessed.

        Returns:
            Any: The result of the attribute access on the underlying LLM instance.
        """
        if self._llm is None:
            self._llm = get_llm()
        return getattr(self._llm, name)
    # ------------------------------------------------------------------------- end __getattr__()
# ------------------------------------------------------------------------- end class LazyLLM

# ------------------------------------------------------------------------- class LazyEmbeddings
class LazyEmbeddings:
    """Lazy loading wrapper for embeddings instance.

    This class implements a lazy loading pattern that delays embeddings initialization
    until the instance is actually used. This improves startup performance and
    provides better error handling by deferring potential connection issues
    until the embeddings are actually needed.

    Class Attributes:
        None

    Instance Attributes:
        _embeddings (GoogleGenerativeAIEmbeddings): The underlying embeddings instance.

    Methods:
        __getattr__(): Proxies attribute access to the underlying embeddings instance.
    """
    
    # -------------------
    # --- Constructor ---
    # -------------------
    
    # ------------------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initializes the LazyEmbeddings wrapper.

        Creates a wrapper instance without immediately initializing the underlying
        embeddings. The actual embeddings creation is deferred until first attribute access.
        """
        self._embeddings = None
    # ------------------------------------------------------------------------- end __init__()

    # ---------------------------------------------
    # --- Internal/Private Methods ---
    # ---------------------------------------------
    
    # ------------------------------------------------------------------------- __getattr__()
    def __getattr__(self, name):
        """Proxies attribute access to the underlying embeddings instance.

        This method implements the lazy loading by creating the embeddings instance
        on first attribute access and then delegating all subsequent calls
        to the actual embeddings object.

        Args:
            name (str): The attribute or method name being accessed.

        Returns:
            Any: The result of the attribute access on the underlying embeddings instance.
        """
        if self._embeddings is None:
            self._embeddings = get_embeddings()
        return getattr(self._embeddings, name)
    # ------------------------------------------------------------------------- end __getattr__()

# ------------------------------------------------------------------------- end class LazyEmbeddings

# =========================================================================
# Module Initialization / Global Variables
# =========================================================================
# Backwards compatibility - create instances when accessed
# This allows existing code to work while providing lazy loading benefits

# Global lazy-loaded LLM instance for module-level access
llm = LazyLLM()

# Global lazy-loaded embeddings instance for module-level access  
embeddings = LazyEmbeddings()

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This module is designed to be imported, not executed directly.
# No main execution guard is needed.

# =========================================================================
# End of File
# =========================================================================