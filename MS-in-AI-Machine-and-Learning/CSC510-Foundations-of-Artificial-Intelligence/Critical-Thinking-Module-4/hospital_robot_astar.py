# -----------------------------------------------------------------------------
# Project: Hospital Medication Delivery Robot
# Module Type: executable script
# Author: Alexander S. Ricciardi
# Created: 2026-08-07
# Last Updated: 2026-08-14
# -----------------------------------------------------------------------------
# Course: CSC510 - Foundations of Artificial Intelligence
# Professor: Dr. Isaac Gang
# Term: Fall A (26FA) - 2026
# Assignment: Critical Thinking Module 4 - Informed Search Heuristics with SimpleAI
# -----------------------------------------------------------------------------
# My Project Description:
# The program uses A* search to find a low-cost route for a hospital medication-
# delivery robot. The robot avoids walls and accounts for normal corridors, busy
# corridors, and sanitation work zones.
# -----------------------------------------------------------------------------
# Assignment:
# Heuristic search functions used in Informed Search methods represent a compelling
# AI development strategy capable of performing many possible functions and solving
# a wide variety of problems.
#
# Please review the following resource:
# SimpleAI: https://pypi.org/project/simpleai/
#
# Examine the examples given under the "samples" directory in the SimpleAI GitHub page
# (available in the resource above).
#
# Define a simple real-world search problem requiring a heuristic solution.
# You can base the problem on the 8-puzzle (or n-puzzle) problem, Towers of Hanoi,
# or even Traveling Salesman. The problem and solution can be utilitarian or entirely inventive.
#
# Write an interactive Python script (using either SimpleAI's library or your resources)
# that utilizes Best-First Search, Greedy Best-First Search, Beam Search, or A* Search
# to calculate an appropriate output based on the proposed function.
# The search function does not have to be optimal or efficient, but it must define an
# initial state and a goal state and reliably find the action sequence leading to the goal.
# Submit an easily executable Python file alongside instructions for testing.
# Include the selected search algorithm and at least one paragraph
# justifying your choice. In your justification, consider the following questions as a guide:
#
# - Is your search method complete? Is it admissible?
# - Does it use an evaluation function?
# - Is it space-efficient?
# - What are the method's advantages and disadvantages for the intended function?
#
# References:
# - PyPI. (2021, September 2). SimpleAI (Version 0.8.3).
#
# -----------------------------------------------------------------------------
# Dependencies:
# - Standard Library: argparse, heapq, itertools, math, os, sys, textwrap, abc,
#   dataclasses, typing
#
# Requirements:
# - Python 3.11+
# -----------------------------------------------------------------------------

"""Plan a low-cost hospital medication-delivery route with A* graph search.

The program models the hospital floor as a finite weighted grid. Immutable
``(row, column)`` states are connected by cardinal movement actions, and entering
normal, busy, or sanitation-zone cells contributes the corresponding path cost.

A* prioritizes candidate nodes with ``f(n) = g(n) + h(n)``, where ``g(n)`` is the
exact accumulated route cost and ``h(n)`` is an admissible Manhattan-distance
estimate of the remaining cost. The interactive workflow reports the resulting
action sequence, route cost, and observed search statistics.
"""

from __future__ import annotations

# ____________________________________________________________________________________
# ====================================================================================
# ________________________________________________
# INFORMED A* SEARCH COMPONENT MAP
# ================================================
#
# The search problem defines WHAT happens:
# - state space: every state the robot may occupy,
# - initial state: state where search begins,
# - actions: available choices from a state,
# - transition model: a successor state produced by an action,
# - goal test: the condition that identifies success,
# - path cost: the exact cost accumulated by a sequence of actions, and
# - heuristic: domain knowledge that estimates the cost still remaining.
#
# A search algorithm defines the HOW:
#  - how the possible paths are explored.
#
# Note that:
# - An uninformed search has no heuristic, but it may use graph structure or known path costs.
# - An informed search uses a heuristic h(n) to estimate the remaining cost.
#
# A* is an informed best-first search. Here, "best" means the frontier node with
# the smallest estimated total route cost f(n), not necessarily the node with the
# smallest accumulated cost g(n) or the fewest movement steps.
#
# This program uses graph search, not tree search.
# - Tree search: may create many nodes for the same state
#   through different routes.
# - Graph search: stores the best discovered g value for each coordinate and
#   rejects equal-or-more-expensive g values for the same state.
#
#-------------------------------------------------------------------------------
# Math symbols - code representations:
#
# Mathematical symbol       Code representation
# -----------------------   ----------------------------------------------------
# n                         one SearchNode: state plus route metadata
# s                         state: immutable (row, column) coordinate
# s0                        s_initial_state
# sg                        s_goal_state
# s'                        s_successor_state
# a                         action: MOVE UP, MOVE RIGHT, MOVE DOWN, MOVE LEFT
# c(s, a, s')               step_cost
# g(n)                      g_path_cost
# h(n)                      h_estimated_remaining_cost
# f(n)                      f_evaluation_cost = g(n) + h(n)
# OPEN                      frontier_heap
# best_g[s]                 best_g_path_cost_by_state
# CLOSED/expanded record    expanded_g_path_cost_by_state
# parent(n)                 SearchNode.parent
#
# Distinction between a state and a node:
# - State s answers "Where is the robot?"
# - Node n answers "How did this candidate route reach s, and what does it cost?"
# Note: several nodes can represent the same state but can have different g values.
#
#-------------------------------------------------------------------------------
# A* EVALUATION EQUATION
#
#                       f(n) = g(n) + h(n)
#     cost from s0 to n --------^       ^-------- estimate from n to sg
#
# g(n) is known exactly for the route stored in node n. h(n) is an estimate.
#
# A* is not a Greedy Best-First Search or a Uniform-Cost Search:
# - Greedy Best-First uses only h(n).
# - Uniform-Cost Search uses only g(n).
# - A* combines both, balancing cost paid and estimated cost left.
#
#-------------------------------------------------------------------------------
# SimpleAI-like interface
#    it  defines the domain behavior
#
# actions(s) -> available actions
# result(s, a) -> successor state s'
# is_goal(s) -> whether s == sg
# cost(s, a, s') -> exact step cost
# heuristic(s) -> estimated remaining cost h(n)
#
#-------------------------------------------------------------------------------
# Hospital floor as a weighted state space
#
# The floor is modeled as a 2D array or grid containing different space types.
# The robot can move up, down, left, or right.
# Each move has a cost that depends on the type of cell being entered
# (normal, busy, or work zone).
# This creates a weighted graph where the weights represent the cost of moving into a cell.
#
# +-------------------+              action a           +-------------------+
# | current state s   | ----------------------------->  | successor state s'|
# | (row, column)     |                                 | (row', column')   |
# +-------------------+                                 +-------------------+
#          |                                                  |
#          | route g(n)                                       |  cost c
#          +-----------------------> g(n') = g(n) + c <-------+
#
#-------------------------------------------------------------------------------
# A* SEARCH PROCESS
#
# - OPEN contains possible routes that A* has discovered but not yet explored.
# - g(n) is the cost already paid to reach node n.
# - h(n) is the estimated remaining cost from node n to the goal.
# - f(n) = g(n) + h(n) is the estimated cost of the route through node n.
# - best_g[s] stores the cheapest route discovered so far to state s.
#
# Phase 0 - Start the search:
# - Create the initial node at the starting state s0.
# - Its route cost is g(s0) = 0 because the robot has not moved yet.
# - Calculate h(s0), the estimated cost from s0 to the goal.
# - Add the initial node to OPEN.
# - Record best_g[s0] = 0.
#
# Phase 1 - Choose a route:
# - Remove the node with the smallest f(n) from OPEN.
# - If multiple nodes have the same f(n), prefer the one with the smaller h(n).
# - If they are still tied, prefer the node that was inserted first.
#
# Phase 2 - Check if the route is still useful:
# - Skip node if A* has already discovered a cheaper route to its state.
# - If node provides a cheaper route to a previously explored state,
#   explore state again using the lower cost.
#
# Phase 3 - Check if the goal was reached:
# - Test whether the node's state is the goal state.
# - The test is performed when the node is removed from OPEN.
#
# Phase 4 - Explore the state:
# - Find every movement the robot can make from the state.
# - For each movement, determine the resulting state and movement cost.
#
# Phase 5 - Evaluate each resulting state:
# - Calculate the new route cost:
#
#       new_g = current g + movement cost
#
# - Compare new_g with the cheapest known cost stored in best_g.
# - Keep the resulting state only if the new route is cheaper.
# - Calculate its estimated remaining cost h(n).
# - Create a new node that points back to its parent node.
# - Add the new node to OPEN so A* can consider it later.
#
# Repeat Phases 1 through 5 until A* reaches the goal or OPEN becomes empty.
#
#-------------------------------------------------------------------------------
# Program heuristic
#
# h(n) = Manhattan distance * minimum move cost
#
# It is Admissible means h(n) never exceeds the true cheapest cost h*(n).
# It is Consistent means h(s) <= c(s, a, s') + h(s') for every edge.
# Manhattan distance is a lower bound cost as it ignores walls,
# detours, and terrain penalties and assumes every remaining move costs
# the minimum 1.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

import argparse
import heapq
import itertools
import math
import os
import sys
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, Iterable, Sequence


# __________________________________________
# TYPES
# ==========================================

# Coordinate is the complete problem state s. A tuple is immutable and hashable,
# so it can safely serve as a key in the graph-search cost dictionaries.
# For example, (1, 1) means row 1 and column 1.
# To move RIGHT increment the column value. To move LEFT decrement the column value.
# To move DOWN increment the row value. To move UP decrement the row value.
Coordinate = tuple[int, int]

# Action is a string that represents one movement command, such as "MOVE UP".
Action = str

# PathEntry is similar to SimpleAI-style output:
# - the action taken from the preceding state
# - the state reached
# Note that the initial entry uses action None because no move
# is required to occupy s0.
PathEntry = tuple[Action | None, Coordinate]


# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

PROGRAM_NAME: Final[str] = "Hospital Medication Delivery Robot"
PROGRAM_VERSION: Final[str] = "1.0.0"
DISPLAY_WIDTH: Final[int] = 92

# Floating-point rounding errors may occur when route costs are compared.
# FLOAT_COMPARISON_TOLERANCE determines when two stored costs are treated as equal.
# This tolerance is used only for
# comparisons; it is never subtracted from the actual route cost.
FLOAT_COMPARISON_TOLERANCE: Final[float] = 1e-12

# Console settings modified by command-line presentation flags.
USE_CONSOLE_COLORS: bool = True
PAUSE_BETWEEN_SECTIONS: bool = True

# ANSI formatting codes.
# See https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
ANSI_RESET: Final[str] = "\033[0m"
ANSI_BOLD: Final[str] = "\033[1m"
ANSI_DIM: Final[str] = "\033[2m"
ANSI_RED: Final[str] = "\033[31m"
ANSI_GREEN: Final[str] = "\033[32m"
ANSI_YELLOW: Final[str] = "\033[33m"
ANSI_BLUE: Final[str] = "\033[34m"
ANSI_MAGENTA: Final[str] = "\033[35m"
ANSI_CYAN: Final[str] = "\033[36m"
ANSI_DEFAULT: Final[str] = "\033[39m"

