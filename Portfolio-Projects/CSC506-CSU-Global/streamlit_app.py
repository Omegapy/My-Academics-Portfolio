# File: streamlit_app.py \
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
# Project: Portfolio Module 8 - Algorithm and Data Structure Comparison Tool
# File Path: Portfolio-Module-8/streamlit_app.py
# -------------------------------------------------------------------------
# Assignment:
# Portfolio Module 8 - Final integrated portfolio application.
# Directions:
# - Present all integrated Module 8 feature areas in one Streamlit interface.
# - Route each tab to its adapted assignment or portfolio milestone renderer.
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Configure the root Streamlit page for the integrated portfolio tool.
# - Route each tab to the matching assignment or milestone module renderer.
# - Render the comprehensive analysis artifact when it is available.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# ROOT APPLICATION:
#   - Constant: APP_TITLE - Display title for the Streamlit app
#   - Function: _render_header() - Shared root page heading
#   - Function: _package_has_files() - Package population check helper
#   - Function: _render_pending_module() - Placeholder module warning helper
#   - Function: _render_markdown_file() - Markdown artifact renderer
#   - Top-level tabs - Overview, modules, and comprehensive analysis
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: pathlib, sys
# - Third-Party: streamlit
# - Local Project Modules: module overview_page renderers
# --- Requirements ---
# - Python 3.12+
# - Streamlit runtime launched with this file as the app target
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Run with: streamlit run Portfolio-Module-8/streamlit_app.py
# Streamlit executes this file top-level, so no __main__ guard is used.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit application entry point for the web application
   Algorithm and Data Structure Comparison Tool.

Launch with:

    streamlit run Portfolio-Module-8/streamlit_app.py
