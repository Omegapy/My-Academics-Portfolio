#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Module Type: executable script
# Author: Alexander Ricciardi (Omega.py)
# Created: 2026-10-14
# -----------------------------------------------------------------------------
# Course: Foundations of Computer Vision CSC515
# Professor: Dr. Bingdong Li
# Term: Fall C (26FC) - 2026
# Assignment: Critical Thinking Module 5 - Option #2
#             Morphology Operations for Handwritten Text Enhancement
# -----------------------------------------------------------------------------
# The Program:
# Load the supplied scan from org_images/sticky_note.png. Separate the yellow
# handwritten note from the printed form and straighten its four sides. Convert
# the note to grayscale, then use inverse Otsu thresholding to make the writing
# white (255) and the background black (0).
# Compare dilation, erosion, opening, and closing on that same binary image,
# using one 3 x 3 elliptical kernel and one iteration for each operation.
# Save the processed images, numerical arrays, foreground measurements, and
# teaching figures in mod_images/. The terminal explains the results in six steps.
# Show one window at a time. Enter C to close it and continue, or Q to quit,
# followed by Enter. Step 6 includes two close-ups; the final view accepts Q.
# With --no-show, save the results and print the explanations without windows.
# All results are saved before the walkthrough; the original scan is unchanged.
# -----------------------------------------------------------------------------
# Requirements:
# - Python 3.12 or later.
# - OpenCV, NumPy, and Matplotlib; the verified versions are in requirements.txt.
#
# Run from this folder:
#    python -m pip install -r requirements.txt
#    python Module5_CTA_Option2.py             # Open the teaching views.
#    python Module5_CTA_Option2.py --no-show   # Save and explain without a GUI.
#
# Dependencies:
# - cv2 (OpenCV), numpy, matplotlib, and matplotlib.pyplot.
# - argparse, csv, io, os, pathlib, queue, sys, textwrap, threading, and typing from Python.
#
# Contents Overview:
# - parse_arguments() / load_image()
#   - Read display options and load the original scan once.
# - extract_note() / prepare_binary()
#   - Separate the note, straighten it, and prepare one binary input.
# - apply_dilation() / apply_erosion() / apply_opening() / apply_closing()
#   - Apply the four required OpenCV operations.
# - create_results() / measure_results()
#   - Keep results independent and count the changes to foreground pixels.
# - display_image() / build_figures()
#   - Present the existing arrays without recalculating the operations.
# - build_walkthrough() / style_text() / format_step() / save_results()
#   - Prepare the explanations and save all results before the presentation.
# - wait_for_guide_command() / run_walkthrough()
#   - Present the six steps while keeping desktop figures responsive.
# - main()
#   - Coordinate image preparation, morphology, saving, and the walkthrough.
# -----------------------------------------------------------------------------

"""Compare four morphological operations on the supplied handwritten note.

The program reads a scan of a yellow sticky note attached to a printed form.
It selects the note's four corners, straightens the note, and converts it to
grayscale. Inverse Otsu thresholding then gives the dark handwriting a value
of 255 (white) and the paper a value of 0 (black). All four operations use
this same uint8 binary image, kernel, and iteration count.

Dilation adds pixels around the handwriting, while erosion removes boundary
pixels. Opening applies erosion followed by dilation; closing uses the reverse
order. The program compares each result with the original binary input rather
than applying one operation to the result of another.

The saved binary images show the same white foreground used in the calculations.
The corner coordinates and two close-up regions are selected for this scan.
The program counts foreground changes but does not measure OCR accuracy.
"""

# ____________________________________________________________________________________
# ====================================================================================
# MORPHOLOGY COMPONENT MAP
#
# image_bgr  -> uint8 (974, 996, 3), original scan in blue, green, red order.
# note_bgr   -> uint8 (772, 769, 3), straightened note after the border is trimmed.
# gray_image -> uint8 (772, 769), one brightness value per pixel, from 0 to 255.
# binary     -> uint8 (772, 769), handwriting = 255; background = 0.
# NumPy selects a pixel with [y, x], which means [row, column].
#
#                       +--> dilation -----------------> thicker foreground
# binary ---------------+--> erosion ------------------> thinner foreground
#                       +--> erosion --> dilation -----> opening
#                       +--> dilation --> erosion -----> closing
#
# The branches are independent. Opening does not start from the saved erosion
# result, and closing does not start from opening. OpenCV performs each pair
# internally through morphologyEx(), beginning with the same binary input.
#
# A morphological operation uses a kernel to select which neighboring pixels
# are examined around each position. At 3 x 3, OpenCV's elliptical element has
# five active positions, arranged as a small cross:
#       0 1 0
#       1 1 1
#       0 1 0
# The ones are the active positions. A zero in the kernel means that position
# is not examined; it does not mean that the image pixel must be black.
# Dilation uses the largest value under the active positions, while erosion
# uses the smallest. Opening and closing combine those two operations.
#
# WHERE THE WORK HAPPENS:
# extract_note() and prepare_binary() prepare the common input.
# The four apply_...() functions calculate the morphological results.
# measure_results() counts pixel changes and connected foreground regions.
# The figure and terminal functions use the results already calculated.
# The teaching steps are views of one experiment, not six processing passes.
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

# The standard library handles command-line options, file paths, saved text,
# and the C/Q commands used while a Matplotlib window is open.
import argparse  # For command-line arguments.
import csv  # For saving measurements in a CSV file.
import io  # For building the terminal explanation as text.
import os  # For terminal color preferences.
from pathlib import Path  # For input and output file paths.
import queue  # For passing terminal commands between threads.
import sys  # For input, error messages, and exit status.
import textwrap  # For wrapping the explanation paragraphs.
import threading  # For reading C/Q without blocking the figure window.
from typing import TextIO  # For terminal output stream type hints.

# OpenCV prepares the note and performs the morphological operations. NumPy
# stores the images as arrays; Matplotlib creates the teaching figures.
import cv2  # Computer Vision Library.
import matplotlib  # Plotting library and backend settings.
import matplotlib.pyplot as plt  # For the teaching and comparison figures.
import numpy as np  # Numerical library for image arrays and measurements.
from matplotlib.axes import Axes  # For figure-panel type hints.
from matplotlib.figure import Figure  # For figure type hints.

# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

