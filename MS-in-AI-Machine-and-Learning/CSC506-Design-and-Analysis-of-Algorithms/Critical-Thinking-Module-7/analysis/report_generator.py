# File: report_generator.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# Report tables and matplotlib charts for CTA-7 graph benchmarks.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - Markdown table helpers summarize benchmark CSV data for written analysis.
# - Chart helpers create static report images for runtime and recommendation views.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Used by Streamlit, tests, and the written-analysis artifact workflow.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Report and chart helpers for CTA-7."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

import math
import shutil
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
# Import graph algorithms
from algorithms.graph_algorithms import (
    bellman_ford_shortest_path,
    breadth_first_search,
    dijkstra_shortest_path,
)
# Import graph protocol
from algorithms.graph_protocol import WeightedGraph
# Import benchmark graphs
from analysis.benchmark_graphs import compute_operation_winners
# Import graph dataset manager
from data.graph_dataset_manager import (
    build_graph,
    generate_classroom_graph_data,
    generate_negative_weight_cost_graph_data,
    generate_positive_distance_graph_data,
    generate_positive_weighted_positive_route_demo_graph_data,
)   
# Import graph label utils
from ui.graph_label_utils import wrap_vertex_label
# Import graphviz visuals
from ui.graphviz_visuals import build_graphviz_dot

# ______________________________________________________________________________
#
# ==============================================================================
# REPORT STYLE CONSTANTS
# ==============================================================================
# Centralized labels, colors, markers, and ordering keep charts consistent.
# ------------------------------------------------------------------------------

METHOD_COLORS: dict[str, str] = {
    "Adjacency List": "#2f6db3",
    "Adjacency Matrix": "#d95f5f",
}
"""Consistent chart colors for representation comparison."""

RUNTIME_SERIES_COLORS: dict[tuple[str, str], str] = {
    ("Adjacency List", "bfs"): "#2563eb",
    ("Adjacency List", "dfs"): "#0f766e",
    ("Adjacency List", "dijkstra"): "#1d4ed8",
    ("Adjacency List", "bellman_ford"): "#0891b2",
    ("Adjacency Matrix", "bfs"): "#dc2626",
    ("Adjacency Matrix", "dfs"): "#9333ea",
    ("Adjacency Matrix", "dijkstra"): "#b91c1c",
    ("Adjacency Matrix", "bellman_ford"): "#c2410c",
}
"""Distinct operation colors for runtime line charts."""

OPERATION_MARKERS: dict[str, str] = {
    "bfs": "o",
    "dfs": "s",
    "dijkstra": "^",
    "bellman_ford": "D",
}
"""Marker shapes that make operation series easier to distinguish."""

GROUP_LABELS: dict[str, str] = {
    "construction": "Construction",
    "adjacency_queries": "Adjacency Queries",
    "neighbor_scan": "Neighbor Scan",
    "traversal": "Traversal",
    "shortest_path": "Shortest Path",
    "mutation": "Mutation",
}
"""Human-readable labels for benchmark operation groups."""

_GROUP_ORDER: tuple[str, ...] = (
    "construction",
    "adjacency_queries",
    "neighbor_scan",
    "traversal",
    "shortest_path",
    "mutation",
)