# __________________________________________
# HOSPITAL FLOOR MAP
# ==========================================
#
# The grid is a 2D array of characters that represents a weighted graph:
# - each passable character position is one state s = (row, column),
# - each cardinal (north, south, east, west) move is an edge from s to s',
# - each wall removes a coordinate or state from the traversable state space, and
# - the destination symbol determines edge cost c(s, a, s').
#
# symbols:
#   # = wall; blocked
#   . = normal corridor; cost 1
#   ~ = busy corridor; cost 3
#   ! = sanitation work zone; cost 6
#   P, N, L, E, S, C = named locations; cost 1
#
# The map is finite and rectangular. The outer wall also prevents a movement
# action from leaving the represented floor.

HOSPITAL_FLOOR_MAP: Final[tuple[str, ...]] = (
    "#################################",
    "#P..............#..............N#",
    "#.###########...#...###########.#",
    "#...............#...............#",
    "#.#####.#################.#####.#",
    "#.....#.......~~~.......#.......#",
    "#####.#.#####.~~~.#####.#.#######",
    "#.....#.....#.~~~.#.....#.......#",
    "#.#########.#.~~~.#.###########.#",
    "#...........#.!!!.#.............#",
    "#.###########.!!!.###########...#",
    "#L............!!!............E..#",
    "#.###############.#############.#",
    "#S.............................C#",
    "#################################",
)

LOCATION_NAME_BY_CODE: Final[dict[str, str]] = {
    "P": "Pharmacy",
    "N": "Nurses' Station",
    "L": "Laboratory",
    "E": "Emergency Department",
    "S": "Medical Supply Room",
    "C": "Robot Charging Station",
}

TERRAIN_NAME_BY_SYMBOL: Final[dict[str, str]] = {
    ".": "normal corridor",
    "~": "busy corridor",
    "!": "sanitation work zone",
}

# Cost for each type of terrain.
TERRAIN_COST_BY_SYMBOL: Final[dict[str, float]] = {
    ".": 1.0,
    "~": 3.0,
    "!": 6.0,
}

# Normal corridor traversal cost, moving from one coordinate to an adjacent one
# without moving into a wall, busy corridor, or sanitation work zone.
LOCATION_TRAVERSAL_COST: Final[float] = 1.0

# Scale Manhattan distance by the minimum cost of any legal move so the heuristic
# remains a lower bound. The value matches LOCATION_TRAVERSAL_COST on this map.
MINIMUM_TRAVERSAL_COST: Final[float] = 1.0

# ACTION_DELTAS maps each movement command to a (row change, column change).
# Negative rows move up, positive rows move down, negative columns move left,
# and positive columns move right.
ACTION_DELTAS: Final[dict[Action, Coordinate]] = {
    "MOVE UP": (-1, 0),
    "MOVE RIGHT": (0, 1),
    "MOVE DOWN": (1, 0),
    "MOVE LEFT": (0, -1),
}

# ACTION_ORDER sets the fixed order in which the robot checks possible
# movements. This is necessary to ensure that the robot explores the search
# space in a consistent order.
ACTION_ORDER: Final[tuple[Action, ...]] = (
    "MOVE UP",
    "MOVE RIGHT",
    "MOVE DOWN",
    "MOVE LEFT",
)

# Map each action to the character used in the compact action-sequence string.
ACTION_ARROW_BY_NAME: Final[dict[Action, str]] = {
    "MOVE UP": "U",
    "MOVE RIGHT": "R",
    "MOVE DOWN": "D",
    "MOVE LEFT": "L",
}

# Default start and goal codes. If the user doesn't provide start and goal codes.
DEFAULT_START_CODE: Final[str] = "P"
DEFAULT_GOAL_CODE: Final[str] = "E"

# This sets the expected cost of the default Pharmacy-to-Emergency route. It is
# used to verify that the A* algorithm is working correctly.
DEFAULT_ROUTE_EXPECTED_COST: Final[float] = 44.0


# ====================================================================================
# __________________________________________
# CLASSES
# ==========================================

# __________________________________________
# ABSTRACT CLASSES
# ==========================================

# ____________________________________________________________________________________
# ====================================================================================
# SIMPLEAI-STYLE SEARCH INTERFACE
# ====================================================================================
#
# This interface provides the information that the A* search needs to solve the
# search problem. The hospital robot problem provides the states, legal actions,
# state transitions, movement costs, goal test, and heuristic estimate.
#
# - actions(state): Return the actions available from a state.
# - result(state, action): Return the state produced by an action.
# - is_goal(state): Return True when the state is the goal.
# - cost(state, action, state2): Return the exact cost of the movement.
# - heuristic(state): Estimate the remaining cost to the goal.
# --- class SearchProblem

# Abstract base class, also called an interface in other languages such as Java.
# It is used to define a contract between the search algorithm and the problem domain.
class SearchProblem(ABC):
    """Define the domain operations required by this project's A* search.

    This interface follows the SimpleAI SearchProblem pattern.

    Attributes:
        initial_state: Immutable state from which the search begins.

    Logic:
        1. Store the initial state s0.
        2. Define actions, transitions, and a goal.
        3. Provide cost and heuristic for A* search.

    """

    # --- __init__()
    def __init__(self, initial_state: Coordinate) -> None:
        """Store the initial state s0.

        Args:
            initial_state: s0.
        """
        self.initial_state = initial_state
    # ---

    # --- actions()
    @abstractmethod # This is used to force subclasses to implement this method.
    def actions(self, state: Coordinate) -> Iterable[Action]:
        """Return every legal action available from state ``s``.

        Args:
            state: Current state ``s``.

        Returns:
            Actions ``a``.
        """
    # ---

    # --- result()
    @abstractmethod # This is used to force subclasses to implement this method.
    def result(self, state: Coordinate, action: Action) -> Coordinate:
        """Return successor state ``s'`` after applying action ``a`` to ``s``.

        Args:
            state: Current state ``s``.
            action: Domain operator ``a``.

        Returns:
            Successor state ``s'``.

        """
    # ---

    # --- is_goal()
    @abstractmethod # This is used to force subclasses to implement this method.
    def is_goal(self, state: Coordinate) -> bool:
        """Return if state ``s`` satisfies the goal condition ``s == sg``.

        """
    # ---

    # --- cost()
    # Concrete weighted problems may override this unit-cost default.
    def cost(
        self,
        state: Coordinate,
        action: Action,
        state2: Coordinate,
    ) -> float:
        """Return edge cost ``c(s, a, s')``; default to one unit."""
        del state, action, state2 # deleted, replaced by Manhattan distance heuristic in HospitalRobotSearchProblem
        return 1.0 # replaced by Manhattan distance heuristic in HospitalRobotSearchProblem
    # ---

    # --- heuristic()
    # Concrete informed problems may override this zero-heuristic default.
    def heuristic(self, state: Coordinate) -> float:
        """Return estimated remaining cost ``h(n)``; zero gives uniform-cost search."""
        del state # deleted, replaced by Manhattan distance heuristic in HospitalRobotSearchProblem
        return 0.0 # replaced by Manhattan distance heuristic in HospitalRobotSearchProblem
    # ---
# --- end class SearchProblem

# __________________________________________
# DATA CLASSES
# ==========================================

# ____________________________________________________________________________________
# ====================================================================================
# SEARCH NODE AND RESULT RECORDS
# ====================================================================================
#
# A STATE is a domain configuration: here, it is a coordinate.
#
# SearchNode stores one route prefix:
#
#   parent --action--> state
#      |                 |
#      |                 +--> g: exact prefix cost
#      |                 +--> h: estimated remaining cost
#      |                 +--> f: g + h
#      +--> another SearchNode, continuing backward toward s0
#
# SearchNode stores one route prefix. SearchStatistics records observed frontier
# and expansion counts. SearchResult combines a successful goal node with those
# measurements.

# --- class SearchNode
# @dataclass is a decorator that generates methods for a class.
# slots=True makes the class more memory-efficient.
@dataclass(slots=True)
class SearchNode:
    """Store one state and its route information in the A* search tree.

    Attributes:
        state: Problem state ``s`` contained in this node ``n``.
        parent: Previous node in the path from ``s0`` to ``sn``.
        action: Action that produced this node from its parent.
        g_path_cost: Exact accumulated route cost ``g(n)``.
        h_estimated_remaining_cost: Heuristic estimate ``h(n)``.
        depth: Number of movement actions from the initial state.

    """

    state: Coordinate
    parent: SearchNode | None
    action: Action | None
    g_path_cost: float
    h_estimated_remaining_cost: float
    depth: int

    # --- f_evaluation_cost()
    @property # Ready only property 
    def f_evaluation_cost(self) -> float:
        """Return the A* value f(n) = g(n) + h(n).

        """
        return self.g_path_cost + self.h_estimated_remaining_cost
    # ---

    # --- path_nodes()
    def path_nodes(self) -> list[SearchNode]:
        """Return a list of nodes from the initial state ``s0`` to this node ``sn``.

        This method is mainly used to reconstruct the path from a goal node ``sg`` back to the initial
        state ``s0``, then reverses it into forward route order.

        Returns:
            Linked nodes in ``s0-to-sn`` order.

        Logic:
            1. Begin at the current node ``sn``.
            2. Follow parent pointers backward until the root's None parent.
            3. Reverse the collected ``s0-to-sn`` sequence into path order.
        """
        reversed_nodes: list[SearchNode] = []
        current_node: SearchNode | None = self

        # Follow the parent chain from this node back to s0.
        while current_node is not None:
            reversed_nodes.append(current_node)
            current_node = current_node.parent

        # Reverse the collected s0-to-sn sequence into path order.
        reversed_nodes.reverse()
        return reversed_nodes
    # ---

    # --- path()
    def path(self) -> list[PathEntry]:
        """Return (action, state)

        The initial pair at ``s0`` is (None, s0).
        """
        return [(node.action, node.state) for node in self.path_nodes()]
    # ---
# --- end class SearchNode

# --- class SearchStatistics
# @dataclass is a decorator that generates methods for a class.
# frozen=True makes the class immutable, slots=True makes the class more memory-efficient.
@dataclass(frozen=True, slots=True) 
class SearchStatistics:
    """Store algorithm performance metrics.

    Attributes:
        expanded_nodes: Number of nodes whose outgoing actions were examined.
        generated_nodes: Number of nodes inserted into the frontier, including the start node.
        stale_frontier_entries_skipped: Number of queued routes superseded before expansion.
        reopened_states: Number of expanded states later reached through a cheaper route.
        maximum_frontier_size: Largest number of queued entries held at once.
        unique_states_discovered: Coordinates assigned at least one best-g value.
    """

    expanded_nodes: int
    generated_nodes: int
    stale_frontier_entries_skipped: int
    reopened_states: int
    maximum_frontier_size: int
    unique_states_discovered: int
# --- end class SearchStatistics

