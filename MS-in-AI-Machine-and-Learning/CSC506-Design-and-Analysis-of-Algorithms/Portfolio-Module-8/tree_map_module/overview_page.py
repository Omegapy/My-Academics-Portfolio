# -------------------------------------------------------------------------
# File: overview_page.py
# Project: Portfolio Module 8 - Tree Map Integration
# Author: Alexander Ricciardi
# Date: 2026-04-21
# File Path: Portfolio-Module-8/tree_map_module/overview_page.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
# -------------------------------------------------------------------------
# Assignment:
# Portfolio Milestone Module 6 - Trees
#
# Directions:
# - Implement a Binary Search Tree with insert, delete, search, and
#   traversal support.
# - Build a BST-backed Map, detect unbalanced trees, and test with at
#   least 50 comparable items.
# - Compare TreeMap search behavior against a list-backed baseline and
#   report the results.
# -------------------------------------------------------------------------
# Project description:
# Module 6 is a small web application that uses Streamlit to that implements    
# BST operations, map-style tree storage, balance detection, and
# TreeMap versus ListMap search analysis with written evaluation artifacts.
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Coordinate the seven Streamlit tabs for datasets, BST labs, map labs,
#   benchmarks, and analysis artifacts.
# - Hold shared page constants, session-state defaults, and result packaging
#   helpers for the live app flow.
# - Render written-analysis and recommendation artifacts with benchmark-aware
#   placeholders.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Global Constants / Variables: page configuration and artifact paths.
# - Class Definitions - Data Classes: ``_StructureSnapshot``.
# - Function Definitions: parsing, session-state, snapshot, and result helpers.
# - Application Orchestration: top-to-bottom Streamlit tab layout and rendering.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: dataclasses, sys, pathlib
# - Third-Party: pandas, streamlit
# - Local Project Modules:
#   - analysis.benchmark_search
#   - analysis.lab_validation
#   - analysis.report_generator
#   - data.dataset_manager
#   - data_structures
#   - models.lab_operation_result
#   - ui.streamlit_helpers
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by ``Portfolio-Module-8/streamlit_app.py``.
# - Exposes ``render_tree_map_page()`` instead of running as a standalone
#   Streamlit entry point.
# - It coordinates the live UI while reading and refreshing saved analysis
#   artifacts from this package's analysis directory.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Import-safe Tree Map page module for Portfolio Module 8.

This module implements the Streamlit interface that incorporates the following features:

- Guided dataset building
- Guided BST and TreeMap operations
- Guided benchmark execution
- Analysis rendering

"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================
# Import-safe page module for the Portfolio Module 8 root app.
#
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import streamlit as st

_MODULE_ROOT = Path(__file__).resolve().parent

# import analysis modules
from tree_map_module.analysis.benchmark_search import (  # noqa: E402
    DEFAULT_QUERY_MODES,
    DEFAULT_REPEATS,
    DEFAULT_SIZES,
    load_results_csv,
    run_benchmarks,
    save_results_csv,
)
# import analysis modules
from tree_map_module.analysis.lab_validation import (  # noqa: E402
    run_benchmark_validation,
    run_bst_demo,
    run_map_demo,
    run_traversal_demo,
    run_unbalanced_tree_demo,
    summarize_benchmark_validation,
)
# import analysis modules
from tree_map_module.analysis.report_generator import (  # noqa: E402
    build_balance_summary_markdown_table,
    build_benchmark_markdown_table,
    build_speedup_summary_markdown_table,
    generate_all_reports,
)
# import data modules
from tree_map_module.data.dataset_manager import (  # noqa: E402
    DATASET_TYPES,
    DEFAULT_DATASET_SIZE,
    DEFAULT_RANDOM_SEED,
    INSERTION_PATTERNS,
    generate_keys,
    parse_manual_keys,
    validate_dataset,
)
# import data structures
from tree_map_module.data_structures import BinarySearchTree, ListMap, Map  # noqa: E402
from tree_map_module.models.lab_operation_result import LabOperationResult  # noqa: E402
from tree_map_module.ui.streamlit_helpers import (  # noqa: E402
    render_analysis_markdown_file,
    render_balance_summary,
    render_benchmark_charts,
    render_benchmark_table,
    render_dataset_info,
    render_guided_operation_results,
    render_header,
    render_lab_quick_start,
    render_manual_operation_result,
    render_section_intro,
    render_traversal_outputs,
    render_tree_ascii_diagram,
    render_tree_state_panel,
)


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# PAGE CONFIGURATION AND ARTIFACT PATHS
# ========================================================================
# These constants define the Streamlit page shell and the saved analysis
# artifacts that the later tabs load, regenerate, or render.
#
# define constants for analysis directory, benchmark csv, written analysis, recommendation guide, and chart directory
_ANALYSIS_DIR = _MODULE_ROOT / "analysis"
_BENCHMARK_CSV = _ANALYSIS_DIR / "benchmark_results.csv"
_WRITTEN_ANALYSIS = _ANALYSIS_DIR / "written_analysis.md"
_RECOMMENDATION_GUIDE = _ANALYSIS_DIR / "recommendation_guide.md"
_CHART_DIR = _ANALYSIS_DIR / "charts"