_OPERATION_ORDER: tuple[str, ...] = (
    "build",
    "adjacency_check",
    "neighbor_scan",
    "bfs",
    "dfs",
    "dijkstra",
    "bellman_ford",
    "remove_edges",
)


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# MARKDOWN TABLE BUILDERS
# ==============================================================================
# Convert benchmark DataFrames into compact tables for written analysis.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- build_benchmark_table()
def build_benchmark_table(df: pd.DataFrame) -> str:
    """Convert benchmark rows into a Markdown table.

    Args:
        df: Benchmark DataFrame.

    Returns:
        Markdown table.
    """
    lines = [
        "| Graph | Structure | Operation | Group | V | E | Time (ms) | Avg (us) | Correct | Complexity |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    sorted_df = df.sort_values(
        by=["graph_kind", "operation_group", "operation", "structure", "size"],
        kind="stable",
    )
    # MAIN ITERATION LOOP: render one benchmark row per Markdown table row
    for _, row in sorted_df.iterrows():
        group_label = GROUP_LABELS.get(str(row["operation_group"]), str(row["operation_group"]))
        lines.append(
            f"| {row['graph_kind']} | {row['structure']} | {row['operation']} "
            f"| {group_label} "
            f"| {int(row['size']):,} | {int(row['edge_count']):,} "
            f"| {float(row['time_ms']):.4f} | {float(row['avg_time_us']):.4f} "
            f"| {'Yes' if bool(row['is_correct']) else 'No'} | {row['complexity']} |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_operation_scaling_table()
def build_operation_scaling_table(df: pd.DataFrame) -> str:
    """Convert scaling summary rows into Markdown.

    Args:
        df: Scaling summary DataFrame.

    Returns:
        Markdown table.
    """
    lines = [
        "| Graph | Structure | Operation | Smallest V | Largest V | Smallest (ms) | Largest (ms) | Growth |",
        "|---|---|---|---|---|---|---|---|",
    ]
    sorted_df = df.sort_values(
        by=["graph_kind", "operation", "structure"],
        kind="stable",
    )
    # MAIN ITERATION LOOP: render one scaling summary row
    for _, row in sorted_df.iterrows():
        lines.append(
            f"| {row['graph_kind']} | {row['structure']} | {row['operation']} "
            f"| {int(row['smallest_size']):,} | {int(row['largest_size']):,} "
            f"| {float(row['smallest_time_ms']):.4f} | {float(row['largest_time_ms']):.4f} "
            f"| {float(row['growth_factor']):.2f}x |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_operation_winners_table()
def build_operation_winners_table(df: pd.DataFrame) -> str:
    """Convert operation-winner rows into Markdown.

    Args:
        df: Operation winners DataFrame.

    Returns:
        Markdown table.
    """
    lines = [
        "| Graph | Operation | Group | V | Fastest Structure | Time (ms) | Runner-Up | Gap |",
        "|---|---|---|---|---|---|---|---|",
    ]
    if df.empty:
        return "\n".join(lines)
    sorted_df = df.sort_values(
        by=["graph_kind", "operation_group", "operation", "size"],
        kind="stable",
    )
    # MAIN ITERATION LOOP: render one winner row per graph-operation bucket
    for _, row in sorted_df.iterrows():
        group_label = GROUP_LABELS.get(str(row["operation_group"]), str(row["operation_group"]))
        lines.append(
            f"| {row['graph_kind']} | {row['operation']} | {group_label} "
            f"| {int(row['size']):,} | {row['fastest_structure']} "
            f"| {float(row['fastest_time_ms']):.4f} | {row['runner_up']} "
            f"| {float(row['pct_faster_than_runner_up']):.1f}% |"
        )
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# REPORT SORTING AND CHART STYLE HELPERS
# ==============================================================================
# Keep report tables and chart series ordered consistently across artifacts.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _operation_sort_key()
def _operation_sort_key(operation: object) -> tuple[int, str]:
    """Return a stable sort key for operation labels.

    Args:
        operation: Operation label.

    Returns:
        Tuple suitable for sorting.
    """
    operation_text = str(operation)
    if operation_text in _OPERATION_ORDER:
        return (_OPERATION_ORDER.index(operation_text), operation_text)
    return (len(_OPERATION_ORDER), operation_text)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _group_sort_key()
def _group_sort_key(group: object) -> tuple[int, str]:
    """Return a stable sort key for operation groups.

    Args:
        group: Operation-group label.

    Returns:
        Tuple suitable for sorting.
    """
    group_text = str(group)
    if group_text in _GROUP_ORDER:
        return (_GROUP_ORDER.index(group_text), group_text)
    return (len(_GROUP_ORDER), group_text)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _runtime_series_style()
def _runtime_series_style(structure: str, operation: str) -> dict[str, object]:
    """Return line-chart styling for a benchmark series.

    Args:
        structure: Graph representation name.
        operation: Benchmark operation name.

    Returns:
        Matplotlib style keyword arguments.
    """
    color = RUNTIME_SERIES_COLORS.get(
        (structure, operation),
        METHOD_COLORS.get(structure, "#6b7280"),
    )
    return {
        "color": color,
        "marker": OPERATION_MARKERS.get(operation, "o"),
        "linestyle": "--" if operation in {"dfs", "bellman_ford"} else "-",
    }
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _positive_log_floor()
def _positive_log_floor(values: pd.Series) -> float:
    """Return a safe positive lower bound for log charts.

    Args:
        values: Runtime values.

    Returns:
        Positive lower y-axis bound.
    """
    positive = values[values > 0]
    if positive.empty:
        return 1e-6
    return max(float(positive.min()) / 2.0, 1e-6)
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _style_runtime_axis()
def _style_runtime_axis(ax: plt.Axes, values: pd.Series) -> None:
    """Style a runtime y-axis.

    Args:
        ax: Axes to style.
        values: Runtime values represented by the axis.

    Returns:
        None.
    """
    if (values > 0).all():
        ax.set_yscale("log")
        ax.set_ylim(bottom=_positive_log_floor(values))
    ax.grid(True, which="major", axis="both", alpha=0.25, linewidth=0.7)
    ax.grid(True, which="minor", axis="y", alpha=0.12, linewidth=0.45)
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# BENCHMARK CHART BUILDERS
# ==============================================================================
# Build matplotlib images that explain runtime, density, and winner trends.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _chart_runtime_by_group()
def _chart_runtime_by_group(df: pd.DataFrame, output_dir: Path) -> Path:
    """Generate runtime line charts faceted by operation group.

    Args:
        df: Benchmark DataFrame.
        output_dir: Chart output directory.

    Returns:
        Saved chart path.
    """
    groups = sorted(df["operation_group"].unique(), key=_group_sort_key)
    columns = 2
    rows = max(math.ceil(len(groups) / columns), 1)
    fig, axes = plt.subplots(rows, columns, figsize=(14, 4.5 * rows), squeeze=False)
    axes_flat = axes.flatten()
    # MAIN ITERATION LOOP: draw one panel per operation group
    for index, group in enumerate(groups):
        # get the current axes
        ax = axes_flat[index]
        subset = df[df["operation_group"] == group].copy()
        subset["series"] = subset["structure"].astype(str) + "." + subset["operation"].astype(str)
        # group by series
        for series, series_df in subset.groupby("series", sort=False):
            ordered = series_df.sort_values("size", kind="stable")
            structure = str(ordered["structure"].iloc[0])
            operation = str(ordered["operation"].iloc[0])
            series_style = _runtime_series_style(structure, operation)
            ax.plot(
                ordered["size"],
                ordered["time_ms"],
                linewidth=1.9,
                label=series,
                alpha=0.78 if "." in series else 1.0,
                **series_style,
            )
        # set title for current axes
        ax.set_title(GROUP_LABELS.get(str(group), str(group)), fontweight="bold")
        # set x and y labels
        ax.set_xlabel("Vertices")
        ax.set_ylabel("Time (ms)")
        # style the y-axis
        _style_runtime_axis(ax, subset["time_ms"])
        # set the legend
        ax.legend(fontsize=7, loc="best")
    # remove unused axes
    for index in range(len(groups), len(axes_flat)):
        axes_flat[index].set_visible(False)
    # set the suptitle
    fig.suptitle("Benchmark Runtime by Operation Group", fontsize=15, fontweight="bold")
    # adjust layout
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    # save the figure
    path = output_dir / "runtime_by_operation_group.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _chart_density_comparison()
def _chart_density_comparison(df: pd.DataFrame, output_dir: Path) -> Path:
    """Generate sparse-vs-dense runtime comparison for the largest size.

    Args:
        df: Benchmark DataFrame.
        output_dir: Chart output directory.

    Returns:
        Saved chart path.
    """
    largest_size = int(df["size"].max())
    subset = df[df["size"] == largest_size].copy()
    graph_kinds = sorted(subset["graph_kind"].unique())
    fig, axes = plt.subplots(1, max(len(graph_kinds), 1), figsize=(15, 5), squeeze=False)
    axes_flat = axes.flatten()
    # MAIN ITERATION LOOP: compare operations within each density class
    for index, graph_kind in enumerate(graph_kinds):
        ax = axes_flat[index]
        graph_df = subset[subset["graph_kind"] == graph_kind].copy()
        operations = sorted(graph_df["operation"].unique(), key=_operation_sort_key)
        x_positions = list(range(len(operations)))
        bar_width = 0.36
        # MAIN ITERATION LOOP: draw one bar per structure
        for offset_index, structure in enumerate(("Adjacency List", "Adjacency Matrix")):
            times: list[float] = []
            # MAIN ITERATION LOOP: draw one bar per operation
            for operation in operations:
                row = graph_df[
                    (graph_df["structure"] == structure)
                    & (graph_df["operation"] == operation)
                ]
                # get the time for the current operation    
                times.append(float(row["time_ms"].iloc[0]) if not row.empty else 0.0)
            # set the offset for the current structure
            offset = -bar_width / 2 if offset_index == 0 else bar_width / 2
            # draw the bar
            ax.bar(
                [x + offset for x in x_positions],
                times,
                width=bar_width,
                label=structure,
                color=METHOD_COLORS.get(structure, "#6b7280"),
            )
        ax.set_title(f"{str(graph_kind).title()} graph, V={largest_size:,}", fontweight="bold")
        ax.set_xticks(x_positions)
        ax.set_xticklabels(operations, rotation=35, ha="right", fontsize=8)
        ax.set_ylabel("Time (ms)")
        _style_runtime_axis(ax, graph_df["time_ms"])
        ax.legend(fontsize=8)
    # set the suptitle  
    fig.suptitle("Sparse vs. Dense Runtime at Largest Benchmarked Size", fontsize=15, fontweight="bold")
    # adjust layout
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    # save the figure
    path = output_dir / "sparse_dense_runtime_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _annotation_color()
def _annotation_color(structure: str) -> str:
    """Return readable text color for a representation-colored cell.

    Args:
        structure: Representation name.

    Returns:
        Hex color string.
    """
    fill = METHOD_COLORS.get(structure, "#e5e7eb")
    red, green, blue = mcolors.to_rgb(fill)
    luminance = (0.299 * red) + (0.587 * green) + (0.114 * blue)
    return "#111827" if luminance > 0.62 else "white"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _chart_winner_heatmap()
def _chart_winner_heatmap(winners_df: pd.DataFrame, output_dir: Path) -> Path:
    """Generate a heatmap of fastest representation winners.

    Args:
        winners_df: Operation winners DataFrame.
        output_dir: Chart output directory.

    Returns:
        Saved chart path.
    """
    # set the structures
    structures = ["Adjacency List", "Adjacency Matrix"]
    # set the structure to number mapping
    structure_to_num = {structure: index for index, structure in enumerate(structures)}
    # set the colormap
    cmap = mcolors.ListedColormap([METHOD_COLORS[structure] for structure in structures])
    # set the sizes
    sizes = sorted(winners_df["size"].unique())
    # copy the winners dataframe
    ordered = winners_df.copy()
    # set the row labels
    ordered["row_label"] = ordered["graph_kind"].astype(str) + " / " + ordered["operation"].astype(str)
    # set the row order
    row_order = sorted(
        ordered[["graph_kind", "operation", "row_label"]].drop_duplicates().itertuples(index=False),
        key=lambda row: (str(row.graph_kind), _operation_sort_key(row.operation)),
    )
    # set the row labels
    row_labels = [str(row.row_label) for row in row_order]
    # set the pivot
    pivot = ordered.pivot(index="row_label", columns="size", values="fastest_structure").reindex(
        index=row_labels,
        columns=sizes,
    )
    # set the time pivot
    time_pivot = ordered.pivot(index="row_label", columns="size", values="fastest_time_ms").reindex(
        index=row_labels,
        columns=sizes,
    )
    # get the grid
    grid = pivot.map(lambda value: structure_to_num.get(value, 0)).to_numpy()
    # set the figure width and height
    fig_width = max(10, len(sizes) * 2.2)
    fig_height = max(6, len(row_labels) * 0.55 + 2)
    # create the figure and axes
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    # display the heatmap
    ax.imshow(grid, cmap=cmap, aspect="auto", vmin=0, vmax=len(structures) - 1)
    # MAIN ITERATION LOOP: iterate over rows and columns
    for row_index, row_label in enumerate(row_labels):
        # MAIN ITERATION LOOP: iterate over columns 
        for column_index, size in enumerate(sizes):
            # get the winner
            winner = pivot.loc[row_label, size]
            # get the time
            time_ms = time_pivot.loc[row_label, size]
            # check if the winner or time is NaN
            if pd.isna(winner) or pd.isna(time_ms):
                cell_text = "no data"
                text_color = "#111827"
            else:
                cell_text = f"{winner}\n{float(time_ms):.3f} ms"
                text_color = _annotation_color(str(winner))
            ax.text(
                column_index,
                row_index,
                cell_text,
                ha="center",
                va="center",
                fontsize=8,
                fontweight="bold",
                color=text_color,
            )
    ax.set_xticks(range(len(sizes)))
    ax.set_xticklabels([f"{size:,}" for size in sizes])
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=8)
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Graph / Operation")
    ax.set_title("Fastest Representation by Graph Density, Operation, and Size", fontweight="bold")
    ax.set_xticks([x - 0.5 for x in range(1, len(sizes))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(row_labels))], minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    legend_handles = [
        Patch(facecolor=METHOD_COLORS[structure], edgecolor="none", label=structure)
        for structure in structures
    ]
    # set the legend  
    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        frameon=False,
    )
    # adjust the layout 
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    # save the figure
    path = output_dir / "operation_winner_heatmap.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _chart_representation_profile()
