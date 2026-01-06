# -------------------------------------------------------------------------
# File: atm_operations.py
# Project: ATM State Machine 
# Author: Alexander Samuel Ricciardi
# Date: 2026-01-11
# File Path: Portfolio-Project-Module-7/atm_operations.py
# -------------------------------------------------------------------------
# Course: CSC-505 Principles of Software Development
# Professor: Dr. Joseph Issa  
# Term: Winter A (25WA) – 2025
# -------------------------------------------------------------------------
# Assignment:
# Portfolio Project - Module 8 – ATM State Machine Diagram
#
# Directions:
# Final Project  
# For your final project, 
# you are going to create a UML diagram of your choice 
# (e.g., Sequence, Class, Activity, etc.) 
# for an automated teller machine (ATM). Your diagram should include the 
# following:
# - The customer must pass authentication before withdrawing money.
# - Authentication is performed by checking a PIN.
# - The PIN can be correct or not.
# - Unsuccessful attempts are counted.
# - If the counter exceeds a limit, then the customer is rejected.
# - If the account balance is zero, then the account is closed.
# Write a Python Script that will the steps in sequence the operations 
# at the teller machine (ATM) as shown in your diagram
# -------------------------------------------------------------------------
# Project Description:
# The Python script is a small console application that print all the steps in sequence 
# for all the operations at an automated teller machine (ATM) shown in 
# the "ATM State Machine UML Diagram.png" diagram.
# -------------------------------------------------------------------------

# --- File Contents ---
# TYPES AND DATA STRUCTURES:
#   - Class: Theme (frozen dataclass) - ANSI color theme for ordered-sequence output
#   - Class: Ctx (dataclass) - Runtime execution context for guards/computations
#   - Class: StateActions (frozen dataclass) - State machine state encoding
#   - Class: StepCounter (regular class) - Ordered-sequence step number counter
#   - Type: ScenarioFunction - Callable type alias for scenario functions
#
# GLOBAL CONSTANTS AND CONFIGURATION DATA:
#   - Constant: MAX_TRIES - Maximum PIN attempts before card rejection
#   - Constant: THEME - Global color theme instance
#   - Dict: STATE_ENTRY_EXPLANATIONS - Explanations for state entries
#   - Dict: STATE_DO_EXPLANATIONS - Explanations for state do-actions
#   - Dict: STATE_EXIT_EXPLANATIONS - Explanations for state exits
#   - Dict: TRANSITION_EXPLANATIONS - Explanations for transitions
#   - Dict: CHOICE_EXPLANATIONS - Explanations for choice/guard evaluations
#   - Dict: STATES - State machine state definitions
#   - List: SCENARIOS - Registry of scenario functions
#
# ORDERED-SEQUENCE FORMATTING UTILITIES:
#   - Function: format_comment() - Wrap text in gray comment styling
#   - Function: format_state_entry() - Format state entry action line
#   - Function: format_state_do() - Format state do-action line
#   - Function: format_state_exit() - Format state exit action line
#   - Function: format_transition_with_comment() - Format transition line
#   - Function: format_choice_with_comment() - Format choice/guard line
#   - Function: format_start_with_comment() - Format initial state marker
#   - Function: format_end_with_comment() - Format final state marker
#
# ORDERED-SEQUENCE HELPERS:
#   - Function: add_state() - Add all actions for a state
#   - Function: add_transition() - Add a transition line
#   - Function: add_choice() - Add a choice/guard line
#   - Function: add_start() - Add the start marker
#   - Function: add_end() - Add the end marker
#
# SCENARIO IMPLEMENTATIONS:
#   - Function: scenario_power_on_shutdown() - Scenario 1
#   - Function: scenario_invalid_card() - Scenario 2
#   - Function: scenario_valid_card_pin_success_account_positive() - Scenario 3
#   - Function: scenario_valid_card_pin_success_account_zero() - Scenario 4
#   - Function: scenario_clear_pin_loop() - Scenario 5
#   - Function: scenario_invalid_pin_then_success() - Scenario 6
#   - Function: scenario_attempts_exhausted() - Scenario 7
#   - Function: scenario_invalid_amount_then_success_positive() - Scenario 8
#   - Function: scenario_invalid_amount_then_success_zero() - Scenario 9
#
# USER INTERFACE - DISPLAY UTILITIES:
#   - Function: render_title_banner() - Create main title banner
#   - Function: render_scenario_banner() - Create scenario header banner
#   - Function: render_footer_banner() - Create scenario footer banner
#   - Function: render_scenarios_index() - Create scenario list
#   - Function: render_main_menu() - Create interactive menu
#   - Function: print_scenario() - Execute and print scenario
#   - Function: print_completion_banner() - Print completion banner
#   - Function: print_exit_banner() - Print exit banner
#
# USER INTERFACE - INPUT PROMPTS:
#   - Function: get_menu_choice() - Prompt for menu selection
#
# APPLICATION ORCHESTRATION:
#   - Function: run_interactive_menu() - Main interactive menu loop
#   - Function: run_all_scenarios() - Non-interactive sequential mode
#   - Function: main() - Main entry point
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: sys, dataclasses, typing
# - Third-Party: colorama (Fore, Style, init)
# - Local Project Modules:
#   - utilities.menu_banner_utilities (Banner, Menu)
#   - utilities.validation_utilities (validate_prompt_int, wait_for_enter)
# --- Requirements ---
# - Python 3.12+
# - colorama package for cross-platform ANSI color support
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
ATM State Machine prints step-by-step sequences

The Python script is a small console application that print all the steps in sequence 
for all the operations at an automated teller machine (ATM) shown in 
the "ATM State Machine UML Diagram.png" diagram.


Nine distinct scenarios:
1. Power On → Shutdown (no card inserted)
2. Invalid Card rejection
3-4. Successful withdrawal with balance > 0 and balance = 0 (closure)
5. PIN clear loop with successful retry
6. Invalid PIN with successful retry
7. PIN attempts exhausted (card rejection)
8-9. Invalid amount retry with balance > 0 and balance = 0 (closure)
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable

from colorama import Fore, Style, init

from utilities.menu_banner_utilities import Banner, Menu
from utilities.validation_utilities import validate_prompt_int, wait_for_enter

# Configure UTF-8 output for Windows console (required for Unicode box characters)
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Initialize colorama for cross-platform ANSI color support (Windows + Unix)
init(autoreset=True)

# ______________________________________________________________________________
# Class Definitions – Data Classes
# ==============================================================================
# TYPES AND DATA STRUCTURES
# ==============================================================================
# Dataclass Classes:
#   - Class: Theme (frozen dataclass) - ANSI color theme for path output
#   - Class: Ctx (mutable dataclass) - Runtime execution context for guards/computations
#   - Class: StateActions (frozen dataclass) - State machine state encoding
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class Theme
@dataclass(frozen=True, slots=True, kw_only=True)
class Theme:
    """Color theme for ordered-sequence output.

    Attributes:
        state_name: Color for state name headers (bright cyan).
        entry_action: Color for entry action text (cyan).
        do_action: Color for do-action text (white).
        exit_action: Color for exit action text (cyan).
        transition: Color for transition events (yellow).
        choice_node: Color for choice/decision nodes (bright magenta).
        guard_true: Color for guards that evaluate true (light green).
        guard_false: Color for guards that evaluate false (light red).
        error_path: Color for error path markers (bright light red).
        success_path: Color for success path markers (bright light green).
        context_info: Color for context information (light blue).
        comment: Color for explanation comments (gray/light black).
        reset: ANSI reset code to clear formatting.

    Logic:
        This frozen dataclass defines ANSI color codes for consistent visual styling.
        1. Group colors by their semantic purpose (state actions, transitions, etc.).
        2. Use colorama's Fore and Style constants for cross-platform compatibility.
        3. Provide a reset code to clear formatting after each colored segment.
    """

    # --- State action colors (used for entry/do/exit formatting) ---
    state_name: str = Fore.LIGHTCYAN_EX + Style.BRIGHT  # Bold state name headers
    entry_action: str = Fore.CYAN                        # Entry action text
    do_action: str = Fore.WHITE                          # Do-action computation text
    exit_action: str = Fore.CYAN                         # Exit action text

    # --- Transition colors (event/action pairs) ---
    transition: str = Fore.YELLOW  # Transition events and actions

    # --- Choice/guard colors (decision point evaluation) ---
    choice_node: str = Fore.MAGENTA + Style.BRIGHT  # Choice node name
    guard_true: str = Fore.LIGHTGREEN_EX            # Guard condition met (path taken)
    guard_false: str = Fore.LIGHTRED_EX             # Guard condition not met (path rejected)

    # --- Special markers (start/end/error/success) ---
    error_path: str = Fore.LIGHTRED_EX + Style.BRIGHT    # Error/failure path markers
    success_path: str = Fore.LIGHTGREEN_EX + Style.BRIGHT  # Success/completion markers
    context_info: str = Fore.LIGHTBLUE_EX                # Context information (step numbers)

    # --- Explanation comments (gray text below ordered-sequence lines) ---
    comment: str = Fore.LIGHTBLACK_EX  # Gray explanation text

    # --- Reset (clears all formatting) ---
    reset: str = Style.RESET_ALL  # ANSI reset code
# ------------------------------------------------------------------------- end class Theme

