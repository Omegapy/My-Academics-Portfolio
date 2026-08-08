# -----------------------------------------------------------------------------
# File: handmade_shallow_ann.py
# Path: CTA_Module-3/handmade_shallow_ann.py
# Project: Critical Thinking Assignments for Foundations of Artificial Intelligence
# Module Type: executable script
# Author: Alexander S. Ricciardi
# Created: 2026-08-01
# Last Updated: 2026-08-04
# -----------------------------------------------------------------------------
# Course: CSC510 - Foundations of Artificial Intelligence
# Professor: Dr. Isaac Gang
# Term: Fall A (26FA) - 2026
# Assignment: Hand-Made Shallow ANN in Python
# -----------------------------------------------------------------------------
# Project Description:
# The program trains a small shallow ANN to predict fictional delivery times
# in minutes, and lets the user test the ANN.
# -----------------------------------------------------------------------------
# Assignment:
# Hand-Made Shallow ANN in Python
# Using your research and resources, write a basic 2-layer Artificial Neural Network
# utilizing static backpropagation using Numpy in Python. Your neural network can
# perform a basic function, such as guessing the next number in a series.
# Using the activation function of your choice to calculate the predicted output
# ŷ, known as the feedforward function, and updating the weights and biases
# through gradient descent (backpropagation) based on your choice of a basic loss
# function.
#
# Your ANN should include the following features:
#
# - An input layer that takes input data as a matrix receives and passes it on
# - A hidden layer
# - An output layer
# - Weights between the layers.
#
# Also, your ANN should demonstrate it can perform the following functions:
#
# - Multiply the input by a set of weights (via matrix multiplication)
# - Apply deliberate activation function for every hidden layer
# - Return an output
# - Calculate error by taking the difference from the desired output
#   and the predicted output giving us the gradient descent to provide our loss function
# - Apply loss function to weights
# - Repeat this process no less than 1,000 times to train the ANN
#
# Your submission should be a script with the .py extension.
# It should be able to be activated easily and have the ability to accept simple inputs,
# such as a series of a particular number of variables or digits, in a manner that is clear to
# the user and predict and visually the final variable in the input set.
# The input and output are up to you. Keep it simple.
#
# -----------------------------------------------------------------------------
# Contents Overview:
# - Class: ShallowANN
# - Functions: synthetic-data construction, standardization, input collection, and main()
#
# Requirements:
# - Python 3.11+
#
# -----------------------------------------------------------------------------

"""Train a small shallow ANN to predict fictional delivery times in minutes,
and let the user test the ANN.

The ANN's inputs are highway miles, local-road miles, and a binary traffic
congestion flag. The program uses feedforward propagation, loss evaluation,
backpropagation, and gradient-descent updates to train the ANN. Equation-related
variables begin with the symbols they implement, such as `x_`, `z1_`, `a1_`,
`y_hat_`, `j_`, and `d_j_d_`.
"""

# ____________________________________________________________________________________
# ====================================================================================
# ________________________________________________
# SHALLOW ARTIFICIAL NEURAL NETWORK COMPONENT MAP
# ================================================
#
# Equation, code-variable, and matrix map:
# X       -> x_input_matrix                              Matrix (m, 3)
# W1      -> self.W1                                     Matrix (3, 6)
# b1      -> self.b1                                     Matrix (1, 6)
# Z1      -> z1_hidden_pre_activations                   Matrix (m, 6)
# A1      -> a1_hidden_activations                       Matrix (m, 6)
# W2      -> self.W2                                     Matrix (6, 1)
# b2      -> self.b2                                     Matrix (1, 1)
# Y_hat   -> y_hat_predictions                           Matrix (m, 1)
# Y       -> y_target_matrix                             Matrix (m, 1)
# Y_hat-Y -> y_hat_minus_y_error                         Matrix (m, 1)
# J       -> j_mse_loss                                  scalar
# eta     -> eta_learning_rate                           scalar hyperparameter
# mu      -> mu_*_mean                                   mean statistic
# sigma   -> sigma_*_std                                 standard-deviation statistic
# dJ/d... -> d_j_d_*_gradient                            derivative matrix
# m       -> number of examples in the current batch
# @       -> matrix multiplication
#
# Naming rule:
# Equation-related variables begin with the symbol they represent, followed by a
# descriptive role. For example, `z1_hidden_pre_activations` stores `Z1`, while
# `d_j_d_w1_weight_gradient` stores `dJ/dW1`.
#
# __________________________________________
# HOW THE SYSTEM LEARNS: FOUR TRAINING PHASES
# __________________________________________
#
# The training loop repeats these phases in order:
#
# Phase 1: Feedforward Propagation
# - Pass X through the current W1, b1, W2, and b2 to calculate Y_hat.
#
# Phase 2: Loss-Function Evaluation
# - Compare Y_hat with the correct target Y and calculate prediction error and J.
#
# Phase 3: Backpropagation
# - Work backward from J to calculate gradients for every weight and bias.
#
# Phase 4: Optimization
# - Use eta and the calculated gradients to update W1, b1, W2, and b2.
#
# Execution loop:
# Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> repeat
#
# Important distinction:
# Backpropagation calculates gradients; optimization uses gradients.
#
# __________________________________________
# SHALLOW ANN ARCHITECTURE
# __________________________________________
# +----------------------+       +----------------------+       +----------------------+
# | INPUT LAYER          |       | HIDDEN LAYER         |       | OUTPUT LAYER         |
# | X Matrix: (m, 3)     |       | A1 Matrix: (m, 6)    |       | Y_hat Matrix: (m, 1) |
# |                      |       |                      |       |                      |
# | x1: highway miles    |       | h1: ReLU neuron      |       |                      |
# | x2: local-road miles |------>| h2: ReLU neuron      |------>| y_hat: predicted     |
# | x3: congestion flag  |       | h3: ReLU neuron      |       | delivery             |
# |                      |       | h4: ReLU neuron      |       | in minutes           |
# |                      |       | h5: ReLU neuron      |       |                      |
# |                      |       | h6: ReLU neuron      |       |                      |
# +----------------------+       +----------------------+       +----------------------+
#            |                              |                              |
#            |                              |                              |
#      W1 Matrix: (3, 6)               W2 Matrix: (6, 1)                   |
#      b1 Matrix: (1, 6)               b2 Matrix: (1, 1)                   |
#            |                              |                              |
#            +------------------------------+------------------------------+
#
# HOW THE SYSTEM LEARNS - PHASE 1
# Purpose: Given the current weights and biases, calculate prediction Y_hat.
#
# __________________________________________
# FORWARD PROPAGATION
# X -> Z1 -> A1 -> Y_hat
# __________________________________________
#
# Input data matrix:
# X Matrix = (m, 3)
#
# Each row of X contains:
# [ x1_highway_miles, x2_local_road_miles, x3_congestion_flag ]
#
#
#                 X (m, 3)
#                     |
#                     |  Multiply by input-to-hidden weights
#                     |  W1 Matrix = (3, 6)
#                     v
#               X @ W1  -----> Matrix = (m, 6)
#                     |
#                     |  Add hidden-layer bias
#                     |  b1 Matrix = (1, 6)
#                     v
#         Z1 = X @ W1 + b1 -----> Matrix = (m, 6)
#                     |
#                     |  Apply activation function
#                     |  A1 = ReLU(Z1)
#                     v
#               A1 (m, 6)
#                     |
#                     |  Multiply by hidden-to-output weights
#                     |  W2 Matrix = (6, 1)
#                     v
#               A1 @ W2 -----> Matrix = (m, 1)
#                     |
#                     |  Add output-layer bias
#                     |  b2 Matrix = (1, 1)
#                     v
#       Y_hat = A1 @ W2 + b2 -----> Matrix = (m, 1)
#                     |
#                     |  Final prediction
#                     v
#            Y_hat (predicted output)
#
#
# Forward equations:
#
# Z1    = X @ W1 + b1
# A1    = ReLU(Z1)
# Y_hat = A1 @ W2 + b2

# _________________________________________________________________
# HOW THE SYSTEM LEARNS - PHASE 2: LOSS-FUNCTION EVALUATION
# Y_hat -> Y_hat - Y -> J
# _________________________________________________________________
#
# Purpose: Compare the prediction Y_hat with the correct target Y.
#
# Step 1: Calculate prediction error.
#
# error = Y_hat - Y
# error Matrix = (m, 1)
#
# Step 2: Calculate mean squared error loss J.
#
# J = mean(error ** 2)
# J = mean((Y_hat - Y) ** 2)
#
# Phase 2 measures prediction quality. It does not calculate parameter gradients
# and does not update any weights or biases.

# HOW THE SYSTEM LEARNS - PHASE 3
# Purpose: Work backward from J to calculate the parameter gradients.
#
# _________________________________________________________________
# BACKPROPAGATION
# Y_hat -> Y_hat - Y -> dJ/dY_hat -> dJ/dW2, dJ/db2 -> dJ/dA1 -> dJ/dW1, dJ/db1
# _________________________________________________________________
#
# Start with:
# Y_hat Matrix = (m, 1)
# Y     Matrix = (m, 1)
#
# Step 1: Compute prediction error
#
# error = Y_hat - Y
# error Matrix = (m, 1)
#                     |
#                     v
#
# Step 2: Differentiate loss with respect to prediction
#
# For MSE:
# J = mean(error^2)
#
# dJ/dY_hat = (2 / error.size) * error
# dJ/dY_hat Matrix = (m, 1)
#                     |
#                     v
#
# Step 3: Compute output-layer gradients
#
# A1.T Matrix = (6, m)
# dJ/dY_hat Matrix = (m, 1)
#
# dJ/dW2 = A1.T @ dJ/dY_hat
# dJ/dW2 Matrix = (6, 1)
#
# dJ/db2 = sum(dJ/dY_hat, axis=0, keepdims=True)
# dJ/db2 Matrix = (1, 1)
#                     |
#                     v
#
# Step 4: Move the gradient backward into the hidden layer
#
# W2.T Matrix = (1, 6)
#
# dJ/dA1 = dJ/dY_hat @ W2.T
# dJ/dA1 Matrix = (m, 6)
#                     |
#                     v
#
# Step 5: Apply derivative of the activation function
#
# ReLU'(Z1) Matrix = (m, 6)
#
# dJ/dZ1 = dJ/dA1 * ReLU'(Z1)
# dJ/dZ1 Matrix = (m, 6)
#                     |
#                     v
#
# Step 6: Compute hidden-layer gradients
#
# X.T Matrix = (3, m)
# dJ/dZ1 Matrix = (m, 6)
#
# dJ/dW1 = X.T @ dJ/dZ1
# dJ/dW1 Matrix = (3, 6)
#
# dJ/db1 = sum(dJ/dZ1, axis=0, keepdims=True)
# dJ/db1 Matrix = (1, 6)
#                     |
#                     v
#
# The gradient calculations above complete Phase 3: Backpropagation.
# The parameter-update equations below begin Phase 4: Optimization.
#
# Step 7: Use gradients in optimization
#
# W1_new = W1_old - eta * dJ/dW1
# b1_new = b1_old - eta * dJ/db1
# W2_new = W2_old - eta * dJ/dW2
# b2_new = b2_old - eta * dJ/db2
#
# HOW THE SYSTEM LEARNS - PHASE 4: OPTIMIZATION
# Purpose: Use eta and the gradients to change the trainable parameters.
# After the update, the next training iteration returns to Phase 1 and calculates
# a new Y_hat with the updated W1, b1, W2, and b2 values.
#
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

