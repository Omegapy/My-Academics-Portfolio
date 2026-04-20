# -------------------------------------------------------------------------
# File: streamlit_helpers.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Streamlit helper functions. Provides ->
# UI components: header banner, dataset info panel, structure-state preview,
# OperationResult metric card, big-O complexity table, structure comparison
# grid, benchmark table, in-app interactive charts, and Markdown template
# rendering with placeholder substitution.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Streamlit UI helpers for the Module 4 Algorithm and Data Structure Comparison Tool."""

# ________________
# Imports
#

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from data.dataset_manager import preview_dataset
from models.operation_result import OperationResult

# __________________________________________________________________________
# Constants
#

# Consistent per-structure color palette (matches report_generator.py)
STRUCTURE_COLORS: dict[str, str] = {
    "Stack": "#e74c3c",
    "Queue": "#f39c12",
    "Deque": "#2ecc71",
    "LinkedList": "#3498db",
}

_STRUCTURE_NAMES: list[str] = list(STRUCTURE_COLORS.keys())
_STRUCTURE_HEX: list[str] = list(STRUCTURE_COLORS.values())

# Eight visually distinct SVG stroke-dasharray patterns for line styling.
# Indexed by an operation's position within its structure so that within any
# one structure (and therefore within any structure-only facet) every line
# has a different pattern. Cycled modulo len() if a structure ever exceeds
# eight operations.
_DASH_PATTERNS: list[list[float]] = [
    [1, 0],              # solid
    [6, 3],              # long dash
    [2, 3],              # short dash
    [1, 3],              # dot
    [6, 3, 1, 3],        # dash-dot
    [10, 3, 2, 3],       # long dash + short dash
    [1, 2, 1, 2, 6, 2],  # dot-dot-dash
    [4, 2, 4, 2, 1, 2],  # dash-dash-dot
]


# --------------------------------------------------------------- _shade_color()
def _shade_color(base_hex: str, idx: int, total: int) -> str:
    """Return a brightness-shifted shade of *base_hex* for series index *idx*.

    The shade interpolates a multiplicative brightness factor across
    ``[0.55, 1.25]`` so consecutive operations within one structure are
    perceptually distinct without leaving the structure's hue family.

    Args:
        base_hex: Hex color string (with or without leading ``#``).
        idx: Zero-based index of this series within its structure.
        total: Total number of series for this structure.

    Returns:
        A new hex color string of the form ``#rrggbb``.
    """
    # Remove the leading '#' from the hex color string
    base_hex = base_hex.lstrip("#")
    
    # Convert the hex color string to RGB
    r, g, b = (int(base_hex[i : i + 2], 16) for i in (0, 2, 4))
    
    # Adjust the brightness of the color based on the index
    if total <= 1:
        factor = 1.0
    else:
        factor = 0.55 + (0.70 * idx / (total - 1))
    
    # Clamp the values to the range [0, 255]
    r = max(0, min(255, int(round(r * factor))))
    g = max(0, min(255, int(round(g * factor))))
    b = max(0, min(255, int(round(b * factor))))
    
    # Return the new hex color string
    return f"#{r:02x}{g:02x}{b:02x}"
# --------------------------------------------------------------- end _shade_color()


# --------------------------------------------------------------- _build_operation_visual_scales()
def _build_operation_visual_scales(
    plot_df: pd.DataFrame,
) -> tuple[list[str], list[str], list[list[float]]]:
    """Return ``(domain, color_range, dash_range)`` for the operation legend.

    Each structure's operations are assigned shades of its base color from
    :data:`STRUCTURE_COLORS` (so the structure-color theme stays intact) AND
    a dash pattern from :data:`_DASH_PATTERNS` indexed by the operation's
    position within its structure (so lines within a structure-only facet
    are distinguishable by line style as well as color). Operations are
    sorted alphabetically inside their structure so the same operation
    always gets the same color/dash across runs.

    Args:
        plot_df: Benchmark DataFrame with ``structure`` and ``operation``
            columns.

    Returns:
        Tuple ``(domain, color_range, dash_range)`` where ``domain[i]`` is
        the ``"Structure.operation"`` label, ``color_range[i]`` is the matching
        hex color, and ``dash_range[i]`` is the matching SVG stroke-dasharray
        list. Suitable for ``alt.Scale(domain=..., range=...)`` on color and
        strokeDash respectively.
    """
    domain: list[str] = []
    color_range: list[str] = []
    dash_range: list[list[float]] = []
    
    # Iterate over each structure
    for structure in _STRUCTURE_NAMES:
        # Get the operations for the current structure
        ops = sorted(
            plot_df.loc[plot_df["structure"] == structure, "operation"]
            .astype(str)
            .unique()
        )
        
        # Iterate over each operation
        for i, op in enumerate(ops):
            # Add the operation to the domain
            domain.append(f"{structure}.{op}")
            # Add the color to the color range
            color_range.append(_shade_color(STRUCTURE_COLORS[structure], i, len(ops)))
            # Add the dash pattern to the dash range
            dash_range.append(_DASH_PATTERNS[i % len(_DASH_PATTERNS)])
    return domain, color_range, dash_range
# --------------------------------------------------------------- end _build_operation_visual_scales()