# --- class SearchResult
# @dataclass is a decorator that generates methods for a class.
# frozen=True makes the class immutable, slots=True makes the class more memory-efficient.
@dataclass(frozen=True, slots=True)
class SearchResult:
    """Container for the goal node and metrics returned by astar_search().

    """

    goal_node: SearchNode
    statistics: SearchStatistics

    # --- state()
    @property
    def state(self) -> Coordinate:
        """Return the final goal state, matching SimpleAI result usage."""
        return self.goal_node.state
    # ---

    # --- path()
    def path(self) -> list[PathEntry]:
        """Return the sequence from initial state to goal state."""
        return self.goal_node.path()
    # ---

    # --- path_nodes()
    def path_nodes(self) -> list[SearchNode]:
        """Return detailed nodes with ``g``, ``h``, and parent information."""
        return self.goal_node.path_nodes()
    # ---
# --- end class SearchResult

# __________________________________________
# REGULAR CLASSES
# ==========================================

# ____________________________________________________________________________________
# ====================================================================================
# HOSPITAL ROBOT SEARCH PROBLEM
# ====================================================================================
#
# Domain idea                         Search representation
# ----------------------------------  -------------------------------------------
# Robot position                      state s = (row, column)
# Selected departure                  initial state s0
# Selected delivery department        goal state sg
# One cardinal movement               action a
# Coordinate offset                   result(s, a) = s'
# Wall or map boundary                illegal successor constraint
# Time/risk proxy for entered cell    cost c(s, a, s')
# Straight-line grid progress         heuristic h(n)
#
# ASSIGNMENT REQUIREMENT: Define a real-world problem with explicit initial and
# goal states, actions, transitions, meaningful constraints, costs, and heuristic.

# --- class HospitalRobotRouteProblem
class HospitalRobotRouteProblem(SearchProblem):
    """Define the weighted path cost search problem for a hospital robot.

    The Real-World Search Problem:
        A medication delivery robot must move in hospital space from a start
        position to a goal position. The robot cannot cross walls. Normal corridors
        are preferred over busy corridors and sanitation work zones.

    State:
        An immutable (row, column) coordinate.

    Initial State:
        The coordinate chosen as the robot's starting location.

    Goal State:
        The coordinate chosen as the delivery destination.

    Actions:
        MOVE UP, MOVE RIGHT, MOVE DOWN, and MOVE LEFT

    Cost Function:
        The cost of the move is the cost of the cell entered:
            1 for normal corridor or a named location,
            3 for a busy corridor,
            6 for a sanitation work zone.

    Heuristic: h(n)
        Manhattan distance to the goal multiplied by the minimum move cost.

        h(n) = (|row - goal_row| + |column - goal_column|) * 1

        This heuristic is admissible because each four-direction step
        costs at least one unit. It is also consistent because one legal move can
        change Manhattan distance by at most one and every legal move costs at
        least one unit.

    Core Equations:
        s' = (row + delta_row, column + delta_column)
        g(n') = g(n) + c(s, a, s')
        h(n) = Manhattan(s, sg) * c_min
        f(n) = g(n) + h(n)

    Conceptual Boundary:
        This class defines the domain graph and heuristic. It does not own OPEN,
        compare ``f`` values, remember expanded states, or reconstruct the path.
    """

    # --- __init__()
    def __init__(
        self,
        floor_map: Sequence[str],
        initial_state: Coordinate,
        goal_state: Coordinate,
    ) -> None:
        """Validate and store the map, initial state ``s0``, and goal ``sg``.

        Args:
            floor_map: Rectangular grid of walls, corridors, and named locations.
            initial_state: Starting coordinate ``s0``.
            goal_state: Goal coordinate ``sg``.

        Raises:
            ValueError: If the map or selected states are invalid.

        Logic:
            1. Validate the static state-space representation.
            2. Store an immutable map snapshot and its dimensions.
            3. Validate that ``s0`` and ``sg`` are passable states.
            4. Initialize the abstract problem with ``s0``.
        """
        # VALIDATION: Search assumptions depend on a rectangular, known-symbol map.
        validate_floor_map(floor_map)

        # Copy the supplied rows into an immutable tuple so the problem's state
        # space cannot change during a search run.
        self.floor_map: tuple[str, ...] = tuple(floor_map)
        self.row_count: int = len(self.floor_map)
        self.column_count: int = len(self.floor_map[0])

        # ASSIGNMENT REQUIREMENT: Store the explicitly selected goal state sg.
        self.goal_state: Coordinate = goal_state

        # VALIDATION: Both endpoints must be legal states in the same graph that
        # actions(), cost(), and heuristic() will use.
        if not self.is_passable(initial_state):
            raise ValueError("the initial state must be a passable map coordinate")
        if not self.is_passable(goal_state):
            raise ValueError("the goal state must be a passable map coordinate")

        # ASSIGNMENT REQUIREMENT: Pass the selected initial state s0 to the shared
        # SearchProblem contract used by astar_search().
        super().__init__(initial_state=initial_state)
    # ---

    # --- is_inside_map()
    def is_inside_map(self, state: Coordinate) -> bool:
        """Return whether ``state`` is within the hospital grid.

        """
        row, column = state
        return 0 <= row < self.row_count and 0 <= column < self.column_count
    # ---

    # --- symbol_at()
    def symbol_at(self, state: Coordinate) -> str:
        """Return the floor-map symbol at ``state``.

        Raises:
            ValueError: If ``state`` is outside the map.
        """
        if not self.is_inside_map(state):
            raise ValueError(f"state {state} is outside the hospital map")

        row, column = state
        return self.floor_map[row][column]
    # ---

    # --- is_passable()
    def is_passable(self, state: Coordinate) -> bool:
        """Return whether the robot can legally enter ``state``.

        """
        return self.is_inside_map(state) and self.symbol_at(state) != "#"
    # ---

    # --- actions()
    def actions(self, state: Coordinate) -> tuple[Action, ...]:
        """Return valid four-direction movement actions from ``state``.

        UP, DOWN, LEFT, RIGHT 
        corresponds to (row-1,col), (row+1,col), (row,col-1), (row,col+1).
        or north, south, west, and east

        Related Operation:
            For each candidate action ``a``, calculate ``s' = result(s, a)`` and
            keep the action only when ``s'`` is passable.

        """
        valid_actions: list[Action] = []

        # ASSIGNMENT REQUIREMENT MET: the four candidate robot actions
        # and return only movements whose successor state is legal.
        for action in ACTION_ORDER:
            # Step 1: Transition ``result(s, a) -> s'``.
            successor_state = self.result(state, action)

            # Step 2: map-boundary and wall constraints on ``s'``.
            if self.is_passable(successor_state):
                valid_actions.append(action)

        return tuple(valid_actions)
    # ---

    # --- result()
    def result(self, state: Coordinate, action: Action) -> Coordinate:
        """Return successor state ``s'`` after one movement action.

        Related Equation:
            s' = (row + delta_row, column + delta_column)

        Raises:
            ValueError: If ``action`` is unknown.
        """
        if action not in ACTION_DELTAS:
            raise ValueError(f"unknown robot action: {action!r}")

        # Extract ``row``, ``column``, and the action's coordinate offset
        row, column = state
        delta_row, delta_column = ACTION_DELTAS[action]

        # ASSIGNMENT REQUIREMENT MET: Apply ``a`` to ``s`` to construct successor ``s'``.
        # s' = (row + delta_row, column + delta_column)
        successor_state = (row + delta_row, column + delta_column)
        return successor_state
    # ---

    # --- is_goal()
    def is_goal(self, state: Coordinate) -> bool:
        """Return whether state ``s`` equals the selected goal state ``sg``.

        Related Equation:
            is_goal(s) = (s == sg)
        """
        # ASSIGNMENT REQUIREMENT MET: Success is defined by reaching sg exactly.
        return state == self.goal_state
    # ---

    # --- cost()
    def cost(
        self,
        state: Coordinate,
        action: Action,
        state2: Coordinate,
    ) -> float:
        """Return exact traversal cost ``c(s, a, s')``.

        The cost belongs to the destination cell. This lets the planner prefer a
        slightly longer clear route when a shorter route crosses expensive areas.

        Related Equation:
            g(n') = g(n) + c(s, a, s')

        Raises:
            ValueError: If ``state2`` does not match the action result or is blocked.
        """
        # VALIDATION: The requested edge must agree with the transition model.
        expected_state2 = self.result(state, action)
        if state2 != expected_state2:
            raise ValueError("state2 does not match result(state, action)")

        # VALIDATION: Blocked cells are not graph vertices the robot may enter; walls are not.
        if not self.is_passable(state2):
            raise ValueError("the robot cannot calculate a move cost into a wall")

        # The assignment's weighted-cost model charges for entering ``s'``, not for
        # leaving s. The same rule is used during search and path-cost auditing.
        destination_symbol = self.symbol_at(state2)
        
        # If the destination symbol is a location code, return the location traversal cost.
        # else return the terrain cost for that symbol. (the weighted cost model)
        if destination_symbol in LOCATION_NAME_BY_CODE:
            return LOCATION_TRAVERSAL_COST

        return TERRAIN_COST_BY_SYMBOL[destination_symbol]
    # ---

    # --- heuristic()
    def heuristic(self, state: Coordinate) -> float:
        """Return admissible Manhattan estimate ``h(n)`` to the goal.

        Related Equation:
            h(n) = (abs(row - goal_row) + abs(column - goal_column)) * c_min

        Equation Relationship:
            The Manhattan distance counts the fewest possible four-direction moves 
            ignoring wall/obstruction and terrain penalties. It is multiplied by the minimum
            legal move cost.

        Why It Is Admissible:
            Ignoring walls and expensive terrain makes the estimate optimistic.
            Every real remaining move costs at least ``c_min``, so ``h(n)`` cannot
            exceed the true lowest possible remaining cost ``h*(n)``.

        Why It Is Consistent:
            One cardinal move changes Manhattan distance by at most ``1``, and its
            cost is at least ``c_min``. Therefore every legal edge is
            ``h(s) <= c(s, a, s') + h(s')``.
        """
        # Step 1: Decompose the current state s and goal state sg.
        row, column = state
        goal_row, goal_column = self.goal_state

        # Step 2: Count the minimum number of cardinal coordinate changes if
        # obstacles and terrain types are temporarily ignored.
        manhattan_distance = abs(row - goal_row) + abs(column - goal_column)

        # Step 3: Convert geometric distance to a cost lower bound with c_min.
        h_estimated_remaining_cost = (
            manhattan_distance * MINIMUM_TRAVERSAL_COST
        )
        return h_estimated_remaining_cost
    # ---
# --- end class HospitalRobotRouteProblem

# ====================================================================================
# __________________________________________
# FUNCTIONS
# ==========================================

