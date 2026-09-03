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

"""Define shared errors and immutable data records for the classifier.

This module provides one project error hierarchy plus dataclasses for validated datasets,
fitted model state, posterior calculation details, and verification outcomes. These records
carry related values across loading, training, probability, display, and command-line
boundaries without performing workflow actions.
"""


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


# _____________________________________________________________________________
# =============================================================================
# CLASSES
#==============================================================================
# _____________________________________________________________________________


# =============================================================================
# EXCEPTIONS
# =============================================================================
#
# Expected data, download, input, and verification failures use one shared base
# class. `main()` can report these errors without hiding programming defects.
# These classes are used to catch and report errors that are expected during 
# program execution, such as missing data or invalid input.

# --- class SmsClassifierError
class SmsClassifierError(Exception):
    """Base class for expected project errors."""
# --- end class SmsClassifierError


# --- class DatasetError
class DatasetError(SmsClassifierError):
    """Raised when a dataset cannot be parsed or validated."""
# --- end class DatasetError


# --- class DownloadError
class DownloadError(SmsClassifierError):
    """Raised when the official UCI archive cannot be downloaded or extracted."""
# --- end class DownloadError


# --- class InputMessageError
class InputMessageError(SmsClassifierError):
    """Raised when an input message cannot be classified meaningfully."""
# --- end class InputMessageError


# --- class VerificationError
class VerificationError(SmsClassifierError):
    """Raised when a mathematical or behavioral verification check fails."""
# --- end class VerificationError


# =============================================================================
# DATA CLASSES
# =============================================================================
#
# These immutable records keep related values together and make the boundaries
# between raw data, the fitted model, one probability calculation, and one
# verification result explicit.
#
# SmsDataset             validated records and dataset metadata
# TrainedSmsModel        fitted estimator plus lookup information
# PosteriorCalculation   intermediate and final values for one message
# VerificationCheck      one named verification observation


#------------------------------------------------------
# Data setclass
#------------------------------------------------------
# --- class SmsDataset
@dataclass(frozen=True)
class SmsDataset:
    """ Dataset container for validated SMS records and source metadata.

    Attributes:
        labels: One normalized `ham` or `spam` label for each message.
        messages: Raw message strings in source order.
        source_path: File from which the records were loaded.
        dataset_mode: Either `complete` or `sample`.
        text_encoding: Encoding that successfully decoded the source file.
        class_counts: Frequency table `M_k` for the class labels.
    """

    labels: np.ndarray
    messages: tuple[str, ...]
    source_path: Path
    dataset_mode: str
    text_encoding: str
    class_counts: dict[str, int]

    # Equation connection: M is the number of labeled training messages.
    # This property supplies denominator M to P(C_k) = M_k / M.
    # --- m_total_messages()
    @property
    def m_total_messages(self) -> int:
        """Return `M`, the total number of messages."""

        return len(self.messages)
    # ---
# --- end class SmsDataset



#------------------------------------------------------
# Trained data set class
#------------------------------------------------------
# --- class TrainedSmsModel
@dataclass(frozen=True)
class TrainedSmsModel:
    """Fitted/Trained vectorizer, classifier, counts, and lookup metadata.
    
    Attributes:
        dataset: The SmsDataset object used to train the model.
        vectorizer: The fitted CountVectorizer object.
        x_training_word_counts: The word count matrix for the training data.
        classifier: The fitted MultinomialNB classifier.
        feature_names: The names of the vocabulary features.
        class_to_index: A dictionary mapping class labels to indices.
    """

    dataset: SmsDataset
    vectorizer: CountVectorizer
    x_training_word_counts: Any
    classifier: MultinomialNB
    feature_names: np.ndarray
    class_to_index: dict[str, int]

    # Equation connection: V is the number of vocabulary columns in X.
    # This property supplies V to P(w_j | C_k) = (N_jk + alpha) / (N_k + alpha * V).
    # --- v_vocabulary_size()
    @property
    def v_vocabulary_size(self) -> int:
        """Return `V`, the number of learned vocabulary features."""

        return int(self.feature_names.size)
    # ---
# --- end class TrainedSmsModel


#------------------------------------------------------
# Posterior Probability Class
#------------------------------------------------------
# --- class PosteriorCalculation
@dataclass(frozen=True)
class PosteriorCalculation:
    """Manual and scikit-learn probability results for one message.

    Attributes:
        message: The input message string.
        x_input_sparse: The sparse vector representation of the input message.
        x_j_input_word_counts: The word count vector for the input message.
        relevant_feature_indices: The indices of the relevant features.
        log_p_x_given_c_k_likelihood: The log-likelihood of the input message given each class.
        log_score_c_k: The log-score of each class given the input message.
        max_log_score: The maximum log-score.
        shifted_exponential_score_c_k: The shifted exponential of the log-scores.
        p_c_k_given_x_posterior: The posterior probability of each class given the input message.
        sklearn_p_c_k_given_x_posterior: The posterior probability of each class given the input message.

    Related equations:
        log_score_k = log(P(C_k)) + sum_j x_j * log(P(w_j | C_k))

        P(C_k | x) = exp(log_score_k - max_log_score)
                     / sum_l exp(log_score_l - max_log_score)

        predicted class = argmax_k P(C_k | x)
    """

    message: str
    x_input_sparse: Any
    x_j_input_word_counts: np.ndarray
    relevant_feature_indices: np.ndarray
    log_p_x_given_c_k_likelihood: np.ndarray
    log_score_c_k: np.ndarray
    max_log_score: float
    shifted_exponential_score_c_k: np.ndarray
    p_c_k_given_x_posterior: np.ndarray
    sklearn_p_c_k_given_x_posterior: np.ndarray
    k_predicted_class_index: int
    max_absolute_probability_difference: float
# --- end class PosteriorCalculation


#------------------------------------------------------
# Verification Check Class
#------------------------------------------------------
# --- class VerificationCheck
@dataclass(frozen=True)
class VerificationCheck:
    """One named internal verification result.

    Attributes:
        name: The name of the verification check.
        passed: Whether the verification check passed.
        detail: The detail of the verification check.
    """

    name: str
    passed: bool
    detail: str
# --- end class VerificationCheck
