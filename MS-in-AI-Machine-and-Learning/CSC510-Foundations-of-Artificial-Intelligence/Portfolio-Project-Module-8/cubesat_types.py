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
#
# Module Purpose:
# - Describe the records passed between data, model, reasoning, planning, and display code.
# - Keep expected errors and result states consistent across the program.
#
# Usage / Integration:
# - Imported by backend modules, the coordinator, presentation modules, and tests.
# - These definitions store values; they do not load data, fit models, or run an analysis.
#
# Contents Overview:
# - Controlled errors and decision/plan enumerations.
# - Dataset, fitted-model, classification, and historical-case records.
# - Facts, rules, explanation traces, simulated planning states, and complete results.
#
# Dependencies:
# - Standard Library: dataclasses, enum, pathlib, typing
# - Third-Party: numpy
# - Local Project: None
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Give the modules shared names for the data they exchange.

A validated dataset becomes explicit row partitions, then fitted model state. An analysis combines
a probability, historical cases, rule evidence, and a simulated plan into one result for display.
The records below keep those stages separate so a renderer can read a result without rerunning it.

Frozen dataclasses prevent field reassignment, not changes inside every contained object. The
data and model modules make retained NumPy arrays read-only separately. Planning states contain
hashable values so the search can recognize a state it has already visited.
"""

# __________________________________________
# IMPORTS
# ==========================================

from dataclasses import dataclass # Import dataclass for data storage.
from enum import Enum # Import Enum for enumerations.
from pathlib import Path # Import Path for path operations.
from typing import Any # Import Any for type hints.

# pyrefly: ignore [missing-import]
import numpy as np

# pyrefly: ignore [missing-import]
from numpy.typing import NDArray # Import NDArray for type hints.

# __________________________________________
# DOMAIN EXCEPTIONS
# ==========================================

# These expected failures share a base type so the CLI can show a controlled
# message. Programming errors outside this hierarchy are not silently converted.

# --- class CubeSatError
class CubeSatError(Exception):
    """Base class for controlled program errors shown without raw tracebacks."""
# --- end class CubeSatError


# --- class DatasetValidationError
class DatasetValidationError(CubeSatError):
    """Report a missing, unreadable, or incompatible telemetry dataset."""
# --- end class DatasetValidationError


# --- class ModelTrainingError
class ModelTrainingError(CubeSatError):
    """Report a controlled classifier fitting or probability failure."""
# --- end class ModelTrainingError


# --- class SegmentSelectionError
class SegmentSelectionError(CubeSatError):
    """Report a telemetry segment identifier or index that cannot be selected."""
# --- end class SegmentSelectionError


# --- class PlanningError
class PlanningError(CubeSatError):
    """Report an invalid action catalog or returned diagnostic transition."""
# --- end class PlanningError


# __________________________________________
# ENUMERATIONS
# ==========================================


# The classifier route and planning outcome have separate vocabularies so consumers can
# distinguish uncertainty in an estimate from the availability of a simulated plan.
# --- class DecisionState
class DecisionState(str, Enum):
    """Name the review route after applying the threshold's uncertainty band.

    An uncertain route still has a binary prediction in ClassificationResult. This extra
    state tells the reader the estimate is close enough to the threshold to need review.
    """

    NORMAL = "normal"
    ANOMALOUS = "anomalous"
    UNCERTAIN = "uncertain"
# --- end class DecisionState


# --- class PlanStatus
class PlanStatus(str, Enum):
    """Distinguish a found plan, a route needing no checks, and an unavailable plan.

    These values describe the search outcome, not whether any diagnostic action was performed.
    """

    FOUND = "found"
    NOT_REQUIRED = "not_required"
    UNAVAILABLE = "unavailable"
# --- end class PlanStatus


# __________________________________________
# DATA AND MODEL TRANSFER OBJECTS
# ==========================================


# ________________________________________________
# Artifact identity records
# ------------------------------------------------
# File measurements retain the evidence used to check the selected source artifact.
# --- class ArtifactVerification
@dataclass(frozen=True, slots=True)
class ArtifactVerification:
    """Store the measured identity of one local file for comparison with expected values.

    Attributes:
        path: File whose bytes were read by the data verification helper.
        size_bytes: Observed file length before comparison with the pinned artifact size.
        md5: Digest compared with the published dataset checksum.
        sha256: Additional digest used to identify the exact local content.
    """

    path: Path
    size_bytes: int
    md5: str
    sha256: str
# --- end class ArtifactVerification


# --- class SegmentsVerification
@dataclass(frozen=True, slots=True)
class SegmentsVerification:
    """Record the raw-reading file's profile after its metadata checks.

    Attributes:
        artifact: Observed identity of the raw `segments.csv` file.
        row_count: Individual reading rows; several can belong to the same segment.
        segment_count: Unique segment identifiers represented by those readings.
        channel_count: Unique source channels in the raw file.
        label_values: Distinct nonblank raw labels observed during verification.
    """

    artifact: ArtifactVerification
    row_count: int
    segment_count: int
    channel_count: int
    label_values: tuple[str, ...]
# --- end class SegmentsVerification


# ________________________________________________
# Dataset and row-role ownership
# ------------------------------------------------
# The table owns aligned row data; partition records select those rows for each workflow role.
# --- class TelemetryDataset
@dataclass(frozen=True, slots=True)
class TelemetryDataset:
    """Store one validated telemetry table in source row order.

    Row position connects every array and tuple: features at row i belong to segment_ids[i]
    and y_anomaly_labels[i]. Keeping that alignment is necessary for both training and display.

    Attributes:
        source_path: CSV file used for this run.
        profile_name: `authentic` or `fixture` validation profile.
        segment_ids: Stable identifiers for each row.
        channels: OPS-SAT-AD channel identifier for each row.
        sampling_values: Dataset sampling metadata for each row.
        y_anomaly_labels: Reviewed binary labels, never used as inference inputs.
        benchmark_training_flags: Official benchmark train/test indicator.
        x_validated_telemetry_features: Finite matrix `(m, 18)`, where m is the segment count.
        feature_names: Feature order shared by every numerical component.
        simulated: Whether fixture validation was selected; exact artifact identity is separate.
    """

    source_path: Path
    profile_name: str
    segment_ids: tuple[str, ...]
    channels: tuple[str, ...]
    sampling_values: tuple[str, ...]
    y_anomaly_labels: NDArray[np.int64]
    benchmark_training_flags: NDArray[np.bool_]
    x_validated_telemetry_features: NDArray[np.float64]
    feature_names: tuple[str, ...]
    simulated: bool
# --- end class TelemetryDataset


# --- class DatasetPartitions
@dataclass(frozen=True, slots=True)
class DatasetPartitions:
    """Identify each row's role without making a second copy of the dataset.

    The reference set intentionally includes both training and validation rows. It is a
    retrieval role, not a fourth disjoint learning split; it excludes the held-out test rows.

    Attributes:
        dataset: Validated table that owns the rows addressed by these indices.
        training_indices: Zero-based rows used to fit the scaler and classifier.
        validation_indices: Separate official-training rows used to choose the threshold.
        test_indices: Official held-out rows used for evaluation and frontend screening.
        reference_indices: All official-training rows available as reviewed historical cases.

    """

    dataset: TelemetryDataset
    training_indices: tuple[int, ...]
    validation_indices: tuple[int, ...]
    test_indices: tuple[int, ...]
    reference_indices: tuple[int, ...]
# --- end class DatasetPartitions


# ________________________________________________
# Fitted model and evaluation state
# ------------------------------------------------
# Training returns reusable estimator state together with the metrics measured for that fit.
# --- class EvaluationMetrics
@dataclass(frozen=True, slots=True)
class EvaluationMetrics:
    """Keep the measured test results beside the threshold used to produce them.

    The model module supplies these values. Storing them does not establish operational
    spacecraft performance, and fixture metrics describe simulated examples only.

    Attributes:
        precision: Share of predicted anomalies whose reviewed label is anomalous.
        recall: Share of reviewed anomalies that the classifier detects.
        f1_score: Harmonic mean balancing precision and recall.
        accuracy: Share of all test rows classified correctly, including normal rows.
        confusion_matrix: Counts `((true normal, false alarm), (missed, detected anomaly))`.
        classification_threshold: Cutoff chosen using validation rows before test evaluation.
        training_iterations: Actual number of optimizer iterations performed by the estimator.
        test_sample_count: Number of held-out rows behind these metrics.

    """

    precision: float
    recall: float
    f1_score: float
    accuracy: float
    confusion_matrix: tuple[tuple[int, int], tuple[int, int]]
    classification_threshold: float
    training_iterations: int
    test_sample_count: int
# --- end class EvaluationMetrics


# --- class TrainedTelemetryModel
@dataclass(frozen=True, slots=True)
class TrainedTelemetryModel:
    """Keep fitted objects and the arrays needed for repeated analysis together.

    Each feature matrix has one row per member of its role and 18 columns. The normal-only
    means/stds have shape `(18,)` and support deviation facts. They are separate from the
    scaler's statistics, which use both classes in the model-training partition.

    Attributes:
        estimator: Fitted multilayer perceptron (MLP) used to estimate anomaly probabilities.
        standardizer: Scaler fitted on model-training rows and reused for other row roles.
        classification_threshold: Validation-selected cutoff for a binary prediction.
        uncertainty_margin: Probability distance around that cutoff assigned to review.
        evaluation: Metrics calculated on the official held-out test rows.
        x_standardized_training_features: Model-training rows on the fitted scale.
        x_standardized_validation_features: Threshold-validation rows on the same scale.
        x_standardized_test_features: Held-out rows transformed without fitting another scaler.
        x_standardized_reference_features: Historical rows in reference_indices order.
        reference_indices: Original dataset row indices behind the historical feature matrix.
        mu_training_normal_feature_means: Per-feature means of raw normal model-training rows.
        sigma_training_normal_feature_stds: Their standard deviations, with zero values guarded.
        feature_names: Ordered names of the 18 columns in every retained feature matrix.
        random_seed: Seed used when the model and its row split were built.

    """

    estimator: Any
    standardizer: Any
    classification_threshold: float
    uncertainty_margin: float
    evaluation: EvaluationMetrics
    x_standardized_training_features: NDArray[np.float64]
    x_standardized_validation_features: NDArray[np.float64]
    x_standardized_test_features: NDArray[np.float64]
    x_standardized_reference_features: NDArray[np.float64]
    reference_indices: tuple[int, ...]
    mu_training_normal_feature_means: NDArray[np.float64]
    sigma_training_normal_feature_stds: NDArray[np.float64]
    feature_names: tuple[str, ...]
    random_seed: int
# --- end class TrainedTelemetryModel


# __________________________________________
# CLASSIFICATION TRANSFER OBJECTS
# ==========================================


# This record carries the model decision into historical comparison, reasoning, and display.
# --- class ClassificationResult
@dataclass(frozen=True, slots=True)
class ClassificationResult:
    """Keep a model estimate separate from its binary prediction and review route.

    Attributes:
        segment_id: Exact dataset identity of the analyzed row.
        anomaly_probability: MLP estimate for class 1, within zero and one.
        predicted_class: `anomalous` at or above the threshold; otherwise `normal`.
        decision_state: Normal/anomalous route, or uncertain inside the inclusive margin.
        classification_threshold: Cutoff selected from validation examples.
        uncertainty_margin: Distance from the cutoff that calls for uncertain review.
        reference_label: Optional reviewed label for comparison, never a prediction input.
        reference_partition: Role of this row in the existing dataset split.
        probability_source: Text identifying the kind of estimate being displayed.
    """

    segment_id: str
    anomaly_probability: float
    predicted_class: str
    decision_state: DecisionState
    classification_threshold: float
    uncertainty_margin: float
    reference_label: str | None
    reference_partition: str
    probability_source: str = "MLP estimate"
# --- end class ClassificationResult


# __________________________________________
# SIMILARITY TRANSFER OBJECTS
# ==========================================


# Individual coordinate gaps and ranked cases form the evidence summarized in SimilarityResult.
# --- class FeatureDifference
@dataclass(frozen=True, slots=True)
class FeatureDifference:
    """Pair a feature name with its absolute query-to-case difference on the fitted scale.

    This measures how two examples differ in one coordinate. It does not measure how much
    that feature influenced the classifier's prediction.
    """

    feature_name: str
    absolute_standardized_difference: float
# --- end class FeatureDifference


# --- class SimilarCase
@dataclass(frozen=True, slots=True)
class SimilarCase:
    """Describe one historical comparison from a reviewed class.

    Attributes:
        case_id: Original segment identifier, not a position inside the neighbor index.
        reviewed_label: Existing class used to group historical cases for retrieval.
        rank: One-based position within this class's returned cases.
        distance: Configured distance between standardized rows, Euclidean by default.
        feature_differences: Largest coordinate differences selected by the similarity module.
    """

    case_id: str
    reviewed_label: str
    rank: int
    distance: float
    feature_differences: tuple[FeatureDifference, ...]
# --- end class SimilarCase


# --- class SimilarityResult
@dataclass(frozen=True, slots=True)
class SimilarityResult:
    """Keep both reviewed classes visible when comparing a prediction with history.

    Historical support describes geometric similarity. It is not a second calibrated
    probability, and an absent conflict flag does not prove that the classifier is correct.

    Attributes:
        normal_cases: Returned cases from the reviewed normal reference rows.
        anomalous_cases: Returned cases from the reviewed anomalous reference rows.
        historical_support: Class favored by mean returned distance, or `None` without cases.
        classifier_conflict: Whether available opposite-class distances meet the conflict rule.
        conflict_reason: Explanation of a detected conflict, or `None` when none was flagged.
        metric: Name of the distance calculation used by the fitted indexes.
        neighbors_per_class: Configured maximum; a returned group may contain fewer cases.

    """

    normal_cases: tuple[SimilarCase, ...]
    anomalous_cases: tuple[SimilarCase, ...]
    historical_support: str | None
    classifier_conflict: bool
    conflict_reason: str | None
    metric: str
    neighbors_per_class: int
# --- end class SimilarityResult


# __________________________________________
# LOGIC TRANSFER OBJECTS
# ==========================================


# These records connect rule patterns, their matched evidence, and selected-segment conclusions.
# --- class Fact
@dataclass(frozen=True, order=True, slots=True)
class Fact:
    """Represent a named relationship and its ordered arguments.

    For example, a predicate can describe a segment's channel. Concrete segment/channel
    names are constants; terms beginning with `?` are variables when used in rule patterns.
    This record stores the expression. Matching and inference belong to cubesat_logic.
    """

    predicate: str
    terms: tuple[str, ...]

    # --- __str__()
    def __str__(self) -> str:
        """Return stable first-order-logic-style display notation."""
        return f"{self.predicate}({', '.join(self.terms)})"
    # ---
# --- end class Fact


# --- class HornRule
@dataclass(frozen=True, slots=True)
class HornRule:
    """Describe an if-all-premises-match rule with one positive conclusion.

    Attributes:
        rule_id: Stable name used to identify a rule in the explanation trace.
        premises: Fact patterns that must match with compatible variable assignments.
        conclusion: Pattern filled with those assignments when every premise matches.
        explanation: Human-readable reason retained with the derived conclusion.
        source_status: Provenance of the rule, including simulated teaching assumptions.
    """

    rule_id: str
    premises: tuple[Fact, ...]
    conclusion: Fact
    explanation: str
    source_status: str
# --- end class HornRule


# --- class InferenceTrace
@dataclass(frozen=True, slots=True)
class InferenceTrace:
    """Keep the evidence for a Horn-rule application or consistency check.

    Attributes:
        rule_id: Rule or consistency-check identifier that produced this conclusion.
        matched_premises: Concrete facts supporting the rule match or detected contradiction.
        bindings: Variable/value pairs connecting the evidence to a segment or channel.
        conclusion: New fact produced by a rule substitution or a consistency check.
        explanation: Reason for the derivation, retained for the reader.
        source_status: Provenance of the rule or consistency policy, not a new measurement.
    """

    rule_id: str
    matched_premises: tuple[Fact, ...]
    bindings: tuple[tuple[str, str], ...]
    conclusion: Fact
    explanation: str
    source_status: str
# --- end class InferenceTrace


# --- class ReasoningResult
@dataclass(frozen=True, slots=True)
class ReasoningResult:
    """Separate starting evidence from conclusions reached by forward chaining.

    Attributes:
        asserted_facts: Initial facts built from numerical results and configured knowledge.
        derived_facts: New facts added by rule applications or consistency checks.
        all_facts: Combined facts available when inference stops.
        traces: Recorded derivations explaining the newly added facts.
        suspected_faults: Selected-segment hypotheses to investigate, not confirmed faults.
        required_checks: Check names requested by rules for the selected segment.
        manual_review_reasons: Reasons to return the evidence to a human for interpretation.
        existential_critical_deviation: Whether a matching critical/deviating channel exists.
    """

    asserted_facts: tuple[Fact, ...]
    derived_facts: tuple[Fact, ...]
    all_facts: tuple[Fact, ...]
    traces: tuple[InferenceTrace, ...]
    suspected_faults: tuple[str, ...]
    required_checks: tuple[str, ...]
    manual_review_reasons: tuple[str, ...]
    existential_critical_deviation: bool
# --- end class ReasoningResult


# __________________________________________
# PLANNING TRANSFER OBJECTS
# ==========================================


# Catalog actions, search states, and selected steps describe proposed simulated reviews.
# PlanResult retains the outcome for consumers without executing those reviews.
# --- class DiagnosticAction
@dataclass(frozen=True, slots=True)
class DiagnosticAction:
    """Define a possible check in the simulated planning problem.

    Attributes:
        action_id: Unique catalog identifier used for selection and traceability.
        description: Human-readable proposed check.
        preconditions: Completed-check names required before this action is eligible.
        effects: Completed-check names added to the simulated state after the action.
        cost: Nonnegative teaching cost used by search, not measured time or money.
        cost_meaning: Explanation of what that simulated cost represents.
        category: Kind of review represented by the action.
        source_status: Provenance label retained when the plan is displayed.
    """

    action_id: str
    description: str
    preconditions: frozenset[str]
    effects: frozenset[str]
    cost: float
    cost_meaning: str
    category: str
    source_status: str = "simulated"
# --- end class DiagnosticAction


# --- class PlanningState
@dataclass(frozen=True, slots=True)
class PlanningState:
    """Describe one search node using values that can be compared and hashed.

    A transition creates another state with additional completed checks. Using frozenset
    makes order irrelevant, so search can recognize the same completed set reached twice.

    Attributes:
        route: Classification route, overridden by manual review when reasoning requests it.
        triggered_requirements: Evidence/reasoning conditions that motivated the plan.
        required_checks: Check effects that must all be present to satisfy the goal.
        completed_checks: Effects already reached along this simulated path.
        suspected_faults: Advisory hypotheses retained from the reasoning result.

    """

    route: str
    triggered_requirements: frozenset[str]
    required_checks: frozenset[str]
    completed_checks: frozenset[str]
    suspected_faults: frozenset[str]
# --- end class PlanningState


# --- class PlannedAction
@dataclass(frozen=True, slots=True)
class PlannedAction:
    """Pair a selected action with the path cost through that action.

    cumulative_cost includes this action and every preceding action in the selected path.
    The action's own cost remains available separately in action.cost.
    """

    action: DiagnosticAction
    cumulative_cost: float
# --- end class PlannedAction


# --- class PlanResult
@dataclass(frozen=True, slots=True)
class PlanResult:
    """Store the outcome and replay evidence from the simulated A* search.

    Found action sequences are replayed to check their prerequisites and recorded costs.
    Empty sequences in early outcomes carry a valid transition flag without replay. Read
    status and goal_satisfied as well: legal transitions alone do not establish a complete plan.

    Attributes:
        status: Found, not required, or unavailable planning outcome.
        ordered_actions: Selected action sequence with cumulative costs.
        total_cost: Sum of costs on the returned path.
        goal_condition: Readable description of the checks needed for this result.
        initial_state: Requirements and completed checks before search.
        final_state: State reached by the returned actions, or unchanged on an early outcome.
        expanded_node_count: Search nodes expanded, not the number of planned actions.
        transitions_valid: Recorded transition check, also true for empty early-outcome sequences.
        goal_satisfied: Whether final completed checks include every required check.
        message: Explanation of the outcome for the person reviewing the result.

    """

    status: PlanStatus
    ordered_actions: tuple[PlannedAction, ...]
    total_cost: float
    goal_condition: str
    initial_state: PlanningState
    final_state: PlanningState
    expanded_node_count: int
    transitions_valid: bool
    goal_satisfied: bool
    message: str
# --- end class PlanResult


# __________________________________________
# COMPLETE RESULT AND VERIFICATION TYPES
# ==========================================


# The coordinator joins the backend producers here so console and frontend consumers receive
# one coherent segment result without repeating inference, reasoning, or search.
# --- class CompleteAnalysisResult
@dataclass(frozen=True, slots=True)
class CompleteAnalysisResult:
    """Keep one segment's complete result together for console and frontend readers.

    Attributes:
        segment_id: Shared identity of the row described by all component results.
        selected_channel: Source channel identifier associated with that segment.
        dataset_profile: Validation profile used to load this analysis's source.
        simulated_source: Whether the data was loaded with the simulated fixture profile.
        classification: Probability, prediction, and uncertainty interpretation.
        similarity: Reviewed historical comparisons and any detected disagreement.
        top_deviating_features: Names ranked by absolute normal-training z-score deviation.
        reasoning: Starting facts, derived conclusions, and their explanation traces.
        plan: Simulated check sequence and its validation outcome.
    """

    segment_id: str
    selected_channel: str
    dataset_profile: str
    simulated_source: bool
    classification: ClassificationResult
    similarity: SimilarityResult
    top_deviating_features: tuple[str, ...]
    reasoning: ReasoningResult
    plan: PlanResult
# --- end class CompleteAnalysisResult


# --- class VerificationCheck
@dataclass(frozen=True, slots=True)
class VerificationCheck:
    """Record one check's identity, outcome, and observed evidence.

    Attributes:
        check_id: Stable identifier that connects the result to its verification function.
        status: Reported pass/fail state for this individual check.
        level: Whether the check inspected source structure or exercised runtime behavior.
        evidence: Description of what was actually observed, including failure details.
    """

    check_id: str
    status: str
    level: str
    evidence: str
# --- end class VerificationCheck


# __________________________________________
# END OF FILE
# ==========================================