# ------------------------------------------------------------------------- class Ctx
@dataclass(slots=True, kw_only=True)
class Ctx:
    """Execution context holding values used in guards and 'do' computations.

    Attributes:
        attempt: Current PIN attempt count (starts at 0, incremented before auth check).
        account_amount: Current account balance in dollars.
        withdraw_amount: Amount user wants to withdraw in dollars.
        computed_amount: Result of accountAmount - withdrawAmount calculation.
        is_valid_card: Whether the inserted card is valid.
        is_valid_pin: Whether the entered PIN is correct.

    Logic:
        This mutable dataclass tracks runtime state during scenario execution.
        1. Store PIN attempt count starting at 0 (incremented before auth check).
        2. Track account balance and withdrawal amounts for computation.
        3. Hold card and PIN validity flags for guard condition evaluation.
    """

    # --- PIN attempt tracking ---
    attempt: int = 0  # Incremented before each auth check; triggers exhaustion at >MAX_TRIES

    # --- Account balance tracking ---
    account_amount: int = 100   # Current balance; updated after Dispense state
    withdraw_amount: int = 0    # User's requested withdrawal; set when scenario starts
    computed_amount: int = 0    # Derived: accountAmount - withdrawAmount; set in ComputeAmt

    # --- Validity flags (for guard condition evaluation) ---
    is_valid_card: bool = True  # False triggers CardCheck → InvalidCard path
    is_valid_pin: bool = True   # False triggers PinCheck → InvalidPin or exhausted path
# ------------------------------------------------------------------------- end class Ctx

# ------------------------------------------------------------------------- class StateActions
@dataclass(frozen=True, slots=True, kw_only=True)
class StateActions:
    """Actions associated with a state machine state.

    Attributes:
        name: Human-readable state name for display purposes.
        entry: Entry action executed when entering the state.
        do: Optional do-action (computation) executed while in the state.
        exit: Exit action or condition that triggers leaving the state.

    Logic:
        This frozen dataclass encodes the entry/do/exit actions for a state machine state.
        1. Store the human-readable state name for display.
        2. Capture the entry action (always required).
        3. Optionally capture the do action (computation during state).
        4. Capture the exit action or condition.
    """

    name: str         # Display name for ordered-sequence output (e.g., "Idle", "Prompt Pin")
    entry: str        # Entry action from UML (e.g., "showingWelcome", "promptingForPin")
    do: str | None = None  # Optional do-action; None if state has no computation
    exit: str = ""    # Exit condition/action from UML (e.g., "readCard or shutdown")
# ------------------------------------------------------------------------- end class StateActions

# ______________________________________________________________________________
# Class Definitions – Regular Classes
# ==============================================================================
# REGULAR CLASS DEFINITIONS
# ==============================================================================
# Behavior-heavy classes that are not suitable for @dataclass usage
# because they have mutable internal state with modified by internal methods.
# ==============================================================================
# Regular Classes:
#   - Class: StepCounter (ordered-sequence step number counter)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class StepCounter
class StepCounter:
    """Tracks step numbers for ordered-sequence output.

    Logic:
        This class tracks the step number for ordered-sequence output.
        1. Initialize counter to zero on construction.
        2. Provide next() to increment and return the new value.
        3. Provide reset() to restart counting from zero for a new scenario.
    """

    # --------------------------------------------------------------- __init__()
    def __init__(self) -> None:
        """Initialize the step counter to zero.

        Logic:
            This initializer prepares the counter for use.
            1. Set the private _count attribute to 0.
        """
        self._count: int = 0
    # ---------------------------------------------------------------

    # ________________________________________________
    # Utilities
    #

    # --------------------------------------------------------------- next()
    def next(self) -> int:
        """Return the next step number after incrementing.

        Logic:
            This utility method increments the counter and returns the new value.
            1. Increment the internal count by 1.
            2. Return the incremented value.
        """
        self._count += 1
        return self._count
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- reset()
    def reset(self) -> None:
        """Reset counter to 0.

        Logic:
            This utility method resets the counter for a new scenario ordered sequence.
            1. Set the internal count back to 0.
        """
        self._count = 0
    # ---------------------------------------------------------------
# ------------------------------------------------------------------------- end class StepCounter

# ______________________________________________________________________________
# Global Constants / Variables
# ==============================================================================
# GLOBAL CONSTANTS AND CONFIGURATION DATA
# ==============================================================================
# Contains module-level constants, type aliases, and data dictionaries that
# configure the ATM state machine behavior.
#
# STATE MACHINE DATA:
# The state machine is derived from PortfolioProject-Module-7/ATM State Machine
# diagram.wsd (PlantUML) and cross-checked with ATM State Machine UML Diagram.csv.
# Each state has entry/do/exit actions, and transitions are triggered by events
# with guard conditions evaluated at decision points.
#
# EXPLANATION DICTIONARIES:
# Gray text explanations are provided for each step type (entry, do, exit,
# transition, choice) to help users understand what is happening during
# execution. These are displayed as comments below each ordered-sequence line.
# ==============================================================================
# Constants:
#   - MAX_TRIES: Maximum PIN attempts before card rejection
#   - THEME: Global color theme instance
# Type Aliases:
#   - ScenarioFunction: Callable type for scenario functions
# Data Dictionaries:
#   - STATE_ENTRY_EXPLANATIONS: Explanations for state entry actions
#   - STATE_DO_EXPLANATIONS: Explanations for state do-actions
#   - STATE_EXIT_EXPLANATIONS: Explanations for state exit actions
#   - TRANSITION_EXPLANATIONS: Explanations for transition events
#   - CHOICE_EXPLANATIONS: Explanations for guard/choice evaluations
#   - STATES: State machine state definitions
#   - SCENARIOS: Registry of scenario functions
# ------------------------------------------------------------------------------

# Constraint: Maximum PIN attempts allowed before card rejection.
# Rationale: This security limit prevents brute-force PIN attacks. After MAX_TRIES
# failed attempts, the AttemptExhausted state is entered and the card is rejected.
# Value derived from diagram note: "Max_tries = 3" means 4th attempt triggers exhaustion.
MAX_TRIES: int = 3

# Global color theme instance (singleton).
# Used throughout the module for consistent ordered-sequence output styling.
THEME: Theme = Theme()

# Type alias for scenario functions.
# Constraint: All scenario functions must return (name, description, steps, context).
# This enables uniform handling in print_scenario() and SCENARIOS registry.
ScenarioFunction = Callable[[], tuple[str, str, list[str], Ctx]]

# Mapping of state keys to entry action explanations.
# These are displayed as gray comments below each state entry line.
# Intent: Help users understand what happens when the ATM enters each state.
STATE_ENTRY_EXPLANATIONS: dict[str, str] = {
    # --- Initial/idle states ---
    "Idle": "ATM enters Idle state; system displays welcome screen to attract users.",

    # --- Card validation states ---
    "InvalidCard": "ATM enters Invalid Card state; system shows error message to user.",

    # --- PIN handling states ---
    "PromptPin": "ATM enters PIN prompt state; system waits for user to enter their PIN.",
    "IncAttempt": "ATM enters Increment Attempt state; system begins tracking this PIN try.",
    "Auth": "ATM enters Authenticating state; system verifies PIN against bank records.",
    "InvalidPin": "ATM enters Invalid PIN state; system notifies user of incorrect PIN.",
    "AttemptExhausted": "ATM enters Attempt Exhausted state; system rejects card after too many failures.",

    # --- Withdrawal states ---
    "PromptAmt": "ATM enters Amount Prompt state; system waits for user to enter withdrawal amount.",
    "ComputeAmt": "ATM enters Compute Amount state; system calculates new balance.",
    "InvalidAmount": "ATM enters Invalid Amount state; system shows insufficient funds error.",
    "Dispense": "ATM enters Dispense Cash state; system prepares to release cash.",

    # --- Account status states ---
    "ShowNewAmt": "ATM enters Show Balance state; system displays updated account balance to user.",
    "CloseAccount": "ATM enters Close Account state; system processes account closure (balance = $0).",
}

# Mapping of state keys to do-action explanations.
# Intent: Explain what computation happens during states with do-actions.
# Only states with do-actions are included (IncAttempt, ComputeAmt, Dispense).
STATE_DO_EXPLANATIONS: dict[str, str] = {
    "IncAttempt": "System increments the PIN attempt counter by 1.",
    "ComputeAmt": "System calculates: new balance = current balance - withdrawal amount.",
    "Dispense": "System updates account balance to the computed amount after dispensing cash.",
}

# Mapping of state keys to exit action explanations.
# These are displayed as gray comments below each state exit line.
# Intent: Explain what triggers the exit from each state.
STATE_EXIT_EXPLANATIONS: dict[str, str] = {
    # --- Initial/idle states ---
    "Idle": "User action required: insert card to begin session, or operator shuts down system.",

    # --- Card validation states ---
    "InvalidCard": "User action required: acknowledge error and remove the rejected card.",

    # --- PIN handling states ---
    "PromptPin": "User action required: submit PIN entry to proceed with authentication.",
    "IncAttempt": "System completed: attempt counter updated successfully.",
    "Auth": "System completed: PIN validation result determined (valid or invalid).",
    "InvalidPin": "User action required: acknowledge the error to retry PIN entry.",
    "AttemptExhausted": "User action required: acknowledge error and remove rejected card.",

    # --- Withdrawal states ---
    "PromptAmt": "User action required: enter the desired withdrawal amount.",
    "ComputeAmt": "System completed: withdrawal amount computation finished.",
    "InvalidAmount": "User action required: acknowledge error to enter a new amount.",
    "Dispense": "System completed: cash has been dispensed to user.",

    # --- Account status states ---
    "ShowNewAmt": "User action required: acknowledge the new balance display.",
    "CloseAccount": "User action required: acknowledge closure and remove card.",
}