import os
import sys
import textwrap

# pyrefly: ignore [missing-import]
import numpy as np


# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

# Matrix
INPUT_SIZE: int = 3 # Input Matrix 3 inputs (m,3)
HIDDEN_SIZE: int = 6 # Hidden Matrix 6 hidden neurons (m,6)
OUTPUT_SIZE: int = 1 # Output Matrix 1 output neuron (m,1)

# Training parameters
ETA_LEARNING_RATE: float = 0.05  # Learning rate eta for gradient descent.
TRAINING_ITERATIONS: int = 5_000 # Training iterations (default 1000)
RANDOM_SEED: int = 510 # Random seed for reproducibility (default 510)

# Training inputs constraints used to generate the training data.
TRAINING_HIGHWAY_MIN_MILES: int = 0    # Minimum highway miles
TRAINING_HIGHWAY_MAX_MILES: int = 30   # Maximum highway miles
TRAINING_HIGHWAY_STEP_MILES: int = 2   # Step size for highway miles
TRAINING_LOCAL_MIN_MILES: int = 0    # Minimum local-road miles
TRAINING_LOCAL_MAX_MILES: int = 10   # Maximum local-road miles
TRAINING_EXAMPLE_COUNT: int = 352    # Number of training examples

# Assumptions for calculating delivery time used to generate training labels
# The labels are not real estimates, but are used to train the ANN to predict delivery time.
PREPARATION_MINUTES: float = 10.0       # Delivery preparation time in minutes
NORMAL_HIGHWAY_SPEED_MPH: float = 50.0  # Normal highway speed in MPH
CONGESTED_HIGHWAY_SPEED_MPH: float = 25.0 # Congested highway speed in MPH
LOCAL_ROAD_SPEED_MPH: float = 20.0      # Local road speed in MPH

# Display width used for print formatting
DISPLAY_WIDTH: int = 76

# Console-presentation settings. ANSI color codes require no third-party package.
# Colors are used only when the output terminal supports them.
USE_CONSOLE_COLORS: bool = True
PAUSE_BETWEEN_SECTIONS: bool = True

# ANSI formatting codes used by the display helpers.
ANSI_RESET: str = "\033[0m"
ANSI_BOLD: str = "\033[1m"
ANSI_DIM: str = "\033[2m"
ANSI_RED: str = "\033[31m"
ANSI_GREEN: str = "\033[32m"
ANSI_YELLOW: str = "\033[33m"
ANSI_BLUE: str = "\033[34m"
ANSI_MAGENTA: str = "\033[35m"
ANSI_CYAN: str = "\033[36m"
ANSI_DEFAULT: str = "\033[39m"

# ____________________________________________________________________________________
# ====================================================================================
# __________________________________________
# SHALLOW ARTIFICIAL NEURAL NETWORK
# ==========================================

# Equation-aligned code names used by this class:
# X       -> x_input_matrix
# Z1      -> z1_hidden_pre_activations
# A1      -> a1_hidden_activations
# Y_hat   -> y_hat_predictions
# Y_hat-Y -> y_hat_minus_y_error
# J       -> j_mse_loss
# dJ/d... -> d_j_d_*_gradient
# eta     -> eta_learning_rate
# ====================================================================================

