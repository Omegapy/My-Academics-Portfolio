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

"""Provide shared configuration for every classifier component.

This module defines program identity, output limits, data paths, expected corpus
properties, repeatable messages, vectorizer and model parameters, and ANSI color codes.
Data loading, training, verification, and display modules import these values so each
stage uses the same settings.
"""


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

import numpy as np


# =============================================================================
# PROGRAM METADATA AND CONFIGURATION
# =============================================================================
#
# These constants define program identity, display limits, data locations,
# expected dataset properties, deterministic examples, and estimator settings.
# None of the presentation constants change the probability equations.

# __________________________________________
# PROGRAM IDENTITY
# ==========================================

PROGRAM_NAME = "UCI SMS Spam Multinomial Naive Bayes Classifier"
PROGRAM_VERSION = "1.0.0"
COURSE_NAME = "CSC510 Module 6 Critical Thinking Assignment"

# __________________________________________
# DISPLAY, NUMERICAL, AND DOWNLOAD LIMITS
# ==========================================

DISPLAY_WIDTH = 92
INNER_WIDTH = DISPLAY_WIDTH - 4
MAX_RELEVANT_TERMS = 18
MAX_TOP_TERMS_PER_CLASS = 6
PROBABILITY_TOLERANCE = 1e-12
DOWNLOAD_TIMEOUT_SECONDS = 30
MAX_DOWNLOAD_BYTES = 10_000_000

# __________________________________________
# PROJECT DATA PATHS
# ==========================================
#
# Paths are derived from this script so the program can be run from another
# working directory without losing its bundled data location.

PROJECT_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = PROJECT_DIRECTORY / "data"
DEFAULT_COMPLETE_DATASET_PATH = DATA_DIRECTORY / "SMSSpamCollection"
BUNDLED_SAMPLE_DATASET_PATH = DATA_DIRECTORY / "SMSSpamCollection.sample"

# __________________________________________
# DATASET SOURCE AND EXPECTED SHAPE
# ==========================================

OFFICIAL_UCI_ZIP_URL = (
    "https://archive.ics.uci.edu/static/public/228/"
    "sms%2Bspam%2Bcollection.zip"
)
UCI_DATASET_DOI = "https://doi.org/10.24432/C5CC84"
EXPECTED_COMPLETE_RECORD_COUNT = 5_574
EXPECTED_SAMPLE_RECORD_COUNT = 100
EXPECTED_SAMPLE_CLASS_COUNTS = {"ham": 83, "spam": 17}
EXPECTED_CLASS_LABELS = ("ham", "spam")

# __________________________________________
# DEMO AND VERIFICATION MESSAGES VARIABLES
# ==========================================
#
# These messages make the demo and verification modes repeatable. They are not
# added to the training data and do not change the fitted frequency tables.

DEMO_MESSAGE = (
    "Dear Valued Customer, Congratulations! Your mobile number has been selected "
    "to receive a cash prize worth one thousand dollars. Please call our claims "
    "department today and provide your confirmation code to collect your reward "
    "before this limited-time offer expires. Sincerely, Rewards Center."
)
VERIFY_HAM_MESSAGE = "Are we still meeting for lunch today"
VERIFY_SPAM_MESSAGE = "WINNER you have won a free cash prize call now to claim"
VERIFY_UNKNOWN_MESSAGE = "qzxqzxqzv nvqzxqzx"

# Store parameters for CountVectorizer in a dictionary to create nonnegative count vectors
VECTORIZER_PARAMETERS: dict[str, Any] = {
    "lowercase": True,  # convert all messages to lowercase
    "token_pattern": r"(?u)\b\w\w+\b",  # keeps words with at least two alphabetic characters
    "ngram_range": (1, 1),  # considers only single words
    "binary": False,  # preserves repeated-word counts
    "dtype": np.int64,  # use 64-bit integers for counts
}

# MultinomialNB parameter relationship:
#
#   alpha=1.0       -> Laplace add-one smoothing.
#   fit_prior=True  -> Estimate P(C_k) from class frequencies M_k / M.
#   force_alpha=True -> Keep the explicitly supplied alpha value.
MODEL_PARAMETERS: dict[str, Any] = {
    "alpha": 1.0,
    "fit_prior": True,
    "force_alpha": True,
}


# =============================================================================
# ANSI TERMINAL STYLING 
# =============================================================================
#
# For displaying output in color, `terminal_supports_color()`
# disables them when output is redirected or color is explicitly disabled.
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_CYAN = "\033[36m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_RED = "\033[31m"
