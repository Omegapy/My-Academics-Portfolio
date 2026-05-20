# Portfolio Milestone Module 6 — Algorithm and Data Structure Comparison Tool

Program Name: Algorithm and Data Structure Comparison Tool

Date: 04/26/2026  
Grade: 100% A

---

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover  
Spring A (26SA) – 2026  
Student: Alexander (Alex) Ricciardi

---

## Program Description

Portfolio Milestone Module 6 is a Streamlit web application that 
compares a Binary Search Tree (BST), a BST-backed Map, and a
list-backed ListMap. The app allows the generation of datasets,
building and inspecting BSTs, running required traversals, demonstrating tree-based 
key-value storage, detecting when a tree becomes unbalanced, and comparing 
TreeMap search performance against a linear-search list-based map.

---

## Benchmark App Feature:

<img width="484" height="607" alt="image" src="https://github.com/user-attachments/assets/bbbada5e-307e-40a8-a3c7-c548af3f8612" />

---

## Portfolio Assignment Context

This module is part of the CSC506 portfolio project. The overall project goal
is to build one consistent web application that demonstrates understanding of
core data structures and algorithms across multiple milestones.

**Implemented portfolio modules**

- Portfolio Milestone Module 2 — see
  [`../Portfolio-Milestone-Module-2/README.md`](../Portfolio-Milestone-Module-2/README.md)
  for the linear search vs. binary search comparison tool
- Portfolio Milestone Module 4 — see
  [`../Portfolio-Milestone-Module-4/README.md`](../Portfolio-Milestone-Module-4/README.md)
  for the stack, queue, deque, and doubly linked list tool
- Portfolio Milestone Module 6 — this module — plain BST, BST-backed `Map`,
  balance detection, and TreeMap vs. ListMap search analysis

---

## Module 6 Assignment

**Requirements**

- Construct a Binary Search Tree class with insert, delete, search, and
  traversal methods
- Implement tree traversal algorithms: in-order, pre-order, and post-order
- Create a Map class that uses your BST to store key-value pairs
- Build algorithms for tree manipulation including finding minimum/maximum
  values
- Develop a tree balancing detection system that identifies when trees become
  unbalanced
- Test implementations with at least 50 data items of different comparable
  types

**Deliverables**

- Source code file with complete Binary Search Tree implementation
- Source code file with Map class that uses BST for key-value storage
- Implementation of all three tree traversal algorithms with output examples
- Test program demonstrating tree construction, searching, and manipulation
- Performance analysis comparing tree-based map vs. list-based map for search
  operations
- Written evaluation assessing when tree data structures are most beneficial in
  programming
- Visual representation showing tree structure after insertions and deletions

**Success Criteria**

- BST correctly maintains binary search tree property after all operations
- All traversal algorithms produce correct output in proper order
- Map implementation successfully stores and retrieves key-value pairs using
  tree structure
- Tree manipulation algorithms correctly find min/max and handle edge cases
- Performance analysis shows clear advantages of tree-based searching
- Evaluation accurately assesses tree benefits and appropriate use cases

---

## Program Requirements

- Python 3.12+
- `streamlit`
- `pandas`
- `matplotlib`
- `altair` for interactive in-app charts when available

---

## How to Run

If using a Python virtual environment

```bash
source venv/bin/activate
```

To run the app

```bash
streamlit run streamlit_app.py
```

To regenerate benchmark CSV summaries and charts after saving
`analysis/benchmark_results.csv`:

```bash
python -c "
from analysis.report_generator import generate_all_reports
generate_all_reports(
    'analysis/benchmark_results.csv',
    'analysis',
)
print('Module 6 report artifacts refreshed.')
"
```

---

## Project Map

