# Portfolio Module 8 - Algorithm and Data Structure Comparison Tool

Program Name: Algorithm and Data Structure Comparison Tool  

Date: 05/10/2026  
Grade: 100% | A

---

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover  
Spring A (26SA) - 2026  
Student: Alexander (Alex) Ricciardi
License: Apache-2.0

Date: 05/10/2026  
Grade: 

---

## Program Description

This Algorithm and Data Structure Comparison Tool combines the following structures and behaviors:

- **Search Comparison** - linear search and binary search workflows that show
  how ordered data changes search efficiency.
- **Linked Structures** - stack, queue, deque, and linked-list behaviors that
  compare list-backed and node-based structure design.
- **Tree Map** - Binary Search Tree, TreeMap, and ListMap workflows that
  compare ordered tree navigation against a linear baseline.
- **Hash Priority** - hash-table and priority-queue operations that compare
  direct key access, heap behavior, and linear-search benchmarking.
- **Graph Algorithms** - graph representations, traversal algorithms, and
  shortest-path workflows that compare structural trade-offs across workloads.
- **Bubble Quickselect Sets** - Bubble Sort, Quickselect, and CourseSet
  demonstrations that connect ordering, selection, and set behavior.

Use the tabs above to build deterministic datasets, compare algorithm and data
structure behavior, run guided operations, benchmark different workloads, and
read the written analysis and recommendation materials from the integrated
portfolio modules.

---

## Labs Example:

<img width="970" height="1218" alt="13 - Linked Structures-Written Analysis-img5" src="https://github.com/user-attachments/assets/c164a6c2-0ed0-41de-ae29-ffe9ece24543" />

---

## Implemented portfolio modules:  

- Portfolio Milestone Module 2 — see [The search comparison module](search_comparison_module/README.md)
  for the linear search vs. binary search comparison tool
- Portfolio Milestone Module 4 — see [The linked structures module](linked_structures_module/README.md)
  for the stack, queue, deque, and doubly linked list tool
- Portfolio Milestone Module 6 - see [The tree map module](tree_map_module/README.md)
- Portfolio Project Module 8 - this project
 Integrating all previous modules and adding Bubble Sort and Quickselect [The Bubble Quickselect Sets module](bubble_quickselect_module/README.md),  
 CTA-5 Hash Table and Priority Queue [the hash priority module](hash_priority_module/README.md), and the CTA-7 graph algorithms and representations [the graph algorithms module](graph_algorithms_module/README.md)


---

## Assignment:

Create a complete portfolio system that demonstrates mastery of all course concepts including sets, sorting algorithms, and data structures from previous modules.

**Requirements:**
- Implement bubble sort algorithm for sorting lists of integers with step-by-step visualization.
- Create quickselect algorithm implementation that finds the kth smallest element in a list.
- Build a comprehensive Set class that supports union, intersection, difference, and symmetric difference operations.
- Integrate all data structures from previous modules (stacks, queues, trees, graphs, hash tables) into one unified system.
- Create a user interface that allows testing and comparison of all implemented algorithms and data structures.
- Develop performance analysis tools that compare different algorithms and data structures across multiple metrics.


**Deliverables:**
- Source code file with bubble sort implementation including visualization of sorting steps
- Source code file with quickselect algorithm that efficiently finds kth smallest elements
- Complete Set class implementation with all set operations and documentation
- Integrated portfolio system containing all course algorithms and data structures
- User interface allowing interactive testing of all implementations
- Comprehensive performance analysis report (5+ pages) comparing all algorithms and data structures
- Final portfolio presentation (video or slides) demonstrating system capabilities and course learning
- Complete project documentation with usage instructions and design decisions

**Success Criteria:**
- Bubble sort correctly sorts integer lists and shows step-by-step process
- Quickselect algorithm efficiently finds kth smallest element in any list
- Set operations work correctly and demonstrate understanding of static vs. dynamic operations
- Portfolio system successfully integrates and demonstrates all course concepts
- Performance analysis provides meaningful insights into algorithm and data structure trade-offs
- Final presentation clearly communicates technical achievements and learning outcomes

---

## How to Run

Run the root portfolio app from the repository root:

```bash
# If using a Python virtual environment, first activate the virtual environment
source venv/bin/activate

# Run the app
streamlit run streamlit_app.py
```

Run the focused Bubble Quickselect Sets checks:

