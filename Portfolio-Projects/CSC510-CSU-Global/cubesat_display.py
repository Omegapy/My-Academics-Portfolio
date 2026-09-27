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
# Module Purpose:
# - Convert stored classifier, historical, reasoning, and planning results to console text.
# - Keep each result's source and advisory limits visible to the reader.
#
# Usage / Integration:
# - The CLI coordinator prints the strings returned by these renderers.
#
# Contents Overview:
# - Heading and historical-case formatting helpers.
# - render_evaluation() for held-out metrics and render_analysis() for one segment.
#
# Dependencies:
# - Standard Library: None
# - Third-Party: None
# - Local Project: cubesat_types
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Turn a completed analysis into a readable console explanation.

The reader sees the selected segment, classifier result, historical comparisons, reasoning,
and simulated plan in that order. Each renderer receives values already calculated by the
backend and returns a string. The coordinator owns printing that string to the terminal.

Formatting a probability or distance changes its displayed precision only. This module does
not fit a model, change a decision, assert facts, or search for a plan.
"""

# __________________________________________
# IMPORTS
# ==========================================

from cubesat_types import CompleteAnalysisResult, EvaluationMetrics, SimilarCase

# __________________________________________
# PRESENTATION HELPERS
# ==========================================


# --- _heading()
def _heading(title: str, *, color_enabled: bool) -> str:
    """Return one stable section heading with optional cyan ANSI styling."""
    if color_enabled:
        return f"\033[1;36m{title}\033[0m"
    return title
# ---


# --- _render_case()
def _render_case(similar_case: SimilarCase) -> str:
    """Describe one ranked case using its stored distance and feature differences.

    The differences compare standardized coordinates, not sensor units or model feature
    importance. The similarity module has already selected and ordered them.
    """
    differences = ", ".join(
        f"{difference.feature_name}={difference.absolute_standardized_difference:.3f}"
        for difference in similar_case.feature_differences
    )
    return (
        f"  {similar_case.rank}. {similar_case.case_id} | reviewed "
        f"{similar_case.reviewed_label} | distance={similar_case.distance:.4f} | "
        f"largest standardized differences: {differences}"
    )
# ---


# __________________________________________
# EVALUATION DISPLAY
# ==========================================


# --- render_evaluation()
def render_evaluation(
    evaluation: EvaluationMetrics,
    *,
    dataset_profile: str,
    color_enabled: bool,
) -> str:
    """Format classifier performance measured on rows reserved for testing.

    Args:
        evaluation: Metrics and threshold already calculated by the model module.
        dataset_profile: Source role used to label fixture versus authentic-run limitations.
        color_enabled: Whether headings may contain terminal color escape sequences.

    Returns:
        A multiline report; no metrics are recomputed and nothing is printed here.
    """
    # Rows describe reviewed labels and columns describe predictions, in [normal,
    # anomalous] order. Naming the four cells makes false alarms and missed anomalies
    # easier to distinguish when reading the printed matrix.
    (true_normal, false_alarm), (missed_anomaly, detected_anomaly) = (
        evaluation.confusion_matrix
    )

    # Return a multiline report with the evaluation metrics.
    lines = [
        _heading("Held-out classifier evaluation", color_enabled=color_enabled),
        f"Dataset profile: {dataset_profile}",
        f"Samples: {evaluation.test_sample_count}",
        f"Validation-selected threshold: {evaluation.classification_threshold:.4f}",
        f"Precision: {evaluation.precision:.4f}",
        f"Recall: {evaluation.recall:.4f}",
        f"F1 score: {evaluation.f1_score:.4f}",
        f"Accuracy: {evaluation.accuracy:.4f} (supplementary, not the only metric)",
        "Confusion matrix [[true normal, false alarm], [missed anomaly, detected anomaly]]:",
        f"  [[{true_normal}, {false_alarm}], [{missed_anomaly}, {detected_anomaly}]]",
        f"Training iterations: {evaluation.training_iterations}",
    ]   
    # Add a limitation to the evaluation metrics.
    if dataset_profile == "fixture": # Check if the dataset profile is "fixture".
        lines.append(
            "Limitation: simulated fixture metrics are workflow evidence, not OPS-SAT benchmark "
            "performance.",
        )
    else:
        lines.append(
            "Limitation: these are observed results from this run; no published benchmark metric "
            "is claimed as reproduced.",
        )
    return "\n".join(lines)
# ---


# __________________________________________
# COMPLETE ANALYSIS DISPLAY
# ==========================================


# --- render_analysis()
def render_analysis(
    result: CompleteAnalysisResult,
    *,
    color_enabled: bool,
) -> str:
    """Build the six-section explanation for one selected telemetry segment.

    Args:
        result: Complete backend result, including source, probability, evidence, and plan.
        color_enabled: Whether headings may contain terminal color escape sequences.

    Returns:
        Joined console text in the same order as the analysis workflow.

    Logic:
        1. Establish the selected segment and data source before showing its prediction.
        2. Show historical evidence, then the facts and rules used for reasoning.
        3. Show the simulated plan and keep final interpretation with the human reader.
    """
    # __________________________________________
    # SEGMENT AND CLASSIFICATION CONTEXT
    # ==========================================
    # Format the stored source and classifier result before presenting its supporting evidence.
    # Get the classification, similarity, reasoning, and plan from the result.
    classification = result.classification # Get the classification from the result.
    similarity = result.similarity # Get the similarity from the result.
    reasoning = result.reasoning # Get the reasoning from the result.
    plan = result.plan # Get the plan from the result.
    lines: list[str] = [] # Initialize the lines list.

    # Add the classification and similarity to the lines list.
    lines.extend(
        [
            _heading("1. Selected telemetry segment", color_enabled=color_enabled),
            f"Segment ID: {result.segment_id}",
            f"Channel: {result.selected_channel}",
            f"Dataset profile: {result.dataset_profile}",
            "Source status: "
            + (
                "simulated deterministic fixture"
                if result.simulated_source
                else "authentic OPS-SAT-AD input"
            ),
            "",
            _heading("2. Classifier result", color_enabled=color_enabled),
            f"Predicted class: {classification.predicted_class}",
            f"Anomaly probability ({classification.probability_source}): "
            f"{classification.anomaly_probability:.4f}",
            f"Validation-selected threshold: {classification.classification_threshold:.4f}",
            f"Uncertainty margin: +/-{classification.uncertainty_margin:.4f}",
            f"Decision state: {classification.decision_state.value}",
            f"Reference partition: {classification.reference_partition}",
        ],
    )
    # A reviewed label helps a student compare the estimate with an existing label.
    # It is displayed separately so it is not mistaken for an input to this prediction.
    if classification.reference_label is not None: # Check if the reference label is not None.
        lines.append(
            "Reviewed reference label (educational evaluation only; not a model input): "
            f"{classification.reference_label}",
        )

    # __________________________________________
    # HISTORICAL COMPARISONS
    # ==========================================
    # Render the retrieved cases and comparison outcome already supplied by similarity search.
    # Add the similarity to the lines list.
    lines.extend(
        [
            "",
            _heading("3. Historical evidence", color_enabled=color_enabled),
            f"Metric: {similarity.metric}; up to {similarity.neighbors_per_class} per class",
            "Similar reviewed normal cases:",
        ],
    )
    # Keep the two reviewed classes separate. An empty group is missing comparison
    # evidence, so the report says so instead of presenting an invented neighbor.
    lines.extend(_render_case(case) for case in similarity.normal_cases)
    if not similarity.normal_cases: # Check if there are no normal cases.
        lines.append("  No eligible reviewed normal case was available."    )
    lines.append("Similar reviewed anomalous cases:")
    lines.extend(_render_case(case) for case in similarity.anomalous_cases)
    if not similarity.anomalous_cases: # Check if there are no anomalous cases.
        lines.append("  No eligible reviewed anomalous case was available.")
    lines.append(f"Historical support: {similarity.historical_support or 'insufficient'}")
    if similarity.classifier_conflict: # Check if there is a classifier conflict.
        lines.append(f"WARNING - conflicting evidence: {similarity.conflict_reason}")

    # __________________________________________
    # SYMBOLIC EVIDENCE
    # ==========================================
    # Present the rule engine's facts and traces so readers can inspect each conclusion.
    # Add the reasoning to the lines list.    
    lines.extend(
        [
            "",
            _heading("4. Symbolic facts and reasoning", color_enabled=color_enabled),
            "Asserted facts:",
        ],
    )
    lines.extend(f"  - {fact}" for fact in reasoning.asserted_facts)
    if not reasoning.asserted_facts: # Check if there are no asserted facts.    
        lines.append("  - No facts were asserted because required evidence was unavailable.")
    lines.append("Triggered rules and explanation traces:")
    # A rule trace connects the matched premises to its conclusion. The bindings
    # show which concrete segment/channel values replaced the rule's variables.
    for trace in reasoning.traces: # Iterate over the traces.
        bindings = ", ".join(f"{name}={value}" for name, value in trace.bindings) or "none" # Get the bindings.
        premises = "; ".join(str(fact) for fact in trace.matched_premises) # Get the premises.
        lines.extend(
            [
                f"  - {trace.rule_id} [{trace.source_status}]",
                f"    Premises: {premises}",
                f"    Bindings: {bindings}",
                f"    Conclusion: {trace.conclusion}",
                f"    Explanation: {trace.explanation}",
            ],
        )
    # Check if there are no traces.           
    if not reasoning.traces: # Check if there are no traces.
        lines.append("  - No rule fired for the available facts.")
    lines.append("Derived conclusions:")
    lines.extend(f"  - {fact}" for fact in reasoning.derived_facts) # Add the derived facts to the lines list.
    if not reasoning.derived_facts: # Check if there are no derived facts.
        lines.append("  - No new conclusion was derived.")
    if result.top_deviating_features: # Check if there are top deviating features.
        lines.append(
            "Largest training-normal z-score deviations: "
            + ", ".join(result.top_deviating_features),
        )
    # Add the existential query result to the lines list.
    lines.append(
        "Existential query result, exists critical deviating channel: "
        f"{reasoning.existential_critical_deviation}",
    )
    # Iterate over the suspected faults.
    for suspected_fault in reasoning.suspected_faults: # Iterate over the suspected faults.
        lines.append(
            f"Advisory hypothesis: {suspected_fault}. This is not a confirmed diagnosis.",
        )
    # Check if there are manual review reasons.
    if reasoning.manual_review_reasons: # Check if there are manual review reasons.
        lines.append("Manual review reasons: " + ", ".join(reasoning.manual_review_reasons))
    # __________________________________________
    # SIMULATED PLAN AND HUMAN REVIEW
    # ==========================================
    # Format the planner's outcome and retain the final decision boundary for the human reader.
    # Add the diagnostic recommendation to the lines list.
    lines.extend(
        [
            "",
            _heading("5. Diagnostic recommendation", color_enabled=color_enabled),
            f"Plan status: {plan.status.value}", # Get the plan status.
            f"Goal: {plan.goal_condition}", # Get the goal condition.
        ],
    )
    # A planned action is a proposed simulated check. Its cumulative cost was
    # calculated by the planner; rendering the sequence does not perform the checks.
    for step_number, planned_action in enumerate(plan.ordered_actions, start=1): # Iterate over the planned actions.
        action = planned_action.action
        lines.append(
            f"  {step_number}. {action.description} [simulated cost={action.cost:.1f}, "
            f"cumulative={planned_action.cumulative_cost:.1f}, {action.source_status}]",
        )
    # Add the total simulated cost to the lines list.   
    lines.extend(
        [
            f"Total simulated cost: {plan.total_cost:.1f}",
            f"Transition validation: {plan.transitions_valid}",
            f"Goal satisfied: {plan.goal_satisfied}",
            f"Planner note: {plan.message}",
            "",
            _heading("6. Decision boundary", color_enabled=color_enabled),
            (
                "This educational program provides simulated advisory evidence and checks. "
                "The human user retains final interpretation and action authority."
            ),
        ],
    )
    return "\n".join(lines)
# ---


# __________________________________________
# END OF FILE
# ==========================================