# Mapping of transition events to explanations.
# These are displayed as gray comments below each transition line.
# Intent: Explain what event triggered the transition and what action is performed.
TRANSITION_EXPLANATIONS: dict[str, str] = {
    # --- System lifecycle events ---
    "PowerOn": "System event: ATM powers on and initializes the welcome display.",
    "Shutdown": "Operator event: ATM is being shut down for maintenance or end of day.",

    # --- Card events ---
    "InsertedCard(validCard)": "User action: customer inserts their ATM card into the reader.",
    "UserRemovedCard": "User action: customer removes their card, ending the session.",

    # --- PIN events ---
    "UserClear(pin)": "User action: customer clears their PIN entry to start over.",
    "PinEntered(pin, attempt)": "User action: customer submits their PIN for verification.",
    "PromptForPin(attempt)": "System event: ATM re-prompts user for PIN after failed attempt.",
    "PinValidation(IsValidPin, attempt)": "System event: PIN validation result is evaluated.",

    # --- Withdrawal events ---
    "Withdraw(amount)": "User action: customer requests to withdraw the specified amount.",
    "ProcessAmount(computedAmount)": "System event: computed balance is checked for validity.",
    "AccountStatus(accountAmount)": "System event: account balance is checked after withdrawal.",
    "InvalidAmount[withdrawAmount]": "System event: invalid amount triggers re-prompt for new amount.",
}

# Nested mapping of choice nodes to guard explanations by outcome type.
# Intent: Explain what guard condition was evaluated and what path is taken.
# Structure: {node_name: {outcome_type: explanation}}
CHOICE_EXPLANATIONS: dict[str, dict[str, str]] = {
    # --- Card validation decision point ---
    "CardCheck": {
        "valid": "Guard evaluates TRUE: card is valid and no prior attempts. Proceed to PIN entry.",
        "invalid": "Guard evaluates TRUE: card is invalid. Route to rejection handling.",
    },

    # --- PIN validation decision point ---
    "PinCheck": {
        "valid": "Guard evaluates TRUE: PIN is correct. Proceed to withdrawal menu.",
        "invalid_retry": "Guard evaluates TRUE: PIN wrong but retries remain. Allow another attempt.",
        "exhausted": "Guard evaluates TRUE: PIN wrong and no retries left. Reject card.",
    },

    # --- Amount validation decision point ---
    "AmtCheck": {
        "valid": "Guard evaluates TRUE: sufficient funds available. Proceed to dispense cash.",
        "invalid": "Guard evaluates TRUE: insufficient funds. Route to error handling.",
    },

    # --- Account balance decision point ---
    "AcctCheck": {
        "positive": "Guard evaluates TRUE: balance remains positive. Show new balance.",
        "zero": "Guard evaluates TRUE: balance is zero. Trigger account closure.",
    },
}

# Mapping of state keys to StateActions definitions.
# Derived from ATM State Machine diagram.wsd (PlantUML).
# Intent: Encode the complete state machine structure for ordered-sequence generation.
# Each entry defines: name (display), entry action, optional do-action, exit condition.
STATES: dict[str, StateActions] = {
    # --- Initial/idle state ---
    "Idle": StateActions(
        name="Idle",
        entry="showingWelcome",
        exit="readCard or shutdown",
    ),

    # --- Card validation states ---
    "InvalidCard": StateActions(
        name="Invalid Card",
        entry="showingError",
        exit="userAcknowledge && userRemoveCard",
    ),

    # --- PIN entry state ---
    "PromptPin": StateActions(
        name="Prompt User For Pin",
        entry="promptingForPin",
        exit="pinEntered",
    ),

    # --- PIN attempt tracking state (has do-action) ---
    "IncAttempt": StateActions(
        name="Increment Attempt",
        entry="incrementingAttempt",
        do="attempt = attempt + 1",
        exit="attemptIncrementedSuccessfully",
    ),

    # --- PIN authentication state ---
    "Auth": StateActions(
        name="Authenticating",
        entry="authenticatingPin",
        exit="pinValidation",
    ),

    # --- PIN error states ---
    "InvalidPin": StateActions(
        name="Invalid Pin",
        entry="showingError",
        exit="userAcknowledge",
    ),
    "AttemptExhausted": StateActions(
        name="Attempt Exhausted",
        entry="showingError",
        exit="userAcknowledge && userRemoveCard",
    ),

    # --- Withdrawal amount entry state ---
    "PromptAmt": StateActions(
        name="Prompt User For Amount to Withdraw",
        entry="promptingForWithdrawAmount",
        exit="userEnteredAmount",
    ),

    # --- Balance computation state (has do-action) ---
    "ComputeAmt": StateActions(
        name="Compute Withdraw Amount",
        entry="processingWithdraw",
        do="computedAmount = accountAmount - withdrawAmount",
        exit="withdrawAmountComputed",
    ),

    # --- Withdrawal error state ---
    "InvalidAmount": StateActions(
        name="Invalid Amount",
        entry="showingError",
        exit="userAcknowledge",
    ),

    # --- Cash dispensing state (has do-action) ---
    "Dispense": StateActions(
        name="Dispense Cash",
        entry="dispensingCash",
        do="accountAmount = computedAmount",
        exit="cashDispensed",
    ),

    # --- Account status display states ---
    "ShowNewAmt": StateActions(
        name="Show Account New Amount",
        entry="showingAccount",
        exit="userAcknowledge",
    ),
    "CloseAccount": StateActions(
        name="Close Account",
        entry="showingClosureMessage",
        exit="userAcknowledge && accountClosed",
    ),
}

# ______________________________________________________________________________
# Function Definitions
# ==============================================================================
# ORDERED-SEQUENCE FORMATTING UTILITIES
# ==============================================================================
# Contains functions for formatting individual ordered-sequence line elements.
# These format state actions, transitions, choices, and markers into
# colored, consistently-styled output strings with explanation comments.
#
# FORMATTING PATTERN:
# Each formatter returns a tuple of (formatted_line, explanation_comment).
# The formatted line includes step number, element type marker, and content.
# The explanation comment is gray text explaining what is happening.
# ==============================================================================
# Functions:
#   - format_comment: Wrap text in gray comment styling
#   - format_state_entry: Format state entry action line
#   - format_state_do: Format state do-action line with computed values
#   - format_state_exit: Format state exit action line
#   - format_transition_with_comment: Format transition event/action line
#   - format_choice_with_comment: Format choice/guard evaluation line
#   - format_start_with_comment: Format initial state marker
#   - format_end_with_comment: Format final state marker
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_comment()
def format_comment(text: str) -> str:
    """Format a gray explanation comment line.

    Logic:
        This function wraps explanatory text in gray color codes for sequence output.
        1. Prepend consistent indentation (8 spaces) for visual alignment.
        2. Apply the comment color from the theme.
        3. Append reset code to prevent color bleeding.
    """
    return f"        {THEME.comment}{text}{THEME.reset}"
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_state_entry()
def format_state_entry(step: int, state_key: str) -> tuple[str, str]:
    """Format a state entry action line with explanation comment.

    Logic:
        This function formats the entry action for a state in the ordered sequence.
        1. Look up the state definition from STATES dictionary.
        2. Build the formatted line with step number, STATE marker, and entry action.
        3. Look up or generate the explanation comment for this entry.
        4. Return both the formatted line and the comment.
    """
    state: StateActions = STATES[state_key]
    line: str = (
        f"  {THEME.context_info}{step:02d}{THEME.reset}  "
        f"{THEME.state_name}STATE{THEME.reset}  "
        f"{THEME.entry_action}{state.name}: entry / {state.entry}{THEME.reset}"
    )
    explanation: str = STATE_ENTRY_EXPLANATIONS.get(
        state_key, f"Entering {state.name} state."
    )
    return line, format_comment(explanation)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_state_do()
def format_state_do(step: int, state_key: str, ctx: Ctx) -> tuple[str, str] | None:
    """Format a state 'do' action line with context values and explanation.

    Logic:
        This function formats the do-action for a state showing computed values.
        1. Check if the state has a do-action; return None if not.
        2. Generate state-specific detail strings showing actual computed values.
        3. Build the formatted line with step number, STATE marker, and do action.
        4. Return the formatted line and explanation comment.
    """
    state: StateActions = STATES[state_key]

    # VALIDATION: Check if state has a do-action
    if state.do is None:
        return None

    # DISPATCH: Generate state-specific detail and explanation based on state key
    detail: str
    explanation: str
    if state_key == "IncAttempt":
        # IncAttempt: Show attempt counter increment (previous → current)
        detail = f"(attempt: {ctx.attempt - 1} → {ctx.attempt})"
        explanation = f"System increments attempt counter: {ctx.attempt - 1} → {ctx.attempt}."
    elif state_key == "ComputeAmt":
        # ComputeAmt: Show balance computation (account - withdraw = computed)
        detail = f"({ctx.account_amount} - {ctx.withdraw_amount} = {ctx.computed_amount})"
        explanation = (
            f"System computes: ${ctx.account_amount} - "
            f"${ctx.withdraw_amount} = ${ctx.computed_amount}."
        )
    elif state_key == "Dispense":
        # Dispense: Show account balance update after dispensing cash
        detail = f"(accountAmount ← {ctx.computed_amount})"
        explanation = (
            f"System updates account balance to ${ctx.computed_amount} after dispensing cash."
        )
    else:
        # Default: No specific detail, use dictionary lookup
        detail = ""
        explanation = STATE_DO_EXPLANATIONS.get(
            state_key, "System performs internal computation."
        )

    line: str = (
        f"  {THEME.context_info}{step:02d}{THEME.reset}  "
        f"{THEME.state_name}STATE{THEME.reset}  "
        f"{THEME.do_action}{state.name}: do / {state.do} {detail}{THEME.reset}"
    )
    return line, format_comment(explanation)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_state_exit()
