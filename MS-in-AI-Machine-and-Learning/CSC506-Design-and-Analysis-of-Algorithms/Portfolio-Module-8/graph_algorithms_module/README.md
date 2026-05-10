# Graph Algorithms Module - Portfolio Module 8

Program Name: Graph Algorithms Integration Module  
Date: 05/05/2026

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover  
Spring A (26SA) - 2026  
Student: Alexander (Alex) Ricciardi

---

## Source Origin

This package integrates the completed `CTA-7/` Graph Representation and
Algorithm Tool into the final `Portfolio-Module-8/` Streamlit portfolio app.
The original `CTA-7/` folder remains unchanged; this package is a copied,
package-qualified Module 8 version.

## Concepts Implemented

- Adjacency-list graph representation.
- Adjacency-matrix graph representation.
- Breadth-first search (BFS).
- Depth-first search (DFS).
- Dijkstra shortest path for non-negative edge weights.
- Bellman-Ford shortest path for negative edge support and negative-cycle
  detection.
- Deterministic classroom, route, sparse, dense, and negative-weight graph
  datasets.
- Benchmark comparison across construction, adjacency checks, neighbor scans,
  traversal, shortest path, and mutation workloads.
- Graphviz DOT visualizations rendered with Streamlit `st.graphviz_chart`.

The separate Python `graphviz` package is not required for the web app.

## How to Run

Run only the Portfolio Module 8 root app:

```bash
source venv/bin/activate
streamlit run Portfolio-Module-8/streamlit_app.py
```

Open the `Graph Algorithms` tab from the root app. This module does not include
a standalone `streamlit_app.py` file.

## Integration Behavior

The page renderer is:

```python
from graph_algorithms_module.overview_page import render_graph_algorithms_page
```

The root app calls that renderer directly. The page preserves the CTA-7 local
tabs:

- Overview
- Graph Builder
- Graph Structure Lab
- Traversal Lab
- Shortest Path Lab
- Benchmark Lab
- Written Analysis
- Recommendation Guide

All imports use Module 8 package-qualified paths such as
`graph_algorithms_module.algorithms`, `graph_algorithms_module.data`,
`graph_algorithms_module.models`, `graph_algorithms_module.analysis`, and
`graph_algorithms_module.ui`. Streamlit session-state and widget keys are
namespaced with `ga_` so this page can run in the same process as the other
portfolio pages.

## Analysis Artifacts

| Artifact | Location |
|---|---|
| Written analysis | `analysis/written_analysis.md` |
| Recommendation guide | `analysis/recommendation_guide.md` |
| Benchmark CSV | `analysis/benchmark_results.csv` |
| Operation winners CSV | `analysis/operation_winners.csv` |
| Operation scaling CSV | `analysis/operation_scaling_summary.csv` |
| Charts | `analysis/charts/` |

## Tests

Graph Algorithms coverage is integrated into the root Module 8 test suite:

```bash
source venv/bin/activate
python -m pytest Portfolio-Module-8/tests -v
```

The tests cover public imports, graph representations, graph algorithms,
dataset generation, benchmark/report helpers, Streamlit DOT helper behavior,
and root app rendering.
