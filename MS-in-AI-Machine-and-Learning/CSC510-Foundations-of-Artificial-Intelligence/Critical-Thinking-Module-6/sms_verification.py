# -----------------------------------------------------------------------------
# Project: UCI SMS Spam Multinomial Naive Bayes Classifier
# Module Type: executable script
# Author: Alexander S. Ricciardi
# Last Updated: 2026-08-30
# -----------------------------------------------------------------------------
# Course: CSC510 - Foundations of Artificial Intelligence
# Professor: Dr. Isaac Gang
# Term: Fall A (26FA) - 2026
# Assignment: Critical Thinking Module 6 - Naive Bayes Classifier
# -----------------------------------------------------------------------------
# My Project Description:
# The program trains a Multinomial Naive Bayes classifier on the UCI SMS Spam
# Collection. It converts messages into word-frequency counts, calculates class
# priors and smoothed word likelihoods, and classifies one message as HAM or SPAM.
# The manual probability calculation is compared with scikit-learn's result.
# -----------------------------------------------------------------------------
# Assignment Requirements: Naive Bayes Classifier
# 
# Naive Bayes classifiers are quick and easy to code in Python and are very efficient. 
# Naive Bayes classifiers are based on Bayes' Theorem and assume independence among 
# predictors (hence the "Naive" terminology). Not only are Naive Bayes classifiers handy 
# and straightforward in a pinch, but they also outperform many other methods without the 
# need for advanced feature engineering of the data.
#
# Read the following article for further information on Naive Bayes classification: 
# https://www.ibm.com/think/topics/naive-bayes
#
# Using scikit-learn, write a Naive Bayes classifier in Python. It can be single or multiple 
# features. Submit the classifier in the form of an executable Python script 
# alongside basic instructions for testing.
#
# Your Naive Bayes classification script should allow you to do the following:
#
# - Calculate the posterior probability by converting the dataset into a frequency 
#   table.
# - Create a "Likelihood" table by finding relevant probabilities.
# - Calculate the posterior probability for each class.
# - Correct Zero Probability errors using Laplacian correction.
#
# Your classifier may use a Gaussian, Multinomial, or Bernoulli model, 
# depending on your chosen function. Your classifier must properly display 
# its probability prediction based on its input data.
#
# Check out scikit-learn and its documentation at the following website:
# https://scikit-learn.org/stable/
#
# Assignment summarization check list:
#
# - Use a scikit-learn Naive Bayes classifier.
# - Convert the dataset into class and word frequency tables.
# - Create a likelihood table with relevant conditional probabilities.
# - Calculate and display the posterior probability for each class.
# - Correct zero-probability errors with Laplace add-one smoothing.
# - Display a clear probability-based prediction.
# - Include an executable script and basic testing instructions.
# -----------------------------------------------------------------------------
# Data Source:
# - UCI SMS Spam Collection, 5,574 labeled messages.
# - Dataset DOI: https://doi.org/10.24432/C5CC84
#
# Dependencies:
# - Standard Library: argparse, io, os, shutil, sys, tempfile, textwrap,
#   urllib, zipfile, collections, dataclasses, pathlib, typing
# - Third Party: NumPy, scikit-learn
#
# Requirements:
# - Python 3.11+
# - NumPy 1.26+
# - scikit-learn 1.4+
# -----------------------------------------------------------------------------

"""Check fitted data, probability mathematics, and representative behavior.

This module compares manual class counts, priors, likelihoods, and posterior probabilities
with the fitted estimator. It also confirms Laplace smoothing and model settings and
exercises known HAM, SPAM, demo, and unknown-vocabulary cases. The caller receives
structured `VerificationCheck` records for display and exit-status decisions.
"""


# ---------------------------------------------------------------------------
# Manual and scikit-learn probability comparison
# ---------------------------------------------------------------------------
#
# The program trains one Multinomial Naive Bayes classifier and then calculates
# the HAM and SPAM probabilities in two ways.
#
# 1. It uses the program's own functions to calculate the Naive Bayes probabilities
#    step by step using the values learned by the trained model.
#
# 2. It uses scikit-learn's probability function by asking the same trained model
#    to calculate the probabilities with the predict_proba() method.
#
# Then the program compares the two results. If they are almost identical, the
# step-by-step probability calculation is working correctly. Note that this
# comparison checks the probability calculation; it does not measure how accurately
# the classifier performs on separate test data.
#
#                     New SMS message
#                           |
#                 +---------+---------+
#                 |                   |
#                 v                   v
#        Program's functions    scikit-learn's
#                               predict_proba()
#                 |                   |
#                 | uses the same     | uses the same
#                 | learned values    | learned values
#                 |                   |
#                 v                   v
#          HAM probability       HAM probability
#          SPAM probability      SPAM probability
#                 |                   |
#                 +---------+---------+
#                           |
#                           v
#                     Compare them
#
# There is only one classifier model: the trained Multinomial Naive Bayes model.
# Only the method used to calculate the prediction probabilities changes.
#


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

import numpy as np

# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_config import (
    DEMO_MESSAGE,
    EXPECTED_CLASS_LABELS,
    EXPECTED_COMPLETE_RECORD_COUNT,
    EXPECTED_SAMPLE_CLASS_COUNTS,
    EXPECTED_SAMPLE_RECORD_COUNT,
    PROBABILITY_TOLERANCE,
    VERIFY_HAM_MESSAGE,
    VERIFY_SPAM_MESSAGE,
    VERIFY_UNKNOWN_MESSAGE,
)
from sms_probability import (
    calculate_manual_class_priors,
    calculate_manual_feature_counts,
    calculate_manual_word_likelihoods,
    calculate_posterior_probabilities,
    find_zero_frequency_example,
)
from sms_types import InputMessageError, TrainedSmsModel, VerificationCheck


# =============================================================================
# INTERNAL VERIFICATION
# =============================================================================
#
# Verification connects the displayed equations to the fitted estimator:
# - manual counts are compared with scikit-learn's learned counts,
# - manual priors and likelihoods are compared with fitted log probabilities,
# - posterior calculations are compared with predict_proba(),
# - a real zero count is checked after Laplace smoothing,
# - representative HAM, SPAM, demo, and unknown-vocabulary cases are exercised.
#
# These checks validate this implementation and the selected dataset. They do not
# measure held-out accuracy or certify the program as a production spam filter.


