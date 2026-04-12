# -------------------------------------------------------------------------
# File: report_generator.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# Converts raw benchmark output into submission-ready artifacts:
# Markdown tables, summary sentences, charts (PNG), and orchestrates
# the full report pipeline.
# -------------------------------------------------------------------------

# --- Functions ---
# - build_comparison_table()    — benchmark DataFrame → Markdown table
# - build_winner_summary()      — scenario winners → Markdown table
# - generate_summary_sentences() — human-readable winner sentences
# - generate_charts()           — save chart PNGs under analysis/charts/
# - generate_all_reports()      — orchestrator: CSV → winners → charts
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Report and chart generation for sorting benchmark results.

Reads benchmark CSVs and produces Markdown tables, summary sentences,
and matplotlib chart images for the written deliverables and the
Streamlit app.
"""

# ________________
# Imports
#

from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for PNG export
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

from analysis.benchmark_sorts import (
    load_results_csv,
    compute_scenario_winners,
    save_scenario_winners_csv,
)
from data.dataset_manager import format_dataset_type_label

# __________________________________________________________________________
# Constants
#

# Consistent algorithm color palette across all charts
ALGO_COLORS: dict[str, str] = {
    "Bubble Sort": "#e74c3c",
    "Selection Sort": "#f39c12",
    "Insertion Sort": "#2ecc71",
    "Merge Sort": "#3498db",
}

_CHARTS_DIR_NAME: str = "charts"

# __________________________________________________________________________
# Markdown Table Builders
#

# ========================================================================
# Comparison Table
# ========================================================================

# --------------------------------------------------------------- build_comparison_table()
def build_comparison_table(df: pd.DataFrame) -> str:
    """Convert a benchmark DataFrame into a human-readable Markdown table.

    Args:
        df: Benchmark results DataFrame with columns ``algorithm``,
            ``dataset_type``, ``size``, ``time_ms``, ``comparisons``,
            ``swaps``, ``writes``, ``is_correct``.

    Returns:
        A Markdown-formatted table string.
    """
    lines: list[str] = [
        "| Algorithm | Dataset Type | Size | Time (ms) | Comparisons | Swaps | Writes | Correct |",
        "|-----------|-------------|------|-----------|-------------|-------|--------|---------|",
    ]
    for _, row in df.iterrows():
        lines.append(
            f"| {row['algorithm']} | {format_dataset_type_label(str(row['dataset_type']))} | "
            f"{row['size']:,} | {row['time_ms']:.2f} | "
            f"{row['comparisons']:,} | {row['swaps']:,} | "
            f"{row['writes']:,} | {'Yes' if row['is_correct'] else 'No'} |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------- end build_comparison_table()

# ========================================================================
# Winner Summary
# ========================================================================

# --------------------------------------------------------------- build_winner_summary()
def build_winner_summary(winners_df: pd.DataFrame) -> str:
    """Convert scenario winners into a Markdown table.

    Args:
        winners_df: DataFrame from :func:`compute_scenario_winners`.

    Returns:
        A Markdown-formatted table string.
    """
    lines: list[str] = [
        "| Dataset Type | Size | Fastest Algorithm | Time (ms) | Runner-Up |",
        "|-------------|------|-------------------|-----------|-----------|",
    ]
    for _, row in winners_df.iterrows():
        lines.append(
            f"| {format_dataset_type_label(str(row['dataset_type']))} | {row['size']:,} | "
            f"{row['fastest_algorithm']} | {row['fastest_time_ms']:.2f} | "
            f"{row['runner_up_algorithm']} |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------- end build_winner_summary()

# ========================================================================
# Summary Sentences
# ========================================================================

# --------------------------------------------------------------- generate_summary_sentences()
def generate_summary_sentences(winners_df: pd.DataFrame) -> list[str]:
    """Produce human-readable sentences describing each scenario winner.

    Args:
        winners_df: DataFrame from :func:`compute_scenario_winners`.

    Returns:
        A list of sentences, one per scenario.
    """
    return [str(row["notes"]) for _, row in winners_df.iterrows()]
# --------------------------------------------------------------- end generate_summary_sentences()

# __________________________________________________________________________
# Chart Generation
#

# ========================================================================
# Chart Helpers
# ========================================================================

# --------------------------------------------------------------- _ensure_charts_dir()
def _ensure_charts_dir(output_dir: Path) -> Path:
    """Create and return the charts sub-directory.

    Args:
        output_dir: The analysis output directory.

    Returns:
        Path to the charts directory.
    """
    charts_dir = output_dir / _CHARTS_DIR_NAME
    charts_dir.mkdir(parents=True, exist_ok=True)
    return charts_dir
# --------------------------------------------------------------- end _ensure_charts_dir()

# ========================================================================
# Individual Chart Generators
# ========================================================================

# --------------------------------------------------------------- _chart_runtime_by_size()
def _chart_runtime_by_size(df: pd.DataFrame, charts_dir: Path) -> Path:
    """Line plot: runtime vs dataset size, one line per algorithm.

    Faceted by dataset type (2x2 subplot grid).

    Args:
        df: Benchmark results DataFrame.
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """
    dtypes = df["dataset_type"].unique()
    n_types = len(dtypes)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes_flat = axes.flatten()

    for idx, dtype in enumerate(dtypes):
        ax = axes_flat[idx]
        subset = df[df["dataset_type"] == dtype]
        for algo, color in ALGO_COLORS.items():
            algo_data = subset[subset["algorithm"] == algo].sort_values("size")
            ax.plot(
                algo_data["size"], algo_data["time_ms"],
                marker="o", color=color, label=algo, linewidth=2,
            )
        ax.set_title(
            format_dataset_type_label(str(dtype)),
            fontsize=12,
            fontweight="bold",
        )
        ax.set_xlabel("Dataset Size")
        ax.set_ylabel("Time (ms)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    # Hide unused subplots
    for idx in range(n_types, 4):
        axes_flat[idx].set_visible(False)

    fig.suptitle("Runtime by Dataset Size", fontsize=16, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    path = charts_dir / "runtime_by_size.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_runtime_by_size()


# --------------------------------------------------------------- _chart_runtime_by_dataset_type()
def _chart_runtime_by_dataset_type(df: pd.DataFrame, charts_dir: Path) -> Path:
    """Grouped bar chart: runtime by dataset type, grouped by algorithm.

    Faceted by dataset size (2x2 subplot grid).

    Args:
        df: Benchmark results DataFrame.
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """
    sizes = sorted(df["size"].unique())
    algos = list(ALGO_COLORS.keys())
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes_flat = axes.flatten()

    for idx, size in enumerate(sizes):
        ax = axes_flat[idx]
        subset = df[df["size"] == size]
        dtypes = subset["dataset_type"].unique()
        x_positions = range(len(dtypes))
        bar_width = 0.18

        for a_idx, algo in enumerate(algos):
            algo_data = subset[subset["algorithm"] == algo]
            # Align by dtype order
            times = []
            for dt in dtypes:
                match = algo_data[algo_data["dataset_type"] == dt]
                times.append(match["time_ms"].values[0] if len(match) > 0 else 0)
            offset = (a_idx - len(algos) / 2 + 0.5) * bar_width
            ax.bar(
                [x + offset for x in x_positions],
                times, bar_width,
                label=algo, color=ALGO_COLORS[algo],
            )

        ax.set_title(f"Size = {size:,}", fontsize=12, fontweight="bold")
        ax.set_xticks(list(x_positions))
        ax.set_xticklabels(
            [format_dataset_type_label(str(dt)) for dt in dtypes],
            fontsize=8, rotation=15,
        )
        ax.set_ylabel("Time (ms)")
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3, axis="y")

    for idx in range(len(sizes), 4):
        axes_flat[idx].set_visible(False)

    fig.suptitle("Runtime by Dataset Type", fontsize=16, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    path = charts_dir / "runtime_by_dataset_type.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_runtime_by_dataset_type()


# --------------------------------------------------------------- _chart_scenario_winner_heatmap()
def _chart_scenario_winner_heatmap(
    winners_df: pd.DataFrame,
    charts_dir: Path,
) -> Path:
    """Heatmap: rows = dataset types, cols = sizes, cells = winner + time.

    Args:
        winners_df: Scenario winners DataFrame.
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """
    algos = list(ALGO_COLORS.keys())
    algo_to_num = {a: i for i, a in enumerate(algos)}
    cmap_colors = [ALGO_COLORS[a] for a in algos]
    cmap = mcolors.ListedColormap(cmap_colors)

    pivot = winners_df.pivot(
        index="dataset_type", columns="size", values="fastest_algorithm",
    )
    time_pivot = winners_df.pivot(
        index="dataset_type", columns="size", values="fastest_time_ms",
    )
    preferred_dtype_order = [
        "random_unsorted",
        "reverse_sorted",
        "partially_sorted",
        "sorted",
    ]
    sizes = sorted(winners_df["size"].unique())
    dtypes = [
        dtype for dtype in preferred_dtype_order
        if dtype in winners_df["dataset_type"].unique()
    ]
    dtypes.extend(
        sorted(
            dtype for dtype in winners_df["dataset_type"].unique()
            if dtype not in dtypes
        )
    )
    pivot = pivot.reindex(index=dtypes, columns=sizes)
    time_pivot = time_pivot.reindex(index=dtypes, columns=sizes)

    num_grid = pivot.map(lambda x: algo_to_num.get(x, -1))

    fig_width = max(9, len(sizes) * 2.2)
    fig_height = max(4.8, len(dtypes) * 1.25 + 1.8)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.imshow(
        num_grid.values, cmap=cmap, aspect="auto",
        vmin=0, vmax=len(algos) - 1,
    )

    # Add crisp cell borders so each scenario reads like a matrix cell.
    ax.set_xticks([x - 0.5 for x in range(1, len(sizes))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(dtypes))], minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)

    def _annotation_color(algorithm: str) -> str:
        """Choose readable text color based on cell fill."""
        cell_hex = ALGO_COLORS.get(algorithm, "#666666")
        red, green, blue = mcolors.to_rgb(cell_hex)
        luminance = (0.299 * red) + (0.587 * green) + (0.114 * blue)
        return "#1f1f1f" if luminance > 0.62 else "white"

    # Annotate cells with algorithm name and winning runtime.
    for i in range(len(dtypes)):
        for j in range(len(sizes)):
            winner = pivot.iloc[i, j]
            time_ms = time_pivot.iloc[i, j]
            if pd.isna(winner) or pd.isna(time_ms):
                cell_text = "No data"
                text_color = "#1f1f1f"
            else:
                winner_label = str(winner).replace(" Sort", "")
                cell_text = f"{winner_label}\n{float(time_ms):.2f} ms"
                text_color = _annotation_color(str(winner))
            ax.text(
                j, i, cell_text,
                ha="center", va="center",
                fontsize=10, fontweight="bold", color=text_color,
            )

    ax.set_xticks(range(len(sizes)))
    ax.set_xticklabels([f"{s:,}" for s in sizes])
    ax.set_yticks(range(len(dtypes)))
    ax.set_yticklabels([format_dataset_type_label(str(dt)) for dt in dtypes])
    ax.set_xlabel("Dataset Size")
    ax.set_ylabel("Dataset Type")
    ax.set_title(
        "Fastest Algorithm by Dataset Type and Size",
        fontsize=14,
        fontweight="bold",
        pad=12,
    )
    visible_algorithms = [
        algo for algo in algos
        if algo in set(winners_df["fastest_algorithm"].dropna().tolist())
    ]
    legend_handles = [
        Patch(facecolor=ALGO_COLORS[algo], edgecolor="none", label=algo)
        for algo in visible_algorithms
    ]
    ax.legend(
        handles=legend_handles,
        title="Cell Color = Winner",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=max(1, len(legend_handles)),
        frameon=False,
        fontsize=9,
        title_fontsize=9,
    )
    fig.text(
        0.5,
        0.02,
        "Each cell shows the fastest algorithm and its winning runtime for that scenario.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    path = charts_dir / "scenario_winner_heatmap.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_scenario_winner_heatmap()


# --------------------------------------------------------------- _chart_algorithm_profile_comparison()
def _chart_algorithm_profile_comparison(charts_dir: Path) -> Path:
    """Table chart: qualitative comparison of algorithm properties.

    Shows time complexity (best/avg/worst), space, stability, and in-place
    properties for all four algorithms.

    Args:
        charts_dir: Output directory for the PNG.

    Returns:
        Path to the saved chart image.
    """
    columns = [
        "Algorithm", "Best", "Average", "Worst",
        "Space", "Stable", "In-Place",
    ]
    data = [
        ["Bubble Sort", "O(n)", "O(n\u00b2)", "O(n\u00b2)", "O(1)", "Yes", "Yes"],
        ["Selection Sort", "O(n\u00b2)", "O(n\u00b2)", "O(n\u00b2)", "O(1)", "No", "Yes"],
        ["Insertion Sort", "O(n)", "O(n\u00b2)", "O(n\u00b2)", "O(1)", "Yes", "Yes"],
        ["Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Yes", "No"],
    ]
    colors = [ALGO_COLORS[row[0]] for row in data]

    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.axis("off")
    table = ax.table(
        cellText=data,
        colLabels=columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.8)

    # Style header row
    for j in range(len(columns)):
        cell = table[0, j]
        cell.set_facecolor("#2c3e50")
        cell.set_text_props(color="white", fontweight="bold")

    # Color-code algorithm rows
    for i, color in enumerate(colors):
        table[i + 1, 0].set_facecolor(color)
        table[i + 1, 0].set_text_props(color="white", fontweight="bold")

    ax.set_title(
        "Algorithm Profile Comparison",
        fontsize=14, fontweight="bold", pad=20,
    )
    fig.tight_layout()
    path = charts_dir / "algorithm_profile_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------- end _chart_algorithm_profile_comparison()

# ========================================================================
# Chart Orchestrator
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
        winners_df: Scenario winners DataFrame.
        output_dir: The analysis output directory (charts go in a
            ``charts/`` sub-directory).

    Returns:
        List of paths to the generated chart images.
    """
    output_dir = Path(output_dir)
    charts_dir = _ensure_charts_dir(output_dir)
    paths: list[Path] = [
        _chart_runtime_by_size(df, charts_dir),
        _chart_runtime_by_dataset_type(df, charts_dir),
        _chart_scenario_winner_heatmap(winners_df, charts_dir),
        _chart_algorithm_profile_comparison(charts_dir),
    ]
    return paths
