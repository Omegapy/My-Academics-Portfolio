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
# - Turn fitted backend results into screening records, tables, and chart values.
# - Keep reusable model resources separate from each user's page selections.
#
# Usage / Integration:
# - Imported by streamlit_app.py, both app_pages scripts, and frontend tests.
# - Reuses cubesat_telemetry_ai and backend helpers for numerical and rule results.
#
# Contents Overview:
# - Source, cache, screening, and walkthrough transfer objects.
# - Local artifact identity and bounded fitted-state caching.
# - Ranked screening, channel summaries, selected evidence, and teaching tables.
#
# Dependencies:
# - Standard Library: hashlib, json, dataclasses, pathlib
# - Third-Party: pandas, plotly, streamlit
# - Local Project: cubesat_config, cubesat_data, cubesat_model, cubesat_planner,
#   cubesat_telemetry_ai, cubesat_types
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Adapt fitted CubeSat telemetry evidence for the local Streamlit interface.

A segment row summarizes telemetry readings with 18 numerical features. The pages
use this module to screen held-out segments, prepare readable tables, and inspect one
selected result. The multilayer perceptron (MLP), historical search, logic, and planner
remain in the backend modules.

The resource cache reuses a fitted assistant for the same data and configuration.
Filters and selected IDs belong to the pages, so changing the view does not change the
model. Helpers reshape stored evidence, derive display summaries such as channel rates,
or call an existing backend calculation. They do not fit a second model for the interface.
"""

# __________________________________________
# IMPORTS
# ==========================================

import hashlib # Fingerprint normalized configuration bytes for cache identity.
import json # Encode normalized configuration fields with stable JSON formatting.
from dataclasses import dataclass, fields # Transfer records and configuration fields.
from pathlib import Path # Resolve configured local artifact paths.

import pandas as pd # Build readable tables from backend records.

# pyrefly: ignore [missing-import]
import plotly.graph_objects as go # Format channel counts as interactive bars.

# pyrefly: ignore [missing-import]
import streamlit as st # Cache fitted resources shared by the pages.

# Share the backend schema, source identity, and fitting settings with presentation.
from cubesat_config import (
    AUTHENTIC_ROW_COUNT, # Pinned authentic segment-feature count.
    AUTHENTIC_SEGMENTS_ROW_COUNT, # Pinned authentic raw-reading count.
    AUTHENTIC_TEST_ROW_COUNT, # Pinned authentic held-out segment count.
    AUTHENTIC_TRAINING_ROW_COUNT, # Pinned authentic official-training-role count.
    DATASET_SHA256, # Expected feature-table byte fingerprint.
    DATASET_SIZE_BYTES, # Expected feature-table byte count.
    DEFAULT_CONFIG, # Shared application settings.
    FEATURE_NAMES, # Ordered model-input schema.
    SEGMENTS_SHA256, # Expected raw-reading byte fingerprint.
    SEGMENTS_SIZE_BYTES, # Expected raw-reading byte count.
    ZENODO_RECORD_URL, # Official source-record link.
    AppConfig, # Configuration fields included in cache identity.
)
from cubesat_data import (
    calculate_artifact_verification, # Read local artifact bytes for their fingerprint and size.
    load_demo_scenarios, # Read names and purposes for fixture examples.
    select_segment_index, # Resolve exact IDs through the backend dataset.
)
from cubesat_model import (
    classify_probability, # Reuse the backend threshold decision.
    predict_anomaly_probability, # Infer with the existing fitted MLP.
    standardize_features, # Reuse the fitted feature scaler.
)
from cubesat_planner import (
    build_diagnostic_actions, # Read the simulated planning catalog for teaching tables.
    estimate_remaining_cost, # Reuse the planner heuristic for the selected path.
)
from cubesat_telemetry_ai import (
    TelemetryAssistant, # Own the fitted backend and complete analysis workflow.
    build_assistant, # Validate, partition, and fit one backend resource.
)
from cubesat_types import (
    CompleteAnalysisResult, # Carry all evidence for one selected segment.
    CubeSatError, # Expose controlled backend and frontend failures.
    DecisionState, # Identify the three backend screening routes.
    EvaluationMetrics, # Carry stored held-out evaluation counts.
    PlanningState, # Describe a simulated planning candidate.
    SimilarCase, # Carry one reviewed historical neighbor.
)

# __________________________________________
# PRESENTATION CONSTANTS
# ==========================================
# Source labels, screening routes, and preparation links give both pages one vocabulary.
# These values describe presentation choices; backend profiles enforce the data contract.

AUTHENTIC_PROFILE_LABEL: str = "Authentic OPS-SAT-AD v2"
FIXTURE_PROFILE_LABEL: str = "Deterministic demo fixture"
PROFILE_OPTIONS: tuple[str, str] = (AUTHENTIC_PROFILE_LABEL, FIXTURE_PROFILE_LABEL)
# Shared profile labels identify the configured local data choices.

FLAGGED_STATUS: str = "Flagged anomaly"
UNCERTAIN_STATUS: str = "Uncertain review"
NORMAL_STATUS: str = "Likely normal"

# These labels name mutually exclusive model screening routes.
STATUS_OPTIONS: tuple[str, str, str] = (
    FLAGGED_STATUS,
    UNCERTAIN_STATUS,
    NORMAL_STATUS,
)

# Preparation link for the model-input feature table.
DATASET_DOWNLOAD_URL: str = (
    "https://zenodo.org/api/records/15108715/files/dataset.csv/content"
)

# Preparation link for raw readings used by the standalone verifier.
SEGMENTS_DOWNLOAD_URL: str = (
    "https://zenodo.org/api/records/15108715/files/segments.csv/content"
)

# Source citation shared by the frontend pages.
OFFICIAL_RECORD_URL: str = ZENODO_RECORD_URL

# Stage order follows the explanation of data, inference, evidence, and planning.
WALKTHROUGH_STAGES: tuple[str, ...] = (
    "Data source and roles",
    "MLP probability",
    "Threshold and evaluation",
    "Similarity search",
    "Logic rules",
    "A-star planning",
    "Architecture map",
)

# Fixed presentation schema shared by ranking, filtering, and selected-row controls.
SCREENING_COLUMNS: tuple[str, ...] = (
    "segment_id",
    "channel",
    "anomaly_probability",
    "predicted_class",
    "decision_state",
    "status",
    "classification_threshold",
    "uncertainty_margin",
    "partition",
)


# __________________________________________
# FRONTEND TRANSFER OBJECTS
# ==========================================
# These records carry source identity, fitted resources, and evidence between the pages.
# Each record keeps its own role explicit so a display count is not mistaken for model state.


# --- class FrontendValidationError
class FrontendValidationError(CubeSatError):
    """Identify invalid frontend-only state without hiding unexpected defects."""


# --- end class FrontendValidationError


# --- class SourceDefinition
@dataclass(frozen=True, slots=True)
class SourceDefinition:
    """Describe the local file and provenance attached to one data-profile choice.

    The object records a configured source. File hashing and dataset validation happen
    when that source is loaded, so constructing this record does not verify its bytes.

    Attributes:
        profile_label: Readable label used by the shared Streamlit selector.
        profile_name: Backend profile key, either authentic or fixture.
        dataset_path: Local segment-feature CSV to load for this choice.
        provenance: Source description displayed beside the active profile.
        simulated: Whether this source choice uses the simulated fixture profile.
    """

    profile_label: str
    profile_name: str
    dataset_path: Path
    provenance: str
    simulated: bool


# --- end class SourceDefinition


# --- class FrontendCacheIdentity
@dataclass(frozen=True, slots=True)
class FrontendCacheIdentity:
    """Identify the data and settings used to build one fitted assistant.

    A SHA-256 digest is a fingerprint of bytes. Including the artifact and configuration
    digests prevents a filename alone from standing for several different model inputs.
    Filters are absent because they change the view after fitting.

    Attributes:
        dataset_path: Resolved local path used to load the feature table.
        artifact_sha256: Fingerprint of the dataset bytes at identity construction.
        artifact_size_bytes: Byte count from the same file read.
        profile_name: Data-validation profile used by the backend.
        random_seed: Seed selected for repeatable partitioning and model fitting.
        config_sha256: Fingerprint of every field in the current AppConfig.
    """

    dataset_path: str
    artifact_sha256: str
    artifact_size_bytes: int
    profile_name: str
    random_seed: int
    config_sha256: str


# --- end class FrontendCacheIdentity


# --- class ScreeningRecord
@dataclass(frozen=True, slots=True)
class ScreeningRecord:
    """Store one held-out segment's model decision before detailed analysis.

    The record deliberately omits the segment's reviewed label. It reports what the
    fitted model predicted, while reviewed classes remain available for later evaluation.

    Attributes:
        segment_id: Stable source identifier used to reconnect a table row to its data.
        channel: Coded telemetry source used to group segments, not a subsystem name.
        anomaly_probability: MLP estimate on the 0-to-1 scale.
        predicted_class: Binary normal or anomalous class chosen at the threshold.
        decision_state: Backend route that also allows a near-threshold uncertain result.
        status: Readable label for that three-way screening route.
        classification_threshold: Operating cutoff already chosen from validation rows.
        uncertainty_margin: Distance on either side of the cutoff reserved for review.
        partition: Row-role description; screening construction uses held-out test rows.
    """

    segment_id: str
    channel: str
    anomaly_probability: float
    predicted_class: str
    decision_state: str
    status: str
    classification_threshold: float
    uncertainty_margin: float
    partition: str


# --- end class ScreeningRecord


# --- class ScreeningSummary
@dataclass(frozen=True, slots=True)
class ScreeningSummary:
    """Store counts for the population represented by one screening frame.

    The flagged, uncertain, and likely-normal counts must add up to screened. These are
    model-decision counts; they do not count reviewed anomalies or physical fault events.
    The same record can summarize the whole held-out set or just one channel.
    """

    screened: int
    flagged: int
    uncertain: int
    likely_normal: int


# --- end class ScreeningSummary


# --- class FrontendState
@dataclass(frozen=True, slots=True)
class FrontendState:
    """Bundle a reusable fitted assistant with its screening snapshot.

    Frozen fields prevent rebinding this record's attributes. The assistant still owns
    nested model objects, so this record should not be read as a deep immutability promise.
    Pages reuse those fitted objects and keep their own selection state elsewhere.

    Attributes:
        identity: Artifact and configuration identity under which the resource was built.
        source: Profile path and provenance associated with the resource.
        assistant: Backend dataset, partitions, model, and historical-search state.
        screening_records: Tuple of per-segment predictions built from held-out rows.
    """

    identity: FrontendCacheIdentity
    source: SourceDefinition
    assistant: TelemetryAssistant
    screening_records: tuple[ScreeningRecord, ...]


# --- end class FrontendState


# --- class DatasetContext
@dataclass(frozen=True, slots=True)
class DatasetContext:
    """Describe data scale and row roles for the active fitted profile.

    The official training-role population is split into model-training and threshold-
    validation rows. Held-out test rows are a separate group. These counts describe data
    roles, not how many anomalies the classifier found.

    Attributes:
        profile_label: Current source choice displayed by both pages.
        simulated: Whether these counts describe data loaded under the fixture profile.
        total_segments: Number of segment-feature rows loaded by the backend.
        official_training_segments: Reference population before the model/threshold split.
        model_training_segments: Rows used to fit the feature scaler and MLP.
        threshold_validation_segments: Separate rows used to choose the score cutoff.
        held_out_segments: Rows reserved from fitting and threshold selection.
        feature_count: Number of numerical inputs in each segment row.
        channel_codes: Sorted distinct source codes in the loaded dataset.
        raw_reading_count: Pinned authentic raw-file count, or None for the fixture.
    """

    profile_label: str
    simulated: bool
    total_segments: int
    official_training_segments: int
    model_training_segments: int
    threshold_validation_segments: int
    held_out_segments: int
    feature_count: int
    channel_codes: tuple[str, ...]
    raw_reading_count: int | None


# --- end class DatasetContext


# --- class DataArtifactContext
@dataclass(frozen=True, slots=True)
class DataArtifactContext:
    """Describe an official file and its role in local preparation.

    These records supply links and expected identity values to the walkthrough. Creating
    a record does not download the file or check whether it exists locally.

    Attributes:
        filename: Official name of the published CSV artifact.
        official_url: Source link opened only if the user follows it.
        local_path: Project destination shown in the preparation guidance.
        expected_size_bytes: Pinned byte count for the authentic artifact.
        expected_sha256: Pinned SHA-256 fingerprint used to identify exact bytes.
        role: Explanation of feature input versus raw-reading verification use.
    """

    filename: str
    official_url: str
    local_path: str
    expected_size_bytes: int
    expected_sha256: str
    role: str


# --- end class DataArtifactContext


# --- class ThresholdContext
@dataclass(frozen=True, slots=True)
class ThresholdContext:
    """Expose the selected segment's probability and review-band values.

    All values use the probability scale before Streamlit formats them as percentages.
    The lower and upper bounds are the stored threshold minus and plus the margin. The
    status comes from the backend decision; this record does not choose a new threshold.

    Attributes:
        segment_id: Exact segment whose complete result supplied the classification.
        probability: Fitted MLP anomaly estimate for that segment.
        threshold: Cutoff chosen from the model's validation rows.
        uncertainty_margin: Plus-or-minus distance around that cutoff.
        lower_bound: Lower edge of the uncertainty band.
        upper_bound: Upper edge of the uncertainty band.
        status: Readable name for the already calculated decision route.
    """

    segment_id: str
    probability: float
    threshold: float
    uncertainty_margin: float
    lower_bound: float
    upper_bound: float
    status: str


# --- end class ThresholdContext


# --- class WalkthroughExampleContext
@dataclass(frozen=True, slots=True)
class WalkthroughExampleContext:
    """Connect one walkthrough example to its source and scenario meaning.

    The segment and channel identify the current data row. A fixture scenario names an
    intended demonstration route, such as an uncertain result, without supplying a model
    score or diagnosing a spacecraft fault. Authentic rows use a general example label.

    Attributes:
        profile_label: Active data source shown beside the example.
        segment_id: Selected record identifier used throughout the walkthrough.
        channel: Source channel associated with that exact record.
        scenario_name: Matching fixture scenario name or a general example label.
        scenario_purpose: Description of what the selected example is intended to show.
    """

    profile_label: str
    segment_id: str
    channel: str
    scenario_name: str
    scenario_purpose: str


# --- end class WalkthroughExampleContext


# --- class TermDefinition
@dataclass(frozen=True, slots=True)
class TermDefinition:
    """Pair one learner-facing term with its meaning in this application."""

    term: str
    definition: str


# --- end class TermDefinition

# ________________________________________________
# Learner vocabulary and feature meanings
# ------------------------------------------------
# Shared definitions connect page terminology to the source fields used by the model.
# The glossary records feature meanings; the backend owns feature validation and computation.


# -----------------------------------------------------------------------------
# --- Learner terms. ---------------------------------------------------------
# -----------------------------------------------------------------------------
LEARNER_TERMS: tuple[TermDefinition, ...] = (
    # Learner-facing terms used by this application. All entries should be
    # short and mapped to single-sentence explanations.

    # Telemetry is the measured signal collected from the CubeSat.  
    TermDefinition(
        "Telemetry",
        "Measurements recorded by a spacecraft system over time.",
    ),
    
    # Dataset definitions establish the local CSV input used throughout the walkthrough.
    TermDefinition(
        "Dataset",
        (
            "An organized collection of records; this project reads local comma-separated "
            "value (CSV) files."
        ),
    ),
    
    # Segment is one time-window summary and the unit screened by the model. 
    TermDefinition(
        "Segment",
        "One time-window summary and the unit screened by the model.",
    ),
    
    # Channel is a coded source identifier supplied by OPS-SAT-AD, not a subsystem name here. 
    TermDefinition(
        "Channel",
        "A coded source identifier supplied by OPS-SAT-AD, not a subsystem name here.",
    ),
    
    # Numerical feature is one measured summary value used as an input to the model. 
    TermDefinition(
        "Numerical feature",
        "One measured summary value used as an input to the model.",
    ),
    
    # Reviewed label is the historical normal or anomalous class recorded for evaluation and examples. 
    TermDefinition(
        "Reviewed label",
        "The historical normal or anomalous class recorded for evaluation and examples.",
    ),
    
    # Anomaly probability is the neural network's 0-to-1 estimate for one segment, not certainty. 
    TermDefinition(
        "Anomaly probability",
        "The neural network's 0-to-1 estimate for one segment, not certainty.",
    ),
    
    # Threshold is the validation-selected probability boundary used for a binary prediction. 
    TermDefinition(
        "Threshold",
        "The validation-selected probability boundary used for a binary prediction.",
    ),
    
    # The uncertainty band explains why near-threshold predictions require human review.
    TermDefinition(
        "Uncertainty band",
        "The plus-or-minus margin around the threshold that routes close values to review.",
    ),
    
    # AI screening status distinguishes the three mutually exclusive review routes.
    TermDefinition(
        "AI screening status",
        "The mutually exclusive flagged, uncertain, or likely-normal result for one segment.",
    ),
)

# Source names and calculations follow the official OPS-SAT-AD paper and generator notebook.
# The wording describes statistical properties without assigning a spacecraft cause.
FEATURE_GLOSSARY: tuple[tuple[str, str, str, str], ...] = (
    # Source names and calculations follow the official OPS-SAT-AD paper and
    # generator notebook. The wording describes statistical properties without assigning
    # a spacecraft cause.
    
    # Elapsed duration: Seconds from the first timestamp to the last timestamp in the segment.
    (
        "duration",
        "Elapsed duration",
        "Seconds from the first timestamp to the last timestamp in the segment.",
        "Time and size",
    ),
    
    # Number of telemetry readings in the segment.
    (
        "len",
        "Reading count",
        "Number of telemetry readings in the segment.",
        "Time and size",
    ),
    
    # Arithmetic average of the segment's telemetry values.
    (
        "mean",
        "Average value",
        "Arithmetic average of the segment's telemetry values.",
        "Signal distribution",
    ),
    
    # Average squared spread of the telemetry values around their mean.
    (
        "var",
        "Variance",
        "Average squared spread of the telemetry values around their mean.",
        "Signal distribution",
    ),
    
    # Square root of variance; spread expressed in the signal's original value scale.
    (
        "std",
        "Standard deviation",
        "Square root of variance; spread expressed in the signal's original value scale.",
        "Signal distribution",
    ),
    
    # Distribution-shape statistic that is sensitive to heavy tails and extreme values.
    (
        "kurtosis",
        "Kurtosis",
        "Distribution-shape statistic that is sensitive to heavy tails and extreme values.",
        "Signal distribution",
    ),
    
    # Signed measure of asymmetry; positive and negative values show opposite tail directions.
    (
        "skew",
        "Skewness",
        "Signed measure of asymmetry; positive and negative values show opposite tail directions.",
        "Signal distribution",
    ),
    
    # Peaks whose prominence is at least 10% of the segment's value range.
    (
        "n_peaks",
        "Raw peak count",
        "Peaks whose prominence is at least 10% of the segment's value range.",
        "Peaks",
    ),
    
    # Peak count after a 10-reading moving average reduces short fluctuations.
    (
        "smooth10_n_peaks",
        "10-reading smoothed peak count",
        "Peak count after a 10-reading moving average reduces short fluctuations.",
        "Smoothed peaks",
    ),
    
    # Peak count after a 20-reading moving average reduces short fluctuations.
    (
        "smooth20_n_peaks",
        "20-reading smoothed peak count",
        "Peak count after a 20-reading moving average reduces short fluctuations.",
        "Smoothed peaks",
    ),
    
    # Peak count in the changes between adjacent telemetry readings.
    (
        "diff_peaks",
        "First-difference peak count",
        "Peak count in the changes between adjacent telemetry readings.",
        "Changes",
    ),
    
    # Peak count in the changes between successive first differences.
    (
        "diff2_peaks",
        "Second-difference peak count",
        "Peak count in the changes between successive first differences.",
        "Changes",
    ),
    
    # Variance of the changes between adjacent readings.
    (
        "diff_var",
        "First-difference variance",
        "Variance of the changes between adjacent readings.",
        "Changes",
    ),
    
    # Variance of how the change between adjacent readings changes again.
    (
        "diff2_var",
        "Second-difference variance",
        "Variance of how the change between adjacent readings changes again.",
        "Changes",
    ),
    
    # Sum of squared elapsed-second gaps; larger gaps contribute more to the score.
    (
        "gaps_squared",
        "Squared time-gap score",
        "Sum of squared elapsed-second gaps; larger gaps contribute more to the score.",
        "Gaps and scaled measures",
    ),
    
    # The source sampling value multiplied by the number of readings.
    (
        "len_weighted",
        "Sampling-weighted length",
        "The source sampling value multiplied by the number of readings.",
        "Gaps and scaled measures",
    ),
    
    # Signal variance divided by the segment duration.
    (
        "var_div_duration",
        "Variance per duration",
        "Signal variance divided by the segment duration.",
        "Gaps and scaled measures",
    ),
    
    # Signal variance divided by the number of readings.
    (
        "var_div_len",
        "Variance per reading",
        "Signal variance divided by the number of readings.",
        "Gaps and scaled measures",
    ),
)


# __________________________________________
# SOURCE AND CACHE IDENTITY
# ==========================================
# Source descriptions connect selector labels to configured paths and preparation guidance.
# Fingerprint helpers below identify cache inputs; assistant construction validates their data.


# --- source_definition()
def source_definition(
    profile_label: str,
    *,
    config: AppConfig = DEFAULT_CONFIG,
) -> SourceDefinition:
    """Select the configured local path and provenance for an approved profile.

    Args:
        profile_label: One of the labels offered by the shared profile selector.
        config: Configuration supplying the authentic and fixture file paths.

    Returns:
        Source metadata that the loading steps can fingerprint and validate.

    Raises:
        FrontendValidationError: If the label does not name a supported profile.
    """
    
    # Map the authentic selector label to its pinned validation profile and local path.
    if profile_label == AUTHENTIC_PROFILE_LABEL:
        return SourceDefinition(
            profile_label=profile_label,
            profile_name="authentic",
            dataset_path=config.default_dataset_path,
            provenance=(
                "Historical OPS-SAT Anomaly Detection (OPS-SAT-AD) v2 data from Zenodo "
                "record 15108715"
            ),
            simulated=False,
        )
    
    # Keep simulated fixture provenance attached to the alternative offline source.
    if profile_label == FIXTURE_PROFILE_LABEL:
        return SourceDefinition(
            profile_label=profile_label,
            profile_name="fixture",
            dataset_path=config.demo_dataset_path,
            provenance=(
                "A fixed set of simulated examples for trying the app offline. "
                "Deterministic means the same data and settings give repeatable results"
            ),
            simulated=True,
        )
    
    # Reject labels outside the shared profile selector before loading a dataset.
    raise FrontendValidationError(f"unsupported data profile: {profile_label!r}")


# ---


# --- official_data_artifacts()
def official_data_artifacts() -> tuple[DataArtifactContext, ...]:
    """Return the two pinned official-file descriptions for the walkthrough.

    The feature table is the model input. The raw-reading file supports the standalone
    verifier's metadata checks. Links, byte counts, and digests are supplied as preparation
    guidance; this function does not read either file or make a network request.
    """

    # Provide preparation metadata for both official artifacts without downloading either.
    return (

        # The feature table is the model input.
        DataArtifactContext(
            filename="dataset.csv",
            official_url=DATASET_DOWNLOAD_URL,
            local_path="data/dataset.csv",
            expected_size_bytes=DATASET_SIZE_BYTES,
            expected_sha256=DATASET_SHA256,
            role=(
                "Validated table with one row per segment and 18 numerical features; "
                "this is the model input."
            ),
        ),

        # The raw-reading file supports the standalone verifier's metadata checks.
        DataArtifactContext(
            filename="segments.csv",
            official_url=SEGMENTS_DOWNLOAD_URL,
            local_path="data/segments.csv",
            expected_size_bytes=SEGMENTS_SIZE_BYTES,
            expected_sha256=SEGMENTS_SHA256,
            role=(
                "Raw 303,493-reading file used by the standalone verifier to cross-check "
                "segment metadata; it is not the MLP input."
            ),
        ),
    )


# ---


# ________________________________________________
# Vocabulary and glossary tables
# ------------------------------------------------
# These transforms prepare shared definitions for teaching tables and check glossary order.


# --- learner_terms_frame()
def learner_terms_frame() -> pd.DataFrame:
    """Return the application terms in stable first-use order."""
    # Pair each stored term with its application meaning for the learner table.
    return pd.DataFrame.from_records(
        [
            {"Term": item.term, "Meaning in this app": item.definition}
            for item in LEARNER_TERMS
        ],
        columns=("Term", "Meaning in this app"),
    )


# ---


# --- feature_glossary_frame()
def feature_glossary_frame() -> pd.DataFrame:
    """Return feature definitions in exactly the configured model-input order.

    The glossary keeps source field names beside their learner-friendly explanations.
    Checking its order catches a missing, repeated, or moved definition before the table
    could explain the wrong position in a feature vector.

    Raises:
        FrontendValidationError: If the glossary names differ from FEATURE_NAMES.
    """
    # INVARIANT: Explanations follow the same feature order that the MLP receives.
    glossary_names = tuple(row[0] for row in FEATURE_GLOSSARY)

    # Reject a glossary whose names cannot explain the configured feature-vector positions.
    if glossary_names != FEATURE_NAMES:
        raise FrontendValidationError(
            "feature glossary does not match the configured model feature order",
        )

    # Expose source names beside their definitions and statistical groups.
    return pd.DataFrame.from_records(
        FEATURE_GLOSSARY,
        columns=(
            "Source feature",
            "Plain-language name",
            "What it measures",
            "Feature group",
        ),
    )


# ---


# ________________________________________________
# Cache fingerprints
# ------------------------------------------------
# A resource key binds local artifact bytes to profile and fitting settings.
# A matching fingerprint identifies inputs; it does not establish dataset validity.


# --- _configuration_value()
def _configuration_value(value: object) -> object:
    """Convert nested configuration values into stable JSON-compatible values.

    Paths become resolved strings, sequence items are converted recursively, and mapping
    keys are sorted by their string form. This prepares comparable input for the digest
    without modifying the configuration objects passed by the caller.
    """
    # Resolve local path spellings before including them in the configuration digest.
    if isinstance(value, Path):
        return str(value.expanduser().resolve())
    
    # Normalize tuple items recursively while retaining their sequence order.
    if isinstance(value, tuple):
        return [_configuration_value(item) for item in value]

    # Normalize nested list values before JSON serialization, including any contained paths.
    if isinstance(value, list):
        return [_configuration_value(item) for item in value]
    
    # Normalize mapping values recursively and sort keys for a stable configuration digest.
    if isinstance(value, dict):
        return {
            str(key): _configuration_value(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    return value


# ---


# --- configuration_sha256()
def configuration_sha256(config: AppConfig = DEFAULT_CONFIG) -> str:
    """Fingerprint every current application-configuration field.

    The dataclass field list supplies the values, so the digest includes configuration
    fields without maintaining a second list here. Stable key order and JSON separators
    keep formatting differences from changing the fingerprint.

    Args:
        config: Settings whose values determine the fitted-resource identity.

    Returns:
        A hexadecimal SHA-256 digest of the normalized configuration representation.
    """
    
    # Enumerate dataclass fields so new settings automatically participate in cache identity.
    payload = {
        field.name: _configuration_value(getattr(config, field.name))
        for field in fields(config)
    }
    
    # Remove key-order and JSON-spacing differences from the fingerprint input.
    encoded_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    # Represent the complete normalized settings as one cache-key digest.
    return hashlib.sha256(encoded_payload).hexdigest()


# ---


# --- build_cache_identity()
def build_cache_identity(
    source: SourceDefinition,
    *,
    config: AppConfig = DEFAULT_CONFIG,
) -> FrontendCacheIdentity:
    """Read the current artifact fingerprint and attach its fitting settings.

    The artifact helper reads local bytes. Dataset schema and authentic-profile checks
    belong to assistant construction; a fingerprint by itself is not a validity result.
    Pages call this before cache lookup so changed inputs request a different resource.

    Args:
        source: Local feature-table path and selected validation profile.
        config: Seed and settings that must remain part of the resource identity.

    Returns:
        The resolved file path, byte identity, profile, seed, and configuration digest.
    """
    
    # Read the artifact bytes for identity; backend construction validates dataset contents.
    artifact = calculate_artifact_verification(source.dataset_path)

    # Bind artifact bytes to the selected profile, seed, and full configuration.
    return FrontendCacheIdentity(
        dataset_path=str(artifact.path.expanduser().resolve()),
        artifact_sha256=artifact.sha256,
        artifact_size_bytes=artifact.size_bytes,
        profile_name=source.profile_name,
        random_seed=config.random_seed,
        config_sha256=configuration_sha256(config),
    )


# ---


# __________________________________________
# SCREENING CONSTRUCTION
# ==========================================
# Bulk screening runs fitted prediction and threshold routing over held-out rows.
# Complete selected-segment analysis later adds historical comparisons, logic, and planning.


# --- status_for_decision()
def status_for_decision(decision_state: DecisionState) -> str:
    """Translate one backend decision state into stable human-facing language."""

    # Map decision states to human-facing status strings.
    status_by_state = {
        DecisionState.ANOMALOUS.value: FLAGGED_STATUS,      # anomalous
        DecisionState.UNCERTAIN.value: UNCERTAIN_STATUS,  # uncertain
        DecisionState.NORMAL.value:    NORMAL_STATUS,     # normal
    }

    return status_by_state[decision_state.value]


# ---


# --- build_screening_records()
def build_screening_records(
    assistant: TelemetryAssistant,
) -> tuple[ScreeningRecord, ...]:
    """Predict each official held-out segment with the fitted model.

    This first pass supplies the review population. It uses prediction and threshold
    classification only, which keeps historical search, logic, and planning available
    for the later selected-segment request instead of repeating them for every row.

    Args:
        assistant: Backend state with validated rows, fixed partitions, and a fitted MLP.

    Returns:
        One record per test index in the partition order, without reviewed labels.
    """
    dataset = assistant.dataset
    trained_model = assistant.trained_model
    records: list[ScreeningRecord] = []

    # INFERENCE: Reuse fitted weights for the held-out partition, one feature row at a time.
    # Preserve the backend test-index order while creating the initial review population.
    for row_index in assistant.partitions.test_indices: #
        # Pass this held-out feature row to the trained backend predictor.
        probability = predict_anomaly_probability(
            trained_model,
            dataset.x_validated_telemetry_features[row_index],
        )
        # Classify the anomaly probability using the current threshold and margin.
        classification = classify_probability(
            dataset.segment_ids[row_index],
            probability,
            classification_threshold=trained_model.classification_threshold,
            uncertainty_margin=trained_model.uncertainty_margin,
            # Keep the historical answer out of this first-pass screening record.
            reference_label=None,
            reference_partition="held-out test",
        )
        # Attach the exact source ID and channel to the model decision for later selection.
        records.append(
            ScreeningRecord(
                segment_id=classification.segment_id,
                channel=dataset.channels[row_index],
                anomaly_probability=classification.anomaly_probability,
                predicted_class=classification.predicted_class,
                decision_state=classification.decision_state.value,
                status=status_for_decision(classification.decision_state),
                classification_threshold=classification.classification_threshold,
                uncertainty_margin=classification.uncertainty_margin,
                partition=classification.reference_partition,
            ),
        )
    return tuple(records)


# ---


# ________________________________________________
# Fitted resource construction and reuse
# ------------------------------------------------
# Build the validated backend on a cache miss and retain its initial screening records.
# Pages keep interactive selections outside this shared fitted resource.


# --- build_frontend_state()
def build_frontend_state(
    identity: FrontendCacheIdentity,
    source: SourceDefinition,
    *,
    config: AppConfig = DEFAULT_CONFIG,
) -> FrontendState:
    """Build one backend assistant and its initial held-out screening records.

    Args:
        identity: File and settings identity already prepared by the caller.
        source: Profile description associated with that identity.
        config: Backend configuration used to validate, partition, and fit the data.

    Returns:
        A reusable assistant together with its presentation source and screening snapshot.

    Raises:
        FrontendValidationError: If identity and source name different profiles.
        CubeSatError: If backend data loading or assistant construction fails.

    Logic:
        1. Check that the two profile names agree.
        2. Let build_assistant validate the data and prepare the fitted backend state.
        3. Screen its held-out rows and keep those records with the assistant.
    """
    
    # Reject inconsistent profile metadata before constructing the reusable resource.
    if identity.profile_name != source.profile_name:
        raise FrontendValidationError("cache identity and source profile do not match")
    # Delegate data validation, partitioning, fitting, and historical indexes to the backend.
    assistant = build_assistant(
        Path(identity.dataset_path),
        profile_name=identity.profile_name,
        config=config,
    )
    # Keep the screening snapshot with the fitted assistant that produced its probabilities.
    return FrontendState(
        identity=identity,
        source=source,
        assistant=assistant,
        screening_records=build_screening_records(assistant),
    )


# ---


# --- get_cached_frontend_state()
# Streamlit resource cache can share this object across sessions.
# Session-specific filters are not part of it. The four-entry limit bounds 
# the number of stored resources.
#   On a cache miss, the body fingerprints the source again before building 
# the assistant.
#   That catches an artifact change between the page's identity read and this check.
#   Cache hits return the existing resource without executing this body; 
# each page still reads a fresh identity before requesting the resource on its 
# next rerun.
#
# --- get_cached_frontend_state()
#
@st.cache_resource(max_entries=4, show_spinner=False)
#
def get_cached_frontend_state(
    identity: FrontendCacheIdentity,
    source: SourceDefinition,
    config: AppConfig = DEFAULT_CONFIG,
) -> FrontendState:
    """Reuse a fitted resource while its data and settings remain the same.

    Streamlit's resource cache can share this object across sessions. Session-specific
    filters are not part of it. The four-entry limit bounds the number of stored resources.

    On a cache miss, the body fingerprints the source again before building the assistant.
    That catches an artifact change between the page's identity read and this check. Cache
    hits return the existing resource without executing this body; each page still reads
    a fresh identity before requesting the resource on its next rerun.

    Raises:
        FrontendValidationError: If the requested and freshly calculated identities differ.
        CubeSatError: If the local artifact cannot be read or the assistant cannot be built.
    """
    # VALIDATION: This body runs on a cache miss, before a new assistant is built.
    current_identity = build_cache_identity(source, config=config)
    if current_identity != identity:
        raise FrontendValidationError(
            "the selected data artifact changed while the analysis was loading; try again",
        )
    return build_frontend_state(identity, source, config=config)


# ---


# ________________________________________________
# Profile scale and walkthrough examples
# ------------------------------------------------
# These helpers explain the active dataset roles and connect held-out IDs to source context.
# Named fixture scenarios contribute teaching text without changing the selected result.


# --- build_dataset_context()
def build_dataset_context(state: FrontendState) -> DatasetContext:
    """Derive profile counts from validated rows and the assistant's partitions.

    The official reference set includes both model-training and threshold-validation rows.
    It is not a fourth disjoint group to add to the dataset total. The authentic raw-reading
    count comes from the pinned source contract because the model loads feature rows.

    Args:
        state: FrontendState object containing the assistant and source information.
    
    Returns:
        DatasetContext object containing the dataset context.
    """
    # Use the fitted resource's validated dataset and established row partitions.
    assistant = state.assistant
    dataset = assistant.dataset
    partitions = assistant.partitions
    # Pair active-profile row counts with the pinned authentic raw-reading reference.
    return DatasetContext(
        profile_label=state.source.profile_label,
        simulated=dataset.simulated,
        total_segments=len(dataset.segment_ids),
        official_training_segments=len(partitions.reference_indices),
        model_training_segments=len(partitions.training_indices),
        threshold_validation_segments=len(partitions.validation_indices),
        held_out_segments=len(partitions.test_indices),
        feature_count=len(dataset.feature_names),
        channel_codes=tuple(sorted(set(dataset.channels))),
        raw_reading_count=(
            None if dataset.simulated else AUTHENTIC_SEGMENTS_ROW_COUNT
        ),
    )


# ---


# --- dataset_role_frame()
def dataset_role_frame(context: DatasetContext) -> pd.DataFrame:
    """Describe the three separate row roles within the active dataset.

    Each count comes from DatasetContext. Training rows fit the scaler and model,
    validation rows choose the cutoff, and held-out rows supply screening and evaluation.
    The table explains those roles without repartitioning the data.

    Args:
        context: DatasetContext object containing the dataset context.

    Returns:
        Pandas DataFrame containing the dataset role frame.
    """
    # Describe the three disjoint roles using counts already derived from backend partitions.
    rows = (
        {
            "Row role": "Model training",
            "Segments": context.model_training_segments,
            "Purpose": "Learn the feature scales and neural-network weights.",
        },
        {
            "Row role": "Threshold validation",
            "Segments": context.threshold_validation_segments,
            "Purpose": "Choose the classification threshold after model fitting.",
        },
        {
            "Row role": "Held-out test",
            "Segments": context.held_out_segments,
            "Purpose": "Screen segments and evaluate predictions after fitting.",
        },
    )
    # Expose role counts and their purposes without assigning any rows to new partitions.
    return pd.DataFrame.from_records(
        rows,
        columns=("Row role", "Segments", "Purpose"),
    )


# ---


# --- authentic_reference_frame()
def authentic_reference_frame() -> pd.DataFrame:
    """Show pinned authentic dataset scale alongside either active profile.

    These reference values describe OPS-SAT-AD v2. They remain separate from the active
    fixture counts and are not measurements calculated from the current screening table.
    """
    return pd.DataFrame.from_records(
        (
            {"Dataset fact": "Total segments", "Value": AUTHENTIC_ROW_COUNT},
            {
                "Dataset fact": "Official training-role segments",
                "Value": AUTHENTIC_TRAINING_ROW_COUNT,
            },
            {
                "Dataset fact": "Held-out test segments",
                "Value": AUTHENTIC_TEST_ROW_COUNT,
            },
            {"Dataset fact": "Numerical features", "Value": 18},
            {"Dataset fact": "Coded channels", "Value": 9},
        ),
        columns=("Dataset fact", "Value"),
    )


# ---


# --- walkthrough_segment_ids()
def walkthrough_segment_ids(state: FrontendState) -> tuple[str, ...]:
    """Return held-out example IDs in the existing probability-ranked order.

    Args:
        state: FrontendState object containing the assistant and screening records.

    Returns:
        Tuple of segment IDs in probability-ranked order.
    """
    frame = screening_frame(state.screening_records)
    return tuple(str(value) for value in frame["segment_id"])


# ---


# --- build_walkthrough_example_context()
def build_walkthrough_example_context(
    state: FrontendState,
    segment_id: str,
) -> WalkthroughExampleContext:
    """Find source context and a matching scenario name for one segment.

    The backend resolves the exact row. In fixture mode, the scenario JSON adds a name
    and purpose when its segment ID matches; an unmatched row keeps the general fixture
    label. Scenario metadata does not alter the row, its probability, or its route.

    Args:
        state: Current fitted profile and its scenario-file configuration.
        segment_id: Exact selected ID, normally taken from the held-out example options.

    Returns:
        Profile, segment, channel, and scenario text for the example caption.
    """
    # Resolve this example's exact source row through the active backend dataset.
    dataset = state.assistant.dataset
    row_index = select_segment_index(dataset, segment_id)
    # Use general authentic-example text until simulated provenance requires fixture wording.
    scenario_name = "authentic held-out example"
    scenario_purpose = "Inspect one authentic held-out segment from the selected local artifact."
    # Fixture rows receive simulated-example wording before any named scenario is matched.
    if dataset.simulated:
        scenario_name = "custom fixture example"
        scenario_purpose = "Inspect one deterministic simulated held-out segment."
        # Read scenario names and purposes from the configured fixture metadata.
        scenarios = load_demo_scenarios(state.assistant.config.demo_scenarios_path)
        # Attach a named scenario only when its stored ID matches this exact example.
        for candidate_name, scenario in scenarios.items():
            if scenario["segment_id"] == segment_id:
                scenario_name = candidate_name
                scenario_purpose = scenario["purpose"]
                break
    # Carry the selected row's channel and scenario meaning into the walkthrough caption.
    return WalkthroughExampleContext(
        profile_label=state.source.profile_label,
        segment_id=segment_id,
        channel=dataset.channels[row_index],
        scenario_name=scenario_name,
        scenario_purpose=scenario_purpose,
    )


# ---


# __________________________________________
# PANDAS PRESENTATION TRANSFORMS
# ==========================================
# Ranked tables and population summaries reuse the screening snapshot.
# Filters alter the displayed rows after inference and keep source IDs available for selection.


# --- screening_frame()
def screening_frame(records: tuple[ScreeningRecord, ...]) -> pd.DataFrame:
    """Build and validate a probability-ranked table of held-out predictions.

    Args:
        records: Per-segment screening results to expose as a presentation table.

    Returns:
        A frame with the fixed screening columns, ranked by descending probability and
        then ascending segment ID. An empty input retains the same column schema.

    Raises:
        FrontendValidationError: If IDs repeat, probabilities leave the 0-to-1 range,
            or a row has a role other than held-out test.

    Logic:
        1. Copy the named record fields into a DataFrame.
        2. Check row identity, probability range, and held-out membership labels.
        3. Apply a stable ranking for display; source segment IDs remain unchanged.
    """
    frame = pd.DataFrame.from_records(
        [
            {
                "segment_id": record.segment_id,
                "channel": record.channel,
                "anomaly_probability": record.anomaly_probability,
                "predicted_class": record.predicted_class,
                "decision_state": record.decision_state,
                "status": record.status,
                "classification_threshold": record.classification_threshold,
                "uncertainty_margin": record.uncertainty_margin,
                "partition": record.partition,
            }
            for record in records
        ],
        columns=SCREENING_COLUMNS,
    )
    # Keep the declared screening columns available even when there are no records to rank.
    if frame.empty:
        return frame
    # Require unique source IDs so selection cannot resolve to multiple screening rows.
    if frame["segment_id"].duplicated().any():
        raise FrontendValidationError("screening contains duplicate segment IDs")
    # Reject scores outside the probability scale before ranking or percentage formatting.
    if not frame["anomaly_probability"].between(0.0, 1.0, inclusive="both").all():
        raise FrontendValidationError("screening contains an invalid anomaly probability")
    if set(frame["partition"]) != {"held-out test"}:
        raise FrontendValidationError("screening contains rows outside the held-out test partition")
    # Tied probabilities retain a predictable order through their stable source IDs.
    return frame.sort_values(
        ["anomaly_probability", "segment_id"],
        ascending=[False, True],
        kind="mergesort",
        ignore_index=True,
    )


# ---


# --- summarize_screening()
def summarize_screening(frame: pd.DataFrame) -> ScreeningSummary:
    """Count the three exclusive statuses within the supplied population.

    The input may be the whole screening frame or one channel's rows. Each segment must
    contribute to exactly one status, so the three counts must equal the frame length.

    Args:
        frame: Pandas DataFrame containing the screening records.

    Returns:
        ScreeningSummary object containing the summary of the screening records.

    Raises:
        FrontendValidationError: If a status is unsupported or the counts do not reconcile.
    """
    # Collect the supplied population's statuses before counting its review routes.
    observed_statuses = set(frame.get("status", pd.Series(dtype="string")))
    # Find labels that the three-way screening vocabulary cannot represent.
    unsupported_statuses = observed_statuses - set(STATUS_OPTIONS)
    # Reject unsupported labels rather than silently omitting them from population totals.
    if unsupported_statuses:
        raise FrontendValidationError(
            "screening contains unsupported statuses: " + ", ".join(sorted(unsupported_statuses)),
        )
    # Count each model route within this supplied population, allowing an empty input.
    flagged = int((frame["status"] == FLAGGED_STATUS).sum()) if not frame.empty else 0
    uncertain = int((frame["status"] == UNCERTAIN_STATUS).sum()) if not frame.empty else 0
    likely_normal = int((frame["status"] == NORMAL_STATUS).sum()) if not frame.empty else 0
    # Keep the population denominator with its three route counts.
    summary = ScreeningSummary(
        screened=len(frame),
        flagged=flagged,
        uncertain=uncertain,
        likely_normal=likely_normal,
    )
    # Require every screened row to contribute to exactly one supported status count.
    if summary.flagged + summary.uncertain + summary.likely_normal != summary.screened:
        raise FrontendValidationError("screening status counts do not reconcile")
    return summary


# ---


# ________________________________________________
# Channel counts and readable comparisons
# ------------------------------------------------
# Group the supplied population by channel and carry each denominator into the display.
# The worked example and largest-count lookup describe those same summary values.


# --- channel_summary_frame()
def channel_summary_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate per-channel counts and their screened-population rates.

    A channel's flagged rate divides its flagged count by its own screened count. The
    uncertain rate uses the same denominator. These describe review load within that
    channel; neither rate is classifier precision or the fraction of all dataset rows.

    Args:
        frame: Pandas DataFrame containing the screening records.

    Returns:
        Pandas DataFrame containing the channel summary frame.
    """
    columns = (
        "channel",
        "screened",
        "flagged",
        "uncertain",
        "likely_normal",
        "flagged_rate",
        "uncertain_rate",
    )
    # Return the channel-summary schema with no rows when screening is empty.
    if frame.empty:
        return pd.DataFrame(columns=columns)
    # Summarize each channel separately so its counts share one channel-specific denominator.
    rows: list[dict[str, object]] = []
    for channel, group in frame.groupby("channel", sort=True):
        summary = summarize_screening(group)

        rows.append(
            {
                "channel": str(channel),
                "screened": summary.screened,
                "flagged": summary.flagged,
                "uncertain": summary.uncertain,
                "likely_normal": summary.likely_normal,
                # The denominator belongs to this channel, not the full held-out dataset.
                "flagged_rate": summary.flagged / summary.screened,
                "uncertain_rate": summary.uncertain / summary.screened,
            },
        )
    return pd.DataFrame.from_records(rows, columns=columns)