def format_state_exit(step: int, state_key: str) -> tuple[str, str]:
    """Format a state exit action line with explanation comment.

    Logic:
        This function formats the exit action for a state in the ordered sequence.
        1. Look up the state definition from STATES dictionary.
        2. Build the formatted line with step number, STATE marker, and exit action.
        3. Look up or generate the explanation comment for this exit.
        4. Return both the formatted line and the comment.
    """
    state: StateActions = STATES[state_key]
    line: str = (
        f"  {THEME.context_info}{step:02d}{THEME.reset}  "
        f"{THEME.state_name}STATE{THEME.reset}  "
        f"{THEME.exit_action}{state.name}: exit / {state.exit}{THEME.reset}"
    )
    explanation: str = STATE_EXIT_EXPLANATIONS.get(
        state_key, f"Exiting {state.name} state."
    )
    return line, format_comment(explanation)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_transition_with_comment()
def format_transition_with_comment(
    step: int, event: str, action: str, custom_explanation: str | None = None
) -> tuple[str, str]:
    """Format a transition line with event, action, and explanation comment.

    Logic:
        This function formats a state machine transition for the ordered sequence.
        1. Build the formatted line with step number, TRANS marker, event, and action.
        2. Use custom explanation if provided.
        3. Otherwise, look up explanation by matching event prefix in dictionary.
        4. Return the formatted line and explanation comment.
    """
    line: str = (
        f"  {THEME.context_info}{step:02d}{THEME.reset}  "
        f"{THEME.transition}TRANS{THEME.reset}  "
        f"{THEME.transition}{event} / {action}{THEME.reset}"
    )

    # DISPATCH: Determine explanation source (custom vs dictionary lookup)
    explanation: str
    if custom_explanation:
        # Custom explanation provided by caller
        explanation = custom_explanation
    else:
        # Look up explanation by matching event prefix in dictionary
        # Handle parameterized events like "Withdraw(50)" matching "Withdraw(amount)"
        base_event: str = event.split("(")[0] + "(" if "(" in event else event
        for key in TRANSITION_EXPLANATIONS:
            if key.startswith(base_event) or event.startswith(key.split("(")[0]):
                explanation = TRANSITION_EXPLANATIONS[key]
                break
        else:
            # Default if no match found
            explanation = f"Transition triggered by {event} event."
    return line, format_comment(explanation)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_choice_with_comment()
def format_choice_with_comment(
    step: int,
    node: str,
    guard: str,
    target: str,
    choice_type: str,
    is_taken: bool = True,
) -> tuple[str, str]:
    """Format a choice/guard evaluation line with explanation comment.

    Logic:
        This function formats a decision point evaluation for the ordered sequence.
        1. Select color based on whether the guard condition is taken.
        2. Build the formatted line with step number, CHOICE marker, guard, and target.
        3. Look up explanation based on the choice node and type.
        4. Return the formatted line and explanation comment.
    """
    # DISPATCH: Select color and arrow based on path taken
    color: str = THEME.guard_true if is_taken else THEME.guard_false
    arrow: str = "→" if is_taken else "✗"

    line: str = (
        f"  {THEME.context_info}{step:02d}{THEME.reset}  "
        f"{THEME.choice_node}CHOICE{THEME.reset} "
        f"{THEME.choice_node}{node}{THEME.reset}: "
        f"{color}[{guard}] {arrow} {target}{THEME.reset}"
    )

    # Look up explanation based on node and choice type
    node_explanations: dict[str, str] = CHOICE_EXPLANATIONS.get(node, {})
    explanation: str = node_explanations.get(
        choice_type, f"Decision point {node}: condition [{guard}] routes to {target}."
    )
    return line, format_comment(explanation)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_start_with_comment()
def format_start_with_comment(step: int) -> tuple[str, str]:
    """Format the initial state marker with explanation comment.

    Logic:
        This function formats the state machine start marker for the ordered sequence.
        1. Build the formatted line with step number and START marker.
        2. Create the explanation comment for the initial state.
        3. Return the formatted line and explanation comment.
    """
    line: str = (
        f"  {THEME.context_info}{step:02d}{THEME.reset}  "
        f"{THEME.success_path}START{THEME.reset}  "
        f"{THEME.success_path}[*] Initial State{THEME.reset}"
    )
    explanation: str = "State machine begins execution from the initial pseudo-state."
    return line, format_comment(explanation)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- format_end_with_comment()
def format_end_with_comment(step: int, reason: str) -> tuple[str, str]:
    """Format the final state marker with explanation comment.

    Logic:
        This function formats the state machine end marker for the ordered sequence.
        1. Build the formatted line with step number, END marker, and reason.
        2. Create the explanation comment describing the session outcome.
        3. Return the formatted line and explanation comment.
    """
    line: str = (
        f"  {THEME.context_info}{step:02d}{THEME.reset}  "
        f"{THEME.success_path}END{THEME.reset}    "
        f"{THEME.success_path}[*] Final State - {reason}{THEME.reset}"
    )
    explanation: str = f"State machine reaches final state. Session outcome: {reason}."
    return line, format_comment(explanation)
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function Definitions
# ==============================================================================
# ORDERED-SEQUENCE HELPERS
# ==============================================================================
# Contains functions that append formatted ordered-sequence elements to a steps list.
# These are higher-level helpers that combine formatting with list management,
# adding complete state visits, transitions, and markers to build ordered sequences.
#
# EMISSION PATTERN:
# Each add function takes a steps list and counter, formats the appropriate
# element(s), and appends both the line and explanation comment to steps.
# ==============================================================================
# Functions:
#   - add_state: Add all actions for a state (entry, do, exit)
#   - add_transition: Add a transition event/action line
#   - add_choice: Add a choice/guard evaluation line
#   - add_start: Add the initial state marker
#   - add_end: Add the final state marker
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- add_state()
def add_state(steps: list[str], counter: StepCounter, state_key: str, ctx: Ctx) -> None:
    """Add all actions for a state (entry, do, exit) with explanation comments.

    Logic:
        This function appends all ordered-sequence lines for visiting a state.
        1. Format and append the entry action with its explanation.
        2. If the state has a do-action, format and append it with explanation.
        3. Format and append the exit action with its explanation.
    """
    # Step 1: Entry action
    entry_line: str
    entry_comment: str
    entry_line, entry_comment = format_state_entry(counter.next(), state_key)
    steps.append(entry_line)
    steps.append(entry_comment)

    # Step 2: Do action (if present)
    state: StateActions = STATES[state_key]
    if state.do:
        do_result: tuple[str, str] | None = format_state_do(counter.next(), state_key, ctx)
        if do_result:
            do_line: str
            do_comment: str
            do_line, do_comment = do_result
            steps.append(do_line)
            steps.append(do_comment)

    # Step 3: Exit action
    exit_line: str
    exit_comment: str
    exit_line, exit_comment = format_state_exit(counter.next(), state_key)
    steps.append(exit_line)
    steps.append(exit_comment)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- add_transition()
def add_transition(
    steps: list[str], counter: StepCounter, event: str, action: str,
    custom_explanation: str | None = None
) -> None:
    """Add a transition line with explanation comment.

    Logic:
        This function appends a transition line to the steps list.
        1. Format the transition with event, action, and optional custom explanation.
        2. Append both the transition line and its explanation comment.
    """
    line: str
    comment: str
    line, comment = format_transition_with_comment(
        counter.next(), event, action, custom_explanation
    )
    steps.append(line)
    steps.append(comment)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- add_choice()
def add_choice(
    steps: list[str], counter: StepCounter, node: str, guard: str,
    target: str, choice_type: str, is_taken: bool = True
) -> None:
    """Add a choice/guard line with explanation comment.

    Logic:
        This function appends a decision point line to the steps list.
        1. Format the choice with node, guard condition, target, and taken flag.
        2. Append both the choice line and its explanation comment.
    """
    line: str
    comment: str
    line, comment = format_choice_with_comment(
        counter.next(), node, guard, target, choice_type, is_taken
    )
    steps.append(line)
    steps.append(comment)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- add_start()