def _chart_representation_profile(output_dir: Path) -> Path:
    """Generate a qualitative adjacency-list vs matrix profile chart.

    Args:
        output_dir: Chart output directory.

    Returns:
        Saved chart path.
    """
    columns = [
        "Representation",
        "Space",
        "Adjacency",
        "Neighbor Scan",
        "Traversal",
        "Best Fit",
    ]
    rows = [
        [
            "Adjacency List",
            "O(V + E)",
            "O(deg(V))",
            "O(deg(V))",
            "O(V + E)",
            "Sparse, growing, traversal-heavy graphs",
        ],
        [
            "Adjacency Matrix",
            "O(V^2)",
            "O(1)",
            "O(V)",
            "O(V^2)",
            "Dense, stable graphs with many edge queries",
        ],
    ]
    # set the figure and axes
    fig, ax = plt.subplots(figsize=(13, 3.2))
    # turn off the axes
    ax.axis("off")
    # set the table
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        colWidths=[0.16, 0.12, 0.14, 0.15, 0.14, 0.29],
        cellLoc="center",
        loc="center",
    )
    # auto set font size
    table.auto_set_font_size(False)
    # set the font size
    table.set_fontsize(9)
    # scale the table
    table.scale(1.0, 1.85)
    # MAIN ITERATION LOOP: iterate over columns
    for column_index in range(len(columns)):
        # get the cell
        cell = table[0, column_index]
        cell.set_facecolor("#111827")
        cell.set_text_props(color="white", fontweight="bold")
    # MAIN ITERATION LOOP: iterate over rows
    for row_index, row in enumerate(rows, start=1):
        # get the cell
        cell = table[row_index, 0]
        # set the cell face color
        cell.set_facecolor(METHOD_COLORS[row[0]])
        cell.set_text_props(color="white", fontweight="bold")
    # MAIN ITERATION LOOP: iterate over cells
    for cell in table.get_celld().values():
        # set the cell padding
        cell.PAD = 0.03
        # wrap the cell text
        cell.get_text().set_wrap(True)
    # set the title 
    ax.set_title("Adjacency List vs. Adjacency Matrix Profile", fontsize=14, fontweight="bold", pad=14)
    # adjust the layout 
    fig.tight_layout(pad=1.0)
    # save the figure
    path = output_dir / "representation_profile_comparison.png"
    # save the figure
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# CHART ORCHESTRATION
# ==============================================================================
# Coordinates all benchmark charts and returns paths for Streamlit/report display.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- generate_charts()
def generate_charts(
    df: pd.DataFrame,
    output_dir: Path,
    winners_df: pd.DataFrame | None = None,
) -> list[Path]:
    """Generate benchmark PNG charts.

    Args:
        df: Benchmark DataFrame.
        output_dir: Directory where PNG files should be written.
        winners_df: Optional precomputed operation-winner DataFrame.

    Returns:
        List of generated chart paths.
    """
    # create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    # check if the dataframe is empty 
    if df.empty:
        return []
    # set the winners dataframe
    winners = winners_df if winners_df is not None else compute_operation_winners(df)
    # set the paths
    paths = [
        _chart_runtime_by_group(df, output_dir),
        _chart_density_comparison(df, output_dir),
    ]
    # check if the winners dataframe is not empty
    if not winners.empty:
        # append the heatmap
        paths.append(_chart_winner_heatmap(winners, output_dir))
    # append the representation profile
    paths.append(_chart_representation_profile(output_dir))
    # return the paths 
    return [path for path in paths if path.exists()]
