# -------------------------------------------------------------------------
# File: streamlit_app.py
#
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
# -----------------------------------------

# --- Module Functionality ---
# Main entry point for the Hash Table & Priority Queue Tool.
# Provides seven tabs: Overview, Dataset Builder,
# Hash Table Lab, Priority Queue Lab, Benchmark Lab, Written Analysis,
# and Recommendation Guide.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit application - Hash Table & Priority Queue Tool.

Launch with::

    streamlit run CTA-5/streamlit_app.py
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

import sys
import time
from collections.abc import Callable
from pathlib import Path

# SETUP: add project root so module packages are importable
_PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
import pandas as pd

# Local module imports
# Algorithms
from algorithms.hash_table import HashTable
from algorithms.priority_queue import BinaryHeapPriorityQueue
from analysis.lab_validation import (
    run_benchmark_validation,
    run_hash_table_demo,
    run_priority_queue_demo,
    summarize_benchmark_validation,
)
# Data
from data.dataset_manager import (
    generate_key_value_dataset,
    generate_priority_items,
    generate_collision_keys,
)
# Models
from models.lab_operation_result import LabOperationResult
from models.priority_item import PriorityItem
from analysis.benchmark_search import (
    DEFAULT_RANDOM_SEED,
    DEFAULT_REPEATS,
    run_benchmarks,
    save_results_csv,
    load_results_csv,
    compute_operation_scaling_summary,
    compute_speedup_summary,
    build_collision_benchmark_state,
    build_priority_queue_benchmark_state,
    DEFAULT_SIZES,
    DEFAULT_QUERY_MODES,
)
# Analysis
from analysis.report_generator import (
    build_benchmark_table,
    build_operation_scaling_table,
    build_speedup_summary_table,
    generate_summary_sentences,
    generate_charts,
)
# UI
from ui.streamlit_helpers import (
    render_header,
    render_dataset_info,
    render_lab_quick_start,
    render_lab_status_summary,
    render_empty_state_guidance,
    render_section_intro,
    render_action_tip,
    render_guided_operation_results,
    render_manual_operation_result,
    render_operation_history,
    render_validation_results,
    render_hash_table_state_panel,
    render_hash_table_buckets,
    render_hash_collision_chain_diagram,
    render_priority_queue_state,
    render_priority_queue_tree_diagram,
    render_benchmark_table,
    render_benchmark_charts,
    render_benchmark_validation_summary,
    render_analysis_markdown_file,
)

# ______________________________________________________________________________
# Global Constants / Variables
# ==============================================================================
# PATHS
# ==============================================================================
# Constraint set: every artifact path is resolved relative to the streamlit_app.py
# location so the launcher works from any current working directory.
# Rationale: keeps `streamlit run CTA-5/streamlit_app.py` reproducible across
# machines and submission environments without environment variables.
# ------------------------------------------------------------------------------

_ANALYSIS_DIR = _PROJECT_ROOT / "analysis"
_CSV_PATH = _ANALYSIS_DIR / "benchmark_results.csv"
_SPEEDUP_CSV_PATH = _ANALYSIS_DIR / "search_speedup_summary.csv"
_SCALING_CSV_PATH = _ANALYSIS_DIR / "operation_scaling_summary.csv"
_WRITTEN_ANALYSIS_PATH = _ANALYSIS_DIR / "written_analysis.md"
_RECOMMENDATION_GUIDE_PATH = _ANALYSIS_DIR / "recommendation_guide.md"

# ______________________________________________________________________________
#
# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="CTA-5 — Hash Tables & Priority Queues",
    page_icon=_PROJECT_ROOT / "icon.png",
    layout="wide",
)

# ______________________________________________________________________________
#
# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
# Streamlit re-executes this module on every interaction. Initializing
# st.session_state with explicit defaults keeps tab state stable across
# reruns and gives every helper a known starting shape.
# ------------------------------------------------------------------------------

_DEFAULTS: dict[str, object] = {
    "kv_dataset": None,
    "priority_items": None,
    "dataset_size": 100,
    "dataset_seed": 506,
    "hash_table": None,
    "priority_queue": None,
    "pq_mode": "max",
    "benchmark_df": None,
    "speedup_df": None,
    "operation_scaling_df": None,
    "hash_demo_result": None,
    "hash_demo_note": "",
    "priority_demo_result": None,
    "priority_demo_note": "",
    "benchmark_validation": None,
    "collision_demo_enabled": False,
    "collision_demo_capacity": 11,
    "collision_demo_target_bucket": 0,
    "hash_history": [],
    "priority_history": [],
    "last_hash_feedback": None,
    "last_priority_feedback": None,
    "last_hash_operation_result": None,
    "last_priority_operation_result": None,
    "benchmark_size_selection": list(DEFAULT_SIZES),
    "benchmark_query_mode_selection": list(DEFAULT_QUERY_MODES),
    "benchmark_repeats": DEFAULT_REPEATS,
}

# Initialize session state
for _key, _val in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# SESSION STATE & FEEDBACK HELPERS
# ==============================================================================
# Small private helpers that read or mutate ``st.session_state``. They keep
# tab code declarative by hiding history-list bookkeeping, feedback storage,
# and "is this lab ready?" guards behind named functions.
#
# - Function: _append_history()           - Push a new message onto a history list
# - Function: _set_feedback()             - Store a (level, message) feedback tuple
# - Function: _render_feedback()          - Render a stored feedback tuple via st
# - Function: _clear_hash_lab_state()     - Reset hash-lab UI state
# - Function: _clear_priority_lab_state() - Reset priority-lab UI state
# - Function: _hash_dataset_ready()       - True when a KV dataset is available
# - Function: _priority_dataset_ready()   - True when priority items are loaded
# - Function: _hash_table_ready()         - True when a hash table is built
# - Function: _priority_queue_ready()     - True when a priority queue is built
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _append_history()
def _append_history(history_key: str, message: str) -> None:
    """Record a recent user-visible action in session state.

    Logic:
        This helper maintains a bounded most-recent-first action log.
        1. Snapshot the existing history list from session state.
        2. Insert the new message at position 0 (most recent first).
        3. Truncate to the last 8 entries before writing back.
    """
    history = list(st.session_state[history_key])
    history.insert(0, message)
    st.session_state[history_key] = history[:8]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _set_feedback()
def _set_feedback(feedback_key: str, level: str, message: str) -> None:
    """Store a feedback message for later rendering.

    Logic:
        This helper persists a feedback envelope across the next rerun.
        1. Pack the level and message as a 2-tuple.
        2. Stash the tuple under *feedback_key* in session state.
    """
    st.session_state[feedback_key] = (level, message)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_feedback()
def _render_feedback(feedback_key: str) -> None:
    """Render a stored feedback message if one exists.

    Logic:
        This helper dispatches feedback to the matching st.* call.
        1. VALIDATION: silently return when no feedback is stored.
        2. Unpack the (level, message) tuple from session state.
        3. DISPATCH: route the message to st.success / warning / error / info.
    """
    feedback = st.session_state[feedback_key]
    # VALIDATION: nothing to render when no feedback has been queued
    if feedback is None:
        return
    level, message = feedback
    # DISPATCH: pick the Streamlit channel that matches the requested level
    if level == "success":
        st.success(message)
    elif level == "warning":
        st.warning(message)
    elif level == "error":
        st.error(message)
    else:
        st.info(message)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _clear_hash_lab_state()
def _clear_hash_lab_state(*, clear_table: bool = False) -> None:
    """Reset hash-table lab UI state when data or structures are replaced.

    Logic:
        This helper wipes derived UI state without touching the dataset.
        1. SAFETY CHECK: only drop the active hash table when *clear_table* is set.
        2. Reset the guided demo result, note, history, feedback, and last result.
    """
    # SAFETY CHECK: only forget the structure when the caller explicitly opts in
    if clear_table:
        st.session_state["hash_table"] = None
    st.session_state["hash_demo_result"] = None
    st.session_state["hash_demo_note"] = ""
    st.session_state["hash_history"] = []
    st.session_state["last_hash_feedback"] = None
    st.session_state["last_hash_operation_result"] = None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _clear_priority_lab_state()
def _clear_priority_lab_state(*, clear_queue: bool = False) -> None:
    """Reset priority-queue lab UI state when data or structures are replaced.

    Logic:
        This helper wipes derived UI state without touching the dataset.
        1. SAFETY CHECK: only drop the active queue when *clear_queue* is set.
        2. Reset the guided demo result, note, history, feedback, and last result.
    """
    # SAFETY CHECK: only forget the structure when the caller explicitly opts in
    if clear_queue:
        st.session_state["priority_queue"] = None
    st.session_state["priority_demo_result"] = None
    st.session_state["priority_demo_note"] = ""
    st.session_state["priority_history"] = []
    st.session_state["last_priority_feedback"] = None
    st.session_state["last_priority_operation_result"] = None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _hash_dataset_ready()
def _hash_dataset_ready() -> bool:
    """Return True when a key-value dataset is available."""
    return st.session_state["kv_dataset"] is not None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _priority_dataset_ready()
def _priority_dataset_ready() -> bool:
    """Return True when priority items are available."""
    return st.session_state["priority_items"] is not None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _hash_table_ready()
def _hash_table_ready() -> bool:
    """Return True when a hash table is available."""
    return st.session_state["hash_table"] is not None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _priority_queue_ready()