def add_start(steps: list[str], counter: StepCounter) -> None:
    """Add the start marker with explanation comment.

    Logic:
        This function appends the initial state marker to the steps list.
        1. Format the start marker with step number.
        2. Append both the start line and its explanation comment.
    """
    line: str
    comment: str
    line, comment = format_start_with_comment(counter.next())
    steps.append(line)
    steps.append(comment)
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- add_end()
def add_end(steps: list[str], counter: StepCounter, reason: str) -> None:
    """Add the end marker with explanation comment.

    Logic:
        This function appends the final state marker to the steps list.
        1. Format the end marker with step number and completion reason.
        2. Append both the end line and its explanation comment.
    """
    line: str
    comment: str
    line, comment = format_end_with_comment(counter.next(), reason)
    steps.append(line)
    steps.append(comment)
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function Definitions
# ==============================================================================
# SCENARIO IMPLEMENTATIONS
# ==============================================================================
# Contains functions that implement each distinct path through the ATM state
# machine. Each scenario function generates a specific ordered sequence of states and
# transitions, demonstrating different operational outcomes.
#
# SCENARIO PATTERN:
# Each scenario initializes a context (Ctx), creates a step counter, and uses
# add_* functions to build an ordered sequence of the path. Returns a tuple containing:
# (scenario_name, description, steps_list, final_context)
#
# COVERAGE:
# These 9 scenarios cover all distinct outcome paths in the state machine:
# - Power on/shutdown (no user interaction)
# - Invalid card rejection
# - Successful transactions (balance > 0 and balance = 0)
# - PIN clear loop, PIN retry, PIN exhaustion
# - Invalid amount retry paths
# ==============================================================================
# Functions:
#   - scenario_power_on_shutdown
#   - scenario_invalid_card
#   - scenario_valid_card_pin_success_account_positive
#   - scenario_valid_card_pin_success_account_zero
#   - scenario_clear_pin_loop
#   - scenario_invalid_pin_then_success
#   - scenario_attempts_exhausted
#   - scenario_invalid_amount_then_success_positive
#   - scenario_invalid_amount_then_success_zero
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_power_on_shutdown()
def scenario_power_on_shutdown() -> tuple[str, str, list[str], Ctx]:
    """Scenario 1: Power on → shutdown (no card inserted).

    Logic:
        This function generates the simplest ATM path: power on then shutdown.
        1. Initialize context with default values and empty steps list.
        2. Add start marker and PowerOn transition to Idle state.
        3. Add Idle state actions (entry, exit).
        4. Add Shutdown transition and end marker.
        5. Return scenario metadata and generated steps.
    """
    name: str = "Power On → Shutdown"
    description: str = "ATM powers on, displays welcome, then shuts down"
    ctx: Ctx = Ctx()
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # [*] --> Idle : PowerOn / showWelcome
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    # Idle --> [*] : Shutdown / poweringOff
    add_transition(steps, counter, "Shutdown", "poweringOff")
    add_end(steps, counter, "System shutdown")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_invalid_card()
