# Critical Thinking Module 3

**Program:** Shallow Neural Network (2-layer) predicting store delivery duration in minutes to a customer's place

**Date:** 08/02/2026  
**Grade:**

---

**Course:** CSC510 - Foundations of Artificial Intelligence  
**Professor:** Dr. Isaac Gang  
**Term:** Fall A (26FA) - 2026  
**Student:** Alexander (Alex) Ricciardi

---

## Assignment:

Hand-Made Shallow ANN in Python
Using your research and resources, write a basic 2-layer Artificial Neural Network utilizing static backpropagation using Numpy in Python. Your neural network can perform a basic function, such as guessing the next number in a series. Using the activation function of your choice to calculate the predicted output ŷ, known as the feedforward function, and updating the weights and biases through gradient descent (backpropagation) based on your choice of a basic loss function.  

Your ANN should include the following features:  

- An input layer that takes input data as a matrix receives and passes it on
- A hidden layer
- An output layer
- Weights between the layers.

Also, your ANN should demonstrate it can perform the following functions:

- Multiply the input by a set of weights (via matrix multiplication)
- Apply deliberate activation function for every hidden layer
- Return an output
- Calculate error by taking the difference from the desired output and the predicted output giving us the gradient descent to provide our loss function
- Apply loss function to weights
- Repeat this process no less than 1,000 times to train the ANN

Your submission should be a script with the .py extension. It should be able to be activated easily and have the ability to accept simple inputs, such as a series of a particular number of variables or digits, in a manner that is clear to the user and predict and visually the final variable in the input set. The input and output are up to you. Keep it simple. 

---

## Program Requirements

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)

---

## Program Overview

`handmade_shallow_ann.py` is a small standalone Python script that implements a hand-made shallow artificial neural network using only NumPy.  
The program predicts a store delivery duration in minutes to a customer's place based on three user inputs:

- Highway miles
- Local-road miles
- A congestion flag, where `0` means normal traffic and `1` means congested traffic

The model uses a `3 -> 6 -> 1` neural network architecture:

- Three input values
- One hidden layer containing six ReLU neurons
- One linear output that predicts a continuous standardized target
- Two trainable weight matrices and two trainable bias arrays

The raw inputs and targets are standardized before the ANN receives them. 

### Synthetic Training Data

The script constructs a deterministic supervised-learning dataset from every combination in this
grid:

| Feature | Values used for training | Count |
| --- | --- | ---: |
| `x1`, highway miles | `0` through `30` in increments of `2` | 16 |
| `x2`, local-road miles | `0` through `10` in increments of `1` | 11 |
| `x3`, congestion flag | `0` for normal or `1` for congested | 2 |

This produces `16 * 11 * 2 = 352` paired examples: raw `X` has shape `(352, 3)` and
raw `Y` has shape `(352, 1)`. Each synthetic target is calculated independently of the ANN:

```text
highway_speed = 50 mph when x3 = 0; 25 mph when x3 = 1
Y_minutes = 10 + (x1 / highway_speed) * 60 + (x2 / 20) * 60
```

The `10` is the fictional preparation time, and `20 mph` is the assumed local-road speed. These
targets are classroom data, not real delivery-time estimates. The generated pairs are all used for
full-batch training; the script does not create a separate validation or test split.

### ANN Architecture

```mermaid
flowchart TB
    X["Input layer: standardized X<br/>shape: (m, 3)<br/>standardized columns: x₁ highway miles · x₂ local-road miles · x₃ congestion flag"]
    W1["Trainable W₁<br/>shape: (3, 6)"]
    B1["Trainable b₁<br/>shape: (1, 6)"]
    Z1["feedforward(): hidden affine transformation<br/>Z₁ = X @ W₁ + b₁<br/>shape: (m, 6)"]
    A1["Hidden layer: A₁ = ReLU(Z₁)<br/>shape: (m, 6)<br/>six neurons: h₁ · h₂ · h₃ · h₄ · h₅ · h₆"]
    W2["Trainable W₂<br/>shape: (6, 1)"]
    B2["Trainable b₂<br/>shape: (1, 1)"]
    YHAT["Output layer: linear identity<br/>Y_hat = A₁ @ W₂ + b₂<br/>standardized shape: (m, 1)"]

    X --> Z1
    W1 --> Z1
    B1 --> Z1
    Z1 --> A1
    A1 --> YHAT
    W2 --> YHAT
    B2 --> YHAT
```