def _priority_queue_ready() -> bool:
    """Return True when a priority queue is available."""
    return st.session_state["priority_queue"] is not None
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# DEMO DATASET & PREVIEW HELPERS
# ==============================================================================
# Helpers that select demo inputs for the guided lab tabs and build short
# preview lists for the UI cards.
#
# - Function: _select_hash_demo_records()  - Pick the source dataset for the hash demo
# - Function: _select_priority_demo_items() - Pick the source list for the heap demo
# - Function: _build_priority_preview()    - Build extraction-order preview lines
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _select_hash_demo_records()
def _select_hash_demo_records() -> tuple[list[tuple[str, int]] | None, str]:
    """Choose the dataset source for the guided hash-table demo.

    Logic:
        This helper prefers the user's loaded dataset over a fresh demo set.
        1. Read the current key-value dataset from session state.
        2. SAFETY CHECK: when at least 100 records are loaded, use the first 100.
        3. Otherwise return ``None`` so the caller generates a 100-item set.
    """
    records = st.session_state["kv_dataset"]
    # SAFETY CHECK: only reuse the loaded dataset when it has enough rows
    if records is not None and len(records) >= 100:
        return records[:100], "Using the first 100 records from the current dataset."
    return None, "Generated a deterministic 100-item validation dataset for this demo run."
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _select_priority_demo_items()
def _select_priority_demo_items() -> tuple[list[PriorityItem] | None, str]:
    """Choose the dataset source for the guided priority-queue demo.

    Logic:
        This helper prefers the user's loaded items over a fresh demo set.
        1. Read the current priority items from session state.
        2. SAFETY CHECK: when at least 100 items are loaded, use the first 100.
        3. Otherwise return ``None`` so the caller generates a 100-item set.
    """
    items = st.session_state["priority_items"]
    # SAFETY CHECK: only reuse the loaded list when it has enough items
    if items is not None and len(items) >= 100:
        return items[:100], "Using the first 100 priority items from the current dataset."
    return None, "Generated a deterministic 100-item priority dataset for this demo run."
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_priority_preview()
def _build_priority_preview(
    queue: BinaryHeapPriorityQueue,
    preview_count: int = 5,
) -> list[str]:
    """Build a short preview of upcoming priority-queue extractions.

    Logic:
        This helper previews the next-out items without disturbing the queue.
        1. Clone the queue so destructive extracts do not mutate the original.
        2. MAIN ITERATION LOOP: pop up to *preview_count* items into a buffer.
        3. Format each as "label (priority=N)" for compact UI display.
    """
    # Step 1: clone the queue so the original is left untouched
    clone = BinaryHeapPriorityQueue(mode=queue.mode)
    for item in queue.to_list():
        clone.insert(item)

    preview: list[str] = []
    # MAIN ITERATION LOOP: pull up to preview_count items in priority order
    while not clone.is_empty() and len(preview) < preview_count:
        item = clone.extract_top()
        preview.append(f"{item.label} (priority={item.priority})")
    return preview
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# BENCHMARK ORCHESTRATION HELPERS
# ==============================================================================
# Helpers that wrap the benchmark engine, persist its CSV/chart artifacts,
# and rebuild the linked diagrams that accompany the benchmark output cards.
#
# - Function: _store_benchmark_outputs()          - Cache + persist all artifacts
# - Function: _set_benchmark_preview_sizes()      - Switch UI to small preview sizes
# - Function: _render_benchmark_note()            - Consistent explanatory caption
# - Function: _select_benchmark_visual_size()     - Pick a readable diagram size
# - Function: _render_benchmark_collision_diagram() - Rebuild collision diagram
# - Function: _render_benchmark_heap_diagram()    - Rebuild priority-queue diagram
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _store_benchmark_outputs()
def _store_benchmark_outputs(benchmark_df: pd.DataFrame) -> None:
    """Compute, cache, and persist benchmark summary artifacts.

    Logic:
        This helper turns raw benchmark rows into the full artifact bundle.
        1. Compute the speedup and operation-scaling summary tables.
        2. Run the benchmark validation summary against all three frames.
        3. Cache every frame and validation result in session state.
        4. Persist the CSV files and regenerate the chart PNGs on disk.
    """
    # derive the two summary tables consumed by the analysis tab
    speedup_df = compute_speedup_summary(benchmark_df)
    operation_scaling_df = compute_operation_scaling_summary(benchmark_df)
    # validate the bundle for monotonic scaling and expected speedup
    validation_result = summarize_benchmark_validation(
        benchmark_df,
        speedup_df,
        operation_scaling_df,
    )

    # cache everything so subsequent reruns skip recomputation
    st.session_state["benchmark_df"] = benchmark_df
    st.session_state["speedup_df"] = speedup_df
    st.session_state["operation_scaling_df"] = operation_scaling_df
    st.session_state["benchmark_validation"] = validation_result

    # persist artifacts so the written analysis can reference them
    save_results_csv(benchmark_df, _CSV_PATH)
    save_results_csv(speedup_df, _SPEEDUP_CSV_PATH)
    save_results_csv(operation_scaling_df, _SCALING_CSV_PATH)
    generate_charts(benchmark_df, speedup_df, _ANALYSIS_DIR)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _set_benchmark_preview_sizes()
def _set_benchmark_preview_sizes() -> None:
    """Switch the benchmark size multiselect to the preview preset."""
    st.session_state["benchmark_size_selection"] = [100, 500]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_benchmark_note()
