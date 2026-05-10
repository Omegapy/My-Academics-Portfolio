# -------------------------------------------------------------------------
# File: lab_validation.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-26
# File Path: Portfolio-Milestone-Module-6/analysis/lab_validation.py
# -------------------------------------------------------------------------
# Course: CSC506 - Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Term: Spring A (26SA) 2026
#
# --- Module Functionality ---
# - Package guided BST, traversal, balance, and TreeMap validation demos.
# - Capture before-and-after snapshots for the lab result cards.
# - Derive rubric-style benchmark validation summaries for the Streamlit UI.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Global Constants / Variables: fixed guided-demo fixtures.
# - Function Definitions: snapshot and lab-result packaging helpers.
# - Function Definitions: guided BST, traversal, balance, and map demos.
# - Function Definitions: benchmark validation summaries and display text.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: typing
# - Third-Party: pandas
# - Local Project Modules:
#   - data.dataset_manager
#   - data_structures.binary_search_tree
#   - data_structures.tree_map
#   - models.lab_operation_result
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the Streamlit labs to populate guided validation cards.
# - Imported by tests to verify stable demo outputs and benchmark summaries.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Guided validation helpers for the Module 6 BST and Map labs.

This module packages fixed demo workflows, before-and-after structure
snapshots, and benchmark validation summaries so the Streamlit UI and tests
can verify Module 6 behavior through stable, display-friendly results.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations
from typing import Any
import pandas as pd

# Import key components from other modules.
from data.dataset_manager import (
    DEFAULT_DATASET_SIZE,
    DEFAULT_RANDOM_SEED,
    generate_keys,
    generate_map_items,
)
from data_structures.binary_search_tree import BinarySearchTree
from data_structures.tree_map import Map
from models.lab_operation_result import LabOperationResult


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# GUIDED DEMO FIXTURES
# ========================================================================
# This fixed traversal dataset keeps the expected in-order, pre-order, and
# post-order outputs stable across the UI and automated tests.
#
TRAVERSAL_DEMO_KEYS: list[int] = [50, 30, 70, 20, 40, 60, 80]
"""Fixed keys used by the traversal correctness demo."""


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# SNAPSHOT HELPERS
# ========================================================================
# Snapshot helpers capture size, height, balance, and ASCII state so the labs
# can show before/after transitions without duplicating that boilerplate.
#
# --------------------------------------------------------------- _tree_snapshot()
def _tree_snapshot(tree: BinarySearchTree) -> tuple[int, int, bool, str]:
    """Return the size, height, balance state, and ASCII snapshot of ``tree``.

    Logic:
        This helper captures the UI-visible state of one BST in a single call.
        1. Read the current size, height, and balance state from the tree.
        2. Render the current ASCII diagram.
        3. Return the collected snapshot tuple.
    """
    return len(tree), tree.height(), tree.is_balanced(), tree.render_ascii()
# --------------------------------------------------------------- 

# --------------------------------------------------------------- _map_snapshot()
def _map_snapshot(tree_map: Map) -> tuple[int, int, bool, str]:
    """Return the size, height, balance state, and ASCII snapshot of ``tree_map``.

    Logic:
        This helper captures the UI-visible state of one TreeMap in a single
        call.
        1. Read the current size, height, and balance state from the map.
        2. Render the current ASCII diagram.
        3. Return the collected snapshot tuple.
    """
    return len(tree_map), tree_map.height(), tree_map.is_balanced(), tree_map.render_ascii()
# --------------------------------------------------------------- 

