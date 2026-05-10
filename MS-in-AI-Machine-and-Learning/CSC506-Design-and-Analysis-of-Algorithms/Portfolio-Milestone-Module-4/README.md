# Portfolio Milestone Module 4 — Algorithm and Data Structure Comparison Tool

Program Name: Algorithm and Data Structure Comparison Tool

Date: 04/12/2026  
Grade: 100% A

---

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover  
Spring A (26SA) – 2026  
Student: Alexander (Alex) Ricciardi

---

## Program Description:

The Algorithm and Data Structure Comparison Tool is a Streamlit web application that
implements, demonstrates, and benchmarks the four linear datastructures: 
a list-backed `Stack`, a list-backed `Queue`, a list-backed `Deque`, and a custom doubly-linked `LinkedList`. 
The tool lets the user generate datasets, use operations in an
playground, run reproducible benchmarks at choosen sizes
`[1_000, 5_000, 10_000, 50_000]`, save results to CSV, render charts, and read
the written analysis and recommendation guide alongside live benchmark output.

---

## Portfolio Assignment Context:

This module is part of the portfolio project for CSC506. The portfolio goal is to build a system demonstrating mastery of the course concepts (sets, sorting, searching, data structures). Module 4 contributes the **data-structure foundation** of that portfolio.

**Implemented Modules:**
- Portfolio Milestone Module 2 — see [`Portfolio-Milestone-Module-2/README.md`](../Portfolio-Milestone-Module-2/README.md). Compares linear search O(n) vs. binary search O(log n).
- Portfolio Milestone Module 4 — *this module* — custom doubly linkedList and the Stack / Queue / Deque using Python list.

**Portfolio Project:**
I choose to create a web application that allows users to interact with and compare different data structures and algorithms. I chose to create a web app using Streamlit, called Algorithm Comparison Tool

---

## This Module Assignment:

**Requirements**
- Implement a `Stack` class with `push`, `pop`, `peek`, and `isEmpty`.
- Implement a `Queue` class with `enqueue`, `dequeue`, `front`, and `isEmpty`.
- Implement a `Deque` class with `addFront`, `addRear`, `removeFront`, `removeRear`, and `isEmpty`.
- Implement a `LinkedList` class with `insert`, `delete`, `search`, and `display`.
- Build test programs that demonstrate when each data structure is most appropriate.
- Develop algorithms that use each data structure to solve a specific problem.

**Deliverables**
- Source files for `Stack`, `Queue`, `Deque`, and (doubly) `LinkedList`.
- Test programs demonstrating each structure with sample data.
- Problem-solving examples for each structure.
- Written analysis (~2 pages) contrasting the four structures and explaining when to use each.
- Performance comparison showing operation efficiency for each implementation.

**Success Criteria**
- All structures correctly implement their required operations.
- Test programs successfully demonstrate each structure's functionality.
- Problem-solving examples clearly show appropriate use cases.
- Analysis accurately contrasts the strengths and weaknesses of each structure.
- Implementations follow Python coding standards and the project documentation guide.

---

## Benchmark Lab App Feature:
<img width="423" height="612" alt="image" src="https://github.com/user-attachments/assets/fed47566-db06-4e9a-b2bb-451b4843370d" />
<img width="514" height="568" alt="image" src="https://github.com/user-attachments/assets/468741d9-7bb2-428b-a1b2-c8fff2f5cac9" />

---

## Program Requirements:
- Python 3.12+
- `streamlit` (install via `pip install streamlit`)
- `pandas` (install via `pip install pandas`)
- `matplotlib` (install via `pip install matplotlib`)
- `altair` (install via `pip install altair`) — used for in-app interactive charts

---

## How to Run:

```bash
# If using a Python virtual environment, first activate it
source venv/bin/activate

# Install dependencies (if not already installed)
pip install streamlit pandas matplotlib altair

# Launch the Streamlit app (from the repository root)
streamlit run Portfolio-Milestone-Module-4/streamlit_app.py
```

The Streamlit app opens in your default browser at `http://localhost:8501`.


--

**Project Map:**

