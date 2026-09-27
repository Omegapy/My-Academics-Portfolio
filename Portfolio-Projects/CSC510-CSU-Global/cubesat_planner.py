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
# - Implement deterministic A-star search with nonnegative simulated action costs.
# - Validate every transition and final diagnostic stopping condition.
#
# Module Purpose:
# - Convert derived checks and uncertainty into a low-cost advisory investigation sequence.
# - Return normal no-plan and unavailable-plan outcomes without executing real actions.
#
# Usage / Integration:
# - Called by the coordinator after forward chaining; returns a structured plan result.
#
# Contents Overview:
# - Action catalog, state construction, conservative heuristic, A-star search, and validation.
#
# Dependencies:
# - Standard Library: heapq, itertools
# - Third-Party: None
# - Local Project: cubesat_types
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Order simulated review steps with A-star graph search.

The reasoning result identifies what needs review. The planner represents each possible stage of
that review as a state containing required and completed checks. An action has preconditions that
must already hold, effects that mark checks complete, and a simulated effort cost.

A-star keeps a frontier of candidate states and chooses the next one by `f(n) = g(n) + h(n)`.
`g(n)` is the cost accumulated so far; the heuristic `h(n)` estimates what remains. The built-in
catalog gives each action one distinct check effect, which makes its remaining-cost estimate a
lower bound. That reasoning does not automatically apply to a replacement catalog with combined
effects. The result is an advisory sequence for a person to inspect; no listed action is executed.
"""

# ____________________________________________________________________________________
# ====================================================================================
#
# A-STAR STATE AND COST MAP
#
# state = (route, triggered requirements, required checks, completed checks, hypotheses)
# g(n) = accumulated nonnegative simulated cost
# h(n) = sum of minimum costs for still-incomplete mandatory checks
# f(n) = g(n) + h(n)
#
# Built-in prerequisite order:
# probability review -> historical review -> critical deviation -> fault mapping
#                                      \-> manual review
#
# Each built-in action produces one distinct check effect, so adding the cost for each
# missing check does not count a shared action twice. The resulting h(n) cannot exceed the
# remaining cost in this catalog. Completing one effect reduces h by at most that action's
# cost, which is the consistency condition h(n) <= cost(n, next) + h(next).
#
# Completed checks only accumulate. The finite action catalog therefore gives this search
# a finite set of states, including separate orders that may reach the same completed set.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

import heapq # Import heapq for heap queue algorithm.
import itertools # Import itertools for iterator functions.

from cubesat_types import (
    ClassificationResult, # Import classification result.
    DiagnosticAction, # Import diagnostic action.
    PlannedAction, # Import planned action.
    PlanningError, # Import planning error.
    PlanningState, # Import planning state.
    PlanResult, # Import plan result.
    PlanStatus, # Import plan status.
    ReasoningResult, # Import reasoning result.
)

# __________________________________________
# ACTION CATALOG
# ==========================================


# The catalog defines available simulated transitions; the state helpers below decide
# which check effects the current classification and reasoning require.
# --- build_diagnostic_actions()
def build_diagnostic_actions() -> tuple[DiagnosticAction, ...]:
    """Return the five educational review actions and their prerequisite relationships.

    Costs 1, 1, 2, 2, and 1 represent relative simulated effort, not measured time or money.
    Each effect names a check that becomes complete after the action. Preconditions keep the
    proposed review in a meaningful order, such as examining historical evidence before a fault
    mapping. Returning these records does not carry out the reviews.

    Args:
        None.
    
    Returns:
        tuple[DiagnosticAction, ...]: Tuple of diagnostic actions.
    """
    return (
        # Probability review action.
        DiagnosticAction(
            action_id="ACTION-001-REVIEW-PROBABILITY",
            description="Review the model probability and validation-selected threshold.",
            preconditions=frozenset(),
            effects=frozenset({"probability_reviewed"}),
            cost=1.0,
            cost_meaning="one simulated unit of operator review effort",
            category="evidence gathering",
        ),
        # Historical cases review action.
        DiagnosticAction(
            action_id="ACTION-002-INSPECT-HISTORICAL-CASES",
            description="Inspect class-aware normal and anomalous historical cases.",
            preconditions=frozenset({"probability_reviewed"}),
            effects=frozenset({"historical_cases_reviewed"}),
            cost=1.0,
            cost_meaning="one simulated unit of comparison effort",
            category="evidence gathering",
        ),
        # Critical deviation review action.
        DiagnosticAction(
            action_id="ACTION-003-INSPECT-CRITICAL-DEVIATION",
            description="Inspect the critical channel deviation and its contributing features.",
            preconditions=frozenset({"historical_cases_reviewed"}),
            effects=frozenset({"critical_deviation_reviewed"}),
            cost=2.0,
            cost_meaning="two simulated units of technical review effort",
            category="diagnostic check",
        ),
        # Fault mapping review action.
        DiagnosticAction(
            action_id="ACTION-004-REVIEW-FAULT-MAPPING",
            description="Review the simulated channel-to-fault hypothesis mapping.",
            preconditions=frozenset({"critical_deviation_reviewed"}),
            effects=frozenset({"fault_mapping_reviewed"}),
            cost=2.0,
            cost_meaning="two simulated units of expert-system review effort",
            category="diagnostic check",
        ),
        # Manual review escalation action.
        DiagnosticAction(
            action_id="ACTION-005-ESCALATE-MANUAL-REVIEW",
            description="Escalate the evidence package for final human interpretation.",
            preconditions=frozenset({"historical_cases_reviewed"}),
            effects=frozenset({"manual_review_escalated"}),
            cost=1.0,
            cost_meaning="one simulated unit of operator escalation effort",
            category="manual review",
        ),
    )
# ---


# __________________________________________
# STATE, GOAL, AND HEURISTIC
# ==========================================


# These helpers turn evidence into a goal and estimate the effort of remaining simulated checks.
# --- build_initial_planning_state()
def build_initial_planning_state(
    classification: ClassificationResult,
    reasoning: ReasoningResult,
) -> PlanningState:
    """Translate the classification and reasoning results into mandatory review checks.

    Args:
        classification: Stored normal, anomalous, or uncertain decision route.
        reasoning: Derived check requests, critical-deviation evidence, simulated hypotheses,
            and reasons for human review.

    Returns:
        An initial state with no completed checks. Frozen sets make states suitable dictionary
        keys, so search can recognize when different action orders reach the same state.

    Logic:
        1. Retain the evidence conditions that triggered planning.
        2. Translate those conditions into the action catalog's check-effect names.
        3. Give manual review priority when reasoning reports uncertainty or conflicting evidence.
    """
    # Triggered requirements explain why planning began; required checks define its stopping goal.
    triggered_requirements: set[str] = set(reasoning.required_checks)
    # Add critical deviation requirement if existential critical deviation exists.
    if reasoning.existential_critical_deviation:
        triggered_requirements.add("critical_deviation")
    # Add manual review requirement if manual review reasons exist.
    if reasoning.manual_review_reasons:
        triggered_requirements.add("manual_review")
    # Add fault hypothesis requirement if suspected faults exist.
    if reasoning.suspected_faults:
        triggered_requirements.add("fault_hypothesis")

    # Determine required checks based on classification decision state.
    required_checks: set[str] = set()
    # Even a normal classification needs evidence review when symbolic reasoning raises a check.
    if classification.decision_state.value != "normal" or triggered_requirements:
        required_checks.update({"probability_reviewed", "historical_cases_reviewed"})
    # Channel-specific RequiresCheck values map to the critical-deviation review action.
    # The two named evidence reviews have their own meaning and are excluded from this mapping.
    # Add critical deviation review requirement if existential critical deviation exists.
    # Add fault mapping review requirement if fault mapping review exists.
    # Add manual review escalation requirement if manual review reasons exist.
    # Add historical evidence review requirement if historical evidence review exists.
    # Add probability review requirement if probability review exists.
    if reasoning.existential_critical_deviation or any(
        check not in {"historical_evidence_review", "fault_mapping_review"}
        for check in reasoning.required_checks
    ):
        required_checks.add("critical_deviation_reviewed")
    # Add fault mapping review requirement if fault mapping review exists.
    # Add fault mapping review requirement if fault mapping review exists.
    if reasoning.suspected_faults or "fault_mapping_review" in reasoning.required_checks:
        required_checks.add("fault_mapping_reviewed")
    # Add manual review escalation requirement if manual review reasons exist.
    if reasoning.manual_review_reasons:
        required_checks.add("manual_review_escalated")

    # Set the route based on classification decision state.
    route = classification.decision_state.value
    # Set the route to manual review if manual review reasons exist.
    if reasoning.manual_review_reasons:
        route = "manual_review"

    # Return the initial state with the determined route, triggered requirements, 
    # required checks, completed checks, and suspected faults.
    return PlanningState(
        route=route, # Determine the route based on classification decision state.  
        triggered_requirements=frozenset(triggered_requirements), # Set the triggered requirements.
        required_checks=frozenset(required_checks), # Set the required checks.
        completed_checks=frozenset(), # Set the completed checks.
        suspected_faults=frozenset(reasoning.suspected_faults), # Set the suspected faults.
    )
# ---


# --- goal_is_satisfied()
def goal_is_satisfied(state: PlanningState) -> bool:
    """Return whether completed checks include every required check; extra checks are allowed.

    Args:
        state: Current required and completed check sets.

    Returns:
        True if all required checks are completed, False otherwise.
    """
    return state.required_checks <= state.completed_checks
# ---


# --- estimate_remaining_cost()
def estimate_remaining_cost(
    state: PlanningState,
    actions: tuple[DiagnosticAction, ...],
) -> float:
    """Add the cheapest action cost for each mandatory check that remains incomplete.

    Args:
        state: Current required and completed check sets.
        actions: Catalog searched for an action that can produce each missing effect.

    Returns:
        The remaining-cost estimate `h(n)`. A check with no producer adds nothing here; the
        planner's separate availability check detects missing required effects before search.

    Related Equation:
        `h(n) = sum(min(cost of actions producing check) for each incomplete required check)`

    Equation Relationship:
        This evaluates the heuristic without enforcing action preconditions. For the built-in
        single-effect catalog it is a lower bound on remaining cost. An optional action that
        completes several required checks could be counted more than once, so this guarantee
        must be reassessed for a different catalog.
    """
    # Identify remaining checks by taking the difference between required and completed checks.
    remaining_checks = state.required_checks - state.completed_checks
    # Initialize estimated cost to zero.
    estimated_cost = 0.0
    # Iterate through remaining checks in sorted order.
    for required_check in sorted(remaining_checks):
        # Find all actions that produce the current required check.
        producing_costs = [
            action.cost for action in actions if required_check in action.effects
        ]
        # Add the minimum cost of producing actions to the estimated cost.
        if producing_costs:
            estimated_cost += min(producing_costs)
    # Return the estimated cost.
    return estimated_cost
# ---


# __________________________________________
# PLAN VALIDATION
# ==========================================


# --- validate_action_catalog()
def validate_action_catalog(actions: tuple[DiagnosticAction, ...]) -> None:
    """Reject duplicate identifiers, negative costs, and actions with no effects.

    These checks catch three malformed catalog conditions before state search begins. They do
    not restrict actions to one effect or prove that the heuristic fits a replacement catalog.

    Args:
        actions: Tuple of DiagnosticAction objects.
    
    Raises:
        PlanningError: If any action identifier repeats, cost is negative, or effect set is empty.
    """
    # Get all action identifiers.
    action_ids = [action.action_id for action in actions]
    # Check for duplicate action identifiers.
    if len(action_ids) != len(set(action_ids)):
        # Raise PlanningError if any action identifier repeats.
        raise PlanningError("diagnostic action identifiers must be unique")
    # Iterate through all actions.
    for action in actions:
        # Check for negative costs.
        if action.cost < 0.0:
            # Raise PlanningError if any action has a negative cost.
            raise PlanningError(f"diagnostic action {action.action_id} has a negative cost")
        # Check for no effects.
        if not action.effects:
            # Raise PlanningError if any action has no effect.
            raise PlanningError(f"diagnostic action {action.action_id} has no effect")
# ---


# --- validate_plan_transitions()
def validate_plan_transitions(
    initial_state: PlanningState,
    planned_actions: tuple[PlannedAction, ...],
) -> tuple[bool, PlanningState]:
    """Replay a proposed sequence to check its transitions and recorded cumulative costs.

    Args:
        initial_state: State before any action in this sequence has been applied.
        planned_actions: Ordered actions carrying the cost recorded after each step.

    Returns:
        A validity flag and the last state reached before a failure, or the replayed final state.
        Valid transitions do not alone establish goal satisfaction; the caller checks that the
        final completed set includes every mandatory check.

    Logic:
        1. Require nonnegative cost and already completed preconditions at each step.
        2. Recalculate cumulative cost and compare it with the recorded value within `1e-9`.
        3. Add the action's effects while preserving the original route and review requirements.
    """
    # Initialize the current state to the initial state.
    current_state = initial_state
    # Initialize the accumulated cost to zero.
    accumulated_cost = 0.0
    # Iterate through the planned actions.
    for planned_action in planned_actions:
        # Get the action from the planned action.
        action = planned_action.action
        # Check for negative costs or unmet preconditions.
        if action.cost < 0.0 or not action.preconditions <= current_state.completed_checks:
            # Return False and the current state if the action has a negative cost or unmet preconditions.
            return False, current_state
        # Accumulate the cost.
        accumulated_cost += action.cost
        # Check for cumulative cost mismatch.
        if abs(accumulated_cost - planned_action.cumulative_cost) > 1e-9:
            # Return False and the current state if the cumulative cost does not match.
            return False, current_state
        # Update the current state with the action's effects.
        current_state = PlanningState(
            route=current_state.route,
            triggered_requirements=current_state.triggered_requirements,
            required_checks=current_state.required_checks,
            completed_checks=current_state.completed_checks | action.effects,
            suspected_faults=current_state.suspected_faults,
        )
    # Return True and the final state if all checks pass.  
    return True, current_state
# ---


# __________________________________________
# A-STAR GRAPH SEARCH
# ==========================================


# --- plan_diagnostic_checks()
def plan_diagnostic_checks(
    classification: ClassificationResult,
    reasoning: ReasoningResult,
    *,
    actions: tuple[DiagnosticAction, ...] | None = None,
) -> PlanResult:
    """Search for an advisory sequence that completes the required simulated checks.

    Args:
        classification: Current decision route used to construct the initial state.
        reasoning: Evidence conditions and review requirements derived by the expert system.
        actions: Optional replacement catalog; `None` selects the built-in five-action catalog.

    Returns:
        A found plan, a normal route that needs no plan, or a controlled unavailable result.
        Found plans include ordered actions, cumulative effort, and separate transition/goal
        checks. The built-in catalog supports the least-cost guarantee described below.

    Related Equations:
        `g(n) = accumulated action cost`
        `h(n) = sum of minimum costs for incomplete mandatory effects`
        `f(n) = g(n) + h(n)`

    Equation Relationship:
        This function calculates A-star priorities and applies effects to simulated states.
        Its lower-bound heuristic supports least-cost search for the built-in single-effect
        catalog. Actions are eligible only when they add an incomplete required check, so this
        is a bounded review planner rather than a general planner for arbitrary prerequisites.

    Raises:
        PlanningError: If the selected catalog fails identifier, cost, or effect validation.

    Logic:
        1. Build the required-check goal and handle no-plan or missing-effect cases.
        2. Expand the cheapest estimated frontier entry and retain cheaper arrivals at each state.
        3. Stop at a satisfied goal, then replay the sequence to check the recorded transitions.
    """
    # __________________________________________
    # CATALOG AND GOAL PREPARATION
    # ==========================================
    # Construct the simulated planning problem from the selected segment's existing results.
    # Select actions, using the built-in catalog if none are provided.
    selected_actions = actions if actions is not None else build_diagnostic_actions()
    # Validate the action catalog.
    validate_action_catalog(selected_actions)
    # Build the initial state.
    initial_state = build_initial_planning_state(classification, reasoning)
    # Build the goal description.
    goal_description = (
        "complete all mandatory simulated checks: "
        + ", ".join(sorted(initial_state.required_checks))
    )

    # __________________________________________
    # INITIAL PLANNING OUTCOMES
    # ==========================================
    # Resolve an empty goal or a missing check producer before allocating the search frontier.
    # A goal with no required checks is already complete and needs no search or action cost.
    if not initial_state.required_checks:
        # Return a normal route plan result.
        return PlanResult(
            status=PlanStatus.NOT_REQUIRED, # Status indicating that no plan is required.
            ordered_actions=(), # No ordered actions are required.
            total_cost=0.0, # Total cost is zero.
            goal_condition="no diagnostic checks are required for the current normal route", # Goal condition is that no diagnostic checks are required.
            initial_state=initial_state, # Initial state is the initial state.
            final_state=initial_state, # Final state is the initial state.
            expanded_node_count=0, # Zero nodes were expanded.
            transitions_valid=True, # Transitions are valid.
            goal_satisfied=True, # Goal is satisfied.
            message="Routine monitoring; no further simulated diagnostic action is required.", # Message indicating that no further simulated diagnostic action is required.
        )

    # Catch a missing check producer before search. Preconditions may still make a listed effect
    # unreachable, which is handled later if the frontier is exhausted.
    producible_effects = frozenset().union(
        *(action.effects for action in selected_actions),
    )

    if not initial_state.required_checks <= producible_effects:
        # Calculate the missing effects.
        missing_effects = sorted(initial_state.required_checks - producible_effects)
        # Return an unavailable plan result.
        return PlanResult(
            status=PlanStatus.UNAVAILABLE, # Status indicating that the plan is unavailable.
            ordered_actions=(), # No ordered actions are required.
            total_cost=0.0, # Total cost is zero.
            goal_condition=goal_description, # Goal condition is that no diagnostic checks are required.
            initial_state=initial_state, # Initial state is the initial state.
            final_state=initial_state, # Final state is the initial state.
            expanded_node_count=0, # Zero nodes were expanded.
            transitions_valid=True, # Transitions are valid.
            goal_satisfied=False, # Goal is not satisfied.
            message=(
                "No valid simulated plan can produce required checks: "
                + ", ".join(missing_effects)
                + ". Manual review is required."
            ), # Message indicating that no valid simulated plan can produce the required checks.
        )

    # __________________________________________
    # FRONTIER SETUP
    # ==========================================
    # Frontier = candidate states still waiting for expansion. The first tuple fields order them
    # by f, then g, then action-ID path. A counter settles any remaining tie before Python reaches
    # the PlanningState object, which has no ordering operation.
    counter = itertools.count() # Counter for tie-breaking.
    frontier: list[
        tuple[
            float, # f, the estimated total cost (h + g).
            float, # g, the accumulated action cost.
            tuple[str, ...], # Action-ID path taken to reach this state.
            int, # Counter for tie-breaking.
            PlanningState, # The current state.
            tuple[PlannedAction, ...], # The sequence of actions taken to reach this state.
        ]
    ] = []
    # Calculate the initial heuristic cost.
    initial_h = estimate_remaining_cost(initial_state, selected_actions)
    # Push the initial state onto the frontier.
    heapq.heappush(frontier, (initial_h, 0.0, (), next(counter), initial_state, ()))
    # Different action orders can reach the same completed-check set. Keep the cheapest arrival.
    best_cost_by_state: dict[PlanningState, float] = {initial_state: 0.0}
    expanded_node_count = 0

    # __________________________________________
    # SIMULATED SEARCH EXPANSION
    # ==========================================
    # Search candidate check sequences and replay a found path before returning it for review.
    # MAIN ITERATION LOOP: Expand the lowest `(f, g, action-id path)` frontier entry.
    while frontier:
        _, g_n_accumulated_path_cost, action_id_path, _, state, planned_actions = heapq.heappop(
            frontier,
        )
        # An older frontier entry may remain after a cheaper route to its state was discovered.
        if g_n_accumulated_path_cost > best_cost_by_state.get(state, float("inf")) + 1e-12:
            continue
        # Check if the goal is satisfied.
        if goal_is_satisfied(state):
            # Replaying checks the proposed steps independently of the state stored in the queue.
            transitions_valid, replayed_final_state = validate_plan_transitions(
                initial_state,
                planned_actions,
            )
            # Check if the goal is satisfied after replaying the transitions.
            goal_satisfied = goal_is_satisfied(replayed_final_state)
            return PlanResult(
                status=PlanStatus.FOUND, # Status indicating that the plan was found.
                ordered_actions=planned_actions, # The sequence of actions taken to reach the goal.
                total_cost=g_n_accumulated_path_cost, # The total cost of the plan.
                goal_condition=goal_description, # The goal condition.
                initial_state=initial_state, # The initial state.
                final_state=replayed_final_state, # The final state.
                expanded_node_count=expanded_node_count, # The number of nodes expanded.
                transitions_valid=transitions_valid, # Whether the transitions are valid.
                goal_satisfied=goal_satisfied, # Whether the goal is satisfied.
                message="Least-cost simulated advisory investigation sequence found.", # Message indicating that the plan was found.
            )
        
        # Increment the number of expanded nodes.
        expanded_node_count += 1
        # Iterate over the sorted selected actions.
        for action in sorted(selected_actions, key=lambda candidate: candidate.action_id):
            # Both conditions matter: prerequisites must hold, and the action must advance a goal.
            if not action.preconditions <= state.completed_checks:
                continue
            # Check if the action effects advance a goal.
            if not action.effects & (state.required_checks - state.completed_checks):
                continue
            # Each branch gets a new state; adding effects leaves other candidate paths intact.
            next_state = PlanningState(
                route=state.route, # The route taken to reach this state.
                triggered_requirements=state.triggered_requirements, # The requirements triggered.
                required_checks=state.required_checks, # The checks required.
                completed_checks=state.completed_checks | action.effects, # The checks completed.
                suspected_faults=state.suspected_faults, # The faults suspected.
            )
            # Add the action cost to the accumulated path cost.
            next_g = g_n_accumulated_path_cost + action.cost
            # The tolerance avoids treating negligible floating-point differences as improvements.
            if next_g >= best_cost_by_state.get(next_state, float("inf")) - 1e-12:
                continue
            # Update the best cost for the next state.
            best_cost_by_state[next_state] = next_g
            # Create the next planned action.
            next_planned_actions = (
                *planned_actions,
                PlannedAction(action=action, cumulative_cost=next_g),
            )
            # Create the next action id path.
            next_action_id_path = (*action_id_path, action.action_id)
            # Estimate the remaining cost.
            h_n_estimated_remaining_cost = estimate_remaining_cost(
                next_state,
                selected_actions,
            )
            # g is the effort already spent on this path; h estimates the checks still required.
            f_n_estimated_total_cost = next_g + h_n_estimated_remaining_cost
            # Push the next state onto the frontier.
            heapq.heappush(
                frontier,
                (
                    f_n_estimated_total_cost, # f, the estimated total cost (h + g).
                    next_g, # g, the accumulated action cost.
                    next_action_id_path, # The action-id path taken to reach this state.
                    next(counter), # Counter for tie-breaking.
                    next_state, # The current state.
                    next_planned_actions, # The sequence of actions taken to reach this state.
                ),
            )

    # __________________________________________
    # EXHAUSTED-SEARCH REPORTING
    # ==========================================
    # FALLBACK: All eligible paths were exhausted without satisfying the required-check goal.
    return PlanResult(
        status=PlanStatus.UNAVAILABLE, # Status indicating that the plan is unavailable.
        ordered_actions=(), # No ordered actions are required.
        total_cost=0.0, # Total cost is zero.
        goal_condition=goal_description, # The goal condition.
        initial_state=initial_state, # The initial state.
        final_state=initial_state, # The final state.
        expanded_node_count=expanded_node_count, # The number of nodes expanded.
        transitions_valid=True, # Whether the transitions are valid.
        goal_satisfied=False, # Whether the goal is satisfied.
        message="No valid simulated plan satisfies the goal; manual review is required.", # Message indicating that no valid simulated plan satisfies the goal.
    )
# ---


# __________________________________________
# END OF FILE
# ==========================================