# Operation group → human-readable label
_GROUP_LABELS: dict[str, str] = {
    "common_build": "Common Build",
    "common_drain": "Common Drain",
    "peek_front": "Peek / Front",
    "deque_ends": "Deque Ends",
    "linked_list_search": "LinkedList Search",
    "linked_list_delete": "LinkedList Delete",
    "linked_list_display": "LinkedList Display",
}

# Lines like {{BENCHMARK_RESULTS_TABLE}}
_PLACEHOLDER_RE = re.compile(r"^\{\{([A-Z0-9_]+)\}\}$")
_IMAGE_MARKDOWN_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)$")

# Maximum size at which we still display step traces in the playground
_TRACE_MAX_SIZE: int = 25

# Color used to highlight a single added/removed value in the operation
# result before/after view (Material yellow 400).
_HIGHLIGHT_COLOR: str = "#ffeb3b"

# __________________________________________________________________________
# Header
#

# ========================================================================
# Header
# ========================================================================

# --------------------------------------------------------------- render_header()
def render_header() -> None:
    """Render the application title and CSC506 course banner."""
    st.title("Algorithm and Data Structure Comparison Tool")
    st.caption(
        "CSC506 – Design and Analysis of Algorithms | "
        "Professor Dr. Jonathan Vanover | Spring A 2026 | "
        "Student: Alexander Ricciardi"
    )
    st.divider()
# --------------------------------------------------------------- end render_header()

# __________________________________________________________________________
# Dataset Display
#

# ========================================================================
# Dataset Info
# ========================================================================

# --------------------------------------------------------------- render_dataset_info()
def render_dataset_info(
    data: list[int],
    dataset_type: str,
    size: int,
) -> None:
    """Display dataset metadata, preview, and an expandable full-table view.

    Args:
        data: The generated dataset.
        dataset_type: Label for the dataset type.
        size: Number of elements.
    """
    
    # Create two columns for the dataset info
    col1, col2 = st.columns(2)
    
    # Display the dataset type and size
    col1.metric("Dataset Type", dataset_type.title())
    col2.metric("Size", f"{size:,}")

    # Display the dataset preview
    st.markdown("**Preview (first / last 15 values):**")
    st.code(preview_dataset(data, count=15))

    # Display the full dataset in an expander
    with st.expander("View Full Dataset", expanded=False):
        df = pd.DataFrame({"Index": range(len(data)), "Value": data})
        st.dataframe(df, height=300, width="stretch", hide_index=True)
# --------------------------------------------------------------- end render_dataset_info()

# __________________________________________________________________________
# Structure State / Operation Result
#

# ========================================================================
# Structure State
# ========================================================================

# --------------------------------------------------------------- render_structure_state()
def render_structure_state(
    name: str,
    state: list[int],
    raw_state: list[int] | None = None,
) -> None:
    """Render the logical state of a structure plus an optional raw view.

    Args:
        name: Structure name (Stack, Queue, Deque, LinkedList).
        state: Logical state in the natural front/head-to-rear/tail order.
        raw_state: Optional raw internal storage for Queue/Deque so the
            student can see how the course-aligned orientation lines up.
    """
    
    # Get the color for the current structure
    color = STRUCTURE_COLORS.get(name, "#7f8c8d")
    
    # Display the structure name and size   
    st.markdown(
        f"#### <span style='color:{color}'>{name}</span> "
        f"&nbsp;<small>size = {len(state):,}</small>",
        unsafe_allow_html=True,
    )
    
    # Display the state
    if not state:
        st.caption("(empty)")
    else:
        st.code(preview_dataset(state, count=15))
    
    # Display the raw state if available
    if raw_state is not None:
        with st.expander(
            "Raw internal list (course-aligned orientation)",
            expanded=False,
        ):
            st.caption(
                "Right end of the internal list is the logical front. "
                "Index 0 is the logical rear."
            )
            st.code(preview_dataset(raw_state, count=15))
# --------------------------------------------------------------- end render_structure_state()

# ========================================================================
# Operation Result Card
# ========================================================================

# Lookup operations across all four ADTs that *return* a single value from
# the structure without mutating it. The "found" value gets highlighted in
# both the state-before and state-after panels.
_LOOKUP_FRONT_OPS: frozenset[str] = frozenset({"peek", "front", "peekFront"})
_LOOKUP_REAR_OPS: frozenset[str] = frozenset({"peekRear"})
_LOOKUP_VALUE_OPS: frozenset[str] = frozenset({"search"})


# --------------------------------------------------------------- _first_diff_index()
def _first_diff_index(before: list[int], after: list[int]) -> int:
    """Return the first index where *before* and *after* differ.

    If one is a strict prefix of the other, returns
    ``min(len(before), len(after))`` — i.e., the position where the longer
    one starts to extend past the shorter. This makes "rear" mutations
    (e.g. ``enqueue`` / ``addRear`` / ``insert (rear)``) report the
    new tail index in the longer state, and "rear remove" mutations
    (``removeRear`` / ``delete (rear)``) report the dropped tail index
    in the longer state.

    Args:
        before: Logical state before the operation.
        after: Logical state after the operation.

    Returns:
        Index of the first divergence (always within both lists for
        prefix-style edits).
    """
    n_min = min(len(before), len(after))
    
    # Iterate over the minimum length of the two lists
    for i in range(n_min):
        # If the values at the current index are not equal, return the index
        if before[i] != after[i]:
            return i
    
    # Return the minimum length of the two lists
    return n_min
