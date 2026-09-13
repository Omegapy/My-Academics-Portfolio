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
# - Represent knowledge with facts and rules that support human decision-making.
# - Connect expert-system reasoning to the program's symbolic planning method.
#
# Module Purpose:
# - Turn numerical and historical evidence into facts, then derive review requirements.
# - Keep simulated fault hypotheses separate from confirmed spacecraft diagnoses.
#
# Usage / Integration:
# - Called by the coordinator and verifier after classification and similarity search.
# - Return facts and inference traces for the planner and presentation modules.
#
# Contents Overview:
# - Horn-rule catalog, variable matching, substitution, and evidence-to-fact conversion.
# - Consistency checks, a critical-deviation query, and traced forward chaining.
#
# Dependencies:
# - Standard Library: collections
# - Third-Party: NumPy
# - Local Project: cubesat_config, cubesat_types
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Connect telemetry evidence to explicit review rules.

The classifier and similarity search produce numbers and historical comparisons. This module first
turns qualifying evidence into facts, then matches those facts against a small expert-system rule
catalog. The result explains which checks are required and why a segment may need human review.

The representation uses a bounded part of first-order logic. A fact contains a predicate, such as
`Deviates`, and its terms, such as a segment ID and channel. Rule terms such as `?s` name variables;
other terms are constants. Matching assigns each variable a consistent value. Rules add
positive conclusions from matching premises, with no general negation or nested function terms.

