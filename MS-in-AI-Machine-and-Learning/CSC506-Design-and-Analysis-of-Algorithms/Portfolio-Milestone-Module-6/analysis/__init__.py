# -------------------------------------------------------------------------
# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-04-21
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# Module Functionality
# Package marker for analysis helpers and report-generation code.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Analysis package for Portfolio Milestone Module 6."""

from __future__ import annotations

from analysis.benchmark_search import (
    DEFAULT_QUERY_MODES,
    DEFAULT_REPEATS,
    DEFAULT_SIZES,
    compute_balance_summary,
    compute_speedup_summary,
    load_results_csv,
    run_benchmarks,
    save_results_csv,
)
from analysis.lab_validation import (
    run_benchmark_validation,
    run_bst_demo,
    run_map_demo,
    run_traversal_demo,
    run_unbalanced_tree_demo,
    summarize_benchmark_validation,
)
from analysis.report_generator import (
    build_balance_summary_table,
    build_benchmark_table,
    build_speedup_summary_table,
    generate_all_reports,
    generate_charts,
    generate_summary_sentences,
)

__all__ = [
    "DEFAULT_QUERY_MODES",
    "DEFAULT_REPEATS",
    "DEFAULT_SIZES",
    "build_balance_summary_table",
    "build_benchmark_table",
    "build_speedup_summary_table",
    "compute_balance_summary",
    "compute_speedup_summary",
    "generate_all_reports",
    "generate_charts",
    "generate_summary_sentences",
    "load_results_csv",
    "run_benchmark_validation",
    "run_benchmarks",
    "run_bst_demo",
    "run_map_demo",
    "run_traversal_demo",
    "run_unbalanced_tree_demo",
    "save_results_csv",
    "summarize_benchmark_validation",
]