# ---


# --- channel_reading_frame()
def channel_reading_frame(channel_frame: pd.DataFrame) -> pd.DataFrame:
    """Label every channel count, denominator, and rate for direct reading.

    Args:
        channel_frame: Pandas DataFrame containing the channel summary frame.

    Returns:
        Pandas DataFrame containing the channel reading frame.
    """
    # Preserve readable channel headings when there are no channel rows to display.
    if channel_frame.empty:
        return pd.DataFrame(
            columns=(
                "Channel code",
                "Screened",
                "Flagged anomaly",
                "Uncertain review",
                "Likely normal",
                "Flagged rate",
                "Uncertain rate",
            ),
        )
    # Select the existing counts and rates in the order expected by the readable table.
    return channel_frame.loc[
        :,
        [
            "channel",
            "screened",
            "flagged",
            "uncertain",
            "likely_normal",
            "flagged_rate",
            "uncertain_rate",
        ],
    # Replace internal field names with the labels used beside the chart.
    ].rename(
        columns={
            "channel": "Channel code",
            "screened": "Screened",
            "flagged": "Flagged anomaly",
            "uncertain": "Uncertain review",
            "likely_normal": "Likely normal",
            "flagged_rate": "Flagged rate",
            "uncertain_rate": "Uncertain rate",
        },
    )