The diagram shows only the ANN itself. Standardization occurs before its input layer, and conversion
back to minutes occurs after its output layer. In the matrix shapes, `m` is the number of examples
processed together in the current batch:

- `INPUT_SIZE = 3`: standardized input matrix `X` has shape `(m, 3)`.
- `HIDDEN_SIZE = 6`: hidden activation matrix `A1` has shape `(m, 6)`.
- `OUTPUT_SIZE = 1`: standardized prediction matrix `Y_hat` has shape `(m, 1)`.

For training, `m = 352`; for the single user prediction, `m = 1`. The hidden layer uses ReLU, and
the output layer uses the linear identity function. `W1` is initialized with He scaling, `W2` with
Xavier-style scaling, both biases with zeroes, and the random generator with seed `510` so the run is
repeatable.

The program trains for `5,000` full-batch rounds, exceeding the assignment minimum of `1,000`.
It uses learning rate `eta = 0.05`, displays the standardized MSE loss before and during training,
explains what each loss value means, and shows one example weight before and after optimization.

### End-to-End Data and Prediction Pipeline <br><br>

```mermaid
flowchart TB
    subgraph PREP["Training-data preparation"]
        direction LR
        XRAW["build_training_data(): raw X<br/>shape: (352, 3)"]
        YRAW["build_training_data(): synthetic Y in minutes<br/>shape: (352, 1)"]
        STATS["calculate_standardization_statistics()<br/>mu_X, sigma_X, mu_Y, sigma_Y"]
        XSTD["standardize_inputs(): X_standardized<br/>shape: (352, 3)"]
        YSTD["standardize_targets(): Y_standardized<br/>shape: (352, 1)"]

        XRAW --> STATS
        YRAW --> STATS
        XRAW --> XSTD
        STATS --> XSTD
        YRAW --> YSTD
        STATS --> YSTD
    end

    TRAIN["model.train(): 5,000 full-batch rounds<br/>feedforward → calculate_loss → backpropagate → apply_gradients<br/>eta = 0.05"]
    THETA["Trained parameters<br/>W1, b1, W2, b2"]

    XSTD --> TRAIN
    YSTD --> TRAIN
    TRAIN --> THETA

    subgraph INFERENCE["Single-row inference"]
        direction LR
        XUSER["Raw X_user<br/>shape: (1, 3)"]
        XUSERSTD["Reuse mu_X and sigma_X<br/>X_user_standardized"]
        FORWARD["model.predict()<br/>calls feedforward() only"]
        YHATSTD["Y_hat_standardized<br/>shape: (1, 1)"]
        MINUTES["destandardize_targets() with mu_Y and sigma_Y<br/>Y_hat in minutes"]

        XUSER --> XUSERSTD
        XUSERSTD --> FORWARD
        FORWARD --> YHATSTD
        YHATSTD --> MINUTES
    end

    THETA --> FORWARD
    STATS --> XUSERSTD
    STATS --> MINUTES

    REFERENCE["calculate_synthetic_target_minutes()<br/>independent reference Y for comparison only"]
    COMPARE["Report Y_hat, Y, and absolute error"]

    XUSER -->|same raw route| REFERENCE
    MINUTES -->|ANN estimate| COMPARE
    REFERENCE -->|reference only| COMPARE
```

---

## How the ANN Learns

Each training round keeps the four learning phases separate and visible:

1. **Feedforward propagation:** Calculates hidden activations and a prediction.
2. **Loss evaluation:** Names the prediction error as `Y_hat - Y` and calculates scalar loss `J`.
3. **Backpropagation:** Uses the chain rule to calculate `dJ/dW1`, `dJ/db1`, `dJ/dW2`,
   and `dJ/db2`.
4. **Gradient descent:** Applies those derivatives in a separate update method using learning
   rate `eta`.

### Forward Propagation Diagram <br><br>

Forward propagation moves from the input matrix toward the prediction. It uses the current
weights and biases but does not change them.