# --- _verification_check()
def _verification_check(
    checks: list[VerificationCheck],
    name: str,
    passed: bool,
    detail: str,
) -> None:
    """Append one normalized verification result.
    
    Args:
        checks: List of verification checks
        name: Name of the verification check
        passed: Whether the verification check passed
        detail: Detailed information about the verification check
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    # Normalize the truth value and preserve a human-readable observation.
    checks.append(VerificationCheck(name=name, passed=bool(passed), detail=detail))
# ---


# _________________________________________________________________
# EQUATION VERIFICATION PIPELINE
# manual reconstruction -> fitted scikit-learn values -> PASS or FAIL
# _________________________________________________________________
#
# Equation relationship: Coordinates independent checks of every calculation stage.
# It compares M_k, N_jk, P(C_k), P(w_j | C_k), P(C_k | x), and argmax behavior.
# Boundary: Verification reads the fitted model and calls calculation functions.
# It does not train a new model or change the fitted parameters.
# --- run_internal_verification()
def run_internal_verification(model: TrainedSmsModel) -> list[VerificationCheck]:
    """Run focused data, mathematics, estimator, and behavior checks.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        
    Returns:
        list[VerificationCheck]: List of verification checks
    
    Related equation:
        None
    
    Boundary: Verification reads the fitted model and calls calculation functions.
        It does not train a new model or change the fitted parameters.
    """

    checks: list[VerificationCheck] = []
    dataset = model.dataset
    classifier = model.classifier
    x_training = model.x_training_word_counts

    # PHASE 1: Verify the selected dataset contract and required labels.
    expected_rows = (
        EXPECTED_COMPLETE_RECORD_COUNT
        if dataset.dataset_mode == "complete"
        else EXPECTED_SAMPLE_RECORD_COUNT
    )
    _verification_check(
        checks,
        "Dataset record count",
        dataset.m_total_messages == expected_rows,
        f"observed={dataset.m_total_messages:,}, expected={expected_rows:,}",
    )
    _verification_check(
        checks,
        "Required class labels",
        set(dataset.class_counts) == set(EXPECTED_CLASS_LABELS),
        f"classes={sorted(dataset.class_counts)}",
    )
    if dataset.dataset_mode == "sample":
        _verification_check(
            checks,
            "Bundled sample distribution",
            dataset.class_counts == EXPECTED_SAMPLE_CLASS_COUNTS,
            f"observed={dataset.class_counts}",
        )

    # PHASE 2: Verify the CountVectorizer feature representation.
    matrix_values = np.asarray(x_training.data)
    matrix_valid = (
        matrix_values.size > 0
        and np.all(np.isfinite(matrix_values))
        and np.all(matrix_values >= 0)
        and np.allclose(matrix_values, np.rint(matrix_values), atol=0.0, rtol=0.0)
    )
    _verification_check(
        checks,
        "Nonnegative integer count matrix",
        matrix_valid,
        f"shape={x_training.shape}, nonzero_values={matrix_values.size:,}",
    )

    # PHASE 3: Verify the estimator configuration required by the assignment.
    parameter_match = (
        float(classifier.alpha) == 1.0
        and bool(classifier.fit_prior)
        and bool(classifier.force_alpha)
    )
    _verification_check(
        checks,
        "MultinomialNB parameter configuration",
        parameter_match,
        "alpha=1.0, fit_prior=True, force_alpha=True",
    )

    # PHASE 4: Recalculate M_k and N_jk independently from the stored dataset and X.
    manual_class_count = np.asarray(
        [dataset.class_counts[str(label)] for label in classifier.classes_],
        dtype=np.float64,
    )
    class_count_difference = float(
        np.max(np.abs(manual_class_count - classifier.class_count_))
    )
    _verification_check(
        checks,
        "Manual class counts match class_count_",
        class_count_difference == 0.0,
        f"maximum difference={class_count_difference:.3e}",
    )

    manual_feature_count = calculate_manual_feature_counts(model)
    feature_count_difference = float(
        np.max(np.abs(manual_feature_count - classifier.feature_count_))
    )
    _verification_check(
        checks,
        "Manual feature counts match feature_count_",
        feature_count_difference == 0.0,
        f"maximum difference={feature_count_difference:.3e}",
    )

    # PHASE 5: Compare manual priors and smoothed word likelihoods with the
    # exponentiated log values stored by scikit-learn.
    manual_priors = calculate_manual_class_priors(model)
    fitted_priors = np.exp(classifier.class_log_prior_)
    prior_difference = float(np.max(np.abs(manual_priors - fitted_priors)))
    _verification_check(
        checks,
        "Manual priors match class_log_prior_",
        prior_difference <= PROBABILITY_TOLERANCE,
        f"maximum difference={prior_difference:.3e}",
    )

    manual_likelihoods = calculate_manual_word_likelihoods(model)
    fitted_likelihoods = np.exp(classifier.feature_log_prob_)
    likelihood_difference = float(
        np.max(np.abs(manual_likelihoods - fitted_likelihoods))
    )
    _verification_check(
        checks,
        "Manual likelihoods match feature_log_prob_",
        likelihood_difference <= PROBABILITY_TOLERANCE,
        f"maximum difference={likelihood_difference:.3e}",
    )

    # PHASE 6: Confirm that a raw zero N_jk receives a positive smoothed value.
    zero_class_index, zero_feature_index = find_zero_frequency_example(model)
    n_jk_zero = float(classifier.feature_count_[zero_class_index, zero_feature_index])
    smoothed_likelihood = float(
        np.exp(classifier.feature_log_prob_[zero_class_index, zero_feature_index])
    )
    _verification_check(
        checks,
        "Laplace correction fixes a raw zero",
        n_jk_zero == 0.0 and smoothed_likelihood > 0.0,
        (
            f"word={model.feature_names[zero_feature_index]!r}, "
            f"class={classifier.classes_[zero_class_index]!r}, "
            f"smoothed={smoothed_likelihood:.3e}"
        ),
    )

    # PHASE 7: Exercise representative messages through the complete posterior path.
    verification_messages = (
        DEMO_MESSAGE,
        VERIFY_HAM_MESSAGE,
        VERIFY_SPAM_MESSAGE,
    )
    posterior_differences: list[float] = []
    posterior_sums: list[float] = []
    predictions: dict[str, str] = {}
    message_error: str | None = None
    for verification_message in verification_messages:
        try:
            result = calculate_posterior_probabilities(model, verification_message)
        except InputMessageError as exc:
            message_error = str(exc)
            break
        posterior_differences.append(result.max_absolute_probability_difference)
        posterior_sums.append(float(result.p_c_k_given_x_posterior.sum()))
        predictions[verification_message] = str(
            classifier.classes_[result.k_predicted_class_index]
        )

    # A calculation error becomes one failed check rather than an incomplete report.
    if message_error is None:
        max_posterior_difference = max(posterior_differences)
        max_sum_error = max(abs(total - 1.0) for total in posterior_sums)
        _verification_check(
            checks,
            "Manual posteriors match predict_proba()",
            max_posterior_difference <= PROBABILITY_TOLERANCE,
            f"maximum difference={max_posterior_difference:.3e}",
        )
        _verification_check(
            checks,
            "Manual posteriors sum to one",
            max_sum_error <= PROBABILITY_TOLERANCE,
            f"maximum sum error={max_sum_error:.3e}",
        )
        _verification_check(
            checks,
            "Representative HAM prediction",
            predictions[VERIFY_HAM_MESSAGE] == "ham",
            f"prediction={predictions[VERIFY_HAM_MESSAGE].upper()}",
        )
        _verification_check(
            checks,
            "Representative SPAM prediction",
            predictions[VERIFY_SPAM_MESSAGE] == "spam",
            f"prediction={predictions[VERIFY_SPAM_MESSAGE].upper()}",
        )
        _verification_check(
            checks,
            "Deterministic demo prediction",
            predictions[DEMO_MESSAGE] == "spam",
            f"prediction={predictions[DEMO_MESSAGE].upper()}",
        )
    else:
        _verification_check(
            checks,
            "Representative posterior calculations",
            False,
            message_error,
        )

    # PHASE 8: Confirm that an all-zero vocabulary vector is rejected explicitly.
    unknown_rejected = False
    try:
        calculate_posterior_probabilities(model, VERIFY_UNKNOWN_MESSAGE)
    except InputMessageError:
        unknown_rejected = True
    _verification_check(
        checks,
        "Unknown-vocabulary input is rejected",
        unknown_rejected,
        f"message={VERIFY_UNKNOWN_MESSAGE!r}",
    )

    return checks
# ---
