# Critical Thinking 7 — Graph Representation & Algorithm Tool
Program Name: Graph Representation & Algorithm Tool

Date: 05/03/2026  
Grade: 100% A

---

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover   
Spring A (26SA) – 2026  
Student: Alexander (Alex) Ricciardi  

---

## Program Description:

The program is a web application built using Streamlit. It implements and compares 
graph data structure representations using both adjacency lists and adjacency matrices. 
It supports weighted directed or undirected graphs, graph manipulation, BFS and DFS
traversal traces, Dijkstra and Bellman-Ford shortest paths, benchmark
comparisons, visual graph rendering through Streamlit's Graphviz chart support, and written
analysis and recommendations guide.

---

## Benchmark Lab:

<img width="418" height="614" alt="image" src="https://github.com/user-attachments/assets/a7c72035-3f93-4595-8624-6ffa82acf155" />

---

## Assignment:

**Requirements:**
- Implement a Graph class using adjacency matrix representation.
- Implement a Graph class using adjacency list representation.
- Create algorithms for adding vertices and edges to both graph types.
- Develop graph traversal algorithms (depth-first search and breadth-first search).
- Build algorithms for finding shortest paths between vertices.
- Create functions to display graph structure and connections.
- Render graph structure visually with labeled weighted edges.


**Deliverables:**
- Source code file with adjacency matrix graph implementation
- Source code file with adjacency list graph implementation
- Graph manipulation algorithms that work with both representations
- Traversal algorithm implementations (DFS and BFS) with step-by-step output
- Shortest path algorithms that find routes between vertices and explain
  Dijkstra vs. Bellman-Ford trade-offs
- Test program demonstrating graph construction and algorithm execution on sample data
- Performance comparison (2 pages) analyzing when to use adjacency matrix vs. adjacency list
- Visual representation showing how algorithms traverse and manipulate graph structures

**Success Criteria:**
- Both graph representations correctly store vertices and edges
- Manipulation algorithms successfully add and remove graph elements
- Traversal algorithms visit all reachable vertices in correct order
- Shortest path algorithms find optimal routes or report reachable negative cycles
- Performance analysis accurately compares the trade-offs between representations
- Graph visualizations clearly show vertices, weighted edges, and highlighted traversal/path output
- Test program demonstrates practical applications of graph algorithms

---

## Program Requirements:
- Python 3.12+
- `streamlit` (install via `pip install streamlit`)
- `pandas` (install via `pip install pandas`)
- `matplotlib` (install via `pip install matplotlib`) for benchmark charts and static report figures
- `colorama` (install via `pip install colorama`) for CLI demo output
- `pytest` (install via `pip install pytest`) for the automated test suite

The Streamlit app renders graph diagrams with `st.graphviz_chart` from DOT
strings generated in `ui/streamlit_helpers.py`. This does **not** require the
separate Python `graphviz` package.

---

## How to Run:

```bash
# If using a Python virtual environment, first activate the virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install streamlit pandas matplotlib colorama pytest

# Launch the Streamlit app (from the repository root)
streamlit run streamlit_app.py

```

The app opens in your default browser at `http://localhost:8501`.

---

## Project Map:

```
CTA-7/
├── README.md                         # This file App documentation
├── streamlit_app.py                  # App entrypoint
├── icon.png                          # App/page icon asset
├── written_analysis.docx             # written analysis in Word format
|                                     # analysis of the performance of algorithms and compares the trade-offs between representations
├── recommendation_guide.docx         # recommendation guide in Word format
|                                     # when to use adjacency matrix vs. adjacency list
├── Screenshots Critical Thinking Module 7.docx   # screenshots of ui of the app and results 
├── algorithms/                       # Graph implementations and algorithms
│   ├── adjacency_list_graph.py       # adjacency-list graph
│   ├── adjacency_matrix_graph.py     # adjacency-matrix graph
│   ├── graph_algorithms.py           # BFS, DFS, Dijkstra, Bellman-Ford, and path helpers
│   └── graph_protocol.py             # Shared graph interface contract
├── models/                           # Dataclasses used by labs, algorithms, and benchmarks
│   ├── benchmark_record.py           # Benchmark result row
│   ├── graph_edge.py                 # Weighted edge model
│   ├── lab_operation_result.py       # UI lab operation result model
│   ├── shortest_path_result.py       # Dijkstra and Bellman-Ford result models
│   └── traversal_result.py           # BFS/DFS traversal result model
├── data/                             # graph dataset builders
│   └── graph_dataset_manager.py      # graph sample sparse, dense, traversal, and route graph datasets
├── analysis/                         # Benchmark, validation, and report-generation assets
│   ├── benchmark_graphs.py           # Benchmark and chart generation
│   ├── lab_validation.py             # validation scenarios for app labs
│   ├── report_generator.py           # Static report tables, figures, and summaries
│   ├── benchmark_results.csv         # Raw benchmark output
│   ├── operation_scaling_summary.csv # Scaling summary by operation and graph size
│   ├── operation_winners.csv         # Fastest representation/algorithm summary
│   ├── written_analysis.md           # Markdown source for written analysis
│   ├── recommendation_guide.md       # Markdown source for recommendation guide
│   └── charts/                       # Generated benchmark and analysis PNG charts
├── ui/                               # Streamlit UI helpers and DOT visualization 
│   ├── graph_label_utils.py          # Graph labels and formatting helpers
│   ├── graphviz_visuals.py           # Graphviz DOT builders for Streamlit charts
│   └── streamlit_helpers.py          # Shared Streamlit controls, tables, and display helpers
```

---

## Deliverables:

| Deliverable                                          | Location                                         |
|------------------------------------------------------|--------------------------------------------------|
| Adjacency matrix source code                         | `algorithms/adjacency_matrix_graph.py`           |
| Adjacency list source code                           | `algorithms/adjacency_list_graph.py`             |
| Shared graph algorithms                              | `algorithms/graph_algorithms.py`                 |
| Streamlit app                                        | `streamlit_app.py`                               |
| Streamlit Graphviz visualization helper              | `ui/streamlit_helpers.py`                        |
| Benchmark pipeline                                   | `analysis/benchmark_graphs.py`                   |
| Written performance comparison                       | `analysis/written_analysis.md`                   |
| Recommendation guide                                 | `analysis/recommendation_guide.md`               |

---

## Operations Supported:

| Tab                    | Description                                                                                                                                                                |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Overview               | Project purpose and complexity comparison tables                                                                                                                           |
| Graph Builder          | Generate sample BFS/DFS, Positive Weighted Positive Route Demo, Negative Weight Cost Demo, sparse, or dense graph datasets and Graphviz visuals                            |
| Graph Structure Lab    | Use one synchronized playground to mutate/query adjacency-list and adjacency-matrix graphs, then compare paired results, adjacency tables, and Graphviz visuals            |
| Traversal Lab          | Run BFS and DFS with step-by-step frontier output, traversal-tree edges, and a visual step selector                                                                        |
| Shortest Path Lab      | Run guided positive-distance Dijkstra and negative-weight Bellman-Ford demos, inspect relaxation steps, and compare Dijkstra vs. Bellman-Ford timing on the positive graph |
| Benchmark Lab          | Compare list vs matrix performance and generate charts/CSV files                                                                                                           |
| Written Analysis       | Two-page style performance analysis                                                                                                                                        |
| Recommendation Guide   | Practical guidance for representation and algorithm choice                                                                                                                 |
---

My Links:

<a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" align="left" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></a>
<a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" align="left" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></a>

[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)

<a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></a>
<a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></a><br>
