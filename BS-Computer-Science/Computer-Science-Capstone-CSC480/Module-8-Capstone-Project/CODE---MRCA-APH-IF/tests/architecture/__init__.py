# -------------------------------------------------------------------------
# File: __init__.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-19 (Creation Date)
# Last Modified: 2025-01-19
# File Path: tests/architecture/__init__.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Package initialization for Architecture tests directory within the MRCA testing framework.
# This module defines constants, shared utilities, and package-level configuration
# for comprehensive architecture testing including confidence validation,
# hallucination prevention, and overall system architecture evaluation.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Package initialization for architecture tests
# - Test constants and shared utilities for architecture validation
# - ASR (Architecture Significant Requirements) validation constants
# - Configuration for architecture-level testing scenarios
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: None (package initialization only)
# - Third-Party: None (package initialization only)  
# - Local Project Modules: References parent testing framework constants
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This package initialization module is imported automatically when the
# architecture tests package is accessed. It provides shared constants and
# utilities for architecture-level tests including Test Case 5 (Confidence
# Score & Hallucination prevention) and other ASR validation scenarios.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Architecture Tests Package

Package initialization for architecture-level testing of the MRCA Advanced
Parallel Hybrid system. Provides shared utilities and constants for validating
Architecture Significant Requirements (ASRs) and system-level behavior.
"""

# =========================================================================
# Package Constants
# =========================================================================

# Architecture test configuration
ARCHITECTURE_TEST_TIMEOUT = 60  # seconds for architecture tests
CONFIDENCE_VALIDATION_THRESHOLD = 0.85  # minimum confidence for architecture tests
HALLUCINATION_DETECTION_SAMPLES = 10  # number of samples for hallucination testing

# ASR validation constants (from Module 6 testing plan)
ASR_CONFIDENCE_THRESHOLDS = {
    "min_single_source": 0.85,
    "min_fusion": 0.70,
    "min_final": 0.90
}

# Off-domain query samples for architecture testing
ARCHITECTURE_OFF_DOMAIN_SAMPLES = [
    "What sound does a dog make?",
    "How do I cook pasta?", 
    "What's the weather forecast?"
]

# Architecture test markers
ARCHITECTURE_TEST_MARKERS = [
    "architecture",
    "confidence_validation", 
    "hallucination_prevention",
    "asr_validation"
]

# =========================================================================
# End of File
# ========================================================================= 