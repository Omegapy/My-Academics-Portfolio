# -------------------------------------------------------------------------
# File: streamlit_helpers.py
#
# Author: Alexander Ricciardi 
# Date: 2026-04-16
# Course: CSC506
# Professor: Dr. Jonathan Vanover 
# Semester: Spring A 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Streamlit helper functions for the Hash Table & Priority Queue Tool.
# Provides reusable UI components: header banner, dataset previews,
# hash-table stats/bucket display, priority-queue state view,
# benchmark tables/charts, and Markdown template rendering.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit UI helpers for the hash table and priority queue tool."""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

import html
import re
from pathlib import Path

try:
    import altair as alt
except ImportError:  # pragma: no cover - fallback path for environments without Altair
    alt = None

import streamlit as st
import pandas as pd

from analysis.lab_validation import (
    BenchmarkValidationResult,
    ValidationStepResult,
)
from models.hash_entry import HashEntry
from models.lab_operation_result import LabOperationResult
from models.hash_table_stats import HashTableStats
from models.priority_item import PriorityItem

# ______________________________________________________________________________
# Global Constants / Variables
# ==============================================================================
# UI CONSTANTS & STYLING
# ==============================================================================
# Color palettes, regex patterns, and label maps used to keep the Streamlit
# UI consistent with the matplotlib charts produced by report_generator.
# Constants mirror chart styling so static and live views stay in sync.
# ------------------------------------------------------------------------------

# Constraint: stable color palette shared with report_generator.METHOD_COLORS.
# Rationale: keeps live Altair charts and saved PNG charts visually consistent.
METHOD_COLORS: dict[str, str] = {
    "Hash Table": "#3498db",
    "Linear Search": "#e74c3c",
}
"""Consistent color palette matching report_generator.py."""

# Markdown template token pattern: lines like "{{PLACEHOLDER}}" trigger
# placeholder substitution inside render_analysis_markdown_file.
_PLACEHOLDER_RE = re.compile(r"^\{\{([A-Z0-9_]+)\}\}$")
# Markdown image pattern: "![alt](path)" lines are promoted to st.image() calls
# when the path resolves to a local file under the markdown's directory.
_IMAGE_MARKDOWN_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)$")

# Constraint: maximum number of snapshot rows shown in the operation card.
# Rationale: keeps the before/after panels compact while preserving context.
_SNAPSHOT_MAX_LINES: int = 8
# Constraint: highlight color applied to the snapshot row impacted by an op.
# Rationale: high-contrast yellow stays readable on the gray code-style block.
_HIGHLIGHT_COLOR: str = "#ffeb3b"

