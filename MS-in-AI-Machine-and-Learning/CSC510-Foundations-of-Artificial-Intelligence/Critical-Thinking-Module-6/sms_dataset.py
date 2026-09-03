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

"""Load and validate complete or sample UCI SMS datasets.

This module decodes UCI-format records, validates labels, messages, and record counts,
checks ZIP members for safe paths, and downloads the official archive when requested.
Successful operations return an `SmsDataset`; invalid data and transfer failures raise
the project's dataset or download errors.
"""


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


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

from __future__ import annotations

import os
import tempfile
import urllib.error
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

import numpy as np

# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_config import (
    DOWNLOAD_TIMEOUT_SECONDS,
    EXPECTED_CLASS_LABELS,
    EXPECTED_COMPLETE_RECORD_COUNT,
    EXPECTED_SAMPLE_CLASS_COUNTS,
    EXPECTED_SAMPLE_RECORD_COUNT,
    MAX_DOWNLOAD_BYTES,
    OFFICIAL_UCI_ZIP_URL,
    PROGRAM_NAME,
    PROGRAM_VERSION,
)
from sms_types import DatasetError, DownloadError, SmsDataset


# _____________________________________________________________________________
# =============================================================================
# FUNCTIONS
#==============================================================================
# _____________________________________________________________________________


# ------------------------------------------------
# Dataset unzipping and validation
# ------------------------------------------------
#
# This function turns a ZIP archive into one SmsDataset.
# It validates data before CountVectorizer or MultinomialNB can use it.
#
# Data boundary:
# - network and archive functions return bytes or a validated file,
# - `load_sms_dataset()` parses and validates records,
# - training receives only a completed SmsDataset.
#
# Safety boundary:
# - ZIP paths are checked before extraction,
# - downloads have a size limit and timeout,
# - temporary files are validated before atomic replacement,
# - a failed operation does not overwrite an existing dataset.


# This function decodes the UCI-format bytes with a narrow, documented encoding strategy.
# --- _decode_dataset_bytes()
def _decode_dataset_bytes(raw_bytes: bytes) -> tuple[str, str]:
    """Decode UCI-format bytes with a narrow, documented encoding strategy.
    
    Args:
        raw_bytes: The raw bytes of the dataset.
    Returns:
        A tuple of the decoded dataset and the encoding used.

    The corpus/dataset is distributed as one text file. UTF-8 is attempted first.
    Latin-1 is the fallback commonly needed by copies of this historical SMS
    corpus. Latin-1 maps every byte, so it must remain the final fallback.
    """

    # -- PHASE 1: Try the narrow UTF-8 decoding first, then the final Latin-1 --
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            return raw_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            # The next listed encoding is the only permitted fallback.
            continue

    # Defensive final branch. Latin-1 normally maps every byte.
    raise DatasetError("The dataset could not be decoded as UTF-8 or Latin-1.")
# ---


# -------------------------------------------------------------------
# Training dataset preparation: 
# - Build M and M_K
# - Dataset rows -> messages and labels -> M and M_k
# -------------------------------------------------------------------
# These functions load, validate, and count records. 
# 