# ---


# --- channel_worked_example()
def channel_worked_example(channel_frame: pd.DataFrame) -> str:
    """Explain the rate arithmetic using one current-profile channel.

    Choose the channel with the most screened segments and use its code to break ties.
    That deterministic choice gives the page a concrete denominator to explain without
    implying that this example has the highest flagged rate.

     Args:
        channel_frame: Pandas DataFrame containing the channel summary frame.

    Returns:
        A string containing the channel worked example.
    """
    # If the frame is empty, return a message indicating that no channel rate can be calculated.
    if channel_frame.empty:
        return "No channel rate can be calculated because no segments were screened."
    # Use the largest screened population, then channel code, to choose a repeatable example.
    example = channel_frame.sort_values(
        ["screened", "channel"],
        ascending=[False, True],
        kind="mergesort",
    ).iloc[0]   
    # Use that channel's integer counts as the worked fraction's numerator and denominator.
    screened = int(example["screened"])
    flagged = int(example["flagged"])
    uncertain = int(example["uncertain"])
    # Show the same channel denominator for flagged and uncertain percentages.
    return (
        f"Worked example for {example['channel']}: flagged rate = {flagged} flagged / "
        f"{screened} screened = {flagged / screened:.1%}; uncertain rate = {uncertain} "
        f"uncertain / {screened} screened = {uncertain / screened:.1%}."
    )


