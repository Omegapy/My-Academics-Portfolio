# -------------------------------------------------------------------------
# File: sales_analysis.py
# Project: Omega.py Sales Analysis
# Author: Alexander Ricciardi
# Date: 2025-11-16
# CTA-Module-1/sales_analysis.py
# ------------------------------------------------------------------------
# Course: CSS-505 Principal of Software Development
# Professor: Dr. Brian Holbert
# Winter W-2025
# Nov.-Jan. 2025
# ------------------------------------------------------------------------
# Assignement:
# Critical Thinking Assignment 1
#
# Directions:
# For this assignment, you will write a simple Python prototype and then create a short developer report, 
# simulating the kind of deliverable expected by a technical team lead or project manager 
# in a modern software development environment. Whether you’re working independently or as part of a team, 
# understanding the challenges of software development and communicating technical work clearly are essential skills for success.
# To get familiar with Python programming and integrated development tools used in the field, 
# begin by writing a Python script with a practical, real-world purpose. 
# Then, create a brief developer-facing report reflecting on key aspects of your experience 
# and how they relate to broader software development challenges.
#
# Part 1: Python Script Development
# Write a Python script that performs a useful or realistic task. 
# 
# You may choose one of the following or propose your own idea:
# A command-line tip calculator.
# A script that reads and analyzes a CSV file (e.g., grades, sales).
# A simple to-do list or task tracker.
# A basic simulation (e.g., mock CPU/memory monitor using random values).
# A log parser that searches for keywords in a sample file.
# Use any modern IDE of your choice (e.g., VS Code, PyCharm, Replit).
#
# Part 2: Developer Report (Professional Documentation)
# After completing your script, 
# prepare a developer report answering the following stakeholder-facing questions based on your experience:
# What was the purpose or intended use case of your script?
# What tools or libraries did you use, and why?
# What challenges did you encounter during development?
# How would you expand or improve this prototype in future iterations?
# What lessons did you learn that apply to broader software development work?
# ------------------------------------------------------------------------
# Project:
# Omega.py Sales Analysis 
#
# Project description:
# Console-based application that loads Omega.py sales CSV data, computes metrics,
# and computes sales analytics
#
# ------------------------------------------------------------------------

