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

"""Calculate and inspect Multinomial Naive Bayes probabilities.

This module reconstructs class priors, feature counts, Laplace-smoothed word likelihoods,
and normalized posteriors from one fitted model. It compares the manual posterior with
`MultinomialNB.predict_proba()` and locates a real zero-frequency word/class pair for the
smoothing demonstration. It does not train the classifier or print output.
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


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

from typing import Iterable

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

# pyrefly: ignore [missing-import]
import numpy as np

# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_types import (
    InputMessageError,
    PosteriorCalculation,
    TrainedSmsModel,
    VerificationError,
)


# _____________________________________________________________________________
# =============================================================================
# FREQUENCY, PRIOR, LIKELIHOOD, AND POSTERIOR CALCULATIONS
# =============================================================================
#
# Frequency and count variables:
#     M      = total number of training messages
#     M_k    = number of training messages in class C_k
#     N_jk   = number of times word w_j occurs in class C_k
#     N_k    = total number of modeled word occurrences in class C_k
#     V      = vocabulary size
#     x_j    = number of times word w_j occurs in the new input message
#
# Prior probability:
#     P(C_k) = probability of class C_k before the new message is considered
#
# Likelihood probabilities:
#     P(w_j | C_k) = probability of word w_j given class C_k
#     P(x | C_k)   = likelihood of the input message x given class C_k
#
# Class score:
#     score_k = P(C_k) * P(x | C_k)
#
# Posterior probability:
#     P(C_k | x) = probability of class C_k after considering input message x
#
# =============================================================================
# _____________________________________________________________________________
#
# These functions reconstruct the probability quantities stored by the fitted
# estimator. The sequence is M_k -> P(C_k), N_jk and N_k -> P(w_j | C_k), then
# x_j -> log P(x | C_k) -> log_score_k -> P(C_k | x) -> argmax.
#
# Every class-indexed array follows `classifier.classes_`. The code therefore does
# not assume that HAM or SPAM occupies a particular numeric position.


# _________________________________________________________________
# TRAINING EQUATION RECONSTRUCTION: CLASS PRIORS
# M and M_k -> P(C_k) = M_k / M
# _________________________________________________________________
#
# Equation relationship: Evaluates the class-prior equation directly.
# Code map: m_total_messages is M; each class_counts value is M_k;
# p_c_k_prior is the resulting prior vector in fitted class order.
# Boundary: This reconstructs learned priors for display and verification.
#
# This function is used in calculate_posterior_probabilities()
# This is for the first section of the explainable classification workflow.
# --- calculate_manual_class_priors()
def calculate_manual_class_priors(model: TrainedSmsModel) -> np.ndarray:
    """Calculate class priors with `P(C_k) = M_k / M`.

    Args:
        model: TrainedSmsModel containing the frequency tables
        
    Returns:
        np.ndarray: Array of class priors in `model.classifier.classes_` order
    
    Related equation:
        P(C_k) = M_k / M
        
    Boundary: This reconstructs learned priors for display and verification.
    """

    # For each class in fitted order, select its M_k value and divide by the same
    # total M. The resulting array is [P(C_0), P(C_1), ...].
    m_total_messages = model.dataset.m_total_messages
    p_c_k_prior = np.asarray(
        [
            model.dataset.class_counts[str(class_label)] / m_total_messages
            for class_label in model.classifier.classes_
        ],
        dtype=np.float64,
    )
    return p_c_k_prior
# ---


# -----------------------------------------------------------------
# TRAINING COUNT EQUATION: BUILD N_JK
# X and labels -> N_jk = sum of X[i, j] where label_i = C_k
# -----------------------------------------------------------------
#
# Equation relationship: Evaluates the class-by-word frequency sum.
# Code map: class_row_mask selects class C_k; class_feature_sum produces one N_jk row;
# n_jk_word_count_by_class stores all class rows.
# Boundary: This function builds N_jk. It does not calculate N_k or probabilities.
#
# This is a function that calculates the N_jk values for each class
# --- calculate_manual_feature_counts()
def calculate_manual_feature_counts(model: TrainedSmsModel) -> np.ndarray:
    """Calculate `N_jk` by summing count-matrix rows within each class.
    
    Args:
        model: TrainedSmsModel object containing the fitted estimator and dataset
        
    Returns:
        np.ndarray: Array of N_jk values in `model.classifier.classes_` order
    """

    # Build one row of N_jk values for each fitted class. The Boolean mask selects
    # all training messages labeled C_k; summing those rows down axis 0 leaves one
    # corpus-wide occurrence count for every vocabulary word w_j.
    n_jk_word_count_by_class: list[np.ndarray] = []
    for class_label in model.classifier.classes_:
        class_row_mask = model.dataset.labels == class_label
        # The resulting column j is N_jk, not the input-message count x_j.
        class_feature_sum = np.asarray(
            model.x_training_word_counts[class_row_mask].sum(axis=0)
        ).ravel()
        n_jk_word_count_by_class.append(class_feature_sum.astype(np.float64))

    # Stack class rows into shape (number of classes, vocabulary size).
    return np.vstack(n_jk_word_count_by_class)
# ---


# _________________________________________________________________
# TRAINING EQUATION RECONSTRUCTION: LAPLACE LIKELIHOODS
# N_jk, N_k, V, alpha -> P(w_j | C_k)
# _________________________________________________________________
#
# Equation relationship: Evaluates the Laplace-smoothed likelihood equation directly.
# Equation: P(w_j | C_k) = (N_jk + alpha) / (N_k + alpha * V).
# Code map: n_jk_word_count_by_class is N_jk; its row sums are N_k;
# v_vocabulary_size is V; theta_hat_jk_word_likelihood is P(w_j | C_k).
# Boundary: This reconstructs fitted likelihoods. It does not refit MultinomialNB.
#
# This is a function that calculates the P(w_j | C_k) values for each class
# --- calculate_manual_word_likelihoods()
def calculate_manual_word_likelihoods(model: TrainedSmsModel) -> np.ndarray:
    """Calculate every Laplace-smoothed `P(w_j | C_k)` value.

    Args:
        model: TrainedSmsModel object containing the fitted estimator and dataset
        
    Returns:
        np.ndarray: Array of P(w_j | C_k) values in `model.classifier.classes_` order

    Related equation:
        theta_hat_jk = (N_jk + alpha) / (N_k + alpha * V)

    Parameters:
        `N_jk` is the count of word `j` in class `k`.
        `N_k` is the total count of all vocabulary words in class `k`.
        `V` is vocabulary size.
        `alpha=1.0` is Laplace add-one smoothing.
    """

    # Reconstruct the complete class-by-word table N_jk, then sum each class row
    # across all V words to obtain N_k.
    n_jk_word_count_by_class = calculate_manual_feature_counts(model)

    # N_k is the total modeled token count for class k, not its message count M_k.
    n_k_total_word_count_by_class = n_jk_word_count_by_class.sum(axis=1)
    v_vocabulary_size = model.v_vocabulary_size
    alpha_smoothing = float(model.classifier.alpha)

    # NumPy broadcasting applies the same estimator to every class-word cell:
    # theta_hat_jk = (N_jk + alpha) / (N_k + alpha * V).
    theta_hat_jk_word_likelihood = (
        n_jk_word_count_by_class + alpha_smoothing
    ) / (
        n_k_total_word_count_by_class[:, np.newaxis]
        + alpha_smoothing * v_vocabulary_size
    )
    return theta_hat_jk_word_likelihood
# ---


# _________________________________________________________________
# MESSAGE PREDICTION EQUATION PIPELINE
# message -> x_j -> log P(x | C_k) -> log_score_k -> posterior -> argmax
# _________________________________________________________________
#
# Equation relationship: Evaluates the complete prediction pipeline for one message.
# Step 1: vectorizer.transform() maps the message to word counts x_j.
# Step 2: x_j dot feature_log_prob_.T evaluates sum_j x_j log P(w_j | C_k).
# Step 3: adding class_log_prior_ evaluates log_score_k.
# Step 4: shifted exponentials normalize scores into P(C_k | x).
# Step 5: argmax returns k, the index of the largest posterior.
# Step 6: predict_proba() supplies the same fitted model's library result for comparison.
# Boundary: Prediction reads learned probabilities. It does not change model parameters.
#
# This is a function that calculates the posterior probabilities for a given message
# --- calculate_posterior_probabilities()
def calculate_posterior_probabilities(
    model: TrainedSmsModel,
    message: str,
) -> PosteriorCalculation:
    """Calculate `P(C_k | x)` manually and with scikit-learn.

    Args:
        model: Fitted vectorizer and MultinomialNB estimator.
        message: One nonblank SMS message.

    Returns:
        A `PosteriorCalculation` containing all intermediate quantities.

    Related equations:
        `x_j` is the CountVectorizer count for feature `j` in this message.

        log P(x | C_k) = sum_j x_j * log(P(w_j | C_k))

        log_score_k = log(P(C_k)) + log P(x | C_k)

        r_k = exp(log_score_k - max_l log_score_l)
        P(C_k | x) = r_k / sum_l r_l

    Equation relationship:
        Bayes' evidence term P(x) is common to every class for the same input.
        Normalizing the positive class scores by their sum supplies the shared
        denominator and produces posteriors that sum to one.
    """

    # PHASE 0: Remove surrounding whitespace but keep the message text otherwise.
    normalized_message = message.strip()

    # VALIDATION: A blank message has no words and no classification evidence.
    if not normalized_message:
        raise InputMessageError("The SMS message is blank.")

    # Transform the message with the fitted vocabulary. The resulting sparse row
    # is x; its column j contains x_j in the same feature order used during fitting.
    x_input_sparse = model.vectorizer.transform([normalized_message])
    # VALIDATION: Reject a prior-only result when every modeled x_j equals zero.
    if int(x_input_sparse.nnz) == 0:
        raise InputMessageError(
            "The message contains no terms in the fitted vocabulary. A prior-only "
            "prediction would hide that limitation, so the program stops instead."
        )

    # Keep a dense copy only for readable tables and equation expansion. The
    # sparse row remains the numerical input, and only x_j > 0 terms need display
    # because x_j = 0 contributes zero to the weighted log-likelihood sum.
    x_j_input_word_counts = np.asarray(
        x_input_sparse.toarray(),
        dtype=np.float64,
    ).ravel()
    relevant_feature_indices = np.flatnonzero(x_j_input_word_counts > 0.0)

    # Matrix multiplication evaluates the weighted sum for all classes at once:
    # x_input_sparse.dot(feature_log_prob_.T)
    #     = sum_j x_j * log P(w_j | C_k).
    log_p_x_given_c_k_likelihood = np.asarray(
        x_input_sparse.dot(model.classifier.feature_log_prob_.T),
        dtype=np.float64,
    ).ravel()

    # Add log P(C_k) to the message log likelihood. This gives the unnormalized
    # class log score used for MAP comparison:
    # log_score_k = log P(C_k) + log P(x | C_k).
    log_score_c_k = (
        np.asarray(model.classifier.class_log_prior_, dtype=np.float64)
        + log_p_x_given_c_k_likelihood
    )

    # Convert log scores into posteriors. Subtracting the largest log score makes
    # the largest exponent exactly exp(0)=1 and keeps the others numerically stable.
    # Because the same constant is removed from every score, ratios and argmax do
    # not change. Dividing by the sum then gives P(C_k | x).
    max_log_score = float(np.max(log_score_c_k))
    shifted_exponential_score_c_k = np.exp(log_score_c_k - max_log_score)
    p_c_k_given_x_posterior = (
        shifted_exponential_score_c_k
        / shifted_exponential_score_c_k.sum()
    )

    # Obtain scikit-learn's posterior from the same fitted model. This is the
    # independent library result used to check the reconstructed arithmetic.
    sklearn_p_c_k_given_x_posterior = np.asarray(
        model.classifier.predict_proba(x_input_sparse)[0],
        dtype=np.float64,
    )

    # np.argmax returns the index k of the largest posterior; it does not return
    # the posterior value. classifier.classes_[k] maps that index back to HAM or SPAM.
    k_predicted_class_index = int(np.argmax(p_c_k_given_x_posterior))
    # Compare every class probability. A matching label alone could hide an error.
    max_absolute_probability_difference = float(
        np.max(
            np.abs(
                p_c_k_given_x_posterior
                - sklearn_p_c_k_given_x_posterior
            )
        )
    )

    # Preserve each intermediate quantity for teaching output and verification.
    return PosteriorCalculation(
        message=normalized_message, # normalized message
        x_input_sparse=x_input_sparse, # sparse matrix of input message
        x_j_input_word_counts=x_j_input_word_counts, # word counts of input message
        relevant_feature_indices=relevant_feature_indices, # indices of words in vocabulary
        log_p_x_given_c_k_likelihood=log_p_x_given_c_k_likelihood, # log likelihood of input message given class
        log_score_c_k=log_score_c_k, # log score of input message given class
        max_log_score=max_log_score, # maximum log score
        shifted_exponential_score_c_k=shifted_exponential_score_c_k, # shifted exponential score
        p_c_k_given_x_posterior=p_c_k_given_x_posterior, # posterior probability of input message given class
        sklearn_p_c_k_given_x_posterior=sklearn_p_c_k_given_x_posterior, # sklearn posterior probability
        k_predicted_class_index=k_predicted_class_index, # predicted class index
        max_absolute_probability_difference=max_absolute_probability_difference, # max absolute probability difference
    )
# ---


# -----------------------------------------------------------------
# LAPLACE EXAMPLE SELECTION: FIND N_JK = 0
# fitted N_jk table -> one zero word-class pair
# -----------------------------------------------------------------
#
# Equation relationship: Constructs evidence for the zero-probability example.
# The returned indices are later substituted into the raw and smoothed equations.
# Boundary: This function selects N_jk = 0. It does not calculate either probability.
#
# This is a function that finds an example of a word that has a zero frequency in the training data
# --- find_zero_frequency_example()
def find_zero_frequency_example(
    model: TrainedSmsModel,
    preferred_feature_indices: Iterable[int] | None = None,
) -> tuple[int, int]:
    """Return `(class_index, feature_index)` for one raw zero count.

    Input-relevant words are searched first so the teaching example can connect
    directly to the current message. If no relevant zero exists, the function
    searches the complete learned frequency table.
    """

    # Read the raw N_jk table learned before smoothing.
    feature_count = np.asarray(model.classifier.feature_count_, dtype=np.float64)

    # Search current-message words first so the displayed example is relevant.
    preferred = (
        []
        if preferred_feature_indices is None
        else [int(index) for index in preferred_feature_indices]
    )
    # Append the rest of the vocabulary without repeating preferred indices.
    remaining = [
        feature_index
        for feature_index in range(model.v_vocabulary_size)
        if feature_index not in set(preferred)
    ]

    # A valid example has a zero in one class and a positive count in another.
    for feature_index in preferred + remaining:
        zero_class_indices = np.flatnonzero(feature_count[:, feature_index] == 0.0)
        for class_index in zero_class_indices:
            if np.any(feature_count[:, feature_index] > 0.0):
                return int(class_index), int(feature_index)

    # The assignment requires a numerical smoothing example. Report a failed
    # assumption instead of inventing one when the fitted table has no such pair.
    raise VerificationError(
        "No zero-frequency feature/class pair was found; Laplace correction "
        "could not be demonstrated."
    )
# ---