# --- class ShallowANN
class ShallowANN:
    """Implement a one-hidden-layer regression ANN with explicit NumPy mathematics.

    The input layer is the data matrix. The network has two trainable weights and bias
    pairs: `W1` and `b1` from input to hidden, `W2` and `b2` from hidden to output.

    The network contains three layers of neurons:

          Input layer            Hidden layer           Output layer
        3 input values      →  6 neurons           →  1 prediction

    However, only two of those layers' connections have trainable weights:

        X  ── W1, b1 ──>  Hidden layer  ── W2, b2 ──>  Output

    ReLU is used as the hidden-layer activation function, introducing the
    nonlinearity needed to learn the synthetic relationship.

    Core Equations:
        `Z1 = X @ W1 + b1`
        `A1 = ReLU(Z1)`
        `Y_hat = A1 @ W2 + b2`

    Equation-to-Code Convention:
        Equation-related local variables begin with the symbol they represent.
        For example, `z1_hidden_pre_activations` stores `Z1`, and
        `d_j_d_w1_weight_gradient` stores `dJ/dW1`.

    Attributes:
        input_size: Number of input features for each input row.
        hidden_size: Number of neurons in the hidden layer.
        output_size: Number of predictions for each input row.
        W1: Input-to-hidden weight matrix.
        b1: Hidden-layer bias row.
        W2: Hidden-to-output weight matrix.
        b2: Output-layer bias row.
        updates_completed: Number of gradient-descent updates applied.
    """

    # __________________________________
    # ==================================
    #
    # Initialization
    #
    # ==================================

    # --- __init__()
    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        *,  # Use * to make seed a keyword-only argument.
        seed: int,  # Random seed for reproducibility.
    ) -> None:
        """Initialize the layer sizes, trainable parameters, and random generator.

        Args:
            input_size: Number of input features represented by the columns of `X`.
            hidden_size: Number of hidden neurons represented by the columns of `Z1`
                and `A1`.
            output_size: Number of output values represented by the columns of
                `Y_hat`.
            seed: Integer used to make random initialization repeatable.

        Related Equations:
            `W1 = random_normal(input_size, hidden_size) * sqrt(2 / input_size)`
            `b1 = 0`
            `W2 = random_normal(hidden_size, output_size) * sqrt(1 / hidden_size)`
            `b2 = 0`
            `theta = {W1, b1, W2, b2}`

        Equation Relationship:
            This method creates the trainable parameter set `theta` used by the
            feedforward, backpropagation, and optimization equations. It initializes
            `W1` for the ReLU hidden layer with He scaling and `W2` for the linear
            output layer with Xavier-style scaling.

        Raises:
            ValueError: If a layer size is not positive or the seed is not an integer.
        """
        # __________________________
        # Init layers
        # --------------------------

        layer_sizes = (input_size, hidden_size, output_size)

        # Validate that matrix dimensions are positive integers.
        if any(
            isinstance(size, bool) or not isinstance(size, int) or size <= 0
            for size in layer_sizes
        ):
            raise ValueError("all layer sizes must be positive integers")
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValueError("seed must be an integer")

        self.input_size: int = input_size
        self.hidden_size: int = hidden_size
        self.output_size: int = output_size
        self.updates_completed: int = 0

        # Initialize the random number generator with the provided seed.
        rng_generator = np.random.default_rng(seed)

        # ______________________________
        # Init weights and biases
        # ------------------------------

        # --------------------------- W1 and b1 initialization
        # ASSIGNMENT REQUIREMENT MET: W1 provides trainable weights between
        # the input layer and the hidden layer.
        # W1 matrix dimensions are (input_size, hidden_size).
        self.W1: np.ndarray = (
            # Generate random values with dimensions (input_size, hidden_size).
            rng_generator.standard_normal(
                (input_size, hidden_size),
                dtype=np.float64,
            )
            # He scaling: W1 = random values * sqrt(2 / input_size).
            * np.sqrt(2.0 / input_size)
        )
        # b1 matrix dimensions are (1, hidden_size); b1 = 0.
        self.b1: np.ndarray = np.zeros((1, hidden_size), dtype=np.float64)

        # --------------------------- W2 and b2 initialization
        # ASSIGNMENT REQUIREMENT MET: W2 provides trainable weights between
        # the hidden layer and the output layer.
        # W2 matrix dimensions are (hidden_size, output_size).
        self.W2: np.ndarray = (
            # Generate random values with dimensions (hidden_size, output_size).
            rng_generator.standard_normal(
                (hidden_size, output_size),
                dtype=np.float64,
            )
            # Xavier-style scaling: W2 = random values * sqrt(1 / hidden_size).
            * np.sqrt(1.0 / hidden_size)
        )
        # b2 matrix dimensions are (1, output_size); b2 = 0.
        self.b2: np.ndarray = np.zeros((1, output_size), dtype=np.float64)
        # ---------------------------
    # ---

    # ______________________________
    # Helper Validation Method
    # ------------------------------

    # --- _validate_input_matrix()
    def _validate_input_matrix(self, x_inputs: np.ndarray) -> np.ndarray:
        """Return a finite two-dimensional matrix representing equation input `X`.

        Args:
            x_inputs: Input values intended to represent the network matrix `X`.

        Returns:
            `x_input_matrix`, a validated matrix with shape
            `(batch_size, self.input_size)`.

        Related Equation:
            `Z1 = X @ W1 + b1`

        Equation Relationship:
            The returned variable `x_input_matrix` represents `X` in the equation
            above. This helper validates `X`; it does not evaluate the equation.

        Raises:
            ValueError: If `X` has invalid dimensions or contains a non-finite value.
        """
        x_input_matrix = np.asarray(x_inputs, dtype=np.float64)

        # Validate input matrix X.
        if (
            # X must have two dimensions.
            x_input_matrix.ndim != 2
            # X must contain at least one input row.
            or x_input_matrix.shape[0] == 0
            # X must contain the expected number of input-feature columns.
            or x_input_matrix.shape[1] != self.input_size
        ):
            raise ValueError(
                f"x_inputs must be a matrix with dimensions "
                f"(batch_size, {self.input_size})",
            )

        # Check X for NaN or infinity.
        if not np.all(np.isfinite(x_input_matrix)):
            raise ValueError("x_inputs must contain only finite values")

        return x_input_matrix
    # ---

    # ____________________________________________________________________________________
    # ====================================================================================
    #
    # Inference and Training
    #
    # ====================================================================================

    # ____________________________________________________________
    # Activation Function
    # This function is used both for inference and training
    # ============================================================
    #
    # Learning-phase roles:
    # - relu() is used during Phase 1 to calculate A1 from Z1.
    # - relu_derivative() is used during Phase 3 to calculate dJ/dZ1.

    # --- relu()
    @staticmethod  # Static methods do not require access to self or cls.
    def relu(z_pre_activations: np.ndarray) -> np.ndarray:
        """Apply the Rectified Linear Unit activation function to `Z`.

        Args:
            z_pre_activations: Pre-activation values represented by `Z`. During this
                network's feedforward pass, these values are `Z1`.

        Returns:
            `a_activations`, the activation values represented by `A`. During this
            network's feedforward pass, the returned matrix is `A1`.

        Related Equation:
            `A = ReLU(Z) = max(0, Z)`

        Equation Relationship:
            This mathematical function transforms each pre-activation in `Z` into
            an activation in `A`. Positive values pass through; zero and negative
            values become zero.
        """
        a_activations = np.maximum(0.0, z_pre_activations)
        return a_activations
    # ---

    # --- relu_derivative()
    @staticmethod
    def relu_derivative(z_pre_activations: np.ndarray) -> np.ndarray:
        """Calculate the ReLU derivative evaluated at pre-activations `Z`.

        Args:
            z_pre_activations: Pre-activation values `Z`. During backpropagation,
                this network passes the cached hidden pre-activations `Z1`.

        Returns:
            `d_relu_d_z`, an element-wise derivative matrix containing `1.0` where
            `Z > 0` and `0.0` where `Z <= 0`.

        Related Equation:
            `dReLU(Z) / dZ = 1 when Z > 0; otherwise 0`

        Equation Relationship:
            Backpropagation multiplies this derivative by `dJ/dA1` to calculate
            `dJ/dZ1 = dJ/dA1 * ReLU'(Z1)`.
        """
        d_relu_d_z = np.where(z_pre_activations > 0.0, 1.0, 0.0)
        return d_relu_d_z
    # ---

    # HOW THE SYSTEM LEARNS - PHASE 1: FEEDFORWARD PROPAGATION
    # Question answered: What prediction does the network produce with its current
    # weights and biases?
    #
    # __________________________________________________________________________________________________
    # Feedforward - forward pass or Feedforward propagation
    #
    # Feedforward propagation is used for both
    # training (calculating loss) and inference (making predictions).
    # During training, the output `Y_hat` is compared to the target values `Y` to calculate the loss.
    # During inference, the output `Y_hat` is the final prediction of the network.
    # =================================================================================================

    # --- feedforward()
    def feedforward(
        self,
        x_inputs: np.ndarray,
    ) -> tuple[np.ndarray, dict[str, np.ndarray]]:
        """Evaluate the three feedforward equations for training or inference.

        Args:
            x_inputs: Standardized input matrix `X` with dimensions `(m, 3)`.
                Standardization uses training-set statistics:
                `X_standardized = (X - mu_X) / sigma_X`.

        Returns:
            A tuple containing:
                - `y_hat_predictions`: `Y_hat`, with shape `(m, 1)`, on the
                  standardized target scale.
                - `forward_cache`: The `Z1` and `A1` matrices required by
                  backpropagation.

        Related Equations:
            `Z1 = X @ W1 + b1`
            `A1 = ReLU(Z1)`
            `Y_hat = A1 @ W2 + b2`

        Equation Relationship:
            This method is the feedforward-propagation process. It evaluates the
            affine hidden-layer function, the ReLU activation function, and the
            linear output-layer function in sequence. Its equation-aligned local
            variables are `x_input_matrix`, `z1_hidden_pre_activations`,
            `a1_hidden_activations`, and `y_hat_predictions`.

        Logic:
            1. Calculate hidden pre-activations `Z1`.
            2. Apply ReLU to calculate hidden activations `A1`.
            3. Calculate output predictions `Y_hat`.

              X @ W1 + b1   ->   Z1   ->   ReLU(Z1)   ->   A1   ->   A1 @ W2 + b2   ->   Y_hat
        """
        # ASSIGNMENT REQUIREMENT: The input layer receives input data as
        # matrix X and passes it to the input-to-hidden transformation.
        x_input_matrix = self._validate_input_matrix(x_inputs)

        # ASSIGNMENT REQUIREMENT: Multiply input matrix X by W1 using
        # NumPy matrix multiplication (@) to supply the hidden layer.
        # Step 1: X @ W1 + b1 -> Z1
        # The variable name begins with z1 so it visibly matches the equation output.
        z1_hidden_pre_activations = x_input_matrix @ self.W1 + self.b1

        # ASSIGNMENT REQUIREMENT: A1 represents the ANN's hidden layer,
        # and ReLU is the deliberate activation applied to that hidden layer.
        # Step 2: ReLU(Z1) -> A1
        # The variable name begins with a1 so it visibly matches the equation output.
        a1_hidden_activations = self.relu(z1_hidden_pre_activations)

        # ASSIGNMENT REQUIREMENT: Y_hat represents the output layer, and
        # W2 connects hidden activations A1 to that output layer.
        # ASSIGNMENT REQUIREMENT A1 @ W2 performs the hidden-to-output
        # matrix multiplication using the second set of weights.
        # Step 3: A1 @ W2 + b2 -> Y_hat
        # The y_hat prefix marks an estimated output rather than the correct target Y.
        y_hat_predictions = a1_hidden_activations @ self.W2 + self.b2

        # A non-finite Y_hat indicates unstable calculations.
        if not np.all(np.isfinite(y_hat_predictions)):
            raise FloatingPointError("feedforward produced a non-finite prediction")

        # Cache Z1 and A1 because backpropagation needs both matrices.
        forward_cache = {
            "z1_hidden_pre_activations": z1_hidden_pre_activations,
            "a1_hidden_activations": a1_hidden_activations,
        }
        # ASSIGNMENT REQUIREMENT: Return the predicted output Y_hat with
        # the cached hidden-layer values required during training.
        return y_hat_predictions, forward_cache
    # ---

    # ____________________________________________________________________________________
    # ====================================================================================
    #
    # Training
    #
    # ====================================================================================

    # HOW THE SYSTEM LEARNS - PHASE 2: LOSS-FUNCTION EVALUATION
    # Question answered: How different is Y_hat from the correct target Y?
    #
    # ________________________________
    # Calculate Loss Function
    # ================================

    # --- calculate_loss()
    @staticmethod
    def calculate_loss(y_hat_minus_y_error: np.ndarray) -> float:
        """Calculate scalar mean squared error `J` from `Y_hat - Y`.

        Args:
            y_hat_minus_y_error: Prediction-error matrix calculated as
                `Y_hat - Y`.

        Returns:
            `j_mse_loss`, the scalar mean squared error `J`.

        Related Equations:
            `error = Y_hat - Y`
            `J = mean(error ** 2)`
            `J = mean((Y_hat - Y) ** 2)`

        Equation Relationship:
            This mathematical loss function receives the already calculated
            prediction difference, squares every value, and returns their mean as
            `J`. It measures prediction quality but does not calculate gradients or
            update parameters.
        """
        y_hat_minus_y_error_matrix = np.asarray(
            y_hat_minus_y_error,
            dtype=np.float64,
        )

        # MSE requires at least one finite value from Y_hat - Y.
        if (
            y_hat_minus_y_error_matrix.size == 0
            or not np.all(np.isfinite(y_hat_minus_y_error_matrix))
        ):
            raise ValueError(
                "y_hat_minus_y_error must contain at least one finite value",
            )

        j_mse_loss = float(np.mean(y_hat_minus_y_error_matrix**2))
        return j_mse_loss
    # --- end calculate_loss()

    # HOW THE SYSTEM LEARNS - PHASE 3: BACKPROPAGATION
    # Question answered: Which weights and biases affected J, and by how much?
    #
    # ________________________________________
    # Backpropagation
    # ========================================

    # --- backpropagate()
    def backpropagate(
        self,
        x_inputs: np.ndarray,
        y_hat_minus_y_error: np.ndarray,
        forward_cache: dict[str, np.ndarray],
    ) -> dict[str, np.ndarray]:
        """Calculate every parameter gradient without updating the parameters.

        Args:
            x_inputs: Standardized input matrix `X` from the matching feedforward
                pass, with shape `(m, 3)`.
            y_hat_minus_y_error: Prediction difference `Y_hat - Y`, with shape
                `(m, 1)`, on the standardized target scale.
            forward_cache: Hidden-layer values from the matching feedforward pass.
                It must contain `z1_hidden_pre_activations` for `Z1` and
                `a1_hidden_activations` for `A1`.

        Returns:
            `parameter_gradients`, a dictionary containing:
                - `"dJ_dW1"`: `dJ/dW1`, with shape `(3, 6)`.
                - `"dJ_db1"`: `dJ/db1`, with shape `(1, 6)`.
                - `"dJ_dW2"`: `dJ/dW2`, with shape `(6, 1)`.
                - `"dJ_db2"`: `dJ/db2`, with shape `(1, 1)`.

        Related Equations:
            `dJ/dY_hat = (2 / error.size) * (Y_hat - Y)`
            `dJ/dW2 = A1.T @ dJ/dY_hat`
            `dJ/db2 = sum(dJ/dY_hat, axis=0)`
            `dJ/dA1 = dJ/dY_hat @ W2.T`
            `dJ/dZ1 = dJ/dA1 * ReLU'(Z1)`
            `dJ/dW1 = X.T @ dJ/dZ1`
            `dJ/db1 = sum(dJ/dZ1, axis=0)`

        Equation Relationship:
            Backpropagation is the algorithm that follows the dependency path from
            `J` toward `W2`, `b2`, `W1`, and `b1`. Each local gradient variable
            starts with `d_j_d_` so its name mirrors the derivative it stores.
            This method calculates gradients only. `apply_gradients()` performs the
            separate optimization step that updates the parameters.
        """
        x_input_matrix = self._validate_input_matrix(x_inputs)
        y_hat_minus_y_error_matrix = np.asarray(
            y_hat_minus_y_error,
            dtype=np.float64,
        )
        expected_error_dimensions = (x_input_matrix.shape[0], self.output_size)

        # Y_hat - Y must align with the input rows and output neurons.
        if y_hat_minus_y_error_matrix.shape != expected_error_dimensions:
            raise ValueError(
                "y_hat_minus_y_error matrix must have dimensions "
                f"{expected_error_dimensions}",
            )

        # Y_hat - Y must contain only finite values.
        if not np.all(np.isfinite(y_hat_minus_y_error_matrix)):
            raise ValueError("y_hat_minus_y_error must contain only finite values")

        # Extract equation values Z1 and A1 from the matching feedforward cache.
        z1_hidden_pre_activations = forward_cache["z1_hidden_pre_activations"]
        a1_hidden_activations = forward_cache["a1_hidden_activations"]

        # Step 1: Calculate dJ/dY_hat from J = mean((Y_hat - Y) ** 2).
        d_j_d_y_hat_output_gradient = (
            2.0 / y_hat_minus_y_error_matrix.size
        ) * y_hat_minus_y_error_matrix

        # Step 2: Calculate dJ/dW2 and dJ/db2.
        d_j_d_w2_weight_gradient = (
            a1_hidden_activations.T @ d_j_d_y_hat_output_gradient
        )
        d_j_d_b2_bias_gradient = np.sum(
            d_j_d_y_hat_output_gradient,
            axis=0,
            keepdims=True,
        )

        # Step 3: Apply the chain rule through W2 to calculate dJ/dA1.
        d_j_d_a1_hidden_activation_gradient = (
            d_j_d_y_hat_output_gradient @ self.W2.T
        )

        # Step 4: Apply ReLU'(Z1) to calculate dJ/dZ1.
        d_j_d_z1_hidden_pre_activation_gradient = (
            d_j_d_a1_hidden_activation_gradient
            * self.relu_derivative(z1_hidden_pre_activations)
        )

        # Step 5: Combine X with dJ/dZ1 to calculate dJ/dW1 and dJ/db1.
        d_j_d_w1_weight_gradient = (
            x_input_matrix.T @ d_j_d_z1_hidden_pre_activation_gradient
        )
        d_j_d_b1_bias_gradient = np.sum(
            d_j_d_z1_hidden_pre_activation_gradient,
            axis=0,
            keepdims=True,
        )

        # Store each derivative under an equation-aligned dictionary key.
        parameter_gradients = {
            "dJ_dW1": d_j_d_w1_weight_gradient,
            "dJ_db1": d_j_d_b1_bias_gradient,
            "dJ_dW2": d_j_d_w2_weight_gradient,
            "dJ_db2": d_j_d_b2_bias_gradient,
        }

        # Stop instead of returning a NaN or infinite derivative.
        if not all(
            np.all(np.isfinite(gradient_matrix))
            for gradient_matrix in parameter_gradients.values()
        ):
            raise FloatingPointError("backpropagation produced a non-finite gradient")

        return parameter_gradients
    # ---

    # HOW THE SYSTEM LEARNS - PHASE 4: OPTIMIZATION
    # Question answered: Given the gradients, how should the parameters change?
    #
    # ________________________________________________
    # Updates weights and biases using gradients
    # ------------------------------------------------

    # --- apply_gradients()
    def apply_gradients(
        self,
        parameter_gradients: dict[str, np.ndarray],
        eta_learning_rate: float,
    ) -> None:
        """Apply gradient-descent equations to `W1`, `b1`, `W2`, and `b2`.

        Args:
            parameter_gradients: Derivative matrices calculated by
                `backpropagate()`, keyed as `dJ_dW1`, `dJ_db1`, `dJ_dW2`, and
                `dJ_db2`.
            eta_learning_rate: Positive learning rate `eta` controlling the size
                of each parameter update.

        Related Equations:
            `W1_new = W1_old - eta * dJ/dW1`
            `b1_new = b1_old - eta * dJ/db1`
            `W2_new = W2_old - eta * dJ/dW2`
            `b2_new = b2_old - eta * dJ/db2`
            `theta_new = theta_old - eta * gradient(J)`

        Equation Relationship:
            This method performs Phase 4, optimization. Backpropagation supplies
            the derivative values; this method uses them to replace each old
            parameter with its gradient-descent update.

        Raises:
            ValueError: If `eta` is invalid or a gradient has invalid dimensions.
            FloatingPointError: If an updated parameter becomes non-finite.
        """
        # Validate the learning rate eta.
        if not np.isfinite(eta_learning_rate) or eta_learning_rate <= 0.0:
            raise ValueError("eta_learning_rate must be a positive finite value")

        # Each derivative must match the dimensions of its corresponding parameter.
        expected_gradient_dimensions = {
            "dJ_dW1": self.W1.shape,
            "dJ_db1": self.b1.shape,
            "dJ_dW2": self.W2.shape,
            "dJ_db2": self.b2.shape,
        }

        for gradient_name, expected_dimensions in expected_gradient_dimensions.items():
            if (
                gradient_name not in parameter_gradients
                or parameter_gradients[gradient_name].shape != expected_dimensions
            ):
                raise ValueError(
                    f"{gradient_name} matrix must have dimensions "
                    f"{expected_dimensions}",
                )

        # --- Phase 4: Gradient Descent Optimization
        # ASSIGNMENT REQUIREMENT MET: Apply the loss-derived gradients to
        # W1 and W2 through gradient-descent weight updates.
        # W_new = W_old - eta * dJ/dW
        # b_new = b_old - eta * dJ/db
        self.W1 = self.W1 - eta_learning_rate * parameter_gradients["dJ_dW1"]
        self.b1 = self.b1 - eta_learning_rate * parameter_gradients["dJ_db1"]
        self.W2 = self.W2 - eta_learning_rate * parameter_gradients["dJ_dW2"]
        self.b2 = self.b2 - eta_learning_rate * parameter_gradients["dJ_db2"]

        # Increment the number of completed theta updates.
        self.updates_completed += 1

        # Stop instead of continuing with NaN or infinite parameter values.
        theta_parameters = (self.W1, self.b1, self.W2, self.b2)
        if not all(
            np.all(np.isfinite(parameter_matrix))
            for parameter_matrix in theta_parameters
        ):
            raise FloatingPointError("gradient descent produced a non-finite parameter")
    # ---

    # HOW THE SYSTEM LEARNS - EXECUTION LOOP
    # train() repeats Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 for every
    # requested training iteration.
    #
    # ______________________________
    # Train the model
    # ==============================

    # --- train()
    def train(
        self,
        x_inputs: np.ndarray,
        y_targets: np.ndarray,
        *,
        iterations: int,
        eta_learning_rate: float,
    ) -> list[tuple[int, float]]:
        """Train the ANN by repeating the four learning phases.

        Args:
            x_inputs: Standardized training matrix `X`.
            y_targets: Standardized correct-output matrix `Y`.
            iterations: Positive number of complete training and update rounds.
            eta_learning_rate: Positive learning rate `eta` used by gradient
                descent.

        Returns:
            `j_loss_history`, containing selected `(completed updates, J)`
            checkpoints, including the initial loss before training.

        Related Equations:
            Phase 1: `Y_hat = feedforward(X; W1, b1, W2, b2)`
            Phase 2: `error = Y_hat - Y`; `J = mean(error ** 2)`
            Phase 3: calculate `dJ/dW1`, `dJ/db1`, `dJ/dW2`, and `dJ/db2`
            Phase 4: `theta_new = theta_old - eta * gradient(J)`

        Equation Relationship:
            This method is the execution loop that coordinates the processes and
            mathematical functions. It does not merge backpropagation with
            optimization: `backpropagate()` calculates derivatives, then
            `apply_gradients()` uses those derivatives to update the parameters.
        """
        # Validate and name the standardized equation matrix X.
        x_input_matrix = self._validate_input_matrix(x_inputs)

        # Convert and name the standardized correct-output matrix Y.
        y_target_matrix = np.asarray(y_targets, dtype=np.float64)
        expected_y_target_dimensions = (
            x_input_matrix.shape[0],
            self.output_size,
        )

        # ____________________________________________
        # Validate the training configuration and Y.
        # --------------------------------------------

        if (
            isinstance(iterations, bool)
            or not isinstance(iterations, int)
            or iterations <= 0
        ):
            raise ValueError("iterations must be a positive integer")

        if not np.isfinite(eta_learning_rate) or eta_learning_rate <= 0.0:
            raise ValueError("eta_learning_rate must be a positive finite value")

        if y_target_matrix.shape != expected_y_target_dimensions:
            raise ValueError(
                f"y_targets matrix must have dimensions "
                f"{expected_y_target_dimensions}",
            )

        # ________________________________________
        # Initialize prediction and loss variables.
        # ----------------------------------------

        # INITIAL CHECKPOINT: Run Phase 1 and Phase 2 before any Phase 3 gradient
        # calculation or Phase 4 parameter update.

        # Y_hat before the first parameter update.
        y_hat_initial_predictions, _ = self.feedforward(x_input_matrix)
        # error = Y_hat - Y before training.
        y_hat_minus_y_initial_error = (
            y_hat_initial_predictions - y_target_matrix
        )
        # J before training.
        j_initial_mse_loss = self.calculate_loss(y_hat_minus_y_initial_error)
        # Stored J checkpoints.
        j_loss_history = [(0, j_initial_mse_loss)]

        # _______________________________________________
        # Training loop and checkpoint configuration.
        # -----------------------------------------------

        checkpoint_interval = max(1, iterations // 5)
        checkpoints = set(
            range(checkpoint_interval, iterations + 1, checkpoint_interval),
        )
        checkpoints.update((1, iterations))

        # ----- MAIN ITERATION LOOP: Repeat the four learning phases. -----
        # ASSIGNMENT REQUIREMENT MET: Repeat feedforward propagation, loss
        # evaluation, backpropagation, and optimization for the requested
        # training count. main() supplies 5,000 iterations, exceeding the
        # assignment minimum of 1,000 iterations.
        for iteration in range(1, iterations + 1):
            # Phase 1 purpose: Produce Y_hat from X and the current parameters.
            # Phase 1: Calculate Y_hat through feedforward propagation.
            y_hat_predictions, forward_cache = self.feedforward(x_input_matrix)

            # Phase 2 purpose: Measure how different Y_hat is from Y.
            # Phase 2: Calculate error = Y_hat - Y and then scalar loss J.
            # ASSIGNMENT REQUIREMENT MET: Calculate prediction error by
            # subtracting desired output Y from predicted output Y_hat.
            y_hat_minus_y_error = y_hat_predictions - y_target_matrix
            # ASSIGNMENT REQUIREMENT MET: Use Y_hat - Y to evaluate the
            # mean squared error loss function J.
            j_current_mse_loss = self.calculate_loss(y_hat_minus_y_error)

            if not np.isfinite(j_current_mse_loss):
                raise FloatingPointError(
                    f"J became non-finite at training round {iteration}",
                )

            # Phase 3 purpose: Calculate how each parameter affected J.
            # Phase 3: Calculate dJ/dW1, dJ/db1, dJ/dW2, and dJ/db2.
            # ASSIGNMENT REQUIREMENT MET: Backpropagation calculates how the
            # loss J changes with W1 and W2, linking the loss function to
            # both sets of weights through dJ/dW1 and dJ/dW2.
            parameter_gradients = self.backpropagate(
                x_input_matrix,
                y_hat_minus_y_error,
                forward_cache,
            )

            # Phase 4 purpose: Update the parameters in the direction that
            # attempts to reduce J.
            # Phase 4: Apply theta_new = theta_old - eta * gradient(J).
            self.apply_gradients(parameter_gradients, eta_learning_rate)

            # CHECKPOINT: Calculate post-update J only at reporting rounds.
            if iteration in checkpoints:
                y_hat_updated_predictions = self.predict(x_input_matrix)
                y_hat_minus_y_updated_error = (
                    y_hat_updated_predictions - y_target_matrix
                )
                j_updated_mse_loss = self.calculate_loss(
                    y_hat_minus_y_updated_error,
                )
                j_loss_history.append((iteration, j_updated_mse_loss))

        return j_loss_history
    # ---

    # INFERENCE USE OF PHASE 1
    # predict() uses feedforward propagation only. Phases 2, 3, and 4 are not
    # performed because inference does not compare against Y or update parameters.
    #
    # _____________________________
    # Predict
    # =============================

    # --- predict()
    def predict(self, x_inputs: np.ndarray) -> np.ndarray:
        """Return `Y_hat` from feedforward propagation without changing `theta`.

        Args:
            x_inputs: Standardized matrix `X` with shape `(m, INPUT_SIZE)`.
                Each row contains `[highway miles, local-road miles,
                congestion flag]` after standardization.

        Returns:
            `y_hat_predictions`, a matrix `Y_hat` with shape
            `(m, OUTPUT_SIZE)`.

        Related Equation:
            `Y_hat = F_theta(X)`

        Equation Relationship:
            This inference helper calls `feedforward()` and returns only its
            predicted output `Y_hat`. It discards the `Z1` and `A1` cache because
            inference does not run backpropagation.
        """
        y_hat_predictions, _ = self.feedforward(x_inputs)
        # ASSIGNMENT REQUIREMENT MET: Return Y_hat as the ANN's predicted
        # output for the supplied input matrix X.
        return y_hat_predictions
    # ---
# --- end class ShallowANN

# ____________________________________________________________________________________
# ====================================================================================
#
# Synthetic training data
# Used to generate a synthetic dataset of 352 examples for training the ANN.
#
# PRE-TRAINING PREPARATION
# This data-construction section prepares X and Y before the four learning phases
# begin. It is not itself one of the four learning phases.
#
# Target = 10 + (highway miles / highway speed) * 60
#             + (local-road miles / 20) * 60
#
# ====================================================================================

#_______________________________________________________
#   Calculations for synthetic data (Training data)
#=======================================================

# --- calculate_synthetic_target_minutes()
def calculate_synthetic_target_minutes(
    x1_highway_miles: float,
    x2_local_road_miles: float,
    x3_congestion_flag: int,
) -> float:
    """Calculate one synthetic correct target `Y` in delivery minutes.

    Args:
        x1_highway_miles: Input feature `x1`, the highway distance.
        x2_local_road_miles: Input feature `x2`, the local-road distance.
        x3_congestion_flag: Input feature `x3`, where `0` means normal traffic
            and `1` means congested traffic.

    Returns:
        `y_target_minutes`, the synthetic correct output `Y` consisting of
        preparation, highway-travel, and local-road-travel minutes.

    Related Equation:
        `Y = preparation_minutes`
        `    + (x1_highway_miles / highway_speed_mph) * 60`
        `    + (x2_local_road_miles / local_road_speed_mph) * 60`

    Equation Relationship:
        This function generates the supervised-learning target `Y`; it does not
        generate the ANN prediction `Y_hat`. The congestion flag selects either
        `50 mph` or `25 mph` for the highway term.
    """
    # Select the highway-speed term used by the synthetic Y equation.
    highway_speed_mph = (
        CONGESTED_HIGHWAY_SPEED_MPH
        if x3_congestion_flag == 1
        else NORMAL_HIGHWAY_SPEED_MPH
    )

    # Calculate the highway and local-road terms of Y.
    y_highway_travel_minutes_term = (
        x1_highway_miles / highway_speed_mph
    ) * 60.0
    y_local_road_travel_minutes_term = (
        x2_local_road_miles / LOCAL_ROAD_SPEED_MPH
    ) * 60.0

    # Y is the correct synthetic target, not the model estimate Y_hat.
    y_target_minutes = (
        PREPARATION_MINUTES
        + y_highway_travel_minutes_term
        + y_local_road_travel_minutes_term
    )
    return y_target_minutes
# ---

# ________________________________________________
#   Build training data from synthetic examples
#=================================================

# --- build_training_data()
def build_training_data() -> tuple[np.ndarray, np.ndarray]:
    """Build the raw feature matrix `X` and correct-target matrix `Y`.

    Returns:
        A tuple containing:
            - `x_input_matrix`: `X` with dimensions `(352, 3)`.
            - `y_target_matrix`: `Y` with dimensions `(352, 1)`.

    Related Equations:
        `X[i] = [x1_highway_miles, x2_local_road_miles, x3_congestion_flag]`
        `Y[i] = calculate_synthetic_target_minutes(X[i])`

    Equation Relationship:
        This data-construction function creates the paired supervised-learning
        matrices `X` and `Y`. It does not create a validation set; every generated
        pair is used by the full-batch training loop.
    """
    x_input_rows: list[list[float]] = []
    y_target_rows: list[list[float]] = []

    # Create every documented combination of distance and congestion state.
    for x1_highway_miles in range(
        TRAINING_HIGHWAY_MIN_MILES,      # 0 highway miles.
        TRAINING_HIGHWAY_MAX_MILES + 1,  # Include 30 highway miles.
        TRAINING_HIGHWAY_STEP_MILES,     # Increase by 2 highway miles.
    ):
        for x2_local_road_miles in range(
            TRAINING_LOCAL_MIN_MILES,      # 0 local-road miles.
            TRAINING_LOCAL_MAX_MILES + 1,  # Include 10 local-road miles.
        ):
            for x3_congestion_flag in (0, 1):
                # Append one row X[i] = [x1, x2, x3].
                x_input_rows.append(
                    [
                        float(x1_highway_miles),
                        float(x2_local_road_miles),
                        float(x3_congestion_flag),
                    ],
                )

                # Append the paired correct target Y[i].
                y_target_rows.append(
                    [
                        calculate_synthetic_target_minutes(
                            float(x1_highway_miles),
                            float(x2_local_road_miles),
                            x3_congestion_flag,
                        ),
                    ],
                )

    # Convert the row lists into equation matrices X and Y.
    x_input_matrix = np.asarray(x_input_rows, dtype=np.float64)
    y_target_matrix = np.asarray(y_target_rows, dtype=np.float64)

    # A changed loop range must not silently alter the documented dataset.
    if x_input_matrix.shape != (TRAINING_EXAMPLE_COUNT, INPUT_SIZE):
        raise RuntimeError("training input matrix X has unexpected dimensions")
    if y_target_matrix.shape != (TRAINING_EXAMPLE_COUNT, OUTPUT_SIZE):
        raise RuntimeError("training target matrix Y has unexpected dimensions")

    return x_input_matrix, y_target_matrix
# ---

# __________________________________________
# STANDARDIZATION
# ==========================================

# PRE-TRAINING PREPARATION
# Standardization places X and Y on the scales used by the training loop. It occurs
# before the four learning phases and does not update the ANN parameters.
#
# Standardization uses x_standardized = (x - mean) / standard_deviation. The same
# training statistics must be reused for user input. Destandardization reverses
# the target transformation so predictions can be reported in minutes.

# --- calculate_standardization_statistics()
def calculate_standardization_statistics(
    x_inputs: np.ndarray,
    y_targets: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Calculate training-set means and standard deviations for `X` and `Y`.

    Args:
        x_inputs: Raw input matrix `X` with shape `(m, 3)`.
        y_targets: Raw correct-target matrix `Y` with shape `(m, 1)`.

    Returns:
        `mu_x_input_mean`, `sigma_x_input_std`, `mu_y_target_mean`, and
        `sigma_y_target_std`.

    Related Equations:
        `mu_X = mean(X, axis=0)`
        `sigma_X = std(X, axis=0)`
        `mu_Y = mean(Y, axis=0)`
        `sigma_Y = std(Y, axis=0)`

    Equation Relationship:
        The returned `mu` and `sigma` values parameterize the standardization and
        destandardization equations. They are calculated from the training data and
        then reused for training inputs, user inputs, targets, and predictions.
    """
    x_input_matrix = np.asarray(x_inputs, dtype=np.float64)
    y_target_matrix = np.asarray(y_targets, dtype=np.float64)

    mu_x_input_mean = np.mean(x_input_matrix, axis=0, keepdims=True)
    sigma_x_input_std = np.std(x_input_matrix, axis=0, keepdims=True)
    mu_y_target_mean = np.mean(y_target_matrix, axis=0, keepdims=True)
    sigma_y_target_std = np.std(y_target_matrix, axis=0, keepdims=True)

    # A zero sigma value would make standardization division invalid.
    if np.any(sigma_x_input_std == 0.0) or np.any(sigma_y_target_std == 0.0):
        raise ValueError("standard deviations used for standardization must be nonzero")

    return (
        mu_x_input_mean,
        sigma_x_input_std,
        mu_y_target_mean,
        sigma_y_target_std,
    )
# ---

# --- standardize_inputs()
def standardize_inputs(
    x_inputs: np.ndarray,
    mu_x_input_mean: np.ndarray,
    sigma_x_input_std: np.ndarray,
) -> np.ndarray:
    """Standardize input matrix `X` with training-set statistics.

    Args:
        x_inputs: Raw input matrix `X` with shape `(m, 3)`.
        mu_x_input_mean: Training-set feature mean `mu_X`, shape `(1, 3)`.
        sigma_x_input_std: Training-set feature standard deviation `sigma_X`,
            shape `(1, 3)`.

    Returns:
        `x_standardized_inputs`, the standardized matrix `X_standardized` with
        shape `(m, 3)`.

    Related Equation:
        `X_standardized = (X - mu_X) / sigma_X`

    Equation Relationship:
        This function evaluates the input-standardization equation. The same
        training-set `mu_X` and `sigma_X` must be used for both training rows and
        later user-input rows.
    """
    x_input_matrix = np.asarray(x_inputs, dtype=np.float64)
    x_standardized_inputs = (
        x_input_matrix - mu_x_input_mean
    ) / sigma_x_input_std
    return x_standardized_inputs
# ---


# --- standardize_targets()
def standardize_targets(
    y_targets: np.ndarray,
    mu_y_target_mean: np.ndarray,
    sigma_y_target_std: np.ndarray,
) -> np.ndarray:
    """Standardize correct-target matrix `Y` with training-set statistics.

    Args:
        y_targets: Raw correct-target matrix `Y` with shape `(m, 1)`.
        mu_y_target_mean: Training-set target mean `mu_Y`, shape `(1, 1)`.
        sigma_y_target_std: Training-set target standard deviation `sigma_Y`,
            shape `(1, 1)`.

    Returns:
        `y_standardized_targets`, the matrix `Y_standardized` with shape
        `(m, 1)`.

    Related Equation:
        `Y_standardized = (Y - mu_Y) / sigma_Y`

    Equation Relationship:
        This function places the correct targets `Y` on the scale learned by the
        ANN. Predictions `Y_hat` produced during training use this same scale.
    """
    y_target_matrix = np.asarray(y_targets, dtype=np.float64)
    y_standardized_targets = (
        y_target_matrix - mu_y_target_mean
    ) / sigma_y_target_std
    return y_standardized_targets
# ---

# --- destandardize_targets()
def destandardize_targets(
    y_standardized_values: np.ndarray,
    mu_y_target_mean: np.ndarray,
    sigma_y_target_std: np.ndarray,
) -> np.ndarray:
    """Convert standardized `Y` or `Y_hat` values back to delivery minutes.

    Args:
        y_standardized_values: Standardized target or prediction matrix with
            shape `(m, 1)`.
        mu_y_target_mean: Training-set target mean `mu_Y`, shape `(1, 1)`.
        sigma_y_target_std: Training-set target standard deviation `sigma_Y`,
            shape `(1, 1)`.

    Returns:
        `y_destandardized_values`, a matrix on the original minute scale.

    Related Equation:
        `Y_original = Y_standardized * sigma_Y + mu_Y`

    Equation Relationship:
        This function reverses target standardization. During inference, the input
        values are standardized predictions `Y_hat_standardized`, so the returned
        values are `Y_hat` expressed in delivery minutes.
    """
    y_standardized_matrix = np.asarray(
        y_standardized_values,
        dtype=np.float64,
    )
    y_destandardized_values = (
        y_standardized_matrix * sigma_y_target_std + mu_y_target_mean
    )
    return y_destandardized_values
# ---

# ____________________________________________________________________________________
# ====================================================================================
# USER INPUT
# ====================================================================================

#____________________________________________________
#   Validating user inputs
#====================================================

# --- prompt_for_distance()
def prompt_for_distance(prompt_text: str, maximum: float) -> float:
    """Prompt until the user enters a finite distance in the accepted range.

    Args:
        prompt_text: Text displayed to the user.
        maximum: Inclusive maximum supported by the training data.

    Returns:
        Validated distance as a float.
    """
    # Validation loop: continue until numeric conversion and range validation succeed.
    while True:
        try:
            raw_value = input(prompt_text)
        except EOFError as exc:
            raise SystemExit("\nNo input was received. The program will stop.") from exc

        try:
            distance = float(raw_value.strip())
        except ValueError:
            print(
                style_text(
                    "  That entry is not a number. Try something like 10 or 2.5.",
                    ANSI_RED,
                    bold=True,
                ),
            )
            continue  # Re-prompt

        # Validation: restrict input to the range represented by the training examples.
        if not np.isfinite(distance) or not 0.0 <= distance <= maximum:
            print(
                style_text(
                    f"  That value is outside the training range. "
                    f"Enter a number from 0 through {maximum:g}.",
                    ANSI_RED,
                    bold=True,
                ),
            )
            continue  # Re-prompt

        return distance
# ---

# --- prompt_for_congestion_flag()
def prompt_for_congestion_flag() -> int:
    """Prompt until the user enters `0` for normal or `1` for congested traffic."""
    # VALIDATION LOOP: Only the two binary feature values used during training are accepted.
    while True:
        prompt_text = style_text(
            "  Enter x3, traffic condition (0 = normal, 1 = congested): ",
            ANSI_CYAN,
            bold=True,
        )
        try:
            raw_value = input(prompt_text).strip()
        except EOFError as exc:
            raise SystemExit("\nNo input was received. The program will stop.") from exc

        if raw_value in {"0", "1"}:
            return int(raw_value)

        print(
            style_text(
                "  For x3, enter 0 for normal traffic or 1 for congested traffic.",
                ANSI_RED,
                bold=True,
            ),
        )
# ---

#____________________________________________________
#   Collecting the user's input values
#====================================================

# --- collect_user_feature_row()
def collect_user_feature_row() -> np.ndarray:
    """Collect `x1`, `x2`, and `x3`, then build one input matrix row `X`.

    Returns:
        `x_user_feature_matrix`, the raw feature matrix `X_user` with dimensions
        `(1, 3)`.

    Related Equation:
        `X_user = [[x1_highway_miles, x2_local_road_miles, x3_congestion_flag]]`

    Equation Relationship:
        This function constructs the same three-column input representation used
        by the training matrix `X`. The row is raw at this point; `main()` applies
        the `X_standardized` equation before inference.

    Logic:
        1. Explain the three values in one `X_user` row.
        2. Collect `x1`, highway miles.
        3. Collect `x2`, local-road miles.
        4. Collect `x3`, the binary congestion flag.
        5. Build one row of `X`.
    """
    print_subheading("Build one input row for the trained network", ANSI_CYAN)
    print_equation("X_user = [[x1, x2, x3]]")
    print("  x1 = highway miles")
    print("  x2 = local-road miles")
    print("  x3 = traffic flag: 0 for normal, 1 for congested")
    print()

    # x1: highway miles.
    x1_highway_miles = prompt_for_distance(
        style_text(
            f"  Enter x1, highway miles (0 to {TRAINING_HIGHWAY_MAX_MILES}): ",
            ANSI_CYAN,
            bold=True,
        ),
        float(TRAINING_HIGHWAY_MAX_MILES),
    )

    # x2: local-road miles.
    x2_local_road_miles = prompt_for_distance(
        style_text(
            f"  Enter x2, local-road miles (0 to {TRAINING_LOCAL_MAX_MILES}): ",
            ANSI_CYAN,
            bold=True,
        ),
        float(TRAINING_LOCAL_MAX_MILES),
    )

    # x3: binary congestion flag.
    x3_congestion_flag = prompt_for_congestion_flag()

    # X_user = [[x1, x2, x3]].
    x_user_feature_matrix = np.asarray(
        [[
            x1_highway_miles,
            x2_local_road_miles,
            float(x3_congestion_flag),
        ]],
        dtype=np.float64,
    )
    return x_user_feature_matrix
# ---

# __________________________________________
# DISPLAY HELPERS
# ==========================================

# --- terminal_supports_color()
def terminal_supports_color() -> bool:
    """Return whether ANSI colors should be used for the current console."""
    if not USE_CONSOLE_COLORS or os.getenv("NO_COLOR") is not None:
        return False

    # FORCE_COLOR allows color in terminals whose capability cannot be detected.
    if os.getenv("FORCE_COLOR") is not None:
        return True

    is_interactive_output = bool(
        getattr(sys.stdout, "isatty", lambda: False)(),
    )
    return is_interactive_output and os.getenv("TERM", "").lower() != "dumb"
# ---

#____________________________________________________
#   Display formatting helpers
#====================================================

# --- style_text()
def style_text(
    text: str,
    color: str = "",
    *,
    bold: bool = False,
    dim: bool = False,
) -> str:
    """Return text wrapped in ANSI formatting when the terminal supports color.

    Args:
        text: Text to format.
        color: ANSI foreground-color code.
        bold: Whether to add bold formatting.
        dim: Whether to add dim formatting.

    Returns:
        Formatted text for an interactive color terminal, otherwise plain text.
    """
    if not terminal_supports_color():
        return text

    formatting_codes = "".join(
        code
        for code in (ANSI_BOLD if bold else "", ANSI_DIM if dim else "", color)
        if code
    )
    return f"{formatting_codes}{text}{ANSI_RESET}"
# ---

#____________________________________________________
#   Displaying headings and titles
#====================================================

# --- print_heading()
def print_heading(title: str, color: str = ANSI_CYAN) -> None:
    """Print one spaced and color-coded console heading.

    Args:
        title: Title string.
        color: ANSI color used for the border and title.

    Returns:
        None
    """
    border = "=" * DISPLAY_WIDTH
    centered_title = title.center(DISPLAY_WIDTH)

    print()
    print(style_text(border, color, bold=True))
    print(style_text(centered_title, color, bold=True))
    print(style_text(border, color, bold=True))
    print()
# ---

# --- print_subheading()
def print_subheading(title: str, color: str = ANSI_DEFAULT) -> None:
    """Print a compact console subheading followed by an underline."""
    print(style_text(title, color, bold=True))
    print(style_text("-" * min(len(title), DISPLAY_WIDTH), color))
# ---

#____________________________________________________
#   Printing paragraphs
#====================================================

# --- print_paragraph()
def print_paragraph(text: str, *, indent: int = 0) -> None:
    """Formatted paragraph printing"""
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

# --- print_styled_paragraph()
def print_styled_paragraph(
    text: str,
    color: str,
    *,
    bold: bool = False,
    indent: int = 0,
) -> None:
    """Wrap a paragraph first, then apply one ANSI style to the wrapped text."""
    indentation = " " * indent
    wrapped_text = textwrap.fill(
        text,
        width=DISPLAY_WIDTH,
        initial_indent=indentation,
        subsequent_indent=indentation,
    )
    print(style_text(wrapped_text, color, bold=bold))
# ---

# --- print_equation()
def print_equation(
    equation: str,
    *,
    indent: int = 4,
    color: str = ANSI_MAGENTA,
) -> None:
    """Print one equation so it is visually distinct from explanatory prose."""
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
    """Print a label and emphasized value with consistent spacing."""
    label_width = 36
    plain_label = f"{' ' * indent}{label:<{label_width}}"
    print(plain_label + style_text(value, value_color, bold=True))
# ---

#____________________________________________________
#   Pausing between sections
#====================================================

# --- pause_for_user()
def pause_for_user(next_action: str) -> None:
    """Pause an interactive run so one section can be read before the next begins.

    A redirected or automated run does not pause because standard input is not a
    terminal in that situation.
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

#____________________________________________________
#   Displaying the training phases
#====================================================

# --- print_training_phase()
def print_training_phase(
    phase_number: int,
    title: str,
    question: str,
    equations: tuple[str, ...],
    result: str,
    color: str,
) -> None:
    """Display one learning phase with its question, equations, and result."""
    phase_title = f"PHASE {phase_number}: {title.upper()}"
    print(style_text(phase_title, color, bold=True))
    print_paragraph(f"Question: {question}", indent=2)
    print("  Equation path:")
    for equation in equations:
        print_equation(equation, indent=4)
    print_paragraph(f"Result: {result}", indent=2)
    print()
# ---

#____________________________________________________
#   Displaying the learning cycle
#====================================================

# --- print_learning_cycle()
def print_learning_cycle() -> None:
    """Display the four phases repeated by every training round."""
    print_subheading("The learning cycle repeated in every training round")
    print_paragraph(
        "One round is one complete trip through all four phases. The model repeats "
        "this cycle with the same training matrices, but with newly updated weights "
        "and biases after each trip.",
    )
    print()
    print_equation(
        "Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> repeat",
        indent=2,
        color=ANSI_DEFAULT,
    )
    print()

    # ---- phase 1
    print_training_phase(
        1,
        "Feedforward propagation",
        "What prediction does the network produce with its current weights and biases?",
        (
            "Z1 = X @ W1 + b1",
            "A1 = ReLU(Z1)",
            "Y_hat = A1 @ W2 + b2",
        ),
        "The prediction matrix Y_hat.",
        ANSI_CYAN,
    )

    # ---- phase 2
    print_training_phase(
        2,
        "Loss-function evaluation",
        "How different is the prediction Y_hat from the correct target Y?",
        (
            "error = Y_hat - Y",
            "J = mean((Y_hat - Y) ** 2)",
        ),
        "One scalar loss value J. Smaller is better.",
        ANSI_YELLOW,
    )

    # ---- phase 3
    print_training_phase(
        3,
        "Backpropagation",
        "Which weights and biases affected J, and by how much?",
        (
            "dJ/dY_hat = (2 / error.size) * error",
            "dJ/dW2 = A1.T @ dJ/dY_hat",
            "dJ/db2 = sum(dJ/dY_hat)",
            "dJ/dA1 = dJ/dY_hat @ W2.T",
            "dJ/dZ1 = dJ/dA1 * ReLU'(Z1)",
            "dJ/dW1 = X.T @ dJ/dZ1",
            "dJ/db1 = sum(dJ/dZ1)",
        ),
        "The gradients dJ/dW1, dJ/db1, dJ/dW2, and dJ/db2.",
        ANSI_MAGENTA,
    )

    # ---- phase 4
    print_training_phase(
        4,
        "Optimization",
        "Given the gradients, how should the weights and biases change?",
        (
            "W_new = W_old - eta * dJ/dW",
            "b_new = b_old - eta * dJ/db",
        ),
        "Updated parameters for the next training round.",
        ANSI_BLUE,
    )

    # ---- distinction between backpropagation and optimization
    print_styled_paragraph(
        "Important distinction: backpropagation calculates gradients; "
        "optimization uses those gradients.",
        ANSI_YELLOW,
        bold=True,
    )
# ---

# __________________________________________
# DISPLAY TRAINING METRICS
# ==========================================

# --- print_training_progress()
def print_training_progress(j_loss_history: list[tuple[int, float]]) -> None:
    """Display selected scalar loss values `J` before and during training.

    Args:
        j_loss_history: List of `(iteration, J)` tuples.

    Related Equation:
        `J = mean((Y_hat - Y) ** 2)`

    Equation Relationship:
        This display helper receives previously calculated values of `J`; it does
        not evaluate the loss equation itself.

    Returns:
        None
    """

    # --- Input validation
    if not j_loss_history:
        raise ValueError("j_loss_history must contain at least one checkpoint")

    # --- Initialization
    j_initial_mse_loss = j_loss_history[0][1]
    final_iteration = j_loss_history[-1][0]

    # ---- print subheading
    print_subheading("Loss checkpoints", ANSI_GREEN)

    # ---- print description
    print_paragraph(
        "J is the mean squared error over the standardized training targets. "
        "It is one score for the whole training set: a smaller J means the model's "
        "predictions are closer to Y, while J = 0 would be a perfect match.",
    )
    print_equation("J = mean((Y_hat - Y) ** 2)")
    print()

    # ---- print header
    header = (
        f"{'Checkpoint':<27}"
        f"{'Loss J':>20}"
        f"{'Change from start':>24}"
    )
    print(style_text(header, ANSI_DEFAULT, bold=True))
    print(style_text("-" * len(header), ANSI_DEFAULT, dim=True))

    # Convert each stored J checkpoint into a readable row.
    for iteration, j_mse_loss in j_loss_history:

        # ---- label
        label = "Before training" if iteration == 0 else f"After round {iteration:,}"

        # ---- change from start
        if iteration == 0 or j_initial_mse_loss == 0.0:
            change_from_start = "starting point"
        else:
            j_reduction_percent = (
                1.0 - j_mse_loss / j_initial_mse_loss
            ) * 100.0
            change_from_start = f"{j_reduction_percent:.6f}% lower"

        # ---- row
        row = (
            f"{label:<27}"
            f"{j_mse_loss:>20.10f}"
            f"{change_from_start:>24}"
        )
        # ---- print row
        if iteration == final_iteration and iteration != 0:
            print(style_text(row, ANSI_GREEN, bold=True))
        elif iteration == 0:
            print(style_text(row, ANSI_YELLOW))
        else:
            print(row)
# ---

# ____________________________________________________
# Displaying the final prediction
# ====================================================

# --- print_prediction_box()
def print_prediction_box(y_hat_predicted_minutes: float) -> None:
    """Display the ANN prediction in a high-contrast console box."""
    inside_width = DISPLAY_WIDTH - 2
    border = "+" + "=" * inside_width + "+"
    blank_line = "|" + " " * inside_width + "|"
    title_line = "|" + "TRAINED ANN PREDICTION".center(inside_width) + "|"
    prediction_text = f"Y_hat (ŷ) = {y_hat_predicted_minutes:.4f} minutes"
    prediction_line = "|" + prediction_text.center(inside_width) + "|"

    print(style_text(border, ANSI_YELLOW, bold=True))
    print(style_text(title_line, ANSI_YELLOW, bold=True))
    print(style_text(blank_line, ANSI_YELLOW))
    print(style_text(prediction_line, ANSI_YELLOW, bold=True))
    print(style_text(border, ANSI_YELLOW, bold=True))
# ---

# ____________________________________________________________________________________
# ====================================================================================
# MAIN FUNCTION - ENTRY POINT
# ====================================================================================

# --- main()
def main() -> None:
    """Train the ANN, collect one `X` row, and display one prediction `Y_hat`.

    Related Equation Pipeline:
        `X, Y = build_training_data()`
        `X_standardized = (X - mu_X) / sigma_X`
        `Y_standardized = (Y - mu_Y) / sigma_Y`
        `Y_hat_standardized = F_theta(X_standardized)`
        `Y_hat_minutes = Y_hat_standardized * sigma_Y + mu_Y`

    Equation Relationship:
        This entry point connects data construction, standardization, the four
        training phases, and inference. Variables that represent mathematical
        values begin with their corresponding symbols, including `x_`, `y_`,
        `y_hat_`, `j_`, `mu_`, and `sigma_`.

    Logic:
        1. Build and standardize the synthetic matrices `X` and `Y`.
        2. Explain the `3 -> 6 -> 1` architecture and all four training phases.
        3. Train the ANN for 5,000 rounds and display readable loss checkpoints.
        4. Collect the three values for one user input row `X_user`.
        5. Calculate `Y_hat`, emphasize the prediction, and compare it with `Y`.
    """

    # __________________________________________
    # DISPLAY MAIN HEADING
    # ==========================================

    print_heading("HAND-MADE SHALLOW ARTIFICIAL NEURAL NETWORK", ANSI_CYAN)
    print_paragraph(
        "This classroom program trains a small NumPy artificial neural network "
        "to estimate a fictional delivery duration. The point is not to model "
        "real traffic. The point is to make the learning process visible, one "
        "phase at a time.",
    )
    print()
    print_paragraph(
        "The walkthrough is divided into readable sections. During an interactive "
        "run, the program pauses between sections so the equations and results do "
        "not arrive as one large wall of text.",
    )
    pause_for_user("prepare the training data")

    # __________________________________________
    # BUILD AND STANDARDIZE THE TRAINING DATA
    # ==========================================

    print_heading("1. PREPARE THE TRAINING MATRICES X AND Y", ANSI_BLUE)

    # Build raw equation matrices X and Y.
    x_training_inputs, y_training_targets = build_training_data()

    # Calculate mu_X, sigma_X, mu_Y, and sigma_Y from training data only.
    (
        mu_x_input_mean,
        sigma_x_input_std,
        mu_y_target_mean,
        sigma_y_target_std,
    ) = calculate_standardization_statistics(
        x_training_inputs,
        y_training_targets,
    )

    # Calculate X_standardized and Y_standardized.
    x_standardized_training_inputs = standardize_inputs(
        x_training_inputs,
        mu_x_input_mean,
        sigma_x_input_std,
    )
    y_standardized_training_targets = standardize_targets(
        y_training_targets,
        mu_y_target_mean,
        sigma_y_target_std,
    )

    # __________________________________________
    # EXPLAIN THE TRAINING DATA
    # ==========================================


    # Explain where the examples come from
    print_subheading("Where the examples come from", ANSI_BLUE)
    print_paragraph(
        "Before the network can learn, it needs paired examples. Each row of X "
        "describes one fictional route, and the matching row of Y contains the "
        "classroom target duration for that route.",
    )

    # Example of the matrix X equation
    print_equation(
        "X[i] = [x1_highway_miles, x2_local_road_miles, x3_congestion_flag]",
    )

    # Example of the matrix Y equation
    print_equation(
        "Y[i] = 10 + (x1 / highway_speed) * 60 + (x2 / 20) * 60",
    )

    # Explain the values of highway_speed and local_road_speed in the equation above.
    print("    highway_speed = 50 mph when x3 = 0; 25 mph when x3 = 1")
    print("    local_road_speed = 20 mph when x3 = 0; 10 mph when x3 = 1")
    print()

    # Explain what the matrix dimensions mean
    print_subheading("What the matrix dimensions mean", ANSI_BLUE)
    print_labeled_value(
        "X.shape =",
        str(x_training_inputs.shape),
        value_color=ANSI_CYAN,
    )
    # Explain what the shape of X means
    print("    352 route examples, with 3 input features in each row")
    # Example of the shape of Y
    print_labeled_value(
        "Y.shape =",
        str(y_training_targets.shape),
        value_color=ANSI_CYAN,
    )
    # Explain what the shape of Y means
    print("    352 matching targets, with 1 delivery duration in each row")
    print()

    # Explain why the values are standardized
    print_subheading("Why the values are standardized", ANSI_BLUE)
    print_paragraph(
        "The raw distances and target minutes use different numerical scales. "
        "Standardization puts them on comparable scales before training. The same "
        "training-set means and standard deviations are later reused for user input.",
    )
    # Example of the standardization equation
    print_equation("X_standardized = (X - mu_X) / sigma_X")
    print_equation("Y_standardized = (Y - mu_Y) / sigma_Y")

    pause_for_user("inspect the network and its learning cycle")

    # __________________________________________
    # CREATE AND EXPLAIN THE SHALLOW ANN
    # ==========================================

    print_heading("2. SET UP THE NETWORK AND ITS FOUR LEARNING PHASES", ANSI_CYAN)
    model = ShallowANN(
        INPUT_SIZE,
        HIDDEN_SIZE,
        OUTPUT_SIZE,
        seed=RANDOM_SEED,
    )

    # Explain the network architecture
    print_subheading("Network architecture", ANSI_CYAN)
    # Example of the network architecture equation
    print_equation(
        f"X (m, {INPUT_SIZE}) -> A1 (m, {HIDDEN_SIZE}) -> "
        f"Y_hat (m, {OUTPUT_SIZE})",
        color=ANSI_CYAN,
    )
    # Example of the layer layout
    print_labeled_value(
        "Layer layout:",
        f"{INPUT_SIZE} inputs -> {HIDDEN_SIZE} hidden neurons -> "
        f"{OUTPUT_SIZE} output",
        value_color=ANSI_CYAN,
    )
    # Example of the weight and bias shapes
    print_labeled_value(
        "W1 and b1 shapes:",
        f"{model.W1.shape} and {model.b1.shape}",
        value_color=ANSI_CYAN,
    )
    # Explain what the weight and bias shapes mean
    print("    W1 connects the 3 inputs to all 6 hidden neurons")
    # Example of the weight and bias shapes for W2 and b2
    print_labeled_value(
        "W2 and b2 shapes:",
        f"{model.W2.shape} and {model.b2.shape}",
        value_color=ANSI_CYAN,
    )
    # Explain what the weight and bias shapes mean for W2 and b2
    print_labeled_value(
        "W2 and b2 shapes:",
        f"{model.W2.shape} and {model.b2.shape}",
        value_color=ANSI_CYAN,
    )
    print("    W2 connects the 6 hidden activations to the single output")
    # Example of the hidden activation
    print_labeled_value("Hidden activation:", "ReLU")
    # Example of the output activation
    print_labeled_value("Output activation:", "linear identity")
    # Example of the loss function
    print_labeled_value("Loss function:", "mean squared error J")
    # Example of the learning rate
    print_labeled_value(
        "Learning rate eta:",
        f"{ETA_LEARNING_RATE:g}",
        value_color=ANSI_YELLOW,
    )
    # Example of the training rounds
    print_labeled_value(
        "Training rounds:",
        f"{TRAINING_ITERATIONS:,}",
        value_color=ANSI_YELLOW,
    )
    print()

    pause_for_user("walk through the four phases of one training round")
    # __________________________________________
    # EXPLAIN THE LEARNING CYCLE
    # ==========================================
    print_subheading("The learning cycle", ANSI_CYAN)
    print_learning_cycle()

    pause_for_user(f"begin {TRAINING_ITERATIONS:,} training rounds")
    # __________________________________________
    # TRAIN THE MODEL
    # ==========================================

    # Store one W1 value before training.
    w1_example_weight_before = float(model.W1[0, 0])

    # model.train() now enters the repeating learning cycle:
    # Phase 1 -> Phase 2 -> Phase 3 -> Phase 4.
    print()
    print(
        style_text(
            f"Training the network for {TRAINING_ITERATIONS:,} rounds...",
            ANSI_CYAN,
            bold=True,
        ),
        end="",
        flush=True,
    )
    # Example of the loss history
    j_loss_history = model.train(
        x_standardized_training_inputs,
        y_standardized_training_targets,
        iterations=TRAINING_ITERATIONS,
        eta_learning_rate=ETA_LEARNING_RATE,
    )
    print(style_text(" complete.", ANSI_GREEN, bold=True))

    # Store the same W1 value after training.
    w1_example_weight_after = float(model.W1[0, 0])

    # __________________________________________
    # GET INITIAL AND FINAL LOSS J
    # ==========================================

    j_initial_mse_loss = j_loss_history[0][1]
    j_final_mse_loss = j_loss_history[-1][1]

    # __________________________________________
    # CHECKS AFTER TRAINING
    # ==========================================

    if j_final_mse_loss >= j_initial_mse_loss:
        raise RuntimeError("training did not reduce the loss J")
    if model.updates_completed != TRAINING_ITERATIONS:
        raise RuntimeError("the model did not complete every requested update")

    # __________________________________________
    # CALCULATIONS
    # ==========================================

    j_loss_reduction_percent = (
        1.0 - j_final_mse_loss / j_initial_mse_loss
    ) * 100.0

    # __________________________________________
    # DISPLAY TRAINING RESULTS
    # ==========================================

    print_heading("3. REVIEW WHAT CHANGED DURING TRAINING", ANSI_GREEN)
    print_training_progress(j_loss_history)
    print()

    print_subheading("Training summary", ANSI_GREEN)
    # Initial loss J to 10 decimal places
    print_labeled_value(
        "Initial loss J:",
        f"{j_initial_mse_loss:.10f}",
        value_color=ANSI_YELLOW,
    )
    # Final loss J to 10 decimal places
    print_labeled_value(
        "Final loss J:",
        f"{j_final_mse_loss:.10f}",
        value_color=ANSI_GREEN,
    )
    # Reduction in J to 6 decimal places
    print_labeled_value(
        "Reduction in J:",
        f"{j_loss_reduction_percent:.6f}%",
        value_color=ANSI_GREEN,
    )
    # Parameter updates completed to 3 decimal places
    print_labeled_value(
        "Parameter updates completed:",
        f"{model.updates_completed:,}",
        value_color=ANSI_GREEN,
    )
    print()
    print_paragraph(
        "The reduction percentage shows how much the MSE changed over the training "
        "process"
    )
    print()

    print_subheading("One visible weight update", ANSI_GREEN)
    print_equation("W1_new = W1_old - eta * dJ/dW1")
    print_labeled_value(
        "W1[0, 0] before training:",
        f"{w1_example_weight_before:.6f}",
        value_color=ANSI_YELLOW,
    )
    print_labeled_value(
        "W1[0, 0] after training:",
        f"{w1_example_weight_after:.6f}",
        value_color=ANSI_GREEN,
    )

    # __________________________________________
    # USER INPUT FEATURES
    # ==========================================

    pause_for_user("Next test the model inference using user inputs")

    print_heading("4. TEST THE TRAINED NETWORK", ANSI_CYAN)
    print_paragraph(
        "Training is finished. From this point forward, the network performs "
        "inference: it uses feedforward propagation to make a prediction, but it "
        "does not calculate a training loss, run backpropagation, or update weights.",
    )
    print_equation("Y_hat = F_theta(X_user_standardized)")
    print()

    # Collect one raw user equation row X_user.
    x_user_feature_matrix = collect_user_feature_row()

    # __________________________________________
    # PREDICTION USING THE TRAINED MODEL
    # ==========================================

    # INFERENCE: The trained model uses Phase 1 feedforward propagation only.
    # No loss evaluation, backpropagation, or optimization occurs here.

    # X_user_standardized = (X_user - mu_X) / sigma_X.
    x_standardized_user_features = standardize_inputs(
        x_user_feature_matrix,
        mu_x_input_mean,
        sigma_x_input_std,
    )

    # Calculate standardized prediction Y_hat.
    y_hat_standardized_prediction = model.predict(
        x_standardized_user_features,
    )

    # Convert Y_hat from the standardized scale to delivery minutes.
    y_hat_predicted_minutes = float(
        destandardize_targets(
            y_hat_standardized_prediction,
            mu_y_target_mean,
            sigma_y_target_std,
        )[0, 0],
    )

    # Extract x1, x2, and x3 from X_user.
    x1_highway_miles = float(x_user_feature_matrix[0, 0])
    x2_local_road_miles = float(x_user_feature_matrix[0, 1])
    x3_congestion_flag = int(x_user_feature_matrix[0, 2])

    # Calculate the synthetic correct target Y for comparison only.
    y_reference_target_minutes = calculate_synthetic_target_minutes(
        x1_highway_miles,
        x2_local_road_miles,
        x3_congestion_flag,
    )

    # Calculate |Y_hat - Y| on the original minute scale.
    y_hat_absolute_prediction_error = abs(
        y_hat_predicted_minutes - y_reference_target_minutes,
    )
    y_hat_absolute_prediction_error_seconds = (
        y_hat_absolute_prediction_error * 60.0
    )

    # __________________________________________
    # PRINT ANN PREDICTION
    # ==========================================

    print_heading("5. READ THE ANN PREDICTION", ANSI_GREEN)
    # Explain the traffic description
    x3_traffic_description = (
        "congested traffic" if x3_congestion_flag == 1 else "normal traffic"
    )
    # Show the input values provided by the user
    # Highway miles, local road miles, and traffic condition
    print_subheading("Input supplied to the network", ANSI_CYAN)
    print_equation(
        "X_user = "
        f"[[{x1_highway_miles:g}, {x2_local_road_miles:g}, "
        f"{x3_congestion_flag}]]",
        color=ANSI_CYAN,
    )
    # Show the x1 highway miles input value
    print_labeled_value(
        "x1, highway miles:",
        f"{x1_highway_miles:g}",
        value_color=ANSI_CYAN,
    )
    # Show the x2 local road miles input value
    print_labeled_value(
        "x2, local-road miles:",
        f"{x2_local_road_miles:g}",
        value_color=ANSI_CYAN,
    )
    # Show the x3 traffic condition input value
    print_labeled_value(
        "x3, traffic condition:",
        f"{x3_congestion_flag} ({x3_traffic_description})",
        value_color=ANSI_CYAN,
    )
    print()

    # Show the predicted output value
    print_equation(
        "Y_hat_minutes = Y_hat_standardized * sigma_Y + mu_Y",
        indent=2,
    )
    # ------------------------------------------------------------ Show the predicted output value in a prediction box
    print_prediction_box(y_hat_predicted_minutes)
    print()
    # ------------------------------------------------------------ Show the reference target value
    print_subheading("Reference check", ANSI_GREEN)
    print_labeled_value(
        "Synthetic reference target Y:",
        f"{y_reference_target_minutes:.4f} minutes",
        value_color=ANSI_GREEN,
    )
    # ------------------------------------------------------------ Show the absolute prediction error in minutes
    print_labeled_value(
        "Absolute error |Y_hat - Y|:",
        f"{y_hat_absolute_prediction_error:.4f} minutes",
        value_color=ANSI_GREEN,
    )
    # ------------------------------------------------------------ Show the absolute prediction error in seconds
    print_labeled_value(
        "The same error in seconds:",
        f"{y_hat_absolute_prediction_error_seconds:.2f} seconds",
        value_color=ANSI_GREEN,
    )
    # The prediction and the reference target in a simple sentence
    print()
    print_paragraph(
        "Y_hat is the neural network's answer. The synthetic target Y is shown "
        "afterward only so we can check how closely the network learned the "
        "fictional classroom rule. Y was not substituted for the prediction.",
    )
    # Explain the trained network produced the highlighted prediction through feedforward propagation using its learned weights and biases
    print()
    print_styled_paragraph(
        "The trained network produced the highlighted prediction through "
        "feedforward propagation using its learned weights and biases.",
        ANSI_GREEN,
        bold=True,
    )
# ---

# __________________________________________
# MODULE INITIALIZATION
# ==========================================

if __name__ == "__main__":
    main()


# __________________________________________
# END OF FILE
# ==========================================