# ---


# --- highest_flagged_channels()
def highest_flagged_channels(channel_frame: pd.DataFrame) -> tuple[str, ...]:
    """Return every channel tied for the highest flagged count in stable order.

     Args:
        channel_frame: Pandas DataFrame containing the channel summary frame.

    Returns:
        A tuple containing the channel codes tied for the highest flagged count.
    """
    # If the frame is empty, return an empty tuple.
    if channel_frame.empty:
        return ()
    # Compare flagged counts rather than rates when identifying the largest review totals.
    maximum = int(channel_frame["flagged"].max())
    # Return the channel codes tied for the maximum flagged count.
    return tuple(
        sorted(
            str(channel)
            for channel in channel_frame.loc[
                channel_frame["flagged"] == maximum,
                "channel",
            ]
        ),
    )


# ---


# ________________________________________________
# Filter and selection reconciliation
# ------------------------------------------------
# Apply view constraints in the existing rank order, then reconcile selection by source ID.
# Display row positions can change while a segment retains its identity.


# --- filter_screening()
def filter_screening(
    frame: pd.DataFrame,
    *,
    statuses: tuple[str, ...] | list[str] | None = None,
    channels: tuple[str, ...] | list[str] | None = None,
    exact_segment_id: str = "",
) -> pd.DataFrame:
    """Narrow a ranked screening frame without changing the underlying model.

    Args:
        frame: Validated screening rows in their existing probability rank order.
        statuses: Allowed status values, or None to leave status unrestricted.
        channels: Allowed channel codes, or None to leave channel unrestricted.
        exact_segment_id: Optional exact ID after removing surrounding whitespace.

    Returns:
        A copied frame containing rows that satisfy all active filters. Its new row index
        is only a display position; segment_id remains the identity of each record.
    """
    # Begin with the ranked input; the final return creates the independent display copy.
    filtered = frame
    # Filter by status if statuses are provided.
    if statuses is not None:
        filtered = filtered.loc[filtered["status"].isin(statuses)]
    # Filter by channel if channels are provided.
    if channels is not None:
        filtered = filtered.loc[filtered["channel"].isin(channels)]
    # Normalize the segment ID by removing any leading or trailing whitespace.
    normalized_segment_id = exact_segment_id.strip()
    # Filter by segment ID if an exact segment ID is provided.
    if normalized_segment_id:
        filtered = filtered.loc[filtered["segment_id"] == normalized_segment_id]
    # Reset display row positions and copy the result while preserving source segment IDs.
    return filtered.reset_index(drop=True).copy()


