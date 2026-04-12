"""Dataset generation, validation, and preview utilities for sorting scenarios."""

from data.dataset_manager import (
    generate_random_dataset,
    generate_sorted_dataset,
    generate_reverse_sorted_dataset,
    generate_partially_sorted_dataset,
    generate_dataset_by_type,
    format_dataset_type_label,
    preview_dataset,
    validate_dataset,
    is_sorted_non_decreasing,
    DATASET_TYPES,
    DATASET_TYPE_LABELS,
)
