# -----------------------------------------------------------------------------
# Project: UCI SMS Spam Multinomial Naive Bayes Classifier
# Module Type: executable script
# Author: Alexander S. Ricciardi
# Last Updated: 2026-08-30
# -----------------------------------------------------------------------------
# Course: CSC510 - Foundations of Artificial Intelligence
# Professor: Dr. Isaac Gang
# Term: Fall A (26FA) - 2026
# Assignment: Critical Thinking Module 6 - Naive Bayes Classifier
# -----------------------------------------------------------------------------
# My Project Description:
# The program trains a Multinomial Naive Bayes classifier on the UCI SMS Spam
# Collection. It converts messages into word-frequency counts, calculates class
# priors and smoothed word likelihoods, and classifies one message as HAM or SPAM.
# The manual probability calculation is compared with scikit-learn's result.
# -----------------------------------------------------------------------------
# Assignment Requirements: Naive Bayes Classifier
# 
# Naive Bayes classifiers are quick and easy to code in Python and are very efficient. 
# Naive Bayes classifiers are based on Bayes' Theorem and assume independence among 
# predictors (hence the "Naive" terminology). Not only are Naive Bayes classifiers handy 
# and straightforward in a pinch, but they also outperform many other methods without the 
# need for advanced feature engineering of the data.
#
# Read the following article for further information on Naive Bayes classification: 
# https://www.ibm.com/think/topics/naive-bayes
#
# Using scikit-learn, write a Naive Bayes classifier in Python. It can be single or multiple 
# features. Submit the classifier in the form of an executable Python script 
# alongside basic instructions for testing.
#
# Your Naive Bayes classification script should allow you to do the following:
#
# - Calculate the posterior probability by converting the dataset into a frequency 
#   table.
# - Create a "Likelihood" table by finding relevant probabilities.
# - Calculate the posterior probability for each class.
# - Correct Zero Probability errors using Laplacian correction.
#
# Your classifier may use a Gaussian, Multinomial, or Bernoulli model, 
# depending on your chosen function. Your classifier must properly display 
# its probability prediction based on its input data.
#
# Check out scikit-learn and its documentation at the following website:
# https://scikit-learn.org/stable/
#
# Assignment summarization check list:
#
# - Use a scikit-learn Naive Bayes classifier.
# - Convert the dataset into class and word frequency tables.
# - Create a likelihood table with relevant conditional probabilities.
# - Calculate and display the posterior probability for each class.
# - Correct zero-probability errors with Laplace add-one smoothing.
# - Display a clear probability-based prediction.
# - Include an executable script and basic testing instructions.
# -----------------------------------------------------------------------------
# Data Source:
# - UCI SMS Spam Collection, 5,574 labeled messages.
# - Dataset DOI: https://doi.org/10.24432/C5CC84
#
# Dependencies:
# - Standard Library: argparse, io, os, shutil, sys, tempfile, textwrap,
#   urllib, zipfile, collections, dataclasses, pathlib, typing
# - Third Party: NumPy, scikit-learn
#
# Requirements:
# - Python 3.11+
# - NumPy 1.26+
# - scikit-learn 1.4+
# -----------------------------------------------------------------------------

"""Format the classifier's bounded, optional-color terminal output.

This module detects ANSI support and prints headings, wrapped paragraphs, equations,
aligned values, and fixed-width tables within the configured display width. It also
manages optional pauses between teaching sections. It does not load data, train the
model, or calculate probabilities.
"""


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

import os
import sys
import textwrap
from typing import Sequence

# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_config import ANSI_BOLD, ANSI_CYAN, ANSI_RESET, DISPLAY_WIDTH


# _____________________________________________________________________________
# =============================================================================
# TERMINAL DISPLAY HELPERS
# =============================================================================
#
# These helpers format text, equations, labels, and tables. They do not calculate
# model probabilities or change the classifier. Keeping display code separate
# makes the mathematical functions easier to inspect and verify.
# _____________________________________________________________________________


# --- terminal_supports_color()
def terminal_supports_color(no_color: bool) -> bool:
    """Return True only when ANSI color is allowed and useful.
    
    Args:
        no_color: Whether to disable color output
        
    Returns:
        bool: True if color output is allowed and useful, False otherwise
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display configuration.
    """

    # Explicit user choice and the cross-tool NO_COLOR convention take priority.
    if no_color or os.environ.get("NO_COLOR") is not None:
        return False

    # A dumb terminal does not advertise ANSI cursor or color support.
    if os.environ.get("TERM", "").lower() == "dumb":
        return False

    # Redirected output should remain plain text for grading and file capture.
    return bool(getattr(sys.stdout, "isatty", lambda: False)())
# ---


# --- style_text()
def style_text(text: str, ansi_code: str, use_color: bool) -> str:
    """Apply one ANSI style when color output is enabled.
    
    Args:
        text: Text to style
        ansi_code: ANSI color code
        use_color: Whether to use color output
        
    Returns:
        str: Styled text
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display configuration.
    """

    return f"{ansi_code}{text}{ANSI_RESET}" if use_color else text