# --- File Contents Overview ---
# - Constants: DEFAULT_DATA_PATH
# - Functions: load_sales_data, compute_metrics, group_by_product, group_by_category,
#              group_by_date, render_banner, format_currency, display_metric,
#              display_best_product_revenues, display_revenue_by_category, display_daily_revenue,
#              show_revenue_graph, prompt_for_csv_path, print_error, print_warning,
#              print_success, print_info, run_app, sales_loaded, main,
#              calculate_discount, my_utility_function, get_user_confirmation,
#              process_module_data
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: pathlib.Path, decimal.Decimal, typing (Any, Final)
# - Third-Party: numpy, pandas, colorama, matplotlib
# - Local Project Modules:
#   - utilities.menu_banner_utilities (Banner, Menu)
#   - utilities.validation_utilities (validate_prompt_string, validate_prompt_yes_or_no)
# --- Requirements ---
# - Python 3.12
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Ac 2025 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Sales analysis console application load hat loads Omega.py sales CSV data, 
computes metrics, and computes sales analytics
"""

# __________________________________________________________________________
# Imports
#

# For annotations (type hints/docstrings)
from __future__ import annotations

# Standard library imports
from decimal import Decimal
from pathlib import Path # File system utilities
from typing import Any, Final

# data analysis
import numpy as np  # Numerical array operations 
import pandas as pd  # Tabular data 
from matplotlib import pyplot as plt  # graph/graph rendering

# Third party library for console UI
from colorama import Fore, Style, init  # Colored console output 
init(autoreset=True) # initializes Colorama for Windows

# Import my utilities from same directory
from utilities.menu_banner_utilities import Banner, Menu  # banner/menu builders
from utilities.validation_utilities import ( # Input validation
    validate_prompt_string,  
    validate_prompt_yes_or_no,
)

# __________________________________________________________________________
# Global Constants / Variables
#

# Default dataset path
DEFAULT_DATA_PATH: Final[Path] = (
    Path(__file__).resolve().parent / "data" / "omega_sales_october.csv"
)  

# Main app banner
MAIN_BANNER: Final[Banner] = Banner(
    [
        ("Omega.py Online Store", "center", True),
        ("Monthly Sales Analysis", "center", False),
    ],
    inner_width=72,
)  

# Main app menu
MAIN_MENU: Final[Menu] = Menu(
    "MENU",
    (
        "Load sales CSV",
        "Show basic summary",
        "Show revenue by product",
        "Show revenue by category",
        "Show revenue by date",
        "Show revenue graph",
        "Quit",
    ),
    prefixes=("l", "s", "p", "c", "d", "g", "q"),
    inner_width=60,
)  

# __________________________________________________________________________
# Standalone Function Definitions
#

# =========================================================================
# Data Loading and Metric
# =========================================================================

# ------------------------------------------------------------------------- load_sales_data()
def load_sales_data(csv_path: Path | str) -> pd.DataFrame:
    """Load the Omega sales CSV dataset 

    Args:
        csv_path: File path 

    Returns:
        DataFrame the raw sales rows sorted by order date

    Raises:
        FileNotFoundError: If the provided path does not exist.
        ValueError: If the file cannot be parsed.
    """
    path = Path(csv_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found at {path}")

    try:
        dataframe = pd.read_csv(path, parse_dates=["order_date"])
    except pd.errors.ParserError as error:
        raise ValueError(f"Unable to parse CSV file: {error}") from error

    dataframe.sort_values(by="order_date", inplace=True)
    dataframe.reset_index(drop=True, inplace=True)
    return dataframe
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def sales_loaded(sales: pd.DataFrame | None) -> bool:
    """Check if a dataset is loaded and notify the user when absent.

    Args:
        sales: Possible DataFrame result from loading a CSV.

    Returns:
        True when sales data is present and non-empty; otherwise False.
    """
    if sales is None:
        print_warning("No sales data loaded. Please load a CSV first.")
        return False
    if sales.empty:
        print_warning("The loaded dataset is empty.")
        return False
    return True
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def compute_metrics(sales: pd.DataFrame) -> dict[str, float]:
    """Compute the core KPIs from the sales dataset.

    Args:
        sales: DataFrame containing the Omega.py sale data

    Returns:
        Dictionary with total orders, items_sold, revenue, and order-value statistics.

    Raises:
        ValueError: If the dataset is empty.
    """
    if sales.empty:
        raise ValueError("Cannot compute metrics for an empty dataset.")

    order_values = sales["order_total"].to_numpy(dtype=np.float64)
    return {
        "num_orders": float(len(sales)),
        "total_items_sold": float(sales["quantity"].sum()),
        "total_revenue": float(order_values.sum()),
        "min_order_total": float(np.min(order_values)),
        "max_order_total": float(np.max(order_values)),
        "mean_order_total": float(np.mean(order_values)),
        "median_order_total": float(np.median(order_values)),
    }
# -------------------------------------------------------------------------

# =========================================================================
# DataFrame grouping by column (Aggregation)
# =========================================================================

# -------------------------------------------------------------------------
def group_by_product(sales: pd.DataFrame) -> pd.DataFrame:
    """Sum/aggregation revenue and items_sold by product

    Args:
        sales: DataFrame sale data

    Returns:
        DataFrame sorted by revenue with per-product unit and revenue totals.
    """
    return (
        sales.groupby("product_name", as_index=False)
        .agg(items_sold=("quantity", "sum"), revenue=("order_total", "sum"))
        .sort_values(by="revenue", ascending=False)
    )
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def group_by_category(sales: pd.DataFrame) -> pd.DataFrame:
    """Sum/aggregation revenue and items_sold by product category

    Args:
        sales: DataFrame sale data

    Returns:
        DataFrame sorted by revenue with per-category unit and revenue totals.
    """
    return (
        sales.groupby("category", as_index=False)
        .agg(items_sold=("quantity", "sum"), revenue=("order_total", "sum"))
        .sort_values(by="revenue", ascending=False)
    )
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def group_by_date(sales: pd.DataFrame) -> pd.DataFrame:
    """Sum/aggregation daily revenue and items_sold

    Args:
        sales: DataFrame sale data

    Returns:
        DataFrame with chronological revenue, order count, and items_sold sold per day.
    """
    return (
        sales.groupby("order_date", as_index=False)
        .agg(
            revenue=("order_total", "sum"),
            orders=("order_id", "count"),
            items_sold=("quantity", "sum"),
        )
        .sort_values(by="order_date")
    )
# -------------------------------------------------------------------------

# =========================================================================
# UI Console format
# =========================================================================

# -------------------------------------------------------------------------
def render_banner(title: str) -> None:
    """Render a banner 

    Args:
        title: string to display in banner
    """
    print(
        Banner(
            [
                ("Omega.py Sales Analyzer", "center", True),
                (title, "center", False),
            ],
            inner_width=72,
        ).render(),
    )
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def format_currency(amount: float) -> str:
    """Return a currency formatted string

    Args:
        amount: Monetary value to present.

    Returns:
        Formatted currency string with two decimals.
    """
    return f"${amount:,.2f}"
# -------------------------------------------------------------------------

# =========================================================================
# UI display data metrics and analytics
# =========================================================================

# -------------------------------------------------------------------------
def display_metric(sales: pd.DataFrame) -> None:
    """Display banner and sales metrics

    Args:
        sales: DataFrame sales data metric
    """
    metrics = compute_metrics(sales)
    render_banner("Basic Sales Summary")
    print(f"Total orders : {int(metrics['num_orders'])}")
    print(f"Total items sold  : {int(metrics['total_items_sold'])}")
    print(f"Total revenue: {format_currency(metrics['total_revenue'])}")
    print("--- Order value statistics ---")
    print(f"Minimum: {format_currency(metrics['min_order_total'])}")
    print(f"Maximum: {format_currency(metrics['max_order_total'])}")
    print(f"Mean   : {format_currency(metrics['mean_order_total'])}")
    print(f"Median : {format_currency(metrics['median_order_total'])}")
    print()
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def display_best_product_revenues(sales: pd.DataFrame, limit: int = 5) -> None:
    """Print the top N best product revenue table.

    Args:
        sales: DataFrame sale data
        limit: Maximum number of product rows to display

    Example:
        >>> p - Show revenue by product 
        ╔═════════════════════════════╗
        ║   Omega.py Sales Analyzer   ║
        ╠═════════════════════════════╣
        ║  Top 5 Products by Revenue  ║
        ╚═════════════════════════════╝
        Omega Laptop 15"                    items sold:  24 | revenue: $28,799.76
        Omega Laptop 13"                    items sold:  13 | revenue: $11,699.87
        Omega 27" Monitor                   items sold:  20 | revenue: $4,999.80
        Omega External SSD 1TB              items sold:  15 | revenue: $1,949.85
        Omega Noise-Cancelling Headphones   items sold:   9 | revenue: $1,349.91
    """
    summary = group_by_product(sales)
    if summary.empty:
        print_warning("No product data to display.")
        return

    render_banner(f"Top {limit} Products by Revenue")
    for row in summary.head(limit).itertuples(index=False):
        print(
            f"{row.product_name:<35} "
            f"items sold: {int(row.items_sold):>3} | revenue: {format_currency(row.revenue)}",
        )
    print()
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def display_revenue_by_category(sales: pd.DataFrame) -> None:
    """Print revenue by category 

    Args:
        sales: DataFrame sale data

    Example:
        >>> c - Show revenue by category 
        ╔═══════════════════════════╗
        ║  Omega.py Sales Analyzer  ║
        ╠═══════════════════════════╣
        ║    Revenue by Category    ║
        ╚═══════════════════════════╝
        Laptops              items sold:  37 | revenue: $40,499.63
        Monitors             items sold:  20 | revenue: $4,999.80
        Storage              items sold:  15 | revenue: $1,949.85
        Accessories          items sold:  40 | revenue: $1,764.60
        Audio                items sold:   9 | revenue: $1,349.91
    """
    summary = group_by_category(sales)
    if summary.empty:
        print_warning("No category data to display.")
        return

    render_banner("Revenue by Category")
    for row in summary.itertuples(index=False):
        print(
            f"{row.category:<20} "
            f"items sold: {int(row.items_sold):>3} | revenue: {format_currency(row.revenue)}",
        )
    print()
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def display_daily_revenue(sales: pd.DataFrame) -> None:
    """Print day-by-day revenue 

    Args:
        sales: DataFrame sale data

    Example:
        >>> g - Show revenue graph 
        ╔═══════════════════════════╗
        ║  Omega.py Sales Analyzer  ║
        ╠═══════════════════════════╣
        ║      Revenue by Date      ║
        ╚═══════════════════════════╝
        2025-10-01 - orders:  1 | items sold:   2 | revenue: $2,399.98
        2025-10-03 - orders:  3 | items sold:   6 | revenue: $3,449.94
        2025-10-04 - orders:  1 | items sold:   4 | revenue: $4,799.96
        2025-10-05 - orders:  1 | items sold:   2 | revenue: $499.98
        ...
    """
    summary = group_by_date(sales)
    if summary.empty:
        print_warning("No daily totals to display.")
        return

    render_banner("Revenue by Date")
    for row in summary.itertuples(index=False):
        day = row.order_date.strftime("%Y-%m-%d")
        print(
            f"{day} - orders: {int(row.orders):>2} | "
            f"items sold: {int(row.items_sold):>3} | revenue: {format_currency(row.revenue)}",
        )
    print()
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def show_revenue_graph(sales: pd.DataFrame) -> None:
    """Render a matplotlib line graph for displaying daily revenues

    Args:
        sales: DataFrame sale data
    
    Example:
        >>> g - Show revenue graph 
        Displaying revenue by date graph. Close the window to return to the menu.
    """
    summary = group_by_date(sales)
    if summary.empty:
        print_warning("No daily totals available to graph.")
        return

    render_banner("Revenue graph")
    print_info("Displaying revenue by date graph. Close the window to return to the menu.")
    plt.figure(figsize=(10, 5))
    plt.plot(summary["order_date"], summary["revenue"], marker="o")
    plt.title("Omega.py Daily Revenue")
    plt.xlabel("Order Date")
    plt.ylabel("Revenue ($)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
# -------------------------------------------------------------------------

# =========================================================================
# UI messages (errors, info, success)
# =========================================================================

#--- Info messages ---

# -------------------------------------------------------------------------
def prompt_for_csv_path() -> Path:
    """Prompt the user to use a CSV file path

    Returns:
        path provided 
    """
    print_info(f"Sample data is available at: {DEFAULT_DATA_PATH}")
    csv_input = validate_prompt_string("Enter CSV file path:\n> ")
    return Path(csv_input).expanduser()
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def print_info(message: str) -> None:
    """Display an info message

    Args:
        info message
    """
    print(Fore.CYAN + message + Style.RESET_ALL)
# -------------------------------------------------------------------------

#--- Error and warning messages ---

# -------------------------------------------------------------------------
def print_error(message: str) -> None:
    """Display an error message

    Args:
        error message.
    """
    print(Fore.LIGHTRED_EX + message + Style.RESET_ALL)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def print_warning(message: str) -> None:
    """Display a warning message

    Args:
        warning message
    """
    print(Fore.YELLOW + message + Style.RESET_ALL)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def print_success(message: str) -> None:
    """Display a success message

    Args:
        success message
    """
    print(Fore.GREEN + message + Style.RESET_ALL)
# -------------------------------------------------------------------------

# =========================================================================
# Main app Loop
# =========================================================================

# -------------------------------------------------------------------------
def run_app() -> None:
    """Run the UI console loop, render main menu

    The loop waits for user selections from menu, 
    and displays info, error/warning, and success messages

    Exxample:
        ╔════════════════════════════════╗
        ║              MENU              ║
        ╠════════════════════════════════╣
        ║ l - Load sales CSV             ║
        ║ s - Show basic summary         ║
        ║ p - Show revenue by product    ║
        ║ c - Show revenue by category   ║
        ║ d - Show revenue by date       ║
        ║ g - Show revenue graph         ║
        ║ q - Quit                       ║
        ╚════════════════════════════════╝
    """
    print(MAIN_BANNER.render())
    sales: pd.DataFrame | None = None
    data_source: Path | None = None

    while True:
        print(MAIN_MENU.render())
        selection = input("Choose an option: ").strip().lower()

        if selection in {"l", "1"}:
            csv_path = prompt_for_csv_path()
            try:
                sales = load_sales_data(csv_path)
                data_source = csv_path
            except (FileNotFoundError, ValueError) as error:
                print_error(str(error))
                continue
            print_success(
                f"Loaded {len(sales)} orders from {data_source}",
            )
        elif selection in {"s", "2"}:
            if not sales_loaded(sales):
                continue
            display_metric(sales)
        elif selection in {"p", "3"}:
            if not sales_loaded(sales):
                continue
            display_best_product_revenues(sales)
        elif selection in {"c", "4"}:
            if not sales_loaded(sales):
                continue
            display_revenue_by_category(sales)
        elif selection in {"d", "5"}:
            if not sales_loaded(sales):
                continue
            display_daily_revenue(sales)
        elif selection in {"g", "6"}:
            if not sales_loaded(sales):
                continue
            show_revenue_graph(sales)
        elif selection in {"q", "7"}:
            if validate_prompt_yes_or_no("Are you sure you want to quit?"):
                print_info("Goodbye!")
                return
        else:
            print_warning("Invalid menu selection. Please choose a listed option.")
# -------------------------------------------------------------------------

# =========================================================================
# Entry Points
# =========================================================================
def main() -> None:
    """Script entrypoint."""
    run_app()
# __________________________________________________________________________
# Module Initialization / Main Execution Guard
#
if __name__ == "__main__":
    main()

# __________________________________________________________________________
# End of File
#
