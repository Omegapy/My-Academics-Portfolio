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
# - Present held-out screening totals, channel comparisons, and a ranked review list.
# - Show backend evidence and recommended review steps for the selected segment.
#
# Usage / Integration:
# - Executed as a page by streamlit_app.py after shared profile initialization.
# - Uses cubesat_frontend records and transforms to assemble the visible results.
#
# Contents Overview:
# - Filter-reset, selected-evidence, and recommendation rendering helpers.
# - Current-profile loading, full-population summaries, filters, and segment selection.
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

"""Render held-out telemetry screening and selected-segment evidence.

The page first describes the complete held-out population, including channel counts and
rates. Filters then narrow the review list while leaving those population summaries and
the fitted model unchanged. A selected segment ID connects the list to its detailed
probability, historical evidence, and proposed review steps, even when row positions change.

Streamlit reruns this page after an interaction. Widget choices stay in session state,
while the frontend adapter reuses the fitted assistant for the current data identity.
The page formats backend results and leaves numerical decisions to their owning modules.
"""

# __________________________________________
# IMPORTS
# ==========================================

import streamlit as st

# Reuse adapter-owned results and view transforms throughout this page.
from cubesat_frontend import (
    STATUS_OPTIONS,
    FrontendState,
    analyze_selected_segment,  # Full evidence for one selected ID.
    authentic_reference_frame,  # Fixed benchmark context.
    build_cache_identity,  # Fingerprint the current source.
    build_channel_figure,  # Chart the shared channel totals.
    build_dataset_context,  # Describe actual row roles.
    channel_accessible_lines,  # Text equivalents of channel counts.
    channel_reading_frame,  # Present counts and denominators.
    channel_summary_frame,  # Aggregate the screened population.
    channel_worked_example,  # Explain one count-to-rate calculation.
    dataset_role_frame,  # Separate fitting, cutoff, and held-out rows.
    decision_explanation,  # Explain the existing backend decision.
    deviation_frame,  # Format stored normal-reference deviations.
    filter_screening,  # Narrow a copy of the ranked view.
    get_cached_frontend_state,  # Reuse the matching fitted assistant.
    highest_flagged_channels,  # Include ties in count leaders.
    learner_terms_frame,  # Shared definitions in reading order.
    reconcile_selection,  # Retain only a currently visible ID.
    review_table_frame,  # Select the human-facing review columns.
    screening_frame,      # Rank stored held-out predictions.
    source_definition,  # Resolve the shared profile choice.
    summarize_screening,  # Count mutually exclusive review statuses.
)
from cubesat_types import CompleteAnalysisResult, CubeSatError, PlanStatus  # CubeSat types.

# __________________________________________
# UI-ONLY HELPERS
# ==========================================


# ________________________________________________
# Filter reset
# ------------------------------------------------
# Reset presentation choices together so the next rerun can show the complete review list.

# --- _reset_filters()
def _reset_filters() -> None:
    """Restore the complete ranked view and remove the selected detail.

    Streamlit calls this button callback before the next page rerun. Updating the widget
    keys together lets that rerun build a consistent unfiltered list with no stale
    segment selection. It does not discard the fitted backend resource.
    """
    st.session_state["filter_statuses"] = []  # Include all review statuses.
    st.session_state["filter_channels"] = []  # Include every channel.
    st.session_state["segment_search"] = ""  # Remove the exact-ID restriction.
    st.session_state["segment"] = None  # Clear detail tied to the old view.


# ---


# ________________________________________________
# Historical-case presentation
# ------------------------------------------------
# Format retrieved normal and anomalous neighbors without repeating the similarity search.

