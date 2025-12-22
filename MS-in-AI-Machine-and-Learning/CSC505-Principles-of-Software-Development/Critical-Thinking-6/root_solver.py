# -------------------------------------------------------------------------
# File: root_solver.py
# Project: Root Solver Console Application
# Author: Alexander Ricciardi
# Date: 2025-12-21
# [File Path] CTA-Module-6/root_solver.py
# ------------------------------------------------------------------------
# Course: CSC-505 Principles of Software Development
# Professor: Dr. Joseph Issa
# Winter A (25WA) – 2025
# ------------------------------------------------------------------------
# Assignment:
# Critical Thinking Assignment 6 – Root Solver
#
# Directions:
# Step 3: Write Your Python Implementation
#   - Translate your lowest-level refined design into working Python code.
#   - Use functions or classes to reflect the structure of your stepwise breakdown.
#   - Keep your code modular and clearly commented.
#   - The final script should demonstrate correct functionality for your selected problem.
#
# Selected Problem Domain: Root Solver
#   - Solve for the roots of a transcendental equation (e.g., using Newton-Raphson or
#     bisection method for equations like cos(x) - x = 0).
# ------------------------------------------------------------------------
# Project description:
# Root Solver is a small python script that solves for 
# the roots of a transcendental equation 
# (e.g., using Newton-Raphson or bisection method for equations like cos(x) - x = 0).
#
# A transcendental equation is an equation that involves functions such as
# sin, cos, exp, log, etc. These equations usually cannot be solved using algebraic methods,
# so numerical methods are used to approximate roots where f(x) ≈ 0.
#
# ------------------------------------------------------------------------

# --- Module Contents Overview ---
#
# TYPES AND DATA STRUCTURES:
#   - Class: Method (Enum) - Supported root-finding methods
#   - Class: Status (Enum) - Solver outcome statuses
#   - Class: SolverConfig (Dataclass) - Configuration for solver runs
#   - Class: SolveResult (Dataclass) - Results from solver execution
#   - Type: NumericFunction - Callable type alias for f(x)
#
# SAFE EXPRESSION HANDLING:
#   - Constant: ALLOWED_NAMES - Whitelist of safe math functions/constants
#   - Class: SafeExpressionValidator - AST validator for expression security
#   - Function: normalize_expression() - Preprocess user input
#   - Function: build_function() - Convert expression string to callable
#
# NUMERICAL SOLVER ALGORITHMS:
#   - Function: _numeric_derivative() - Central difference derivative
#   - Function: bisection_solve() - Bisection root-finding algorithm
#   - Function: newton_solve() - Newton-Raphson root-finding algorithm
#
# USER INTERFACE - DISPLAY UTILITIES:
#   - Function: render_menu() - Display and handle menu selection
#   - Function: print_banner() - Display colored section banners
#   - Function: show_equation_help() - Display equation syntax help
#   - Function: show_method_intro() - Display method-specific guidance
#   - Function: report_result() - Display solver results
#
# USER INTERFACE - INPUT PROMPTS:
#   - Function: prompt_equation() - Collect and validate equation input
#   - Function: prompt_method() - Collect method selection
#   - Function: prompt_tolerance() - Collect tolerance parameter
#   - Function: prompt_max_iterations() - Collect max iterations parameter
#   - Function: prompt_bisection_interval() - Collect bisection [a,b] interval
#   - Function: prompt_newton_config() - Collect Newton x0 and h parameters
#
# APPLICATION ORCHESTRATION:
#   - Function: solve_once() - Execute single solve cycle
#   - Function: main() - Main entry point and event loop
#
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: ast, math, re, dataclasses, enum, typing
# - Third-Party: colorama
# - Local Project Modules:
#   - utilities.menu_banner_utilities
#   - utilities.validation_utilities
# --- Requirements ---
# - Python 3.12
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Ac 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""
Root Solver is a small python script that solves for 
the roots of a transcendental equation 
(e.g., using Newton-Raphson or bisection method for equations like cos(x) - x = 0).