def scenario_invalid_card() -> tuple[str, str, list[str], Ctx]:
    """Scenario 2: Invalid card path.

    Logic:
        This function generates the invalid card rejection path.
        1. Initialize context with is_valid_card=False.
        2. Add start, PowerOn, and Idle state.
        3. Add card insertion transition and CardCheck choice (invalid branch).
        4. Add InvalidCard state and user card removal transition.
        5. Return to Idle and add end marker.
    """
    name: str = "Invalid Card"
    description: str = "User inserts invalid card → rejected → removes card → session ends"
    ctx: Ctx = Ctx(is_valid_card=False)
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start and enter Idle
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    # Idle --> CardCheck : InsertedCard(validCard)
    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")

    # CardCheck --> InvalidCard : [isValidCard=false] / rejectCard
    add_choice(steps, counter, "CardCheck", "isValidCard=false", "InvalidCard", "invalid")
    add_state(steps, counter, "InvalidCard", ctx)

    # InvalidCard --> Idle : UserRemovedCard / endSession
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes rejected card; system returns to idle and ends the session."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, "Session ended - invalid card")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_valid_card_pin_success_account_positive()
def scenario_valid_card_pin_success_account_positive() -> tuple[str, str, list[str], Ctx]:
    """Scenario 3: Valid card → PIN success (1st try) → withdraw → account > 0.

    Logic:
        This function generates the happy path with remaining balance.
        1. Initialize context with account_amount=100, withdraw_amount=50.
        2. Add start, PowerOn, Idle, card insertion, and CardCheck (valid).
        3. Add PromptPin, PIN entry, IncAttempt, Auth, and PinCheck (valid).
        4. Add PromptAmt, withdrawal, ComputeAmt, AmtCheck (valid), Dispense.
        5. Add AcctCheck (positive), ShowNewAmt, card removal, and end.
    """
    name: str = "Valid Card → PIN Success → Account > 0"
    description: str = "Full successful transaction with remaining balance"
    ctx: Ctx = Ctx(account_amount=100, withdraw_amount=50)
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    # Insert valid card
    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")
    add_choice(
        steps, counter, "CardCheck", "isValidCard=true && attempt==0", "PromptPin", "valid"
    )

    # Prompt for PIN
    add_state(steps, counter, "PromptPin", ctx)

    # Enter PIN and increment attempt
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
        "User submits PIN; system routes to increment the attempt counter."
    )
    ctx.attempt += 1
    add_state(steps, counter, "IncAttempt", ctx)

    # Authenticate
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "authenticating",
        "System forwards PIN and attempt count to authentication module."
    )
    add_state(steps, counter, "Auth", ctx)

    # PIN check - success
    add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")
    add_choice(steps, counter, "PinCheck", "IsValidPin=true", "PromptAmt", "valid")

    # Prompt for amount
    add_state(steps, counter, "PromptAmt", ctx)

    # Withdraw
    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests ${ctx.withdraw_amount} withdrawal; system begins balance computation."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount
    add_state(steps, counter, "ComputeAmt", ctx)

    # Amount check - valid
    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(steps, counter, "AmtCheck", "computedAmount >= 0", "Dispense", "valid")

    # Dispense cash
    ctx.account_amount = ctx.computed_amount
    add_state(steps, counter, "Dispense", ctx)

    # Account check - positive balance
    add_transition(steps, counter, "AccountStatus(accountAmount)", "check")
    add_choice(steps, counter, "AcctCheck", "accountAmount > 0", "ShowNewAmt", "positive")

    # Show new amount
    add_state(steps, counter, "ShowNewAmt", ctx)

    # End session
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes card after viewing balance; session ends successfully."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, f"Transaction complete - balance: ${ctx.account_amount}")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_valid_card_pin_success_account_zero()
def scenario_valid_card_pin_success_account_zero() -> tuple[str, str, list[str], Ctx]:
    """Scenario 4: Valid card → PIN success → withdraw → account == 0 → close.

    Logic:
        This function generates the full withdrawal path triggering account closure.
        1. Initialize context with account_amount=100, withdraw_amount=100.
        2. Follow the same path as scenario 3 through Dispense state.
        3. At AcctCheck, take the zero branch to CloseAccount.
        4. Add CloseAccount state and session end.
    """
    name: str = "Valid Card → PIN Success → Account = 0"
    description: str = "Full withdrawal depletes account, triggering account closure"
    ctx: Ctx = Ctx(account_amount=100, withdraw_amount=100)
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    # Insert valid card
    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")
    add_choice(
        steps, counter, "CardCheck", "isValidCard=true && attempt==0", "PromptPin", "valid"
    )

    # Prompt for PIN
    add_state(steps, counter, "PromptPin", ctx)

    # Enter PIN and increment attempt
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
        "User submits PIN; system routes to increment the attempt counter."
    )
    ctx.attempt += 1
    add_state(steps, counter, "IncAttempt", ctx)

    # Authenticate
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "authenticating",
        "System forwards PIN and attempt count to authentication module."
    )
    add_state(steps, counter, "Auth", ctx)

    # PIN check - success
    add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")
    add_choice(steps, counter, "PinCheck", "IsValidPin=true", "PromptAmt", "valid")

    # Prompt for amount
    add_state(steps, counter, "PromptAmt", ctx)

    # Withdraw full balance
    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests full balance (${ctx.withdraw_amount}); system begins computation."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount
    add_state(steps, counter, "ComputeAmt", ctx)

    # Amount check - valid
    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(steps, counter, "AmtCheck", "computedAmount >= 0", "Dispense", "valid")

    # Dispense cash
    ctx.account_amount = ctx.computed_amount
    add_state(steps, counter, "Dispense", ctx)

    # Account check - zero balance
    add_transition(steps, counter, "AccountStatus(accountAmount)", "check")
    add_choice(steps, counter, "AcctCheck", "accountAmount == 0", "CloseAccount", "zero")

    # Close account
    add_state(steps, counter, "CloseAccount", ctx)

    # End session
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes card; session ends with account closure processed."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, "Account closed - zero balance")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_clear_pin_loop()
def scenario_clear_pin_loop() -> tuple[str, str, list[str], Ctx]:
    """Scenario 5: Clear PIN loop once → PIN success → withdraw.

    Logic:
        This function generates the path where user clears PIN entry once.
        1. Initialize context and proceed to PromptPin state.
        2. Add UserClear transition looping back to PromptPin.
        3. Continue with successful PIN entry and withdrawal.
        4. Complete with ShowNewAmt and session end.
    """
    name: str = "Clear PIN Loop → Success"
    description: str = "User clears PIN entry once, then enters correct PIN"
    ctx: Ctx = Ctx(account_amount=100, withdraw_amount=30)
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    # Insert valid card
    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")
    add_choice(
        steps, counter, "CardCheck", "isValidCard=true && attempt==0", "PromptPin", "valid"
    )

    # Prompt for PIN
    add_state(steps, counter, "PromptPin", ctx)

    # User clears PIN (loop back to PromptPin)
    add_transition(
        steps, counter, "UserClear(pin)", "clearPin && repromptForPin",
        "User clears PIN input (e.g., pressed 'Clear' button); system re-prompts for PIN."
    )
    add_state(steps, counter, "PromptPin", ctx)

    # Now enter PIN correctly
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
        "User submits PIN (after clearing); system increments attempt counter."
    )
    ctx.attempt += 1
    add_state(steps, counter, "IncAttempt", ctx)

    # Authenticate
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "authenticating",
        "System forwards PIN and attempt count to authentication module."
    )
    add_state(steps, counter, "Auth", ctx)

    # PIN check - success
    add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")
    add_choice(steps, counter, "PinCheck", "IsValidPin=true", "PromptAmt", "valid")

    # Continue to withdrawal
    add_state(steps, counter, "PromptAmt", ctx)
    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests ${ctx.withdraw_amount} withdrawal; system begins computation."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount
    add_state(steps, counter, "ComputeAmt", ctx)

    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(steps, counter, "AmtCheck", "computedAmount >= 0", "Dispense", "valid")

    ctx.account_amount = ctx.computed_amount
    add_state(steps, counter, "Dispense", ctx)

    add_transition(steps, counter, "AccountStatus(accountAmount)", "check")
    add_choice(steps, counter, "AcctCheck", "accountAmount > 0", "ShowNewAmt", "positive")

    add_state(steps, counter, "ShowNewAmt", ctx)
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes card after viewing balance; session ends successfully."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, f"Transaction complete - balance: ${ctx.account_amount}")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_invalid_pin_then_success()
def scenario_invalid_pin_then_success() -> tuple[str, str, list[str], Ctx]:
    """Scenario 6: Invalid PIN → retry → success.

    Logic:
        This function generates the path with one failed PIN attempt then success.
        1. Initialize context and proceed through first PIN entry.
        2. At PinCheck, take invalid_retry branch to InvalidPin state.
        3. Add PromptForPin transition back to PromptPin.
        4. Enter correct PIN and complete successful withdrawal.
    """
    name: str = "Invalid PIN → Retry → Success"
    description: str = "First PIN attempt fails, second attempt succeeds"
    ctx: Ctx = Ctx(account_amount=100, withdraw_amount=25)
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    # Insert valid card
    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")
    add_choice(
        steps, counter, "CardCheck", "isValidCard=true && attempt==0", "PromptPin", "valid"
    )
    add_state(steps, counter, "PromptPin", ctx)

    # First PIN attempt (wrong)
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
        "User submits INCORRECT PIN; system increments attempt counter."
    )
    ctx.attempt += 1
    add_state(steps, counter, "IncAttempt", ctx)

    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "authenticating",
        "System forwards PIN and attempt count to authentication module."
    )
    add_state(steps, counter, "Auth", ctx)

    # PIN check - fail (attempt 1 <= 3)
    ctx.is_valid_pin = False
    add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")
    add_choice(
        steps, counter, "PinCheck",
        f"IsValidPin=false && attempt({ctx.attempt}) <= Max_tries({MAX_TRIES})",
        "InvalidPin", "invalid_retry"
    )

    add_state(steps, counter, "InvalidPin", ctx)

    # Return to PIN prompt
    add_transition(
        steps, counter, "PromptForPin(attempt)", "promptForPin",
        f"System allows retry (attempt {ctx.attempt} of {MAX_TRIES}); re-prompts for PIN."
    )
    add_state(steps, counter, "PromptPin", ctx)

    # Second PIN attempt (correct)
    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
        "User submits CORRECT PIN; system increments attempt counter."
    )
    ctx.attempt += 1
    add_state(steps, counter, "IncAttempt", ctx)

    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "authenticating",
        "System forwards PIN and attempt count to authentication module."
    )
    add_state(steps, counter, "Auth", ctx)

    # PIN check - success
    ctx.is_valid_pin = True
    add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")
    add_choice(steps, counter, "PinCheck", "IsValidPin=true", "PromptAmt", "valid")

    # Continue to withdrawal
    add_state(steps, counter, "PromptAmt", ctx)
    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests ${ctx.withdraw_amount} withdrawal; system begins computation."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount
    add_state(steps, counter, "ComputeAmt", ctx)

    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(steps, counter, "AmtCheck", "computedAmount >= 0", "Dispense", "valid")

    ctx.account_amount = ctx.computed_amount
    add_state(steps, counter, "Dispense", ctx)

    add_transition(steps, counter, "AccountStatus(accountAmount)", "check")
    add_choice(steps, counter, "AcctCheck", "accountAmount > 0", "ShowNewAmt", "positive")

    add_state(steps, counter, "ShowNewAmt", ctx)
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes card after viewing balance; session ends successfully."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, f"Transaction complete - balance: ${ctx.account_amount}")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_attempts_exhausted()
def scenario_attempts_exhausted() -> tuple[str, str, list[str], Ctx]:
    """Scenario 7: PIN attempts exhausted → card rejected.

    Note on attempt semantics (faithful to diagram):
    - attempt starts at 0
    - Incremented BEFORE authentication check
    - Exhaustion triggers when IsValidPin=false && attempt > Max_tries(3)
    - This means 4 failed attempts total (attempt becomes 4 on 4th try)

    Logic:
        This function generates the path where all PIN attempts are exhausted.
        1. Initialize context with is_valid_pin=False for all attempts.
        2. Loop through MAX_TRIES+1 failed PIN attempts.
        3. For attempts 1-3, take invalid_retry branch and return to PromptPin.
        4. On attempt 4, take exhausted branch to AttemptExhausted state.
        5. Add card rejection and session end.
    """
    name: str = "PIN Attempts Exhausted"
    description: str = f"User fails PIN {MAX_TRIES + 1} times, card is rejected"
    ctx: Ctx = Ctx(account_amount=100, is_valid_pin=False)
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    # Insert valid card
    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")
    add_choice(
        steps, counter, "CardCheck", "isValidCard=true && attempt==0", "PromptPin", "valid"
    )
    add_state(steps, counter, "PromptPin", ctx)

    # MAIN ITERATION LOOP: Process each PIN attempt until exhausted
    # Iterates from attempt 1 to MAX_TRIES+1 (4), with exhaustion on final iteration
    for attempt_num in range(1, MAX_TRIES + 2):  # 1, 2, 3, 4 (exhausted on 4)
        # Step 1: User enters PIN, system increments attempt counter
        add_transition(
            steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
            f"User submits INCORRECT PIN (attempt #{attempt_num}); system increments counter."
        )
        ctx.attempt += 1
        add_state(steps, counter, "IncAttempt", ctx)

        # Step 2: System authenticates (fails because is_valid_pin=False)
        add_transition(
            steps, counter, "PinEntered(pin, attempt)", "authenticating",
            "System forwards PIN and attempt count to authentication module."
        )
        add_state(steps, counter, "Auth", ctx)

        # Step 3: PIN validation check - routes based on attempt count
        add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")

        # Step 4: Check if retries remain or exhausted
        if ctx.attempt <= MAX_TRIES:
            # Step 4a: Still have retries - go to InvalidPin and loop back to PromptPin
            add_choice(
                steps, counter, "PinCheck",
                f"IsValidPin=false && attempt({ctx.attempt}) <= Max_tries({MAX_TRIES})",
                "InvalidPin", "invalid_retry"
            )
            add_state(steps, counter, "InvalidPin", ctx)
            add_transition(
                steps, counter, "PromptForPin(attempt)", "promptForPin",
                f"System allows retry (attempt {ctx.attempt} of {MAX_TRIES}); re-prompts for PIN."
            )
            add_state(steps, counter, "PromptPin", ctx)
        else:
            # Step 4b: Exhausted - go to AttemptExhausted (final iteration)
            add_choice(
                steps, counter, "PinCheck",
                f"IsValidPin=false && attempt({ctx.attempt}) > Max_tries({MAX_TRIES})",
                "AttemptExhausted", "exhausted"
            )
            add_state(steps, counter, "AttemptExhausted", ctx)

    # Card rejected - session ends after exhaustion
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes rejected card; session ends with security lockout."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, "Card rejected - PIN attempts exhausted")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_invalid_amount_then_success_positive()
def scenario_invalid_amount_then_success_positive() -> tuple[str, str, list[str], Ctx]:
    """Scenario 8: Invalid withdraw amount → retry → success (account > 0).

    Logic:
        This function generates the path with one invalid withdrawal then success.
        1. Initialize context with withdraw_amount exceeding account balance.
        2. Complete PIN authentication successfully.
        3. First withdrawal attempt fails at AmtCheck (invalid branch).
        4. Add InvalidAmount state and re-prompt transition.
        5. Retry with valid amount and complete successful withdrawal.
    """
    name: str = "Invalid Amount → Success (Account > 0)"
    description: str = "User enters amount exceeding balance, retries with valid amount"
    ctx: Ctx = Ctx(account_amount=100, withdraw_amount=150)  # First attempt exceeds balance
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start through PIN success
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")
    add_choice(
        steps, counter, "CardCheck", "isValidCard=true && attempt==0", "PromptPin", "valid"
    )
    add_state(steps, counter, "PromptPin", ctx)

    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
        "User submits PIN; system increments attempt counter."
    )
    ctx.attempt += 1
    add_state(steps, counter, "IncAttempt", ctx)

    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "authenticating",
        "System forwards PIN and attempt count to authentication module."
    )
    add_state(steps, counter, "Auth", ctx)

    add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")
    add_choice(steps, counter, "PinCheck", "IsValidPin=true", "PromptAmt", "valid")

    # First withdrawal attempt - invalid (exceeds balance)
    add_state(steps, counter, "PromptAmt", ctx)
    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests ${ctx.withdraw_amount} (EXCEEDS ${ctx.account_amount} balance); "
        f"computation begins."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount  # -50
    add_state(steps, counter, "ComputeAmt", ctx)

    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(
        steps, counter, "AmtCheck",
        f"computedAmount({ctx.computed_amount}) < 0",
        "InvalidAmount", "invalid"
    )

    add_state(steps, counter, "InvalidAmount", ctx)

    # Retry with valid amount
    add_transition(
        steps, counter, "InvalidAmount[withdrawAmount]", "promptUserForNewAmount",
        "Insufficient funds detected; system prompts user to enter a smaller amount."
    )
    ctx.withdraw_amount = 40  # Valid retry amount
    add_state(steps, counter, "PromptAmt", ctx)

    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests ${ctx.withdraw_amount} (valid amount); system begins computation."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount  # 60
    add_state(steps, counter, "ComputeAmt", ctx)

    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(steps, counter, "AmtCheck", "computedAmount >= 0", "Dispense", "valid")

    ctx.account_amount = ctx.computed_amount
    add_state(steps, counter, "Dispense", ctx)

    add_transition(steps, counter, "AccountStatus(accountAmount)", "check")
    add_choice(steps, counter, "AcctCheck", "accountAmount > 0", "ShowNewAmt", "positive")

    add_state(steps, counter, "ShowNewAmt", ctx)
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes card after viewing balance; session ends successfully."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, f"Transaction complete - balance: ${ctx.account_amount}")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- scenario_invalid_amount_then_success_zero()
def scenario_invalid_amount_then_success_zero() -> tuple[str, str, list[str], Ctx]:
    """Scenario 9: Invalid amount → retry → success (account == 0 → close).

    Logic:
        This function generates invalid withdrawal then full balance withdrawal.
        1. Initialize context with withdraw_amount exceeding account balance.
        2. Complete PIN authentication and first (invalid) withdrawal attempt.
        3. Retry with full balance amount (100), depleting the account.
        4. At AcctCheck, take zero branch to CloseAccount state.
        5. Complete with account closure and session end.
    """
    name: str = "Invalid Amount → Success (Account = 0)"
    description: str = "User retries with full balance withdrawal, triggering account closure"
    ctx: Ctx = Ctx(account_amount=100, withdraw_amount=200)  # First attempt exceeds balance
    steps: list[str] = []
    counter: StepCounter = StepCounter()

    # Start through PIN success
    add_start(steps, counter)
    add_transition(steps, counter, "PowerOn", "showWelcome")
    add_state(steps, counter, "Idle", ctx)

    add_transition(steps, counter, "InsertedCard(validCard)", "checkCard")
    add_choice(
        steps, counter, "CardCheck", "isValidCard=true && attempt==0", "PromptPin", "valid"
    )
    add_state(steps, counter, "PromptPin", ctx)

    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "incrementAttempt",
        "User submits PIN; system increments attempt counter."
    )
    ctx.attempt += 1
    add_state(steps, counter, "IncAttempt", ctx)

    add_transition(
        steps, counter, "PinEntered(pin, attempt)", "authenticating",
        "System forwards PIN and attempt count to authentication module."
    )
    add_state(steps, counter, "Auth", ctx)

    add_transition(steps, counter, "PinValidation(IsValidPin, attempt)", "check")
    add_choice(steps, counter, "PinCheck", "IsValidPin=true", "PromptAmt", "valid")

    # First withdrawal attempt - invalid
    add_state(steps, counter, "PromptAmt", ctx)
    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests ${ctx.withdraw_amount} (EXCEEDS ${ctx.account_amount} balance); "
        f"computation begins."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount  # -100
    add_state(steps, counter, "ComputeAmt", ctx)

    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(
        steps, counter, "AmtCheck",
        f"computedAmount({ctx.computed_amount}) < 0",
        "InvalidAmount", "invalid"
    )

    add_state(steps, counter, "InvalidAmount", ctx)

    # Retry with full balance
    add_transition(
        steps, counter, "InvalidAmount[withdrawAmount]", "promptUserForNewAmount",
        "Insufficient funds detected; system prompts user to enter a valid amount."
    )
    ctx.withdraw_amount = 100  # Full balance
    add_state(steps, counter, "PromptAmt", ctx)

    add_transition(
        steps, counter, f"Withdraw({ctx.withdraw_amount})", "computeWithdraw",
        f"User requests full balance (${ctx.withdraw_amount}); system begins computation."
    )
    ctx.computed_amount = ctx.account_amount - ctx.withdraw_amount  # 0
    add_state(steps, counter, "ComputeAmt", ctx)

    add_transition(steps, counter, "ProcessAmount(computedAmount)", "check")
    add_choice(steps, counter, "AmtCheck", "computedAmount >= 0", "Dispense", "valid")

    ctx.account_amount = ctx.computed_amount
    add_state(steps, counter, "Dispense", ctx)

    add_transition(steps, counter, "AccountStatus(accountAmount)", "check")
    add_choice(steps, counter, "AcctCheck", "accountAmount == 0", "CloseAccount", "zero")

    add_state(steps, counter, "CloseAccount", ctx)
    add_transition(
        steps, counter, "UserRemovedCard", "endSession",
        "User removes card; session ends with account closure processed."
    )
    add_state(steps, counter, "Idle", ctx)
    add_end(steps, counter, "Account closed - zero balance")

    return name, description, steps, ctx