# This function loads and validates a complete or sample UCI-format SMS dataset.
# --- load_sms_dataset()
def load_sms_dataset(source_path: Path, dataset_mode: str) -> SmsDataset:
    """Load and validate a complete or sample UCI-format SMS dataset.

    Args:
        source_path: Path to the tab-delimited text file.
        dataset_mode: `complete` requires exactly 5,574 rows. `sample`
            requires exactly 100 rows and the bundled sample distribution.

    Returns:
        A validated `SmsDataset`.

    Related frequency symbols:
        `M`   = number of parsed messages.
        `M_k` = number of messages with class label `k`.

    Logic:
        1. Read and decode the file.
        2. Split each line on the first tab only.
        3. Validate the label and nonblank message.
        4. Validate record count and presence of both classes.
        5. Store `M_k` in `class_counts`.
    """

    # -- PHASE 0: Normalize the path before validation so later errors report one 
    # absolute location. --
    #
    source_path = Path(source_path).expanduser().resolve()

    # VALIDATION: Only the two dataset-counts are supported.
    # dataset_mode:
    #    `complete`:  Requires exactly 5,574 rows.
    #    `sample`:    Requires exactly 100 rows and the bundled sample distribution.
    if dataset_mode not in {"complete", "sample"}:
        raise DatasetError(
            f"Unsupported dataset mode {dataset_mode!r}; use 'complete' or 'sample'."
        )
    # VALIDATION: Training cannot continue without a regular source file.
    if not source_path.is_file():
        raise DatasetError(f"Dataset file not found: {source_path}")

    # -- PHASE 1: Read the complete source as bytes. Decoding is handled separately. --
    #
    try:
        raw_bytes = source_path.read_bytes()
    except OSError as exc:
        raise DatasetError(f"Could not read dataset file {source_path}: {exc}") from exc

    # VALIDATION: An empty file has no frequency table and cannot train a model.
    if not raw_bytes:
        raise DatasetError(f"Dataset file is empty: {source_path}")

    # -- PHASE 2: Decode once, preserve source order, and prepare aligned columns. --
    # 
    decoded_text, text_encoding = _decode_dataset_bytes(raw_bytes)
    # splitlines(): Splits a string into a list of strings at line breaks.
    raw_lines = decoded_text.splitlines()
    #
    labels: list[str] = []     # spam / ham labels
    messages: list[str] = []  # SMS messages

    # -- PHASE 3: Parse one UCI record per line. The first tab separates the label;
    # later tabs, if present in a message, remain part of the message text. --
    # 
    for line_number, raw_line in enumerate(raw_lines, start=1):
        # VALIDATION: Blank records and missing delimiters would break alignment.
        if raw_line == "":
            raise DatasetError(f"Blank record at line {line_number} in {source_path}.")
        if "\t" not in raw_line:
            raise DatasetError(
                f"Malformed record at line {line_number}: expected one tab between "
                "the class label and message."
            )

        # Normalize the class spelling but preserve the message's internal text.
        raw_label, raw_message = raw_line.split("\t", 1) # Split only once.
                                                         # "1" = max splits.
                                                         # If message has tabs,
                                                         # they are preserved.
        # Strip leading/trailing whitespace and convert to lowercase.
        label = raw_label.strip().lower()
        # Strip leading/trailing whitespace from the message.
        message = raw_message.strip()                    

        # VALIDATION: The classifier is defined only for HAM and SPAM.
        if label not in EXPECTED_CLASS_LABELS:
            raise DatasetError(
                f"Unsupported label {raw_label!r} at line {line_number}; "
                "expected 'ham' or 'spam'."
            )
        # VALIDATION: A labeled row still needs message content.
        if not message:
            raise DatasetError(f"Blank SMS message at line {line_number}.")

        # INVARIANT: labels[i] and messages[i] describe the same source record.
        labels.append(label)
        messages.append(message)

    # -- PHASE 4: Validate the completed frequency table. --
    #
    # VALIDATION: An empty or malformed frequency table cannot train a model.
    if not labels:
        raise DatasetError("The dataset contains no records.")

    # --- Build M_k class-frequency table ---
    # Counter produces the class-frequency table M_k. Dividing each class count
    # by M later gives the fitted prior P(C_k) = M_k / M.
    class_counts = dict(Counter(labels)) # class-frequency table
    # VALIDATION: Both classes must be present.
    missing_classes = [ # List of missing classes
        class_label
        for class_label in EXPECTED_CLASS_LABELS # HAM or SPAM
        # if the class is not found in the dataset, it is added to the list
        if class_label not in class_counts
    ]
    # VALIDATION: Raise an error if any classes are missing.
    if missing_classes:
        raise DatasetError(
            "Dataset is missing required class(es): " + ", ".join(missing_classes)
        )
    # VALIDATION: Check the record count against the expected count for the mode.
    # Use the expected record count based on the dataset mode.
    expected_count = (
        EXPECTED_COMPLETE_RECORD_COUNT
        if dataset_mode == "complete"
        else EXPECTED_SAMPLE_RECORD_COUNT
    )
    # VALIDATION: Reject truncated, expanded, or accidentally substituted data.
    if len(labels) != expected_count:
        raise DatasetError(
            f"{dataset_mode.capitalize()} dataset contains {len(labels):,} records; "
            f"expected exactly {expected_count:,}."
        )
    # VALIDATION: The bundled sample is a fixed teaching fixture.
    # Its class distribution must match the expected distribution.
    if dataset_mode == "sample" and class_counts != EXPECTED_SAMPLE_CLASS_COUNTS:
        raise DatasetError(
            "Bundled sample class counts changed. Expected "
            f"{EXPECTED_SAMPLE_CLASS_COUNTS}, found {class_counts}."
        )

    # -- PHASE 5: Freeze the validated records and their M_k counts in one object. --
    #
    return SmsDataset(
        labels=np.asarray(labels, dtype=object), # typed record buffer
        messages=tuple(messages),                # tuple of message strings
        source_path=source_path,                 # record origin (absolute path)
        dataset_mode=dataset_mode,               # mode indicator
        text_encoding=text_encoding,             # decoded-text encoding
        class_counts=class_counts,               # class frequency table
    )
