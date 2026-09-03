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

"""Build the word-count representation and fit the SMS classifier.

This module transforms validated messages with `CountVectorizer`, checks that the training
matrix contains valid count features, and fits `MultinomialNB` with the shared parameters.
It packages the estimator, count matrix, class indices, vocabulary, and lookup metadata in
a `TrainedSmsModel` for probability and display operations.
"""


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


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

from typing import Any

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_config import (
    EXPECTED_CLASS_LABELS,
    MODEL_PARAMETERS,
    VECTORIZER_PARAMETERS,
)
from sms_types import DatasetError, SmsDataset, TrainedSmsModel


# _____________________________________________________________________________
# =============================================================================
# FEATURE EXTRACTION AND MODEL TRAINING
# =============================================================================
#______________________________________________________________________________
#
# CountVectorizer converts raw text into X, a sparse matrix of discrete word
# counts. MultinomialNB then fits the class-frequency and word-frequency model.
#
# Training data flow:
#
#   messages -> CountVectorizer.fit_transform() -> X counts
#   labels + X -> MultinomialNB.fit() -> priors and word likelihoods
#
# The fitted vectorizer and classifier must stay together. A new message must be
# transformed with the same vocabulary and feature order used during training.


# --------------------------------------------------------------------
# TRAINING INPUT VALIDATION: CHECK X
# messages -> CountVectorizer -> X
# --------------------------------------------------------------------
#
# Equation relationship: Validates an equation input. X[i, j] is the count of
# vocabulary word j in training message i. Later class-wise sums of X produce N_jk.
# Boundary: This function checks X. It does not calculate N_jk or fit the model.
#
# This function is used to verify the word counts of the training data.
# --- _verify_count_matrix()
def _verify_count_matrix(x_word_counts: Any) -> None:
    """Verify that `X` contains finite, nonnegative integer word counts.
    
    Args:
        x_word_counts: The word count matrix to verify.
    
    Returns:
        None
    
    Raises:
        DatasetError: If the word count matrix is invalid.
    
    Notes:
        The word count matrix is a sparse matrix where each row represents a
        message and each column represents a word. The value at each cell is the
        count of the word in the message.
    """

    # VALIDATION: X needs at least one message row and one vocabulary column.
    if x_word_counts.shape[0] == 0 or x_word_counts.shape[1] == 0:
        raise DatasetError("CountVectorizer produced an empty feature matrix.")

    # Sparse matrices store only nonzero counts in `.data`.
    data_values = np.asarray(x_word_counts.data)

    # VALIDATION: A matrix with dimensions but no modeled words cannot train.
    if data_values.size == 0:
        raise DatasetError("No modeled words were found in the dataset.")
    # VALIDATION: Multinomial word counts must be finite and nonnegative.
    if not np.all(np.isfinite(data_values)):
        raise DatasetError("The word-count matrix contains a non-finite value.")
    if np.any(data_values < 0):
        raise DatasetError("The word-count matrix contains a negative value.")
    # VALIDATION: `binary=False` should produce integer occurrence counts.
    if not np.allclose(data_values, np.rint(data_values), atol=0.0, rtol=0.0):
        raise DatasetError("The word-count matrix contains a non-integer value.")
# ---


# ------------------------------------------------------------------
# TRAINING STEPS 1-4: FIT THE MULTINOMIAL MODEL
# messages -> X; X and labels -> P(C_k) and P(w_j | C_k)
# ------------------------------------------------------------------
#
# Equation relationship: Coordinates feature construction and model fitting.
# Step 1: CountVectorizer builds X; each X[i, j] is a word count.
# Step 2: fit() counts messages M_k and word occurrences N_jk by class.
# Step 3: fit_prior=True learns P(C_k) = M_k / M.
# Step 4: alpha=1.0 learns P(w_j | C_k) = (N_jk + 1) / (N_k + V).
# Code map: class_count_ stores M_k; feature_count_ stores N_jk.
# Code map: class_log_prior_ and feature_log_prob_ store the learned log probabilities.
# Boundary: The manual calculation functions reconstruct these values for teaching
# and verification. They do not fit a second classifier.
# 
# This function is used to train the Multinomial Naive Bayes model.
# --- train_multinomial_naive_bayes()
def train_multinomial_naive_bayes(dataset: SmsDataset) -> TrainedSmsModel:
    """Transform all messages into counts and fit Multinomial Naive Bayes.

    Why this is classification:
        The output is one category, HAM or SPAM. Regression would predict a
        continuous numeric target and therefore does not fit this task.

    Why MultinomialNB is selected:
        `CountVectorizer` creates discrete nonnegative word counts. The
        Multinomial model estimates each word's class-conditional probability
        from those counts.

    Why GaussianNB is not selected:
        GaussianNB models continuous features with Gaussian distributions.

    Why BernoulliNB is not selected:
        BernoulliNB models binary present/absent features and would discard the
        information that a word appears more than once in a message.

    Args:
        dataset: The dataset to train on.

    Returns:
        A TrainedSmsModel containing the fitted model.

    Raises:
        DatasetError: If the dataset is invalid.
    """

    # CountVectorizer fixes the vocabulary and creates X, where row i is one
    # training message and column j stores that message's count for word w_j.
    # Because binary=False, repeated words remain counts rather than collapsing to
    # present/absent indicators. Those counts become N_jk during class-wise sums.
    vectorizer = CountVectorizer(**VECTORIZER_PARAMETERS)
    try:
        x_training_word_counts = vectorizer.fit_transform(dataset.messages)
    except ValueError as exc:
        # ERROR TRANSLATION: Vocabulary failures are dataset failures at this boundary.
        raise DatasetError(f"CountVectorizer could not build a vocabulary: {exc}") from exc

    # MultinomialNB requires finite, nonnegative count features. The feature-name
    # array preserves the exact column-to-word mapping used by the sparse matrix.
    _verify_count_matrix(x_training_word_counts)
    feature_names = vectorizer.get_feature_names_out()

    # Fitting stores M_k in class_count_ and N_jk in feature_count_. With alpha=1,
    # each fitted word likelihood uses (N_jk + 1) / (N_k + V).
    classifier = MultinomialNB(**MODEL_PARAMETERS)
    classifier.fit(x_training_word_counts, dataset.labels)

    # Record scikit-learn's fitted class order. Every later count row, log score,
    # posterior vector, and argmax index must be interpreted in this same order.
    class_to_index = {
        str(class_label): int(class_index)
        for class_index, class_label in enumerate(classifier.classes_)
    }

    # INVARIANT: The fitted estimator must contain exactly HAM and SPAM.
    if set(class_to_index) != set(EXPECTED_CLASS_LABELS):
        raise DatasetError(
            "The fitted classifier does not contain exactly the HAM and SPAM classes."
        )

    # -- PHASE 5: Return the vectorizer, estimator, count matrix, and lookup metadata
    # as one unit so feature order cannot be separated from the fitted model. --
    #
    return TrainedSmsModel(
        dataset=dataset,
        vectorizer=vectorizer,
        x_training_word_counts=x_training_word_counts,
        classifier=classifier,
        feature_names=feature_names,
        class_to_index=class_to_index,
    )
# ---
