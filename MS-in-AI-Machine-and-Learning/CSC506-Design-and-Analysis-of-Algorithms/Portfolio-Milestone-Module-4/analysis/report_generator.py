# -------------------------------------------------------------------------
# File: report_generator.py
# Author: Alexander Ricciardi
# Date: 2026-04-12
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Converts benchmark output into
# Markdown tables, summary sentences, and matplotlib charts (PNG).
# -------------------------------------------------------------------------

# --- Functions ---
# - build_benchmark_table()         — benchmark DataFrame → Markdown table
# - build_operation_winners_table() — winners DataFrame → Markdown table
# - generate_summary_sentences()    — human-readable winner sentences
# - generate_charts()               — save chart PNGs under analysis/charts/
# - generate_all_reports()          — orchestrator: CSV → winners → charts
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Report and chart benchmark results visual generator.

From benchmark results stored in CSVs, it produces Markdown tables, summary sentences, and
matplotlib chart images.
"""

# ________________
# Imports
#

from __future__ import annotations

from pathlib import Path
from textwrap import fill

import matplotlib

matplotlib.use("Agg")  # non-interactive backend for PNG export

import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.ticker import LogFormatterMathtext, LogLocator, NullFormatter  # noqa: E402

from analysis.benchmark_structures import (  # noqa: E402
    compute_operation_winners,
    load_results_csv,
    save_operation_winners_csv, 
)

# __________________________________________________________________________
# Constants
#

# ========================================================================
# Visual Style
# ========================================================================

STRUCTURE_COLORS: dict[str, str] = {
    "Stack": "#e74c3c",
    "Queue": "#f39c12",
    "Deque": "#2ecc71",
    "LinkedList": "#3498db",
}
"""Consistent per-structure color palette across every chart."""

_CHARTS_DIR_NAME: str = "charts"

# Operation group → human-readable label, used in tables and headings.
_GROUP_LABELS: dict[str, str] = {
    "common_build": "Common Build",
    "common_drain": "Common Drain",
    "peek_front": "Peek / Front",
    "deque_ends": "Deque Ends",
    "linked_list_search": "LinkedList Search",
    "linked_list_delete": "LinkedList Delete",
    "linked_list_display": "LinkedList Display",
}

# __________________________________________________________________________
# Markdown Table Builders
#

# ========================================================================
# Benchmark Table
# ========================================================================

# --------------------------------------------------------------- build_benchmark_table()
def build_benchmark_table(df: pd.DataFrame) -> str:
    """Convert a benchmark DataFrame into a Markdown table.

    Args:
        df: Benchmark results DataFrame with columns ``structure``,
            ``operation``, ``operation_group``, ``size``, ``time_ms``,
            ``size_before``, ``size_after``, ``complexity``, ``is_correct``.

    Returns:
        A Markdown-formatted table string ready for direct embedding.
    """
    lines: list[str] = [
        "| Structure | Operation | Group | Size | Time (ms) | Big-O | Correct |",
        "|-----------|-----------|-------|------|-----------|-------|---------|",
    ]
    # Sort by size, operation group, structure, and operation
    sorted_df = df.sort_values(
        by=["size", "operation_group", "structure", "operation"],
        kind="stable",
    )
    # Append each row to the Markdown table
    for _, row in sorted_df.iterrows():
        group_label = _GROUP_LABELS.get(
            str(row["operation_group"]), str(row["operation_group"])
        )
        # Format the row as a Markdown table row
        lines.append(
            f"| {row['structure']} | {row['operation']} | {group_label} | "
            f"{int(row['size']):,} | {float(row['time_ms']):.4f} | "
            f"{row['complexity']} | "
            f"{'Yes' if bool(row['is_correct']) else 'No'} |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------- end build_benchmark_table()

# ========================================================================
# Operation Winners Table
# ========================================================================

# --------------------------------------------------------------- build_operation_winners_table()
def build_operation_winners_table(winners_df: pd.DataFrame) -> str:
    """Convert the operation winners DataFrame into a Markdown table.

    Args:
        winners_df: DataFrame from
            :func:`analysis.benchmark_structures.compute_operation_winners`.

    Returns:
        A Markdown-formatted table string.
    """
    lines: list[str] = [
        "| Operation Group | Size | Fastest Structure | Fastest Operation | Time (ms) | Runner-Up |",
        "|-----------------|------|-------------------|-------------------|-----------|-----------|",
    ]
    # Sort by size and operation group
    sorted_df = winners_df.sort_values(
        by=["size", "operation_group"], kind="stable"
    )
    # Append each row to the Markdown table
    for _, row in sorted_df.iterrows():
        group_label = _GROUP_LABELS.get(
            str(row["operation_group"]), str(row["operation_group"])
        )
        # Format the row as a Markdown table row
        lines.append(
            f"| {group_label} | {int(row['size']):,} | "
            f"{row['fastest_structure']} | {row['fastest_operation']} | "
            f"{float(row['fastest_time_ms']):.4f} | "
            f"{row['runner_up']} |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------- end build_operation_winners_table()

# ========================================================================
# Summary Sentences
# ========================================================================

# --------------------------------------------------------------- generate_summary_sentences()
def generate_summary_sentences(winners_df: pd.DataFrame) -> list[str]:
    """Produce sentences describing each operation winner.

    Args:
        winners_df: DataFrame from
            :func:`analysis.benchmark_structures.compute_operation_winners`.

    Returns:
        A list of sentences, one per winner row.
    """
    return [str(row["notes"]) for _, row in winners_df.iterrows()]
# --------------------------------------------------------------- end generate_summary_sentences()

# __________________________________________________________________________
# Chart Helpers
#

# ========================================================================
# Charts Directory
# ========================================================================

# --------------------------------------------------------------- _ensure_charts_dir()
def _ensure_charts_dir(output_dir: Path) -> Path:
    """Create and return the ``charts`` sub-directory under *output_dir*."""
    charts_dir = output_dir / _CHARTS_DIR_NAME
    charts_dir.mkdir(parents=True, exist_ok=True)
    return charts_dir
# --------------------------------------------------------------- end _ensure_charts_dir()


# --------------------------------------------------------------- _structure_color()
def _structure_color(structure: str) -> str:
    """Return the color associated with *structure*, fallback to grey."""
    return STRUCTURE_COLORS.get(structure, "#7f8c8d")
# --------------------------------------------------------------- end _structure_color()


# --------------------------------------------------------------- _annotation_color()
def _annotation_color(structure: str) -> str:
    """Pick a readable label color for a colored cell or bar.

    Args:
        structure: Structure name; its fill color drives luminance.

    Returns:
        ``"#1f1f1f"`` on light fills, ``"white"`` on dark fills.
    """
    fill = _structure_color(structure)
    red, green, blue = mcolors.to_rgb(fill)
    luminance = (0.299 * red) + (0.587 * green) + (0.114 * blue)
    return "#1f1f1f" if luminance > 0.62 else "white"
# --------------------------------------------------------------- end _annotation_color()


# --------------------------------------------------------------- _style_log_y_axis()
def _style_log_y_axis(ax: plt.Axes) -> None:
    """Apply clearer major/minor tick and grid styling for log y-axes.

    Args:
        ax: Matplotlib axes already configured with ``yscale='log'``.
    """
    # Set the major and minor locators for the y-axis
    ax.yaxis.set_major_locator(LogLocator(base=10.0))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=(2.0, 5.0)))
    ax.yaxis.set_major_formatter(LogFormatterMathtext(base=10.0))
    ax.yaxis.set_minor_formatter(NullFormatter())
    # Set the grid
    ax.grid(
        True,
        which="major",
        axis="y",
        color="#94a3b8",
        alpha=0.35,
        linewidth=0.85,
    )
    # Set the minor grid (base 10)
    ax.grid(
        True,
        which="minor",
        axis="y",
        color="#cbd5e1",
        alpha=0.16,
        linewidth=0.45,
    )
    # Set the tick parameters
    ax.tick_params(axis="y", which="major", length=5, width=0.9)
    ax.tick_params(axis="y", which="minor", length=2.5, width=0.6)
# --------------------------------------------------------------- end _style_log_y_axis()

# __________________________________________________________________________
# Individual Chart Generators
#

# ========================================================================
# Chart 1: Common Operation Runtime
# ========================================================================

# --------------------------------------------------------------- _chart_common_operation_runtime()
def _chart_common_operation_runtime(df: pd.DataFrame, charts_dir: Path) -> Path:
    """Line plot of runtime vs. size for the common build/drain workloads.

    Args:
        df: Full benchmark DataFrame.
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """
    common_groups = ("common_build", "common_drain")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    # Iterate over the common operation groups
    for ax, group in zip(axes, common_groups):
        subset = df[df["operation_group"] == group]
        # Plot one line per (structure, operation) pair
        for (structure, operation), grp_df in subset.groupby(
            ["structure", "operation"]
        ):

            ordered = grp_df.sort_values("size")
            ax.plot(
                ordered["size"],
                ordered["time_ms"],
                marker="o",
                linewidth=2,
                color=_structure_color(str(structure)),
                label=f"{structure}.{operation}",
            )
        # Se    t the title
        ax.set_title(_GROUP_LABELS.get(group, group), fontsize=12, fontweight="bold")
        # Set the x-axis label
        ax.set_xlabel("Dataset Size")
        # Set the y-axis label
        ax.set_ylabel("Time (ms)")
        # Set the x-axis scale
        ax.set_xscale("log")
        # Set the y-axis scale
        _style_log_y_axis(ax)
        # Set the grid
        ax.grid(
            True,
            which="major",
            axis="x",
            color="#94a3b8",
            alpha=0.18,
            linewidth=0.65,
        )
        # Set the minor grid
        ax.grid(
            True,
            which="minor",
            axis="x",
            color="#cbd5e1",
            alpha=0.08,
            linewidth=0.4,
        )
        # Set the legend
        ax.legend(fontsize=8, loc="best")
    # Set the title
    fig.suptitle(
        "Common Operation Runtime (log-log)",
        fontsize=15,
        fontweight="bold",
    )
    # Adjust layout
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    # Save the chart
    path = charts_dir / "common_operation_runtime.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_common_operation_runtime()


# ========================================================================
# Chart 2: Structure Specific Runtime
# ========================================================================

# --------------------------------------------------------------- _chart_structure_specific_runtime()
def _chart_structure_specific_runtime(df: pd.DataFrame, charts_dir: Path) -> Path:
    """Grouped bar chart of structure-specific operations across sizes.

    Args:
        df: Full benchmark DataFrame.
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """ 
    # Define the specific operation groups
    specific_groups = (
        "deque_ends",
        "linked_list_search",
        "linked_list_delete",
        "linked_list_display",
    )
    # Get the sizes
    sizes = sorted(df["size"].unique())

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes_flat = axes.flatten()
    # Iterate over the specific operation groups
    for idx, group in enumerate(specific_groups):
        ax = axes_flat[idx]
        subset = df[df["operation_group"] == group]
        operations = sorted(subset["operation"].unique())
        n_ops = len(operations)
        # Skip if no operations
        if n_ops == 0:
            ax.set_visible(False)
            continue
        # Set the bar width
        bar_width = 0.8 / n_ops
        x_positions = list(range(len(sizes)))
        # Iterate over the operations
        for op_idx, operation in enumerate(operations):
            op_data = subset[subset["operation"] == operation]
            times: list[float] = []
            structure_for_op = ""
            # Iterate over the sizes
            for size in sizes:
                row = op_data[op_data["size"] == size]
                times.append(
                    float(row["time_ms"].iloc[0]) if not row.empty else 0.0
                )
                # Get the structure for the operation
                if not row.empty:
                    structure_for_op = str(row["structure"].iloc[0])
            offset = (op_idx - n_ops / 2 + 0.5) * bar_width
            # Plot the bars
            ax.bar(
                [x + offset for x in x_positions],
                times,
                bar_width,
                label=operation,
                color=_structure_color(structure_for_op),
                edgecolor="white",
                linewidth=0.5,
            )

        ax.set_title(
            _GROUP_LABELS.get(group, group), fontsize=12, fontweight="bold"
        )
        # Set the x-axis ticks
        ax.set_xticks(x_positions)
        # Set the x-axis tick labels
        ax.set_xticklabels([f"{s:,}" for s in sizes], fontsize=9)
        # Set the x-axis label
        ax.set_xlabel("Dataset Size")
        # Set the y-axis label
        ax.set_ylabel("Time (ms)")
        # Set the y-axis scale
        ax.set_yscale("log")
        _style_log_y_axis(ax)
        ax.legend(fontsize=7, loc="best")

    # Hide unused panels (we already plot 4 in a 2x2 grid)
    for idx in range(len(specific_groups), len(axes_flat)):
        axes_flat[idx].set_visible(False)

    fig.suptitle(
        "Structure-Specific Operation Runtime",
        fontsize=15,
        fontweight="bold",
    )
    # Adjust layout
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    # Save the chart
    path = charts_dir / "structure_specific_runtime.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_structure_specific_runtime()


# ========================================================================
# Chart 3: Operation Winner Heatmap
# ========================================================================

# --------------------------------------------------------------- _chart_operation_winner_heatmap()
def _chart_operation_winner_heatmap(
    winners_df: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Heatmap of fastest structure per (operation_group, size).

    Args:
        winners_df: DataFrame from
            :func:`analysis.benchmark_structures.compute_operation_winners`.
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """
    # Get the structures
    structures = list(STRUCTURE_COLORS.keys())
    # Map structures to numbers
    structure_to_num = {s: i for i, s in enumerate(structures)}
    # Get the colors
    cmap_colors = [STRUCTURE_COLORS[s] for s in structures]
    # Create the colormap
    cmap = mcolors.ListedColormap(cmap_colors)

    pivot = winners_df.pivot(
        index="operation_group",
        columns="size",
        values="fastest_structure",
    )
    # Get the pivot table for the fastest time
    time_pivot = winners_df.pivot(
        index="operation_group",
        columns="size",
        values="fastest_time_ms",
    )
    # Get the pivot table for the fastest operation
    op_pivot = winners_df.pivot(
        index="operation_group",
        columns="size",
        values="fastest_operation",
    )
    # Get the sizes
    sizes = sorted(winners_df["size"].unique())

    # Define the preferred group order
    preferred_group_order = [
        "common_build",
        "common_drain",
        "peek_front",
        "deque_ends",
        "linked_list_search",
        "linked_list_delete",
        "linked_list_display",
    ]
    # Get the groups
    groups = [
        g for g in preferred_group_order
        if g in winners_df["operation_group"].unique()
    ]
    # Reindex the pivot table
    pivot = pivot.reindex(index=groups, columns=sizes)
    time_pivot = time_pivot.reindex(index=groups, columns=sizes)
    op_pivot = op_pivot.reindex(index=groups, columns=sizes)
    # Get the number grid
    num_grid = pivot.map(lambda v: structure_to_num.get(v, -1))

    # Set the figure width and height
    fig_width = max(10, len(sizes) * 2.4)
    fig_height = max(5.5, len(groups) * 0.95 + 1.8)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    # Display the number grid
    ax.imshow(
        num_grid.values,
        cmap=cmap,
        aspect="auto",
        vmin=0,
        vmax=len(structures) - 1,
    )

    # Cell borders for crisp matrix appearance
    ax.set_xticks([x - 0.5 for x in range(1, len(sizes))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(groups))], minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    # Iterate over the groups
    for i, group in enumerate(groups):
        # Iterate over the sizes
        for j, size in enumerate(sizes):
            # Get the winner
            winner = pivot.loc[group, size] if group in pivot.index else None
            # Get the time
            time_ms = (
                time_pivot.loc[group, size]
                if group in time_pivot.index else None
            )
            # Get the operation name
            op_name = (
                op_pivot.loc[group, size]
                if group in op_pivot.index else None
            )
            # Check if the winner or time is NaN
            if pd.isna(winner) or pd.isna(time_ms):
                cell_text = "no data"
                text_color = "#1f1f1f"
            else:
                op_label = "" if pd.isna(op_name) else f"\n{op_name}"
                cell_text = (
                    f"{winner}{op_label}\n{float(time_ms):.3f} ms"
                )
                text_color = _annotation_color(str(winner))
            # Add the text to the cell  
            ax.text(
                j,
                i,
                cell_text,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                color=text_color,
            )
    # Set the x-axis ticks
    ax.set_xticks(range(len(sizes)))
    # Set the x-axis tick labels
    ax.set_xticklabels([f"{s:,}" for s in sizes])
    # Set the y-axis ticks
    ax.set_yticks(range(len(groups)))
    # Set the y-axis tick labels
    ax.set_yticklabels([_GROUP_LABELS.get(g, g) for g in groups])
    # Set the x-axis label
    ax.set_xlabel("Dataset Size")
    # Set the y-axis label
    ax.set_ylabel("Operation Group")
    # Set the title
    ax.set_title(
        "Fastest Structure by Operation Group and Size",
        fontsize=14,
        fontweight="bold",
        pad=12,
    )
    # Get the visible structures
    visible = sorted(set(winners_df["fastest_structure"].dropna().tolist()))
    # Get the legend handles
    legend_handles = [
        Patch(facecolor=STRUCTURE_COLORS[s], edgecolor="none", label=s)
        for s in structures if s in visible
    ]
    # Add the legend
    ax.legend(
        handles=legend_handles,
        title="Cell Color = Winning Structure",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        ncol=max(1, len(legend_handles)),
        frameon=False,
        fontsize=9,
        title_fontsize=9,
    )
    # Adjust the layout
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    # Save the chart
    path = charts_dir / "operation_winner_heatmap.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_operation_winner_heatmap()


