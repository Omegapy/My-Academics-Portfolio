# -----------------------------------------------------------------------------
# Module Type: Streamlit page script
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
# Module Purpose:
# - Explain the implemented data and AI methods through one selected example.
# - Present current backend values beside their meanings and limits.
#
# Usage / Integration:
# - Executed by streamlit_app.py at the data-and-ai-walkthrough page route.
# - Uses the shared profile and cached assistant also used by Analyze telemetry.
#
# Contents Overview:
# - Shared stage-context and table-guide renderers.
# - Data, MLP, threshold, similarity, logic, planning, and architecture renderers.
# - Stage selection and current-profile example dispatch.
#
# Dependencies:
# - Standard Library: None
# - Third-Party: streamlit
# - Local Project: cubesat_frontend, cubesat_types
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Render a selectable walkthrough of the implemented data and AI pipeline.

Each renderer connects one course concept to the current profile and, where needed, one
held-out segment. Shared helpers place the stage's purpose and table meanings beside its
values. The functions present the existing backend result instead of implementing the
model, historical search, rule engine, or A* search again.

Only the selected stage renders during a page run. Data and architecture stages use the
fitted profile context; the other stages request one complete segment result and display
the relevant part. The profile uses the same cached assistant as Analyze telemetry.
"""

# __________________________________________
# IMPORTS
# ==========================================

import streamlit as st

# Presentation helpers connect this page to shared fitted state and backend evidence.
from cubesat_frontend import (
    OFFICIAL_RECORD_URL,  # Published source record for file provenance.
    WALKTHROUGH_STAGES,  # Ordered stage labels shared with navigation.
    FrontendState,  # Cached assistant and screening context.
    analyze_selected_segment,  # Complete backend result for one chosen ID.
    architecture_map_frame,  # Explicit module responsibility map.
    build_cache_identity,  # Source and configuration fingerprint.
    build_dataset_context,  # Validated profile and partition counts.
    build_threshold_context,  # Selected cutoff and review-band values.
    build_walkthrough_example_context,  # Selected row and fixture scenario metadata.
    confusion_matrix_frame,  # Stored evaluation as a labeled table.
    dataset_role_frame,  # Partition sizes and permitted uses.
    decision_explanation,  # Readable classification and review context.
    feature_glossary_frame,  # Meanings of the 18 source features.
    get_cached_frontend_state,  # Reuse of fitted profile resources.
    held_out_reviewed_counts,  # Reviewed class balance for evaluation.
    logic_facts_frame,  # Starting and derived fact records.
    logic_trace_frame,  # Recorded premises and conclusions.
    official_data_artifacts,  # Pinned file roles and fingerprints.
    planning_actions_frame,  # Catalog with selected-plan membership.
    planning_path_frame,  # Reconstructed chosen states and costs.
    similar_cases_frame,  # Ranked historical evidence as a table.
    source_definition,  # Metadata for the active profile.
    walkthrough_feature_frame,  # Selected raw and standardized inputs.
    walkthrough_segment_ids,  # Held-out IDs in screening order.
)
from cubesat_types import CompleteAnalysisResult, CubeSatError

# __________________________________________
# UI-ONLY HELPERS
# ==========================================


# ________________________________________________
# Shared stage and table explanations
# ------------------------------------------------
# These helpers give all stages the same reading order and explain table fields.
# Their callers supply the method-specific text and current example values.

# --- _render_stage_contract()
def _render_stage_contract(
    *,
    concept_text: str,
    purpose_text: str,
    input_text: str,
    action_text: str,
    output_text: str,
    role_text: str,
    connection_text: str,
    limit_text: str,
) -> None:
    """Place each stage's purpose, data flow, and limits in a consistent order.

    The caller supplies explanatory text for the selected method. Keeping these fields
    in one renderer helps a learner compare stages while each stage remains responsible
    for its own meaning and example values.

    Args:
        concept_text: Brief definition of the method or responsibility.
        purpose_text: Reason this program uses that method.
        input_text: Data or evidence the method receives.
        action_text: Operation the method performs on that input.
        output_text: Result passed to the user or the next program stage.
        role_text: The method's responsibility within this program.
        connection_text: How its input and output connect to neighboring stages.
        limit_text: What the displayed result cannot establish.
    """
    with st.container(border=True):
        st.write(f"{concept_text} {purpose_text}") # Define the method and its purpose.
        st.markdown(f"**Input:** {input_text}") # Name the stage's incoming evidence.
        st.markdown(f"**Action:** {action_text}") # Explain the operation on that evidence.
        st.markdown(f"**Output:** {output_text}") # Identify the result passed onward.
        st.write(f"{role_text} {connection_text}") # Connect this stage to its neighbors.
        st.write(limit_text) # State what the result cannot establish.


# ---


# --- _render_table_guide()
def _render_table_guide(
    title: str,
    fields: tuple[tuple[str, str], ...],
) -> None:
    """Explain a nearby table's field meanings before the reader inspects values.

    The guide is persistent page text. It does not depend on hover or add columns to the
    underlying evidence table.

    Args:
        title: Contextual heading identifying the table being explained.
        fields: Ordered pairs of visible field names and their meanings.
    """
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(
            "\n".join(f"- **{field}:** {meaning}" for field, meaning in fields),
        )


# ---


# ________________________________________________
# Data source and row roles
# ------------------------------------------------
# This stage connects source identity to permitted dataset uses before model inputs
# are discussed. Profile counts come from the fitted state.

# --- _render_data_stage()
def _render_data_stage(state: FrontendState) -> None:
    """Explain file identity and the active profile's permitted row roles.

    The frontend context supplies segment counts, feature count, and partition sizes.
    Official artifact records supply preparation links and expected fingerprints; the
    shell commands are displayed as text for the user to run separately.

    Args:
        state: Already fitted profile whose dataset and partitions supply the example.

    Logic:
        1. Explain why data identity and training/validation/test separation matter.
        2. Present official-file roles and optional local preparation guidance.
        3. Connect the active profile's row counts to their allowed model uses.
    """
    context = build_dataset_context(state)
    _render_stage_contract(
        # Introduce the three row roles before explaining their model uses.
        concept_text=(
            "Each row in dataset.csv describes one segment. The program gives each row a job: "
            "train the model, choose its cutoff, or test its predictions."
        ),
        # Explain why test examples must remain independent of fitting.
        purpose_text=(
            "Keeping the test rows separate lets us check the model on examples it has not "
            "learned from."
        ),
        # Identify the authentic and simulated input alternatives.
        input_text=(
            "Local OPS-SAT-AD comma-separated value (CSV) files, or the small set of simulated "
            "examples included with the app. CSV stores a table as lines of text."
        ),
        # Summarize the backend checks performed before partition use.
        action_text="Check the expected file, columns, and values, then assign the row groups.",
        # Describe the validated feature table passed to later methods.
        output_text="A checked table of 18 features per segment, with separate row groups.",
        role_text="These checks prepare the model's inputs.",
        connection_text=(
            "The MLP probability stage then puts the features on a common scale and uses them "
            "to make a prediction."
        ),
        # Separate file validity from the certainty of historical labels or physical events.
        limit_text=(
            "A matching file can still contain imperfect historical labels. Checking the file "
            "does not establish what physically happened on the spacecraft."
        ),
    )

    # __________________________________________
    # OFFICIAL ARTIFACTS AND LOCAL PREPARATION
    # ==========================================
    # The following links and file metadata explain what authentic input requires.
    # The optional terminal instructions are display content under user control.

    # Identify the pinned source and explain how local files enter the app.
    st.subheader("Official source and local files", anchor=False)
    st.write(
        "OPS-SAT-AD v2 is the historical anomaly-detection dataset used for the authentic "
        "profile. The source is Zenodo record 15108715. The app never downloads or replaces "
        "these files during startup or interaction."
    )
    
    # Expose official file links as user-controlled navigation.
    with st.container(horizontal=True, wrap=True):
        st.link_button("Open Zenodo record 15108715", OFFICIAL_RECORD_URL)
        for artifact in official_data_artifacts():
            st.link_button(f"Official {artifact.filename}", artifact.official_url)
    
    # Pair each published artifact's identity with its local destination and program use.
    artifact_rows = [
        {
            "File": artifact.filename,
            "Local destination": artifact.local_path,
            "Expected size": f"{artifact.expected_size_bytes:,} bytes",
            "Expected SHA-256": artifact.expected_sha256,
            "Program role": artifact.role,
        }
        for artifact in official_data_artifacts()
    ]
    # Explain the fingerprint and file-role columns before showing their values.
    _render_table_guide(
        "How to read the file table",
        (
            ("File", "The official filename published with the OPS-SAT-AD v2 record."),
            ("Local destination", "Where the user places that file for this program."),
            (
                "Expected size",
                "The reviewed byte count; a mismatch can indicate a wrong or incomplete file.",
            ),
            (
                "Expected SHA-256",
                "A Secure Hash Algorithm 256-bit fingerprint used to check the exact file bytes.",
            ),
            ("Program role", "Why the program reads the file and what it may use it for."),
        ),
    )
    # Display artifact metadata without reading or downloading the source files here.
    st.dataframe(
        artifact_rows,
        hide_index=True,
        width="stretch",
        key="walkthrough_artifact_table",
    )
    # Distinguish model feature rows from raw readings used by the separate verifier.
    st.caption(
        "dataset.csv has one derived feature row per segment and is the model input. "
        "segments.csv has 303,493 raw readings and is used by the standalone verifier to "
        "cross-check segment metadata."
    )
    # Keep optional local setup instructions alongside the source identity table.
    with st.expander("Optional: prepare the data files in Terminal"):
        st.write(
            "If authentic data is already loading, you can skip this setup. Otherwise, open "
            "Terminal in Portfolio-Project-Module-8 and run the commands below. Compare the "
            "SHA-256 results with the file table above. See data/README.md for the full setup."
        )
        # These shell commands are teaching text; rendering st.code does not execute them.
        st.code(
            "curl -fL "
            "https://zenodo.org/api/records/15108715/files/dataset.csv/content "
            "-o data/dataset.csv\n"
            "curl -fL "
            "https://zenodo.org/api/records/15108715/files/segments.csv/content "
            "-o data/segments.csv\n"
            "md5 data/dataset.csv data/segments.csv\n"
            "shasum -a 256 data/dataset.csv data/segments.csv",
            language="bash",
        )
        # Make the boundary between displayed commands and command execution explicit.
        st.caption("The app displays these commands; it does not run them.")
    
    # __________________________________________
    # ACTIVE PROFILE AND PARTITION USES
    # ==========================================
    # Relate the selected profile to the existing train, validation, and test groups.
    # These counts explain how the backend keeps fitting and evaluation separate.

    # Introduce the active profile's actual partition sizes.
    st.subheader("How this dataset is divided", anchor=False)
    # Use validated profile counts to distinguish segments, channels, and features.
    st.write(
        f"{context.profile_label} has {context.total_segments:,} segment rows across "
        f"{len(context.channel_codes)} channels. The app checks the {context.feature_count} "
        "numerical features already stored for each segment. It does not calculate these "
        "summaries from raw readings during page loading."
    )
    # Include the expected raw-reading count only for a profile that defines it.
    if context.raw_reading_count is not None:
        st.write(
            f"The official raw file, segments.csv, is expected to contain "
            f"{context.raw_reading_count:,} individual readings. The separate verification "
            "command checks that file and compares its segment metadata with dataset.csv."
        )
    # Explain how each row group may influence the model workflow.
    _render_table_guide(
        "How to read the row-role table",
        (
            ("Row role", "The one job assigned to that group of segment rows."),
            ("Segments", "The number of rows in that group for the active data profile."),
            ("Purpose", "What that group may influence in the machine-learning workflow."),
            (
                "Model training",
                "Rows used to learn feature averages and scales, and the network's weights.",
            ),
            (
                "Threshold validation",
                "Separate rows used after fitting to choose the probability cutoff.",
            ),
            (
                "Held-out test",
                "Rows reserved from fitting and threshold selection for final screening and tests.",
            ),
        ),
    )
    # Present the existing partition counts without assigning new row roles.
    st.dataframe(
        dataset_role_frame(context),
        hide_index=True,
        width="stretch",
        key="walkthrough_data_roles",
    )
    # Connect the training-role split to the reason held-out rows remain separate.
    st.caption(
        f"The {context.official_training_segments:,} official training-role rows are split into "
        f"{context.model_training_segments:,} model-training rows and "
        f"{context.threshold_validation_segments:,} threshold-validation rows. The "
        f"{context.held_out_segments:,} held-out rows are not used to fit weights or choose the "
        "threshold. Using test answers to make those choices would be data leakage: the model "
        "would get help from the same examples later used to judge it."
    )
    # Keep the fixture's demonstration scope visible beside its smaller population.
    if context.simulated:
        st.caption(
            "The demo fixture is a small, fixed set of simulated examples for trying the app. "
            "It is not the authentic 2,123-segment benchmark."
        )


# ---


# ________________________________________________
# MLP feature inputs and prediction
# ------------------------------------------------
# The fitted model supplies the probability; this stage explains its numerical
# inputs, layer structure, and the interpretation limits of the displayed output.

# --- _render_mlp_stage()
def _render_mlp_stage(
    state: FrontendState,
    result: CompleteAnalysisResult,
) -> None:
    """Connect one segment's feature values to its fitted MLP probability.

    A multilayer perceptron (MLP) combines numerical inputs through learned weights and
    hidden layers. The backend has already fitted that model. This renderer uses the
    existing feature transformation and classification result to illustrate prediction,
    then gives the source feature names their plain-language meanings.

    Args:
        state: Fitted profile supplying the training scaler and selected feature row.
        result: Complete analysis supplying the same segment's probability and channel.
    """
    # Relate the selected segment's fitted prediction to the shared stage explanation.
    _render_stage_contract(
        # Define an MLP in terms of its numerical inputs and anomaly estimate.
        concept_text=(
            "A multilayer perceptron (MLP) is a neural network that combines numerical inputs "
            "to make a prediction. Here, it estimates whether a segment is anomalous."
        ),
        # Explain why learning joint feature patterns is useful for this classifier.
        purpose_text=(
            "It can learn patterns involving several features together, such as a change in "
            "both the average value and the amount of variation."
        ),
        # Tie the network input to this segment's ordered standardized features.
        input_text=f"Segment {result.segment_id}'s 18 standardized numerical features.",
        # Describe prediction through the fitted topology without implying retraining.
        action_text="Pass values forward through the fitted 18-32-16-8-1 neural network.",
        # Use the selected backend classification as the stage's concrete output.
        output_text=(
            f"Anomaly probability {result.classification.anomaly_probability:.1%} for this "
            "segment."
        ),
        # Identify classification as the network's responsibility.
        role_text="The network classifies numerical examples.",
        # Connect the probability to thresholding and the scaled inputs to similarity.
        connection_text=(
            "The next stage compares its probability with a cutoff. Similarity search also "
            "uses the same list of scaled features."
        ),
        # Separate the model estimate from certainty and causal diagnosis.
        limit_text=(
            "The probability is a model estimate, not certainty, a physical diagnosis, or an "
            "explanation of cause."
        ),
    )
    # Introduce how the network's layers produce the displayed probability.
    st.subheader("Multilayer perceptron (MLP) probability", anchor=False)
    # Explain reviewed training labels, learned weights, and hidden layers together.
    st.write(
        "Supervised learning means learning from examples with known answers. Here, those "
        "answers are the dataset's reviewed normal or anomalous labels. Weights are numbers "
        "the network learns during training; they control how strongly one value affects the "
        "next layer. Hidden layers are the intermediate calculations between inputs and output."
    )
    # Distinguish training updates from this page's use of fitted feedforward prediction.
    st.write(
        "This network is fully connected: each value in one layer connects to every unit in "
        "the next. The rectified linear unit (ReLU) keeps positive hidden-layer values and "
        "sets negative ones to zero. During training, backpropagation calculates how each "
        "weight contributes to error, and the optimizer uses that information to adjust the "
        "weights. Here, feedforward prediction means passing the selected example through "
        "the trained network without changing those weights."
    )
    # Make the implemented layer widths visible in input-to-output order.
    st.markdown("**Implemented shape:** 18 inputs -> 32 -> 16 -> 8 -> 1 probability")
    # Relate the three intermediate widths to the hidden layers.
    st.caption("The three hidden layers contain 32, 16, and 8 units, respectively.")

    # __________________________________________
    # SELECTED FEATURE EXAMPLE
    # ==========================================
    # Use one segment to connect stored feature summaries with training-based scaling.
    # The guide and glossary explain how to read the resulting feature table.

    # Bind the following feature example to its profile, segment, and source channel.
    st.caption(
        f"Current example: {state.source.profile_label}, segment {result.segment_id}, channel "
        f"{result.selected_channel}. Channel is a source code, not an inferred subsystem name."
    )
    # Distinguish stored feature summaries from their standardized model inputs.
    _render_table_guide(
        "How to read the feature table",
        (
            ("Feature", "The exact OPS-SAT-AD source name for one calculated signal summary."),
            (
                "Raw value",
                "The stored feature before this app scales it. It is already a summary of "
                "readings, rather than one original sensor reading.",
            ),
            (
                "Standardized value",
                "The raw value measured in model-training standard deviations from the "
                "model-training mean.",
            ),
        ),
    )
    # Explain the training-based scale and how to interpret signed standardized values.
    st.write(
        "The program calculates each standardized value as (raw value - model-training mean) / "
        "model-training standard deviation. A value near 0 is near the training average for that "
        "feature. Positive and negative values are above and below that average. Standardization "
        "puts differently scaled inputs on a comparable basis; it is not a percentage or a class "
        "label. A standard deviation describes the spread of values around their average. "
        "For example, a standardized value of +2 means two training standard deviations above "
        "that feature's average. A value of -2 is the same distance below it."
    )
    # Show this segment's raw inputs alongside the fitted scaler's transformation.
    st.dataframe(
        walkthrough_feature_frame(state, result.segment_id),
        column_config={
            "Raw value": st.column_config.NumberColumn(
                "Raw value",
                format="%.6g",
            ),
            "Standardized value": st.column_config.NumberColumn(
                "Standardized value",
                format="%.3f",
            ),
        },
        hide_index=True,
        width="stretch",
        key="walkthrough_feature_vector",
    )
    # Keep full feature definitions available beside the numerical example.
    with st.expander("Feature glossary: what the 18 MLP inputs measure"):
        # Connect glossary source names to feature rows without implying fault detection.
        st.write(
            "Use the source name in parentheses to find the matching row in the feature table. "
            "Each explanation describes a numerical summary; a larger value alone does not "
            "identify a fault."
        )
        # Wrapping text keeps full definitions readable, including on narrow screens.
        for source_name, plain_name, meaning, group in feature_glossary_frame().itertuples(
            index=False, name=None,
        ):
            st.markdown(f"**{plain_name} ({source_name})**")
            st.write(f"{meaning} Group: {group}.")

    # __________________________________________
    # PREDICTION AND ROUNDING LIMITS
    # ==========================================
    # Finish the feature example with its existing model output and explain what the
    # displayed percentage can establish.

    # Display the probability already returned for the selected segment.
    st.metric(
        "MLP anomaly probability",
        f"{result.classification.anomaly_probability:.1%}",
        border=True,
    )
    # Explain percentage rounding so a displayed extreme is not read as certainty.
    st.caption(
        "The model returns a value from 0 to 1, displayed here as a percentage rounded to one "
        "decimal place. A displayed 100.0% can be a rounded value close to 1. It does not mean "
        "the prediction is guaranteed to be correct."
    )


# ---


# ________________________________________________
# Threshold decisions and held-out evaluation
# ------------------------------------------------
# Keep one segment's review status separate from the fitted model's population-wide
# evaluation, even though both use the same cutoff.

# --- _render_threshold_stage()
def _render_threshold_stage(
    state: FrontendState,
    result: CompleteAnalysisResult,
) -> None:
    """Present the selected review band and the model's held-out evaluation.

    ThresholdContext copies the selected classification and supplies its displayed band
    edges. Evaluation metrics and the confusion matrix come from the cached trained
    model. Reviewed class counts explain their test-population denominator.

    The three-way screening status includes an uncertain route. The confusion matrix
    compares binary predictions with reviewed classes, so those quantities have different
    roles even though both start with the same model probabilities.

    Args:
        state: Fitted profile supplying stored evaluation and reviewed test labels.
        result: Selected analysis whose probability and status illustrate the cutoff.
    """
    # Copy the selected cutoff values and calculate their displayed band edges.
    threshold = build_threshold_context(result)
    # Connect individual review status with evaluation across the held-out population.
    _render_stage_contract(
        # Introduce the separate roles of review routing and prediction evaluation.
        concept_text=(
            "This stage turns the MLP's probability into a review status, then compares all "
            "held-out predictions with their reviewed classes."
        ),
        # Explain validation-based cutoff selection and the reason for a review band.
        purpose_text=(
            "The threshold is a cutoff chosen using the validation rows. A band around it "
            "marks close calls for review. Evaluation shows how often predictions agree with "
            "the recorded labels."
        ),
        # Identify the three classification values needed to explain a close call.
        input_text="One MLP probability, the chosen cutoff, and the uncertainty margin.",
        # Distinguish assigning a status from comparing predictions with reviewed labels.
        action_text="Assign a review status and compare test predictions with reviewed labels.",
        # Use this segment's actual status to anchor the evaluation explanation.
        output_text=f"{threshold.status} plus current evaluation metrics.",
        # Describe how screening status directs human inspection.
        role_text="The status helps you decide which segments to inspect.",
        # Connect classification to logic while keeping evaluation population-wide.
        connection_text=(
            "The logic stage uses the classification and probability to form facts. The "
            "evaluation below measures the model across all test segments."
        ),
        # Bound the metrics to the current local model and profile.
        limit_text=(
            "These values describe one fitted model on the selected local profile. They are not "
            "published benchmark results or operational spacecraft performance."
        ),
    )

    # __________________________________________
    # SELECTED PROBABILITY AND REVIEW BAND
    # ==========================================
    # Place the selected values beside the band arithmetic so the review status can
    # be understood without changing the classification.

    # Introduce a worked cutoff example using the selected result.
    st.subheader("One classification calculation", anchor=False)
    # Identify the segment whose probability is compared with the shared cutoff.
    st.caption(
        f"Current example: {state.source.profile_label}, segment {result.segment_id}, channel "
        f"{result.selected_channel}."
    )
    # Place the model estimate beside the operating cutoff for direct comparison.
    threshold_primary_columns = st.columns(2)
    # Show the selected segment's probability on the same percentage scale as the cutoff.
    threshold_primary_columns[0].metric(
        "Probability",
        f"{threshold.probability:.1%}",
        border=True,
    )
    # Show the validation-selected cutoff shared by this fitted model.
    threshold_primary_columns[1].metric(
        "Threshold",
        f"{threshold.threshold:.1%}",
        border=True,
    )
    # Pair the band width with the status it helps explain.
    threshold_secondary_columns = st.columns(2)
    # Show the margin applied on each side of the cutoff.
    threshold_secondary_columns[0].metric(
        "Uncertainty margin (plus or minus)",
        f"{threshold.uncertainty_margin:.1%}",
        border=True,
    )
    # Use the backend decision's readable screening status.
    threshold_secondary_columns[1].metric(
        "AI screening status",
        threshold.status,
        border=True,
    )
    # Substitute the current values into both band-edge calculations.
    st.code(
        f"lower edge = {threshold.threshold:.3f} - {threshold.uncertainty_margin:.3f} "
        f"= {threshold.lower_bound:.3f}\n"
        f"upper edge = {threshold.threshold:.3f} + {threshold.uncertainty_margin:.3f} "
        f"= {threshold.upper_bound:.3f}\n"
        f"segment probability = {threshold.probability:.3f} -> {threshold.status}",
        language="text",
    )
    # Explain the selected result's classification and review context in plain language.
    st.write(decision_explanation(result))
    # Clarify inclusive band edges and percentage points rather than statistical confidence.
    st.write(
        f"The margin is {threshold.uncertainty_margin * 100:g} percentage points on each side "
        f"of the {threshold.threshold:.1%} threshold. Probabilities from "
        f"{threshold.lower_bound:.1%} through {threshold.upper_bound:.1%}, including both "
        "edges, receive Uncertain review. This band is a review rule chosen for the app; "
        "it is not a statistical confidence interval."
    )

    # __________________________________________
    # STORED EVALUATION AND CLASS COUNTS
    # ==========================================
    # The following measures describe all held-out predictions for the fitted model.
    # Their guides and matrix explain the class counts behind those measures.

    # Reuse the evaluation produced during fitting; selecting another example does not rescore it.
    evaluation = state.assistant.trained_model.evaluation
    st.subheader("Current held-out evaluation", anchor=False)
    st.write(
        "These metrics use two predictions: anomalous at or above the threshold, and normal "
        "below it. A segment marked Uncertain review still receives one of those predictions "
        "here. That is why the confusion matrix can differ from the three screening-status "
        "counts on Analyze telemetry. Choosing another example does not change this evaluation; "
        "it covers the full test set for the current model."
    )
    
    # Keep complementary evaluation measures together for the same held-out population.
    evaluation_columns = st.columns(4)
    # Report how many predicted anomalies match reviewed anomalies.
    evaluation_columns[0].metric("Precision", f"{evaluation.precision:.1%}", border=True)
    # Report how many reviewed anomalies the model detected.
    evaluation_columns[1].metric("Recall", f"{evaluation.recall:.1%}", border=True)
    # Show the stored harmonic balance of precision and recall.
    evaluation_columns[2].metric("F1 score", f"{evaluation.f1_score:.1%}", border=True)
    # Report correct predictions across both reviewed classes.
    evaluation_columns[3].metric("Accuracy", f"{evaluation.accuracy:.1%}", border=True)
    # Count reviewed test labels to explain the evaluation population's class balance.
    reviewed_normal, reviewed_anomalous = held_out_reviewed_counts(state)
    # State the population size behind the metrics rather than the selected example alone.
    st.write(
        f"The evaluation denominator is {evaluation.test_sample_count:,} held-out segments: "
        f"{reviewed_normal:,} reviewed normal and {reviewed_anomalous:,} reviewed anomalous. "
        "The reviewed classes are revealed for evaluation only after prediction."
    )

    # Explain each measure's denominator and interpretation before the confusion matrix.
    _render_table_guide(
        "What the evaluation metrics answer",
        (
            (
                "Precision",
                "Of all predicted anomalies, what fraction were reviewed anomalies? Higher "
                "precision means fewer false anomaly flags.",
            ),
            (
                "Recall",
                "Of all reviewed anomalies, what fraction did the model detect? Higher recall "
                "means fewer missed anomalies.",
            ),
            (
                "F1 score",
                "The harmonic mean of precision and recall, calculated as "
                "2 × precision × recall / (precision + recall). It drops when either measure "
                "is low, so a high value needs both to be strong.",
            ),
            (
                "Accuracy",
                "The fraction of all held-out predictions that were correct. If most examples "
                "are normal, many correct normal predictions can hide missed anomalies. "
                "Read accuracy together with recall.",
            ),
        ),
    )

    # Map reviewed and predicted classes to matrix rows and columns.
    _render_table_guide(
        "How to read the confusion matrix",
        (
            ("Rows", "The reviewed normal or anomalous class for each held-out segment."),
            ("Columns", "The normal or anomalous class predicted by the MLP and threshold."),
            ("Reviewed normal / predicted normal", "Correctly classified normal segments."),
            ("Reviewed normal / predicted anomalous", "False anomaly flags."),
            ("Reviewed anomalous / predicted normal", "Missed anomalies."),
            ("Reviewed anomalous / predicted anomalous", "Correctly detected anomalies."),
        ),
    )

    # Present the confusion matrix already calculated during model evaluation.
    st.dataframe(
        confusion_matrix_frame(evaluation),
        width="stretch",
        key="walkthrough_confusion_matrix",
    )
    
    # Name the four stored outcomes for a concrete account of detections and errors.
    true_normal, false_alarm = evaluation.confusion_matrix[0]
    missed_anomaly, detected_anomaly = evaluation.confusion_matrix[1]
    predicted_anomalies = false_alarm + detected_anomaly
    st.write(
        f"In this run, the model detected {detected_anomaly:,} of {reviewed_anomalous:,} "
        f"reviewed anomalies and missed {missed_anomaly:,}. It correctly classified "
        f"{true_normal:,} normal segments and raised {false_alarm:,} false anomaly flags."
    )

    # Use the current anomaly-prediction count to illustrate precision when it is nonzero.
    if predicted_anomalies:
        st.write(
            f"For example, precision is {detected_anomaly:,} correct anomaly predictions / "
            f"{predicted_anomalies:,} total anomaly predictions = {evaluation.precision:.1%}."
        )
    else:
        st.write("The model predicted no anomalies, so this run reports precision as 0%.")

    # Distinguish model-performance evidence from tests of program correctness.
    st.caption(
        "Rows are reviewed classes and columns are model predictions. Diagonal cells are "
        "correct; off-diagonal cells are errors. The software test suite separately checks "
        "program behavior and does not improve these model-performance scores."
    )
    if state.source.simulated:
        st.caption("Fixture metrics demonstrate the workflow only, not benchmark performance.")


# ---


# ________________________________________________
# Class-aware historical comparison
# ------------------------------------------------
# This stage presents the neighbors already returned for the selected segment.
# Separate reviewed classes keep both kinds of historical evidence visible.

# --- _render_similarity_stage()
def _render_similarity_stage(
    state: FrontendState,
    result: CompleteAnalysisResult,
) -> None:
    """Explain the selected segment's separate normal and anomalous neighbors.

    The result already contains historical cases selected in standardized feature space.
    The two tables preserve each class's ranks, reviewed labels, and distances, while the
    nearby text explains how to read the largest coordinate gaps. The selected segment's
    prediction remains the classification supplied in the complete result.

    Args:
        state: Current profile used to label the example's source.
        result: Selected backend evidence with class-separated nearest cases.
    """

    # Frame nearest neighbors as historical evidence for the selected segment.
    _render_stage_contract(
        concept_text=(
            "Similarity search is a historical comparison tool. It finds the recorded segments "
            "whose 18 feature values most closely resemble the selected example. These are "
            "called nearest neighbors."
        ),
        # Explain why a reviewer needs class-aware examples alongside model probability.
        purpose_text=(
            "A reviewer can compare the selected segment with known normal and anomalous examples "
            "instead of relying on the MLP probability alone."
        ),
        # Identify the selected feature vector used for historical distance comparisons.
        input_text=(
            f"Segment {result.segment_id}'s feature vector: its ordered list of 18 scaled values."
        ),
        # Describe separate searches within reviewed normal and anomalous references.
        action_text=(
            "Measure Euclidean distance to historical examples, searching the reviewed normal "
            "and anomalous groups separately."
        ),
        # Name the two evidence groups returned by the historical search.
        output_text="Separate nearest normal and anomalous historical cases.",
        # Keep the comparison's role distinct from the classifier's prediction.
        role_text="These comparisons add context to the MLP prediction.",
        # Connect shared scaling to similarity evidence and later logic facts.
        connection_text=(
            "The search reuses the standardized feature vector from the MLP stage. Its historical "
            "evidence can become explicit facts for the logic stage."
        ),
        # State the limits of transferring labels or causal explanations between neighbors.
        limit_text=(
            "Numerical similarity does not transfer a neighbor's label to the selected segment "
            "and does not prove that two segments have the same physical cause."
        ),
    )

    # __________________________________________
    # REFERENCE ELIGIBILITY AND DISTANCE MEANING
    # ==========================================
    # Explain the historical population and numerical scale before the case tables.
    # The comparison uses feature-space proximity as evidence for a reviewer.

    # Explain which row roles may supply references and why channels can differ.
    st.caption(
        f"Current example: {state.source.profile_label}, segment {result.segment_id}, channel "
        f"{result.selected_channel}. Historical references include both the model-training "
        "and threshold-validation rows. Held-out test rows are excluded. The search groups "
        "references by reviewed class, not by channel, so a neighbor may be from another channel."
    )
    
    # Define smaller distance as greater numerical resemblance without label transfer.
    st.write(
        "Euclidean distance combines the differences across all 18 scaled features into one "
        "number. A smaller value means the two examples are more alike. A neighbor's reviewed "
        "label supplies context; "
        "it never becomes the selected segment's prediction."
    )

    # Explain within-class ranks, distances, and coordinate gaps before showing cases.
    _render_table_guide(
        "How to read each similarity table",
        (
            ("Rank", "Position within that reviewed class; rank 1 has the smallest distance."),
            ("Reviewed case", "The segment identifier of the historical comparison record."),
            ("Reviewed label", "The historical normal or anomalous class assigned by reviewers."),
            (
                "Euclidean distance",
                "The square root of the summed squared gaps across all 18 standardized features; "
                "smaller means closer in this feature space.",
            ),
            (
                "Largest standardized feature gaps",
                "The inputs on which the selected segment and neighbor differ most, measured in "
                "training-standard-deviation units. These gaps explain how the two examples "
                "differ; they are not scores of feature importance in the MLP.",
            ),
        ),
    )
    
    # Explain why each reviewed class gets its own nearest-case list.
    st.caption(
        "The normal and anomalous lists are separate so a larger class cannot hide the nearest "
        "examples from the other class. Distance is a comparison value, not a probability."
    )

    # __________________________________________
    # NORMAL AND ANOMALOUS CASE EVIDENCE
    # ==========================================
    # Each class keeps its own ranked cases and empty-result handling.
    # The table and wrapped text present the same stored comparisons.

    # Render each reviewed class with its own cases, heading, and stable table key.
    for heading, cases, key in (
        (
            "Nearest reviewed normal cases",
            result.similarity.normal_cases,
            "walkthrough_normal_cases",
        ),
        (
            "Nearest reviewed anomalous cases",
            result.similarity.anomalous_cases,
            "walkthrough_anomalous_cases",
        ),
    ):
        # Identify the reviewed class before its case evidence.
        st.subheader(heading, anchor=False)
        # Format the backend's selected neighbors without changing their ranks or distances.
        case_frame = similar_cases_frame(cases)
        # Represent a class with no eligible reference explicitly.
        if case_frame.empty:
            st.caption("No eligible case is available for this class.")
        else:
            # Round displayed distances while keeping the case evidence table unchanged.
            st.dataframe(
                case_frame,
                column_config={
                    "Euclidean distance": st.column_config.NumberColumn(
                        "Euclidean distance",
                        format="%.3f",
                    ),
                },
                hide_index=True,
                width="stretch",
                key=key,
            )
            # Give each neighbor's largest feature gaps enough room to remain readable.
            st.markdown(
                "\n".join(
                    (
                        f"- Rank {case.rank} is segment {case.case_id}, reviewed as "
                        f"{case.reviewed_label}, at distance {case.distance:.3f}. "
                        "Its largest feature gaps are "
                        + ", ".join(
                            f"{gap.feature_name} "
                            f"({gap.absolute_standardized_difference:.3f})"
                            for gap in case.feature_differences
                        )
                        + "."
                    )
                    for case in cases
                )
            )
    
    # Keep the fitted backend as the source of distance evidence and preserve causal limits.
    st.caption(
        "Distances and largest feature gaps come from the current fitted backend. They are "
        "comparison evidence, not proof of the same cause."
    )


# ---


# ________________________________________________
# Facts, rule traces, and review reasons
# ------------------------------------------------
# This stage explains how explicit statements support recorded conclusions.
# It renders the selected reasoning result without running the rules again.

# --- _render_logic_stage()
def _render_logic_stage(
    state: FrontendState,
    result: CompleteAnalysisResult,
) -> None:
    """Make the existing expert-system reasoning readable for one example.

    Facts are Boolean statements. Rule applications and consistency checks retain the
    facts and variable bindings supporting their conclusions. The adapter formats that
    evidence; this renderer presents it beside the meanings of those concepts. An empty
    trace means no new derivation was recorded for the current facts.

    Args:
        state: Current profile used to identify the example's data source.
        result: Selected backend analysis containing asserted facts, derived facts,
            rule traces, review reasons, and any simulated fault hypotheses.
    """
    # Connect the expert-system method to this segment's already calculated evidence.
    _render_stage_contract(
        concept_text=(
            "An expert system applies written rules to facts. Here, the rules connect a "
            "segment's classification and historical comparisons to checks a person can review."
        ),
        # Explain how recorded premises and conclusions make reasoning inspectable.
        purpose_text=(
            "Each rule that fires records its supporting facts and conclusion, so you can "
            "follow how the program reached that result."
        ),
        # Distinguish calculated evidence, reviewed labels, and configured assumptions.
        input_text="Calculated results, reviewed historical labels, and configured assumptions.",
        action_text="Match the conditions in each if/then rule to the available facts.",
        output_text="Rule-derived conclusions, review reasons, and simulated hypotheses.",
        role_text="The rules explain which conditions call for further review.",
        connection_text=(
            "The rule engine receives the classification and historical comparisons. Any "
            "required checks then pass to A-star planning."
        ),
        limit_text=(
            "The engine can use only facts and rules encoded by this program. It does not learn "
            "the MLP probability or confirm a physical fault."
        ),
    )

    # Keep the source profile and selected segment attached to the reasoning example.
    st.caption(
        f"Current example: {state.source.profile_label}, segment {result.segment_id}, channel "
        f"{result.selected_channel}."
    )

    # Distinguish numerical probability from facts and avoid treating absence as negation.
    st.write(
        "A probability is a number. A fact is a statement the program currently treats as true, "
        "such as Uncertain(segment_id). This is Boolean logic: a rule condition either matches a "
        "known fact or does not. A missing fact does not establish that its opposite is true."
    )
    
    # __________________________________________
    # FACT ORIGINS AND THRESHOLDS
    # ==========================================
    # Explain the difference between model evidence and configured assumptions, then
    # show the starting and derived facts retained for this segment.

    # Introduce the starting and derived statements used by the rule engine.
    st.subheader("Facts available to the expert system", anchor=False)
    
    # Identify simulated channel assumptions even when telemetry is authentic.
    st.write(
        "Starting facts combine calculated results, reviewed labels, and teaching assumptions. "
        "Critical and FaultMapping come from configured assumptions, including when you select "
        "authentic data. They do not identify a verified critical channel or spacecraft fault."
    )
    # Explain how fact thresholds and normal-reference deviations differ from MLP screening.
    st.write(
        f"The rule engine checks uncertainty first. For other segments, it uses a separate "
        f"{state.assistant.config.anomaly_fact_threshold:.0%} cutoff to add Anomalous. "
        "A Flagged anomaly screening status below that cutoff can therefore appear as "
        "InsufficientEvidence here. Deviates means at least one feature is "
        f"{state.assistant.config.deviation_zscore_threshold:g} or more standard deviations "
        "from the reviewed normal model-training average. This normal-only comparison differs "
        "from the MLP scaler, which uses both training classes."
    )
    
    # Help the learner distinguish supplied facts from conclusions added during reasoning.
    _render_table_guide(
        "How to read the fact table",
        (
            (
                "Fact role",
                "Starting fact means it was supplied to the rules. Derived by a rule means "
                "the program added it after matching rule conditions.",
            ),
            (
                "Fact",
                "A named statement, or predicate, such as Uncertain(segment). The text in "
                "parentheses identifies the segment or other item the statement describes.",
            ),
        ),
    )
    # Display existing facts and their origins without deriving new conclusions here.
    st.dataframe(
        logic_facts_frame(result),
        hide_index=True,
        width="stretch",
        key="walkthrough_logic_facts",
    )
    
    # __________________________________________
    # RULE MATCHES AND RECORDED BINDINGS
    # ==========================================
    # Connect the rule vocabulary to the existing trace table and individual records.
    # An empty trace has its own explanation before any result warnings.

    # Introduce the recorded matches that connect facts to conclusions.
    st.subheader("Rules that fired", anchor=False)
    # Explain rule premises and the segment variable through one illustrative Horn clause.
    st.write(
        "A Horn clause is an if/then rule with one conclusion. Its premises are the conditions "
        "that must all match before it fires. For example, "
        "Uncertain(?s) -> ManualReviewRequired(?s) means: if segment ?s is uncertain, require "
        "manual review of that segment. The ?s is a placeholder for a segment ID; the arrow "
        "means 'then'. This example explains the rule, whether or not it fires for your selection."
    )
    
    # Connect consistent variable bindings to repeated forward-chaining derivations.
    st.write(
        "Unification matches that placeholder to an actual ID and keeps the match consistent "
        "through the rule. The recorded match is a variable binding. Forward chaining repeats "
        "this process, using newly added facts to check more rules until no new facts are added. "
        "A trace is the record of one rule application. Any resulting fault name remains a "
        "simulated hypothesis to investigate."
    )

    # Explain each trace field, including source status, before presenting recorded matches.
    _render_table_guide(
        "How to read a fired-rule trace",
        (
            ("Rule", "The stable identifier of the Horn clause that matched."),
            ("Matched facts", "Known facts that satisfied every premise of that rule."),
            (
                "Variable bindings",
                "The constants substituted for placeholders such as ?s for segment.",
            ),
            ("Conclusion", "The new fact added after all premises matched."),
            ("Why it fired", "A plain-language explanation of the rule's intended reasoning."),
            (
                "Source status",
                "Whether the rule pattern is source-derived or a simulated educational rule; it "
                "is not a confidence score.",
            ),
        ),
    )
    
    # Format rule and consistency-check traces from the selected reasoning result.
    trace_frame = logic_trace_frame(result)
    
    if trace_frame.empty:
        # Explain an empty trace as the absence of recorded matches for this example.
        st.caption(
            "No Horn rule fired for this selected segment because its current facts did not "
            "satisfy every premise of any rule. This is a valid no-match result, not an engine "
            "failure."
        )
        # The alternate branch below presents recorded traces when the table is nonempty.
    else:
        st.dataframe(
            trace_frame,
            hide_index=True,
            width="stretch",
            key="walkthrough_logic_traces",
        )
        
        for trace in result.reasoning.traces:
            # Keep each trace's premises, bindings, and conclusion together in a readable block.
            with st.container(border=True):
                # Identify the rule whose recorded evidence follows.
                st.markdown(f"**Rule:** {trace.rule_id}")
                # List the actual premises retained with this application.
                st.markdown(
                    "**Matched facts:** "
                    + "; ".join(str(fact) for fact in trace.matched_premises)
                )
                # Format recorded substitutions, including the case where no variables were needed.
                bindings = ", ".join(
                    f"{name} = {value}" for name, value in trace.bindings
                ) or "No variables"
                # Show the substitutions connecting this rule to concrete items.
                st.markdown(f"**Variable bindings:** {bindings}")
                # Show the conclusion supported by this trace before its explanation.
                st.markdown(f"**Conclusion:** {trace.conclusion}")
                st.caption(f"Why it fired: {trace.explanation}")
    
    # __________________________________________
    # HYPOTHESES AND HUMAN REVIEW CONTEXT
    # ==========================================
    # Expose any selected-result hypotheses and review reasons after their evidence.
    # These advisory conclusions retain their simulation and probability boundaries.

    # Present only fault hypotheses actually returned, with simulated status explicit.
    if result.reasoning.suspected_faults:
        st.warning(
            "Simulated hypotheses: " + ", ".join(result.reasoning.suspected_faults)
        )

    # Surface the selected reasoning result's reasons for human review.
    if result.reasoning.manual_review_reasons:
        st.warning(
            "Review context: " + " ".join(result.reasoning.manual_review_reasons)
        )
        
    # Keep symbolic conclusions separate from the unchanged MLP probability.
    st.caption(
        "The probability remains the MLP output; rules operate on explicit facts after that "
        "calculation."
    )


# ---


# ________________________________________________
# Simulated action catalog and chosen path
# ------------------------------------------------
# This stage explains the original plan through allowed actions, selected state
# transitions, and outcome measures. It does not perform diagnostic actions.

# --- _render_planning_stage()
def _render_planning_stage(
    state: FrontendState,
    result: CompleteAnalysisResult,
) -> None:
    """Explain the simulated actions and path already selected by A*.

    The action table describes the permitted catalog. The path table reconstructs only
    the selected sequence, using stored cumulative costs and the backend's estimate of
    remaining cost. Displayed expanded-node and goal values come from the original plan.

    A row describes a planning-state transition. Displaying that row does not execute a
    hardware check or establish that a real diagnostic step occurred.

    Args:
        state: Current profile used to label the selected example.
        result: Complete analysis containing the backend's simulated advisory plan.
    """

    # Use the simulated advisory plan already produced for this segment.
    plan = result.plan

    # Relate graph-search concepts to the stored plan's goal and outcome.
    _render_stage_contract(
        # Define nodes and edges through simulated check states and allowed actions.
        concept_text=(
            "A-star (A*) is a graph-search algorithm that chooses a sequence of steps. Each "
            "node records which checks are complete and which remain. Each connection, or "
            "edge, represents an allowed simulated review action."
        ),
        # Explain why incurred cost and remaining effort are considered together.
        purpose_text=(
            "It compares the cost so far with an estimate of the work left to find a "
            "low-cost sequence that completes the required checks."
        ),
        # Identify the state, goal, and action catalog required by the search.
        input_text="A planning state, required checks, allowed actions, costs, and a goal.",
        # Name the search priority equation used by the backend planner.
        action_text="Use A-star to compare candidate states with f(n) = g(n) + h(n).",
        # Use the stored outcome message, including plans with no action sequence.
        output_text=plan.message,
        # Keep review ordering distinct from anomaly classification.
        role_text="A-star orders the review checks; it does not detect anomalies.",
        # Connect checks required by earlier methods to the human-facing advisory sequence.
        connection_text=(
            "It receives required checks derived from the classification and logic stages, then "
            "returns an advisory sequence for a human reviewer."
        ),
        # Keep simulated costs and proposed actions separate from physical execution.
        limit_text=(
            "The costs are coursework values and the actions are simulated. The plan does not "
            "execute a command, inspect hardware, or prove that a check occurred."
        ),
    )

    # Identify the plan's segment and retain the simulation boundary for all following values.
    st.caption(
        f"Current example: {state.source.profile_label}, segment {result.segment_id}, channel "
        f"{result.selected_channel}. Every action and cost below is simulated."
    )

    # Define the cost symbols in relative coursework units before displaying them.
    st.write(
        "In f(n) = g(n) + h(n), n is one planning state. g(n) is the cost of the simulated "
        "steps taken so far. h(n), called the heuristic, estimates the least cost still needed. "
        "A-star considers smaller totals, f(n), first. The costs represent relative review "
        "effort chosen for this coursework example; they are not minutes or money."
    )
    
    # Show the route that initializes this segment's planning state.
    st.markdown(f"**Starting route:** {plan.initial_state.route}")
    # Identify the backend goal against which the simulated outcome is judged.
    st.markdown(f"**Goal:** {plan.goal_condition}")
    
    # __________________________________________
    # ALLOWED ACTIONS AND SELECTED MEMBERSHIP
    # ==========================================
    # Describe the action catalog with its preconditions, effects, and effort costs.
    # Membership markers connect the available actions to this segment's plan.

    # Introduce the available catalog before narrowing attention to the chosen sequence.
    st.subheader("Allowed simulated actions", anchor=False)
    # Explain eligibility, effects, and selected membership for each simulated action.
    _render_table_guide(
        "How to read the action table",
        (
            ("Action", "The stable identifier for one allowed simulated review step."),
            ("Description", "What evidence the simulated step would review."),
            ("Preconditions", "Facts that must already be true before the action is allowed."),
            ("Effects", "Checks marked complete after the simulated action is applied."),
            ("Cost", "A nonnegative coursework value used to compare possible sequences."),
            ("Selected", "Whether the final A-star path includes that action."),
        ),
    )
    # Display the catalog with membership markers from this segment's stored plan.
    st.dataframe(
        planning_actions_frame(result),
        # Format relative effort consistently without assigning physical units.
        column_config={
            "Cost": st.column_config.NumberColumn("Cost", format="%.1f"),
        },
        hide_index=True,
        width="stretch",
        key="walkthrough_planning_actions",
    )

    # __________________________________________
    # SELECTED STATE AND COST PROGRESSION
    # ==========================================
    # Read the stored sequence as state transitions beginning at step zero.
    # The adapter reconstructs that sequence and estimates its remaining effort.

    # Introduce the selected path's state transitions and cost progression.
    st.subheader("Chosen path and simulated costs", anchor=False)
    # Distinguish path rows from alternative states counted during search expansion.
    st.write(
        "This table follows only the chosen sequence, starting at step 0. A-star may examine "
        "other states while searching; those alternatives are included in the expanded-node "
        "count but are not listed here."
    )
    # Define state and cost columns, including the initial state at step zero.
    _render_table_guide(
        "How to read the selected path",
        (
            ("Step", "The position in the chosen sequence; step 0 is the starting state."),
            ("Selected action", "The action that produced the state shown on that row."),
            (
                "Candidate state",
                "Which mandatory checks are complete and which still remain after the action.",
            ),
            ("g(n) accumulated", "The simulated action cost already spent to reach this state."),
            (
                "h(n) remaining estimate",
                "A conservative estimate of the least cost still needed to finish required checks.",
            ),
            (
                "f(n) total estimate",
                "The priority value g(n) + h(n); A-star considers lower values first.",
            ),
        ),
    )
    # Reconstruct only the stored action sequence through the adapter's path view.
    path_frame = planning_path_frame(result)
    # Display the reconstructed states in their selected order.
    st.dataframe(
        path_frame,
        # Use matching decimal precision so the three cost components are easy to compare.
        column_config={
            "g(n) accumulated": st.column_config.NumberColumn(
                "g(n) accumulated",
                format="%.1f",
            ),
            "h(n) remaining estimate": st.column_config.NumberColumn(
                "h(n) remaining estimate",
                format="%.1f",
            ),
            "f(n) total estimate": st.column_config.NumberColumn(
                "f(n) total estimate",
                format="%.1f",
            ),
        },
        hide_index=True,
        width="stretch",
        key="walkthrough_planning_path",
    )
    # Use the always-present start row to illustrate the initial cost estimate.
    first_state = path_frame.iloc[0]
    # Explain the initial g, h, and f values using the current reconstructed path.
    st.write(
        f"At step 0, no action has been taken, so g(n) = {first_state['g(n) accumulated']:.1f}. "
        f"The estimated work left is h(n) = {first_state['h(n) remaining estimate']:.1f}, "
        f"giving f(n) = {first_state['f(n) total estimate']:.1f}. As checks are marked complete "
        "in the simulation, g(n) increases and the remaining estimate falls toward zero."
    )

    # Provide a readable narrative for the same ordered states and costs as the table.
    st.markdown(
        "\n".join(
            (
                f"- Step {step}: {action}. State: {candidate}. Cost so far "
                f"g(n) = {g_value:.1f}, "
                f"h(n) = {h_value:.1f}, f(n) = {f_value:.1f}."
            )
            # Step counts positions in the chosen sequence, beginning with the initial state.
            # Action names identify the selected transition, or the initial-state label.
            # Candidate summarizes completed and remaining simulated checks at that position.
            # g_value is the accumulated cost of the selected actions so far.
            # h_value is the backend heuristic's remaining-cost estimate for that state.
            # f_value combines accumulated cost and remaining estimate for comparison.
            for step, action, candidate, g_value, h_value, f_value in path_frame.itertuples(
                index=False,
                name=None,
            )
        )
    )

    # __________________________________________
    # PLAN OUTCOME AND EXECUTION LIMITS
    # ==========================================
    # Use the original search result to report cost, expansion effort, and goal status.
    # These measures describe a simulated plan for human review.

    # Group the original plan's outcome measures after its path explanation.
    planning_columns = st.columns(3)
    # Show the backend's final cumulative simulated effort.
    planning_columns[0].metric("Total simulated cost", f"{plan.total_cost:.1f}", border=True)
    # Report the original search's expansion count, including states outside the chosen path.
    planning_columns[1].metric("Expanded nodes", plan.expanded_node_count, border=True)
    # Display the backend's stored goal-satisfaction result.
    planning_columns[2].metric(
        "Goal satisfied",
        "Yes" if plan.goal_satisfied else "No",
        border=True,
    )
    
    # Connect total cost, search effort, and completion to their distinct meanings.
    st.caption(
        "Total simulated cost is the final g(n). Expanded nodes counts the planning states A-star "
        "examined while finding the path. Goal satisfied means every mandatory simulated check is "
        "complete in the final state."
    )

    # Close the planning example with the boundary between advice and physical work.
    st.caption(
        "The sequence is advisory coursework output. It does not execute a command, diagnose "
        "hardware, or show that a physical check occurred."
    )


# ---


# ________________________________________________
# Source ownership and course lineage
# ------------------------------------------------
# This final stage maps program responsibilities to modules and course milestones.
# The mapping is shared explanatory metadata for either data profile.

# --- _render_architecture_stage()
def _render_architecture_stage(state: FrontendState) -> None:
    """Connect workflow responsibilities to current source files and course work.

    The adapter supplies an explicit map of inputs, outputs, modules, and ownership.
    The profile caption keeps the user's current context visible, but the map itself is
    explanatory metadata rather than a runtime call trace for the selected segment.

    Args:
        state: Current fitted profile used for the source-context caption.
    """
    # Explain how the source map connects course concepts to current responsibilities.
    _render_stage_contract(
        # Introduce source ownership and course lineage as the map's two purposes.
        concept_text=(
            "This map shows which source file handles each part of the app and which course "
            "module introduced the method."
        ),
        # Explain how a learner can trace a visible result back to its producer.
        purpose_text=(
            "It lets a learner trace a screen value back to the code that supplies it and see how "
            "earlier course modules contribute to the integrated Module 8 program."
        ),
        # Use program stages and displayed results as the map's organizing inputs.
        input_text="The program stages and the results displayed on these pages.",
        action_text="Connect each stage to its source file and course milestone.",
        output_text="A guide to where each result comes from.",
        role_text="The backend is the Python code that calculates results.",
        # Distinguish page interaction from the adapter's conversion of backend records.
        connection_text=(
            "The frontend is the interface you use to choose examples and read those results. "
            "The presentation adapter converts the calculated results into tables and charts."
        ),
        # Clarify that responsibility metadata does not record execution for this selection.
        limit_text=(
            "This is a guide to responsibilities, not a runtime call trace: it does not record "
            "which functions ran when you selected an example."
        ),
    )
    # Keep the active profile visible even though the architecture map is shared.
    st.caption(f"Current profile context: {state.source.profile_label}.")

    # __________________________________________
    # MODULE RESPONSIBILITY GUIDE
    # ==========================================
    # Connect each stage's inputs and outputs to the source that owns the behavior.
    # The table and narrative provide complementary routes through the same map.

    # Obtain the adapter's explicit ownership map rather than collecting a runtime trace.
    architecture = architecture_map_frame()
    # Explain how inputs, outputs, source modules, and course lineage relate in each row.
    _render_table_guide(
        "How to read the architecture map",
        (
            (
                "Stage",
                "One problem, data, AI-method, coordination, or presentation responsibility.",
            ),
            ("Input", "The information that responsibility receives."),
            ("Output", "The record or decision support that responsibility produces."),
            ("Current source", "The current document or Python module that supplies the behavior."),
            (
                "Layer",
                "Backend calculates results, frontend presents them, and design evidence records "
                "the problem and intended human decision.",
            ),
            (
                "Course lineage",
                "The earlier course module or Module 8 integration work demonstrated by the stage.",
            ),
        ),
    )
    # Present the current source-responsibility table with its declared column meanings.
    st.dataframe(
        architecture,
        hide_index=True,
        width="stretch",
        key="walkthrough_architecture_map",
    )

    # Connect the compact map to a readable account of each module's contribution.
    st.markdown(
        "- **Problem and human decision.** The Module 2 milestone and README.md describe the "
        "CubeSat use case and the decision a person needs to make.\n"
        "- **Data validation and roles.** `cubesat_data.py` checks the files and separates "
        "training, validation, and test rows. This builds on Modules 2 and 5.\n"
        "- **MLP fitting and classification.** `cubesat_model.py` learns from the 18 features "
        "and reviewed labels, then supplies probabilities, a threshold, and evaluation "
        "metrics. The neural-network methods connect to Modules 3 and 5.\n"
        "- **Historical similarity.** `cubesat_similarity.py` finds nearby normal and anomalous "
        "examples using the selected feature values. This applies search concepts from Module 4.\n"
        "- **Logic and expert system.** `cubesat_logic.py` turns results and teaching assumptions "
        "into facts, then applies rules and records their conclusions. This uses Module 6 "
        "knowledge-representation concepts.\n"
        "- **A-star planning.** `cubesat_planner.py` uses states, allowed actions, and costs to "
        "choose simulated review steps. A-star also connects to Module 4.\n"
        "- **Analysis coordination.** `cubesat_telemetry_ai.py` calls these methods for one "
        "segment and collects their outputs in `CompleteAnalysisResult`. This is part of the "
        "Module 8 integration.\n"
        "- **Presentation adapter.** `cubesat_frontend.py` turns those results into tables, "
        "charts, and walkthrough examples for the Module 8 interface.\n"
        "- **Interactive pages.** `streamlit_app.py` and `app_pages/` display the results and "
        "handle your selections. They form the frontend added for Module 8."
    )
    # Separate historical course lineage from the current code that determines behavior.
    st.caption(
        "The milestone PDFs establish course lineage. The current Python modules determine the "
        "behavior shown in this app. Analyze telemetry is the screening workflow; this page is "
        "the learner walkthrough."
    )


# ---

# __________________________________________
# DIRECT PAGE FLOW
# ==========================================

# ________________________________________________
# Overview and stage selection
# ------------------------------------------------
# Introduce the ordered pipeline before choosing the one explanation to render.
# The remaining page flow supplies that stage with the active profile and example.

st.title("Data and AI walkthrough", anchor=False)
st.write(
    "Follow one recorded telemetry segment through the artificial intelligence (AI) methods "
    "used by Analyze telemetry. Telemetry means measurements recorded by a spacecraft. "
    "A segment groups readings from one channel over a time window. The app represents it "
    "with 18 numerical features, such as its average value and the spread of its readings. "
    "An anomaly is an unusual pattern in those measurements."
)
st.write(
    "The examples come from held-out test data: segments kept out of model training and "
    "threshold selection. The threshold is the probability cutoff used to classify a segment. "
    "Start with Data source and roles, then follow the stages in order or open the method "
    "you want to understand. Each stage explains its result using the selected example."
)

# Keep the pipeline order visible before the learner chooses a stage.
with st.container(border=True):
    # Label the overview so it remains distinct from the selected stage's explanation.
    st.markdown("**Pipeline overview**")
    # Describe the method sequence and its final source map in navigation order.
    st.markdown(
        "1. Check the data and separate training, validation, and test rows.\n"
        "2. Scale the 18 features and estimate anomaly probability with a neural network "
        "called a multilayer perceptron (MLP).\n"
        "3. Apply the cutoff and compare predictions with reviewed labels.\n"
        "4. Find similar examples in the normal and anomalous groups.\n"
        "5. Apply if/then rules to identify reasons for further review.\n"
        "6. Use A-star to order simulated review checks.\n"
        "7. See how the source code connects these methods and course concepts."
    )

# One selected stage keeps each rerun focused on the explanation the learner opened.
active_stage = st.segmented_control(
    "Choose one walkthrough stage",
    WALKTHROUGH_STAGES,
    default=WALKTHROUGH_STAGES[0],
    key="walkthrough_stage",
    selection_mode="single",
    required=True,
    width="stretch",
    wrap=True,
)

# __________________________________________
# LOAD THE ACTIVE PROFILE
# ==========================================
# Resolve the shared profile and obtain its fitted state inside the loading region.
# Controlled source errors prevent the example-dependent flow from continuing.

# Resolve the profile chosen in the router's shared session state.
active_source = source_definition(st.session_state["data_profile"])
# Keep source provenance visible while loading that profile's fitted resources.
st.caption(f"Active data profile: {active_source.profile_label}. {active_source.provenance}.")

# Reserve a loading region for profile preparation and evaluation reuse.
evaluation_loading_region = st.container()
try:
    with evaluation_loading_region.skeleton(height=180):
        # Fingerprint the active source and configuration before selecting a cached resource.
        active_identity = build_cache_identity(active_source)
        # Reuse matching fitted state or build it when this identity has no cached resource.
        frontend_state = get_cached_frontend_state(active_identity, active_source)
except CubeSatError as exc:
    st.error(f"Current-profile evaluation is unavailable: {exc}")
    if not active_source.simulated:
        st.info(
            "Follow data/README.md to prepare the expected files, or choose Deterministic demo "
            "fixture from Data profile to try the included simulated examples."
        )
else:

    # __________________________________________
    # CHOOSE A HELD-OUT EXAMPLE
    # ==========================================
    # Use the loaded screening population for example choices and attach source context.
    # The selected ID is passed unchanged to the stage dispatch below.

    # Offer only held-out IDs, ordered by the existing screening probabilities.
    segment_ids = walkthrough_segment_ids(frontend_state)
    # Explain example ordering and which views depend on the chosen segment.
    st.write(
        "Choose a segment to follow through the methods. The highest anomaly probabilities "
        "appear first. Selecting another example does not retrain or refit the model. The data "
        "overview and architecture map describe the whole program, so those views stay the same."
    )
    # Keep example selection attached to an exact held-out segment ID across reruns.
    selected_segment_id = st.selectbox(
        "Example held-out test segment",
        segment_ids,
        key="walkthrough_segment",
        help=(
            "Choose one exact test segment that was excluded from fitting and threshold selection."
        ),
        filter_mode="contains",
        persist_state="session",
    )
    # Resolve the segment's channel and optional fixture scenario for context captions.
    example_context = build_walkthrough_example_context(
        frontend_state,
        selected_segment_id,
    )
    # Identify the exact row and source channel behind the following method example.
    st.caption(f"Selected segment {example_context.segment_id}, channel {example_context.channel}.")
    st.caption(
        "The segment ID identifies this example. The channel code identifies its telemetry "
        "source; it does not tell us which spacecraft subsystem caused an unusual reading."
    )
    # Limit scenario labels to the simulated profile that defines them.
    if active_source.simulated:
        # Describe the fixture scenario's intended route without changing the analysis.
        st.caption(
            f"Demo scenario {example_context.scenario_name}: {example_context.scenario_purpose} "
            "The scenario name describes the example's intended review route."
        )

    # __________________________________________
    # DISPATCH THE SELECTED STAGE
    # ==========================================
    # Choose the renderer after the profile and example are available.
    # Only method stages require a complete selected-segment result.

    # These two stages need profile context but no complete selected-segment analysis.
    if active_stage == "Data source and roles":
        _render_data_stage(frontend_state)
    elif active_stage == "Architecture map":
        _render_architecture_stage(frontend_state)
    else:
        # The five method stages share one complete backend result for the selected example.
        try:
            selected_result = analyze_selected_segment(
                frontend_state,
                selected_segment_id,
            )
        except CubeSatError as exc:
            st.error(f"The selected example could not be analyzed: {exc}")
        else:
            if active_stage == "MLP probability":
                _render_mlp_stage(frontend_state, selected_result)
            elif active_stage == "Threshold and evaluation":
                _render_threshold_stage(frontend_state, selected_result)
            elif active_stage == "Similarity search":
                _render_similarity_stage(frontend_state, selected_result)
            elif active_stage == "Logic rules":
                _render_logic_stage(frontend_state, selected_result)
            elif active_stage == "A-star planning":
                _render_planning_stage(frontend_state, selected_result)


# __________________________________________
# END OF FILE
# ==========================================