# --------------------------------------------------------------------------------

# Registry of all scenario functions for iteration and menu display.
# Constraint: Order matches menu option numbers (1-9).
# Intent: Enable uniform execution via SCENARIOS[choice - 1].
SCENARIOS: list[ScenarioFunction] = [
    scenario_power_on_shutdown,              # 1: Power On → Shutdown
    scenario_invalid_card,                   # 2: Invalid Card
    scenario_valid_card_pin_success_account_positive,  # 3: Valid Card → PIN Success → Account > 0
    scenario_valid_card_pin_success_account_zero,      # 4: Valid Card → PIN Success → Account = 0
    scenario_clear_pin_loop,                 # 5: Clear PIN Loop → Success
    scenario_invalid_pin_then_success,       # 6: Invalid PIN → Retry → Success
    scenario_attempts_exhausted,             # 7: PIN Attempts Exhausted
    scenario_invalid_amount_then_success_positive,     # 8: Invalid Amount → Success (Account > 0)
    scenario_invalid_amount_then_success_zero,         # 9: Invalid Amount → Success (Account = 0)
]

# ______________________________________________________________________________
# Function Definitions
# ==============================================================================
# USER INTERFACE - DISPLAY UTILITIES
# ==============================================================================
# Contains functions for displaying information to the user:
# banners, menus, scenario output, and completion messages.
# These handle OUTPUT to the console with consistent formatting and colors.
# ==============================================================================
# Functions:
#   - render_title_banner: Create the main application title banner
#   - render_scenario_banner: Create scenario header banner with initial context
#   - render_footer_banner: Create scenario completion banner with final context
#   - render_scenarios_index: Create numbered list of available scenarios
#   - render_main_menu: Create interactive menu for scenario selection
#   - print_scenario: Execute and print a complete scenario ordered sequence
#   - print_completion_banner: Print all-scenarios-complete banner
#   - print_exit_banner: Print goodbye/exit banner
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_title_banner()
def render_title_banner() -> str:
    """Render the main application title banner.

    Logic:
        This function creates the header banner displayed at program start.
        1. Define banner content with centered title and subtitle lines.
        2. Include course/project identification.
        3. Delegate rendering to the Banner utility class.
    """
    content: list[tuple[str, str] | tuple[str, str, bool] | tuple[()]] = [
        ("ATM Operations", "center", True),
        ("State Machine Step-by-Step Execution", "center"),
        ("CSC-505 Portfolio Project - Module 7", "center"),
    ]
    return Banner(content).render()
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_scenario_banner()
def render_scenario_banner(name: str, description: str, ctx: Ctx) -> str:
    """Render a scenario header banner with initial context.

    Logic:
        This function creates a banner introducing each scenario ordered sequence.
        1. Format the context summary showing account balance and attempt count.
        2. Build banner content with scenario name, description, and context.
        3. Delegate rendering to the Banner utility class.
    """
    ctx_info: str = f"account=${ctx.account_amount}, attempt={ctx.attempt}"
    content: list[tuple[str, str] | tuple[str, str, bool] | tuple[()]] = [
        (f"Scenario: {name}", "center", True),
        (description, "center"),
        (),
        (f"Initial Context: {ctx_info}", "left"),
    ]
    return Banner(content).render()
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_footer_banner()
def render_footer_banner(result: str, ctx: Ctx) -> str:
    """Render a scenario footer banner with final context.

    Logic:
        This function creates a banner summarizing scenario completion.
        1. Format the final context summary showing ending state values.
        2. Build banner content with result and context information.
        3. Delegate rendering to the Banner utility class.
    """
    ctx_info: str = f"account=${ctx.account_amount}, attempt={ctx.attempt}"
    content: list[tuple[str, str] | tuple[str, str, bool] | tuple[()]] = [
        ("Scenario Complete", "center", True),
        (f"Result: {result}", "left"),
        (f"Final Context: {ctx_info}", "left"),
    ]
    return Banner(content).render()
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_scenarios_index()
def render_scenarios_index() -> str:
    """Render an index of all scenarios using Menu.

    Logic:
        This function creates a numbered list of available scenarios.
        1. Define the list of scenario names/descriptions.
        2. Delegate rendering to the Menu utility class.
    """
    scenarios: list[str] = [
        "Power On → Shutdown",
        "Invalid Card",
        "Valid Card → PIN Success → Withdraw → Account > 0",
        "Valid Card → PIN Success → Withdraw → Account = 0 (Close)",
        "Clear PIN Loop → PIN Success → Withdraw",
        "Invalid PIN → Retry → PIN Success → Withdraw",
        "PIN Attempts Exhausted → Card Rejected",
        "Invalid Withdraw Amount → Retry → Success (Account > 0)",
        "Invalid Withdraw Amount → Retry → Success (Account = 0)",
    ]
    menu: Menu = Menu("ATM Operation Scenarios", scenarios)
    return menu.render()
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- render_main_menu()
def render_main_menu() -> str:
    """Render the interactive scenario selection menu.

    Logic:
        This function creates the main menu for scenario selection.
        1. Define the list of scenario options including Exit.
        2. Delegate rendering to the Menu utility class.
    """
    options: list[str] = [
        "Power On → Shutdown",
        "Invalid Card",
        "Valid Card → PIN Success → Withdraw → Account > 0",
        "Valid Card → PIN Success → Withdraw → Account = 0 (Close)",
        "Clear PIN Loop → PIN Success → Withdraw",
        "Invalid PIN → Retry → PIN Success → Withdraw",
        "PIN Attempts Exhausted → Card Rejected",
        "Invalid Withdraw Amount → Retry → Success (Account > 0)",
        "Invalid Withdraw Amount → Retry → Success (Account = 0)",
        "Exit Program",
    ]
    menu: Menu = Menu("ATM Operations - Scenario Menu", options)
    return menu.render()
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- print_scenario()
def print_scenario(scenario_num: int, scenario_fn: ScenarioFunction) -> None:
    """Execute and print a single scenario.

    Logic:
        This function runs a scenario function and prints its formatted output.
        1. Execute the scenario function to get name, description, steps, and context.
        2. Determine initial context values based on scenario name for banner display.
        3. Print scenario header with separator lines and banner.
        4. Print all generated ordered-sequence steps.
        5. Determine result string and print footer banner.
    """
    # Step 1: Execute the scenario function
    name: str
    description: str
    steps: list[str]
    ctx: Ctx
    name, description, steps, ctx = scenario_fn()

    # Step 2: Determine initial context for banner display
    # DISPATCH: Select initial context based on scenario name pattern
    initial_ctx: Ctx = Ctx()
    if "Account = 0" in name or "close" in description.lower():
        # Account closure scenarios
        if "Amount" in name:
            initial_ctx = Ctx(account_amount=100, withdraw_amount=200)
        else:
            initial_ctx = Ctx(account_amount=100, withdraw_amount=100)
    elif "Invalid Amount" in name:
        # Invalid amount retry scenario (Account > 0 case)
        initial_ctx = Ctx(account_amount=100, withdraw_amount=150)
    elif "Exhausted" in name:
        # PIN exhaustion scenario
        initial_ctx = Ctx(account_amount=100, is_valid_pin=False)
    elif "Invalid Card" in name:
        # Invalid card scenario
        initial_ctx = Ctx(is_valid_card=False)
    elif "Invalid PIN" in name:
        # Invalid PIN retry scenario
        initial_ctx = Ctx(account_amount=100, withdraw_amount=25)
    elif "Clear PIN" in name:
        # Clear PIN loop scenario
        initial_ctx = Ctx(account_amount=100, withdraw_amount=30)
    elif "Account > 0" in name:
        # Successful withdrawal with remaining balance
        initial_ctx = Ctx(account_amount=100, withdraw_amount=50)

    # Step 3: Print scenario header
    print()
    print(f"{THEME.choice_node}{'─' * 70}{THEME.reset}")
    print(f"{THEME.success_path}  SCENARIO {scenario_num}{THEME.reset}")
    print(f"{THEME.choice_node}{'─' * 70}{THEME.reset}")
    print()
    print(render_scenario_banner(name, description, initial_ctx))
    print()

    # Step 4: Print all ordered-sequence steps
    for step in steps:
        print(step)

    # Step 5: Determine result string and print footer
    print()
    # DISPATCH: Select result string based on scenario name pattern
    result: str
    if "shutdown" in name.lower():
        result = "System shutdown"
    elif "invalid card" in name.lower():
        result = "Session ended - card rejected"
    elif "exhausted" in name.lower():
        result = "Card rejected - too many PIN attempts"
    elif "= 0" in name or "close" in description.lower():
        result = "Account closed"
    else:
        result = f"Transaction successful - remaining balance: ${ctx.account_amount}"

    print(render_footer_banner(result, ctx))
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- print_completion_banner()
def print_completion_banner() -> None:
    """Print the final completion banner.

    Logic:
        This function prints a banner indicating all scenarios are complete.
        1. Define banner content with completion message.
        2. Print separator lines with success color.
        3. Render and print the banner.
    """
    content: list[tuple[str, str] | tuple[str, str, bool] | tuple[()]] = [
        ("All Scenarios Complete", "center", True),
        (),
        ("All ATM operation paths have been sequenced", "center"),
        ("demonstrating the full state machine behavior", "center"),
    ]
    print()
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")
    print(Banner(content).render())
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- print_exit_banner()
def print_exit_banner() -> None:
    """Print the exit/goodbye banner.

    Logic:
        This function prints a farewell banner when exiting the program.
        1. Define banner content with thank you and goodbye messages.
        2. Print separator lines with success color.
        3. Render and print the banner.
    """
    content: list[tuple[str, str] | tuple[str, str, bool] | tuple[()]] = [
        ("Thank You!", "center", True),
        (),
        ("ATM Operations", "center"),
        ("Program terminated successfully", "center"),
        (),
        ("Goodbye!", "center"),
    ]
    print()
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")
    print(Banner(content).render())
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function Definitions
# ==============================================================================
# USER INTERFACE - INPUT PROMPTS
# ==============================================================================
# Contains functions for getting and validating user input from the console.
# These handle INPUT from the user with consistent validation and error handling.
# ==============================================================================
# Functions:
#   - get_menu_choice: Prompt for menu selection with range validation
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- get_menu_choice()
def get_menu_choice(max_choice: int = 10) -> int:
    """Prompt user for menu selection and validate input is in range 1-max_choice.

    Logic:
        This function handles user input for menu selection with validation.
        1. Loop until valid input is received.
        2. Use validate_prompt_int to get integer input from user.
        3. Check if input is within valid range (1 to max_choice).
        4. Print error message and retry if input is out of range.
        5. Return validated choice when input is valid.
    """
    # Validation loop: keep prompting until valid choice (1-max_choice) is entered
    while True:
        choice: int = validate_prompt_int(f"\nEnter your choice (1-{max_choice}): ")

        # VALIDATION: Check if choice is within valid range
        if 1 <= choice <= max_choice:
            return choice

        # Invalid choice - print error and re-prompt continues automatically
        print(
            f"{THEME.error_path}Invalid choice. "
            f"Please enter a number between 1 and {max_choice}.{THEME.reset}"
        )
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function Definitions
# ==============================================================================
# APPLICATION ORCHESTRATION
# ==============================================================================
# Contains the main program entry points.
# These functions coordinate the overall application flow.
# ==============================================================================
# Functions:
#   - run_interactive_menu: Main interactive loop with menu-driven scenario selection
#   - run_all_scenarios: Non-interactive mode that runs all scenarios sequentially
#   - main: Program entry point
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- run_interactive_menu()
def run_interactive_menu() -> None:
    """Run the interactive menu loop.

    Displays a menu allowing users to select individual scenarios to view.
    After viewing a scenario, prompts user to press Enter to return to menu.
    Option 10 exits the program.

    Logic:
        This function implements the main interactive loop for scenario selection.
        1. Display the title banner once at program start.
        2. Enter the main loop displaying the menu each iteration.
        3. Get user choice and handle exit (option 10) by printing exit banner.
        4. For options 1-9, execute the selected scenario function.
        5. Wait for user to press Enter before returning to menu.
    """
    # Step 1: Display title banner once at start
    print()
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")
    print(render_title_banner())
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")

    # MAIN ITERATION LOOP: Process user menu selections until exit
    while True:
        # Step 2: Display menu
        print()
        print(render_main_menu())

        # Step 3: Get user choice
        choice: int = get_menu_choice(10)

        # Step 4: Check for exit condition
        if choice == 10:
            # User selected Exit - print banner and break loop
            print_exit_banner()
            break

        # Step 5: Execute selected scenario (choice 1-9 maps to SCENARIOS index 0-8)
        print_scenario(choice, SCENARIOS[choice - 1])

        # Step 6: Wait for user to press Enter before returning to menu
        wait_for_enter()