# ____________________________________________________________________________________
# ====================================================================================
# A* GRAPH SEARCH
# ====================================================================================
#
# A* is a BEST-FIRST search; it evaluates nodes, not edges, and expands them in order.
# It is INFORMED because h(n) adds to the domain knowledge about the goal. 
# It is COST-AWARE because g(n) stores the exact cost paid from the start state.
# It is GRAPH SEARCH because costs are remembered by state.
#
# A* does not simply choose the neighbor with the smallest h value. It uses the evaluation
# function f(n) = g(n) + h(n) to evaluate each node. g(n) is the actual cost from the
# start state to state n, and h(n) is an estimate of the cost from state n to the
# goal state.
#
# --------------------------------
# A* Evaluation Function
# --------------------------------
# 
# The following invariant prevents A* from wasting time on more expensive duplicate routes:
#   
#   best_g_path_cost_by_state[s] = lowest discovered route cost to state s
#
# For example, suppose A* discovers three routes to (5, 7):
# First route:  cost 12 → store 12
# Second route: cost 9  → replace 12 with 9
# Third route:  cost 11 → reject it because 9 is better
#
# A successor node n' is competitive only when its path cost g(n') is
# lower than best_g[s']. 
# This is done before adding n' to OPEN.
# Older, more expensive nodes still in the priority queue are skipped later as stale.
#
# Ordering used by priority queue (heapq):
#
#   (f(n), h(n), insertion_order, SearchNode)
#
# Python compares tuple elements from left to right. 
#  - The smallest f is primary.
#  - smaller h breaks an f tie.
#  - insertion order makes exact ties stable.
# The integer counter also prevents Python from trying to order SearchNode objects.
#
# --- astar_search()
def astar_search(problem: SearchProblem) -> SearchResult | None:
    """Find a least-cost goal route with A* graph search.

    Evaluation Function:
        ``f(n) = g(n) + h(n)``

        ``g(n)`` stores the exact cost of the route prefix from the start state to state ``n``.
        ``h(n)`` stores an estimate of the remaining cost from state ``n`` to the goal state.
        ``f(n)`` is the estimated total cost of the path through ``n``.

    Priority Selection:
        Remove from the frontier the node with the smallest ``f(n)``. A counter 
        breaks exact ties without comparing node objects.

    Repeated State:
        ``best_g_path_cost_by_state`` stores the lowest discovered ``g`` for each
        state. A successor is inserted only if its new ``g`` is lower.

    Search Phases:
        1. Initialize the start node and OPEN frontier.
        2. Select the node with minimum ``(f, h, insertion order)``.
        3. Return when the selected node satisfies the goal test.
        4. Expand legal actions and calculate successor ``g`` values.
        5. Relax improved successors, calculate ``h``, and add them to OPEN.
        6. Report failure only after OPEN is empty.

    Args:
        problem: Search problem that provides states, actions, transitions, costs,
            goal test, and heuristic values.

    Returns:
        SearchResult containing the goal route and observed statistics, or
        None when no reachable goal exists.

    """
    # __________________________________________
    # PHASE 0: INITIALIZE THE SEARCH
    # ==========================================

    # s0 is the root state. No action or edge cost precedes it, so g(s0) = 0.
    s_initial_state = problem.initial_state

    # Ask the domain for its optimistic remaining-cost estimate at s0.
    h_initial_estimated_remaining_cost = problem.heuristic(s_initial_state)

    # SAFETY CHECK: Non-finite or negative values make frontier ordering undefined
    if not math.isfinite(h_initial_estimated_remaining_cost):
        raise ValueError("the initial heuristic value must be finite")
    if h_initial_estimated_remaining_cost < 0.0:
        raise ValueError("heuristic values must not be negative")

    # The root has no parent and no previous action. Its f value is 0 + h(s0).
    initial_node = SearchNode(
        state=s_initial_state,
        parent=None,
        action=None,
        g_path_cost=0.0,
        h_estimated_remaining_cost=h_initial_estimated_remaining_cost,
        depth=0,
    )

    # OPEN FRONTIER: generated routes that have not yet been selected.
    frontier_heap: list[tuple[float, float, int, SearchNode]] = []
    insertion_counter = itertools.count()

    # ASSIGNMENT REQUIREMENT MET: Queue s0 by the A* evaluation f(s0) = g + h.
    # Priority is (f_evaluation_cost, h_estimated_remaining_cost, insertion_order, node)
    heapq.heappush(
        frontier_heap,
        (
            initial_node.f_evaluation_cost,
            initial_node.h_estimated_remaining_cost,
            next(insertion_counter),
            initial_node,
        ),
    )

    # DISCOVERED-STATE MEMORY:
    # best_g contains the cheapest route discovered to each state, whether or not
    # that state has already been expanded. It is the main duplicate-state rule.
    best_g_path_cost_by_state: dict[Coordinate, float] = {
        s_initial_state: 0.0,
    }

    # EXPANDED-STATE MEMORY: expanded_g records the g value used the last time
    # outgoing edges were examined. A later lower g reopens the state; an 
    # equal or higher g is stale.
    expanded_g_path_cost_by_state: dict[Coordinate, float] = {}

    # Runtime counters 
    expanded_nodes = 0          # number of nodes removed from the frontier
    generated_nodes = 1         # number of nodes added to the frontier
    stale_frontier_entries_skipped = 0  # number of stale nodes skipped
    reopened_states = 0         # number of states re-added to the frontier
    maximum_frontier_size = 1   # maximum number of nodes in the frontier

    # __________________________________________
    # MAIN ITERATION LOOP: SELECT AND EXPAND
    # ==========================================
    # Continue until a selected node is the goal or no candidate route remains.
    while frontier_heap:
        # PHASE 1 - SELECT: heapq removes the smallest f, then h, then insertion
        # order. The ignored tuple fields have already performed their ranking job;
        # the selected SearchNode retains the route information used below.
        _, _, _, current_node = heapq.heappop(frontier_heap)
        s_current_state = current_node.state
        g_current_path_cost = current_node.g_path_cost

        # PHASE 2 - DISCARD superseded frontier entries.
        # heapq has no direct decrease-key. When a cheaper route to the same state
        # is found, the new node is pushed and the old node remains in OPEN. 
        # Comparing its g with best_g.
        best_known_g_path_cost = best_g_path_cost_by_state[s_current_state]
        if g_current_path_cost > (
            best_known_g_path_cost + FLOAT_COMPARISON_TOLERANCE
        ):
            stale_frontier_entries_skipped += 1
            continue

        # PHASE 3 - GOAL TEST THE SELECTED NODE.
        # The test occurs on removal from OPEN, not when a goal successor is first
        # generated. With this problem's consistent heuristic, the selected goal
        # has minimum route cost; an arbitrary first-generated goal may not.
        if problem.is_goal(s_current_state):
            # SearchStatistics records resource use at the exact stopping point.
            statistics = SearchStatistics(
                expanded_nodes=expanded_nodes,
                generated_nodes=generated_nodes,
                stale_frontier_entries_skipped=stale_frontier_entries_skipped,
                reopened_states=reopened_states,
                maximum_frontier_size=maximum_frontier_size,
                unique_states_discovered=len(best_g_path_cost_by_state),
            )

            return SearchResult(goal_node=current_node, statistics=statistics)

        # REOPENING CHECK: (Defensive) consistent heuristic
        # A state is expanded when A* examines its outgoing actions.
        # The first expansion should already use the state's lowest-cost route.
        # As a defensive measure, if a cheaper route to an expanded state is discovered,
        # reopen and expand that state again using the improved cost.
        # Skip equal or more expensive rediscoveries.
        previous_expanded_g_path_cost = expanded_g_path_cost_by_state.get(
            s_current_state,
        )
        # If the current path cost is greater than the previous expanded g_path_cost,
        # then the current path is stale and should be skipped.
        # Skip equal or more expensive rediscoveries.
        if previous_expanded_g_path_cost is not None:
            if g_current_path_cost >= (
                previous_expanded_g_path_cost - FLOAT_COMPARISON_TOLERANCE
            ):
                stale_frontier_entries_skipped += 1 # Count stale nodes skipped
                continue
            reopened_states += 1 # Count reopened states

        # Mark this g as the version whose outgoing graph edges are being expanded.
        expanded_g_path_cost_by_state[s_current_state] = g_current_path_cost
        expanded_nodes += 1 # Count expanded nodes

        # PHASE 4 - EXPAND THE STATE.
        for action in problem.actions(s_current_state):
            # Step 1: Apply the transition model result(s, a) -> s'.
            s_successor_state = problem.result(s_current_state, action)

            # Step 2: Obtain the exact cost of this one graph edge (n, n').
            step_cost = problem.cost(
                s_current_state,
                action,
                s_successor_state,
            )

            # SAFETY CHECK: completeness
            # Positive finite costs are required by the completeness
            # and route-order reasoning stated for this implementation.
            if not math.isfinite(step_cost) or step_cost <= 0.0:
                raise ValueError("A* requires every action cost to be positive and finite")

            # PHASE 5 - RELAX THE SUCCESSOR.
            # "Relax" means test whether this edge supplies a cheaper known route.
            # Step 3: g(n') = g(n) + c(s, a, s').
            g_successor_path_cost = g_current_path_cost + step_cost

            # Infinity means s' has not yet been discovered, so its first finite
            # route necessarily improves the stored value.
            previous_best_successor_g = best_g_path_cost_by_state.get(
                s_successor_state,
                math.inf,
            )

            # Step 4: Reject equal-or-more-expensive duplicates. Keeping only a
            # strict improvement prevents cycles such as LEFT then RIGHT from
            # generating an endless sequence of equivalent route prefixes.
            if g_successor_path_cost >= (
                previous_best_successor_g - FLOAT_COMPARISON_TOLERANCE
            ):
                continue

            # Step 5: Calculate goal-directed estimate h(n') only for a route that
            # is competitive under the best-g rule.
            h_successor_estimated_remaining_cost = problem.heuristic(
                s_successor_state,
            )

            # SAFETY CHECK: Every queued priority must remain finite and
            # nonnegative so the heap order matches the A* model.
            if (
                not math.isfinite(h_successor_estimated_remaining_cost)
                or h_successor_estimated_remaining_cost < 0.0
            ):
                raise ValueError("heuristic values must be finite and nonnegative")

            # Step 6: Store the improved route prefix. The parent and action form
            # one link that path reconstruction can later follow from goal to s0.
            successor_node = SearchNode(
                state=s_successor_state,  # Successor State
                parent=current_node,  # Parent Node
                action=action,  # Action
                g_path_cost=g_successor_path_cost,  # Path Cost
                h_estimated_remaining_cost=h_successor_estimated_remaining_cost,  # Heuristic Estimate
                depth=current_node.depth + 1,  # Depth
            )

            # INVARIANT: Store the improved g before queuing n' 
            # to prevent duplicates from being added to the frontier heap
            best_g_path_cost_by_state[s_successor_state] = g_successor_path_cost

            # Step 7: Queue by f(n') = g(n') + h(n'). The h tie breaker favors the
            # candidate estimated to be closer when total f values are equal.
            heapq.heappush(
                frontier_heap,
                (
                    successor_node.f_evaluation_cost,  # f(n')
                    successor_node.h_estimated_remaining_cost,  # h(n')
                    next(insertion_counter),  # tie-breaker
                    successor_node,  # SearchNode object 
                ),
            )

            # Update observations only after a successor actually enters OPEN.
            generated_nodes += 1 # Count generated nodes
            maximum_frontier_size = max( # Update maximum frontier size
                maximum_frontier_size,  # Current maximum size
                len(frontier_heap),  # Size of frontier heap
            )

    # FAILURE CONDITION: In this finite graph, an empty OPEN means every reachable
    # route has been exhausted without selecting a goal state.
    return None
# ---

# ____________________________________________________________________________________
# ====================================================================================
# MAP VALIDATION AND LOCATION HELPERS
# ====================================================================================
#
# These helpers set up and audit the domain used by the search problem. 
# They are support code, not additional search strategies. 
# Validating the map before exploration protects the assumptions made by actions() and cost().