# --------------------------------------------------------------- _make_lab_result()
def _make_lab_result(
    *,
    section: str,
    operation: str,
    input_key: object | None,
    input_value: object | None,
    returned_value: object | None,
    success: bool,
    size_before: int,
    size_after: int,
    height_before: int | None,
    height_after: int | None,
    balanced_before: bool | None,
    balanced_after: bool | None,
    tree_before_ascii: str,
    tree_after_ascii: str,
    message: str,
) -> LabOperationResult:
    """Build a standardized :class:`LabOperationResult`.

    Logic:
        This helper packages one guided or manual lab action into the shared
        result model.
        1. Copy the provided operation metadata and before/after snapshots.
        2. Build one immutable ``LabOperationResult`` instance.
        3. Return the packaged result for UI rendering or tests.
    """
    return LabOperationResult(
        section=section,
        operation=operation,
        input_key=input_key,
        input_value=input_value,
        returned_value=returned_value,
        success=success,
        size_before=size_before,
        size_after=size_after,
        height_before=height_before,
        height_after=height_after,
        balanced_before=balanced_before,
        balanced_after=balanced_after,
        tree_before_ascii=tree_before_ascii,
        tree_after_ascii=tree_after_ascii,
        message=message,
    )
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# GUIDED LAB DEMOS
# ========================================================================
# Each demo returns a list of immutable operation snapshots so the UI can
# render the same validation story that the tests assert against.
#
# --------------------------------------------------------------- run_bst_demo()
def run_bst_demo(
    size: int = DEFAULT_DATASET_SIZE,
    dataset_type: str = "integers",
    insertion_pattern: str = "random",
    seed: int = DEFAULT_RANDOM_SEED,
) -> list[LabOperationResult]:
    """Run a guided BST demonstration with at least 50 items by default.

    Logic:
        1. Generate a comparable dataset and bulk-load it into a BST.
        2. Capture representative search, min/max, and traversal checkpoints.
        3. Return one immutable lab-result record per guided operation.
    """
    keys = generate_keys(
        size=size,
        dataset_type=dataset_type,
        insertion_pattern=insertion_pattern,
        seed=seed,
    )
    tree = BinarySearchTree()
    results: list[LabOperationResult] = []

    # Step 1: bulk-load the guided dataset and record the tree before/after state.
    size_before, height_before, balanced_before, before_ascii = _tree_snapshot(tree)
    for key in keys:
        tree.insert(key)
    size_after, height_after, balanced_after, after_ascii = _tree_snapshot(tree)
    results.append(
        _make_lab_result(
            section="BST Lab",
            operation="bulk_insert",
            input_key=None,
            input_value=None,
            returned_value=len(tree),
            success=len(tree) == len(keys),
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message=f"Built a BST with {len(tree)} {dataset_type} keys.",
        )
    )

    # Step 2: search for a representative middle key from the generated dataset.
    target_key = keys[len(keys) // 2]
    size_before, height_before, balanced_before, before_ascii = _tree_snapshot(tree)
    found = tree.search(target_key)
    size_after, height_after, balanced_after, after_ascii = _tree_snapshot(tree)
    results.append(
        _make_lab_result(
            section="BST Lab",
            operation="search",
            input_key=target_key,
            input_value=None,
            returned_value=found.key if found else None,
            success=found is not None,
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message=f"Successfully searched for key {target_key!r}.",
        )
    )

    # Step 3: capture the minimum/maximum boundary keys without mutating the tree.
    size_before, height_before, balanced_before, before_ascii = _tree_snapshot(tree)
    minimum = tree.min_key()
    maximum = tree.max_key()
    size_after, height_after, balanced_after, after_ascii = _tree_snapshot(tree)
    results.append(
        _make_lab_result(
            section="BST Lab",
            operation="min_max",
            input_key=None,
            input_value=None,
            returned_value={"min": minimum, "max": maximum},
            success=minimum is not None and maximum is not None,
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message="Collected the BST minimum and maximum keys.",
        )
    )

    # Step 4: verify that each traversal returns one entry per stored node.
    size_before, height_before, balanced_before, before_ascii = _tree_snapshot(tree)
    traversal_summary = {
        "inorder_count": len(tree.inorder()),
        "preorder_count": len(tree.preorder()),
        "postorder_count": len(tree.postorder()),
    }
    size_after, height_after, balanced_after, after_ascii = _tree_snapshot(tree)
    results.append(
        _make_lab_result(
            section="BST Lab",
            operation="traversals",
            input_key=None,
            input_value=None,
            returned_value=traversal_summary,
            success=all(count == len(tree) for count in traversal_summary.values()),
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message="Verified that all traversal outputs are non-empty and complete.",
        )
    )

    return results
# --------------------------------------------------------------- 

# --------------------------------------------------------------- run_traversal_demo()
def run_traversal_demo() -> list[LabOperationResult]:
    """Run the fixed traversal correctness demo used by tests and the UI.

    Logic:
        This function validates that the three traversal orders match a known
        BST shape.
        1. Build the fixed demo tree from the shared traversal fixture keys.
        2. Capture the actual traversal outputs and compare them with the
           expected orders.
        3. Return one lab-result record per traversal type.
    """
    tree = BinarySearchTree()
    # Step 1: build the known tree shape whose traversals have stable expected output.
    for key in TRAVERSAL_DEMO_KEYS:
        tree.insert(key)

    size_before, height_before, balanced_before, before_ascii = _tree_snapshot(tree)
    inorder = tree.inorder()
    preorder = tree.preorder()
    postorder = tree.postorder()
    size_after, height_after, balanced_after, after_ascii = _tree_snapshot(tree)

    # Expected traversal orders for the fixed demo tree shape.
    expected = {
        "inorder": [20, 30, 40, 50, 60, 70, 80],  # Left-root-right yields sorted keys
        "preorder": [50, 30, 20, 40, 70, 60, 80],  # Root-left-right visitation order
        "postorder": [20, 40, 30, 60, 80, 70, 50],  # Left-right-root visitation order
    }
    # Actual traversal outputs captured from the BST under test.
    actual = {
        "inorder": inorder,  # Measured in-order traversal output
        "preorder": preorder,  # Measured pre-order traversal output
        "postorder": postorder,  # Measured post-order traversal output
    }

    results: list[LabOperationResult] = []
    # MAIN ITERATION LOOP: package one lab result per traversal order so the UI
    # can display each correctness check independently.
    for traversal_name in ("inorder", "preorder", "postorder"):
        # Step 3: compare one actual traversal output against its fixed expectation.
        results.append(
            _make_lab_result(
                section="Traversal Demo",
                operation=traversal_name,
                input_key=None,
                input_value=None,
                returned_value=actual[traversal_name],
                success=actual[traversal_name] == expected[traversal_name],
                size_before=size_before,
                size_after=size_after,
                height_before=height_before,
                height_after=height_after,
                balanced_before=balanced_before,
                balanced_after=balanced_after,
                tree_before_ascii=before_ascii,
                tree_after_ascii=after_ascii,
                message=f"{traversal_name.title()} traversal matched the expected order.",
            )
        )

    return results
# --------------------------------------------------------------- 

# --------------------------------------------------------------- run_unbalanced_tree_demo()
def run_unbalanced_tree_demo(
    size: int = 15,
    dataset_type: str = "integers",
    seed: int = DEFAULT_RANDOM_SEED,
) -> list[LabOperationResult]:
    """Compare sorted-insertion and balanced-insertion tree shapes.

    Logic:
        This function contrasts an intentionally skewed tree with a
        median-first comparison tree.
        1. Generate sorted and balanced insertion orders for the same dataset.
        2. Build one BST from each insertion order.
        3. Return result records that compare height and balance outcomes.
    """
    sorted_keys = generate_keys(size, dataset_type, "sorted", seed)
    balanced_keys = generate_keys(size, dataset_type, "balanced", seed)

    sorted_tree = BinarySearchTree()
    balanced_tree = BinarySearchTree()
    # Step 1: build the intentionally skewed sorted tree.
    for key in sorted_keys:
        sorted_tree.insert(key)
    # Step 2: build the median-first tree used as the healthier comparison shape.
    for key in balanced_keys:
        balanced_tree.insert(key)

    sorted_size, sorted_height, sorted_balanced, sorted_ascii = _tree_snapshot(sorted_tree)
    (
        balanced_size,
        balanced_height,
        balanced_balanced,
        balanced_ascii,
    ) = _tree_snapshot(balanced_tree)
    # End the balanced tree demo.
    return [
        # Return a single detailed result for the skewed-insertion tree.
        # This serves as the primary "unbalanced" data point for the demo.
        _make_lab_result(
            section="Balance Demo",
            operation="sorted_insertion",
            input_key=None,
            input_value=None,
            returned_value={
                "height": sorted_height,  # Observed height for the skewed tree
                "is_balanced": sorted_balanced,  # Whether the skewed tree passed the balance rule
                "unbalanced_keys": sorted_tree.unbalanced_keys(),  # Keys at unbalanced nodes
            },  
            success=sorted_balanced is False,
            size_before=0,
            size_after=sorted_size,
            height_before=-1,
            height_after=sorted_height,
            balanced_before=True,
            balanced_after=sorted_balanced,
            tree_before_ascii="(empty tree)",
            tree_after_ascii=sorted_ascii,
            message="Sorted insertions produced an unbalanced BST.",
        ),
        # Return a single detailed result for the healthier median-first tree.
        # This shows what happens when the same number of keys are inserted in balanced order.
        _make_lab_result(
            section="Balance Demo",
            operation="balanced_insertion",
            input_key=None,
            input_value=None,
            returned_value={
                "height": balanced_height,  # Observed height for the median-first tree
                "is_balanced": balanced_balanced,  # Whether the tree stayed balanced
                "unbalanced_keys": balanced_tree.unbalanced_keys(),  # Keys at any unbalanced nodes
            },
            success=balanced_balanced is True,
            size_before=0,
            size_after=balanced_size,
            height_before=-1,
            height_after=balanced_height,
            balanced_before=True,
            balanced_after=balanced_balanced,
            tree_before_ascii="(empty tree)",
            tree_after_ascii=balanced_ascii,
            message="Balanced insertion order kept the BST well-shaped.",
        ),
        # Return a single detailed result for the comparison between the two tree shapes.     
        _make_lab_result(
            section="Balance Demo",
            operation="comparison",
            input_key=None,
            input_value=None,
            returned_value={
                "sorted_height": sorted_height,  # Height after sorted insertion order
                "balanced_height": balanced_height,  # Height after median-first insertion order
            },
            success=sorted_height > balanced_height,
            size_before=sorted_size,
            size_after=balanced_size,
            height_before=sorted_height,
            height_after=balanced_height,
            balanced_before=sorted_balanced,
            balanced_after=balanced_balanced,
            tree_before_ascii=sorted_ascii,
            tree_after_ascii=balanced_ascii,
            message="Balanced insertion order produced a shorter tree than sorted insertion.",
        ),
    ]
# --------------------------------------------------------------- 

# --------------------------------------------------------------- run_map_demo()
def run_map_demo(
    size: int = 10,
    dataset_type: str = "integers",
    insertion_pattern: str = "random",
    seed: int = DEFAULT_RANDOM_SEED,
) -> list[LabOperationResult]:
    """Run a guided TreeMap demo covering put, update, get, and delete.

    Logic:
        1. Generate key-value items and bulk-load them into a fresh TreeMap.
        2. Demonstrate update, get, and delete behavior on representative keys.
        3. Return before/after snapshots that the UI can render directly.
    """
    items = generate_map_items(size, dataset_type, insertion_pattern, seed)
    tree_map = Map()
    results: list[LabOperationResult] = []

    # Step 1: bulk-load the generated key-value pairs.
    size_before, height_before, balanced_before, before_ascii = _map_snapshot(tree_map)
    for key, value in items:
        tree_map.put(key, value)
    size_after, height_after, balanced_after, after_ascii = _map_snapshot(tree_map)
    results.append(
        _make_lab_result(
            section="Map Lab",
            operation="bulk_load",
            input_key=None,
            input_value=None,
            returned_value=len(tree_map),
            success=len(tree_map) == len(items),
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message=f"Loaded {len(tree_map)} key-value pairs into the TreeMap.",
        )
    )

    # Step 2: update one existing key to prove size stays stable on overwrite.
    existing_key, existing_value = items[0]
    updated_value: dict[str, Any] = {
        "id": "updated",  # Marker that this payload came from the overwrite step
        "label": "updated-value",  # Human-friendly label shown after the update
        "source_key": existing_key,  # Original key retained for traceability
    }
    # Step 3: update one existing key to prove size stays stable on overwrite.
    size_before, height_before, balanced_before, before_ascii = _map_snapshot(tree_map)
    tree_map.put(existing_key, updated_value)
    size_after, height_after, balanced_after, after_ascii = _map_snapshot(tree_map)
    results.append(
        _make_lab_result(
            section="Map Lab",
            operation="update",
            input_key=existing_key,
            input_value=updated_value,
            returned_value=tree_map.get(existing_key),
            success=tree_map.get(existing_key) == updated_value,
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message="Updated an existing key without changing the TreeMap size.",
        )
    )

    # Step 3: retrieve a middle key to validate lookup behavior.
    middle_key, middle_value = items[len(items) // 2]
    size_before, height_before, balanced_before, before_ascii = _map_snapshot(tree_map)
    fetched_value = tree_map.get(middle_key)
    size_after, height_after, balanced_after, after_ascii = _map_snapshot(tree_map)
    results.append(
        _make_lab_result(
            section="Map Lab",
            operation="get",
            input_key=middle_key,
            input_value=None,
            returned_value=fetched_value,
            success=fetched_value == middle_value,
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message=f"Retrieved key {middle_key!r} from the TreeMap.",
        )
    )

    # Step 4: delete the last inserted key and verify it is gone.
    delete_key, _ = items[-1]
    size_before, height_before, balanced_before, before_ascii = _map_snapshot(tree_map)
    deleted = tree_map.delete(delete_key)
    size_after, height_after, balanced_after, after_ascii = _map_snapshot(tree_map)
    results.append(
        _make_lab_result(
            section="Map Lab",
            operation="delete",
            input_key=delete_key,
            input_value=None,
            returned_value=deleted,
            success=deleted and not tree_map.contains_key(delete_key),
            size_before=size_before,
            size_after=size_after,
            height_before=height_before,
            height_after=height_after,
            balanced_before=balanced_before,
            balanced_after=balanced_after,
            tree_before_ascii=before_ascii,
            tree_after_ascii=after_ascii,
            message=f"Deleted key {delete_key!r} from the TreeMap.",
        )
    )

    return results
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# BENCHMARK VALIDATION AND REPORTING
# ========================================================================
# These helpers collapse raw benchmark outputs into rubric-style checks and
# short summary text for the Streamlit benchmark tab.
#
# --------------------------------------------------------------- run_benchmark_validation()
def run_benchmark_validation(results_df: pd.DataFrame) -> dict[str, object]:
    """Summarize whether benchmark results match expected rubric signals.

    Logic:
        1. Return a stable empty summary when no benchmark data exists.
        2. Compare TreeMap and ListMap timings for the random-hit workload.
        3. Check whether sorted insertion produced the expected imbalance signal.
    """
    # VALIDATION: return a stable summary schema even before any results exist.
    if results_df.empty:
        return {
            "has_results": False,  # Signals that no benchmark run has been captured yet
            "tree_beats_list_count": 0,  # Count of sizes where TreeMap beat ListMap
            "tree_beats_list_sizes": [],  # Concrete sizes where TreeMap was faster
            "sorted_scenario_unbalanced": False,  # Whether sorted insertion showed skew
            "summary_lines": ["No benchmark results available yet."],  # UI-ready summary text
        }

    # Step 1: pivot the results so TreeMap and ListMap timings align by case.
    pivot = results_df.pivot_table(
        index=["scenario", "query_mode", "size"],
        columns="method",
        values="time_ms",
        aggfunc="min",
    ).reset_index()
    # DISPATCH: compare runtimes only when both TreeMap and ListMap timing
    # columns survived the pivot step.
    if "TreeMap" in pivot and "ListMap" in pivot:
        faster_rows = pivot[
            (pivot["scenario"] == "random_insertion")
            & (pivot["query_mode"] == "hits")
            & (pivot["TreeMap"] < pivot["ListMap"])
        ]
    else:
        faster_rows = pivot.iloc[0:0]

    # Step 2: inspect the sorted-insertion TreeMap rows for the expected skew signal.
    tree_rows = results_df[results_df["method"] == "TreeMap"].copy()
    sorted_rows = tree_rows[tree_rows["scenario"] == "sorted_insertion"]
    sorted_scenario_unbalanced = (
        not sorted_rows.empty and (sorted_rows["is_balanced"] == False).any()
    )

    # Step 3: collapse the rubric signals into display-ready summary lines.
    summary_lines = [
        (
            f"TreeMap was faster than ListMap for random hit searches at "
            f"{len(faster_rows)} tested sizes."
        ),
        (
            "Sorted insertion scenario reported an unbalanced tree."
            if sorted_scenario_unbalanced
            else "Sorted insertion scenario did not report an unbalanced tree."
        ),
    ]

    # Summary payload fields reused by the benchmark tab and tests.
    return {
        "has_results": True,  # Signals that at least one benchmark run exists
        "tree_beats_list_count": int(len(faster_rows)),  # Number of favorable TreeMap cases
        "tree_beats_list_sizes": faster_rows["size"].tolist(),  # Specific favorable sizes
        "sorted_scenario_unbalanced": bool(sorted_scenario_unbalanced),  # Skew-detection flag
        "summary_lines": summary_lines,  # UI-ready narrative summary lines
    }
# --------------------------------------------------------------- 

# --------------------------------------------------------------- summarize_benchmark_validation()
def summarize_benchmark_validation(validation: dict[str, object]) -> str:
    """Collapse benchmark-validation output into one display-friendly string.

    Logic:
        This helper converts the validation summary list into one sentence
        block for the UI.
        1. Read the prepared summary lines from the validation payload.
        2. Return a placeholder message when no lines are available.
        3. Join the summary lines into one display-friendly string.
    """
    summary_lines = validation.get("summary_lines", [])
    # VALIDATION: keep a stable placeholder message when the summary payload is empty.
    if not summary_lines:
        return "No validation summary available."
    return " ".join(str(line) for line in summary_lines)
# ---------------------------------------------------------------  

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------   
