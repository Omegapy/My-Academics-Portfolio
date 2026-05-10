# File: graphviz_visuals.py
#
# Author: Alexander Ricciardi
# Date: 2026-05-03
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# - DOT formatting helpers quote identifiers, attributes, and graph legend markup.
# - build_graphviz_dot() renders graph state and optional algorithm highlights.
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Shared by Streamlit helpers and graph lab tabs through st.graphviz_chart().
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Shared Graphviz DOT rendering helpers for CTA-7 graph visuals."""

from __future__ import annotations

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from algorithms.graph_protocol import WeightedGraph
from ui.graph_label_utils import wrap_vertex_label


# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# GRAPHVIZ DOT HELPERS
# ==============================================================================
# Format DOT-safe strings, attributes, legends, and graph canvas settings.
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _dot_quote()
def _dot_quote(value: object) -> str:
    """Return a safely quoted DOT string value.

    Args:
        value: Value to quote for Graphviz DOT syntax.

    Returns:
        Quoted and escaped DOT string.
    """
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _dot_attributes()
def _dot_attributes(attributes: dict[str, object]) -> str:
    """Format Graphviz DOT attributes.

    Args:
        attributes: Attribute names and values.

    Returns:
        DOT attribute block.
    """
    parts = [f"{name}={_dot_quote(value)}" for name, value in attributes.items()]
    return f"[{', '.join(parts)}]"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_graph_legend_html()
def build_graph_legend_html() -> str:
    """Build the shared graph color legend.

    Returns:
        HTML legend explaining vertex and edge visual roles.
    """
    return """
<div style="display:flex; flex-wrap:wrap; gap:0.85rem 1.25rem; align-items:center; font-size:0.86rem; color:#374151; margin:0.25rem 0 1rem 0;">
  <strong style="color:#111827;">Legend</strong>
  <span><span style="display:inline-block; width:0.85rem; height:0.85rem; border-radius:50%; background:#fb923c; border:2px solid #7c2d12; vertical-align:-0.12rem;"></span> current vertex</span>
  <span><span style="display:inline-block; width:0.85rem; height:0.85rem; border-radius:50%; background:#ffdf6b; border:2px solid #2f6db3; vertical-align:-0.12rem;"></span> final path / highlighted vertex</span>
  <span><span style="display:inline-block; width:0.85rem; height:0.85rem; border-radius:50%; background:#bfdbfe; border:2px solid #1d4ed8; vertical-align:-0.12rem;"></span> frontier / queue</span>
  <span><span style="display:inline-block; width:0.85rem; height:0.85rem; border-radius:50%; background:#dbeafe; border:2px solid #3b82f6; vertical-align:-0.12rem;"></span> discovered</span>
  <span><span style="display:inline-block; width:1.4rem; height:0; border-top:3px solid #60a5fa; vertical-align:middle;"></span> final shortest path</span>
  <span><span style="display:inline-block; width:1.4rem; height:0; border-top:3px solid #3b82f6; vertical-align:middle;"></span> predecessor / tree edge</span>
  <span><span style="display:inline-block; width:1.4rem; height:0; border-top:3px solid #16a34a; vertical-align:middle;"></span> relaxation updated</span>
  <span><span style="display:inline-block; width:1.4rem; height:0; border-top:3px dashed #dc2626; vertical-align:middle;"></span> checked, no update</span>
  <span><span style="display:inline-block; width:1.4rem; height:0; border-top:4px solid #dc2626; vertical-align:middle;"></span> negative weight</span>
  <span><span style="display:inline-block; width:1.4rem; height:0; border-top:3px solid #f59e0b; vertical-align:middle;"></span> traversal / cycle edge</span>
  <span><span style="display:inline-block; width:1.4rem; height:0; border-top:2px solid #9ca3af; vertical-align:middle;"></span> normal edge</span>
