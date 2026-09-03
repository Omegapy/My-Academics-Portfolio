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

"""Present the classifier's step-by-step teaching output.

This module renders program context, model equations, training frequencies, selected word
likelihoods, manual posterior steps, scikit-learn comparisons, predictions, and internal
verification results. It receives calculated values from the model modules and delegates
low-level width and ANSI formatting to `sms_terminal`.
"""


# Display boundary:
# - Display functions explain stored or fitted values unless their local equation block
#   states that they also derive a table value or Laplace example.
#


# =============================================================================
# STANDARD-LIBRARY IMPORTS
# =============================================================================

import sys
from pathlib import Path
from typing import Sequence

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

# pyrefly: ignore [missing-import]
import numpy as np
import sklearn

# =============================================================================
# LOCAL-PROJECT IMPORTS
# =============================================================================

from sms_config import (
    ANSI_BOLD,
    ANSI_GREEN,
    ANSI_RED,
    ANSI_YELLOW,
    COURSE_NAME,
    MAX_RELEVANT_TERMS,
    MAX_TOP_TERMS_PER_CLASS,
    PROBABILITY_TOLERANCE,
    PROGRAM_NAME,
    PROGRAM_VERSION,
    PROJECT_DIRECTORY,
)
from sms_probability import calculate_manual_class_priors, find_zero_frequency_example
from sms_terminal import (
    print_equation,
    print_heading,
    print_labeled_value,
    print_paragraph,
    print_subheading,
    print_table,
    style_text,
)
from sms_types import PosteriorCalculation, TrainedSmsModel, VerificationCheck


# =============================================================================
# TEACHING OUTPUT SECTIONS
# =============================================================================
#
# The assignment requires visible frequency, likelihood, smoothing, posterior,
# and prediction work. These display functions present the already calculated
# values as one connected explanation. They do not alter the fitted model.


# --- display_path()
def display_path(path: Path) -> str:
    """Return a short project-relative path when possible."""

    resolved_path = Path(path).resolve()

    # Prefer a compact project-relative path; retain an absolute path for files
    # outside the project directory.
    try:
        return str(resolved_path.relative_to(PROJECT_DIRECTORY))
    except ValueError:
        return str(resolved_path)
# ---