```text
Portfolio-Milestone-Module-6/
├── README.md                    # This file
├── streamlit_app.py             # Main Streamlit app 
├── written_analysis.docx        # -- Written analysis Word Doc format --
|                                # BST, TreeMap, and ListMap performance evaluation
|                                # Comparative Big-O analysis
|                                # Benchmark results and balance detection findings
├── recommendation_guide.docx    # -- Recommendation guide Word Doc format --
|                                # Guidance for choosing TreeMap vs. ListMap
|                                # When plain BST search outperforms linear search
|                                # Impact of insertion order and tree shape on performance
├── Screenshots Portfolio Milestone Module 6.docx  # Screenshots of the app
├── data_structures/             # Data structure implementations
│   ├── __init__.py
│   ├── binary_search_tree.py    # BinarySearchTree with insert, delete, search,
|   |                            # traversals, min/max, and balance detection
│   ├── tree_map.py              # BST-backed Map (TreeMap) for key-value storage
│   └── list_map.py              # List-backed baseline map with linear search
├── models/                      # Shared dataclasses
│   ├── __init__.py
│   ├── benchmark_record.py      # BenchmarkRecord for search timing
│   ├── lab_operation_result.py  # LabOperationResult for guided demo output
│   ├── balance_report.py        # BalanceReport for node-level balance diagnostics
│   └── traversal_result.py      # TraversalResult for traversal output
├── data/                        # Dataset generation and validation
│   ├── __init__.py
│   └── dataset_manager.py       # Key generation, parsing, and validation helpers
├── analysis/                    # Benchmark pipeline and reports
│   ├── __init__.py
│   ├── benchmark_search.py      # TreeMap vs. ListMap search timing engine
│   ├── lab_validation.py        # Guided lab-demo and validation helpers
│   ├── report_generator.py      # Markdown tables and chart generation
│   ├── benchmark_results.csv    # Generated benchmark results
│   ├── search_speedup_summary.csv  # TreeMap speedup relative to ListMap
│   ├── balance_summary.csv      # BST height and balance status per scenario
│   ├── written_analysis.md      # -- Written analysis --
|   |                            # BST, TreeMap, and ListMap performance evaluation
|   |                            # Comparative Big-O analysis
|   |                            # Benchmark results and balance detection findings
│   ├── recommendation_guide.md  # -- Recommendation guide --
|   |                            # Guidance for choosing TreeMap vs. ListMap
|   |                            # When plain BST search outperforms linear search
|   |                            # Impact of insertion order and tree shape on performance
│   └── charts/                                        # Generated chart images
│       ├── tree_vs_list_search.png                    # TreeMap vs. ListMap runtime chart
│       ├── search_speedup.png                         # Speedup factor chart
│       ├── bst_height_growth.png                      # BST height growth by scenario
│       └── balance_detection_profile.png              # Balance detection profile chart
└── ui/                                                # Streamlit UI helpers
    ├── __init__.py
    └── streamlit_helpers.py                           # Render functions for all tabs

```

---

## Deliverables

| Deliverable                            | Location                                         |
|----------------------------------------|--------------------------------------------------|
| Binary Search Tree implementation      | `data_structures/binary_search_tree.py`          |
| BST-backed Map implementation          | `data_structures/tree_map.py`                    |
| List-based baseline map                | `data_structures/list_map.py`                    |
| Dataset generation and parsing         | `data/dataset_manager.py`                        |
| Guided validation demos                | `analysis/lab_validation.py`                     |
| Search benchmark pipeline              | `analysis/benchmark_search.py`                   |
| Benchmark summary and chart generation | `analysis/report_generator.py`                   |
| Benchmark CSV results                  | `analysis/benchmark_results.csv`                 |
| Speedup summary CSV                    | `analysis/search_speedup_summary.csv`            |
| Balance summary CSV                    | `analysis/balance_summary.csv`                   |
| Written evaluation                     | `analysis/written_analysis.md`                   |
| Recommendation guide                   | `analysis/recommendation_guide.md`               | 
| Streamlit app                          | `streamlit_app.py`                               |
| Automated test suite                   | `tests/`                                         |

---

## App Features

| Feature                | Description                                                                                                |
|------------------------|------------------------------------------------------------------------------------------------------------|
| Overview               | Explains BST rules, traversal order, balance detection, and TreeMap vs. ListMap goals                      |
| Dataset Builder        | Generates integer, string, or tuple datasets with random, sorted, balanced, or manual input paths          |
| BST Lab                | Builds a BST, runs insert/search/delete, shows traversals, renders ASCII tree output, and reports balance  |
| Map Lab                | Builds TreeMap key-value storage and compares it with the list-backed baseline                       |
| Benchmark Lab          | Runs TreeMap vs. ListMap search benchmarks, shows validation summaries, and saves CSV results              |
| Written Analysis       | Renders the benchmark-aware Markdown evaluation                                                            |
| Recommendation Guide   | Renders the decision-focused Markdown guide for choosing TreeMap or ListMap                                |

---

## Benchmark Workloads

The benchmark layer measures search behavior rather than construction cost.
Setup happens outside the timed block so the recorded runtime reflects search
work only.

| Workload                    | Description                                                                  |
|-----------------------------|------------------------------------------------------------------------------|
| `random_insertion + hits`   | TreeMap and ListMap search for keys that exist after random-order insertion  |
| `random_insertion + misses` | Search for keys that do not exist after random-order insertion               |
| `random_insertion + mixed`  | Alternate hit/miss workload after random-order insertion                     |
| `sorted_insertion + hits`   | Search for existing keys after sorted-order insertion creates a skewed BST   |
| `sorted_insertion + misses` | Search for missing keys in the skewed BST scenario                           |
| `sorted_insertion + mixed`  | Alternate hit/miss workload in the skewed BST scenario                       |
| `balance summary`           | Records tree height and balance status to explain timing results             |

Default benchmark sizes:

```python
[50, 100, 500, 1000, 5000]
```

---

My Links:

<a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" align="left" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></a>
<a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" align="left" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></a>

[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/@AngryOwl-AI)
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)

<a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></a>
<a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></a><br>