# --------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- run_all_scenarios()
def run_all_scenarios() -> None:
    """Run all scenarios sequentially (non-interactive mode).

    This is the original behavior - prints all scenarios one after another.

    Logic:
        This function executes all scenarios in sequence without user interaction.
        1. Print the title banner at program start.
        2. Print the scenario index showing all available scenarios.
        3. Print separator and "beginning ordered sequences" message.
        4. Loop through all scenarios, executing and printing each one.
        5. Print the completion banner when all scenarios are done.
    """
    # Step 1: Print title banner
    print()
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")
    print(render_title_banner())
    print(f"{THEME.success_path}{'═' * 70}{THEME.reset}")
    print()

    # Step 2: Print scenario index
    print(f"{THEME.context_info}The following scenarios will be sequenced:{THEME.reset}")
    print()
    print(render_scenarios_index())
    print()

    # Step 3: Print separator
    print(f"{THEME.transition}{'━' * 70}{THEME.reset}")
    print(f"{THEME.transition}  Beginning scenario ordered sequences...{THEME.reset}")
    print(f"{THEME.transition}{'━' * 70}{THEME.reset}")

    # Step 4: Execute all scenarios
    for i, scenario_fn in enumerate(SCENARIOS, start=1):
        print_scenario(i, scenario_fn)

    # Step 5: Print completion banner
    print_completion_banner()
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Function Definitions
# ==============================================================================
# MAIN FUNCTION – Entry Point
# ==============================================================================
# The main() function serves as the primary entry point for the program. 
# ==============================================================================

# -------------------------------------------------------------------------------- main()
def main() -> None:
    """Main entry point - interactive menu for ATM operation scenarios.

    Logic:
        This function serves as the program entry point.
        1. Delegate to run_interactive_menu() for the main program loop.
    """
    run_interactive_menu()
    return None
# --------------------------------------------------------------------------------

# ==============================================================================
# MODULE INITIALIZATION
# ==============================================================================
if __name__ == "__main__":
    main()

# ______________________________________________________________________________
#
# ==============================================================================
# End of File
# ==============================================================================