```mermaid
flowchart TD
    X["Standardized input matrix X<br/>shape: (m, 3)"]
    W1["Input-to-hidden weights W1<br/>shape: (3, 6)"]
    B1["Hidden bias b1<br/>shape: (1, 6)"]
    XW1["Matrix multiplication<br/>X @ W1<br/>shape: (m, 6)"]
    Z1["Hidden pre-activations Z1<br/>Z1 = X @ W1 + b1<br/>shape: (m, 6)"]
    RELU["relu(): hidden activation<br/>A1 = ReLU(Z1)"]
    A1["Hidden activations A1<br/>shape: (m, 6)"]
    W2["Hidden-to-output weights W2<br/>shape: (6, 1)"]
    B2["Output bias b2<br/>shape: (1, 1)"]
    A1W2["Matrix multiplication<br/>A1 @ W2<br/>shape: (m, 1)"]
    YHAT["feedforward() output: standardized Y_hat<br/>Y_hat = A1 @ W2 + b2<br/>shape: (m, 1)"]

    X --> XW1
    W1 --> XW1
    XW1 --> Z1
    B1 --> Z1
    Z1 --> RELU
    RELU --> A1
    A1 --> A1W2
    W2 --> A1W2
    A1W2 --> YHAT
    B2 --> YHAT
```

During training, both `X` and the comparison target `Y` are standardized and `m = 352`. During
inference, the same feedforward equations receive one standardized user row and `m = 1`.
Feedforward does not convert its result to minutes; `destandardize_targets()` performs that separate
step after `predict()` returns.

### Backpropagation Diagram <br><br>

Backpropagation begins after the prediction has been compared with the target. It moves backward
through the network and calculates the gradients for all four trainable parameter arrays.

```mermaid
flowchart TD
    YHAT["Standardized prediction Y_hat<br/>shape: (m, 1)"]
    Y["Standardized target Y<br/>shape: (m, 1)"]
    ERROR["Standardized prediction error<br/>error = Y_hat - Y<br/>shape: (m, 1)"]
    LOSS["calculate_loss(): standardized MSE<br/>J = mean(error ** 2)<br/>scalar"]
    DY["backpropagate(): output gradient<br/>dJ/dY_hat = (2 / error.size) * error<br/>shape: (m, 1)"]

    A1T["Cached A1.T<br/>shape: (6, m)"]
    DW2["Output-weight gradient<br/>dJ/dW2 = A1.T @ dJ/dY_hat<br/>shape: (6, 1)"]
    DB2["Output-bias gradient<br/>dJ/db2 = sum(dJ/dY_hat, axis=0)<br/>shape: (1, 1)"]

    W2T["Current W2.T<br/>shape: (1, 6)"]
    DA1["Hidden-activation gradient<br/>dJ/dA1 = dJ/dY_hat @ W2.T<br/>shape: (m, 6)"]
    RELUD["relu_derivative() on cached Z1<br/>ReLU'(Z1)<br/>shape: (m, 6)"]
    DZ1["Hidden pre-activation gradient<br/>dJ/dZ1 = dJ/dA1 * ReLU'(Z1)<br/>shape: (m, 6)"]

    XT["Training X.T<br/>shape: (3, m)"]
    DW1["Input-weight gradient<br/>dJ/dW1 = X.T @ dJ/dZ1<br/>shape: (3, 6)"]
    DB1["Hidden-bias gradient<br/>dJ/db1 = sum(dJ/dZ1, axis=0)<br/>shape: (1, 6)"]
    GRADIENTS["backpropagate() result<br/>dJ/dW1, dJ/db1, dJ/dW2, and dJ/db2"]
    UPDATE["Separate Phase 4: apply_gradients()<br/>theta_new = theta_old - eta * gradient(J)"]

    YHAT --> ERROR
    Y --> ERROR
    ERROR --> LOSS
    ERROR --> DY

    DY --> DW2
    A1T --> DW2
    DY --> DB2

    DY --> DA1
    W2T --> DA1
    DA1 --> DZ1
    RELUD --> DZ1

    DZ1 --> DW1
    XT --> DW1
    DZ1 --> DB1

    DW2 --> GRADIENTS
    DB2 --> GRADIENTS
    DW1 --> GRADIENTS
    DB1 --> GRADIENTS
    GRADIENTS -. "passed to optimizer" .-> UPDATE
```

The loss and output derivative both use the same cached `error = Y_hat - Y` matrix. This mirrors the
implementation: `calculate_loss()` evaluates `J`, while `backpropagate()` separately receives the
error and calculates gradients. The resulting gradient dictionary is then passed to
`apply_gradients()`; backpropagation itself does not update parameters.