# --------------------------------------------------------------- end _first_diff_index()


# --------------------------------------------------------------- _lookup_highlight_index()
def _lookup_highlight_index(result: OperationResult) -> int | None:
    """Return the state index to highlight for non-mutating lookup operations.

    Lookups don't mutate the state — they "find" or "peek at" a single
    element. We highlight the element they were *looking at* so the user
    can see exactly which value the call returned even when the structure
    is too long for the head preview window.

    Args:
        result: The :class:`OperationResult` for the operation.

    Returns:
        Zero-based index into ``result.state_after`` to highlight, or
        ``None`` if the operation is not a lookup or the structure is empty.
    """
    op = result.operation
    state = result.state_after
    
    # If the state is empty, return None
    if not state:
        return None
    
    # If the operation is a lookup front operation, return 0
    if op in _LOOKUP_FRONT_OPS:
        return 0
    
    # If the operation is a lookup rear operation, return the last index
    if op in _LOOKUP_REAR_OPS:
        return len(state) - 1
    if op in _LOOKUP_VALUE_OPS:
        returned = result.returned_value
        # SAFETY CHECK: bool is a subclass of int — exclude isEmpty/etc.
        if isinstance(returned, int) and not isinstance(returned, bool):
            try:
                return state.index(returned)
            except ValueError:
                return None
    return None
# --------------------------------------------------------------- end _lookup_highlight_index()


# --------------------------------------------------------------- _highlights_for_result()
def _highlights_for_result(
    result: OperationResult,
) -> tuple[int | None, int | None]:
    """Return ``(before_idx, after_idx)`` — index to highlight in each panel.

    Mutations are detected by a multiset diff between ``state_before`` and
    ``state_after``. Single-element adds highlight the new tail/middle/front
    cell in *state_after*; single-element removes highlight the vacated
    cell in *state_before*. The exact index comes from
    :func:`_first_diff_index`, which is robust against duplicate values
    (e.g. ``LinkedList.delete`` of a value that appears more than once).

    Lookups are routed through :func:`_lookup_highlight_index`, which
    highlights the *same* index in both panels (the state didn't change).

    Args:
        result: The :class:`OperationResult` for the operation.

    Returns:
        Tuple ``(before_idx, after_idx)``: index to highlight in the
        state-before / state-after panel, or ``None`` for "no highlight".
    """
    added_counts = Counter(result.state_after) - Counter(result.state_before)
    removed_counts = Counter(result.state_before) - Counter(result.state_after)
    added_total = sum(added_counts.values())
    removed_total = sum(removed_counts.values())

    # MUTATION: single-element add (push, enqueue, addFront/Rear, insert ...)
    if added_total == 1 and removed_total == 0:
        idx = _first_diff_index(result.state_before, result.state_after)
        return (None, idx)
    # MUTATION: single-element remove (pop, dequeue, removeFront/Rear, delete ...)
    if removed_total == 1 and added_total == 0:
        idx = _first_diff_index(result.state_before, result.state_after)
        return (idx, None)

    # LOOKUP: state unchanged, highlight the value the op was looking at
    lookup_idx = _lookup_highlight_index(result)
    if lookup_idx is not None:
        return (lookup_idx, lookup_idx)

    return (None, None)
# --------------------------------------------------------------- end _highlights_for_result()