# ---

# This function is used by download_uci_dataset() and extract_uci_dataset_zip()
# --- _safe_dataset_member()
def _safe_dataset_member(archive: zipfile.ZipFile) -> zipfile.ZipInfo:
    """Find the expected dataset member and reject unsafe archive paths.

    Args:
        archive: The downloaded ZIP archive.

    Returns:
        The ZipInfo object for the dataset member.
    
    Raises:
        DownloadError: If the ZIP contains an unsafe path.
    """

    # Inspect metadata only.
    dataset_members: list[zipfile.ZipInfo] = []
    # Iterate through the archive members to find the dataset member.
    for member in archive.infolist():
        # Create a pure path to handle the member filename.
        pure_path = PurePosixPath(member.filename)
        # SAFETY CHECK: Reject absolute paths and parent traversal components.
        if pure_path.is_absolute() or ".." in pure_path.parts:
            raise DownloadError(
                f"The downloaded ZIP contains an unsafe path: {member.filename!r}."
            )
        # Directories are not candidate dataset files.
        if member.is_dir():
            continue

        # Match the official member by final filename, independent of a safe
        # containing directory used by the archive.
        if pure_path.name == "SMSSpamCollection":
            dataset_members.append(member)

    # Extraction is unambiguous only when exactly one member matches.
    if len(dataset_members) != 1:
        raise DownloadError(
            "The downloaded ZIP must contain exactly one file named "
            f"'SMSSpamCollection'; found {len(dataset_members)}."
        )
    return dataset_members[0]
# ---

# This function extracts and validates the UCI dataset from an existing ZIP file.
# --- extract_uci_dataset_zip()
def extract_uci_dataset_zip(zip_path: Path, destination_path: Path) -> SmsDataset:
    """Extract and validate the UCI dataset from an existing ZIP file.

    Args:
        zip_path: The path to the downloaded ZIP file.
        destination_path: The path to the destination directory.

    Returns:
        An SmsDataset object containing the extracted dataset.
    
    Raises:
        DatasetError: If the dataset is malformed.
        DownloadError: If the ZIP contains an unsafe path.
    """

    # -- PHASE 0: Resolve both paths and create only the trusted destination folder. --
    #
    zip_path = Path(zip_path).resolve()
    destination_path = Path(destination_path).resolve()
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    # -- PHASE 1: Open the archive, test its stored CRC values, and select one safe --
    #
    # dataset member without extracting arbitrary archive paths.
    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            # SAFETY CHECK: testzip() reports the first corrupt stored member.
            corrupt_member = archive.testzip()
            if corrupt_member is not None:
                raise DownloadError(
                    f"The downloaded ZIP failed its integrity check at {corrupt_member!r}."
                )
            # Read only the validated member into memory.
            dataset_member = _safe_dataset_member(archive)
            dataset_bytes = archive.read(dataset_member)
    except zipfile.BadZipFile as exc:
        raise DownloadError(f"The downloaded file is not a valid ZIP archive: {exc}") from exc
    except OSError as exc:
        raise DownloadError(f"Could not read ZIP archive {zip_path}: {exc}") from exc

    # VALIDATION: An archive may be structurally valid but contain an empty file.
    if not dataset_bytes:
        raise DownloadError("The SMS dataset member in the ZIP archive is empty.")

    # -- PHASE 2: Write beside the final destination so os.replace() can install the --
    # 
    # validated file atomically on the same filesystem.
    with tempfile.NamedTemporaryFile(
        mode="wb",
        prefix="SMSSpamCollection.",
        suffix=".tmp",
        dir=destination_path.parent,
        delete=False,
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)
        temporary_file.write(dataset_bytes)

        # DATA INTEGRITY: Flush Python and operating-system buffers before the
        # temporary file is reopened for complete record validation.
        temporary_file.flush()
        os.fsync(temporary_file.fileno())

    # -- PHASE 3: Validate all 5,574 records before replacing the destination. --
    try:
        validated_dataset = load_sms_dataset(temporary_path, dataset_mode="complete")

        # ATOMIC INSTALL: The destination changes only after validation succeeds.
        os.replace(temporary_path, destination_path)
    except Exception:
        # CLEANUP: Remove an untrusted temporary file and preserve the real error.
        temporary_path.unlink(missing_ok=True)
        raise

    # Return the already validated data with the permanent source path recorded.
    return SmsDataset(
        labels=validated_dataset.labels, # validated dataset labels
        messages=validated_dataset.messages, # validated dataset messages
        source_path=destination_path, # destination path
        dataset_mode="complete", # dataset mode
        text_encoding=validated_dataset.text_encoding, # text encoding
        class_counts=validated_dataset.class_counts, # class counts
    )
