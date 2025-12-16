#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: phtrs_summary.py
# Project: CTA Module 5 – PHTRS Summary
# Author: Alexander Ricciardi
# Date: 2025-12-16
# [File Path] CTA-Module-5/phtrs_summary.py
# ------------------------------------------------------------------------
# Course: CSC-505 Principles of Software Development – Python Programming
# Professor: Dr. Joseph Issa
# Winter A (25WA) – 2025
# ------------------------------------------------------------------------
# Assignment:
# Critical Thinking Assignment 5 – PHTRS
#
# Directions:
# Summarize actors and use cases for the Pothole Tracking and Repair System (PHTRS),
# displaying tables of actors/use cases and a textual diagram summary.
# ------------------------------------------------------------------------
# Project:
# PHTRS (Pothole Tracking and Repair System) summarizer
#
# Project description:
# Write a Python Summary Script that:
# - Defines the actors and use cases shown in your diagram
# - Prints out each actor and a brief description of their associated use cases
# - Outputs a short textual summary of your diagram structure
# ------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: UseCase
# - Class: Actor
# - Functions: build_model, actors_table, use_cases_table, actor_summaries,main
# - Constants: MAX_LINE_WIDTH, _BANNER_OVERHEAD, MAX_CONTENT_WIDTH, SECTION_DIVIDER
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: dataclasses, pathlib, re, textwrap, typing
# - Local Project Modules: utilities.menu_banner_utilities.Banner
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------
"""
It is small console program that summarizes the PHTRS (Pothole Tracking and Repair System) use-case model.
"""

# __________________________________________________________________________
# Imports

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
import textwrap
from typing import Dict, List, Sequence, Tuple

from utilities.menu_banner_utilities import Banner

# __________________________________________________________________________
# Class Definitions

# ------------------------------------------------------------------------- class UseCase
@dataclass(frozen=True)
class UseCase:
    """Represents a PHTRS use case with optional include and extend relations.

    Attributes:
        name: Code and title of the use case.
        description: Brief explanation of the behavior.
        includes: Codes of use cases that this one includes.
        extends: Codes of use cases that extend this one.
    """

    name: str
    description: str
    includes: List[str] = field(default_factory=list)
    extends: List[str] = field(default_factory=list)

# ------------------------------------------------------------------------- end class UseCase

# ------------------------------------------------------------------------- class Actor
@dataclass(frozen=True)
class Actor:
    """Represents an actor interacting with PHTRS and its associated use cases.

    Attributes:
        name: Actor code and label.
        description: Brief role description.
        is_primary: Whether the actor is primary or supporting.
        is_abstract: Whether the actor is abstract/generalized.
        org_boundary: Organizational boundary classification
            ("Internal", "External", "External System").
        directness: Whether the actor interacts directly or indirectly.
        associated_use_cases: Use-case codes linked directly to this actor.
        notes: Optional additional notes about the actor.
    """

    name: str
    description: str

    # Classification captured from this conversation
    is_primary: bool
    is_abstract: bool
    org_boundary: str  # "Internal", "External", "External System"
    directness: str  # "Direct" / "Indirect"

    # Direct association lines (actor -> use case)
    associated_use_cases: List[str] = field(default_factory=list)

    # Optional notes
    notes: str = ""

# ------------------------------------------------------------------------- end class Actor

# =============================================================================
# Model builder (actors + use cases)
# =============================================================================

# __________________________________________________________________________
# Standalone Function Definitions