# --------------------------------------------------------------- _select_preview_indices()
def _select_preview_indices(
    n: int,
    highlight_idx: int | None,
    count: int,
) -> list[int]:
    """Choose which indices of a length-*n* state to show in a *count*-item preview.

    If a *highlight_idx* falls outside the head window, the preview is
    split into a small head segment plus a tail window centered on the
    highlight, so the highlighted value is always visible.

    Args:
        n: Total length of the state being previewed.
        highlight_idx: Index of the cell that must remain visible, or
            ``None`` for the standard head-window behavior.
        count: Maximum number of items to show.

    Returns:
        Sorted list of indices to render. Consecutive non-adjacent indices
        signal a gap that the caller should mark with an ellipsis.
    """
    # SHORT LIST: nothing to truncate
    if n <= count:
        return list(range(n))

    # HEAD WINDOW: highlight (if any) is already visible in the first `count`
    if highlight_idx is None or highlight_idx < count:
        return list(range(count))

    # SPLIT: small head + tail window centered on the highlight
    head_size = max(3, count // 3)
    tail_size = count - head_size
    # Calculate the tail start and end indices
    half = tail_size // 2
    tail_start = max(head_size, highlight_idx - half)
    tail_end = min(n, tail_start + tail_size)
    if tail_end - tail_start < tail_size:
        # SAFETY CHECK: window clipped at the end — slide it left so we still
        # show `tail_size` items even when the highlight is near the very end.
        tail_start = max(head_size, n - tail_size)
        tail_end = n

    return list(range(head_size)) + list(range(tail_start, tail_end))
# --------------------------------------------------------------- end _select_preview_indices()


# --------------------------------------------------------------- _render_state_with_highlight()
def _render_state_with_highlight(
    state: list[int],
    highlight_idx: int | None,
    *,
    context_idx: int | None = None,
    count: int = 15,
) -> None:
    """Render *state* with the value at *highlight_idx* shown in yellow.

    The preview shows up to *count* items. When the focus index (the
    highlight, or the cross-panel *context_idx* fallback) falls past the
    head window, the preview is split into a small head segment plus a
    tail window centered on the focus, with gaps marked ``…``.

    Args:
        state: The full logical state to render.
        highlight_idx: Index of the cell to highlight in yellow, or
            ``None`` for plain rendering.
        context_idx: Optional secondary focus that influences the preview
            window without painting any cell. Used so the unhighlighted
            panel of a mutation (e.g. ``state_after`` for ``removeRear``)
            still shows the same region as its highlighted twin.
        count: Maximum number of values to display before truncation.
    """
    
    # If the state is empty, return None
    if not state:
        st.caption("(empty)")
        return

    n = len(state)
    # SAFETY CHECK: out-of-range indices fall back to no-highlight / no-focus
    if highlight_idx is not None and not (0 <= highlight_idx < n):
        highlight_idx = None
    if context_idx is not None and not (0 <= context_idx < n):
        context_idx = None

    # FOCUS: prefer the highlight, fall back to the cross-panel context
    focus_idx = highlight_idx if highlight_idx is not None else context_idx
    indices = _select_preview_indices(n, focus_idx, count)
    
    # Build the parts list
    parts: list[str] = []

    # Iterate over the indices
    for pos, i in enumerate(indices):
        # GAP: emit "…" between non-adjacent shown indices
        if pos > 0 and i - indices[pos - 1] > 1:
            parts.append("…")
        v = state[i]
        # Highlight the cell if it is the highlighted index
        if highlight_idx is not None and i == highlight_idx:
            parts.append(
                f"<span style='background:{_HIGHLIGHT_COLOR};"
                "color:#000;padding:0 6px;border-radius:3px;"
                f"font-weight:600;'>{v}</span>"
            )
        else:
            parts.append(str(v))

    # TRAILING ELLIPSIS: if we don't render through the final element
    if indices and indices[-1] < n - 1:
        parts.append("…")

    body = ", ".join(parts)
    # NOTE: explicit dark text color so unhighlighted values are readable on
    # the light panel background under both light and dark Streamlit themes.
    html = (
        "<div style='font-family:ui-monospace,SFMono-Regular,Menlo,monospace;"
        "background:#f5f5f5;color:#1f2328;padding:8px 10px;border-radius:4px;"
        "border:1px solid #e0e0e0;font-size:0.9rem;line-height:1.6;'>"
        f"[{body}]"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)
# --------------------------------------------------------------- end _render_state_with_highlight()


# --------------------------------------------------------------- render_operation_result()
def render_operation_result(result: OperationResult) -> None:
    """Render an :class:`OperationResult` as a metrics card.

    The before/after panels highlight in yellow:

    * the cell *added* by single-element mutations (push, enqueue,
      addFront/Rear, insert in any mode) — in **state_after**
    * the cell *vacated* by single-element mutations (pop, dequeue,
      removeFront/Rear, delete in any mode) — in **state_before**
    * the cell *looked at* by non-mutating lookups (peek, front,
      peekFront, peekRear, search) — in **both** panels

    Multi-element mutations (``clear``) and ops with no useful highlight
    (``display``, ``isEmpty``, ``__len__``) render plain. When the
    highlighted cell falls past the head preview window, the panel
    splits into a small head segment plus a tail window centered on the
    highlight so the change is always visible.

    Args:
        result: The :class:`OperationResult` to display.
    """
    color = STRUCTURE_COLORS.get(result.structure, "#888888")
    st.markdown(
        f"### <span style='color:{color}'>{result.structure}.{result.operation}</span>",
        unsafe_allow_html=True,
    )

    # Create columns for the metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Returned", _format_returned(result.returned_value))
    c2.metric("Size", f"{result.size_before:,} → {result.size_after:,}")
    c3.metric("Time", f"{result.elapsed_time * 1_000:.4f} ms")
    c4.metric("Big-O", result.complexity)

    # Display input and anchor values if they exist 
    if result.input_value is not None or result.anchor_value is not None:
        bits: list[str] = []
        if result.input_value is not None:
            bits.append(f"value = `{result.input_value}`")
        if result.anchor_value is not None:
            bits.append(f"anchor = `{result.anchor_value}`")
        st.caption(" • ".join(bits))

    if result.operation.startswith("display"):
        st.caption(
            "Display traverses the structure without changing it. "
            "The structure state stays the same; the returned traversal shows "
            "the requested order."
        )
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Structure state (unchanged):**")
            _render_state_with_highlight(result.state_after, None)
        with cols[1]:
            st.markdown("**Traversal returned:**")
            traversal = (
                result.returned_value
                if isinstance(result.returned_value, list)
                else []
            )
            _render_state_with_highlight(traversal, None)
        return

    before_idx, after_idx = _highlights_for_result(result)
    # CROSS-CONTEXT: when only one side is highlighted (single-element
    # mutation), focus the other panel's preview window on the same logical
    # region so the user can see "what changed" on both sides — e.g. for
    # ``removeRear`` the state_after panel should show the new rear, not
    # just the head window.
    n_before = len(result.state_before)
    n_after = len(result.state_after)
    before_context: int | None = None
    after_context: int | None = None

    # Set the context index for the cross-panel highlighting
    if before_idx is not None and after_idx is None and n_after > 0:
        after_context = min(before_idx, n_after - 1)
    elif after_idx is not None and before_idx is None and n_before > 0:
        before_context = min(after_idx, n_before - 1)

    cols = st.columns(2)

    # Render the state before
    with cols[0]:
        st.markdown("**State before:**")
        _render_state_with_highlight(
            result.state_before, before_idx, context_idx=before_context
        )
    with cols[1]:
        st.markdown("**State after:**")
        _render_state_with_highlight(
            result.state_after, after_idx, context_idx=after_context
        )

    # Display step trace if it exists and the state size is within the limit
    if result.step_trace and result.size_after <= _TRACE_MAX_SIZE:
        with st.expander(
            f"Step Trace ({len(result.step_trace)} steps)", expanded=False
        ):
            for step in result.step_trace:
                st.text(step)
# --------------------------------------------------------------- end render_operation_result()


# --------------------------------------------------------------- _format_returned()
def _format_returned(value: int | bool | list[int] | None) -> str:
    """Format an operation return value for the metric card.

    Args:
        value: The value returned by the operation.

    Returns:
        A short, display-ready string.
    """

    # Format the return value for the metric card
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, list):
        if not value:
            return "[]"
        head = ", ".join(str(v) for v in value[:5])
        if len(value) > 5:
            head += f", … (+{len(value) - 5})"
        return f"[{head}]"
    return str(value)