```bash
source venv/bin/activate
python -m pytest \
  Portfolio-Module-8/tests/test_bubble_sort.py \
  Portfolio-Module-8/tests/test_quickselect.py \
  Portfolio-Module-8/tests/test_course_set.py \
  Portfolio-Module-8/tests/test_benchmark_bubble_quickselect.py \
  Portfolio-Module-8/tests/test_bubble_quickselect_streamlit.py
```

---
## Root App Tabs

| Tab                     | Purpose                                                         |
|-------------------------|-----------------------------------------------------------------|
| Overview                | Summarizes the integrated portfolio and key algorithm concepts. |
| Search Comparison       | Compares linear search and binary search workflows.             |
| Linked Structures       | Demonstrates stack, queue, deque, and linked-list behavior.     |
| Tree Map                | Compares BST, TreeMap, and ListMap behavior.                    |
| Hash Priority           | Demonstrates hash table and priority queue behavior.            |
| Graph Algorithms        | Compares graph representations, traversal, and shortest paths.  |
| Bubble Quickselect Sets | Runs Bubble Sort, Quickselect, and CourseSet labs.              |
| Comprehensive Analysis  | Renders the cross-module performance analysis artifact.         |

---

## Project Map

```text
Portfolio-Module-8/
├── README.md                  # This file project documentation
├── streamlit_app.py           # Streamlit app entry point
├── icon.png                   # App icon
| -----------------------------------------------
| # -- Comprehensive written analysis in Word document format --
├── comprehensive_annalysis.docx             
| #  -- see analysis/comprehensive_performance_analysis.md for markdown version --
| -----------------------------------------------
| # -- Quickselect/Set written analysis in Word document format --
├── written_analysis_bubble_quickselect_set.docx 
| # -- see bubble_quickselect_module/analysis/written_analysis.md for markdown version --
| -----------------------------------------------
| #  -- Project Presentation slide deck in powerpoint format --
├── Final_Project_Presentation.pptx  
| #  -- Project Presentation Slide deck and speaker notes PDF              
├── Final_Project_Presentation_Speaker_Notes.pdf  
|
| -----------------------------------------------
├── analysis/                                     # Project analysis directory
│   └── comprehensive_performance_analysis.md     # Cross-module performance analysis in markdown format
|
| -----------------------------------------------
├── search_comparison_module/                     # Module 2: linear vs. binary search comparison
│   ├── algorithms/
│   │   ├── binary_search.py
│   │   └── linear_search.py
│   ├── analysis/
│   │   ├── benchmark_results.csv
│   │   ├── benchmark_searches.py
│   │   ├── big_o_analysis.md
│   │   └── recommendation_guide.md
│   ├── data/
│   │   └── dataset_manager.py
│   ├── models/
│   │   └── search_result.py
│   ├── ui/
│   │   └── streamlit_helpers.py
│   ├── overview_page.py
│   └── README.md
│ 
| -----------------------------------------------
├── linked_structures_module/                     # Module 4: stack, queue, deque, and linked list labs
│   ├── data_structures/
│   │   ├── deque.py
│   │   ├── linked_list.py
│   │   ├── queue.py
│   │   └── stack.py
│   ├── analysis/
│   │   ├── benchmark_results.csv
│   │   ├── benchmark_structures.py
│   │   ├── operation_winners.csv
│   │   ├── recommendation_guide.md
│   │   ├── report_generator.py
│   │   ├── written_analysis.md
│   │   └── charts/
│   ├── data/
│   │   └── dataset_manager.py
│   ├── models/
│   │   ├── benchmark_record.py
│   │   ├── operation_result.py
│   │   └── operation_winner.py
│   ├── ui/
│   │   └── streamlit_helpers.py
│   ├── overview_page.py
│   └── README.md
|
| -----------------------------------------------
├── tree_map_module/                              # Module 6: BST, TreeMap, and ListMap comparison
│   ├── data_structures/
│   │   ├── binary_search_tree.py
│   │   ├── list_map.py
│   │   └── tree_map.py
│   ├── analysis/
│   │   ├── balance_summary.csv
│   │   ├── benchmark_results.csv
│   │   ├── benchmark_search.py
│   │   ├── lab_validation.py
│   │   ├── recommendation_guide.md
│   │   ├── report_generator.py
│   │   ├── search_speedup_summary.csv
│   │   ├── written_analysis.md
│   │   └── charts/
│   ├── data/
│   │   └── dataset_manager.py
│   ├── models/
│   │   ├── balance_report.py
│   │   ├── benchmark_record.py
│   │   ├── lab_operation_result.py
│   │   └── traversal_result.py
│   ├── ui/
│   │   └── streamlit_helpers.py
│   ├── overview_page.py
│   └── README.md
|
| -----------------------------------------------
├── hash_priority_module/                         # CTA-5: hash table and priority queue demonstrations
│   ├── algorithms/
│   │   ├── hash_table.py
│   │   ├── linear_search.py
│   │   └── priority_queue.py
│   ├── analysis/
│   │   ├── benchmark_results.csv
│   │   ├── benchmark_search.py
│   │   ├── lab_validation.py
│   │   ├── operation_scaling_summary.csv
│   │   ├── recommendation_guide.md
│   │   ├── report_generator.py
│   │   ├── search_speedup_summary.csv
│   │   ├── written_analysis.md
│   │   └── charts/
│   ├── data/
│   │   └── dataset_manager.py
│   ├── models/
│   │   ├── benchmark_record.py
│   │   ├── hash_entry.py
│   │   ├── hash_table_stats.py
│   │   ├── lab_operation_result.py
│   │   └── priority_item.py
│   ├── ui/
│   │   └── streamlit_helpers.py
│   ├── overview_page.py
│   └── README.md
|
| -----------------------------------------------
├── graph_algorithms_module/                      # CTA-7: graph representations, traversal, and shortest paths
│   ├── algorithms/
│   │   ├── adjacency_list_graph.py
│   │   ├── adjacency_matrix_graph.py
│   │   ├── graph_algorithms.py
│   │   └── graph_protocol.py
│   ├── analysis/
│   │   ├── benchmark_graphs.py
│   │   ├── benchmark_results.csv
│   │   ├── lab_validation.py
│   │   ├── operation_scaling_summary.csv
│   │   ├── operation_winners.csv
│   │   ├── recommendation_guide.md
│   │   ├── report_generator.py
│   │   ├── written_analysis.md
│   │   └── charts/
│   ├── data/
│   │   └── graph_dataset_manager.py
│   ├── models/
│   │   ├── benchmark_record.py
│   │   ├── graph_edge.py
│   │   ├── lab_operation_result.py
│   │   ├── shortest_path_result.py
│   │   └── traversal_result.py
│   ├── ui/
│   │   ├── graph_label_utils.py
│   │   ├── graphviz_visuals.py
│   │   └── streamlit_helpers.py
│   ├── icon.png
│   ├── overview_page.py
│   └── README.md
|
| -----------------------------------------------
├── bubble_quickselect_module/                    # Module 8: Bubble Sort, Quickselect, and CourseSet labs
│   ├── algorithms/
│   │   ├── bubble_sort.py
│   │   └── quickselect.py
│   ├── analysis/
│   │   ├── benchmark_bubble_quickselect.py
│   │   ├── benchmark_results.csv
│   │   └── written_analysis.md
│   ├── data/
│   │   └── dataset_manager.py
│   ├── models/
│   │   ├── quickselect_result.py
│   │   └── sort_result.py
│   ├── set_operations/
│   │   ├── course_set.py
│   │   └── set_operation_result.py
│   ├── overview_page.py
│   ├── written_analysis.docx
│   └── README.md
|
| -----------------------------------------------
├── app_screenshots/                         # Captured screenshots for app documentation/submission
│   ├── README.md
│   └── *.png

```
---

