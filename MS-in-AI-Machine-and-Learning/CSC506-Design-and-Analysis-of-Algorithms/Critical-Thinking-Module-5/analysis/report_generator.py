# File: report_generator.py | Author: Alexander Ricciardi | Date: 2026-04-15
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
#
# -------------------------------------------------------------------------
# Module Functionality
# Report-generation for Benchmark Lab. Builds Markdown
# tables from benchmark summaries and generates saved charts used
# by the Streamlit app and written-analysis placeholders.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Report and chart generation for benchmark lab."""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from math import ceil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from analysis.benchmark_search import (
    build_collision_benchmark_state,
    compute_operation_scaling_summary,
    compute_speedup_summary,
    load_results_csv,
)


# ______________________________________________________________________________
# Global Constants / Variables
# ==============================================================================
# REPORT CONSTANTS
# ==============================================================================
# Color palette and human-readable group titles used by every chart and
# Markdown table. Keeping these centralized prevents palette drift between
# the Streamlit UI, saved PNGs, and the written analysis.
# ------------------------------------------------------------------------------

# Whitelist of structures whose runtime curves get a fixed color in saved charts.
# Anything not listed falls back to matplotlib's default cycle.
METHOD_COLORS: dict[str, str] = {
    "Hash Table": "#2f6db3",     # Cool blue: hash table series
    "Linear Search": "#d95f5f",  # Warm red: linear-search baseline series
}
"""Consistent color palette for saved search-comparison charts."""

# Mapping from internal operation_group ids to display titles used by tables/charts.
# Keys must match the operation_group values produced by analysis.benchmark_search.
_GROUP_TITLES: dict[str, str] = {
    "search_comparison": "Search Comparison",       # Hash vs linear lookup workloads
    "hash_core": "Hash Core",                       # Insert/delete on the hash table
    "hash_collision": "Hash Collision",             # Forced-collision stress workloads
    "priority_queue_core": "Priority Queue Core",   # Insert/extract on the heap
}


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# FORMATTING HELPERS
# ==============================================================================
# Helpers used by the Markdown table builders to keep "missing"
# values rendered as "-" rather than "nan" or "None".
#
# - Function: _format_float() - Float with N digits or "-"
# - Function: _format_int()   - Comma-grouped int or "-"
# - Function: _format_bool()  - Yes/No or "-"
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _format_float()
def _format_float(value: object | None, digits: int = 4) -> str:
    """Return a compact float string or ``"-"`` for missing values.

    Logic:
        This helper renders an optional float for Markdown table cells.
        1. SAFETY CHECK: return "-" for None or pandas NA values.
        2. Cast to float and apply the requested precision.
        3. Return the formatted string.
    """
    # SAFETY CHECK: missing values render as "-" instead of "nan"/"None"
    if value is None or pd.isna(value):
        return "-"
    return f"{float(value):.{digits}f}"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _format_int()
def _format_int(value: object | None) -> str:
    """Return a compact integer string or ``"-"`` for missing values.

    Logic:
        This helper renders an optional integer for Markdown table cells.
        1. SAFETY CHECK: return "-" for None or pandas NA values.
        2. Cast to int and apply comma grouping.
        3. Return the formatted string.
    """
    # SAFETY CHECK: missing values render as "-" instead of "nan"/"None"
    if value is None or pd.isna(value):
        return "-"
    return f"{int(value):,}"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _format_bool()
