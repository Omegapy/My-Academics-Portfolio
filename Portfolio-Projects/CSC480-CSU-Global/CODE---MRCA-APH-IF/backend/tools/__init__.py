# -------------------------------------------------------------------------
# File: __init__.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: backend/tools/__init__.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# This module serves as the package initialization file for the MRCA tools package.
# It provides various agent tools for querying the MSHA regulatory knowledge graph
# through different retrieval methods including VectorRAG, GraphRAG, and general
# query processing. The package contains specialized tools that implement the
# core retrieval functionality used by the Advanced Parallel Hybrid system.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Package: tools - Contains agent tools for regulatory knowledge graph querying
# - Module: cypher.py - Cypher query generation and GraphRAG functionality
# - Module: vector.py - Vector similarity search and VectorRAG functionality
# - Module: general.py - General query processing and fallback functionality
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: None (package initialization file)
# - Third-Party: None (package initialization file)
# - Local Project Modules: None (package initialization file)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This package is imported by various MRCA backend components:
# - parallel_hybrid.py: Uses tools for parallel VectorRAG and GraphRAG execution
# - main.py: May import tools for API endpoint functionality
# - Other backend modules requiring regulatory knowledge graph access
# The tools package provides the core retrieval functionality for the
# Advanced Parallel Hybrid system's query processing capabilities.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
Tools package for MRCA application.

This package contains various agent tools for querying the MSHA regulatory 
knowledge graph through different retrieval methods including VectorRAG, 
GraphRAG, and general query processing capabilities.
"""

# =========================================================================
# Package Information
# =========================================================================
__version__ = "2.0.0"
__description__ = "MRCA Advanced Parallel Hybrid Tools Package"

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================
# This is a package initialization file, no main execution guard needed.

# --------------------------------------------------------------------------------- 