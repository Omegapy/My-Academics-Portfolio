"""Benchmarking, report generation, and performance analysis tools."""

from analysis.benchmark_search import (
    run_benchmarks,
    save_results_csv,
    load_results_csv,
    compute_speedup_summary,
    compute_operation_scaling_summary,
    estimate_search_time,
    benchmark_hash_table_search,
    benchmark_linear_search,
    build_collision_benchmark_state,
    build_priority_queue_benchmark_state,
    DEFAULT_SIZES,
    DEFAULT_QUERY_MODES,
    DEFAULT_QUERY_COUNT,
    DEFAULT_DELETE_SAMPLE_SIZE,
    DEFAULT_REPEATS,
    DEFAULT_RANDOM_SEED,
    DEFAULT_HEAP_MODES,
)
from analysis.report_generator import (
    build_benchmark_table,
    build_speedup_summary_table,
    build_operation_scaling_table,
    generate_summary_sentences,
    generate_charts,
    generate_all_reports,
)
from analysis.lab_validation import (
    ValidationStepResult,
    HashTableDemoResult,
    PriorityQueueDemoResult,
    BenchmarkValidationResult,
    run_hash_table_demo,
    run_priority_queue_demo,
    run_benchmark_validation,
    summarize_benchmark_validation,
)
