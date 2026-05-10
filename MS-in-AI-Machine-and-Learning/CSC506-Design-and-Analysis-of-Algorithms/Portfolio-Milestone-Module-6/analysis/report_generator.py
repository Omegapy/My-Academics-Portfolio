# -------------------------------------------------------------------------
# File: report_generator.py
# Project: Portfolio Milestone Module 6 - Algorithm and Data Structure
#   Comparison Tool
# Author: Alexander Ricciardi
# Date: 2026-04-21
# File Path: Portfolio-Milestone-Module-6/analysis/report_generator.py
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
# Module 6 is a Streamlit-centered comparison tool that demonstrates plain
# BST operations, map-style tree storage, balance detection, and TreeMap
# versus ListMap search analysis with written evaluation artifacts.
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Convert raw benchmark rows into display-ready tables and Markdown blocks.
# - Generate saved chart artifacts used by the Streamlit analysis tabs.
# - Refresh CSV summaries and chart outputs from the benchmark result file.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Global Constants / Variables: stable chart artifact filename contracts.
# - Function Definitions: table builders and Markdown formatting helpers.
# - Function Definitions: chart generation and artifact refresh helpers.
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: pathlib
# - Third-Party: matplotlib, pandas
# - Local Project Modules:
#   - analysis.benchmark_search
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# - Imported by the Streamlit analysis tabs to render tables and charts.
# - Imported by maintenance workflows to regenerate CSV and PNG artifacts.
# - Not intended to run as a standalone script.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Report and chart-generation helpers.

It turns raw benchmark rows into summary tables, Markdown-ready
content, and saved chart images.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations
from pathlib import Path
import matplotlib
import pandas as pd
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# Benchmark search modules
from analysis.benchmark_search import (
    compute_balance_summary,
    compute_speedup_summary,
    load_results_csv,
)

# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# REPORT ARTIFACT CONFIGURATION
# ========================================================================
# These stable filenames are referenced by the UI and by the saved analysis
# folder, so they act as the contract for generated chart artifacts.
#
# Chart artifact keys map internal report names to stable saved filenames.
# These lookup keys are reused by both report generation and Streamlit display code.
CHART_FILENAMES: dict[str, str] = {
    # Runtime comparison artifacts
    "tree_vs_list": "tree_vs_list_search.png",  # TreeMap vs ListMap runtime line chart
    "speedup": "search_speedup.png",  # Relative speedup chart for TreeMap over ListMap
    # Tree-shape analysis artifacts
    "height": "bst_height_growth.png",  # Height growth chart by insertion scenario
    "balance": "balance_detection_profile.png",  # Balanced/unbalanced profile chart
}
"""Stable filenames used for saved benchmark chart artifacts."""


# __________________________________________________________________________
# Function Definitions
# ========================================================================
# TABLE / MARKDOWN FORMATTERS
# ========================================================================
# Formatting helpers convert numeric benchmark outputs into display-friendly
# tables for Streamlit tabs and Markdown placeholder substitution.
#
# --------------------------------------------------------------- _format_float()
def _format_float(value: object | None, digits: int = 4) -> str:
    """Return a compact float string or ``"-"`` for missing values.

    Logic:
        This helper keeps float display formatting consistent across analysis
        tables.
        1. Return ``"-"`` when the value is missing.
        2. Format present values to the requested decimal precision.
        3. Return the formatted string.
    """
    if value is None or pd.isna(value):
        return "-"
    return f"{float(value):.{digits}f}"
# --------------------------------------------------------------- 

# --------------------------------------------------------------- _format_int()
def _format_int(value: object | None) -> str:
    """Return a compact integer string or ``"-"`` for missing values.

    Logic:
        This helper keeps integer display formatting consistent across
        analysis tables.
        1. Return ``"-"`` when the value is missing.
        2. Format present values with integer comma separators.
        3. Return the formatted string.
    """
    if value is None or pd.isna(value):
        return "-"
    return f"{int(value):,}"
# ---------------------------------------------------------------

# --------------------------------------------------------------- _format_bool()
def _format_bool(value: object | None) -> str:
    """Return ``Yes``/``No``/``-`` for optional boolean values.

    Logic:
        This helper normalizes optional boolean display values for tables and
        Markdown.
        1. Return ``"-"`` when the value is missing.
        2. Convert present values into ``Yes`` or ``No``.
        3. Return the normalized label.
    """
    if value is None or pd.isna(value):
        return "-"
    return "Yes" if bool(value) else "No"