# Friendly group / operation / scenario labels for benchmark tables and charts.
# Group labels
_BENCHMARK_GROUP_LABELS: dict[str, str] = {
    "search_comparison": "Search Comparison",  # Hash vs linear baseline
    "hash_core": "Hash Core",                  # Hash table on normal data
    "hash_collision": "Hash Collision",        # Hash table on collision data
    "priority_queue_core": "Priority Queue Core",  # Priority queue workloads
}
# Operation labels
_BENCHMARK_OPERATION_LABELS: dict[str, str] = {
    "search": "Search",
    "insert_bulk": "Insert",
    "delete_sample": "Delete",
    "search_hits": "Search Hit",
    "search_misses": "Search Miss",
    "collision_insert_bulk": "Collision Insert",
    "collision_search_hits": "Collision Search",
    "collision_delete_sample": "Collision Delete",
    "peek": "Peek",
    "extract_top_drain": "Extract",
}
# Within-group operation order used to keep chart series stable across runs.
# Operation order
_BENCHMARK_OPERATION_ORDER: dict[str, int] = {
    "insert_bulk": 0,
    "collision_insert_bulk": 0,
    "peek": 1,
    "search": 2,
    "search_hits": 2,
    "collision_search_hits": 2,
    "search_misses": 3,
    "delete_sample": 4,
    "collision_delete_sample": 4,
    "extract_top_drain": 5,
}
# Within-group scenario order used to keep chart series stable across runs.
# Scenario order
_BENCHMARK_SCENARIO_ORDER: dict[str, int] = {
    "normal": 0,
    "forced_collision": 0,
    "hits": 0,
    "misses": 1,
    "mixed": 2,
    "max": 0,
    "min": 1,
}

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# HEADER & LAB SHELL
# ==============================================================================
# Top-level layout helpers shared by every tab: page banner, quick-start
# guidance, status summaries, action tips, history blocks, and the manual /
# guided operation result cards.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_header()
def render_header() -> None:
    """Render the application title and course information banner.

    Logic:
        1. Render the page title and course / professor / student caption.
        2. Drop a horizontal divider so tab content has visual separation.
    """
    st.title("Hash Table & Priority Queue Tool")
    st.caption(
        "CSC506 – Design and Analysis of Algorithms | "
        "Professor Dr. Jonathan Vanover | Spring A 2026 | "
        "Student: Alexander Ricciardi"
    )
    st.divider()
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_lab_quick_start()
def render_lab_quick_start(title: str, steps: list[str]) -> None:
    """Render a short guided workflow banner for a lab.

    Logic:
        1. Open a bordered container so the workflow stands apart from controls.
        2. MAIN ITERATION LOOP: enumerate steps starting at 1 and render each as a numbered list item.
    """
    with st.container(border=True):
        st.markdown(f"**{title}**")
        # MAIN ITERATION LOOP: emit "N. step" entries for the workflow
        for index, step in enumerate(steps, start=1):
            st.markdown(f"{index}. {step}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_lab_status_summary()
def render_lab_status_summary(
    items: list[tuple[str, str]],
    *,
    title: str = "Current State",
) -> None:
    """Render a row of compact status metrics.

    Logic:
        1. Render the section title above the metric row.
        2. Allocate one Streamlit column per status item.
        3. Render each (label, value) pair as a column metric.
    """
    st.markdown(f"**{title}**")
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        column.metric(label, value)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_empty_state_guidance()
def render_empty_state_guidance(title: str, message: str) -> None:
    """Render a more actionable empty-state block.

    Logic:
        1. Open a bordered container to draw the user's eye to the guidance.
        2. Render the heading and an info banner with the action hint.
    """
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.info(message)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_section_intro()
def render_section_intro(title: str, body: str) -> None:
    """Render a standard subheader with short context copy.

    Logic:
        1. Render the section title via st.subheader.
        2. Render the supporting body text via st.markdown.
    """
    st.subheader(title)
    st.markdown(body)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_action_tip()
def render_action_tip(message: str) -> None:
    """Render a lightweight tip beneath controls.

    Logic:
        1. Render the message as a "Tip:"-prefixed caption.
    """
    st.caption(f"Tip: {message}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_operation_history()
def render_operation_history(
    title: str,
    entries: list[str],
    empty_message: str,
) -> None:
    """Render a compact history of recent user actions.

    Logic:
        1. Open a bordered container with the section title.
        2. VALIDATION: render the empty-state info banner and bail out when no entries exist.
        3. MAIN ITERATION LOOP: render every entry as a markdown bullet.
    """
    with st.container(border=True):
        st.markdown(f"**{title}**")
        # VALIDATION: empty history surfaces a friendly placeholder
        if not entries:
            st.info(empty_message)
            return
        # MAIN ITERATION LOOP: render every entry as a bullet
        for entry in entries:
            st.markdown(f"- {entry}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _format_operation_value()
def _format_operation_value(value: object | None) -> str:
    """Return a compact display string for a manual operation return value.

    Logic:
        1. DISPATCH on the value type to choose the most readable format.
        2. None / bool / PriorityItem each get a tailored short string.
        3. Lists render up to three items with a "(+N more)" suffix.
        4. Everything else falls back to str(value).
    """
    # DISPATCH: type-specific formatting keeps the metric card readable
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, PriorityItem):
        return f"{value.label} (priority={value.priority})"
    if isinstance(value, list):
        if not value:
            return "[]"
        preview = ", ".join(str(item) for item in value[:3])
        if len(value) > 3:
            preview += f", ... (+{len(value) - 3})"
        return f"[{preview}]"
    return str(value)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _select_snapshot_indices()
def _select_snapshot_indices(
    line_count: int,
    highlight_idx: int | None,
    count: int,
) -> list[int]:
    """Choose which snapshot rows to display while keeping highlights visible.

    Logic:
        1. SAFETY CHECK: when the snapshot is short, return every index.
        2. When no highlight (or it lies inside the head window), return the head window.
        3. Otherwise reserve a head window plus a tail window centered on the highlight.
        4. Adjust the tail window to fit when it would overflow the snapshot.
    """
    # SAFETY CHECK: the whole snapshot fits without truncation
    if line_count <= count:
        return list(range(line_count))

    # highlight inside the head window — show the head only
    if highlight_idx is None or highlight_idx < count:
        return list(range(count))

    # reserve room for a head + tail window
    head_size = max(3, count // 3)
    tail_size = count - head_size
    half = tail_size // 2
    tail_start = max(head_size, highlight_idx - half)
    tail_end = min(line_count, tail_start + tail_size)
    # clamp the tail window when it would overflow
    if tail_end - tail_start < tail_size:
        tail_start = max(head_size, line_count - tail_size)
        tail_end = line_count

    return list(range(head_size)) + list(range(tail_start, tail_end))
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_snapshot_lines()
def _render_snapshot_lines(
    lines: list[str],
    highlight_idx: int | None,
    *,
    context_idx: int | None = None,
    count: int = _SNAPSHOT_MAX_LINES,
) -> None:
    """Render snapshot rows with an optional highlighted line.

    Logic:
        1. VALIDATION: render an "(empty)" caption when no lines were captured.
        2. SAFETY CHECK: clamp out-of-range highlight / context indices to None.
        3. Pick which row indices to display via _select_snapshot_indices.
        4. MAIN ITERATION LOOP: emit each row, inserting "..." between gaps and
           wrapping the highlighted row in an inline-styled span.
        5. Append a trailing "..." marker when the tail of the snapshot is hidden.
        6. Wrap the rendered rows in a code-style div via st.markdown.
    """
    # VALIDATION: render a tiny placeholder when no snapshot is available
    if not lines:
        st.caption("(empty)")
        return

    line_count = len(lines)
    # SAFETY CHECK: out-of-range highlight / context indices collapse to None
    if highlight_idx is not None and not (0 <= highlight_idx < line_count):
        highlight_idx = None
    if context_idx is not None and not (0 <= context_idx < line_count):
        context_idx = None

    focus_idx = highlight_idx if highlight_idx is not None else context_idx
    indices = _select_snapshot_indices(line_count, focus_idx, count)

    rendered_rows: list[str] = []
    # MAIN ITERATION LOOP: render each chosen row with ellipsis breaks
    for position, row_index in enumerate(indices):
        # Insert an ellipsis whenever the visible window jumps over hidden rows
        if position > 0 and row_index - indices[position - 1] > 1:
            rendered_rows.append(html.escape("..."))
        escaped_line = html.escape(lines[row_index])
        # Highlight the row if it is the one that was highlighted
        if highlight_idx is not None and row_index == highlight_idx:
            rendered_rows.append(
                "<span style='background:"
                f"{_HIGHLIGHT_COLOR};color:#000;padding:0 6px;border-radius:3px;"
                "font-weight:600;display:block;'>"
                f"{escaped_line}</span>"
            )
        else:
            rendered_rows.append(escaped_line)

    # trailing ellipsis when the tail of the snapshot is hidden
    if indices and indices[-1] < line_count - 1:
        rendered_rows.append(html.escape("..."))
    # Join the rendered rows with <br> tags to create a block of text
    body = "<br>".join(rendered_rows)
    # Render the block of text in a code-style div
    st.markdown(
        "<div style='font-family:ui-monospace,SFMono-Regular,Menlo,monospace;"
        "background:#f5f5f5;color:#1f2328;padding:8px 10px;border-radius:4px;"
        "border:1px solid #e0e0e0;font-size:0.9rem;line-height:1.7;"
        "white-space:pre-wrap;'>"
        f"{body}"
        "</div>",
        unsafe_allow_html=True,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_manual_operation_result()
def render_manual_operation_result(result: LabOperationResult) -> None:
    """Render the last manual lab operation in a CTA-5 result card.

    Logic:
        1. Delegate to render_lab_operation_result with a "Last Manual..." heading.
    """
    render_lab_operation_result(
        result,
        heading=f"Last Manual Operation Output - {result.structure}.{result.operation}",
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_lab_operation_result()
def render_lab_operation_result(
    result: LabOperationResult,
    *,
    heading: str,
) -> None:
    """Render a CTA-5 operation result card with a custom heading.

    Logic:
        1. Open a bordered container with the supplied heading.
        2. Render the four headline metrics: Returned, Size, Time, Big-O.
        3. Render the summary line and any input-detail captions.
        4. Compute optional context indices so the before/after panels stay aligned.
        5. Render the before/after snapshot panels side by side.
    """
    with st.container(border=True):
        st.markdown(f"**{heading}**")

        # Step 2: four headline metrics rendered as a metric row
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        metric_col1.metric("Returned", _format_operation_value(result.returned_value))
        metric_col2.metric("Size", f"{result.size_before:,} -> {result.size_after:,}")
        metric_col3.metric("Time", f"{result.elapsed_time * 1_000:.4f} ms")
        metric_col4.metric("Big-O", result.complexity)

        # Step 3: summary + optional input details captions
        st.caption(result.summary)
        if result.input_details:
            st.caption(" | ".join(result.input_details))

        # Step 4: align before/after panels via context-index fallbacks
        before_idx = result.state_before_highlight_idx
        after_idx = result.state_after_highlight_idx
        before_context: int | None = None
        after_context: int | None = None
        # If one index is missing, try to infer it from the other
        if before_idx is not None and after_idx is None and result.state_after:
            after_context = min(before_idx, len(result.state_after) - 1)
        elif after_idx is not None and before_idx is None and result.state_before:
            before_context = min(after_idx, len(result.state_before) - 1)

        # side-by-side before/after snapshot columns
        state_col1, state_col2 = st.columns(2)
        # Render the before snapshot
        with state_col1:
            st.markdown(f"**{result.state_label} before:**")
            _render_snapshot_lines(
                result.state_before,
                before_idx,
                context_idx=before_context,
            )
        # Render the after snapshot
        with state_col2:
            st.markdown(f"**{result.state_label} after:**")
            _render_snapshot_lines(
                result.state_after,
                after_idx,
                context_idx=after_context,
            )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_guided_operation_results()
def render_guided_operation_results(
    title: str,
    operation_results: list[tuple[str, LabOperationResult]],
) -> None:
    """Render guided demo operation outputs beneath the validation table.

    Logic:
        1. Render the section title via st.subheader.
        2. VALIDATION: render an info banner and bail out when no results are present.
        3. MAIN ITERATION LOOP: render each result as a "Guided Operation Output" card.
    """
    st.subheader(title)
    # VALIDATION: friendly placeholder when no guided runs have happened
    if not operation_results:
        st.info("No guided operation outputs are available yet.")
        return

    # MAIN ITERATION LOOP: one card per (step_name, result) pair
    for step_name, result in operation_results:
        render_lab_operation_result(
            result,
            heading=f"Guided Operation Output - {step_name}",
        )
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# DATASET DISPLAY
# ==============================================================================
# Side-by-side previews of the key-value and priority datasets shown in the
# Dataset Builder tab.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_dataset_info()
def render_dataset_info(
    records: list[tuple[str, int]] | None,
    items: list[PriorityItem] | None,
) -> None:
    """Display previews of both the key-value and priority datasets.

    Logic:
        1. Split the row into two columns (one per dataset family).
        2. DISPATCH per column: render a metric + 10-row preview when data
           exists; otherwise render an info placeholder.
        3. Append a "Showing 10 of N" caption when the dataset is larger than the preview.
    """
    col1, col2 = st.columns(2)

    # DISPATCH: column 1 holds the key-value dataset preview
    with col1:
        st.markdown("**Key-Value Dataset**")
        if records:
            st.metric("Records", f"{len(records):,}")
            preview = records[:10]
            df = pd.DataFrame(preview, columns=["Key", "Value"])
            st.dataframe(df, hide_index=True, height=250)
            if len(records) > 10:
                st.caption(f"Showing 10 of {len(records):,} records")
        else:
            st.info("No dataset generated yet.")

    # DISPATCH: column 2 holds the priority items preview
    with col2:
        st.markdown("**Priority Items**")
        if items:
            st.metric("Items", f"{len(items):,}")
            preview = items[:10]
            df = pd.DataFrame([
                {"Label": it.label, "Priority": it.priority, "Seq": it.sequence_number}
                for it in preview
            ])
            st.dataframe(df, hide_index=True, height=250)
            if len(items) > 10:
                st.caption(f"Showing 10 of {len(items):,} items")
        else:
            st.info("No priority items generated yet.")
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# HASH TABLE DISPLAY
# ==============================================================================
# Stats panel, bucket inspector, and collision-chain diagram used by the
# Search Lab and Hash Table tabs.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_hash_table_stats()
def render_hash_table_stats(stats: HashTableStats) -> None:
    """Render hash table statistics as metric cards.

    Logic:
        1. Render the four primary metrics (size, capacity, load, collisions).
        2. Render the four secondary metrics (used / empty / collision buckets, longest chain).
    """
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Size", f"{stats.size:,}")
    c2.metric("Capacity", f"{stats.capacity:,}")
    c3.metric("Load Factor", f"{stats.load_factor:.4f}")
    c4.metric("Total Collisions", f"{stats.total_collisions:,}")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Used Buckets", f"{stats.used_buckets:,}")
    c6.metric("Empty Buckets", f"{stats.empty_buckets:,}")
    c7.metric("Collision Buckets", f"{stats.collision_buckets:,}")
    c8.metric("Longest Chain", f"{stats.longest_bucket_length:,}")
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_hash_table_state_panel()
def render_hash_table_state_panel(
    stats: HashTableStats,
    collision_demo_enabled: bool,
) -> None:
    """Render hash-table metrics plus a short interpretation line.

    Logic:
        1. Render the metric grid via render_hash_table_stats.
        2. DISPATCH on collision-demo flag and chain length to choose a tailored
           interpretation caption that matches the table's current state.
        3. Render the chosen caption below the metrics.
    """
    render_hash_table_stats(stats)

    # DISPATCH: caption depends on demo mode and current chain depth
    if collision_demo_enabled:
        summary = (
            "Collision demo mode is active, so a higher collision count is "
            "expected and useful for teaching separate chaining."
        )
    elif stats.total_collisions == 0:
        summary = (
            "No collisions are visible yet; the current keys are distributing "
            "cleanly across the table."
        )
    elif stats.longest_bucket_length <= 2:
        summary = (
            "A small number of collisions is present, but bucket chains remain "
            "short and healthy."
        )
    else:
        summary = (
            "Collisions are visible in the current table state. Inspect the "
            "bucket chains below to see how separate chaining resolves them."
        )
    st.caption(summary)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_hash_table_buckets()
def render_hash_table_buckets(buckets: list[list[HashEntry]]) -> None:
    """Render the bucket contents as an expandable table.

    Logic:
        1. Open an "Bucket Contents" expander (collapsed by default).
        2. MAIN ITERATION LOOP: build one row per bucket showing length and chain text.
        3. Render the assembled rows as a Streamlit DataFrame.
    """
    with st.expander("Bucket Contents", expanded=False):
        rows = []
        # MAIN ITERATION LOOP: one row per bucket with chain summary
        for i, bucket in enumerate(buckets):
            if bucket:
                chain_str = " -> ".join(f"({e.key}: {e.value})" for e in bucket)
                rows.append({"Bucket": i, "Length": len(bucket), "Chain": chain_str})
            else:
                rows.append({"Bucket": i, "Length": 0, "Chain": "(empty)"})
        df = pd.DataFrame(rows)
        st.dataframe(df, hide_index=True, height=400)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _truncate_diagram_text()
def _truncate_diagram_text(text: str, *, max_length: int) -> str:
    """Return a shortened label for compact diagram nodes.

    Logic:
        1. SAFETY CHECK: return *text* unchanged when it already fits.
        2. Otherwise return *text* truncated to ``max_length - 3`` chars + "...".
    """
    # SAFETY CHECK: short text needs no truncation
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 3]}..."
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _render_hash_bucket_map()
def _render_hash_bucket_map(
    buckets: list[list[HashEntry]],
    *,
    focus_bucket_index: int,
) -> None:
    """Render a compact occupancy map for all hash-table buckets.

    Logic:
        1. MAIN ITERATION LOOP: build one styled "card" per bucket.
        2. DISPATCH on bucket role: focused / occupied / empty -> color palette.
        3. Render the card row inside a flex-wrap container via st.markdown.
    """
    cells: list[str] = []
    # MAIN ITERATION LOOP: one card per bucket (focus / occupied / empty palette)
    for bucket_index, bucket in enumerate(buckets):
        bucket_size = len(bucket)
        # DISPATCH: pick a color palette by bucket role
        if bucket_index == focus_bucket_index:
            background = "#dbeafe"
            border = "#2563eb"
            text_color = "#1d4ed8"
        elif bucket_size > 0:
            background = "#eff6ff"
            border = "#93c5fd"
            text_color = "#1e3a8a"
        else:
            background = "#f8fafc"
            border = "#cbd5e1"
            text_color = "#64748b"

        cells.append(
            "<div style='width:64px;padding:8px 6px;border-radius:8px;"
            f"border:1px solid {border};background:{background};text-align:center;'>"
            f"<div style='font-size:0.75rem;color:{text_color};'>bucket[{bucket_index}]</div>"
            f"<div style='font-size:1rem;font-weight:700;color:{text_color};'>{bucket_size}</div>"
            "</div>"
        )

    st.markdown("**Bucket Occupancy Map**")
    st.markdown(
        "<div style='display:flex;flex-wrap:wrap;gap:8px;align-items:stretch;'>"
        + "".join(cells)
        + "</div>",
        unsafe_allow_html=True,
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_hash_collision_chain_diagram()
def render_hash_collision_chain_diagram(
    buckets: list[list[HashEntry]],
    *,
    max_visible_nodes: int = 7,
) -> None:
    """Render a readable collision-chain diagram for the densest bucket.

    Logic:
        1. VALIDATION: bail out with an info banner when every bucket is empty.
        2. Pick the densest bucket (longest chain, lowest index on ties).
        3. Render the bucket-occupancy map highlighting the focus bucket.
        4. Build a head-then-tail preview when the chain exceeds *max_visible_nodes*.
        5. MAIN ITERATION LOOP: emit the bucket header node followed by chain entry nodes.
        6. Render the chain row and a caption noting the chain length.
    """
    # Filter out empty buckets
    non_empty_buckets = [
        (bucket_index, bucket)
        for bucket_index, bucket in enumerate(buckets)
        if bucket
    ]
    # VALIDATION: nothing to draw when every bucket is empty
    if not non_empty_buckets:
        st.info("No bucket chains are available to draw.")
        return

    # pick the densest bucket (ties broken by lowest index)
    focus_bucket_index, focus_bucket = max(
        non_empty_buckets,
        key=lambda item: (len(item[1]), -item[0]),
    )
    # Render the bucket-occupancy map highlighting the focus bucket
    _render_hash_bucket_map(buckets, focus_bucket_index=focus_bucket_index)

    st.markdown("**Longest Collision Chain**")
    # head + tail preview when the chain is long
    preview_entries: list[HashEntry | None]
    if len(focus_bucket) <= max_visible_nodes:
        preview_entries = list(focus_bucket)
        hidden_count = 0
    else:
        head_count = max(3, max_visible_nodes - 2)
        tail_count = 2
        preview_entries = list(focus_bucket[:head_count]) + [None] + list(focus_bucket[-tail_count:])
        hidden_count = len(focus_bucket) - head_count - tail_count

    # Build the chain nodes
    chain_nodes: list[str] = [
        "<div style='padding:10px 12px;border-radius:8px;border:1px solid #1d4ed8;"
        "background:#1d4ed8;color:#ffffff;font-weight:700;'>"
        f"bucket[{focus_bucket_index}]"
        "</div>"
    ]
    # Render the arrow node
    arrow_node = (
        "<div style='padding:0 2px;color:#475569;font-weight:700;font-size:1.1rem;'>"
        "-&gt;"
        "</div>"
    )
    # MAIN ITERATION LOOP: render each chain entry (None = "+N more" placeholder)
    for entry in preview_entries:
        chain_nodes.append(arrow_node)
        if entry is None:
            chain_nodes.append(
                "<div style='padding:10px 12px;border-radius:8px;border:1px dashed #94a3b8;"
                "background:#f8fafc;color:#475569;font-weight:600;'>"
                f"... (+{hidden_count} more)"
                "</div>"
            )
            continue
        # Truncate the key and value to prevent them from being too long
        key_text = html.escape(_truncate_diagram_text(str(entry.key), max_length=18))
        value_text = html.escape(
            _truncate_diagram_text(str(entry.value), max_length=12)
        )
        # Render the chain entry
        chain_nodes.append(
            "<div style='min-width:120px;padding:10px 12px;border-radius:8px;"
            "border:1px solid #93c5fd;background:#eff6ff;color:#0f172a;'>"
            f"<div style='font-weight:700;color:#1e3a8a;'>{key_text}</div>"
            f"<div style='font-size:0.8rem;color:#475569;'>value={value_text}</div>"
            "</div>"
        )
    # Render the chain row and a caption noting the chain length
    st.markdown(
        "<div style='display:flex;flex-wrap:wrap;gap:8px;align-items:center;"
        "padding:10px 0;'>"
        + "".join(chain_nodes)
        + "</div>",
        unsafe_allow_html=True,
    )
    # Render a caption noting the chain length
    st.caption(
        f"bucket[{focus_bucket_index}] is the longest chain in this benchmark "
        f"snapshot with {len(focus_bucket):,} entries."
    )
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# PRIORITY QUEUE DISPLAY
# ==============================================================================
# Heap state metrics, expandable heap-array table, and a tree-style diagram
# of the binary heap rendered for the Priority Queue tab.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_priority_queue_state()
def render_priority_queue_state(
    heap_list: list[PriorityItem],
    mode: str,
    *,
    heap_valid: bool | None = None,
    show_mode_explanation: bool = False,
    extraction_preview: list[str] | None = None,
) -> None:
    """Render priority queue metrics and heap array.

    Logic:
        1. Pick the top-of-heap label / priority (or N/A when empty).
        2. Render a five-metric row: size, mode, top label, top priority, validity.
        3. DISPATCH on *mode* to render an optional explanation caption.
        4. Render an optional "Next Extractions" preview list.
        5. Render the full heap array inside a collapsed expander.
    """
    # Pick the top-of-heap label / priority (or N/A when empty)
    top_label = heap_list[0].label if heap_list else "N/A"
    top_priority = str(heap_list[0].priority) if heap_list else "N/A"
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Size", f"{len(heap_list):,}")
    c2.metric("Mode", mode.upper())
    c3.metric("Current Top Item", top_label)
    c4.metric("Top Priority", top_priority)
    # Render the heap validity metric
    if heap_valid is None:
        c5.metric("Heap Validity", "N/A")
    else:
        c5.metric("Heap Validity", "VALID" if heap_valid else "CHECK")

    # DISPATCH: optional caption explains the heap orientation
    if show_mode_explanation:
        if mode == "max":
            st.caption("MAX heap mode: the highest priority item leaves the queue first.")
        else:
            st.caption("MIN heap mode: the lowest priority item leaves the queue first.")

    # optional upcoming-extractions preview
    if extraction_preview:
        st.markdown("**Next Extractions**")
        for item in extraction_preview:
            st.markdown(f"- {item}")

    # full heap array in a collapsed expander
    if heap_list:
        with st.expander("Heap Array", expanded=False):
            # Build the heap array
            rows = [
                {
                    "Index": i,
                    "Label": it.label,
                    "Priority": it.priority,
                    "Seq": it.sequence_number,
                }
                for i, it in enumerate(heap_list)
            ]
            # Render the heap array
            df = pd.DataFrame(rows)
            st.dataframe(df, hide_index=True, height=400)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_priority_queue_tree_diagram()
def render_priority_queue_tree_diagram(
    heap_list: list[PriorityItem],
    mode: str,
    *,
    max_levels: int = 4,
) -> None:
    """Render a compact tree-style view of the binary heap.

    Logic:
        1. VALIDATION: bail out with an info banner when the heap is empty.
        2. Compute the visible node count = min(len(heap), 2**max_levels - 1).
        3. DISPATCH on *mode* to choose a heap-mode color palette and label.
        4. MAIN ITERATION LOOP: build one row per heap level with sized node cards.
        5. Wrap the rendered rows in a centered container and emit the markdown.
        6. Note any nodes hidden below the visible level cap.
    """
    # VALIDATION: nothing to draw when the heap is empty
    if not heap_list:
        st.info("No heap nodes are available to draw.")
        return

    visible_count = min(len(heap_list), (2 ** max_levels) - 1)
    # DISPATCH: heap-mode palette keeps max-heap and min-heap views distinguishable
    accent_color = "#0f766e" if mode == "max" else "#7c3aed"
    node_background = "#ecfeff" if mode == "max" else "#f5f3ff"
    node_border = "#99f6e4" if mode == "max" else "#c4b5fd"
    node_label = "Highest priority first" if mode == "max" else "Lowest priority first"
    # Render the heap tree diagram
    st.markdown("**Heap Tree Diagram**")
    st.caption(
        f"{mode.upper()}-heap view. Parent nodes must outrank their children. "
        f"Showing the top {visible_count:,} nodes arranged by heap level."
    )
    # Build the heap tree diagram
    rows_html: list[str] = []
    # MAIN ITERATION LOOP: one row per heap level
    for level in range(max_levels):
        start = (2 ** level) - 1
        # Skip levels beyond the visible count
        if start >= visible_count:
            break
        end = min((2 ** (level + 1)) - 1, visible_count)
        row_gap = max(12, 60 - (level * 10))
        node_cards: list[str] = []
        # Build the node cards
        for index in range(start, end):
            item = heap_list[index]
            label_text = html.escape(
                _truncate_diagram_text(str(item.label), max_length=18)
            )
            # Render the node cards
            node_cards.append(
                "<div style='min-width:128px;max-width:140px;padding:10px 12px;"
                f"border-radius:10px;border:1px solid {node_border};"
                f"background:{node_background};text-align:center;'>"
                f"<div style='font-size:0.72rem;color:{accent_color};font-weight:700;'>"
                f"idx {index}"
                "</div>"
                f"<div style='font-weight:700;color:#0f172a;'>{label_text}</div>"
                f"<div style='font-size:0.8rem;color:#475569;'>priority={item.priority}</div>"
                f"<div style='font-size:0.75rem;color:#64748b;'>seq={item.sequence_number}</div>"
                "</div>"
            )
        # Render the heap tree diagram
        rows_html.append(
            "<div style='display:flex;justify-content:center;align-items:center;"
            f"gap:{row_gap}px;margin:10px 0 0 0;'>"
            + "".join(node_cards)
            + "</div>"
        )
    # Render the heap tree diagram
    st.markdown(
        "<div style='padding:12px 0 4px 0;'>"
        f"<div style='text-align:center;font-size:0.8rem;color:{accent_color};"
        "font-weight:700;margin-bottom:8px;'>"
        f"{node_label}"
        "</div>"
        + "".join(rows_html)
        + "</div>",
        unsafe_allow_html=True,
    )

    # note any hidden nodes below the visible level cap
    hidden_count = len(heap_list) - visible_count
    if hidden_count > 0:
        st.caption(
            f"{hidden_count:,} additional heap nodes are hidden below the top "
            f"{max_levels} levels. Open the Heap Array for the full structure."
        )
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# BENCHMARK DISPLAY
# ==============================================================================
# Benchmark table rendering, live Altair charts (with PNG fallback), label
# helpers used by the chart encodings, and validation summary panels.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_benchmark_table()
def render_benchmark_table(df: pd.DataFrame) -> None:
    """Render benchmark results as a formatted, scrollable table.

    Logic:
        1. Copy *df* and stable-sort by the canonical display order.
        2. Map operation_group codes to friendly group labels.
        3. Convert boolean columns to Yes / No / "-" for human reading.
        4. Title-case underscore-separated column names.
        5. Render the formatted DataFrame in a scrollable Streamlit table.
    """
    display = df.copy()
    display = display.sort_values(
        by=["operation_group", "scenario", "structure", "operation", "size"],
        kind="stable",
    )
    # map operation_group codes to friendly group labels
    if "operation_group" in display.columns:
        display["operation_group"] = display["operation_group"].map(
            lambda value: _BENCHMARK_GROUP_LABELS.get(str(value), str(value))
        )
    # boolean columns rendered as Yes / No / "-"
    for column in ("is_correct", "heap_valid_after"):
        if column in display.columns:
            display[column] = display[column].map(
                lambda value: "Yes"
                if value is True else "No" if value is False else "-"
            )
    # title-case underscore-separated column names
    display.columns = [c.replace("_", " ").title() for c in display.columns]
    st.dataframe(display, hide_index=True, height=400)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_benchmark_charts()
def render_benchmark_charts(df: pd.DataFrame) -> None:
    """Render live runtime charts with a saved-PNG fallback.

    Logic:
        1. SAFETY CHECK: when Altair is missing, df is empty, or required columns
           are absent, fall back to the saved PNG (or an info placeholder).
        2. Annotate the DataFrame with chart-friendly label and sort columns.
        3. Render the "Runtime by Size" line chart faceted by operation group.
        4. Slice the largest-size subset and render the bar comparison chart.
    """
    charts_dir = Path(__file__).resolve().parent.parent / "analysis" / "charts"
    required_columns = {"operation_group", "structure", "operation", "scenario", "size", "time_ms"}

    # SAFETY CHECK: gracefully fall back to saved PNG when live charts can't be drawn
    if alt is None or df.empty or not required_columns.issubset(df.columns):
        path = charts_dir / "benchmark_operation_runtime.png"
        if path.exists():
            st.image(str(path), caption="Saved runtime overview")
        else:
            st.info("Runtime charts are not available yet.")
        return

    # build chart-friendly label / sort columns once for both charts
    plot_df = df.copy()
    # map operation_group codes to friendly group labels
    plot_df["operation_group_label"] = plot_df["operation_group"].map(
        lambda value: _BENCHMARK_GROUP_LABELS.get(str(value), str(value))
    )
    # build series labels
    plot_df["series_short_label"] = plot_df.apply(
        _build_benchmark_series_short_label,
        axis=1,
    )
    # build series labels
    plot_df["series_axis_label"] = plot_df.apply(
        _build_benchmark_series_axis_label,
        axis=1,
    )
    # build series labels   
    plot_df["series_long_label"] = plot_df.apply(
        _build_benchmark_series_long_label,
        axis=1,
    )
    # build series sort
    plot_df["series_sort"] = plot_df.apply(_build_benchmark_series_sort_value, axis=1)
    benchmarked_sizes = sorted(int(size) for size in plot_df["size"].unique().tolist())
    workload_legend = alt.Legend(
        title="Workload",
        orient="bottom",
        direction="horizontal",
        columns=4,
        labelLimit=180,
        titleLimit=220,
        symbolSize=110,
    )

    # faceted line chart of runtime vs dataset size
    st.markdown("**Runtime by Size**")
    # line chart
    line_chart = (
        alt.Chart(plot_df)
        .mark_line(point=True)
        .encode(
            # x-axis
            x=alt.X(
                "size:Q",
                title="Dataset Size",
                axis=alt.Axis(values=benchmarked_sizes, format=","),
            ),
            # y-axis
            y=alt.Y("time_ms:Q", title="Time (ms)"),
            color=alt.Color(
                "series_short_label:N",
                title="Workload",
                sort=alt.EncodingSortField(
                    field="series_sort",
                    op="min",
                    order="ascending",
                ),
                legend=workload_legend,
            ),
            # tooltip
            tooltip=[
                "operation_group_label",
                alt.Tooltip("series_long_label:N", title="Workload"),
                "size",
                alt.Tooltip("time_ms:Q", format=".4f"),
                "complexity",
            ],
        )
        # properties
        .properties(height=300, width=260)
        .facet(
            facet=alt.Facet("operation_group_label:N", title="Operation Group"),
            columns=2,
        )
        .resolve_scale(y="independent")
    )
    # render the line chart
    st.altair_chart(line_chart, width="stretch")
    st.caption(
        "Note: The runtime-by-size chart illustrates how each benchmark workload "
        "changes as dataset size grows, so you can compare scaling trends within "
        "each operation group."
    )

    # largest-size bar chart for at-a-glance "where is the cost?" comparison
    largest_size = int(plot_df["size"].max())
    largest_df = plot_df[plot_df["size"] == largest_size].copy()
    if largest_df.empty:
        return
    # facet height
    facet_height = max(
        220,
        28 * int(largest_df.groupby("operation_group_label").size().max()),
    )
    # bar chart
    st.markdown(f"**Largest-Size Comparison (n = {largest_size:,})**")
    bar_chart = (
        alt.Chart(largest_df)
        .mark_bar()
        .encode(
            # x-axis
            x=alt.X("time_ms:Q", title="Time (ms)"),
            # y-axis
            y=alt.Y(
                "series_axis_label:N",
                title=None,
                sort=alt.EncodingSortField(
                    field="series_sort",
                    op="min",
                    order="ascending",
                ),
                axis=alt.Axis(labelLimit=220, labelLineHeight=16),
            ),
            # color
            color=alt.Color(
                "series_short_label:N",
                sort=alt.EncodingSortField(
                    field="series_sort",
                    op="min",
                    order="ascending",
                ),
                legend=None,
            ),
            # tooltip
            tooltip=[
                "operation_group_label",
                alt.Tooltip("series_long_label:N", title="Workload"),
                alt.Tooltip("time_ms:Q", format=".4f"),
                "complexity",
            ],
        )
        # properties
        .properties(height=facet_height, width=260)
        # facet
        .facet(
            facet=alt.Facet("operation_group_label:N", title=None),
            columns=2,
        )
        .resolve_scale(x="independent", y="independent")
    )
    # render the bar chart
    st.altair_chart(bar_chart, width="stretch")
    st.caption(
        "Note: The largest-size comparison chart illustrates the relative cost of "
        "each workload at the largest selected dataset size, making the most "
        "expensive operations easy to spot."
    )
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_benchmark_series_short_label()
def _build_benchmark_series_short_label(row: pd.Series) -> str:
    """Return a compact legend label for a benchmark workload row.

    Logic:
        1. Pull structure / operation / scenario / group out of *row*.
        2. Look up the friendly operation label (fall back to title-case).
        3. DISPATCH on operation_group to pick a group-specific label format.
    """
    # pull structure / operation / scenario / group out of *row*
    structure = str(row["structure"])
    operation = str(row["operation"])
    scenario = str(row["scenario"])
    group = str(row["operation_group"])
    # look up the friendly operation label (fall back to title-case)
    operation_label = _BENCHMARK_OPERATION_LABELS.get(
        operation,
        operation.replace("_", " ").title(),
    )

    # DISPATCH: each group has its own legend label format
    # search comparison
    if group == "search_comparison":
        structure_label = "Hash" if structure == "Hash Table" else "Linear"
        return f"{structure_label} {scenario.title()}"
    # priority queue core
    if group == "priority_queue_core":
        return f"{scenario.title()} {operation_label}"
    # hash collision
    if group == "hash_collision":
        return operation_label
    # hash table
    if structure == "Hash Table":
        return f"Hash {operation_label}"
    # default
    return f"{structure} {operation_label}"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_benchmark_series_axis_label()
def _build_benchmark_series_axis_label(row: pd.Series) -> str:
    """Return a compact x-axis label for the largest-size comparison chart.

    Logic:
        1. Mirror the dispatch logic of the short-label helper.
        2. Insert newlines so multi-word labels stay readable inside the bar axis.
    """
    structure = str(row["structure"])
    operation = str(row["operation"])
    scenario = str(row["scenario"])
    group = str(row["operation_group"])
    operation_label = _BENCHMARK_OPERATION_LABELS.get(
        operation,
        operation.replace("_", " ").title(),
    )

    # DISPATCH: each group has its own axis-label format with newlines
    # search comparison
    if group == "search_comparison":
        structure_label = "Hash" if structure == "Hash Table" else "Linear"
        return f"{structure_label}\n{scenario.title()}"
    # priority queue core
    if group == "priority_queue_core":
        return f"{scenario.title()}\n{operation_label}"
    # hash collision
    if group == "hash_collision":
        collision_label = operation_label.replace("Collision ", "")
        return f"Collision\n{collision_label}"
    # hash table
    if " " in operation_label:
        first_word, remainder = operation_label.split(" ", maxsplit=1)
        return f"{first_word}\n{remainder}"
    # default
    return operation_label
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_benchmark_series_long_label()
def _build_benchmark_series_long_label(row: pd.Series) -> str:
    """Return a descriptive tooltip label for a benchmark workload row.

    Logic:
        1. Translate scenario codes into descriptive English (e.g., "Forced Collision").
        2. Combine structure, operation, and scenario into a single tooltip string.
    """
    structure = str(row["structure"])
    operation = str(row["operation"])
    scenario = str(row["scenario"])
    operation_label = _BENCHMARK_OPERATION_LABELS.get(
        operation,
        operation.replace("_", " ").title(),
    )

    # human-friendly scenario phrasing for the tooltip
    if scenario in {"normal", "forced_collision"}:
        scenario_label = scenario.replace("_", " ").title()
    elif scenario in {"max", "min"}:
        scenario_label = f"{scenario.title()} Heap"
    else:
        scenario_label = scenario.title()

    return f"{structure} - {operation_label} ({scenario_label})"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _build_benchmark_series_sort_value()
def _build_benchmark_series_sort_value(row: pd.Series) -> int:
    """Return a stable sort key for benchmark workload display order.

    Logic:
        1. Map operation_group / structure / operation / scenario to integer ranks.
        2. Combine the ranks via positional weights (group * 100 + op * 10 + ...).
    """
    # map operation_group / structure / operation / scenario to integer ranks
    group = str(row["operation_group"])
    structure = str(row["structure"])
    operation = str(row["operation"])
    scenario = str(row["scenario"])
    # combine the ranks via positional weights (group * 100 + op * 10 + ...)
    group_order = {
        "hash_collision": 0,
        "hash_core": 1,
        "priority_queue_core": 2,
        "search_comparison": 3,
    }.get(group, 9)
    # structure order
    structure_order = 0 if structure in {"Hash Table", "Priority Queue"} else 1
    operation_order = _BENCHMARK_OPERATION_ORDER.get(operation, 9)
    scenario_order = _BENCHMARK_SCENARIO_ORDER.get(scenario, 9)
    return group_order * 100 + operation_order * 10 + scenario_order + structure_order
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_validation_results()
def render_validation_results(
    steps: list[ValidationStepResult],
    summary_lines: list[str],
    *,
    title: str = "Validation Results",
) -> None:
    """Render guided-demo validation steps and summary notes.

    Logic:
        1. Render the section title.
        2. VALIDATION: render an info banner and bail when there are no steps.
        3. Render the headline metrics (passed count + overall pass/check).
        4. Render any summary lines as markdown bullets.
        5. Render the validation steps as a Streamlit DataFrame.
    """
    st.subheader(title)

    # VALIDATION: friendly placeholder when no steps have been recorded
    if not steps:
        st.info("No validation results available yet.")
        return
    # headline metrics
    passed_count = sum(1 for step in steps if step.passed)
    c1, c2 = st.columns(2)
    c1.metric("Checks Passed", f"{passed_count}/{len(steps)}")
    c2.metric("Overall Status", "PASS" if passed_count == len(steps) else "CHECK")
    # summary lines 
    if summary_lines:
        for line in summary_lines:
            st.markdown(f"- {line}")
    # validation steps
    rows = [step.as_dict() for step in steps]
    st.dataframe(pd.DataFrame(rows), hide_index=True, height=280)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- render_benchmark_validation_summary()
def render_benchmark_validation_summary(
    result: BenchmarkValidationResult,
) -> None:
    """Render benchmark validation metrics and pass/fail checks.

    Logic:
        1. Render the three headline metrics (rows correct, hash faster, assignment check).
        2. Render the underlying validation steps + summary lines via render_validation_results.
    """
    # headline metrics
    c1, c2, c3 = st.columns(3)
    # rows correct
    c1.metric("Rows Correct", f"{result.correct_rows}/{result.total_rows}")
    # hash faster
    c2.metric(
        "Hash Faster",
        f"{result.hash_faster_scenarios}/{result.total_search_scenarios}",
    )
    # assignment check
    c3.metric(
        "Assignment Check",
        "PASS" if result.meets_assignment_requirement else "CHECK",
    )
    # validation steps
    render_validation_results(
        result.checks,
        result.summary_lines,
        title="Benchmark Validation",
    )
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# MARKDOWN TEMPLATE RENDERING
# ==============================================================================
# Loads a Markdown file from disk, substitutes "{{PLACEHOLDER}}" tokens with
# rendered content, and promotes local image lines to st.image() calls.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_analysis_markdown_file()
def render_analysis_markdown_file(
    path: Path,
    placeholders: dict[str, str] | None = None,
) -> None:
    """Read a Markdown file, replace ``{{PLACEHOLDER}}`` tokens, and render.

    Image markdown lines pointing to local files are promoted to
    ``st.image()`` calls.

    Logic:
        1. VALIDATION: render an error and return when *path* does not exist.
        2. Read the file and default the placeholder map to {} when omitted.
        3. Define helper closures that flush an accumulated markdown buffer
           and that promote local image lines to st.image().
        4. MAIN ITERATION LOOP: walk every line and dispatch placeholders /
           images / plain markdown to the right rendering path.
        5. Flush any remaining buffered markdown after the loop ends.
    """
    # VALIDATION: missing file path surfaces a clear error
    # read the file
    if not path.exists():
        st.error(f"File not found: {path}")
        return
    # default placeholders
    text = path.read_text(encoding="utf-8")
    # placeholders  
    if placeholders is None:
        placeholders = {}
    # buffer
    md_buffer: list[str] = []
    #--- render content
    def _render_content(content: str) -> None:
        """Render markdown content, promoting local images to st.image()."""
        image_match = _IMAGE_MARKDOWN_RE.fullmatch(content.strip())
        # image match
        if image_match:
            alt_text, image_target = image_match.groups()
            image_path = path.parent / image_target
            if image_path.exists():
                st.image(str(image_path), caption=alt_text or None)
                return
        st.markdown(content)
    #--------------------------------                                            
    #--- flush
    def _flush() -> None:
        """Emit accumulated markdown lines as one block."""
        if md_buffer:
            _render_content("\n".join(md_buffer))
            md_buffer.clear()

    # MAIN ITERATION LOOP: dispatch each line to the right rendering path
    for line in text.splitlines():
        # DISPATCH: "{{PLACEHOLDER}}" lines pull rendered content from the map
        match = _PLACEHOLDER_RE.fullmatch(line.strip())
        # placeholder match
        if match:
            _flush()
            key = match.group(1)
            if key in placeholders:
                _render_content(placeholders[key])
            else:
                st.info(
                    f"Placeholder `{key}` — data not yet available. "
                    "Run a benchmark to populate."
                )
            continue

        # DISPATCH: image lines flush the buffer then render via st.image()
        image_match = _IMAGE_MARKDOWN_RE.fullmatch(line.strip())
        # image match
        if image_match:
            _flush()
            _render_content(line)
            continue

        md_buffer.append(line)

    # flush any trailing markdown after the loop
    _flush()
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
