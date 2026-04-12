"""Benchmarking, report generation, and performance analysis tools."""

from analysis.benchmark_sorts import (
    run_benchmarks,
    save_results_csv,
    load_results_csv,
    compute_scenario_winners,
    save_scenario_winners_csv,
    estimate_sort_time,
    benchmark_single,
    DEFAULT_SIZES,
    DEFAULT_DATASET_TYPES,
    DEFAULT_REPEATS,
    DEFAULT_RANDOM_SEED,
)
from analysis.report_generator import (
    build_comparison_table,
    build_winner_summary,
    generate_summary_sentences,
    generate_charts,
    generate_all_reports,
)