"""

from __future__ import annotations

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from pathlib import Path
import sys

import streamlit as st


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# PATHS AND PAGE CONFIGURATION
# ========================================================================

# Paths and page configuration for the web application
_PORTFOLIO_ROOT = Path(__file__).resolve().parent
_COMPREHENSIVE_ANALYSIS_PATH = (
    _PORTFOLIO_ROOT / "analysis" / "comprehensive_performance_analysis.md"
)
APP_TITLE = "Algorithm and Data Structure Comparison Tool"

# Setup: root directory path to python import path for local modules to be imported
if str(_PORTFOLIO_ROOT) not in sys.path:
    sys.path.insert(0, str(_PORTFOLIO_ROOT))
# import all module overview pages
from bubble_quickselect_module.overview_page import (  # noqa: E402
    render_bubble_quickselect_sets_page,
)
# import graph algorithms module overview page
from graph_algorithms_module.overview_page import render_graph_algorithms_page  # noqa: E402
# import hash priority module overview page
from hash_priority_module.overview_page import render_hash_priority_page  # noqa: E402
# import linked structures module overview page
from linked_structures_module.overview_page import (  # noqa: E402
    render_linked_structures_page,
)   
# import search comparison module overview page
from search_comparison_module.overview_page import (  # noqa: E402
    render_search_comparison_page,
)
# import tree map module overview page
from tree_map_module.overview_page import render_tree_map_page  # noqa: E402

# SETUP: configure the root page before rendering any visible Streamlit elements.
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=_PORTFOLIO_ROOT / "icon.png",
    layout="wide",
)


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# RENDER HELPERS
# ========================================================================
# Contains small display helpers used by the root portfolio app.
#
# UI DISPLAY OVERVIEW:
# Root helpers render the shared header, inspect package availability, and show
# Markdown artifacts or missing-artifact messages.
# =========================================================================
# - Function: _render_header()
# - Function: _package_has_files()
# - Function: _render_pending_module()
# - Function: _render_markdown_file()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- _render_header()
def _render_header() -> None:
    """Render the root portfolio header.

    Returns:
        None.
    """
    st.title(APP_TITLE)
    st.caption(
        "CSC506 Design and Analysis of Algorithms | "
        "Professor Dr. Jonathan Vanover | Spring A 2026 | "
        "Student: Alexander Ricciardi"
    )
    st.divider()
# --------------------------------------------------------------- end _render_header()


# --------------------------------------------------------------- _package_has_files()
def _package_has_files(package_name: str) -> bool:
    """Return whether a Module 8 package directory contains source files.

    Args:
        package_name: Root-level Module 8 package directory name.

    Returns:
        True when the package has at least one Python source file.
    """
    package_dir = _PORTFOLIO_ROOT / package_name
    # VALIDATION: pending modules count as populated only when Python files exist.
    return package_dir.exists() and any(package_dir.rglob("*.py"))
# --------------------------------------------------------------- end _package_has_files()


# --------------------------------------------------------------- _render_pending_module()
def _render_pending_module(package_name: str, title: str, source_hint: str) -> None:
    """Render a warning for a module reserved for a later integration pass.

    Args:
        package_name: Module 8 package directory name.
        title: Human-readable module title.
        source_hint: Source assignment or module that will populate it.

    Returns:
        None.
    """
    st.header(title)
    # DISPATCH: distinguish populated-but-unwired modules from empty placeholders.
    if _package_has_files(package_name):
        st.info(
            f"`{package_name}` contains source files, but this root tab has not "
            "been wired into the final portfolio navigation yet."
        )
    else:
        st.warning(
            f"`{package_name}` is not populated yet. Later integration should "
            f"copy and adapt the {source_hint} app into this package."
        )
# --------------------------------------------------------------- end _render_pending_module()


# --------------------------------------------------------------- _render_markdown_file()
def _render_markdown_file(path: Path) -> None:
    """Render a Markdown file or a missing-artifact warning.

    Args:
        path: Markdown file path.

    Returns:
        None.
    """
    # VALIDATION: the report is optional during integration, so fail visibly.
    if not path.exists():
        st.warning(
            "Missing comprehensive analysis artifact: "
            f"`{path}`. Create this report in a later integration pass and "
            "the root app will render it here."
        )
        return
    st.markdown(path.read_text(encoding="utf-8"))
# --------------------------------------------------------------- end _render_markdown_file()


# __________________________________________________________________________
# Application Orchestration
# ========================================================================
# ROOT TABS
# ========================================================================
# APPLICATION ORCHESTRATION:
# The root app renders a shared header, creates one tab per integrated module,
# and delegates each feature area to its package-level page renderer.
#
# ROOT TAB FLOW:
#   1. Overview summarizes all integrated modules and key concepts.
#   2. Each module tab delegates to its package-level Streamlit renderer.
#   3. Comprehensive Analysis renders the cross-module Markdown report.
# =========================================================================
# - Tab: Overview
# - Tab: Search Comparison
# - Tab: Linked Structures
# - Tab: Tree Map
# - Tab: Hash Priority
# - Tab: Graph Algorithms
# - Tab: Bubble Quickselect Sets
# - Tab: Comprehensive Analysis

_render_header()

# Step 1: Create stable root tabs that match the final portfolio structure.
(
    tab_overview,
    tab_search,
    tab_linked,
    tab_tree,
    tab_hash,
    tab_graph,
    tab_bubble,
    tab_analysis,
) = st.tabs(
    [
        "Overview",
        "Search Comparison",
        "Linked Structures",
        "Tree Map",
        "Hash Priority",
        "Graph Algorithms",
        "Bubble Quickselect Sets",
        "Comprehensive Analysis",
    ]
)


# ========================================================================
# Tab 1 - Overview
# ========================================================================

with tab_overview:
    # Step 2: Summarize how each integrated module supports the portfolio goals.
    st.header("Overview")
    st.markdown(
        """
This Algorithm and Data Structure Comparison Tool combines the following
Portfolio Module 8 structures and behaviors:

- **Search Comparison** - linear search and binary search workflows that show
  how ordered data changes search efficiency.
- **Linked Structures** - stack, queue, deque, and linked-list behaviors that
  compare list-backed and node-based structure design.
- **Tree Map** - Binary Search Tree, TreeMap, and ListMap workflows that
  compare ordered tree navigation against a linear baseline.
- **Hash Priority** - hash-table and priority-queue operations that compare
  direct key access, heap behavior, and linear-search benchmarking.
- **Graph Algorithms** - graph representations, traversal algorithms, and
  shortest-path workflows that compare structural trade-offs across workloads.
- **Bubble Quickselect Sets** - Bubble Sort, Quickselect, and CourseSet
  demonstrations that connect ordering, selection, and set behavior.

Use the tabs above to build deterministic datasets, compare algorithm and data
structure behavior, run guided operations, benchmark different workloads, and
read the written analysis and recommendation materials from the integrated
portfolio modules.

### Project Goals

