# -----------------------------------------------------------------------------
# Module Type: library module
# -----------------------------------------------------------------------------
# Project: CubeSat Telemetry AI Portfolio Program
# Author: Alexander S. Ricciardi
# Date: 09/13/2026
# -----------------------------------------------------------------------------
# Course: Foundations of Artificial Intelligence CSC510
# Professor: Dr. Isaac Gang
# Term: Fall A (26FA) - 2026
# Assignment: AI Use-Case Problem With Solution - Portfolio Project
# -----------------------------------------------------------------------------
# Project Description:
# Analyze OPS-SAT telemetry with classification, similarity, symbolic reasoning,
# and simulated diagnostic planning while preserving human decision authority.
# ------------------------------------------------------------------------------
# Assignment:
# Your final Portfolio Project will be a fully-functioning AI program built to solve
# a real-world problem of your choosing, utilizing the tools and techniques outlined
# in this course. Your program will interact with human beings to support decision-making
# processes by delivering relevant information about the problem.
#
# Your final project submission should include a self-executable Python program. The
# program should be complete and straightforward to test. The program should leverage
# methods learned from at least 2 of the modules from this course. The submission
# must function and be a reasonable attempt at a solution for your chosen problem.
# The solution does not have to be correct or useful in the real world, but the
# solution MUST provide reasonable answers without error.
#
# In addition to your program, your submission should include a 2-4 page essay
# describing the final version of your AI program, the use-case it intends to
# solve, and the methods you used toward that goal. In your paper, please address
# the following details:
# - The tools, libraries, and APIs utilized,
# - Search methods used and how they contributed toward the program goal,
# - Inclusion of any deep learning models,
# - Aspects of your program that utilize expert system concepts,
# - How your program represent knowledge,
# - How symbolic planning is used in your program (remember, symbolic planning
# is not limited to robot navigation).
# -----------------------------------------------------------------------------
# Module Purpose:
# - Find reviewed normal and anomalous segments close to the selected feature row.
# - Describe historical agreement or conflict with the classifier's prediction.
#
# Usage / Integration:
# - The coordinator builds one index with its fitted model and reuses it for analyses.
# - Verification/tests also call the index and retrieval functions directly.
#
# Contents Overview:
# - SimilarityIndex stores class estimators, reference rows, and their identities.
# - build_similarity_index() fits the available class indexes.
# - _retrieve_class_cases() and find_similar_cases() return comparison evidence.
#
# Dependencies:
# - Standard Library: dataclasses, typing.
# - Third-Party: NumPy, scikit-learn.
# - Local Project: cubesat_config, cubesat_types.
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Retrieve inspectable class-aware historical evidence for one telemetry segment.

The selected segment is the query. The historical references are reviewed examples from official
training rows. Comparing their standardized features gives the user nearby normal and anomalous
examples to inspect alongside the classifier's probability.