# --------------------------------------------------------------- end _format_returned()

# __________________________________________________________________________
# Complexity Table
#

# ========================================================================
# Complexity Table
# ========================================================================

_COMPLEXITY_ROWS: list[dict[str, str]] = [
    {"Operation": "build (n items)",
     "Stack": "O(n)",
     "Queue": "O(n²)",
     "Deque": "O(n²) addRear / O(n) addFront",
     "LinkedList": "O(n) insert_rear"},
    {"Operation": "drain (n items)",
     "Stack": "O(n)",
     "Queue": "O(n)",
     "Deque": "O(n) removeFront / O(n²) removeRear",
     "LinkedList": "O(n) delete head"},
    {"Operation": "push / enqueue / addRear / insert_rear",
     "Stack": "O(1)",
     "Queue": "O(n)",
     "Deque": "O(n)",
     "LinkedList": "O(1)"},
    {"Operation": "addFront / insert_front",
     "Stack": "n/a",
     "Queue": "n/a",
     "Deque": "O(1)",
     "LinkedList": "O(1)"},
    {"Operation": "pop / dequeue / removeFront / delete head",
     "Stack": "O(1)",
     "Queue": "O(1)",
     "Deque": "O(1)",
     "LinkedList": "O(1)"},
    {"Operation": "removeRear / delete tail",
     "Stack": "n/a",
     "Queue": "n/a",
     "Deque": "O(n)",
     "LinkedList": "O(1)"},
    {"Operation": "peek / front / peekFront / peekRear",
     "Stack": "O(1)",
     "Queue": "O(1)",
     "Deque": "O(1)",
     "LinkedList": "O(1)"},
    {"Operation": "search (value)",
     "Stack": "O(n)",
     "Queue": "O(n)",
     "Deque": "O(n)",
     "LinkedList": "O(n)"},
    {"Operation": "delete (value, middle)",
     "Stack": "n/a",
     "Queue": "n/a",
     "Deque": "n/a",
     "LinkedList": "O(n)"},
    {"Operation": "insert before/after anchor",
     "Stack": "n/a",
     "Queue": "n/a",
     "Deque": "n/a",
     "LinkedList": "O(n) (search) + O(1) (splice)"},
    {"Operation": "display (forward / reverse)",
     "Stack": "O(n)",
     "Queue": "O(n)",
     "Deque": "O(n)",
     "LinkedList": "O(n)"},
]


# --------------------------------------------------------------- render_complexity_table()
def render_complexity_table() -> None:
    """Render a Big-O complexity table covering every required operation."""
    df = pd.DataFrame(_COMPLEXITY_ROWS)
    st.dataframe(df, hide_index=True, width="stretch")
# --------------------------------------------------------------- end render_complexity_table()

# __________________________________________________________________________
# Comparison Grid
#

_STRUCTURE_PROFILES: dict[str, dict[str, str]] = {
    "Stack": {
        "ordering": "LIFO",
        "ends": "top only",
        "build": "O(n)",
        "best": "push / pop at top",
        "use": "Undo, expression eval, DFS, brackets",
    },
    "Queue": {
        "ordering": "FIFO",
        "ends": "front + rear",
        "build": "O(n²) (insert(0))",
        "best": "front-only consumption",
        "use": "Scheduling, BFS, buffers",
    },
    "Deque": {
        "ordering": "Both ends",
        "ends": "front + rear",
        "build": "addFront O(n) / addRear O(n²)",
        "best": "front operations",
        "use": "Sliding windows, palindromes",
    },
    "LinkedList": {
        "ordering": "Doubly linked",
        "ends": "head + tail",
        "build": "O(n) insert_rear",
        "best": "splice around known nodes",
        "use": "LRU caches, playlists, history",
    },
}