## Module Sources

| Module 8 package            | Source                          |
|-----------------------------|---------------------------------|
| `search_comparison_module/` | `Portfolio-Milestone-Module-2/` |
| `linked_structures_module/` | `Portfolio-Milestone-Module-4/` |
| `tree_map_module/`          | `Portfolio-Milestone-Module-6/` |
| `hash_priority_module/`     | `CTA-5/`                        |
| `graph_algorithms_module/`  | `CTA-7/`                        |
| `bubble_quickselect_module/`| This module, Module 8           |

---

## Bubble Quickselect Sets Module

The `bubble_quickselect_module` is the Module 8-native feature area. It
contains:

- `Bubble Sort`: adjacent comparison sort with early exit, operation counts,
  timing, and optional trace output.
- `Quickselect`: deterministic right-pivot kth-smallest selection with
  partition traces and correctness checking.
- `CourseSet`: hash-backed Set ADT preserving first-seen display order.
- `SetOperationResult`: before/after operation metadata for manual and
  automatic set demos.
- `BenchmarkRecord`: CSV-ready benchmark row model for algorithm comparisons.
- Streamlit labs for set operations, Bubble Sort, Quickselect, benchmarks, and
  written analysis.

The target Python files in `bubble_quickselect_module/` and the root
`streamlit_app.py` have been documented using the local
`Step-by-step-Comments/` Phase 1 through Phase 5 templates. The `__init__.py`
files are intentionally left minimal.