# -------------------------------------------------------------- build_model()
def build_model() -> tuple[Dict[str, Actor], Dict[str, UseCase], List[Tuple[str, str, str]]]:
    """Build the actor and use-case dictionaries plus actor generalizations.

    Returns:
        Tuple containing:
            Dict[str, Actor]: Actors keyed by identifier.
            Dict[str, UseCase]: Use cases keyed by identifier.
            List[Tuple[str, str, str]]: Actor generalization edges
                (child, parent, relationship label).
    """
    # -------------------------------------------------------------------------
    # Data Structure: use_cases (Dict[str, UseCase])
    # -------------------------------------------------------------------------
    # A dictionary mapping use-case identifiers (e.g., "UC01-Report Pothole") to
    # UseCase dataclass instances. Each UseCase contains:
    #   - name: The identifier and title (e.g., "UC01-Report Pothole")
    #   - description: A brief explanation of the behavior
    #   - includes: List of UC codes this use case always invokes (<<include>>)
    #   - extends: List of UC codes that optionally extend this use case (<<extend>>)
    #
    # Keys are the full use-case names (e.g., "UC01-Report Pothole") to keep
    # references stable when rendering tables, summaries, or mapping associations.
    # The UC## prefix follows UML naming conventions for traceability.
    # -------------------------------------------------------------------------
    # -----------------------------
    # Use cases (UC## / US##)
    # -----------------------------
    use_cases: Dict[str, UseCase] = {
        # Staff authentication (secure dashboard/mobile access)
        "US00-Authenticate Staff User": UseCase(
            name="US00-Authenticate Staff User",
            description=(
                "Representing a staff user being authenticating via a secure login."
            ),
        ),

        # Citizen-facing
        "UC01-Report Pothole": UseCase(
            name="UC01-Report Pothole",
            description=(
                "Representing a citizen reporting a pothole street address, severity/size (1–10), "
                "and location details (e.g., middle of road, curb)."
            ),
            includes=[
                "UC13-Validate Address",
                "UC14-Determine District",
                "UC15-Calculate Repair Priority",
                "UC03-Submit Damage Claim",
            ],
            extends=["UC11-Upload Photo"],
        ),
        "UC02-Track Report Status": UseCase(
            name="UC02-Track Report Status",
            description="Representing a citizen viewing  reported potholes updates.",
        ),
        "UC03-Submit Damage Claim": UseCase(
            name="UC03-Submit Damage Claim",
            description=(
                "Representing a citizen submitting a damage claim including the citizen’s name, "
                "address, phone number, damage type, and dollar amount "
                "(and a brief damage description)."
            ),
            extends=["UC12-Upload Report"],
        ),

        # Admin-facing
        "UC04-Review/Validate Pothole Report": UseCase(
            name="UC04-Review/Validate Pothole Report",
            description=(
                "Representing an admin employee reviewing submitted pothole reports "
                "and validating them."
            ),
            includes=["UC21-Report Database"],
        ),
        "UC05-Assign Repair Crew": UseCase(
            name="UC05-Assign Repair Crew",
            description=(
                "Representing an admin employee assigning/scheduling/queuing crew to a pothole "
                "repair."
            ),
            includes=["UC16-Create/Update Work Order", "UC17-Notify Crew / Citizen"],
        ),
        "UC06-Update Pothole Record": UseCase(
            name="UC06-Update Pothole Record",
            description=(
                "Representing an admin employee updating pothole record fields "
                "(status, notes, metrics, etc.)."
            ),
        ),
        "UC07-Generate Reports": UseCase(
            name="UC07-Generate Reports",
            description=(
                "Representing an admin employee creating reports "
                "(e.g., by district/priority/status/workload)."
            ),
        ),

        # Repair crew-facing
        "UC08-View Assigned Work Orders": UseCase(
            name="UC08-View Assigned Work Orders",
            description=(
                "Representing a repair crew employee viewing potholes repair assignments and "
                "associated work orders via a mobile/tablet interface."
            ),
        ),
        "UC09-Log Repair Work": UseCase(
            name="UC09-Log Repair Work",
            description=(
                "Representing a repair crew employee logging in hours of work, number of people "
                "on the crew, equipment assigned/used, and filler material used; it supports "
                "repair cost calculation."
            ),
            includes=[
                "UC10-Update Repair Status",
                "UC06-Update Pothole Record",
                "UC16-Create/Update Work Order",
            ],
        ),
        "UC10-Update Repair Status": UseCase(
            name="UC10-Update Repair Status",
            description=(
                "Representing a repair crew employee updating hole status (work in progress, "
                "repaired, temporary repair, not repaired)."
            ),
        ),

        # Optional citizen uploads
        "UC11-Upload Photo": UseCase(
            name="UC11-Upload Photo",
            description=(
                "Representing an optional photo upload to support a pothole report from a citizen."
            ),
        ),
        "UC12-Upload Report": UseCase(
            name="UC12-Upload Report",
            description=(
                "Representing an optional upload of a report (e.g., photos, receipts, attachments)."
            ),
            includes=["UC21-Report Database"],
        ),

        # System / supporting services
        "UC13-Validate Address": UseCase(
            name="UC13-Validate Address",
            description=(
                "Representing the system validating the street address (via GIS/address services)."
            ),
        ),
        "UC14-Determine District": UseCase(
            name="UC14-Determine District",
            description=(
                "Representing the system determining a city district from an address."
            ),
        ),
        "UC15-Calculate Repair Priority": UseCase(
            name="UC15-Calculate Repair Priority",
            description=(
                "Representing the system determining repair priority from pothole severity/size."
            ),
        ),
        "UC16-Create/Update Work Order": UseCase(
            name="UC16-Create/Update Work Order",
            description=(
                "Representing interface usage for creating/updating a work order associated with a "
                "pothole, including: pothole location and size, repair crew identifying number, "
                "number of people on the crew, equipment assigned, hours applied to repair, "
                "hole status, amount of filler material used, and cost of repair (calculated based "
                "on time, labor, equipment, and materials)."
            ),
        ),
        "UC17-Notify Crew / Citizen": UseCase(
            name="UC17-Notify Crew / Citizen",
            description=(
                "Representing the system sending notifications (email/SMS/in-app) to employees and "
                "citizens."
            ),
        ),

        # Damage claims processing
        "UC18-Review Damage Claim": UseCase(
            name="UC18-Review Damage Claim",
            description=(
                "Representing an admin employee reviewing and processing damage claim."
            ),
            includes=["UC19-Route Claim for Processing"],
        ),
        "UC19-Route Claim for Processing": UseCase(
            name="UC19-Route Claim for Processing",
            description=(
                "Representing a claim being sent to a claims processing function/department."
            ),
        ),
        "UC20-Update Claim Status": UseCase(
            name="UC20-Update Claim Status",
            description=(
                "Representing an admin/claims employee updating claim status/outcomes."
            ),
            includes=["UC17-Notify Crew / Citizen"],
        ),

        # NEW (Step 2): Report database
        "UC21-Report Database": UseCase(
            name="UC21-Report Database",
            description=(
                "Representing storing and retrieving reports in the PHTRS report database "
                "(report records and supporting attachments) for validation, tracking, and processing."
            ),
        ),
    }

    # __________________________________________________________________________
    # Data Structures - Global Dicts

    # -------------------------------------------------------------------------
    # Data Structure: actors (Dict[str, Actor])
    # -------------------------------------------------------------------------
    # A dictionary mapping actor identifiers (e.g., "A01-Citizen") to Actor
    # dataclass instances. Each Actor contains:
    #   - name: The identifier and label (e.g., "A01-Citizen")
    #   - description: A brief role description
    #   - is_primary: True if the actor initiates use cases (drives the system)
    #   - is_abstract: True if the actor is a generalization (not instantiated)
    #   - org_boundary: "Internal", "External", or "External System"
    #   - directness: "Direct" (interacts with UI) or "Indirect" (via other actors)
    #   - associated_use_cases: List of UC codes directly linked to this actor
    #   - notes: Optional additional context
    #
    # Keys follow the A## naming convention for UML traceability.
    # -------------------------------------------------------------------------
    # -----------------------------
    # Actors (A##)
    # -----------------------------
    actors: Dict[str, Actor] = {
        "A00-Staff User (abstract)": Actor(
            name="A00-Staff User (abstract)",
            description=(
                "The actor is an abstract actor of a general City/DPW staff that can access PHTRS "
                "interfaces."
            ),
            is_primary=True,
            is_abstract=True,
            org_boundary="Internal",
            directness="Indirect",
            associated_use_cases=["US00-Authenticate Staff User"],
            notes=(
                "Abstract generalization only; specializations carry the functional association "
                "lines."
            ),
        ),
        "A01-Citizen": Actor(
            name="A01-Citizen",
            description=(
                "The actor is a public user who can report potholes, track report status, "
                "and submit damage claims on the PHTRS website."
            ),
            is_primary=True,
            is_abstract=False,
            org_boundary="External",
            directness="Direct",
            associated_use_cases=["UC01-Report Pothole", "UC02-Track Report Status"],
        ),
        "A02-Public Works Admin": Actor(
            name="A02-Public Works Admin",
            description="The actor is a DPW employee who can manage reports and assign crews.",
            is_primary=True,
            is_abstract=False,
            org_boundary="Internal",
            directness="Direct",
            associated_use_cases=[
                "US00-Authenticate Staff User",
                "UC04-Review/Validate Pothole Report",
                "UC05-Assign Repair Crew",
                "UC06-Update Pothole Record",
                "UC07-Generate Reports",
                "UC18-Review Damage Claim",
                "UC20-Update Claim Status",
            ],
        ),
        "A03-Repair Crew": Actor(
            name="A03-Repair Crew",
            description=(
                "The actor is a DPW employee field crew member who can access and view work "
                "orders, log work, and update repair status."
            ),
            is_primary=True,
            is_abstract=False,
            org_boundary="Internal",
            directness="Direct",
            associated_use_cases=[
                "US00-Authenticate Staff User",
                "UC08-View Assigned Work Orders",
                "UC09-Log Repair Work",
                "UC10-Update Repair Status",
            ],
        ),
        "A04-Claims Processor": Actor(
            name="A04-Claims Processor",
            description=(
                "The actor is the city's claims function/department that can process routed claims "
                "and update claim outcomes/status."
            ),
            is_primary=False,
            is_abstract=False,
            org_boundary="Internal",
            directness="Direct",
            associated_use_cases=[
                "US00-Authenticate Staff User",
                "UC19-Route Claim for Processing",
                "UC20-Update Claim Status",
            ],
        ),
        "A05-GIS/Address Service": Actor(
            name="A05-GIS/Address Service",
            description=(
                "The actor is an external service/system that can validate addresses and determine districts."
            ),
            is_primary=False,
            is_abstract=False,
            org_boundary="External System",
            directness="Direct",
            associated_use_cases=["UC13-Validate Address", "UC14-Determine District"],
        ),
        "A06-Notification Service": Actor(
            name="A06-Notification Service",
            description=(
                "The actor is an external service/system that can be used to deliver notifications (email/SMS/in-app)."
            ),
            is_primary=False,
            is_abstract=False,
            org_boundary="External System",
            directness="Direct",
            associated_use_cases=["UC17-Notify Crew / Citizen"],
        ),
    }

    # -------------------------------------------------------------------------
    # Data Structure: actor_generalizations (List[Tuple[str, str, str]])
    # -------------------------------------------------------------------------
    # A list of tuples representing UML generalization (inheritance) relationships
    # between actors. Each tuple contains:
    #   - Element 0: Child actor name (the specialized role)
    #   - Element 1: Parent actor name (the generalized/abstract role)
    #   - Element 2: Relationship label (always "Generalization" here)
    #
    # In UML, generalization means the child actor inherits all associations from
    # the parent. Here, A02/A03/A04 all inherit the US00-Authenticate use case
    # from the abstract A00-Staff User actor.
    # -------------------------------------------------------------------------
    actor_generalizations: List[Tuple[str, str, str]] = [
        ("A02-Public Works Admin", "A00-Staff User (abstract)", "Generalization"),
        ("A03-Repair Crew", "A00-Staff User (abstract)", "Generalization"),
        ("A04-Claims Processor", "A00-Staff User (abstract)", "Generalization"),
    ]

    return actors, use_cases, actor_generalizations