The central data, training, and inference equations implemented by the script are:

```text
Y_minutes = 10 + (x1 / highway_speed) * 60 + (x2 / 20) * 60
X_standardized = (X - mu_X) / sigma_X
Y_standardized = (Y - mu_Y) / sigma_Y
Z1 = X @ W1 + b1
A1 = ReLU(Z1)
Y_hat = A1 @ W2 + b2
error = Y_hat - Y
J = mean(error ** 2)
theta_new = theta_old - eta * gradient(J)
Y_hat_minutes = Y_hat_standardized * sigma_Y + mu_Y
```

### Equation-to-Code Naming Convention

Equation-related variables begin with the mathematical symbol they represent and then add a
plain-language description. This makes each line of NumPy code traceable to the equation above it:

- `X` becomes `x_input_matrix` or another `x_...` variable.
- `Z1` becomes `z1_hidden_pre_activations`.
- `A1` becomes `a1_hidden_activations`.
- `Y_hat` becomes `y_hat_predictions`.
- `Y` becomes `y_target_matrix`.
- `Y_hat - Y` becomes `y_hat_minus_y_error`.
- `J` becomes `j_mse_loss` or another `j_...` variable.
- `eta` becomes `eta_learning_rate`.
- `mu` and `sigma` become `mu_..._mean` and `sigma_..._std`.
- A derivative such as `dJ/dW1` becomes `d_j_d_w1_weight_gradient`.

For example, the feedforward equations now appear directly in the variable names:

```python
# Step 1: X @ W1 + b1 -> Z1
z1_hidden_pre_activations = x_input_matrix @ self.W1 + self.b1

# Step 2: ReLU(Z1) -> A1
a1_hidden_activations = self.relu(z1_hidden_pre_activations)

# Step 3: A1 @ W2 + b2 -> Y_hat
y_hat_predictions = a1_hidden_activations @ self.W2 + self.b2
```

Backpropagation follows the same convention. For example,
`d_j_d_y_hat_output_gradient` stores `dJ/dY_hat`, while
`d_j_d_w1_weight_gradient` stores `dJ/dW1`. Gradient dictionary keys also mirror the equations:
`dJ_dW1`, `dJ_db1`, `dJ_dW2`, and `dJ_db2`.

Every equation-related function or method now includes two explicit docstring sections:

- **Related Equation** or **Related Equations:** Lists the mathematics implemented or used.
- **Equation Relationship:** Explains whether the software unit evaluates a mathematical function,
  coordinates a process, calculates gradients, performs optimization, constructs `X` and `Y`, or
  only displays a previously calculated value.

This distinction matters because feedforward propagation is a process, ReLU and MSE are
mathematical functions, backpropagation is a gradient-calculation algorithm, and gradient descent
is the separate optimization step that updates parameters.

The Python file retains the established project comment format, including the standardized file
header, section banners, class and function wrappers, proportional docstrings, intent labels, and
step comments for the main training loop.

---

## How to Run the Script

Run the following commands from the repository root.

1. Install NumPy into the project virtual environment:

   ```bash
   .venv/bin/python -m pip install -r CTA_Module-3/requirements.txt
   ```

2. Start the ANN script:

   ```bash
   .venv/bin/python CTA_Module-3/handmade_shallow_ann.py
   ```

3. Read each section and press `Enter` when the console asks to continue. After training, enter
   the three requested values. For example:

   ```text
   Enter x1, highway miles (0 to 30): 10
   Enter x2, local-road miles (0 to 10): 2
   Enter x3, traffic condition (0 = normal, 1 = congested): 1
   ```

For this example, the trained ANN should predict approximately `40` minutes. The final `Y_hat` is
highlighted in a green console box. The script then prints the synthetic reference target `Y`, the
absolute difference `|Y_hat - Y|`, and the same error in seconds so the result is easier to interpret.

---

## Files

```text
./
├── handmade_shallow_ann.py
├── requirements.txt
├── console-output.pdf
└── README.md
```

---

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img width="27" height="27" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53" alt="Code Chronicles logo"></a><a href="https://www.alexomegapy.com"><img height="30" src="https://img.shields.io/badge/Code%20Chronicles%20%7C%20Omegapy-0D1117?style=for-the-badge" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>