def _render_benchmark_note(message: str) -> None:
    """Render a consistent explanatory note under a benchmark artifact.

    Logic:
        This helper standardizes the "Note: The ..." caption format.
        1. Prepend the fixed "Note: The " preamble to the supplied phrase.
        2. Display the resulting line via st.caption().
    """
    st.caption(f"Note: The {message}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _select_benchmark_visual_size()
def _select_benchmark_visual_size(benchmark_df: pd.DataFrame) -> int:
    """Choose a readable size for the benchmark-linked diagrams.

    Logic:
        This helper picks a small representative n for diagram rebuilds.
        1. Collect the unique sizes present in the benchmark frame.
        2. SAFETY CHECK: fall back to 100 when no sizes are recorded.
        3. Prefer 100 when available, otherwise return the smallest size.
    """
    sizes = sorted(int(value) for value in benchmark_df["size"].unique().tolist())
    # SAFETY CHECK: degenerate frames default to a readable n = 100
    if not sizes:
        return 100
    return 100 if 100 in sizes else sizes[0]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_benchmark_collision_diagram()
def _render_benchmark_collision_diagram(benchmark_df: pd.DataFrame) -> None:
    """Render the collision diagram rebuilt from the benchmark settings.

    Logic:
        This helper rebuilds a tiny snapshot for the collision visual.
        1. Filter the benchmark frame to forced-collision rows only.
        2. VALIDATION: surface a friendly notice when no rows are present.
        3. Pick a representative size and rebuild the colliding hash table.
        4. Render the stats panel, chain diagram, bucket dump, and caption.
    """
    st.subheader("Collision Diagram")
    collision_rows = benchmark_df[benchmark_df["operation_group"] == "hash_collision"]
    # VALIDATION: nothing to render when the benchmark skipped collision runs
    if collision_rows.empty:
        st.info("No forced-collision benchmark rows are available.")
        return

    # rebuild a small representative collision table
    diagram_size = _select_benchmark_visual_size(collision_rows)
    collision_table = build_collision_benchmark_state(
        diagram_size,
        seed=DEFAULT_RANDOM_SEED,
    )
    # render the linked visuals and explanatory caption
    render_hash_table_state_panel(
        collision_table.get_stats(),
        collision_demo_enabled=True,
    )
    # render the chain diagram
    render_hash_collision_chain_diagram(collision_table.get_buckets())
    # render the bucket table
    render_hash_table_buckets(collision_table.get_buckets())
    # render the note
    _render_benchmark_note(
        f"collision diagram illustrates how multiple keys cluster into a small "
        f"set of buckets during the forced-collision benchmark, using a "
        f"representative n = {diagram_size:,} snapshot rebuilt from the same "
        "benchmark inputs. The supporting bucket table below shows the full "
        "raw chain data."
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_benchmark_heap_diagram()
def _render_benchmark_heap_diagram(benchmark_df: pd.DataFrame) -> None:
    """Render the priority-queue heap diagram rebuilt from the benchmark.

    Logic:
        This helper rebuilds a tiny heap snapshot for the priority visual.
        1. Filter the benchmark frame to priority-queue core rows only.
        2. VALIDATION: surface a friendly notice when no rows are present.
        3. Pick a representative size + mode and rebuild the heap.
        4. Render the heap diagram, state panel, and explanatory caption.
    """
    st.subheader("Heap Diagram")
    priority_rows = benchmark_df[benchmark_df["operation_group"] == "priority_queue_core"]
    # VALIDATION: nothing to render when the benchmark skipped priority runs
    if priority_rows.empty:
        st.info("No priority-queue benchmark rows are available.")
        return

    # rebuild a small representative heap, preferring max-mode
    diagram_size = _select_benchmark_visual_size(priority_rows)
    scenarios = sorted(str(value) for value in priority_rows["scenario"].unique().tolist())
    representative_mode = "max" if "max" in scenarios else scenarios[0]
    # build the heap
    queue = build_priority_queue_benchmark_state(
        diagram_size,
        mode=representative_mode,
        seed=DEFAULT_RANDOM_SEED,
    )
    # render the linked visuals and explanatory caption
    render_priority_queue_tree_diagram(
        queue.to_list(),
        representative_mode,
    )
    # render the state panel
    render_priority_queue_state(
        queue.to_list(),
        representative_mode,
        heap_valid=queue.is_valid_heap(),
        show_mode_explanation=True,
        extraction_preview=_build_priority_preview(queue),
    )
    # render the note
    _render_benchmark_note(
        f"heap diagram illustrates the representative {representative_mode.upper()}-"
        f"heap layout used by the priority-queue benchmark at n = {diagram_size:,}, "
        "showing that items stay in valid priority order while the heap property "
        "is preserved."
    )
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# OPERATION SNAPSHOT & HIGHLIGHT HELPERS
# ==============================================================================
# Helpers that snapshot lab structures before/after each manual operation
# and pick which row to highlight in the operation result cards.
#
# - Function: _get_example_hash_key()         - Suggest an example key for the UI
# - Function: _build_high_priority_example()  - Build a demo priority item tuple
# - Function: _snapshot_hash_table()          - Compact bucket snapshot lines
# - Function: _snapshot_priority_queue()      - Compact heap-array snapshot lines
# - Function: _first_snapshot_diff()          - First row index that differs
# - Function: _find_snapshot_row()            - First row containing *token*
# - Function: _resolve_snapshot_highlights()  - Pick before/after highlight rows
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _get_example_hash_key()
def _get_example_hash_key() -> str | None:
    """Return an existing key from the active hash table when available."""
    hash_table: HashTable | None = st.session_state["hash_table"]
    # SAFETY CHECK: empty or absent tables have no example to surface
    if hash_table is None or len(hash_table) == 0:
        return None
    return hash_table.items()[0][0]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_high_priority_example()
def _build_high_priority_example(
    queue: BinaryHeapPriorityQueue,
) -> tuple[str, int, str]:
    """Return a label, priority, and payload for a demo priority item.

    Logic:
        This helper builds an item guaranteed to outrank the current top.
        1. Read the current top priority (or 100 when the queue is empty).
        2. DISPATCH on queue.mode: max-mode adds, min-mode subtracts 100.
        3. Build a deterministic label that includes mode and queue size.
    """
    top_priority = queue.peek().priority if not queue.is_empty() else 100
    # DISPATCH: max-mode wants higher priorities, min-mode wants lower ones
    if queue.mode == "max":
        priority = top_priority + 100
        payload = "demo high-priority item"
    else:
        priority = top_priority - 100
        payload = "demo low-priority item"
    label = f"demo-{queue.mode}-priority-{len(queue) + 1:03d}"
    return label, priority, payload
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _snapshot_hash_table()
def _snapshot_hash_table(table: HashTable, preview_count: int = 6) -> list[str]:
    """Return a compact snapshot of the hash table's non-empty buckets.

    Logic:
        This helper formats every non-empty bucket as a single text line.
        1. MAIN ITERATION LOOP: walk every bucket index in the table.
        2. Skip empty buckets so the snapshot stays compact.
        3. Render each chain as ``bucket[i]: (k1: v1) -> (k2: v2)``.
    """
    rows: list[str] = []
    # MAIN ITERATION LOOP: scan every bucket and skip the empty ones
    for bucket_index, bucket in enumerate(table.get_buckets()):
        if bucket:
            chain = " -> ".join(f"({entry.key}: {entry.value})" for entry in bucket)
            rows.append(f"bucket[{bucket_index}]: {chain}")
    return rows
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _snapshot_priority_queue()
def _snapshot_priority_queue(
    queue: BinaryHeapPriorityQueue,
    preview_count: int = 8,
) -> list[str]:
    """Return a compact snapshot of the heap array.

    Logic:
        This helper formats the heap array slot-by-slot as text lines.
        1. Pull the current heap array via to_list() (preserves order).
        2. Format each slot as ``[i] label (priority=N, seq=N)``.
    """
    heap_items = queue.to_list()
    return [
        (
            f"[{index}] {item.label} "
            f"(priority={item.priority}, seq={item.sequence_number})"
        )
        for index, item in enumerate(heap_items)
    ]
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _first_snapshot_diff()
def _first_snapshot_diff(before_lines: list[str], after_lines: list[str]) -> int | None:
    """Return the first differing row between two snapshot line lists.

    Logic:
        This helper finds the earliest row that changed across an operation.
        1. MAIN ITERATION LOOP: compare row-by-row up to the shorter length.
        2. Return the first index whose before/after rows disagree.
        3. When lengths differ but prefixes match, return the shorter length.
        4. Return ``None`` when the two snapshots are identical.
    """
    min_len = min(len(before_lines), len(after_lines))
    # MAIN ITERATION LOOP: scan paired rows until we find a divergence
    for index in range(min_len):
        if before_lines[index] != after_lines[index]:
            return index
    # Step 3: a length difference with matching prefix points at the boundary
    if len(before_lines) != len(after_lines):
        return min_len
    return None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _find_snapshot_row()
def _find_snapshot_row(lines: list[str], token: str) -> int | None:
    """Return the index of the first snapshot row containing *token*.

    Logic:
        This helper finds the row whose text mentions a key or label.
        1. MAIN ITERATION LOOP: scan each row in order.
        2. Return the first index whose row contains the *token* substring.
        3. Return ``None`` when no row matches.
    """
    # MAIN ITERATION LOOP: linear search for the token-bearing row
    for index, line in enumerate(lines):
        if token in line:
            return index
    return None
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _resolve_snapshot_highlights()
def _resolve_snapshot_highlights(
    before_lines: list[str],
    after_lines: list[str],
    *,
    match_token: str | None = None,
) -> tuple[int | None, int | None]:
    """Choose which snapshot rows to highlight before and after an operation.

    Logic:
        This helper decides which row index the UI should highlight.
        1. STRATEGY A: when *match_token* is provided, prefer token-matched rows.
        2. STRATEGY B: fall back to the first differing row across snapshots.
        3. Adjust the (before, after) pair when the lengths changed: a longer
           ``after`` means an insertion, a longer ``before`` means a deletion.
    """
    # STRATEGY A: prefer matching by token (e.g. specific key or label)
    if match_token:
        before_idx = _find_snapshot_row(before_lines, match_token)
        after_idx = _find_snapshot_row(after_lines, match_token)
        if before_idx is not None or after_idx is not None:
            return before_idx, after_idx

    # STRATEGY B: locate the first divergent row when no token matches
    diff_idx = _first_snapshot_diff(before_lines, after_lines)
    if diff_idx is None:
        return None, None

    # align the highlight to the side that actually grew or shrunk
    if len(after_lines) > len(before_lines):
        return None, diff_idx
    if len(before_lines) > len(after_lines):
        return diff_idx, None
    return diff_idx, diff_idx
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# OPERATION RESULT RECORDERS
# ==============================================================================
# Helpers that time a single manual operation, snapshot the structure, and
# package the captured fields into a LabOperationResult for the result card.
#
# - Function: _record_hash_operation_result()    - One hash-table op + snapshot
# - Function: _record_priority_operation_result() - One priority-queue op + snapshot
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _record_hash_operation_result()
def _record_hash_operation_result(
    operation: str,
    *,
    complexity: str,
    summary: str | Callable[[object | None], str],
    input_details: list[str] | None = None,
    match_key: str | None = None,
    op_callable: Callable[[], object | None],
) -> object | None:
    """Capture and store a hash-table manual operation result.

    Logic:
        This helper times one manual op and packages a LabOperationResult.
        1. Snapshot the table state and size before running the operation.
        2. Time the callable with perf_counter() and capture its return value.
        3. Snapshot the table state again and resolve the highlight indices.
        4. Build the LabOperationResult and stash it in session state.
    """
    active_table: HashTable = st.session_state["hash_table"]
    # snapshot the bucket layout before the operation runs
    before_state = _snapshot_hash_table(active_table)
    size_before = len(active_table)
    # time the operation precisely with perf_counter()
    start_time = time.perf_counter()
    returned_value = op_callable()
    elapsed_time = time.perf_counter() - start_time
    after_state = _snapshot_hash_table(active_table)
    # pick the bucket row that should be highlighted in the result card
    before_idx, after_idx = _resolve_snapshot_highlights(
        before_state,
        after_state,
        match_token=f"({match_key}:" if match_key else None,
    )
    # convert summary to text
    summary_text = summary(returned_value) if callable(summary) else summary
    # package the captured fields into a LabOperationResult
    st.session_state["last_hash_operation_result"] = LabOperationResult(
        structure="Hash Table",
        operation=operation,
        returned_value=returned_value,
        elapsed_time=elapsed_time,
        complexity=complexity,
        size_before=size_before,
        size_after=len(active_table),
        summary=summary_text,
        input_details=input_details or [],
        state_label="Bucket Snapshot",
        state_before=before_state,
        state_after=after_state,
        state_before_highlight_idx=before_idx,
        state_after_highlight_idx=after_idx,
    )
    # return the result
    return returned_value
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _record_priority_operation_result()
def _record_priority_operation_result(
    operation: str,
    *,
    complexity: str,
    summary: str | Callable[[object | None], str],
    input_details: list[str] | None = None,
    match_label: str | None = None,
    op_callable: Callable[[], object | None],
) -> object | None:
    """Capture and store a priority-queue manual operation result.

    Logic:
        This helper times one manual op and packages a LabOperationResult.
        1. Snapshot the heap state and size before running the operation.
        2. Time the callable with perf_counter() and capture its return value.
        3. Snapshot the heap state again and resolve the highlight indices.
        4. Build the LabOperationResult and stash it in session state.
    """
    active_queue: BinaryHeapPriorityQueue = st.session_state["priority_queue"]
    # snapshot the heap array before the operation runs
    before_state = _snapshot_priority_queue(active_queue)
    size_before = len(active_queue)
    # time the operation precisely with perf_counter()
    start_time = time.perf_counter()
    returned_value = op_callable()
    elapsed_time = time.perf_counter() - start_time
    after_state = _snapshot_priority_queue(active_queue)
    # SAFETY CHECK: derive a label from the returned PriorityItem when caller skipped it
    resolved_label = match_label
    if resolved_label is None and isinstance(returned_value, PriorityItem):
        resolved_label = returned_value.label
    # pick the heap row that should be highlighted in the result card
    before_idx, after_idx = _resolve_snapshot_highlights(
        before_state,
        after_state,
        match_token=f"] {resolved_label} " if resolved_label else None,
    )
    summary_text = summary(returned_value) if callable(summary) else summary
    # package the captured fields into a LabOperationResult
    st.session_state["last_priority_operation_result"] = LabOperationResult(
        structure="Priority Queue",
        operation=operation,
        returned_value=returned_value,
        elapsed_time=elapsed_time,
        complexity=complexity,
        size_before=size_before,
        size_after=len(active_queue),
        summary=summary_text,
        input_details=input_details or [],
        state_label="Heap Array",
        state_before=before_state,
        state_after=after_state,
        state_before_highlight_idx=before_idx,
        state_after_highlight_idx=after_idx,
    )
    # return the result
    return returned_value
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
#
# ==============================================================================
# MAIN ENTRY POINT — APP HEADER & TAB LAYOUT
# ==============================================================================
# Streamlit treats the rest of this file as the "main script" — every line
# below executes top-to-bottom on each rerun. The header is rendered first,
# then the tab container is created, then each tab block populates one
# learning area: Overview, Datasets, Hash Lab, Priority Lab, Benchmarks,
# Written Analysis, Recommendation Guide.
# ------------------------------------------------------------------------------

# ______________________________________________________________________________
#
# ==============================================================================
# APP HEADER
# ==============================================================================

render_header()

# ______________________________________________________________________________
#
# ==============================================================================
# TAB LAYOUT
# ==============================================================================
# Streamlit creates the seven top-level tabs in a single call. Each tab is
# rendered by its own ``with`` block below, in dependency order: Overview
# explains the project, the Datasets tab builds inputs consumed by the two
# lab tabs, and the Benchmark Lab consumes the structures produced by both.
# ------------------------------------------------------------------------------

tab_overview, tab_dataset, tab_hash, tab_pq, tab_bench, tab_analysis, tab_guide = (
    st.tabs([
        "Overview",
        "Dataset Builder",
        "Hash Table Lab",
        "Priority Queue Lab",
        "Benchmark Lab",
        "Written Analysis",
        "Recommendation Guide",
    ])
)

# ______________________________________________________________________________
#
# ==============================================================================
# TAB 1 — OVERVIEW
# ==============================================================================

with tab_overview:
    st.header("Project Overview")
    st.markdown(
        """
This Hash Table and Priority Queue Tool compares the following
Module 5 data structures:

* **Hash Table** — a custom key-value store that uses a position-weighted hash
  function with separate chaining for collision handling.
* **Priority Queue** — an array-backed binary heap that supports both
  max-heap and min-heap behavior.

Use the tabs above to build datasets, run individual structure operations,
benchmark them, and read the written analysis and recommendation guide.

### Assignment Goals

- Implement insert, search, and delete for both structures
- Test both implementations with at least 100 data items
- Compare hash table search performance against linear search
- Explain perfect and non-perfect hashing
        """
    )

    st.subheader("Hash Table")
    st.info(
        "A hash table stores key-value pairs by using a hash function to map "
        "each key to a bucket. In this project the hash table uses separate "
        "chaining, so keys that land in the same bucket are stored together in "
        "a small chain. That makes insert, search, and delete O(1) on average, "
        "but those operations can become O(n) in the worst case when many keys "
        "collide."
    )

    st.subheader("Priority Queue")
    st.info(
        "A priority queue removes items by priority instead of by insertion "
        "order. This module uses a binary heap stored in a Python list, so "
        "insert and extract-top both run in O(log n) time while peek runs in "
        "O(1). Searching for an item by label, and deleting an item by label, "
        "still requires O(n) work because the heap only guarantees the top "
        "item, not the position of every item."
    )

    st.subheader("Complexity Overview")
    st.markdown(
        """
**Hash Table**

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| Insert    | O(1)         | O(n)       |
| Search    | O(1)         | O(n)       |
| Delete    | O(1)         | O(n)       |

**Binary Heap Priority Queue**

| Operation      | Complexity |
|----------------|------------|
| Insert         | O(log n)   |
| Peek           | O(1)       |
| Extract Top    | O(log n)   |
| Search (label) | O(n)       |
| Delete (label) | O(n) + O(log n) |
        """
    )

    st.subheader("Key Concepts")
    st.info(
        "**Collision handling** explains what happens when two keys hash to the "
        "same bucket. This project uses separate chaining to keep those pairs "
        "together instead of replacing earlier data.\n\n"
        "**Heap property** means a parent node stays above its children in "
        "priority order. In a max-heap the largest priority stays near the top, "
        "while in a min-heap the smallest priority stays near the top.\n\n"
        "**Average case vs worst case** helps explain why hash tables are often "
        "very fast, but can slow down when too many keys land in one bucket.\n\n"
        "**Perfect vs non-perfect hashing** compares an ideal no-collision hash "
        "function with practical hash functions that may still need a collision "
        "strategy."
    )

    st.subheader("How to Use This Tool")
    st.info(
        "Use Dataset Builder to generate matching key-value and priority-item "
        "data. Use Hash Table Lab to load data, inspect bucket chains, and test "
        "insert, search, and delete. Use Priority Queue Lab to test heap "
        "operations in max-heap or min-heap mode. Use Benchmark Lab to compare "
        "hash table search against linear search, then read the Written "
        "Analysis and Recommendation Guide tabs to connect the results to the "
        "assignment requirements."
    )

    st.subheader("Project Files")
    st.markdown(
        f"""
- README — `{(_PROJECT_ROOT / 'README.md').name}`
- Implementation plan — `{(_PROJECT_ROOT / 'implementation_plan.md').name}`
- Written analysis — `{_WRITTEN_ANALYSIS_PATH.name}`
- Recommendation guide — `{_RECOMMENDATION_GUIDE_PATH.name}`
- Reference PDFs — `Ref-Docs/` (hash tables, heaps, treaps, and the Module 5 lecture)
        """
    )

    st.info(
        "**Note:** Treaps are included in the reference materials, but they are "
        "outside the scope of this assignment."
    )

# ______________________________________________________________________________
#
# ==============================================================================
# TAB 2 — DATASET BUILDER
# ==============================================================================

# Dataset Builder Tab
with tab_dataset:
    st.header("Dataset Builder")
    # layout for dataset size and seed
    col_size, col_seed = st.columns(2)
    # dataset size slider
    with col_size:
        dataset_size = st.slider(
            "Dataset Size",
            min_value=10,
            max_value=5_000,
            value=st.session_state["dataset_size"],
            step=10,
        )
    # random seed number input
    with col_seed:
        dataset_seed = st.number_input(
            "Random Seed",
            min_value=0,
            value=st.session_state["dataset_seed"],
            step=1,
        )
    # collision demo checkbox
    use_collision_demo = st.checkbox(
        "Use Forced-Collision Hash Demo",
        value=st.session_state["collision_demo_enabled"],
        help=(
            "Generate string keys that intentionally hash to the same bucket "
            "for a chosen hash-table capacity."
        ),
    )
    # collision demo capacity and target bucket
    collision_capacity = int(st.session_state["collision_demo_capacity"])
    collision_target_bucket = int(st.session_state["collision_demo_target_bucket"])
    # collision demo layout
    if use_collision_demo:
        # collision demo caption
        st.caption(
            "This mode is best for a small teaching dataset that makes "
            "collision chains easy to inspect."
        )
        # collision demo capacity and target bucket layout
        col_capacity, col_bucket = st.columns(2)
        # collision demo capacity
        with col_capacity:
            collision_capacity = int(st.number_input(
                "Collision Demo Capacity",
                min_value=3,
                value=int(st.session_state["collision_demo_capacity"]),
                step=1,
            ))
        # collision demo target bucket
        with col_bucket:
            collision_target_bucket = int(st.number_input(
                "Target Bucket",
                min_value=0,
                max_value=max(collision_capacity - 1, 0),
                value=min(
                    int(st.session_state["collision_demo_target_bucket"]),
                    max(collision_capacity - 1, 0),
                ),
                step=1,
            ))
    # generate dataset button
    if st.button("Generate Dataset", type="primary"):
        st.session_state["dataset_size"] = dataset_size
        st.session_state["dataset_seed"] = dataset_seed
        st.session_state["collision_demo_enabled"] = use_collision_demo
        st.session_state["collision_demo_capacity"] = collision_capacity
        st.session_state["collision_demo_target_bucket"] = collision_target_bucket
        # generate key-value dataset    
        base_records = generate_key_value_dataset(dataset_size, seed=dataset_seed)
        # collision demo
        if use_collision_demo:
            collision_keys = generate_collision_keys(
                dataset_size,
                capacity=collision_capacity,
                target_bucket=collision_target_bucket,
            )
            st.session_state["kv_dataset"] = [
                (collision_key, value)
                for collision_key, (_, value) in zip(collision_keys, base_records)
            ]
        else:
            st.session_state["kv_dataset"] = base_records

        st.session_state["priority_items"] = generate_priority_items(
            dataset_size, seed=dataset_seed
        )
        # Reset dependent lab state after replacing the datasets.
        _clear_hash_lab_state(clear_table=True)
        _clear_priority_lab_state(clear_queue=True)
        # success message
        if use_collision_demo:
            st.success(
                f"Generated {dataset_size} forced-collision key-value records and "
                f"{dataset_size} priority items (seed={dataset_seed})."
            )
        else:
            st.success(
                f"Generated {dataset_size} key-value records and priority items "
                f"(seed={dataset_seed})."
            )
    # render dataset info
    render_dataset_info(
        st.session_state["kv_dataset"],
        st.session_state["priority_items"],
    )
    # collision demo info
    if st.session_state["collision_demo_enabled"] and st.session_state["kv_dataset"] is not None:
        st.info(
            "Forced-collision demo is active. In the Hash Table Lab, use "
            f"`initial capacity = {st.session_state['collision_demo_capacity']}` "
            "with auto-resize disabled, or click the dedicated demo-load button, "
            "to guarantee those keys land in the same bucket."
        )

# ______________________________________________________________________________
#
# ==============================================================================
# TAB 3 — HASH TABLE LAB
# ==============================================================================

with tab_hash:
    st.header("Hash Table Lab")
    render_lab_quick_start(
        "Quick Start",
        [
            "Generate dataset",
            "Load hash table or run guided demo",
            "Try manual operations or inspect collisions",
        ],
    )
    # hash table state
    ht: HashTable | None = st.session_state["hash_table"]
    hash_demo_result = st.session_state["hash_demo_result"]
    # render lab status summary
    render_lab_status_summary(
        [
            ("Dataset", "Ready" if _hash_dataset_ready() else "Not Ready"),
            (
                "Dataset Size",
                f"{len(st.session_state['kv_dataset']):,}" if _hash_dataset_ready() else "0",
            ),
            ("Hash Table", "Loaded" if _hash_table_ready() else "Not Loaded"),
            (
                "Collision Demo",
                "Active" if st.session_state["collision_demo_enabled"] else "Standard",
            ),
        ]
    )
    # setup section
    with st.container(border=True):
        render_section_intro(
            "Setup",
            (
                "Choose the table settings for the next load or guided demo, then "
                "build a fresh hash table from the current dataset."
            ),
        )
        # setup section layout  
        cfg1, cfg2 = st.columns(2)
        # initial capacity
        with cfg1:
            initial_capacity = st.number_input(
                "Initial Capacity",
                min_value=1,
                value=53,
                step=1,
            )
        # enable auto-resize
        with cfg2:
            enable_resize = st.checkbox("Enable Auto-Resize", value=True)

        max_lf = 0.75 if enable_resize else 0.0
        # render action tip
        render_action_tip(
            "Initial capacity and resize settings apply the next time you load "
            "data or run a guided demo."
        )
        # collision demo info
        if st.session_state["collision_demo_enabled"]:
            st.info(
                "Forced-collision data is ready. Use the dedicated load button "
                "below to keep those keys in the same bucket chain."
            )
        # load section layout
        load_col1, load_col2 = st.columns(2)
        with load_col1:
            if st.button(
                "Bulk Load Dataset into Hash Table",
                key="ht_bulk_load_btn",
                disabled=not _hash_dataset_ready(),
                help=(
                    "Generate a dataset in the Dataset Builder tab first."
                    if not _hash_dataset_ready()
                    else "Build a fresh hash table from the current dataset."
                ),
            ):
                # bulk load dataset into hash table
                records = st.session_state["kv_dataset"]
                if records is not None:
                    hash_table = HashTable(
                        initial_capacity=int(initial_capacity),
                        max_load_factor=max_lf,
                    )
                    # bulk load dataset into hash table
                    for key, value in records:
                        hash_table.insert(key, value)
                    _clear_hash_lab_state()
                    st.session_state["hash_table"] = hash_table
                    _set_feedback(
                        "last_hash_feedback",
                        "success",
                        f"Hash table loaded with {len(hash_table)} items.",
                    )
                    # append history
                    _append_history(
                        "hash_history",
                        f"Loaded a hash table with {len(hash_table)} items.",
                    )
                    st.rerun()
        # load forced-collision demo
        with load_col2:
            # load forced-collision demo
            if st.button(
                "Load Forced-Collision Demo",
                key="ht_collision_demo_load_btn",
                disabled=not (
                    _hash_dataset_ready() and st.session_state["collision_demo_enabled"]
                ),
                help=(
                    "Enable Forced-Collision Hash Demo in Dataset Builder first."
                    if not st.session_state["collision_demo_enabled"]
                    else "Load the current forced-collision dataset without auto-resize."
                ),
            ):
                # load forced-collision demo
                records = st.session_state["kv_dataset"]
                # load forced-collision demo
                if records is not None:
                    demo_capacity = int(st.session_state["collision_demo_capacity"])
                    hash_table = HashTable(initial_capacity=demo_capacity, max_load_factor=0.0)
                    # load forced-collision demo
                    for key, value in records:
                        hash_table.insert(key, value)
                    _clear_hash_lab_state()
                    st.session_state["hash_table"] = hash_table
                    # set feedback
                    _set_feedback(
                        "last_hash_feedback",
                        "success",
                        (
                            f"Forced-collision hash table loaded with {len(hash_table)} items "
                            f"using capacity {demo_capacity}."
                        ),
                    )
                    # append history
                    _append_history(
                        "hash_history",
                        "Loaded the forced-collision hash table demo dataset.",
                    )
                    # rerun
                    st.rerun()
    # hash table state
    ht = st.session_state["hash_table"]
    hash_demo_result = st.session_state["hash_demo_result"]
    # guided demo section
    with st.container(border=True):
        render_section_intro(
            "Guided Demo",
            (
                "Use the guided demos to validate the required behaviors and produce "
                "screenshot-friendly results for insert, search, delete, and collisions."
            ),
        )
        # guided demo section layout
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            st.markdown("**Run Guided Hash Table Demo (100 items)**")
            st.caption(
                "Validates bulk loading, insert, search hits and misses, and delete "
                "behavior using a 100-item sample."
            )
            # run guided hash table demo
            if st.button(
                "Run Guided Hash Table Demo (100 items)",
                key="ht_run_guided_demo_btn",
            ):
                # run guided hash table demo
                demo_records, demo_note = _select_hash_demo_records()
                demo_table, demo_result = run_hash_table_demo(
                    records=demo_records,
                    dataset_size=100,
                    seed=int(st.session_state["dataset_seed"]),
                    initial_capacity=int(initial_capacity),
                    max_load_factor=max_lf,
                )
                # clear hash lab state
                _clear_hash_lab_state()
                st.session_state["hash_table"] = demo_table
                st.session_state["hash_demo_result"] = demo_result
                st.session_state["hash_demo_note"] = demo_note
                _set_feedback(
                    "last_hash_feedback",
                    "success",
                    "Guided hash table demo complete.",
                )
                # append history    
                _append_history(
                    "hash_history",
                    "Ran the guided hash table demo with 100 items.",
                )
                # rerun
                st.rerun()
        # run guided collision demo
        with demo_col2:
            st.markdown("**Run Guided Collision Demo**")
            st.caption(
                "Builds a small table with intentionally colliding keys so you can "
                "see separate chaining create visible bucket chains."
            )
            # run guided collision demo
            if st.button(
                "Run Guided Collision Demo",
                key="ht_run_collision_demo_btn",
            ):
                # run guided collision demo
                demo_capacity = (
                    int(st.session_state["collision_demo_capacity"])
                    if st.session_state["collision_demo_enabled"]
                    else max(int(initial_capacity), 11)
                )
                # run guided collision demo
                demo_bucket = int(st.session_state["collision_demo_target_bucket"])
                demo_table, demo_result = run_hash_table_demo(
                    dataset_size=12,
                    seed=int(st.session_state["dataset_seed"]),
                    initial_capacity=demo_capacity,
                    max_load_factor=0.0,
                    force_collisions=True,
                    collision_target_bucket=demo_bucket,
                )
                # clear hash lab state
                _clear_hash_lab_state()
                st.session_state["hash_table"] = demo_table
                st.session_state["hash_demo_result"] = demo_result
                st.session_state["hash_demo_note"] = (
                    f"Generated 12 colliding keys aimed at bucket {demo_bucket} "
                    f"in a {demo_capacity}-bucket table with auto-resize disabled."
                )
                # set feedback
                _set_feedback(
                    "last_hash_feedback",
                    "success",
                    "Guided collision demo complete.",
                )   
                # append history
                _append_history(
                    "hash_history",
                    "Ran the guided collision demo.",
                )
                # rerun
                st.rerun()

        # hash demo result
        hash_demo_result = st.session_state["hash_demo_result"]
        # hash demo result
        if hash_demo_result is not None:
            # hash demo note
            if st.session_state["hash_demo_note"]:
                st.caption(st.session_state["hash_demo_note"])
            # render validation results
            render_validation_results(
                hash_demo_result.steps,
                hash_demo_result.summary_lines,
                title="Hash Table Demo Results",
            )
            # render guided operation results
            render_guided_operation_results(
                "Hash Table Guided Operation Outputs",
                hash_demo_result.operation_results,
            )

    # hash table state
    ht = st.session_state["hash_table"]
    manual_hash_ready = _hash_table_ready()

    # manual operations
    with st.container(border=True):
        # render section intro
        render_section_intro(
            "Manual Operations",
            (
                "Use the forms below to run your own insert, search, and delete "
                "checks against the active hash table."
            ),
        )
        # render action tip
        render_action_tip(
            "Use the example buttons to prefill a guaranteed hit or miss before "
            "submitting the forms."
        )
        # example key
        example_key = _get_example_hash_key()
        example_col1, example_col2 = st.columns(2)
        # example existing key
        with example_col1:
            # use example existing key
            if st.button(
                "Use Example Existing Key",
                key="ht_use_existing_btn",
                disabled=not manual_hash_ready or example_key is None,
                help=(
                    "Load or generate a hash table first."
                    if not manual_hash_ready
                    else "Populate the search and delete forms with a key that exists."
                ),
            ):
                # use example existing key
                st.session_state["ht_search_key"] = example_key or ""
                st.session_state["ht_del_key"] = example_key or ""
        
        with example_col2:
            # use example missing key
            if st.button(
                "Use Example Missing Key",
                key="ht_use_missing_btn",
                disabled=not manual_hash_ready,
                help=(
                    "Load or generate a hash table first."
                    if not manual_hash_ready
                    else "Populate the search and delete forms with keys that are absent."
                ),
            ):
                # use example missing key
                st.session_state["ht_search_key"] = "missing-hash-key"
                st.session_state["ht_del_key"] = "missing-delete-key"
        # operation columns
        op_col1, op_col2, op_col3 = st.columns(3)
        # insert
        with op_col1:
            # insert form
            with st.form("ht_insert_form"):
                st.markdown("**Insert**")
                ins_key = st.text_input(
                    "Key",
                    key="ht_ins_key",
                    disabled=not manual_hash_ready,
                )
                # insert value
                ins_val = st.text_input(
                    "Value",
                    key="ht_ins_val",
                    disabled=not manual_hash_ready,
                )
                # insert submitted
                insert_submitted = st.form_submit_button(
                    "Insert",
                    key="ht_insert_btn",
                    disabled=not manual_hash_ready,
                )
            # insert submitted
            if insert_submitted:
                # insert key
                if not ins_key:
                    st.session_state["last_hash_operation_result"] = None
                    _set_feedback(
                        "last_hash_feedback",
                        "warning",
                        "Enter a non-empty key before inserting into the hash table.",
                    )
                    _append_history(
                        "hash_history",
                        "Insert blocked because the key field was empty.",
                    )
                # insert value
                else:
                    try:
                        insert_value = int(ins_val) if ins_val.lstrip("-").isdigit() else ins_val
                    except ValueError:
                        insert_value = ins_val
                    # record hash operation result                                                                      
                    _record_hash_operation_result(
                        "insert",
                        # complexity
                        complexity="Avg O(1)",
                        summary=(
                            f"Inserted or updated key '{ins_key}' in the active hash table."
                        ),
                        # input details
                        input_details=[
                            f"key = {ins_key}",
                            f"value = {insert_value!r}",
                        ],
                        # match key
                        match_key=ins_key,
                        op_callable=lambda: st.session_state["hash_table"].insert(
                            ins_key,
                            insert_value,
                        ),
                    )
                    # clear hash demo result
                    st.session_state["hash_demo_result"] = None
                    st.session_state["hash_demo_note"] = ""
                    # set feedback
                    _set_feedback(
                        "last_hash_feedback",
                        "success",
                        f"Hash table insert succeeded: {ins_key} -> {insert_value}",
                    )
                    # append history
                    _append_history(
                        "hash_history",
                        f"Inserted {ins_key} -> {insert_value}.",
                    )
                    # rerun
                    st.rerun()
        # search
        with op_col2:
            # search form
            with st.form("ht_search_form"):
                st.markdown("**Search**")
                # search key
                search_key = st.text_input(
                    "Key to Search",
                    key="ht_search_key",
                    disabled=not manual_hash_ready,
                )
                # search submitted
                search_submitted = st.form_submit_button(
                    "Search",
                    key="ht_search_btn",
                    disabled=not manual_hash_ready,
                )
            # search submitted
            if search_submitted:
                result = _record_hash_operation_result(
                    "search",
                    complexity="Avg O(1)",
                    # summary
                    summary=lambda returned: (
                        f"Lookup returned a stored value for '{search_key}'."
                        if returned is not None
                        else f"Lookup did not find '{search_key}' in the active hash table."
                    ),
                    # input details
                    input_details=[f"key = {search_key}"],
                    match_key=search_key,
                    op_callable=lambda: st.session_state["hash_table"].search(search_key),
                )
                # result is not None
                if result is not None:
                    _set_feedback(
                        "last_hash_feedback",
                        "success",
                        f"Hash table lookup succeeded: {search_key} -> {result}",
                    )
                    _append_history(
                        "hash_history",
                        f"Searched for {search_key} and found {result}.",
                    )
                else:
                    _set_feedback(
                        "last_hash_feedback",
                        "warning",
                        f"Hash table lookup did not find '{search_key}'.",
                    )
                    _append_history(
                        "hash_history",
                        f"Searched for {search_key} and received a miss.",
                    )
        # delete
        with op_col3:
            # delete form
            with st.form("ht_delete_form"):
                st.markdown("**Delete**")
                # delete key
                del_key = st.text_input(
                    "Key to Delete",
                    key="ht_del_key",
                    disabled=not manual_hash_ready,
                )
                # delete submitted
                delete_submitted = st.form_submit_button(
                    "Delete",
                    key="ht_delete_btn",
                    disabled=not manual_hash_ready,
                )
            # delete submitted
            if delete_submitted:
                deleted_value = _record_hash_operation_result(
                    "delete",
                    complexity="Avg O(1)",
                    summary=lambda returned: (
                        f"Removed '{del_key}' from the active hash table."
                        if returned is not None
                        else f"Delete could not find '{del_key}' in the active hash table."
                    ),
                    input_details=[f"key = {del_key}"],
                    match_key=del_key,
                    op_callable=lambda: st.session_state["hash_table"].delete(del_key),
                )
                # deleted value is not None
                if deleted_value is not None:
                    st.session_state["hash_demo_result"] = None
                    st.session_state["hash_demo_note"] = ""
                    # set feedback
                    _set_feedback(
                        "last_hash_feedback",
                        "success",
                        f"Hash table delete succeeded: {del_key} -> {deleted_value}",
                    )   
                    # append history
                    _append_history(
                        "hash_history",
                        f"Deleted {del_key} -> {deleted_value}.",
                    )
                    # rerun
                    st.rerun()
                else:
                    _set_feedback(
                        "last_hash_feedback",
                        "warning",
                        f"Hash table delete could not find '{del_key}'.",
                    )
                    _append_history(
                        "hash_history",
                        f"Attempted to delete {del_key}, but the key was missing.",
                    )
        # render feedback
        _render_feedback("last_hash_feedback")
        hash_operation_result = st.session_state["last_hash_operation_result"]
        # render manual operation result
        if hash_operation_result is not None:
            render_manual_operation_result(hash_operation_result)
        # render operation history
        render_operation_history(
            "Recent Hash Table Actions",
            list(st.session_state["hash_history"]),
            "No hash-table actions yet. Load a table or run a guided demo to begin.",
        )
    # hash table
    ht = st.session_state["hash_table"]
    # hash table state panel
    with st.container(border=True):
        # render section intro
        render_section_intro(
            "Collision / Structure View",
            (
                "Review the current collision summary, then inspect the bucket chains "
                "to see exactly how the active hash table is storing keys."
            ),
        )
        # hash table is not None
        if ht is not None:
            render_hash_table_state_panel(
                ht.get_stats(),
                bool(st.session_state["collision_demo_enabled"]),
            )
            # render action tip
            render_action_tip(
                "Each row below represents one bucket. A chain like (a: 1) -> (b: 2) "
                "means both keys hashed to the same bucket and are stored together."
            )
            # render hash table buckets
            render_hash_table_buckets(ht.get_buckets())
        else:
            render_empty_state_guidance(
                "Hash Table Not Loaded",
                "Generate data in Dataset Builder, then bulk-load the hash table or run a guided demo to inspect collisions.",
            )
    # concept notes
    with st.container(border=True):
        render_section_intro(
            "Concept Notes",
            "Use this section to connect the UI behavior back to the underlying collision strategy.",
        )
        # collision strategy
        with st.expander("Collision Strategy"):
            st.markdown("""
**Separate Chaining** — each bucket stores a linked list (Python list) of
entries. When a new key hashes to an occupied bucket, the entry is appended
to that bucket's chain.

- **Insert:** Compute bucket index, scan chain for existing key (update if
  found), otherwise append.
- **Search:** Compute bucket index, scan chain for matching key.
- **Delete:** Compute bucket index, scan chain, remove matching entry.

This approach is simpler than linear probing because no tombstone logic is
needed for deletions.
""")

# ______________________________________________________________________________
#
# ==============================================================================
# TAB 4 — PRIORITY QUEUE LAB
# ==============================================================================

with tab_pq:
    st.header("Priority Queue Lab")
    render_lab_quick_start(
        "Quick Start",
        [
            "Generate dataset",
            "Choose heap mode and load queue or run guided demo",
            "Try peek, extract, search, or delete",
        ],
    )

    # render status summary
    pq: BinaryHeapPriorityQueue | None = st.session_state["priority_queue"]
    pq_mode = st.session_state["pq_mode"]
    current_mode = pq.mode if pq is not None else pq_mode
    current_validity = pq.is_valid_heap() if pq is not None else None
    # render status summary
    render_lab_status_summary(
        [
            ("Dataset", "Ready" if _priority_dataset_ready() else "Not Ready"),
            (
                "Dataset Size",
                f"{len(st.session_state['priority_items']):,}" if _priority_dataset_ready() else "0",
            ),
            ("Queue", "Loaded" if _priority_queue_ready() else "Not Loaded"),
            ("Heap Mode", current_mode.upper()),
            (
                "Heap Validity",
                "VALID" if current_validity else ("CHECK" if current_validity is not None else "N/A"),
            ),
        ]
    )

    # render setup
    with st.container(border=True):
        # render section intro
        render_section_intro(
            "Setup",
            (
                "Choose which heap mode to demonstrate, then load a fresh queue "
                "from the current dataset or launch the guided demo."
            ),
        )
        # render heap mode radio
        selected_mode = st.radio(
            "Heap Mode",
            options=["max", "min"],
            index=0 if st.session_state["pq_mode"] == "max" else 1,
            horizontal=True,
        )
        # set heap mode
        st.session_state["pq_mode"] = selected_mode
        pq_mode = selected_mode
        st.caption("MAX: highest priority leaves first. MIN: lowest priority leaves first.")
        render_action_tip(
            "The selected mode applies to the next bulk load or guided demo. "
            "The current queue keeps its existing mode until it is rebuilt."
        )
        # render bulk load button
        if st.button(
            "Bulk Load Priority Items",
            key="pq_bulk_load_btn",
            disabled=not _priority_dataset_ready(),
            help=(
                "Generate a dataset in the Dataset Builder tab first."
                if not _priority_dataset_ready()
                else "Build a fresh priority queue from the current dataset."
            ),
        ):
            # get items
            items = st.session_state["priority_items"]
            # if items is not None
            if items is not None:
                # create queue
                queue = BinaryHeapPriorityQueue(mode=pq_mode)
                # insert items
                for item in items:
                    queue.insert(item)
                _clear_priority_lab_state()
                st.session_state["priority_queue"] = queue
                # set feedback
                _set_feedback(
                    "last_priority_feedback",
                    "success",
                    f"Priority queue loaded with {len(queue)} items in {pq_mode.upper()} mode.",
                )
                # append history
                _append_history(
                    "priority_history",
                    f"Loaded a {pq_mode.upper()} priority queue with {len(queue)} items.",
                )
                # rerun
                st.rerun()
    
    # get priority queue
    pq = st.session_state["priority_queue"]
    # render guided demo
    with st.container(border=True):
        # render section intro
        render_section_intro(
            "Guided Demo",
            (
                "Use the guided priority-queue demo to validate insert, peek, search, "
                "delete, and extract behavior on a 100-item sample."
            ),
        )
        # render caption
        st.caption(
            "The guided run validates insert, peek, search, delete, and extract "
            "behavior using the currently selected heap mode."
        )
        # render button
        if st.button(
            "Run Guided Priority Queue Demo (100 items)",
            key="pq_run_guided_demo_btn",
        ):
            # select demo items
            demo_items, demo_note = _select_priority_demo_items()
            # run demo
            demo_queue, demo_result = run_priority_queue_demo(
                items=demo_items,
                dataset_size=100,
                seed=int(st.session_state["dataset_seed"]),
                mode=pq_mode,
            )
            # clear state
            _clear_priority_lab_state()
            # set state
            st.session_state["priority_queue"] = demo_queue
            st.session_state["priority_demo_result"] = demo_result
            st.session_state["priority_demo_note"] = demo_note
            # set feedback
            _set_feedback(
                "last_priority_feedback",
                "success",
                f"Guided priority queue demo complete in {pq_mode.upper()} mode.",
            )
            # append history
            _append_history(
                "priority_history",
                f"Ran the guided priority queue demo in {pq_mode.upper()} mode.",
            )
            # rerun
            st.rerun()

        # get priority demo result
        priority_demo_result = st.session_state["priority_demo_result"]
        # if priority demo result is not None
        if priority_demo_result is not None:
            # if priority demo note is not None
            if st.session_state["priority_demo_note"]:
                # render caption
                st.caption(st.session_state["priority_demo_note"])
            # render validation results
            render_validation_results(
                priority_demo_result.steps,
                priority_demo_result.summary_lines,
                title=f"Priority Queue Demo Results ({priority_demo_result.mode.upper()}-heap)",
            )
            # render guided operation results
            render_guided_operation_results(
                "Priority Queue Guided Operation Outputs",
                priority_demo_result.operation_results,
            )

    # get priority queue
    pq = st.session_state["priority_queue"]
    manual_priority_ready = _priority_queue_ready()

    # render manual operations
    with st.container(border=True):
        # render section intro
        render_section_intro(
            "Manual Operations",
            (
                "Run your own queue operations below. These controls are enabled "
                "once a queue has been loaded or generated through the guided demo."
            ),
        )
        # render action tip
        render_action_tip(
            "Search and delete by label are O(n) operations because heaps optimize "
            "top access, not direct label lookup."
        )

        # get example label
        example_label = pq.to_list()[0].label if pq is not None and not pq.is_empty() else None
        # create columns
        example_col1, example_col2, example_col3 = st.columns(3)
        # with example column 1
        with example_col1:
            # render button
            if st.button(
                "Use Example Label",
                key="pq_use_existing_btn",
                disabled=not manual_priority_ready or example_label is None,
                help=(
                    "Load or generate a queue first."
                    if not manual_priority_ready
                    else "Populate the search/delete field with a label that exists."
                ),
            ):
                st.session_state["pq_search_del"] = example_label or ""
        # with example column 2
        with example_col2:
            # render button
            if st.button(
                "Use Missing Label",
                key="pq_use_missing_btn",
                disabled=not manual_priority_ready,
                help=(
                    "Load or generate a queue first."
                    if not manual_priority_ready
                    else "Populate the search/delete field with a missing label."
                ),
            ):
                st.session_state["pq_search_del"] = "no-such-task"
        # with example column 3
        with example_col3:
            # render button
            if st.button(
                "Insert High-Priority Example",
                key="pq_use_insert_example_btn",
                disabled=not manual_priority_ready,
                help=(
                    "Load or generate a queue first."
                    if not manual_priority_ready
                    else "Populate the insert form with an item that should move to the root."
                ),
            ):
                # get active queue
                active_queue: BinaryHeapPriorityQueue = st.session_state["priority_queue"]
                # build high priority example
                label, priority, payload = _build_high_priority_example(active_queue)
                # set state
                st.session_state["pq_label"] = label
                st.session_state["pq_priority"] = priority
                st.session_state["pq_payload"] = payload

        # create columns
        op1, op2, op3 = st.columns(3)

        # with op1
        with op1:
            # render form
            with st.form("pq_insert_form"):
                # render section intro
                st.markdown("**Insert Item**")
                # render text input
                pq_label = st.text_input(
                    "Label",
                    key="pq_label",
                    disabled=not manual_priority_ready,
                )
                # render number input
                pq_priority = st.number_input(
                    "Priority",
                    value=50,
                    step=1,
                    key="pq_priority",
                    disabled=not manual_priority_ready,
                )
                # render text input
                pq_payload = st.text_input(
                    "Payload",
                    value="",
                    key="pq_payload",
                    disabled=not manual_priority_ready,
                )
                # render submit button
                insert_priority_submitted = st.form_submit_button(
                    "Insert Item",
                    key="pq_insert_btn",
                    disabled=not manual_priority_ready,
                )

            # if insert priority submitted
            if insert_priority_submitted:
                # if label is empty
                if not pq_label:
                    # set last priority operation result to None
                    st.session_state["last_priority_operation_result"] = None
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "warning",
                        "Enter a label before inserting into the priority queue.",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        "Insert blocked because the label field was empty.",
                    )
                else:
                    # get active queue
                    active_queue: BinaryHeapPriorityQueue = st.session_state["priority_queue"]
                    # build new item
                    # build new item
                    new_item = PriorityItem(
                        label=pq_label,
                        priority=int(pq_priority),
                        payload=pq_payload,
                        sequence_number=len(active_queue),
                    )
                    # build input details
                    input_details = [
                        f"label = {pq_label}",
                        f"priority = {int(pq_priority)}",
                        f"mode = {active_queue.mode.upper()}",
                    ]
                    # if payload is not empty
                    if pq_payload:
                        # append payload to input details
                        input_details.append(f"payload = {pq_payload!r}")
                    # record priority operation result
                    _record_priority_operation_result(
                        "insert",
                        complexity="O(log n)",
                        summary=(
                            f"Inserted '{pq_label}' and restored heap order in "
                            f"{active_queue.mode.upper()} mode."
                        ),
                        input_details=input_details,
                        match_label=pq_label,
                        op_callable=lambda: active_queue.insert(new_item),
                    )
                    # clear demo result and note
                    st.session_state["priority_demo_result"] = None
                    st.session_state["priority_demo_note"] = ""
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "success",
                        f"Priority queue insert succeeded: {pq_label} (priority={int(pq_priority)})",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        f"Inserted {pq_label} with priority {int(pq_priority)}.",
                    )
                    # rerun
                    st.rerun()

        # with op2
        with op2:
            # render form
            with st.form("pq_peek_extract_form"):
                # render section intro
                st.markdown("**Peek / Extract**")
                # render peek button
                peek_submitted = st.form_submit_button(
                    "Peek",
                    key="pq_peek_btn",
                    disabled=not manual_priority_ready,
                )
                # render extract button
                extract_submitted = st.form_submit_button(
                    "Extract Top",
                    key="pq_extract_btn",
                    disabled=not manual_priority_ready,
                )

            # if peek submitted
            if peek_submitted:
                # get active queue
                active_queue = st.session_state["priority_queue"]
                # if queue is empty
                if active_queue.is_empty():
                    # record priority operation result
                    _record_priority_operation_result(
                        "peek",
                        complexity="O(1)",
                        summary="Peek could not run because the queue is empty.",
                        input_details=[f"mode = {active_queue.mode.upper()}"],
                        op_callable=lambda: None,
                    )
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "warning",
                        "Priority queue peek is unavailable because the queue is empty.",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        "Attempted to peek, but the queue was empty.",
                    )
                else:
                    # record priority operation result
                    top_item = _record_priority_operation_result(   
                        "peek",
                        complexity="O(1)",
                        summary=(
                            f"Peek inspected the current root in {active_queue.mode.upper()} mode."
                        ),
                        input_details=[f"mode = {active_queue.mode.upper()}"],
                        match_label=active_queue.peek().label,
                        op_callable=lambda: active_queue.peek(),
                    )
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "success",
                        f"Priority queue peek returned {top_item.label} (priority={top_item.priority}).",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        f"Peeked at {top_item.label} with priority {top_item.priority}.",
                    )

            # if extract submitted
            if extract_submitted:
                # get active queue
                active_queue = st.session_state["priority_queue"]
                # if queue is empty
                if active_queue.is_empty():
                    # record priority operation result
                    _record_priority_operation_result(
                        "extract_top",
                        complexity="O(log n)",
                        summary="Extract could not run because the queue is empty.",
                        input_details=[f"mode = {active_queue.mode.upper()}"],
                        op_callable=lambda: None,
                    )
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "warning",
                        "Priority queue extract is unavailable because the queue is empty.",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        "Attempted to extract, but the queue was empty.",
                    )
                else:
                    # record priority operation result
                    extracted_item = _record_priority_operation_result(
                        "extract_top",
                        complexity="O(log n)",
                        summary=(
                            f"Extract removed the root item and restored heap order in "
                            f"{active_queue.mode.upper()} mode."
                        ),
                        input_details=[f"mode = {active_queue.mode.upper()}"],
                        op_callable=lambda: active_queue.extract_top(),
                    )
                    # clear demo result and note
                    st.session_state["priority_demo_result"] = None
                    st.session_state["priority_demo_note"] = ""
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "success",
                        f"Priority queue extracted {extracted_item.label} (priority={extracted_item.priority}).",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        f"Extracted {extracted_item.label} with priority {extracted_item.priority}.",
                    )
                    # rerun
                    st.rerun()

        # with op3
        with op3:
            # render form
            with st.form("pq_search_delete_form"):
                # render section intro
                st.markdown("**Search / Delete**")
                # render search/delete label input
                pq_search_label = st.text_input(
                    "Label to Search/Delete",
                    key="pq_search_del",
                    disabled=not manual_priority_ready,
                )
                # render search/delete submit button
                search_priority_submitted = st.form_submit_button(
                    "Search",
                    key="pq_search_btn",
                    disabled=not manual_priority_ready,
                )
                # render delete submit button
                delete_priority_submitted = st.form_submit_button(
                    "Delete",
                    key="pq_delete_btn",
                    disabled=not manual_priority_ready,
                )

            # if search/delete submitted
            if search_priority_submitted:
                # get active queue
                active_queue = st.session_state["priority_queue"]
                # record priority operation result
                found_item = _record_priority_operation_result(
                    "search",
                    complexity="O(n)",
                    summary=lambda returned: (
                        f"Search found label '{pq_search_label}' in the active heap."
                        if returned is not None
                        else f"Search did not find label '{pq_search_label}'."
                    ),
                    input_details=[
                        f"label = {pq_search_label}",
                        f"mode = {active_queue.mode.upper()}",
                    ],
                    match_label=pq_search_label,
                    op_callable=lambda: active_queue.search(pq_search_label),
                )
                # if found item
                if found_item is not None:
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "success",
                        f"Priority queue search found {found_item.label} (priority={found_item.priority}).",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        f"Searched for {pq_search_label} and found it.",
                    )
                else:
                    # set feedback
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "warning",
                        f"Priority queue search did not find '{pq_search_label}'.",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        f"Searched for {pq_search_label} and received a miss.",
                    )

            # if delete submitted
            if delete_priority_submitted:
                active_queue = st.session_state["priority_queue"]
                removed_item = _record_priority_operation_result(
                    "delete",
                    complexity="O(n) + O(log n)",
                    summary=lambda returned: (
                        f"Delete removed '{pq_search_label}' and restored heap order."
                        if returned is not None
                        else f"Delete could not find label '{pq_search_label}'."
                    ),
                    # input details
                    input_details=[
                        f"label = {pq_search_label}",
                        f"mode = {active_queue.mode.upper()}",
                    ],
                    match_label=pq_search_label,
                    op_callable=lambda: active_queue.delete(pq_search_label),
                )
                # if removed item
                if removed_item is not None:
                    # clear demo result and note
                    st.session_state["priority_demo_result"] = None
                    st.session_state["priority_demo_note"] = ""
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "success",
                        f"Priority queue delete succeeded: {removed_item.label} (priority={removed_item.priority}).",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        f"Deleted {removed_item.label} with priority {removed_item.priority}.",
                    )
                    # rerun
                    st.rerun()
                else:
                    # set feedback
                    _set_feedback(
                        "last_priority_feedback",
                        "warning",
                        f"Priority queue delete could not find '{pq_search_label}'.",
                    )
                    # append history
                    _append_history(
                        "priority_history",
                        f"Attempted to delete {pq_search_label}, but the label was missing.",
                    )

        # render feedback
        _render_feedback("last_priority_feedback")
        # get priority operation result
        priority_operation_result = st.session_state["last_priority_operation_result"]
        # if priority operation result
        if priority_operation_result is not None:
            # render manual operation result
            render_manual_operation_result(priority_operation_result)
        # render operation history
        render_operation_history(
            "Recent Priority Queue Actions",
            list(st.session_state["priority_history"]),
            "No priority-queue actions yet. Load a queue or run a guided demo to begin.",
        )

    # get priority queue
    pq = st.session_state["priority_queue"]
    # render heap view
    with st.container(border=True):
        # render section intro
        render_section_intro(
            "Heap View",
            (
                "Review the current root item, heap validity, and the upcoming "
                "extractions before opening the full heap array."
            ),
        )
        # if priority queue
        if pq is not None:
            # render priority queue state
            render_priority_queue_state(
                pq.to_list(),
                pq.mode,
                heap_valid=pq.is_valid_heap(),
                show_mode_explanation=True,
                extraction_preview=_build_priority_preview(pq),
            )
        else:
            # render empty state guidance
            render_empty_state_guidance(
                "Priority Queue Not Loaded",
                "Generate data in Dataset Builder, then bulk-load the queue or run a guided demo to inspect heap behavior.",
            )

    # render concept notes
    with st.container(border=True):
        # render section intro
        render_section_intro(
            "Concept Notes",
            "These reminders help connect the visible heap behavior back to the queue design.",
        )
        # render concept notes
        st.markdown(
            "- Insert and extract run in O(log n) because the heap only repairs one root-to-leaf path.\n"
            "- Peek runs in O(1) because the highest-priority item stays at the root.\n"
            "- Search and delete by label are O(n) because the heap is not sorted by label."
        )