# --------------------------------------------------------------- 

# --------------------------------------------------------------- build_benchmark_table()
def build_benchmark_table(results_df: pd.DataFrame) -> pd.DataFrame:
    """Build a sorted benchmark results table for display or export.

    Logic:
        This function reduces raw benchmark rows into the stable display schema
        used by the app and reports.
        1. Return an empty table with the expected columns when no data exists.
        2. Select only the display-facing benchmark columns.
        3. Sort the rows into a stable scenario and size order.
    """
    # VALIDATION: preserve a stable empty schema when no benchmark rows exist yet.
    if results_df.empty:
        return pd.DataFrame(
            columns=[
                "method",
                "scenario",
                "query_mode",
                "size",
                "time_ms",
                "height",
                "is_balanced",
            ]
        )

    return (
        results_df[
            ["method", "scenario", "query_mode", "size", "time_ms", "height", "is_balanced"]
        ]
        .sort_values(["scenario", "query_mode", "size", "method"])
        .reset_index(drop=True)
    )
# --------------------------------------------------------------- 

# --------------------------------------------------------------- build_speedup_summary_table()
def build_speedup_summary_table(results_df: pd.DataFrame) -> pd.DataFrame:
    """Build the ListMap-to-TreeMap speedup summary table.

    Logic:
        This function exposes the shared speedup summary for display layers.
        1. Delegate the computation to the benchmark summary helper.
        2. Return the resulting speedup DataFrame unchanged.
    """
    return compute_speedup_summary(results_df)
# --------------------------------------------------------------- 

# --------------------------------------------------------------- build_balance_summary_table()
def build_balance_summary_table(results_df: pd.DataFrame) -> pd.DataFrame:
    """Build the TreeMap height-and-balance summary table.

    Logic:
        This function exposes the shared balance summary for display layers.
        1. Delegate the computation to the balance-summary helper.
        2. Return the resulting summary DataFrame unchanged.
    """
    return compute_balance_summary(results_df)
# --------------------------------------------------------------- 

