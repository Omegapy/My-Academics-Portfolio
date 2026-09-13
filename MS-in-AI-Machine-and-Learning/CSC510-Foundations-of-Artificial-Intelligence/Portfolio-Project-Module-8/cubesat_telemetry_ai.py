#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Module Type: executable script
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
# Module Purpose:
# - Connect data preparation, prediction, historical evidence, reasoning, and planning.
# - Reuse one fitted assistant for repeated segment selections during a CLI run.
#
# Usage / Integration:
# - Execute with the parent .venv Python interpreter; --help lists the input modes.
# - The frontend also imports build_assistant() to reuse this backend workflow.
#
# Contents Overview:
# - TelemetryAssistant.analyze() and build_assistant() for reusable fitted state.
# - Demo/interactive coordinators and main() for command-line execution.
#
# Dependencies:
# - Standard Library: sys, dataclasses, pathlib
# - Third-Party: None
# - Local Project: cubesat_cli, cubesat_config, cubesat_data, cubesat_display,
#   cubesat_logic, cubesat_model, cubesat_planner, cubesat_similarity, cubesat_types
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Connect the program's AI methods for one selected telemetry segment.

The command-line run first loads the data and fits a multilayer perceptron (MLP), a neural network
that estimates anomaly probability. It also prepares the shared feature scale and historical
neighbor indexes. Those fitted objects can then be reused for several segment selections.