The returned trace records the first derivation that adds each new fact. A suspected fault remains
a simulated hypothesis to investigate, even when every premise of its rule matches.
"""

# ____________________________________________________________________________________
# ====================================================================================
#
# SYMBOLIC REASONING MAP
#
# numerical probability and normal-training z-scores -> asserted facts
# ordered facts + ordered Horn rules -> unification -> forward-chaining fixed point
# derived RequiresCheck and SuspectedFault facts -> simulated A-star planning inputs
#
# A Horn rule says that all its premises imply one positive conclusion:
# Anomalous(?s) AND Deviates(?s, ?c) AND Critical(?c) -> RequiresCheck(?s, ?c)
#
# For example, binding ?s to "demo-046" and ?c to "CADC0872" connects the same segment
# and channel across all three premises. The conclusion then uses those bound values.
#
# Forward chaining repeatedly adds conclusions to the known facts. A fixed point means
# that another pass adds nothing. The built-in rules reuse a finite set of constants, and
# the fact set stores each fact once, so this process has a finite stopping condition.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

from collections import defaultdict # Import defaultdict for default dictionary. 

# pyrefly: ignore [missing-import]
import numpy as np # Import numpy for numerical operations.

from cubesat_config import CHANNEL_KNOWLEDGE, DEFAULT_CONFIG, AppConfig # Import configuration constants.
from cubesat_types import (
    ClassificationResult, # Import classification results. 
    Fact, # Import facts. 
    HornRule, # Import Horn rules. 
    InferenceTrace, # Import inference traces. 
    ReasoningResult, # Import reasoning results. 
    SimilarityResult, # Import similarity results.
    TrainedTelemetryModel, # Import trained telemetry model.
)

# __________________________________________
# KNOWLEDGE-BASE CATALOG
# ==========================================


# --- build_horn_rules()
def build_horn_rules() -> tuple[HornRule, ...]:
    """Return the ordered rules used to turn evidence into review requirements.

    `?s` stands for a segment, `?c` for a channel, and `?f` for a simulated fault name.
    A rule can fire only when every premise matches with the same values for shared variables.
    The stored explanation and source status travel with the resulting inference trace.

    Args:
        config: Configuration for the application. 
        channel_knowledge: Knowledge about the channels. 

    Returns:
        Rules for critical-deviation checks, simulated hypotheses, and human-review routes.
        Their tuple order also determines which derivation is recorded first when rules overlap.
    """
    # Return the Horn rules.
    return (
        # This rule requires all three facts for the same segment and channel.
        HornRule(
            rule_id="RULE-001-REQUIRE-CRITICAL-DEVIATION-CHECK",
            premises=(
                Fact("Anomalous", ("?s",)),
                Fact("Deviates", ("?s", "?c")),
                Fact("Critical", ("?c",)),
            ),
            conclusion=Fact("RequiresCheck", ("?s", "?c")),
            explanation="A critical channel deviation in an anomalous segment requires review.",
            source_status="source-derived rule pattern",
        ),
        # A fault hypothesis needs historical support and an explicit simulated mapping as well.
        HornRule(
            rule_id="RULE-002-SUSPECT-SIMULATED-FAULT",
            premises=(
                Fact("Anomalous", ("?s",)),
                Fact("Deviates", ("?s", "?c")),
                Fact("Critical", ("?c",)),
                Fact("HistoricalSupports", ("?s", "anomalous")),
                Fact("FaultMapping", ("?c", "?f")),
            ),
            conclusion=Fact("SuspectedFault", ("?s", "?f")),
            explanation=(
                "Classification, critical deviation, and historical evidence support a simulated "
                "fault hypothesis to investigate."
            ),
            source_status="simulated educational rule",
        ),
        # These separate routes preserve the reason that stronger interpretation needs a person.
        HornRule(
            rule_id="RULE-003-UNCERTAINTY-REQUIRES-MANUAL-REVIEW",
            premises=(Fact("Uncertain", ("?s",)),),
            conclusion=Fact("ManualReviewRequired", ("?s",)),
            explanation="A near-threshold or otherwise uncertain result requires human review.",
            source_status="source-derived route rule",
        ),
        # This rule requires conflicting evidence for the same segment.
        HornRule(
            rule_id="RULE-004-CONFLICT-REQUIRES-MANUAL-REVIEW",
            premises=(Fact("ConflictingEvidence", ("?s",)),),
            conclusion=Fact("ManualReviewRequired", ("?s",)),
            explanation="Conflicting evidence must be resolved by a human reviewer.",
            source_status="source-derived route rule",
        ),
        # This rule requires insufficient evidence for the same segment.
        HornRule(
            rule_id="RULE-005-INSUFFICIENT-EVIDENCE-REQUIRES-MANUAL-REVIEW",
            premises=(Fact("InsufficientEvidence", ("?s",)),),
            conclusion=Fact("ManualReviewRequired", ("?s",)),
            explanation="Unavailable or insufficient evidence prevents a stronger conclusion.",
            source_status="source-derived route rule",
        ),
        # This rule requires conflicting classifications for the same segment.
        HornRule(
            rule_id="RULE-006-MUTUALLY-EXCLUSIVE-CLASSIFICATIONS-CONFLICT",
            premises=(Fact("Normal", ("?s",)), Fact("Anomalous", ("?s",))),
            conclusion=Fact("ConflictingEvidence", ("?s",)),
            explanation="A segment cannot be presented as both normal and anomalous.",
            source_status="simulated consistency rule",
        ),
        # This rule requires a suspected fault for the same segment and fault.
        HornRule(
            rule_id="RULE-007-FAULT-HYPOTHESIS-REQUIRES-MAPPING-REVIEW",
            premises=(Fact("SuspectedFault", ("?s", "?f")),),
            conclusion=Fact("RequiresCheck", ("?s", "fault_mapping_review")),
            explanation="A simulated fault hypothesis requires review of its supporting mapping.",
            source_status="simulated educational rule",
        ),
        # This rule requires uncertainty for the same segment.
        HornRule(
            rule_id="RULE-008-UNCERTAINTY-REQUIRES-HISTORICAL-REVIEW",
            premises=(Fact("Uncertain", ("?s",)),),
            conclusion=Fact("RequiresCheck", ("?s", "historical_evidence_review")),
            explanation="An uncertain route requires additional historical-evidence review.",
            source_status="simulated educational rule",
        ),
    )
# ---


# __________________________________________
# UNIFICATION AND SUBSTITUTION
# ==========================================


# --- is_variable()
def is_variable(term: str) -> bool:
    """Return whether a term starts with `?` followed by a nonempty variable name. 
    
    Args:
        term: The term to check. 

    Returns:
        True if the term is a variable, False otherwise.
    """
    # Return whether a term starts with `?` followed by a nonempty variable name.
    return term.startswith("?") and len(term) > 1
# ---


# --- unify_fact()
def unify_fact(
    pattern: Fact,
    concrete_fact: Fact,
    bindings: dict[str, str] | None = None,
) -> dict[str, str] | None:
    """Match a rule pattern to one fact while keeping shared variable values consistent.

    Unification is the matching step that finds values for variables. For example, matching
    `Deviates(?s, ?c)` with `Deviates(demo-046, CADC0872)` binds the segment and channel names.

    Args:
        pattern: Rule premise containing variables, constants, or both.
        concrete_fact: Candidate fact whose terms supply the values for this match.
        bindings: Values already established by earlier premises in the same rule match.

    Returns:
        A new binding dictionary, or `None` if predicates, term counts, constants, or an existing
        variable value disagree. The caller's dictionary is not changed by a failed branch.
    """
    # A predicate's name and number of terms identify the relation before values are compared.
    if pattern.predicate != concrete_fact.predicate or len(pattern.terms) != len(
        concrete_fact.terms,
    ):
        return None

    # Each possible match gets its own copy so trying one candidate cannot affect another.
    updated_bindings = dict(bindings or {})
    # Loop through the terms of the pattern and the concrete fact.
    for pattern_term, concrete_term in zip(pattern.terms, concrete_fact.terms, strict=True):
        # Check if the pattern term is a variable. 
        if is_variable(pattern_term):
            existing_value = updated_bindings.get(pattern_term)
            # INVARIANT: A repeated ?s or ?c must still refer to the previously matched value.
            if existing_value is not None and existing_value != concrete_term:
                return None
            updated_bindings[pattern_term] = concrete_term
        # If the pattern term is not a variable, check if it matches the concrete fact.
        elif pattern_term != concrete_term:
            return None
    # Return the updated bindings.
    return updated_bindings
# ---


# --- substitute_fact()
def substitute_fact(pattern: Fact, bindings: dict[str, str]) -> Fact:
    """Build a concrete conclusion from a pattern and its matched variable values.

    Args:
        pattern: Usually a rule conclusion, with the same variable names used in its premises.
        bindings: Variable values collected by a complete premise match.

    Returns:
        A new fact with all variables replaced; existing constant terms retain their values.

    Raises:
        ValueError: If a variable has no binding. The engine cannot invent its value.
    """
    # Substitute the terms of the pattern with the bindings.
    substituted_terms: list[str] = []
    # Loop through the terms of the pattern.
    for term in pattern.terms:
        # Check if the term is a variable. 
        if is_variable(term):
            # Check if the variable is in the bindings.
            if term not in bindings:
                # Raise an error if the variable is not in the bindings. 
                raise ValueError(f"unbound rule variable {term!r}")
            substituted_terms.append(bindings[term])
        else:
            substituted_terms.append(term)
    # Return the new fact.
    return Fact(pattern.predicate, tuple(substituted_terms))
# ---


# --- _match_rule_premises()
def _match_rule_premises(
    rule: HornRule,
    facts: tuple[Fact, ...],
) -> tuple[tuple[dict[str, str], tuple[Fact, ...]], ...]:
    """Find every way that the known facts satisfy all premises of one rule.

    Args:
        rule: Ordered premises that must hold together before its conclusion can be added.
        facts: Current facts in a stable order, used as candidates for each premise.

    Returns:
        Complete matches, each containing its variable bindings and supporting facts. A partial
        match is omitted because one satisfied premise does not establish the whole rule.

    Logic:
        1. Try each fact against the next premise using the bindings already collected.
        2. Continue with each consistent match until all premises have supporting facts.
        3. Retain the complete path so the caller can explain the resulting conclusion.
    """
    matches: list[tuple[dict[str, str], tuple[Fact, ...]]] = []

    # --- match_from()
    def match_from(
        premise_index: int,
        current_bindings: dict[str, str],
        matched_facts: tuple[Fact, ...],
    ) -> None:
        """Extend one possible match to the next premise, retaining only complete paths.

        `premise_index` counts the premises already matched. Each recursive call advances that
        index while carrying the same segment/channel bindings and the evidence used so far.
        """
        # If the premise index is equal to the length of the rule's premises, then add the match.   
        if premise_index == len(rule.premises):
            # Add the match to the list of matches. 
            matches.append((dict(current_bindings), matched_facts))
            return
        # Get the current premise. 
        premise = rule.premises[premise_index]
        # Backtracking tries other candidates when a later premise cannot use the same bindings.
        # Loop through the facts.
        for candidate_fact in facts:
            # Update the bindings with the current fact.
            updated_bindings = unify_fact(premise, candidate_fact, current_bindings)
            # If the updated bindings are not None, then add the match.
            if updated_bindings is not None:
                # Recurse with the next premise index, updated bindings, and matched facts.
                match_from(
                    premise_index + 1,
                    updated_bindings,
                    (*matched_facts, candidate_fact),
                )
    # ---

    match_from(0, {}, ())
    return tuple(matches)
# ---


# __________________________________________
# NUMERICAL-EVIDENCE FACT DERIVATION
# ==========================================


# --- derive_initial_facts()
def derive_initial_facts(
    *,
    segment_id: str,
    channel: str,
    x_raw_telemetry_features: np.ndarray,
    trained_model: TrainedTelemetryModel,
    classification: ClassificationResult,
    similarity: SimilarityResult,
    config: AppConfig = DEFAULT_CONFIG,
) -> tuple[tuple[Fact, ...], tuple[str, ...]]:
    """Assert facts only when the current numerical or historical evidence meets its rule.

    Args:
        segment_id: Identity shared by the selected segment's facts and final result.
        channel: Source channel ID used to look up the configured educational knowledge.
        x_raw_telemetry_features: Selected segment's 18 raw features in the fitted feature order.
        trained_model: Fitted state containing the normal-training means and standard deviations.
        classification: Stored probability and decision route, including the uncertainty result.
        similarity: Reviewed cases, class support, and any classifier/history conflict.
        config: Separate thresholds for an anomaly fact and for a large feature deviation.

    Returns:
        Sorted asserted facts and up to three feature names with the largest qualifying
        deviations. The full probability and historical comparisons remain in their own results.

    Related Equation:
        `absolute_z[j] = abs((raw_feature[j] - normal_mean[j]) / normal_std[j])`

    Equation Relationship:
        This function measures departure from normal training examples, then compares the result
        with a configured cutoff. These statistics differ from the scaler fitted on all training
        rows for the MLP and similarity search.
    """
    asserted_facts: set[Fact] = set()

    # __________________________________________
    # CLASSIFIER FACTS
    # ==========================================
    # PHASE 1: Translate the classifier route using the separate logic assertion threshold.
    # Uncertainty takes precedence, so a near-threshold probability cannot also assert Anomalous.
    if classification.decision_state.value == "uncertain": # If the classifier route is uncertain, add the fact. 
        asserted_facts.add(Fact("Uncertain", (segment_id,)))
    elif classification.anomaly_probability >= config.anomaly_fact_threshold: # If the anomaly probability is greater than the threshold, then add the fact. 
        asserted_facts.add(Fact("Anomalous", (segment_id,)))
    elif classification.decision_state.value == "normal": # If the classifier route is normal, then add the fact. 
        asserted_facts.add(Fact("Normal", (segment_id,)))
    # Else (the anomaly probability is less than the threshold and the classifier route is not uncertain or normal), add the fact. 
    else:
        # The classifier route is anomalous, but the distinct logic assertion gate was not met.
        asserted_facts.add(Fact("InsufficientEvidence", (segment_id,)))

    # __________________________________________
    # NORMAL-REFERENCE DEVIATIONS
    # ==========================================
    # PHASE 2: Measure distance from each feature's normal-training mean in standard deviations.
    # Absolute values treat unusually high and unusually low features as possible deviations.
    # Convert the raw telemetry features to a numpy array and calculate the z-scores.
    normal_zscores = np.abs(
        (
            np.asarray(x_raw_telemetry_features, dtype=np.float64)
            - trained_model.mu_training_normal_feature_means
        )
        / trained_model.sigma_training_normal_feature_stds,
    )
    # Get the indices of the features that deviate from the mean.
    deviating_indices = [
        index
        for index, zscore in enumerate(normal_zscores)
        if zscore >= config.deviation_zscore_threshold
    ]
    # Keep three names for explanation; any qualifying feature is enough to assert Deviates.
    # Feature-name ordering settles equal deviations without depending on set iteration order.
    # Sort the deviating indices by the z-score in descending order and take the top 3.
    top_deviating_indices = sorted(
        deviating_indices,
        key=lambda index: (-float(normal_zscores[index]), trained_model.feature_names[index]),
    )[:3]
    # Get the names of the top deviating features.
    top_deviating_features = tuple(
        trained_model.feature_names[index] for index in top_deviating_indices
    )
    # If there are any deviating indices, then add the fact.
    if deviating_indices:
        asserted_facts.add(Fact("Deviates", (segment_id, channel)))

    # __________________________________________
    # SIMULATED CHANNEL ASSUMPTIONS
    # ==========================================
    # PHASE 3: Add the selected channel's configured teaching assumptions, when a mapping exists.
    # A source channel identifier alone does not establish a real subsystem fault or limit.
    # Find the channel knowledge for the current channel.
    channel_knowledge = next(
        (knowledge for knowledge in CHANNEL_KNOWLEDGE if knowledge.channel == channel),
        None,
    )
    # If the channel knowledge is not None, then add the fact.
    if channel_knowledge is not None:
        asserted_facts.add(
            Fact("FaultMapping", (channel, channel_knowledge.fault_name)),
        )
        # If the channel knowledge is critical, then add the fact.
        if channel_knowledge.critical:
            asserted_facts.add(Fact("Critical", (channel,)))

    # __________________________________________
    # HISTORICAL EVIDENCE FACTS
    # ==========================================
    # PHASE 4: Preserve the retrieved case identities and labels as inspectable evidence facts.
    # Loop through the similar cases.
    for similar_case in (*similarity.normal_cases, *similarity.anomalous_cases):
        # Add the similar case to the set of facts.
        asserted_facts.add(Fact("SimilarTo", (segment_id, similar_case.case_id)))
        # Add the reviewed label to the set of facts.
        asserted_facts.add(
            Fact("ReviewedLabel", (similar_case.case_id, similar_case.reviewed_label)),
        )
    # If the historical support is not None, then add the fact.
    if similarity.historical_support is not None:
        asserted_facts.add(
            Fact("HistoricalSupports", (segment_id, similarity.historical_support)),
        )
    # If the classifier conflict is true, then add the fact.
    if similarity.classifier_conflict:
        asserted_facts.add(Fact("ConflictingEvidence", (segment_id,)))
    # A comparison needs examples from both classes; absence is recorded as missing evidence.
    if not similarity.normal_cases or not similarity.anomalous_cases:
        asserted_facts.add(Fact("InsufficientEvidence", (segment_id,)))
    

    return tuple(sorted(asserted_facts)), top_deviating_features
# ---


# __________________________________________
# FORWARD CHAINING AND CONSISTENCY
# ==========================================


# --- _find_consistency_conflicts()
def _find_consistency_conflicts(facts: set[Fact]) -> tuple[InferenceTrace, ...]:
    """Describe contradictory facts that need human review.

    The consistency policy flags Normal and Anomalous for the same segment, or more than one
    simulated fault hypothesis for that segment. It preserves the original facts so the conflict
    remains visible instead of choosing a diagnosis on the user's behalf.

    Args: 
        facts: A set of facts.

    Returns:
        Traces proposing new ConflictingEvidence facts. The caller decides whether to add them
        to the fact set, which this function only reads.
    """
    # Initialize an empty list to store the traces.
    traces: list[InferenceTrace] = []
    # Get the normal segments from the facts.
    normal_segments = {fact.terms[0] for fact in facts if fact.predicate == "Normal"}
    # Get the anomalous segments from the facts.
    anomalous_segments = {fact.terms[0] for fact in facts if fact.predicate == "Anomalous"}
    # Loop through the normal and anomalous segments.
    for segment_id in sorted(normal_segments & anomalous_segments):
        # Create a new fact for the conclusion.
        conclusion = Fact("ConflictingEvidence", (segment_id,))
        # If the conclusion is not in the facts, then add the fact.
        if conclusion not in facts:
            traces.append(
                # InferenceTrace: Rule ID, Matched Premises, Bindings, Conclusion, Explanation, Source Status 
                InferenceTrace(
                    rule_id="CONSISTENCY-001-CLASSIFICATION", # Rule ID: The ID of the rule that was matched.
                    matched_premises=(
                        Fact("Normal", (segment_id,)),
                        Fact("Anomalous", (segment_id,)),
                    ),
                    # Bindings for the rule. 
                    bindings=(("?s", segment_id),),
                    # Conclusion of the rule.
                    conclusion=conclusion,
                    # Explanation of the rule.
                    explanation="Mutually exclusive classification facts were both present.",
                    # Source status of the rule.
                    source_status="simulated consistency check",
                ),
            )
    # Get the faults by segment from the facts.
    faults_by_segment: dict[str, set[str]] = defaultdict(set)
    # Loop through the facts to find the faults.
    for fact in facts:
        # If the fact is a suspected fault and has two terms, then add the fact.
        if fact.predicate == "SuspectedFault" and len(fact.terms) == 2:
            faults_by_segment[fact.terms[0]].add(fact.terms[1])
    # Loop through the faults by segment.
    for segment_id, fault_names in sorted(faults_by_segment.items()):
        # If the fault names are more than one, then add the fact.
        if len(fault_names) > 1:
            # Create a new fact for the conclusion.
            conclusion = Fact("ConflictingEvidence", (segment_id,))
            # If the conclusion is not in the facts, then add the fact.
            if conclusion not in facts:
                # Get the matched facts.
                matched = tuple(
                    Fact("SuspectedFault", (segment_id, fault_name))
                    for fault_name in sorted(fault_names)
                )
                traces.append(
                    # InferenceTrace: Rule ID, Matched Premises, Bindings, Conclusion, Explanation, Source Status 
                    InferenceTrace(
                        rule_id="CONSISTENCY-002-FAULT-HYPOTHESES", # Rule ID: The ID of the rule that was matched.
                        matched_premises=matched, # Matched premises for the rule.
                        bindings=(("?s", segment_id),), # Bindings for the rule.
                        conclusion=conclusion, # Conclusion of the rule.
                        explanation="Mutually exclusive simulated fault hypotheses need review.", # Explanation of the rule.
                        source_status="simulated consistency check",
                    ),
                )
    return tuple(traces)
# ---


# --- exists_critical_deviation()
def exists_critical_deviation(facts: tuple[Fact, ...], segment_id: str) -> bool:
    """Return whether at least one critical channel deviates for this segment.

    This is the existential query `exists c: Critical(c) AND Deviates(segment_id, c)`.
    The intersection supplies the shared channel value; unrelated channels cannot satisfy it.   
    
    Args:
        facts: A tuple of facts.
        segment_id: The ID of the segment.

    Returns:
        True if at least one critical channel deviates for this segment, False otherwise.
    """
    # Get the critical channels from the facts.
    critical_channels = {fact.terms[0] for fact in facts if fact.predicate == "Critical"}
    # Get the deviating channels from the facts.
    deviating_channels = {
        fact.terms[1]
        for fact in facts
        if fact.predicate == "Deviates" and fact.terms[0] == segment_id
    }
    return bool(critical_channels & deviating_channels)
# ---


# --- run_forward_chaining()
def run_forward_chaining(
    asserted_facts: tuple[Fact, ...],
    *,
    selected_segment_id: str,
    rules: tuple[HornRule, ...] | None = None,
) -> ReasoningResult:
    """Derive review requirements until another pass adds no facts.

    Args:
        asserted_facts: Evidence facts supplied before rule inference begins.
        selected_segment_id: Segment whose hypotheses, checks, and review reasons are returned.
        rules: Optional rule tuple; `None` uses the built-in educational catalog.

    Returns:
        Original facts, newly derived facts, and the first recorded derivation of each new fact.
        The complete fact store is retained, while advisory result fields concern the selected
        segment. No fact is removed or strengthened into a confirmed diagnosis.

    Raises:
        ValueError: If a supplied rule conclusion contains a variable its premises did not bind.

    Logic:
        1. Record consistency conflicts and try rules against the current ordered facts.
        2. Add each previously unknown conclusion with its premises and variable bindings.
        3. Repeat until a full pass makes no change, then collect the selected segment's results.
    """
    # __________________________________________
    # FACT AND TRACE INITIALIZATION
    # ==========================================
    # Keep the supplied evidence distinct from conclusions added by the chosen rule catalog.
    # If rules are provided, use them; otherwise, build the horn rules.
    selected_rules = rules if rules is not None else build_horn_rules()
    # Create a set of facts from the asserted facts.
    fact_set = set(asserted_facts)
    # Create a set of asserted facts.
    asserted_set = set(asserted_facts)
    # Create a list of traces.
    traces: list[InferenceTrace] = []

    # __________________________________________
    # FIXED-POINT DERIVATION
    # ==========================================
    # Consistency checks and rule applications share each pass through the growing fact store.
    # MAIN ITERATION LOOP: Add only previously unknown conclusions until no rule changes the store.
    while True:
        changed = False
        # Check contradictions first so the ordinary manual-review rule can use them this pass.
        consistency_traces = _find_consistency_conflicts(fact_set)
        # Loop through the consistency traces.
        for consistency_trace in consistency_traces:
            # If the conclusion is not in the fact set, then add it.
            if consistency_trace.conclusion not in fact_set:
                fact_set.add(consistency_trace.conclusion)
                traces.append(consistency_trace)
                changed = True

        # Stable fact and rule order makes the evidence trace repeatable for the same input.
        ordered_facts = tuple(sorted(fact_set))
        # Loop through the rules.
        for rule in selected_rules:
            # Loop through the bindings and matched premises.
            for bindings, matched_premises in _match_rule_premises(rule, ordered_facts):
                # Substitute the rule's conclusion with the bindings.
                conclusion = substitute_fact(rule.conclusion, bindings)
                # If the conclusion is already in the fact set, then continue.
                if conclusion in fact_set:
                    continue
                # Add the conclusion to the fact set.
                fact_set.add(conclusion)
                # Add the trace to the list of traces.
                traces.append(
                    # InferenceTrace: Rule ID, Matched Premises, Bindings, Conclusion, Explanation, Source Status 
                    InferenceTrace(
                        rule_id=rule.rule_id, # Rule ID: The ID of the rule that was matched.
                        matched_premises=matched_premises, # Matched premises for the rule.
                        bindings=tuple(sorted(bindings.items())), # Bindings for the rule.
                        conclusion=conclusion, # Conclusion: The conclusion that was reached.   
                        explanation=rule.explanation, # Explanation: The explanation for the conclusion.
                        source_status=rule.source_status, # Source status: The status of the source.
                    ),
                )
                changed = True
                # Later rules can use this conclusion; earlier rules see it on the next pass.
                ordered_facts = tuple(sorted(fact_set))
        # If no changes were made in this pass, then break the loop.
        if not changed:
            break

    # __________________________________________
    # SELECTED-SEGMENT REASONING RESULT
    # ==========================================
    # Collect this segment's review requirements while retaining the full derivation evidence.
    # Separate supplied evidence from conclusions without losing either part of the explanation.
    # Get all the facts.
    all_facts = tuple(sorted(fact_set))
    # Get the derived facts.
    derived_facts = tuple(sorted(fact_set - asserted_set))
    # Get the suspected faults.
    suspected_faults = tuple(
        sorted(
            fact.terms[1]
            for fact in fact_set
            if fact.predicate == "SuspectedFault" and fact.terms[0] == selected_segment_id
        ),
    )
    # Get the required checks for the selected segment.
    required_checks = tuple(
        sorted(
            fact.terms[1]
            for fact in fact_set
            if fact.predicate == "RequiresCheck" and fact.terms[0] == selected_segment_id
        ),
    )

    # Report the evidence condition behind human review, in the same order on repeated runs.
    # Initialize an empty list to store the manual review reasons.
    manual_review_reasons: list[str] = []
    # Check if there is conflicting evidence.
    if Fact("ConflictingEvidence", (selected_segment_id,)) in fact_set:
        manual_review_reasons.append("conflicting evidence")
    # Check if there is insufficient evidence.
    if Fact("InsufficientEvidence", (selected_segment_id,)) in fact_set:
        manual_review_reasons.append("insufficient evidence")
    # Check if the probability is within the uncertainty band.
    if Fact("Uncertain", (selected_segment_id,)) in fact_set:
        manual_review_reasons.append("probability within the uncertainty band")
    # Check if a reasoning rule requires manual review.
    if (
        Fact("ManualReviewRequired", (selected_segment_id,)) in fact_set
        and not manual_review_reasons
    ):
        manual_review_reasons.append("a reasoning rule requires manual review")
    # Return the reasoning result.
    return ReasoningResult(
        asserted_facts=tuple(sorted(asserted_set)), # Asserted facts for the selected segment.
        derived_facts=derived_facts, # Derived facts for the selected segment.
        all_facts=all_facts, # All facts for the selected segment.
        traces=tuple(traces), # Traces for the selected segment.
        suspected_faults=suspected_faults, # Suspected faults for the selected segment.
        required_checks=required_checks, # Required checks for the selected segment.
        manual_review_reasons=tuple(manual_review_reasons), # Manual review reasons for the selected segment.
        existential_critical_deviation=exists_critical_deviation(
            all_facts,
            selected_segment_id,
        ), # Existential critical deviation for the selected segment.
    )
# ---


# __________________________________________
# END OF FILE
# ==========================================