# __________________________________________________________________________
# Class Definitions - Data Classes
# ========================================================================
# TYPES AND DATA STRUCTURES
# ========================================================================
# This lightweight snapshot keeps the UI-visible size, height, balance, and
# ASCII state together for before/after result packaging.
#
# ------------------------------------------------------------------------- class _StructureSnapshot
@dataclass(slots=True, kw_only=True)
class _StructureSnapshot:
    """Immutable snapshot of the UI-visible tree state for one structure.

    Attributes:
        size: Current number of stored keys.
        height: Current tree height using the Module 6 height convention.
        balanced: Whether the structure currently satisfies the balance rule.
        ascii: ASCII rendering used in result cards and diagram panels.
    """

    size: int
    height: int
    balanced: bool
    ascii: str


# ---------------------------------------------------------- end class _StructureSnapshot


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# DATASET / SESSION HELPERS
# ========================================================================
# These helpers normalize user input and initialize the stable session-state
# contract used across the dataset, BST, map, benchmark, and analysis tabs.
#
# --------------------------------------------------------------- _items_from_keys()
def _items_from_keys(keys: list[object]) -> list[tuple[object, object]]:
    """Build readable key-value items from a key list.

    Logic:
        This helper converts one key sequence into the value shape used by the
        map lab.
        1. Walk the keys in their current dataset order.
        2. Build one readable value payload for each key.
        3. Return the resulting key-value item list.
    """
    return [
        (
            key,
            {
                "id": index,  # Stable 1-based position within the current dataset
                "label": f"value-{index:03d}",  # Human-friendly label shown in the labs
                "source_key": key,  # Original key preserved for display and traceability
            },
        )
        for index, key in enumerate(keys, start=1)
    ]
# --------------------------------------------------------------- end _items_from_keys()


# --------------------------------------------------------------- _parse_single_key()
def _parse_single_key(raw_value: str, dataset_type: str) -> object:
    """Parse one key value from a text input according to ``dataset_type``.

    Logic:
        This helper normalizes one manual key input for BST and TreeMap
        actions.
        1. Dispatch to the parser that matches the active dataset type.
        2. Enforce the non-empty string rule for string keys.
        3. Enforce the single-key rule for tuple parsing paths.
    """
    # DISPATCH: parse the text according to the active comparable key family.
    if dataset_type == "integers":
        return int(raw_value.strip())
    if dataset_type == "strings":
        cleaned = raw_value.strip()
        # VALIDATION: empty strings would create ambiguous visible keys in the UI.
        if not cleaned:
            raise ValueError("String key cannot be empty.")
        return cleaned
    parsed = parse_manual_keys(raw_value.strip(), dataset_type)
    # VALIDATION: manual single-key actions must resolve to exactly one key.
    if len(parsed) != 1:
        raise ValueError("Provide exactly one tuple key for manual operations.")
    return parsed[0]
# --------------------------------------------------------------- end _parse_single_key()


# --------------------------------------------------------------- _empty_benchmark_df()
def _empty_benchmark_df() -> pd.DataFrame:
    """Return an empty benchmark DataFrame with expected columns.

    Logic:
        This helper provides the stable benchmark schema used by session state
        and fallback rendering.
        1. Define the expected benchmark columns.
        2. Return an empty DataFrame with that schema.
    """
    return pd.DataFrame(
        columns=[
            "method",
            "scenario",
            "query_mode",
            "size",
            "time_ms",
            "repeat_count",
            "height",
            "is_balanced",
            "notes",
            "speedup_vs_list",
        ]
    )
# --------------------------------------------------------------- end _empty_benchmark_df()


# --------------------------------------------------------------- _init_session_state()
def _init_session_state() -> None:
    """Initialize all required session-state keys.

    Logic:
        1. Define the shared defaults used by every Module 6 tab.
        2. Populate only missing session keys so reruns preserve user state.
        3. Keep the app's cross-tab contract stable from the first render.
    """
    # Constraint: every tab reads from the same shared session-state keys, so
    # the defaults must be present before any UI interaction occurs.
    defaults: dict[str, object] = {
        # Dataset builder selections and generated workloads.
        "tm_dataset_keys": [],
        "tm_dataset_items": [],
        "tm_dataset_type": "integers",
        "tm_insertion_pattern": "random",
        "tm_dataset_size": DEFAULT_DATASET_SIZE,
        "tm_dataset_seed": DEFAULT_RANDOM_SEED,
        # Live structure instances shown in the BST and Map labs.
        "tm_bst": None,
        "tm_tree_map": None,
        "tm_list_map": None,
        # Most recent manual-operation result cards.
        "tm_last_bst_result": None,
        "tm_last_map_result": None,
        # Guided demo result collections keyed by lab section.
        "tm_guided_bst_results": [],
        "tm_guided_traversal_results": [],
        "tm_guided_balance_results": [],
        "tm_guided_map_results": [],
        # Benchmark artifacts shared by the benchmark and analysis tabs.
        "tm_benchmark_df": _empty_benchmark_df(),
        "tm_benchmark_validation": None,
    }

    # initialize session state
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
# --------------------------------------------------------------- end _init_session_state()


# --------------------------------------------------------------- _resolved_benchmark_df()
def _resolved_benchmark_df() -> pd.DataFrame:
    """Return session benchmark data, or load the saved CSV when available.

    Logic:
        1. Prefer non-empty benchmark data already stored in session state.
        2. Fall back to the saved benchmark CSV after app reloads.
        3. Return a stable empty DataFrame when no benchmark data exists yet.
    """
    benchmark_df = st.session_state.get("tm_benchmark_df")
    # VALIDATION: prefer live in-memory results when the current session has them.
    if isinstance(benchmark_df, pd.DataFrame) and not benchmark_df.empty:
        return benchmark_df
    # SAFETY CHECK: fall back to the saved CSV so analysis tabs still render after reloads.
    if _BENCHMARK_CSV.exists():
        return load_results_csv(_BENCHMARK_CSV)
    return _empty_benchmark_df()