def _format_bool(value: object | None) -> str:
    """Return ``Yes``/``No``/``-`` for optional boolean values.

    Logic:
        This helper renders an optional boolean for Markdown table cells.
        1. SAFETY CHECK: return "-" for None or pandas NA values.
        2. Cast to bool and return "Yes" or "No" accordingly.
    """
    # SAFETY CHECK: missing values render as "-"
    if value is None or pd.isna(value):
        return "-"
    return "Yes" if bool(value) else "No"
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# MARKDOWN TABLE BUILDERS
# ==============================================================================
# Convert benchmark DataFrames into Markdown tables for the Streamlit
# Benchmark Lab and the written-analysis report. All builders sort
# deterministically so successive runs produce identical output.
#
# - Function: build_benchmark_table()         - Full per-row benchmark table
# - Function: build_speedup_summary_table()   - Hash-vs-linear speedup summary
# - Function: build_operation_scaling_table() - Smallest/largest scaling summary
# - Function: generate_summary_sentences()    - Extract notes column as bullets
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_benchmark_table()
def build_benchmark_table(df: pd.DataFrame) -> str:
    """Convert a CTA-5 benchmark DataFrame into a Markdown table.

    Logic:
        This builder renders one Markdown row per benchmark record.
        1. Emit the table header and separator rows.
        2. Sort rows deterministically by group/scenario/structure/operation/size.
        3. Format each row using the optional-aware _format_* helpers.
    """
    lines = [
        "| Group | Scenario | Structure | Operation | Size | Workload | Time (ms) | Avg (us) | Correct | Found | Deleted | Collisions | Load Factor | Heap Valid | Speedup |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    # Step 1: deterministic sort so successive runs produce identical output
    sorted_df = df.sort_values(
        by=["operation_group", "scenario", "structure", "operation", "size"],
        kind="stable",
    )
    # MAIN ITERATION LOOP: render one Markdown row per benchmark record
    for _, row in sorted_df.iterrows():
        lines.append(
            f"| {_GROUP_TITLES.get(str(row['operation_group']), str(row['operation_group']))} "
            f"| {row['scenario']} | {row['structure']} | {row['operation']} "
            f"| {int(row['size']):,} | {int(row['workload_count']):,} "
            f"| {float(row['time_ms']):.4f} | {float(row['avg_time_us']):.4f} "
            f"| {'Yes' if bool(row['is_correct']) else 'No'} "
            f"| {_format_int(row['found_count'])} | {_format_int(row['deleted_count'])} "
            f"| {_format_int(row['collision_count'])} | {_format_float(row['load_factor'])} "
            f"| {_format_bool(row['heap_valid_after'])} "
            f"| {_format_float(row['speedup_vs_linear'], 2)} |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_speedup_summary_table()
def build_speedup_summary_table(speedup_df: pd.DataFrame) -> str:
    """Convert the hash-vs-linear speedup summary into Markdown.

    Logic:
        This builder renders the speedup summary as a Markdown table.
        1. Emit the table header and separator rows.
        2. Walk every speedup row in input order (already sorted upstream).
        3. Format size, mode, both timings, and the speedup ratio.
    """
    lines = [
        "| Dataset Size | Query Mode | Hash (ms) | Linear (ms) | Speedup |",
        "|---|---|---|---|---|",
    ]
    # MAIN ITERATION LOOP: render one Markdown row per (size, mode) pair
    for _, row in speedup_df.iterrows():
        lines.append(
            f"| {int(row['dataset_size']):,} | {row['query_mode']} "
            f"| {float(row['hash_time_ms']):.4f} | {float(row['linear_time_ms']):.4f} "
            f"| {float(row['speedup']):.2f}x |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_operation_scaling_table()
def build_operation_scaling_table(scaling_df: pd.DataFrame) -> str:
    """Convert the operation scaling summary into Markdown.

    Logic:
        This builder renders the smallest/largest scaling summary as a table.
        1. Emit header rows and a deterministic sort key.
        2. Walk every (group, structure, operation, scenario) summary row.
        3. Render smallest/largest sizes, both timings, and growth factor.
    """
    lines = [
        "| Group | Structure | Operation | Scenario | Smallest Size | Largest Size | Smallest Time (ms) | Largest Time (ms) | Growth |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    # Step 1: deterministic sort keeps row order stable across runs
    sorted_df = scaling_df.sort_values(
        by=["operation_group", "scenario", "structure", "operation"],
        kind="stable",
    )
    # MAIN ITERATION LOOP: render one Markdown row per scaling summary entry
    for _, row in sorted_df.iterrows():
        lines.append(
            f"| {_GROUP_TITLES.get(str(row['operation_group']), str(row['operation_group']))} "
            f"| {row['structure']} | {row['operation']} | {row['scenario']} "
            f"| {int(row['smallest_size']):,} | {int(row['largest_size']):,} "
            f"| {float(row['smallest_time_ms']):.4f} | {float(row['largest_time_ms']):.4f} "
            f"| {float(row['growth_factor']):.2f}x |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_summary_sentences()
def generate_summary_sentences(df: pd.DataFrame) -> list[str]:
    """Extract the ``notes`` column as human-readable summary sentences.

    Logic:
        This helper exposes the `notes` column as a flat list of strings.
        1. Iterate every row in the benchmark DataFrame.
        2. Cast each `notes` cell to str to defend against NA/None values.
        3. Return the list in row order for downstream rendering.
    """
    return [str(row["notes"]) for _, row in df.iterrows()]
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# CHART RENDERERS
# ==============================================================================
# Saved-PNG charts used by the Streamlit Benchmark Lab and the
# generate_all_reports() entry point. matplotlib uses the headless "Agg"
# backend so charts can be produced from any environment.
#
# - Function: _ensure_charts_dir()         - Create charts/ subdirectory
# - Function: _chart_hash_vs_linear()      - Search-comparison line chart
# - Function: _chart_speedup()             - Speedup bar chart
# - Function: _chart_operation_runtime()   - Per-group runtime small multiples
# - Function: _chart_collision_distribution() - Forced-collision bucket bar chart
# - Function: generate_charts()            - Top-level chart orchestrator
# - Function: generate_all_reports()       - Load CSV and regenerate charts
# ------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _ensure_charts_dir()
def _ensure_charts_dir(output_dir: Path) -> Path:
    """Create the charts subdirectory if needed.

    Logic:
        This helper guarantees the charts subdirectory exists before saving.
        1. Compute the charts subdirectory path under output_dir.
        2. mkdir with parents=True/exist_ok=True so re-runs are idempotent.
        3. Return the resolved Path for downstream chart writers.
    """
    charts_dir = output_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    return charts_dir
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _chart_hash_vs_linear()
def _chart_hash_vs_linear(df: pd.DataFrame, charts_dir: Path) -> Path:
    """Generate the saved hash-vs-linear runtime chart.

    Logic:
        This renderer produces one subplot per query mode (hits/misses/mixed).
        1. Filter the DataFrame down to the search_comparison rows.
        2. Build one subplot per query-mode scenario.
        3. Plot both methods (Hash Table, Linear Search) with their fixed colors.
        4. Save the figure as a PNG and return its Path.
    """
    # Step 1: isolate the search-comparison subset
    search_df = df[df["operation_group"] == "search_comparison"].copy()
    modes = sorted(search_df["scenario"].unique().tolist())
    fig, axes = plt.subplots(1, max(1, len(modes)), figsize=(5 * max(1, len(modes)), 4.5), sharey=True)
    # SAFETY CHECK: matplotlib returns a single axis (not a list) when only one mode exists
    if not hasattr(axes, "__iter__"):
        axes = [axes]

    # MAIN ITERATION LOOP: one subplot per query-mode scenario
    for ax, mode in zip(axes, modes):
        subset = search_df[search_df["scenario"] == mode]
        # plot each method's curve in its fixed color
        for method, color in METHOD_COLORS.items():
            method_df = subset[subset["structure"] == method].sort_values("size")
            ax.plot(
                method_df["size"],
                method_df["time_ms"],
                marker="o",
                label=method,
                color=color,
            )
        # standard axes/legend formatting
        ax.set_title(f"Query Mode: {mode}")
        ax.set_xlabel("Dataset Size")
        ax.set_ylabel("Time (ms)")
        ax.grid(True, alpha=0.3)
        ax.legend()
    # Set the title and labels
    fig.suptitle("Hash Table Search vs Linear Search", fontsize=14)
    fig.tight_layout()
    path = charts_dir / "hash_vs_linear_search.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _chart_speedup()
def _chart_speedup(speedup_df: pd.DataFrame, charts_dir: Path) -> Path:
    """Generate the saved search-speedup chart.

    Logic:
        This renderer produces a grouped bar chart of speedups per size/mode.
        1. Build x-axis positions for each dataset size.
        2. For each query mode, draw a side-by-side bar series.
        3. Add the y=1 reference line, legend, and tight layout.
        4. Save the PNG and return its Path.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    modes = sorted(speedup_df["query_mode"].unique().tolist())
    sizes = sorted(speedup_df["dataset_size"].unique().tolist())
    bar_width = 0.22
    x_positions = list(range(len(sizes)))

    # MAIN ITERATION LOOP: one grouped-bar series per query mode
    for index, mode in enumerate(modes):
        mode_df = speedup_df[speedup_df["query_mode"] == mode].sort_values("dataset_size")
        positions = [x + (index * bar_width) for x in x_positions]
        ax.bar(
            positions,
            mode_df["speedup"],
            width=bar_width,
            label=mode,
            alpha=0.85,
        )
    # Set the title and labels
    ax.set_title("Hash Table Speedup over Linear Search")
    ax.set_xlabel("Dataset Size")
    ax.set_ylabel("Speedup (x)")
    ax.set_xticks([x + bar_width for x in x_positions])
    ax.set_xticklabels([f"{size:,}" for size in sizes])
    # Reference line: speedup of 1.0 means hash equals linear performance
    ax.axhline(y=1.0, color="#666666", linestyle="--", linewidth=1)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(title="Query Mode")
    # Save the chart
    fig.tight_layout()
    path = charts_dir / "search_speedup.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _chart_operation_runtime()
def _chart_operation_runtime(df: pd.DataFrame, charts_dir: Path) -> Path:
    """Generate a saved runtime overview for the full benchmark matrix.

    Logic:
        This renderer produces a small-multiples grid of runtime curves.
        1. Determine the subplot grid (one cell per operation_group).
        2. Disable any unused axes when groups < grid cells.
        3. For each group, plot one runtime curve per (structure, op, scenario).
        4. Save the PNG and return its Path.
    """
    groups = sorted(df["operation_group"].unique().tolist())
    columns = 2
    rows = ceil(len(groups) / columns)
    fig, axes = plt.subplots(rows, columns, figsize=(15, 4.5 * rows))
    # SAFETY CHECK: flatten to a 1-D list whether axes is a 2-D ndarray or a single axis
    axes_list = axes.flatten() if hasattr(axes, "flatten") else [axes]

    # Disable unused axes so the grid does not show empty boxes
    for ax in axes_list[len(groups):]:
        ax.axis("off")

    # MAIN ITERATION LOOP: one subplot per operation_group
    for ax, operation_group in zip(axes_list, groups):
        subset = df[df["operation_group"] == operation_group].copy()
        # Step 1: build a stable label combining structure, operation, and scenario
        subset["label"] = (
            subset["structure"].astype(str)
            + "."
            + subset["operation"].astype(str)
            + " ["
            + subset["scenario"].astype(str)
            + "]"
        )
        # plot one curve per label (already sorted by size)
        for label, series in subset.groupby("label"):
            ordered = series.sort_values("size")
            ax.plot(
                ordered["size"],
                ordered["time_ms"],
                marker="o",
                linewidth=1.8,
                label=label,
            )
        # Set the title and labels
        ax.set_title(_GROUP_TITLES.get(operation_group, operation_group))
        ax.set_xlabel("Dataset Size")
        ax.set_ylabel("Time (ms)")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    # Set the title and labels
    fig.suptitle("CTA-5 Benchmark Runtime by Operation Group", fontsize=14)
    fig.tight_layout()
    path = charts_dir / "benchmark_operation_runtime.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _chart_collision_distribution()
def _chart_collision_distribution(df: pd.DataFrame, charts_dir: Path) -> Path:
    """Generate a collision distribution chart from the benchmarked run size.

    Logic:
        This renderer reproduces a forced-collision hash table at one size and
        plots the per-bucket chain lengths.
        1. Find the available collision sizes; fall back to [100] when empty.
        2. Prefer size=100 when present; otherwise pick the smallest available.
        3. Rebuild the collision hash table state and read its bucket lengths.
        4. Render a bar chart annotated with the load factor and chain stats.
    """
    collision_rows = df[df["operation_group"] == "hash_collision"]
    available_sizes = sorted(int(size) for size in collision_rows["size"].unique().tolist())
    # SAFETY CHECK: fall back to a small default when no collision rows are present
    if not available_sizes:
        available_sizes = [100]
    chosen_size = 100 if 100 in available_sizes else available_sizes[0]
    hash_table = build_collision_benchmark_state(chosen_size)
    bucket_lengths = [len(bucket) for bucket in hash_table.get_buckets()]
    stats = hash_table.get_stats()
    # Set the title and labels
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.bar(range(len(bucket_lengths)), bucket_lengths, color="#2f6db3", alpha=0.85)
    ax.set_title(f"Clustered Forced-Collision Bucket Occupancy at n = {chosen_size:,}")
    ax.set_xlabel(
        "Bucket Index\n"
        f"Load Factor: {stats.load_factor:.2f} | "
        f"Collision Buckets: {stats.collision_buckets} | "
        f"Collisions: {stats.total_collisions} | "
        f"Longest Chain: {stats.longest_bucket_length}"
    )
    # Set the title and labels
    ax.set_ylabel("Chain Length")
    ax.grid(True, axis="y", alpha=0.3)
    # Save the chart
    fig.tight_layout()
    path = charts_dir / "collision_distribution.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_charts()
def generate_charts(
    df: pd.DataFrame,
    speedup_df: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    """Generate all saved CTA-5 benchmark charts.

    Logic:
        This orchestrator dispatches each renderer when its DataFrame is non-empty.
        1. Resolve the output directory and ensure charts/ exists.
        2. SAFETY CHECK: skip per-row renderers when df is empty.
        3. SAFETY CHECK: skip the speedup chart when speedup_df is empty.
    """
    output_path = Path(output_dir)
    charts_dir = _ensure_charts_dir(output_path)
    # SAFETY CHECK: skip renderers that need per-row data when df is empty
    if not df.empty:
        _chart_hash_vs_linear(df, charts_dir)
        _chart_operation_runtime(df, charts_dir)
        _chart_collision_distribution(df, charts_dir)
    # SAFETY CHECK: skip speedup chart when no summary rows are present
    if not speedup_df.empty:
        _chart_speedup(speedup_df, charts_dir)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_all_reports()
def generate_all_reports(
    csv_path: str | Path,
    output_dir: str | Path | None = None,
) -> None:
    """Load saved benchmark results and regenerate chart artifacts.

    Logic:
        This entry point reloads a saved benchmark CSV and rebuilds chart PNGs.
        1. Resolve csv_path and pick a default output_dir alongside the CSV.
        2. Load the benchmark DataFrame from disk.
        3. Compute the speedup summary used by the speedup chart.
        4. Compute the scaling summary (return value not consumed by charts).
        5. Delegate chart rendering to generate_charts().
    """
    csv_path = Path(csv_path)
    # default output dir is alongside the CSV when not provided
    if output_dir is None:
        output_dir = csv_path.parent
    # Load the benchmark DataFrame from disk
    df = load_results_csv(csv_path)
    speedup_df = compute_speedup_summary(df)
    # Compute the scaling summary for its side effects/validation; result unused here
    _ = compute_operation_scaling_summary(df)
    generate_charts(df, speedup_df, output_dir)
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================
