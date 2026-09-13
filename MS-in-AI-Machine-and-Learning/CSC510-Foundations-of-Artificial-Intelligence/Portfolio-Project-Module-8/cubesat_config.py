# -----------------------------------------------------------------------------
# Module Type: constants/configuration module
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
# - Keep the dataset column order, source checks, and program settings in one place.
# - Identify the channel-to-fault mappings as teaching assumptions.
#
# Usage / Integration:
# - Imported by data, model, similarity, reasoning, CLI, and frontend modules.
# - Consumers read these settings and validate the values they use.
#
# Contents Overview:
# - Feature/metadata schemas and pinned authentic artifact identities.
# - ChannelKnowledge and the simulated channel mapping.
# - AppConfig and DEFAULT_CONFIG for paths and numerical settings.
#
# Dependencies:
# - Standard Library: dataclasses, pathlib
# - Third-Party: None
# - Local Project: None
#
# Requirements:
# - Python 3.12+
#
# License:
# - Not specified
# -----------------------------------------------------------------------------

"""Keep the data contract and adjustable program settings together.

The data contract describes the columns and artifact identity expected from the OPS-SAT Anomaly
Detection (OPS-SAT-AD) dataset. AppConfig holds choices such as the model size and uncertainty
margin. Keeping them here gives the modules one shared feature order and set of defaults.

Channel criticality and subsystem names are simulated teaching assumptions. The source channel
identifiers do not come with engineering limits that would establish those interpretations.
"""

# __________________________________________
# IMPORTS
# ==========================================

from dataclasses import dataclass
from pathlib import Path

# __________________________________________
# DATASET SCHEMA AND PROFILE
# ==========================================

# ________________________________________________
# Ordered feature and metadata columns
# ------------------------------------------------
# Each model row contains these 18 numerical summaries of one telemetry segment.
# Their order must stay the same during loading, training, and prediction: the model
# learns a meaning for each column position, not for the column's text label.
FEATURE_NAMES: tuple[str, ...] = (
    "duration",
    "len",
    "mean",
    "var",
    "std",
    "kurtosis",
    "skew",
    "n_peaks",
    "smooth10_n_peaks",
    "smooth20_n_peaks",
    "diff_peaks",
    "diff2_peaks",
    "diff_var",
    "diff2_var",
    "gaps_squared",
    "len_weighted",
    "var_div_duration",
    "var_div_len",
)

# The first five columns describe the row. In particular, anomaly is a reviewed
# label for training/evaluation; it is not included among the model's input features.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "segment",
    "anomaly",
    "train",
    "channel",
    "sampling",
    *FEATURE_NAMES,
)

# The companion file stores individual readings, so a segment can occupy many rows.
# Its metadata is checked against the one-row-per-segment feature table above.
SEGMENTS_REQUIRED_COLUMNS: tuple[str, ...] = (
    "channel",
    "timestamp",
    "value",
    "label",
    "sampling",
    "anomaly",
    "segment",
    "train",
)
# ________________________________________________
# Authentic profile expectations
# ------------------------------------------------
# The accepted channels and population counts constrain the reviewed data profile.
# Expected channel names from the dataset.
EXPECTED_CHANNELS: tuple[str, ...] = (
    "CADC0872",
    "CADC0873",
    "CADC0874",
    "CADC0884",
    "CADC0886",
    "CADC0888",
    "CADC0890",
    "CADC0892",
    "CADC0894",
)

# These are expected values for the pinned authentic dataset version. The loader
# compares the local artifact with them; they are not measurements from the current run.
# The 529 test rows include both reviewed classes, not 529 anomalous segments.
AUTHENTIC_ROW_COUNT: int = 2_123
AUTHENTIC_TRAINING_ROW_COUNT: int = 1_594
AUTHENTIC_TEST_ROW_COUNT: int = 529
AUTHENTIC_ANOMALOUS_ROW_COUNT: int = 434
AUTHENTIC_SEGMENTS_ROW_COUNT: int = 303_493
AUTHENTIC_SEGMENTS_LABEL_VALUES: tuple[str, ...] = ("anomaly",)
# ________________________________________________
# Pinned artifact identity
# ------------------------------------------------
# Record identifiers, file sizes, and digests tie authentic validation to exact local bytes.
ZENODO_RECORD_ID: int = 15108715
ZENODO_RECORD_URL: str = "https://zenodo.org/records/15108715"
DATASET_SIZE_BYTES: int = 507_550
DATASET_MD5: str = "5246fdc5e4630a4cecbf7fb6bc8b795e"
DATASET_SHA256: str = "b524177da6f516d5c9f63c7acbc385341f0ad42046ef20c1bed2d25e51b98f02"
SEGMENTS_SIZE_BYTES: int = 18_987_091
SEGMENTS_MD5: str = "72f109630abb933a386106897a631188"
SEGMENTS_SHA256: str = "d5201e9e751eb2a53a0ff7c11567dc4239f594ea4b479b2aa66fe67ddcbcb9ba"


