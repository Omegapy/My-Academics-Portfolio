# File: overview_page.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Render the Bubble Quickselect Sets page inside the root portfolio app.
# - Provide labs for CourseSet operations, Bubble Sort, Quickselect, benchmarks,
#   and written analysis.
# - Coordinate Streamlit session state for repeatable interactive workflows.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# CONFIGURATION:
#   - Paths, dataset source lists, set operation lists, and session defaults
#
# INPUT HELPERS:
#   - Functions: state initialization, parsing, dataset selection, formatting
#
# RENDER HELPERS:
#   - Functions: metrics, traces, Markdown, set results, algorithm results
#
# PAGE ORCHESTRATION:
#   - Function: render_bubble_quickselect_sets_page()
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: collections.abc, pathlib, sys, time
# - Third-Party: altair, pandas, streamlit
# - Local Project Modules: algorithms, analysis, data, models, set operations
# --- Requirements ---
# - Python 3.12+
# - altair, pandas, streamlit
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by Portfolio-Module-8/streamlit_app.py as one root app tab renderer.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Root-rendered Streamlit page for Module 8 Bubble Sort and Quickselect labs."""

from __future__ import annotations

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from collections.abc import Hashable
from pathlib import Path
import sys
import time

import altair as alt
import pandas as pd
import streamlit as st


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# PATHS
# ========================================================================
# Contains module-local artifact paths and UI configuration constants for the
# Bubble Quickselect Sets page.
#
# PATH AND CONFIGURATION OVERVIEW:
# This section resolves analysis artifacts, imports local packages after path
# setup, and declares Streamlit option lists used by controls.
#
# Constraint: all artifacts resolve from the module directory, not the shell CWD.
# Rationale: Streamlit apps are commonly launched from different directories.

_MODULE_DIR = Path(__file__).resolve().parent
_PORTFOLIO_ROOT = _MODULE_DIR.parent
_ANALYSIS_DIR = _MODULE_DIR / "analysis"
_CSV_PATH = _ANALYSIS_DIR / "benchmark_results.csv"
_WRITTEN_ANALYSIS_PATH = _ANALYSIS_DIR / "written_analysis.md"

# SETUP: add Portfolio-Module-8 root so local packages import correctly.
if str(_PORTFOLIO_ROOT) not in sys.path:
    sys.path.insert(0, str(_PORTFOLIO_ROOT))

# __________________________________________________________________________
# Function Definitions
# __________________________________________________________________________
# IMPORT ALGORITHMS FROM ALGORITHMS.PY
# __________________________________________________________________________
from bubble_quickselect_module.algorithms import bubble_sort, quickselect

# __________________________________________________________________________
# IMPORT ANALYSIS MODULES FROM ANALYSIS.PY
# __________________________________________________________________________
from bubble_quickselect_module.analysis import (
    DEFAULT_BENCHMARK_DATASET_TYPES,
    DEFAULT_FULL_SIZES,
    DEFAULT_QUICK_SIZES,
    load_results_csv,
    run_benchmarks,
    save_results_csv,
)

# __________________________________________________________________________
# IMPORT DATASET MODULES FROM DATASET_MANAGER.PY
# __________________________________________________________________________
from bubble_quickselect_module.data import (
    DEFAULT_RANDOM_SEED,
    generate_dataset_by_type,
    parse_manual_input,
    preview_dataset,
)

# __________________________________________________________________________
# IMPORT MODELS FROM MODELS.PY
# __________________________________________________________________________
from bubble_quickselect_module.models import QuickSelectResult, SortResult

# __________________________________________________________________________
# IMPORT SET OPERATIONS FROM SET_OPERATIONS.PY
# __________________________________________________________________________
from bubble_quickselect_module.set_operations import CourseSet, SetOperationResult

_TRACE_THRESHOLD: int = 25

# Whitelist of integer dataset sources available to the page controls.
# Any source not listed here is rejected by dataset dispatch helpers.
_DATASET_SOURCES: list[str] = [
    "random",  # generated pseudo-random integer dataset
    "sorted",  # generated non-decreasing integer dataset
    "reverse_sorted",  # generated descending integer dataset
    "partially_sorted",  # generated mostly ordered integer dataset
    "manual",  # user-entered comma-separated integer dataset
]
_SET_A_DEFAULT = "1, 2, 3, 3, 5, 8"
_SET_B_DEFAULT = "3, 4, 5, 9"

# Whitelist of CourseSet operations available in the manual playground.
# Any operation not listed here is rejected before operation recording.
_SET_OPERATION_NAMES: list[str] = [
    "add",  # dynamic mutation operation
    "remove",  # dynamic mutation operation
    "contains",  # dynamic membership check
    "union",  # static two-set operation
    "intersection",  # static two-set operation
    "difference",  # static two-set operation
    "symmetric_difference",  # static two-set operation
]
_SET_DYNAMIC_OPERATIONS: set[str] = {"add", "remove", "contains"}

# Complexity labels shown by the set-operation result panel.
# Constraint: keys must match ``_SET_OPERATION_NAMES`` for result lookup.
_SET_COMPLEXITIES: dict[str, str] = {
    # Dynamic single-set operations
    "add": "O(1) average",  # hash-backed insert
    "remove": "O(1) average",  # hash-backed delete
    "contains": "O(1) average",  # hash-backed membership

    # Static two-set operations
    "union": "O(n + m)",  # scan both operands
    "intersection": "O(n + m)",  # scan operands for shared values
    "difference": "O(n + m)",  # scan operands for target-only values
    "symmetric_difference": "O(n + m)",  # scan operands for unique-side values
}


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# SESSION STATE DEFAULTS
# ========================================================================
# Contains namespaced session-state defaults for this page's interactive labs.
#
# SESSION STATE OVERVIEW:
# Defaults preserve the last set operation, algorithm result, benchmark table,
# and generated demo history across Streamlit reruns.
#
# Constraint: keys are namespaced to avoid collisions with other root app tabs.
# Rationale: Streamlit stores all tab state in one shared session dictionary.

_DEFAULTS: dict[str, object] = {
    # Persistent set lab state
    "bubble_quickselect_set_a_values": [1, 2, 3, 5, 8],
    "bubble_quickselect_set_b_values": [3, 4, 5, 9],
    "bubble_quickselect_last_set_operation_result": None,
    "bubble_quickselect_set_operation_history": [],
    "bubble_quickselect_set_auto_demo_results": [],

    # Algorithm lab state
    "bubble_quickselect_bubble_result": None,
    "bubble_quickselect_bubble_dataset": [],
    "bubble_quickselect_quickselect_result": None,
    "bubble_quickselect_quickselect_dataset": [],

    # Benchmark lab state
    "bubble_quickselect_benchmark_df": None,
}


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# PARSING AND DATASET HELPERS
# ========================================================================
# Contains non-rendering helpers used by controls before operations execute.
#
# INPUT HELPER OVERVIEW:
# These functions initialize state, parse set inputs, select datasets, format
# timing, and read/write Set A or Set B values.
# =========================================================================
# - Function: _initialize_session_state()
# - Function: _parse_hashable_values()
# - Function: _parse_single_value()
# - Function: _dataset_from_controls()
# - Function: _format_ms()
# - Function: _set_values_for_label()
# - Function: _store_set_values_for_label()
# - Function: _format_set_value()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- _initialize_session_state()
def _initialize_session_state() -> None:
    """Initialize namespaced Streamlit session state for this page.

    Returns:
        None.
    """
    # MAIN ITERATION LOOP: seed only missing keys to preserve user interactions.
    for key, value in _DEFAULTS.items():
        # VALIDATION: do not overwrite values already set by Streamlit widgets.
        if key not in st.session_state:
            st.session_state[key] = value
# --------------------------------------------------------------- end _initialize_session_state()

# --------------------------------------------------------------- _parse_hashable_values()
def _parse_hashable_values(raw: str) -> list[Hashable]:
    """Parse comma-separated values for set demonstrations.

    Args:
        raw: Comma-separated text values.

    Returns:
        Parsed values with integer tokens converted to ``int``.

    Raises:
        ValueError: If the input is blank or contains a blank token.
    """
    # VALIDATION: a set demonstration needs at least one user-provided token.
    if not raw or not raw.strip():
        raise ValueError("Set input cannot be blank.")

    parsed_values: list[Hashable] = []
    # MAIN ITERATION LOOP: preserve token order while normalizing integer text.
    for token in raw.split(","):
        cleaned = token.strip()
        # VALIDATION: blank tokens usually indicate duplicate/trailing commas.
        if not cleaned:
            raise ValueError("Set input contains a blank value.")
        try:
            # Step 1: prefer integers when tokens parse cleanly.
            parsed_values.append(int(cleaned))
        except ValueError:
            # Step 2: keep non-integer tokens as hashable strings.
            parsed_values.append(cleaned)
    return parsed_values
# --------------------------------------------------------------- end _parse_hashable_values()


# --------------------------------------------------------------- _parse_single_value()
def _parse_single_value(raw: str) -> Hashable:
    """Parse one text value for membership, add, and remove demos.

    Args:
        raw: User-entered value.

    Returns:
        Parsed hashable value.

    Raises:
        ValueError: If the input is blank.
    """
    values = _parse_hashable_values(raw)
    # VALIDATION: dynamic operations accept exactly one membership/update value.
    if len(values) != 1:
        raise ValueError("Enter exactly one demonstration value.")
    return values[0]
# --------------------------------------------------------------- end _parse_single_value()


# --------------------------------------------------------------- _dataset_from_controls()
def _dataset_from_controls(
    source: str,
    size: int,
    seed: int,
    manual_text: str,
) -> list[int]:
    """Return a dataset from Streamlit controls.

    Args:
        source: Dataset source key.
        size: Generated dataset size.
        seed: Random seed.
        manual_text: Comma-separated manual dataset.

    Returns:
        Integer dataset.

    Raises:
        ValueError: If source or manual input is invalid.
    """
    # DISPATCH: manual datasets come from text parsing instead of generation.
    if source == "manual":
        return parse_manual_input(manual_text)
    return generate_dataset_by_type(source, size=size, seed=seed)
# --------------------------------------------------------------- end _dataset_from_controls()


# --------------------------------------------------------------- _format_ms()
def _format_ms(seconds: float) -> str:
    """Format elapsed seconds as milliseconds.

    Args:
        seconds: Elapsed seconds.

    Returns:
        Display-ready millisecond string.
    """
    return f"{seconds * 1_000.0:.4f} ms"
# --------------------------------------------------------------- end _format_ms()


# --------------------------------------------------------------- _set_values_for_label()
def _set_values_for_label(
    label: str,
    source_values: dict[str, list[Hashable]] | None = None,
) -> list[Hashable]:
    """Return stored values for a set label.

    Args:
        label: ``"Set A"`` or ``"Set B"``.
        source_values: Optional override values used by read-only demos.

    Returns:
        Stored values for the selected set.
    """
    # DISPATCH: read-only automatic demos use supplied copies instead of session state.
    if source_values is not None:
        return list(source_values[label])
    # DISPATCH: persistent manual operations read the selected Streamlit key.
    if label == "Set A":
        return list(st.session_state["bubble_quickselect_set_a_values"])
    return list(st.session_state["bubble_quickselect_set_b_values"])
# --------------------------------------------------------------- end _set_values_for_label()


# --------------------------------------------------------------- _store_set_values_for_label()
def _store_set_values_for_label(label: str, values: list[Hashable]) -> None:
    """Store values for a persistent manual set.

    Args:
        label: ``"Set A"`` or ``"Set B"``.
        values: Values to store.

    Returns:
        None.
    """
    # DISPATCH: write the mutated set back to the correct namespaced state key.
    if label == "Set A":
        st.session_state["bubble_quickselect_set_a_values"] = values
    else:
        st.session_state["bubble_quickselect_set_b_values"] = values
# --------------------------------------------------------------- end _store_set_values_for_label()


# --------------------------------------------------------------- _format_set_value()
def _format_set_value(value: object) -> str:
    """Format a set operation value for display.

    Args:
        value: Value returned by an operation.

    Returns:
        Display string.
    """
    # DISPATCH: booleans are displayed without Python's lowercase variants.
    if isinstance(value, bool):
        return "True" if value else "False"
    # DISPATCH: None is a visible return value for operations without operands.
    if value is None:
        return "None"
    return str(value)
# --------------------------------------------------------------- end _format_set_value()


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# RENDER HELPERS
# ========================================================================
# Contains reusable Streamlit output helpers for metrics, traces, Markdown,
# dataset controls, set results, algorithm results, and benchmark charts.
#
# UI DISPLAY OVERVIEW:
# Render helpers keep the page renderer readable by isolating repeated visual
# patterns from the tab orchestration code.
# =========================================================================
# - Function: _render_header()
# - Function: _render_metric_row()
# - Function: _render_trace()
# - Function: _render_markdown_file()
# - Function: _render_dataset_controls()
# - Function: _render_set_state_summary()
# - Function: _record_set_operation()
# - Function: _render_set_operation_result()
# - Function: _render_set_operation_history()
# - Function: _run_set_auto_demo()
# - Function: _render_sort_result()
# - Function: _render_quickselect_result()
# - Function: _render_benchmark_chart()
# -------------------------------------------------------------------------

# --------------------------------------------------------------- _render_header()
def _render_header() -> None:
    """Render the app title.

    Returns:
        None.
    """
    st.title("Bubble Quickselect Sets")
    st.divider()
# --------------------------------------------------------------- end _render_header()


# --------------------------------------------------------------- _render_metric_row()
def _render_metric_row(items: list[tuple[str, str]]) -> None:
    """Render a compact metric row.

    Args:
        items: Label/value pairs.

    Returns:
        None.
    """
    columns = st.columns(len(items))
    # MAIN ITERATION LOOP: each metric occupies one Streamlit column.
    for column, (label, value) in zip(columns, items):
        column.metric(label, value)
# --------------------------------------------------------------- end _render_metric_row()


# --------------------------------------------------------------- _render_trace()
def _render_trace(title: str, trace: list[str], input_size: int) -> None:
    """Render algorithm trace lines.

    Args:
        title: Expander title.
        trace: Trace lines.
        input_size: Algorithm input size.

    Returns:
        None.
    """
    # VALIDATION: large traces are skipped by the algorithm to protect responsiveness.
    if input_size > _TRACE_THRESHOLD:
        st.info("Trace collection is disabled for larger datasets to keep the app responsive.")
        return
    # VALIDATION: small already-sorted or trivial inputs may have no trace lines.
    if not trace:
        st.info("No trace entries were needed for this input.")
        return
    with st.expander(title, expanded=False):
        # MAIN ITERATION LOOP: render each saved algorithm narration line.
        for line in trace:
            st.write(line)
# --------------------------------------------------------------- end _render_trace()


# --------------------------------------------------------------- _render_markdown_file()
def _render_markdown_file(path: Path) -> None:
    """Render a Markdown file or warning.

    Args:
        path: Markdown path to render.

    Returns:
        None.
    """
    # VALIDATION: missing analysis files should explain the missing artifact.
    if not path.exists():
        st.warning(f"Missing Markdown file: {path.name}")
        return
    st.markdown(path.read_text(encoding="utf-8"))
# --------------------------------------------------------------- end _render_markdown_file()


# --------------------------------------------------------------- _render_dataset_controls()
def _render_dataset_controls(prefix: str) -> tuple[str, int, int, str]:
    """Render common integer dataset controls.

    Args:
        prefix: Unique key prefix for Streamlit widgets.

    Returns:
        Tuple of source, size, seed, and manual text.
    """
    # Split the layout into two columns: control panel on left, manual entry on right
    control_col, manual_col = st.columns([2, 3])
    with control_col:
        source = st.selectbox(
            "Dataset Source",
            _DATASET_SOURCES,
            key=f"{prefix}_dataset_source",
        )
        size = st.slider(
            "Dataset Size",
            min_value=0,
            max_value=1_000,
            value=10,
            step=1,
            key=f"{prefix}_dataset_size",
        )
        seed = st.number_input(
            "Random Seed",
            min_value=0,
            value=DEFAULT_RANDOM_SEED,
            step=1,
            key=f"{prefix}_seed",
        )
    # Manual entry on right
    with manual_col:
        manual_text = st.text_area(
            "Manual Dataset",
            value="9, 1, 5, 3, 7, 3",
            key=f"{prefix}_manual_dataset",
            height=130,
        )
        st.caption("Manual source accepts comma-separated integers.")
    return source, int(size), int(seed), manual_text
# --------------------------------------------------------------- end _render_dataset_controls()


# --------------------------------------------------------------- _render_set_state_summary()
def _render_set_state_summary() -> None:
    """Render the current Set A and Set B states.

    Returns:
        None.
    """
    # Pull current set values from session state
    set_a_values = list(st.session_state["bubble_quickselect_set_a_values"])
    set_b_values = list(st.session_state["bubble_quickselect_set_b_values"])

    # Create CourseSet instances
    set_a = CourseSet(set_a_values)
    set_b = CourseSet(set_b_values)

    # Display current set state
    st.subheader("Current Set State")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Set": "A",
                    "Stored state": str(set_a_values),
                    "Unique values": str(set_a.to_list()),
                    "Duplicates removed": len(set_a_values) - len(set_a),
                },
                {
                    "Set": "B",
                    "Stored state": str(set_b_values),
                    "Unique values": str(set_b.to_list()),
                    "Duplicates removed": len(set_b_values) - len(set_b),
                },
            ]
        ),
        width="stretch",
        hide_index=True,
    )
# --------------------------------------------------------------- end _render_set_state_summary()


# --------------------------------------------------------------- _record_set_operation()
def _record_set_operation(
    operation: str,
    target_set: str,
    *,
    operand_set: str | None = None,
    input_value: Hashable | None = None,
    mutate_session: bool = True,
    source_values: dict[str, list[Hashable]] | None = None,
    notes_prefix: str = "",
) -> SetOperationResult:
    """Execute and record one set operation.

    Args:
        operation: Operation name to execute.
        target_set: Primary set label.
        operand_set: Optional secondary set label.
        input_value: Optional value for dynamic operations.
        mutate_session: Whether dynamic mutations update persistent Set A/B.
        source_values: Optional values used for read-only demos.
        notes_prefix: Optional note prefix for demo results.

    Returns:
        SetOperationResult containing before/after state and metadata.

    Raises:
        ValueError: If required operation inputs are missing.
    """
    target = CourseSet(_set_values_for_label(target_set, source_values))
    operand = (
        CourseSet(_set_values_for_label(operand_set, source_values))
        if operand_set is not None
        else None
    )
    state_before = target.to_list()
    operand_before = operand.to_list() if operand is not None else None
    size_before = len(state_before)
    returned_value: object
    result_values: list[Hashable] | None = None

    start_time = time.perf_counter()
    # DISPATCH: dynamic operations mutate/check one target set value.
    if operation == "add":
        # VALIDATION: add requires a concrete value before calling CourseSet.add().
        if input_value is None:
            raise ValueError("Add requires one operation value.")
        returned_value = target.add(input_value)
    elif operation == "remove":
        # VALIDATION: remove requires a concrete value before calling CourseSet.remove().
        if input_value is None:
            raise ValueError("Remove requires one operation value.")
        returned_value = target.remove(input_value)
    elif operation == "contains":
        # VALIDATION: contains requires a concrete value before membership lookup.
        if input_value is None:
            raise ValueError("Contains requires one operation value.")
        returned_value = target.contains(input_value)
    # DISPATCH: static operations return derived sets and leave operands unchanged.
    elif operation == "union":
        # VALIDATION: union needs both operands.
        if operand is None:
            raise ValueError("Union requires a second set operand.")
        result_values = target.union(operand).to_list()
        returned_value = result_values
    elif operation == "intersection":
        # VALIDATION: intersection needs both operands.
        if operand is None:
            raise ValueError("Intersection requires a second set operand.")
        result_values = target.intersection(operand).to_list()
        returned_value = result_values
    elif operation == "difference":
        # VALIDATION: difference needs both operands and respects operand order.
        if operand is None:
            raise ValueError("Difference requires a second set operand.")
        result_values = target.difference(operand).to_list()
        returned_value = result_values
    elif operation == "symmetric_difference":
        # VALIDATION: symmetric difference needs both operands.
        if operand is None:
            raise ValueError("Symmetric difference requires a second set operand.")
        result_values = target.symmetric_difference(operand).to_list()
        returned_value = result_values
    else:
        # VALIDATION: operation names must come from the configured UI choices.
        raise ValueError(f"Unsupported set operation: {operation!r}.")
    elapsed_time = time.perf_counter() - start_time

    state_after = target.to_list()
    operand_after = operand.to_list() if operand is not None else None
    # MUTATION: only successful add/remove operations update the persistent sets.
    if mutate_session and operation in {"add", "remove"}:
        _store_set_values_for_label(target_set, state_after)

    operands_unchanged = (
        operand_before == operand_after and state_before == state_after
        if operand is not None
        else operation == "contains" or state_before == state_after
    )
    # DISPATCH: compose an operation note that matches dynamic vs. static behavior.
    if operation in {"union", "intersection", "difference", "symmetric_difference"}:
        notes = "Static operation returned a derived set; operands unchanged: "
        notes += "Yes" if operands_unchanged else "No"
    elif operation == "contains":
        notes = "Membership check does not mutate the target set."
    elif operation == "add":
        notes = "Dynamic add mutates the target set when the value is new."
    else:
        notes = "Dynamic remove mutates the target set when the value is present."
    # Step 1: automatic demos prepend a reminder that source sets are copied.
    if notes_prefix:
        notes = f"{notes_prefix} {notes}"

    # Step 2: package before/after state and complexity metadata for rendering.
    return SetOperationResult(
        operation=operation,
        target_set=target_set,
        operand_set=operand_set,
        input_value=input_value,
        returned_value=returned_value,
        result_values=result_values,
        size_before=size_before,
        size_after=len(state_after),
        elapsed_time=elapsed_time,
        complexity=_SET_COMPLEXITIES[operation],
        state_before=state_before,
        state_after=state_after,
        notes=notes,
        operand_before=operand_before,
        operand_after=operand_after,
    )
# --------------------------------------------------------------- end _record_set_operation()


# --------------------------------------------------------------- _render_set_operation_result()
def _render_set_operation_result(result: SetOperationResult) -> None:
    """Render one set operation result with before/after states.

    Args:
        result: Set operation result to render.

    Returns:
        None.
    """
    operation_title = f"{result.target_set}.{result.operation}"
    # DISPATCH: static operations read better when the operand set is named.
    if result.operand_set is not None:
        operation_title = f"{result.target_set} {result.operation} {result.operand_set}"
    st.markdown(f"### {operation_title}")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Returned", _format_set_value(result.returned_value))
    metric_cols[1].metric("Size", f"{result.size_before:,} -> {result.size_after:,}")
    metric_cols[2].metric("Time", _format_ms(result.elapsed_time))
    metric_cols[3].metric("Big-O", result.complexity)

    details: list[str] = []
    # Step 1: collect optional details only when the operation used them.
    if result.input_value is not None:
        details.append(f"value = `{result.input_value}`")
    if result.operand_set is not None:
        details.append(f"operand = `{result.operand_set}`")
    # VALIDATION: avoid rendering an empty caption row.
    if details:
        st.caption(" | ".join(details))

    # Split the layout into two columns: target state before on left, target state after on right
    state_cols = st.columns(2)
    with state_cols[0]:
        st.markdown("**Target state before:**")
        st.code(str(result.state_before))
    with state_cols[1]:
        st.markdown("**Target state after:**")
        st.code(str(result.state_after))

    # DISPATCH: operand state is meaningful only for two-set operations.
    if result.operand_before is not None and result.operand_after is not None:
        operand_cols = st.columns(2)
        with operand_cols[0]:
            st.markdown("**Operand state before:**")
            st.code(str(result.operand_before))
        with operand_cols[1]:
            st.markdown("**Operand state after:**")
            st.code(str(result.operand_after))

    # DISPATCH: derived results are only created by static set operations.
    if result.result_values is not None:
        st.markdown("**Derived result:**")
        st.code(str(result.result_values))
    st.info(result.notes)
# --------------------------------------------------------------- end _render_set_operation_result()


# --------------------------------------------------------------- _render_set_operation_history()
def _render_set_operation_history(results: list[SetOperationResult]) -> None:
    """Render compact manual set operation history.

    Args:
        results: Historical set operation results.

    Returns:
        None.
    """
    # VALIDATION: no history exists until the user runs at least one operation.
    if not results:
        st.info("Run a manual set operation to build operation history.")
        return
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Operation": result.operation,
                    "Target": result.target_set,
                    "Operand": result.operand_set or "-",
                    "Input": _format_set_value(result.input_value),
                    "Returned": _format_set_value(result.returned_value),
                    "Size before": result.size_before,
                    "Size after": result.size_after,
                    "Big-O": result.complexity,
                }
                for result in results
            ]
        ),
        width="stretch",
        hide_index=True,
    )
# --------------------------------------------------------- end _render_set_operation_history()


# --------------------------------------------------------------- _run_set_auto_demo()
def _run_set_auto_demo(input_value: Hashable) -> list[SetOperationResult]:
    """Run every required set operation on read-only copies.

    Args:
        input_value: Value used for contains, add, and remove demos.

    Returns:
        Ordered set operation demo results.
    """
    source_values = {
        "Set A": list(st.session_state["bubble_quickselect_set_a_values"]),
        "Set B": list(st.session_state["bubble_quickselect_set_b_values"]),
    }
    demo_note = "Automatic demo uses copies and leaves manual Set A/B unchanged."
    # MAIN ITERATION LOOP: return every required operation in a fixed teaching order.
    return [
        _record_set_operation(
            "contains",
            "Set A",
            input_value=input_value,
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
        _record_set_operation(
            "add",
            "Set A",
            input_value=input_value,
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
        _record_set_operation(
            "remove",
            "Set A",
            input_value=input_value,
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
        _record_set_operation(
            "union",
            "Set A",
            operand_set="Set B",
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
        _record_set_operation(
            "intersection",
            "Set A",
            operand_set="Set B",
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
        _record_set_operation(
            "difference",
            "Set A",
            operand_set="Set B",
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
        _record_set_operation(
            "difference",
            "Set B",
            operand_set="Set A",
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
        _record_set_operation(
            "symmetric_difference",
            "Set A",
            operand_set="Set B",
            mutate_session=False,
            source_values=source_values,
            notes_prefix=demo_note,
        ),
    ]
# --------------------------------------------------------------- end _run_set_auto_demo()


# --------------------------------------------------------------- _render_sort_result()
def _render_sort_result(result: SortResult | None) -> None:
    """Render Bubble Sort result details.

    Args:
        result: SortResult to render.

    Returns:
        None.
    """
    # VALIDATION: the result panel remains empty until the user runs Bubble Sort.
    if result is None:
        st.info("Run Bubble Sort to generate results.")
        return

    # Render metric row
    _render_metric_row(
        [
            ("Input Size", f"{result.input_size:,}"),
            ("Comparisons", f"{result.comparisons:,}"),
            ("Swaps", f"{result.swaps:,}"),
            ("Writes", f"{result.writes:,}"),
            ("Elapsed", _format_ms(result.elapsed_time)),
        ]
    )

    # Render property dataframe
    property_df = pd.DataFrame(
        [
            {"Property": "Stable", "Value": "Yes" if result.is_stable else "No"},
            {"Property": "Conceptually in-place", "Value": "Yes" if result.is_in_place else "No"},
            {"Property": "Extra space", "Value": result.extra_space},
            {"Property": "Early exit used", "Value": "Yes" if result.early_exit_used else "No"},
        ]
    )

    # Render property dataframe
    st.dataframe(property_df, width="stretch", hide_index=True)

    # Render result columns (original dataset and sorted dataset)
    result_col_a, result_col_b = st.columns(2)
    with result_col_a:
        st.subheader("Original Dataset")
        st.code(preview_dataset(result.original_data, count=30))
    with result_col_b:
        st.subheader("Sorted Dataset")
        st.code(preview_dataset(result.sorted_data, count=30))
    _render_trace("Bubble Sort Step Trace", result.step_trace, result.input_size)
# --------------------------------------------------------------- end _render_sort_result()


# --------------------------------------------------------------- _render_quickselect_result()
def _render_quickselect_result(result: QuickSelectResult | None) -> None:
    """Render Quickselect result details.

    Args:
        result: QuickSelectResult to render.

    Returns:
        None.
    """
    # VALIDATION: the result panel remains empty until the user runs Quickselect.
    if result is None:
        st.info("Run Quickselect to generate results.")
        return

    # Calculate expected value
    expected = sorted(result.original_data)[result.k - 1]

    # Render metric row
    _render_metric_row(
        [
            ("Input Size", f"{result.input_size:,}"),
            ("k", f"{result.k:,}"),
            ("Zero-Based Rank", f"{result.zero_based_rank:,}"),
            ("Selected Value", str(result.selected_value)),
            ("Correct", "Yes" if result.is_correct else "No"),
        ]
    )

    # Render count dataframe
    count_df = pd.DataFrame(
        [
            {"Metric": "Expected value from sorted(data)[k - 1]", "Value": str(expected)},
            {"Metric": "Comparisons", "Value": f"{result.comparisons:,}"},
            {"Metric": "Swaps", "Value": f"{result.swaps:,}"},
            {"Metric": "Writes", "Value": f"{result.writes:,}"},
            {"Metric": "Elapsed time", "Value": _format_ms(result.elapsed_time)},
        ]
    )

    # Render count dataframe
    st.dataframe(count_df, width="stretch", hide_index=True)
    result_col_a, result_col_b = st.columns(2)
    with result_col_a:
        st.subheader("Original Dataset")
        st.code(preview_dataset(result.original_data, count=30))
    with result_col_b:
        st.subheader("Partitioned Dataset")
        st.code(preview_dataset(result.partitioned_data, count=30))
    _render_trace("Quickselect Partition Trace", result.step_trace, result.input_size)
# --------------------------------------------------------------- end _render_quickselect_result()


# --------------------------------------------------------------- _render_benchmark_chart()
def _render_benchmark_chart(df: pd.DataFrame | None) -> None:
    """Render average runtime chart by operation and size.

    Args:
        df: Benchmark results DataFrame.

    Returns:
        None.
    """
    # VALIDATION: benchmark charts require at least one completed result row.
    if df is None or df.empty:
        st.info("Run the benchmark to generate a runtime chart.")
        return
    average_df = df.groupby(["size", "operation"], as_index=False)["elapsed_time_ms"].mean()
    chart_df = average_df.pivot(index="size", columns="operation", values="elapsed_time_ms")
    st.subheader("Average Runtime by Operation and Size")
    st.line_chart(chart_df)

    log_chart_df = average_df[average_df["elapsed_time_ms"] > 0.0].copy()
    # SAFETY CHECK: log-scale charts cannot display zero or negative runtimes.
    if log_chart_df.empty:
        return
    st.subheader("Log-Scale Runtime Detail")
    st.caption(
        "This view separates very fast operations such as Python sorted full sort "
        "from the near-zero baseline on the linear chart."
    )
    # Create log-scale chart
    log_chart = (
        alt.Chart(log_chart_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("size:Q", title="Input size"),
            y=alt.Y(
                "elapsed_time_ms:Q",
                scale=alt.Scale(type="log"),
                title="Average elapsed time (ms, log scale)",
            ),
            color=alt.Color("operation:N", title="Operation"),
            tooltip=[
                alt.Tooltip("size:Q", title="Size"),
                alt.Tooltip("operation:N", title="Operation"),
                alt.Tooltip("elapsed_time_ms:Q", title="Average ms", format=".6f"),
            ],
        )
        .properties(height=360)
    )
    st.altair_chart(log_chart, width="stretch")
# --------------------------------------------------------------- end _render_benchmark_chart()


# __________________________________________________________________________
# Page Renderer
# ========================================================================
# APPLICATION ORCHESTRATION:
# The page renderer creates the Module 8-native tabs, wires controls to the
# algorithm/set helpers, and renders saved analysis artifacts.
#
# TAB FLOW:
#   1. Overview explains the feature area and Big-O comparison.
#   2. Build Set Lab demonstrates dynamic and static CourseSet operations.
#   3. Bubble Sort and Quickselect labs run algorithms on selected datasets.
#   4. Benchmark Lab records comparison evidence and CSV output.
#   5. Written Analysis displays the module analysis Markdown.
# =========================================================================
# - Function: render_bubble_quickselect_sets_page()
# -------------------------------------------------------------------------

# --------------------------------------------------------- render_bubble_quickselect_sets_page()
def render_bubble_quickselect_sets_page() -> None:
    """Render the Bubble Quickselect Sets page inside the root portfolio app.

    Returns:
        None.
    """
    # Step 1: initialize page-scoped state before widgets read or write values.
    _initialize_session_state()
    _render_header()

    # Step 2: create the feature tabs for the native Module 8 workflow.
    (
        tab_overview,
        tab_set,
        tab_bubble,
        tab_quickselect,
        tab_benchmark,
        tab_analysis,
    ) = st.tabs(
        [
            "Overview",
            "Build Set Lab",
            "Bubble Sort Lab",
            "Quickselect Lab",
            "Benchmark Lab",
            "Written Analysis",
        ]
    )

    # Step 3: introduce the feature area before users run individual labs.
    with tab_overview:
        st.header("Overview")
        st.markdown(
            """
