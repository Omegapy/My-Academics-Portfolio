# Hash Priority Module

Program Name: Hash Table & Priority Queue Integration  
Date: 05/05/2026

Design and Analysis of Algorithms CSC506  
Professor: Dr. Jonathan Vanover  
Spring A (26SA) - 2026  
Student: Alexander (Alex) Ricciardi

---

## Source Origin

This package integrates the CTA-5 Hash Table & Priority Queue Tool into the
single Portfolio Module 8 Streamlit app. The original `CTA-5/` folder remains
unchanged; Module 8 uses this copied package with package-qualified imports.

## Concepts Implemented

- Separate-chaining `HashTable` with insert, search, delete, update, resizing,
  collision statistics, and bucket inspection.
- `BinaryHeapPriorityQueue` with max-heap and min-heap modes, insert, peek,
  extract, search, delete, and heap validation.
- `linear_search_by_key` baseline for hash table search comparisons.
- Deterministic key-value datasets, forced-collision datasets, priority-item
  datasets, benchmark query sets, and validation helpers.
- Benchmark reporting for hash search vs. linear search, collision behavior,
  heap operations, speedup summaries, operation scaling, and chart artifacts.

## Module 8 Integration

The root app imports:

```python
from hash_priority_module.overview_page import render_hash_priority_page
```

Run only the root app:

```bash
source venv/bin/activate
streamlit run Portfolio-Module-8/streamlit_app.py
```

This package does not contain a standalone `streamlit_app.py`. Its
`overview_page.py` module exposes `render_hash_priority_page()` and namespaces
Streamlit state/widget keys with `hp_` so it can render safely beside the other
Portfolio Module 8 pages.

## Package Changes

Local CTA-5 imports were rewritten from generic names such as `algorithms`,
`analysis`, `data`, `models`, and `ui` to package-qualified Module 8 imports
such as `hash_priority_module.algorithms` and `hash_priority_module.analysis`.

The public package exports include:

- `HashTable`
- `BinaryHeapPriorityQueue`
- `linear_search_by_key`
- `HashEntry`
- `HashTableStats`
- `PriorityItem`
- `BenchmarkRecord`

## Analysis Artifacts

| Artifact | Location |
|---|---|
| Written analysis | `analysis/written_analysis.md` |
| Recommendation guide | `analysis/recommendation_guide.md` |
| Benchmark CSV | `analysis/benchmark_results.csv` |
| Search speedup summary | `analysis/search_speedup_summary.csv` |
| Operation scaling summary | `analysis/operation_scaling_summary.csv` |
| Benchmark charts | `analysis/charts/` |

## How to Test

```bash
source venv/bin/activate
python -m pytest Portfolio-Module-8/tests -v
```