# ---


# This function downloads the UCI SMS dataset and saves it to a specified path.
# --- download_uci_dataset()
def download_uci_dataset(destination_path: Path) -> SmsDataset:
    """Download, extract, and validate the  UCI SMS dataset.

    Args:
        destination_path: The path to the destination directory.

    Returns:
        An SmsDataset object containing the extracted dataset.
    
    Raises:
        DatasetError: If the dataset is malformed.
        DownloadError: If the ZIP contains an unsafe path.
    """

    # -- PHASE 0: Resolve the local destination and prepare its parent directory. --
    #
    destination_path = Path(destination_path).expanduser().resolve()
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    # Build one explicit GET request with a project-identifying user agent.
    request = urllib.request.Request(
        OFFICIAL_UCI_ZIP_URL,
        headers={"User-Agent": f"{PROGRAM_NAME}/{PROGRAM_VERSION}"},
        method="GET",
    )

    # -- PHASE 1: Stream network bytes into a temporary ZIP. --
    # 
    with tempfile.NamedTemporaryFile(
        mode="wb", # write binary mode
        prefix="uci_sms_spam.", # prefix for the temporary file
        suffix=".zip.tmp", # suffix for the temporary file
        dir=destination_path.parent, # directory for the temporary file
        delete=False, # do not delete the temporary file
    ) as temporary_file:
        temporary_zip_path = Path(temporary_file.name) # path to the temporary file
        bytes_written = 0

        # NETWORK BOUNDARY: Apply a timeout and read bounded chunks.
        try:
            with urllib.request.urlopen(  # urlopen returns a file-like object for reading from the URL
                request, # the GET request to send
                timeout=DOWNLOAD_TIMEOUT_SECONDS, # timeout in seconds
            ) as response: # response is the downloaded file
                while True:
                    # A fixed chunk size avoids one unbounded response.read().
                    chunk = response.read(64 * 1024)
                    if not chunk:
                        break

                    bytes_written += len(chunk)

                    # SAFETY CHECK: Stop if the transfer exceeds the documented
                    # maximum expected size for this small dataset archive.
                    if bytes_written > MAX_DOWNLOAD_BYTES:
                        raise DownloadError(
                            "The UCI download exceeded the 10 MB safety limit."
                        )
                    temporary_file.write(chunk)

                # DATA INTEGRITY: Finish the temporary ZIP before it is reopened.
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            # EXPECTED FAILURE: Remove the partial transfer and give the user an
            # offline alternative instead of exposing a transport traceback.
            temporary_zip_path.unlink(missing_ok=True)
            raise DownloadError(
                "Could not download the UCI archive. Check the network "
                f"connection or use --sample-data for the bundled teaching sample. "
                f"Technical detail: {exc}"
            ) from exc
        except Exception:
            # CLEANUP: Unexpected errors still remove the partial file, then
            # propagate unchanged so programming defects remain visible.
            temporary_zip_path.unlink(missing_ok=True)
            raise

    # VALIDATION: A successful connection that returns no bytes is still failure.
    if bytes_written == 0:
        temporary_zip_path.unlink(missing_ok=True)
        raise DownloadError("The UCI server returned an empty download.")

    # -- PHASE 2: Apply archive safety and record validation to the completed ZIP. --
    #
    try:
        return extract_uci_dataset_zip(temporary_zip_path, destination_path)
    finally:
        # The transport archive is temporary even after successful installation.
        temporary_zip_path.unlink(missing_ok=True)
# ---
