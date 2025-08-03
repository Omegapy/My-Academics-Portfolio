# -------------------------------------------------------------------------
# File: __init__.py
# Project: MRCA - Testing Infrastructure  
# Author: Testing Team
# Date: 2025-01-19 (Creation Date)
# Last Modified: 2025-01-19
# File Path: tests/e2e/__init__.py
# -------------------------------------------------------------------------

# --- Module Objective ---
# Package initialization for End-to-End (E2E) tests directory
# This module defines constants, shared utilities, and package-level configuration
# for comprehensive end-to-end testing of the MRCA application workflows.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2025 Alexander Samuel Ricciardi
# SPDX-License-Identifier: Apache-2.0
# -------------------------------------------------------------------------

"""
End-to-End Testing Package

This package contains comprehensive end-to-end tests that validate complete
user workflows through the MRCA Advanced Parallel Hybrid system.
"""

# =========================================================================
# Package Constants
# =========================================================================

# Test configuration constants
E2E_TEST_TIMEOUT = 240  # seconds (updated for LLM calls)
DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_FRONTEND_URL = "http://localhost:8501"

# Test data constants
SAMPLE_QUERIES = [
    "What are methane monitoring requirements?",
    "What are ventilation standards for underground mines?", 
    "What are the requirements for coal dust control?",
    "What safety equipment is required for miners?",
    "What are the emergency evacuation procedures?"
]

# Expected response patterns
EXPECTED_RESPONSE_INDICATORS = [
    "CFR",  # Code of Federal Regulations
    "30 CFR",  # Title 30 CFR
    "MSHA",  # Mine Safety and Health Administration
    "requirement",
    "regulation",
    "safety",
    "mining"
]

# =========================================================================
# End of File
# ========================================================================= 