# ========================================================================
# Chart 4: Structure Profile Comparison
# ========================================================================

# --------------------------------------------------------------- _chart_structure_profile_comparison()
def _chart_structure_profile_comparison(charts_dir: Path) -> Path:
    """Qualitative comparison table of the four ADTs.

    Args:
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """
    # Define the columns
    columns = [
        "Structure",
        "Order",
        "Build O()",
        "Access End O()",
        "Search O()",
        "Middle Insert O()",
        "Use Cases",
    ]
    # Define the data
    data = [
        [
            "Stack",
            "LIFO",
            "O(n)",
            "O(1) push/pop",
            "O(n)",
            "n/a",
            "Undo, call stack, brackets",
        ],
        [
            "Queue",
            "FIFO",
            "O(n^2) (insert(0))",
            "O(1) dequeue",
            "O(n)",
            "n/a",
            "Scheduling, BFS, buffers",
        ],
        [
            "Deque",
            "Both ends",
            "addFront O(n) / addRear O(n^2)",
            "O(1) front, O(n) rear",
            "O(n)",
            "n/a",
            "Sliding windows, palindromes",
        ],
        [
            "LinkedList",
            "Sequential",
            "O(n) (insert_rear)",
            "O(1) head/tail",
            "O(n)",
            "O(1) given node",
            "Frequent middle insert/remove",
        ],
    ]
    # Define the colors
    colors = [_structure_color(row[0]) for row in data]
    # Define the column widths
    col_widths = [0.145, 0.145, 0.17, 0.145, 0.145, 0.145, 0.165]
    # Wrap the data
    wrapped_data = [
        [
            row[0],
            row[1],
            fill(str(row[2]), width=20),
            fill(str(row[3]), width=18),
            fill(str(row[4]), width=12),
            fill(str(row[5]), width=16),
            fill(str(row[6]), width=24),
        ]
        for row in data
    ]
    
    fig, ax = plt.subplots(figsize=(14.5, 4.8))
    ax.axis("off")
    table = ax.table(
        cellText=wrapped_data,
        colLabels=columns,
        colWidths=col_widths,
        cellLoc="center",
        loc="center",
    )
    # Set the font size
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    # Set the table scale
    table.scale(1.0, 2.05)

    # Style header row
    for j in range(len(columns)):
        cell = table[0, j]
        cell.set_facecolor("#2c3e50")
        cell.set_text_props(color="white", fontweight="bold")

    # Color-code structure rows by structure name column
    for i, color in enumerate(colors):
        struct_cell = table[i + 1, 0]
        struct_cell.set_facecolor(color)
        struct_cell.set_text_props(color="white", fontweight="bold")

    # Enable wrapping and add a little padding for readability.
    for (_, _), cell in table.get_celld().items():
        cell.PAD = 0.03
        cell.get_text().set_wrap(True)
    
    ax.set_title(
        "Structure Profile Comparison",
        fontsize=14,
        fontweight="bold",
        pad=18,
    )
    # Adjust the layout
    fig.tight_layout(pad=1.1)
    # Save the chart
    path = charts_dir / "structure_profile_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_structure_profile_comparison()