# --- _render_similar_cases()
def _render_similar_cases(result: CompleteAnalysisResult) -> None:
    """Present normal and anomalous historical neighbors as separate groups.

    Each card uses the neighbor's stored rank, reviewed label, distance, and largest
    standardized feature gaps. The groups retain their reviewed-class meaning even when
    one has no eligible cases. This helper formats the evidence already retrieved by
    the backend; it does not run another similarity search.

    Args:
        result: Complete backend analysis with class-specific neighbor records.
    """
    st.subheader("Similar reviewed historical cases", anchor=False)  # Stored neighbors.
    # Explain the distance scale and the limits of historical comparison.
    st.caption(
        "Distance compares two segments across the same 18 scaled features; smaller values "
        "mean more similar examples. The normal and anomalous lists are searched separately "
        "and can include other channels. Reviewed labels describe those historical cases; "
        "they do not change this segment's prediction. The largest feature gaps show where "
        "two examples differ, not which features caused the MLP prediction."
    )
    # Keep reviewed classes separate so support and conflict remain visible.
    for heading, cases in (
        ("Reviewed normal cases", result.similarity.normal_cases),
        ("Reviewed anomalous cases", result.similarity.anomalous_cases),
    ):
        # Identify which reviewed class supplies this group.
        st.markdown(f"**{heading}**")
        # Explain a missing reference class without inventing a comparison.
        if not cases:
            st.caption(f"No eligible {heading.lower()[:-1]} was available.")
            continue
        # Preserve the backend neighbor order within each reviewed class.
        for case in cases:
            # Pair each named feature with its stored standardized difference.
            feature_gaps = ", ".join(
                (
                    f"{difference.feature_name} "  # Backend feature identity.
                    f"({difference.absolute_standardized_difference:.3f})" # Scaled gap.
                )
                for difference in case.feature_differences
            )
            # Keep one case identifier, distance, and feature-gap list together.
            with st.container(border=True):
                # Use the returned rank and stable historical segment ID.
                st.markdown(f"**Rank {case.rank}: segment {case.case_id}**")
                # Attach the reviewed class to its distance from the selected segment.
                st.caption(
                    f"Reviewed label: {case.reviewed_label} · Euclidean distance: "
                    f"{case.distance:.3f}"
                )
                # Show where these two examples differ on the shared scaled features.
                st.caption(f"Largest standardized feature gaps: {feature_gaps}")


# ---


# ________________________________________________
# Selected recommendations
# ------------------------------------------------
# Read the returned simulated plan and explain its outcome before listing any actions.

# --- _render_recommendations()
def _render_recommendations(result: CompleteAnalysisResult) -> None:
    """Present the existing plan as proposed human reviews for the selected segment.

    The backend owns action selection, order, and cost. This helper displays those
    results without running another analysis or recording any review as completed.

    Args:
        result: Current segment analysis with its reasoning and simulated plan.

    Logic:
        1. Identify the segment and explain the advisory meaning of the recommendations.
        2. Show routine monitoring or manual review when there is no usable sequence.
        3. Display a found plan in its returned order with its simulated effort cost.
    """
    # Use the simulated plan already produced for the selected segment.
    plan = result.plan
    # Give the selected plan a single location in the detail panel.
    st.subheader("Recommended next steps", anchor=False)
    # Tie the proposed reviews to this segment and state their simulated scope.
    st.caption(
        f"For segment {result.segment_id}, channel {result.selected_channel}. "
        "These are proposed human reviews. The actions are simulated; the app does not "
        "perform them, inspect spacecraft hardware, or confirm that a review occurred."
    )
    # Display hypotheses only when the selected reasoning result contains them.
    if result.reasoning.suspected_faults:
        # List only hypotheses present in this segment's reasoning result.
        # Keep their simulated status explicit in the message below.
        st.write(
            "Possible fault hypotheses to investigate (simulated teaching assumptions): "
            + ", ".join(result.reasoning.suspected_faults)
            + ". These are not confirmed diagnoses."
        )

    # __________________________________________
    # OUTCOMES WITHOUT AN ACTION SEQUENCE
    # ==========================================
    # Monitoring and unavailable-plan outcomes each explain their result and return early.

    # A normal outcome can request monitoring without a diagnostic sequence.
    if plan.status == PlanStatus.NOT_REQUIRED:
        # Explain why no additional simulated checks are listed.
        st.info(
            "Continue routine monitoring. The current analysis requests no further "
            "simulated diagnostic checks."
        )
        return
    # An unavailable path requires manual review rather than an invented action order.
    if plan.status == PlanStatus.UNAVAILABLE:
        # Make the lack of a valid recommendation sequence visible.
        st.warning(
            "No valid recommendation sequence is available. Review the evidence manually "
            "before deciding what to investigate next."
        )
        # Preserve the planner explanation for this unavailable outcome.
        st.caption(plan.message)
        return

    # __________________________________________
    # ORDERED SIMULATED REVIEWS
    # ==========================================
    # A found path supplies the action order and accumulated effort shown below.

    # Introduce the found sequence as reviews to perform in the returned order.
    st.write("Review the evidence in this order using the results above and below:")
    # Preserve the backend's order, which already satisfies the action prerequisites.
    st.markdown(
        "\n".join(
            f"{step}. {planned_action.action.description}"
            for step, planned_action in enumerate(plan.ordered_actions, start=1)
        )
    )
    # Display the stored path cost with its coursework effort units.
    st.caption(
        f"Total simulated review effort: {plan.total_cost:g} units. "
        "These coursework costs represent relative effort, not minutes or money. "
        "A-star planning orders the required checks according to their prerequisites and costs."
    )
    # Link the concise recommendation to the walkthrough of the full action catalog.
    st.caption(
        "To see all five available checks and their prerequisites, open Data and AI "
        "walkthrough and select A-star planning."
    )