# --- print_program_banner()
def print_program_banner(use_color: bool) -> None:
    """Print program identity and course context.
    
    Args:
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    print_heading(PROGRAM_NAME, use_color)
    print_labeled_value("Course", COURSE_NAME)
    print_labeled_value("Program version", PROGRAM_VERSION)
    print_labeled_value("Python", sys.version.split()[0])
    print_labeled_value("NumPy", np.__version__)
    print_labeled_value("scikit-learn", sklearn.__version__)
# ---


# -------------------------------------------------------------------
# EQUATION DISPLAY MAP: DEFINE THE FULL PROBABILITY PATH
# counts -> priors and likelihoods -> scores -> posteriors -> argmax
# -------------------------------------------------------------------
#
# Equation relationship: Displays equations and symbol-to-variable mappings.
# The calculation functions later evaluate the equations shown here.
# Boundary: This function does not load data, fit the model, or calculate a posterior.
#
# This function is used in explain_classification_workflow()
# This is for the first section of the explainable classification workflow.
# --- print_model_and_equations()
def print_model_and_equations(use_color: bool) -> None:
    """Display the task, model choice, probability path, and equation map.
    
    Args:
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        None
    
    Boundary: No calculation occurs here; only display formatting.
    """

    # SECTION 1: Establish the complete probability path before any fitted values
    # are shown. Later sections substitute counts and scores into these equations.
    print_heading("1. TASK, MODEL, PARAMETERS, AND EQUATIONS", use_color)
    print_paragraph(
        "This program sorts an SMS message into one of two groups: HAM or SPAM. "
        "CountVectorizer first learns the words used in the UCI SMS dataset. It "
        "then turns each message into word counts. The dataset contains 5,574 "
        "messages. Of these, 4,825 are HAM, which means non-spam, and 747 are SPAM."
    )
    print_paragraph(
        "The program trains MultinomialNB(alpha=1.0) with those word counts. During "
        "training, the model learns how common HAM and SPAM messages are and how "
        "often each word appears in each group. Laplace smoothing keeps a word with "
        "a zero count from making the probability for that whole group zero."
    )
    print_paragraph(
        "When the user enters a message, or the demo supplies one, CountVectorizer "
        "counts only words learned during training. The program then calculates the "
        "chance that the message is HAM and the chance that it is SPAM. It performs "
        "the calculation step by step and compares it with scikit-learn's "
        "predict_proba() result. The class with the higher probability becomes the "
        "prediction."
    )
    print_paragraph(
        "The terminal shows each part of the calculation so the final result is "
        "easier to follow."
    )

    print_subheading("Problem definition", use_color)
    print_labeled_value("Learning setting", "Supervised learning")
    print_labeled_value("Decision", "Binary text classification")
    print_labeled_value("Candidate classes", "HAM and SPAM")
    print_labeled_value("Input x", "One SMS message represented as word counts")
    print_labeled_value("Feature values x_j", "Discrete nonnegative occurrence counts")
    print_labeled_value("Why not regression", "The required output is a class label")

    print_subheading(
    "Why Multinomial Naive Bayes works well with word counts",
    use_color
    )
    print_paragraph(
        "CountVectorizer counts how many times each word appears in a message. "
        "Multinomial Naive Bayes works well with these word counts, which is why "
        "it is often used to classify text. Gaussian Naive Bayes is a better fit "
        "for continuous measurements. Bernoulli Naive Bayes only checks whether "
        "a word appears, so it ignores repeated words."
    )
    print_paragraph(
        "Naive Bayes makes one simplifying assumption. When it scores a message "
        "as spam or not spam, it treats each word as if it were unrelated to the "
        "other words. Real language does not work exactly this way, but this "
        "shortcut lets the model combine what it learned about each word into "
        "one score for each class."
    )
    print_subheading("scikit-learn configuration", use_color)
    parameter_rows = [
        ("CountVectorizer", "lowercase=True", "Convert tokens to lowercase"),
        ("CountVectorizer", "binary=False", "Retain repeated word counts"),
        ("CountVectorizer", "ngram_range=(1, 1)", "Use one-word features"),
        ("MultinomialNB", "alpha=1.0", "Apply Laplace add-one smoothing"),
        ("MultinomialNB", "fit_prior=True", "Estimate P(C_k) from M_k / M"),
        ("MultinomialNB", "force_alpha=True", "Use alpha exactly as supplied"),
    ]
    print_table(
        headers=("Component", "Parameter", "What it controls"),
        rows=parameter_rows,
        widths=(20, 27, 39),
    )

    print_subheading("Bayes' theorem, class ranking, and MAP", use_color)
    print_equation(
        [
            "P(C_k | x) = P(x | C_k) * P(C_k) / P(x)",
            "",
            "For the same input x, P(x) is common to HAM and SPAM:",
            "P(C_k | x) is proportional to P(x | C_k) * P(C_k)",
            "",
            "C_hat = argmax_k P(C_k | x)",
            "",
            "C_k        = candidate class k, HAM or SPAM",
            "x          = input word-count vector",
            "P(C_k)     = prior before the input words are considered",
            "P(x | C_k) = likelihood of those word counts under class C_k",
            "P(C_k | x) = posterior after prior and word evidence are combined",
        ]
    )
    print_paragraph(
        "P(x) has the same value for HAM and SPAM, so it does not change which "
        "class gets the higher score. The program still turns the scores into "
        "probabilities so the two results add up to one."
    )

    print_subheading("Frequency, likelihood, score, and posterior equations", use_color)
    print_equation(
        [
            "Class prior from message frequencies:",
            "    P(C_k) = M_k / M",
            "",
            "Raw word-frequency estimate:",
            "    P_MLE(w_j | C_k) = N_jk / N_k",
            "",
            "Laplace-smoothed estimate used by MultinomialNB:",
            "    P(w_j | C_k) = (N_jk + alpha) / (N_k + alpha * V)",
            "",
            "Message likelihood and unnormalized class score:",
            "    P(x | C_k) = product_j P(w_j | C_k) ** x_j",
            "    score_k = P(C_k) * P(x | C_k)",
            "",
            "Equivalent log-space calculation used by the program:",
            "    log P(x | C_k) = sum_j x_j * log P(w_j | C_k)",
            "    log_score_k = log P(C_k) + log P(x | C_k)",
            "",
            "Stable normalization:",
            "    r_k = exp(log_score_k - max_l log_score_l)",
            "    P(C_k | x) = r_k / sum_l r_l",
        ]
    )

    print_subheading("Equation symbols and source-code variables", use_color)
    symbol_rows = [
        ("M", "m_total_messages", "All labeled training messages"),
        ("M_k", "m_k_class_message_count", "Training messages in class k"),
        ("V", "v_vocabulary_size", "Number of learned word features"),
        ("N_jk", "n_jk_word_count_by_class", "Training count of word j in class k"),
        ("N_k", "n_k_total_word_count_by_class", "All modeled word counts in class k"),
        ("x_j", "x_j_input_word_counts", "Input-message count for word j"),
        ("theta_jk", "theta_hat_jk_word_likelihood", "Smoothed P(word j | class k)"),
        ("P(C_k|x)", "p_c_k_given_x_posterior", "Normalized class posterior"),
        ("argmax", "k_predicted_class_index", "Index of the largest posterior"),
    ]
    print_table(
        headers=("Symbol", "Source variable", "Meaning"),
        rows=symbol_rows,
        widths=(12, 34, 40),
    )
    print_paragraph(
        "Inside calculate_posterior_probabilities(), "
        "x_input_sparse.dot(feature_log_prob_.T) adds up how much the message's "
        "words support HAM and SPAM. Then np.argmax picks the class with the higher "
        "final probability."
    )
# ---


# Frequency-table display helper: Select the largest fitted N_jk counts for one class.
# Boundary: This changes only which rows are shown. It does not change feature_count_.
# --- _top_terms_for_class()
def _top_terms_for_class(
    model: TrainedSmsModel,
    class_index: int,
    limit: int = MAX_TOP_TERMS_PER_CLASS,
) -> list[tuple[str, int]]:
    """Return the highest raw word counts for one fitted class."""

    # Read raw N_jk counts for the requested fitted class.
    class_counts = np.asarray(
        model.classifier.feature_count_[class_index],
        dtype=np.float64,
    )

    # Descending argsort selects the largest counts without changing the model.
    top_indices = np.argsort(class_counts)[::-1][:limit]
    return [
        (str(model.feature_names[index]), int(class_counts[index]))
        for index in top_indices
    ]
# ---


# _________________________________________________________________
# TRAINING TABLE DISPLAY: M, M_K, P(C_K), N_K, AND N_JK
# fitted training data -> frequency-table rows
# _________________________________________________________________
#
# Equation relationship: Coordinates calculation and display of training statistics.
# It calls P(C_k) = M_k / M and evaluates N_k = sum_j N_jk from feature_count_.
# Code map: frequency_rows combines M_k, P(C_k), and N_k in fitted class order.
# Boundary: These values come from training data. The new message is not used here.
# --- print_dataset_and_frequency_tables()
def print_dataset_and_frequency_tables(
    model: TrainedSmsModel,
    use_color: bool,
) -> None:
    """Display the training frequencies used for priors and word likelihoods.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        P(C_k) = M_k / M
        N_k = sum_j N_jk
        
    Boundary: This function does not load data, fit the model, or calculate a posterior.
    """

    # SECTION 2: Show the two count systems learned from the training corpus.
    print_heading("2. DATASET AND FREQUENCY TABLES", use_color)
    dataset = model.dataset
    mode_label = (
        "COMPLETE UCI DATASET"
        if dataset.dataset_mode == "complete"
        else "BUNDLED 100-MESSAGE SAMPLE"
    )
    print_labeled_value("Dataset mode", mode_label)
    print_labeled_value("Dataset path", display_path(dataset.source_path))
    print_labeled_value("Decoded as", dataset.text_encoding)
    print_labeled_value("M, total messages", f"{dataset.m_total_messages:,}")
    print_labeled_value("V, vocabulary size", f"{model.v_vocabulary_size:,}")
    print_paragraph(
        "M_k is the number of messages in each class, and the program uses it to "
        "find each class prior. N_k and N_jk are word counts used to find the "
        "likelihood for each word. Message counts and word counts have different "
        "jobs in the calculation."
    )

    if dataset.dataset_mode == "sample":
        print()
        sample_notice = (
            "SAMPLE MODE: This run uses 100 authentic UCI messages. Its probabilities "
            "will not match those from the complete 5,574-message dataset."
        )
        print_paragraph(sample_notice)

    # Recalculate P(C_k) from M_k and derive N_k from fitted word counts.
    p_c_k_prior = calculate_manual_class_priors(model)
    n_k_total_word_count_by_class = np.asarray(
        model.classifier.feature_count_,
        dtype=np.float64,
    ).sum(axis=1)

    # Build one frequency-table row per class in fitted class order.
    frequency_rows: list[tuple[object, ...]] = []
    for class_index, class_label in enumerate(model.classifier.classes_):
        m_k_class_message_count = dataset.class_counts[str(class_label)]
        frequency_rows.append(
            (
                str(class_label).upper(),
                f"{m_k_class_message_count:,}",
                f"{p_c_k_prior[class_index]:.8f}",
                f"{int(n_k_total_word_count_by_class[class_index]):,}",
            )
        )
    # The total row checks that M_k sums to M and the priors sum to one.
    frequency_rows.append(
        (
            "TOTAL",
            f"{dataset.m_total_messages:,}",
            f"{p_c_k_prior.sum():.8f}",
            f"{int(n_k_total_word_count_by_class.sum()):,}",
        )
    )

    print_subheading("Class counts, priors, and class word totals", use_color)
    print_equation(
        [
            "P(C_k) = M_k / M",
            "N_k = sum_j N_jk",
        ]
    )
    print_table(
        headers=("Class", "M_k messages", "Prior P(C_k)", "N_k word tokens"),
        rows=frequency_rows,
        widths=(14, 18, 20, 31),
        alignments=("<", ">", ">", ">"),
    )
    print_paragraph(
        "M_k counts the labeled messages in one class. The formula P(C_k)=M_k/M "
        "uses that count to find the class prior. N_k counts all word occurrences "
        "in that class. It belongs in the denominator of P(w_j | C_k) and is not "
        "another message count."
    )

    print_subheading("Examples from the class-by-word frequency table", use_color)
    # Print a small sample of N_jk values without implying that omitted words are
    # absent from the fitted vocabulary or the posterior calculation.
    top_rows: list[tuple[str, str, str]] = []
    for class_index, class_label in enumerate(model.classifier.classes_):
        top_terms = _top_terms_for_class(model, class_index)
        for rank, (term, count) in enumerate(top_terms, start=1):
            top_rows.append(
                (str(class_label).upper(), f"{rank}. {term}", f"{count:,}")
            )
    print_table(
        headers=("Class", "Training word w_j", "Count N_jk"),
        rows=top_rows,
        widths=(14, 55, 17),
        alignments=("<", "<", ">"),
    )
    print_paragraph(
        "The table shows only a few of the most common words. The model still keeps "
        "the full table of V words and uses every learned word that appears in the "
        "new message."
    )
# ---


# Message-display selection: Choose which nonzero x_j rows fit the terminal table.
# Boundary: Every nonzero x_j remains in the probability calculation, including omitted rows.
# --- _selected_relevant_indices()
def _selected_relevant_indices(
    result: PosteriorCalculation,
) -> tuple[np.ndarray, int]:
    """Select at most `MAX_RELEVANT_TERMS` nonzero input features.
    
    Args:
        result: PosteriorCalculation containing the feature counts
        
    Returns:
        tuple[np.ndarray, int]: Tuple of selected indices and omitted count
    
    Related equation:
        None
    
    Boundary: Every nonzero x_j remains in the probability calculation, including omitted rows.
    """

    indices = result.relevant_feature_indices

    # Keep every nonzero input term when the table already fits the display limit.
    if indices.size <= MAX_RELEVANT_TERMS:
        return indices, 0

    # Otherwise prefer larger x_j counts and use feature index as a stable tie rule.
    counts = result.x_j_input_word_counts[indices]
    sort_order = np.lexsort((indices, -counts))
    selected = indices[sort_order[:MAX_RELEVANT_TERMS]]
    omitted = int(indices.size - selected.size)
    return np.sort(selected), omitted
# ---


# _________________________________________________________________
# MESSAGE EVIDENCE DISPLAY AND LAPLACE EXAMPLE
# x_j and fitted N_jk -> likelihood rows and one zero-count correction
# _________________________________________________________________
#
# Equation relationship: Displays fitted P(w_j | C_k) values for words with x_j > 0.
# It also evaluates one teaching example twice:
# P_MLE(w_j | C_k) = N_jk / N_k, then
# P(w_j | C_k) = (N_jk + alpha) / (N_k + alpha * V).
# Code map: unsmoothed_probability and smoothed_probability store those two results.
# Boundary: Limiting printed rows does not remove terms from the model calculation.
# --- print_input_frequency_and_likelihoods()
def print_input_frequency_and_likelihoods(
    model: TrainedSmsModel,
    result: PosteriorCalculation,
    use_color: bool,
) -> None:
    """Display the input counts and the fitted likelihoods they activate.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        result: PosteriorCalculation containing the feature counts
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        x_j (word count in this message)
        N_jk (word count in training class k)
        
    Boundary: Limiting printed rows does not remove terms from the model calculation.
    """

    # SECTION 3: Connect this message's x_j values to training-corpus N_jk values.
    print_heading("3. INPUT WORD COUNTS, LIKELIHOODS, AND LAPLACE CORRECTION", use_color)
    print_subheading(
        style_text("Input message", ANSI_BOLD + ANSI_RED, use_color),
    )
    print_paragraph(
        f'"{result.message}"',
        indent=2,
        ansi_code=ANSI_RED,
        use_color=use_color,
    )
    print_paragraph(
        "Here, CountVectorizer works on the new message only. Its x_j values show "
        "how many times each known word appears in that message. The N_jk values "
        "come from the training messages and show how often those words appeared "
        "in each class."
    )

    # Limit only the printed table. The complete sparse vector remains in the math.
    selected_indices, omitted_count = _selected_relevant_indices(result)
    print_subheading("Input vector x: nonzero word counts", use_color)
    word_count_rows = [
        (
            str(model.feature_names[feature_index]),
            int(result.x_j_input_word_counts[feature_index]),
        )
        for feature_index in selected_indices
    ]
    print_table(
        headers=("Vocabulary word w_j", "Input count x_j"),
        rows=word_count_rows,
        widths=(65, 24),
        alignments=("<", ">"),
    )
    print_paragraph(
        "The table only needs to show words with x_j > 0. When x_j = 0, the word "
        "adds 0 * log P(w_j | C_k) = 0 to both class scores."
    )
    if omitted_count:
        print_paragraph(
            f"{omitted_count} more nonzero input terms are left out of the table to "
            "keep it within 92 columns. The calculation still uses those terms."
        )

    print_subheading("Class-conditional likelihoods used for this message", use_color)
    print_equation(
        [
            "Raw estimate:      P_MLE(w_j | C_k) = N_jk / N_k",
            "Fitted estimate:   P(w_j | C_k)",
            "                 = (N_jk + alpha) / (N_k + alpha * V)",
            "alpha = 1.0",
        ]
    )

    ham_index = model.class_to_index["ham"]
    spam_index = model.class_to_index["spam"]
    feature_count = np.asarray(model.classifier.feature_count_, dtype=np.float64)
    feature_probability = np.exp(model.classifier.feature_log_prob_)

    # For each displayed input word, pair its x_j value with the training counts
    # N_j,HAM and N_j,SPAM and the corresponding smoothed likelihoods.
    likelihood_rows: list[tuple[object, ...]] = []
    for feature_index in selected_indices:
        likelihood_rows.append(
            (
                str(model.feature_names[feature_index]),
                int(result.x_j_input_word_counts[feature_index]),
                int(feature_count[ham_index, feature_index]),
                f"{feature_probability[ham_index, feature_index]:.8f}",
                int(feature_count[spam_index, feature_index]),
                f"{feature_probability[spam_index, feature_index]:.8f}",
            )
        )
    print_table(
        headers=("Word", "x_j", "N_j,HAM", "P(w|HAM)", "N_j,SPAM", "P(w|SPAM)"),
        rows=likelihood_rows,
        widths=(20, 6, 10, 14, 11, 16),
        alignments=("<", ">", ">", ">", ">", ">"),
    )
    print_paragraph(
        "Each P(w_j | C_k) describes how likely one word is for one class. It is "
        "only one part of the calculation, not the final P(C_k | x). The model "
        "combines all of these word likelihoods with x_j and the class prior."
    )

    print_subheading("A real zero count and its Laplace correction", use_color)
    # Select an observed N_jk=0 cell so the output can substitute real values into
    # both the raw relative-frequency estimate and the alpha=1 Laplace estimate.
    zero_class_index, zero_feature_index = find_zero_frequency_example(
        model,
        preferred_feature_indices=selected_indices,
    )
    zero_class_label = str(model.classifier.classes_[zero_class_index]).upper()
    zero_word = str(model.feature_names[zero_feature_index])
    n_jk_zero = float(feature_count[zero_class_index, zero_feature_index])
    n_k_total = float(feature_count[zero_class_index].sum())
    alpha_smoothing = float(model.classifier.alpha)
    v_vocabulary_size = model.v_vocabulary_size
    # Both estimates use the same observed N_jk and N_k. Smoothing changes only the
    # probability estimate, not the stored training count.
    unsmoothed_probability = 0.0 if n_jk_zero == 0.0 else n_jk_zero / n_k_total
    smoothed_probability = (
        n_jk_zero + alpha_smoothing
    ) / (
        n_k_total + alpha_smoothing * v_vocabulary_size
    )

    print_labeled_value("Example word w_j", zero_word)
    print_labeled_value("Example class C_k", zero_class_label)
    print_labeled_value("Observed training count N_jk", int(n_jk_zero))
    print_equation(
        [
            "Raw relative-frequency estimate:",
            f"    P_MLE({zero_word} | {zero_class_label})",
            f"        = {int(n_jk_zero)} / {int(n_k_total)}",
            f"        = {unsmoothed_probability:.12f}",
            "",
            "Laplace estimate used by the fitted model:",
            f"    P({zero_word} | {zero_class_label})",
            f"        = ({int(n_jk_zero)} + 1)",
            f"          / ({int(n_k_total)} + 1 * {v_vocabulary_size})",
            f"        = {smoothed_probability:.12f}",
        ]
    )
    print_paragraph(
        "The word still has a count of zero for this class. Laplace smoothing does "
        "not change that count. It only gives the word a small positive likelihood "
        "so one unseen word cannot reduce the entire class score to zero."
    )
# ---


# Equation display helper: Expand one stored log_score_k into readable symbolic terms.
# Boundary: This creates text only. calculate_posterior_probabilities() did the arithmetic.
# --- _expanded_log_expression()
def _expanded_log_expression(
    model: TrainedSmsModel,
    result: PosteriorCalculation,
    class_index: int,
    selected_indices: np.ndarray,
) -> str:
    """Build a readable multiline expansion for one class log score.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        result: PosteriorCalculation containing the feature counts and log scores
        class_index: Index of the class for which to expand the log score
        selected_indices: Array of feature indices to include in the expansion
        
    Returns:
        str: Multiline string representing the expanded log score expression
    
    Related equation:
        log_score_k = log P(C_k) + sum_j x_j * log P(w_j | C_k)
        
    Boundary: Limiting printed terms does not alter the stored numerical result.
    """

    # Expand only the displayed x_j > 0 terms. This changes presentation only; the
    # stored numerical result was calculated with the complete sparse input vector.
    class_label = str(model.classifier.classes_[class_index]).upper()
    expression_lines = [
        f"log_score_{class_label} =",
        f"    log P({class_label})",
    ]
    expression_lines.extend(
        f"    + {int(result.x_j_input_word_counts[feature_index])} * "
        f"log P({model.feature_names[feature_index]} | {class_label})"
        for feature_index in selected_indices
    )
    if result.relevant_feature_indices.size > selected_indices.size:
        expression_lines.append("    + [remaining modeled input terms]")
    return "\n".join(expression_lines)
# ---


# ------------------------------------------------------------------
# POSTERIOR PIPELINE DISPLAY
# stored log likelihoods and scores -> displayed P(C_k | x)
# ------------------------------------------------------------------
#
# Equation relationship: Displays previously calculated values for each posterior step.
# It shows log P(x | C_k), log_score_k, shifted score r_k, and normalized P(C_k | x).
# Boundary: This function does not recalculate the posterior or choose the class.
#
# This function is used in explain_classification_workflow()
# This is for the second section of the explainable classification workflow.
# --- print_manual_posterior_calculation()
def print_manual_posterior_calculation(
    model: TrainedSmsModel,
    result: PosteriorCalculation,
    use_color: bool,
) -> None:
    """Display how each class log score becomes a normalized posterior.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        result: PosteriorCalculation containing log scores and posterior
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        log P(x | C_k) = sum_j x_j * log P(w_j | C_k)
        log_score_k = log P(C_k) + log P(x | C_k)
        r_k = exp(log_score_k - max_l log_score_l)
        P(C_k | x) = r_k / sum_l r_l
        
    Boundary: This function displays computed values but does not perform new calculations.
    """

    # SECTION 4: Trace each class from log prior and message likelihood through
    # the stability shift and final posterior normalization.
    print_heading("4. MANUAL NAIVE BAYES POSTERIOR CALCULATION", use_color)
    print_subheading("From message likelihood to posterior", use_color)
    print_equation(
        [
            "log P(x | C_k) = sum_j x_j * log P(w_j | C_k)",
            "log_score_k = log P(C_k) + log P(x | C_k)",
            "",
            "r_k = exp(log_score_k - max_l log_score_l)",
            "P(C_k | x) = r_k / sum_l r_l",
        ]
    )
    print_paragraph(
        "Multiplying many very small word probabilities can produce a number too "
        "small for the computer to store accurately. The program uses logarithms "
        "to turn the multiplication into addition. It also shifts both scores by "
        "the same amount before exponentiation. These steps keep the calculation "
        "stable without changing which class wins."
    )

    selected_indices, _ = _selected_relevant_indices(result)

    # Display the same sequence for each class so the two alternatives can be
    # compared term by term.
    for class_index, class_label in enumerate(model.classifier.classes_):
        class_label_upper = str(class_label).upper()
        print_subheading(f"Class {class_label_upper}", use_color)
        expression = _expanded_log_expression(
            model,
            result,
            class_index,
            selected_indices,
        )
        print_equation(expression.splitlines())
        print_labeled_value(
            f"Log prior, log P({class_label_upper})",
            f"{model.classifier.class_log_prior_[class_index]:.12f}",
        )
        print_labeled_value(
            "Message log likelihood",
            f"{result.log_p_x_given_c_k_likelihood[class_index]:.12f}",
        )
        print_labeled_value(
            "Unnormalized class log score",
            f"{result.log_score_c_k[class_index]:.12f}",
        )
        print_labeled_value(
            "Shifted relative score r_k",
            f"{result.shifted_exponential_score_c_k[class_index]:.12f}",
        )
        print_labeled_value(
            f"Posterior P({class_label_upper} | x)",
            f"{result.p_c_k_given_x_posterior[class_index]:.12f}",
        )

    print_subheading("Normalization check", use_color)
    print_labeled_value("Largest class log score", f"{result.max_log_score:.12f}")
    print_labeled_value(
        "Sum of shifted scores",
        f"{result.shifted_exponential_score_c_k.sum():.12f}",
    )
    print_labeled_value(
        "Sum of manual posteriors",
        f"{result.p_c_k_given_x_posterior.sum():.12f}",
    )
    print_paragraph(
        "r_k is a temporary score, not a probability yet. The program divides each "
        "r_k by the total of both scores. This produces the two posterior "
        "probabilities and makes them add up to one."
    )
# ---


# -----------------------------------------------------------------
# PREDICTION COMPARISON AND DECISION DISPLAY
# manual posterior vs predict_proba() -> stored argmax class
# -----------------------------------------------------------------
#
# Equation relationship: Displays the two posterior vectors and checks their stored difference.
# Code map: k_predicted_class_index is k from argmax_k P(C_k | x).
# Boundary: calculate_posterior_probabilities() already evaluated posterior and argmax.
# This function formats the comparison, maps k to HAM or SPAM, and explains the result.
#
# This function is used in explain_classification_workflow()
# This is for the third section of the explainable classification workflow.
# --- print_prediction_and_verification()
def print_prediction_and_verification(
    model: TrainedSmsModel,
    result: PosteriorCalculation,
    use_color: bool,
) -> None:
    """Compare posterior calculations and report the MAP class decision.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        result: PosteriorCalculation containing log scores and posterior
        use_color: Whether to use color output
        
    Returns:
        None
    
    Related equation:
        argmax_k P(C_k | x)
        
    Boundary: This function compares computed values but does not perform new calculations.
    """

    # SECTION 5: Check the reconstructed posteriors against predict_proba(), then
    # translate the winning argmax index into the final class label.
    print_heading("5. SCIKIT-LEARN COMPARISON AND FINAL PREDICTION", use_color)
    print_paragraph(
        "Both columns come from the same trained MultinomialNB model. The manual "
        "column shows the calculation steps, while predict_proba() shows "
        "scikit-learn's answer. If the values match, the program's probability "
        "calculation is working as intended. This comparison does not measure how "
        "well the model classifies new labeled messages."
    )

    comparison_rows: list[tuple[str, str, str, str]] = []
    for class_index, class_label in enumerate(model.classifier.classes_):
        manual_probability = result.p_c_k_given_x_posterior[class_index]
        library_probability = result.sklearn_p_c_k_given_x_posterior[class_index]
        comparison_rows.append(
            (
                str(class_label).upper(),
                f"{manual_probability:.12f}",
                f"{library_probability:.12f}",
                f"{abs(manual_probability - library_probability):.3e}",
            )
        )

    print_table(
        headers=("Class", "Manual P(C_k|x)", "sklearn P(C_k|x)", "Absolute difference"),
        rows=comparison_rows,
        widths=(12, 22, 22, 27),
        alignments=("<", ">", ">", ">"),
    )

    # Require probability agreement for every class, not merely the same label.
    probability_match = (
        result.max_absolute_probability_difference <= PROBABILITY_TOLERANCE
    )
    verification_text = "PASS" if probability_match else "FAIL"
    verification_color = ANSI_GREEN if probability_match else ANSI_RED
    print()
    print_labeled_value(
        "Largest probability difference",
        f"{result.max_absolute_probability_difference:.3e}",
    )
    print_labeled_value("Allowed numerical tolerance", f"{PROBABILITY_TOLERANCE:.1e}")
    print_labeled_value(
        "Manual calculation matches",
        style_text(verification_text, verification_color + ANSI_BOLD, use_color),
    )
    print_paragraph(
        "PASS means the manual probability for each class matches predict_proba() "
        "within the small rounding difference allowed above."
    )

    # Translate the argmax array index back to the fitted class label.
    k_predicted_class_index = result.k_predicted_class_index
    predicted_class = str(
        model.classifier.classes_[k_predicted_class_index]
    ).upper()
    winning_probability = result.p_c_k_given_x_posterior[
        k_predicted_class_index
    ]
    ham_index = model.class_to_index["ham"]
    spam_index = model.class_to_index["spam"]

    print_subheading("Maximum a posteriori (MAP) decision", use_color)
    print_equation(
        [
            "C_hat = argmax_k P(C_k | x)",
            "argmax returns k, the class index with the largest posterior.",
        ]
    )
    print_labeled_value(
        "P(HAM | message)",
        f"{result.p_c_k_given_x_posterior[ham_index]:.12f}",
    )
    print_labeled_value(
        "P(SPAM | message)",
        f"{result.p_c_k_given_x_posterior[spam_index]:.12f}",
    )
    print_labeled_value("Predicted class", predicted_class)
    print_labeled_value("Winning posterior", f"{winning_probability:.12f}")
    print_labeled_value("Winning percentage", f"{winning_probability * 100:.2f}%")
    print_paragraph(
        "The model compares the two posterior probabilities and picks the larger "
        "one. argmax does this comparison. It does not use an extra cutoff for SPAM."
    )

    if model.dataset.dataset_mode == "sample":
        print_paragraph(
            "Sample mode trains on 100 authentic UCI messages. The full model trains "
            "on 5,574 messages, so it can learn different class priors and word "
            "likelihoods. Its final probabilities may be different."
        )

    print_subheading("Final classification summary", use_color)
    print_paragraph(
        f'Input message: "{result.message}"',
        ansi_code=ANSI_GREEN + ANSI_BOLD,
        use_color=use_color,
    )
    print_labeled_value(
        "HAM percentage",
        style_text(
            f"{result.p_c_k_given_x_posterior[ham_index] * 100:.2f}%",
            ANSI_YELLOW + ANSI_BOLD,
            use_color,
        ),
    )
    print_labeled_value(
        "SPAM percentage",
        style_text(
            f"{result.p_c_k_given_x_posterior[spam_index] * 100:.2f}%",
            ANSI_YELLOW + ANSI_BOLD,
            use_color,
        ),
    )
    print_paragraph(
        f"Conclusion: It is {predicted_class}.",
        ansi_code=ANSI_RED + ANSI_BOLD,
        use_color=use_color,
    )
# ---


# =============================================================================
# INTERNAL VERIFICATION
# =============================================================================

# Verification display boundary: Convert completed checks into a terminal report.
# This function does not repeat the equation calculations that produced each check.
# --- print_internal_verification()
def print_internal_verification(
    model: TrainedSmsModel,
    checks: Sequence[VerificationCheck],
    use_color: bool,
) -> bool:
    """Print internal checks and return True only if every check passed.
    
    Args:
        model: TrainedSmsModel containing the frequency tables
        checks: Sequence of VerificationCheck objects
        use_color: Whether to use color output
        
    Returns:
        bool: True if all checks passed, False otherwise
    
    Related equation:
        None
    
    Boundary: This function displays computed values but does not perform new calculations.
    """

    print_program_banner(use_color)
    print_heading("INTERNAL VERIFICATION", use_color)
    print_labeled_value("Dataset mode", model.dataset.dataset_mode.upper())
    print_labeled_value("Dataset path", display_path(model.dataset.source_path))
    print_labeled_value("Tolerance", f"{PROBABILITY_TOLERANCE:.1e}")
    print_paragraph(
        "These checks compare the program's counts and probabilities with "
        "scikit-learn and also test a few example messages. They show whether both "
        "calculations agree. They do not measure accuracy on a separate test dataset."
    )

    # Convert structured check results into a fixed-width terminal table.
    rows: list[tuple[str, str, str]] = []
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        rows.append((check.name, status, check.detail))
    print()
    print_table(
        headers=("Check", "Result", "Observed detail"),
        rows=rows,
        widths=(42, 8, 36),
    )

    # Return one process-level result after every individual observation is shown.
    all_passed = all(check.passed for check in checks)
    print()
    if all_passed:
        print(
            style_text(
                "All internal verification checks passed.",
                ANSI_GREEN + ANSI_BOLD,
                use_color,
            )
        )
    else:
        failed_count = sum(not check.passed for check in checks)
        print(
            style_text(
                f"Internal verification failed: {failed_count} check(s) did not pass.",
                ANSI_RED + ANSI_BOLD,
                use_color,
            )
        )
    return all_passed
# ---