# ---


# --- truncate_cell()
def truncate_cell(value: object, width: int) -> str:
    """Fit one table cell to a fixed width with an explicit ellipsis.
    
    Args:
        value: Value to truncate
        width: Maximum width of the truncated value
        
    Returns:
        str: Truncated value
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    text = str(value)

    # Preserve complete values when they already fit the assigned column.
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."
# ---


# --- print_heading()
def print_heading(title: str, use_color: bool = False) -> None:
    """Print one 92-character top-level heading.
    
    Args:
        title: Title to print
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    print()
    print("=" * DISPLAY_WIDTH)
    print(style_text(title.center(DISPLAY_WIDTH), ANSI_BOLD + ANSI_CYAN, use_color))
    print("=" * DISPLAY_WIDTH)
# ---


# --- print_subheading()
def print_subheading(title: str, use_color: bool = False) -> None:
    """Print one bounded subsection heading.
    
    Args:
        title: Title to print
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    print()
    print(style_text(title, ANSI_BOLD, use_color))
    print("-" * DISPLAY_WIDTH)
# ---


# --- print_paragraph()
def print_paragraph(
    text: str,
    indent: int = 2,
    *,
    ansi_code: str | None = None,
    use_color: bool = False,
) -> None:
    """Wrap text within the 92-character design width and apply an optional style.
    
    Args:
        text: Text to print
        indent: Indentation level
        ansi_code: Optional ANSI style applied after line wrapping
        use_color: Whether to apply the optional ANSI style
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    prefix = " " * indent
    wrapper = textwrap.TextWrapper(
        width=max(20, DISPLAY_WIDTH - indent),
        initial_indent=prefix,
        subsequent_indent=prefix,
        replace_whitespace=True,
        drop_whitespace=True,
    )
    wrapped_text = wrapper.fill(text)
    if ansi_code is not None:
        wrapped_text = style_text(wrapped_text, ansi_code, use_color)
    print(wrapped_text)
# ---


# Equation display boundary: This helper renders equation text exactly as supplied.
# It does not evaluate an equation or change any probability value.
# --- print_equation()
def print_equation(lines: Sequence[str]) -> None:
    """Print one equation block while preserving line breaks.
    
    Args:
        lines: Sequence of strings representing equation lines
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    for line in lines:
        if not line:
            print()
        else:
            print(f"    {line}")
# ---


# --- print_labeled_value()
def print_labeled_value(label: str, value: object, label_width: int = 31) -> None:
    """Print an aligned label/value row.
    
    Args:
        label: Label to print
        value: Value to print
        label_width: Width of the label column
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    label_text = truncate_cell(label, label_width)
    value_text = str(value)
    available = DISPLAY_WIDTH - label_width - 5
    if len(value_text) <= available:
        print(f"  {label_text:<{label_width}} : {value_text}")
        return

    wrapped_lines = textwrap.wrap(value_text, width=max(20, available))
    print(f"  {label_text:<{label_width}} : {wrapped_lines[0]}")
    continuation_prefix = " " * (label_width + 5)
    for line in wrapped_lines[1:]:
        print(continuation_prefix + line)
# ---


# --- print_table()
def print_table(
    headers: Sequence[str],
    rows: Sequence[Sequence[object]],
    widths: Sequence[int],
    alignments: Sequence[str] | None = None,
) -> None:
    """Print a fixed-width ASCII table that fits `DISPLAY_WIDTH`.

    Args:
        headers: Column headings.
        rows: Table data rows.
        widths: Exact width of each column.
        alignments: Optional `<`, `>`, or `^` alignment per column.
    """

    # VALIDATION: Column metadata and every data row must describe one shape.
    if len(headers) != len(widths):
        raise ValueError("headers and widths must have the same length")
    if any(len(row) != len(headers) for row in rows):
        raise ValueError("every table row must match the header length")

    # Left alignment is the default unless a numeric column requests otherwise.
    alignments = alignments or ["<"] * len(headers)
    separator_width = 3 * (len(headers) - 1)

    # INVARIANT: Header, separator, and data rows stay inside DISPLAY_WIDTH.
    if sum(widths) + separator_width > DISPLAY_WIDTH:
        raise ValueError("table width exceeds DISPLAY_WIDTH")

    # Format headers and data through the same truncation and alignment rule.
    def format_row(values: Sequence[object]) -> str:
        cells: list[str] = []
        for value, width, alignment in zip(values, widths, alignments):
            cell = truncate_cell(value, width)
            cells.append(f"{cell:{alignment}{width}}")
        return " | ".join(cells)

    print(format_row(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(format_row(row))
# ---


# --- pause_for_user()
def pause_for_user(enabled: bool) -> None:
    """Pause between teaching sections only in interactive mode.
    
    Args:
        enabled: Whether to pause for user input
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    # Noninteractive, demo, message, and no-pause modes return immediately.
    if not enabled:
        return
    try:
        input("\nPress Enter to continue...")
    except EOFError:
        print()
# ---