# ---


# ________________________________________________
# Selected evidence and detail
# ------------------------------------------------
# Join one complete analysis with its matching screening record for a consistent detail view.

# --- _render_selected_detail()
def _render_selected_detail(state: FrontendState, segment_id: str) -> None:
    """Show evidence and recommended review steps for one current segment selection.

    The cached assistant performs the selected-segment analysis. Its classification and
    historical results and plan supply the detail panel, while the screening snapshot
    supplies the matching three-way status. Repeated review messages are displayed once in their
    original order so the same conflict does not produce duplicate warnings.

    Args:
        state: Fitted profile resource already used to construct the review list.
        segment_id: Exact ID retained by the filtered segment selector.

    Logic:
        1. Request the selected result and show controlled backend errors in the page.
        2. Match the screening status by segment ID and format the stored probabilities.
        3. Present review reasons and recommendations before detailed supporting evidence.
    """
    # Request full evidence only for the exact ID chosen in the ranked view.
    try:
        result = analyze_selected_segment(state, segment_id)
    except CubeSatError as exc:
        # Keep expected analysis failures local to this detail panel.
        st.error(f"Unable to analyze segment {segment_id}: {exc}")
        return

    # __________________________________________
    # CLASSIFICATION AND REVIEW CONTEXT
    # ==========================================
    # Present stored probability and cutoff values, then the reasons and proposed next steps.

    # Use the classification returned with the complete selected analysis.
    classification = result.classification
    # Match the population screening status by stable segment ID.
    status = next(
        record.status
        for record in state.screening_records
        if record.segment_id == result.segment_id
    )
    # Header for the selected segment.
    st.header(f"Selected segment: {result.segment_id}", anchor=False)
    # Keep channel, held-out role, and review status beside the selected ID.
    st.caption(
        f"Telemetry channel {result.selected_channel} · held-out test segment · {status}"
    )

    # Primary metrics columns.
    primary_metric_columns = st.columns(2)
    # Anomaly probability metric.
    primary_metric_columns[0].metric(
        "Anomaly probability",
        f"{classification.anomaly_probability:.1%}",
        border=True,
    )
    # Validation threshold metric.
    primary_metric_columns[1].metric(
        "Validation threshold",
        f"{classification.classification_threshold:.1%}",
        border=True,
    )
    # Secondary metrics columns.
    secondary_metric_columns = st.columns(2)
    # Uncertainty margin metric.
    secondary_metric_columns[0].metric(
        "Uncertainty margin",
        f"±{classification.uncertainty_margin:.1%}",
        border=True,
    )
    # AI screening status metric.
    secondary_metric_columns[1].metric("AI screening status", status, border=True)
    # Explain cutoff and uncertainty values without treating rounded probability as certainty.
    st.caption(
        "Anomaly probability is the neural network's 0-to-1 estimate, not certainty. The "
        "validation threshold is the cutoff for predicting normal or anomalous. The uncertainty "
        "margin adds a band around that cutoff for close calls needing review. Percentages are "
        "rounded to one decimal place, so even 100.0% does not guarantee a correct prediction."
    )
    # Interpret the existing decision using its exact threshold and margin.
    st.write(decision_explanation(result))
    # Start with the symbolic reasoning reasons that require human review.
    review_messages = list(result.reasoning.manual_review_reasons)
    # Include any disagreement between classification and historical comparisons.
    if result.similarity.conflict_reason:
        review_messages.append(result.similarity.conflict_reason)
    # One conflict can appear in more than one backend field. Preserve order without repeating it.
    for message in dict.fromkeys(review_messages):
        st.warning(f"Review context: {message}")
    # Present the backend plan before the detailed supporting measurements.
    _render_recommendations(result)

    # __________________________________________
    # MEASUREMENT AND HISTORICAL EVIDENCE
    # ==========================================
    # Show the stored deviations and neighbor records that support inspection of this result.

    # Feature deviations header.
    st.subheader("Largest feature deviations", anchor=False)
    # Distinguish unusual normal-reference measurements from physical-cause explanations.
    st.caption(
        "These features differ most from the reviewed normal model-training examples. "
        "The program compares each value with that group's average and spread. This "
        "comparison helps locate unusual measurements; it does not explain their physical cause. "
        "The MLP probability stage in Data and AI walkthrough explains all 18 feature names."
    )
    # Format deviations already calculated during selected-segment reasoning.
    feature_frame = deviation_frame(result)
    # An empty table means no feature crossed the configured deviation threshold.
    if feature_frame.empty:
        st.caption("No feature crossed the configured deviation threshold for this segment.")
    # Keep the nonempty deviation records in their supplied order.
    else:
        # Present the stored feature values and deviation measures together.
        st.dataframe(
            feature_frame,
            hide_index=True,
            width="stretch",
            key="deviation_table",
        )
    # Follow the feature evidence with separately reviewed historical comparisons.
    _render_similar_cases(result)

    # Include the backend historical assessment when one was supplied.
    if result.similarity.historical_support:
        st.caption(f"Historical evidence summary: {result.similarity.historical_support}.")