```
Portfolio-Milestone-Module-4/
├── README.md                                       # This file
├── streamlit_app.py                                # Main Streamlit application 
├── written_analysis.docx                           # Analysis Word Doc format
├── recommendation_guide.docx                       # Recommendation guide/comparison Word Doc format
├── Screenshots Portfolio Milestone Module 4.docx   # Screenshots of the app  
├── data_structures/                                # ADT implementations
│   ├── __init__.py
│   ├── stack.py                           # List-backed Stack
│   ├── queue.py                           # List-backed Queue (course-aligned)
│   ├── deque.py                           # List-backed Deque (course-aligned)
│   └── linked_list.py                     # Doubly linked Node + LinkedList
├── models/                                # Dataclass result contracts
│   ├── __init__.py
│   ├── operation_result.py                # Playground operation result
│   ├── benchmark_record.py                # One row of benchmark data
│   └── operation_winner.py                # Fastest structure per group/size
├── data/                                  # Dataset generation
│   ├── __init__.py
│   └── dataset_manager.py
├── analysis/                              # Benchmark engine, report, deliverables
│   ├── __init__.py
│   ├── benchmark_structures.py            # Timing engine + run_benchmarks
│   ├── report_generator.py                # Markdown tables + chart PNGs
│   ├── benchmark_results.csv              # Generated benchmark output
│   ├── operation_winners.csv              # Generated winners output
│   ├── written_analysis.md                # ~2 page written analysis
│   ├── recommendation_guide.md            # Decision-focused guide
│   └── charts/                            # Generated PNG charts
│       ├── common_operation_runtime.png
│       ├── structure_specific_runtime.png
│       ├── operation_winner_heatmap.png
│       └── structure_profile_comparison.png
```

---

**Deliverables:**

| Deliverable                              | Location                                                                  |
|------------------------------------------|---------------------------------------------------------------------------|
| `Stack` source                           | `data_structures/stack.py`                                                |
| `Queue` source                           | `data_structures/queue.py`                                                |
| `Deque` source                           | `data_structures/deque.py`                                                |
| `Node` + `LinkedList` source             | `data_structures/linked_list.py`                                          |
| Interactive test programs                | `streamlit_app.py` (Structure Playground tab)                             |
| Pytest correctness tests                 | `tests/test_data_structures.py`                                           |
| Use-case examples and recommendations    | `analysis/recommendation_guide.md`                                        |
| Written analysis (~2 pages)              | `analysis/written_analysis.md`                                            |
| Benchmark engine                         | `analysis/benchmark_structures.py`                                        |
| Benchmark results CSV                    | `analysis/benchmark_results.csv`                                          |
| Operation winners CSV                    | `analysis/operation_winners.csv`                                          |
| Benchmark charts (PNG)                   | `analysis/charts/`                                                        |
| Streamlit app                            | `streamlit_app.py`                                                        |

---

**App Features:**

| Feature              | Description                                                                                       |
|----------------------|---------------------------------------------------------------------------------------------------|
| Overview             | Project description, the four ADTs, key operations, and Big-O concepts                           |
| Dataset Builder      | Generate sequential / random / reverse / manual datasets with seed and size controls            |
| Structure Playground | Run every required operation against a selected structure on the loaded dataset                  |
| Compare Structures   | Side-by-side cards plus a Big-O complexity table covering every required operation               |
| Benchmark Lab        | Run, save, and load benchmarks; render the table and interactive charts                          |
| Written Analysis     | Render `analysis/written_analysis.md` with live placeholder substitution                         |
| Recommendation Guide | Render `analysis/recommendation_guide.md` with the live operation-winner heatmap                 |

---

## Benchmark Workloads

The Benchmark Lab measures the following workloads on fresh structure instances per size, using `timeit.Timer.autorange()` + `min(timer.repeat(...))` for stable timings:

| Workload              | Description                                                                                 |
|-----------------------|---------------------------------------------------------------------------------------------|
| `common_build`        | Add `n` values to an empty structure (`push`, `enqueue`, `addRear`, `insert(rear)`)          |
| `common_drain`        | Remove all values from a preloaded structure (`pop`, `dequeue`, `removeFront`, `delete`)    |
| `peek_front`          | Inspect the front/top without removal (`peek`, `front`, `peekFront`, `peekRear`)             |
| `deque_ends`          | Compare both deque ends (`addFront`, `addRear`, `removeFront`, `removeRear`)                 |
| `linked_list_search`  | Search for a middle value and a missing value                                                |
| `linked_list_delete`  | Delete head, tail, middle, and missing values                                                |
| `linked_list_display` | Forward and reverse traversal of the entire list                                             |

Default sizes: `[1_000, 5_000, 10_000, 50_000]`. Default repeats: `5`. Results are saved to `analysis/benchmark_results.csv` from the Save Results to CSV button in the Benchmark Lab tab.

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