# --------------------------------------------------------------------------------


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# WRITTEN ANALYSIS GRAPH EXPORT HELPERS
# ==============================================================================
# Render curated graph examples as images for the written analysis artifacts.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- write_graphviz_png()
def write_graphviz_png(dot_source: str, output_path: Path) -> Path:
    """Render Graphviz DOT source to a PNG file with the local ``dot`` command.

    Args:
        dot_source: Graphviz DOT source text.
        output_path: Destination PNG path.

    Returns:
        Saved PNG path.

    Raises:
        RuntimeError: If the Graphviz ``dot`` command is unavailable or fails.
    """
    dot_path = shutil.which("dot")
    # check if the dot path is None
    if dot_path is None:
        raise RuntimeError("Graphviz dot command is required to render graph PNGs.")
    # create the output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # run the subprocess
    completed = subprocess.run(
        [dot_path, "-Tpng", "-o", str(output_path)],
        input=dot_source,
        text=True,
        capture_output=True,
        check=False,
    )
    # check if the subprocess return code is not 0
    if completed.returncode != 0:
        message = completed.stderr.strip() or "Graphviz dot failed without an error message."
        raise RuntimeError(message)
    return output_path
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- generate_written_analysis_graphs()
def generate_written_analysis_graphs(output_dir: Path) -> list[Path]:
    """Generate Written Analysis graph figures with the shared Graphviz style.

    Args:
        output_dir: Directory where Written Analysis graph PNG files are saved.

    Returns:
        List of generated graph PNG paths.
    """
    # create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    # create an empty list of paths
    paths: list[Path] = []
    # generate the structure vertices and edges
    structure_vertices, structure_edges = generate_positive_weighted_positive_route_demo_graph_data()
    # build the structure graph
    structure_graph = build_graph("list", structure_vertices, structure_edges)
    # append the graph to the paths list
    paths.append(
        write_graphviz_png(
            build_graphviz_dot(
                structure_graph,
                title="Generated Graph",
                show_edge_weights=True,
                compact=False,
            ),
            output_dir / "written_analysis_structure_route_graph.png",
        )
    )

    # generate the traversal vertices and edges
    traversal_vertices, traversal_edges = generate_classroom_graph_data()
    # build the traversal graph
    traversal_graph = build_graph("list", traversal_vertices, traversal_edges)
    # append the graph to the paths list
    paths.append(
        write_graphviz_png(
            build_graphviz_dot(
                traversal_graph,
                title="Generated Graph",
                show_edge_weights=False,
                compact=False,
            ),
            output_dir / "written_analysis_traversal_graph.png",
        )
    )

    # run the breadth-first search
    bfs_result = breadth_first_search(traversal_graph, "A")
    # get the final breadth-first search step
    final_bfs_step = bfs_result.steps[-1]
    # append the graph to the paths list
    paths.append(
        write_graphviz_png(
            build_graphviz_dot(
                traversal_graph,
                title=(
                    "Adjacency List Representation "
                    f"{bfs_result.algorithm} Step {final_bfs_step.step_number}: "
                    f"{final_bfs_step.current_vertex}"
                ),
                highlighted_vertices=final_bfs_step.visited,
                highlighted_edges=final_bfs_step.traversed_edges,
                current_vertex=final_bfs_step.current_vertex,
                frontier_vertices=final_bfs_step.frontier,
                discovered_vertices=final_bfs_step.discovered,
                show_edge_weights=False,
                compact=False,
            ),
            output_dir / "written_analysis_traversal_lab_bfs_result.png",
        )
    )

    # generate the positive vertices and edges
    positive_vertices, positive_edges = generate_positive_distance_graph_data()
    # build the positive graph
    positive_graph = build_graph("list", positive_vertices, positive_edges)
    # run the dijkstra shortest path
    positive_result = dijkstra_shortest_path(positive_graph, "Denver", "Vail")
    # append the graph to the paths list
    paths.append(
        write_graphviz_png(
            build_graphviz_dot(
                positive_graph,
                title=f"{positive_result.algorithm} Shortest Path Result",
                highlighted_path=positive_result.path,
                show_edge_weights=True,
                compact=False,
            ),
            output_dir / "written_analysis_positive_shortest_path.png",
        )
    )

    # generate the negative vertices and edges
    negative_vertices, negative_edges = generate_negative_weight_cost_graph_data()
    # build the negative graph
    negative_graph = build_graph("list", negative_vertices, negative_edges, directed=True)
    # run the bellman-ford shortest path
    negative_result = bellman_ford_shortest_path(
        negative_graph,
        "Start Purchase",
        "Order Complete",
    )
    # append the graph to the paths list
    paths.append(
        write_graphviz_png(
            build_graphviz_dot(
                negative_graph,
                title=f"{negative_result.algorithm} Shortest Path Result",
                highlighted_path=negative_result.path,
                show_edge_weights=True,
                compact=False,
            ),
            output_dir / "written_analysis_negative_cost_path.png",
        )
    )

    return paths
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _edge_label_position()
def _edge_label_position(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label_index: int,
) -> tuple[float, float]:
    """Calculate a readable edge-label position near an edge.

    Args:
        x1: Source vertex x-coordinate.
        y1: Source vertex y-coordinate.
        x2: Target vertex x-coordinate.
        y2: Target vertex y-coordinate.
        label_index: Count of earlier labels sharing the same midpoint.

    Returns:
        Offset ``(x, y)`` coordinates for the label.
    """
    # calculate the difference in x and y coordinates
    delta_x = x2 - x1
    delta_y = y2 - y1
    anchor_pattern = (0.50, 0.42, 0.58, 0.35, 0.65)
    anchor = anchor_pattern[label_index % len(anchor_pattern)]
    # calculate the base x and y coordinates
    base_x = x1 + delta_x * anchor
    base_y = y1 + delta_y * anchor
    # calculate the distance between the two points
    distance = math.hypot(delta_x, delta_y)
    # check if the distance is 0
    if distance == 0:
        return base_x, base_y

    offset_pattern = (0.10, -0.10, 0.16, -0.16)
    offset = offset_pattern[label_index % len(offset_pattern)]
    # calculate the tier
    tier = label_index // len(offset_pattern)
    # check if the tier is not 0
    if tier:
        offset += 0.04 * tier if offset > 0 else -0.04 * tier

    # READABILITY: Shift labels perpendicular to the edge so they do not sit on
    # top of crossing lines or each other.
    # calculate the normal x and y coordinates
    normal_x = -delta_y / distance
    normal_y = delta_x / distance
    return base_x + normal_x * offset, base_y + normal_y * offset
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_graph_figure()
def build_graph_figure(
    graph: WeightedGraph,
    *,
    title: str,
    highlighted_vertices: list[str] | None = None,
    highlighted_path: list[str] | None = None,
) -> plt.Figure:
    """Build a custom matplotlib graph visualization.

    Args:
        graph: Graph to draw.
        title: Figure title.
        highlighted_vertices: Vertices to emphasize.
        highlighted_path: Source-to-target path to emphasize.

    Returns:
        Matplotlib figure.
    """ 
    # get the vertices
    vertices = graph.vertices()
    # set the highlighted vertices
    highlighted_vertices = highlighted_vertices or []
    # set the highlighted path
    highlighted_path = highlighted_path or []
    # set the path edges
    path_edges = set(zip(highlighted_path, highlighted_path[1:]))
    # check if the graph is not directed
    if not graph.directed:
        path_edges.update((b, a) for a, b in list(path_edges))

    # create the figure and axes
    fig, ax = plt.subplots(figsize=(7, 5))
    # set the title
    ax.set_title(title)
    # turn off the axis
    ax.axis("off")
    # check if there are no vertices
    if not vertices:
        ax.text(0.5, 0.5, "Empty graph", ha="center", va="center")
        return fig
    # set the radius    
    radius = 1.0
    # set the positions
    positions: dict[str, tuple[float, float]] = {}
    # MAIN ITERATION LOOP: place vertices around a stable circle
    for index, vertex in enumerate(vertices):
        angle = 2.0 * math.pi * index / len(vertices)
        positions[vertex] = (math.cos(angle) * radius, math.sin(angle) * radius)
    
    # set the midpoint counts
    midpoint_counts: dict[tuple[float, float], int] = {}
    # MAIN ITERATION LOOP: iterate over the edges
    for edge in graph.edges():
        x1, y1 = positions[edge.source]
        x2, y2 = positions[edge.target]
        is_highlight = (edge.source, edge.target) in path_edges
        # set the edge color
        color = "#2f6db3" if is_highlight else "#777777"
        # set the edge width
        width = 2.8 if is_highlight else 1.1
        # draw the edge
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops={
                "arrowstyle": "->" if graph.directed else "-",
                "color": color,
                "lw": width,
                "shrinkA": 18,
                "shrinkB": 18,
            },
        )
        # calculate the midpoint key
        midpoint_key = (round((x1 + x2) / 2, 3), round((y1 + y2) / 2, 3))
        # get the label index
        label_index = midpoint_counts.get(midpoint_key, 0)
        # update the midpoint counts
        midpoint_counts[midpoint_key] = label_index + 1
        # get the label coordinates
        label_x, label_y = _edge_label_position(x1, y1, x2, y2, label_index)
        # draw the label
        ax.text(
            label_x,
            label_y,
            f"w={edge.weight:g}",
            ha="center",
            va="center",
            fontsize=9,
            color="#111827",
            zorder=5,
            bbox={
                "boxstyle": "round,pad=0.18",
                "facecolor": "#ffffff",
                "edgecolor": "#c8ced8",
                "linewidth": 0.6,
                "alpha": 0.94,
            },
        )
    
    # MAIN ITERATION LOOP: iterate over the vertices
    for vertex, (x, y) in positions.items():
        # check if the vertex is highlighted
        is_highlight = vertex in highlighted_vertices or vertex in highlighted_path
        # set the vertex color
        face = "#ffdf6b" if is_highlight else "#f3f6fb"
        # set the edge color
        edge_color = "#2f6db3" if is_highlight else "#394150"
        # wrap the vertex label
        wrapped_label = wrap_vertex_label(vertex)
        node_size = 1_150
        font_size = 8
        # plot the vertex
        ax.scatter([x], [y], s=node_size, c=face, edgecolors=edge_color, linewidths=1.6, zorder=3)
        # plot the vertex label
        ax.text(x, y, wrapped_label, ha="center", va="center", fontsize=font_size, zorder=4)
    # set the x-axis limits
    ax.set_xlim(-1.35, 1.35)
    # set the y-axis limits
    ax.set_ylim(-1.25, 1.25)
    # add the edge weight label
    ax.text(
        0.98,
        0.02,
        "w = edge weight",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#4b5563",
    )
    fig.tight_layout()
    return fig
# --------------------------------------------------------------------------------

# ==============================================================================
# End of File
# ==============================================================================