# --------------------------------------------------------------

# =============================================================================
# Banner rendering helpers
# =============================================================================

# __________________________________________________________________________
# Global Constants / Variables

MAX_LINE_WIDTH = 120
# Banner typically adds left+right border padding similar to: "║ " + " ║"
_BANNER_OVERHEAD = 4
MAX_CONTENT_WIDTH = MAX_LINE_WIDTH - _BANNER_OVERHEAD
SECTION_DIVIDER = "-" * 88

# -------------------------------------------------------------- _wrap_text_preserve_indent()
def _wrap_text_preserve_indent(line: str, width: int = MAX_CONTENT_WIDTH) -> List[str]:
    """Wrap a single line to ``width`` while preserving indentation and bullets.

    Args:
        line: Line to wrap.
        width: Maximum content width for wrapping.

    Returns:
        Wrapped line segments preserving indentation.
    """
    if not line:
        return [""]

    # Calculate leading whitespace to preserve indentation on wrapped lines
    indent = len(line) - len(line.lstrip(" "))
    stripped = line.lstrip(" ")

    # -------------------------------------------------------------------------
    # BULLET LINE HANDLING: Lines starting with "- " (e.g., "    - UCxx: ...")
    # -------------------------------------------------------------------------
    # For bullet lines, we:
    #   1. Preserve the original indent + bullet prefix on the first line
    #   2. Use indent+2 on continuation lines (aligns text under the bullet)
    # -------------------------------------------------------------------------
    if stripped.startswith("- "):
        prefix = " " * indent + "- "
        body = stripped[2:]  # Text after "- "
        wrapped = textwrap.wrap(
            body,
            width=max(1, width - len(prefix)),
            break_long_words=False,
            break_on_hyphens=True,
        )
        if not wrapped:
            return [prefix.rstrip()]
        # First line: original prefix + first wrapped segment
        out = [prefix + wrapped[0]]
        # Continuation indent: 2 extra spaces to align under bullet text
        cont_indent = " " * (indent + 2)
        # Loop: Iterate over remaining wrapped segments (index 1 onwards)
        # Each segment 'w' is a chunk of text that fits within the width limit
        for w in wrapped[1:]:
            out.append(cont_indent + w)
        return out

    # -------------------------------------------------------------------------
    # DEFAULT LINE HANDLING: Non-bullet lines
    # -------------------------------------------------------------------------
    # For regular lines, we:
    #   1. Preserve the original indent on all lines (first + continuation)
    #   2. Wrap the body text to fit within (width - indent) characters
    # -------------------------------------------------------------------------
    prefix = " " * indent
    body = stripped
    wrapped = textwrap.wrap(
        body,
        width=max(1, width - len(prefix)),
        break_long_words=False,
        break_on_hyphens=True,
    )
    if not wrapped:
        return [prefix.rstrip()]
    # First line: prefix + first wrapped segment
    out = [prefix + wrapped[0]]
    # Loop: Iterate over remaining wrapped segments (index 1 onwards)
    # Each segment 'w' gets the same indent prefix as the first line
    for w in wrapped[1:]:
        out.append(prefix + w)
    return out
