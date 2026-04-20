# -------------------------------------------------------------------------
# File: streamlit_app.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Streamlit application entry point for the Algorithm and Data Structure Comparison Tool
# (Portfolio Milestone Module 4). The app exposes seven tabs:
#   1. Overview
#   2. Dataset Builder
#   3. Structure Playground
#   4. Compare Structures
#   5. Benchmark Lab
#   6. Written Analysis
#   7. Recommendation Guide
# The app is the assignment's required testing/comparison UI; CLI demos are
# intentionally not used as the test interface.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit entry point for the Module 4 Algorithm and Data Structure Comparison Tool."""

# ________________
# Imports
#

from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd
import streamlit as st

# SETUP: ensure Module 4 root is on sys.path so package imports resolve
_MODULE_ROOT = Path(__file__).resolve().parent
if str(_MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(_MODULE_ROOT))

from analysis.benchmark_structures import (  # noqa: E402
    DEFAULT_REPEATS,
    DEFAULT_SIZES,
    compute_operation_winners,
    load_results_csv,
    run_benchmarks,
    save_operation_winners_csv,
    save_results_csv,
)
from data.dataset_manager import (  # noqa: E402
    DATASET_TYPES,
    DEFAULT_DATASET_SIZE,
    DEFAULT_RANDOM_SEED,
    generate_dataset_by_type,
    parse_manual_input,
    validate_dataset,
)
from data_structures import Deque, LinkedList, Queue, Stack  # noqa: E402
from models.operation_result import OperationResult  # noqa: E402
from ui.streamlit_helpers import (  # noqa: E402
    render_analysis_markdown_file,
    render_benchmark_charts,
    render_benchmark_table,
    render_comparison_grid,
    render_complexity_table,
    render_dataset_info,
    render_header,
    render_operation_result,
    render_structure_state,
)

# __________________________________________________________________________
# Configuration
#

# ========================================================================
# Page Config
# ========================================================================

st.set_page_config(
    page_title="Algorithm and Data Structure Comparison Tool",
    page_icon=_MODULE_ROOT / "icon.png",
    layout="wide",
    initial_sidebar_state="auto",
)

# Paths to Markdown deliverables and CSV artifacts
_ANALYSIS_DIR = _MODULE_ROOT / "analysis"
_BENCHMARK_CSV = _ANALYSIS_DIR / "benchmark_results.csv"
_WINNERS_CSV = _ANALYSIS_DIR / "operation_winners.csv"
_WRITTEN_ANALYSIS = _ANALYSIS_DIR / "written_analysis.md"
_RECOMMENDATION = _ANALYSIS_DIR / "recommendation_guide.md"

_STRUCTURE_NAMES = ("Stack", "Queue", "Deque", "LinkedList")

# Display labels for the Dataset Builder selectbox. The keys are the
# underlying identifiers used by ``generate_dataset_by_type`` and stored
# in session state; the values are the friendlier labels shown to the user.
_DATASET_TYPE_LABELS = {
    "sequential": "sequential (ordered)",
    "random": "random (unordered)",
    "reverse": "reverse",
    "manual": "manual",
}

# __________________________________________________________________________
# Session State
#

# ========================================================================
# Defaults
# ========================================================================