# ---


# --- reconcile_selection()
def reconcile_selection(filtered_frame: pd.DataFrame, selected_segment_id: str | None) -> str:
    """Keep an exact segment selection only while it remains in the visible rows.

    Filtering can remove the selected record or change table row positions. Checking IDs
    lets the page clear stale detail without accidentally selecting a different segment.
    An empty or absent selection returns an empty string.

    Args:
        filtered_frame: Pandas DataFrame containing the filtered screening frame.
        selected_segment_id: The segment ID to reconcile.

    Returns:
        The segment ID to reconcile.
    """
    # Normalize the segment ID by removing any leading or trailing whitespace.
    normalized_selection = (selected_segment_id or "").strip()
    # If the normalized segment ID is empty, return an empty string.
    if not normalized_selection:
        return ""
    # Allow selection only among the IDs still visible after filtering.
    valid_ids = set(filtered_frame.get("segment_id", pd.Series(dtype="string")))
    return normalized_selection if normalized_selection in valid_ids else ""


# ---


# --- review_table_frame()
def review_table_frame(filtered_frame: pd.DataFrame) -> pd.DataFrame:
    """Return only the four approved columns passed to the read-only Streamlit table.

    Args:
        filtered_frame: Pandas DataFrame containing the filtered screening frame.

    Returns:
        Pandas DataFrame containing the review table frame.
    """
    # If the frame is empty, return an empty DataFrame.
    if filtered_frame.empty:
        return pd.DataFrame(
            columns=("Segment ID", "Channel", "AI status", "Probability"),
        )
    # Keep source IDs beside model status and probability in the compact review table.
    return filtered_frame.loc[
        :, ["segment_id", "channel", "status", "anomaly_probability"]
    ].rename(
        columns={
            "segment_id": "Segment ID",
            "channel": "Channel",
            "status": "AI status",
            "anomaly_probability": "Probability",
        },
    )