# --------------------------------------------------------------

# -------------------------------------------------------------- _wrap_lines()
def _wrap_lines(lines: Sequence[str], width: int = MAX_CONTENT_WIDTH) -> List[str]:
    """Wrap multiple lines while preserving indentation and bullets.

    Args:
        lines: Logical lines to wrap.
        width: Maximum width used for wrapping.

    Returns:
        Flattened list of wrapped lines.
    """
    # out: Accumulator list that collects all wrapped line segments
    out: List[str] = []
    # Loop: Iterate over each logical line 'ln' in the input sequence
    # Each logical line may produce multiple physical lines after wrapping
    # (e.g., a 200-char line becomes 2-3 lines when wrapped to 116 chars)
    for ln in lines:
        # extend() adds all wrapped segments from this line to the output
        out.extend(_wrap_text_preserve_indent(ln, width=width))
    return out
# --------------------------------------------------------------

# -------------------------------------------------------------- _choose_col_widths()
def _choose_col_widths(
    headers: Sequence[str],
    max_content_width: int = MAX_CONTENT_WIDTH,
) -> List[int]:
    """Choose column widths that keep the table within the maximum content width.

    Args:
        headers: Header labels used for the table.
        max_content_width: Maximum width available for table content.

    Returns:
        List of column widths sized to the available content width.
    """
    # Calculate space consumed by column separators: " | " = 3 chars each
    # For N columns, there are (N-1) separators
    sep_total = (len(headers) - 1) * 3  # for " | "
    available = max_content_width - sep_total

    # -------------------------------------------------------------------------
    # KNOWN TABLE LAYOUTS: Hardcoded widths for the two specific tables we render
    # -------------------------------------------------------------------------
    # These heuristic layouts allocate more space to columns with longer content
    # (e.g., Description) and less to short categorical columns (e.g., Directness).
    # -------------------------------------------------------------------------
    if list(headers) == [
        "Actor",
        "Description",
        "Primary/Secondary",
        "Abstract/Concrete",
        "Directness",
        "Org Boundary",
    ]:
        # Actors table: 6 columns, sep_total=15 => widths sum must be <= 101
        # Widths: Actor=22, Description=38, P/S=11, A/C=11, Direct=10, OrgBnd=9
        return [22, 38, 11, 11, 10, 9]
    if list(headers) == ["Use Case", "Description", "Includes", "Extends"]:
        # Use Cases table: 4 columns, sep_total=9 => widths sum must be <= 107
        # Widths: UC=24, Desc=44, Includes=21, Extends=18
        return [24, 44, 21, 18]

    # -------------------------------------------------------------------------
    # FALLBACK: Dynamic width distribution for unknown table structures
    # -------------------------------------------------------------------------
    n = len(headers)
    # Start with even distribution (minimum 6 chars per column)
    base = max(6, available // max(1, n))
    widths = [base] * n
    # Give first 2 columns +1 char (often name/description need more space)
    for i in range(min(2, n)):
        widths[i] += 1
    # Shrink loop: If total exceeds available, reduce columns from right to left
    # until we fit, but never shrink below 6 chars minimum
    while sum(widths) > available and any(w > 6 for w in widths):
        # Inner loop: Iterate columns in reverse order (rightmost first)
        for i in range(n - 1, -1, -1):
            if sum(widths) <= available:
                break
            if widths[i] > 6:
                widths[i] -= 1
    return widths
# --------------------------------------------------------------

# -------------------------------------------------------------- _cell_lines()
def _cell_lines(cell: str, width: int, is_header: bool = False) -> List[str]:
    """Wrap a cell to a width, preserving explicit newlines.

    Args:
        cell: Cell content to wrap.
        width: Maximum width for wrapping.
        is_header: Whether the cell represents a header.

    Returns:
        Lines of wrapped cell content.
    """
    # Normalize cell content: None becomes empty string
    s = "" if cell is None else str(cell)
    # Special handling for headers like "Primary/Secondary": add space after "/"
    # so textwrap can break at the "/" if needed (e.g., "Primary/ Secondary")
    if is_header and "/" in s and " " not in s:
        s = s.replace("/", "/ ")

    # Split on explicit newlines (e.g., UC includes list uses "\n" between items)
    # parts: List of line segments from the original cell content
    parts = s.splitlines() or [""]
    # out: Accumulator for all wrapped line segments
    out: List[str] = []
    # Loop: Iterate over each explicit line segment 'part' in the cell
    # Each part may itself be wrapped into multiple lines if it exceeds width
    for part in parts:
        if part == "":
            out.append("")
            continue
        # Wrap this segment to fit within the column width
        wrapped = textwrap.wrap(
            part,
            width=max(1, width),
            break_long_words=False,
            break_on_hyphens=True,
        )
        # extend() adds all wrapped segments; if wrap returned empty, add ""
        out.extend(wrapped or [""])
    return out or [""]
# --------------------------------------------------------------

# -------------------------------------------------------------- _format_table()
def _format_table(
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    *,
    row_spacing: int = 1,
) -> List[str]:
    """Format rows into wrapped table lines respecting ``MAX_CONTENT_WIDTH``.

    Args:
        headers: Column headers.
        rows: Row data aligning to headers.
        row_spacing: Spacer rows between logical records.

    Returns:
        Wrapped lines ready for banner rendering.
    """
    # Get column widths (hardcoded for known tables, or dynamically calculated)
    col_widths = _choose_col_widths(headers, max_content_width=MAX_CONTENT_WIDTH)

    # -------------------------------------------------------------------------
    # NESTED FUNCTION: build_physical_lines
    # -------------------------------------------------------------------------
    # Converts a single logical row (list of cell strings) into multiple
    # physical lines. This is needed because cells may wrap to multiple lines.
    # -------------------------------------------------------------------------
    def build_physical_lines(cells: Sequence[str], is_header: bool = False) -> List[str]:
        # wrapped_cols: List of lists; each inner list contains the wrapped
        # line segments for one column. Example for a 4-column row:
        # [["UC01-Report", "Pothole"], ["Description..."], ["UC13", "UC14"], ["UC11"]]
        wrapped_cols = [
            _cell_lines(cells[i], col_widths[i], is_header=is_header)
            for i in range(len(headers))
        ]
        # Height: Maximum number of physical lines needed across all columns
        # in this row. All columns must render this many lines (padding with "").
        height = max(len(w) for w in wrapped_cols)
        out_lines: List[str] = []
        # Outer loop: Iterate over each physical row index 'r' (0 to height-1)
        # This builds the table row-by-row, where each iteration creates one
        # horizontal line of the table output.
        for r in range(height):
            parts = []
            # Inner loop: Iterate over each column index 'c'
            # Collects the r-th line segment from each column
            for c in range(len(headers)):
                # Get the r-th line of this column, or "" if column is shorter
                txt = wrapped_cols[c][r] if r < len(wrapped_cols[c]) else ""
                # Left-justify and pad to column width for alignment
                parts.append(txt.ljust(col_widths[c]))
            # Join columns with " | " separator to form one table line
            out_lines.append(" | ".join(parts))
        return out_lines

    # Build header row(s) - may be multiple lines if headers wrap
    header_lines = build_physical_lines(headers, is_header=True)
    # Separator line: dashes under each column, joined by "-+-"
    # Example: "----------------------+-----------------------------------------+-..."
    sep_line = "-+-".join("-" * w for w in col_widths)

    # Spacer line: empty cells for visual separation between logical rows
    spacer_line = " | ".join("".ljust(w) for w in col_widths)

    # -------------------------------------------------------------------------
    # DATA ROWS LOOP: Process each logical row from the input 'rows' sequence
    # -------------------------------------------------------------------------
    # data_lines: Accumulator for all physical lines from all data rows
    data_lines: List[str] = []
    # Loop: Iterate over each logical row with its index 'idx'
    # - row: A sequence of cell strings (one per column)
    # - idx: Row index, used to determine if we should add a spacer after
    for idx, row in enumerate(rows):
        # Convert this logical row to physical lines and add to accumulator
        data_lines.extend(build_physical_lines(row, is_header=False))
        # Add spacer row(s) between logical records for readability
        # Skip spacer after the last row (idx == len(rows) - 1)
        if row_spacing > 0 and idx != len(rows) - 1:
            # Inner loop: Add 'row_spacing' number of blank spacer lines
            for _ in range(row_spacing):
                data_lines.append(spacer_line)

    # -------------------------------------------------------------------------
    # FINAL ASSEMBLY: Combine headers, separator, and data; apply safety wrap
    # -------------------------------------------------------------------------
    # All lines should fit within MAX_CONTENT_WIDTH, but we apply a defensive
    # wrap in case a future change introduces overflow.
    final_lines: List[str] = []
    # Loop: Iterate over all lines (header + separator + data)
    for ln in [*header_lines, sep_line, *data_lines]:
        if len(ln) <= MAX_CONTENT_WIDTH:
            final_lines.append(ln)
        else:
            # Defensive wrap for any overflow lines
            final_lines.extend(
                textwrap.wrap(
                    ln,
                    width=MAX_CONTENT_WIDTH,
                    break_long_words=False,
                    break_on_hyphens=True,
                )
            )
    return final_lines
# --------------------------------------------------------------

# -------------------------------------------------------------- banner_table()
def banner_table(title: str, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    """Render a banner-wrapped table.

    Args:
        title: Title to center at the top of the banner.
        headers: Table column headers.
        rows: Table rows; each row aligns to the headers.

    Returns:
        Rendered banner string containing the table.
    """
    # -------------------------------------------------------------------------
    # Data Structure: content (List[Tuple])
    # -------------------------------------------------------------------------
    # A list of tuples for the Banner class. Each tuple contains:
    #   - Element 0: Text content for this line
    #   - Element 1: Alignment ("center" or "left")
    #   - Element 2 (optional): Bold flag (True for title)
    # The Banner class renders these as a bordered box with aligned content.
    # -------------------------------------------------------------------------
    content = [(title, "center", True)]  # Title line, centered and bold
    # Loop: Iterate over each formatted table line from _format_table()
    # Each 'ln' is a pre-formatted string (e.g., "Actor | Description | ...")
    for ln in _format_table(headers, rows):
        content.append((ln, "left"))  # Table lines are left-aligned
    return Banner(content).render()
# --------------------------------------------------------------

# -------------------------------------------------------------- banner_block()
def banner_block(title: str, lines: Sequence[str]) -> str:
    """Render a banner-wrapped block of text.

    Args:
        title: Title to center at the top of the banner.
        lines: Text lines to include in the block.

    Returns:
        Rendered banner string containing the block.
    """
    # -------------------------------------------------------------------------
    # Data Structure: content (List[Tuple])
    # -------------------------------------------------------------------------
    # Similar to banner_table(), this builds a list of tuples for the Banner class.
    # The difference is that lines are wrapped text (not table rows).
    # -------------------------------------------------------------------------
    content = [(title, "center", True)]  # Title line, centered and bold
    # Loop: Iterate over each wrapped line from _wrap_lines()
    # _wrap_lines() handles word wrapping and indentation preservation
    for ln in _wrap_lines(lines, width=MAX_CONTENT_WIDTH):
        content.append((ln, "left"))  # Content lines are left-aligned
    return Banner(content).render()
# --------------------------------------------------------------


# =============================================================================
# Required outputs Actors
# =============================================================================

# -------------------------------------------------------------- actors_table()
def actors_table(actors: Dict[str, Actor]) -> str:
    """Render a bannered table of actors and key attributes.

    Args:
        actors: Mapping of actor codes to actor data.

    Returns:
        Rendered actor table.
    """
    # -------------------------------------------------------------------------
    # Data Structure: rows (List[List[str]])
    # -------------------------------------------------------------------------
    # A list of row data, where each row is a list of 6 cell strings:
    #   [name, description, primary/secondary, abstract/concrete, directness, org_boundary]
    # This structure aligns with the 6-column header defined below.
    # -------------------------------------------------------------------------
    rows = []
    # Loop: Iterate over actor keys in sorted order (A00, A01, A02, ...)
    # Sorted iteration ensures deterministic output for grading and diffing.
    # - a_key: The dictionary key (e.g., "A01-Citizen")
    # - a: The Actor dataclass instance with all attributes
    for a_key in sorted(actors.keys()):
        a = actors[a_key]
        # Build a row with 6 cells matching the header columns
        rows.append([
            a.name,  # Column 1: Actor identifier and label
            a.description,  # Column 2: Brief role description
            "Primary" if a.is_primary else "Secondary",  # Column 3: Actor type
            "Abstract" if a.is_abstract else "Concrete",  # Column 4: Instantiation
            a.directness,  # Column 5: Direct/Indirect interaction
            a.org_boundary,  # Column 6: Internal/External/External System
        ])
    return banner_table(
        "PHTRS Actors",
        [
            "Actor",
            "Description",
            "Primary/Secondary",
            "Abstract/Concrete",
            "Directness",
            "Org Boundary",
        ],
        rows,
    )
# --------------------------------------------------------------

# -------------------------------------------------------------- use_cases_table()
def use_cases_table(use_cases: Dict[str, UseCase]) -> str:
    """Render a bannered table of use cases.

    Args:
        use_cases: Mapping of use case codes to use-case data.

    Returns:
        Rendered use-case table.
    """
    # -------------------------------------------------------------------------
    # Data Structure: rows (List[List[str]])
    # -------------------------------------------------------------------------
    # A list of row data, where each row is a list of 4 cell strings:
    #   [name, description, includes (newline-separated), extends (newline-separated)]
    # The includes/extends cells use "\n" to separate multiple UC codes, which
    # _cell_lines() will split into separate lines within the cell.
    # -------------------------------------------------------------------------
    rows = []
    # Loop: Iterate over use-case keys in sorted order (UC01, UC02, ..., US00)
    # Sorted iteration keeps table output stable and deterministic across runs.
    # - uc_key: The dictionary key (e.g., "UC01-Report Pothole")
    # - uc: The UseCase dataclass instance with name, description, includes, extends
    for uc_key in sorted(use_cases.keys()):
        uc = use_cases[uc_key]
        # Build a row with 4 cells matching the header columns
        # Note: "\n".join() creates a newline-separated string from the lists
        # Example: ["UC13-Validate", "UC14-Determine"] → "UC13-Validate\nUC14-Determine"
        rows.append([
            uc.name,  # Column 1: Use case identifier and title
            uc.description,  # Column 2: Brief behavior explanation
            "\n".join(uc.includes),  # Column 3: <<include>> relationships (multi-line)
            "\n".join(uc.extends),  # Column 4: <<extend>> relationships (multi-line)
        ])
    return banner_table(
        "PHTRS Use Cases",
        ["Use Case", "Description", "Includes", "Extends"],
        rows,
    )
# --------------------------------------------------------------

# -------------------------------------------------------------- actor_summaries()
def actor_summaries(actors: Dict[str, Actor], use_cases: Dict[str, UseCase]) -> str:
    """Render actor summaries with their associated use cases.

    Args:
        actors: Mapping of actor codes to actor data.
        use_cases: Mapping of use case codes to use-case data.

    Returns:
        Rendered banner summarizing actor relationships.
    """
    # -------------------------------------------------------------------------
    # Data Structure: lines (List[str])
    # -------------------------------------------------------------------------
    # An accumulator list that builds up the human-readable summary output.
    # Each element is a single line of text. The structure for each actor is:
    #   - Line 1: "A##-Name — description"
    #   - Line 2 (optional): "  Note: additional notes"
    #   - Line 3: "  Associated use cases:"
    #   - Lines 4+: "    - UC##-Name: description" (one per associated use case)
    #   - Final line: "" (blank line separator between actors)
    # -------------------------------------------------------------------------
    lines: List[str] = []

    # -------------------------------------------------------------------------
    # OUTER LOOP: Iterate over each actor in sorted key order
    # -------------------------------------------------------------------------
    # Sorted iteration (A00, A01, A02, ...) keeps summaries stable and easy to
    # scan. Each iteration builds the summary block for one actor.
    # - a_key: The dictionary key (e.g., "A01-Citizen")
    # - a: The Actor dataclass instance
    # -------------------------------------------------------------------------
    for a_key in sorted(actors.keys()):
        a = actors[a_key]
        # Actor header line: name and description
        lines.append(f"{a.name} — {a.description}")
        # Optional notes line (only if actor has notes)
        if a.notes:
            lines.append(f"  Note: {a.notes}")

        # Handle actors with no associated use cases
        if not a.associated_use_cases:
            lines.append("  Associated use cases: (none)")
            lines.append("")  # Blank line separator
            continue

        # Section header for associated use cases
        lines.append("  Associated use cases:")

        # -------------------------------------------------------------------------
        # INNER LOOP: Iterate over each use case associated with this actor
        # -------------------------------------------------------------------------
        # - uc_name: The use case key from the actor's associated_use_cases list
        #   (e.g., "UC01-Report Pothole")
        # - uc: The UseCase dataclass looked up from use_cases dict (or None)
        # -------------------------------------------------------------------------
        for uc_name in a.associated_use_cases:
            # Look up the use case in the use_cases dictionary
            uc = use_cases.get(uc_name)
            if uc is None:
                # Safety fallback: use case not found in dictionary
                lines.append(f"    - {uc_name} (not found)")
            else:
                # Normal case: format as bullet with UC name and description
                lines.append(f"    - {uc.name}: {uc.description}")

        # Blank line separator after each actor's block
        lines.append("")

    return banner_block("Actor Summaries", lines)
# --------------------------------------------------------------

# -------------------------------------------------------------- main()
def main() -> None:
    """Render the four required outputs for the PHTRS model."""
    # -------------------------------------------------------------------------
    # Build the domain model: actors dict, use_cases dict, and generalizations list
    # -------------------------------------------------------------------------
    # actors: Dict[str, Actor] - All actors keyed by their A##-Name identifier
    # use_cases: Dict[str, UseCase] - All use cases keyed by their UC##-Name identifier
    # generalizations: List[Tuple[str, str, str]] - Actor inheritance relationships
    # -------------------------------------------------------------------------
    actors, use_cases, generalizations = build_model()

    # -------------------------------------------------------------------------
    # OUTPUT 1: Actors Table
    # -------------------------------------------------------------------------
    # Renders a bannered table showing all actors with their attributes
    # (name, description, primary/secondary, abstract/concrete, directness, org boundary)
    # -------------------------------------------------------------------------
    print(actors_table(actors))
    print()

    # -------------------------------------------------------------------------
    # OUTPUT 2: Use Cases Table
    # -------------------------------------------------------------------------
    # Renders a bannered table showing all use cases with their relationships
    # (name, description, includes list, extends list)
    # -------------------------------------------------------------------------
    print(use_cases_table(use_cases))
    print()

    # -------------------------------------------------------------------------
    # OUTPUT 3: Actor Summaries
    # -------------------------------------------------------------------------
    # Renders a bannered block showing each actor with their associated use cases
    # and descriptions (the assignment's primary "actor summary" requirement)
    # -------------------------------------------------------------------------
    print(actor_summaries(actors, use_cases))
    print()

    # -------------------------------------------------------------------------
    # OUTPUT 4: Diagram Structure Summary
    # -------------------------------------------------------------------------
    # Renders a narrative text summary describing the diagram's structure,
    # including counts, workflows, and relationship types
    # -------------------------------------------------------------------------
    summary = """----------------------------------------------------------------------------------------
Diagram Structure Summary
----------------------------------------------------------------------------------------
System: PHTRS (Web-Based System)
Totals:
   Actors=7 (Primary=3, Secondary=3, Abstract=1)
   Use Cases=22
   Relationships=35 (Actor–UseCase=17, <<include>>=13, <<extend>>=2, Actor Generalization=3).
----------------------------------------------------------------------------------------
Actors and intent (from the PHTRS Actors table):
- Primary: A01-Citizen, A02-Public Works Admin, A03-Repair Crew
- Secondary: A04-Claims Processor, A05-GIS/Address Service, A06-Notification Service
- Abstract: A00-Staff User (abstract)
----------------------------------------------------------------------------------------
High-level structure:
- Citizen flow: UC01-Report Pothole → UC02-Track Report Status (report a pothole, then track status).
- Staff access is gated by authentication: US00-Authenticate Staff User.
- Operational flow: staff review/validate reports, assign crews and work orders, then crews log work and update status
  (UC04-Review/Validate Pothole Report, UC05-Assign Repair Crew, UC09-Log Repair Work).
- Claims flow: UC03-Submit Damage Claim supports downstream claim review and status updates (UC18-Review Damage Claim,
  UC20-Update Claim Status).
- Report storage: UC21-Report Database is included where citizen reports/evidence are stored/retrieved (e.g., via
  UC04-Review/Validate Pothole Report, UC12-Upload Report).
- Notifications: UC17-Notify Crew / Citizen supports key workflow transitions (assignment and claim status updates).

Optional behavior modeled with <<extend>>: UC11-Upload Photo → UC01-Report Pothole; UC12-Upload Report → UC03-Submit
Damage Claim.
----------------------------------------------------------------------------------------
Relationships:
- Full line "――――" Association Relationship is used to link an actor to a use case.
- Arrow dotted line <<include>> "--->" Association Relationship is used to represent use cases included in other use
  cases.
- Arrow dotted line <<extend>> "<---" Association Interface Relationship is an inheritance relationship between use
  cases (child extends parent).
 - Arrow full line "<|――" Generalization is also an inheritance relationship, but between actors (child of parent).
----------------------------------------------------------------------------------------
    """
    print(SECTION_DIVIDER)
    print("Diagram Structure Summary")
    print(SECTION_DIVIDER)
    print(summary)
# --------------------------------------------------------------


# __________________________________________________________________________
# Module Initialization / Main Execution Guard
# This code runs only when the file is executed
# --------------------------------------------------------------------------------- main_guard
if __name__ == "__main__":
    main()
# --------------------------------------------------------------------------------- end main_guard

# __________________________________________________________________________
# End of File
# -------------------------------------------------------------------------