"""

from __future__ import annotations

# __________________________________________________________________________
# 
# ==========================================================================
# IMPORTS
# ==========================================================================

import ast
import math
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable

from colorama import Fore, Style, init

from utilities.menu_banner_utilities import Menu
from utilities.validation_utilities import (
    validate_prompt_float,
    validate_prompt_nonezero_positive_float,
    validate_prompt_nonezero_positive_int,
    validate_prompt_string,
    validate_prompt_yes_or_no,
    wait_for_enter,
)

init(autoreset=True)

# ____________________________________________________________________________
# Class Definitions
# ==========================================================================
# TYPES AND DATA STRUCTURES
# ==========================================================================
#
# Contains definitions of the types used in the program
# - Enums for method selection and status reporting
# - Dataclasses for configuration and results
# - Type aliases for cleaner function signatures
# ==========================================================================

# ------------------------------------------------------------------------- class Method
class Method(Enum):
    """Supported root-finding methods.

    Used by: the SolverConfig class, prompt_method(), show_method_intro(), solve_once(), 
    to determine which solver implementation to dispatch.

    Logic:
        - BISECTION: A method that requires an interval [a, b] where f(a) and f(b)
          have opposite signs (Intermediate Value Theorem guarantees a root exists between them).
          The interval is repeatedly halved until the root is found within tolerance.
          Pros: Always converges if bracket is valid. Cons: Slower convergence (linear).

        - NEWTON: An iterative method using the derivative f'(x) to refine guesses.
          Uses the formula: x_next = x - f(x) / f'(x)
          Pros: Fast convergence (quadratic near root). Cons: May diverge if f'(x) ≈ 0 or
          initial guess is poor.
    """

    BISECTION = auto()
    NEWTON = auto()
# ------------------------------------------------------------------------- end class Method

# ------------------------------------------------------------------------- class Status
class Status(Enum):
    """Outcome status returned by solvers.

    Used by: solver_bisection() and solver_newton() to label convergence/failure for reporting.

    Logic:
        - CONVERGED: The solver found a root within the specified tolerance. This is the
          successful outcome indicating |f(root)| <= tol or the step/interval size <= tol.

        - NOT_CONVERGED: The solver exhausted max_iter iterations without meeting the
          tolerance threshold. The returned root is the best estimate found, but may not
          be accurate enough.

        - FAILED_SAFELY: The solver encountered an unrecoverable condition (e.g., derivative
          too small in Newton, non-finite function value, invalid bracket). The solver
          stopped gracefully to prevent numerical instability or infinite loops.
    """

    CONVERGED = auto()
    NOT_CONVERGED = auto()
    FAILED_SAFELY = auto()
# ------------------------------------------------------------------------- end class Status

# ------------------------------------------------------------------------- class SolverConfig
@dataclass(slots=True, kw_only=True)
class SolverConfig:
    """Configuration inputs for a solver run.

    This dataclass encapsulates all parameters needed by the solvers, using a single
    unified structure for both bisection and Newton-Raphson methods.

    Attributes:
        equation: Original equation text (stored for display/reporting purposes).
        method: Solver method to use (BISECTION or NEWTON).
        tol: Residual or interval tolerance threshold. The solver stops when:
             - Bisection: |f(midpoint)| <= tol OR interval_width <= tol
             - Newton: |f(x)| <= tol OR |x_next - x| <= tol
        max_iter: Maximum iterations before giving up (safety cap to prevent infinite loops).
        a: Interval start for bisection (required when method=BISECTION).
        b: Interval end for bisection (required when method=BISECTION).
        x0: Initial guess for Newton-Raphson (required when method=NEWTON).
        use_numeric_derivative: Whether to use numeric derivative (always true here since
                                we don't ask users to provide analytical derivatives).
        h: Step size for numeric derivative using central difference formula:
           f'(x) ≈ (f(x+h) - f(x-h)) / (2h). Default 1e-6 balances accuracy and stability.

    Logic:
        Using a dataclass with slots=True for memory efficiency and kw_only=True to ensure
        all parameters are explicitly named when creating instances, reducing errors.
        Method-specific parameters (a, b for bisection; x0, h for Newton) default to None
        and are only populated based on the selected method.
    """

    equation: str
    method: Method
    tol: float
    max_iter: int
    a: float | None = None  # Bisection: left endpoint of bracket interval
    b: float | None = None  # Bisection: right endpoint of bracket interval
    x0: float | None = None  # Newton: starting guess for iteration
    use_numeric_derivative: bool = True  # Newton: use finite difference for f'(x)
    h: float = 1e-6  # Newton: step size for central difference derivative
# ------------------------------------------------------------------------- end class SolverConfig

# ------------------------------------------------------------------------- class SolveResult
@dataclass(slots=True, kw_only=True)
class SolveResult:
    """Result details from running a solver.

    Attributes:
        root: Computed root estimate (if any).
        iterations: Iterations performed.
        status: Convergence status flag.
        residual: Absolute residual at the returned root (if available).
        message: Human-readable status message.
    """

    root: float | None
    iterations: int
    status: Status
    residual: float | None
    message: str
# ------------------------------------------------------------------------- end class SolveResult


# __________________________________________________________________________
# Global Constants / Variablesas 
NumericFunction = Callable[[float], float]


## __________________________________________________________________________
# Global Constants / Variables
# ==========================================================================
# SAFE EXPRESSION HANDLING
# ==========================================================================
#
# Handles the parsing and validation of user-entered mathematical
# expressions (functions).
#
# User is prompted to use a mathematical expression to solve 
# these expressions can be Python code, so we need to validate them 
#
# SECURITY CONCERN: Note that Python's eval() is dangerous when used
# with untrusted input because it can execute any Python code.
# SOLUTION: A restricted evaluator is implemented using Python's AST (Abstract Syntax Tree)
# --------------------------------------------------------------------------- #

# Allowed function names and constants that can appear in user expressions.
# These are mapped to their actual Python/math implementations for use during evaluation.
ALLOWED_NAMES: dict[str, Any] = {
    # Trigonometric functions (transcendental)
    "sin": math.sin,    # sine function
    "cos": math.cos,    # cosine function
    "tan": math.tan,    # tangent function
    # Exponential and logarithmic functions (transcendental)
    "exp": math.exp,    # e^x exponential function
    "log": math.log,    # natural logarithm ln(x)
    # Other mathematical functions
    "sqrt": math.sqrt,  # square root √x
    "abs": abs,         # absolute value |x|
    "pow": pow,         # power function x^y
    # Mathematical constants
    "pi": math.pi,      # π ≈ 3.14159...
    "e": math.e,        # Euler's number e ≈ 2.71828...
}

# ____________________________________________________________________________
# Class Definitions
# ==========================================================================
# Safe Expression Validator
# ==========================================================================
#

# ------------------------------------------------------------------------- class SafeExpressionValidator
class SafeExpressionValidator(ast.NodeVisitor):
    """AST validator, a simple whitelist for safe expression evaluation.

    Logic:
        This class inherits from ast.NodeVisitor, which provides methods for walking
        through every node in a Python AST. By overriding the visit() method and specific
        visit_* methods, each node can be inspected and anything not on the whitelist will be rejected.

        In other words, any node type not explicitly listed
        in ALLOWED_NODES raises a ValueError, preventing execution of malicious code.
    """

    # Whitelist of AST node types that are safe for mathematical expressions.
    # Any node type not in this tuple will be rejected.
    ALLOWED_NODES = (
        ast.Expression,  # Top-level expression wrapper (required for mode="eval")
        ast.BinOp,       # Binary operations: x + y, x - y, x * y, x / y, x ** y
        ast.UnaryOp,     # Unary operations: -x, +x
        ast.Add,         # Addition operator (+)
        ast.Sub,         # Subtraction operator (-)
        ast.Mult,        # Multiplication operator (*)
        ast.Div,         # Division operator (/)
        ast.Pow,         # Power/exponent operator (**)
        ast.USub,        # Unary minus (-x)
        ast.UAdd,        # Unary plus (+x)
        ast.Call,        # Function calls: sin(x), cos(x), etc.
        ast.Name,        # Variable/function names: x, sin, cos, pi, etc.
        ast.Load,        # Context for loading a value (read access)
        ast.Constant,    # Numeric literals: 1, 2.5, 3.14, etc.
    )

    # -------------------------------------------------------------- visit()
    def visit(self, node: ast.AST) -> Any:  # type: ignore[override]
        """Visit each AST node and validate it against the whitelist.

        Logic:
            For every node in the AST, check if its type is in ALLOWED_NODES.
            If not, raise ValueError immediately to stop processing.
            If allowed, continue traversing child nodes via super().visit().
        """
        if not isinstance(node, self.ALLOWED_NODES):
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")
        return super().visit(node)
    # --------------------------------------------------------------

    # -------------------------------------------------------------- visit_Call()
    def visit_Call(self, node: ast.Call) -> Any:  # noqa: D401
        """Validate function calls, only approved math functions are used.

        Logic:
            Function calls like sin(x), cos(x), exp(x) are represented as ast.Call nodes.
            We check that:
            1. The function being called is a simple name (not an attribute like obj.method)
            2. The function name is in our ALLOWED_NAMES whitelist
            3. All arguments to the function are also valid (recursive validation)

            This prevents calls to dangerous functions like exec(), eval(), __import__(), etc.
        """
        if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_NAMES:
            raise ValueError("Only approved math functions are allowed.")
        # Recursively validate all function arguments
        for arg in node.args:
            self.visit(arg)
        return None
    # --------------------------------------------------------------

    # -------------------------------------------------------------- visit_Name()
    def visit_Name(self, node: ast.Name) -> Any:  # noqa: D401
        """Validate variable names, only 'x' and approved math names are used.

        Logic:
            Variable names in the expression can only be:
            1. 'x' - the independent variable we're solving for
            2. Names in ALLOWED_NAMES - math functions and constants (sin, cos, pi, e, etc.)

            This prevents access to Python builtins, globals, or any other dangerous names
            that could be used maliciously.
        """
        if node.id != "x" and node.id not in ALLOWED_NAMES:
            raise ValueError("Only variable 'x' and approved math names are allowed.")
        return None
    # --------------------------------------------------------------

    # -------------------------------------------------------------- visit_Attribute()
    def visit_Attribute(self, node: ast.Attribute) -> Any:  # noqa: D401
        """Reject attribute access explicitly to prevent sandbox escapes.

        Logic:
            Attribute access (like obj.attr) is a common vector for sandbox escapes.
            For example: "".__class__.__bases__[0].__subclasses__() can access dangerous classes.
            By rejecting ALL attribute access, we close this attack vector entirely.

            Mathematical expressions don't need attribute access - all functions are
            provided as top-level names in ALLOWED_NAMES.
        """
        raise ValueError("Attribute access is not allowed.")
    # --------------------------------------------------------------
# ------------------------------------------------------------------------- end class SafeExpressionValidator

# ____________________________________________________________________________
# Functions definitions
# ==========================================================================
# Normalize Expression and build function
# ==========================================================================
#

# -------------------------------------------------------------- normalize_expression()
def normalize_expression(expr: str) -> str:
    """Strip whitespace, convert caret, and validate allowed characters.

    Used by: build_function to pre-clean user input before AST parsing.

    Args:
        expr: Raw user-entered expression string.

    Returns:
        Normalized expression with whitespace removed and caret converted to exponent.

    Raises:
        ValueError: If disallowed characters are present.

    Logic:
        This function performs preprocessing on user input before AST parsing:

        1. Remove all whitespace: "cos(x) - x" → "cos(x)-x"
           This simplifies parsing and prevents whitespace-related edge cases.

        2. Convert caret to Python exponent: "x^2" → "x**2"
           Users commonly write x^2 for exponents (math notation), but Python uses **.

        3. Character whitelist validation: Only allow characters that could appear in
           valid mathematical expressions. This is an early filter before AST parsing.
           Allowed: digits, letters (for function/variable names), operators (+, -, *, /),
           parentheses, decimal point, comma (for function arguments like pow(x,2)), underscore.

        This preprocessing makes the expression Python-parseable while accepting
        common mathematical notation from users.
    """
    # Step 1: Remove all whitespace (spaces, tabs, newlines)
    cleaned = re.sub(r"\s+", "", expr)

    # Step 2: Convert caret notation to Python exponent notation
    # e.g., "x^2" becomes "x**2", "x^(1/2)" becomes "x**(1/2)"
    cleaned = cleaned.replace("^", "**")

    # Step 3: Validate that only allowed characters remain
    # Regex matches any character NOT in the allowed set
    # If a match is found, the expression contains invalid characters
    if re.search(r"[^0-9a-zA-Z+\-*/().,_]", cleaned):
        raise ValueError("Expression contains invalid characters.")

    return cleaned
# --------------------------------------------------------------

# -------------------------------------------------------------- build_function()
def build_function(expr: str) -> NumericFunction:
    """Build a safe callable f(x) from a user-entered expression.

    Args:
        expr: User-entered expression in terms of x.

    Returns:
        Callable numeric function of one float argument.

    Raises:
        ValueError: If parsing or evaluation fails or yields non-finite output.

    Logic:
        This function converts a user-entered string like "cos(x)-x" into a callable
        Python function f(x) that can be evaluated at any point. The process is:

        1. NORMALIZE: Clean up the expression (remove whitespace, convert ^ to **)
        2. PARSE: Use Python's ast module to parse the string into an Abstract Syntax Tree
        3. VALIDATE: Walk the AST to ensure only safe operations are present
        4. COMPILE: Convert the validated AST to bytecode for efficient repeated evaluation
        5. WRAP: Create a closure that evaluates the bytecode with x as the variable
        6. TEST: Probe with sample values to catch runtime errors early

        The resulting function can be called thousands of times during iteration
        without re-parsing the expression each time.
    """
    # Step 1: Normalize the expression (whitespace removal, ^ to ** conversion)
    expr = normalize_expression(expr)

    # Step 2: Parse the expression string into an Abstract Syntax Tree (AST)
    # mode="eval" indicates this is a single expression (not statements)
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Step 3: Validate the AST using our whitelist-based validator
    # This ensures no dangerous operations can be executed
    SafeExpressionValidator().visit(parsed)

    # Step 4: Compile the validated AST to bytecode for efficient evaluation
    # The bytecode is stored and reused for all subsequent evaluations
    code = compile(parsed, "<user_expr>", "eval")

    # Step 5: Create a closure function that evaluates the expression
    # - {"__builtins__": {}} removes access to Python builtins (security)
    # - {**ALLOWED_NAMES, "x": x} provides only our whitelisted names plus the x variable
    def f(x: float) -> float:
        return float(eval(code, {"__builtins__": {}}, {**ALLOWED_NAMES, "x": x}))

    # Step 6: Probe the function with test values to catch errors early
    # Some expressions might parse correctly but fail at runtime (e.g., log(-1), sqrt(-1))
    # Testing at x=0 and x=1 catches many common issues before the solver runs
    for probe in (0.0, 1.0):
        try:
            result = f(probe)
        except Exception as exc:
            raise ValueError(f"Expression failed evaluation: {exc}") from exc
        # Ensure the result is a finite number (not inf, -inf, or NaN)
        if not math.isfinite(result):
            raise ValueError("Expression must produce finite numeric values.")

    return f
# --------------------------------------------------------------

# ____________________________________________________________________________
# Functions definitions
#
# ==========================================================================
# NUMERICAL SOLVER ALGORITHMS
# ==========================================================================
#
# Contains the core numerical algorithms for finding roots.
# Each solver takes a configuration and function, returning a SolveResult.
#
# ROOT-FINDING OVERVIEW:
# A "root" of f(x) is a value x* where f(x*) = 0. Finding roots of transcendental
# equations analytically is often impossible, so we use numerical methods that
# iteratively refine an estimate until it's "close enough" to the true root.
#
# CONVERGENCE CRITERIA:
# We stop iterating when either:
#   1. The residual |f(x)| is smaller than tolerance (found a good root)
#   2. The step size or interval width is smaller than tolerance (can't improve further)
#   3. Maximum iterations reached (safety limit)
#   4. An error condition occurs (derivative too small, non-finite values)
# --------------------------------------------------------------------------- #

# -------------------------------------------------------------- _numeric_derivative()
def _numeric_derivative(f: NumericFunction, x: float, h: float) -> float:
    """Compute central-difference derivative approximation.

    Args:
        f: Function to differentiate.
        x: Point of evaluation.
        h: Step size (small positive value, typically 1e-6).

    Returns:
        Central-difference derivative estimate at x.

    Logic:
        The derivative f'(x) measures the rate of change of f at point x.
        Since we don't have an analytical formula for f'(x), we approximate it
        numerically using the central difference formula:

            f'(x) ≈ [f(x + h) - f(x - h)] / (2h)

        Why central difference instead of forward difference [f(x+h) - f(x)]/h?
        - Central difference has O(h²) error vs O(h) for forward difference
        - This means smaller h gives much better accuracy with central difference

        The step size h must be chosen carefully:
        - Too large: approximation error is significant
        - Too small: floating-point rounding errors dominate
        - Default h=1e-6 is a good balance for most functions
    """
    return (f(x + h) - f(x - h)) / (2.0 * h)
# --------------------------------------------------------------

# -------------------------------------------------------------- bisection_solve()
def bisection_solve(config: SolverConfig, f: NumericFunction) -> SolveResult:
    """Run bisection on [a, b] with the given tolerance and iteration cap.

    Used by: solve_once() after collecting bisection inputs to compute the root.

    Args:
        config: Solver configuration containing interval and tolerances.
        f: Function whose root is sought.

    Returns:
        SolveResult describing convergence status and root estimate.

    Logic:
        THE BISECTION METHOD (also called "binary search for roots"):

        Mathematical Foundation - Intermediate Value Theorem (IVT):
            If f is continuous on [a, b] and f(a) and f(b) have opposite signs,
            then there exists at least one root c in (a, b) where f(c) = 0.

        Algorithm:
            1. Start with interval [a, b] where f(a) * f(b) < 0 (sign change)
            2. Compute midpoint m = (a + b) / 2
            3. Evaluate f(m)
            4. The root is in whichever half has the sign change:
               - If f(a) * f(m) < 0: root is in [a, m], so set b = m
               - Otherwise: root is in [m, b], so set a = m
            5. Repeat until |f(m)| <= tol or interval width <= tol

        Convergence Properties:
            - GUARANTEED to converge if the initial bracket is valid
            - Each iteration halves the interval, so after n iterations:
              interval width = (b - a) / 2^n
            - Linear convergence rate: gains about 1 bit of precision per iteration
            - Slow but reliable - often used as a fallback method

        Example: Finding root of cos(x) - x = 0 on [0, 1]
            f(0) = cos(0) - 0 = 1 > 0
            f(1) = cos(1) - 1 ≈ -0.46 < 0
            Sign change exists, so a root is between 0 and 1.
    """
    # VALIDATION: Ensure interval endpoints are provided
    if config.a is None or config.b is None:
        return SolveResult(
            root=None,
            iterations=0,
            status=Status.FAILED_SAFELY,
            residual=None,
            message="Missing interval endpoints for bisection.",
        )

    # Initialize interval bounds and evaluate function at endpoints
    a = config.a
    b = config.b
    fa = f(a)  # f(a) = function value at left endpoint
    fb = f(b)  # f(b) = function value at right endpoint

    # VALIDATION: Ensure function produces finite values at endpoints
    if not (math.isfinite(fa) and math.isfinite(fb)):
        return SolveResult(
            root=None,
            iterations=0,
            status=Status.FAILED_SAFELY,
            residual=None,
            message="Function not finite at interval endpoints.",
        )

    # VALIDATION: Check the bracketing condition (IVT prerequisite)
    # f(a) * f(b) < 0 means they have opposite signs (one positive, one negative)
    # This guarantees a root exists in the interval by the Intermediate Value Theorem
    if fa * fb >= 0:
        return SolveResult(
            root=None,
            iterations=0,
            status=Status.FAILED_SAFELY,
            residual=None,
            message="Invalid bracket: f(a) and f(b) must have opposite signs.",
        )

    # MAIN ITERATION LOOP: Repeatedly halve the interval until convergence
    for iteration in range(1, config.max_iter + 1):
        # Step 1: Compute the midpoint of the current interval
        mid = (a + b) / 2.0

        # Step 2: Evaluate the function at the midpoint
        fm = f(mid)

        # SAFETY CHECK: Ensure function value is finite (not inf or NaN)
        if not math.isfinite(fm):
            return SolveResult(
                root=None,
                iterations=iteration,
                status=Status.FAILED_SAFELY,
                residual=None,
                message="Function produced non-finite value during bisection.",
            )

        # Step 3: Check convergence criteria
        interval_width = (b - a) / 2.0
        # Converged if: residual is small enough OR interval is small enough
        if abs(fm) <= config.tol or interval_width <= config.tol:
            return SolveResult(
                root=mid,
                iterations=iteration,
                status=Status.CONVERGED,
                residual=abs(fm),
                message="Converged by tolerance.",
            )

        # Step 4: Narrow the interval - keep the half that contains the root
        # The root is in the half where the sign change occurs
        if fa * fm < 0:
            # Sign change is between a and mid, so root is in [a, mid]
            b = mid
            fb = fm
        else:
            # Sign change is between mid and b, so root is in [mid, b]
            a = mid
            fa = fm

    # If we exit the loop, we've exhausted max_iter without converging
    # Return the best estimate (final midpoint) with NOT_CONVERGED status
    return SolveResult(
        root=(a + b) / 2.0,
        iterations=config.max_iter,
        status=Status.NOT_CONVERGED,
        residual=abs(f((a + b) / 2.0)),
        message="Reached max iterations without convergence.",
    )
# --------------------------------------------------------------

# -------------------------------------------------------------- newton_solve()
def newton_solve(config: SolverConfig, f: NumericFunction) -> SolveResult:
    """Run Newton-Raphson with numeric derivative by default.

    Used by: solve_once() after collecting Newton inputs to compute the root.

    Args:
        config: Solver configuration containing initial guess and tolerances.
        f: Function whose root is sought.

    Returns:
        SolveResult describing convergence status and root estimate.

    Logic:
        THE NEWTON-RAPHSON METHOD (also called "Newton's Method"):

        Mathematical Foundation:
            Uses Taylor series approximation. Near a point x, f can be approximated as:
                f(x + Δx) ≈ f(x) + f'(x) * Δx

            Setting f(x + Δx) = 0 and solving for Δx:
                0 ≈ f(x) + f'(x) * Δx
                Δx ≈ -f(x) / f'(x)

            So the next estimate is:
                x_next = x + Δx = x - f(x) / f'(x)

        Algorithm:
            1. Start with initial guess x₀
            2. Compute f(x) and f'(x)
            3. Update: x_next = x - f(x) / f'(x)
            4. Repeat until |f(x)| <= tol or |x_next - x| <= tol

        Geometric Interpretation:
            At each iteration, we draw the tangent line to the curve at point (x, f(x))
            and find where this tangent crosses the x-axis. That intersection becomes
            our next estimate. Near a simple root, this converges very quickly.

        Convergence Properties:
            - QUADRATIC convergence near a simple root: error roughly squares each iteration
            - Much faster than bisection when it works (often 4-6 iterations vs 20-50)
            - NOT guaranteed to converge: can diverge if:
                * Initial guess is too far from root
                * f'(x) ≈ 0 at some point (division by near-zero)
                * Function has inflection points or multiple roots nearby

        Why Numeric Derivative?
            We use central difference approximation f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
            instead of requiring users to provide analytical derivatives. This makes
            the method easier to use at the cost of slightly reduced accuracy.

        Example: Finding root of cos(x) - x = 0 starting at x₀ = 1
            f(1) = cos(1) - 1 ≈ -0.4597
            f'(1) = -sin(1) - 1 ≈ -1.8415
            x₁ = 1 - (-0.4597) / (-1.8415) ≈ 0.7504
            ... converges to ≈ 0.7391 in about 3-4 iterations
    """
    # VALIDATION: Ensure initial guess is provided
    if config.x0 is None:
        return SolveResult(
            root=None,
            iterations=0,
            status=Status.FAILED_SAFELY,
            residual=None,
            message="Missing initial guess for Newton-Raphson.",
        )

    # Initialize current estimate and derivative step size
    x = config.x0  # Current estimate of the root
    h = config.h   # Step size for numerical derivative (default 1e-6)

    # MAIN ITERATION LOOP: Refine estimate using Newton's formula
    for iteration in range(1, config.max_iter + 1):
        # Step 1: Evaluate the function at current estimate
        fx = f(x)

        # SAFETY CHECK: Ensure function value is finite (not inf or NaN)
        if not math.isfinite(fx):
            return SolveResult(
                root=None,
                iterations=iteration,
                status=Status.FAILED_SAFELY,
                residual=None,
                message="Function produced non-finite value during Newton-Raphson.",
            )

        # Step 2: Check if we've found a root (residual convergence)
        # If |f(x)| is small enough, x is close to a root
        if abs(fx) <= config.tol:
            return SolveResult(
                root=x,
                iterations=iteration,
                status=Status.CONVERGED,
                residual=abs(fx),
                message="Converged by residual tolerance.",
            )

        # Step 3: Compute the derivative f'(x) using central difference
        derivative = _numeric_derivative(f, x, h)

        # SAFETY CHECK: Ensure derivative is finite and not too small
        # If f'(x) ≈ 0, division would cause huge steps (instability) or inf
        # Threshold 1e-12 prevents division by very small numbers
        if not math.isfinite(derivative) or abs(derivative) < 1e-12:
            return SolveResult(
                root=None,
                iterations=iteration,
                status=Status.FAILED_SAFELY,
                residual=abs(fx),
                message="Derivative too small; failing safely.",
            )

        # Step 4: Apply Newton's update formula: x_next = x - f(x) / f'(x)
        # This is the core of the algorithm - move to where the tangent line hits y=0
        x_next = x - fx / derivative

        # Step 5: Check for step-size convergence
        # If the change in x is tiny, we've effectively converged
        # (useful when f(x) is small but not quite below tolerance)
        if abs(x_next - x) <= config.tol:
            return SolveResult(
                root=x_next,
                iterations=iteration,
                status=Status.CONVERGED,
                residual=abs(f(x_next)),
                message="Converged by step tolerance.",
            )

        # Step 6: Update x for next iteration
        x = x_next

    # If we exit the loop, we've exhausted max_iter without converging
    # Return the best estimate with NOT_CONVERGED status
    return SolveResult(
        root=x,
        iterations=config.max_iter,
        status=Status.NOT_CONVERGED,
        residual=abs(f(x)),
        message="Reached max iterations without convergence.",
    )
# --------------------------------------------------------------

# ____________________________________________________________________________
# Functions definitions
# ==========================================================================
# USER INTERFACE - DISPLAY UTILITIES
# ==========================================================================
#
# Contains functions for displaying information to the user:
# menus, banners, help screens, method introductions, and result reports.
# These handle OUTPUT to the console with consistent formatting and colors.
# ==========================================================================

# -------------------------------------------------------------- render_menu()
def render_menu(title: str, options: list[str]) -> int:
    """Render a menu and return the validated user choice.

    Used by: main loop and method selection to capture numbered choices.

    Args:
        title: Menu title text.
        options: List of option strings.

    Returns:
        Selected option index (1-based).

    Logic:
        This function encapsulates the pattern of displaying a numbered menu
        and validating user input. It uses the shared Menu utility for consistent
        visual formatting across the application.

        The validation loop ensures the user must enter a valid option number:
        1. Display the menu with numbered options
        2. Prompt for a positive integer
        3. If the number is out of range (< 1 or > number of options), re-prompt
        4. Return only when a valid choice is made

        The 1-based indexing is user-friendly (humans count from 1, not 0).
    """
    print()
    # Create a Menu object using the shared utility for consistent formatting
    menu = Menu(title, options)
    print(menu.render())

    # Get initial input - validate_prompt_nonezero_positive_int ensures positive integer
    choice = validate_prompt_nonezero_positive_int(
        f"Enter a choice ({menu._choice_index_list()}): "
    )

    # Validation loop: keep prompting until choice is within valid range [1, len(options)]
    while choice < 1 or choice > len(options):
        print(Fore.LIGHTRED_EX + "Please select a valid option.")
        choice = validate_prompt_nonezero_positive_int(
            f"Enter a choice ({menu._choice_index_list()}): "
        )

    return choice
# --------------------------------------------------------------

# -------------------------------------------------------------- print_banner()
def print_banner(title: str, color: str = Fore.CYAN) -> None:
    """Display a colored banner using the shared Banner utility.

    Used by: main loop and method intro screens to frame sections.

    Args:
        title: Text to place inside the banner.
        color: Color escape for the banner text.
    """
    from utilities.menu_banner_utilities import Banner

    banner_obj = Banner([(title, "center", False)], inner_width=max(20, len(title) + 4))
    rendered = banner_obj.render()
    colored = "\n".join(color + line + Style.RESET_ALL for line in rendered.splitlines())
    print("\n" + colored + "\n")
# -------------------------------------------------------------- 

# -------------------------------------------------------------- show_equation_help()
def show_equation_help() -> None:
    """Display guidance on entering transcendental equations and supported syntax.

    Used by: main menu help option.
    """
    print_banner("How to Write a Transcendental Equation", Fore.LIGHTBLUE_EX)
    print(Fore.CYAN + "What is a transcendental equation?")
    print(
        Fore.WHITE
        + (
            "An equation involving transcendental functions such as exp, log, sin, cos, tan, "
            "sqrt, or x^x."
        ),
    )
    print()
    print(Fore.CYAN + "Syntax tips:")
    print(Fore.WHITE + "- Use aly 'x' as the variable.")
    print(Fore.WHITE + "- Use ^ or ** for exponents (e.g., x^3, x^(1/2), x^x).")
    print(Fore.WHITE + "- Use pow(x,y) for exponents (e.g., pow(x,3), pow(x,1/3)).")
    print(Fore.WHITE + "- Use log(x) for logarithmic functions.")
    print(Fore.WHITE + "- Use sin(x) for sine functions.")
    print(Fore.WHITE + "- Use cos(x) for cosine functions.")
    print(Fore.WHITE + "- Use tan(x) for tangent functions.")
    print(Fore.WHITE + "- Use abs(x) for absolute value functions.")
    print(Fore.WHITE + "- Use pi and e for mathematical constants.")
    print()
    print(Fore.CYAN + "Examples:")
    examples = [
        "cos(x)-x",
        "x^x-2",
        "sqrt(x)-1",
        "pow(x,3)-8",
        "x^(1/3)-2",
    ]
    for ex in examples:
        print(Fore.WHITE + f"  - {ex}")
    print()
    wait_for_enter()
    print()
# --------------------------------------------------------------

# ____________________________________________________________________________
# Functions definitions
# ==========================================================================
# USER INTERFACE - INPUT PROMPTS
# ==========================================================================
#
# Contains functions for collecting INPUT from the user:
# equation entry, method selection, and solver parameter collection.
# Each function validates input and re-prompts until valid data is provided.
# ==========================================================================

# -------------------------------------------------------------- prompt_equation()
def prompt_equation() -> tuple[str, NumericFunction]:
    """Prompt for a transcendental equation and return validated text and callable.

    Used by: main() to capture the user equation before method selection.

    Returns:
        Tuple of raw expression text and compiled numeric function.

    Logic:
        This function collects the equation from the user and converts it into
        a callable function f(x). It implements a validation loop that continues
        until valid input is received.

        VALIDATION STEPS:
        1. Read string input from user
        2. Quick check: equation must contain 'x' (the variable we're solving for)
        3. Full validation via build_function():
           - Character validation (no weird symbols)
           - AST parsing (valid Python expression syntax)
           - Security validation (only allowed functions/names)
           - Runtime test (evaluates at x=0 and x=1 to catch errors)

        WHY TWO RETURN VALUES?
        - expr (string): Kept for display purposes in report_result()
        - func (callable): The compiled function used by solvers

        The loop catches ValueError from build_function() and displays the error
        message, allowing the user to try again with a corrected expression.

        EXAMPLE INTERACTION:
        > Enter transcendental equation in x: cos(x-x
        Error: Invalid expression syntax: ...
        > Enter transcendental equation in x: import os
        Error: Only approved math functions are allowed.
        > Enter transcendental equation in x: cos(x)-x
        [Success - returns ("cos(x)-x", <function>)]
    """
    print()
    # Validation loop - continues until valid equation is entered
    while True:
        # Get raw string input from user
        expr = validate_prompt_string("Enter transcendental equation in x (e.g., cos(x)-x): ")

        # Quick validation: equation must reference the variable 'x'
        # An equation like "cos(2)-1" has no variable and isn't useful for root-finding
        if "x" not in expr:
            print(Fore.LIGHTRED_EX + "Expression must contain variable 'x'.")
            continue  # Re-prompt

        # Full validation: try to build a callable function
        # build_function() will raise ValueError if anything is wrong
        try:
            func = build_function(expr)
            # Success! Return both the original text and the compiled function
            return expr, func
        except ValueError as exc:
            # Display the specific error and re-prompt
            print(Fore.LIGHTRED_EX + f"{exc}")
# --------------------------------------------------------------

# -------------------------------------------------------------- prompt_method()
def prompt_method() -> Method:
    """Prompt for solver method selection and show method intro.

    Used by: solve_once to branch into bisection or Newton configuration.

    Returns:
        Chosen Method enum value.
    """
    choice = render_menu("Select Method", ["Bisection", "Newton-Raphson"])
    method = Method.BISECTION if choice == 1 else Method.NEWTON
    show_method_intro(method)
    return method
# -------------------------------------------------------------- 

# -------------------------------------------------------------- show_method_intro()
def show_method_intro(method: Method) -> None:
    """Print a brief description of the chosen method and its parameters.

    Used by: prompt_method to give context before parameter prompts.

    Args:
        method: Selected solver method.
    """
    if method is Method.BISECTION:
        print_banner("Bisection Method", Fore.LIGHTGREEN_EX)
        print(Fore.WHITE + "Requires a sign change on [a, b]; repeatedly halves the interval.")
        print(Fore.CYAN + "You will enter:")
        print(Fore.WHITE + "- Tolerance (stopping threshold)")
        print(Fore.WHITE + "- Max iterations")
        print(Fore.WHITE + "- Interval start (a)")
        print(Fore.WHITE + "- Interval end (b)")
        print()
        print(Fore.CYAN + "Parameter notes:")
        print(Fore.WHITE + "- Tolerance: stop when |f(m)| <= tol or interval width <= tol.")
        print(Fore.WHITE + "- Max iterations: safety cap on loop count.")
        print(
            Fore.WHITE
            + (
                "- Interval start/end: [a, b] must bracket a sign change "
                "(f(a)*f(b) < 0)."
            ),
        )
    else:
        print_banner("Newton-Raphson Method", Fore.MAGENTA)
        print(Fore.WHITE + "Uses derivative to refine an initial guess x0.")
        print(Fore.CYAN + "You will enter:")
        print(Fore.WHITE + "- Tolerance (stopping threshold)")
        print(Fore.WHITE + "- Max iterations")
        print(Fore.WHITE + "- Initial guess x0")
        print(Fore.WHITE + "- Derivative step h (e.g., 1e-6)")
        print()
        print(Fore.CYAN + "Parameter notes:")
        print(Fore.WHITE + "- Tolerance: stop when residual or step size is below tol.")
        print(Fore.WHITE + "- Max iterations: safety cap on loop count.")
        print(Fore.WHITE + "- Initial guess x0: starting point; better guesses converge faster.")
        print(Fore.WHITE + "- Derivative step h: finite-difference step; too small may be unstable.")
    print()
# -------------------------------------------------------------- 

# -------------------------------------------------------------- prompt_tolerance()
def prompt_tolerance() -> float:
    """Prompt for a positive tolerance.

    Used by: solve_once prior to method-specific prompts.

    Returns:
        Positive tolerance value.
    """
    while True:
        tol = validate_prompt_nonezero_positive_float("Enter tolerance (>0): ")
        if tol > 0:
            return tol
        print(Fore.LIGHTRED_EX + "Tolerance must be greater than zero.")
# -------------------------------------------------------------- 

# -------------------------------------------------------------- prompt_max_iterations()
def prompt_max_iterations() -> int:
    """Prompt for a positive max iteration count.

    Used by: solve_once prior to method-specific prompts.

    Returns:
        Max iteration count (>=1).
    """
    while True:
        max_iter = validate_prompt_nonezero_positive_int("Enter max iterations (>=1): ")
        if max_iter >= 1:
            return max_iter
        print(Fore.LIGHTRED_EX + "Max iterations must be at least 1.")
# -------------------------------------------------------------- 

# -------------------------------------------------------------- prompt_bisection_interval()
def prompt_bisection_interval(f: NumericFunction) -> tuple[float, float]:
    """Prompt for a valid bisection interval and enforce sign change.

    Used by: solve_once when method is bisection.

    Args:
        f: Function to evaluate interval endpoints.

    Returns:
        Tuple of (a, b) satisfying a < b and f(a)*f(b) < 0.

    Logic:
        The bisection method requires a valid "bracket" - an interval [a, b] where:
        1. a < b (proper interval ordering)
        2. f(a) and f(b) have opposite signs (one positive, one negative)

        The second condition is crucial: by the Intermediate Value Theorem, if a
        continuous function changes sign over an interval, it must cross zero
        somewhere in that interval. This guarantees a root exists.

        VALIDATION PROCESS:
        1. Prompt for interval endpoints a and b
        2. Check a < b (reject if not)
        3. Evaluate f(a) and f(b)
        4. Check f(a) * f(b) < 0 (product is negative when signs differ)
        5. If checks fail, explain the error and re-prompt

        The loop continues until the user provides valid input. This "fail early,
        fail helpfully" approach prevents the solver from starting with invalid
        inputs that would immediately fail.

        Example for cos(x) - x = 0:
        - f(0) = cos(0) - 0 = 1 > 0 (positive)
        - f(1) = cos(1) - 1 ≈ -0.46 < 0 (negative)
        - f(0) * f(1) = 1 * (-0.46) < 0 ✓ Valid bracket!
    """
    # Loop until the user provides a valid bracket with a sign change.
    while True:
        # Get interval endpoints from user
        a = validate_prompt_float("Enter interval start a: ")
        b = validate_prompt_float("Enter interval end b: ")

        # Validation 1: Ensure proper interval ordering (a must be less than b)
        if a >= b:
            print(Fore.LIGHTRED_EX + "Require a < b.")
            continue  # Re-prompt

        # Evaluate function at both endpoints
        fa = f(a)
        fb = f(b)

        # Validation 2: Check for sign change (bracketing condition)
        # If f(a) * f(b) >= 0, both have the same sign (or one is zero)
        # This means there might not be a root in the interval
        if fa * fb >= 0:
            print(Fore.LIGHTRED_EX + "f(a) and f(b) must have opposite signs.")
            continue  # Re-prompt

        # Both validations passed - return the valid interval
        return a, b
# --------------------------------------------------------------

# -------------------------------------------------------------- prompt_newton_config()
def prompt_newton_config() -> tuple[float, float]:
    """Prompt for Newton-Raphson initial guess and derivative step.

    Used by: solve_once when method is Newton-Raphson.

    Returns:
        Tuple of (x0, h) values.
    """
    # Loop until both the initial guess and derivative step validate.
    x0 = validate_prompt_float("Enter initial guess x0: ")
    h = validate_prompt_nonezero_positive_float("Enter derivative step h (e.g., 1e-6): ")
    return x0, h
# -------------------------------------------------------------- 

# -------------------------------------------------------------- report_result()
def report_result(result: SolveResult, equation: str, method: Method) -> None:
    """Print a formatted summary of solver results.

    Used by: solve_once after solver execution to display status.

    Args:
        result: Outcome from the solver.
        equation: Original equation text.
        method: Method used to obtain the result.

    Logic:
        This function presents the solver output in a clear, color-coded format.
        Color-coding provides immediate visual feedback on success/failure:

        OUTPUT FIELDS:
            Equation: The original equation being solved (for reference)
            Method: BISECTION or NEWTON (which algorithm was used)
            Iterations: How many iterations the solver performed
            Root: The computed root estimate (or N/A if solver failed)
            Residual: |f(root)| - how close the root is to zero (smaller is better)
            Status: Convergence outcome with color coding

        COLOR SCHEME:
            GREEN (CONVERGED): Success! Root found within tolerance.
            YELLOW (NOT_CONVERGED): Partial success - best estimate returned
                                    but didn't meet tolerance criteria.
            RED (FAILED_SAFELY): Solver couldn't proceed (invalid input,
                                 derivative issues, etc.)

        FORMATTING CHOICES:
            - Root shown with 10 decimal places for precision
            - Residual in scientific notation (e.g., 1.234e-07) for small values
            - Status message in dimmed text to not overwhelm the main results
    """
    # Map status to appropriate color for visual feedback
    status_color = {
        Status.CONVERGED: Fore.LIGHTGREEN_EX,       # Green = success
        Status.NOT_CONVERGED: Fore.YELLOW,          # Yellow = partial success/warning
        Status.FAILED_SAFELY: Fore.LIGHTRED_EX,     # Red = failure
    }[result.status]

    print()
    # Display input summary (what was being solved)
    print(f"{Fore.CYAN}Equation: {equation}")
    print(f"{Fore.CYAN}Method: {method.name.title()}")

    # Display solver metrics
    print(f"{Fore.CYAN}Iterations: {result.iterations}")

    # Format root: show with precision or N/A if solver failed
    root_text = "N/A" if result.root is None else f"{result.root:.10f}"

    # Format residual: scientific notation for small numbers, N/A if unavailable
    residual_text = "N/A" if result.residual is None else f"{result.residual:.3e}"

    print(f"{Fore.CYAN}Root: {root_text}")
    print(f"{Fore.CYAN}Residual: {residual_text}")

    # Status line with color-coded outcome
    print(status_color + f"Status: {result.status.name}")

    # Additional message (if any) in dimmed text
    if result.message:
        print(f"{Style.DIM}{result.message}{Style.RESET_ALL}")

    print()
# --------------------------------------------------------------

# ____________________________________________________________________________
# Functions definitions
# ==========================================================================
# APPLICATION ORCHESTRATION
# ==========================================================================
#
# These functions coordinate the high-level flow of the application without
# implementing the details. They call the appropriate prompt, validation,
# solver, and reporting functions in sequence.
#
# ==========================================================================

# -------------------------------------------------------------- solve_once()
def solve_once() -> None:
    """Execute one solve cycle: prompt, configure, solve, and report.

    Used by: main loop for each run.

    Logic:
        This function orchestrates a single root-solving session by coordinating
        the flow through all the steps required to solve for a root:

        STEP 1: GATHER EQUATION
            - Prompt user for equation text (e.g., "cos(x)-x")
            - Parse and validate the equation, building a callable f(x)
            - Re-prompt if equation is invalid

        STEP 2: SELECT METHOD
            - Show menu for bisection vs Newton-Raphson
            - Display method-specific introduction and parameter requirements

        STEP 3: COLLECT COMMON PARAMETERS
            - Get tolerance (stopping threshold for convergence)
            - Get max iterations (safety limit)

        STEP 4: COLLECT METHOD-SPECIFIC PARAMETERS
            - Bisection: interval [a, b] with sign change validation
            - Newton: initial guess x0 and derivative step h

        STEP 5: BUILD CONFIGURATION AND SOLVE
            - Create SolverConfig dataclass with all parameters
            - Dispatch to appropriate solver function

        STEP 6: REPORT RESULTS
            - Display root estimate, iterations, status, residual

        This flow matches the Level 2 mid-level refinement in the assignment's
        stepwise breakdown: main() → prompt_equation() → prompt_config() →
        solve_root() → report_results()
    """
    # Step 1: Get and validate the equation from the user
    # Returns both the original text (for display) and the compiled function
    equation_text, func = prompt_equation()

    # Step 2: Let user choose the root-finding method
    # Also shows an introduction to the selected method
    method = prompt_method()

    # Step 3: Collect parameters common to both methods
    tol = prompt_tolerance()      # Convergence threshold (e.g., 1e-6)
    max_iter = prompt_max_iterations()  # Safety limit (e.g., 100)

    # Step 4 & 5: Collect method-specific parameters and run solver
    if method is Method.BISECTION:
        # Bisection requires interval [a, b] with a sign change
        a, b = prompt_bisection_interval(func)
        config = SolverConfig(
            equation=equation_text,
            method=method,
            tol=tol,
            max_iter=max_iter,
            a=a,
            b=b,
        )
        # Run bisection algorithm
        result = bisection_solve(config, func)
    else:
        # Newton requires initial guess x0 and derivative step h
        x0, h = prompt_newton_config()
        config = SolverConfig(
            equation=equation_text,
            method=method,
            tol=tol,
            max_iter=max_iter,
            x0=x0,
            use_numeric_derivative=True,
            h=h,
        )
        # Run Newton-Raphson algorithm
        result = newton_solve(config, func)

    # Step 6: Display the results to the user
    report_result(result, equation_text, method)
# --------------------------------------------------------------

# ____________________________________________________________________________
# Functions definitions
# ==========================================================================
# MAIN FUNCTION- Entry Point
# ==========================================================================
#
# -------------------------------------------------------------- main()
def main() -> None:
    """Run the root solver in a loop until the user chooses to exit.

    Used by: module entry point.

    Logic:
        This is the top-level entry point (Level 1 in Stepwise Refinement).
        It implements a simple event loop pattern:

        1. Display welcome banner
        2. Show main menu with options
        3. Execute the selected action
        4. Repeat until user confirms exit

        MENU OPTIONS:
            [1] Solve a root
                → Runs the complete solve cycle via solve_once()
                → User can solve multiple equations in one session

            [2] How to write a transcendental equation
                → Educational help screen explaining syntax
                → Shows supported functions, operators, and examples
                → Helps users who are unfamiliar with expression format

            [3] Exit
                → Confirmation prompt prevents accidental exits
                → Only exits on explicit "yes" confirmation

        This structure follows the assignment's requirement for a menu-driven
        interface and allows users to solve multiple equations without
        restarting the program.

        The infinite while loop with explicit break is a common pattern for
        interactive console applications - it continues running until the
        user explicitly chooses to exit and confirms their choice.
    """
    # Display the application title banner
    print_banner("Root Resolver", Fore.LIGHTBLUE_EX)

    # Main event loop - continues until user chooses to exit
    while True:
        # Display menu and get user's choice (1, 2, or 3)
        choice = render_menu(
            "Main Menu",
            ["Solve a root", "How to write a transcendental equation", "Exit"],
        )

        if choice == 1:
            # Option 1: Run a complete root-solving session
            solve_once()
        elif choice == 2:
            # Option 2: Show help documentation on equation syntax
            show_equation_help()
        else:
            # Option 3: Exit with confirmation to prevent accidents
            if validate_prompt_yes_or_no("Are you sure you want to quit?"):
                print(Fore.LIGHTBLUE_EX + "Goodbye!")
                break  # Exit the while loop, ending the program

    return None
# --------------------------------------------------------------

# ==========================================================================
# MODULE INITIALIZATION
# ==========================================================================
if __name__ == "__main__":
    main()

# ____________________________________________________________________________
# 
# ==========================================================================
#  End of File
# ==========================================================================
