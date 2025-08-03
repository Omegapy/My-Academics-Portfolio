# -------------------------------------------------------------------------
# File: __init__.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25 
# File Path: tests/__init__.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Tests package initialization for the MRCA testing framework.
# Provides shared testing utilities, constants, and imports for all test modules.
# Maintains separation between production tests and formal testing framework.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
MRCA Testing Framework

This package contains formal tests for the Mining Regulatory Compliance Assistant.
These tests complement the existing operational tests embedded in production modules.

Test Categories:
- Unit Tests: Individual component testing
- Integration Tests: Component interaction testing  
- End-to-End Tests: Complete workflow testing
- Reliability Tests: Fault injection and resilience testing
- Architecture Tests: ASR validation and performance testing

Usage:
    pytest tests/                    # Run all tests
    pytest tests/unit/               # Run unit tests only
    pytest -m "unit and not slow"    # Run fast unit tests
    pytest -m requires_neo4j         # Run tests needing Neo4j
"""

# Testing framework version
__version__ = "1.0.0"

# Test configuration constants
TEST_TIMEOUT_SHORT = 240    # Short operations (seconds) - Updated for LLM calls
TEST_TIMEOUT_MEDIUM = 240   # Medium operations (seconds) - Updated for LLM calls
TEST_TIMEOUT_LONG = 240     # Long operations (seconds) - Updated for LLM calls

# Test data constants
SAMPLE_CFR_QUERIES = [
    "What are methane monitoring requirements?",
    "What does 30 CFR 56.12016 say about grounding?",
    "What are the regulations for underground drilling generating silica dust?"
]

SAMPLE_OFF_DOMAIN_QUERIES = [
    "What sound does a dog make?",
    "How do I cook pasta?",
    "What's the weather today?"
]

# ASR validation thresholds (from Module 6 testing plan)
ASR_THRESHOLDS = {
    "min_confidence_single_source": 0.85,
    "min_confidence_fusion": 0.70,
    "max_response_time_p95": 45.0,      # seconds - adjusted for complex parallel hybrid queries with rate limiting
    "max_response_time_normal": 45.0,   # seconds
    "min_final_confidence": 0.90
}

# Health check constants
HEALTH_CHECK_ENDPOINTS = {
    "backend_basic": "http://localhost:8000/health",
    "backend_detailed": "http://localhost:8000/parallel_hybrid/health",
    "frontend": "http://localhost:8501/_stcore/health"
}

# Circuit breaker test constants
CIRCUIT_BREAKER_SERVICES = [
    "neo4j_service",
    "openai_service", 
    "gemini_service"
]

# =========================================================================
# End of File
# ========================================================================= 