# __________________________________________
# SIMULATED KNOWLEDGE CONFIGURATION
# ==========================================

# The rule engine reads these records to connect channel evidence with simulated hypotheses.
# --- class ChannelKnowledge
@dataclass(frozen=True, slots=True)
class ChannelKnowledge:
    """Describe one inspectable, simulated channel-to-fault mapping.

    Attributes:
        channel: OPS-SAT-AD channel identifier.
        critical: Whether the educational knowledge base treats the channel as critical.
        fault_name: Simulated fault hypothesis associated with a deviation.
        check_name: Simulated diagnostic check transferred to planning.
        source_status: Provenance label for the mapping.
    """

    channel: str
    critical: bool
    fault_name: str
    check_name: str
    source_status: str = "simulated"
# --- end class ChannelKnowledge


# These mappings give the rule engine concrete examples to reason about. The
# simulated fault names and critical flags do not identify confirmed spacecraft faults.
CHANNEL_KNOWLEDGE: tuple[ChannelKnowledge, ...] = (
    ChannelKnowledge("CADC0872", True, "simulated_power_subsystem", "CADC0872"),
    ChannelKnowledge("CADC0873", True, "simulated_power_subsystem", "CADC0873"),
    ChannelKnowledge("CADC0874", True, "simulated_power_subsystem", "CADC0874"),
    ChannelKnowledge("CADC0884", True, "simulated_thermal_subsystem", "CADC0884"),
    ChannelKnowledge("CADC0886", True, "simulated_thermal_subsystem", "CADC0886"),
    ChannelKnowledge("CADC0888", False, "simulated_attitude_subsystem", "CADC0888"),
    ChannelKnowledge("CADC0890", False, "simulated_attitude_subsystem", "CADC0890"),
    ChannelKnowledge("CADC0892", False, "simulated_payload_subsystem", "CADC0892"),
    ChannelKnowledge("CADC0894", False, "simulated_payload_subsystem", "CADC0894"),
)


# __________________________________________
# RUNTIME CONFIGURATION
# ==========================================

# These defaults travel together through loading, fitting, similarity, and reasoning.
# Resolve bundled files relative to this module so launching the CLI from another
# directory does not change where the default dataset and examples are found.
PROJECT_ROOT: Path = Path(__file__).resolve().parent


# --- class AppConfig
@dataclass(frozen=True, slots=True)
class AppConfig:
    """Store the settings shared by one fitted assistant.

    This dataclass collects values; it does not validate them when constructed. The
    loading and calculation functions check the settings they need. A frozen instance
    keeps those settings from being reassigned while the assistant is being reused.

    Attributes:
        random_seed: Split and estimator seed for repeating a run with the same data/environment.
        hidden_layer_sizes: Units in each hidden layer of the multilayer perceptron (MLP).
        max_training_iterations: Upper limit on optimizer iterations, not a promised run length.
        validation_fraction: Share of official training rows reserved for threshold selection.
        uncertainty_margin: Probability distance on either side of the selected threshold.
        anomaly_fact_threshold: Separate probability cutoff used to assert `Anomalous` facts.
        neighbors_per_class: Maximum historical cases returned for each class.
        similarity_metric: Distance method used to compare standardized feature rows.
        similarity_cutoff: Largest accepted neighbor distance, or `None` for no cutoff.
        similarity_conflict_ratio: How much closer opposite-class cases must be to flag conflict.
        deviation_zscore_threshold: Absolute deviation from normal training mean, in std units.
        expected_feature_names: Ordered columns shared by every numerical component.
        expected_channels: Source channel identifiers accepted when loading either data profile.
        default_dataset_path: Prepared authentic feature table; loading does not download it.
        demo_dataset_path: Bundled simulated table used by the deterministic demonstrations.
        demo_scenarios_path: JSON file connecting each named example to its segment ID.
    """

    random_seed: int = 2_137
    hidden_layer_sizes: tuple[int, int, int] = (32, 16, 8)
    max_training_iterations: int = 500
    validation_fraction: float = 0.20
    uncertainty_margin: float = 0.05
    anomaly_fact_threshold: float = 0.80
    neighbors_per_class: int = 3
    similarity_metric: str = "euclidean"
    similarity_cutoff: float | None = None
    similarity_conflict_ratio: float = 0.80
    deviation_zscore_threshold: float = 2.0
    expected_feature_names: tuple[str, ...] = FEATURE_NAMES
    expected_channels: tuple[str, ...] = EXPECTED_CHANNELS
    default_dataset_path: Path = PROJECT_ROOT / "data" / "dataset.csv"
    demo_dataset_path: Path = PROJECT_ROOT / "data" / "demo_opssat_fixture.csv"
    demo_scenarios_path: Path = PROJECT_ROOT / "data" / "demo_scenarios.json"
# --- end class AppConfig


# Callers can make a replacement configuration, such as one with a different seed,
# while this shared default remains available to later calls.
DEFAULT_CONFIG: AppConfig = AppConfig()


# __________________________________________
# END OF FILE
# ==========================================
