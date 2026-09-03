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
# It uses scikit-learn to calculate the probabilities and compares them with a locally 
# computed calculation.
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


"""Multinomial Naive Bayes classifier for UCI SMS messages program.

The program classifies an inputted SMS message as HAM or SPAM. 
It uses CountVectorizer that learns a vocabulary from the UCI SMS dataset 
and converts each SMS message into vectorized word counts. 
Note that the dataset has 5,574 SMS messages, 4,825 HAM (non-spam) and 
747 SPAM.

Then a Multinomial Naive Bayes model, MultinomialNB(alpha=1.0), is trained 
using the vectorized word counts to categorize the SMS messages as HAM or SPAM.
This training allows the model to learn the class priors HAM and SPAM. The 
Laplace-smoothed method is used to calculate the word likelihoods, 
preventing a word with a zero count in one class from making that class's 
probability zero. 

A new message entered by a user or by the demo feature of the program is converted 
into vectorized word counts based on the vocabulary learned from the training dataset. 
Then, the program calculates the posterior probabilities that the new message is 
HAM or SPAM step by step using both its own functions and scikit-learn's 
predict_proba() method. The two probability results are compared to verify that they match.
Then, the class with the highest posterior probability is returned as the final prediction.

Finally, it displays the results with an explanation of the probability calculation.
"""


