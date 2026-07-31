# Portfolio Milestone Module 2 — Algorithm Comparison Tool Linear and Binary Search
Program Name: Algorithm Comparison Tool

Date: 03/29/2026  
Grade: 100% A

---

Design and Analysis of Algorithms CSC506.   
Professor: Dr. Jonathan Vanover.  
Spring A (26SA) – 2026.  
Student: Alexander (Alex) Ricciardi. 

---

## Program Description:

The Algorithm Comparison Tool is a web-app that compares linear search O(n) vs. binary search O(log n) algorithms using integer datasets. The tool provides a browser UI that allows the user to build datasets, run searches with step traces, compare both algorithms side by side, and benchmark at scale with timing charts. It also provides a Big-O analysis and recommendation guide.

---

## Assignment:

**Main Project Goal:**
Build the foundation of your portfolio project with comprehensive search and sorting algorithm implementations.

**Selected Option:** Algorithm Comparison Tool

**This Portfolio Milestone:**

Deliverables:
- Source code file with linear search implementation
- Source code file with binary search implementation
- Performance testing results showing execution times for different array sizes
- Written analysis (1-2 pages) explaining Big O notation for both algorithms
- Screenshots showing the tool finding items in different sized datasets
- Recommendation guide explaining when to choose each algorithm

Success Criteria:
- Linear search works correctly on any array
- Binary search works correctly on sorted arrays only
- Timing results clearly show performance differences
- Analysis correctly explains O(n) vs O(log n) complexity
- Tool demonstrates real-world application of search algorithms

---

## Program Requirements:
- Python 3.12+
- `streamlit` (install via `pip install streamlit`)
- `pandas` (install via `pip install pandas`)
- `colorama` (install via `pip install colorama`)

---

## How to Run:

```bash
# If using a Python virtual environment, first activate the virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install streamlit pandas colorama

# Launch the Streamlit app (from the repository root)
streamlit run Portfolio-Milestone-Module-2/streamlit_app.py
```

The app opens in your default browser at `http://localhost:8501`.

---

Algorithm Comparison Tool - Benchmark Lab Feature

<img width="351" height="617" alt="image" src="https://github.com/user-attachments/assets/a205970d-5fbc-42a2-856d-3429e66b85e4" />

---

**Project Map:**

```
Portfolio-Milestone-Module-2/
├── streamlit_app.py                                   # Application UI entry point
├── README.md                                          # This file
├── Big-O-Analysis-Module-2.docx                       # Big-O analysis Word Doc format
├── Recommendation-Guide-Module-2.docx                 # Recommendation guide Word Doc format
├── video_demo.mp4  -> https://youtu.be/KCxRs8Ug5m0    # Video demo of the app
├── Screenshots Portfolio Milestone Module 2.docx      # Screenshots of the app
├── algorithms/
│   ├── __init__.py
│   ├── linear_search.py              # Linear (sequential) search — O(n)
│   └── binary_search.py              # Iterative binary search — O(log n)
├── models/
│   ├── __init__.py
│   └── search_result.py              # SearchResult dataclass
├── data/
│   ├── __init__.py
│   └── dataset_manager.py            # Dataset generation
├── ui/
│   ├── __init__.py
│   └── streamlit_helpers.py          # Streamlit UI helpers
├── analysis/
│   ├── __init__.py
│   ├── benchmark_searches.py         # Benchmarking logic (timing, CSV export)
│   ├── benchmark_results.csv         # Generated benchmark data (after running)
│   ├── big_o_analysis.md             # Written Big-O analysis (1-2 pages)
│   ├── recommendation_guide.md       # When-to-choose-each-algorithm guide
```

---

**Deliverables:**

| Deliverable                        | Location                                                                    |
|------------------------------------|-----------------------------------------------------------------------------|
| Linear search implementation       | `algorithms/linear_search.py`                                               |
| Binary search implementation       | `algorithms/binary_search.py`                                               |
| Performance testing results        | Benchmark Lab tab / `analysis/benchmark_results.csv`                        |
| Big-O analysis (1-2 pages)         | `analysis/big_o_analysis.md` and `analysis/big_o_analysis.docx`             |
| Recommendation guide               | `analysis/recommendation_guide.md` and `analysis/recommendation_guide.docx` |
| Video demo                         | `video_demo.mp4`                                                            |

---

**App Features:**

| Feature                  | Description                                                    |
|--------------------------|----------------------------------------------------------------|
| Dataset Builder          | Generate sample, random, or manually entered integer datasets  |
| Search Playground        | Run linear or binary search with trace                         |
| Algorithm Comparison     | Comparison of the algorithms metrics on the same dataset       |
| Benchmark Lab            | Algorithm performance benchmarks for various dataset sizes     |
| Big-O Analysis           | In-browser Big-O analysis document                             |
| Recommendation Guide     | In-browser algorithm recommendation guide                      |
| CSV Export               | Save benchmark results to CSV                                  |

---

## Search and Timing Approaches

This project uses slightly different search/timing approaches depending on the feature being used:

| Feature | Purpose | Search Approach | Timing Approach |
|---------|---------|-----------------|-----------------|
| Search Playground | Interactive single-search demo | Runs one selected algorithm on the current dataset and shows the full result with step trace | Uses a stable batched timing estimate so very small searches are less affected by microsecond-level noise |
| Compare Algorithms | Side-by-side demonstration | Runs both linear search and binary search on the same sorted dataset for a fair comparison | Uses the same stable batched timing estimate as the Search Playground |
| Benchmark Lab | Performance measurement across dataset sizes | Generates fresh sorted datasets for each size and uses a worst-case missing target to force maximum comparisons | Uses repeated `timeit`-style batched measurements so the timing results are more reliable for analysis |

### Why these approaches are different

- The Search Playground and Compare Algorithms tabs prioritize responsiveness and explanation, so they keep the step trace and show a stable estimate of the search time.
- The Benchmark Lab prioritizes measurement quality, so it disables step-trace overhead and runs repeated batched timing samples to better reflect algorithm scaling.
- Binary search is always performed on sorted data in the app. In the interactive tabs and benchmark, the app uses datasets that are already sorted before the search is run.

---

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img width="27" height="27" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53" alt="Code Chronicles logo"></a><a href="https://www.alexomegapy.com"><img height="30" src="https://img.shields.io/badge/Code%20Chronicles%20%7C%20Omegapy-0D1117?style=for-the-badge" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>