# --------------------------------------------------------------- end generate_charts()

# __________________________________________________________________________
# Full Report Orchestrator
#

# ========================================================================
# Generate All Reports
# ========================================================================

# --------------------------------------------------------------- generate_all_reports()
def generate_all_reports(
    benchmark_csv_path: str | Path,
    output_dir: str | Path,
) -> dict[str, object]:
    """Orchestrate the full report pipeline.

    Loads the benchmark CSV, computes scenario winners, saves the winners
    CSV, and generates all charts.

    Args:
        benchmark_csv_path: Path to the benchmark results CSV.
        output_dir: The analysis output directory.

    Returns:
        A dict with keys: ``"benchmark_df"``, ``"winners_df"``,
        ``"comparison_table"``, ``"winner_summary"``,
        ``"summary_sentences"``, ``"chart_paths"``.
    """
    output_dir = Path(output_dir)
    df = load_results_csv(benchmark_csv_path)
    winners_df = compute_scenario_winners(df)
    save_scenario_winners_csv(winners_df, output_dir / "scenario_winners.csv")
    chart_paths = generate_charts(df, winners_df, output_dir)

    return {
        "benchmark_df": df,
        "winners_df": winners_df,
        "comparison_table": build_comparison_table(df),
        "winner_summary": build_winner_summary(winners_df),
        "summary_sentences": generate_summary_sentences(winners_df),
        "chart_paths": chart_paths,
    }
# --------------------------------------------------------------- end generate_all_reports()

# __________________________________________________________________________
# End of File
#