# ---


# __________________________________________
# CHART AND EVIDENCE TRANSFORMS
# ==========================================
# These helpers prepare chart values and evidence tables for page rendering.
# Stored backend results retain ownership of classification, neighbors, rules, and plans.


# ________________________________________________
# Channel chart and accessible text
# ------------------------------------------------
# Both outputs read the channel summary so count bars and textual rates share their values.


# --- build_channel_figure()
def build_channel_figure(channel_frame: pd.DataFrame) -> go.Figure:
    """Format supplied channel counts as two grouped Plotly bar traces.

    The same channel summary also supplies the page's readable table. The chart retains
    counts as its bar heights and pairs each height with its screened denominator and rate
    for hover text. Printed values, trace names, and adjacent text make the quantities
    available beyond color alone.

    Args:
        channel_frame: Pandas DataFrame containing the channel summary frame.

    Returns:
        Plotly Figure containing the channel summary figure.
    """
    # Prepare the chart that will display the supplied channel summary.
    figure = go.Figure()
    # Pair each review status count with its matching rate and visible trace label.
    for count_column, rate_column, trace_name in (
        ("flagged", "flagged_rate", FLAGGED_STATUS),    
        ("uncertain", "uncertain_rate", UNCERTAIN_STATUS),
    ):
        # Carry each bar's screened denominator and rate into its hover values.
        custom_data = list(
            zip(
                channel_frame["screened"].tolist(),
                channel_frame[rate_column].tolist(),
                strict=True,
            ),
        )
        # Plot the stored count while keeping its value available as printed text.
        figure.add_trace(
            go.Bar(
                name=trace_name,
                x=channel_frame["channel"],
                y=channel_frame[count_column],
                customdata=custom_data,
                text=channel_frame[count_column],
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x}</b><br>" + trace_name + ": %{y}<br>"
                    "Screened: %{customdata[0]}<br>Rate: %{customdata[1]:.1%}"
                    "<extra></extra>"
                ),
            ),
        )
    # Label grouped bars as held-out counts and identify their screening routes.
    figure.update_layout(
        title="Segments needing review by telemetry channel",
        xaxis_title="Telemetry channel",
        yaxis_title="Held-out segment count",
        barmode="group",
        legend_title_text="AI screening status",
        margin={"l": 20, "r": 20, "t": 70, "b": 20},
        hovermode="x unified",
    )   
    # Anchor integer segment counts at zero so bar heights share a comparable scale.
    figure.update_yaxes(rangemode="tozero", dtick=1)
    # Return the configured chart for the page to render.
    return figure


# ---


# --- channel_accessible_lines()
def channel_accessible_lines(channel_frame: pd.DataFrame) -> tuple[str, ...]:
    """Return complete channel values that do not require color or pointer hover.

    Args:
        channel_frame: Pandas DataFrame containing the channel summary frame.

    Returns:
        Tuple of strings containing the channel accessible lines.
    """
    return tuple(
        (
            f"**{row.channel}** — {int(row.flagged)} flagged " # flagged
            f"({float(row.flagged_rate):.1%}), {int(row.uncertain)} uncertain " # uncertain
            f"({float(row.uncertain_rate):.1%}), and {int(row.likely_normal)} likely normal " # likely normal
            f"of {int(row.screened)} screened."
        )
        # Provide one complete text alternative for each channel summary row.
        for row in channel_frame.itertuples(index=False)
    )


# ---


# ________________________________________________
# Selected classification and historical evidence
# ------------------------------------------------
# Explain the selected backend route and format its ranked deviations and reviewed neighbors.