# ____________________________________________________________________________________
# ====================================================================================
# Calculation Steps Explanation
# ====================================================================================
#
# The program has two main stages:
#
#     1. Train the Multinomial Naive Bayes classifier using labeled SMS messages.
#     2. Use the trained classifier to calculate the probabilities that a new SMS
#        message is HAM or SPAM.
#
# During training, the program learns:
#
#     P(C_k)         = probability of each class, HAM or SPAM
#     P(w_j | C_k)   = probability of each vocabulary word within each class
#
# After training, the probability calculation for a new SMS follows these steps:
#
# 1. Convert the new input message into word counts x_j.
# 2. Use the learned class prior P(C_k).
# 3. Use the learned word likelihoods P(w_j | C_k).
# 4. Combine the prior and word likelihoods into one score for each class.
# 5. Normalize the scores into P(C_k | x), so the HAM and SPAM probabilities
#    sum to approximately 1.
# 6. Use argmax to return the class index with the largest posterior probability.
#
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
# ---------------------------------------------------------------------------
# Important information about training data
# ---------------------------------------------------------------------------
#
# The program can train the same Multinomial Naive Bayes classifier using two
# different datasets:
#
# 1. Normal mode uses the complete UCI SMS Spam Collection with 5,574 messages.
#
# 2. If the --sample-data flag is used, the classifier is trained using the smaller
#    100-message sample included with this project. This mode is useful for offline
#    testing, demonstrations, and automated tests when the complete dataset or a
#    network connection is unavailable.
#
# Both modes use the same MultinomialNB algorithm and settings. Only the training
# data changes. Because the training data changes, the probabilities learned by
# the model can also change.
#
# For example, the complete dataset and the 100-message sample can contain
# different HAM/SPAM proportions and different word counts. Therefore, they can
# produce different values for:
#
#     P(HAM)
#     P(SPAM)
#     P(w_j | HAM)
#     P(w_j | SPAM)
#
# and can therefore produce different final HAM and SPAM probabilities for the
# same input message.
#
# ---------------------------------------------------------------------------
# Equations used to train the Multinomial Naive Bayes model
# ---------------------------------------------------------------------------
#
# Training happens before the program classifies a new SMS message.
#
# CountVectorizer first learns the training vocabulary and converts the training
# messages into a matrix of word counts. MultinomialNB.fit() then uses those word
# counts together with the known HAM and SPAM labels to learn the probabilities
# needed by the classifier.
#
# The Multinomial Naive Bayes model mainly learns two types of probabilities:
#
#     1. Class priors:
#
#            P(HAM)
#            P(SPAM)
#
#     2. Word likelihoods:
#
#            P(w_j | HAM)
#            P(w_j | SPAM)
#
# After these values have been learned, the classifier is considered trained.
#
# ---------------------------------------------------------------------------
# Training Step 
# ---------------------------------------------------------------------------
# 
# Training Step 1 - Count the messages in each class
# Training Step 2 - Count each vocabulary word within each class
# Training Step 3 - Convert word counts into word probabilities
# Training Step 4 - Apply Laplace smoothing
#
# ---------------------------------------------------------------------------
# Training summary
# ---------------------------------------------------------------------------
#
#
#                       Labeled training messages
#                                  |
#                                  v
#                          CountVectorizer
#                                  |
#                                  v
#                      Training word-count matrix
#                                  |
#                    +-------------+-------------+
#                    |                           |
#                    v                           v
#          Count HAM/SPAM messages      Count words in each class
#                    |                           |
#                    v                           v
#               M and M_k                   N_jk and N_k
#                    |                           |
#                    |                           |
#                    |                           v
#                    |            Apply Laplace smoothing
#                    |                           |
#                    v                           v
#           P(C_k) = M_k / M                 P(w_j | C_k)
#                    |                           |
#                    +-------------+-------------+
#                                  |
#                                  v
#                      Trained MultinomialNB model
#                                  |
#                         learned values include:
#
#                              P(HAM)
#                              P(SPAM)
#                              P(w_j | HAM)
#                              P(w_j | SPAM)
#
# At this point, model training is complete.
#
# The model has learned probabilities from the labeled training messages, but the
# new SMS message that will be classified has not yet been used.
#
# ________________________________________________
# Equation-to-function
# ------------------------------------------------
#
# -- Equation and variable map --
# - M -> m_total_messages
# - M_k -> m_k_class_message_count or class_counts
# - X -> x_training_word_counts
# - V -> v_vocabulary_size
# - N_jk -> n_jk_word_count_by_class or classifier.feature_count_
# - N_k -> n_k_total_word_count_by_class
# - x_j -> x_j_input_word_counts
# - P(C_k) -> p_c_k_prior
# - P(w_j | C_k) -> theta_hat_jk_word_likelihood
# - log P(x | C_k) -> log_p_x_given_c_k_likelihood.
# - log_score_k -> log_score_c_k; r_k -> shifted_exponential_score_c_k.
# - P(C_k | x) -> p_c_k_given_x_posterior.
# - argmax index k -> k_predicted_class_index.
#
# Training preparation and fitted values:
# - `load_sms_dataset()` builds messages, labels, total M, and class counts M_k.
# - `train_multinomial_naive_bayes()` builds X and fits P(C_k) and P(w_j | C_k).
# - `calculate_manual_class_priors()` evaluates P(C_k) = M_k / M.
# - `calculate_manual_feature_counts()` evaluates N_jk from X and class labels.
# - `calculate_manual_word_likelihoods()` evaluates the Laplace likelihood equation.
#
# Message prediction:
# - `collect_message()` selects the raw message. It performs no probability math.
# - `calculate_posterior_probabilities()` evaluates the complete prediction pipeline:
#   message -> x_j -> log P(x | C_k) -> log_score_k -> P(C_k | x) -> argmax.
# - `run_teaching_classification()` calculates one result, then coordinates its display.
#
# Display boundary:
# - Display functions explain stored or fitted values unless their local equation block
#   states that they also derive a table value or Laplace example.
#
# -----------------------------------------------------------------------------
# For more information about the equations and how they relate to the code, see
# README.md.
# -----------------------------------------------------------------------------


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

import argparse
import io
import os
import shutil
import sys
import tempfile
import textwrap
import urllib.error
import urllib.request
import zipfile
# pyright: ignore [reportMissingImports]
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

# DEPENDENCY CHECK: Import the numerical and machine-learning packages before
# any configuration refers to NumPy types or scikit-learn estimators.
try:
    # Code for loading scikit-learn and NumPy
    # pyrefly: ignore [missing-import]
    import numpy as np
    import sklearn
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
except ImportError as exc:  # pragma: no cover - exercised only without dependencies.
    # ERROR TRANSLATION: Replace an import traceback with one installation command.
    missing_name = getattr(exc, "name", None) or "a required package"
    raise SystemExit(
        "Missing dependency: "
        f"{missing_name}. Install the project packages with "
        "'python -m pip install -r requirements.txt'."
    ) from exc




# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_cli import build_argument_parser, collect_message, resolve_dataset
from sms_config import (
    ANSI_BOLD,
    ANSI_CYAN,
    ANSI_GREEN,
    ANSI_RED,
    ANSI_RESET,
    ANSI_YELLOW,
    BUNDLED_SAMPLE_DATASET_PATH,
    COURSE_NAME,
    DATA_DIRECTORY,
    DEFAULT_COMPLETE_DATASET_PATH,
    DEMO_MESSAGE,
    DISPLAY_WIDTH,
    DOWNLOAD_TIMEOUT_SECONDS,
    EXPECTED_CLASS_LABELS,
    EXPECTED_COMPLETE_RECORD_COUNT,
    EXPECTED_SAMPLE_CLASS_COUNTS,
    EXPECTED_SAMPLE_RECORD_COUNT,
    INNER_WIDTH,
    MAX_DOWNLOAD_BYTES,
    MAX_RELEVANT_TERMS,
    MAX_TOP_TERMS_PER_CLASS,
    MODEL_PARAMETERS,
    OFFICIAL_UCI_ZIP_URL,
    PROBABILITY_TOLERANCE,
    PROGRAM_NAME,
    PROGRAM_VERSION,
    PROJECT_DIRECTORY,
    UCI_DATASET_DOI,
    VECTORIZER_PARAMETERS,
    VERIFY_HAM_MESSAGE,
    VERIFY_SPAM_MESSAGE,
    VERIFY_UNKNOWN_MESSAGE,
)
from sms_dataset import (
    _decode_dataset_bytes,
    _safe_dataset_member,
    download_uci_dataset,
    extract_uci_dataset_zip,
    load_sms_dataset,
)
from sms_display import (
    _expanded_log_expression,
    _selected_relevant_indices,
    _top_terms_for_class,
    display_path,
    print_dataset_and_frequency_tables,
    print_input_frequency_and_likelihoods,
    print_internal_verification,
    print_manual_posterior_calculation,
    print_model_and_equations,
    print_prediction_and_verification,
    print_program_banner,
)
from sms_probability import (
    calculate_manual_class_priors,
    calculate_manual_feature_counts,
    calculate_manual_word_likelihoods,
    calculate_posterior_probabilities,
    find_zero_frequency_example,
)
from sms_terminal import (
    pause_for_user,
    print_equation,
    print_heading,
    print_labeled_value,
    print_paragraph,
    print_subheading,
    print_table,
    style_text,
    terminal_supports_color,
    truncate_cell,
)
from sms_training import _verify_count_matrix, train_multinomial_naive_bayes
from sms_types import (
    DatasetError,
    DownloadError,
    InputMessageError,
    PosteriorCalculation,
    SmsClassifierError,
    SmsDataset,
    TrainedSmsModel,
    VerificationCheck,
    VerificationError,
)
from sms_verification import _verification_check, run_internal_verification