# ---


# __________________________________________
# DIRECT PAGE FLOW
# ==========================================

# Title for the telemetry page.
st.title("Analyze telemetry", anchor=False)
# Introductory text.
st.write(
    "This app helps you decide which recorded spacecraft measurements need a closer look. "
    "Each result describes a segment: a group of readings from one telemetry channel over "
    "a time window. Start with the counts below, then choose a segment to inspect its results."
)
# Text describing the AI's role.
st.write(
    "Artificial intelligence (AI) supplies an anomaly probability, a review status, and similar "
    "historical examples. You decide whether more review is needed. These results do not "
    "confirm a spacecraft fault."
)

# __________________________________________
# SOURCE LOADING
# ==========================================
# Resolve the shared profile and obtain its fitted state before building population views.

# Resolve the profile selected in the shared router sidebar.
active_source = source_definition(st.session_state["data_profile"])
# Keep active-profile provenance next to the dataset interpretation.
with st.container(border=True):
    # Name the profile whose rows will supply this view.
    st.markdown(f"**Active data profile:** {active_source.profile_label}")
    # Use the source definition associated with that exact profile.
    st.caption(active_source.provenance)
    # Caption for the segment ID.
    st.caption(
        "Each segment ID identifies one example. Channel codes group examples by telemetry "
        "source; they do not identify separate spacecraft or count events within a segment."
    )
    # Caption for held-out segments.
    st.caption(
        "Held-out means these examples were kept out of model training and threshold selection. "
        "They let us check the model on separate data."
    )