# --- decision_explanation()
def decision_explanation(result: CompleteAnalysisResult) -> str:
    """Describe the backend's chosen threshold route for one selected segment.

    The threshold and margin supply the band edges shown in the sentence. Dispatch uses
    the decision's stored value, which remains comparable when Streamlit reloads a module
    and creates a new enum class. This formatter does not classify the probability again.

    Args:
        result: CompleteAnalysisResult object.

    Returns:
        String containing the decision explanation.
    """
    classification = result.classification
    # Read the backend route as a stable value for dispatch across module reloads.
    decision_value = classification.decision_state.value
    # Use the stored cutoff and margin to explain the lower edge of the review band.
    lower_bound = classification.classification_threshold - classification.uncertainty_margin
    # Use the same cutoff and margin to explain the upper edge.
    upper_bound = classification.classification_threshold + classification.uncertainty_margin
    # Explain the existing uncertain route without classifying the probability again.
    if decision_value == DecisionState.UNCERTAIN.value:
        return (
            f"The probability is inside the uncertainty band from {lower_bound:.1%} to "
            f"{upper_bound:.1%}, so this segment is routed to human review."
        )
    # Explain why the stored anomalous route directs this segment to review.
    if decision_value == DecisionState.ANOMALOUS.value:
        return (
            f"The probability is above the {upper_bound:.1%} upper edge of the uncertainty "
            "band, so the AI flags this segment for review."
        )
    # Describe the remaining likely-normal route relative to the lower band edge.
    return (
        f"The probability is below the {lower_bound:.1%} lower edge of the uncertainty band, "
        "so the AI marks this segment as likely normal."
    )


# ---


# --- deviation_frame()
def deviation_frame(result: CompleteAnalysisResult) -> pd.DataFrame:
    """Return the backend-ranked deviating feature names without raw feature arrays.

    Args:
        result: CompleteAnalysisResult object.

    Returns:
        Pandas DataFrame containing the deviation frame.
    """
    # Expose feature names in the deviation order already supplied by the backend.
    return pd.DataFrame.from_records(
        [
            {"Rank": rank, "Feature": feature_name}
            for rank, feature_name in enumerate(result.top_deviating_features, start=1)
        ],
        columns=("Rank", "Feature"),
    )


# ---


# --- similar_cases_frame()
def similar_cases_frame(cases: tuple[SimilarCase, ...]) -> pd.DataFrame:
    """Format reviewed neighbors without transferring their labels to the query.

    Each row retains its within-class rank, segment ID, and backend distance, which is
    Euclidean by default. Feature gaps describe the largest standardized coordinate
    differences; they are comparison evidence, not model feature-importance scores.

    Args:
        cases: Tuple of SimilarCase objects.

    Returns:
        Pandas DataFrame containing the similar cases frame.
    """
    # Build comparison rows from the retrieved neighbors and their stored evidence.
    return pd.DataFrame.from_records(
        [
            # Keep the case identity, reviewed label, and distance together.
            {
                "Rank": case.rank,
                "Reviewed case": case.case_id,
                "Reviewed label": case.reviewed_label,
                "Euclidean distance": case.distance,
                "Largest standardized feature gaps": ", ".join(
                    # Round standardized coordinate gaps only for readable comparison text.
                    (
                        f"{difference.feature_name} "
                        f"({difference.absolute_standardized_difference:.3f})"
                    )
                    for difference in case.feature_differences
                ),
            }
            # Retain the backend's neighbor order within the supplied reviewed class.
            for case in cases
        ],
        columns=(
            "Rank",
            "Reviewed case",
            "Reviewed label",
            "Euclidean distance",
            "Largest standardized feature gaps",
        ),
    )


# ---


# ________________________________________________
# Held-out evaluation context
# ------------------------------------------------
# The evaluation matrix and reviewed-label counts describe model assessment.
# These helpers keep reviewed outcomes separate from first-pass screening decisions.


# --- confusion_matrix_frame()
def confusion_matrix_frame(evaluation: EvaluationMetrics) -> pd.DataFrame:
    """Label the existing evaluation matrix by reviewed and predicted class.

    Rows are actual normal/anomalous labels and columns are predicted normal/anomalous
    classes. The supplied matrix already contains the counts; this helper only gives the
    axes readable names.

    Args:
        evaluation: EvaluationMetrics object.

    Returns:
        Pandas DataFrame containing the confusion matrix frame.
    """
    # Label the existing matrix axes without recomputing prediction counts.
    return pd.DataFrame(
        evaluation.confusion_matrix,
        index=("Actual normal", "Actual anomalous"),
        columns=("Predicted normal", "Predicted anomalous"),
    )


# ---


# --- held_out_reviewed_counts()
def held_out_reviewed_counts(state: FrontendState) -> tuple[int, int]:
    """Count reviewed classes in held-out rows for evaluation context.

    The backend validated binary labels, with anomalous encoded as one. Their sum is the
    anomalous count, and the remaining labels are normal. These labels explain evaluation
    denominators and do not enter the screening-record prediction call.

    Args:
        state: FrontendState object.

    Returns:
        Tuple of integers containing the normal and anomalous counts.
    """
    # Read labels only from the held-out indices for evaluation context.
    labels = state.assistant.dataset.y_anomaly_labels[
        list(state.assistant.partitions.test_indices)
    ]
    # Sum the validated binary labels, where one denotes an anomalous reviewed segment.
    anomalous = int(labels.sum())
    # The remaining held-out labels supply the reviewed normal count.
    normal = int(len(labels) - anomalous)
    # Return evaluation denominators in normal, then anomalous class order.
    return normal, anomalous


# ---


# ________________________________________________
# Complete selected analysis
# ------------------------------------------------
# The page supplies an exact ID to the existing assistant for the full evidence workflow.
# This request extends bulk screening with historical search, reasoning, and a simulated plan.


# --- analyze_selected_segment()
def analyze_selected_segment(
    state: FrontendState,
    segment_id: str,
) -> CompleteAnalysisResult:
    """Ask the existing assistant for one complete selected-segment result.

    Args:
        state: Cached backend resource associated with the active data profile.
        segment_id: Exact ID supplied by the page's selector.

    Returns:
        The backend result unchanged, including classification, similar cases, reasoning,
        and a simulated review plan.

    Raises:
        FrontendValidationError: If no nonblank segment ID was supplied.
        CubeSatError: If the backend cannot resolve or analyze the selected segment.
    """
    # Trim surrounding whitespace while preserving the exact selected source ID.
    normalized_segment_id = segment_id.strip()
    
    # Require a selected record before requesting the full backend workflow.
    if not normalized_segment_id:
        raise FrontendValidationError("select a segment before requesting detail")
    
    # Reuse the fitted assistant for classification, historical evidence, logic, and planning.
    return state.assistant.analyze(normalized_segment_id)


# ---


# ________________________________________________
# Walkthrough feature and reasoning transforms
# ------------------------------------------------
# Pair the selected row with fitted scaling, threshold values, and recorded symbolic evidence.
# These tables explain backend outputs while preserving their selected-segment context.


# --- walkthrough_feature_frame()
def walkthrough_feature_frame(
    state: FrontendState,
    segment_id: str,
) -> pd.DataFrame:
    """Pair one segment's raw features with the fitted scaler's transformation.

    The backend standardizer reuses the model-training mean and spread. It does not learn
    new statistics from this selected example. The returned row from that transformation
    is paired with raw values and feature names in the validated model-input order.

    Args:
        state: Cached backend resource associated with the active data profile.
        segment_id: Exact ID supplied by the page's selector.

    Returns:
        One table row per feature, with its source name, raw value, and standardized value.
    """
    # Reuse the active profile's validated data and fitted model.
    assistant = state.assistant
    
    # Resolve the selected source ID independently of its current display row position.
    row_index = select_segment_index(assistant.dataset, segment_id)
    
    # Read that segment's feature vector in the validated model-input order.
    raw_values = assistant.dataset.x_validated_telemetry_features[row_index]
    # Apply the backend scaler with the existing model-training statistics.
    standardized_values = standardize_features(
        assistant.trained_model,
        raw_values,
    )[0]
    # Pair raw and transformed values for direct feature-by-feature inspection.
    return pd.DataFrame.from_records(
        [
            # Keep each source feature name beside both representations of its value.
            {
                "Feature": feature_name,
                "Raw value": float(raw_value),
                "Standardized value": float(standardized_value),
            }
            # Require names, raw values, and standardized values to align without truncation.
            for feature_name, raw_value, standardized_value in zip(
                assistant.dataset.feature_names,
                raw_values,
                standardized_values,
                strict=True,
            )
        ],
        # Fix the teaching table's raw-to-standardized comparison column order.
        columns=("Feature", "Raw value", "Standardized value"),
    )


# ---


# --- build_threshold_context()
def build_threshold_context(result: CompleteAnalysisResult) -> ThresholdContext:
    """Prepare the selected result's exact threshold and uncertainty-band values.

    The backend already chose the decision state. This helper copies the probability,
    threshold, and margin, calculates the two displayed edges, and translates the state
    to its readable screening status.
    """
    classification = result.classification
    return ThresholdContext(
        segment_id=result.segment_id,
        probability=classification.anomaly_probability,
        threshold=classification.classification_threshold,
        uncertainty_margin=classification.uncertainty_margin,
        lower_bound=(
            classification.classification_threshold - classification.uncertainty_margin
        ),
        upper_bound=(
            classification.classification_threshold + classification.uncertainty_margin
        ),
        status=status_for_decision(classification.decision_state),
    )


# ---


# --- logic_facts_frame()
def logic_facts_frame(result: CompleteAnalysisResult) -> pd.DataFrame:
    """Distinguish starting facts from rule-derived and consistency-check conclusions.

    The rule engine has already produced both groups. Formatting their predicates as text
    makes their origin visible without turning Boolean facts into probability estimates.

    Args:
        result: CompleteAnalysisResult object.

    Returns:
        Pandas DataFrame containing the logic facts frame.
    """
    # Start with the numerical and historical facts asserted before rule derivation.
    rows = [
        {"Fact role": "Starting fact", "Fact": str(fact)}
        for fact in result.reasoning.asserted_facts
    ]
    # Label the backend's derived conclusions separately from its starting evidence.
    rows.extend(
        {"Fact role": "Derived by a rule", "Fact": str(fact)}
        for fact in result.reasoning.derived_facts
    )
    # Return fact text with its origin so the page can explain the reasoning stages.
    return pd.DataFrame.from_records(
        rows,
        columns=("Fact role", "Fact"),
    )