# ______________________________________________________________________________
#
# ==============================================================================
# TAB 5 — BENCHMARK LAB
# ==============================================================================

with tab_bench:
    st.header("Benchmark Lab")
    st.markdown(
        "Benchmark the required **hash table** and **priority queue** "
        "operations, then compare **hash table search** against the "
        "**linear-search baseline** on the same datasets."
    )
    with st.expander("Benchmark Fairness Rules", expanded=False):
        st.markdown("""
- The dataset is generated once per benchmark size.
- Read-only workloads use autorange-style timing on prebuilt structures.
- Mutating workloads rebuild fresh structures for each repeat.
- The same query list is reused for hash table search and linear search.
- Collision workloads use a fixed-capacity table so duplicate hashes stay visible.
- The assignment suite includes 100 items and larger sizes up to 10,000.
""")

    # --- Benchmark Controls ---
    # render benchmark controls
    ctrl1, ctrl2, ctrl3 = st.columns(3)
    with ctrl1:
        # render preview button
        st.button(
            "Preview [100, 500]",
            key="bench_preview_btn",
            on_click=_set_benchmark_preview_sizes,
        )
        # render dataset sizes
        bench_sizes = st.multiselect(
            "Dataset Sizes",
            options=[100, 500, 1_000, 5_000, 10_000],
            default=list(DEFAULT_SIZES),
            key="benchmark_size_selection",
        )
    # render benchmark modes
    with ctrl2:
        bench_modes = st.multiselect(
            "Query Modes",
            options=["hits", "misses", "mixed"],
            default=list(DEFAULT_QUERY_MODES),
            key="benchmark_query_mode_selection",
        )
    # render benchmark repeats
    with ctrl3:
        bench_repeats = st.number_input(
            "Repeats per timed workload",
            min_value=1,
            max_value=10,
            value=DEFAULT_REPEATS,
            step=1,
            key="benchmark_repeats",
        )

    # render run benchmark button
    run_col1, run_col2 = st.columns(2)
    with run_col1:
        if st.button("Run Benchmark", type="primary"):
            # if not bench sizes or not bench modes
            if not bench_sizes or not bench_modes:
                # render warning
                st.warning("Select at least one size and one query mode.")
            else:
                # render progress
                progress = st.progress(0, text="Starting benchmark...")

                # progress callback
                def _progress_cb(current: int, total: int, label: str) -> None:
                    progress.progress(current / total, text=f"Benchmarking: {label}")

                # run benchmarks
                df = run_benchmarks(
                    sizes=bench_sizes,
                    query_modes=bench_modes,
                    repeats=int(bench_repeats),
                    progress_callback=_progress_cb,
                )
                # store benchmark outputs
                _store_benchmark_outputs(df)
                # empty progress
                progress.empty()
                # render success
                st.success("Benchmark complete. CSV summaries and charts saved.")

    # render run assignment benchmark suite button
    with run_col2:
        if st.button("Run Assignment Benchmark Suite", key="run_assignment_suite_btn"):
            # render progress
            progress = st.progress(0, text="Starting assignment benchmark suite...")

            # progress callback
            def _progress_cb(current: int, total: int, label: str) -> None:
                progress.progress(current / total, text=f"Benchmarking: {label}")

            # run benchmark validation
            validation_result = run_benchmark_validation(
                sizes=[100, 500, 1_000, 5_000, 10_000],
                query_modes=["hits", "misses", "mixed"],
                progress_callback=_progress_cb,
            )
            # store benchmark outputs
            _store_benchmark_outputs(validation_result.benchmark_df)
            # empty progress
            progress.empty()
            # render success
            st.success("Assignment benchmark suite complete. CSV summaries and charts saved.")

    # --- Load Previous ---
    if _CSV_PATH.exists() and st.session_state["benchmark_df"] is None:
        if st.button("Load Previous Results"):
            df = load_results_csv(_CSV_PATH)
            _store_benchmark_outputs(df)

    # --- Display Results ---
    bench_df = st.session_state["benchmark_df"]
    # if benchmark dataframe
    if bench_df is not None and not bench_df.empty:
        # get benchmark validation
        benchmark_validation = st.session_state["benchmark_validation"]
        # if benchmark validation
        if benchmark_validation is not None:
            # render benchmark validation summary
            render_benchmark_validation_summary(benchmark_validation)
            # render benchmark note
            _render_benchmark_note(
                "benchmark validation summary illustrates whether the current "
                "benchmark run covers every required workload and satisfies the "
                "correctness, collision, heap-validity, and hash-faster-than-linear "
                "success checks."
            )

        # get speedup dataframe
        speedup_df = st.session_state["speedup_df"]
        # if speedup dataframe
        if speedup_df is not None:
            # render speedup dataframe
            st.subheader("Search Comparison Summary")
            st.dataframe(speedup_df, hide_index=True)
            # render benchmark note
            _render_benchmark_note(
                "search comparison summary table illustrates how much faster "
                "hash-table lookup is than linear search for each dataset size "
                "and query mode."
            )

            # generate summary sentences
            sentences = generate_summary_sentences(speedup_df)
            # if sentences
            if sentences:
                # render key findings
                st.subheader("Key Findings")
                # for each sentence
                for s in sentences:
                    # render sentence
                    st.markdown(f"- {s}")

            # get chart paths
            search_chart_path = _ANALYSIS_DIR / "charts" / "hash_vs_linear_search.png"
            speedup_chart_path = _ANALYSIS_DIR / "charts" / "search_speedup.png"
            # if search chart path exists
            if search_chart_path.exists():
                # render search chart
                st.image(
                    str(search_chart_path),
                    caption="Hash table search vs linear search",
                )
                # render benchmark note
                _render_benchmark_note(
                    "hash-versus-linear search chart illustrates the raw runtime "
                    "gap between hash-table search and linear search across hit, "
                    "miss, and mixed-query scenarios."
                )
            # if speedup chart path exists
            if speedup_chart_path.exists():
                # render speedup chart
                st.image(
                    str(speedup_chart_path),
                    caption="Hash table speedup over linear search",
                )
                # render benchmark note
                _render_benchmark_note(
                    "search speedup chart illustrates the multiplicative speedup "
                    "provided by hash-table search over linear search; larger values "
                    "mean a bigger hashing advantage."
                )

        # render full benchmark results table
        st.subheader("Full Benchmark Results Table")
        render_benchmark_table(bench_df)
        # render benchmark note
        _render_benchmark_note(
            "full benchmark results table illustrates the raw timing, workload "
            "size, scenario, and correctness results for every benchmarked "
            "hash-table and priority-queue operation."
        )

        # get operation scaling dataframe
        operation_scaling_df = st.session_state["operation_scaling_df"]
        # if operation scaling dataframe
        if operation_scaling_df is not None:
            # render operation scaling table
            st.subheader("Operation Scaling Table")
            st.dataframe(operation_scaling_df, hide_index=True)
            # render benchmark note
            _render_benchmark_note(
                "operation scaling table illustrates how each operation grows "
                "from the smallest to the largest tested size, highlighting "
                "scaling behavior instead of declaring a single winner."
            )

        # render runtime charts
        st.subheader("Runtime Charts")
        render_benchmark_charts(bench_df)

        # render collision diagram
        _render_benchmark_collision_diagram(bench_df)
        # render heap diagram
        _render_benchmark_heap_diagram(bench_df)
    else:
        # render info
        st.info("Run a benchmark or load previous results to see data here.")