# Reserve loading feedback before obtaining the fitted resource.
loading_region = st.container()
# Validate source identity and reuse or build its matching fitted state.
try:
    with loading_region.skeleton(height=180):
        # Fingerprint the current file on each rerun, then reuse its matching fitted resource.
        active_identity = build_cache_identity(active_source)
        frontend_state = get_cached_frontend_state(active_identity, active_source)
# Explain source-validation failures before any population results are rendered.
except CubeSatError as exc:
    st.error(f"The selected data profile could not be loaded: {exc}")
    # Offer local preparation guidance when authentic data cannot be loaded.
    if not active_source.simulated:
        st.info(
            "Prepare the pinned files with data/README.md, or choose Deterministic demo fixture "
            "from Data profile to exercise the workflow offline."
        )
    # Stop this page before dereferencing an unavailable fitted state.
    st.stop()


# __________________________________________
# DATA CONTEXT
# ==========================================
# Build the complete screening frame and partition context used by the following explanations.

# Keep population summaries upstream of filters so a narrowed list cannot change their totals.
full_screening_frame = screening_frame(frontend_state.screening_records)
# Count every held-out prediction before any view filter is applied.
summary = summarize_screening(full_screening_frame)
# Read actual source dimensions and partition roles from the fitted assistant.
dataset_context = build_dataset_context(frontend_state)

# Header for the data section.
st.header("Understand the data", anchor=False)
# Text describing the dataset.
st.write(
    f"The active {dataset_context.profile_label} contains "
    f"{dataset_context.total_segments:,} segments, {dataset_context.feature_count} numerical "
    f"features per segment, and {len(dataset_context.channel_codes)} coded channels. Its "
    f"{dataset_context.official_training_segments:,} official training-role segments become "
    f"{dataset_context.model_training_segments:,} model-training rows plus "
    f"{dataset_context.threshold_validation_segments:,} threshold-validation rows. The remaining "
    f"{dataset_context.held_out_segments:,} segments are held out."
)
# Keep fixture scale separate from the authentic benchmark reference.
if dataset_context.simulated:
    # Read the benchmark reference separately from active fixture counts.
    authentic_values = dict(authentic_reference_frame().itertuples(index=False, name=None))
    # Label these fixed benchmark counts as context for the smaller active fixture.
    st.caption(
        "This active profile is a simulated fixture. The separate authentic OPS-SAT-AD v2 "
        f"benchmark has {authentic_values['Total segments']:,} total segments, "
        f"{authentic_values['Official training-role segments']:,} official training-role "
        f"segments, {authentic_values['Held-out test segments']:,} held-out segments, "
        f"{authentic_values['Numerical features']} features, and "
        f"{authentic_values['Coded channels']} coded channels."
    )
# Show which rows train weights, choose the threshold, or remain held out.
st.dataframe(
    dataset_role_frame(dataset_context),
    hide_index=True,
    width="stretch",
    key="analysis_data_roles",
)
# Caption for the held-out population.
st.caption(
    "The held-out population is the set being screened, not a count of anomalies. Reviewed "
    "normal/anomalous labels are revealed only for evaluation; AI screening statuses come from "
    "the current model run."
)
# Header for the terms section.
st.subheader("Terms used on this page", anchor=False)
# Get the terms frame.
term_frame = learner_terms_frame()
# Render the terms.
st.markdown(
    "\n".join(
        f"- **{term}:** {definition}"
        for term, definition in term_frame.itertuples(index=False, name=None)
    )
)