# --- validate_floor_map()
def validate_floor_map(floor_map: Sequence[str]) -> None:
    """Validate dimensions, symbols, border walls, and named locations.

    Raises:
        ValueError: If any structural requirement is not satisfied.

    Logic:
        1. Require at least one nonempty row.
        2. Require equal row lengths and only documented map symbols.
        3. Require a wall around the complete outer border.
        4. Require each named selectable location exactly once.

    """
    # VALIDATION: A state space needs at least one row and one column.
    if not floor_map:
        raise ValueError("the floor map must contain at least one row")

    # Determine the number of columns in the floor map
    column_count = len(floor_map[0])
    if column_count == 0:
        raise ValueError("the floor map must contain at least one column")

    # Define known symbols in the floor map
    known_symbols = {
        "#",
        *TERRAIN_COST_BY_SYMBOL.keys(),
        *LOCATION_NAME_BY_CODE.keys(),
    }
    
    # Count occurrences of each location code in the floor map
    location_counts = {code: 0 for code in LOCATION_NAME_BY_CODE}

    # Inspect every stored cell while confirming that the grid stays rectangular.
    for row_index, row in enumerate(floor_map):
        # VALIDATION: Rows must have equal length.
        if len(row) != column_count:
            raise ValueError(
                f"floor-map row {row_index} has length {len(row)}; "
                f"expected {column_count}",
            )
        
        for symbol in row:
            # VALIDATION: Symbols must be recognized.
            if symbol not in known_symbols:
                raise ValueError(f"unknown floor-map symbol: {symbol!r}")
            
            # Count occurrences of each location code in the floor map
            if symbol in location_counts:
                location_counts[symbol] += 1

    # VALIDATION: The closed wall border makes an out-of-map movement visibly
    # blocked and preserves the finite rectangular classroom environment.
    if any(symbol != "#" for symbol in floor_map[0]):
        raise ValueError("the top map border must contain only walls")
    if any(symbol != "#" for symbol in floor_map[-1]):
        raise ValueError("the bottom map border must contain only walls")
    if any(row[0] != "#" or row[-1] != "#" for row in floor_map):
        raise ValueError("the left and right map borders must contain only walls")

    # VALIDATION: Each named location must appear exactly once. 
    invalid_location_counts = {
        code: count
        for code, count in location_counts.items()
        if count != 1
    }
    # VALIDATION: Raise error if any location appears more than once or not at all
    if invalid_location_counts:
        raise ValueError(
            "each named location must appear exactly once; "
            f"invalid counts: {invalid_location_counts}",
        )
# ---

# --- find_location_coordinates()
def find_location_coordinates(
    floor_map: Sequence[str],
) -> dict[str, Coordinate]:
    """Return each named location code and its immutable coordinate state.

    This helper converts human-facing department codes into the same ``s`` tuple
    representation consumed by the search problem.
    """
    validate_floor_map(floor_map)
    coordinates: dict[str, Coordinate] = {}

    # Construct code -> s without embedding coordinates in the search algorithm.
    for row_index, row in enumerate(floor_map): # Iterate through rows
        for column_index, symbol in enumerate(row): # Iterate through columns
            # If the symbol is a location code, add it to the coordinates dictionary
            if symbol in LOCATION_NAME_BY_CODE:
                coordinates[symbol] = (row_index, column_index)

    return coordinates
# ---

# --- describe_state()
def describe_state(
    floor_map: Sequence[str],
    state: Coordinate,
) -> str:
    """Return a readable description of a coordinate and its map cell.
    
    Args:
        floor_map (Sequence[str]): The floor map.
        state (Coordinate): The coordinate to describe.
    
    Returns:
        str: The description of the coordinate.
    
    """
    row, column = state
    symbol = floor_map[row][column]
    # Check if the symbol is a location code, get the name, otherwise get the terrain name
    if symbol in LOCATION_NAME_BY_CODE:
        cell_description = LOCATION_NAME_BY_CODE[symbol]
    else:
        cell_description = TERRAIN_NAME_BY_SYMBOL[symbol]

    return f"(row {row}, column {column}) - {cell_description}"
# ---

# --- terrain_name_for_symbol()
def terrain_name_for_symbol(symbol: str) -> str:
    """Return a short terrain or location name for a map symbol.
    
    Args:
        symbol (str): The symbol to convert to a terrain or location name.
    
    Returns:
        str: The terrain or location name.
    
    """
    if symbol in LOCATION_NAME_BY_CODE:
        return LOCATION_NAME_BY_CODE[symbol]
    return TERRAIN_NAME_BY_SYMBOL[symbol]
# ---

# --- calculate_path_cost()
def calculate_path_cost(
    problem: HospitalRobotRouteProblem,
    path: Sequence[PathEntry],
) -> float:
    """Recalculate a returned path's total cost from its state transitions.

    Related Equation:
        ``g(goal) = sum(c(s_i, a_i, s_(i+1)))``

    Equation Relationship:
        This independent audit walks the returned path and re-evaluates every
        edge cost through the problem. It checks, rather than trusts, the goal
        node's stored ``g_path_cost``.
    """
    # VALIDATION: A valid path begins with exactly one action-free initial state.
    if not path:
        raise ValueError("path must contain at least the initial state")
    if path[0][0] is not None:
        raise ValueError("the initial path entry must use action None")

    total_cost = 0.0
    previous_state = path[0][1]

    # Accumulate one destination-entry cost for each non-initial path entry.
    for action, current_state in path[1:]:
        if action is None:
            raise ValueError("non-initial path entries must contain an action")
        total_cost += problem.cost(previous_state, action, current_state)
        previous_state = current_state

    return total_cost
# ---

# ____________________________________________________________________________________
# ====================================================================================
# DISPLAY HELPERS
# ====================================================================================

# --- terminal_supports_color()
def terminal_supports_color() -> bool:
    """Return whether ANSI colors should be used for the current output.
    
    Returns:
        bool: True if the terminal supports color, False otherwise.
    """
    # Determine if the terminal supports color
    # This is a simple check to see if the terminal supports color
    # If the terminal supports color, return True, otherwise return False
    # If the terminal supports color, return True, otherwise return False
    if not USE_CONSOLE_COLORS or os.getenv("NO_COLOR") is not None:
        return False
    if os.getenv("FORCE_COLOR") is not None:
        return True

    is_interactive_output = bool(
        getattr(sys.stdout, "isatty", lambda: False)(),
    )
    return is_interactive_output and os.getenv("TERM", "").lower() != "dumb"
# ---

# --- style_text()
def style_text(
    text: str,
    color: str = "",
    *,
    bold: bool = False,
    dim: bool = False,
) -> str:
    """Return ANSI-formatted text when the console supports it.
    
    Args:
        text (str): The text to format.
        color (str, optional): The color of the text. Defaults to "".
        bold (bool, optional): Whether the text should be bold. Defaults to False.
        dim (bool, optional): Whether the text should be dim. Defaults to False.
    
    Returns:
        str: The formatted text.
    
    """
    if not terminal_supports_color():
        return text

    formatting_codes = "".join(
        code
        for code in (
            ANSI_BOLD if bold else "", 
            ANSI_DIM if dim else "",
            color,
        )
        if code
    )
    return f"{formatting_codes}{text}{ANSI_RESET}"
# ---

# --- print_heading()
def print_heading(title: str, color: str = ANSI_CYAN) -> None:
    """Print a centered section heading.
    
    Args:
        title (str): The title of the heading.
        color (str, optional): The color of the heading. Defaults to ANSI_CYAN.
    
    """
    border = "=" * DISPLAY_WIDTH
    print()
    print(style_text(border, color, bold=True))
    print(style_text(title.center(DISPLAY_WIDTH), color, bold=True))
    print(style_text(border, color, bold=True))
    print()
# ---

# --- print_subheading()
def print_subheading(title: str, color: str = ANSI_DEFAULT) -> None:
    """Print a compact subheading and underline.
    
    Args:
        title (str): The title of the subheading.
        color (str, optional): The color of the subheading. Defaults to ANSI_DEFAULT.
    
    """
    print(style_text(title, color, bold=True))
    print(style_text("-" * min(len(title), DISPLAY_WIDTH), color))
# ---

# --- print_paragraph()
def print_paragraph(text: str, *, indent: int = 0) -> None:
    """Print a wrapped explanatory paragraph.
    
    Args:
        text (str): The text to print.
        indent (int, optional): The indentation level. Defaults to 0.
    
    """
    indentation = " " * indent
    print(
        textwrap.fill(
            text,
            width=DISPLAY_WIDTH,
            initial_indent=indentation,
            subsequent_indent=indentation,
        ),
    )
# ---

# --- print_equation()
def print_equation(
    equation: str,
    *,
    indent: int = 4,
    color: str = ANSI_MAGENTA,
) -> None:
    """Print one equation so it stands apart from explanatory prose.
    
    Args:
        equation (str): The equation to print.
        indent (int, optional): The indentation level. Defaults to 4.
        color (str, optional): The color of the equation. Defaults to ANSI_MAGENTA.
    
    """
    print(" " * indent + style_text(equation, color, bold=True))
# ---

# --- print_labeled_value()
def print_labeled_value(
    label: str,
    value: str,
    *,
    value_color: str = ANSI_DEFAULT,
    indent: int = 2,
) -> None:
    """Print a label and emphasized value using consistent alignment.
    
    """
    label_width = 38
    plain_label = f"{' ' * indent}{label:<{label_width}}"
    print(plain_label + style_text(value, value_color, bold=True))
# ---

# --- pause_for_user()
def pause_for_user(next_action: str) -> None:
    """Pause a terminal run between major explanatory sections.
    
    Args:
        next_action (str): The name of the next action to perform.
    
    """
    if (
        not PAUSE_BETWEEN_SECTIONS
        or not bool(getattr(sys.stdin, "isatty", lambda: False)())
    ):
        return

    prompt = style_text(
        f"Press Enter to {next_action}...",
        ANSI_YELLOW,
        bold=True,
    )
    try:
        input(f"\n{prompt}")
    except EOFError:
        print()
# ---

# --- colorize_map_symbol()
def colorize_map_symbol(symbol: str) -> str:
    """Apply a readable console color to one floor-map symbol.
    
    Args:
        symbol (str): The symbol to colorize.
    
    Returns:
        str: The colorized symbol.
    
    """
    if symbol == "#":
        return style_text(symbol, ANSI_BLUE, dim=True)
    if symbol == "~":
        return style_text(symbol, ANSI_YELLOW, bold=True)
    if symbol == "!":
        return style_text(symbol, ANSI_RED, bold=True)
    if symbol in LOCATION_NAME_BY_CODE:
        return style_text(symbol, ANSI_CYAN, bold=True)
    return symbol
# ---

