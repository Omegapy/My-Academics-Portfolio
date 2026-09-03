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

"""Resolve command-line data and message choices for the classifier.

This module builds the argument parser, chooses the complete, sample, downloaded, or
user-supplied dataset, and collects an explicit, demo, or interactive SMS message. It
delegates dataset parsing and validation to `sms_dataset` and performs no model training
or probability calculation.
"""


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

import argparse
from pathlib import Path

# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_config import (
    BUNDLED_SAMPLE_DATASET_PATH,
    DEFAULT_COMPLETE_DATASET_PATH,
    DEMO_MESSAGE,
    PROGRAM_VERSION,
)
from sms_dataset import download_uci_dataset, load_sms_dataset
from sms_types import DatasetError, InputMessageError, SmsDataset


# =============================================================================
# COMMAND-LINE AND PROGRAM FLOW
# =============================================================================
#
# The command line selects a data source and one action: interactive classification,
# an explicit message, the deterministic demo, or internal verification. Every
# classification mode uses the same load, train, calculate, and display functions.


# --- build_argument_parser()
def build_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line interface.
    
    Args:
        None
    
    Returns:
        argparse.ArgumentParser: Argument parser for the command-line interface
    
    Related equation:
        None
    
    Boundary: This function only defines command-line arguments; it does not perform any calculations.
    """

    # Build one parser shared by interactive, scripted, demo, and verify modes.
    parser = argparse.ArgumentParser(
        description=(
            "Train an explainable Multinomial Naive Bayes SMS classifier and "
            "display the frequency, likelihood, smoothing, and posterior math."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # ACTION MODES: At most one message source or verification action may run.
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--message",
        metavar="TEXT",
        help="Classify one explicit SMS message without prompting.",
    )
    action_group.add_argument(
        "--demo",
        action="store_true",
        help="Classify the deterministic demonstration message.",
    )
    action_group.add_argument(
        "--verify",
        action="store_true",
        help="Run internal mathematical and behavioral verification checks.",
    )

    # DATA MODES: Sample data and a supplied complete file cannot both be selected.
    data_group = parser.add_mutually_exclusive_group()
    data_group.add_argument(
        "--sample-data",
        action="store_true",
        help="Use the bundled 100-message teaching sample explicitly.",
    )
    data_group.add_argument(
        "--dataset",
        type=Path,
        metavar="PATH",
        help="Use an existing complete 5,574-record UCI-format dataset file.",
    )

    parser.add_argument(
        "--download-data",
        action="store_true",
        help="Force a fresh download of the official UCI ZIP archive.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color even when the terminal supports it.",
    )
    parser.add_argument(
        "--no-pause",
        action="store_true",
        help="Do not pause between teaching sections.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {PROGRAM_VERSION}",
    )
    return parser
# ---


# Training preparation step 0: Select and validate the data source used to build X.
# Boundary: This routes dataset modes. It does not vectorize messages or fit the model.
# --- resolve_dataset()
def resolve_dataset(args: argparse.Namespace) -> SmsDataset:
    """Resolve explicit sample, explicit path, or primary complete-data mode. 

    Args:
        args: Parsed command-line arguments
        
    Returns:
        SmsDataset: Loaded dataset
    
    Raises:
        DatasetError: If both --sample-data and --download-data are used
        DatasetError: If both --dataset and --download-data are used
    
    Related equation:
        None
    
    Boundary: This function routes dataset modes. It does not vectorize messages or fit the model.
    """

    # DISPATCH 1: Explicit sample mode never performs a network download.
    if args.sample_data:
        if args.download_data:
            raise DatasetError(
                "--sample-data and --download-data cannot be used together."
            )
        return load_sms_dataset(BUNDLED_SAMPLE_DATASET_PATH, dataset_mode="sample")

    # DISPATCH 2: A supplied complete file is validated in place.
    if args.dataset is not None:
        if args.download_data:
            raise DatasetError(
                "--dataset and --download-data cannot be used together."
            )
        return load_sms_dataset(args.dataset, dataset_mode="complete")

    # DISPATCH 3: Primary mode downloads only when forced or when data is absent.
    if args.download_data or not DEFAULT_COMPLETE_DATASET_PATH.is_file():
        print(
            "Complete UCI dataset not available locally. Downloading the official "
            "archive..."
        )
        return download_uci_dataset(DEFAULT_COMPLETE_DATASET_PATH)

    # DISPATCH 4: Reuse the existing complete dataset after full validation.
    return load_sms_dataset(DEFAULT_COMPLETE_DATASET_PATH, dataset_mode="complete")
# ---


# Message-processing step 0: Select explicit, demonstration, or interactive text.
# Boundary: This returns raw message text. Vectorization into x_j happens later.
# --- collect_message()
def collect_message(args: argparse.Namespace) -> str:
    """Resolve explicit, demo, or interactive input text."""

    # Explicit text takes priority, followed by the deterministic demo fixture.
    if args.message is not None:
        return args.message
    if args.demo:
        return DEMO_MESSAGE

    # Interactive mode uses the demo only when the user submits an empty line.
    try:
        entered_message = input(
            "Enter an SMS message, or press Enter to use the demonstration:\n> "
        )
    except EOFError as exc:
        raise InputMessageError("No SMS input was received.") from exc

    return entered_message if entered_message.strip() else DEMO_MESSAGE
# ---