Separate indexes search each available reviewed class. Eligible retrieved candidates are sorted
by distance and segment ID before display. Smaller distances mean closer numerical feature values;
they do not establish a shared physical cause or a calibrated anomaly probability.
"""

# ____________________________________________________________________________________
# ====================================================================================
#
# SIMILARITY EQUATION AND EVIDENCE MAP
#
# d(x, r) = sqrt(sum_j((x_standardized[j] - r_standardized[j]) ** 2))
#
# Euclidean distance is the straight-line separation in the 18-feature space.
# j selects a feature column; x is the query and r is one reference segment.
# Both rows use the classifier's training-fitted mean and spread for each feature.
# This keeps a feature with a large raw scale from dominating only because of its units.
#
# query -> normal index and anomalous index -> ranked cases -> support/conflict result
#
# A class estimator returns positions within its own rows. class_positions maps
# those positions to the complete reference matrix, which retains original segment IDs.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

from dataclasses import dataclass # Import dataclass for data storage.
from typing import Any # Import Any for type hinting.

# pyrefly: ignore [missing-import]
import numpy as np # Import numpy for numerical operations.
from sklearn.neighbors import NearestNeighbors # Import NearestNeighbors for neighbor search.

from cubesat_config import DEFAULT_CONFIG, AppConfig # Import the default configuration and app configuration.
from cubesat_types import (
    ClassificationResult, # Import classification result.
    DatasetPartitions, # Import dataset partitions.
    FeatureDifference, # Import feature difference.
    SimilarCase, # Import similar case.
    SimilarityResult, # Import similarity result.
    TrainedTelemetryModel, # Import trained telemetry model.
)

# __________________________________________
# INDEX STATE
# ==========================================


# --- class SimilarityIndex
@dataclass(frozen=True, slots=True)
class SimilarityIndex:
    """Store reusable neighbor indexes and the row mappings needed to explain a match.

    The frozen dataclass prevents rebinding its fields. The estimators are still fitted library
    objects; freezing this record does not make every nested object immutable.

    Attributes:
        normal_estimator: Fitted normal-class index, or `None` if no such rows are available.
        anomalous_estimator: Fitted anomalous-class index, with the same absence convention.
        normal_reference_positions: Normal rows' positions in the complete reference matrix.
        anomalous_reference_positions: Anomalous rows' positions in that same matrix.
        reference_dataset_indices: Original dataset row index for each reference-matrix row.
        x_standardized_reference_features: Reference matrix in the classifier's fitted scale.
        reference_segment_ids: Segment identity for each reference-matrix row.
        reference_labels: Reviewed binary labels aligned with those IDs and rows.
        feature_names: Column names in the same order as every stored feature vector.
    """

    normal_estimator: Any | None
    anomalous_estimator: Any | None
    normal_reference_positions: tuple[int, ...]
    anomalous_reference_positions: tuple[int, ...]
    reference_dataset_indices: tuple[int, ...]
    x_standardized_reference_features: np.ndarray
    reference_segment_ids: tuple[str, ...]
    reference_labels: tuple[int, ...]
    feature_names: tuple[str, ...]
# --- end class SimilarityIndex


# ________________________________________________
# Class-specific reference indexes
# ------------------------------------------------
# Build reusable retrieval state from reviewed rows already expressed on the model's scale.
# --- build_similarity_index()
def build_similarity_index(
    partitions: DatasetPartitions,
    trained_model: TrainedTelemetryModel,
    *,
    config: AppConfig = DEFAULT_CONFIG,
) -> SimilarityIndex:
    """Fit one reusable neighbor index for each available reviewed class.

    Args:
        partitions: Dataset and historical-reference indices from the same fitted workflow.
        trained_model: Model holding the reference rows transformed by its training-only scaler.
        config: Shared similarity settings; the project default metric is Euclidean distance.

    Returns:
        Class indexes and metadata aligned to the model's complete reference matrix.

    Logic:
        1. Read reviewed labels in reference-row order.
        2. Select each class's positions within that reference matrix.
        3. Fit an index for each nonempty class and retain the shared row/ID mapping.
    """
    # Read reviewed labels in reference-row order.
    dataset = partitions.dataset

    reference_labels_array = dataset.y_anomaly_labels[
        np.asarray(partitions.reference_indices, dtype=np.int64)
    ]
    # These are positions within the reference matrix, not indices into the full dataset.
    # Keeping that distinction avoids attaching a neighbor's distance to the wrong segment.
    #
    # Select each class's positions within that reference matrix.
    # Normal positions within that reference matrix.
    normal_positions = tuple(
        int(position) for position in np.flatnonzero(reference_labels_array == 0)
    )
    # Anomalous positions within that reference matrix.
    anomalous_positions = tuple(
        int(position) for position in np.flatnonzero(reference_labels_array == 1)
    )

    # --- fit_class_estimator()
    def fit_class_estimator(reference_positions: tuple[int, ...]) -> Any | None:
        """Fit the selected class rows, or return `None` when that class is unavailable.

        The input positions select already standardized rows. Building a neighbor index does not
        refit the feature scaler or train another anomaly classifier.

        Args:
            reference_positions: Positions within the reference matrix belonging to this class.

        Returns:
            Fitted neighbor index for the class, or `None` if the class is empty.
        """
        # Return `None` when that class is unavailable.
        if not reference_positions:
            return None
        
        # Build a neighbor index for the class.
        estimator = NearestNeighbors(metric=config.similarity_metric)

        # Fit the neighbor index.
        estimator.fit(
            trained_model.x_standardized_reference_features[
                np.asarray(reference_positions, dtype=np.int64)
            ],
        )
        
        # Return the fitted neighbor index.
        return estimator
    # ---

    # Return SimilarityIndex
    return SimilarityIndex(
        normal_estimator=fit_class_estimator(normal_positions), # Fitted normal-class index, or None if no such rows are available.
        anomalous_estimator=fit_class_estimator(anomalous_positions), # Fitted anomalous-class index, with the same absence convention.
        # Normal rows' positions in the complete reference matrix.
        normal_reference_positions=normal_positions, 
        # Anomalous rows' positions in that same matrix.
        anomalous_reference_positions=anomalous_positions, 
        # Original dataset row index for each reference-matrix row.
        reference_dataset_indices=partitions.reference_indices, 
        # Reference matrix in the classifier's fitted scale.
        x_standardized_reference_features=trained_model.x_standardized_reference_features, 
        # Reference segment IDs.
        reference_segment_ids=tuple(
            dataset.segment_ids[index] for index in partitions.reference_indices
        ),
        # Reviewed binary labels aligned with those IDs and rows.
        reference_labels=tuple(int(label) for label in reference_labels_array), 
        # Column names in the same order as every stored feature vector.
        feature_names=dataset.feature_names,
    )
# ---


# __________________________________________
# CLASS-AWARE RETRIEVAL
# ==========================================


# This helper selects eligible neighbors within one class and attaches inspectable row evidence.
# --- _retrieve_class_cases()
def _retrieve_class_cases(
    *,
    estimator: Any | None,
    class_positions: tuple[int, ...],
    class_label: str,
    query_standardized_features: np.ndarray,
    query_segment_id: str,
    similarity_index: SimilarityIndex,
    config: AppConfig,
) -> tuple[SimilarCase, ...]:
    """Filter and rank the candidates retrieved from one reviewed class.

    The stable ordering applies to the candidates returned by `kneighbors`. It does not establish
    a global segment-ID order among every tied row outside that retrieved candidate set.

    Args:
        estimator: That class's fitted index, or `None` if the class is unavailable.
        class_positions: Map from estimator-local rows to the complete reference matrix.
        class_label: Reviewed class name carried into each returned case.
        query_standardized_features: One `(1, number of features)` row in the fitted scale.
        query_segment_id: Exact identity to exclude when the query is also a reference row.
        similarity_index: Shared reference vectors, segment IDs, and feature names.
        config: Maximum case count and optional distance cutoff.

    Returns:
        Eligible cases ordered by distance then segment ID, each with a one-based rank and its
        three largest feature differences. An unavailable class returns an empty tuple.
    """
    # __________________________________________
    # CANDIDATE RETRIEVAL
    # ==========================================
    # Query the available class index before applying identity and distance restrictions.
    # If the estimator is None or the class positions are empty, return an empty tuple.
    if estimator is None or not class_positions:
        return ()

    # Ask for one extra neighbor because the query may be in the reference set.
    # Removing its own segment ID keeps it from appearing as evidence for itself.   
    requested_count = min(config.neighbors_per_class + 1, len(class_positions))

    # Return the distances and local positions of the neighbors.
    distances, local_positions = estimator.kneighbors(
        query_standardized_features,
        n_neighbors=requested_count,
        return_distance=True,
    )

    # __________________________________________
    # ROW-ID MAPPING AND CANDIDATE FILTERING
    # ==========================================
    # Map index-local positions back to shared reference rows before checking eligibility.
    # List of eligible cases.
    eligible: list[tuple[float, str, int]] = []
    
    # Iterate through the distances and local positions of the neighbors.
    for distance, local_position in zip(distances[0], local_positions[0], strict=True):
        # Translate that position before looking up the segment ID or its complete standardized feature vector.
        reference_position = class_positions[int(local_position)]
        case_id = similarity_index.reference_segment_ids[reference_position]
        
        # Skip if the case_id is the same as the query_segment_id.
        if case_id == query_segment_id:
            continue
        # A configured cutoff can leave fewer than the requested number of cases.
        if config.similarity_cutoff is not None and distance > config.similarity_cutoff:
            continue
        eligible.append((float(distance), case_id, reference_position))

    # Resolve equal distances among retrieved candidates by the exact segment ID.
    eligible.sort(key=lambda item: (item[0], item[1]))

    # __________________________________________
    # FEATURE-GAP CONSTRUCTION
    # ==========================================
    # Attach standardized coordinate differences only to the retained, ranked comparisons.
    # List of returned cases.
    returned_cases: list[SimilarCase] = []

    # Query vector.
    query_vector = query_standardized_features[0]
    # Iterate through the eligible cases.
    for rank, (distance, case_id, reference_position) in enumerate(
        eligible[: config.neighbors_per_class],
        start=1,
    ):
        reference_vector = similarity_index.x_standardized_reference_features[reference_position]
        # For this pair, show where the standardized coordinates differ most.
        # These differences explain the comparison; they are not MLP feature importance.
        absolute_differences = np.abs(query_vector - reference_vector)
        # Sort the feature indices by the absolute differences in descending order.
        top_feature_indices = sorted(
            # Range of feature indices. 
            range(len(similarity_index.feature_names)),
            # Sort by the absolute differences in descending order.
            key=lambda index: (
                -float(absolute_differences[index]),
                similarity_index.feature_names[index],
            ),
        )[:3]    
        
        # List of feature differences.
        feature_differences = tuple(
            FeatureDifference(
                feature_name=similarity_index.feature_names[index],
                absolute_standardized_difference=float(absolute_differences[index]),
            )
            # Iterate through the top feature indices.
            for index in top_feature_indices
        )

        # Append the similar case to the list of returned cases.
        returned_cases.append(
            # Create a SimilarCase object with the feature differences.
            SimilarCase(
                case_id=case_id, # Case ID.
                reviewed_label=class_label, # Reviewed label.
                rank=rank, # Rank of the case.
                distance=distance, # Distance of the case.
                feature_differences=feature_differences, # Feature differences.
            ),
        )
    return tuple(returned_cases)
# ---


# ________________________________________________
# Combined historical support and conflict
# ------------------------------------------------
# Coordinate both class queries and relate their returned distances to the classifier decision.
# --- find_similar_cases()
def find_similar_cases(
    similarity_index: SimilarityIndex,
    trained_model: TrainedTelemetryModel,
    classification: ClassificationResult,
    x_raw_query_features: np.ndarray,
    *,
    config: AppConfig = DEFAULT_CONFIG,
) -> SimilarityResult:
    """Return normal/anomalous comparisons and their agreement with the classifier.

    Args:
        similarity_index: Reviewed reference rows and their fitted class indexes.
        trained_model: The model whose scaler was used to build those reference rows.
        classification: Selected segment ID, binary prediction, and uncertainty route.
        x_raw_query_features: One complete feature vector in the index's column order.
        config: Retrieval limits and the mean-distance ratio used to flag a conflict.

    Returns:
        Retrieved cases, the closer historical class if available, and any classifier conflict.

    Related Equation:
        `distance = ||x_standardized_query - x_standardized_reference||_2`

    Equation Relationship:
        This function coordinates the two class-aware indexes and compares their mean returned
        distances. The fitted estimators evaluate Euclidean distances with the default metric.

    Raises:
        ValueError: If the query does not have exactly one complete feature row.
    """
    # __________________________________________
    # PREPARE THE SHARED QUERY
    # ==========================================
    # Validate one feature row before transforming it for both reviewed-class comparisons.
    # Convert the query feature matrix to a numpy array.
    query_feature_matrix = np.asarray(x_raw_query_features, dtype=np.float64)

    # Reshape the query feature matrix if it is one-dimensional.
    if query_feature_matrix.ndim == 1:
        query_feature_matrix = query_feature_matrix.reshape(1, -1)

    # Raise a ValueError if the query feature matrix does not have one complete feature vector.
    if query_feature_matrix.shape != (1, len(similarity_index.feature_names)):
        raise ValueError("similarity query must contain one complete feature vector")

    # Reuse the fitted scale. Learning a new scale from this one query would make its
    # coordinates incompatible with the reference rows already stored in the indexes.
    query_standardized_features = trained_model.standardizer.transform(query_feature_matrix)

    # __________________________________________
    # RETRIEVE BOTH REVIEWED CLASSES
    # ==========================================
    # Keep class-specific results separate while applying the same query and retrieval settings.
    # Get normal cases.
    normal_cases = _retrieve_class_cases(
        estimator=similarity_index.normal_estimator,
        class_positions=similarity_index.normal_reference_positions,
        class_label="normal",
        query_standardized_features=query_standardized_features,
        query_segment_id=classification.segment_id,
        similarity_index=similarity_index,
        config=config,
    )
    # Get anomalous cases.
    anomalous_cases = _retrieve_class_cases(
        estimator=similarity_index.anomalous_estimator,
        class_positions=similarity_index.anomalous_reference_positions,
        class_label="anomalous",
        query_standardized_features=query_standardized_features,
        query_segment_id=classification.segment_id,
        similarity_index=similarity_index,
        config=config,
    )

    # __________________________________________
    # HISTORICAL EVIDENCE AGGREGATION
    # ==========================================
    # Compare the average distances of the cases actually returned from each class.
    # No returned cases means missing evidence, represented by None rather than zero.
    normal_mean = float(np.mean([case.distance for case in normal_cases])) if normal_cases else None
    anomalous_mean = (
        float(np.mean([case.distance for case in anomalous_cases])) if anomalous_cases else None
    )
    # A sole available class supplies the historical support. When both means exist,
    # the smaller mean wins; equal means follow the normal branch used by this program.
    
    # Get historical support.
    if normal_mean is None and anomalous_mean is None:
        historical_support = None
    
    # If only anomalous mean is available, return anomalous.
    elif anomalous_mean is None:
        historical_support = "normal"
    # If only normal mean is available, return normal.
    elif normal_mean is None:
        historical_support = "anomalous"
    # If both means are available, return the one with the smaller mean.
    elif normal_mean <= anomalous_mean:
        historical_support = "normal"
    else:
        historical_support = "anomalous"

    classifier_conflict = False
    conflict_reason = None
    # Conflict requires a definite classifier route and both historical class means.
    # With ratio 0.80, opposite_mean must be <= 0.80 * predicted_class_mean. For a
    # positive predicted-class mean, that is at least 20% closer on average.
    # An uncertain classification already calls for review without this test.
    
    # Check for classifier conflict.
    if classification.decision_state.value != "uncertain" and normal_mean is not None:
        # If anomalous mean is not None and classification.predicted_class is "normal", then set 
        # classifier conflict to anomalous mean <= normal mean * config.similarity_conflict_ratio.
        if anomalous_mean is not None and classification.predicted_class == "normal":
            classifier_conflict = anomalous_mean <= normal_mean * config.similarity_conflict_ratio
        # Else, if anomalous mean is not None and classification.predicted_class is "anomalous", then set 
        # classifier conflict to normal mean <= anomalous mean * config.similarity_conflict_ratio.
        elif anomalous_mean is not None and classification.predicted_class == "anomalous":
            classifier_conflict = normal_mean <= anomalous_mean * config.similarity_conflict_ratio
    
    # If classifier conflict, set conflict reason.
    if classifier_conflict:
        # Set conflict reason.
        conflict_reason = (
            f"classifier predicted {classification.predicted_class}, while the opposite historical "
            "class had a mean distance at least 20% smaller"
        )

    return SimilarityResult(
        normal_cases=normal_cases,
        anomalous_cases=anomalous_cases,
        historical_support=historical_support,
        classifier_conflict=classifier_conflict,
        conflict_reason=conflict_reason,
        metric=config.similarity_metric,
        neighbors_per_class=config.neighbors_per_class,
    )
# ---


# __________________________________________
# END OF FILE
# ==========================================
