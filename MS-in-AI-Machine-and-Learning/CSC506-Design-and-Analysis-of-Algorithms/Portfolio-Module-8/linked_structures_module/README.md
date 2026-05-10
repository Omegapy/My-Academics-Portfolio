# Linked Structures Module

Program Name: Portfolio Module 8 Linked Structures  
Date: 05/05/2026

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover  
Spring A (26SA) - 2026  
Student: Alexander (Alex) Ricciardi

---

## Source Origin

This package was copied from `Portfolio-Milestone-Module-4/` and adapted for
the final `Portfolio-Module-8/` Streamlit portfolio. The original assignment
folder remains unchanged.

## Concepts Implemented

- `Stack`: list-backed LIFO structure with `push`, `pop`, `peek`, `isEmpty`,
  `clear`, and `to_list`.
- `Queue`: course-aligned list-backed FIFO structure with `enqueue`,
  `dequeue`, `front`, `isEmpty`, `clear`, and logical/internal list views.
- `Deque`: list-backed double-ended queue with front/rear add, remove, and
  peek operations.
- `LinkedList`: custom doubly linked list using `Node` objects with front,
  rear, before-anchor, after-anchor, search, delete, and traversal workflows.
- Benchmark engine: common build, common drain, peek/front, deque-end, linked
  list search, linked list delete, and linked list display workloads.

## Module 8 Integration Behavior

The package is import-safe and no longer has a runnable `streamlit_app.py`.
The root app imports:

```python
from linked_structures_module.overview_page import render_linked_structures_page
```

The renderer exposes these local tabs inside the single Portfolio Module 8 app:

- Overview
- Dataset Builder
- Structure Playground
- Compare Structures
- Benchmark Lab
- Written Analysis
- Recommendation Guide

Streamlit session-state keys and widget keys are namespaced with `ls_` so this
page can run in the same process as the Search Comparison and Bubble
Quickselect Sets pages.

## How to Run

Run only the root Portfolio Module 8 app:

```bash
source venv/bin/activate
streamlit run Portfolio-Module-8/streamlit_app.py
```

Then open the `Linked Structures` tab.

## How to Test

```bash
source venv/bin/activate
python -m pytest Portfolio-Module-8/tests -v
```

Relevant test files:

- `tests/test_linked_structures_data_structures.py`
- `tests/test_linked_structures_dataset_and_benchmark.py`
- `tests/test_module8_integration_imports.py`
- `tests/test_module8_streamlit_integration.py`

## Package Map

```text
linked_structures_module/
├── README.md
├── __init__.py
├── overview_page.py
├── icon.png
├── data/
├── data_structures/
├── models/
├── analysis/
│   ├── benchmark_structures.py
│   ├── report_generator.py
│   ├── benchmark_results.csv
│   ├── operation_winners.csv
│   ├── written_analysis.md
│   ├── recommendation_guide.md
│   └── charts/
└── ui/
```

## Analysis Artifacts

| Artifact | Location |
|---|---|
| Written analysis | `analysis/written_analysis.md` |
| Recommendation guide | `analysis/recommendation_guide.md` |
| Benchmark CSV | `analysis/benchmark_results.csv` |
| Operation winners CSV | `analysis/operation_winners.csv` |
| Benchmark charts | `analysis/charts/` |

## Import Changes

The original Module 4 code used generic imports such as `from data...`,
`from models...`, and `from analysis...`. Module 8 rewrites those imports to
package-qualified paths such as:

```python
from linked_structures_module.data.dataset_manager import generate_dataset_by_type
from linked_structures_module.data_structures import Stack, Queue, Deque, LinkedList
from linked_structures_module.analysis.benchmark_structures import run_benchmarks
```

This prevents collisions with other integrated portfolio packages that also
contain `data`, `models`, `analysis`, and `ui` folders.
