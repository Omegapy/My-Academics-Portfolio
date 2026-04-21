# Critical Thinking 5 — Hash Table & Priority Queue Tool
Program Name: Hash Table & Priority Queue Demonstration Tool

Date: 04/19/2026  
Grade: 

---

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover   
Spring A (26SA) – 2026  
Student: Alexander (Alex) Ricciardi  

---

## Program Description:

The program is a small streamlit application that implements a hash table, separate chaining collision resolution, 
and a binary heap priority queue. The tool has 7 tabs, which are: 
1. Hash Table
2. Priority Queue
3. Benchmark
4. Lab Validation
5. Written Analysis
6. Recommendation Guide
7. Charts

---

## Assignment:

**Requirements:**
- Create a hash table class that uses a simple hash function to store key-value pairs.
- Implement collision handling using either chaining or linear probing.
- Build a priority queue class using a binary heap data structure.
- Create functions to insert, delete, and search in both the hash table and priority queue.
- Test your implementations with at least 100 data items.
- Compare hash table search performance vs. linear search on the same dataset.


**Deliverables:**
- Source code file with hash table implementation including hash function and collision handling
- Source code file with priority queue implementation using binary heap
- Streamlit demonstration that inserts, searches, and deletes items from both data structures
- Performance comparison results showing hash table vs. linear search execution times
- Written explanation (2 pages) describing your hash function choice and collision resolution method
- Documentation explaining the difference between perfect and non-perfect hashing with examples
- Demo showing priority queue operations (insert, extract-max/min, peek)

**Success Criteria:**
- Hash table correctly stores and retrieves key-value pairs
- Collision handling works properly when hash function produces duplicate values
- Priority queue maintains heap property and correctly prioritizes items
- Performance testing shows hash table provides faster search than linear search
- Analysis clearly explains hashing concepts and implementation decisions
- Code includes proper error handling and user-friendly output

---

## Benchmark App Feature:

<img width="439" height="616" alt="image" src="https://github.com/user-attachments/assets/7615579f-3c83-4837-a37a-a5fc4b35608d" />
<img width="468" height="646" alt="image" src="https://github.com/user-attachments/assets/3a46cf5d-b3be-458e-9648-3ad721aa291d" />
<img width="391" height="648" alt="image" src="https://github.com/user-attachments/assets/a269ddb1-5c8b-4b57-9a0a-560fdf27e125" />
<img width="342" height="648" alt="image" src="https://github.com/user-attachments/assets/6dba7a8a-6f34-4a35-9a56-c5eb9c37ae7e" />
<img width="383" height="648" alt="image" src="https://github.com/user-attachments/assets/3537e574-eb75-481a-83f2-851ff02a8a84" />

---

## Program Requirements:
- Python 3.12+
- `streamlit` (install via `pip install streamlit`)
- `pandas` (install via `pip install pandas`)
- `matplotlib` (install via `pip install matplotlib`)

---

## How to Run:

```bash
# If using a Python virtual environment, first activate the virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install streamlit pandas matplotlib

# Launch the Streamlit app (from the repository root)
streamlit run streamlit_app.py

```

The app opens in your default browser at `http://localhost:8501`.

---

## Project Map:

```
CTA-5/
├── README.md                    # This file
├── streamlit_app.py             # Main Streamlit app 
├── written_analysis.docx        # -- written analysis Word Doc format --
|                                # describing hash function choice 
|                                # and collision resolution method
|                                # Comparative Big-O Analysis
├── recommendation_guide.docx    # -- Recommendation guide Word Doc format --
|                                # Recommendation guide for hashing choices 
|                                # and search strategy
|                                # difference between perfect and non-perfect 
|                                # hashing with examples
├── Screenshots Critical Thinking Module 5.docx      # Screenshots of the app
├── algorithms/                  # Data structure implementations
│   ├── __init__.py
│   ├── hash_table.py            # HashTable with separate chaining
│   ├── priority_queue.py        # BinaryHeapPriorityQueue (min/max)
│   └── linear_search.py         # Linear search baseline
├── models/                      # Shared dataclasses
│   ├── __init__.py
│   ├── hash_entry.py            # HashEntry (key, value)
│   ├── hash_table_stats.py      # HashTableStats snapshot
│   ├── priority_item.py         # PriorityItem with tie-breaking
│   └── benchmark_record.py      # BenchmarkRecord for search timing
├── data/                        # Dataset generation and validation
│   ├── __init__.py
│   └── dataset_manager.py       # Key-value, priority, and query generators
├── analysis/                    # Benchmark pipeline and reports
│   ├── __init__.py
│   ├── benchmark_search.py      # Search timing engine
│   ├── lab_validation.py        # Guided lab-demo and validation helpers
│   ├── report_generator.py      # Markdown tables and chart generation
│   ├── benchmark_results.csv    # Generated benchmark results
│   ├── written_analysis.md      # -- written analysis --
|   |                            # describing hash function choice 
|   |                            # and collision resolution method
|   |                            # Comparative Big-O Analysis
│   ├── recommendation_guide.md  # -- Recommendation guide --
|   |                            # Recommendation guide for hashing choices 
|   |                            # and search strategy
|   |                            # difference between perfect and non-perfect 
|   |                            # hashing with examples
│   └── charts/                                        # Generated chart images
│       ├── hash_vs_linear_search.png                  # Runtime comparison chart
│       ├── search_speedup.png                         # Speedup factor chart
│       └── collision_distribution.png                 # Bucket occupancy chart
├── ui/                                                # Streamlit UI helpers
│   ├── __init__.py
│   └── streamlit_helpers.py                           # Render functions for all tabs
```
---

## Deliverables:

| Deliverable                                          | Location                                         |
|------------------------------------------------------|--------------------------------------------------|
| Hash table source code                               | `algorithms/hash_table.py`                       |
| Priority queue source code                           | `algorithms/priority_queue.py`                   |
| Linear search baseline                               | `algorithms/linear_search.py`                    |
| Streamlit insert/search/delete demonstration         | `streamlit_app.py`                               |
| Guided in-app validation helpers                     | `analysis/lab_validation.py`                     |
| Benchmark results (CSV)                              | `analysis/benchmark_results.csv`                 |
| Performance comparison charts                        | `analysis/charts/*.png`                          |
| Written explanation (hash function & collision)      | `analysis/written_analysis.md`                   |
| Perfect vs non-perfect hashing documentation         | `analysis/recommendation_guide.md`               |
| Streamlit demo app                                   | `streamlit_app.py`                               |

---

## Operations Supported:

| Tab                    | Description                                                                                                               |
|------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Overview               | Project purpose, complexity tables for both data structures                                                               |
| Dataset Builder        | Generate key-value and priority datasets with configurable size/seed, including an optional forced-collision demo dataset |
| Hash Table Lab         | Bulk load, insert, search, delete, inspect bucket chains, and run guided 100-item and forced-collision validation demos   |
| Priority Queue Lab     | Bulk load, insert, peek, extract, search, delete, inspect heap state, and run guided 100-item min/max validation demos    |
| Benchmark Lab          | Run custom benchmarks or the assignment benchmark suite, then view validation checks, tables, and charts                  |
| Written Analysis       | (2-page) analysis with benchmark data placeholders                                                                        |
| Recommendation Guide   | Perfect vs non-perfect hashing explanation, examples, and hash table vs. linear search guidance                           |

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