# ========================================================================
# Comparison Grid
# ========================================================================

# --------------------------------------------------------------- render_comparison_grid()
def render_comparison_grid() -> None:
    """Render side-by-side cards for all four structures."""
    cols_top = st.columns(2)
    cols_bot = st.columns(2)
    cell_columns = [cols_top[0], cols_top[1], cols_bot[0], cols_bot[1]]

    for col, name in zip(cell_columns, _STRUCTURE_NAMES):
        profile = _STRUCTURE_PROFILES[name]
        color = STRUCTURE_COLORS[name]
        with col:
            st.markdown(
                f"#### <span style='color:{color}'>{name}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**Ordering:** {profile['ordering']}")
            st.markdown(f"**Ends used:** {profile['ends']}")
            st.markdown(f"**Build cost:** `{profile['build']}`")
            st.markdown(f"**Best at:** {profile['best']}")
            st.markdown(f"**Typical use:** {profile['use']}")
# --------------------------------------------------------------- end render_comparison_grid()

# __________________________________________________________________________
# Benchmark Table & Charts
#

# ========================================================================
# Benchmark Table
# ========================================================================

# --------------------------------------------------------------- render_benchmark_table()
def render_benchmark_table(df: pd.DataFrame) -> None:
    """Render a benchmark DataFrame as a formatted, scrollable table.

    Args:
        df: Benchmark results DataFrame with columns ``structure``,
            ``operation``, ``operation_group``, ``size``, ``time_ms``,
            ``size_before``, ``size_after``, ``complexity``, ``is_correct``.
    """
    display = df.copy()
    
    # Map the operation group to a more readable label
    display["operation_group"] = display["operation_group"].map(
        lambda g: _GROUP_LABELS.get(str(g), str(g))
    )
    
    # Reorder the columns
    display = display[
        [
            "structure",
            "operation",
            "operation_group",
            "size",
            "time_ms",
            "size_before",
            "size_after",
            "complexity",
            "is_correct",
        ]
    ]

    # Rename the columns
    display.columns = [
        "Structure",
        "Operation",
        "Group",
        "Size",
        "Time (ms)",
        "Size Before",
        "Size After",
        "Big-O",
        "Correct",
    ]

    # Format the columns for display
    display["Size"] = display["Size"].apply(lambda x: f"{int(x):,}")
    display["Time (ms)"] = display["Time (ms)"].apply(lambda x: f"{float(x):.4f}")
    display["Size Before"] = display["Size Before"].apply(lambda x: f"{int(x):,}")
    display["Size After"] = display["Size After"].apply(lambda x: f"{int(x):,}")
    display["Correct"] = display["Correct"].apply(
        lambda x: "✓" if bool(x) else "✗"
    )

    # Render the table
    st.dataframe(display, width="stretch", hide_index=True, height=520)
# --------------------------------------------------------------- end render_benchmark_table()

# ========================================================================
# Benchmark Charts
# ========================================================================

