# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-04-27
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
#
# --- Module Functionality ---
# Package exports for CTA-7 graph analysis helpers.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Analysis helpers for the Module 8 graph algorithms page."""

from __future__ import annotations

from graph_algorithms_module.analysis.benchmark_graphs import (
    DEFAULT_GRAPH_KINDS,
    DEFAULT_SEED,
    DEFAULT_SIZES,
    compute_operation_scaling_summary,
    compute_operation_winners,
    load_results_csv,
    run_benchmarks,
    save_operation_winners_csv,
    save_results_csv,
)
from graph_algorithms_module.analysis.lab_validation import (
    run_bellman_ford_demo,
    run_benchmark_validation,
    run_positive_shortest_path_comparison,
    run_shortest_path_demo,
    run_traversal_demo,
)
from graph_algorithms_module.analysis.report_generator import (
    build_benchmark_table,
    build_operation_scaling_table,
    build_operation_winners_table,
    generate_charts,
)

__all__: list[str] = [
    "DEFAULT_GRAPH_KINDS",
    "DEFAULT_SEED",
    "DEFAULT_SIZES",
    "build_benchmark_table",
    "build_operation_scaling_table",
    "build_operation_winners_table",
    "compute_operation_scaling_summary",
    "compute_operation_winners",
    "generate_charts",
    "load_results_csv",
    "run_bellman_ford_demo",
    "run_benchmark_validation",
    "run_benchmarks",
    "run_positive_shortest_path_comparison",
    "run_shortest_path_demo",
    "run_traversal_demo",
    "save_operation_winners_csv",
    "save_results_csv",
]