# --------------------------------------------------------------- build_benchmark_markdown_table()
def build_benchmark_markdown_table(results_df: pd.DataFrame) -> str:
    """Build a Markdown benchmark-results table for analysis placeholder use.

    Logic:
        This function converts the benchmark display table into Markdown rows.
        1. Build the normalized benchmark table.
        2. Seed the Markdown header row and divider row.
        3. Append one formatted Markdown row per benchmark record.
    """
    table_df = build_benchmark_table(results_df)
    lines = [
        "| Method | Scenario | Query Mode | Size | Time (ms) | Height | Balanced |",
        "|---|---|---|---|---|---|---|",
    ]
    for _, row in table_df.iterrows():
        lines.append(
            f"| {row['method']} | {row['scenario']} | {row['query_mode']} "
            f"| {_format_int(row['size'])} | {_format_float(row['time_ms'])} "
            f"| {_format_int(row['height'])} | {_format_bool(row['is_balanced'])} |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------- 

# --------------------------------------------------------- build_speedup_summary_markdown_table()
def build_speedup_summary_markdown_table(results_df: pd.DataFrame) -> str:
    """Build a Markdown speedup-summary table for analysis placeholder use.

    Logic:
        This function converts the speedup summary table into Markdown rows.
        1. Build the normalized speedup summary table.
        2. Seed the Markdown header row and divider row.
        3. Append one formatted Markdown row per speedup record.
    """
    speedup_df = build_speedup_summary_table(results_df)
    lines = [
        "| Scenario | Query Mode | Size | ListMap (ms) | TreeMap (ms) | Speedup |",
        "|---|---|---|---|---|---|",
    ]
    for _, row in speedup_df.iterrows():
        lines.append(
            f"| {row['scenario']} | {row['query_mode']} | "
            f"{_format_int(row['size'])} | {_format_float(row['list_time_ms'])} | "
            f"{_format_float(row['tree_time_ms'])} "
            f"| {_format_float(row['speedup_vs_list'], 2)}x |"
        )
    return "\n".join(lines)
# -------------------------------------------------------------- 

# --------------------------------------------------------- build_balance_summary_markdown_table()
def build_balance_summary_markdown_table(results_df: pd.DataFrame) -> str:
    """Build a Markdown balance-summary table for analysis placeholder use.

    Logic:
        This function converts the balance summary table into Markdown rows.
        1. Build the normalized balance summary table.
        2. Seed the Markdown header row and divider row.
        3. Append one formatted Markdown row per balance record.
    """
    balance_df = build_balance_summary_table(results_df)
    lines = [
        "| Scenario | Size | Height | Balanced |",
        "|---|---|---|---|",
    ]
    for _, row in balance_df.iterrows():
        lines.append(
            f"| {row['scenario']} | {_format_int(row['size'])} | "
            f"{_format_int(row['height'])} "
            f"| {_format_bool(row['is_balanced'])} |"
        )
    return "\n".join(lines)
# -------------------------------------------------------------- 

# --------------------------------------------------------------- generate_summary_sentences()
def generate_summary_sentences(results_df: pd.DataFrame) -> list[str]:
    """Generate short narrative summary sentences for the analysis views.

    Logic:
        1. Return a placeholder sentence when no benchmark results exist.
        2. Highlight the strongest observed TreeMap speedup.
        3. Compare sorted and random insertion behavior when both are present.
    """
    # VALIDATION: analysis tabs need a safe placeholder sentence before any
    # benchmark data has been generated or loaded.
    if results_df.empty:
        return ["No benchmark results are available yet."]

    speedup_df = build_speedup_summary_table(results_df)
    balance_df = build_balance_summary_table(results_df)

    sentences: list[str] = []
    if not speedup_df.empty:
        # Step 1: highlight the single strongest observed TreeMap speedup.
        best_speedup = speedup_df.loc[speedup_df["speedup_vs_list"].idxmax()]
        sentences.append(
            "Best observed TreeMap speedup over ListMap was "
            f"{best_speedup['speedup_vs_list']:.2f}x for "
            f"{best_speedup['scenario']} {best_speedup['query_mode']} queries "
            f"at size {int(best_speedup['size'])}."
        )

    if not balance_df.empty:
        # Step 2: compare sorted vs random insertion shapes when both are present.
        sorted_rows = balance_df[balance_df["scenario"] == "sorted_insertion"]
        random_rows = balance_df[balance_df["scenario"] == "random_insertion"]
        if not sorted_rows.empty and not random_rows.empty:
            sentences.append(
                "Sorted insertions produced taller, less balanced trees than "
                "random insertions across the tested sizes."
            )

    return sentences
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# CHART GENERATION HELPERS
# ========================================================================
# These helpers render and save the chart artifacts referenced by the
# Benchmark tab and the written analysis markdown.
#
# --------------------------------------------------------------- _save_figure()
def _save_figure(figure: plt.Figure, path: Path) -> Path:
    """Save ``figure`` to ``path`` and close it.

    Logic:
        This helper centralizes the final figure-save workflow for each chart.
        1. Create the target directory when needed.
        2. Apply tight layout and save the figure to disk.
        3. Close the figure and return the saved path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(figure)
    return path
# --------------------------------------------------------------- 

# --------------------------------------------------------------- generate_charts()
def generate_charts(
    results_df: pd.DataFrame,
    chart_dir: str | Path,
) -> dict[str, Path]:
    """Generate chart PNGs used by the Benchmark and Analysis tabs.

    Logic:
        1. Build display-ready benchmark, speedup, and balance summary tables.
        2. Render the four required chart families from those summaries.
        3. Save each figure to its stable Module 6 analysis filename.
    """
    output_dir = Path(chart_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # VALIDATION: skip chart generation entirely when no benchmark rows exist.
    if results_df.empty:
        return {}
    # Create chart paths
    chart_paths: dict[str, Path] = {}
    benchmark_df = build_benchmark_table(results_df)
    speedup_df = build_speedup_summary_table(results_df)
    balance_df = build_balance_summary_table(results_df)

    # Step 1: runtime comparison line chart.
    figure, axis = plt.subplots(figsize=(8, 4.5))
    # Plot runtime comparison for hits.
    for (method, scenario), group in benchmark_df.groupby(["method", "scenario"]):
        filtered = group[group["query_mode"] == "hits"]
        if filtered.empty:
            continue
        # Plot the runtime comparison.
        axis.plot(
            filtered["size"],
            filtered["time_ms"],
            marker="o",
            label=f"{method} - {scenario}",
        )
    # Set chart title and labels.
    axis.set_title("TreeMap vs ListMap Search Runtime")
    axis.set_xlabel("Dataset Size")
    axis.set_ylabel("Best Runtime (ms)")
    axis.legend()
    # Save the chart.
    chart_paths["tree_vs_list"] = _save_figure(
        figure,
        output_dir / CHART_FILENAMES["tree_vs_list"],
    )

    # Step 2: speedup chart.
    figure, axis = plt.subplots(figsize=(8, 4.5))
    # Plot speedup for each scenario.
    for scenario, group in speedup_df.groupby("scenario"):
        axis.plot(
            group["size"],
            group["speedup_vs_list"],
            marker="o",
            label=scenario,
        )
    # Set chart title and labels.
    axis.set_title("TreeMap Speedup Relative to ListMap")
    axis.set_xlabel("Dataset Size")
    axis.set_ylabel("Speedup Factor (ListMap / TreeMap)")
    axis.axhline(1.0, color="black", linestyle="--", linewidth=1)
    axis.legend()
    chart_paths["speedup"] = _save_figure(
        figure,
        output_dir / CHART_FILENAMES["speedup"],
    )

    # Step 3: height growth chart.
    figure, axis = plt.subplots(figsize=(8, 4.5))
    # Plot height growth for each scenario.
    for scenario, group in balance_df.groupby("scenario"):
        axis.plot(
            group["size"],
            group["height"],
            marker="o",
            label=scenario,
        )
    # Set chart title and labels.
    axis.set_title("BST Height Growth by Insertion Scenario")
    axis.set_xlabel("Dataset Size")
    axis.set_ylabel("Tree Height")
    axis.legend()
    # Save the chart.
    chart_paths["height"] = _save_figure(
        figure,
        output_dir / CHART_FILENAMES["height"],
    )

    # Step 4: balance profile chart.
    figure, axis = plt.subplots(figsize=(8, 4.5))
    balance_plot = balance_df.copy()
    balance_plot["balanced_flag"] = balance_plot["is_balanced"].astype(int)
    # Plot balance profile for each scenario.
    for scenario, group in balance_plot.groupby("scenario"):
        axis.plot(
            group["size"],
            group["balanced_flag"],
            marker="o",
            label=scenario,
        )
    # Set chart title and labels.
    axis.set_title("Balance Detection Profile")
    axis.set_xlabel("Dataset Size")
    axis.set_ylabel("Balanced (1=True, 0=False)")
    axis.set_ylim(-0.1, 1.1)
    axis.legend()   
    # Save the chart.
    chart_paths["balance"] = _save_figure(
        figure,
        output_dir / CHART_FILENAMES["balance"],
    )

    return chart_paths
# --------------------------------------------------------------- 

# __________________________________________________________________________
# Function Definitions
# ========================================================================
# REPORT ARTIFACT ORCHESTRATION
# ========================================================================
# This helper refreshes the saved CSV summaries and chart artifacts from one
# benchmark-results CSV input.
#
# --------------------------------------------------------------- generate_all_reports()
def generate_all_reports(
    results_csv_path: str | Path,
    analysis_dir: str | Path,
) -> dict[str, Path]:
    """Load benchmark CSVs, save summary CSVs, and regenerate charts.

    Logic:
        1. Load the raw benchmark CSV from disk.
        2. Recompute the speedup and balance summary CSV artifacts.
        3. Regenerate the chart image set used by the app and analysis docs.
    """
    analysis_path = Path(analysis_dir)
    results_df = load_results_csv(results_csv_path)
    speedup_df = build_speedup_summary_table(results_df)
    balance_df = build_balance_summary_table(results_df)

    speedup_df.to_csv(analysis_path / "search_speedup_summary.csv", index=False)
    balance_df.to_csv(analysis_path / "balance_summary.csv", index=False)

    return generate_charts(results_df, analysis_path / "charts")
# --------------------------------------------------------------- 

# -------------------------------------------------------------------------
# End of File
# -------------------------------------------------------------------------
