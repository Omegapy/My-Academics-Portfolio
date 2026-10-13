#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Module Type: executable script
# Author: Alexander Ricciardi (Omega.py)
# Created: 2026-10-11
# -----------------------------------------------------------------------------
# Course: Foundations of Computer Vision CSC515
# Professor: Dr. Bingdong Li
# Term: Fall C (26FC) - 2026
# Assignment: Critical Thinking Module 4 - Option #2
#             Laplacian Filters for Different Kernel Windows
# -----------------------------------------------------------------------------
# The Program:
# Load the supplied photograph from org_images/Mod4CT2.jpg and convert it to
# grayscale. Use the same image to compare three filtering methods: Gaussian
# smoothing, the Laplacian, and Gaussian smoothing followed by the Laplacian.
# Repeat the comparison with 3 x 3, 5 x 5, and 7 x 7 windows, keeping one
# Gaussian sigma for all three sizes.
# Save the nine filtered images, their numerical arrays, a labeled 3 x 3
# comparison, a source reference, and a written explanation in mod_images/.
# The main results are saved before the five-stage teaching walkthrough begins.
# Each stage saves a matching figure before its terminal explanation. In an
# interactive run, the figure also opens, and earlier views remain available.
# Enter C to continue or Q to quit, then press Enter. The last view accepts Q
# only. Use --no-show to save all five teaching views without opening windows.
# The original photograph is not modified.
# -----------------------------------------------------------------------------
# Requirements:
# - Python 3.12; checked with Python 3.12.13.
# - Package pins: opencv-contrib-python==4.13.0.92, numpy==2.5.3,
#   and matplotlib==3.11.2. No extra packages are required by this script.
#
# Run from this folder:
#    python -m pip install -r requirements.txt
#    python Module4_CTA_Option2.py                  # Open the desktop teaching views.
#    python Module4_CTA_Option2.py --no-show        # Save and explain without a GUI.
#
# Dependencies:
# - cv2 (OpenCV), numpy, matplotlib, matplotlib.pyplot, matplotlib.figure,
#   matplotlib.axes, and matplotlib.backends.backend_agg.
# - argparse, hashlib, os, pathlib, queue, shutil, sys, textwrap, threading,
#   and typing from the Python standard library.
# - Pinned package versions are listed in requirements.txt.
#
# Contents Overview:
# - parse_arguments() / validate_gray_image()
#   - Validate run options and the floating-point grayscale representation.
# - load_image()
#   - Read the original BGR photograph and prepare a grayscale array.
# - laplacian_scale() / gaussian_kernel() / laplacian_kernel()
#   - Explain and construct the actual coefficients used by the filters.
# - apply_gaussian() / apply_laplacian() / create_results()
#   - Calculate the nine required results without changing the input.
# - derivative_display_limit() / show_filter_panel() / draw_source_reference()
#   - Keep image scales and color order consistent in saved and windowed figures.
# - draw_filter_comparison() / create_figures() / save_results()
#   - Export the required comparison, individual images, and numerical arrays.
# - build_walkthrough()
#   - Explain the calculations with real matrices, pixel values, and measurements.
# - style_text() / print_wrapped() / print_banner() / print_filter_guide_step()
#   - Present colored explanations, aligned matrices, and picture-reading guidance.
# - build_filter_guide_figure()
#   - Create the matching teaching view from already-calculated arrays.
# - wait_for_guide_command() / run_walkthrough()
#   - Keep Matplotlib responsive while the terminal waits for C or Q.
# - main()
#   - Coordinate validation, calculations, exports, and the walkthrough.
# -----------------------------------------------------------------------------

"""Compare Gaussian smoothing and Laplacian filtering on the supplied photograph.

OpenCV reads the color image, then converts it to a float64 grayscale array.
For each window size, the program smooths the original image, calculates its
Laplacian, and calculates the Laplacian of the smoothed image. All nine results
start with the same grayscale pixels and use the same border rule.

The Laplacian measures second-order changes in brightness. Its responses can be
positive or negative, and noise can produce strong responses along with real
boundaries. The saved PNGs show response magnitude for comparison, while the
numerical arrays retain the original signed values. The Laplacian is scaled to
compensate for differences in OpenCV's derivative coefficients between apertures.

Gaussian followed by Laplacian is two separate filtering operations, not one
analytically constructed Laplacian-of-Gaussian kernel. The program compares
possible boundaries visually. It does not threshold the responses, locate zero
crossings, or calculate edge-detection accuracy against a reference image.
"""

# ____________________________________________________________________________________
# ====================================================================================
# FILTERING COMPONENT MAP
#
# image_bgr  -> uint8 (H, W, 3), BGR color channels, intensities 0 to 255.
# gray_image -> float64 (H, W), one grayscale intensity per pixel, still 0 to 255.
# H and W are the original height and width. All nine results keep these dimensions.
# NumPy selects a pixel with [y, x], which means [row, column].

#                        +--> Gaussian(k, sigma) ------------------> Gaussian
# gray_image ------------+--> Laplacian(k, scale) -----------------> Laplacian
#                        +--> Gaussian(k, sigma) --> Laplacian(k) --> Combined

# Here, k is the square window size and sigma is the Gaussian spread in pixels.
# Gaussian: G * I, where G is the weight matrix and I is the grayscale image.
# Here, * means image convolution, not NumPy element-by-element multiplication.
# Laplacian: d2I/dx2 + d2I/dy2; combined: Laplacian(G * I).
# The Laplacian results are signed float64 arrays. The PNGs show their magnitudes,
# but filter_arrays.npz keeps the original signed values for inspection.
#
# WHERE THE WORK HAPPENS:
# apply_gaussian() and apply_laplacian() calculate filtered pixel values.
# create_results() applies those methods at all three kernel sizes.
# The display and export functions work with the calculated arrays afterward.
# build_walkthrough() prepares five explanations; run_walkthrough() presents them.
# The five teaching steps are views of the results, not five new filtering runs.
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

# The standard library handles command-line options, file paths, terminal text,
# and input while the teaching figures stay open. hashlib identifies the exact
# assignment image so image-specific measurements are not used for custom inputs.
import argparse # For command-line arguments
import hashlib # For hashing the image
import os # For file operations
from pathlib import Path # For file operations
import queue # For queue operations
import shutil # For file operations
import sys # For system operations
import textwrap # For text wrapping
import threading # For threading
from typing import TextIO # For type hinting

# OpenCV performs the image filtering. NumPy stores the pixel arrays and carries
# out matrix calculations. Matplotlib creates the comparisons and teaching views.
# FigureCanvasAgg saves the two main figures without opening desktop windows.
import cv2 # Computer Vision Library
import matplotlib # Plotting Library 
import matplotlib.pyplot as plt # Plotting Library
from matplotlib.axes import Axes # Used for creating plots
from matplotlib.backends.backend_agg import FigureCanvasAgg # Used for creating plots
from matplotlib.figure import Figure # Used for creating plots
import numpy as np # Numerical Library


# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

# The supplied image lives beside this script in org_images/. Paths based on __file__
# work even when Python is launched from another working directory. Derived files
# go to mod_images/; the original photograph is never an output destination.
ASSIGNMENT_DIRECTORY = Path(__file__).resolve().parent
INPUT_PATH = ASSIGNMENT_DIRECTORY / "org_images" / "Mod4CT2.jpg"
OUTPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "mod_images"
WALKTHROUGH_SUBDIRECTORY = Path("diagnostics") / "walkthrough"
# The sizes become the three comparison rows. FILTER_NAMES gives the column order
# and the dictionary keys used again for figures, filenames, and teaching examples.
KERNEL_SIZES: tuple[int, ...] = (3, 5, 7)
FILTER_NAMES: tuple[str, ...] = ("gaussian", "laplacian", "gaussian_laplacian")

# Sigma controls how quickly Gaussian weights decrease with distance from the
# center, measured in pixels. I use 1.0 for moderate smoothing of this noisy image.
# The same sigma is used with every kernel. A 3 x 3 window includes fewer outer
# weights than the 5 x 5 and 7 x 7 windows, even when sigma does not change.
GAUSSIAN_SIGMA: float = 1.0
# REFLECT_101 mirrors neighboring pixels at an image border without duplicating
# the border pixel. All three methods use the same rule for edge neighborhoods.
BORDER_TYPE: int = cv2.BORDER_REFLECT_101

# The six derivative pictures use one shared maximum and a square-root display
# mapping. Gamma 0.5 makes weaker response magnitudes easier to see without giving
# every panel its own scale. Only the display changes; signed arrays are retained.
# DPI controls the resolution of saved figures, not the filtering window or input.
DISPLAY_GAMMA: float = 0.5
FIGURE_DPI: int = 160
# ANSI codes color headings, calculations, saved-file messages, and prompts on
# a supported terminal. Redirected text is left plain by style_text().
TEXT_RESET: str = "\033[0m"
TEXT_STYLES: dict[str, str] = {
    "heading": "\033[1;96m",
    "rule": "\033[36m",
    "info": "\033[36m",
    "code": "\033[1;93m",
    "matrix": "\033[96m",
    "example": "\033[93m",
    "success": "\033[1;92m",
    "error": "\033[1;91m",
    "prompt": "\033[1;95m",
}
# The regular prompt advances the guide; the last stage has no next view and
# therefore accepts only Q. The prompt waits for Enter, not a single keypress.
NEXT_PROMPT: str = "Enter C to continue or Q to quit, then press Enter."
EXIT_PROMPT: str = "Enter Q to quit, then press Enter."

# The same order identifies terminal explanations, figure titles, and saved teaching views.
STAGE_TITLES: tuple[str, ...] = (
    "Load the photograph and identify the filtering input",
    "Gaussian filtering and the meaning of sigma",
    "Use the Laplacian to examine possible boundaries",
    "Smooth first, then apply the Laplacian",
    "Compare the results and check what was saved",
)