# --------------------------------------------------------------- end _resolved_benchmark_df()


# --------------------------------------------------------------- _analysis_placeholders()
def _analysis_placeholders(benchmark_df: pd.DataFrame) -> dict[str, str]:
    """Build the markdown placeholder map used by the analysis tabs.

    Logic:
        1. Skip placeholder injection when benchmark data is empty.
        2. Build each markdown table from the current benchmark DataFrame.
        3. Return a placeholder map keyed to the analysis-document tokens.
    """
    # VALIDATION: placeholder tables should not be injected until benchmark data exists.
    if benchmark_df.empty:
        return {}

    # Placeholder tokens mirrored by the saved analysis markdown artifacts.
    return {
        "BENCHMARK_RESULTS_TABLE": build_benchmark_markdown_table(benchmark_df),  # Raw rows
        "SEARCH_SPEEDUP_TABLE": build_speedup_summary_markdown_table(benchmark_df),  # Speedups
        "BALANCE_SUMMARY_TABLE": (
            build_balance_summary_markdown_table(benchmark_df)
        ),  # Heights/balance
    }
# --------------------------------------------------------------- end _analysis_placeholders()


# --------------------------------------------------------------- _build_tree_from_dataset()
def _build_tree_from_dataset() -> BinarySearchTree:
    """Build a BST from the current session dataset.

    Logic:
        1. Create a fresh BST so rebuilds never reuse stale state.
        2. Insert keys in the dataset's current order.
        3. Return the finished tree for storage in session state.
    """
    tree = BinarySearchTree()
    # MAIN ITERATION LOOP: insert the current dataset in the same order chosen
    # by the Dataset Builder so tree shape stays faithful to the selection.
    for key in st.session_state["tm_dataset_keys"]:
        tree.insert(key)
    return tree
# --------------------------------------------------------------- end _build_tree_from_dataset()


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# STRUCTURE SNAPSHOT HELPERS
# ========================================================================
# These helpers package BST and TreeMap before/after state into shared
# dataclass-based result objects for the manual and guided labs.
#
# --------------------------------------------------------------- _capture_structure_snapshot()
def _capture_structure_snapshot(
    structure: BinarySearchTree | Map,
) -> _StructureSnapshot:
    """Capture the current size, height, balance, and ASCII state.

    Logic:
        This helper freezes one structure's UI-visible state for before-and-
        after result cards.
        1. Read the structure size, height, and balance status.
        2. Render the current ASCII representation.
        3. Return the collected snapshot object.
    """
    return _StructureSnapshot(
        size=len(structure),
        height=structure.height(),
        balanced=structure.is_balanced(),
        ascii=structure.render_ascii(),
    )
# --------------------------------------------------------------- end _capture_structure_snapshot()


# --------------------------------------------------------------- _capture_tree_result()
def _capture_tree_result(
    *,
    operation: str,
    input_key: object | None,
    input_value: object | None,
    returned_value: object | None,
    success: bool,
    before_snapshot: _StructureSnapshot,
    after_snapshot: _StructureSnapshot,
    message: str,
) -> LabOperationResult:
    """Build a :class:`LabOperationResult` for a BST operation.

    Logic:
        This helper packages one BST action into the shared result model used
        by the UI.
        1. Copy the provided operation metadata.
        2. Copy the before-and-after snapshot values into result fields.
        3. Return the completed lab-operation result object.
    """
    return LabOperationResult(
        section="BST Lab",
        operation=operation,
        input_key=input_key,
        input_value=input_value,
        returned_value=returned_value,
        success=success,
        size_before=before_snapshot.size,
        size_after=after_snapshot.size,
        height_before=before_snapshot.height,
        height_after=after_snapshot.height,
        balanced_before=before_snapshot.balanced,
        balanced_after=after_snapshot.balanced,
        tree_before_ascii=before_snapshot.ascii,
        tree_after_ascii=after_snapshot.ascii,
        message=message,
    )
# --------------------------------------------------------------- end _capture_tree_result()


# --------------------------------------------------------------- _capture_map_result()
def _capture_map_result(
    *,
    operation: str,
    input_key: object | None,
    input_value: object | None,
    returned_value: object | None,
    success: bool,
    before_snapshot: _StructureSnapshot,
    after_snapshot: _StructureSnapshot,
    message: str,
) -> LabOperationResult:
    """Build a :class:`LabOperationResult` for a TreeMap operation.

    Logic:
        This helper packages one TreeMap action into the shared result model
        used by the UI.
        1. Copy the provided operation metadata.
        2. Copy the before-and-after snapshot values into result fields.
        3. Return the completed lab-operation result object.
    """
    return LabOperationResult(
        section="Map Lab",
        operation=operation,
        input_key=input_key,
        input_value=input_value,
        returned_value=returned_value,
        success=success,
        size_before=before_snapshot.size,
        size_after=after_snapshot.size,
        height_before=before_snapshot.height,
        height_after=after_snapshot.height,
        balanced_before=before_snapshot.balanced,
        balanced_after=after_snapshot.balanced,
        tree_before_ascii=before_snapshot.ascii,
        tree_after_ascii=after_snapshot.ascii,
        message=message,
    )