# _________________________________________________________________
# MESSAGE CLASSIFICATION AND TEACHING ROADMAP
# raw message -> posterior result -> five display sections
# _________________________________________________________________
#
# Equation relationship: Coordinates one prediction and its explanation.
# It calls calculate_posterior_probabilities() once, then passes the stored result
# to display functions in equation order: definitions, training counts, message
# likelihoods, posterior normalization, and final argmax comparison.
# Boundary: The display calls do not retrain the classifier.
# --- run_teaching_classification()
def run_teaching_classification(
    model: TrainedSmsModel,
    message: str,
    use_color: bool,
    pause_enabled: bool,
) -> PosteriorCalculation:
    """Run the five-section explainable classification workflow.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        message: SMS message to classify
        use_color: Whether to use color output
        pause_enabled: Whether to pause between sections
        
    Returns:
        PosteriorCalculation: Posterior calculation result
    
    Related equation:
        None
    
    Boundary: The display calls do not retrain the classifier.
    """

    # Calculate once. Each teaching section reads from the same stored result.
    result = calculate_posterior_probabilities(model, message)

    # PRESENTATION PHASE 1: task, model choice, parameters, and equations.
    print_program_banner(use_color)
    print_model_and_equations(use_color)
    pause_for_user(pause_enabled)

    # PRESENTATION PHASE 2: dataset source, M_k, priors, N_k, and sample N_jk.
    print_dataset_and_frequency_tables(model, use_color)
    pause_for_user(pause_enabled)

    # PRESENTATION PHASE 3: input x_j, relevant likelihoods, and smoothing.
    print_input_frequency_and_likelihoods(model, result, use_color)
    pause_for_user(pause_enabled)

    # PRESENTATION PHASE 4: manual class scores and normalized posteriors.
    print_manual_posterior_calculation(model, result, use_color)
    pause_for_user(pause_enabled)

    # PRESENTATION PHASE 5: predict_proba() comparison and argmax decision.
    print_prediction_and_verification(model, result, use_color)
    return result
# ---


# _________________________________________________________________
# END-TO-END PROGRAM ROADMAP
# dataset -> X -> fitted model -> message -> posterior or verification
# _________________________________________________________________
#
# Equation relationship: Coordinates the full training and prediction pipeline.
# Phase 1 resolves validated messages and labels, which define M and M_k.
# Phase 2 builds X and fits P(C_k) and P(w_j | C_k).
# Phase 3 obtains the new message that will become x_j.
# Phase 4 evaluates P(C_k | x), selects argmax, and displays the calculation.
# Verification mode follows the same training path, then audits each equation.
# --- main()
def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments, load data, train, classify or verify, and return status.
    
    Args:
        argv: Command-line arguments
        
    Returns:
        int: Exit status (0 for success, 1 for error)
    
    Related equation:
        None
    
    Boundary: Coordinates the full training and prediction pipeline.
    """

    # __________________________________________
    # CONFIGURE THIS EXECUTION
    # ==========================================

    parser = build_argument_parser()
    args = parser.parse_args(argv)
    use_color = terminal_supports_color(args.no_color)

    try:
        # --- PHASE 1: Resolve, decode, parse, and validate SMS dataset. ---
        dataset = resolve_dataset(args)

        # --- PHASE 2: Build the word-frequency matrix and fit MultinomialNB. ---
        model = train_multinomial_naive_bayes(dataset)

        # DISPATCH: Verification mode exercises deterministic contracts and exits
        # before the learner-facing classification sections.
        if args.verify:
            checks = run_internal_verification(model)
            return 0 if print_internal_verification(model, checks, use_color) else 1

        # --- PHASE 3: Resolve explicit or demo message input. ---
        message = collect_message(args)
        # Pauses belong only to a real terminal session.
        pause_enabled = (
            not args.no_pause
            and args.message is None
            and not args.demo
            and sys.stdin.isatty()
        )
        # --- PHASE 4: Calculate and display the five-section teaching workflow. ---
        result = run_teaching_classification(
            model=model,
            message=message,
            use_color=use_color,
            pause_enabled=pause_enabled,
        )
        # INVARIANT: Do not return success when the displayed manual calculation
        # disagrees with scikit-learn beyond the documented tolerance.
        if result.max_absolute_probability_difference > PROBABILITY_TOLERANCE:
            raise VerificationError(
                "Manual posterior does not match scikit-learn within the required "
                f"tolerance of {PROBABILITY_TOLERANCE:.1e}."
            )
        return 0

    except SmsClassifierError as exc:
        # ERROR TRANSLATION: Expected project failures use a concise message and
        # status 2 instead of a traceback.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nOperation cancelled by the user.", file=sys.stderr)
        return 130
# ---


# __________________________________________
# MODULE INITIALIZATION
# ==========================================

if __name__ == "__main__":
    raise SystemExit(main())


# __________________________________________
# END OF FILE
# ==========================================
