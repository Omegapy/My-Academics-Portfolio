# Tree Map Module

Portfolio Module 8 integration package for the Portfolio Milestone Module 6
tree and map comparison work.

## Source Origin

This package was copied and adapted from `Portfolio-Milestone-Module-6/`.
The original assignment folder remains unchanged.

## Concepts Implemented

- Binary Search Tree with insert, search, delete, minimum, maximum, traversal,
  height, balance detection, and ASCII rendering.
- BST-backed `Map` class for ordered key-value storage.
- `ListMap` baseline for linear-search map comparison.
- Dataset builders for integer, string, and tuple keys.
- Guided BST, traversal, unbalanced-tree, and map validation demos.
- TreeMap versus ListMap search benchmarks.

## Root App Integration

Run the single Portfolio Module 8 app:

```bash
streamlit run Portfolio-Module-8/streamlit_app.py
```

This package does not provide a standalone `streamlit_app.py`. The root app
imports `tree_map_module.overview_page.render_tree_map_page()` and renders the
Tree Map workflows inside the main `Tree Map` tab.

## Module 8 Adaptations

- Local imports were rewritten to package-qualified paths such as
  `tree_map_module.data_structures` and `tree_map_module.analysis`.
- Streamlit session-state keys and widget keys use the `tm_` prefix so this
  page can run beside other integrated modules in one Streamlit process.
- The preserved Module 6 UI is exposed as an import-safe page renderer with an
  added Portfolio Module 8 overview tab.

## Analysis Artifacts

| Artifact | Location |
|---|---|
| Written analysis | `tree_map_module/analysis/written_analysis.md` |
| Recommendation guide | `tree_map_module/analysis/recommendation_guide.md` |
| Benchmark CSV | `tree_map_module/analysis/benchmark_results.csv` |
| Search speedup summary | `tree_map_module/analysis/search_speedup_summary.csv` |
| Balance summary | `tree_map_module/analysis/balance_summary.csv` |
| Benchmark charts | `tree_map_module/analysis/charts/` |

## Tests

Run the Module 8 test suite from the repository root:

```bash
python -m pytest Portfolio-Module-8/tests -v
```