# --------------------------------------------------------------- end _capture_map_result()


# __________________________________________________________________________
# Application Orchestration
# ========================================================================
# STREAMLIT ENTRY FLOW
# ========================================================================
# Streamlit executes the rest of the module at import time, so state
# initialization and tab layout happen immediately after helper definitions.
#
# --------------------------------------------------------------- render_tree_map_page()
def render_tree_map_page() -> None:
    """Render the Tree Map page inside the root portfolio app.

    Returns:
        None.
    """
    # MODULE INITIALIZATION: seed session state first, then render the shared page shell.
    _init_session_state()
    render_header()
    
    tabs = st.tabs(
        [
            "Overview",
            "Dataset Builder",
            "BST Lab",
            "Map Lab",
            "Benchmark Lab",
            "Written Analysis",
            "Recommendation Guide",
        ]
    )
    
    
    # __________________________________________________________________________
    # Overview Tab
    # ========================================================================
    # PROJECT CONTEXT AND CONCEPT OVERVIEW
    # ========================================================================
    # This tab frames the assignment goals, the three compared structures, and
    # the complexity expectations users should keep in mind while exploring.
    #
    with tabs[0]:
        st.header("Overview")
        st.markdown(
            """
    This Binary Search Tree and TreeMap Tool compares the following
    Module 6 structures and behaviors:
    
    * **Binary Search Tree (BST)** — a plain binary search tree that supports
      insert, search, delete, minimum, maximum, and in-order / pre-order /
      post-order traversal.
    * **TreeMap** — a key-value map backed by the BST so keys stay logically
      ordered and can be searched through tree navigation.
    * **ListMap** — a simple list-backed key-value baseline used to compare
      tree-based search against linear search.
    
    Use the tabs above to build datasets, inspect tree shape, run guided
    operations, benchmark search behavior, and read the written analysis and
    recommendation guide.
    
    ### Project Goals
    
    - Implement insert, search, delete, minimum, maximum, and traversal operations
      for a plain BST
    - Build a `Map` class that uses the BST for key-value storage
    - Detect when a tree becomes unbalanced
    - Test the implementation with at least 50 comparable data items
    - Compare TreeMap search performance against a list-based baseline
            """
        )
    
        # overview of Binary Search Tree
        st.subheader("Binary Search Tree")
        st.info(
            "A Binary Search Tree stores each key according to one ordering rule: "
            "smaller keys go to the left subtree and larger keys go to the right "
            "subtree. That makes search, insert, delete, minimum, maximum, and "
            "in-order traversal naturally structured around comparisons. When the "
            "tree stays relatively short, those operations are efficient. When "
            "insertion order creates a skewed tree, performance can move toward "
            "O(n)."
        )
    
        # overview of TreeMap
        st.subheader("TreeMap")
        st.info(
            "TreeMap uses the BST as a key-value storage engine. That means the "
            "project can demonstrate both map-style lookup and ordered output in "
            "the same structure. A TreeMap is especially useful when a program "
            "needs repeated key lookup, sorted keys, traversal-based reporting, "
            "and direct access to minimum and maximum keys."
        )
    
        st.subheader("ListMap")
        st.info(
            "ListMap is the linear-search baseline in this project. It stores "
            "key-value pairs in a Python list and scans that list when searching "
            "for a key. That makes it simpler than TreeMap, but it also means "
            "lookup remains O(n) because the structure does not use tree ordering "
            "to narrow the search space."
        )
    
        # complexity overview
        st.subheader("Complexity Overview")
        st.markdown(
            """
    **Plain BST / TreeMap**
    
    | Operation | Healthy Tree | Worst Case (Skewed) |
    |-----------|--------------|---------------------|
    | Insert    | O(log n)     | O(n)                |
    | Search    | O(log n)     | O(n)                |
    | Delete    | O(log n)     | O(n)                |
    | Min / Max | O(log n)     | O(n)                |
    | Traversal | O(n)         | O(n)                |
    
    **ListMap**
    
    | Operation | Complexity |
    |-----------|------------|
    | Put       | O(n)       |
    | Get       | O(n)       |
    | Delete    | O(n)       |
            """
        )
    
        # key concepts
        st.subheader("Key Concepts")
        st.info(
            "**BST ordering rule** means all smaller keys stay in the left "
            "subtree and all larger keys stay in the right subtree.\n\n"
            "**Traversal order** explains why in-order traversal returns sorted "
            "keys, while pre-order and post-order help reveal structure and "
            "processing order.\n\n"
            "**Balance detection** shows when subtree heights differ enough to "
            "signal that the tree is becoming unhealthy.\n\n"
            "**Insertion order matters** because a plain BST can stay relatively "
            "short under favorable insertion order or become tall and skewed under "
            "sorted insertion."
        )
    
        # how to use this tool
        st.subheader("How to Use This Tool")
        st.info(
            "Use Dataset Builder to generate one comparable key type at a time. "
            "Use BST Lab to build the tree, inspect traversal outputs, and view "
            "balance reports. Use Map Lab to test TreeMap operations and compare "
            "them with ListMap state. Use Benchmark Lab to compare TreeMap and "
            "ListMap search under random and sorted insertion scenarios. Then read "
            "the Written Analysis and Recommendation Guide tabs to connect the "
            "results to the assignment requirements."
        )
    
        # note about AVL trees
        st.info(
            "**Note:** AVL and other self-balancing tree ideas appear in the "
            "reference materials, but automatic rebalancing is outside the scope "
            "of this assignment."
        )
    
    
    # __________________________________________________________________________
    # Dataset Builder Tab
    # ========================================================================
    # DATASET CREATION AND VALIDATION
    # ========================================================================
    # The dataset tab defines the one comparable key family that all later tabs
    # reuse when building the BST, TreeMap, ListMap, and benchmark workloads.
    #
    # dataset builder
    with tabs[1]:
        render_section_intro(
            "Dataset Builder",
            "Generate a dataset of one comparable key type at a time. This keeps "
            "the BST ordering rules valid and makes TreeMap/ListMap comparisons fair.",
        )
    
        # dataset type selection
        dataset_type = st.selectbox(
            "Dataset Type",
            DATASET_TYPES,
            index=DATASET_TYPES.index(st.session_state["tm_dataset_type"]),
            key="tm_dataset_type_select",
        )
    
        # insertion pattern selection
        insertion_pattern = st.selectbox(
            "Insertion Pattern",
            INSERTION_PATTERNS,
            index=INSERTION_PATTERNS.index(st.session_state["tm_insertion_pattern"]),
            key="tm_insertion_pattern_select",
        )
    
        # dataset size selection
        dataset_size = st.number_input(
            "Dataset Size",
            min_value=1,
            value=int(st.session_state["tm_dataset_size"]),
            step=1,
            key="tm_dataset_size_input",
        )
    
        # dataset seed selection
        dataset_seed = st.number_input(
            "Dataset Seed",
            value=int(st.session_state["tm_dataset_seed"]),
            step=1,
            key="tm_dataset_seed_input",
        )
    
        # manual input
        manual_input = st.text_area(
            "Manual Input",
            help=(
                "Integers and strings use comma-separated input. "
                "Tuple keys use [(1, 2), (3, 4)] or (1, 2); (3, 4)."
            ),
            key="tm_manual_dataset_input",
        )
    
        # dataset generation
        if st.button("Generate Dataset", key="tm_generate_dataset_btn"):
            # Step 1: generate a dataset using the selected key family and insertion pattern.
            keys = generate_keys(
                size=int(dataset_size),
                dataset_type=dataset_type,
                insertion_pattern=insertion_pattern,
                seed=int(dataset_seed),
            )
            is_valid, message = validate_dataset(keys, dataset_type)
            # VALIDATION: only persist datasets that satisfy the type-family and uniqueness rules.
            if is_valid:
                st.session_state["tm_dataset_keys"] = keys
                st.session_state["tm_dataset_items"] = _items_from_keys(keys)
                st.session_state["tm_dataset_type"] = dataset_type
                st.session_state["tm_insertion_pattern"] = insertion_pattern
                st.session_state["tm_dataset_size"] = int(dataset_size)
                st.session_state["tm_dataset_seed"] = int(dataset_seed)
                st.session_state["tm_bst"] = None
                st.session_state["tm_tree_map"] = None
                st.session_state["tm_list_map"] = None
                st.success(message)
            else:
                st.error(message)
    
        # manual dataset
        if st.button("Load Manual Dataset", key="tm_manual_dataset_btn"):
            try:
                # Step 1: parse the user-provided text into one supported key family.
                keys = parse_manual_keys(manual_input, dataset_type)
                is_valid, message = validate_dataset(keys, dataset_type)
                if not is_valid:
                    st.error(message)
                else:
                    st.session_state["tm_dataset_keys"] = keys
                    st.session_state["tm_dataset_items"] = _items_from_keys(keys)
                    st.session_state["tm_dataset_type"] = dataset_type
                    st.session_state["tm_insertion_pattern"] = "manual"
                    st.session_state["tm_dataset_size"] = len(keys)
                    st.success("Loaded manual dataset successfully.")
            except ValueError as exc:
                st.error(str(exc))
        
        # dataset info
        if st.session_state["tm_dataset_keys"]:
            render_dataset_info(
                st.session_state["tm_dataset_keys"],
                st.session_state["tm_dataset_type"],
                st.session_state["tm_insertion_pattern"],
            )
        else:
            st.info("Generate or load a dataset to continue.")
    
    
    # __________________________________________________________________________
    # BST Lab Tab
    # ========================================================================
    # BST BUILD / TRAVERSAL / BALANCE EXPLORATION
    # ========================================================================
    # This tab lets the user build a plain BST from the active dataset, inspect
    # the resulting structure, and run both guided and manual tree operations.
    #
    
    # bst lab
    with tabs[2]:
        render_section_intro(
            "BST Lab",
            "Build a Binary Search Tree from the current dataset, run guided demos, "
            "and try manual insert/search/delete operations.",
        )
    
        # render quick start
        render_lab_quick_start(
            "BST Lab Quick Start",
            [
                "Generate a dataset first.",
                "Build the BST from the dataset.",
                "Inspect the tree diagram, traversals, and balance summary.",
                "Run the guided traversal and unbalanced-tree demos.",
            ],
        )
    
        # build BST from dataset
        if st.button("Build BST from Dataset", key="tm_build_bst_btn"):
            # VALIDATION: the BST cannot be built until a dataset has been defined.
            if not st.session_state["tm_dataset_keys"]:
                st.warning("Generate a dataset before building the BST.")
            else:
                before_snapshot = _capture_structure_snapshot(BinarySearchTree())
                after_tree = _build_tree_from_dataset()
                after_snapshot = _capture_structure_snapshot(after_tree)
                st.session_state["tm_bst"] = after_tree
                st.session_state["tm_last_bst_result"] = _capture_tree_result(
                    operation="build_from_dataset",
                    input_key=None,
                    input_value=None,
                    returned_value=len(after_tree),
                    success=len(after_tree) == len(st.session_state["tm_dataset_keys"]),
                    before_snapshot=before_snapshot,
                    after_snapshot=after_snapshot,
                    message=f"Built a BST with {len(after_tree)} keys from the dataset.",
                )
        
        # run guided bst demo
        if st.button("Run Guided BST Demo (50 items)", key="tm_guided_bst_demo_btn"):
            st.session_state["tm_guided_bst_results"] = run_bst_demo()
            st.success("Guided BST demo complete.")
        
        # run guided traversal demo
        if st.button("Run Guided Traversal Demo", key="tm_guided_traversal_demo_btn"):
            st.session_state["tm_guided_traversal_results"] = run_traversal_demo()
            st.success("Guided traversal demo complete.")
        
        # run guided unbalanced demo
        if st.button("Run Guided Unbalanced Demo", key="tm_guided_unbalanced_demo_btn"):
            st.session_state["tm_guided_balance_results"] = run_unbalanced_tree_demo()
            st.warning("Unbalanced-tree demo complete.")
    
        # manual operations
        manual_key_raw = st.text_input("BST Manual Key", key="tm_bst_manual_key_input")
        col1, col2, col3 = st.columns(3)
    
        # BST insert
        if col1.button("BST Insert", key="tm_bst_insert_btn"):
            tree = st.session_state["tm_bst"]
            # VALIDATION: manual operations require a live BST instance first.
            if tree is None:
                st.warning("Build the BST before running manual operations.")
            else:
                try:
                    key = _parse_single_key(manual_key_raw, st.session_state["tm_dataset_type"])
                    before_snapshot = _capture_structure_snapshot(tree)
                    inserted = tree.insert(key)
                    after_snapshot = _capture_structure_snapshot(tree)
                    st.session_state["tm_last_bst_result"] = _capture_tree_result(
                        operation="insert",
                        input_key=key,
                        input_value=None,
                        returned_value=inserted,
                        success=True,
                        before_snapshot=before_snapshot,
                        after_snapshot=after_snapshot,
                        message="Inserted a new key." if inserted else "Updated an existing key.",
                    )
                except (TypeError, ValueError) as exc:
                    st.error(str(exc))
    
        # BST search
        if col2.button("BST Search", key="tm_bst_search_btn"):
            tree = st.session_state["tm_bst"]
            # VALIDATION: searches run only after the BST exists in session state.
            if tree is None:
                st.warning("Build the BST before running manual operations.")
            else:
                try:
                    key = _parse_single_key(manual_key_raw, st.session_state["tm_dataset_type"])
                    before_snapshot = _capture_structure_snapshot(tree)
                    found = tree.search(key)
                    after_snapshot = _capture_structure_snapshot(tree)
                    st.session_state["tm_last_bst_result"] = _capture_tree_result(
                        operation="search",
                        input_key=key,
                        input_value=None,
                        returned_value=found.key if found else None,
                        success=found is not None,
                        before_snapshot=before_snapshot,
                        after_snapshot=after_snapshot,
                        message="Search completed.",
                    )
                except (TypeError, ValueError) as exc:
                    st.error(str(exc))
        # BST delete
        if col3.button("BST Delete", key="tm_bst_delete_btn"):
            tree = st.session_state["tm_bst"]
            # VALIDATION: deletes run only after the BST exists in session state.
            if tree is None:
                st.warning("Build the BST before running manual operations.")
            else:
                try:
                    key = _parse_single_key(manual_key_raw, st.session_state["tm_dataset_type"])
                    before_snapshot = _capture_structure_snapshot(tree)
                    deleted = tree.delete(key)
                    after_snapshot = _capture_structure_snapshot(tree)
                    st.session_state["tm_last_bst_result"] = _capture_tree_result(
                        operation="delete",
                        input_key=key,
                        input_value=None,
                        returned_value=deleted,
                        success=deleted,
                        before_snapshot=before_snapshot,
                        after_snapshot=after_snapshot,
                        message="Delete completed.",
                    )
                except (TypeError, ValueError) as exc:
                    st.error(str(exc))
        
        # render manual operation result
        render_manual_operation_result(st.session_state["tm_last_bst_result"])
        
        # render tree state panel
        bst: BinarySearchTree | None = st.session_state["tm_bst"]
        if bst is not None:
            render_tree_state_panel(
                name="BST",
                size=len(bst),
                height=bst.height(),
                balanced=bst.is_balanced(),
                min_key=bst.min_key(),
                max_key=bst.max_key(),
            )
            render_tree_ascii_diagram(bst.render_ascii())
            render_traversal_outputs(bst.inorder(), bst.preorder(), bst.postorder())
            render_balance_summary(bst.balance_report())
        else:
            st.info("Build the BST from the dataset to view live tree state.")
        
        # render guided operation results
        render_guided_operation_results(
            "BST Guided Demo Results",
            st.session_state["tm_guided_bst_results"],
        )
        render_guided_operation_results(
            "Traversal Guided Demo Results",
            st.session_state["tm_guided_traversal_results"],
        )
        render_guided_operation_results(
            "Balance Guided Demo Results",
            st.session_state["tm_guided_balance_results"],
        )
    
    
    # __________________________________________________________________________
    # Map Lab Tab
    # ========================================================================
    # TREEMAP / LISTMAP COMPARISON
    # ========================================================================
    # The map tab reuses the active dataset as key-value pairs so users can
    # compare BST-backed mapping behavior against the list-backed baseline.
    #
    # map tab
    with tabs[3]:
        render_section_intro(
            "Map Lab",
            "Store and retrieve key-value pairs through the BST-backed Map, then "
            "compare that behavior with the list-backed baseline.",
        )
        # build treemap from dataset
        if st.button("Build TreeMap from Dataset", key="tm_build_tree_map_btn"):
            # VALIDATION: map structures depend on dataset items, not just raw keys.
            if not st.session_state["tm_dataset_items"]:
                st.warning("Generate a dataset before building the TreeMap.")
            else:
                tree_map = Map(st.session_state["tm_dataset_items"])
                list_map = ListMap(st.session_state["tm_dataset_items"])
                st.session_state["tm_tree_map"] = tree_map
                st.session_state["tm_list_map"] = list_map
                st.success("Built TreeMap and ListMap from the dataset.")
        # run guided map demo
        if st.button("Run Guided Map Demo", key="tm_guided_map_demo_btn"):
            st.session_state["tm_guided_map_results"] = run_map_demo()
            st.success("Guided Map demo complete.")
        # manual map operations
        map_key_raw = st.text_input("Map Manual Key", key="tm_map_manual_key_input")
        map_value_raw = st.text_input("Map Manual Value", key="tm_map_manual_value_input")
        col1, col2, col3 = st.columns(3)
    
        if col1.button("Map Put", key="tm_map_put_btn"):
            tree_map = st.session_state["tm_tree_map"]
            list_map = st.session_state["tm_list_map"]
            # VALIDATION: manual map actions require both comparison structures.
            if tree_map is None or list_map is None:
                st.warning("Build the TreeMap from the dataset before manual operations.")
            else:
                try:
                    # Step 1: parse the key, then update both map implementations with
                    # the same payload so their states stay comparable.
                    key = _parse_single_key(map_key_raw, st.session_state["tm_dataset_type"])
                    value = map_value_raw.strip() or f"value-for-{key!r}"
                    before_snapshot = _capture_structure_snapshot(tree_map)
                    tree_map.put(key, value)
                    list_map.put(key, value)
                    after_snapshot = _capture_structure_snapshot(tree_map)
                    st.session_state["tm_last_map_result"] = _capture_map_result(
                        operation="put",
                        input_key=key,
                        input_value=value,
                        returned_value=tree_map.get(key),
                        success=True,
                        before_snapshot=before_snapshot,
                        after_snapshot=after_snapshot,
                        message="Inserted or updated a key-value pair in the TreeMap.",
                    )
                except (TypeError, ValueError) as exc:
                    st.error(str(exc))
        # map get
        if col2.button("Map Get", key="tm_map_get_btn"):
            tree_map = st.session_state["tm_tree_map"]
            # VALIDATION: lookups require a built TreeMap first.
            if tree_map is None:
                st.warning("Build the TreeMap from the dataset before manual operations.")
            else:
                try:
                    key = _parse_single_key(map_key_raw, st.session_state["tm_dataset_type"])
                    before_snapshot = _capture_structure_snapshot(tree_map)
                    returned_value = tree_map.get(key)
                    after_snapshot = _capture_structure_snapshot(tree_map)
                    st.session_state["tm_last_map_result"] = _capture_map_result(
                        operation="get",
                        input_key=key,
                        input_value=None,
                        returned_value=returned_value,
                        success=returned_value is not None,
                        before_snapshot=before_snapshot,
                        after_snapshot=after_snapshot,
                        message="Retrieved a value from the TreeMap.",
                    )
                except (TypeError, ValueError) as exc:
                    st.error(str(exc))
        # map delete
        if col3.button("Map Delete", key="tm_map_delete_btn"):
            tree_map = st.session_state["tm_tree_map"]
            list_map = st.session_state["tm_list_map"]
            # VALIDATION: keep the TreeMap/ListMap comparison honest by deleting
            # from both structures only after both have been initialized.
            if tree_map is None or list_map is None:
                st.warning("Build the TreeMap from the dataset before manual operations.")
            else:
                try:
                    key = _parse_single_key(map_key_raw, st.session_state["tm_dataset_type"])
                    before_snapshot = _capture_structure_snapshot(tree_map)
                    deleted = tree_map.delete(key)
                    list_map.delete(key)
                    after_snapshot = _capture_structure_snapshot(tree_map)
                    st.session_state["tm_last_map_result"] = _capture_map_result(
                        operation="delete",
                        input_key=key,
                        input_value=None,
                        returned_value=deleted,
                        success=deleted,
                        before_snapshot=before_snapshot,
                        after_snapshot=after_snapshot,
                        message="Deleted a key-value pair from the TreeMap.",
                    )
                except (TypeError, ValueError) as exc:
                    st.error(str(exc))
        # render manual operation result    
        render_manual_operation_result(st.session_state["tm_last_map_result"])
        # render tree map state panel
        tree_map: Map | None = st.session_state["tm_tree_map"]
        list_map: ListMap | None = st.session_state["tm_list_map"]
        # render tree map state panel
        if tree_map is not None:
            render_tree_state_panel(
                name="TreeMap",
                size=len(tree_map),
                height=tree_map.height(),
                balanced=tree_map.is_balanced(),
                min_key=tree_map.min_key(),
                max_key=tree_map.max_key(),
            )
            # render tree map ascii diagram
            render_tree_ascii_diagram(tree_map.render_ascii(), title="TreeMap Diagram")
            # render tree map sorted items
            st.markdown("**TreeMap Sorted Items**")
            st.dataframe(
                pd.DataFrame(tree_map.items(), columns=["Key", "Value"]),
                width="stretch",
                hide_index=True,
            )
            # render list map insertion order items
            if list_map is not None:
                st.markdown("**ListMap Insertion-Order Items**")
                st.dataframe(
                    pd.DataFrame(list_map.items(), columns=["Key", "Value"]),
                    width="stretch",
                    hide_index=True,
                )
        else:
            st.info("Build the TreeMap from the dataset to view live map state.")
    
        render_guided_operation_results(
            "Map Guided Demo Results",
            st.session_state["tm_guided_map_results"],
        )
    
    
    # __________________________________________________________________________
    # Benchmark Lab Tab
    # ========================================================================
    # SEARCH PERFORMANCE COMPARISON
    # ========================================================================
    # The benchmark tab runs matched TreeMap/ListMap workloads, stores the active
    # results in session state, and regenerates saved summary artifacts on demand.
    #
    # benchmark tab    
    with tabs[4]:
        render_section_intro(
            "Benchmark Lab",
            "Compare TreeMap and ListMap search performance under random and "
            "sorted insertion scenarios.",
        )
        # benchmark sizes    
        benchmark_sizes = st.multiselect(
            "Benchmark Sizes",
            DEFAULT_SIZES,
            default=DEFAULT_SIZES[:3],
            key="tm_benchmark_sizes_select",
        )
        # benchmark query modes    
        benchmark_query_modes = st.multiselect(
            "Query Modes",
            DEFAULT_QUERY_MODES,
            default=["hits", "misses"],
            key="tm_benchmark_query_modes_select",
        )
        # benchmark repeats    
        benchmark_repeats = st.number_input(
            "Benchmark Repeats",
            min_value=1,
            value=DEFAULT_REPEATS,
            step=1,
            key="tm_benchmark_repeats_input",
        )
        # run benchmark suite
        if st.button("Run Benchmark Suite", key="tm_run_benchmark_btn"):
            # Step 1: run the matched search benchmark cases for the active selections.
            results_df = run_benchmarks(
                sizes=[int(size) for size in benchmark_sizes],
                repeats=int(benchmark_repeats),
                dataset_type=st.session_state["tm_dataset_type"],
                query_modes=list(benchmark_query_modes),
                seed=int(st.session_state["tm_dataset_seed"]),
            )
            st.session_state["tm_benchmark_df"] = results_df
            st.session_state["tm_benchmark_validation"] = run_benchmark_validation(results_df)
            st.success("Benchmark suite complete.")
        # save benchmark csv
        col1, col2 = st.columns(2)
        if col1.button("Save Benchmark CSV", key="tm_save_benchmark_csv_btn"):
            results_df = _resolved_benchmark_df()
            # VALIDATION: only save artifacts after a benchmark run or CSV load has produced data.
            if results_df.empty:
                st.warning("Run or load benchmark results before saving.")
            else:
                save_results_csv(results_df, _BENCHMARK_CSV)
                generate_all_reports(_BENCHMARK_CSV, _ANALYSIS_DIR)
                st.success("Saved benchmark results and regenerated summary artifacts.")
        # load benchmark csv    
        if col2.button("Load Benchmark CSV", key="tm_load_benchmark_csv_btn"):
            # VALIDATION: loading requires the saved benchmark CSV to exist on disk.
            if not _BENCHMARK_CSV.exists():
                st.warning("No saved benchmark CSV was found.")
            else:
                loaded_df = load_results_csv(_BENCHMARK_CSV)
                st.session_state["tm_benchmark_df"] = loaded_df
                st.session_state["tm_benchmark_validation"] = run_benchmark_validation(loaded_df)
                st.success("Loaded benchmark results from CSV.")
        # render benchmark table
        benchmark_df = _resolved_benchmark_df()
        render_benchmark_table(benchmark_df)
        # render benchmark charts
        render_benchmark_charts(benchmark_df, chart_dir=_CHART_DIR)
        # render benchmark validation summary
        if st.session_state["tm_benchmark_validation"] is not None:
            st.markdown("**Benchmark Validation Summary**")
            st.info(summarize_benchmark_validation(st.session_state["tm_benchmark_validation"]))
        else:
            st.info("Run the benchmark suite to generate a validation summary.")
    
    
    # __________________________________________________________________________
    # Analysis Tabs
    # ========================================================================
    # WRITTEN ANALYSIS AND RECOMMENDATION GUIDE
    # ========================================================================
    # These final tabs read Markdown deliverables and inject live benchmark
    # summary tables when current results are available.
    #
    # render written analysis    
    with tabs[5]:
        st.header("Written Analysis")
        render_analysis_markdown_file(
            _WRITTEN_ANALYSIS,
            _analysis_placeholders(_resolved_benchmark_df()),
        )
    # render recommendation guide    
    with tabs[6]:
        st.header("Recommendation Guide")
        render_analysis_markdown_file(
            _RECOMMENDATION_GUIDE,
            _analysis_placeholders(_resolved_benchmark_df()),
        )
    
    
    # -------------------------------------------------------------------------
    # End of File
    # -------------------------------------------------------------------------
# --------------------------------------------------------------- end render_tree_map_page()