---
## Package Integration

Portfolio Module 8 uses copied, package-qualified modules to prevent collisions
between repeated generic package names such as `algorithms`, `data`, `models`,
`analysis`, and `ui`.

Examples:

- `search_comparison_module.algorithms`
- `linked_structures_module.data_structures`
- `tree_map_module.data_structures`
- `hash_priority_module.algorithms`
- `graph_algorithms_module.algorithms`
- `bubble_quickselect_module.algorithms`

Module UI files expose root-callable functions instead of separate app launch
files:

- `render_search_comparison_page()`
- `render_linked_structures_page()`
- `render_tree_map_page()`
- `render_hash_priority_page()`
- `render_graph_algorithms_page()`
- `render_bubble_quickselect_sets_page()`

Graph Algorithms visualizations use DOT strings rendered through Streamlit's
`st.graphviz_chart`; this app does not require the separate Python `graphviz`
package.

---

## Analysis 

| Artifact                                 | Location                                                         |
|------------------------------------------|------------------------------------------------------------------|
| Comprehensive performance analysis       | `analysis/comprehensive_performance_analysis.md`                 |
| Search Big-O analysis                    | `search_comparison_module/analysis/big_o_analysis.md`            |
| Search recommendation guide              | `search_comparison_module/analysis/recommendation_guide.md`      |
| Search benchmark CSV                     | `search_comparison_module/analysis/benchmark_results.csv`        |
| Linked Structures written analysis       | `linked_structures_module/analysis/written_analysis.md`          |
| Linked Structures recommendation guide   | `linked_structures_module/analysis/recommendation_guide.md`      |
| Linked Structures benchmark CSV          | `linked_structures_module/analysis/benchmark_results.csv`        |
| Linked Structures operation winners CSV  | `linked_structures_module/analysis/operation_winners.csv`        |
| Linked Structures benchmark charts       | `linked_structures_module/analysis/charts/`                      |
| Tree Map written analysis                | `tree_map_module/analysis/written_analysis.md`                   |
| Tree Map recommendation guide            | `tree_map_module/analysis/recommendation_guide.md`               |
| Tree Map benchmark CSV                   | `tree_map_module/analysis/benchmark_results.csv`                 |
| Tree Map benchmark charts                | `tree_map_module/analysis/charts/`                               |
| Hash Priority written analysis           | `hash_priority_module/analysis/written_analysis.md`              |
| Hash Priority recommendation guide       | `hash_priority_module/analysis/recommendation_guide.md`          |
| Hash Priority benchmark CSV              | `hash_priority_module/analysis/benchmark_results.csv`            |
| Hash Priority speedup summary CSV        | `hash_priority_module/analysis/search_speedup_summary.csv`       |
| Hash Priority operation scaling CSV      | `hash_priority_module/analysis/operation_scaling_summary.csv`    |
| Hash Priority benchmark charts           | `hash_priority_module/analysis/charts/`                          |
| Graph Algorithms written analysis        | `graph_algorithms_module/analysis/written_analysis.md`           |
| Graph Algorithms recommendation guide    | `graph_algorithms_module/analysis/recommendation_guide.md`       |
| Graph Algorithms benchmark CSV           | `graph_algorithms_module/analysis/benchmark_results.csv`         |
| Graph Algorithms operation winners CSV   | `graph_algorithms_module/analysis/operation_winners.csv`         |
| Graph Algorithms operation scaling CSV   | `graph_algorithms_module/analysis/operation_scaling_summary.csv` |
| Graph Algorithms benchmark charts        | `graph_algorithms_module/analysis/charts/`                       |
| Bubble Quickselect Sets analysis         | `bubble_quickselect_module/analysis/written_analysis.md`         |
| Bubble Quickselect Sets benchmark CSV    | `bubble_quickselect_module/analysis/benchmark_results.csv`       |

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
