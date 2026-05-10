# File: graph_label_utils.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - wrap_label() breaks long graph labels into compact display rows.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Used by Graphviz visual builders and Streamlit graph rendering helpers.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Shared graph label formatting helpers."""

from __future__ import annotations


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# GRAPH LABEL FORMATTERS
# ==============================================================================
# Compact labels keep Graphviz nodes readable without changing original data.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- wrap_vertex_label()
def wrap_vertex_label(label: str, *, max_line_length: int = 10) -> str:
    """Wrap a vertex label onto short display lines.

    Args:
        label: Original vertex label.
        max_line_length: Preferred maximum characters per display line.

    Returns:
        Label with newline separators for graph drawing.
    """
    words = str(label).split()
    if len(words) <= 1:
        return str(label)

    lines: list[str] = []
    current_line = words[0]
    # MAIN ITERATION LOOP: keep words together while keeping labels compact
    for word in words[1:]:
        candidate = f"{current_line} {word}"
        # VALIDATION: maximum line length for display
        if len(candidate) <= max_line_length:
            current_line = candidate
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return "\n".join(lines)
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