This page demonstrates the Module 8-native requirements inside the single
Portfolio Module 8 Streamlit app: a Set ADT, Bubble Sort visualization,
Quickselect kth-smallest selection, benchmark comparison, and written analysis.

The tabs cover concept overview, static and dynamic set behavior, adjacent
comparison sorting, partition-based selection, repeatable benchmarks, and the
Markdown analysis source used for final portfolio discussion.
            """
        )

        # Feature tabs table
        st.subheader("Feature Tabs")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Tab": "Overview", "Purpose": "Summarize Set, Bubble Sort, and Quickselect complexity."},
                    {"Tab": "Build Set Lab", "Purpose": "Build sets and compare static operations with dynamic mutation."},
                    {"Tab": "Bubble Sort Lab", "Purpose": "Run Bubble Sort and inspect adjacent comparison traces."},
                    {"Tab": "Quickselect Lab", "Purpose": "Find kth-smallest values and inspect partition traces."},
                    {"Tab": "Benchmark Lab", "Purpose": "Compare Bubble Sort, Python sorted, Quickselect, and full-sort selection."},
                    {"Tab": "Written Analysis", "Purpose": "Read the Markdown explanation and practical recommendations."},
                ]
            ),
            width="stretch",
            hide_index=True,
        )
        st.subheader("Concept Overview")
        st.markdown(
            """