For each selection, the coordinator asks the backend modules for a prediction, similar cases,
facts, rule-derived conclusions, and a simulated plan. It gathers their outputs into one record
for presentation. The calculations remain in the modules that own them.
"""

# ____________________________________________________________________________________
# ====================================================================================
#
# COMPLETE WORKFLOW MAP
#
# load/validate -> partition -> standardize/train/evaluate -> build historical indexes
# select -> predict -> retrieve -> assert facts -> forward chain -> A-star plan -> display
#
# A telemetry segment is one row of extracted features. Its identifier follows the result
# through each stage, while its reviewed label stays separate from the prediction inputs.
# Forward chaining applies matching rules until no new facts are added. A* uses those results
# to order simulated checks; it does not establish the physical cause of an anomaly.
#
# Backend modules return structured values. The CLI owns raw input, and the display module owns
# presentation. No diagnostic or corrective action is executed.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

import sys 
from dataclasses import dataclass, replace # Import dataclass for data storage.
from pathlib import Path # Import Path for path operations.

# Import cli functions.
from cubesat_cli import (
    parse_cli_arguments, # Parse command line arguments.
    prompt_for_another_analysis, # Prompt for another analysis.
    prompt_segment_selector, # Prompt for segment selector.
)
# Import configuration and app configuration.
from cubesat_config import DEFAULT_CONFIG, AppConfig
# Import data functions.
from cubesat_data import (
    create_dataset_partitions, # Create dataset partitions.
    identify_partition, # Identify partition.
    load_demo_scenarios, # Load demo scenarios.
    load_telemetry_dataset, # Load telemetry dataset.
    select_segment_index, # Select segment index.
)
# Import display functions.
from cubesat_display import render_analysis, render_evaluation
# Import logic functions.
from cubesat_logic import derive_initial_facts, run_forward_chaining
# Import model functions.
from cubesat_model import (
    classify_probability, # Classify probability.
    predict_anomaly_probability, # Predict anomaly probability.
    train_telemetry_model, # Train telemetry model.
)
# Import planner functions.
from cubesat_planner import plan_diagnostic_checks # Plan diagnostic checks.
# Import similarity functions.
from cubesat_similarity import SimilarityIndex, build_similarity_index, find_similar_cases # Find similar cases.
# Import type functions.
from cubesat_types import (
    CompleteAnalysisResult, # Complete analysis result.
    CubeSatError, # CubeSat error.
    DatasetPartitions, # Dataset partitions.
    SegmentSelectionError, # Segment selection error.
    TelemetryDataset, # Telemetry dataset.
    TrainedTelemetryModel, # Trained telemetry model.
)

# __________________________________________
# FITTED APPLICATION STATE
# ==========================================


# --- class TelemetryAssistant
@dataclass(frozen=True, slots=True)
class TelemetryAssistant:
    """Keep fitted state for every analysis requested from this assistant instance.

    The CLI builds one assistant for a run. A frontend process can cache several assistants
    for different profiles or configurations, each retaining its own matching data and model.

    Attributes:
        dataset: Validated authentic or fixture telemetry rows.
        partitions: Explicit model, validation, test, and reference roles.
        trained_model: One fitted MLP and training-only standardizer.
        similarity_index: Reusable normal and anomalous historical indexes.
        config: Shared thresholds, feature order, seed, and source paths for this instance.
    """

    dataset: TelemetryDataset
    partitions: DatasetPartitions
    trained_model: TrainedTelemetryModel
    similarity_index: SimilarityIndex
    config: AppConfig

    # --- analyze()
    def analyze(self, selector: str | int) -> CompleteAnalysisResult:
        """Run one complete analysis without rebuilding fitted state.

        Args:
            selector: Exact segment ID, `#N`, or integer N for a one-based dataset row.

        Returns:
            One segment's source context, probability, historical cases, reasoning, and plan.

        Related Equation Pipeline:
            `X_standardized = (X - mu_training) / sigma_training`
            `p_anomaly = MLP(X_standardized)`
            `facts -> forward chaining -> A-star simulated checks`

        Equation Relationship:
            This method coordinates the backend operations. The called modules evaluate the
            numerical, unification, inference, and planning equations.

        Raises:
            CubeSatError: If selection, model inference, or planning reports a controlled error.
        """
        # __________________________________________
        # SELECTION AND INFERENCE
        # ==========================================
        # PHASE 1: Resolve a stable ID to its source row and retrieve the 18 raw
        # features. Selection does not create a new split or change the fitted model.
        row_index = select_segment_index(self.dataset, selector)
        segment_id = self.dataset.segment_ids[row_index]
        raw_features = self.dataset.x_validated_telemetry_features[row_index]
        # INFERENCE: The model helper reuses training-fitted scaling before prediction.
        anomaly_probability = predict_anomaly_probability(self.trained_model, raw_features)
        # Keep the reviewed label for the result's educational comparison only.
        # It is absent from raw_features and does not determine the estimate above.
        reference_label = "anomalous" if self.dataset.y_anomaly_labels[row_index] else "normal"
        classification = classify_probability(
            segment_id,
            anomaly_probability,
            classification_threshold=self.trained_model.classification_threshold,
            uncertainty_margin=self.trained_model.uncertainty_margin,
            reference_label=reference_label,
            reference_partition=identify_partition(self.partitions, row_index),
        )
        # __________________________________________
        # REVIEWED HISTORICAL COMPARISONS
        # ==========================================
        # PHASE 2: Compare this row with reviewed normal and anomalous cases. Both
        # groups stay visible so historical evidence can agree or disagree with the model.
        similarity = find_similar_cases(
            self.similarity_index,
            self.trained_model,
            classification,
            raw_features,
            config=self.config,
        )
        # __________________________________________
        # SYMBOLIC REASONING
        # ==========================================
        # PHASE 3: Translate documented numerical conditions into starting facts,
        # then let the rule engine derive conclusions and keep their explanation traces.
        asserted_facts, top_deviating_features = derive_initial_facts(
            segment_id=segment_id,
            channel=self.dataset.channels[row_index],
            x_raw_telemetry_features=raw_features,
            trained_model=self.trained_model,
            classification=classification,
            similarity=similarity,
            config=self.config,
        )
        reasoning = run_forward_chaining(
            asserted_facts,
            selected_segment_id=segment_id,
        )
        # __________________________________________
        # SIMULATED PLANNING AND RESULT ASSEMBLY
        # ==========================================
        # PHASE 4: Turn the classification and reasoning into a simulated check plan.
        # The returned record connects every stage without making presentation recalculate it.
        plan = plan_diagnostic_checks(classification, reasoning)
        return CompleteAnalysisResult(
            segment_id=segment_id,
            selected_channel=self.dataset.channels[row_index],
            dataset_profile=self.dataset.profile_name,
            simulated_source=self.dataset.simulated,
            classification=classification,
            similarity=similarity,
            top_deviating_features=top_deviating_features,
            reasoning=reasoning,
            plan=plan,
        )
    # ---
# --- end class TelemetryAssistant


# ________________________________________________
# One-time fitted-state construction
# ------------------------------------------------
# Prepare matching data, model, and reference indexes once for each assistant instance.
# Repeated analyze() calls then reuse this state for the selected segments.
# --- build_assistant()
def build_assistant(
    dataset_path: Path,
    *,
    profile_name: str,
    config: AppConfig = DEFAULT_CONFIG,
) -> TelemetryAssistant:
    """Prepare the state needed to analyze several segments on one consistent scale.

    Args:
        dataset_path: Local feature CSV, already prepared for the requested profile.
        profile_name: `authentic` for pinned source checks or `fixture` for simulated examples.
        config: Shared column order, split/model settings, and comparison thresholds.

    Returns:
        An assistant holding the validated data, row roles, fitted model, and history indexes.

    Raises:
        CubeSatError: If the dataset or fitted model fails a controlled validation check.

    Logic:
        1. Validate the file and establish training, validation, test, and reference row roles.
        2. Fit the model using those roles and select its threshold from validation data.
        3. Build historical indexes from the same standardized feature representation.
    """
    dataset = load_telemetry_dataset(
        dataset_path,
        profile_name=profile_name,
        config=config,
    )
    # Row roles are decided before fitting. The held-out rows remain available for
    # evaluation, while the reference role identifies eligible historical comparisons.
    partitions = create_dataset_partitions(dataset, config=config)
    trained_model = train_telemetry_model(partitions, config=config)
    # Reuse the fitted scale for distance calculations instead of fitting another scaler.
    similarity_index = build_similarity_index(partitions, trained_model, config=config)
    return TelemetryAssistant(
        dataset=dataset,
        partitions=partitions,
        trained_model=trained_model,
        similarity_index=similarity_index,
        config=config,
    )
# ---


# __________________________________________
# EXECUTION MODES
# ==========================================


# --- _run_demo()
def _run_demo(
    assistant: TelemetryAssistant,
    scenario_name: str,
    *,
    color_enabled: bool,
) -> None:
    """Analyze the fixture segments selected by the named scenario metadata.

    Each scenario supplies a segment ID and explanation. Its prediction still comes from
    assistant.analyze(); the JSON metadata does not supply a substitute probability.

    Args:
        assistant: Already fitted assistant using the simulated fixture dataset.
        scenario_name: One supported route name, or `all` for the four demonstration routes.
        color_enabled: Whether the result renderer may color console headings.

    """
    scenarios = load_demo_scenarios(assistant.config.demo_scenarios_path)
    selected_names = (
        ("normal", "anomalous", "uncertain", "conflicting")
        if scenario_name == "all"
        else (scenario_name,)
    )
    # All examples share this assistant so their results come from the same fitted state.
    # Iterate through the selected scenarios.
    for index, selected_name in enumerate(selected_names):
        # Get the scenario.
        scenario = scenarios[selected_name]
        # Print separator if not the first scenario.
        if index:
            print("\n" + "=" * 80 + "\n")
        # Print the scenario name and purpose.
        print(f"Deterministic simulated scenario: {selected_name}")
        print(f"Purpose: {scenario['purpose']}\n")
        print(
            render_analysis(
                assistant.analyze(scenario["segment_id"]),
                color_enabled=color_enabled,
            ),
        )
# ---


# --- _run_interactive()
def _run_interactive(
    assistant: TelemetryAssistant,
    *,
    color_enabled: bool,
) -> int:
    """Keep accepting segment choices while reusing the existing fitted assistant.

    Selection errors are recoverable inside this loop. Other controlled program errors and
    keyboard interrupts are handled by main(), which owns the process exit status.

    Returns:
        Status 0 when the user chooses to stop. A bad segment choice is reported and retried.
    """
    print(
        "CubeSat telemetry AI decision support. Results and checks are simulated/advisory; "
        "the human user decides what to do.",
    )
    # VALIDATION LOOP: Retry a bad selection without rebuilding data or model state.
    while True:
        # Prompt for a segment selection.
        selector = prompt_segment_selector(assistant.dataset.segment_ids)
        # If the user chooses to exit, return 0.
        if selector is None:
            return 0
        # Try to analyze the selected segment.
        try:
            result = assistant.analyze(selector)
        # Catch validation errors.
        except SegmentSelectionError as exc:
            print(f"Validation error: {exc}", file=sys.stderr)
            continue
        print(render_analysis(result, color_enabled=color_enabled))
        if not prompt_for_another_analysis():
            return 0
# ---


# __________________________________________
# MAIN FUNCTION - ENTRY POINT
# ==========================================


# --- main()
def main(arguments: list[str] | None = None) -> int:
    """Run help, demo, evaluation, explicit-segment, or interactive mode.

    argparse handles help and argument syntax with its own SystemExit before fitting begins.

    Args:
        arguments: Option strings supplied by a caller/test, or `None` for the process CLI.

    Returns:
        Process status `0` for success, `2` for controlled validation/execution failure, or `130`
        after an interactive keyboard interrupt.

    Logic:
        1. Parse the requested mode and choose the local source and seed.
        2. Build one assistant, then optionally display its held-out evaluation.
        3. Run the selected demo, explicit segment, or interactive workflow.

    """
    try:
        # __________________________________________
        # CHOOSE THIS RUN'S INPUTS
        # ==========================================
        parsed = parse_cli_arguments(arguments)
        # A replacement carries the chosen seed without modifying the shared defaults.
        config = replace(DEFAULT_CONFIG, random_seed=parsed.seed)
        # Choose the dataset path and profile based on the arguments.
        if parsed.demo is not None: # If demo is not None, use the demo dataset path and profile.
            dataset_path = config.demo_dataset_path # Use the demo dataset path.
            profile_name = "fixture" # Use the fixture profile.
        else: # Otherwise, use the default dataset path and profile.
            dataset_path = parsed.dataset or config.default_dataset_path # Use the default dataset path or the provided dataset path.
            profile_name = parsed.profile # Use the provided profile name.

        # __________________________________________
        # PREPARE FITTED STATE ONCE
        # ==========================================
        assistant = build_assistant(dataset_path, profile_name=profile_name, config=config)
        # Color is useful in a terminal; redirected output should contain plain text.
        color_enabled = not parsed.no_color and sys.stdout.isatty()

        # __________________________________________
        # DISPLAY THE REQUESTED RESULTS
        # ==========================================
        if parsed.evaluate: # If evaluate is not None, display the evaluation.
            print(
                render_evaluation(
                    assistant.trained_model.evaluation, # Display the evaluation.
                    dataset_profile=assistant.dataset.profile_name, # Display the dataset profile.
                    color_enabled=color_enabled, # Display the color enabled.
                ),
            )
            # Evaluation alone is a complete non-interactive request. With a segment
            # or demo, continue to the requested analysis after displaying the metrics.
            if parsed.segment is None and parsed.demo is None:
                return 0
            print()

        # DISPATCH: Reuse the prepared assistant in whichever interaction mode was chosen.
        if parsed.demo is not None:
            _run_demo(assistant, parsed.demo, color_enabled=color_enabled)
            return 0
        if parsed.segment is not None: # If segment is not None, display the analysis.
            print(
                render_analysis(
                    assistant.analyze(parsed.segment), # Display the analysis.
                    color_enabled=color_enabled, # Display the color enabled.
                ),
            )
            return 0
        return _run_interactive(assistant, color_enabled=color_enabled) # Run the interactive mode.
    except CubeSatError as exc: # Catch validation errors.
        # Expected data/model/selection/planning failures get a readable error and
        # nonzero status. Other exception types are not hidden by this handler.
        print(f"Execution error: {exc}", file=sys.stderr) # Print the error.
        return 2
    except KeyboardInterrupt: # Catch keyboard interrupts.
        print("\nInterrupted by user.", file=sys.stderr) # Print the error.
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
