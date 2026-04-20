"""Benchmark engine and report generation for the Algorithm and Data Structure Comparison Tool."""

from analysis.benchmark_structures import (
    DEFAULT_SIZES,
    DEFAULT_REPEATS,
    DEFAULT_RANDOM_SEED,
    build_structure,
    benchmark_single,
    run_benchmarks,
    save_results_csv,
    load_results_csv,
    compute_operation_winners,
    save_operation_winners_csv,
)
from analysis.report_generator import (
    build_benchmark_table,
    build_operation_winners_table,
    generate_summary_sentences,
    generate_charts,
    generate_all_reports,
)

__all__ = [
    "DEFAULT_SIZES",
    "DEFAULT_REPEATS",
    "DEFAULT_RANDOM_SEED",
    "build_structure",
    "benchmark_single",
    "run_benchmarks",
    "save_results_csv",
    "load_results_csv",
    "compute_operation_winners",
    "save_operation_winners_csv",
    "build_benchmark_table",
    "build_operation_winners_table",
    "generate_summary_sentences",
    "generate_charts",
    "generate_all_reports",
]