</div>
"""
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _graph_density()
def _graph_density(graph: WeightedGraph) -> float:
    """Return the graph edge density for visual layout choices.

    Args:
        graph: Graph to inspect.

    Returns:
        Density between 0.0 and 1.0.
    """
    vertex_count = graph.order()
    if vertex_count <= 1:
        return 0.0
    if graph.directed:
        max_edges = vertex_count * (vertex_count - 1)
    else:
        max_edges = vertex_count * (vertex_count - 1) // 2
    if max_edges == 0:
        return 0.0
    return graph.size() / max_edges
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _is_dense_visual_graph()
def _is_dense_visual_graph(graph: WeightedGraph) -> bool:
    """Return whether a graph needs a larger dense-layout canvas.

    Args:
        graph: Graph to inspect.

    Returns:
        Whether the graph should use dense visual sizing.
    """
    return graph.order() >= 6 and _graph_density(graph) >= 0.45
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _graphviz_canvas_size()
def _graphviz_canvas_size(graph: WeightedGraph) -> str:
    """Return the Graphviz drawing size for a graph.

    Args:
        graph: Graph to inspect.

    Returns:
        Graphviz size attribute value.
    """
    if _is_dense_visual_graph(graph):
        return "18,10!"
    if graph.order() >= 8:
        return "14,8!"
    return "10,6!"
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _graphviz_chart_height()
def _graphviz_chart_height(graph: WeightedGraph) -> int:
    """Return the Streamlit chart height for a graph visual.

    Args:
        graph: Graph to inspect.

    Returns:
        Chart height in pixels.
    """
    if _is_dense_visual_graph(graph):
        return 720
    if graph.order() >= 8:
        return 620
    return 520
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- build_graphviz_dot()
def build_graphviz_dot(
    graph: WeightedGraph,
    *,
    title: str,
    # --- ALGORITHM HIGHLIGHTS (passed by algorithm step functions) ---
    # --- Vertices ---
    highlighted_vertices: list[str] | None = None,
    current_vertex: str | None = None,
    frontier_vertices: list[str] | None = None,
    discovered_vertices: list[str] | None = None,
    # --- Edges ---
    highlighted_edges: list[tuple[str, str]] | None = None,
    predecessor_edges: list[tuple[str, str]] | None = None,
    updated_candidate_edge: tuple[str, str] | None = None,
    rejected_candidate_edge: tuple[str, str] | None = None,
    highlighted_path: list[str] | None = None,
    # --- Visual & Layout Options ---
    show_edge_weights: bool = True,
    canvas_size: str | None = None,
    compact: bool = False,
) -> str:
    """Build DOT source for a Streamlit Graphviz chart.

    Args:
        graph: Graph to render.
        title: Figure title.
        # --- Vertex Highlighting ---
        highlighted_vertices: Vertices to emphasize.
        current_vertex: Vertex currently being processed.
        frontier_vertices: Queue/stack vertices waiting to be processed.
        discovered_vertices: Vertices discovered by the algorithm.
        # --- Edge Highlighting ---
        highlighted_edges: Edges to emphasize.
        highlighted_path: Path to emphasize.
        predecessor_edges: Current predecessor-tree edges to emphasize.
        updated_candidate_edge: Candidate edge that improved a distance.
        rejected_candidate_edge: Candidate edge that did not improve a distance.
        # --- Visual & Layout Options ---
        show_edge_weights: Whether to draw weight labels on edges.
        canvas_size: Optional Graphviz size override.
        compact: Whether to use smaller sizing for gallery-style previews.

    Returns:
        DOT source for ``st.graphviz_chart``.
    """
        # --- Normalize highlighting sets ---
    highlighted_vertex_set = set(highlighted_vertices or [])
    highlighted_path = highlighted_path or []
    highlighted_vertex_set.update(highlighted_path)
    # --- Build edge sets from path and edge arguments ---
    highlighted_path_edges = set(zip(highlighted_path, highlighted_path[1:]))
    emphasized_edges = set(highlighted_edges or [])
    predecessor_edge_set = set(predecessor_edges or [])
    updated_candidate_edges = {updated_candidate_edge} if updated_candidate_edge else set()
    rejected_candidate_edges = {rejected_candidate_edge} if rejected_candidate_edge else set()
    # Handle undirected graphs by adding symmetric edges
    if not graph.directed:
        highlighted_path_edges.update(
            (target, source) for source, target in list(highlighted_path_edges)
        )
        emphasized_edges.update((target, source) for source, target in list(emphasized_edges))
        predecessor_edge_set.update((target, source) for source, target in list(predecessor_edge_set))
        updated_candidate_edges.update((target, source) for source, target in list(updated_candidate_edges))
        rejected_candidate_edges.update((target, source) for source, target in list(rejected_candidate_edges))
    # Frontier/discovered vertex sets
    frontier_vertex_set = set(frontier_vertices or [])
    discovered_vertex_set = set(discovered_vertices or [])
    # Set drawing canvas size
    drawing_size = canvas_size or ("5.8,3.4!" if compact else _graphviz_canvas_size(graph))
    # Dynamic font sizing
    title_font_size = "14" if compact else "22"
    graph_pad = "0.12" if compact else "0.35"
    nodesep = "0.34" if compact else "0.75"
    ranksep = "0.46" if compact else "1.0"
    node_width = "0.68" if compact else "1.05"
    node_font_size = "9" if compact else "11"
    node_pen_width = "1.5" if compact else "2.2"
    edge_font_size = "9" if compact else "15"
    edge_pen_width = "1.25" if compact else "1.8"
    arrow_size = "0.55" if compact else "0.75"
    graph_font_color = "#f8fafc" if compact else "#111827"
    edge_font_color = "#f8fafc" if compact else "#111827"

    lines = [
        "digraph CTA7Graph {",
        f"    label={_dot_quote(title)};",
        "    labelloc=\"t\";",
        f"    fontsize=\"{title_font_size}\";",
        "    fontname=\"Helvetica\";",
        f"    fontcolor=\"{graph_font_color}\";",
        "    rankdir=\"LR\";",
        "    bgcolor=\"transparent\";",
        f"    pad=\"{graph_pad}\";",
        f"    size=\"{drawing_size}\";",
        "    ratio=\"expand\";",
        f"    nodesep=\"{nodesep}\";",
        f"    ranksep=\"{ranksep}\";",
        "    splines=\"polyline\";",
        f"    node [shape=\"circle\", style=\"filled\", fixedsize=\"true\", width=\"{node_width}\", height=\"{node_width}\", margin=\"0.01\", fillcolor=\"#f3f6fb\", color=\"#394150\", fontcolor=\"#111827\", fontname=\"Helvetica\", fontsize=\"{node_font_size}\", penwidth=\"{node_pen_width}\"];",
        f"    edge [color=\"#9ca3af\", fontcolor=\"{edge_font_color}\", fontname=\"Helvetica\", fontsize=\"{edge_font_size}\", penwidth=\"{edge_pen_width}\", arrowsize=\"{arrow_size}\"];",
    ]

    # MAIN ITERATION LOOP: emit vertices before edges so isolated vertices appear
    for vertex in graph.vertices():
        attributes: dict[str, object] = {
            "label": wrap_vertex_label(vertex),
            "tooltip": vertex,
        }
        # --- Vertex styling based on algorithm state ---   
        if vertex in discovered_vertex_set:
            attributes.update({"fillcolor": "#dbeafe", "color": "#3b82f6", "penwidth": "2.4"})
        if vertex in highlighted_vertex_set:
            attributes.update({"fillcolor": "#ffdf6b", "color": "#2f6db3", "penwidth": "2.8"})
        if vertex in frontier_vertex_set:
            attributes.update({"fillcolor": "#bfdbfe", "color": "#1d4ed8", "penwidth": "3.0"})
        if current_vertex is not None and vertex == current_vertex:
            attributes.update({"fillcolor": "#fb923c", "color": "#7c2d12", "penwidth": "3.3"})
        lines.append(f"    {_dot_quote(vertex)} {_dot_attributes(attributes)};")

    # --- MAIN ITERATION LOOP: emit edges with algorithm-relevant styling ---   
    for edge in graph.edges():
        attributes = {"tooltip": f"{edge.source} to {edge.target}"}
        is_negative_edge = edge.weight < 0
        # --- Show edge weights when requested (important for Bellman-Ford) --- 
        if show_edge_weights:
            weight_label = f"w={edge.weight:g}" if compact else f"weight={edge.weight:g}"
            tooltip_label = (
                f"negative weight={edge.weight:g}"
                if is_negative_edge
                else weight_label
            )
            attributes.update(
                {
                    "label": weight_label,
                    "tooltip": f"{edge.source} to {edge.target}, {tooltip_label}",
                }
            )   
        # --- Handle undirected graphs by setting dir="none" (Graphviz will render as unlabeled edge) ---
        if not graph.directed:
            attributes["dir"] = "none"
        # --- Algorithm-specific edge highlighting ---
        if (edge.source, edge.target) in predecessor_edge_set:
            attributes.update({"color": "#3b82f6", "fontcolor": edge_font_color, "penwidth": "2.4"})
        if (edge.source, edge.target) in emphasized_edges:
            attributes.update({"color": "#f59e0b", "fontcolor": edge_font_color, "penwidth": "3.0"})
        if (edge.source, edge.target) in updated_candidate_edges:
            attributes.update({"color": "#16a34a", "fontcolor": edge_font_color, "penwidth": "3.4"})
        if (edge.source, edge.target) in rejected_candidate_edges:
            attributes.update({"color": "#dc2626", "fontcolor": edge_font_color, "penwidth": "3.2", "style": "dashed"})
        if (edge.source, edge.target) in highlighted_path_edges:
            attributes.update({"color": "#60a5fa", "fontcolor": edge_font_color, "penwidth": "3.0", "style": "solid"})
        if is_negative_edge:
            attributes.update({"color": "#dc2626", "fontcolor": "#dc2626", "penwidth": "3.8"})
        lines.append(
            f"    {_dot_quote(edge.source)} -> {_dot_quote(edge.target)} "
            f"{_dot_attributes(attributes)};"
        )

    lines.append("}")
    return "\n".join(lines)
# --------------------------------------------------------------------------------


# ==============================================================================
# End of File
# ==============================================================================