**Sets** store unique hashable values. Membership is the central operation, and
static operations create derived sets without changing either original operand.

**Bubble Sort** repeatedly compares adjacent values and swaps out-of-order
pairs. Its early-exit optimization makes already sorted inputs finish after one
no-swap pass.

**Quickselect** partitions values around a pivot to find one rank without
paying for a complete sorted order.
            """
        )
        st.subheader("Big-O Table")
        st.markdown(
            """
| Concept | Best | Average | Worst | Space | Notes |
|---|---:|---:|---:|---:|---|
| Bubble Sort with early exit | `O(n)` | `O(n^2)` | `O(n^2)` | `O(1)` | Trace every adjacent comparison on small inputs |
| Quickselect | `O(n)` | `O(n)` | `O(n^2)` | `O(1)` conceptual | Partially partitions data instead of fully sorting |
| Set membership | `O(1)` average | `O(1)` average | `O(n)` | `O(n)` | Hash-backed membership |
| Set union/intersection/difference | `O(n + m)` | `O(n + m)` | `O(nm)` if hashing degrades | `O(n + m)` | Static operations return a new set |
            """
        )
    
    with tab_set:
        # Step 4: let users rebuild Set A and Set B from comma-separated values.
        st.header("Build Set Lab")
        input_col_a, input_col_b = st.columns(2)
        with input_col_a:
            set_a_raw = st.text_input(
                "Set A Values",
                value=_SET_A_DEFAULT,
                key="bubble_quickselect_set_a_input",
            )
            build_a = st.button("Build Set A", key="bubble_quickselect_build_set_a")
        with input_col_b:
            set_b_raw = st.text_input(
                "Set B Values",
                value=_SET_B_DEFAULT,
                key="bubble_quickselect_set_b_input",
            )
            build_b = st.button("Build Set B", key="bubble_quickselect_build_set_b")

        # VALIDATION: build buttons parse input and surface friendly errors.
        if build_a:
            try:
                # Step 1: parse Set A text into hashable values.
                st.session_state["bubble_quickselect_set_a_values"] = _parse_hashable_values(set_a_raw)
                # Step 2: clear the prior operation result after rebuilding Set A.
                st.session_state["bubble_quickselect_last_set_operation_result"] = None
                st.success("Set A built.")
            except ValueError as exc:
                # VALIDATION: malformed set text is reported without changing state.
                st.error(str(exc))
                st.info("Use comma-separated values such as 1, 2, 3.")

        # VALIDATION: Set B uses the same parsing rules as Set A.
        if build_b:
            try:
                # Step 1: parse Set B text into hashable values.
                st.session_state["bubble_quickselect_set_b_values"] = _parse_hashable_values(set_b_raw)
                # Step 2: clear the prior operation result after rebuilding Set B.
                st.session_state["bubble_quickselect_last_set_operation_result"] = None
                st.success("Set B built.")
            except ValueError as exc:
                # VALIDATION: malformed set text is reported without changing state.
                st.error(str(exc))
                st.info("Use comma-separated values such as 3, 4, 5.")
        
        # Divider between set builder and manual operations
        st.divider()
        
        st.subheader("Manual Operation Playground")
        # Split the layout into three columns for operation, target set, and operand set selection
        operation_col, target_col, operand_col = st.columns(3)
        with operation_col:
            set_operation = st.selectbox(
                "Set Operation",
                _SET_OPERATION_NAMES,
                key="bubble_quickselect_manual_set_operation",
            )
        with target_col:
            target_set = st.selectbox(
                "Target Set",
                ["Set A", "Set B"],
                key="bubble_quickselect_manual_target_set",
            )
        # Operand set selection
        operand_set: str | None = None
        with operand_col:
            # DISPATCH: dynamic operations require no second set operand.
            if set_operation in _SET_DYNAMIC_OPERATIONS:
                st.caption("Dynamic operation uses the selected target set.")
            else:
                operand_order = st.selectbox(
                    "Operand Order",
                    ["Set A op Set B", "Set B op Set A"],
                    key="bubble_quickselect_manual_operand_order",
                )
                target_set = "Set A" if operand_order == "Set A op Set B" else "Set B"
                operand_set = "Set B" if target_set == "Set A" else "Set A"

        manual_value: Hashable | None = None
        # VALIDATION: dynamic operations need exactly one parsed value.
        if set_operation in _SET_DYNAMIC_OPERATIONS:
            manual_value_raw = st.text_input(
                "Add / Remove / Contains Value",
                value="3",
                key="bubble_quickselect_manual_operation_value",
            )
            try:
                manual_value = _parse_single_value(manual_value_raw)
            except ValueError as exc:
                # VALIDATION: keep the operation disabled by leaving value as None.
                st.error(str(exc))
                st.info("Enter exactly one operation value.")

        # DISPATCH: run the selected CourseSet operation only after button click.
        if st.button(
            "Run Set Operation",
            type="primary",
            key="bubble_quickselect_run_set_operation",
        ):
            try:
                # Step 1: execute the selected CourseSet operation.
                result = _record_set_operation(
                    set_operation,
                    target_set,
                    operand_set=operand_set,
                    input_value=manual_value,
                    mutate_session=True,
                )
                # Step 2: store the latest result and bounded manual history.
                st.session_state["bubble_quickselect_last_set_operation_result"] = result
                st.session_state["bubble_quickselect_set_operation_history"] = [
                    *st.session_state["bubble_quickselect_set_operation_history"],
                    result,
                ][-10:]
                st.success(f"Set operation complete: {result.target_set}.{result.operation}.")
            except ValueError as exc:
                # VALIDATION: report missing operands or values without mutating state.
                st.error(str(exc))
                st.info("Check the selected operation and required input value.")

        _render_set_state_summary()

        last_result = st.session_state["bubble_quickselect_last_set_operation_result"]
        # DISPATCH: render the detailed result card only after an operation exists.
        if last_result is not None:
            _render_set_operation_result(last_result)

        st.subheader("Manual Operation History")
        _render_set_operation_history(st.session_state["bubble_quickselect_set_operation_history"])
        
        # Divider for automatic set operations demo
        st.divider()
        st.subheader("Automatic Set Operations Demo")
        demo_value_raw = st.text_input(
            "Automatic Demo Value",
            value="3",
            key="bubble_quickselect_auto_demo_value",
        )
        # DISPATCH: the automatic demo runs read-only operation copies.
        if st.button(
            "Run Automatic Set Operations Demo",
            key="bubble_quickselect_run_auto_demo",
        ):
            try:
                # Step 1: parse one demo value for add/remove/contains.
                demo_value = _parse_single_value(demo_value_raw)
                # Step 2: run every set operation against read-only source copies.
                st.session_state["bubble_quickselect_set_auto_demo_results"] = _run_set_auto_demo(demo_value)
                st.success("Automatic set operations demo complete.")
            except ValueError as exc:
                # VALIDATION: automatic demos require exactly one input value.
                st.error(str(exc))
                st.info("Enter exactly one value for the automatic demo.")

        demo_results = st.session_state["bubble_quickselect_set_auto_demo_results"]
        # DISPATCH: show expandable results when the demo has completed.
        if demo_results:
            st.subheader("Automatic Demo Results")
            # MAIN ITERATION LOOP: one expander per required set operation.
            for index, result in enumerate(demo_results, start=1):
                # Step 1: include operand text only for two-set operations.
                operand_text = f" {result.operand_set}" if result.operand_set is not None else ""
                with st.expander(
                    f"Demo {index}: {result.target_set} {result.operation}{operand_text}",
                    expanded=index == 1,
                ):
                    _render_set_operation_result(result)
        else:
            st.info("Run the automatic demo to see every required set operation.")

    with tab_bubble:
        # Step 5: collect a dataset and run the native Bubble Sort implementation.
        st.header("Bubble Sort Lab")
        bubble_source, bubble_size, bubble_seed, bubble_manual = _render_dataset_controls(
            "bubble_quickselect_bubble"
        )
        if st.button(
            "Run Bubble Sort",
            type="primary",
            key="bubble_quickselect_run_bubble_sort",
        ):
            try:
                # Step 1: construct the dataset from generated or manual controls.
                dataset = _dataset_from_controls(
                    bubble_source,
                    bubble_size,
                    bubble_seed,
                    bubble_manual,
                )
                # Step 2: run the algorithm with traces enabled for small inputs.
                result = bubble_sort(dataset, collect_trace=True)
                st.session_state["bubble_quickselect_bubble_dataset"] = dataset
                st.session_state["bubble_quickselect_bubble_result"] = result
                st.success("Bubble Sort complete.")
            except ValueError as exc:
                # VALIDATION: report dataset errors without replacing prior results.
                st.error(str(exc))
                st.info("Choose a generated dataset or enter comma-separated integers.")
        _render_sort_result(st.session_state["bubble_quickselect_bubble_result"])

    with tab_quickselect:
        # Step 6: collect a dataset/rank and run the native Quickselect implementation.
        st.header("Quickselect Lab")
        quick_source, quick_size, quick_seed, quick_manual = _render_dataset_controls(
            "bubble_quickselect_quickselect"
        )
        k_value = st.number_input(
            "k (1-based rank)",
            min_value=0,
            value=1,
            step=1,
            key="bubble_quickselect_k_value",
        )
        if st.button(
            "Run Quickselect",
            type="primary",
            key="bubble_quickselect_run_quickselect",
        ):
            try:
                # Step 1: construct the dataset from generated or manual controls.
                dataset = _dataset_from_controls(
                    quick_source,
                    quick_size,
                    quick_seed,
                    quick_manual,
                )
                # VALIDATION: Quickselect needs one value and an in-range rank.
                if not dataset:
                    raise ValueError("Quickselect requires at least one value.")
                if int(k_value) < 1:
                    raise ValueError("k must be at least 1.")
                if int(k_value) > len(dataset):
                    raise ValueError("k must be no larger than the dataset size.")
                # Step 2: run the selection algorithm after validation succeeds.
                result = quickselect(dataset, int(k_value), collect_trace=True)
                st.session_state["bubble_quickselect_quickselect_dataset"] = dataset
                st.session_state["bubble_quickselect_quickselect_result"] = result
                st.success("Quickselect complete.")
            except ValueError as exc:
                # VALIDATION: report dataset/rank errors without replacing prior results.
                st.error(str(exc))
                st.info("Use a non-empty integer dataset and choose a valid 1-based rank.")
        _render_quickselect_result(st.session_state["bubble_quickselect_quickselect_result"])

    with tab_benchmark:
        # Step 7: run repeatable benchmark profiles and render CSV-backed results.
        st.header("Benchmark Lab")
        profile_col, config_col = st.columns([1, 2])
        with profile_col:
            profile = st.radio(
                "Benchmark Profile",
                ["Quick", "Full"],
                horizontal=True,
                key="bubble_quickselect_benchmark_profile",
            )
            # DISPATCH: the quick profile keeps runtime low; full profile broadens scale.
            default_sizes = DEFAULT_QUICK_SIZES if profile == "Quick" else DEFAULT_FULL_SIZES
        benchmark_size_options = sorted(set(DEFAULT_QUICK_SIZES + DEFAULT_FULL_SIZES))
        # Add benchmark size and type selectors
        with config_col:
            sizes = st.multiselect(
                "Benchmark Sizes",
                benchmark_size_options,
                default=default_sizes,
                key="bubble_quickselect_benchmark_sizes",
            )
            # Dataset types selector
            dataset_types = st.multiselect(
                "Benchmark Dataset Types",
                DEFAULT_BENCHMARK_DATASET_TYPES,
                default=DEFAULT_BENCHMARK_DATASET_TYPES,
                key="bubble_quickselect_benchmark_dataset_types",
            )
            # Repeats per workload selector
            repeats = st.number_input(
                "Repeats per workload",
                min_value=1,
                max_value=5,
                value=1,
                step=1,
                key="bubble_quickselect_benchmark_repeats",
            )
        # Divider for benchmark controls
        
        action_col_a, action_col_b = st.columns(2)
        run_clicked = action_col_a.button(
            "Run Benchmark",
            type="primary",
            key="bubble_quickselect_run_benchmark",
        )
        load_clicked = action_col_b.button(
            "Load saved CSV",
            key="bubble_quickselect_load_saved_csv",
        )

        # DISPATCH: benchmarks can be freshly run or loaded from the saved CSV.
        if run_clicked:
            selected_sizes = sizes or DEFAULT_QUICK_SIZES
            selected_types = dataset_types or DEFAULT_BENCHMARK_DATASET_TYPES
            progress = st.progress(0.0, text="Starting benchmark...")

            # --------------------------------------------------------------- _progress()
            def _progress(done: int, total: int, label: str) -> None:
                """Update benchmark progress.

                Args:
                    done: Completed workload count.
                    total: Total workload count.
                    label: Current workload label.

                Returns:
                    None.
                """
                # Step 1: advance Streamlit progress using the benchmark callback.
                progress.progress(done / total, text=f"{label} ({done}/{total})")
            # --------------------------------------------------------------- end _progress()

            # Step 2: run the benchmark matrix and persist the latest CSV artifact.
            benchmark_df = run_benchmarks(
                sizes=selected_sizes,
                dataset_types=selected_types,
                repeats=int(repeats),
                seed=DEFAULT_RANDOM_SEED,
                progress_callback=_progress,
            )
            progress.empty()
            save_results_csv(benchmark_df, _CSV_PATH)
            st.session_state["bubble_quickselect_benchmark_df"] = benchmark_df
            st.success(f"Benchmark complete. Saved {_CSV_PATH.name} with {len(benchmark_df)} rows.")

        # DISPATCH: reload prior benchmark output without rerunning workloads.
        if load_clicked:
            st.session_state["bubble_quickselect_benchmark_df"] = load_results_csv(_CSV_PATH)
            st.success("Loaded saved benchmark CSV.")

        benchmark_df = st.session_state["bubble_quickselect_benchmark_df"]
        # DISPATCH: render results table and download button only when rows exist.
        if benchmark_df is not None and not benchmark_df.empty:
            st.subheader("Benchmark Results")
            st.dataframe(benchmark_df, width="stretch", hide_index=True)
            # Step 1: encode the visible results table for download.
            csv_bytes = benchmark_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Benchmark CSV",
                data=csv_bytes,
                file_name="benchmark_results.csv",
                mime="text/csv",
                key="bubble_quickselect_download_benchmark_csv",
            )
        else:
            # FALLBACK: no saved or freshly run benchmark rows are available yet.
            st.info("Run the benchmark to generate comparison results.")
        _render_benchmark_chart(benchmark_df)

    with tab_analysis:
        # Step 8: render the written analysis Markdown artifact.
        st.header("Written Analysis")
        _render_markdown_file(_WRITTEN_ANALYSIS_PATH)
# ----------------------------------------------------- end render_bubble_quickselect_sets_page()


# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