# --------------------------------------------------------------- render_benchmark_charts()
def render_benchmark_charts(
    df: pd.DataFrame,
    winners_df: pd.DataFrame | None = None,
) -> None:
    """Render in-app interactive Altair charts from benchmark results.

    Args:
        df: Benchmark results DataFrame.
        winners_df: Optional operation winners DataFrame; when provided a
            heatmap-style table is rendered alongside the runtime charts.
    """
    plot_df = df.copy()
    plot_df["operation_label"] = (
        plot_df["structure"].astype(str)
        + "."
        + plot_df["operation"].astype(str)
    )

    # FACET TITLES: annotate each operation_group with the structures it
    # actually contains, sorted in canonical structure order. Computed from
    # the live DataFrame so the annotations stay correct if the workload
    # registry adds operations later.
    group_to_structures: dict[str, list[str]] = {
        str(grp): sorted(
            sub["structure"].astype(str).unique().tolist(),
            key=lambda s: (
                _STRUCTURE_NAMES.index(s) if s in _STRUCTURE_NAMES else 99
            ),
        )
        for grp, sub in plot_df.groupby("operation_group")
    }

    # Annotated group label
    def _annotated_group_label(grp: object) -> str:
        base = _GROUP_LABELS.get(str(grp), str(grp))
        structs = group_to_structures.get(str(grp), [])
        if structs:
            return f"{base} ({', '.join(structs)})"
        return base

    # Add the annotated group label to the DataFrame
    plot_df["operation_group_label"] = plot_df["operation_group"].map(
        _annotated_group_label
    )

    # VISUAL SCALES: per-operation shades of each structure's base color so
    # the legend shows every (Structure, operation) pair as a unique swatch,
    # PLUS a parallel dash-pattern range so lines whose colors are close
    # (e.g. four shades of blue inside the LinkedList facets) stay visually
    # distinguishable by line style as well as hue.
    op_domain, op_color_range, op_dash_range = _build_operation_visual_scales(plot_df)
    op_color_scale = alt.Scale(domain=op_domain, range=op_color_range)
    op_dash_scale = alt.Scale(domain=op_domain, range=op_dash_range)

    # AXIS SETUP: pin x-ticks to the actual benchmarked sizes so gridlines
    # align with real data points instead of arbitrary log decades.
    benchmarked_sizes = sorted(plot_df["size"].unique().tolist())

    # ---- Chart 1: Runtime by size, faceted by operation group ----
    st.subheader("Runtime by Size (per operation group)")

    # Create the line chart
    line = (
        alt.Chart(plot_df)
        .mark_line(point=True)
        # Encode the x and y axes
        .encode(
            x=alt.X(
                "size:Q",
                title="Dataset Size",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(values=benchmarked_sizes, format=","),
            ),
            y=alt.Y(
                "time_ms:Q",
                title="Time (ms)",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(format=".0e", tickCount=6),
            ),
            # Color encode by operation label
            color=alt.Color(
                "operation_label:N",
                title="Operation",
                scale=op_color_scale,
                # LEGEND STYLING: symbolType="stroke" renders each legend
                # entry as a horizontal line sample so the merged dash
                # pattern is visible alongside the color swatch.
                legend=alt.Legend(
                    columns=1,
                    symbolLimit=40,
                    symbolType="stroke",
                    symbolStrokeWidth=2,
                    symbolSize=200,
                ),
            ),
            # Stroke dash encode by operation label
            strokeDash=alt.StrokeDash(
                "operation_label:N",
                scale=op_dash_scale,
                legend=None,  # legend merges with color via shared field
            ),
            # Add detail and tooltip
            detail="structure:N",
            tooltip=[
                "structure",
                "operation",
                "operation_group_label",
                "size",
                alt.Tooltip("time_ms:Q", format=".4f"),
                "complexity",
            ],
        )
        # Set the height and facet the chart
        .properties(height=340)
        .facet(
            facet=alt.Facet("operation_group_label:N", title="Operation Group"),
            columns=2,
        )
    )
    # Render the line chart
    st.altair_chart(line, width="stretch")

    # ---- Chart 2: Bar chart at the largest size, faceted by group ----
    largest = int(plot_df["size"].max())
    largest_df = plot_df[plot_df["size"] == largest].copy()

    # Render the bar chart
    if not largest_df.empty:
        st.subheader(f"Per-operation runtime at n = {largest:,}")
        # BASELINE FIX: ``mark_bar`` on a log y-scale needs an explicit
        # positive baseline because log(0) is undefined — without one,
        # Vega-Lite renders every bar with zero height (invisible). Pick a
        # baseline one decade below the smallest positive runtime so every
        # bar has a visible body and the relative heights are still
        # meaningful on log scale.
        positive_times = largest_df.loc[largest_df["time_ms"] > 0, "time_ms"]
        if not positive_times.empty:
            baseline_value = float(positive_times.min()) / 10.0
        else:
            baseline_value = 1e-6
        # SAFETY CHECK: clamp the baseline so it never collapses to zero
        # (would re-introduce the log(0) problem) and never goes absurdly
        # small (would dwarf every bar visually).
        baseline_value = max(baseline_value, 1e-9)
        largest_df["_baseline"] = baseline_value

        # Create the bar chart
        bar = (
            alt.Chart(largest_df)
            .mark_bar()
            .encode(
                x=alt.X(
                    "operation:N",
                    title=None,
                    sort="-y",
                    # LABELS: ``labelOverlap=False`` forces every operation
                    # name to render even when tilted labels would otherwise
                    # collide; the steeper -40° angle keeps each label's
                    # horizontal footprint small enough that 4 bars fit in
                    # one facet column without dropping any tick.
                    axis=alt.Axis(
                        labelAngle=-40,
                        labelLimit=200,
                        labelOverlap=False,
                    ),
                    # BAND PADDING: extra inner padding gives each bar a
                    # narrower footprint with more whitespace around it,
                    # leaving room for the rotated labels beneath.
                    scale=alt.Scale(paddingInner=0.25, paddingOuter=0.15),
                ),
                # Encode the y-axis
                y=alt.Y(
                    "time_ms:Q",
                    title="Time (ms)",
                    scale=alt.Scale(type="log", domainMin=baseline_value),
                    axis=alt.Axis(format=".0e", tickCount=6),
                ),
                y2=alt.Y2("_baseline:Q"),
                color=alt.Color(
                    "operation_label:N",
                    title="Operation",
                    scale=op_color_scale,
                    legend=alt.Legend(columns=1, symbolLimit=40),
                ),
                # Add tooltip
                tooltip=[
                    "structure",
                    "operation",
                    "operation_group_label",
                    alt.Tooltip("time_ms:Q", format=".4f"),
                    "complexity",
                ],
            )
            # Set the height and facet the chart
            .properties(height=260)
            .facet(
                facet=alt.Facet("operation_group_label:N", title=None),
                columns=2,
            )
            .resolve_scale(y="shared", x="independent")
        )
        # Render the bar chart
        st.altair_chart(bar, width="stretch")

    # ---- Chart 3: Winners heatmap-style table ----
    if winners_df is not None and not winners_df.empty:
        st.subheader("Fastest structure per operation group and size")
        winners_display = winners_df.copy()

        # Map operation group labels
        winners_display["operation_group"] = winners_display["operation_group"].map(
            lambda g: _GROUP_LABELS.get(str(g), str(g))
        )
        # Format size column
        winners_display["size"] = winners_display["size"].apply(
            lambda x: f"{int(x):,}"
        )
        winners_display["fastest_time_ms"] = winners_display["fastest_time_ms"].apply(
            lambda x: f"{float(x):.4f}"
        )
        # Select and rename columns
        winners_display = winners_display[
            [
                "operation_group",
                "size",
                "fastest_structure",
                "fastest_operation",
                "fastest_time_ms",
                "runner_up",
            ]
        ]
        # Rename columns
        winners_display.columns = [
            "Operation Group",
            "Size",
            "Fastest Structure",
            "Fastest Operation",
            "Time (ms)",
            "Runner-Up",
        ]
        # Render the dataframe
        st.dataframe(winners_display, hide_index=True, width="stretch")