# ______________________________________________________________________________
#
# ==============================================================================
# TAB 6 — WRITTEN ANALYSIS
# ==============================================================================

with tab_analysis:
    st.header("Written Analysis")

    # placeholders
    placeholders: dict[str, str] = {}
    # get benchmark dataframe
    bench_df = st.session_state["benchmark_df"]
    # get speedup dataframe
    speedup_df = st.session_state["speedup_df"]
    # get operation scaling dataframe
    operation_scaling_df = st.session_state["operation_scaling_df"]
    # if benchmark dataframe
    if bench_df is None and _CSV_PATH.exists():
        bench_df = load_results_csv(_CSV_PATH)
    # if speedup dataframe
    if speedup_df is None and _SPEEDUP_CSV_PATH.exists():
        speedup_df = load_results_csv(_SPEEDUP_CSV_PATH)
    # if operation scaling dataframe
    if operation_scaling_df is None and _SCALING_CSV_PATH.exists():
        operation_scaling_df = load_results_csv(_SCALING_CSV_PATH)
    # if benchmark dataframe
    if bench_df is not None:
        # build benchmark table
        placeholders["BENCHMARK_RESULTS_TABLE"] = build_benchmark_table(bench_df)
    # if speedup dataframe
    if speedup_df is not None:
        # build speedup summary table
        placeholders["SPEEDUP_SUMMARY_TABLE"] = build_speedup_summary_table(speedup_df)
    # if operation scaling dataframe
    if operation_scaling_df is not None:
        # build operation scaling table
        placeholders["OPERATION_SCALING_TABLE"] = build_operation_scaling_table(
            operation_scaling_df
        )

    # render analysis markdown file
    render_analysis_markdown_file(_WRITTEN_ANALYSIS_PATH, placeholders)

# ______________________________________________________________________________
#
# ==============================================================================
# TAB 7 — RECOMMENDATION GUIDE
# ==============================================================================

with tab_guide:
    st.header("Recommendation Guide")

    # placeholders
    placeholders: dict[str, str] = {}
    # get speedup dataframe
    speedup_df = st.session_state["speedup_df"]
    # if speedup dataframe
    if speedup_df is None and _SPEEDUP_CSV_PATH.exists():
        # load speedup dataframe
        speedup_df = load_results_csv(_SPEEDUP_CSV_PATH)
    # if speedup dataframe
    if speedup_df is not None:
        # build speedup summary table
        placeholders["SPEEDUP_SUMMARY_TABLE"] = build_speedup_summary_table(speedup_df)

    render_analysis_markdown_file(_RECOMMENDATION_GUIDE_PATH, placeholders)

# ==============================================================================
# End of File
# ==============================================================================