# __________________________________________________________________________
# Chart Orchestrator
#

# ========================================================================
# generate_charts()
# ========================================================================

# --------------------------------------------------------------- generate_charts()
def generate_charts(
    df: pd.DataFrame,
    winners_df: pd.DataFrame,
    output_dir: str | Path,
) -> list[Path]:
    """Generate all four chart PNGs from benchmark data.

    Args:
        df: Full benchmark results DataFrame.
        winners_df: Operation winners DataFrame.
        output_dir: The analysis output directory; charts go in
            ``output_dir/charts/``.

    Returns:
        List of paths to the generated chart images, in the same order
        as the chart table in ``task.md``.
    """
    output_dir = Path(output_dir)
    charts_dir = _ensure_charts_dir(output_dir)
    return [
        _chart_common_operation_runtime(df, charts_dir),
        _chart_structure_specific_runtime(df, charts_dir),
        _chart_operation_winner_heatmap(winners_df, charts_dir),
        _chart_structure_profile_comparison(charts_dir),
    ]
# --------------------------------------------------------------- end generate_charts()

# __________________________________________________________________________
# Full Report Orchestrator
#

# ========================================================================
# generate_all_reports()
# ========================================================================

# --------------------------------------------------------------- generate_all_reports()
def generate_all_reports(
    benchmark_csv_path: str | Path,
    output_dir: str | Path,
) -> dict[str, object]:
    """Orchestrate the full report pipeline.

    Loads the benchmark CSV, computes operation winners, saves the winners
    CSV, generates all four chart PNGs, and returns a dict that can be
    used to substitute placeholders in the Markdown deliverables.

    Args:
        benchmark_csv_path: Path to the benchmark results CSV.
        output_dir: The analysis output directory.

    Returns:
        A dict with keys: ``"benchmark_df"``, ``"winners_df"``,
        ``"benchmark_table"``, ``"operation_winners_table"``,
        ``"summary_sentences"``, ``"chart_paths"``.
    """
    output_dir = Path(output_dir)
    df = load_results_csv(benchmark_csv_path)
    winners_df = compute_operation_winners(df)
    save_operation_winners_csv(winners_df, output_dir / "operation_winners.csv")
    chart_paths = generate_charts(df, winners_df, output_dir)
    return {
        "benchmark_df": df,
        "winners_df": winners_df,
        "benchmark_table": build_benchmark_table(df),
        "operation_winners_table": build_operation_winners_table(winners_df),
        "summary_sentences": generate_summary_sentences(winners_df),
        "chart_paths": chart_paths,
    }
# --------------------------------------------------------------- end generate_all_reports()

# __________________________________________________________________________
# End of File
#
