# -------------------------------------------------------------------------
# File: scenario_summary.py
# Author: Alexander Ricciardi
# Date: 2026-04-05
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# ScenarioSummary dataclass representing the best algorithm for a given
# (dataset_type, size) benchmark scenario.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Data class for benchmark scenario winner summaries.

Each ScenarioSummary identifies the fastest algorithm for one
(dataset_type, size) benchmark scenario.
"""

# ________________
# Imports
#

from __future__ import annotations

from dataclasses import dataclass

# __________________________________________________________________________
# ScenarioSummary Dataclass
#

# ========================================================================
# ScenarioSummary
# ========================================================================
# --------------------------------------------------------------- dataclass ScenarioSummary
@dataclass
class ScenarioSummary:
    """Winner record for one benchmark scenario.

    Args:
        dataset_type: Dataset category (e.g., "random").
        size: Scenario size.
        fastest_algorithm: Name of the winning algorithm by time.
        fastest_time_ms: Winning time in milliseconds.
        runner_up_algorithm: Second-place algorithm name.
        notes: Human-readable summary for reports.
    """

    dataset_type: str
    size: int
    fastest_algorithm: str
    fastest_time_ms: float
    runner_up_algorithm: str
    notes: str

# --------------------------------------------------------------- end dataclass ScenarioSummary

# __________________________________________________________________________
# End of File
#