# --------------------------------------------------------------- end render_benchmark_charts()

# __________________________________________________________________________
# Markdown Template Rendering
#

# ========================================================================
# Analysis Markdown
# ========================================================================

# --------------------------------------------------------------- render_analysis_markdown_file()
def render_analysis_markdown_file(
    path: Path,
    benchmark_df: pd.DataFrame | None = None,
    winners_df: pd.DataFrame | None = None,
) -> None:
    """Read a Markdown file, substitute ``{{PLACEHOLDER}}`` tokens, and render.

    Args:
        path: Path to the Markdown deliverable.
        benchmark_df: Optional benchmark DataFrame for the data tables.
        winners_df: Optional operation winners DataFrame for the winner
            tables and the heatmap reference.
    """
    # Check if the file exists
    if not path.exists():
        st.error(f"File not found: {path}")
        return

    text = path.read_text(encoding="utf-8")

    # SETUP: build placeholder substitutions from the live DataFrames
    placeholders: dict[str, str] = {}
    chart_paths = {
        "COMMON_OPERATION_CHART": Path(
            "Portfolio-Milestone-Module-4/analysis/charts/common_operation_runtime.png"
        ),
        "STRUCTURE_SPECIFIC_CHART": Path(
            "Portfolio-Milestone-Module-4/analysis/charts/structure_specific_runtime.png"
        ),
        "OPERATION_WINNER_HEATMAP": Path(
            "Portfolio-Milestone-Module-4/analysis/charts/operation_winner_heatmap.png"
        ),
        "STRUCTURE_PROFILE_TABLE": Path(
            "Portfolio-Milestone-Module-4/analysis/charts/structure_profile_comparison.png"
        ),
    }
    # Build benchmark results table
    if benchmark_df is not None and not benchmark_df.empty:
        # Local import to avoid circular dependency at package import time.
        from analysis.report_generator import build_benchmark_table
        placeholders["BENCHMARK_RESULTS_TABLE"] = build_benchmark_table(
            benchmark_df
        )
    # Build operation winners table
    if winners_df is not None and not winners_df.empty:
        from analysis.report_generator import build_operation_winners_table
        placeholders["OPERATION_WINNERS_TABLE"] = (
            build_operation_winners_table(winners_df)
        )

    md_buffer: list[str] = []

    # Render content, promoting bare image lines to ``st.image``
    def render_content(content: str) -> None:
        """Render content, promoting bare image lines to ``st.image``."""
        image_match = _IMAGE_MARKDOWN_RE.fullmatch(content.strip())
        if image_match:
            alt_text, target = image_match.groups()
            image_path = Path(target)
            if image_path.exists():
                st.image(str(image_path), caption=alt_text or None)
                return
        st.markdown(content)
    # Flush accumulated markdown
    def flush() -> None:
        """Emit accumulated markdown, splitting out standalone image lines."""
        if not md_buffer:
            return
        # Create a text buffer
        text_buffer: list[str] = []
        # Iterate over the buffered markdown
        for buffered_line in md_buffer:
            if _IMAGE_MARKDOWN_RE.fullmatch(buffered_line.strip()):
                if text_buffer:
                    st.markdown("\n".join(text_buffer))
                    text_buffer.clear()
                render_content(buffered_line)
            else:
                text_buffer.append(buffered_line)
        # Flush the text buffer
        if text_buffer:
            st.markdown("\n".join(text_buffer))

        md_buffer.clear()
    # Iterate over the lines in the text
    for line in text.splitlines():
        match = _PLACEHOLDER_RE.fullmatch(line.strip()) 
        # If a match is found, flush the text buffer
        if match:
            flush()
            key = match.group(1)
            # If the key is in the placeholders, render the content
            if key in placeholders:
                render_content(placeholders[key])
                continue
            if key in chart_paths and chart_paths[key].exists():
                st.image(str(chart_paths[key]), caption=key.replace("_", " ").title())
                continue
            st.info(
                f"Placeholder `{key}` — data not yet available. "
                "Run a benchmark or generate charts first."
            )
        else:
            md_buffer.append(line)

    flush()
# --------------------------------------------------------------- end render_analysis_markdown_file()

# __________________________________________________________________________
# End of File
#