# __________________________________________
# FULL-POPULATION SUMMARY
# ==========================================
# Present mutually exclusive screening counts from the complete held-out snapshot.

# Header for the screening summary.
st.header("Held-out screening summary", anchor=False)
st.caption(
    "Each held-out segment receives exactly one status. The three status counts add up to "
    "the screened total."
)
# Build the summary columns.
summary_columns = st.columns(4)
summary_columns[0].metric("Segments screened", summary.screened, border=True)
summary_columns[1].metric("Flagged anomaly", summary.flagged, border=True)
summary_columns[2].metric("Uncertain review", summary.uncertain, border=True)
summary_columns[3].metric("Likely normal", summary.likely_normal, border=True)
# Caption for the summary columns.
st.caption(
    "Flagged anomaly means the probability is above the uncertainty band; Uncertain review "
    "means it is inside the band; Likely normal means it is below the band."
)
# Caption for evaluation metrics.
st.caption(
    "These screening counts summarize model decisions. Evaluation metrics compare predictions "
    "with reviewed labels after prediction. Software tests separately check that the code and "
    "interface behave as specified; they are not model-performance scores."
)

# __________________________________________
# CHANNEL COMPARISON
# ==========================================
# Calculate channel totals once for the chart, table, and text.
# Each rate uses that channel's screened population as its denominator.

# The chart, readable table, and text descriptions all use this same channel summary.
# Aggregate all held-out records so each rate has its full channel denominator.
channel_frame = channel_summary_frame(full_screening_frame) 
# Retain all tied count leaders independently of the per-channel rates.
leading_channels = highest_flagged_channels(channel_frame) 
# Header for the channel comparison section.
st.header("Channel comparison", anchor=False)
# Caption for the channel comparison section.
st.caption(
    "The horizontal labels are coded source identifiers, not inferred subsystem names. The "
    "vertical axis is held-out segment count. Bars compare flagged and uncertain counts in "
    "ascending channel-code order; printed values and the table preserve meaning without color "
    "or pointer hover."
)
# Plot counts from the same summary used by the adjacent table.
st.plotly_chart(
    build_channel_figure(channel_frame),
    theme="streamlit",
    width="stretch",
    key="channel_review_chart",
    config={"displayModeBar": False, "displaylogo": False, "scrollZoom": False},
)
# Subheader for channel counts and rates.
st.subheader("Channel counts and rates", anchor=False)
# Caption for channel counts and rates.
st.caption(
    "Each row uses one channel's screened count as its denominator. Count ranking answers which "
    "channel has the most segments; rate ranking answers which has the largest share, so the two "
    "rankings can differ."
)
# Display the channel reading frame.
st.dataframe(
    channel_reading_frame(channel_frame),
    hide_index=True,
    width="stretch",
    key="channel_reading_table",
    column_config={
        "Flagged rate": st.column_config.NumberColumn(format="percent"),
        "Uncertain rate": st.column_config.NumberColumn(format="percent"),
    },
)
# Markdown for channel accessible lines.
st.markdown("\n".join(f"- {line}" for line in channel_accessible_lines(channel_frame)))
# Caption for the worked example.
st.caption(channel_worked_example(channel_frame))
# If there are leading channels, then show the caption.
if leading_channels:
    # Use the shared maximum for every channel tied at the top.
    leading_count = int(channel_frame["flagged"].max())
    # Build the segment word.
    segment_word = "segment" if leading_count == 1 else "segments"
    # Caption for the leading channels.
    st.caption(
        "Highest flagged count: "
        + ", ".join(leading_channels)
        + f" ({leading_count} held-out {segment_word})."
    )


# __________________________________________
# RANKED REVIEW AND FILTERS
# ==========================================
# These controls narrow the held-out review list after the model has been fitted.
# Population totals and channel comparisons continue to use the full screening data.

