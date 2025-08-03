# -------------------------------------------------------------------------
# File: __init__.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-19 (Creation Date)
# Last Modified: 2025-01-19
# File Path: tests/unit/__init__.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Package initialization for Unit tests directory within the MRCA testing framework.
# This module defines constants, shared utilities, and package-level configuration
# for comprehensive unit testing including individual component validation,
# mock testing scenarios, and isolated functionality testing.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Package initialization for unit tests
# - Test constants and shared utilities for unit validation
# - Mock object configuration and testing patterns
# - Individual component testing constants and helpers
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: None (package initialization only)
# - Third-Party: None (package initialization only)  
# - Local Project Modules: References parent testing framework constants
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This package initialization module is imported automatically when the
# unit tests package is accessed. It provides shared constants and utilities
# for unit-level testing of individual MRCA components including backend
# modules, configuration, database, LLM, tools, and utility functions.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Unit Tests Package

Package initialization for unit-level testing of the MRCA Advanced
Parallel Hybrid system. Provides shared utilities and constants for validating
individual components in isolation with comprehensive mock testing support.
"""

# =========================================================================
# Package Constants
# =========================================================================

# Unit test configuration
UNIT_TEST_TIMEOUT = 240  # seconds for unit tests (updated for LLM calls)
MOCK_RESPONSE_DELAY = 0.1  # seconds for mock response simulation
UNIT_TEST_ITERATIONS = 5  # default iterations for statistical validation

# Mock testing constants
MOCK_API_KEYS = {
    "openai": "sk-test-mock-openai-key-for-unit-testing",
    "gemini": "mock-gemini-api-key-for-unit-testing"
}

MOCK_DATABASE_CONFIG = {
    "neo4j_uri": "neo4j+s://mock.databases.neo4j.io",
    "neo4j_username": "neo4j",
    "neo4j_password": "mock-password"
}

# Unit test validation patterns
UNIT_TEST_PATTERNS = {
    "config_validation": "Missing.*configuration",
    "llm_validation": "Mock LLM response",
    "database_validation": "Mock.*query.*result",
    "vector_validation": "Mock vector search",
    "graph_validation": "Mock.*graph.*query"
}

# Component test modules
UNIT_TEST_MODULES = [
    "test_circuit_breaker",
    "test_config", 
    "test_context_fusion",
    "test_database",
    "test_graph",
    "test_hybrid_templates",
    "test_llm",
    "test_parallel_hybrid",
    "test_tools",
    "test_utils"
]

# Mock object creation helpers
MOCK_CREATION_PATTERNS = {
    "llm_mock": "Mock LLM instance with invoke method",
    "embeddings_mock": "Mock embeddings with embed_query method",
    "graph_mock": "Mock graph with query and get_schema methods",
    "config_mock": "Mock configuration with all required attributes"
}

# Unit test success criteria
UNIT_TEST_CRITERIA = {
    "mock_validation": True,
    "isolation_verification": True,
    "error_handling_coverage": True,
    "edge_case_testing": True
}

# =========================================================================
# End of File
# ========================================================================= 