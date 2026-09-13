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
# - Validate local telemetry files and keep features aligned with their metadata.
# - Assign row roles and resolve the segment or demonstration selected by the user.
#
# Usage / Integration:
# - Imported by cubesat_telemetry_ai, cubesat_frontend, and verification/tests.
# - Returns data records or controlled errors before model fitting and inference.
#
# Contents Overview:
# - Artifact checks for dataset.csv and the raw readings in segments.csv.
# - CSV field/profile validation and load_telemetry_dataset().
# - create_dataset_partitions(), segment selection, and demo scenario loading.
#
# Dependencies:
# - Standard Library: csv, hashlib, json, math, pathlib.
# - Third-Party: NumPy, scikit-learn.
# - Local Project: cubesat_config, cubesat_types.
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Load, validate, partition, and select OPS-SAT-AD telemetry rows.

A telemetry segment is a group of readings summarized as one model example. In `dataset.csv`, each
segment has 18 numerical features, such as statistics describing the readings. This module checks
those values before the numerical pipeline receives them.

The segment ID, channel, sampling value, reviewed label, and official split remain beside the
features as metadata. Labels support training and evaluation; they are never part of the 18 model
inputs. All returned columns preserve the same row order.
"""

# ____________________________________________________________________________________
# ====================================================================================
#
# DATA REPRESENTATION AND SPLIT MAP
#
# X[i, j] -> x_validated_telemetry_features[i, j]
#            Feature j for segment i; m rows and 18 feature columns.
# y[i]    -> y_anomaly_labels[i]; 0 is reviewed normal and 1 is reviewed anomalous.
# train[i] -> benchmark_training_flags[i]; the source's training/test assignment.
#
#                        Validated segment rows
#                         /                  \
#                Official training       Held-out test
#                 /            \          Final evaluation
#          Model training   Validation
#          Fit the model    Choose the classification threshold
#
# Historical references contain all official training rows, including validation
# rows. This is an overlapping comparison role, not a fourth disjoint partition.
# Every role uses the same feature names and row identifiers.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

import csv # Used for reading the CSV files.
import hashlib # Used for calculating the MD5 and SHA-256 hashes of the files.
import json # Used for reading the JSON files.
import math # Used for calculating the number of rows in the CSV files.
from pathlib import Path # Used for working with file paths.

# pyrefly: ignore [missing-import]
import numpy as np # Used for numerical operations.
from sklearn.model_selection import train_test_split # Used for splitting the data into training and testing sets.

# Import constants from cubesat_config.
from cubesat_config import (
    AUTHENTIC_ANOMALOUS_ROW_COUNT, # The number of anomalous rows in the authentic dataset.
    AUTHENTIC_ROW_COUNT, # The total number of rows in the authentic dataset.
    AUTHENTIC_SEGMENTS_LABEL_VALUES, # The values of the labels in the authentic dataset.
    AUTHENTIC_SEGMENTS_ROW_COUNT, # The number of rows in the authentic dataset.
    AUTHENTIC_TEST_ROW_COUNT, # The number of test rows in the authentic dataset.
    AUTHENTIC_TRAINING_ROW_COUNT, # The number of training rows in the authentic dataset.
    DATASET_MD5, # The MD5 hash of the authentic dataset.
    DATASET_SHA256, # The SHA-256 hash of the authentic dataset.
    DATASET_SIZE_BYTES, # The size of the authentic dataset in bytes.
    DEFAULT_CONFIG, # The default configuration for the program.
    REQUIRED_COLUMNS, # The required columns for the dataset.
    SEGMENTS_MD5, # The MD5 hash of the segments dataset.
    SEGMENTS_REQUIRED_COLUMNS, # The required columns for the segments dataset.
    SEGMENTS_SHA256, # The SHA-256 hash of the segments dataset.
    SEGMENTS_SIZE_BYTES, # The size of the segments dataset in bytes.
    AppConfig, # The configuration for the program.
)
# Import types from cubesat_types.
from cubesat_types import (
    ArtifactVerification, # Dataclass to hold artifact verification results.
    DatasetPartitions, # Dataclass to hold dataset partitions.
    DatasetValidationError, # Custom exception raised when the dataset is invalid.
    SegmentSelectionError, # Custom exception raised when the segment selection is invalid.
    SegmentsVerification, # Dataclass to hold segments verification results.
    TelemetryDataset, # Class to hold the telemetry dataset.
)

# __________________________________________
# ARTIFACT INTEGRITY
# ==========================================


# --- calculate_artifact_verification()
def calculate_artifact_verification(artifact_path: Path) -> ArtifactVerification:
    """Calculate one local artifact's byte size, published MD5, and SHA-256 evidence.

    MD5 is retained only because Zenodo publishes it for artifact identity. SHA-256 supplies the
    stronger locally reviewed digest.

    Args:
        artifact_path: Local file to inspect; a leading `~` is expanded.

    Returns:
        Observed path, byte count, and digests. This calculation does not compare a baseline.

    Raises:
        DatasetValidationError: If the artifact is missing or unreadable.
    """
    # Expand the path to a local file.
    resolved_path = artifact_path.expanduser()
    # Check if the artifact is a file.
    if not resolved_path.is_file():
        raise DatasetValidationError(f"data artifact not found: {resolved_path}")

    # Calculate the MD5 hash of the artifact.
    md5_digest = hashlib.md5(usedforsecurity=False) # MD5 hash for the artifact.
    # Calculate the SHA-256 hash of the artifact.
    sha256_digest = hashlib.sha256() # SHA-256 hash for the artifact.
    # Initialize the size of the artifact.
    size_bytes = 0 # Size of the artifact in bytes.
    try: # Try to open the artifact file.
        with resolved_path.open("rb") as artifact_file: # Open the artifact file in binary read mode.
            # Read one MiB at a time so hashing raw telemetry does not require
            # keeping the complete file in memory. Both digests see identical bytes.
            while chunk := artifact_file.read(1_048_576): # Read one MiB at a time so hashing raw telemetry does not require
                # keeping the complete file in memory. Both digests see identical bytes.
                size_bytes += len(chunk) # Add the size of the chunk to the size of the artifact.
                md5_digest.update(chunk) # Update the MD5 hash of the artifact.
                sha256_digest.update(chunk) # Update the SHA-256 hash of the artifact.
    except OSError as exc: # If the artifact file cannot be opened.
        raise DatasetValidationError(f"unable to read data artifact: {exc}") from exc

    return ArtifactVerification(
        path=resolved_path, # The path to the artifact.
        size_bytes=size_bytes, # The size of the artifact in bytes.
        md5=md5_digest.hexdigest(), # The MD5 hash of the artifact.
        sha256=sha256_digest.hexdigest(), # The SHA-256 hash of the artifact.
    )
# ---


# --- _require_artifact_identity() ---
def _require_artifact_identity(
    artifact: ArtifactVerification,
    *,
    artifact_name: str,
    expected_size_bytes: int,
    expected_md5: str,
    expected_sha256: str,
) -> None:
    """Reject a local file that differs from the exact reviewed Zenodo v2 artifact.

    The expected values identify one published file version. Matching them checks the file's
    bytes; the CSV functions still check how those bytes are interpreted as rows and columns.

    Args:
        artifact: Observed size and digests from the local file.
        artifact_name: Dataset name included in the error message.
        expected_size_bytes: Pinned byte count for the reviewed file.
        expected_md5: Published MD5 checksum for that file.
        expected_sha256: Locally reviewed SHA-256 digest for the same bytes.

    Raises:
        DatasetValidationError: If size, MD5, or SHA-256 differs from the pinned baseline.
    """
    # Collect every difference so one error explains the full identity mismatch.
    mismatches: list[str] = [] # List to hold any mismatches found. (Note: This may need to be reworded to be more clear.)

    # Check if the artifact size matches the expected size.
    if artifact.size_bytes != expected_size_bytes: # Check if the artifact size matches the expected size.
        mismatches.append(
            f"size observed {artifact.size_bytes}, expected {expected_size_bytes}", # Append the size mismatch to the list of mismatches. (Note: This may need to be reworded to be more clear.)
        )
    # Check if the artifact MD5 hash matches the expected MD5 hash.
    if artifact.md5 != expected_md5: # Check if the artifact MD5 hash matches the expected MD5 hash.
        mismatches.append(f"MD5 observed {artifact.md5}, expected {expected_md5}") # Append the MD5 mismatch to the list of mismatches. (Note: This may need to be reworded to be more clear.)
    # Check if the artifact SHA-256 hash matches the expected SHA-256 hash.
    if artifact.sha256 != expected_sha256: # Check if the artifact SHA-256 hash matches the expected SHA-256 hash.
        mismatches.append(
            f"SHA-256 observed {artifact.sha256}, expected {expected_sha256}", # Append the SHA-256 mismatch to the list of mismatches. (Note: This may need to be reworded to be more clear.)
        )
    # If there are any mismatches, raise a DatasetValidationError.
    if mismatches: # If there are any mismatches.
        raise DatasetValidationError(
            f"authentic {artifact_name} artifact mismatch: " + "; ".join(mismatches), # Raise a DatasetValidationError with the list of mismatches. (Note: This may need to be reworded to be more clear.)
        )
# --- 


# --- verify_authentic_dataset_artifact() ---
def verify_authentic_dataset_artifact(dataset_path: Path) -> ArtifactVerification:
    """Verify exact Zenodo v2 `dataset.csv` size, MD5, and SHA-256.

    Returns:
        The observed artifact evidence after all three pinned values match.

    Raises:
        DatasetValidationError: If the file is unreadable or differs from the reviewed artifact.
    """
    # Calculate the artifact verification for the dataset path.
    artifact = calculate_artifact_verification(dataset_path)
    # Require the artifact identity for the dataset path.
    _require_artifact_identity(
        artifact,
        artifact_name="dataset.csv", # The name of the artifact.
        expected_size_bytes=DATASET_SIZE_BYTES, # The expected size of the artifact in bytes.
        expected_md5=DATASET_MD5, # The expected MD5 hash of the artifact.
        expected_sha256=DATASET_SHA256, # The expected SHA-256 hash of the artifact.
    )
    # Return the artifact verification.
    return artifact
# ---


# __________________________________________
# ARRAY AND FIELD VALIDATION
# ==========================================


# --- _as_read_only_array()
def _as_read_only_array(array: np.ndarray) -> np.ndarray:
    """Copy an array and disable writes to the returned numerical data.

    The copy separates the stored dataset from the caller's original array. The write flag helps
    catch accidental changes after row alignment and value validation are complete.
    """
    # Create a copy of the array.
    owned_array = np.array(array, copy=True) # Copy the array to prevent accidental changes.
    # Set the array to read-only.
    owned_array.setflags(write=False) # Set the array to read-only to prevent accidental changes.
    # Return the owned array.
    return owned_array
# ---


# --- _parse_binary_field()
def _parse_binary_field(raw_value: str, *, field_name: str, row_number: int) -> int:
    """Parse one required `0` or `1` field with a row-specific error.

    The schema uses these exact strings for both the reviewed anomaly label and the official
    training flag. `row_number` counts CSV records with the header counted as row one.

    Raises:
        DatasetValidationError: If the value is not exactly `0` or `1`.
    """
    if raw_value not in {"0", "1"}: # Check if the raw value is not "0" or "1".
        raise DatasetValidationError(
            f"row {row_number}: {field_name} must be 0 or 1; received {raw_value!r}", # Raise a DatasetValidationError with the row number and field name. (Note: This may need to be reworded to be more clear.)
        )
    return int(raw_value) # Return the integer value of the raw value.
# ---


# --- _parse_finite_feature()
def _parse_finite_feature(raw_value: str, *, feature_name: str, row_number: int) -> float:
    """Convert one feature to a finite floating-point value.

    Raises:
        DatasetValidationError: If conversion fails or the result is non-finite.
    """
    try:
        feature_value = float(raw_value)
    except (TypeError, ValueError) as exc: # If the raw value cannot be converted to a float.
        raise DatasetValidationError(
            f"row {row_number}: feature {feature_name!r} must be numeric", # Raise a DatasetValidationError with the row number and feature name. (Note: This may need to be reworded to be more clear.)
        ) from exc

    # VALIDATION: float() accepts NaN and infinity, but neither is a usable model input.
    if not math.isfinite(feature_value): # Check if the feature value is finite.
        raise DatasetValidationError(
            f"row {row_number}: feature {feature_name!r} must be finite", # Raise a DatasetValidationError with the row number and feature name. (Note: This may need to be reworded to be more clear.)
        )
    # Return the feature value.
    return feature_value
# ---


# --- _validate_dataset_profile()
def _validate_dataset_profile(dataset: TelemetryDataset, config: AppConfig) -> None:
    """Validate authentic benchmark counts or the bounded fixture profile.

    Authentic data must match the pinned population and channels. Fixture data has minimum row
    counts and must contain both classes; this function does not require the exact bundled fixture
    digest or exactly 50 rows. The standalone verifier checks the bundled fixture's identity.

    Raises:
        DatasetValidationError: If the selected profile is incompatible with the data.
    """
    row_count = len(dataset.segment_ids) # Get the number of segment IDs.
    training_count = int(np.count_nonzero(dataset.benchmark_training_flags)) # Get the number of training flags.
    test_count = row_count - training_count # Get the number of test rows.
    anomalous_count = int(np.count_nonzero(dataset.y_anomaly_labels)) # Get the number of anomalous rows.

    # These population checks add schema context to the earlier byte-identity check.
    if dataset.profile_name == "authentic": # Check if the dataset profile is authentic.
        expected_observations = (
            ("rows", row_count, AUTHENTIC_ROW_COUNT), # Expected number of rows.
            ("training rows", training_count, AUTHENTIC_TRAINING_ROW_COUNT), # Expected number of training rows.
            ("test rows", test_count, AUTHENTIC_TEST_ROW_COUNT), # Expected number of test rows.
            ("anomalous rows", anomalous_count, AUTHENTIC_ANOMALOUS_ROW_COUNT), # Expected number of anomalous rows.
        )
        # Identify mismatches between observed and expected values.
        mismatches = [
            f"{name}: observed {observed}, expected {expected}"
            for name, observed, expected in expected_observations
            if observed != expected # Check if the observed value is not equal to the expected value.
        ]
        # Get the observed channels.
        observed_channels = set(dataset.channels)
        # Check if the observed channels match the expected channels.
        if observed_channels != set(config.expected_channels): # Check if the observed channels match the expected channels.
            # Append the channel mismatches to the list of mismatches.
            mismatches.append(
                "channels: observed "
                f"{sorted(observed_channels)}, expected {sorted(config.expected_channels)}",
            )
        # Raise a DatasetValidationError with the list of mismatches if there are any.
        if mismatches: # Check if there are any mismatches.
            raise DatasetValidationError(
                "authentic OPS-SAT-AD v2 profile mismatch: " + "; ".join(mismatches),
            )
        return

    # Check if the dataset profile is not "fixture".
    if dataset.profile_name != "fixture": # Check if the dataset profile is not "fixture".
        raise DatasetValidationError("dataset profile must be 'authentic' or 'fixture'")
    # Check if the row count is less than 20 or the training count is less than 16 or the test count is less than 2.
    if row_count < 20 or training_count < 16 or test_count < 2: # Check if the row count is less than 20 or the training count is less than 16 or the test count is less than 2.
        raise DatasetValidationError(
            "fixture requires at least 20 rows, 16 training rows, and 2 test rows",
        )
    # Check if the set of unique anomaly labels is not equal to {0, 1}.
    if set(np.unique(dataset.y_anomaly_labels)) != {0, 1}: # Check if the set of unique anomaly labels is not equal to {0, 1}.
        raise DatasetValidationError("fixture must include both normal and anomalous labels")
# ---


# __________________________________________
# DATASET LOADING
# ==========================================


# --- load_telemetry_dataset()
def load_telemetry_dataset(
    dataset_path: Path, # Path to the dataset file.
    *,
    profile_name: str, # Name of the dataset profile.
    config: AppConfig = DEFAULT_CONFIG, # Configuration for the dataset. 
) -> TelemetryDataset:
    """Load and validate one OPS-SAT-AD-compatible CSV file.

    Args:
        dataset_path: CSV path supplied by the coordinator or CLI.
        profile_name: Strict `authentic` profile or bounded `fixture` profile.
        config: Shared runtime and schema configuration.

    Returns:
        A validated dataset with read-only numerical arrays.

    Raises:
        DatasetValidationError: If the path, schema, row values, or profile is invalid.

    Logic:
        1. Verify the exact artifact identity in authentic mode.
        2. Validate the file and exact reviewed column order.
        3. Parse identifiers, labels, split flags, channels, and 18 finite features.
        4. Reject duplicate identifiers or unsupported channels.
        5. Validate the authentic or bounded fixture profile.
    """
    # __________________________________________
    # SOURCE AND VALIDATION PROFILE
    # ==========================================
    # PHASE 1: Establish which local file and validation profile the caller selected.
    # Resolve the dataset path to an absolute path.
    resolved_path = dataset_path.expanduser()
    # Check if the dataset file exists.
    if not resolved_path.is_file(): # Check if the dataset file exists.
        # Raise a DatasetValidationError with the path to the dataset file.
        raise DatasetValidationError(
            f"dataset file not found: {resolved_path}. See data/README.md for preparation steps.",
        ) # Raise a DatasetValidationError with the path to the dataset file.
        
    if profile_name == "authentic": # Check if the dataset profile is authentic.
        # Verify the authentic dataset artifact.
        verify_authentic_dataset_artifact(resolved_path) # Verify the authentic dataset artifact.

    # Initialize lists to store dataset values.
    segment_ids: list[str] = [] # List to store segment identifiers.
    channels: list[str] = [] # List to store channel identifiers.
    sampling_values: list[str] = [] # List to store sampling values.
    anomaly_labels: list[int] = [] # List to store anomaly labels.
    training_flags: list[bool] = [] # List to store training flags.
    feature_rows: list[list[float]] = [] # List to store feature values.
    seen_segment_ids: set[str] = set() # Set to store seen segment identifiers.

    try: # Try to open and read the dataset file.
        with resolved_path.open("r", encoding="utf-8", newline="") as source_file: # Open the dataset file for reading.
            reader = csv.DictReader(source_file) # Create a CSV reader.
            # __________________________________________
            # ORDERED SCHEMA VALIDATION
            # ==========================================
            # PHASE 2: Require the reviewed schema, including its column order.
            # A feature name and its position must mean the same thing at every stage.
            if reader.fieldnames != list(REQUIRED_COLUMNS): # Check if the dataset columns are incompatible.
                # Raise a DatasetValidationError with the list of mismatches.
                raise DatasetValidationError(
                    "dataset columns are incompatible; observed "
                    f"{reader.fieldnames}, expected {list(REQUIRED_COLUMNS)}",
                )

            # __________________________________________
            # COMPLETE ROW VALIDATION
            # ==========================================
            # PHASE 3: Validate a complete segment before appending any of its values.
            # The header counts as row 1, so the first data record is reported as row 2.
            for row_number, row in enumerate(reader, start=2): # Enumerate the rows starting from row 2.
                segment_id = (row.get("segment") or "").strip() # Get the segment identifier.
                # Raise a DatasetValidationError with the row number if the segment identifier is empty.
                if not segment_id: # Check if the segment identifier is empty.
                    raise DatasetValidationError(f"row {row_number}: segment identifier is empty") # Raise a DatasetValidationError with the row number if the segment identifier is empty.
                # VALIDATION: Exact-ID selection must identify one row without ambiguity.
                if segment_id in seen_segment_ids: # Check if the segment identifier has been seen before.
                    # Raise a DatasetValidationError with the row number if the segment identifier has been seen before.
                    raise DatasetValidationError(
                        f"row {row_number}: duplicate segment identifier {segment_id!r}",
                    )

                channel = (row.get("channel") or "").strip()
                # Raise a DatasetValidationError with the row number if the channel is not supported.
                if channel not in config.expected_channels: # Check if the channel is supported.
                    raise DatasetValidationError(
                        f"row {row_number}: unsupported channel {channel!r}",
                    ) # Raise a DatasetValidationError with the row number if the channel is not supported.
                sampling = (row.get("sampling") or "").strip() # Get the sampling value.
                # Raise a DatasetValidationError with the row number if the sampling value is empty.
                if not sampling: # Check if the sampling value is empty.
                    raise DatasetValidationError(f"row {row_number}: sampling value is empty") # Raise a DatasetValidationError with the row number if the sampling value is empty.

                anomaly_label = _parse_binary_field( # Parse the anomaly label.
                    row["anomaly"],
                    field_name="anomaly",
                    row_number=row_number,
                ) # Parse the anomaly label.
                training_flag = _parse_binary_field( # Parse the training flag.
                    row["train"],
                    field_name="train",
                    row_number=row_number,
                ) # Parse the training flag.
                # Only these 18 feature columns become numerical model inputs.
                # The label, source split, and channel stay in separate metadata columns.
                feature_row = [
                    _parse_finite_feature(
                        row[feature_name],
                        feature_name=feature_name,
                        row_number=row_number,
                    )
                    for feature_name in config.expected_feature_names
                ]

                seen_segment_ids.add(segment_id) # Add the segment identifier to the set of seen segment identifiers.
                # INVARIANT: Position i stays aligned across the metadata lists and feature_rows.
                segment_ids.append(segment_id) # Add the segment identifier to the list of segment identifiers.
                channels.append(channel) # Add the channel to the list of channels.
                sampling_values.append(sampling) # Add the sampling value to the list of sampling values.
                anomaly_labels.append(anomaly_label) # Add the anomaly label to the list of anomaly labels.
                training_flags.append(bool(training_flag)) # Add the training flag to the list of training flags.
                feature_rows.append(feature_row) # Add the feature row to the list of feature rows.
    except OSError as exc:
        raise DatasetValidationError(f"unable to read dataset: {exc}") from exc

    if not segment_ids:
        raise DatasetValidationError("dataset contains no telemetry rows")

    # __________________________________________
    # DATASET CONSTRUCTION AND PROFILE CHECK
    # ==========================================
    # PHASE 4: Store stable metadata and owned arrays with shapes (m,) and (m, 18).
    dataset = TelemetryDataset( # Create a TelemetryDataset instance.
        source_path=resolved_path, # Source path to the dataset file.
        profile_name=profile_name, # Profile name for the dataset.
        segment_ids=tuple(segment_ids), # Tuple of segment identifiers.
        channels=tuple(channels), # Tuple of channel identifiers.
        sampling_values=tuple(sampling_values), # Tuple of sampling values.
        y_anomaly_labels=_as_read_only_array(np.asarray(anomaly_labels, dtype=np.int64)), # Array of anomaly labels.
        benchmark_training_flags=_as_read_only_array(
            np.asarray(training_flags, dtype=np.bool_),
        ), # Array of training flags.
        x_validated_telemetry_features=_as_read_only_array(
            np.asarray(feature_rows, dtype=np.float64),
        ), # Array of telemetry features.
        feature_names=config.expected_feature_names, # Tuple of feature names.
        simulated=profile_name == "fixture", # Boolean indicating if the dataset is simulated.
    ) # Create a TelemetryDataset instance.
    # PHASE 5: Check the completed population after individual records have passed.
    _validate_dataset_profile(dataset, config) # Validate the dataset profile.
    return dataset
# ---


# --- verify_authentic_segments_artifact()
def verify_authentic_segments_artifact(
    segments_path: Path,
    dataset: TelemetryDataset,
) -> SegmentsVerification:
    """Verify and cross-check the exact Zenodo v2 raw telemetry segments.

    `segments.csv` contains repeated raw readings for each segment; `dataset.csv` contains one
    extracted feature row for that segment. This check connects their metadata. It does not
    recreate the 18 features or interpret the timestamp text as a chronological series.

    Args:
        segments_path: Local `segments.csv` beside the prepared feature dataset.
        dataset: Already validated authentic `dataset.csv` representation.

    Returns:
        Exact artifact evidence plus observed row, segment, channel, and label profile.

    Raises:
        DatasetValidationError: If identity, schema, values, metadata, or profile differs.

    Logic:
        1. Verify exact size, MD5, and SHA-256.
        2. Validate the raw-segment schema and finite telemetry values.
        3. Require stable metadata for every segment and cross-check it with `dataset.csv`.
        4. Confirm 303,493 rows cover the same 2,123 segments and nine channels.
    """
    # Check if the dataset profile is authentic.
    if dataset.profile_name != "authentic":
        raise DatasetValidationError("segments.csv cross-check requires an authentic dataset") # Raise a DatasetValidationError if the dataset profile is not authentic.

    artifact = calculate_artifact_verification(segments_path) # Calculate the artifact verification.
    _require_artifact_identity( # Require exact identity for the artifact.
        artifact,
        artifact_name="segments.csv", # Name of the artifact.
        expected_size_bytes=SEGMENTS_SIZE_BYTES, # Expected size in bytes.
        expected_md5=SEGMENTS_MD5, # Expected MD5 hash.
        expected_sha256=SEGMENTS_SHA256, # Expected SHA-256 hash.
    )

    # Use the already validated feature rows as the segment-to-metadata lookup.
    # The same segment can appear many times in the raw readings, but its role stays fixed.
    expected_metadata = { # Dictionary mapping segment identifiers to their metadata.
        segment_id: (
            dataset.channels[index], # Channel identifier.
            dataset.sampling_values[index], # Sampling value.
            int(dataset.y_anomaly_labels[index]), # Anomaly label.
            int(dataset.benchmark_training_flags[index]), # Training flag.
        )
        for index, segment_id in enumerate(dataset.segment_ids)
    }
    observed_metadata: dict[str, tuple[str, str, int, int, str]] = {} # Dictionary to store observed metadata.
    observed_label_values: set[str] = set() # Set to store observed label values.
    observed_channels: set[str] = set() # Set to store observed channel identifiers.
    row_count = 0

    try: # Try to open and read the dataset file.
        with artifact.path.open("r", encoding="utf-8", newline="") as source_file: # Open the dataset file.
            reader = csv.DictReader(source_file) # Create a DictReader instance.
            if reader.fieldnames != list(SEGMENTS_REQUIRED_COLUMNS): # Check if the fieldnames match the expected fieldnames.
                raise DatasetValidationError(
                    "segments.csv columns are incompatible; observed " # Raise a DatasetValidationError if the fieldnames do not match.
                    f"{reader.fieldnames}, expected {list(SEGMENTS_REQUIRED_COLUMNS)}",
                )

            for row_number, row in enumerate(reader, start=2): # Iterate over the rows in the dataset file.
                row_count += 1
                segment_id = (row.get("segment") or "").strip()
                if segment_id not in expected_metadata: # Check if the segment identifier is in the expected metadata.
                    raise DatasetValidationError(
                        f"segments.csv row {row_number}: unknown segment {segment_id!r}",
                    )
                channel = (row.get("channel") or "").strip()
                sampling = (row.get("sampling") or "").strip()
                timestamp = (row.get("timestamp") or "").strip()
                label_name = (row.get("label") or "").strip()
                # VALIDATION: Timestamps must be present. Their format and ordering are
                # not parsed here, so this check cannot establish temporal relationships.
                if not channel or not sampling or not timestamp or not label_name: # Check if the metadata fields are non-empty.
                    raise DatasetValidationError(
                        f"segments.csv row {row_number}: metadata fields must be non-empty",
                    )
                anomaly_label = _parse_binary_field( # Parse the anomaly label.
                    row["anomaly"],
                    field_name="segments anomaly", # Name of the anomaly field.
                    row_number=row_number, # Row number.
                )
                training_flag = _parse_binary_field( # Parse the training flag.
                    row["train"],
                    field_name="segments train",
                    row_number=row_number, # Row number.
                )
                _parse_finite_feature( # Parse the feature value.
                    row["value"],
                    feature_name="segments value",
                    row_number=row_number, # Row number.
                )

                compact_metadata = (channel, sampling, anomaly_label, training_flag) # Compact metadata.
                if compact_metadata != expected_metadata[segment_id]: # Check if the metadata agrees with the expected metadata.
                    raise DatasetValidationError(
                        f"segments.csv row {row_number}: metadata disagrees with dataset.csv "
                        f"for segment {segment_id!r}",
                    )
                # Remember the first reading's label as well as its shared metadata.
                # Later readings from this segment must agree with that first record.
                complete_metadata = (*compact_metadata, label_name) # Complete metadata.
                previous_metadata = observed_metadata.setdefault(segment_id, complete_metadata) # Set the previous metadata.
                if previous_metadata != complete_metadata: # Check if the previous metadata agrees with the complete metadata.
                    raise DatasetValidationError(
                        f"segments.csv row {row_number}: inconsistent metadata within segment "
                        f"{segment_id!r}",
                    )
                observed_label_values.add(label_name) # Add the label name to the set.
                observed_channels.add(channel) # Add the channel identifier to the set.
    except OSError as exc: # Catch OSError.
        raise DatasetValidationError(f"unable to read segments.csv: {exc}") from exc

    # A valid individual reading does not prove complete coverage. Check the whole
    # raw file against the reviewed row count, segment set, channels, and label names.
    mismatches: list[str] = []
    if row_count != AUTHENTIC_SEGMENTS_ROW_COUNT: # Check if the row count matches the expected row count.
        mismatches.append(
            f"rows observed {row_count}, expected {AUTHENTIC_SEGMENTS_ROW_COUNT}",
        )
    if set(observed_metadata) != set(dataset.segment_ids): # Check if the observed metadata matches the expected metadata.
        mismatches.append(
            f"segments observed {len(observed_metadata)}, expected {len(dataset.segment_ids)}",
        )
    if observed_channels != set(dataset.channels): # Check if the observed channels match the expected channels.
        expected_channels = sorted(set(dataset.channels))
        mismatches.append(
            f"channels observed {sorted(observed_channels)}, expected {expected_channels}",
        )
    if observed_label_values != set(AUTHENTIC_SEGMENTS_LABEL_VALUES): # Check if the observed label values match the expected label values.
        mismatches.append(
            f"label values observed {sorted(observed_label_values)}, "
            f"expected {sorted(AUTHENTIC_SEGMENTS_LABEL_VALUES)}",
        )
    if mismatches: # Check if there are any mismatches.
        raise DatasetValidationError(
            "authentic segments.csv profile mismatch: " + "; ".join(mismatches),
        )

    # Return the SegmentsVerification instance.
    return SegmentsVerification(
        artifact=artifact,
        row_count=row_count,
        segment_count=len(observed_metadata),
        channel_count=len(observed_channels),
        label_values=tuple(sorted(observed_label_values)),
    )
# ---


# __________________________________________
# DETERMINISTIC PARTITIONS
# ==========================================


# --- create_dataset_partitions()
def create_dataset_partitions(
    dataset: TelemetryDataset,
    *,
    config: AppConfig = DEFAULT_CONFIG,
) -> DatasetPartitions:
    """Create training and validation roles without consuming held-out test labels.

    Stratification uses the reviewed labels to preserve class proportions as closely as whole-row
    counts allow. The configured seed makes the selection repeatable for the same data and
    environment. Historical references reuse all official training rows, so that role intentionally
    overlaps model training and threshold validation.

    Args:
        dataset: Validated rows with the official training flag still attached.
        config: Validation share and random seed for splitting official training rows.

    Returns:
        Zero-based indices into the original dataset, sorted within the derived partitions.

    Raises:
        DatasetValidationError: If a deterministic stratified partition cannot be created.
    """
    # The official test flag decides test membership before the local split occurs.
    benchmark_training_indices = np.flatnonzero(dataset.benchmark_training_flags) # Get the indices of the benchmark training data.
    benchmark_test_indices = np.flatnonzero(~dataset.benchmark_training_flags) # Get the indices of the benchmark test data.
    benchmark_training_labels = dataset.y_anomaly_labels[benchmark_training_indices] # Get the anomaly labels for the benchmark training data.

    try: # Try to create the deterministic stratified validation partition.
        training_indices, validation_indices = train_test_split(
            benchmark_training_indices,
            test_size=config.validation_fraction,
            random_state=config.random_seed,
            stratify=benchmark_training_labels,
        )
    except ValueError as exc: # Catch ValueError.
        raise DatasetValidationError(
            f"unable to create deterministic stratified validation partition: {exc}",
        ) from exc

    # INVARIANT: This split uses only official training labels. Held-out labels are
    # reserved for later evaluation, while sorted indices retain source-row order.
    return DatasetPartitions(
        dataset=dataset,
        training_indices=tuple(sorted(int(index) for index in training_indices)), # Get the indices of the training data.
        validation_indices=tuple(sorted(int(index) for index in validation_indices)), # Get the indices of the validation data.
        test_indices=tuple(int(index) for index in benchmark_test_indices), # Get the indices of the test data.
        reference_indices=tuple(int(index) for index in benchmark_training_indices), # Get the indices of the reference data.
    )
# ---


# __________________________________________
# SEGMENT AND SCENARIO SELECTION
# ==========================================


# ________________________________________________
# Exact segment selection and row roles
# ------------------------------------------------
# Resolve a user selection into the table, then describe its role in the existing partitions.
# --- select_segment_index()
def select_segment_index(dataset: TelemetryDataset, selector: str | int) -> int:
    """Resolve an exact segment identifier or one-based validated row index.

    A string first tries the exact segment ID, even if it looks numeric. An integer or `#N` then
    means row N as counted by a user, starting at one. The returned array index starts at zero.

    Raises:
        SegmentSelectionError: If the selector does not identify one row.
    """
    # Check the type of the selector.
    if isinstance(selector, int): # Check if the selector is an integer.
        one_based_index = selector
    else:
        normalized_selector = selector.strip() # Remove whitespace from the selector.
        if normalized_selector in dataset.segment_ids: # Check if the selector is in the dataset segment IDs.
            return dataset.segment_ids.index(normalized_selector) # Return the index of the selector.
        if normalized_selector.startswith("#") and normalized_selector[1:].isdigit(): # Check if the selector starts with "#" and is followed by digits.
            one_based_index = int(normalized_selector[1:]) # Convert the selector to an integer.
        else:
            raise SegmentSelectionError(
                f"unknown segment {selector!r}; use an exact identifier or #<one-based-index>",
            )

    if not 1 <= one_based_index <= len(dataset.segment_ids): # Check if the segment index is valid.
        raise SegmentSelectionError(
            f"segment index must be between 1 and {len(dataset.segment_ids)}",
        )
    return one_based_index - 1 # Return the index of the selector.
# ---


# --- identify_partition()
def identify_partition(partitions: DatasetPartitions, row_index: int) -> str:
    """Return the first matching primary role for a zero-based dataset row.

    Historical references overlap training and validation. Checking those primary roles first
    gives the reader the row's more specific use; the final fallback covers an unassigned index.

    Args:
        partitions: The dataset partitions.
        row_index: The zero-based index of the row.

    Returns:
        The partition role of the row index.
    """
    # Check if the row index is in the test indices.
    if row_index in partitions.test_indices:
        return "held-out test"
    # Check if the row index is in the validation indices.
    if row_index in partitions.validation_indices:
        return "validation"
    if row_index in partitions.training_indices:
        return "model training"
    if row_index in partitions.reference_indices: # Check if the row index is in the reference indices.
        return "historical reference"
    return "unassigned" # Return "unassigned" if the row index is not in any of the partitions.
# ---


# ________________________________________________
# Named fixture scenarios
# ------------------------------------------------
# Load the example-name mapping used to select fixture rows for the same analysis pipeline.
# --- load_demo_scenarios()
def load_demo_scenarios(scenarios_path: Path) -> dict[str, dict[str, str]]:
    """Load the non-executable deterministic demonstration scenario mapping.

    Each scenario names a segment and explains its teaching purpose. The coordinator analyzes that
    segment through the fitted model; this JSON supplies no replacement probability or action.

    Returns:
        Scenario names mapped to their validated `segment_id` and `purpose` strings.

    Raises:
        DatasetValidationError: If the JSON structure or scenario values are invalid.
    """
    # Try to load the demo scenarios from the scenarios path.
    try:
        decoded = json.loads(scenarios_path.read_text(encoding="utf-8")) # Load the JSON data from the scenarios path.
    except (OSError, json.JSONDecodeError) as exc: # Catch OSError and JSONDecodeError.
        raise DatasetValidationError(f"unable to read demo scenarios: {exc}") from exc

    scenarios = decoded.get("scenarios") if isinstance(decoded, dict) else None # Get the scenarios from the decoded JSON data.
    if not isinstance(scenarios, dict) or not scenarios: # Check if the scenarios are valid.
        raise DatasetValidationError("demo scenario file must contain a non-empty scenarios object")

    validated: dict[str, dict[str, str]] = {} # Initialize the validated scenarios dictionary.
    for scenario_name, scenario in scenarios.items(): # Iterate over the scenarios.
        if not isinstance(scenario_name, str) or not isinstance(scenario, dict): # Check if the scenario name and scenario are valid.
            raise DatasetValidationError("demo scenario entries must be named objects")
        segment_id = scenario.get("segment_id") # Get the segment ID from the scenario.
        purpose = scenario.get("purpose") # Get the purpose from the scenario.
        if not isinstance(segment_id, str) or not isinstance(purpose, str): # Check if the segment ID and purpose are valid.
            raise DatasetValidationError(
                f"demo scenario {scenario_name!r} requires segment_id and purpose strings",
            )
        validated[scenario_name] = {"segment_id": segment_id, "purpose": purpose} # Add the validated scenario to the dictionary.
    return validated
# ---


# __________________________________________
# END OF FILE
# ==========================================