# --- print_floor_map()
def print_floor_map(floor_map: Sequence[str]) -> None:
    """Print the original hospital floor map with row and column guides.
    
    Args:
        floor_map (Sequence[str]): The floor map.
    
    """
    column_count = len(floor_map[0])
    tens_line = "".join(str((column // 10) % 10) for column in range(column_count))
    ones_line = "".join(str(column % 10) for column in range(column_count))

    print("    " + tens_line)
    print("    " + ones_line)
    for row_index, row in enumerate(floor_map):
        colored_row = "".join(colorize_map_symbol(symbol) for symbol in row)
        print(f"{row_index:>2}  {colored_row}")
# ---

# --- print_map_legend()
def print_map_legend() -> None:
    """Print map symbols and exact traversal costs.
    
    """
    print_subheading("How to read the map", ANSI_CYAN)
    print_labeled_value("#", "wall (the robot cannot enter)")
    print_labeled_value(".", "normal corridor (costs 1 unit to enter)")
    print_labeled_value("~", "busy corridor (costs 3 units to enter)", value_color=ANSI_YELLOW)
    print_labeled_value("!", "sanitation zone (costs 6 units to enter)", value_color=ANSI_RED)
    for code, name in LOCATION_NAME_BY_CODE.items():
        print_labeled_value(code, f"{name} (costs 1 unit to enter)", value_color=ANSI_CYAN)
# ---

# --- render_route_map()
def render_route_map(
    floor_map: Sequence[str],
    path: Sequence[PathEntry],
) -> list[str]:
    """Return a copy of the map with ``A``, ``G``, and ``*`` route markers.
    
    Args:
        floor_map (Sequence[str]): The floor map.
        path (Sequence[PathEntry]): The path to visualize.
    
    Returns:
        list[str]: The floor map with route markers.
    """
    # Convert only the display copy to mutable row lists; floor_map stays unchanged.
    route_map = [list(row) for row in floor_map]
    path_states = [state for _, state in path]

    # Mark interior path states while reserving distinct endpoint symbols.
    for row, column in path_states[1:-1]:
        route_map[row][column] = "*"

    start_row, start_column = path_states[0]
    goal_row, goal_column = path_states[-1]
    route_map[start_row][start_column] = "A"
    route_map[goal_row][goal_column] = "G"

    return ["".join(row) for row in route_map]
# ---

# --- colorize_route_symbol()
def colorize_route_symbol(symbol: str) -> str:
    """Apply console colors to route map symbols.
    
    Args:
        symbol (str): The symbol to colorize.
    
    Returns:
        str: The colorized symbol.
    """
    if symbol == "A":
        return style_text(symbol, ANSI_CYAN, bold=True)
    if symbol == "G":
        return style_text(symbol, ANSI_MAGENTA, bold=True)
    if symbol == "*":
        return style_text(symbol, ANSI_GREEN, bold=True)
    return colorize_map_symbol(symbol)
# ---

# --- print_route_map()
def print_route_map(route_map: Sequence[str]) -> None:
    """Print a route overlay with row and column guides.
    
    Args:
        route_map (Sequence[str]): The route map.
    
    """
    column_count = len(route_map[0])
    tens_line = "".join(str((column // 10) % 10) for column in range(column_count))
    ones_line = "".join(str(column % 10) for column in range(column_count))

    print("    " + tens_line)
    print("    " + ones_line)
    for row_index, row in enumerate(route_map):
        colored_row = "".join(colorize_route_symbol(symbol) for symbol in row)
        print(f"{row_index:>2}  {colored_row}")
# ---

# ____________________________________________________________________________________
# ====================================================================================
# INPUT HELPERS
# ====================================================================================

# --- print_location_menu()
def print_location_menu(
    location_coordinates: dict[str, Coordinate],
) -> None:
    """Print selectable named locations with stable numbers and coordinates.
    
    Args:
        location_coordinates (dict[str, Coordinate]): A dictionary of location codes to their coordinates.
    
    """
    print_subheading("Choose from these hospital locations", ANSI_CYAN)

    for menu_number, code in enumerate(LOCATION_NAME_BY_CODE, start=1):
        row, column = location_coordinates[code]
        name = LOCATION_NAME_BY_CODE[code]
        print(
            f"  {menu_number}. {style_text(code, ANSI_CYAN, bold=True)}: "
            f"{name} at (row {row}, column {column})",
        )
# ---

# --- normalize_location_choice()
def normalize_location_choice(raw_choice: str) -> str | None:
    """Convert a menu number or location code into one canonical location code.
    
    Args:
        raw_choice (str): The raw choice from the user.
    
    Returns:
        str | None: The normalized location code, or None if the choice is invalid.
    
    """
    cleaned_choice = raw_choice.strip().upper()
    if cleaned_choice in LOCATION_NAME_BY_CODE:
        return cleaned_choice

    codes_in_menu_order = tuple(LOCATION_NAME_BY_CODE)
    if cleaned_choice.isdigit():
        menu_index = int(cleaned_choice) - 1
        if 0 <= menu_index < len(codes_in_menu_order):
            return codes_in_menu_order[menu_index]

    return None
# ---

# --- prompt_for_location()
def prompt_for_location(
    prompt_label: str,
    *,
    default_code: str,
    forbidden_code: str | None = None,
) -> str:
    """Prompt until the user selects a valid named location.
    
    Args:
        prompt_label (str): The label for the prompt.
        default_code (str): The default location code to use if the user does not provide one.
        forbidden_code (str | None, optional): The location code that is forbidden. Defaults to None.
    
    Returns:
        str: The selected location code.
    
    Logic:
        1. Read a menu number or location code.
        2. Substitute the documented default for an empty response.
        3. Normalize and reject unknown selections.
        4. Reject a goal equal to the selected start.
        5. Return the first valid canonical code.
    """
    # VALIDATION LOOP
    while True:
        prompt = style_text(
            f"  Choose the {prompt_label} (number/code; Enter = {default_code}): ",
            ANSI_CYAN,
            bold=True,
        ) # This is a prompt for the user to select a location.
        try: # This is a try block to catch an EOFError.
            raw_choice = input(prompt)
        except EOFError as exc:
            raise SystemExit("\nNo input was received. The program will stop.") from exc

        if not raw_choice.strip():
            location_code = default_code
        else:
            location_code = normalize_location_choice(raw_choice)

        # Unknown text does not correspond to any state the UI may select.
        if location_code is None:
            print(
                style_text(
                    "  I did not recognize that choice. Enter a menu number or location code.",
                    ANSI_RED,
                    bold=True,
                ),
            )
            continue

        # A zero-action start-equals-goal route is valid mathematically, but the
        # interactive assignment requires a visible sequence between locations.
        if forbidden_code is not None and location_code == forbidden_code:
            print(
                style_text(
                    "  Choose a destination different from the starting location.",
                    ANSI_RED,
                    bold=True,
                ),
            )
            continue

        return location_code
# ---

# --- validate_cli_location_code()
def validate_cli_location_code(code: str | None, argument_name: str) -> str | None:
    """Validate an optional command-line location code.
    Args:
        code (str | None): The command-line location code.
        argument_name (str): The name of the argument.
    Returns:
        str | None: The validated location code.
    """
    if code is None:
        return None

    normalized_code = normalize_location_choice(code)
    if normalized_code is None:
        valid_codes = ", ".join(LOCATION_NAME_BY_CODE)
        raise ValueError(
            f"{argument_name} must be one of these codes: {valid_codes}",
        )

    return normalized_code
# ---

# ____________________________________________________________________________________
# ====================================================================================
# SEARCH EXPLANATION AND RESULT DISPLAY
# ====================================================================================

# --- print_problem_definition()
def print_problem_definition() -> None:
    """Display the initial state, goal, action, cost, and constraint concepts.

    """
    print_subheading("What the robot is trying to do", ANSI_CYAN)
    print_paragraph(
        "The medication-delivery robot needs a low-cost route from one hospital "
        "location to another. It can move one square up, right, down, or left, "
        "but it cannot pass through walls. Busy corridors and sanitation zones "
        "are open, although entering them costs more to represent delay and risk.",
    )
    print()
    print_labeled_value("Robot position (state s):", "current square, written as (row, column)")
    print_labeled_value("Starting position (state s0):", "location where the route begins")
    print_labeled_value("Destination (goal state sg):", "location the robot must reach")
    print_labeled_value("Allowed moves (actions a):", "UP, RIGHT, DOWN, or LEFT")
    print_labeled_value("Blocked move:", "any move that would enter a wall")
    print_labeled_value(
        "Search stops when:",
        "the robot's position equals the destination (s == sg)",
    )
# ---

# --- print_search_method_explanation()
def print_search_method_explanation() -> None:
    """Display A* algorithm, its evaluation terms, heuristic, and repeated-state rule.

    Equation Relationship:
        This helper displays ``f = g + h`` and the Manhattan formula. The
        corresponding values are calculated by SearchNode, the problem heuristic,
        and astar_search().
    """
    print_subheading("How A* decides what to check next", ANSI_MAGENTA)
    print_paragraph(
        "A* keeps a waiting list, called the frontier, of possible routes. Each "
        "route ends at a search node n. A* gives every node a score and checks "
        "the node with the lowest score first.",
    )
    print_equation("f(n) = g(n) + h(n)")
    print("    n    = one possible route ending at one map position")
    print("    g(n) = exact travel cost already paid (cost so far)")
    print("    h(n) = optimistic estimate of the travel cost still left")
    print("    f(n) = combined A* score; a lower score is checked first")
    print()
    print_paragraph(
        "The estimate h(n) uses Manhattan distance: the vertical row difference "
        "plus the horizontal column difference. It assumes every remaining move "
        "costs only 1 unit and temporarily ignores walls and expensive terrain. "
        "That makes the estimate optimistic rather than too large.",
    )
    print_equation(
        "h(n) = (|row - goal_row| + |column - goal_column|) * 1",
    )
    print()
    print_paragraph(
        "A* may reach the same map position by more than one route. It remembers "
        "the cheapest cost-so-far value g(n) found for that position and ignores "
        "another route when it costs the same or more.",
    )
# ---


# --- print_route_step_table()
def print_route_step_table(
    problem: HospitalRobotRouteProblem,
    result: SearchResult,
) -> None:
    """Display every returned action and its ``g``, ``h``, and ``f`` values.
    
    Args:
        problem (HospitalRobotRouteProblem): The problem instance.
        result (SearchResult): The result of the search.
    
    """
    print_subheading("Route details: one row per move", ANSI_GREEN)
    print_paragraph(
        "Step 0 is the starting square; every later row is one move. Move cost is "
        "what that move adds. Cost so far is g(n), Est. left is h(n), and A* score "
        "is f(n) = g(n) + h(n).",
    )
    print()

    header = (
        f"{'Step':>4}  "
        f"{'Move':<5}  "
        f"{'Position':<8}  "
        f"{'Terrain / location':<22}  "
        f"{'Move cost':>9}  "
        f"{'Cost so far':>11}  "
        f"{'Est. left':>9}  "
        f"{'A* score':>9}"
    )
    print(style_text(header, ANSI_DEFAULT, bold=True))
    print(style_text("-" * len(header), ANSI_DEFAULT, dim=True))

    # Reconstruct the selected route once, then expose the cost meaning at every
    # path position. Nodes expanded but excluded from the solution are not shown.
    path_nodes = result.path_nodes()
    for step_number, node in enumerate(path_nodes):
        if node.parent is None or node.action is None:
            action_label = "START"
            step_cost = 0.0
        else:
            action_label = node.action.replace("MOVE ", "")
            step_cost = problem.cost(
                node.parent.state,
                node.action,
                node.state,
            )

        row, column = node.state
        symbol = problem.symbol_at(node.state)
        cell_name = terrain_name_for_symbol(symbol)
        if len(cell_name) > 22:
            cell_name = cell_name[:19] + "..."

        table_row = (
            f"{step_number:>4}  "
            f"{action_label:<5}  "
            f"{f'({row}, {column})':<8}  "
            f"{cell_name:<22}  "
            f"{step_cost:>9.1f}  "
            f"{node.g_path_cost:>11.1f}  "
            f"{node.h_estimated_remaining_cost:>9.1f}  "
            f"{node.f_evaluation_cost:>9.1f}"
        )

        if step_number == 0:
            print(style_text(table_row, ANSI_CYAN, bold=True))
        elif step_number == len(path_nodes) - 1:
            print(style_text(table_row, ANSI_MAGENTA, bold=True))
        else:
            print(table_row)
# ---


# --- print_action_sequence()
def print_action_sequence(result: SearchResult) -> None:
    """Print the route as a compact sequence of direction letters."""
    direction_letters = [
        ACTION_ARROW_BY_NAME[action]
        for action, _ in result.path()[1:]
        if action is not None
    ]
    sequence = " -> ".join(direction_letters)

    print_subheading("Route directions (read from left to right)", ANSI_GREEN)
    print_paragraph(
        "U means move up, R means move right, D means move down, and L means "
        "move left. Each arrow means then.",
        indent=2,
    )
    print_paragraph(sequence, indent=2)
# ---


# --- print_search_summary()
def print_search_summary(
    start_code: str,
    goal_code: str,
    problem: HospitalRobotRouteProblem,
    result: SearchResult,
) -> None:
    """Display solution quality and observed A* resource statistics.
    
    Args:
        start_code (str): The starting location code.
        goal_code (str): The goal location code.
        problem (HospitalRobotRouteProblem): The problem instance.
        result (SearchResult): The result of the search.
    
    """
    path = result.path()
    recalculated_path_cost = calculate_path_cost(problem, path)

    # INVARIANT: The node's accumulated g(goal) must equal the sum of displayed
    # action costs. A mismatch would mean path links or cost accounting is wrong.
    if not math.isclose(
        recalculated_path_cost,
        result.goal_node.g_path_cost,
        rel_tol=0.0,
        abs_tol=FLOAT_COMPARISON_TOLERANCE,
    ):
        raise RuntimeError("the returned goal cost does not match the route transitions")

    statistics = result.statistics

    print_subheading("Route result", ANSI_GREEN)
    print_labeled_value(
        "Starting location:",
        f"{start_code} - {describe_state(problem.floor_map, problem.initial_state)}",
        value_color=ANSI_CYAN,
    )
    print_labeled_value(
        "Destination:",
        f"{goal_code} - {describe_state(problem.floor_map, problem.goal_state)}",
        value_color=ANSI_MAGENTA,
    )
    print_labeled_value(
        "Route found:",
        "Yes" if result.state == problem.goal_state else "No",
        value_color=ANSI_GREEN,
    )
    print_labeled_value(
        "Number of moves:",
        f"{len(path) - 1}",
        value_color=ANSI_GREEN,
    )
    print_labeled_value(
        "Total travel cost (g at goal):",
        f"{result.goal_node.g_path_cost:.1f} cost units",
        value_color=ANSI_GREEN,
    )
    print()

    print_subheading("How much work A* did", ANSI_BLUE)
    print_paragraph(
        "A node records one possible route to a map position. The frontier is "
        "A*'s waiting list of nodes that it may examine next.",
    )
    print()
    print_labeled_value("Expanded nodes (examined):", f"{statistics.expanded_nodes}")
    print_labeled_value("Generated nodes (created):", f"{statistics.generated_nodes}")
    print_labeled_value(
        "Unique states (positions found):",
        f"{statistics.unique_states_discovered}",
    )
    print_labeled_value(
        "Maximum frontier (largest waitlist):",
        f"{statistics.maximum_frontier_size}",
    )
    print_labeled_value(
        "Stale entries (outdated routes):",
        f"{statistics.stale_frontier_entries_skipped}",
    )
    print_labeled_value("Reopened states (searched again):", f"{statistics.reopened_states}")
    print()
    print_paragraph(
        "These counts describe only this route request, not A*'s worst case. A* "
        "can use a lot of memory on a large map because it keeps its waiting list "
        "and the best cost found for each position. This hospital map is small, "
        "so the stored information remains manageable.",
    )
# ---


# --- print_method_justification()
def print_method_justification() -> None:
    """Display the assignment's required search-method justification.

    The explanation distinguishes completeness of this finite graph search from
    admissibility of its heuristic and also states evaluation, memory, advantages,
    and disadvantages. It reports properties already established by the design.
    """
    print_subheading("Why A* is a good fit", ANSI_MAGENTA)
    print_paragraph(
        "Evaluation function: The robot must consider both distance and terrain "
        "cost. Greedy Best-First Search uses only h(n), so it may choose a "
        "short-looking but expensive route. Uniform-Cost Search uses only g(n), "
        "so it has no estimate pointing toward the destination. A* balances both "
        "values with f(n) = g(n) + h(n).",
    )
    print()
    print_paragraph(
        "Completeness: On this finite map, A* will find a route whenever one "
        "exists. Every legal move has a positive cost, and remembering the best "
        "cost for each position prevents endless cycling.",
    )
    print()
    print_paragraph(
        "Minimum-cost result: The Manhattan estimate is admissible because it "
        "never claims the remaining trip will cost more than it really must. It "
        "is also consistent from one move to the next. With these properties and "
        "positive move costs, this A* graph search returns a minimum-cost route.",
    )
    print()
    print_paragraph(
        "Main tradeoff: A*'s advantage is that it reliably combines exact travel "
        "cost with useful goal direction. Its disadvantage is memory use: on a "
        "much larger map, its waiting list and saved best costs could grow very "
        "large. The small classroom map makes that tradeoff reasonable.",
    )
# ---


# ____________________________________________________________________________________
# ====================================================================================
# INTERNAL VERIFICATION MODE
# ====================================================================================
#
# Verification connects the comments' theoretical claims to observable behavior:
# - structural validation checks that the encoded graph satisfies map assumptions,
# - all named pairs check that each selectable classroom route is reachable,
# - transition summation checks the meaning of g(goal),
# - the canonical route fixture detects a changed weighted solution, and
# - every legal edge checks heuristic consistency directly.
#
# These checks validate this fixed model and implementation. They do not certify
# a physical robot, prove all A* implementations correct, or make Manhattan
# distance suitable for maps with diagonal or nonstandard movement rules.

# --- run_internal_verification()
def run_internal_verification() -> None:
    """Run focused deterministic checks without requiring interactive input.

    This mode is intentionally small. It verifies the main behavioral contract:
    map validity, all named-location pairs being reachable, route endpoints, path
    cost consistency, the expected default-route cost, and heuristic consistency.

    Logic:
        1. Validate the floor-map representation.
        2. Search every ordered pair of distinct named endpoints.
        3. Audit the canonical route and its weighted cost.
        4. Check the consistency inequality on every legal directed edge.
        5. Confirm the heuristic is zero at the goal.
    """
    print_heading("INTERNAL VERIFICATION", ANSI_BLUE)

    # CHECK 1: Domain encoding satisfies the assumptions used by problem methods.
    validate_floor_map(HOSPITAL_FLOOR_MAP)
    print(style_text("PASS: floor-map structure and symbols are valid", ANSI_GREEN))

    location_coordinates = find_location_coordinates(HOSPITAL_FLOOR_MAP)

    # CHECK 2: Six named locations produce 6 * 5 = 30 ordered distinct pairs.
    # A -> B and B -> A are separate because destination-entry costs define
    # directed edge costs, even though both cardinal movements may be legal.
    route_count = 0
    for start_code, start_state in location_coordinates.items():
        for goal_code, goal_state in location_coordinates.items():
            if start_code == goal_code:
                continue

            problem = HospitalRobotRouteProblem(
                HOSPITAL_FLOOR_MAP,
                start_state,
                goal_state,
            )
            result = astar_search(problem)

            # Every selectable pair must return a goal-linked SearchResult.
            if result is None:
                raise RuntimeError(
                    f"no route found from {start_code} to {goal_code}",
                )
            if result.path()[0][1] != start_state:
                raise RuntimeError("a route did not begin at its initial state")
            if result.state != goal_state:
                raise RuntimeError("a route did not end at its goal state")

            # Recalculate each edge cost independently of the stored goal g.
            route_cost = calculate_path_cost(problem, result.path())
            if not math.isclose(
                route_cost,
                result.goal_node.g_path_cost,
                rel_tol=0.0,
                abs_tol=FLOAT_COMPARISON_TOLERANCE,
            ):
                raise RuntimeError("a returned route has an inconsistent cost")

            route_count += 1

    print(
        style_text(
            f"PASS: all {route_count} ordered pairs of distinct named locations "
            "are reachable",
            ANSI_GREEN,
        ),
    )

    # CHECK 3: Protect the stable, documented default demonstration.
    default_problem = HospitalRobotRouteProblem(
        HOSPITAL_FLOOR_MAP,
        location_coordinates[DEFAULT_START_CODE],
        location_coordinates[DEFAULT_GOAL_CODE],
    )
    default_result = astar_search(default_problem)
    if default_result is None:
        raise RuntimeError("the default route unexpectedly has no solution")

    # The expected 44-unit value tests weighted optimality for this fixture, not
    # merely whether some path reaches Emergency.
    if not math.isclose(
        default_result.goal_node.g_path_cost,
        DEFAULT_ROUTE_EXPECTED_COST,
        rel_tol=0.0,
        abs_tol=FLOAT_COMPARISON_TOLERANCE,
    ):
        raise RuntimeError(
            "the default route cost changed; expected "
            f"{DEFAULT_ROUTE_EXPECTED_COST}, received "
            f"{default_result.goal_node.g_path_cost}",
        )

    # The selected optimum should avoid the higher-cost sanitation symbols. This
    # makes the effect of the weighted cost model visible in the classroom route.
    default_path_symbols = {
        default_problem.symbol_at(state)
        for _, state in default_result.path()
    }
    if "!" in default_path_symbols:
        raise RuntimeError("the default route entered the expensive sanitation zone")

    print(
        style_text(
            "PASS: default P-to-E route costs 44 units and avoids sanitation cells",
            ANSI_GREEN,
        ),
    )

    # CHECK 4: Verify consistency h(s) <= c(s,a,s') + h(s') on every legal edge.
    # This is stronger and more systematic than checking only states on one route.
    for row_index, row in enumerate(HOSPITAL_FLOOR_MAP):
        for column_index, symbol in enumerate(row):
            if symbol == "#":
                continue

            state = (row_index, column_index)
            h_state = default_problem.heuristic(state)
            for action in default_problem.actions(state):
                state2 = default_problem.result(state, action)
                step_cost = default_problem.cost(state, action, state2)
                h_state2 = default_problem.heuristic(state2)

                if h_state > (
                    step_cost + h_state2 + FLOAT_COMPARISON_TOLERANCE
                ):
                    raise RuntimeError(
                        "heuristic consistency failed at "
                        f"state={state}, action={action}, state2={state2}",
                    )

    # CHECK 5: An estimate of cost remaining at the goal must be exactly zero.
    if default_problem.heuristic(default_problem.goal_state) != 0.0:
        raise RuntimeError("the heuristic must equal zero at the goal")

    print(
        style_text(
            "PASS: Manhattan heuristic is consistent on every legal map edge",
            ANSI_GREEN,
        ),
    )
    print()
    print(style_text("All internal verification checks passed.", ANSI_GREEN, bold=True))
# ---

# ____________________________________________________________________________________
# ====================================================================================
# COMMAND-LINE CONFIGURATION
# ====================================================================================
#
# CLI configuration selects a mode and endpoint codes. It never changes A*'s
# evaluation rule. Demo, interactive, and explicit-code runs all call the same
# HospitalRobotRouteProblem and astar_search() backend.

# --- build_argument_parser()
def build_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line interface used for interactive and test runs.

    The flags control reproducibility and presentation. None selects a different
    search algorithm or heuristic.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Use A* graph search to plan a weighted route for a hospital "
            "medication-delivery robot."
        ),
    )
    parser.add_argument(
        "--start",
        metavar="CODE",
        help="starting location code, such as P, N, L, E, S, or C",
    )
    parser.add_argument(
        "--goal",
        metavar="CODE",
        help="goal location code, such as P, N, L, E, S, or C",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="run the default Pharmacy-to-Emergency route without prompts",
    )
    parser.add_argument(
        "--verify-map",
        action="store_true",
        help="run focused internal verification checks and exit",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable ANSI console colors",
    )
    parser.add_argument(
        "--no-pause",
        action="store_true",
        help="disable Enter-key pauses between sections",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {PROGRAM_VERSION}",
    )
    return parser
# ---


# --- resolve_location_selection()
def resolve_location_selection(
    start_argument: str | None,
    goal_argument: str | None,
    *,
    demo_mode: bool,
    location_coordinates: dict[str, Coordinate],
) -> tuple[str, str]:
    """Resolve CLI or interactive start and goal selections.
    
    Args:
        start_argument (str | None): The starting location code provided via the CLI.
        goal_argument (str | None): The goal location code provided via the CLI.
        demo_mode (bool): Whether to run in demo mode.
        location_coordinates (dict[str, Coordinate]): A dictionary of location codes to their coordinates.
    
    Returns:
        tuple[str, str]: The starting and goal location codes.
    
    Logic:
        1. Use fixed defaults in reproducible demo mode.
        2. Validate any endpoint supplied through the CLI.
        3. Prompt only for endpoints not already supplied.
        4. Require different start and goal codes.
    """
    # DISPATCH: Demo mode fixes both endpoints and requires no user input.
    if demo_mode:
        return DEFAULT_START_CODE, DEFAULT_GOAL_CODE

    # Validate explicit CLI values before combining them with interactive input.
    start_code = validate_cli_location_code(start_argument, "--start")
    goal_code = validate_cli_location_code(goal_argument, "--goal")

    print_location_menu(location_coordinates)
    print()

    # ASSIGNMENT REQUIREMENT MET: Prompt clearly for a missing initial state.
    if start_code is None:
        start_code = prompt_for_location(
            "starting location",
            default_code=DEFAULT_START_CODE,
        )

    # ASSIGNMENT REQUIREMENT MET: Prompt clearly for a missing, distinct goal.
    if goal_code is None:
        default_goal = (
            DEFAULT_GOAL_CODE
            if DEFAULT_GOAL_CODE != start_code
            else "N"
        )
        goal_code = prompt_for_location(
            "destination",
            default_code=default_goal,
            forbidden_code=start_code,
        )

    if start_code == goal_code:
        raise ValueError("the start and goal location codes must be different")

    return start_code, goal_code
# ---


# ____________________________________________________________________________________
# ====================================================================================
# MAIN FUNCTION - ENTRY POINT
# ====================================================================================

# --- main()
def main(argv: Sequence[str] | None = None) -> None:
    """Collect a route request, run A*, and display the solution path.

    Related Search Pipeline:
        map -> named coordinates -> s0 and sg -> problem formulation
        problem -> A* OPEN loop -> goal SearchNode -> parent-linked path
        path -> route map, action table, g/h/f values, and justification

    Search Relationship:
        This entry point coordinates problem setup, algorithm execution, and
        presentation. ``HospitalRobotRouteProblem`` evaluates domain operations;
        ``astar_search()`` performs the search; display helpers explain results.

    Logic:
        1. Parse execution and presentation options.
        2. Validate the map or dispatch to internal verification mode.
        3. Explain the state-space model and collect ``s0`` and ``sg``.
        4. Construct the concrete problem and explain A*.
        5. Run A* and handle an exhausted frontier.
        6. Reconstruct and display the route and required justification.
    """
    global USE_CONSOLE_COLORS, PAUSE_BETWEEN_SECTIONS

    # __________________________________________
    # CONFIGURE THIS EXECUTION
    # ==========================================

    parser = build_argument_parser()
    arguments = parser.parse_args(argv)

    # Presentation flags affect only formatting and pauses, never search order.
    USE_CONSOLE_COLORS = not arguments.no_color
    PAUSE_BETWEEN_SECTIONS = not arguments.no_pause and not arguments.demo

    try:
        # VALIDATION: Establish a sound state-space encoding before any display,
        # endpoint selection, heuristic evaluation, or search.
        validate_floor_map(HOSPITAL_FLOOR_MAP)

        # DISPATCH: Verification mode exercises deterministic contracts and exits
        # without entering the learner-facing route-selection workflow.
        if arguments.verify_map:
            PAUSE_BETWEEN_SECTIONS = False
            run_internal_verification()
            return

        location_coordinates = find_location_coordinates(HOSPITAL_FLOOR_MAP)

        # __________________________________________
        # SECTION 1: DEFINE THE SEARCH PROBLEM
        # ==========================================

        # DISPLAY BOUNDARY: Explain the domain formulation. No nodes are expanded
        # and no route is selected in this section.

        print_heading(PROGRAM_NAME.upper(), ANSI_CYAN)
        print_paragraph(
            "This classroom program uses A* graph search to find a low-cost route "
            "for a hospital medication-delivery robot. The chosen route must avoid "
            "the map's walls and account for the extra cost of busy corridors and "
            "sanitation zones.",
        )
        print()
        print_paragraph(
            "Each open map square is one possible robot position. The program "
            "defines the robot's legal moves, the cost of entering each square, "
            "the destination check, and an estimate that helps A* search toward "
            "the destination.",
        )

        print_heading("1. UNDERSTAND THE ROUTING PROBLEM", ANSI_BLUE)
        print_problem_definition()
        print()
        print_floor_map(HOSPITAL_FLOOR_MAP)
        print()
        print_map_legend()

        pause_for_user("choose a starting location and destination")

        # __________________________________________
        # SECTION 2: SELECT INITIAL AND GOAL STATES
        # ==========================================

        # USER INPUT BOUNDARY: Resolve human-facing location codes before mapping
        # them to immutable coordinate states.
        print_heading("2. CHOOSE THE START AND DESTINATION", ANSI_CYAN)
        start_code, goal_code = resolve_location_selection(
            arguments.start,
            arguments.goal,
            demo_mode=arguments.demo,
            location_coordinates=location_coordinates,
        )

        s_initial_state = location_coordinates[start_code]
        s_goal_state = location_coordinates[goal_code]

        print()
        print_labeled_value(
            "Starting location (s0):",
            f"{start_code} - {describe_state(HOSPITAL_FLOOR_MAP, s_initial_state)}",
            value_color=ANSI_CYAN,
        )
        print_labeled_value(
            "Destination (sg):",
            f"{goal_code} - {describe_state(HOSPITAL_FLOOR_MAP, s_goal_state)}",
            value_color=ANSI_MAGENTA,
        )

        # ASSIGNMENT REQUIREMENT MET: Bind explicit s0 and sg to a problem object
        # that provides actions, result, goal test, cost, and heuristic.
        problem = HospitalRobotRouteProblem(
            HOSPITAL_FLOOR_MAP,
            s_initial_state,
            s_goal_state,
        )

        pause_for_user("learn how A* scores possible routes")

        # __________________________________________
        # SECTION 3: EXPLAIN AND RUN A*
        # ==========================================

        # DISPLAY BOUNDARY: Present the evaluation and heuristic before executing
        # the backend search so the learner knows how candidates will be ranked.
        print_heading("3. SEE HOW A* SCORES POSSIBLE ROUTES", ANSI_MAGENTA)
        print_search_method_explanation()
        print()
        print_labeled_value(
            "Estimated cost left at start h(s0):",
            f"{problem.heuristic(problem.initial_state):.1f} cost units",
            value_color=ANSI_YELLOW,
        )
        print_labeled_value(
            "Estimated cost left at goal h(sg):",
            f"{problem.heuristic(problem.goal_state):.1f} cost units",
            value_color=ANSI_GREEN,
        )

        pause_for_user("let A* calculate the route")

        print()
        print(
            style_text(
                "A* is searching for the lowest-cost route...",
                ANSI_CYAN,
                bold=True,
            ),
            end="",
            flush=True,
        )

        # BACKEND SEARCH: This call performs the OPEN loop phases documented in
        # astar_search(); display helpers do not participate in node selection.
        # ASSIGNMENT REQUIREMENT MET: Execute A* informed graph search.
        result = astar_search(problem)
        print(style_text(" done.", ANSI_GREEN, bold=True))

        if result is None:
            print_heading("NO ROUTE FOUND", ANSI_RED)
            print_paragraph(
                "A* checked every map position it could reach but did not find a "
                "path to the selected destination. Choose different locations or "
                "inspect the map for disconnected areas.",
            )
            raise SystemExit(1)

        # __________________________________________
        # SECTION 4: DISPLAY THE SOLUTION
        # ==========================================

        # PATH PRESENTATION: Reconstruct the selected parent chain and expose both
        # the compact action sequence and every state's c, g, h, and f values.
        print_heading("4. FOLLOW THE ROUTE A* FOUND", ANSI_GREEN)
        route_map = render_route_map(HOSPITAL_FLOOR_MAP, result.path())
        print_subheading("Route map", ANSI_GREEN)
        print("  A = start, G = destination, * = each square on the selected route")
        print_route_map(route_map)
        print()

        print_action_sequence(result)
        print()
        print_route_step_table(problem, result)
        print()
        print_search_summary(start_code, goal_code, problem, result)

        pause_for_user("read why A* fits this problem")

        # __________________________________________
        # SECTION 5: JUSTIFY THE METHOD
        # ==========================================

        # ASSIGNMENT REQUIREMENT: Explain selection, completeness conditions,
        # heuristic admissibility, evaluation, memory use, benefits, and limits.
        print_heading("5. WHY A* IS A GOOD CHOICE", ANSI_MAGENTA)
        print_method_justification()

        print()
        print(style_text("Finished: A* found a route to the destination.", ANSI_GREEN, bold=True))

    except ValueError as exc:
        # ERROR TRANSLATION: Present domain or search validation failures through
        # argparse's consistent user-facing CLI error format.
        parser.error(str(exc))
# ---


# __________________________________________
# MODULE INITIALIZATION
# ==========================================

if __name__ == "__main__":
    main()


# __________________________________________
# END OF FILE
# ==========================================