# The image is stored beside the script in org_images/. Using __file__ keeps
# these paths correct even when Python is started from another directory.
# All generated results go to mod_images/; the original scan is not replaced.
ASSIGNMENT_DIRECTORY = Path(__file__).resolve().parent
INPUT_PATH = ASSIGNMENT_DIRECTORY / "org_images" / "sticky_note.png"
OUTPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "mod_images"

# These four points were selected from the supplied 996 x 974-pixel scan.
# Each point is (x, y), ordered top-left, top-right, bottom-right, bottom-left.
# Selecting the note avoids including the surrounding printed form in the
# grayscale and foreground measurements.
NOTE_CORNERS = np.float32([[55, 136], [844, 61], [919, 853], [130, 928]])
NOTE_BORDER: int = 12  # Trim the note edge, not the handwritten text.

# The assignment uses one small structuring element for all four operations.
# MORPH_ELLIPSE at 3 x 3 has five active positions, not nine as in a full square.
# One iteration keeps the changes limited so the results can be compared.
KERNEL_SIZE: tuple[int, int] = (3, 3)
ITERATIONS: int = 1
FIGURE_DPI: int = 160  # Saved figure resolution; it does not change image pixels.

# Match Module 4's terminal palette. style_text() leaves redirected output plain.
TEXT_RESET: str = "\033[0m"
TEXT_STYLES: dict[str, str] = {
    "heading": "\033[1;96m",
    "rule": "\033[36m",
    "info": "\033[36m",
    "matrix": "\033[96m",
    "example": "\033[93m",
    "success": "\033[1;92m",
    "error": "\033[1;91m",
    "prompt": "\033[1;95m",
}

# The close-up coordinates belong to the straightened note: x1, y1, x2, y2.
# The first crop shows the curved C in the model label; the second shows the
# spacing between S and e in Set. Morphology is performed on the full note.
STROKE_BOX: tuple[int, int, int, int] = (540, 183, 707, 250)
GAP_BOX: tuple[int, int, int, int] = (382, 308, 480, 375)
OPERATION_NAMES = ("dilation", "erosion", "opening", "closing")
STAGE_TITLES = (
    "Prepare the handwritten note",
    "Dilation: expand the foreground",
    "Erosion: reduce the foreground",
    "Opening: remove small foreground marks",
    "Closing: fill small gaps",
    "Compare the four operations",
)
FIGURE_NAMES = (
    "01_preparation.png", "02_dilation.png", "03_erosion.png",
    "04_opening.png", "05_closing.png", "06_morphology_comparison.png",
    "07_stroke_detail.png", "08_gap_detail.png",
)

# These type aliases identify the result dictionaries and the six lists of
# terminal paragraphs. They do not change how the image data is processed.
MorphologyResults = dict[str, np.ndarray]
Measurements = dict[str, dict[str, int | float]]
GuideSteps = list[list[str]]

# __________________________________________
# PROGRAM OPTIONS AND IMAGE LOADING
# ==========================================

# --- parse_arguments()
def parse_arguments() -> argparse.Namespace:
    """Read the output folder and display options from the command line.

    Returns:
        The selected output directory and the --no-show and --no-pause options.

    Logic:
        Use mod_images/ as the default output folder. Both display options
        control the walkthrough, not the morphological calculations.
    """
    # ArgumentParser reads the optional settings. The formatter displays their
    # default values when the program is run with --help.
    parser = argparse.ArgumentParser(
        description="Compare dilation, erosion, opening, and closing on a handwritten note.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # A different output folder changes where files are saved, not the input image.
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIRECTORY,
                        help="Folder for the generated images and explanations.")
    # With --no-show, the program saves figures without opening desktop windows.
    parser.add_argument("--no-show", action="store_true", help="Save without opening windows.")
    # With --no-pause, the figures open without waiting for C/Q between views.
    parser.add_argument("--no-pause", action="store_true", help="Show without C/Q pauses.")
    return parser.parse_args()
# ---


# --- load_image()
def load_image(path: Path) -> np.ndarray:
    """Load the original color scan without changing its stored pixels.

    Args:
        path: Path to the supplied scanned image.

    Returns:
        A uint8 image with shape (height, width, 3) in BGR color order.

    Raises:
        OSError: If OpenCV cannot read or decode the image.
    """
    # cv2.imread() reads the scan into a NumPy array. IMREAD_COLOR requests three
    # channels in blue, green, red (BGR) order. The supplied PNG has an alpha
    # channel, but its image is opaque, so transparency does not need processing.
    image_bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
    # Error check: OpenCV returns None if the file cannot be decoded. Stop here
    # rather than passing an invalid image to the perspective transformation.
    if image_bgr is None:
        raise OSError(f"Could not load the input image: {path}")
    return image_bgr
# ---

# __________________________________________
# IMAGE PREPARATION - NOTE, GRAYSCALE, AND BINARY INPUT
# ==========================================

# First separate the handwritten note from the surrounding form. Then convert
# it to one grayscale image and prepare the binary input used by all operations.

# --- extract_note()
def extract_note(image_bgr: np.ndarray) -> np.ndarray:
    """Extract the handwritten note and straighten it using its four corners.

    Args:
        image_bgr: The original scan with BGR color channels.

    Returns:
        A uint8 BGR image of the straightened note with its border trimmed.

    Logic:
        Calculate the note's width and height from the selected corner positions.
        Use a perspective transformation to map those corners to a rectangle,
        then remove 12 pixels from each side. This step does not apply morphology.
    """
    # NOTE_CORNERS contains four (x, y) coordinates selected from the scan.
    # Unpack them in the same order used for the destination rectangle below.
    top_left, top_right, bottom_right, bottom_left = NOTE_CORNERS
    # np.linalg.norm() calculates the distance between two corners. Compare the
    # opposite sides and use the larger distance for the new width and height.
    # This gives the perspective transformation a rectangular output area.
    width = round(max(np.linalg.norm(top_right - top_left),
                      np.linalg.norm(bottom_right - bottom_left)))
    height = round(max(np.linalg.norm(bottom_left - top_left),
                       np.linalg.norm(bottom_right - top_right)))
    destination = np.float32([[0, 0], [width - 1, 0],
                             [width - 1, height - 1], [0, height - 1]])
    # The destination points describe the four corners of the new rectangle.
    # getPerspectiveTransform() calculates the matrix that maps the original
    # corners to those points. warpPerspective() uses the matrix to straighten
    # the note. INTER_LINEAR estimates pixel values between original positions.
    transform = cv2.getPerspectiveTransform(NOTE_CORNERS, destination)
    straight_note = cv2.warpPerspective(image_bgr, transform, (width, height),
                                       flags=cv2.INTER_LINEAR)
    # Remove 12 pixels around the edge after straightening. All five handwritten
    # lines remain. copy() gives the extracted note its own array in memory.
    return straight_note[NOTE_BORDER:-NOTE_BORDER, NOTE_BORDER:-NOTE_BORDER].copy()
