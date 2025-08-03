# -------------------------------------------------------------------------
# File: __init__.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-19 (Creation Date)
# Last Modified: 2025-01-19
# File Path: tests/reliability/__init__.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Package initialization for Reliability tests directory within the MRCA testing framework.
# This module defines constants, shared utilities, and package-level configuration
# for comprehensive reliability testing including fault injection, load testing,
# circuit breaker validation, and degraded service scenarios.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Package initialization for reliability tests
# - Test constants and shared utilities for reliability validation
# - Circuit breaker and fault injection testing configuration
# - Load testing and degraded service testing constants
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: None (package initialization only)
# - Third-Party: None (package initialization only)  
# - Local Project Modules: References parent testing framework constants
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This package initialization module is imported automatically when the
# reliability tests package is accessed. It provides shared constants and
# utilities for reliability testing including Test Case 3 (Degraded Services)
# and Test Case 4 (Load Testing with Fault Injection) validation scenarios.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Reliability Tests Package

Package initialization for reliability-level testing of the MRCA Advanced
Parallel Hybrid system. Provides shared utilities and constants for validating
system resilience, fault tolerance, and performance under degraded conditions.
"""

# =========================================================================
# Package Constants
# =========================================================================

# Reliability test configuration
RELIABILITY_TEST_TIMEOUT = 240  # seconds for reliability tests (updated for LLM calls)
FAULT_INJECTION_PROBABILITY = 0.3  # default fault injection rate
LOAD_TEST_DURATION = 30  # seconds for load testing scenarios
CIRCUIT_BREAKER_TEST_THRESHOLD = 3  # failures to trigger circuit breaker

# Service degradation test scenarios
DEGRADATION_SCENARIOS = [
    "neo4j_downtime",
    "llm_api_failure", 
    "slow_service_timeout",
    "network_connectivity_issues",
    "multiple_service_failures"
]

# Load testing configuration
LOAD_TEST_CONFIG = {
    "concurrent_users": 5,
    "requests_per_user": 3,
    "max_response_time": 60.0,  # seconds
    "expected_error_rate_threshold": 0.3
}

# Circuit breaker service targets
CIRCUIT_BREAKER_SERVICES = [
    "neo4j_service",
    "openai_service", 
    "gemini_service",
    "api_service"
]

# Fault injection patterns
FAULT_INJECTION_TYPES = [
    "timeout",
    "connection_error", 
    "malformed_payload",
    "invalid_endpoint",
    "service_unavailable"
]

# Reliability test validation thresholds
RELIABILITY_THRESHOLDS = {
    "degraded_service_recovery_time": 5.0,  # seconds
    "load_test_success_rate": 0.7,  # minimum success rate under load
    "circuit_breaker_response_time": 1.0,  # seconds for circuit breaker activation
    "fault_tolerance_threshold": 0.8  # minimum system availability during faults
}

# =========================================================================
# End of File
# ========================================================================= 