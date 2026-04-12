# Critical Thinking 3 - Sorting Algorithm Performance Comparison Tool

Program Name: Sorting Algorithm Performance Comparison Tool

Data:  04/05/2026  
Grade: 100% A 

---

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover   
Spring A (26SA) – 2026  
Student: Alexander (Alex) Ricciardi  

---

## Program Description:

The program is a Sorting Algorithm Performance Comparison Tool web-app that compares 4 sorting algorithms 
: bubble sort O(n^2), selection sort O(n^2), insertion sort O(n^2), and merge sort O(n log n) 
The program compares these algorithms across different dataset types and sizes. The web-app allows the user to build datasets (random, sorted, reverse sorted, partially sorted), to run individual sorts with step traces, to compare all four algorithms side by side, to benchmark at scale with timing charts, and to review a written analysis and recommendation guide.

---

## Assignment:

**Requirements:**
- Implement four different sorting algorithms: bubble sort, selection sort, insertion sort, and merge sort.
- Create a data generator that produces different types of datasets (random, already sorted, reverse sorted, partially sorted).
- Build a timing system that measures execution time for datasets of different sizes (1000, 5000, 10000, 50000 elements).
- Test each algorithm on all dataset types and sizes.
- Create a report generator that shows which algorithm performs best for each scenario.


**Deliverables:**
- Source code files for all four sorting algorithms with clear documentation
- Data generator that creates the four types of test datasets
- Performance testing results in a table showing execution times for all combinations
- Written analysis (2-3 pages) explaining when to use each sorting algorithm
- Charts or graphs visualizing the performance differences between algorithms
- Recommendation guide for choosing sorting algorithms based on data characteristics

**Success Criteria:**
- All four sorting algorithms correctly sort arrays of any size
- Performance testing shows clear timing differences between algorithms
- Analysis correctly explains the trade-offs between different sorting methods
- Recommendations provide practical guidance for algorithm selection
- Tool demonstrates real-world application for large data processing

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
CTA-3/
├── README.md                                        # This file
├── streamlit_app.py                                 # Application UI entry point
├── written_analysis.docx                            # Big-O analysis Word Doc format
├── recommendation_guide.docx                        # Recommendation guide Word Doc format
├── Screenshots Critical Thinking Module 3.docx      # Screenshots of the app
├── algorithms/
│   ├── __init__.py
│   ├── bubble_sort.py                                 # Bubble sort — O(n^2)
│   ├── selection_sort.py                              # Selection sort — O(n^2)
│   ├── insertion_sort.py                              # Insertion sort — O(n^2)
│   └── merge_sort.py                                  # Merge sort — O(n log n)
├── models/
│   ├── __init__.py
│   ├── sort_result.py                                 # SortResult dataclass
│   ├── benchmark_record.py                            # BenchmarkRecord dataclass
│   └── scenario_summary.py                            # ScenarioSummary dataclass
├── data/
│   ├── __init__.py
│   └── dataset_manager.py                             # Dataset generation and validation
├── analysis/
│   ├── __init__.py
│   ├── benchmark_sorts.py                             # Benchmark engine (timing, CSV export)
│   ├── report_generator.py                            # Report and chart generation
│   ├── benchmark_results.csv                          # Generated benchmark data
│   ├── scenario_winners.csv                           # Best algorithm per scenario
│   ├── written_analysis.md                            # Written analysis (2-3 pages)
│   ├── recommendation_guide.md                        # Algorithm selection guide
│   └── charts/
│       ├── runtime_by_size.png                        # Runtime growth visual
│       ├── runtime_by_dataset_type.png                # Dataset-type comparison visual
│       ├── scenario_winner_heatmap.png                # Winner matrix heatmap
│       └── algorithm_profile_comparison.png           # Qualitative tradeoff view
├── ui/
│   ├── __init__.py
│   └── streamlit_helpers.py                           # Streamlit UI rendering helpers
|
```

---

## Deliverables:

| Deliverable                        | Location                                                           |
|------------------------------------|--------------------------------------------------------------------|
| Bubble sort implementation         | `algorithms/bubble_sort.py`                                        |
| Selection sort implementation      | `algorithms/selection_sort.py`                                     |
| Insertion sort implementation      | `algorithms/insertion_sort.py`                                     |
| Merge sort implementation          | `algorithms/merge_sort.py`                                         |
| Data generator                     | `data/dataset_manager.py`                                          |
| Performance testing results        | Benchmark Lab tab -> `analysis/benchmark_results.csv`              |
| Written analysis (2-3 pages)       | `analysis/written_analysis.docx` and `analysis/written_analysis.md`|
| Charts / graphs                    | Benchmark Lab tab -> `analysis/charts/*.png`                       |
| Recommendation guide               | `recommendation_guide.docx` and `analysis/recommendation_guide.md` |

---

## Operations Supported:

| Tab                    | Description                                                              |
|------------------------|--------------------------------------------------------------------------|
| Overview               | Project description, sorting concepts, assignment goals                  |
| Dataset Builder        | Build and preview datasets of different types and sizes                  |
| Sort Playground        | Run one algorithm on one dataset and inspect metrics / step trace        |
| Compare Algorithms     | Compare all four algorithms on the same dataset side by side             |
| Benchmark Lab          | Run benchmark scenarios, inspect tables, charts, and export CSV          |
| Written Analysis       | In-browser written analysis document with benchmark data                 |
| Recommendation Guide   | In-browser algorithm selection recommendation guide                      |

---

## Sorting and Timing Approaches

This project uses different sorting/timing approaches depending on the feature being used:

| Feature                    | Purpose                                                  | Sort Feature Description                                                                          | Timing Feature Description                                                                                                                  |
|----------------------------|----------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Sort Playground            | Single-sort demo                                         | Run one algorithm on the user-generated dataset and show the results                              | Use a stable batched timing estimate computed on fresh dataset copies with tracing disabled so small sorts are less affected by timer noise |
| Compare Algorithms         | Side-by-side comparison                                  | Run the four sorting algorithms on the user-generated dataset, display results side-by-side       | Use the same stable batched timing estimate as the playground                                                                               |
| Benchmark Lab              | Runs benchmarks across different sizes and dataset types | Generate different dataset sizes and types and run all four algorithms on each                    | Use repeated batched measurements with tracing disabled and report median or best normalized times                                          |
| Benchmark in CMD (offline) | Run benchmarks in the terminal offline                   | Generate different dataset sizes and types and run all four algorithms on each using the terminal | Use the same repeated batched measurement as the Benchmark Lab, running from the terminal                                                   |


---

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 