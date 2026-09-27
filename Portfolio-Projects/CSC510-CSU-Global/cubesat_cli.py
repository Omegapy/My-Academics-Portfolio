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
#
# Assignment Requirements:
# - Provide help, authentic data, segment, evaluation, demo, seed, and no-color options.
# - Re-prompt invalid interactive input and reject invalid non-interactive combinations.
#
# Module Purpose:
# - Own raw command-line arguments and interactive text input.
# - Return validated values without running backend calculations.
#
# Usage / Integration:
# - Imported by the executable coordinator.
#
# Contents Overview:
# - Parser construction, argument validation, segment prompting, and repeat prompting.
#
# Dependencies:
# - Standard Library: argparse, pathlib
# - Third-Party: None
# - Local Project: cubesat_config, cubesat_types
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Collect command-line options and interactive selections for the coordinator.

The command-line interface (CLI) turns text options into values such as a dataset path or segment
selector. The coordinator then loads the chosen data and runs the analysis. Keeping those steps
separate lets a user request help or receive an option error before a model is fitted.

Interactive helpers collect text and yes/no choices. The data module checks whether a segment
selector exists in the loaded dataset; this module does not calculate or render analysis results.
"""

# __________________________________________
# IMPORTS
# ==========================================

import argparse
from pathlib import Path

from cubesat_config import DEFAULT_CONFIG
from cubesat_types import SegmentSelectionError

# __________________________________________
# ARGUMENT PARSING
# ==========================================


# ________________________________________________
# Option declarations and help
# ------------------------------------------------
# Declare accepted options and help text before any dataset is loaded or model is fitted.
# --- build_argument_parser()
def build_argument_parser() -> argparse.ArgumentParser:
    """Define the supported options without parsing them or starting an analysis.
        This function builds the argument parser for the CLI.

    Returns:
        An argparse parser that also provides the program's `--help` response.
    """
    # This parser builds the argument parser for the CLI.
    parser = argparse.ArgumentParser(
        prog="cubesat_telemetry_ai.py",
        description=(
            "Analyze OPS-SAT telemetry with an MLP, historical similarity, Horn-rule "
            "reasoning, and simulated A-star diagnostic planning. Results are advisory."
        ),
        epilog="The human user retains final interpretation and action authority.",
    )
    # The dataset option is used to specify the path to the dataset.csv file.
    parser.add_argument(
        "--dataset",
        type=Path,
        help="Path to a prepared OPS-SAT-AD-compatible dataset.csv file.",
    )
    # The profile option is used to specify the validation profile.
    parser.add_argument(
        "--profile",
        choices=("authentic", "fixture"),
        default="authentic",
        help="Validation profile for --dataset (default: authentic).",
    )
    # The segment option is used to specify the segment identifier.
    parser.add_argument(
        "--segment",
        help="Exact segment identifier or #<one-based-row-index> for non-interactive analysis.",
    )
    # The evaluate option is used to specify whether to evaluate the model.
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Display held-out precision, recall, F1, accuracy, and confusion matrix.",
    )
    # A bare --demo selects all examples. With a value, it selects one named route;
    # the coordinator later resolves that name to an actual fixture segment.
    parser.add_argument(
        "--demo",
        nargs="?",
        const="all",
        choices=("all", "normal", "anomalous", "uncertain", "conflicting"),
        help=(
            "Use the deterministic simulated fixture; optionally select one route "
            "(default: all)."
        ),
    )
    # The seed option is used to specify the random seed.
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_CONFIG.random_seed,
        help=f"Reproducible split and MLP seed (default: {DEFAULT_CONFIG.random_seed}).",
    )
    # The no-color option is used to specify whether to disable color output.
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color so output remains stable for capture and automated checks.",
    )
    return parser
# ---


# ________________________________________________
# Execution-mode validation
# ------------------------------------------------
# Reject competing dataset and segment choices before the coordinator starts backend work.
# --- parse_cli_arguments()
def parse_cli_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    """Parse and validate CLI arguments without starting backend work.

    Args:
        arguments: Explicit option strings for a test/caller, or `None` to read the process CLI.

    Returns:
        Named option values used by the coordinator to choose the data and execution mode.

    Raises:
        SegmentSelectionError: If options select incompatible execution modes.
        SystemExit: If argparse handles help or rejects an unknown/malformed option.
    """
    parsed = build_argument_parser().parse_args(arguments)
    # VALIDATION: A named demo already chooses its dataset and segment. Reject
    # competing choices rather than silently ignoring one of the user's options.
    if parsed.demo is not None and parsed.dataset is not None:
        raise SegmentSelectionError("--demo uses the bundled fixture and cannot use --dataset")
    if parsed.demo is not None and parsed.segment is not None:
        raise SegmentSelectionError("--demo selects its own scenario segment; omit --segment")
    # authentic is the parser default, not the profile a demo will use. The
    # coordinator switches every demo to fixture validation after parsing succeeds.
    if parsed.demo is not None and parsed.profile != "authentic":
        raise SegmentSelectionError("--demo selects fixture validation automatically")
    return parsed
# ---


# __________________________________________
# INTERACTIVE INPUT
# ==========================================


# --- prompt_segment_selector()
def prompt_segment_selector(segment_ids: tuple[str, ...]) -> str | None:
    """Prompt for an exact segment identifier, a one-based index, or quit.

    The coordinator passes the text to dataset selection and re-prompts after a controlled
    selection error. Keeping the text intact lets an exact numeric-looking ID take precedence
    over a row number; `#1` explicitly means the first row.

    Args:
        segment_ids: IDs from the loaded dataset, used only to show a short example list.

    Returns:
        Stripped selector text, or `None` when the user enters a quit choice.

    """
    # This function prompts the user for a segment identifier.
    # The segment identifier is used to specify the segment to analyze.
    # The segment identifier can be either an exact segment identifier or a one-based index.
    # The segment identifier can also be a quit choice, which will return None.

    # Display the first 5 segment IDs as examples.
    preview = ", ".join(segment_ids[:5])

    # If there are more than 5 segment IDs, add "..." to the preview    .
    if len(segment_ids) > 5:
        preview += ", ..."
        
    # Print the available segment examples.
    print(f"Available segment examples: {preview}")
    
    # Prompt the user for a segment identifier.
    raw_selector = input("Segment ID or #<row index> (q to quit): ").strip()
    # Check if the user wants to quit.
    if raw_selector.lower() in {"q", "quit", "exit"}:
        return None
    return raw_selector
# ---


# --- prompt_for_another_analysis()
def prompt_for_another_analysis() -> bool:
    """Return a valid repeat choice so the coordinator can reuse its fitted model."""
    # VALIDATION LOOP: A typo is not treated as a decision to stop or retrain.
    # This function prompts the user for whether they want to analyze another segment.
    # It will keep prompting until the user enters a valid choice.
    
    while True:
        # Prompt the user for whether they want to analyze another segment.
        response = input("Analyze another segment? [y/n]: ").strip().lower()
        # Check if the user wants to analyze another segment.
        if response in {"y", "yes"}:
            return True
        # Check if the user does not want to analyze another segment.
        if response in {"n", "no"}:
            return False
        print("Enter y or n.")
# ---


# __________________________________________
# END OF FILE
# ==========================================
