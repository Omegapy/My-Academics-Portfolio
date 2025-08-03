# -------------------------------------------------------------------------
# File: __init__.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-19 (Creation Date)
# Last Modified: 2025-01-19
# File Path: tests/integration/__init__.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Package initialization for Integration tests directory within the MRCA testing framework.
# This module defines constants, shared utilities, and package-level configuration
# for comprehensive integration testing including component interaction validation,
# multi-domain query testing, and regulatory citation retrieval scenarios.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Package initialization for integration tests
# - Test constants and shared utilities for integration validation
# - Component interaction testing configuration
# - Multi-domain and citation retrieval testing constants
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: None (package initialization only)
# - Third-Party: None (package initialization only)  
# - Local Project Modules: References parent testing framework constants
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This package initialization module is imported automatically when the
# integration tests package is accessed. It provides shared constants and
# utilities for integration testing including Test Case 1 (Regulatory Citation
# Retrieval) and Test Case 2 (Multi-Domain Query) validation scenarios.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Integration Tests Package

Package initialization for integration-level testing of the MRCA Advanced
Parallel Hybrid system. Provides shared utilities and constants for validating
component interactions, multi-domain queries, and regulatory citation retrieval.
"""

# =========================================================================
# Package Constants
# =========================================================================

# Integration test configuration
INTEGRATION_TEST_TIMEOUT = 240  # seconds for integration tests (updated for LLM calls)
COMPONENT_HEALTH_CHECK_TIMEOUT = 240  # seconds for component health validation (updated for LLM calls)
MULTI_DOMAIN_FUSION_THRESHOLD = 0.70  # minimum fusion quality for multi-domain tests

# Component integration test endpoints
INTEGRATION_TEST_ENDPOINTS = {
    "vector_search": "/tools/vector/search",
    "graph_query": "/tools/cypher/query", 
    "parallel_hybrid": "/generate_parallel_hybrid",
    "health_check": "/parallel_hybrid/health"
}

# Multi-domain test query samples
MULTI_DOMAIN_TEST_QUERIES = [
    "What are the regulations for underground drilling generating silica dust near diesel equipment?",
    "What safety training and PPE requirements apply to miners working with explosives?",
    "How do methane monitoring requirements interact with electrical equipment grounding?"
]

# Citation retrieval test samples
CITATION_TEST_QUERIES = [
    "What does 30 CFR 56.12016 say about grounding of electrical equipment?",
    "Tell me about 30 CFR 75.380 methane monitoring requirements",
    "What are the requirements in 30 CFR 56.5005 for safety training?"
]

# Integration test validation thresholds
INTEGRATION_THRESHOLDS = {
    "citation_confidence": 0.85,
    "multi_domain_fusion": 0.70,
    "component_response_time": 35.0,  # seconds
    "p95_response_time": 5.0  # seconds
}

# =========================================================================
# End of File
# ========================================================================= 