# ---


# --- logic_trace_frame()
def logic_trace_frame(result: CompleteAnalysisResult) -> pd.DataFrame:
    """Format the recorded rule applications and consistency checks.

    Each trace connects supporting facts, variable bindings, and one conclusion. Keeping
    those fields together lets a reader follow the existing reasoning; this helper does
    not match premises or add facts itself.

    Args:
        result: CompleteAnalysisResult object.

    Returns:
        Pandas DataFrame containing the logic trace frame.
    """
    # Expose the recorded reasoning chain without rerunning premise matching.
    return pd.DataFrame.from_records(
        [
            # Keep each recorded conclusion with the facts and bindings that support it.
            {
                "Rule": trace.rule_id,
                "Matched facts": "; ".join(
                    str(fact) for fact in trace.matched_premises
                ),
                "Variable bindings": (
                    ", ".join(f"{name} = {value}" for name, value in trace.bindings)
                    or "No variables"
                ),
                "Conclusion": str(trace.conclusion),
                "Why it fired": trace.explanation,
                "Source status": trace.source_status,
            }
            for trace in result.reasoning.traces
        ],
        # Use a consistent evidence-to-conclusion order for all recorded traces.
        columns=(
            "Rule",
            "Matched facts",
            "Variable bindings",
            "Conclusion",
            "Why it fired",
            "Source status",
        ),
    )


# ---


# ________________________________________________
# Simulated planning tables
# ------------------------------------------------
# Catalog membership and selected-path states explain the plan already returned by A*.
# Path reconstruction reuses its ordered actions and heuristic without starting another search.


# --- planning_actions_frame()
def planning_actions_frame(result: CompleteAnalysisResult) -> pd.DataFrame:
    """List the simulated action catalog and mark actions in the chosen plan.

    The catalog supplies descriptions, preconditions, effects, and coursework costs. The
    backend's selected action IDs supply the Yes/No membership column. Listing an action
    or marking it selected does not execute a diagnostic check.

    Args:
        result: CompleteAnalysisResult object.

    Returns:
        Pandas DataFrame containing the planning actions frame.
    """
    # Use backend-selected action IDs to mark membership in the displayed catalog.
    selected_ids = {
        planned_action.action.action_id
        for planned_action in result.plan.ordered_actions
    }
    return pd.DataFrame.from_records(
        [
            {
                "Action": action.action_id,
                "Description": action.description,
                "Preconditions": ", ".join(sorted(action.preconditions)) or "None",
                "Effects": ", ".join(sorted(action.effects)),
                "Cost": action.cost,
                "Selected": "Yes" if action.action_id in selected_ids else "No",
            }
            for action in build_diagnostic_actions()
        ],
        # Keep simulated action requirements, effects, costs, and membership directly comparable.
        columns=(
            "Action",
            "Description",
            "Preconditions",
            "Effects",
            "Cost",
            "Selected",
        ),
    )


# ---


# --- _planning_state_label()
def _planning_state_label(state: PlanningState) -> str:
    """Summarize completed and remaining checks for one displayed candidate state.

    Args:
        state: PlanningState object.
        
    Returns:
        String containing the planning state label.
    """
    # Describe the checks already present in this simulated candidate state.
    completed = ", ".join(sorted(state.completed_checks)) or "none"
    # Show only required checks that the candidate has not yet completed.
    remaining = ", ".join(
        sorted(state.required_checks - state.completed_checks),
    ) or "none"
    # Pair completed and outstanding checks in the candidate-state table cell.
    return f"completed: {completed}; remaining: {remaining}"


# ---


# --- planning_path_frame()
def planning_path_frame(result: CompleteAnalysisResult) -> pd.DataFrame:
    """Reconstruct the selected planning path for its state-and-cost table.

    This table follows the action sequence already chosen by A*. It does not search again
    or include every state expanded during the original search. Each step copies the
    previous planning state with that action's effects added to completed checks.

    The backend plan supplies cumulative cost g(n). Its shared heuristic estimates the
    remaining cost h(n), and their sum gives the displayed f(n). These are simulated
    coursework costs rather than measured time or money.

    Args:
        result: CompleteAnalysisResult object.

    Returns:
        Pandas DataFrame containing the planning path frame.
    """
    # Use the shared simulated action costs when displaying the backend heuristic.
    actions = build_diagnostic_actions()
    # Start from the initial state stored in this selected segment's plan.
    state = result.plan.initial_state
    # Calculate the displayed starting heuristic with the existing backend helper.
    start_h = estimate_remaining_cost(state, actions)
    # Before any selected action, accumulated cost is zero and f(n) equals h(n).
    rows: list[dict[str, object]] = [
        {
            "Step": 0,
            "Selected action": "Start state",
            "Candidate state": _planning_state_label(state),
            "g(n) accumulated": 0.0,
            "h(n) remaining estimate": start_h,
            "f(n) total estimate": start_h,
        },
    ]
    # Reconstruct only the chosen sequence; expanded alternatives are not stored in this table.
    for step, planned_action in enumerate(result.plan.ordered_actions, start=1):
        # Apply this selected action's effects to the displayed copy of the prior state.
        state = PlanningState(
            route=state.route,
            triggered_requirements=state.triggered_requirements,
            required_checks=state.required_checks,
            completed_checks=state.completed_checks | planned_action.action.effects,
            suspected_faults=state.suspected_faults,
        )
        # Reuse the backend heuristic for the remaining checks at this displayed step.
        h_value = estimate_remaining_cost(state, actions)
        # Pair each reconstructed state with its stored cumulative and estimated remaining costs.
        rows.append(
            {
                "Step": step,
                "Selected action": planned_action.action.action_id,
                "Candidate state": _planning_state_label(state),
                "g(n) accumulated": planned_action.cumulative_cost,
                "h(n) remaining estimate": h_value,
                "f(n) total estimate": planned_action.cumulative_cost + h_value,
            },
        )
    # Expose only the selected action sequence and its state-and-cost explanation.
    return pd.DataFrame.from_records(
        rows,
        columns=(
            "Step",
            "Selected action",
            "Candidate state",
            "g(n) accumulated",
            "h(n) remaining estimate",
            "f(n) total estimate",
        ),
    )


# ---


# ________________________________________________
# Architecture metadata
# ------------------------------------------------
# This maintained teaching map names module responsibilities and course lineage.
# Its rows describe structure rather than recording which modules ran for a selected stage.


# --- architecture_map_frame()
def architecture_map_frame() -> pd.DataFrame:
    """Map visible workflow responsibilities to their current source modules.

    The rows identify inputs, outputs, ownership, and course lineage for the learner.
    They are an explicit explanatory map, not a trace collected from the current run;
    a listed module is not evidence that it executed for this selected stage.

    Returns:
        Pandas DataFrame containing the architecture map frame.
    """
    # List explanatory ownership and course lineage for the current module structure.
    rows = (
        # Row 1: Problem and human decision.
        (
            "Problem and human decision",
            "CubeSat telemetry use case",
            "Human-review objective",
            "Milestone Module 2 and README.md",
            "Design evidence",
            "Module 2",
        ),
        # Row 2: Data validation and roles.
        (
            "Data validation and roles",
            "Local OPS-SAT-AD comma-separated value (CSV) files",
            "Checked dataset with training, validation, and test groups",
            "cubesat_data.py",
            "Backend",
            "Modules 2 and 5",
        ),
        # Row 3: MLP fitting and classification.
        (
            "MLP fitting and classification",
            "18 numerical features and labels",
            "Probability, threshold, and metrics",
            "cubesat_model.py",
            "Backend",
            "Modules 3 and 5",
        ),
        # Row 4: Historical similarity.
        (
            "Historical similarity",
            "Selected feature values and historical training examples",
            "Similar normal and anomalous examples in separate groups",
            "cubesat_similarity.py",
            "Backend",
            "Module 4",
        ),
        # Row 5: Logic and expert system.
        (
            "Logic and expert system",
            "Numerical and similarity evidence",
            "Facts, traces, and hypotheses",
            "cubesat_logic.py",
            "Backend",
            "Module 6",
        ),
        # Row 6: A-star planning.
        (
            "A-star planning",
            "Planning state, actions, costs, and goal",
            "Simulated advisory action sequence",
            "cubesat_planner.py",
            "Backend",
            "Module 4",
        ),
        # Row 7: Analysis coordination.
        (
            "Analysis coordination",
            "Selected segment",
            "CompleteAnalysisResult (the combined results for one segment)",
            "cubesat_telemetry_ai.py",
            "Backend",
            "Module 8 integration",
        ),
        # Row 8: Presentation adapter.
        (
            "Presentation adapter",
            "Validated backend objects",
            "Tables, chart, and walkthrough records",
            "cubesat_frontend.py",
            "Frontend",
            "Module 8 integration",
        ),
        # Row 9: Interactive pages.
        (
            "Interactive pages",
            "Presentation records and user selections",
            "Screening and learner walkthrough",
            "streamlit_app.py and app_pages/",
            "Frontend",
            "Module 8 integration",
        ),
    )
    # Return the architecture map with stage inputs, outputs, ownership, and course lineage.
    return pd.DataFrame.from_records(
        rows,
        columns=("Stage", "Input", "Output", "Current source", "Layer", "Course lineage"),
    )


# ---


# __________________________________________
# END OF FILE
# ==========================================