# ---


# --- prepare_binary()
def prepare_binary(note_bgr: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Convert the straightened note to grayscale and prepare its binary image.

    Args:
        note_bgr: The straightened BGR note returned by extract_note().

    Returns:
        The grayscale uint8 image, the binary uint8 image with white handwriting,
        and the threshold calculated by Otsu's method.

    Logic:
        Keep one brightness value per pixel, then use inverse Otsu thresholding
        to assign 255 to dark writing and 0 to the brighter paper. No morphology
        is applied while the common binary input is prepared.
    """
    # cv2.cvtColor() converts the three BGR values into one brightness value per
    # pixel, still between 0 and 255. Morphology uses uint8 here because the
    # binary result contains only 0 or 255, not signed derivative responses.
    gray_image = cv2.cvtColor(note_bgr, cv2.COLOR_BGR2GRAY)
    # Otsu's method selects a threshold from the distribution of grayscale values.
    # THRESH_BINARY_INV assigns 255 to pixels at or below that threshold and 0
    # to brighter pixels. This makes the handwriting white so dilation expands
    # the writing rather than the surrounding paper.
    threshold, binary = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU,
    )
    # No Gaussian smoothing or opening is applied before the comparison. The
    # same binary image, including its remaining small marks, goes to all four
    # morphological operations.
    return gray_image, binary, threshold
# ---

# __________________________________________
# MORPHOLOGICAL OPERATIONS - IMAGE PROCESSING ONLY
# ==========================================

# All four methods use the same 3 x 3 elliptical kernel, one iteration, and a
# constant black border. Pixels beyond the image are treated as background (0).
# The handwriting is inside the trimmed note, away from this artificial border.

# --- apply_dilation()
def apply_dilation(binary: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply dilation to increase the white handwriting foreground.

    Args:
        binary: The binary uint8 input, handwriting = 255 and paper = 0.
        kernel: The 3 x 3 structuring element shared by all four operations.

    Returns:
        A binary image with thicker foreground strokes and enlarged white marks.

    Logic:
        For each pixel, take the largest value under the active kernel positions.
        This can strengthen a weak stroke, but may also join separate letters.
    """
    # cv2.dilate() takes the maximum of the selected neighboring pixel values.
    # A white pixel at any active position can make the output pixel white.
    # The operation adds foreground around the writing and can enlarge noise specks.
    return cv2.dilate(binary, kernel, iterations=ITERATIONS,
                      borderType=cv2.BORDER_CONSTANT, borderValue=0)
# ---


# --- apply_erosion()
def apply_erosion(binary: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply erosion to reduce the white handwriting foreground.

    Args:
        binary: The same binary image used by the other three operations.
        kernel: The 3 x 3 structuring element shared by all four operations.

    Returns:
        A binary image with thinner strokes and some small white marks removed.

    Logic:
        Take the smallest value under the active kernel positions. A pixel stays
        white only when all those positions are white. Thin strokes may break.
    """
    # cv2.erode() takes the minimum of the selected neighboring pixel values.
    # A black pixel under an active position makes the output pixel black.
    # This can remove an isolated speck, but may also remove part of a letter.
    return cv2.erode(binary, kernel, iterations=ITERATIONS,
                     borderType=cv2.BORDER_CONSTANT, borderValue=0)
# ---


# --- apply_opening()
def apply_opening(binary: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply opening to remove small white marks from the binary image.

    Args:
        binary: The unchanged binary input prepared from the note.
        kernel: The same structuring element used for erosion and dilation.

    Returns:
        A binary image with some isolated white marks and protrusions removed.

    Logic:
        Erosion is applied first, followed by dilation. The second operation
        expands what remains but cannot recover a mark removed completely.
    """
    # MORPH_OPEN performs erosion followed by dilation inside morphologyEx().
    # The same kernel is used for both operations. With one iteration, the
    # surviving strokes expand again, but a completely removed mark stays absent.
    return cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=ITERATIONS,
                            borderType=cv2.BORDER_CONSTANT, borderValue=0)
# ---


# --- apply_closing()
def apply_closing(binary: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply closing to fill small gaps in the white handwriting foreground.

    Args:
        binary: The unchanged binary input prepared from the note.
        kernel: The same structuring element used for dilation and erosion.

    Returns:
        A binary image with some small foreground gaps or holes filled.

    Logic:
        Dilation is applied first, followed by erosion. The second operation
        reduces the enlarged boundaries, but some filled gaps stay connected.
    """
    # MORPH_CLOSE performs dilation followed by erosion. It can fill a narrow
    # break in a stroke, but may also join letters separated by a small gap.
    # Isolated white background specks are not removed by this operation.
    return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=ITERATIONS,
                            borderType=cv2.BORDER_CONSTANT, borderValue=0)
# ---


# --- create_results()
def create_results(binary: np.ndarray, kernel: np.ndarray) -> MorphologyResults:
    """Calculate four independent results from the same binary image.

    Args:
        binary: The common input, which is not changed by these function calls.
        kernel: One structuring element shared by all four operations.

    Returns:
        The input and four named result arrays for saving, measurement, and display.

    Logic:
        Pass the original binary image separately to each operation. Opening
        does not use the erosion result, and closing does not use opening.
    """
    # ASSIGNMENT REQUIREMENT: Compare dilation, erosion, opening, and closing.
    # Each dictionary entry uses binary and the same kernel. No previous result
    # becomes the input to another operation. The binary image is also stored
    # so every calculated result can be compared with its original foreground.
    return {
        "binary": binary,
        "dilation": apply_dilation(binary, kernel),
        "erosion": apply_erosion(binary, kernel),
        "opening": apply_opening(binary, kernel),
        "closing": apply_closing(binary, kernel),
    }
# ---

# __________________________________________
# RESULT MEASUREMENTS - NO RECOGNITION MODEL
# ==========================================

# The program measures how the white foreground changes after morphology.
# These numbers describe pixels and connected regions, not recognized letters.

# --- measure_results()
def measure_results(results: MorphologyResults) -> Measurements:
    """Measure foreground pixel changes in the binary input and four results.

    Args:
        results: The unchanged binary input and the four morphological images.

    Returns:
        A dictionary containing foreground, added, and removed pixel counts,
        percentage change, and connected regions for each image.

    Logic:
        Count the pixels with a nonzero value, then compare each result with
        the original binary foreground. Count connected regions using eight
        neighbors, including diagonals. This does not measure OCR accuracy.
    """
    # White handwriting has a value of 255, so > 0 selects foreground pixels.
    # count_nonzero() gives the input count used as the comparison baseline.
    original_foreground = results["binary"] > 0
    original_count = int(np.count_nonzero(original_foreground))
    measurements: Measurements = {}
    # MAIN ITERATION LOOP: Start with the binary input, then visit the four
    # morphological results. The same order is used in the CSV and terminal table.
    for name, image in results.items():
        # Count every white foreground pixel in this image. Its total can be
        # larger or smaller than the original count, depending on the operation.
        foreground = image > 0
        count = int(np.count_nonzero(foreground))
        # connectedComponents() uses all eight neighboring directions. Its first
        # return value includes the background as one label, so subtract one.
        # A connected region could be a mark, one letter, or several joined letters.
        regions = cv2.connectedComponents(image, connectivity=8)[0] - 1
        # For added pixels, select positions that are now white but were black in
        # binary. For removed pixels, select positions that were white but are
        # now black. The percentage uses the original foreground count, not the
        # total number of pixels in the scanned image.
        measurements[name] = {
            "foreground_pixels": count,
            "added_pixels": int(np.count_nonzero(foreground & ~original_foreground)),
            "removed_pixels": int(np.count_nonzero(~foreground & original_foreground)),
            "change_percent": (100.0 * (count - original_count) / original_count
                               if original_count else 0.0),
            "connected_regions": int(regions),
        }
    return measurements
# ---

# __________________________________________
# FIGURES - DISPLAY ONLY
# ==========================================

# The figures use images already calculated by create_results(). Displaying
# the note does not apply morphology again or change any of the saved arrays.

# --- display_image()
def display_image(axis: Axes, image: np.ndarray, title: str) -> None:
    """Display a stored color, grayscale, or binary image in one panel.

    Args:
        axis: The Matplotlib panel where the image will appear.
        image: An existing BGR, grayscale, or binary image array.
        title: The label displayed above the image.

    Logic:
        Convert BGR to RGB for color display. Keep grayscale and binary values
        on the 0-to-255 scale without changing the source arrays.
    """
    # Color images have three dimensions: height, width, and BGR channel.
    if image.ndim == 3:
        # OpenCV reads blue, green, red. Matplotlib displays red, green, blue.
        # cvtColor() changes the display copy, not the saved original image.
        axis.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:
        # Use 0 for black and 255 for white. With binary images this displays the
        # handwriting in white, exactly as it was processed. Nearest-neighbor
        # display avoids smoothing the appearance of individual mask pixels.
        axis.imshow(image, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    # Keep the panel title but hide the axes; pixel coordinates are not needed
    # for comparing the appearance of the handwriting in these figures.
    axis.set_title(title, fontsize=11)
    axis.set_axis_off()
# ---


# --- build_figures()
def build_figures(image_bgr: np.ndarray, note_bgr: np.ndarray,
                  gray_image: np.ndarray, results: MorphologyResults) -> list[Figure]:
    """Create the six teaching figures and two close-ups from stored images.

    Args:
        image_bgr: Original scan showing the note and printed form.
        note_bgr: The extracted and straightened color note.
        gray_image: Grayscale note used to prepare the binary input.
        results: The binary input and all four calculated morphological results.

    Returns:
        Eight Matplotlib figures in the same order as FIGURE_NAMES.

    Logic:
        Show image preparation first, then compare each operation with its
        binary input. Finish with the full comparison and two close-up views.
        Every panel reads a stored array; morphology is not recalculated.
    """
    figures: list[Figure] = []
    # DISPLAY STEP 1: Use a 2-by-2 figure to show the original scan, straightened
    # note, grayscale note, and binary input. This separates image preparation
    # from the changes produced by morphology in the later figures.
    figure, axes = plt.subplots(2, 2, figsize=(10, 10), layout="constrained")
    preparation = ((image_bgr, "Original scan"),
                   (note_bgr, "Straightened note"),
                   (gray_image, "Grayscale note"),
                   (results["binary"], "Otsu binary input"))
    # DISPLAY LOOP: zip() pairs each of the four panels with the corresponding
    # prepared image and label. No image-processing function runs in this loop.
    for axis, (image, title) in zip(axes.flat, preparation):
        display_image(axis, image, title)
    figure.suptitle("STEP 1/6: Prepare the handwritten note", fontsize=15)
    figures.append(figure)

    # DISPLAY STEPS 2-5: Give each operation its own 1-by-2 comparison.
    # MAIN ITERATION LOOP: enumerate() supplies the step number, starting at 2.
    # The left panel always shows the same binary input; the right panel shows
    # one of the four operations. Both show the entire note at the same size.
    for step, name in enumerate(OPERATION_NAMES, start=2):
        figure, axes = plt.subplots(1, 2, figsize=(11, 6), layout="constrained")
        display_image(axes[0], results["binary"], "Same binary input")
        display_image(axes[1], results[name], name.capitalize())
        figure.suptitle(f"STEP {step}/6: {STAGE_TITLES[step - 1]}\n"
                       "3 x 3 elliptical kernel; one iteration", fontsize=14)
        figures.append(figure)

    # DISPLAY STEP 6: The six panels contain the straightened note, the binary
    # input, and the four morphological results. The same kernel was used for all.
    figure, axes = plt.subplots(2, 3, figsize=(12, 9), layout="constrained")
    display_image(axes[0, 0], note_bgr, "Straightened color note")
    # The remaining five panels follow results.items(), starting with binary.
    # zip() assigns an image and a title to each panel in that order.
    for axis, (name, image) in zip(list(axes.flat)[1:], results.items()):
        label = "Binary input" if name == "binary" else name.capitalize()
        display_image(axis, image, label)
    figure.suptitle("STEP 6/6: Compare the four operations\n"
                   "3 x 3 elliptical kernel; one iteration", fontsize=15)
    figures.append(figure)

    # CLOSE-UP FIGURES: Compare two small areas where morphology changes writing.
    # The first shows the curved stroke in the model label; the second shows
    # the space between S and e in Set. Only the displayed area is cropped.
    details = ((STROKE_BOX, "Thin curved stroke in the model label"),
               (GAP_BOX, "Letter spacing in the word Set"))
    # OUTER LOOP: Make one five-panel figure for each close-up region.
    for box, heading in details:
        x1, y1, x2, y2 = box
        figure, axes = plt.subplots(1, 5, figsize=(13, 3.1), layout="constrained")
        # INNER LOOP: Use the same crop coordinates and the same order for the
        # binary input and four operations. NumPy slices rows first, then columns:
        # image[y1:y2, x1:x2]. The crop does not change the full image array.
        for axis, (name, image) in zip(axes, results.items()):
            label = "Binary input" if name == "binary" else name.capitalize()
            display_image(axis, image[y1:y2, x1:x2], label)
        figure.suptitle(f"{heading}\n3 x 3 elliptical kernel; one iteration", fontsize=14)
        figures.append(figure)
    # All eight figures are returned together and saved before being displayed.
    return figures
# ---

# __________________________________________
# TERMINAL EXPLANATIONS - SIX TEACHING STEPS
# ==========================================

# This section prepares the text shown with the eight figures. It explains
# how the note was prepared, what each operation does, and the measured changes.
# The morphological calculations were completed before this function runs.

# --- build_walkthrough()
def build_walkthrough(image_bgr: np.ndarray, note_bgr: np.ndarray,
                      threshold: float, kernel: np.ndarray,
                      measurements: Measurements) -> GuideSteps:
    """Prepare six explanations of the processing and observed results.

    Args:
        image_bgr: The original scan, used to report its width and height.
        note_bgr: The straightened note, used to report its width and height.
        threshold: The Otsu threshold calculated from this note's grayscale image.
        kernel: The actual 3 x 3 element used by all four operations.
        measurements: Foreground counts and changes measured from this run.

    Returns:
        Six lists of paragraphs, in the same order as the teaching figures.

    Logic:
        Explain preparation, dilation, erosion, opening, closing, and the final
        comparison. Insert the measured values rather than fixed numbers from
        the paper. The same text is saved and printed in the terminal.
    """
    # Read the measurements calculated from the binary and morphological images.
    # No values from the written paper are substituted for the program's counts.
    base = measurements["binary"]
    dilation, erosion = measurements["dilation"], measurements["erosion"]
    opening, closing = measurements["opening"], measurements["closing"]
    # Each row of the kernel is converted to text so the reader can see the five
    # active positions. The four spaces keep the matrix aligned in the terminal.
    kernel_text = "\n".join("    " + " ".join(str(int(v)) for v in row) for row in kernel)
    table = ["    Operation   Foreground     Added   Removed   Change %   Regions"]
    # TABLE LOOP: List the original binary input, then the four operations.
    # The columns report actual foreground counts, added/removed pixels, net
    # percentage change, and connected regions. The CSV uses the same order.
    for name, values in measurements.items():
        table.append(f"    {name:<11}{values['foreground_pixels']:>10,}"
                     f"{values['added_pixels']:>10,}{values['removed_pixels']:>10,}"
                     f"{values['change_percent']:>11.2f}{values['connected_regions']:>10}")
    # The six steps below are explanation paragraphs, not six processing passes.
    # Each step is paired with its already-calculated image in run_walkthrough().
    return [
        # __________________________________________
        # TEACHING STEP 1 OF 6: PREPARE THE NOTE
        # ==========================================
        [
            f"The program loads the {image_bgr.shape[1]} x {image_bgr.shape[0]}-pixel scan. "
            "It shows a tilted yellow sticky note attached to a printed form. "
            "In extract_note(), four selected corners are used to straighten the note. "
            f"A {NOTE_BORDER}-pixel border is then removed. The resulting image is "
            f"{note_bgr.shape[1]} x {note_bgr.shape[0]} pixels.",
            "In prepare_binary(), grayscale conversion gives each pixel one brightness "
            "value instead of three color values. Otsu's method selects a threshold "
            f"of {threshold:.0f} on the 0-255 scale. Pixels at or below this value "
            "become white foreground (255); brighter pixels become black background "
            "(0). The saved and displayed binary images use these same values.",
            "Morphology uses a structuring element, also called a kernel, to select "
            "the neighboring pixels examined around each position. The 3 x 3 "
            "elliptical element has five active positions (1). Positions marked 0 "
            "are ignored:\n" + kernel_text,
            f"The binary image contains {base['foreground_pixels']:,} white foreground "
            "pixels. All four operations use this same input. No noise is added, and "
            "no Gaussian smoothing or opening is performed before the comparison.",
        ],
        # __________________________________________
        # TEACHING STEP 2 OF 6: DILATION
        # ==========================================
        [
            "Dilation expands the white foreground, making the handwriting thicker. "
            "For each position, it uses the largest value under the five active "
            "kernel positions. One white neighboring pixel can make the output white.",
            f"Dilation adds {dilation['added_pixels']:,} foreground pixels, an increase "
            f"of {dilation['change_percent']:.2f}%. This can help when a stroke is "
            "weak or disconnected. However, the small white marks in the background "
            "also become larger.",
            "For example, a small gap separates S and e in the word Set in the "
            "binary input, but dilation joins the two letters. This could make "
            "character separation more difficult. It does not mean that a damaged "
            "stroke has been repaired.",
        ],
        # __________________________________________
        # TEACHING STEP 3 OF 6: EROSION
        # ==========================================
        [
            "Erosion removes pixels around the white foreground boundaries, making "
            "the strokes thinner. A pixel remains white only when every active "
            "kernel position fits inside the white handwriting.",
            f"Erosion removes {erosion['removed_pixels']:,} foreground pixels, or "
            f"{abs(erosion['change_percent']):.2f}% of the input foreground. Some small "
            "background specks disappear, but thin portions of letters can also "
            "be removed.",
            "In the model label, a thin curved stroke becomes broken near the "
            "following i. The background may look cleaner in some areas, but part "
            "of the handwriting has been lost. See figures/07_stroke_detail.png "
            "to compare the stroke before and after erosion.",
        ],
        # __________________________________________
        # TEACHING STEP 4 OF 6: OPENING
        # ==========================================
        [
            "Opening applies erosion followed by dilation. Erosion removes small "
            "foreground structures, and dilation expands the parts that remain. "
            "However, dilation cannot restore a mark removed completely by erosion.",
            f"Opening removes {opening['removed_pixels']:,} foreground pixels "
            f"({abs(opening['change_percent']):.2f}%) without adding white pixels. "
            "Three small isolated marks near the upper-right background disappear. "
            "Most of the handwriting remains close to its original stroke width.",
            "The curved stroke in the model label stays connected after opening, "
            "unlike direct erosion. Some other small fragments and boundary details "
            "are removed. A detached mark could belong to a letter, so its removal "
            "does not automatically mean the writing has been improved.",
        ],
        # __________________________________________
        # TEACHING STEP 5 OF 6: CLOSING
        # ==========================================
        [
            "Closing applies dilation followed by erosion. Dilation can fill a "
            "small hole or gap, while erosion reduces the expanded outer boundary. "
            "A connection made during dilation may still remain afterward.",
            f"Closing adds {closing['added_pixels']:,} foreground pixels "
            f"({closing['change_percent']:.2f}%) without removing foreground. The "
            "handwriting changes very little overall, but the small isolated "
            "marks in the upper-right background remain.",
            "The S and e in Set become connected. This reduces the number of "
            f"connected regions from {base['connected_regions']} to "
            f"{closing['connected_regions']}. The program cannot determine "
            "whether this space was a damaged stroke or a separation between letters. "
            "See figures/08_gap_detail.png to compare the gap.",
        ],
        # __________________________________________
        # TEACHING STEP 6 OF 6: COMPARE RESULTS
        # ==========================================
        [
            "The final comparison shows the straightened color note, its binary "
            "input, and the four morphological results. All four start with the "
            "same binary image; they are not a sequence of processing steps.",
            "\n".join(table),
            "The foreground counts show how many white pixels were added or "
            "removed. A connected region can contain several letters or only one "
            "small mark. These measurements do not count characters or indicate "
            "whether an OCR system can recognize the handwriting accurately.",
            "For this note, the 3 x 3 opening removes several background marks "
            "without the thicker strokes of dilation or the broken curve seen "
            "with erosion. Closing changes fewer foreground pixels, but it joins "
            "the space between S and e in Set. Much of the improvement in paper "
            "contrast comes from Otsu thresholding before morphology. These "
            "results do not mean opening will be best for every handwritten note.",
        ],
    ]
# ---


# --- style_text()
def style_text(message: str, style: str = "", *, stream: TextIO | None = None) -> str:
    """Add terminal color without changing the message's text or spacing.

    Args:
        message: The original text to display.
        style: A name in TEXT_STYLES; an empty value leaves text unchanged.
        stream: Destination checked for terminal support; defaults to stdout.

    Returns:
        Colored text for a supported terminal, otherwise the original text.
    """
    # Check the actual destination so redirected stdout or stderr stays plain.
    # NO_COLOR and TERM="dumb" disable colors, matching Module 4's behavior.
    output = sys.stdout if stream is None else stream
    if (not message or not style or not output.isatty() or os.environ.get("NO_COLOR")
            or os.environ.get("TERM", "").lower() == "dumb"):
        return message
    # Reset immediately after the message so later terminal text keeps its style.
    code = TEXT_STYLES.get(style, "")
    return f"{code}{message}{TEXT_RESET}" if code else message
# ---


# --- format_step()
def format_step(step: int, paragraphs: list[str], *, color: bool = False) -> str:
    """Format one teaching step for both the terminal and saved transcript.

    Args:
        step: Step number, from 1 through 6.
        paragraphs: The explanation paragraphs prepared by build_walkthrough().
        color: Request terminal colors; leave False for the saved transcript.

    Returns:
        A string containing the step banner, paragraphs, and saved figure name.

    Logic:
        Wrap ordinary paragraphs at word boundaries, but keep the indented
        kernel matrix and measurement table aligned. Use the same text for
        the live terminal and terminal_output.txt.
    """
    # StringIO collects the complete teaching step before it is printed or saved.
    # The fixed separator keeps the six step titles easy to distinguish.
    text = io.StringIO()
    rule = style_text("=" * 88, "rule" if color else "")
    text.write("\n" + rule + "\n")
    text.write(style_text(f"STEP {step}/6: {STAGE_TITLES[step - 1]}",
                          "heading" if color else "") + "\n")
    text.write(rule + "\n\n")
    # OUTER LOOP: Read each paragraph in the current teaching step.
    # INNER LOOP: Process its lines separately. Kernel and table rows start with
    # four spaces, so leave them aligned rather than wrapping their columns.
    # Other lines are wrapped at word boundaries using the 88-character width.
    for paragraph in paragraphs:
        for line in paragraph.splitlines():
            wrapped = (line if line.startswith("    ") else
                       textwrap.fill(line, width=88, break_long_words=False,
                                     break_on_hyphens=False))
            # Add color after wrapping so escape codes cannot shift the text.
            style = "matrix" if line.startswith("    ") else "info"
            text.write(style_text(wrapped, style if color else "") + "\n")
        text.write("\n")
    # The first six filenames belong to the six teaching steps. The two close-up
    # filenames are reported separately with Step 6 in the walkthrough.
    text.write(style_text(f"Saved teaching view: figures/{FIGURE_NAMES[step - 1]}",
                          "success" if color else "") + "\n")
    return text.getvalue()
# ---

# __________________________________________
# SAVE RESULTS - IMAGES, ARRAYS, AND EXPLANATIONS
# ==========================================

# Save the calculated images and their data before opening any teaching views.
# The binary PNG files keep white handwriting and black paper, while the NPZ
# archive also retains the kernel, note corners, threshold, and original arrays.

# --- save_results()
def save_results(output_directory: Path, note_bgr: np.ndarray,
                 gray_image: np.ndarray, results: MorphologyResults,
                 kernel: np.ndarray, threshold: float, measurements: Measurements,
                 figures: list[Figure], walkthrough: GuideSteps) -> None:
    """Save the prepared images, measurements, and complete terminal explanation.

    Args:
        output_directory: Folder where the generated files are written.
        note_bgr: The extracted and straightened BGR note.
        gray_image: The grayscale note before thresholding.
        results: The binary input and four morphological result arrays.
        kernel: The 3 x 3 structuring element used by the operations.
        threshold: Otsu's threshold calculated from the supplied note.
        measurements: Foreground changes and connected-region counts.
        figures: Six teaching figures and the two close-up comparisons.
        walkthrough: The text for all six steps of the terminal explanation.

    Raises:
        OSError: If an output directory or output file cannot be written.

    Logic:
        Save viewable PNG images, original numerical arrays in an NPZ file,
        measurements in a CSV file, and the complete terminal explanation in
        a text file. All files are saved before the reader can quit the guide.
    """
    # Create the main output directory and a separate folder for the eight
    # Matplotlib figures. Repeated runs can use the same directories.
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = output_directory / "figures"
    figure_directory.mkdir(exist_ok=True)
    images = {"note_rectified.png": note_bgr, "grayscale.png": gray_image,
              "binary_foreground.png": results["binary"]}
    # IMAGE LIST LOOP: Include the common binary input and all four results.
    # Their PNGs use the actual binary values: white handwriting (255) and black
    # background (0). binary_foreground.png and binary.png contain the same mask.
    for name, image in results.items():
        images[f"{name}.png"] = image
    # SAVE LOOP: Write the prepared and morphological images. imwrite() returns
    # False when it cannot write a file, so report that output instead of
    # continuing as if the image had been saved.
    for name, image in images.items():
        if not cv2.imwrite(str(output_directory / name), image):
            raise OSError(f"Could not save the output image: {name}")
    # savez_compressed() stores the arrays and experiment settings in one NPZ
    # archive. The masks keep their original dimensions and uint8 values; they
    # are not inverted or modified for display before being stored.
    np.savez_compressed(output_directory / "morphology_arrays.npz", **results,
                        note_bgr=note_bgr, gray_image=gray_image, kernel=kernel,
                        threshold=threshold, note_corners=NOTE_CORNERS,
                        note_border=NOTE_BORDER, iterations=ITERATIONS)
    # FIGURE LOOP: zip() pairs each of the eight figures with its filename.
    # savefig() includes the panel titles and notes. DPI changes the resolution
    # of the saved figure, not the pixel values used in morphology.
    for figure, name in zip(figures, FIGURE_NAMES):
        figure.savefig(figure_directory / name, dpi=FIGURE_DPI)
    with (output_directory / "measurements.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        # The CSV header uses the measurement names produced by measure_results().
        writer.writerow(["operation", *next(iter(measurements.values())).keys()])
        # TABLE LOOP: Write the binary input first and then the four operations.
        # Each image gets the same columns used in the terminal comparison table.
        for name, values in measurements.items():
            writer.writerow([name, *values.values()])
    with (output_directory / "terminal_output.txt").open("w", encoding="utf-8") as stream:
        stream.write("CSC515 Module 5 - Morphology Operations for Handwritten Text Enhancement\n")
        # EXPLANATION LOOP: Save all six formatted steps now. Quitting with Q
        # during the live walkthrough will not remove any of the saved text.
        for step, paragraphs in enumerate(walkthrough, start=1):
            stream.write(format_step(step, paragraphs))
        stream.write("\nAdditional views: figures/07_stroke_detail.png and figures/08_gap_detail.png\n")
# ---

# __________________________________________
# TEACHING CONTROLS - WINDOWS AND TERMINAL INPUT
# ==========================================

# Terminal input and Matplotlib use different threads on macOS. Only the main
# thread updates the figure windows. The input thread reads a line of text and
# passes the command back through a queue.

# --- wait_for_guide_command()
def wait_for_guide_command(figure: Figure, final_step: bool = False) -> str:
    """Read C or Q while keeping the current Matplotlib figure responsive.

    Args:
        figure: The current figure whose window must continue updating.
        final_step: True when the last close-up is open and only Q is allowed.

    Returns:
        The accepted uppercase command C or Q.

    Logic:
        A reader thread receives one line from the terminal. The main thread
        continues processing figure events and checks the command. Invalid
        entries are rejected without moving to another teaching view.
    """
    commands: queue.Queue[str] = queue.Queue()
    prompt = ("Enter Q to finish, then press Enter: " if final_step
              else "Enter C to continue or Q to quit, then press Enter: ")

    # Reading terminal input separately avoids blocking the image window.
    # input() can start Matplotlib's macOS GUI input hook in the worker thread.
    # Use stdin.readline() below so native figure events stay on the main thread.
    # --- read_command()
    def read_command() -> None:
        """Read a terminal line and send its command to the waiting main thread.

        End of input or an OSError is treated as Q. This function does not
        draw, process, or close any Matplotlib figures.
        """
        try:
            # readline() waits until Enter is pressed. strip() removes spaces
            # and upper() accepts both lowercase and uppercase C/Q. An empty
            # input stream is treated as Q; an empty submitted line is invalid.
            line = sys.stdin.readline()
            commands.put(line.strip().upper() if line else "Q")
        except OSError:
            # An unreadable input stream also finishes the guide with Q.
            commands.put("Q")
    # ---

    # VALIDATION LOOP: Ask for another command only when the submitted one is
    # not allowed. C advances before the final view; Q finishes at any view.
    while True:
        print(style_text(prompt, "prompt"), end="", flush=True)
        # The input reader never calls Matplotlib. It only puts the text in
        # the queue, which the main thread checks while the window stays active.
        threading.Thread(target=read_command, daemon=True).start()
        while commands.empty():
            # Process the current figure's events for 50 ms at a time.
            # plt.pause() uses the global display and could open later figures
            # before their turn, so use this figure's event loop instead.
            figure.canvas.start_event_loop(0.05)
        command = commands.get()
        # Q always finishes. At the last close-up C is no longer a valid choice.
        if command == "Q" or (command == "C" and not final_step):
            return command
        print(style_text("Please enter Q." if final_step else "Please enter C or Q.",
                         "example"), flush=True)
# ---


# --- run_walkthrough()
def run_walkthrough(walkthrough: GuideSteps, figures: list[Figure],
                    no_show: bool, no_pause: bool) -> None:
    """Print the six explanations and display their matching teaching figures.

    Args:
        walkthrough: The six sets of paragraphs prepared by build_walkthrough().
        figures: Six step figures followed by two close-up comparisons.
        no_show: If True, print the text without opening image windows.
        no_pause: If True, open the figures without asking for C/Q.

    Logic:
        Print each step from the text already prepared. Show one matching figure
        at a time, followed by both close-ups during Step 6. C closes the current
        view and continues; Q stops the guide. No morphological result is changed.
    """
    # MAIN ITERATION LOOP: Present Steps 1 through 6 in order. format_step()
    # produces the same wording and spacing saved in terminal_output.txt.
    # The figures were created earlier and no morphological operation is rerun.
    for step, paragraphs in enumerate(walkthrough, start=1):
        print(format_step(step, paragraphs, color=True), flush=True)
        if no_show:
            # Headless mode still prints all six steps; it just skips windows.
            continue
        # Steps 1-5 each use one figure. Step 6 uses the full comparison and
        # both close-ups. Later views are not shown before their own turn.
        step_figures = figures[5:] if step == 6 else figures[step - 1:step]
        # DISPLAY LOOP: Open the selected figure, wait for the command if the
        # guide is paused, and close this figure before opening the next one.
        for view, figure in enumerate(step_figures):
            if view > 0:
                # The two detail views belong to Step 6 and have separate files.
                print(style_text(f"STEP 6/6 - Close-up {view}/2: "
                                 f"figures/{FIGURE_NAMES[5 + view]}", "heading"), flush=True)
            figure.show()
            figure.canvas.start_event_loop(0.05)
            if not no_pause:
                # Only the last close-up accepts Q. If Q is entered sooner,
                # the saved files remain available even though the guide stops.
                final_view = step == 6 and view == len(step_figures) - 1
                if wait_for_guide_command(figure, final_step=final_view) == "Q":
                    plt.close("all")
                    return
                # C closes the current window before the next view is shown.
                plt.close(figure)
    if not no_show and no_pause:
        # In --no-pause mode, leave the displayed figures open until the reader
        # closes them. The terminal input loop is not used in this mode.
        plt.show()  # Keep the open views available until their windows are closed.
    plt.close("all")
# ---

# _________________________________________________________
# MAIN FUNCTION - Interface of the program (entry point)
# =======================================================

# --- main()
def main() -> int:
    """Prepare the note, compare the four operations, and present the results.

    Returns:
        0 on completion or Q, 1 for an input/output error, or 130 for Ctrl+C.

    Logic:
        Load and prepare one binary input, apply each morphological operation
        independently, and count the foreground changes. Save the results,
        then present the six-step explanation and eight prepared figures.
    """
    # Parse the output and display settings before loading the scan.
    args = parse_arguments()
    if args.no_show:
        plt.switch_backend("Agg")  # Saving does not require a desktop backend.
    # Disable automatic figure display. All eight figures are built and saved
    # before the walkthrough opens them, one at a time.
    plt.ioff()
    try:
        # __________________________________________
        # STEP 1: LOAD AND PREPARE THE HANDWRITTEN NOTE
        # ==========================================
        # Read the original scan once. Straighten the note, convert it to
        # grayscale, then use Otsu to prepare the shared binary input.
        image_bgr = load_image(INPUT_PATH)
        note_bgr = extract_note(image_bgr)
        gray_image, binary, threshold = prepare_binary(note_bgr)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, KERNEL_SIZE)

        # __________________________________________
        # STEPS 2-5: CALCULATE THE FOUR MORPHOLOGICAL OPERATIONS
        # ==========================================
        # All four methods use this binary image, the same 3 x 3 kernel, and one
        # iteration. measure_results() counts changes after processing is complete.
        results = create_results(binary, kernel)
        measurements = measure_results(results)

        # __________________________________________
        # STEP 6: BUILD THE FIGURES AND EXPLANATIONS
        # ==========================================
        # Prepare the eight figures and six teaching explanations using the
        # stored arrays and actual measurements, without applying morphology again.
        figures = build_figures(image_bgr, note_bgr, gray_image, results)
        walkthrough = build_walkthrough(image_bgr, note_bgr, threshold, kernel, measurements)
        # __________________________________________
        # SAVE THE RESULTS BEFORE THE WALKTHROUGH
        # ==========================================
        # Save the PNGs, arrays, CSV measurements, and full terminal transcript.
        # Leaving the guide early does not remove any of these files.
        save_results(args.output_dir, note_bgr, gray_image, results, kernel,
                     threshold, measurements, figures, walkthrough)
        print(style_text("CSC515 Module 5 - Morphology Operations for Handwritten Text Enhancement",
                         "heading"))
        print(style_text("The images, measurements, and complete explanation were saved before the walkthrough.",
                         "success"))
        # __________________________________________
        # PRESENT THE SIX TEACHING STEPS
        # ==========================================
        # Display the figures in order unless --no-show was selected. The guide
        # uses C/Q for navigation but does not recalculate the image results.
        run_walkthrough(walkthrough, figures, args.no_show, args.no_pause)
        print(style_text(f"\nSaved results: {args.output_dir.resolve()}", "success"))
        return 0
    except (OSError, cv2.error) as error:
        # Report a failed image read, OpenCV operation, or output write with the
        # underlying error. Repeating the same checks in every function is not needed.
        print(style_text(f"The program could not finish: {error}", "error", stream=sys.stderr),
              file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Ctrl+C stops the walkthrough with exit status 130. Any results written
        # before the interruption remain in the selected output folder.
        print(style_text("\nThe walkthrough was stopped.", "info", stream=sys.stderr), file=sys.stderr)
        return 130
    finally:
        # CLEANUP: Close the figure windows after normal completion or an error.
        plt.close("all")
# ---


# __________________________________________
# MODULE INITIALIZATION
# =========================================
# 
# Init. and launch the program
if __name__ == "__main__":
    raise SystemExit(main())

# __________________________________________
# END OF FILE
# ==========================================