# This Git blob hash identifies the encoded bytes of the course-supplied image.
# Matching it enables the fixed background measurements and the conclusion written
# for that photograph. A different image is still filtered, but is not identified
# as the assignment image merely because it has the same dimensions.
SOURCE_GIT_BLOB: str = "d04fde764976613ae3381505848ac75cd8a48a01"

# results[kernel_size][filter_name] selects one calculated float64 (H, W) image.
FilterResults = dict[int, dict[str, np.ndarray]]

# A teaching stage holds (message, color style) pairs. The terminal uses both;
# the saved transcript uses only their text so it stays readable without color.
GuideStep = list[tuple[str, str]]


# __________________________________________
# INPUT AND PARAMETER VALIDATION
# ==========================================

# --- parse_arguments()
def parse_arguments() -> argparse.Namespace:
    """Read the input, output, Gaussian sigma, and display options from the terminal.

    Returns:
        The parsed paths, shared sigma, and switches for showing or pausing figures.

    Raises:
        SystemExit: If argparse finds an invalid option or sigma is not finite and positive.
    """
    # ArgumentParser reads the optional command-line settings. The defaults point
    # to this assignment's photograph and output folder. The formatter also shows
    # those defaults when the reader runs the script with --help.
    parser = argparse.ArgumentParser(
        description="Compare Gaussian and Laplacian filters in a labeled 3 x 3 figure.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # type=Path turns a filename into a Path object. A custom --image replaces
    # only the input for this run; it does not change INPUT_PATH.
    parser.add_argument("--image", type=Path, default=INPUT_PATH, help="Input image path.")
    # --output-dir selects where derived files are written, rather than overwriting
    # any file in org_images/.
    parser.add_argument(
        "--output-dir", type=Path, default=OUTPUT_DIRECTORY, help="Derived output folder.",
    )
    # A custom sigma changes all three Gaussian windows together. The comparison
    # must not use a different sigma for each kernel size.
    parser.add_argument(
        "--sigma", type=float, default=GAUSSIAN_SIGMA,
        help="Positive Gaussian sigma used for every kernel size in this run.",
    )
    # With --no-show, the guide still saves its PNG views and prints explanations,
    # but does not require a graphical desktop or terminal input.
    parser.add_argument("--no-show", action="store_true", help="Export without GUI windows.")
    # With --no-pause, the script opens the views without waiting for C/Q between
    # them; Matplotlib then waits for the reader to close the windows.
    parser.add_argument("--no-pause", action="store_true", help="Print without C/Q pauses.")
    args = parser.parse_args()
    # Error check: A Gaussian standard deviation must be positive and finite.
    # isfinite() rejects NaN and infinity; parser.error() reports the problem
    # before any image is loaded or processed.
    if not np.isfinite(args.sigma) or args.sigma <= 0:
        parser.error("--sigma must be a finite number greater than zero.")
    return args
# ---


# --- validate_gray_image()
def validate_gray_image(gray_image: np.ndarray) -> None:
    """Check the grayscale representation once before image filtering begins.

    Args:
        gray_image: Grayscale intensities with shape (height, width) and dtype float64.

    Raises:
        ValueError: If the image has no pixels, has extra dimensions, or is not float64.
    """
    # Error check: The filters share one two-dimensional grayscale image.
    # size rejects an empty array, and float64 is needed to retain fractional
    # Gaussian averages and the signed Laplacian values.
    if gray_image.ndim != 2 or gray_image.size == 0 or gray_image.dtype != np.float64:
        raise ValueError("Expected a nonempty, two-dimensional float64 grayscale image.")
# ---


# __________________________________________
# IMAGE LOADING AND GRAYSCALE CONVERSION
# ==========================================

# Read the source pixels once. These grayscale values are the common input for
# the Gaussian, Laplacian, and combined filtering methods.

# --- load_image()
def load_image(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Read a color photograph and prepare the grayscale input for all three filters.

    Args:
        path: The file containing the original photograph.

    Returns:
        The original uint8 BGR image with shape (H, W, 3) and a separate float64
        grayscale array with shape (H, W). Both use the original image size.

    Raises:
        FileNotFoundError: If the input path does not identify an existing file.
        ValueError: If OpenCV cannot decode the photograph.
    """
    # Error check: Stop with the original filename if the photograph is missing,
    # rather than allowing a failed read to reach an OpenCV filter.
    if not path.is_file():
        raise FileNotFoundError(f"Input image does not exist: {path}")
    # cv2.imread() decodes the photograph into a NumPy array in memory.
    # str(path) supplies the filename string expected by OpenCV; IMREAD_COLOR
    # requests three uint8 channels in blue, green, red (BGR) order. A color image
    # has shape (height, width, 3), with each channel ranging from 0 to 255.
    image_bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
    # Error check: OpenCV returns None when it cannot decode a usable image.
    # Do not attempt grayscale conversion on that result.
    if image_bgr is None:
        raise ValueError(f"OpenCV could not decode the image: {path}")
    # cv2.cvtColor() uses COLOR_BGR2GRAY to convert the three color values into one
    # brightness value at each pixel. The resulting 2D image keeps the same H and W.
    # astype(np.float64) makes a new double-precision array so filtering can retain
    # fractions and negative responses. It does not rescale intensities to 0 to 1.
    # This separate array leaves the BGR source and its original file unchanged.
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY).astype(np.float64)
    validate_gray_image(gray_image)
    return image_bgr, gray_image
# ---


# __________________________________________
# FILTER COEFFICIENTS AND TEACHING MATRICES
# ==========================================

# laplacian_scale() supplies the gain correction used by the real Laplacian.
# gaussian_kernel() and laplacian_kernel() construct matrices for the teaching
# explanation; neither function filters the source photograph.

# --- laplacian_scale()
def laplacian_scale(kernel_size: int) -> float:
    """Calculate the scale used to compare OpenCV Laplacians with different apertures.

    Args:
        kernel_size: The selected Sobel-based Laplacian aperture: 3, 5, or 7.

    Returns:
        A scale of 1/4, 1/64, or 1/1024 for the corresponding aperture.

    Related Equation:
        scale = 2 ** (4 - 2 * kernel_size)

    Equation Relationship:
        The scale compensates for the larger raw derivative coefficients used by
        wider apertures. It does not make the filters cover the same neighborhood.
    """
    # OpenCV's Sobel second-derivative coefficients grow with the aperture size.
    # Dividing by 2 ** (2*k - 4) adjusts their gain: 3 -> 1/4, 5 -> 1/64,
    # and 7 -> 1/1024. The larger windows still examine different neighborhoods.
    # The three permitted sizes are already defined in KERNEL_SIZES.
    # Reference: OpenCV getDerivKernels(), normalize parameter.
    # https://docs.opencv.org/4.13.0/d4/d86/group__imgproc__filter.html
    return 2.0 ** (4 - 2 * kernel_size)
# ---


# --- gaussian_kernel()
def gaussian_kernel(kernel_size: int, sigma: float) -> np.ndarray:
    """Build the Gaussian weight matrix used in the printed pixel calculation.

    Args:
        kernel_size: Width and height of the square Gaussian window, in pixels.
        sigma: Standard deviation of the Gaussian weights, in pixels.

    Returns:
        A float64 (kernel_size, kernel_size) array whose weights add up to one.

    Logic:
        Calculate one column of weights, then combine it with its transpose to
        obtain the two-dimensional Gaussian kernel used for the example.
    """
    # cv2.getGaussianKernel() produces one column of k Gaussian weights using
    # the given sigma. CV_64F asks OpenCV to store the weights as float64.
    # weights @ weights.T multiplies the column by its transpose, producing a
    # k-by-k matrix. Every position receives a weight, and the weights sum to 1.
    weights = cv2.getGaussianKernel(kernel_size, sigma, cv2.CV_64F)
    return weights @ weights.T
# ---


# --- laplacian_kernel()
def laplacian_kernel(kernel_size: int) -> np.ndarray:
    """Build the normalized Laplacian matrix shown in the terminal example.

    Args:
        kernel_size: OpenCV's Sobel derivative aperture, 3, 5, or 7.

    Returns:
        A float64 (kernel_size, kernel_size) matrix whose coefficients sum to zero.

    Related Equation:
        Laplacian = d2I/dx2 + d2I/dy2

    Equation Relationship:
        The matrix combines the second derivative in x and the second derivative
        in y. It uses the same scale as apply_laplacian() so the example matches
        the OpenCV filtering result.
    """
    # Use the same scale as cv2.Laplacian() so the printed matrix describes the
    # actual normalized operator applied to the image in the comparison.
    scale = laplacian_scale(kernel_size)
    # getDerivKernels(2, 0) gives second-derivative weights along x and smoothing
    # weights along y. normalize=False keeps the native coefficient values;
    # CV_64F stores them as float64 for this calculation.
    # ky @ kx.T forms the two-dimensional x-derivative matrix. Its transpose
    # gives the matching y-derivative matrix for a square, symmetric aperture.
    kx, ky = cv2.getDerivKernels(2, 0, kernel_size, normalize=False, ktype=cv2.CV_64F)
    dxx_kernel = ky @ kx.T
    # The Laplacian adds both second derivatives. Multiply by scale only after
    # adding them, just as apply_laplacian() requests from OpenCV.
    return (dxx_kernel + dxx_kernel.T) * scale
# ---


# __________________________________________
# GAUSSIAN FILTERING - IMAGE CALCULATION
# ==========================================

# This is where GaussianBlur() changes the grayscale pixel values.
# gaussian_kernel() above only constructs the weights shown in the explanation.

# --- apply_gaussian()
def apply_gaussian(gray_image: np.ndarray, kernel_size: int, sigma: float) -> np.ndarray:
    """Smooth a grayscale image with the requested Gaussian window and sigma.

    Args:
        gray_image: The unchanged float64 grayscale input, with shape (H, W).
        kernel_size: The width and height of the smoothing window: 3, 5, or 7.
        sigma: Gaussian standard deviation, in pixels, used along both axes.

    Returns:
        A separate float64 array with the original height and width.
    """
    # cv2.GaussianBlur() replaces each pixel intensity with a weighted average of
    # nearby intensities. Pixels near the center have more influence than those
    # farther away, which reduces small brightness fluctuations and some noise.
    # The tuple selects a square k-by-k window; sigmaX and sigmaY use the same
    # standard deviation so the horizontal and vertical weighting stays equal.
    # BORDER_REFLECT_101 extends the image at its boundary using reflected pixels
    # without repeating the outermost pixel. The returned array stays float64.
    return cv2.GaussianBlur(
        gray_image, (kernel_size, kernel_size), sigmaX=sigma, sigmaY=sigma,
        borderType=BORDER_TYPE,
    )
# ---


# __________________________________________
# LAPLACIAN FILTERING - IMAGE CALCULATION
# ==========================================

# This function calculates the signed derivative response of its input.
# create_results() passes either the original image or a Gaussian result.

# --- apply_laplacian()
def apply_laplacian(gray_image: np.ndarray, kernel_size: int) -> np.ndarray:
    """Calculate the signed Laplacian response of a grayscale image.

    The result measures how brightness changes vary across nearby pixels.
    A strong response can indicate an object boundary or a change caused by noise.

    Args:
        gray_image: Original or Gaussian-smoothed float64 grayscale pixels.
        kernel_size: The Sobel-based derivative aperture: 3, 5, or 7.

    Returns:
        A float64 (H, W) image containing both positive and negative responses.

    Related Equation:
        L = d2I/dx2 + d2I/dy2

    Equation Relationship:
        OpenCV calculates second derivatives in the horizontal and vertical
        directions and adds them. laplacian_scale() adjusts their coefficient gain.
    """
    # cv2.Laplacian() adds the estimated horizontal and vertical second derivatives.
    # ddepth=CV_64F keeps negative as well as positive responses; uint8 would clip
    # negative values and make the numerical comparison incomplete.
    # ksize selects the Sobel derivative aperture. scale compensates for the
    # aperture's coefficient gain, delta=0 adds no offset, and BORDER_TYPE uses
    # the same reflected-border rule as the Gaussian filter.
    # A strong response is a possible boundary, not a confirmed detected edge.
    return cv2.Laplacian(
        gray_image, ddepth=cv2.CV_64F, ksize=kernel_size,
        scale=laplacian_scale(kernel_size), delta=0, borderType=BORDER_TYPE,
    )
# ---


# __________________________________________
# FILTERING WORKFLOW - THREE METHODS
# ==========================================

# Run both OpenCV filters for each kernel size. The combined result is the
# Laplacian of the Gaussian output from that same comparison row.

# --- create_results()
def create_results(gray_image: np.ndarray, sigma: float) -> FilterResults:
    """Calculate the three filtering methods for each of the three kernel sizes.

    Args:
        gray_image: The common float64 grayscale image used in all nine calculations.
        sigma: One Gaussian standard deviation shared by every window size.

    Returns:
        A dictionary indexed first by kernel size and then by filter name.
        Each entry holds a separate float64 image with shape (H, W).

    Logic:
        For each size, calculate the Gaussian result, the direct Laplacian of the
        original image, and the Laplacian of that size's Gaussian result. Each row
        starts with the original image rather than the preceding row's result.
    """
    # Store all three methods under their shared kernel size. The dictionary
    # keys also determine which arrays the figures and saved PNGs display.
    results: FilterResults = {}
    # ASSIGNMENT REQUIREMENT: Compare all three filters for 3 x 3, 5 x 5, and 7 x 7.
    # MAIN ITERATION LOOP: Each pass produces one comparison row. Every row starts
    # with gray_image and uses the same sigma, not a blurred result from a prior row.
    for kernel_size in KERNEL_SIZES:
        # METHOD 1: Smooth the original grayscale image for this window size.
        gaussian_image = apply_gaussian(gray_image, kernel_size, sigma)
        # METHOD 2: Apply the Laplacian directly to the original pixels.
        # METHOD 3: Apply it to this row's Gaussian-smoothed pixels.
        # Keep all three arrays, including the intermediate Gaussian result.
        results[kernel_size] = {
            "gaussian": gaussian_image,
            "laplacian": apply_laplacian(gray_image, kernel_size),
            "gaussian_laplacian": apply_laplacian(gaussian_image, kernel_size),
        }
    return results
# ---


# __________________________________________
# DISPLAY SCALING AND IMAGE PANELS
# ==========================================

# These helpers set consistent image brightness for the comparison panels.
# They do not recalculate Gaussian or Laplacian filtering.

# --- derivative_display_limit()
def derivative_display_limit(results: FilterResults) -> float:
    """Find one magnitude limit for all six Laplacian display images.

    Args:
        results: The nine calculated arrays, grouped by kernel size and filter name.

    Returns:
        The largest absolute Laplacian or combined response. Return 1.0 when every
        response is zero so the display can divide by a nonzero number.
    """
    # Only the Laplacian and Gaussian-then-Laplacian columns contain signed
    # derivative responses. For each row and each of those two names, abs()
    # removes the sign for display, max() finds the strongest pixel magnitude,
    # and the outer max() finds one limit shared by all six result pictures.
    maximum = max(
        float(np.abs(row[name]).max())
        for row in results.values() for name in FILTER_NAMES[1:]
    )
    # If the image is constant, the Laplacian can be zero everywhere. A limit
    # of 1.0 avoids division by zero while those panels still appear black.
    return maximum if maximum > 0 else 1.0
# ---


# --- show_filter_panel()
def show_filter_panel(
    axis: Axes, result: np.ndarray, name: str, limit: float,
) -> None:
    """Display a calculated result without changing the stored image array.

    Args:
        axis: The Matplotlib panel where the image is displayed.
        result: A Gaussian intensity image or a signed derivative result.
        name: The filter name used to choose the display scale.
        limit: The same maximum magnitude used for all derivative panels.

    Logic:
        Show Gaussian intensity directly on the 0-to-255 grayscale range. Show
        derivative magnitude with the shared square-root scale, so negative values
        remain visible without altering the original signed arrays.
    """
    # Gaussian output contains regular pixel intensities. Show them in grayscale
    # from 0 (black) to 255 (white) without adjusting each panel individually.
    # interpolation="nearest" displays the calculated pixel grid without plot smoothing.
    if name == "gaussian":
        axis.imshow(result, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    else:
        # A Laplacian response may have either sign. abs() shows its magnitude so
        # both directions of brightness change are visible. Dividing by limit
        # gives all six derivative images the same scale. The exponent 0.5
        # brings out weaker responses, but does not change the saved signed arrays.
        display_image = (np.abs(result) / limit) ** DISPLAY_GAMMA
        axis.imshow(display_image, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
    # Pixel coordinates are not needed in this comparison. Hide the axis ticks
    # while leaving the figure's row and column labels visible.
    axis.set_xticks([])
    axis.set_yticks([])
# ---


# __________________________________________
# FIGURE LAYOUT - SOURCE AND COMPARISON
# ==========================================

# Draw the source view and the labeled 3 x 3 comparison using existing arrays.
# BGR-to-RGB conversion is for Matplotlib display, not for filtering.

# --- draw_source_reference()
def draw_source_reference(
    figure: Figure, image_bgr: np.ndarray, gray_image: np.ndarray,
) -> None:
    """Show the original color photograph beside the grayscale filtering input.

    Args:
        figure: The Matplotlib figure receiving the two panels.
        image_bgr: The unchanged source photograph in OpenCV's BGR order.
        gray_image: The float64 grayscale array used by the filters.
    """
    # Show the photograph beside the grayscale image actually sent to the filters.
    # A 1-by-2 layout makes it clear that the grayscale array is the common input.
    axes = figure.subplots(1, 2)
    figure.suptitle("Module 4, Option #2: source image and filtering input", fontsize=13)
    # OpenCV stores color as BGR, but Matplotlib displays RGB. COLOR_BGR2RGB
    # rearranges the channels for this panel only; it does not alter image_bgr.
    axes[0].imshow(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), interpolation="nearest")
    axes[0].set_title("Original photograph (RGB display)", fontsize=11)
    axes[1].imshow(gray_image, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    axes[1].set_title("Grayscale input (0 to 255)", fontsize=11)
    # The same loop removes coordinate ticks from both panels. The pictures keep
    # their original pixels and resolution; only plot markings are hidden.
    for axis in axes:
        axis.set_xticks([])
        axis.set_yticks([])
    # NumPy shape stores (height, width). State the source resolution below the
    # panels to make clear that conversion did not resize the photograph.
    height, width = gray_image.shape
    figure.supxlabel(f"Original resolution: {width} x {height} pixels; no resizing", fontsize=10)
# ---


# --- draw_filter_comparison()
def draw_filter_comparison(figure: Figure, results: FilterResults, sigma: float) -> None:
    """Draw the assignment's labeled 3-by-3 comparison of all nine filter results.

    Args:
        figure: The Matplotlib figure receiving the comparison grid.
        results: All nine images, grouped by window size and filter name.
        sigma: The Gaussian setting displayed with the figure.

    Logic:
        Each row uses a different kernel size. Each column uses one filtering
        method. Both derivative columns share their magnitude display scale.
    """
    # ASSIGNMENT REQUIREMENT: Three rows for window sizes and three columns for
    # the filter methods. Every panel reads an existing result array.
    axes = figure.subplots(3, 3)
    # Leave room for the comparison title, row labels, and notes below the images.
    figure.subplots_adjust(left=0.08, right=0.98, top=0.87, bottom=0.10,
                           wspace=0.06, hspace=0.12)
    # One limit makes the strength of a derivative response comparable between
    # different methods and window sizes rather than rescaling each image.
    limit = derivative_display_limit(results)
    column_titles = ("Gaussian", "Laplacian", "Gaussian then Laplacian")
    # OUTER LOOP: Each kernel size becomes a row, from 3 x 3 through 7 x 7.
    # enumerate() gives the row index for Matplotlib and the size for results.
    for row_index, kernel_size in enumerate(KERNEL_SIZES):
        # INNER LOOP: Each filter name selects one column within the current row.
        # The pair of indices locates the same array in the 3-by-3 subplot grid.
        for column_index, name in enumerate(FILTER_NAMES):
            axis = axes[row_index, column_index]
            show_filter_panel(axis, results[kernel_size][name], name, limit)
            # Label the columns once, across the top row, instead of in every panel.
            if row_index == 0:
                axis.set_title(column_titles[column_index], fontsize=12, pad=12)
            # Label each kernel size only in the leftmost panel of its row.
            if column_index == 0:
                axis.set_ylabel(f"{kernel_size} x {kernel_size}", fontsize=13, labelpad=12)
    # The title records the common sigma so the figure identifies this experiment.
    figure.suptitle(
        "Laplacian filters for different kernel windows\n"
        f"Same Gaussian sigma in every row: {sigma:g} px", fontsize=15, y=0.975,
    )
    # The note below the panels distinguishes actual grayscale intensities from
    # derivative magnitudes. A bright derivative pixel does not mean a bright
    # source pixel, and the scale adjustment does not create an edge map.
    figure.text(
        0.5, 0.045,
        "Gaussian: linear intensities 0-255. Derivatives: shared square-root display of |L|.\n"
        f"Normalized derivative gain; shared maximum {limit:.3f}. "
        "Combined column uses the row's window in both stages.",
        ha="center", va="center", fontsize=10,
    )
# ---


# --- create_figures()
def create_figures(
    image_bgr: np.ndarray, gray_image: np.ndarray, results: FilterResults, sigma: float,
) -> tuple[Figure, Figure]:
    """Prepare the two main figures for saving without opening desktop windows.

    Args:
        image_bgr: The original color photograph in BGR order.
        gray_image: The grayscale input used for image filtering.
        results: The nine already-calculated filtering arrays.
        sigma: The Gaussian setting displayed above the comparison.

    Returns:
        Two Matplotlib Figure objects: source reference, then 3-by-3 comparison.
    """
    # Construct the two saved figures with different layouts. Figure() does not
    # open the walkthrough's desktop windows; those are created later with pyplot.
    source_figure = Figure(figsize=(9, 4.2), layout="constrained")
    comparison_figure = Figure(figsize=(12, 9))
    # Attach a noninteractive Agg canvas to each figure so savefig() can render
    # it directly to PNG. The loop handles both figures in the same way.
    for figure in (source_figure, comparison_figure):
        FigureCanvasAgg(figure)
    # The drawing helpers only present the existing arrays; they do not filter again.
    draw_source_reference(source_figure, image_bgr, gray_image)
    draw_filter_comparison(comparison_figure, results, sigma)
    return source_figure, comparison_figure
# ---


# __________________________________________
# SAVE FILTER RESULTS - FILE EXPORT
# ==========================================

# Save the already-filtered images as viewable PNGs and the signed float64
# arrays as an NPZ file. The walkthrough text is also saved here.

# --- save_results()
def save_results(
    input_path: Path, output_directory: Path, gray_image: np.ndarray,
    results: FilterResults, figures: tuple[Figure, Figure], sigma: float,
    walkthrough: list[GuideStep],
) -> None:
    """Save the main figures, individual filter images, signed arrays, and explanation.

    The PNGs are meant for viewing. The NPZ file keeps the float64 results so
    positive and negative Laplacian responses are not lost during display scaling.

    Args:
        input_path: Path to the original photograph, which must not be overwritten.
        output_directory: Folder receiving the generated result files.
        gray_image: The float64 grayscale input retained in the NPZ file.
        results: Dictionary containing the nine filter results.
        figures: The source-reference and 3-by-3 comparison figures.
        sigma: The Gaussian setting saved with the arrays.
        walkthrough: Five explanation sections to write to a plain-text transcript.

    Raises:
        OSError: If an output folder or file cannot be created or written.
        ValueError: If a generated filename would replace the source photograph.

    Logic:
        Check the planned output filenames against the original image, save the
        figures and individual PNGs, and preserve the numerical arrays separately.
        Write all five explanations before the interactive walkthrough starts.
    """
    # Give the source reference and the labeled comparison their own filenames.
    # The list comprehension creates nine individual image names: for each kernel
    # size, include all three filter methods using the same name as results[k][name].
    figure_names = ("01_source_reference.png", "02_filter_comparison_3x3.png")
    image_names = [f"{name}_{k}x{k}.png" for k in KERNEL_SIZES for name in FILTER_NAMES]
    # Include the five teaching-view filenames in the source-protection check,
    # even though run_walkthrough() will save each view at its own stage.
    teaching_names = [str(WALKTHROUGH_SUBDIRECTORY / f"stage_{step:02d}.png")
                      for step in range(1, len(STAGE_TITLES) + 1)]
    names = [*figure_names, *image_names, "filter_arrays.npz", "terminal_output.txt",
             *teaching_names]
    # SAFETY CHECK: Inspect every planned output name before writing anything.
    # resolve() catches a matching path or symbolic link; samefile() also detects
    # an existing hard link that points to the photograph's file. The loop stops
    # the run if any derived file could replace the source image.
    for name in names:
        destination = output_directory / name
        if (destination.resolve() == input_path.resolve()
                or (destination.exists() and destination.samefile(input_path))):
            raise ValueError("A generated output would replace the original image.")
    # mkdir() creates the output folder. parents=True makes missing parent folders;
    # exist_ok=True permits repeated runs. The script replaces its named results
    # there and leaves the input in org_images/ unchanged.
    output_directory.mkdir(parents=True, exist_ok=True)
    # zip() pairs each prepared figure with its matching filename, first the
    # source reference and then the 3-by-3 comparison. savefig() includes titles,
    # labels, and notes. DPI changes only the PNG's rendering resolution.
    for figure, name in zip(figures, figure_names):
        figure.savefig(output_directory / name, dpi=FIGURE_DPI)

    # Use the same derivative-display limit that the Matplotlib panels use.
    # The NPZ stores both the numerical input/results and the values needed to
    # reproduce how the PNG display copies were scaled.
    limit = derivative_display_limit(results)
    arrays: dict[str, np.ndarray] = {
        "gray_input": gray_image,
        "sigma": np.array(sigma),
        "derivative_display_limit": np.array(limit),
        "display_gamma": np.array(DISPLAY_GAMMA),
    }
    # OUTER LOOP: results.items() visits each kernel size and its three arrays.
    # INNER LOOP: row.items() visits the Gaussian, Laplacian, and combined result.
    # Both loops preserve the original float64 images under names such as
    # "laplacian_5x5" while also making one separate 8-bit PNG per result.
    for kernel_size, row in results.items():
        for name, result in row.items():
            key = f"{name}_{kernel_size}x{kernel_size}"
            arrays[key] = result
            # Gaussian intensities already occupy the 0-to-255 range. Clip any
            # rounding effects, round to whole values, and convert to uint8 for PNG.
            if name == "gaussian":
                display_image = np.rint(np.clip(result, 0, 255)).astype(np.uint8)
            else:
                # A derivative can be negative. Show abs(result), scaled by the
                # common limit and raised to gamma 0.5 so weaker values remain
                # visible. Convert 0-to-1 display values into uint8 0-to-255.
                # The original signed result remains in arrays[key] above.
                mapped = (np.abs(result) / limit) ** DISPLAY_GAMMA
                display_image = np.rint(np.clip(mapped * 255, 0, 255)).astype(np.uint8)
            # cv2.imwrite() uses the .png extension to save lossless image pixels.
            # str() supplies the output filename. False means no image was written;
            # raising OSError prevents a false success message for that output.
            if not cv2.imwrite(str(output_directory / f"{key}.png"), display_image):
                raise OSError(f"Could not write {key}.png")
    # savez_compressed() writes a NumPy NPZ archive containing all float64
    # arrays and the display settings. This keeps signs and fractional values
    # that the viewable 8-bit PNG files cannot represent.
    np.savez_compressed(output_directory / "filter_arrays.npz", **arrays)
    # Build a readable transcript from the same explanation blocks shown in the
    # terminal. enumerate(..., 1) numbers stages from 1 rather than Python's 0.
    # Within each stage, the generator takes each message and discards its color
    # style, so the saved text contains neither ANSI codes nor plotting commands.
    transcript = []
    for step, blocks in enumerate(walkthrough, 1):
        title = f"STEP {step}/{len(STAGE_TITLES)}: {STAGE_TITLES[step - 1]}"
        body = "\n\n".join(message for message, _ in blocks)
        transcript.append(f"{title}\n{'=' * len(title)}\n{body}")
    # Join the five numbered explanations with blank lines. Writing them now
    # preserves the complete guide even if the reader later quits at stage 2.
    text = "\n\n".join(transcript)
    (output_directory / "terminal_output.txt").write_text(text + "\n", encoding="utf-8")
# ---


# __________________________________________
# TEACHING WALKTHROUGH - FIVE EXPLANATIONS
# ==========================================

# This section prepares what the student reads at Steps 1 through 5. It
# examines the existing arrays; GaussianBlur() and Laplacian() ran earlier.

# --- build_walkthrough()
def build_walkthrough(
    image_path: Path, image_bgr: np.ndarray, gray_image: np.ndarray,
    results: FilterResults, sigma: float, output_directory: Path,
) -> list[GuideStep]:
    """Build five teaching explanations using the calculated images and coefficients.

    Args:
        image_path: Path to the photograph used in this run.
        image_bgr: Original BGR pixels used for the first example.
        gray_image: Grayscale pixels used for the filter and neighborhood examples.
        results: The nine already-calculated filtering results.
        sigma: The shared Gaussian standard deviation in pixels.
        output_directory: Folder named in the final explanation.

    Returns:
        Five ordered sections. Each section holds (message, style) pairs used by
        the terminal. save_results() also writes their text without color codes.

    Logic:
        Explain the source and grayscale conversion, Gaussian weighting, the
        Laplacian, the combined method, and the final comparison. Use real pixel
        values and kernels from this run rather than invented demonstration numbers.
    """
    # Read the encoded bytes to identify whether the selected file is the exact
    # course image. The Git blob hash includes a "blob <size>" header and the
    # bytes, not just the visible pixels or the photograph's dimensions.
    source_bytes = image_path.read_bytes()
    source_blob = hashlib.sha1(
        b"blob " + str(len(source_bytes)).encode("ascii") + b"\0" + source_bytes,
    ).hexdigest()
    # Use image-specific background measurements and feature descriptions only
    # when the file matches the original assignment photograph.
    is_assignment_image = source_blob == SOURCE_GIT_BLOB
    # The guide reports actual values from this run, including the display limit.
    # Half the image height/width selects an interior example at [row=y, column=x].
    limit = derivative_display_limit(results)
    y, x = gray_image.shape[0] // 2, gray_image.shape[1] // 2
    # __________________________________________
    # TEACHING STEP 1 OF 5: SOURCE AND INPUT
    # ==========================================

    # A GuideStep contains (message, style) pairs. The first step introduces the
    # input photograph, BGR/grayscale representations, and why noise matters.
    # Later steps reuse the same format for calculations, code, and reading guides.
    steps: list[GuideStep] = [[
        ("This assignment compares Gaussian smoothing, Laplacian filtering, and both "
         "filters together. The goal is to see how the window size and smoothing "
         "affect the outlines and small details in the photograph.", "info"),
        (f"Input image: {image_path}", ""),
        ("The Laplacian responds to changes in brightness around image features. "
         "Small background fluctuations can also produce a response. The program "
         "compares the three methods using the same input so their effects can be "
         "examined side by side.", ""),
        ("OpenCV first reads the color photograph in BGR order (blue, green, red). "
         "It then converts those three values into one grayscale intensity per pixel. "
         "float64 keeps decimal values from smoothing and positive or negative "
         "Laplacian results. The original image size and 0-255 intensity scale remain.", ""),
        ("Code in load_image():", "heading"),
        ("    image_bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)\n"
         "    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY).astype(np.float64)",
         "code"),
        ("Image representations:", "heading"),
        (f"    image_bgr  -> {image_bgr.shape}, uint8, channels B G R\n"
         f"    gray_image -> {gray_image.shape}, float64, intensity 0..255\n"
         "    image_bgr[y, x] -> one BGR pixel -> gray_image[y, x]", "matrix"),
        (f"Example: At row {y}, column {x}, the color pixel contains "
         f"BGR {image_bgr[y, x].tolist()}. Its grayscale intensity is "
         f"{gray_image[y, x]:.1f}. Both values come from the image used in this run.",
         "example"),
        ("Reading the pictures:", "heading"),
        ("The left panel shows the original photograph. Its BGR values are displayed "
         "in RGB order because Matplotlib expects red, green, and blue. The right "
         "panel shows the grayscale image that all filters will use. Compare the "
         "background texture with the larger outlines in the picture.", ""),
        ("The original photograph is not replaced. The program saves the filtered "
         "results as separate files.", "info"),
    ]]
    # __________________________________________
    # TEACHING STEP 2 OF 5: GAUSSIAN BLUR
    # ==========================================

    # Stage 2 explains the weighted averaging before the reader examines the
    # three Gaussian figures. The printed matrices use this run's selected sigma.
    gaussian_blocks: GuideStep = [
        ("Gaussian smoothing calculates a new pixel intensity from a weighted average of nearby "
         "intensities. It can reduce small changes caused by noise, but it can also "
         "soften details and boundaries.", "info"),
        (f"This run uses sigma = {sigma:g}, measured in pixels, in both directions. "
         "The same sigma is used for the 3 x 3, 5 x 5, and 7 x 7 windows, as required "
         "by the assignment. Kernel size selects how many neighboring pixels enter "
         "the calculation. Sigma controls how much their influence decreases with "
         "distance from the center. All the weights add up to one.", ""),
        ("Code in apply_gaussian():", "heading"),
        ("    return cv2.GaussianBlur(\n"
         "        gray_image, (kernel_size, kernel_size), sigmaX=sigma, sigmaY=sigma,\n"
         "        borderType=BORDER_TYPE,\n"
         "    )", "code"),
        ("BORDER_TYPE is cv2.BORDER_REFLECT_101. When a filter window reaches the "
         "edge of the photograph, OpenCV reflects nearby pixels to complete that "
         "neighborhood. This avoids adding a black border during filtering. All "
         "three methods use the same setting.", ""),
        ("Gaussian weight matrices for the three window sizes:", "heading"),
        ("Each number is the weight assigned to one position in the window. "
         "The center receives more weight than distant pixels. Very small values "
         "may appear in scientific notation; for example, 2e-05 means 0.00002.", ""),
    ]
    # This loop constructs each actual Gaussian matrix, from 3 x 3 through 7 x 7.
    # array2string() keeps the rows aligned. indent() moves the entire matrix
    # away from the terminal margin while preserving its column positions.
    # The sum next to each matrix shows that the averaging weights total one.
    for k in KERNEL_SIZES:
        matrix = gaussian_kernel(k, sigma)
        gaussian_blocks.append((
            f"    {k} x {k}; weight sum = {matrix.sum():.6f}\n"
            + textwrap.indent(np.array2string(matrix, precision=4), "    "), "matrix",
        ))
    # A 3 x 3 neighborhood contains nine real intensity values around the chosen
    # pixel. Both images and kernel use [row, column] order, so elementwise
    # multiplication pairs each intensity with the weight at the same position.
    # For very small custom inputs, skip the example rather than slicing a partial
    # neighborhood. The supplied assignment image contains the complete patch.
    if min(gray_image.shape) >= 3:
        patch = gray_image[y - 1:y + 2, x - 1:x + 2]
        products = patch * gaussian_kernel(3, sigma)
        gaussian_blocks.extend([
            (f"Actual 3 x 3 neighborhood centered at [row={y}, column={x}]:", "heading"),
            (textwrap.indent(np.array2string(patch, precision=1), "    "), "matrix"),
            ("Multiply each of these nine pixel intensities by the Gaussian weight "
             "at the same position:", ""),
            (textwrap.indent(np.array2string(products, precision=3), "    "), "matrix"),
            (f"Example: Adding the nine products gives {products.sum():.6f}. This "
             f"is the new center-pixel intensity. GaussianBlur() gives "
             f"{results[3]['gaussian'][y, x]:.6f} at the same location.", "example"),
        ])
    # Finish Stage 2 with instructions for reading the three Gaussian pictures.
    # This text explains why a fixed sigma can give similar 5 x 5 and 7 x 7 views.
    gaussian_blocks.extend([
        ("Reading the pictures:", "heading"),
        ("From left to right, the panels show smoothing with 3 x 3, 5 x 5, and "
         "7 x 7 windows. Compare how much background texture becomes less noticeable "
         "and whether small features also become softer. With sigma held constant, "
         "the 5 x 5 and 7 x 7 results may look very similar because the additional "
         "outer weights contribute only a small amount.", ""),
        ("All three panels show grayscale intensities on the same 0-255 scale: "
         "0 is black and 255 is white. Gaussian smoothing does not calculate a "
         "Laplacian response; that is examined in the next step.", "info"),
    ])
    steps.append(gaussian_blocks)

    # __________________________________________
    # TEACHING STEP 3 OF 5: LAPLACIAN
    # ==========================================

    # Stage 3 prints the range of direct Laplacian responses for each aperture.
    # The loop reads the signed arrays, so minimum/maximum retain the distinction
    # between a negative and a positive change in local brightness curvature.
    range_lines = ["    Aperture     Scale          Signed minimum     Signed maximum"]
    for k in KERNEL_SIZES:
        lap = results[k]["laplacian"]
        range_lines.append(
            f"    {k} x {k}      {laplacian_scale(k):.9f}    {lap.min():>12.4f}"
            f"       {lap.max():>12.4f}",
        )
    # The next section connects the second-derivative equation to OpenCV's
    # Laplacian and to the 3 x 3 kernel that the program actually uses.
    laplacian_blocks: GuideStep = [
        ("The direct Laplacian examines brightness changes without Gaussian "
         "smoothing first. It makes many boundaries stand out, but it also responds "
         "to small changes in texture and noise.", "info"),
        ("A first derivative describes how brightness changes between nearby "
         "positions. A second derivative describes how that rate of change changes "
         "across the image. The Laplacian adds the horizontal and vertical second "
         "derivatives. Nearly uniform areas give values close to zero. Strong "
         "changes can give positive or negative responses, depending on the local "
         "brightness pattern.", ""),
        ("Code in apply_laplacian():", "heading"),
        ("    return cv2.Laplacian(\n"
         "        gray_image, ddepth=cv2.CV_64F, ksize=kernel_size,\n"
         "        scale=laplacian_scale(kernel_size), delta=0, borderType=BORDER_TYPE,\n"
         "    )", "code"),
        ("OpenCV calculates the Laplacian using second-derivative coefficients. "
         "The scale setting adjusts their numerical gain for each window size: "
         "1/4 for 3 x 3, 1/64 for 5 x 5, and 1/1024 for 7 x 7. A larger window "
         "still examines a different neighborhood. CV_64F keeps negative values "
         "instead of losing them in an 8-bit image; delta=0 adds no offset.", ""),
        ("Direct Laplacian results before converting them for display:", "heading"),
        ("\n".join(range_lines), "matrix"),
        ("The 3 x 3 Laplacian weight matrix used in this calculation:", "heading"),
        (textwrap.indent(np.array2string(laplacian_kernel(3), precision=3), "    "), "matrix"),
        ("The center has a negative weight and the diagonal neighbors have positive "
         "weights. These coefficients add up to zero. If every pixel in the "
         "neighborhood has the same brightness, their weighted sum is approximately "
         "zero. Different surrounding intensities can produce a signed response.", ""),
    ]
    # Use the same nine grayscale pixels as Stage 2. The Gaussian weights average
    # these values, whereas the Laplacian coefficients measure local curvature.
    # Elementwise products add to a signed number, which can be compared directly
    # with the value calculated by cv2.Laplacian() at the same pixel.
    # patch exists only when the image is large enough, so repeat that condition.
    if min(gray_image.shape) >= 3:
        laplacian_products = patch * laplacian_kernel(3)
        laplacian_blocks.extend([
            (f"Laplacian calculation at [row={y}, column={x}]:", "heading"),
            (textwrap.indent(np.array2string(laplacian_products, precision=3), "    "),
             "matrix"),
            (f"The program uses the same nine pixels from Step 2, but multiplies "
             f"them by the Laplacian coefficients instead of Gaussian weights. "
             f"The products sum to {laplacian_products.sum():.6f}; cv2.Laplacian() "
             f"returns {results[3]['laplacian'][y, x]:.6f}. The result keeps its "
             "positive or negative sign.", "example"),
        ])
    laplacian_blocks.extend([
        ("Reading the pictures:", "heading"),
        ("From left to right, these are the direct 3 x 3, 5 x 5, and 7 x 7 "
         "Laplacian results. Bright areas represent a stronger response, whether "
         "the original value was positive or negative. Compare the main outlines "
         "with the smaller bright marks in the background. Some of those marks may "
         "come from image noise rather than a useful feature.", ""),
        (f"The six Laplacian panels in Steps 3 and 4 use the same display scale, "
         f"based on maximum absolute response {limit:.6f}. The full signed values "
         "remain available in the saved numerical arrays.", "info"),
    ])
    steps.append(laplacian_blocks)

    # __________________________________________
    # TEACHING STEP 4 OF 5: COMBINED FILTER
    # ==========================================

    # Stage 4 explains the combined method: first use the Gaussian output from
    # a given window size, then calculate its Laplacian with that same size.
    # The associated figure shows both images without recalculating either.
    steps.append([
        ("This method applies Gaussian smoothing first, then calculates the "
         "Laplacian from that smoothed image. The purpose is to reduce small "
         "brightness fluctuations before examining possible boundaries.", "info"),
        ("The program starts each kernel size with the original grayscale image. "
         "For the combined result, it passes the Gaussian output directly to the "
         "Laplacian. Both operations use that row's 3 x 3, 5 x 5, or 7 x 7 window, "
         "and every Gaussian uses the same sigma.", ""),
        ("Code in create_results():", "heading"),
        ("    gaussian_image = apply_gaussian(gray_image, kernel_size, sigma)\n"
         "    results[kernel_size] = {\n"
         "        \"gaussian\": gaussian_image,\n"
         "        \"laplacian\": apply_laplacian(gray_image, kernel_size),\n"
         "        \"gaussian_laplacian\": apply_laplacian(gaussian_image, kernel_size),\n"
         "    }", "code"),
        ("How the two filtering operations are connected:", "heading"),
        ("    gray_image -> Gaussian(k, sigma) -> Laplacian(k) -> signed response\n"
         "    k = 3            3 x 3                3 x 3       support 5 x 5\n"
         "    k = 5            5 x 5                5 x 5       support 9 x 9\n"
         "    k = 7            7 x 7                7 x 7       support 13 x 13", "matrix"),
        ("In create_results(), the direct Laplacian uses gray_image, while the "
         "combined result uses gaussian_image. This is the difference being tested. "
         "For an interior pixel, the support sizes above show the total original-image "
         "neighborhood that can affect the final result after both operations. "
         "They do not mean "
         "that a separate 9 x 9 or 13 x 13 Laplacian was applied.", ""),
        ("Reading the pictures:", "heading"),
        ("Each column uses one window size. The upper image shows the Gaussian "
         "result, and the lower image shows the Laplacian calculated from it. "
         "Compare the lower images with the direct Laplacian pictures in Step 3. "
         "Look for less background clutter while checking whether the main outlines "
         "and smaller details remain visible.", ""),
        ("The upper images show grayscale brightness. The lower images show the "
         "strength of the Laplacian response, so a bright area has a different "
         "meaning in each row.", "info"),
    ])

    # __________________________________________
    # TEACHING STEP 5 OF 5: COMPARE RESULTS
    # ==========================================

    # Stage 5 compares the entire nine-panel figure. The mean absolute difference
    # between the 5 x 5 and 7 x 7 Gaussian results reports how far their pixel
    # intensities differ on average. It is not an edge-detection accuracy score.
    difference = float(np.mean(np.abs(results[5]["gaussian"] - results[7]["gaussian"])))
    comparison_blocks: GuideStep = [
        ("The final 3 x 3 figure contains the nine filtering results required by "
         "the assignment. It brings the three methods and three window sizes "
         "together for a direct visual comparison.", "info"),
        ("Each row uses one window size: 3 x 3, 5 x 5, or 7 x 7. Each column "
         "shows Gaussian, direct Laplacian, or Gaussian followed by Laplacian. "
         "Read across to compare the methods, then down to compare window sizes "
         "while the Gaussian sigma stays fixed.", ""),
        ("How the Laplacian responses are displayed in grayscale:", "heading"),
        ("    display = (abs(response) / shared_maximum) ** 0.5", "code"),
        (f"The six Laplacian views share a maximum absolute response of "
         f"{limit:.6f}. abs() lets positive and negative responses appear as "
         "brightness; the square root makes weaker responses easier to see. "
         "The same response strength therefore looks equally bright in every "
         "Laplacian panel. This changes the display only. Gaussian panels still "
         "use the regular 0-255 grayscale intensity scale.", ""),
        (f"Example: The average absolute pixel difference between the 5 x 5 and "
         f"7 x 7 Gaussian results is {difference:.6f} intensity levels. A smaller "
         "number means the two smoothed images are more alike at corresponding "
         "pixel positions.", "example"),
    ]
    # Only the exact assignment image uses this fixed background patch. Its
    # row/column slices were selected from that photograph and may not describe
    # the background of a custom input. For each aperture, compare the direct
    # and smoothed-then-Laplacian response in the same rectangle. RMS means
    # root mean square; it measures average response strength, not edge accuracy.
    if is_assignment_image:
        rms_lines = ["    Aperture      Laplacian RMS      Gaussian + Laplacian RMS"]
        for k in KERNEL_SIZES:
            lap = results[k]["laplacian"][20:140, 195:235]
            combined = results[k]["gaussian_laplacian"][20:140, 195:235]
            rms_lines.append(
                f"    {k} x {k}           {np.sqrt(np.mean(lap**2)):>9.4f}"
                f"                    {np.sqrt(np.mean(combined**2)):>9.4f}",
            )
        comparison_blocks.extend([
            ("For the supplied photograph, the program measures a small area in "
             "the right background, using rows 20:140 and columns 195:235. "
             "RMS (root mean square) summarizes the strength of the Laplacian values: "
             "square them, average them, and take the square root. Compare the "
             "direct and combined columns to see how smoothing changes the response "
             "in that area. The selected area contains shading as well as noise.", ""),
            ("Background response measurements:", "heading"),
            ("\n".join(rms_lines), "matrix"),
        ])
    # The visual preference written for this experiment belongs to the exact
    # photograph with sigma 1.0. For a different image or sigma, the guide asks
    # the reader to inspect the new results instead of claiming the same winner.
    comparison_blocks.append(("Reading the pictures:", "heading"))
    if is_assignment_image and sigma == GAUSSIAN_SIGMA:
        comparison_blocks.append((
            "For the supplied photograph, I prefer Gaussian followed by Laplacian "
            "using a 5 x 5 window and sigma 1.0. The direct 3 x 3 result contains "
            "more small background responses. Smoothing first reduces some of "
            "those responses while keeping the hair outline, shirt collar, and "
            "crossed arms recognizable. The 7 x 7 result can soften narrower "
            "details, including parts of the hair and face. Those features matter "
            "because they help describe the subject's shape.", "",
        ))
    else:
        comparison_blocks.append((
            "For this image, compare the direct Laplacian with the version that "
            "uses Gaussian smoothing first. Look at the main outlines, the small "
            "features, and the amount of background clutter. The best-looking "
            "window may differ when the image or sigma is changed.", "",
        ))
    comparison_blocks.extend([
        ("Gaussian smoothing reduces small intensity variations but also softens "
         "details. The direct Laplacian makes changes stand out, including noise. "
         "For a noisy photograph, Gaussian followed by Laplacian can give "
         "a useful balance: fewer background responses while keeping the larger "
         "outlines visible. The amount of smoothing still affects fine detail.", ""),
        (f"Output folder: {output_directory}\n"
         "The program saves the original/grayscale reference, the labeled 3 x 3 "
         "comparison, and nine individual filtered PNGs. filter_arrays.npz holds "
         "the original signed filter values, and terminal_output.txt contains "
         "a copy of these five explanations.", "success"),
    ])
    # The five sections now use one shared (text, style) structure. Nothing has
    # been printed or redrawn here; that happens after save_results() is complete.
    steps.append(comparison_blocks)
    return steps
# ---


# __________________________________________
# TERMINAL EXPLANATIONS - TEXT DISPLAY
# ==========================================

# These functions format and print teaching text. They do not alter pixels.

# --- style_text()
def style_text(message: str, style: str = "", *, stream: TextIO | None = None) -> str:
    """Add terminal color only when the selected output supports it.

    Args:
        message: Text to print, without changes to its words.
        style: Name of a color style; an empty value leaves text unchanged.
        stream: Destination used to check terminal support; defaults to stdout.

    Returns:
        Colored text when available, otherwise the original plain text.
    """
    # Most messages go to stdout; errors can select stderr instead. isatty()
    # checks whether that particular destination is a terminal, not a file.
    output = sys.stdout if stream is None else stream
    # Leave redirected output plain. NO_COLOR and TERM="dumb" also turn colors off.
    # An empty message or style has nothing to color. This avoids putting ANSI
    # escape sequences into logs while retaining accents in an interactive terminal.
    if (not message or not style or not output.isatty() or os.environ.get("NO_COLOR")
            or os.environ.get("TERM", "").lower() == "dumb"):
        return message
    # A recognized style puts a color code before the text and TEXT_RESET after
    # it. An unknown style leaves the original message alone.
    code = TEXT_STYLES.get(style, "")
    return f"{code}{message}{TEXT_RESET}" if code else message
# ---


# --- print_wrapped()
def print_wrapped(message: str, style: str = "", *, stream: TextIO | None = None) -> None:
    """Wrap explanation paragraphs without breaking the alignment of code and matrices.

    Args:
        message: The text to print, including intentional newlines.
        style: Optional color style used after wrapping.
        stream: Output destination; defaults to standard output.
    """
    output = sys.stdout if stream is None else stream
    # Leave two columns of margin and cap the text at 100 characters. max(1, ...)
    # keeps the line width valid even if the terminal reports a very small size.
    width = max(1, min(100, shutil.get_terminal_size().columns - 2))
    lines = []
    # Process each intentionally separated line. Code and NumPy matrices start
    # with four spaces, so keep those lines exactly aligned rather than wrapping
    # through their matrix columns. Wrap ordinary prose at word boundaries only.
    for line in message.split("\n"):
        if line.startswith("    "):
            lines.append(line)
        else:
            lines.append(textwrap.fill(line, width, break_long_words=False,
                                       break_on_hyphens=False))
    # Add color only after line wrapping. ANSI escape codes should not count as
    # printable characters; flush=True prints the text before the next prompt.
    print(style_text("\n".join(lines), style, stream=output), file=output, flush=True)
# ---


# --- print_banner()
def print_banner(title: str) -> None:
    """Print a visible program or stage heading without clearing earlier explanations.

    Args:
        title: The program name or current teaching-stage heading.
    """
    # Use the current terminal width for the separator rules. Earlier messages
    # remain visible, so the student can scroll back to another stage's example.
    width = max(1, min(100, shutil.get_terminal_size().columns - 2))
    print("\n" + style_text("=" * width, "rule"))
    print_wrapped(title, style="heading")
    print(style_text("=" * width, "rule"), flush=True)
# ---


# --- print_filter_guide_step()
def print_filter_guide_step(step: int, blocks: GuideStep, teaching_path: Path) -> None:
    """Print the explanation for a teaching figure that has already been saved.

    Args:
        step: Teaching-stage number, from 1 to 5.
        blocks: Messages and their presentation styles for this stage.
        teaching_path: File path of the figure saved before this explanation.
    """
    print_banner(f"STEP {step}/{len(STAGE_TITLES)}: {STAGE_TITLES[step - 1]}")
    # Each pair contains the explanation and its display style. The loop prints
    # them in the order prepared by build_walkthrough(), leaving blank lines
    # between ideas. Code and matrices keep their alignment through print_wrapped().
    for message, style in blocks:
        print_wrapped(message, style=style)
        print()
    # The figure was saved before this function was called. Print its path so
    # the student can reopen the exact picture described by this stage.
    print_wrapped(f"Saved teaching view: {teaching_path}", style="success")
    print(flush=True)
# ---


# __________________________________________
# TEACHING FIGURES - DISPLAY ONLY
# ==========================================

# Select panels for each numbered teaching step from the stored filter results.
# Drawing a figure does not apply a filter or modify the original photograph.

# --- build_filter_guide_figure()
def build_filter_guide_figure(
    step: int, image_bgr: np.ndarray, gray_image: np.ndarray,
    results: FilterResults, sigma: float,
) -> Figure:
    """Create a teaching figure for one stage from the existing filter arrays.

    Args:
        step: Stage number. 1 shows the source; 2 Gaussian; 3 Laplacian;
            4 Gaussian above combined responses; and 5 the full comparison.
        image_bgr: The original BGR photograph used in stage 1.
        gray_image: The grayscale input used in stage 1.
        results: The nine filtering results used by stages 2 through 5.
        sigma: Gaussian setting displayed with each applicable comparison.

    Returns:
        A Matplotlib figure ready to save and show. No filter is recalculated.
    """
    # The final 3-by-3 comparison needs more height. Stage 4 has two image
    # rows, while the source, Gaussian, and Laplacian stages use shorter figures.
    # figsize is in inches; it does not resize any of the image arrays.
    size = (12, 9) if step == 5 else ((12, 7.4) if step == 4 else (12, 5.2))
    # pyplot manages these stage figures as open desktop windows when available.
    # The larger final grid uses manual spacing from draw_filter_comparison().
    figure = plt.figure(figsize=size, layout=None if step == 5 else "constrained")
    figure.canvas.manager.set_window_title(f"CSC515 Module 4 - Step {step}/5")
    limit = derivative_display_limit(results)
    # DISPLAY STEP 1: Original photograph and grayscale input.
    # DISPLAY STEP 2: Gaussian images at all three kernel sizes.
    # DISPLAY STEP 3: Direct Laplacian responses at all three sizes.
    # DISPLAY STEP 4: Gaussian above its Laplacian response for each size.
    # DISPLAY STEP 5: All nine results in the assignment's 3 x 3 comparison.
    # The branches below only choose panels; filtering was done in create_results().
    if step == 1:
        draw_source_reference(figure, image_bgr, gray_image)
    elif step == 5:
        draw_filter_comparison(figure, results, sigma)
    else:
        # Stage 2 shows Gaussian alone; Stage 3 shows the direct Laplacian.
        # Stage 4 places the Gaussian image above the Laplacian of that image,
        # so each column compares the two stages of the combined method.
        names = (("gaussian", "gaussian_laplacian") if step == 4
                 else (("gaussian",) if step == 2 else ("laplacian",)))
        # squeeze=False keeps axes in a 2D row/column array even if a stage
        # uses just one row. Each column always corresponds to one kernel size.
        axes = figure.subplots(len(names), 3, squeeze=False)
        # OUTER LOOP: Select the method for this image row.
        # INNER LOOP: Display its 3 x 3, 5 x 5, and 7 x 7 results in order.
        for row, name in enumerate(names):
            for column, k in enumerate(KERNEL_SIZES):
                axis = axes[row, column]
                show_filter_panel(axis, results[k][name], name, limit)
                # Place the kernel label at the top of each column only once.
                if row == 0:
                    axis.set_title(f"{k} x {k}", fontsize=12)
                # The left panel of each row identifies which method is shown.
                if column == 0:
                    label = {"gaussian": "Gaussian", "laplacian": "Laplacian",
                             "gaussian_laplacian": "Gaussian then Laplacian"}[name]
                    axis.set_ylabel(label, fontsize=11)
        # This note separates the original intensity scale from the magnitude
        # mapping applied to derivative views. Neither changes the filter arrays.
        figure.supxlabel(
            f"Sigma: {sigma:g} px. Gaussian: intensities 0-255. "
            f"Derivatives: shared sqrt(|L| / {limit:.3f}).", fontsize=10,
        )
    # Use the same stage title here and in the terminal. The last stage also
    # prints sigma with the grid because all three Gaussian rows share it.
    heading = f"STEP {step}/{len(STAGE_TITLES)}: {STAGE_TITLES[step - 1]}"
    if step == 5:
        heading += f"\nSame Gaussian sigma in every row: {sigma:g} px"
    figure.suptitle(heading, fontsize=14)
    return figure
# ---


# __________________________________________
# TEACHING CONTROLS - WINDOWS AND INPUT
# ==========================================

# --- wait_for_guide_command()
def wait_for_guide_command(final_step: bool = False) -> str:
    """Wait for a terminal command while Matplotlib continues updating the windows.

    Args:
        final_step: True when the final view is open and only Q may finish the guide.

    Returns:
        Lowercase "c" to advance or "q" to finish. End of input is treated as Q.

    Logic:
        A reader thread waits for one line of text and puts it in a queue. The main
        thread keeps the image windows responsive and checks the returned command.
        Invalid letters prompt again without advancing to the next stage.
    """
    # The input reader and Matplotlib run on different threads:
    #
    #     terminal -> read_command() -> replies.put()
    #                                      |
    #     figure updates <- plt.pause() <- replies.get() -> C or Q
    #
    # Queue passes the command to the main thread. No image calculations are
    # performed here, and the worker thread never touches Matplotlib figures.
    replies: queue.Queue[str] = queue.Queue()
    prompt = EXIT_PROMPT if final_step else NEXT_PROMPT

    # --- read_command()
    def read_command() -> None:
        """Read one terminal line and send its lowercase command to the waiting main thread.

        An ended input stream or an OSError becomes Q. This worker does not draw or
        close Matplotlib windows.
        """
        try:
            # readline() waits for a complete line, including Enter. strip()
            # removes surrounding whitespace and lower() accepts either c/q or C/Q.
            # Reading in a worker avoids entering the macOS GUI event loop from
            # input(); all Matplotlib calls remain on the main thread.
            line = sys.stdin.readline()
            command = line.strip().lower() if line else "q"
        except OSError:
            # An input failure is handled like Q: the main program will finish
            # with any completed filter results still saved on disk.
            command = "q"
        # The queue receives only the command. This reader does not decide
        # whether C is valid at the last stage; the main prompt loop does that.
        replies.put(command)
    # ---

    # VALIDATION LOOP: Continue asking until the command is allowed at this stage.
    # Invalid or empty submissions display the choices again without advancing.
    while True:
        print_wrapped(prompt, style="prompt")
        # A daemon thread can wait for terminal input without preventing Python
        # from exiting on cancellation. Normal C/Q operation consumes its answer
        # before a new reader is started on another prompt.
        threading.Thread(target=read_command, daemon=True).start()
        # While the reader waits, pause() processes Matplotlib window events.
        # The short wait keeps the pictures responsive without a busy loop.
        while replies.empty():
            plt.pause(0.1)
        command = replies.get()
        # Q is always allowed. C advances only before the final teaching view;
        # that last view stays available until Q is entered.
        if command == "q" or (command == "c" and not final_step):
            return command
        print_wrapped("Please use one of the choices shown above.", style="info")
# ---


# --- run_walkthrough()
def run_walkthrough(
    sections: list[GuideStep], image_bgr: np.ndarray, gray_image: np.ndarray,
    results: FilterResults, sigma: float, output_directory: Path,
    *, show: bool, pause: bool,
) -> int:
    """Save and present the five teaching views in the same order as their explanations.

    Args:
        sections: The five sets of prepared terminal messages.
        image_bgr: Original BGR image used in the reference view.
        gray_image: Grayscale image used for the reference view.
        results: The nine calculated filter results, reused without recalculation.
        sigma: Gaussian setting shown with the relevant views.
        output_directory: Folder receiving the teaching-view PNG files.
        show: Whether Matplotlib should open desktop windows.
        pause: Whether the terminal should ask for C or Q after each view.

    Returns:
        The number of stages presented. Q stops future stages; a headless run
        saves all five views and prints their explanations without waiting.

    Logic:
        Build one figure, save it, display it if requested, and print its matching
        explanation. Leave earlier windows open for comparison and close them on exit.
    """
    # Teaching PNGs are separate from the nine individual filter results.
    # mkdir() permits the folder to exist from an earlier run.
    teaching_directory = output_directory / WALKTHROUGH_SUBDIRECTORY
    teaching_directory.mkdir(parents=True, exist_ok=True)
    presented = 0
    # figure.raise_window=False prevents repeated window updates from taking
    # focus away from the terminal. rc_context() restores that setting afterward.
    with plt.rc_context({"figure.raise_window": False}):
        try:
            # MAIN ITERATION LOOP: Each stage has one figure and one matching
            # explanation. enumerate(..., 1) gives the displayed stage number.
            # Pressing C advances through these prepared results; no filter reruns.
            for step, blocks in enumerate(sections, 1):
                action = "Opening" if show else "Saving"
                print_wrapped(f"{action} step {step}/{len(STAGE_TITLES)}...", style="info")
                # Build from existing arrays and save the PNG before showing or
                # describing it. :02d makes filenames stage_01.png, stage_02.png, etc.
                figure = build_filter_guide_figure(step, image_bgr, gray_image, results, sigma)
                teaching_path = teaching_directory / f"stage_{step:02d}.png"
                figure.savefig(teaching_path, dpi=FIGURE_DPI)
                if show:
                    # block=False opens this window while letting the terminal
                    # continue to the explanation and C/Q prompt. Earlier figures
                    # remain open, and pause() allows time to draw the new view.
                    plt.show(block=False)
                    plt.pause(0.1)
                print_filter_guide_step(step, blocks, teaching_path)
                presented = step
                if show and pause:
                    # On the final view, only Q is accepted. Q at an earlier stage
                    # leaves later views unpresented, but the main results are saved.
                    if wait_for_guide_command(final_step=step == len(STAGE_TITLES)) == "q":
                        break
                if not show:
                    # Headless mode saves every view, prints its explanation, and
                    # closes that figure immediately to avoid collecting open plots.
                    plt.close(figure)
            if show and not pause:
                # In --no-pause mode, keep the opened figures visible until the
                # student closes the windows rather than asking for C or Q.
                print_wrapped("Close the Matplotlib windows to finish.", style="prompt")
                plt.show(block=True)
        finally:
            # CLEANUP: Close any remaining teaching windows after Q, Ctrl+C,
            # a failure, or normal window closure. The saved PNGs are not removed.
            plt.close("all")
    return presented
# ---


# __________________________________________
# MAIN FUNCTION - ENTRY POINT
# ==========================================

# --- main()
def main() -> int:
    """Calculate and save the filtering comparison, then present the teaching guide.

    Returns:
        0 after completion or Q, 1 for an input or output failure, and 130 on Ctrl+C.

    Logic:
        Read options and the image, calculate all nine filters once, and save the
        main results before presenting any teaching stage. Display controls change
        how the views are presented, not the filtering calculations. If the reader
        quits early, the already-saved main results remain available.
    """
    # Parse the options before starting. outputs_saved becomes True only after
    # the source reference, comparison, nine PNGs, NPZ, and transcript are saved.
    # It lets error messages distinguish saved work from an incomplete run.
    args = parse_arguments()
    outputs_saved = False
    # expanduser() interprets a leading ~, and resolve() makes the selected
    # result folder an absolute path for the saved-file messages.
    output_directory = args.output_dir.expanduser().resolve()
    print_banner("CSC515 - Critical Thinking Module 4\n"
                 "Option #2: Laplacian Filters for Different Kernel Windows")
    print_wrapped("The program compares Gaussian smoothing, the direct Laplacian, "
                  "and Gaussian followed by Laplacian on the same grayscale image. "
                  "It uses 3 x 3, 5 x 5, and 7 x 7 windows with one Gaussian sigma.",
                  style="info")
    try:
        # __________________________________________
        # LOAD THE ORIGINAL IMAGE
        # ==========================================
        # --no-show selects a noninteractive Matplotlib backend so the program
        # can render files without a desktop display. It does not change filters.
        if args.no_show:
            plt.switch_backend("Agg")
        input_path = args.image.expanduser().resolve()
        # Load once, then pass the shared float64 grayscale input to all filters.
        image_bgr, gray_image = load_image(input_path)
        print_wrapped("\nCalculating all nine results from the same grayscale input...",
                      style="info")
        # __________________________________________
        # CALCULATE THE NINE FILTER RESULTS
        # ==========================================

        # All nine results are calculated here, before any figure is opened.
        results = create_results(gray_image, args.sigma)

        # __________________________________________
        # PREPARE FIGURES AND EXPLANATIONS
        # ==========================================
        # Prepare the source and comparison figures for file export, then build
        # the explanations using the same calculated pixel values and kernels.
        figures = create_figures(image_bgr, gray_image, results, args.sigma)
        sections = build_walkthrough(
            input_path, image_bgr, gray_image, results, args.sigma, output_directory,
        )
        # __________________________________________
        # SAVE THE MAIN RESULTS
        # ==========================================

        # Save the main outputs and all five text explanations before displaying
        # a teaching stage. Quitting the guide cannot discard these files.
        save_results(input_path, output_directory, gray_image, results, figures,
                     args.sigma, sections)
        outputs_saved = True
        print_wrapped(f"All nine results saved to: {output_directory}\n"
                      "The source reference, required comparison, arrays, and full explanation "
                      "are saved before the walkthrough starts.", style="success")

        # __________________________________________
        # PRESENT THE FIVE TEACHING STEPS
        # ==========================================
        # Some Matplotlib backends save images but cannot open desktop windows.
        # If --no-show was selected, or a noninteractive backend is active, save
        # teaching views without attempting to open windows.
        backend = str(matplotlib.get_backend()).lower()
        show = not args.no_show and backend not in {"agg", "pdf", "ps", "svg", "cairo", "pgf"}
        if not args.no_show and not show:
            print_wrapped("No interactive Matplotlib backend is active. "
                          "The walkthrough will save its views without opening windows.",
                          style="info")
        # Ask for C/Q only with visible windows and an interactive terminal.
        # A redirected input stream or --no-pause does not use the command prompt.
        pause = show and not args.no_pause and sys.stdin.isatty()
        presented = run_walkthrough(sections, image_bgr, gray_image, results, args.sigma,
                                    output_directory, show=show, pause=pause)
        # The returned stage count distinguishes an early Q from completion.
        # Core result files remain available in either case.
        if presented < len(STAGE_TITLES):
            print_wrapped(f"Walkthrough stopped after step {presented}/{len(STAGE_TITLES)}. "
                          "Remaining stages were not presented.", style="info")
        else:
            print_wrapped("Walkthrough complete. All five teaching views were saved.",
                          style="success")
        print_wrapped(f"The filter results and main figures remain available in "
                      f"{output_directory}.", style="success")
        return 0
    except KeyboardInterrupt:
        # Ctrl+C reports an interruption with exit status 130. Whether the core
        # outputs were saved depends on which stage the interruption reached.
        print_wrapped("\nWalkthrough cancelled. Remaining stages were not presented.", style="info")
        if outputs_saved:
            print_wrapped(f"The filter results and main figures were already saved in "
                          f"{output_directory}.", style="success")
        else:
            print_wrapped("Processing stopped before all core outputs were saved.", style="error")
        return 130
    except (OSError, ValueError, RuntimeError, ImportError, cv2.error) as error:
        # Report input, output, numeric, and OpenCV errors on stderr, keeping
        # the underlying message so the student can identify what failed.
        # Return status 1 rather than claiming that a partial run succeeded.
        print_wrapped(f"The filtering run could not finish: {error}",
                      style="error", stream=sys.stderr)
        if outputs_saved:
            print_wrapped(f"The saved filter results and main figures remain available in "
                          f"{output_directory}.", style="info", stream=sys.stderr)
        else:
            print_wrapped("Check the input path, parameters, and output-folder permissions.",
                          style="info", stream=sys.stderr)
        return 1
    finally:
        # CLEANUP: Release figure windows even if an error interrupts processing.
        plt.close("all")
# ---


# __________________________________________
# MODULE INITIALIZATION
# ==========================================

# Python sets __name__ to "__main__" when this script is run directly. Importing
# it does not start filtering or open teaching windows. SystemExit passes the
# return value from main() to the terminal: success, failure, or Ctrl+C.
if __name__ == "__main__":
    raise SystemExit(main())


# __________________________________________
# END OF FILE
# ==========================================
