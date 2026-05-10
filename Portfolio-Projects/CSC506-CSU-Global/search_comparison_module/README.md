# Search Comparison Module

Program Name: Search Comparison Tool  
Course: CSC506 - Design and Analysis of Algorithms  
Professor: Dr. Jonathan Vanover  
Spring A 2026  
Student: Alexander Ricciardi  
License: Apache-2.0

## Module Purpose

This package integrates the Portfolio Milestone Module 2 Algorithm Comparison
Tool into the final Portfolio Module 8 app. It preserves the original linear
search and binary search workflows while adapting imports to the Module 8
package layout. The Streamlit UI is exposed through an importable page renderer
and runs inside the root Portfolio Module 8 app.

The module demonstrates:

- Linear search over integer lists with step-by-step tracing.
- Binary search over sorted integer lists with step-by-step tracing.
- Dataset generation, manual parsing, duplicate removal, and sorted copies.
- Side-by-side algorithm comparison.
- Benchmarking for worst-case missing-target searches.
- Big-O analysis and recommendation guidance.

## Source Origin

The implementation was copied from:

```text
Portfolio-Milestone-Module-2/
```

Original behavior is preserved. The copied files now use package-qualified
imports such as `search_comparison_module.algorithms`,
`search_comparison_module.data`, `search_comparison_module.models`,
`search_comparison_module.analysis`, and `search_comparison_module.ui` so they
can coexist with the other Portfolio Module 8 packages.

## How to Run

From the repository root:

```bash
source venv/bin/activate
streamlit run Portfolio-Module-8/streamlit_app.py
```

Open the `Search Comparison` tab in the root app. This module intentionally has
no separate `streamlit_app.py` entrypoint.

## How to Test

```bash
source venv/bin/activate
python -m pytest Portfolio-Module-8/tests -v
```

## Feature Map

| Area | Location |
|---|---|
| Linear search | `algorithms/linear_search.py` |
| Binary search | `algorithms/binary_search.py` |
| Search result model | `models/search_result.py` |
| Dataset helpers | `data/dataset_manager.py` |
| Benchmark engine | `analysis/benchmark_searches.py` |
| Big-O analysis | `analysis/big_o_analysis.md` |
| Recommendation guide | `analysis/recommendation_guide.md` |
| Saved benchmark CSV | `analysis/benchmark_results.csv` |
| Root-rendered Streamlit page | `overview_page.py` |

## Overview Page Integration

The root app imports
`search_comparison_module.overview_page.render_search_comparison_page()` and
renders it directly inside the `Search Comparison` tab. The page starts with an
`Overview` landing tab, then preserves the original Module 2 dataset builder,
search playground, comparison, benchmark, Big-O analysis, and recommendation
guide workflows.
