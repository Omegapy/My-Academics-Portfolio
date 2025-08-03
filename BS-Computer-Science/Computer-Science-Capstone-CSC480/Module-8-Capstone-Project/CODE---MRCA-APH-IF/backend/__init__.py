# File: stop_services.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: stop_services.py
# ------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
MRCA Backend Package - Advanced Parallel Hybrid System

This package contains the core backend services for the Mining Regulatory Compliance Assistant (MRCA).
It implements the Advanced Parallel Hybrid technology that combines VectorRAG and GraphRAG 
with research-based context fusion for superior regulatory query processing.

Core Components:
- parallel_hybrid.py: Simultaneous VectorRAG + GraphRAG execution engine
- context_fusion.py: Research-based fusion algorithms (4 strategies)  
- hybrid_templates.py: Advanced prompt templates (5 types)
- tools/: VectorRAG, GraphRAG, and General query tools
- main.py: FastAPI server with Advanced Parallel Hybrid endpoints

Architecture:
- Service-based design with HTTP API
- Async parallel processing using ThreadPoolExecutor
- Circuit breaker patterns for resilience
- Health monitoring and performance analytics
- Neo4j knowledge graph + OpenAI/Gemini LLM integration

Version: 2.0.0 (Advanced Parallel Hybrid System)
"""

__version__ = "2.0.0"
__title__ = "MRCA Backend - Advanced Parallel Hybrid System"

# Core engine exports for easier importing
from .parallel_hybrid import get_parallel_engine, ParallelRetrievalEngine
from .context_fusion import get_fusion_engine, HybridContextFusion, FusionStrategy
from .hybrid_templates import get_template_engine, TemplateType, TemplateConfig

# Configuration and utilities
from .config import get_config
from .llm import get_llm
from .graph import get_graph

# Health and monitoring
from .database import database_health_check
from .circuit_breaker import CircuitBreaker

__all__ = [
    # Core engines
    "get_parallel_engine", "ParallelRetrievalEngine",
    "get_fusion_engine", "HybridContextFusion", "FusionStrategy", 
    "get_template_engine", "TemplateType", "TemplateConfig",
    
    # Infrastructure
    "get_config", "get_llm", "get_graph",
    "database_health_check", "CircuitBreaker",
] 