# Header for the ranked segment review.
st.header("Ranked segment review", anchor=False)
# Caption for the ranked segment review.
st.caption(
    "The highest anomaly probabilities appear first. Equal scores are ordered by segment ID. "
    "Filters narrow this list without retraining the model or changing the overall counts."
)
# Offer every screened channel even when current filters hide some rows.
all_channels = tuple(sorted(str(channel) for channel in full_screening_frame["channel"].unique()))
# setdefault preserves choices on reruns and page visits; empty choices include every value.
st.session_state.setdefault("filter_statuses", [])
st.session_state.setdefault("filter_channels", [])
# Caption for the filters.
st.caption("Leave status or channel empty to include all available values.")
# Build the filter columns.
filter_columns = st.columns(3)
# Multiselect for AI screening status.
with filter_columns[0]:
    selected_statuses = st.multiselect(
        "AI screening status",
        STATUS_OPTIONS,
        key="filter_statuses",
        placeholder="All statuses",
        persist_state="session",
    )
# Multiselect for telemetry channel.
with filter_columns[1]:
    selected_channels = st.multiselect(
        "Telemetry channel",
        all_channels,
        key="filter_channels",
        placeholder="All channels",
        persist_state="session",
    )
# Text input for exact segment ID.
with filter_columns[2]:
    exact_segment_id = st.text_input(
        "Exact segment ID",
        key="segment_search",
        type="search",
        placeholder="For example, demo-046",
        persist_state="session",
    )
# Button to reset filters.
st.button(
    "Reset filters",
    key="reset_filters",
    on_click=_reset_filters,
)

# Filtering copies the view after fitting. The complete held-out snapshot stays available.
# Apply the selected status, channel, and exact-ID restrictions to the view.
filtered_screening_frame = filter_screening(
    full_screening_frame,
    statuses=selected_statuses or None,
    channels=selected_channels or None,
    exact_segment_id=exact_segment_id,
)
# Compare the visible count with the unchanged full held-out population.
st.caption(
    f"Showing {len(filtered_screening_frame)} of {len(full_screening_frame)} held-out segments."
)
# If the filtered screening frame is empty, then show the warning.
if filtered_screening_frame.empty:
    st.warning("No held-out segment matches the current filters.")
# Otherwise, display the review table frame.
else:
    st.dataframe(
        review_table_frame(filtered_screening_frame),
        hide_index=True,
        width="stretch",
        key="screening_table",
        column_config={
            "Probability": st.column_config.NumberColumn(format="percent"),
        },
    )


# __________________________________________
# SELECTION RECONCILIATION
# ==========================================
# Check the previous ID against the visible records before constructing this rerun's selector.

# A displayed row index can change after filtering. Resolve selection against exact segment IDs.
current_selection = st.session_state.get("segment")
valid_selection = reconcile_selection(filtered_screening_frame, current_selection)
# Clear stale widget state before creating the selector in this run.
if valid_selection != current_selection:
    st.session_state.pop("segment", None)

# Offer only stable IDs still present after filtering.
segment_options = tuple(str(value) for value in filtered_screening_frame["segment_id"])
# Bind the exact chosen ID to session state and its shareable URL parameter.
selected_segment_id = st.selectbox(
    "Segment to inspect",
    segment_options,
    index=None,
    key="segment",
    placeholder="Select an exact segment ID",
    disabled=not segment_options,
    filter_mode="contains",
    bind="query-params",
    persist_state="session",
)

# __________________________________________
# DETAIL DISPATCH
# ==========================================
# A valid selection supplies the exact segment ID for the complete evidence panel.

# Full historical, logic, and planning analysis is requested only after a segment is selected.
if selected_segment_id:
    # Use the same fitted profile resource that supplied the ranked list.
    _render_selected_detail(frontend_state, selected_segment_id)
# Otherwise, display the info message.
else:
    st.info(
        "Select a segment ID to inspect its probability, threshold, recommended next steps, "
        "deviations, and similar reviewed cases."
    )


# __________________________________________
# END OF FILE
# ==========================================
