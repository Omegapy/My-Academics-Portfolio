"""
MRCA Build Data Package

This package contains utilities for building the MRCA knowledge graph and vector store.
It includes data collection, processing, and graph construction tools.

Components:
- cfr_downloader: Downloads Title 30 CFR PDFs from govinfo.gov
- build_hybrid_store: Builds Neo4j knowledge graph and vector embeddings
- build_graph_debug: Debug utilities for graph construction
"""

from .cfr_downloader import CFRDownloader
from .build_hybrid_store import HybridStoreBuilder

__version__ = "2.0.0"
__author__ = "MRCA Development Team"

# Package exports
__all__ = [
    "CFRDownloader",
    "HybridStoreBuilder",
]

# Package metadata
PACKAGE_INFO = {
    "name": "build_data",
    "version": __version__,
    "description": "MRCA Knowledge Graph and Vector Store Building Tools",
    "components": [
        "cfr_downloader - CFR PDF downloading utilities",
        "build_hybrid_store - Neo4j graph and vector construction",
        "build_graph_debug - Debug and validation tools"
    ]
} 