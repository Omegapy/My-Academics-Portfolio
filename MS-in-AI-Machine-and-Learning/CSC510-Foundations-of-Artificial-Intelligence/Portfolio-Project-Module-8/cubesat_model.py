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
# - Fit the telemetry classifier, select its threshold, and measure held-out results.
# - Reuse the fitted feature scale and model for later probability estimates.
#
# Usage / Integration:
# - Called by cubesat_telemetry_ai, cubesat_frontend, and verification/tests.
# - Returns fitted state and numerical results for history, logic, and presentation.
#
# Contents Overview:
# - Validation-threshold selection and probability routing.
# - train_telemetry_model() and retained training/normal-reference statistics.
# - standardize_features() and predict_anomaly_probability().
#
# Dependencies:
# - Standard Library: None.
# - Third-Party: NumPy, scikit-learn.
# - Local Project: cubesat_config, cubesat_types.
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Train and evaluate the supervised OPS-SAT telemetry classifier.

Supervised learning uses feature rows with reviewed normal/anomalous labels. The multilayer
perceptron (MLP) learns a relationship between those 18 features and the binary label. scikit-learn
performs the neural-network calculations; this module prepares the rows and coordinates fitting.

Training data owns the fitted feature scale. Separate validation rows select the operating
threshold, and held-out test data supplies final metrics. Later inference reuses that fitted state
to estimate an anomaly probability. The estimate supports review of a segment; it cannot confirm
a spacecraft fault.
"""

# ____________________________________________________________________________________
# ====================================================================================
#
# MLP EQUATION AND SHAPE MAP
#
# X -> feature matrix (m, 18), with one segment per row and one feature per column.
# mu_training -> standardizer.mean_; fitted mean of each training feature.
# sigma_training -> standardizer.scale_; feature standard deviation, or 1.0 if constant.
# X_standardized = (X - mu_training) / sigma_training
#
# A_0 = X_standardized
# Z_l = A_(l-1) @ W_l + b_l
# A_l = ReLU(Z_l) for hidden widths 32, 16, and 8
# p_anomaly = sigmoid(Z_output), with one output value per segment.
#
# W_l -> estimator.coefs_; weight shapes (18, 32), (32, 16), (16, 8), (8, 1).
# b_l -> estimator.intercepts_; one bias for each unit in the next layer.
# ReLU, the rectified linear unit, keeps positive values and replaces negatives with zero.
# The sigmoid maps the last layer's value to the interval from zero to one.
# predict_proba() returns two columns: normal probability, then anomaly probability.
#
# Training -> validation threshold selection -> held-out evaluation -> repeated inference
#
# The normal-only means/stds stored later are a separate reference for logic facts.
# They do not replace the scaler used by the MLP and similarity search.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

# pyrefly: ignore [missing-import]
import numpy as np # Import numpy for numerical operations.
from sklearn.metrics import ( # Import metrics from scikit-learn.
    accuracy_score, # Import accuracy score.
    confusion_matrix, # Import confusion matrix.
    f1_score, # Import f1 score.
    precision_score, # Import precision score.
    recall_score, # Import recall score.
)
from sklearn.neural_network import MLPClassifier # Import MLPClassifier from scikit-learn.
from sklearn.preprocessing import StandardScaler # Import StandardScaler from scikit-learn.

from cubesat_config import DEFAULT_CONFIG, AppConfig # Import configuration constants.
from cubesat_types import (
    ClassificationResult, # Import classification results.
    DatasetPartitions, # Import dataset partitions.
    DecisionState, # Import decision states.
    EvaluationMetrics, # Import evaluation metrics.
    ModelTrainingError, # Import model training errors.
    TrainedTelemetryModel, # Import trained telemetry models.
)

# __________________________________________
# NUMERICAL HELPERS
# ==========================================


# --- _as_read_only_array()
def _as_read_only_array(array: np.ndarray) -> np.ndarray:
    """Copy numerical results and disable writes to the retained arrays.

    Stored transformed rows must keep the same values and ordering as the fitted model's inputs.
    Owning the copy avoids later changes through the caller's original array.

    Args:
        array (np.ndarray): The array to copy and disable writes to.

    Returns:
        np.ndarray: The copied array with writes disabled.
    """
    owned_array = np.array(array, copy=True) # Copy the array to avoid later changes.
    owned_array.setflags(write=False) # Disable writes to the copied array.
    return owned_array # Return the copied array.
# ---


# ________________________________________________
# Validation cutoff selection
# ------------------------------------------------
# Choose an operating threshold using reviewed validation labels and their fitted probabilities.
# --- select_classification_threshold()
def select_classification_threshold(
    y_validation_labels: np.ndarray,
    y_hat_validation_probabilities: np.ndarray,
) -> float:
    """Select the maximum-F1 validation threshold with a lower-threshold tie break.

    F1 combines precision and recall into one score. Precision is the fraction of predicted
    anomalies that are reviewed anomalies; recall is the fraction of reviewed anomalies found.
    A lower threshold predicts at least as many anomalies on the same probabilities, which gives
    recall priority when F1 is tied.

    Args:
        y_validation_labels (np.ndarray): Reviewed binary labels for the external validation rows.
        y_hat_validation_probabilities (np.ndarray): Anomaly estimates for the same rows in the same order.

    Returns:
        float: The first candidate attaining the best score within the improvement tolerance.

    Related Equation:
        `F1 = 2 * precision * recall / (precision + recall)`

    Equation Relationship:
        This function tries thresholds and compares scikit-learn's calculated F1 scores.
        `zero_division=0` supplies zero when the required ratio is undefined.

    Raises:
        ModelTrainingError: If the arrays are empty/misaligned or probabilities are non-finite.
    """
    # Raise ModelTrainingError if the arrays are empty/misaligned or probabilities are non-finite.
    if (
        y_validation_labels.size == 0
        or y_validation_labels.shape != y_hat_validation_probabilities.shape
    ):
        raise ModelTrainingError(
            "validation labels and probabilities must be non-empty and aligned",
        )
    # Raise ModelTrainingError if the probabilities are non-finite.
    if not np.all(np.isfinite(y_hat_validation_probabilities)):
        raise ModelTrainingError("validation probabilities must be finite")

    # Search the fixed grid from 0.05 through 0.95 in 0.005 steps. Test labels
    # never enter this choice, so evaluation can use a threshold already selected.
    candidate_thresholds = np.linspace(0.05, 0.95, num=181, dtype=np.float64)
    best_threshold = 0.50
    best_f1_score = -1.0
    # Iterate over candidate thresholds to find the best one.
    for candidate_threshold in candidate_thresholds:
        # Convert anomaly estimates to binary labels using the candidate threshold.
        y_hat_binary_labels = (y_hat_validation_probabilities >= candidate_threshold).astype(int)
        # Calculate the F1 score for the current candidate threshold.
        candidate_f1 = float(
            f1_score(y_validation_labels, y_hat_binary_labels, zero_division=0),
        )
        # Candidates arrive in increasing order. Replacing only for an improvement
        # greater than 1e-12 leaves the lower threshold in place for a numerical tie.
        if candidate_f1 > best_f1_score + 1e-12:
            best_f1_score = candidate_f1
            best_threshold = float(candidate_threshold)
    return best_threshold
# ---


# ________________________________________________
# Probability-to-review interpretation
# ------------------------------------------------
# Apply that cutoff and the uncertainty margin to an existing selected-segment estimate.
# --- classify_probability()
def classify_probability(
    segment_id: str,
    anomaly_probability: float,
    *,
    classification_threshold: float,
    uncertainty_margin: float,
    reference_label: str | None,
    reference_partition: str,
) -> ClassificationResult:
    """Apply the documented threshold and uncertainty band to one probability.

    Args:
        segment_id: Identity carried into the result for this selected example.
        anomaly_probability: Fitted model's anomaly estimate between zero and one.
        classification_threshold: Validation-selected cutoff for the binary class.
        uncertainty_margin: Distance on either side of the cutoff that calls for review.
        reference_label: Reviewed label retained as an annotation, if available.
        reference_partition: The selected row's pipeline role for reporting context.

    Returns:
        Both a binary predicted class and a normal/anomalous/uncertain decision state.

    Related Equations:
        `predicted_anomalous = p >= threshold`
        `uncertain = abs(p - threshold) <= uncertainty_margin`

    Equation Relationship:
        The comparisons translate one existing probability into the program's review route.

    Raises:
        ModelTrainingError: If probability or routing configuration is invalid.
    """
    # Raise ModelTrainingError if probability or routing configuration is invalid.
    if not np.isfinite(anomaly_probability) or not 0.0 <= anomaly_probability <= 1.0:
        raise ModelTrainingError("anomaly probability must be finite and within [0, 1]")
    if not 0.0 < classification_threshold < 1.0:
        raise ModelTrainingError("classification threshold must be between zero and one")
    if not 0.0 <= uncertainty_margin < 0.5:
        raise ModelTrainingError("uncertainty margin must be within [0, 0.5)")

    # The binary class remains useful for reporting even when the review route is
    # uncertain. Both edges of the uncertainty band count as uncertain here.
    # The reviewed label below annotates the result; it does not choose either route.
    predicted_class = "anomalous" if anomaly_probability >= classification_threshold else "normal"
    # Set the decision state based on the anomaly probability and uncertainty margin.
    if abs(anomaly_probability - classification_threshold) <= uncertainty_margin:
        decision_state = DecisionState.UNCERTAIN
    elif predicted_class == "anomalous":
        decision_state = DecisionState.ANOMALOUS
    else:
        decision_state = DecisionState.NORMAL

    # Return the classification result.
    return ClassificationResult(
        segment_id=segment_id, # Return the segment ID.
        anomaly_probability=float(anomaly_probability), # Return the anomaly probability.
        predicted_class=predicted_class, # Return the predicted class.
        decision_state=decision_state, # Return the decision state.
        classification_threshold=float(classification_threshold), # Return the classification threshold.
        uncertainty_margin=float(uncertainty_margin), # Return the uncertainty margin.
        reference_label=reference_label, # Return the reference label.
        reference_partition=reference_partition, # Return the reference partition.
    )
# ---


# __________________________________________
# MODEL TRAINING AND EVALUATION
# ==========================================


# --- train_telemetry_model()
def train_telemetry_model(
    partitions: DatasetPartitions,
    *,
    config: AppConfig = DEFAULT_CONFIG,
) -> TrainedTelemetryModel:
    """Fit training-only standardization and one bounded 18-32-16-8-1 MLP.

    Args:
        partitions: Validated rows and explicit training, validation, test, and reference indices.
        config: Hidden widths, iteration cap, random seed, and uncertainty margin.

    Returns:
        The fitted scaler/estimator, transformed partitions, selected threshold, held-out metrics,
        and separate normal-training means/stds used when constructing logic facts.

    Related Equation Pipeline:
        `X_standardized = (X - mu_training) / sigma_training`
        `Z_l = A_(l-1) @ W_l + b_l`
        `A_l = ReLU(Z_l)`
        `p_anomaly = sigmoid(Z_output)`

    Equation Relationship:
        This function coordinates preprocessing, library-provided backpropagation, validation
        threshold selection, and held-out evaluation. MLPClassifier evaluates the layer equations
        and updates weights through Adam optimization.

    Raises:
        ModelTrainingError: If fitting, held-out probability checks, or topology validation fails.

    Logic:
        1. Select raw rows by their existing roles and fit the training feature scale.
        2. Fit the MLP, which uses an internal early-stopping subset of its training input.
        3. Choose a threshold on the separate external validation partition.
        4. Evaluate the held-out test rows and verify the fitted layer shapes.
        5. Store fitted state and normal-only reference statistics for later analysis.
    """
    # __________________________________________
    # ROW-ROLE EXTRACTION
    # ==========================================
    # PHASE 1: Select aligned feature rows and labels using zero-based dataset indices.
    dataset = partitions.dataset
    # Convert indices to numpy arrays.
    training_indices = np.asarray(partitions.training_indices, dtype=np.int64) # Training indices.
    validation_indices = np.asarray(partitions.validation_indices, dtype=np.int64) # Validation indices.
    test_indices = np.asarray(partitions.test_indices, dtype=np.int64) # Test indices.
    reference_indices = np.asarray(partitions.reference_indices, dtype=np.int64) # Reference indices.

    # Select raw feature rows based on the indices.
    x_training_raw = dataset.x_validated_telemetry_features[training_indices] # Training features.
    x_validation_raw = dataset.x_validated_telemetry_features[validation_indices] # Validation features.
    x_test_raw = dataset.x_validated_telemetry_features[test_indices] # Test features.
    x_reference_raw = dataset.x_validated_telemetry_features[reference_indices] # Reference features.
    y_training_labels = dataset.y_anomaly_labels[training_indices] # Training labels.
    y_validation_labels = dataset.y_anomaly_labels[validation_indices] # Validation labels.
    y_test_labels = dataset.y_anomaly_labels[test_indices] # Test labels.

    # __________________________________________
    # TRAINING-ONLY FEATURE SCALE
    # ==========================================
    # PHASE 2: Learn the feature means and spreads from model-training rows.
    # Each matrix keeps shape (number of rows in that role, 18). transform() reuses
    # the fitted values, so validation and testing cannot change the feature scale.
    standardizer = StandardScaler() # Create a standard scaler.
    x_standardized_training_features = standardizer.fit_transform(x_training_raw) # Fit and standardize training features.
    x_standardized_validation_features = standardizer.transform(x_validation_raw) # Standardize validation features.
    x_standardized_test_features = standardizer.transform(x_test_raw) # Standardize test features.
    x_standardized_reference_features = standardizer.transform(x_reference_raw) # Standardize reference features.

    # __________________________________________
    # MLP FITTING
    # ==========================================
    # PHASE 3: Fit the project's 18-32-16-8-1 network through scikit-learn.
    # Backpropagation computes parameter gradients; Adam updates the weights and biases.
    # early_stopping reserves 15% of this model-training input to monitor progress.
    # That internal subset differs from the external threshold-validation rows.
    estimator = MLPClassifier(
        hidden_layer_sizes=config.hidden_layer_sizes, # Hidden layer sizes.
        activation="relu", # ReLU activation function.
        solver="adam", # Adam solver.
        max_iter=config.max_training_iterations, # Maximum number of iterations.
        early_stopping=True, # Early stopping.
        validation_fraction=0.15, # Validation fraction.
        n_iter_no_change=20, # No change in iterations.
        random_state=config.random_seed, # Random seed.
    )
    try:
        estimator.fit(x_standardized_training_features, y_training_labels) # Fit the model.
    except (TypeError, ValueError, FloatingPointError) as exc: # Handle exceptions.
        raise ModelTrainingError(f"unable to train MLP classifier: {exc}") from exc

    # __________________________________________
    # VALIDATION CUTOFF SELECTION
    # ==========================================
    # PHASE 4: Use external validation probabilities to choose the operating cutoff.
    # With reviewed labels 0 and 1, predict_proba's second column is the anomaly estimate.
    y_hat_validation_probabilities = estimator.predict_proba(
        x_standardized_validation_features,
    )[:, 1]
    classification_threshold = select_classification_threshold(
        y_validation_labels,
        y_hat_validation_probabilities,
    )

    # __________________________________________
    # HELD-OUT EVALUATION AND TOPOLOGY CHECKS
    # ==========================================
    # PHASE 5: Apply the already selected threshold to held-out predictions.
    # These test labels measure the result; they do not fit the model or select its cutoff.
    y_hat_test_probabilities = estimator.predict_proba(x_standardized_test_features)[:, 1]
    if not np.all(np.isfinite(y_hat_test_probabilities)) or not np.all(
        (0.0 <= y_hat_test_probabilities) & (y_hat_test_probabilities <= 1.0),
    ):
        raise ModelTrainingError("MLP returned an invalid held-out probability")
    y_hat_test_labels = (y_hat_test_probabilities >= classification_threshold).astype(int)
    # Rows are reviewed labels and columns are predicted labels, both ordered [0, 1].
    # The four cells are ((true normal, false anomaly), (missed anomaly, true anomaly)),
    # conventionally written ((TN, FP), (FN, TP)).
    observed_confusion = confusion_matrix(y_test_labels, y_hat_test_labels, labels=[0, 1]) # Observed confusion matrix.
    # Create evaluation metrics.
    evaluation = EvaluationMetrics(
        precision=float(precision_score(y_test_labels, y_hat_test_labels, zero_division=0)), # Precision.
        recall=float(recall_score(y_test_labels, y_hat_test_labels, zero_division=0)), # Recall.
        f1_score=float(f1_score(y_test_labels, y_hat_test_labels, zero_division=0)), # F1 score.
        accuracy=float(accuracy_score(y_test_labels, y_hat_test_labels)), # Accuracy.
        # Confusion matrix.
        confusion_matrix=(
            (int(observed_confusion[0, 0]), int(observed_confusion[0, 1])),
            (int(observed_confusion[1, 0]), int(observed_confusion[1, 1])),
        ),
        classification_threshold=classification_threshold, # Classification threshold.
        training_iterations=int(estimator.n_iter_), # Training iterations.
        test_sample_count=int(y_test_labels.size), # Test sample count.
    )

    # VALIDATION: Check the learned matrices themselves, not only constructor settings.
    expected_weight_shapes = ((18, 32), (32, 16), (16, 8), (8, 1)) # Expected weight shapes.
    observed_weight_shapes = tuple(weight_matrix.shape for weight_matrix in estimator.coefs_) # Observed weight shapes.
    # MLP topology mismatch check.
    if observed_weight_shapes != expected_weight_shapes or estimator.out_activation_ != "logistic":
        raise ModelTrainingError(
            "fitted MLP topology mismatch: "
            f"weights={observed_weight_shapes}, output={estimator.out_activation_}",
        ) # Raise model training error if MLP topology mismatch.

    # __________________________________________
    # NORMAL-REFERENCE STATISTICS AND FITTED RESULT
    # ==========================================
    # PHASE 6: Build a separate normal-only reference for the symbolic deviation facts.
    # These arrays describe raw features among reviewed normal training rows. The MLP's
    # scaler above describes all model-training rows, including anomalous examples.
    normal_training_rows = x_training_raw[y_training_labels == 0] # Normal training rows.
    mu_training_normal_feature_means = np.mean(normal_training_rows, axis=0) # Mean of normal training features.
    sigma_training_normal_feature_stds = np.std(normal_training_rows, axis=0) # Std of normal training features.
    # SAFETY CHECK: A constant normal feature has zero spread. Store 1.0 in that
    # position so the later feature-deviation calculation has a nonzero denominator.
    sigma_training_normal_feature_stds = np.where(
        sigma_training_normal_feature_stds == 0.0, # If std is 0.0.
        1.0, # Store 1.0.
        sigma_training_normal_feature_stds, # Otherwise store the std.
    )

    # Keep transformed reference rows beside this model. Similarity retrieval must use
    # the same training scale and feature order as the selected segment's prediction.
    return TrainedTelemetryModel(
        estimator=estimator, # Estimator.
        standardizer=standardizer, # Standardizer.
        classification_threshold=classification_threshold, # Classification threshold.
        uncertainty_margin=config.uncertainty_margin, # Uncertainty margin.
        evaluation=evaluation, # Evaluation metrics.
        x_standardized_training_features=_as_read_only_array(
            x_standardized_training_features,
        ), # Standardized training features.
        x_standardized_validation_features=_as_read_only_array(
            x_standardized_validation_features,
        ), # Standardized validation features.
        x_standardized_test_features=_as_read_only_array(x_standardized_test_features), # Standardized test features.
        x_standardized_reference_features=_as_read_only_array(
            x_standardized_reference_features,
        ), # Standardized reference features.
        reference_indices=partitions.reference_indices, # Reference indices.
        mu_training_normal_feature_means=_as_read_only_array(
            mu_training_normal_feature_means,
        ), # Mean of normal training features.
        sigma_training_normal_feature_stds=_as_read_only_array(
            sigma_training_normal_feature_stds,
        ), # Std of normal training features.
        feature_names=dataset.feature_names, # Feature names.
        random_seed=config.random_seed, # Random seed.
    )
# ---


# __________________________________________
# PROBABILITY INFERENCE
# ==========================================


# --- standardize_features()
def standardize_features(
    trained_model: TrainedTelemetryModel,
    x_raw_telemetry_features: np.ndarray,
) -> np.ndarray:
    """Transform inference rows with the unchanged training-only standardizer.

    Args:
        trained_model: Existing model state whose scaler owns the training means and spreads.
        x_raw_telemetry_features: One `(18,)` vector or an `(m, 18)` matrix in fitted feature order.

    Returns:
        A two-dimensional standardized matrix with the same number of feature rows.

    Related Equation:
        `X_standardized = (X - mu_training) / sigma_training`

    Equation Relationship:
        The fitted scaler evaluates this transformation without learning new statistics.

    Raises:
        ModelTrainingError: If the input shape is invalid or a feature is non-finite.
    """
    feature_matrix = np.asarray(x_raw_telemetry_features, dtype=np.float64) # Convert to numpy array.
    if feature_matrix.ndim == 1: # If 1D array.
        feature_matrix = feature_matrix.reshape(1, -1) # Reshape to 2D array.
    if feature_matrix.ndim != 2 or feature_matrix.shape[1] != 18: # If 2D array with wrong shape.
        raise ModelTrainingError("inference features must have shape (m, 18)") # Raise model training error.
    if not np.all(np.isfinite(feature_matrix)): # If non-finite features.
        raise ModelTrainingError("inference features must be finite")
    return trained_model.standardizer.transform(feature_matrix)
# ---


# --- predict_anomaly_probability()
def predict_anomaly_probability(
    trained_model: TrainedTelemetryModel,
    x_raw_telemetry_features: np.ndarray,
) -> float:
    """Return the first row's anomaly estimate without changing the fitted model.

    Args:
        trained_model: Fitted scaler and MLP reused for the current analysis.
        x_raw_telemetry_features: Normally one segment's 18 raw features. If a matrix is supplied,
            all rows are transformed/predicted, but this helper returns only the first result.

    Returns:
        The first row's class-1 probability as a finite value in the inclusive interval [0, 1].

    Raises:
        ModelTrainingError: If feature validation or the returned probability check fails.
    """
    # Standardize the features.
    x_standardized_telemetry_features = standardize_features(
        trained_model,
        x_raw_telemetry_features,
    )
    # INFERENCE: Evaluate feedforward probability only; do not update fitted parameters.
    y_hat_anomaly_probabilities = trained_model.estimator.predict_proba(
        x_standardized_telemetry_features,
    )[:, 1] # Pr    edict anomaly probabilities.
    
    probability = float(y_hat_anomaly_probabilities[0]) # Convert to float.
    if not np.isfinite(probability) or not 0.0 <= probability <= 1.0: # If invalid probability.
        raise ModelTrainingError("MLP returned an invalid anomaly probability") # Raise model training error.
    return probability
# ---


# __________________________________________
# END OF FILE
# ==========================================