- Compare multiple algorithm and data structure categories inside one root app
- Demonstrate guided operations, traces, and benchmark workflows across modules
- Connect measured performance to Big-O reasoning and recommendation writing
- Preserve milestone and CTA work in one integrated Streamlit interface
        """
    )
    st.subheader("Search Comparison")
    st.info(
        "Search Comparison focuses on how dataset ordering changes search "
        "behavior. Linear search scans item by item, while binary search uses "
        "sorted structure to cut the search space in half at each step. That "
        "makes the area useful for comparing straightforward correctness "
        "against stronger search efficiency when ordering rules are available."
    )

    st.subheader("Linked Structures")
    st.info(
        "Linked Structures compares common abstract data types through both "
        "behavior and implementation choice. Stack, Queue, and Deque show how "
        "removal order shapes real use cases, while the custom linked list "
        "shows what changes when nodes and pointer-style traversal replace "
        "contiguous list storage."
    )

    st.subheader("Tree Map")
    st.info(
        "Tree Map focuses on ordered search and key-value storage. A plain BST "
        "shows how comparison-driven branching supports search, insertion, "
        "deletion, and traversal, while TreeMap and ListMap make it easier to "
        "compare tree-based lookup against a linear baseline."
    )

    st.subheader("Hash Priority")
    st.info(
        "Hash Priority compares two different ways to organize fast access. A "
        "hash table is useful for direct key lookup through bucket placement, "
        "while a priority queue is useful when removal order depends on "
        "priority instead of insertion order. The benchmark workflow ties that "
        "behavior back to search-cost trade-offs."
    )

    st.subheader("Graph Algorithms")
    st.info(
        "Graph Algorithms compares relationship-focused structures and path "
        "workflows. Adjacency lists and adjacency matrices store the same graph "
        "in different ways, while BFS, DFS, and Dijkstra show how traversal "
        "and shortest-path behavior depend on representation and workload."
    )

    st.subheader("Bubble Quickselect Sets")
    st.info(
        "Bubble Quickselect Sets connects ordering, selection, and set "
        "reasoning in one feature area. Bubble Sort highlights repeated "
        "adjacent swaps, Quickselect highlights targeted rank selection "
        "without fully sorting every value, and CourseSet shows how set "
        "operations group related course data."
    )

    st.subheader("Key Concepts")
    st.info(
        "**Ordering rules** explain why sorted data, tree structure, and graph "
        "representation can change operation cost.\n\n"
        "**Workload shape** explains why the best structure depends on whether "
        "the task emphasizes lookup, traversal, updates, or benchmark scale.\n\n"
        "**Structure choice** means selecting the representation whose behavior "
        "fits the problem instead of forcing one tool into every workload.\n\n"
        "**Benchmark evidence** connects theoretical complexity to measured "
        "results so the recommendation guides can make defensible choices."
    )

    st.subheader("How to Use This Tool")
    st.info(
        "Use Overview to compare the integrated feature areas before diving "
        "into a module tab. Use each module tab to build datasets, inspect "
        "guided operations, and compare benchmark results for its specific "
        "structures or algorithms. Use Comprehensive Analysis after the module "
        "workflows to connect the full portfolio results to the course "
        "requirements."
    )


# ========================================================================
# Tab 2 - Search Comparison
# ========================================================================

with tab_search:
    # DISPATCH: delegate search workflows to the Portfolio Milestone Module 2 page.
    render_search_comparison_page()


# ========================================================================
# Tab 3 - Linked Structures
# ========================================================================

with tab_linked:
    # DISPATCH: delegate linked-structure workflows to the Module 4 page.
    render_linked_structures_page()


# ========================================================================
# Tab 4 - Tree Map
# ========================================================================

with tab_tree:
    # DISPATCH: delegate tree/map workflows to the Module 6 page.
    render_tree_map_page()


# ========================================================================
# Tab 5 - Hash Priority
# ========================================================================

with tab_hash:
    # DISPATCH: delegate hash-table and priority-queue workflows to the CTA-5 page.
    render_hash_priority_page()


# ========================================================================
# Tab 6 - Graph Algorithms
# ========================================================================

with tab_graph:
    # DISPATCH: delegate graph representation and algorithm workflows to CTA-7.
    render_graph_algorithms_page()


# ========================================================================
# Tab 7 - Bubble Quickselect Sets
# ========================================================================

with tab_bubble:
    # DISPATCH: delegate native Module 8 set, sort, and selection workflows.
    render_bubble_quickselect_sets_page()


# ========================================================================
# Tab 8 - Comprehensive Analysis
# ========================================================================

with tab_analysis:
    # Step 3: Render the cross-module written analysis when the artifact exists.
    st.header("Comprehensive Analysis")
    _render_markdown_file(_COMPREHENSIVE_ANALYSIS_PATH)


# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