# --------------------------------------------------------------- _init_session_state()
def _init_session_state() -> None:
    """Initialize all required session state keys with safe defaults."""
    defaults: dict[str, object] = {
        "dataset": None,
        "dataset_type": "sequential",
        "dataset_size": DEFAULT_DATASET_SIZE,
        "structure_state": {},
        "structure_objects": {},
        "active_structure": "Stack",
        "last_operation_result": None,
        # Identifies which playground section produced the last result, so
        # the result panel can render inline below the triggering buttons.
        "last_section": None,
        "benchmark_df": None,
        "operation_winners_df": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
# --------------------------------------------------------------- end _init_session_state()


_init_session_state()

# __________________________________________________________________________
# Helpers
#

# ========================================================================
# Structure Utilities
# ========================================================================

# --------------------------------------------------------------- _logical_state()
def _logical_state(structure_name: str, structure: object) -> list[int]:
    """Return the logical state of *structure* in display order.

    The Stack branch reverses ``to_list()`` so that the conceptual *top* of
    the stack appears on the **left** of the playground display. This is a
    pure presentation tweak — the underlying ``Stack`` class is unchanged
    (``push``/``pop``/``peek`` remain O(1) ``list.append`` / ``list.pop``).
    """
    if structure_name == "Stack":
        return list(reversed(structure.to_list()))  # type: ignore[union-attr]
    if structure_name == "Queue":
        return list(structure.to_list())  # type: ignore[union-attr]
    if structure_name == "Deque":
        return list(structure.to_list())  # type: ignore[union-attr]
    if structure_name == "LinkedList":
        return list(structure.display())  # type: ignore[union-attr]
    return []
# --------------------------------------------------------------- end _logical_state()


# --------------------------------------------------------------- _raw_state()
def _raw_state(structure_name: str, structure: object) -> list[int] | None:
    """Return the raw internal list for course-aligned structures."""
    if structure_name in ("Queue", "Deque"):
        return list(structure.to_internal_list())  # type: ignore[union-attr]
    return None
# --------------------------------------------------------------- end _raw_state()


# --------------------------------------------------------------- _build_fresh_structure()
def _build_fresh_structure(structure_name: str, values: list[int]) -> object:
    """Build a brand-new structure of *structure_name* loaded with *values*.

    For ``Stack`` we reverse the dataset before constructing so that, after
    the matching reversal in :func:`_logical_state`, the playground displays
    the *first* dataset value on the left (logical top of the stack). The
    ``Stack`` class itself is untouched.
    """
    if structure_name == "Stack":
        return Stack(list(reversed(values)))
    if structure_name == "Queue":
        return Queue(values)
    if structure_name == "Deque":
        return Deque(values)
    if structure_name == "LinkedList":
        return LinkedList(values)
    raise ValueError(f"Unknown structure: {structure_name!r}")
# --------------------------------------------------------------- end _build_fresh_structure()


# --------------------------------------------------------------- _record_op()
def _record_op(
    structure_name: str,
    operation: str,
    op_callable,
    *,
    input_value: int | None = None,
    anchor_value: int | None = None,
    complexity: str = "O(?)",
    structure: object,
) -> OperationResult:
    """Time *op_callable* once and capture an :class:`OperationResult`."""
    state_before = _logical_state(structure_name, structure)
    size_before = len(state_before)
    start = time.perf_counter()
    returned = op_callable()
    elapsed = time.perf_counter() - start
    state_after = _logical_state(structure_name, structure)
    size_after = len(state_after)
    return OperationResult(
        structure=structure_name,
        operation=operation,
        input_value=input_value,
        anchor_value=anchor_value,
        returned_value=returned,
        size_before=size_before,
        size_after=size_after,
        elapsed_time=elapsed,
        complexity=complexity,
        state_before=state_before,
        state_after=state_after,
        step_trace=[],
    )
# --------------------------------------------------------------- end _record_op()


# --------------------------------------------------------------- _record_and_locate()
def _record_and_locate(section_id: str, *args, **kwargs) -> None:
    """Record an operation result and stamp it as belonging to *section_id*.

    Args:
        section_id: Identifier of the playground section that triggered the
            operation. Used by :func:`_maybe_render_section_result` so the
            result panel can render inline next to the buttons that produced
            it instead of in the right-hand view column.
        *args: Forwarded positional args for :func:`_record_op`.
        **kwargs: Forwarded keyword args for :func:`_record_op`.
    """
    st.session_state["last_operation_result"] = _record_op(*args, **kwargs)
    st.session_state["last_section"] = section_id
# --------------------------------------------------------------- end _record_and_locate()


# --------------------------------------------------------------- _maybe_render_section_result()
def _maybe_render_section_result(section_id: str, structure_name: str) -> None:
    """Render the last operation result iff it came from *section_id*.

    Args:
        section_id: The section's identifier (must match the value passed
            to :func:`_record_and_locate` when the operation was recorded).
        structure_name: Currently active structure; results from a different
            structure are silently skipped.
    """
    if st.session_state.get("last_section") != section_id:
        return
    result = st.session_state.get("last_operation_result")
    if result is None or result.structure != structure_name:
        return
    render_operation_result(result)
# --------------------------------------------------------------- end _maybe_render_section_result()

# __________________________________________________________________________
# UI: Header
#

render_header()

tabs = st.tabs(
    [
        "Overview",
        "Dataset Builder",
        "Structure Playground",
        "Compare Structures",
        "Benchmark Lab",
        "Written Analysis",
        "Recommendation Guide",
    ]
)

# __________________________________________________________________________
# Tab 1 — Overview
#

with tabs[0]:
    st.header("Project Overview")
    st.markdown(
        """
This Algorithm and Data Structure Comparison Tool compares the following
linear data structures:

* **Stack** — a list-backed LIFO structure with `push`, `pop`, and `peek`.
* **Queue** — a list-backed FIFO structure with `enqueue`, `dequeue`, and `front`.
* **Deque** — a list-backed double-ended queue with add and remove operations at both ends.
* **LinkedList** — a custom doubly linked list with front and rear inserts, search,
  traversal, and deletion support.

Use the tabs above to build datasets, run individual structure operations,
compare their time complexity, benchmark them, and read the written analysis
and recommendation guide.
        """
    )
    #--- stack 
    st.subheader("Stack")
    st.info(
        "A stack is a last-in, first-out (LIFO) structure. The most recently "
        "added item is the first one removed. In this project the stack is "
        "implemented with a Python list, so `push`, `pop`, and `peek` all act "
        "on the top of the structure and run in O(1) time."
    )
    #--- Queue 
    st.subheader("Queue")
    st.info(
        "A queue is a first-in, first-out (FIFO) structure. The earliest item "
        "added is the first one removed. This module uses the course-aligned "
        "list-backed implementation where `enqueue` inserts at index 0 and "
        "`dequeue` removes from the rear, making enqueue O(n) and dequeue/front O(1)."
    )
    # --- Deque 
    st.subheader("Deque")
    st.info(
        "A deque supports insertion and removal from both the front and rear. "
        "This makes it more flexible than a stack or queue when a workload "
        "needs two-ended access. In the list-backed implementation, rear-end "
        "operations are O(1), while front-end operations that shift elements "
        "are O(n)."
    )
    #--- LinkedList 
    st.subheader("LinkedList")
    st.info(
        "The linked list in this project is a custom doubly linked structure "
        "built from nodes with `prev` and `next` references. It keeps both "
        "head and tail pointers, so inserts at either end are O(1), while "
        "searching, traversing, and most middle-position operations are O(n)."
    )
    #--- key concepts 
    st.subheader("Key Concepts")
    st.info(
        "**LIFO vs FIFO** describes the removal order of a structure. A stack "
        "uses LIFO behavior, while a queue uses FIFO behavior.\n\n"
        "**List-backed vs node-based** compares contiguous array storage "
        "against pointer-linked nodes. Stack, Queue, and Deque are backed by "
        "Python lists, while LinkedList is built from custom nodes.\n\n"
        "**Doubly linked traversal** means each node stores links in both "
        "directions. That makes front and rear updates efficient and allows "
        "forward or reverse traversal of the list.\n\n"
        "**Big-O notation** describes how operation cost grows as input size "
        "increases. This project focuses on why some operations stay O(1) "
        "while others become O(n) because of shifting or traversal."
    )   
    #--- how to use this tool 
    st.subheader("How to Use This Tool")
    st.info(
        "Use Dataset Builder to generate or enter integer data, then load that "
        "data into the Structure Playground to test operations. Use Compare "
        "Structures to review supported operations and Big-O behavior side by "
        "side. Use Benchmark Lab to measure performance at larger sizes, then "
        "read the Written Analysis and Recommendation Guide to connect the "
        "results to practical design choices."
    )
    #--- project files      
    st.subheader("Project Files")
    st.markdown(
        f"""
- README — `{(_MODULE_ROOT / 'README.md').name}`
- Task plan — `{(_MODULE_ROOT / 'task.md').name}`
- Implementation plan — `{(_MODULE_ROOT / 'implementation_plan.md').name}`
- Reference PDFs — `ref_docs/` (Stack, Queue, LinkedList, Doubly LinkedList,
  Module 4 lecture)
        """
    )

# __________________________________________________________________________
# Tab 2 — Dataset Builder
#

with tabs[1]:
    st.header("Dataset Builder")
    col_left, col_right = st.columns([2, 3])
    #--- dataset builder 
    with col_left:
        #--- dataset type 
        dtype = st.selectbox(
            "Dataset type",
            DATASET_TYPES,
            index=DATASET_TYPES.index(st.session_state["dataset_type"])
            if st.session_state["dataset_type"] in DATASET_TYPES
            else 0,
            format_func=lambda dt: _DATASET_TYPE_LABELS.get(dt, dt),
        )
        #--- dataset size 
        size_value = st.number_input(
            "Size",
            min_value=1,
            max_value=1_000_000,
            value=int(st.session_state["dataset_size"]),
            step=100,
        )
        #--- quick presets 
        st.caption("Quick presets")
        preset_cols = st.columns(4)
        for idx, preset in enumerate([1_000, 5_000, 10_000, 50_000]):
            if preset_cols[idx].button(f"{preset:,}", key=f"preset_{preset}"):
                size_value = preset
                st.session_state["dataset_size"] = preset
        seed_value = st.number_input(
            "Random seed",
            min_value=0,
            max_value=10_000_000,
            value=DEFAULT_RANDOM_SEED,
            help="Used by the random generator for reproducibility.",
        )
        #--- manual input 
        manual_text = ""
        if dtype == "manual":
            manual_text = st.text_area(
                "Comma-separated integers",
                value="10, 20, 30, 40, 50",
                height=120,
            )
        #--- generate dataset button 
        if st.button("Generate Dataset", type="primary"):
            try:
                if dtype == "manual":
                    data = parse_manual_input(manual_text)
                else:
                    data = generate_dataset_by_type(
                        dtype,
                        size=int(size_value),
                        seed=int(seed_value),
                    )
                validate_dataset(data)
                st.session_state["dataset"] = data
                st.session_state["dataset_type"] = dtype
                st.session_state["dataset_size"] = len(data)
                st.success(f"Generated {len(data):,} values.")
            except (ValueError, TypeError) as exc:
                st.error(f"Could not generate dataset: {exc}")
    #--- dataset info 
    with col_right:
        if st.session_state["dataset"] is None:
            st.info("Generate or paste a dataset on the left to get started.")
        else:
            render_dataset_info(
                data=st.session_state["dataset"],
                dataset_type=_DATASET_TYPE_LABELS.get(
                    st.session_state["dataset_type"],
                    st.session_state["dataset_type"],
                ),
                size=st.session_state["dataset_size"],
            )

# __________________________________________________________________________
# Tab 3 — Structure Playground
#

with tabs[2]:
    st.header("Structure Playground")
    #--- structure playground 
    if st.session_state["dataset"] is None:
        st.warning(
            "Generate a dataset on the **Dataset Builder** tab first."
        )
    else:
        controls_col, view_col = st.columns([2, 3])
        #--- controls column 
        with controls_col:
            structure_name = st.selectbox(
                "Structure",
                _STRUCTURE_NAMES,
                index=_STRUCTURE_NAMES.index(
                    st.session_state["active_structure"]
                ),
                key="active_structure",
            )
            #--- load current dataset button 
            if st.button("Load Current Dataset", type="primary"):
                fresh = _build_fresh_structure(
                    structure_name, list(st.session_state["dataset"])
                )
                st.session_state["structure_objects"][structure_name] = fresh
                st.session_state["last_operation_result"] = None
                st.session_state["last_section"] = None
                st.success(
                    f"Loaded {len(st.session_state['dataset']):,} values "
                    f"into a fresh {structure_name}."
                )
            #--- structure object dataset
            structure = st.session_state["structure_objects"].get(structure_name)
            if structure is None:
                st.info(
                    "Click Load Current Dataset to populate this structure."
                )
            else:
                st.divider()
                st.subheader(f"{structure_name} operations")
                #--- stack operations 
                if structure_name == "Stack":
                    st.subheader("Operations with a value")
                    val = st.number_input(
                        "value",
                        min_value=-1_000_000,
                        max_value=1_000_000,
                        value=0,
                        key="stack_value",
                    )
                    #--- push operation 
                    push_col = st.columns([1, 3])
                    if push_col[0].button("push", key="op_push"):
                        _record_and_locate(
                            "stack_with_value",
                            structure_name,
                            "push",
                            lambda: structure.push(int(val)),  # type: ignore[union-attr]
                            input_value=int(val),
                            complexity="O(1)",
                            structure=structure,
                        )
                    _maybe_render_section_result("stack_with_value", structure_name)
                    #--- stack operations without input 
                    st.divider()
                    st.subheader("Operations without input")
                    no_cols = st.columns(4)
                    #--- pop operation 
                    if no_cols[0].button("pop", key="op_pop"):
                        _record_and_locate(
                            "stack_no_input",
                            structure_name,
                            "pop",
                            lambda: structure.pop(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- peek operation 
                    if no_cols[1].button("peek", key="op_peek"):
                        _record_and_locate(
                            "stack_no_input",
                            structure_name,
                            "peek",
                            lambda: structure.peek(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- is_empty operation 
                    if no_cols[2].button("isEmpty", key="op_is_empty"):
                        _record_and_locate(
                            "stack_no_input",
                            structure_name,
                            "isEmpty",
                            lambda: structure.isEmpty(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- clear operation 
                    if no_cols[3].button("clear", key="op_clear"):
                        _record_and_locate(
                            "stack_no_input",
                            structure_name,
                            "clear",
                            lambda: structure.clear() or None,  # type: ignore[union-attr]
                            complexity="O(n)",
                            structure=structure,
                        )
                    _maybe_render_section_result("stack_no_input", structure_name)
                #--- queue operations 
                elif structure_name == "Queue":
                    st.subheader("Operations with a value")
                    val = st.number_input(
                        "value",
                        min_value=-1_000_000,
                        max_value=1_000_000,
                        value=0,
                        key="queue_value",
                    )
                    #--- enqueue operation 
                    enq_col = st.columns([1, 3])
                    if enq_col[0].button("enqueue", key="q_enq"):
                        _record_and_locate(
                            "queue_with_value",
                            structure_name,
                            "enqueue",
                            lambda: structure.enqueue(int(val)),  # type: ignore[union-attr]
                            input_value=int(val),
                            complexity="O(n)",
                            structure=structure,
                        )
                    _maybe_render_section_result("queue_with_value", structure_name)
                    #--- queue operations without input 
                    st.divider()
                    st.subheader("Operations without input")
                    no_cols = st.columns(4)
                    #--- dequeue operation 
                    if no_cols[0].button("dequeue", key="q_deq"):
                        _record_and_locate(
                            "queue_no_input",
                            structure_name,
                            "dequeue",
                            lambda: structure.dequeue(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- front operation 
                    if no_cols[1].button("front", key="q_front"):
                        _record_and_locate(
                            "queue_no_input",
                            structure_name,
                            "front",
                            lambda: structure.front(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- is_empty operation 
                    if no_cols[2].button("isEmpty", key="q_isempty"):
                        _record_and_locate(
                            "queue_no_input",
                            structure_name,
                            "isEmpty",
                            lambda: structure.isEmpty(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- clear operation 
                    if no_cols[3].button("clear", key="q_clear"):
                        _record_and_locate(
                            "queue_no_input",
                            structure_name,
                            "clear",
                            lambda: structure.clear() or None,  # type: ignore[union-attr]
                            complexity="O(n)",
                            structure=structure,
                        )
                    _maybe_render_section_result("queue_no_input", structure_name)
                #--- deque operations 
                elif structure_name == "Deque":
                    st.subheader("Operations with a value")
                    val = st.number_input(
                        "value",
                        min_value=-1_000_000,
                        max_value=1_000_000,
                        value=0,
                        key="deque_value",
                    )
                    #--- add front operation 
                    add_cols = st.columns(2)
                    if add_cols[0].button("addFront", key="d_addF"):
                        _record_and_locate(
                            "deque_with_value",
                            structure_name,
                            "addFront",
                            lambda: structure.addFront(int(val)) or None,  # type: ignore[union-attr]
                            input_value=int(val),
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- add rear operation 
                    if add_cols[1].button("addRear", key="d_addR"):
                        _record_and_locate(
                            "deque_with_value",
                            structure_name,
                            "addRear",
                            lambda: structure.addRear(int(val)) or None,  # type: ignore[union-attr]
                            input_value=int(val),
                            complexity="O(n)",
                            structure=structure,
                        )
                    _maybe_render_section_result("deque_with_value", structure_name)
                    #--- deque operations without input     
                    st.divider()
                    st.subheader("Operations without input")
                    rem_cols = st.columns(2)
                    #--- remove front operation 
                    if rem_cols[0].button("removeFront", key="d_remF"):
                        _record_and_locate(
                            "deque_no_input",
                            structure_name,
                            "removeFront",
                            lambda: structure.removeFront(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- remove rear operation 
                    if rem_cols[1].button("removeRear", key="d_remR"):
                        _record_and_locate(
                            "deque_no_input",
                            structure_name,
                            "removeRear",
                            lambda: structure.removeRear(),  # type: ignore[union-attr]
                            complexity="O(n)",
                            structure=structure,
                        )
                    #--- peek front operation 
                    peek_cols = st.columns(2)
                    if peek_cols[0].button("peekFront", key="d_pF"):
                        _record_and_locate(
                            "deque_no_input",
                            structure_name,
                            "peekFront",
                            lambda: structure.peekFront(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- peek rear operation     
                    if peek_cols[1].button("peekRear", key="d_pR"):
                        _record_and_locate(
                            "deque_no_input",
                            structure_name,
                            "peekRear",
                            lambda: structure.peekRear(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- is_empty operation  
                    meta_cols = st.columns(2)
                    if meta_cols[0].button("isEmpty", key="d_isempty"):
                        _record_and_locate(
                            "deque_no_input",
                            structure_name,
                            "isEmpty",
                            lambda: structure.isEmpty(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- clear operation     
                    if meta_cols[1].button("clear", key="d_clear"):
                        _record_and_locate(
                            "deque_no_input",
                            structure_name,
                            "clear",
                            lambda: structure.clear() or None,  # type: ignore[union-attr]
                            complexity="O(n)",
                            structure=structure,
                        )
                    _maybe_render_section_result("deque_no_input", structure_name)
                #--- linked list operations 
                elif structure_name == "LinkedList":
                    st.subheader("Insert")
                    ins_val = st.number_input(
                        "value",
                        min_value=-1_000_000,
                        max_value=1_000_000,
                        value=0,
                        key="ll_insert_value",
                    )
                    #--- insert mode selection 
                    ins_mode = st.selectbox(
                        "mode",
                        ("front", "rear", "before", "after"),
                        key="ll_mode",
                    )
                    #--- anchor selection 
                    anchor_val: int | None = None
                    if ins_mode in ("before", "after"):
                        anchor_val = int(
                            st.number_input(
                                "anchor",
                                min_value=-1_000_000,
                                max_value=1_000_000,
                                value=0,
                                key="ll_anchor",
                            )
                        )
                    #--- insert operation    
                    ins_col = st.columns([1, 3])
                    if ins_col[0].button("insert", key="ll_ins"):
                        complexity = (
                            "O(1)" if ins_mode in ("front", "rear")
                            else "O(n)"
                        )
                        _record_and_locate(
                            "ll_insert",
                            structure_name,
                            f"insert ({ins_mode})",
                            lambda: structure.insert(  # type: ignore[union-attr]
                                int(ins_val),
                                mode=ins_mode,
                                anchor=anchor_val,
                            ),
                            input_value=int(ins_val),
                            anchor_value=anchor_val,
                            complexity=complexity,
                            structure=structure,
                        )
                    _maybe_render_section_result("ll_insert", structure_name)
                    #--- delete operation 
                    st.divider()
                    st.subheader("Delete")
                    del_mode = st.selectbox(
                        "mode",
                        ("value", "front", "rear", "before", "after"),
                        key="ll_delete_mode",
                    )
                    #--- delete value selection 
                    del_val: int | None = None
                    del_anchor: int | None = None
                    if del_mode == "value":
                        del_val = int(
                            st.number_input(
                                "value",
                                min_value=-1_000_000,
                                max_value=1_000_000,
                                value=0,
                                key="ll_delete_value",
                            )
                        )
                    #--- delete anchor selection 
                    if del_mode in ("before", "after"):
                        del_anchor = int(
                            st.number_input(
                                "anchor",
                                min_value=-1_000_000,
                                max_value=1_000_000,
                                value=0,
                                key="ll_delete_anchor",
                            )
                        )
                    #--- delete operation    
                    del_col = st.columns([1, 3])
                    if del_col[0].button("delete", key="ll_del"):
                        del_complexity = (
                            "O(1)" if del_mode in ("front", "rear")
                            else "O(n)"
                        )
                        _record_and_locate(
                            "ll_delete",
                            structure_name,
                            f"delete ({del_mode})",
                            lambda: structure.delete(  # type: ignore[union-attr]
                                del_val,
                                mode=del_mode,
                                anchor=del_anchor,
                            ),
                            input_value=del_val,
                            anchor_value=del_anchor,
                            complexity=del_complexity,
                            structure=structure,
                        )
                    _maybe_render_section_result("ll_delete", structure_name)
                    #--- search operation 
                    st.divider()
                    st.subheader("Search")
                    search_val = int(
                        st.number_input(
                            "value",
                            min_value=-1_000_000,
                            max_value=1_000_000,
                            value=0,
                            key="ll_search_value",
                        )
                    )
                    #--- search operation 
                    search_col = st.columns([1, 3])
                    if search_col[0].button("search", key="ll_srch"):
                        _record_and_locate(
                            "ll_search",
                            structure_name,
                            "search",
                            lambda: (
                                None if structure.search(int(search_val)) is None  # type: ignore[union-attr]
                                else structure.search(int(search_val)).data  # type: ignore[union-attr]
                            ),
                            input_value=int(search_val),
                            complexity="O(n)",
                            structure=structure,
                        )
                    _maybe_render_section_result("ll_search", structure_name)
                    #--- display operation 
                    st.divider()
                    st.subheader("Display")
                    reverse_display = st.checkbox(
                        "reverse", value=False, key="ll_rev"
                    )
                    disp_col = st.columns([1, 3])
                    if disp_col[0].button("display", key="ll_disp"):
                        _record_and_locate(
                            "ll_display",
                            structure_name,
                            "display" + (" reverse" if reverse_display else ""),
                            lambda: structure.display(reverse=reverse_display),  # type: ignore[union-attr]
                            complexity="O(n)",
                            structure=structure,
                        )
                    _maybe_render_section_result("ll_display", structure_name)
                    #--- operations without input 
                    st.divider()
                    st.subheader("Operations without input")
                    meta_cols = st.columns(3)
                    if meta_cols[0].button("isEmpty", key="ll_isempty"):
                        _record_and_locate(
                            "ll_no_input",
                            structure_name,
                            "isEmpty",
                            lambda: structure.isEmpty(),  # type: ignore[union-attr]
                            complexity="O(1)",
                            structure=structure,
                        )
                    #--- clear operation 
                    if meta_cols[1].button("clear", key="ll_clear"):
                        _record_and_locate(
                            "ll_no_input",
                            structure_name,
                            "clear",
                            lambda: structure.clear() or None,  # type: ignore[union-attr]
                            complexity="O(n)",
                            structure=structure,
                        )
                    #--- length operation 
                    if meta_cols[2].button("len", key="ll_len"):
                        _record_and_locate(
                            "ll_no_input",
                            structure_name,
                            "__len__",
                            lambda: len(structure),  # type: ignore[arg-type]
                            complexity="O(1)",
                            structure=structure,
                        )
                    _maybe_render_section_result("ll_no_input", structure_name)
        #--- view operation 
        with view_col:
            structure = st.session_state["structure_objects"].get(structure_name)
            if structure is not None:
                state = _logical_state(structure_name, structure)
                raw = _raw_state(structure_name, structure)
                render_structure_state(structure_name, state, raw_state=raw)

# __________________________________________________________________________
# Tab 4 — Compare Structures
#

with tabs[3]:
    st.header("Compare Structures")
    render_comparison_grid()
    st.divider()
    st.subheader("Big-O Complexity Reference")
    render_complexity_table()
    st.divider()
    st.subheader("Behavioral Notes")
    st.markdown(
        """
- Common Build is a bulk insertion process that is used to measure how fast each structure can fill itself up from empty using its normal add operation (`Stack.push`, `Queue.enqueue`, `Deque.addRear`, `LinkedList.insert_rear`).
- Common Drain is bulk removal process that is used to measure how fast each structure can empty itself out using its normal remove operation (`Stack.pop`, `Queue.dequeue`, `Deque.removeFront`, `LinkedList.delete_head`).
- Peek / Front is an operation that reads the next element to be removed without removing it.
- Deque Ends is an operation that inserts or removes elements from both ends of the deque.
- LinkedList Delete / Search / Display is an operation that deletes, searches, or displays elements in the linked list.
        """
    )
    st.info(
        "See the **Recommendation Guide** tab for actionable structure-"
        "selection advice tied to actual benchmark winners."
    )

# __________________________________________________________________________
# Tab 5 — Benchmark Lab
#

with tabs[4]:
    st.header("Benchmark Lab")
    st.markdown(
        "Run the reproducible benchmark engine. Mutating workloads use a "
        "fresh structure per timed iteration; non-mutating workloads use "
        "`timeit.Timer.autorange` to amortize many calls."
    )
    config_col, action_col = st.columns([3, 2])
    #--- benchmark configuration 
    with config_col:
        size_choices = [100, 500, 1_000, 5_000, 10_000, 50_000]
        chosen_sizes = st.multiselect(
            "Sizes",
            options=size_choices,
            default=list(DEFAULT_SIZES),
        )
        preset_cols = st.columns(2)
        if preset_cols[0].button("Preview [100, 500]"):
            chosen_sizes = [100, 500]
        if preset_cols[1].button("Full required [1k, 5k, 10k, 50k]"):
            chosen_sizes = list(DEFAULT_SIZES)
        #--- repeats selection 
        repeats = st.number_input(
            "Repeats per workload",
            min_value=1,
            max_value=20,
            value=DEFAULT_REPEATS,
        )
        include_specific = st.checkbox(
            "Include structure-specific workloads", value=True
        )
    #--- benchmark action column 
    with action_col:
        if 50_000 in chosen_sizes and include_specific:
            st.warning(
                "Heads up: at n = 50,000 the `Queue.enqueue`, "
                "`Deque.addRear`, and `Deque.removeRear` workloads are "
                "intentionally `O(n²)` and will take noticeably longer."
            )
        run_clicked = st.button("Run Benchmark", type="primary")
        save_clicked = st.button("Save Results to CSV")
        load_clicked = st.button("Load saved CSV")
    #--- run benchmark operation 
    if run_clicked:
        if not chosen_sizes:
            st.error("Pick at least one size.")
        else:
            progress = st.progress(0.0, text="Starting…")

            def _cb(done: int, total: int, label: str) -> None:
                progress.progress(done / total, text=f"{label} ({done}/{total})")

            df = run_benchmarks(
                sizes=sorted(chosen_sizes),
                repeats=int(repeats),
                include_specific=include_specific,
                progress_callback=_cb,
            )
            progress.empty()
            st.session_state["benchmark_df"] = df
            st.session_state["operation_winners_df"] = compute_operation_winners(df)
            st.success(f"Benchmark complete: {len(df)} rows.")
    #--- save benchmark operation   
    if save_clicked:
        if st.session_state.get("benchmark_df") is None:
            st.error("No benchmark in memory. Run the benchmark first.")
        else:
            save_results_csv(st.session_state["benchmark_df"], _BENCHMARK_CSV)
            save_operation_winners_csv(
                st.session_state["operation_winners_df"], _WINNERS_CSV
            )
            st.success(
                f"Saved `{_BENCHMARK_CSV.name}` and `{_WINNERS_CSV.name}` "
                f"under `analysis/`."
            )
    #--- load benchmark operation 
    if load_clicked:
        if not _BENCHMARK_CSV.exists():
            st.error(f"No saved file at {_BENCHMARK_CSV}.")
        else:
            df = load_results_csv(_BENCHMARK_CSV)
            st.session_state["benchmark_df"] = df
            if _WINNERS_CSV.exists():
                st.session_state["operation_winners_df"] = pd.read_csv(_WINNERS_CSV)
            else:
                st.session_state["operation_winners_df"] = compute_operation_winners(df)
            st.success(f"Loaded {len(df)} rows from `{_BENCHMARK_CSV.name}`.")
    #--- benchmark results display 
    df = st.session_state.get("benchmark_df")
    if df is not None and not df.empty:
        st.divider()
        st.markdown(
            "**Operation groups (facet titles):**\n"
            "- **Common Build** — bulk insertion at the *natural growth end* of "
            "each structure (`Stack.push`, `Queue.enqueue`, `Deque.addRear`, "
            "`LinkedList.insert_rear`). Used to compare how fast each structure "
            "can *fill it up* from empty using its normal add operation.\n"
            "- **Common Drain** — bulk removal from the *natural consumption end* "
            "of each structure (`Stack.pop`, `Queue.dequeue`, `Deque.removeFront`, "
            "`LinkedList.delete_front`). Used to compare how fast each structure "
            "can *empty it out* using its normal remove operation.\n"
            "- **Peek / Front** — read-only inspection of the next element to be "
            "removed; tests cache and pointer overhead, not allocation.\n"
            "- **Deque Ends** — both-end inserts and removes that only the Deque "
            "supports natively (`addFront`, `addRear`, `removeFront`, "
            "`removeRear`).\n"
            "- **LinkedList Delete / Search / Display** — LinkedList-only "
            "scenarios that exercise positional deletion, linear search, and "
            "full-traversal output respectively."
        )
        st.subheader("Results")
        render_benchmark_table(df)
        st.divider()
        render_benchmark_charts(
            df, winners_df=st.session_state.get("operation_winners_df")
        )

# __________________________________________________________________________
# Tab 6 — Written Analysis
#

with tabs[5]:
    st.header("Written Analysis")
    df = st.session_state.get("benchmark_df")
    winners_df = st.session_state.get("operation_winners_df")
    # SAFETY CHECK: fall back to saved CSVs when nothing is in memory
    if (df is None or df.empty) and _BENCHMARK_CSV.exists():
        df = load_results_csv(_BENCHMARK_CSV)
    if (winners_df is None) and _WINNERS_CSV.exists():
        winners_df = pd.read_csv(_WINNERS_CSV)
    render_analysis_markdown_file(
        _WRITTEN_ANALYSIS,
        benchmark_df=df,
        winners_df=winners_df,
    )

# __________________________________________________________________________
# Tab 7 — Recommendation Guide
#

with tabs[6]:
    st.header("Recommendation Guide")
    winners_df = st.session_state.get("operation_winners_df")
    if winners_df is None and _WINNERS_CSV.exists():
        winners_df = pd.read_csv(_WINNERS_CSV)
    render_analysis_markdown_file(
        _RECOMMENDATION,
        benchmark_df=None,
        winners_df=winners_df,
    )

# __________________________________________________________________________
# End of File
#
