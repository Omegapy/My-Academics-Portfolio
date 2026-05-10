# File: __init__.py | Author: Alexander Ricciardi | Date: 2026-05-05
# Course: CSC506 | Professor: Dr. Jonathan Vanover | Spring A 2026
# -------------------------------------------------------------------------
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Benchmarking and performance analysis tools."""

from __future__ import annotations

from search_comparison_module.analysis.benchmark_searches import (
    DEFAULT_REPEATS,
    DEFAULT_SIZES,
    benchmark_single,
    load_results_csv,
    run_benchmarks,
    save_results_csv,
)

__all__ = [
    "DEFAULT_REPEATS",
    "DEFAULT_SIZES",
    "benchmark_single",
    "load_results_csv",
    "run_benchmarks",
    "save_results_csv",
]
