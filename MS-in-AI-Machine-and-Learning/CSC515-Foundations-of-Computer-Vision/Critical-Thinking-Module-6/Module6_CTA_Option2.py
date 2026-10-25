#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Module Type: executable script
# Author: Alexander Ricciardi (Omega.py)
# Created: 2026-10-19
# -----------------------------------------------------------------------------
# Course: Foundations of Computer Vision CSC515
# Professor: Dr. Bingdong Li
# Term: Fall C (26FC) - 2026
# Assignment: Critical Thinking Module 6 - Option #2
#             Adaptive Thresholding Scheme Accounting for Changes in Illumination
# -----------------------------------------------------------------------------
# The Program
# Read the two supplied mug photographs from org_images/, starting with light
# from the white mug's side, followed by light from the black mug's side
# Resize each full scene to 1,000 pixels wide, convert it to grayscale, and blur
# Compare an initial and revised inverse Gaussian adaptive thresholding scheme
# Apply the same settings to both photographs and examine changes in illumination
# Save the images, measurements, and five teaching figures in mod_images/
# White mask pixels identify locally dark regions, not complete mug silhouettes
# The terminal explains five steps and prints the actual runtime versions
# Enter C to close the current view and continue, or Q to quit, then press Enter
# All results are saved before the first view; --no-show runs without windows
# -----------------------------------------------------------------------------
# Requirements
# - Python 3.12 (reference version: 3.12.13)
# - OpenCV 4.13.0 (opencv-contrib-python==4.13.0.92), NumPy 2.5.3, Matplotlib 3.11.2
# - Install dependencies if needed: python -m pip install -r requirements.txt
#
# Run from the folder containing this file:
#    python Module6_CTA_Option2.py
#    python Module6_CTA_Option2.py --no-show
#
# Dependencies
# - cv2 4.13.0 (opencv-contrib-python), numpy 2.5.3, matplotlib 3.11.2
# - matplotlib.pyplot, matplotlib.axes, and matplotlib.figure (part of Matplotlib)
# - argparse, csv, io, os, pathlib, queue, sys, textwrap, threading, and typing
#
# Contents Overview
# - parse_arguments() / load_and_prepare()
#   - Read the program options and prepare both complete photographs
# - threshold_image() / measure_masks()
#   - Calculate both adaptive masks and count the selected pixels
# - display_image() / make_figure() / build_figures()
#   - Present calculated arrays without changing the processing results
# - build_walkthrough() / format_step() / save_results()
#   - Prepare and save the five explanations, measurements, and figures
# - wait_for_guide_command() / run_walkthrough() / main()
#   - Present the C/Q guide and coordinate the program
# -----------------------------------------------------------------------------

"""Compare adaptive thresholding under two directions of illumination.

The scene contains a glossy black mug, a light mug, a dark backdrop, and a light
surface. The black mug reflects objects in its surroundings. These reflections,
cast shadows, and the light mug's embossed pattern all change image brightness.
They must not all be described as random noise.

The program compares initial and revised inverse adaptive Gaussian results.
The same settings process both complete scenes. White pixels
in the adaptive masks identify locally dark regions. They do not establish
which pixels belong to either mug, and the output does not isolate complete
objects from their background.

The revised adaptive mask is the final output for each photograph.
The program measures pixel coverage and connectivity, not segmentation accuracy.
Both photographs were used during development; neither is a held-out test image.
"""

# ____________________________________________________________________________________
# ====================================================================================
# IMAGE REPRESENTATIONS AND PROCESSING
#
# original_bgr: original uint8 photograph, with blue, green, and red channels
# scene_bgr: full photograph resized to a width of 1,000 pixels
# gray / blurred: one uint8 brightness value per pixel, from 0 to 255
# masks: uint8 images with locally dark regions at 255 and other regions at 0
# NumPy selects image pixels with [y, x], which means [row, column]
#
# blurred image -------+--> adaptive Gaussian (31, C=5) -----------> initial_adaptive
#                      +--> adaptive Gaussian (101, C=10) ---------> revised_adaptive
# revised_adaptive --------> final display overlay and measurements
#
# Both adaptive calculations use the same blurred image
# The revision starts from that input and does not process the initial binary mask
# The revised mask is the final result; the overlay only shows its selected pixels
#
# The adaptive threshold T at a pixel is the Gaussian-weighted local mean minus C
# THRESH_BINARY_INV writes 255 for pixels at or below T and 0 for brighter pixels
# The block size determines the neighborhood; C changes the local brightness cutoff
# White mask pixels identify locally dark image regions, not either mug by identity
#
# WHERE THE WORK HAPPENS
# load_and_prepare() reads each photograph, converts it to grayscale, and smooths it
# threshold_image() calculates the initial and revised binary masks
# measure_masks() counts white pixels and connected regions without a reference mask
# build_figures() and build_walkthrough() use the already-calculated results
# Saving and displaying the teaching figures do not repeat the threshold calculations
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

# The Python standard library handles command-line arguments, file paths
# saved tables, the five terminal explanations, and C/Q commands while a figure is open
import argparse  # For optional output and display settings
import csv  # For the measured pixel counts
import io  # For building the saved terminal explanation
import os  # For checking terminal color preferences
from pathlib import Path  # For paths relative to this script
import queue  # For passing C/Q commands to the main thread
import sys  # For the Python version, input, and exit status
import textwrap  # For wrapping terminal paragraphs
import threading  # For terminal input while the picture stays responsive
from typing import Any, TextIO  # For result and output-stream type hints

# OpenCV loads and processes the photographs, NumPy holds the image arrays
# and Matplotlib creates the teaching figures without changing the original pixels
import cv2  # Computer Vision Library
import matplotlib  # For the installed version and backend settings
import matplotlib.pyplot as plt  # For teaching figures and desktop windows
import numpy as np  # For image arrays and pixel counts
from matplotlib.axes import Axes  # For figure-panel type hints
from matplotlib.figure import Figure  # For figure type hints

# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

# Input paths belong to this assignment, regardless of the shell's current folder
ASSIGNMENT_DIRECTORY = Path(__file__).resolve().parent
INPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "org_images"
OUTPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "mod_images"
# Process the two illumination directions in the order given by the assignment
# The name selects the source JPEG; the title identifies the lighting direction
SCENES = (
    ("light_white_mug_side", "Light from the white mug's side"),
    ("light_black_mug_side", "Light from the black mug's side"),
)

# Use one processing width while retaining the aspect ratio of each photograph
# A 5 x 5 Gaussian reduces small image changes before the threshold comparison
# The 31 x 31 adaptive window is the first attempt, with C subtracting 5
# The revised 101 x 101 window examines a wider area and subtracts 10
# Both block sizes are odd, as required by cv2.adaptiveThreshold()
PROCESSING_WIDTH: int = 1000
BLUR_SIZE: tuple[int, int] = (5, 5)
INITIAL_BLOCK_SIZE: int = 31
INITIAL_C: int = 5
REVISED_BLOCK_SIZE: int = 101
REVISED_C: int = 10
FIGURE_DPI: int = 150

# The step titles and figure names follow the same order as the terminal guide
# Each step has one view, so C advances one picture and Q ends the walkthrough
STAGE_TITLES = (
    "Prepare the two full scenes",
    "Threshold the scene lit from the white mug's side",
    "Use the same scheme with light from the black mug's side",
    "Revise the adaptive settings for both photographs",
    "Examine the results and their limits",
)
FIGURE_NAMES = (
    "01_preparation.png", "02_white_side_thresholding.png",
    "03_black_side_thresholding.png", "04_adaptive_revision.png",
    "05_final_comparison.png",
)
# Keep each saved figure paired with its terminal explanation
STAGE_FIGURES = ((0,), (1,), (2,), (3,), (4,))

# Yellowish green banners separate the steps while redirected output stays plain
# ANSI color 191 gives the title and border the same shade in a 256-color terminal
TEXT_RESET = "\033[0m"
TEXT_STYLES = {
    "heading": "\033[1;38;5;191m", "rule": "\033[38;5;191m", "info": "\033[36m",
    "matrix": "\033[96m", "example": "\033[93m", "success": "\033[1;92m",
    "error": "\033[1;91m", "prompt": "\033[1;95m",
}
# These aliases describe the result dictionaries and the five lists of teaching text
# They do not change how OpenCV or NumPy handles image data
SceneResult = dict[str, Any]
Measurements = dict[str, dict[str, int | float]]
GuideSteps = list[list[str]]

# __________________________________________
# PROGRAM OPTIONS AND IMAGE PREPARATION
# ==========================================

# --- parse_arguments()
def parse_arguments() -> argparse.Namespace:
    """Read the output destination and display options.

    Returns:
        The output directory, --no-show setting, and --no-pause setting.

    Logic:
        Keep input paths beside the script. Display options control the guide;
        they do not change any threshold, mask, or saved measurement.
    """
    # ArgumentParser reads optional terminal settings and shows their defaults with --help
    # Each option controls files or figure presentation, not the image-processing parameters
    parser = argparse.ArgumentParser(
        description="Compare adaptive thresholding on two illuminated mug scenes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # --output-dir selects where the derived images and measurements will be written
    # type=Path converts the supplied name to a Path object for file operations
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIRECTORY,
                        help="Folder for generated images and explanations.")
    # --no-show creates the images and text without requesting desktop figure windows
    parser.add_argument("--no-show", action="store_true",
                        help="Save and explain without opening windows.")
    # --no-pause shows the figures without waiting for C or Q after each view
    # store_true keeps the option False unless it appears in the command
    parser.add_argument("--no-pause", action="store_true",
                        help="Show the figures without C/Q pauses.")
    return parser.parse_args()
# ---


# --- load_and_prepare()
def load_and_prepare(stem: str, title: str) -> SceneResult:
    """Read one photograph and prepare the common thresholding input.

    Args:
        stem: Photograph filename without its .jpeg extension.
        title: Human-readable description of the illumination direction.

    Returns:
        A dictionary containing the original, resized BGR, grayscale, and
        blurred images, along with their filename and illumination label.

    Raises:
        OSError: If OpenCV cannot read the supplied photograph.

    Logic:
        Resize the full image with its aspect ratio preserved. Use the same
        grayscale conversion and small Gaussian blur for both photographs.
    """
    # The source file is selected by SCENES and kept in org_images/
    # __file__ keeps the path correct when Python is started in another folder
    path = INPUT_DIRECTORY / f"{stem}.jpeg"
    # cv2.imread() decodes the JPEG into a NumPy array in RAM
    # str(path) passes a filename string to OpenCV, while IMREAD_COLOR requests
    # three uint8 channels in BGR order with shape (height, width, 3)
    original = cv2.imread(str(path), cv2.IMREAD_COLOR)
    # Error check: OpenCV returns None when the image cannot be opened or decoded
    # Stop before calling resize() with an invalid input image
    if original is None:
        raise OSError(f"Could not load the input image: {path}")
    # NumPy stores dimensions as height first, then width
    # cv2.resize() instead expects the new width and height in that order
    height, width = original.shape[:2]
    resized_height = round(PROCESSING_WIDTH * height / width)
    # round() preserves the photograph aspect ratio as closely as whole pixels allow
    # INTER_AREA is used when the original image is reduced to the processing width
    # The whole scene stays in the calculation, including both mugs and their shadows
    scene_bgr = cv2.resize(original, (PROCESSING_WIDTH, resized_height),
                           interpolation=cv2.INTER_AREA)
    # cv2.COLOR_BGR2GRAY combines the three color channels into one intensity value
    # The returned uint8 image keeps the resized height and width, with values 0-255
    gray = cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2GRAY)
    # GaussianBlur() averages neighboring intensities with larger weights near the center
    # The tuple BLUR_SIZE fixes the neighborhood and sigmaX=0 derives its spread
    # Smoothing can reduce small variations but retains shadows and broad reflections
    blurred = cv2.GaussianBlur(gray, BLUR_SIZE, sigmaX=0)
    # Keep the original and prepared arrays separate so later figures can show both
    # Both adaptive threshold calculations will receive the same blurred array from this dictionary
    return {"stem": stem, "title": title, "original_bgr": original,
            "scene_bgr": scene_bgr, "gray": gray, "blurred": blurred}
# ---

# __________________________________________
# ADAPTIVE THRESHOLDING
# ==========================================

# --- threshold_image()
def threshold_image(blurred: np.ndarray) -> dict[str, np.ndarray]:
    """Calculate the initial and revised adaptive masks.

    Args:
        blurred: Common single-channel uint8 image for this photograph.

    Returns:
        Initial and revised binary masks, each containing only 0 and 255.
        The revised mask is the final thresholding result.

    Logic:
        Adaptive Gaussian thresholding uses a weighted neighborhood mean
        minus C at each pixel. Inverse thresholding assigns 255 to values at
        or below the threshold. Both calculations start from the same input.
    """
    # ASSIGNMENT REQUIREMENT: Use adaptive thresholding with a local block size and C
    # INITIAL ADAPTIVE THRESHOLD
    # adaptiveThreshold() calculates a separate cutoff around each pixel
    # GAUSSIAN_C weights nearby intensities more strongly than distant intensities
    # The maximum output is 255, and THRESH_BINARY_INV selects locally darker pixels
    # INITIAL_BLOCK_SIZE is 31 and INITIAL_C subtracts 5 from the weighted mean
    # This small neighborhood follows fine details but leaves thin or broken regions
    initial = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
        INITIAL_BLOCK_SIZE, INITIAL_C,
    )
    # REVISED ADAPTIVE THRESHOLD
    # Start again from blurred so the revision retains the original intensity values
    # A wider 101 x 101 neighborhood produces more continuous local responses
    # C=10 requires a stronger darkness difference for a fixed local weighted mean
    # This balances some fragmentation against the selection of shadows and backdrop
    # Both settings change, so the comparison does not isolate their individual effects
    # The block sizes are odd and greater than one, as adaptiveThreshold() requires
    revised = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
        REVISED_BLOCK_SIZE, REVISED_C,
    )
    # Retain both masks for the comparison under each illumination direction
    # A white pixel meets the local threshold; it is not an identified mug pixel
    return {"initial_adaptive": initial, "revised_adaptive": revised}
# ---


# --- measure_masks()
def measure_masks(masks: dict[str, np.ndarray]) -> Measurements:
    """Count selected pixels and connected white regions in each mask.

    Args:
        masks: Initial and revised adaptive masks for the same photograph.

    Returns:
        White-pixel count, percentage of the full image, and connected-region
        count for each mask. These are descriptive measurements, not accuracy.

    Logic:
        Count nonzero pixels because the masks contain only 0 and 255. Use
        eight-connectivity, so diagonal white neighbors belong to one region.
        Subtract the background label from the connected-component total.
    """
    # The measurements describe the mask pixels, not which mug each pixel belongs to
    measurements: Measurements = {}
    # MAIN ITERATION LOOP: Visit the initial and revised masks in their calculation order
    # Each row describes one mask under one illumination direction
    for name, mask in masks.items():
        # count_nonzero() counts the 255-valued foreground pixels selected by this mask
        # It cannot tell whether a selected pixel is a mug, reflection, shadow, or backdrop
        white_pixels = int(np.count_nonzero(mask))
        # connectedComponents() groups white pixels that touch in any of eight directions
        # The first return value includes the black background as one label
        # Subtract one below to report foreground groups only
        component_count, _ = cv2.connectedComponents(mask, connectivity=8)
        measurements[name] = {
            "white_pixels": white_pixels,
            # Divide by all pixels in the resized photograph, not by a hand-selected mug
            "percent_image_white": 100.0 * white_pixels / mask.size,
            "connected_regions": int(component_count - 1),
        }
    return measurements
# ---

# __________________________________________
# TEACHING FIGURES - DISPLAY CALCULATED ARRAYS
# ==========================================

# The panels and overlays use the stored masks and do not calculate new thresholds

# --- make_overlay()
def make_overlay(scene_bgr: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Mark the selected local regions in cyan on a copy of the scene.

    Args:
        scene_bgr: Full resized BGR photograph.
        mask: Revised adaptive mask with selected pixels at 255.

    Returns:
        A BGR display copy with selected pixels blended with cyan.

    Logic:
        Leave the original array unchanged. Color indicates threshold selection;
        it does not label a mug or measure how well an object was recovered.
    """
    # copy() leaves the processed photograph unchanged for other saved panels
    overlay = scene_bgr.copy()
    # Select only the positions already marked white in the revised adaptive mask
    # This is a display overlay and does not assign pixels to the black or white mug
    selected = mask > 0
    # The weighted average blends 55% of the original pixel and 45% of cyan
    # [210, 205, 0] is cyan-like in OpenCV BGR channel order
    # round() then uint8 keeps display pixel values between 0 and 255
    overlay[selected] = np.round(
        0.55 * overlay[selected] + 0.45 * np.array([210, 205, 0]),
    ).astype(np.uint8)
    return overlay
# ---


# --- display_image()
def display_image(axis: Axes, image: np.ndarray, title: str) -> None:
    """Display an existing color, grayscale, or binary array.

    Args:
        axis: Matplotlib panel receiving the image.
        image: BGR color image or single-channel uint8 image.
        title: Short label explaining what the panel contains.

    Logic:
        Convert only the color display copy from BGR to RGB. Keep binary
        values on the 0-to-255 scale with no display interpolation.
    """
    # DISPLAY DECISION: Three dimensions mean a color image with BGR channels
    if image.ndim == 3:
        # Matplotlib expects RGB, so cvtColor() switches channel order for this panel
        # This does not change the original BGR image used by OpenCV
        axis.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:
        # Grayscale and binary masks have one channel, so use the gray color map
        # vmin/vmax preserve the 0-255 scale and nearest avoids smoothing mask boundaries
        axis.imshow(image, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    # Keep the panel label but hide coordinate axes so the image regions are easier to read
    axis.set_title(title, fontsize=10, pad=8)
    axis.set_axis_off()
# ---


# --- make_figure()
def make_figure(panels: list[tuple[np.ndarray, str]], rows: int, columns: int,
                heading: str) -> Figure:
    """Arrange labeled image panels beneath a teaching title.

    Args:
        panels: Stored image arrays and their panel labels, in reading order.
        rows: Number of panel rows.
        columns: Number of panel columns.
        heading: Figure-level teaching title.

    Returns:
        A Matplotlib figure ready to save and later display.

    Logic:
        Keep the area below the panels free of commentary and axis labels.
        A common layout makes the comparisons readable without changing
        any processing resolution.
    """
    # subplots() allocates the required panel grid; figsize affects the plot, not image data
    # squeeze=False keeps a two-dimensional axes array even for a single panel row
    figure, axes = plt.subplots(rows, columns, figsize=(5 * columns, 5.1 * rows),
                                squeeze=False, layout="constrained")
    # Keep room between panels for labels, including photographs of different heights
    figure.get_layout_engine().set(w_pad=0.12, h_pad=0.16, wspace=0.04, hspace=0.10)
    # DISPLAY LOOP: zip() matches each panel with one stored array and its title
    # display_image() shows the result but never calls an image-processing method
    for axis, (image, title) in zip(axes.flat, panels):
        display_image(axis, image, title)
    figure.suptitle(heading, fontsize=15, fontweight="bold")
    return figure
# ---


# --- build_figures()
def build_figures(scenes: list[SceneResult]) -> list[Figure]:
    """Build five teaching figures from the two stored result sets.

    Args:
        scenes: White-side illumination first, then black-side illumination.

    Returns:
        Five figures in the order listed in FIGURE_NAMES.

    Logic:
        Show preparation, the initial scheme under both lighting directions,
        the revised settings, and the final masks beside the original scenes.
        Displaying these arrays does not repeat or change thresholding.
    """
    # __________________________________________
    # DISPLAY STEP 1 OF 5: PREPARE BOTH PHOTOGRAPHS
    # ==========================================
    # Give each photograph a row with its original color and resized grayscale input
    # display_image() converts BGR to RGB only for the color display
    panels = []
    for scene in scenes:
        panels.extend(((scene["original_bgr"], f"{scene['title']}\nOriginal photograph"),
                       (scene["gray"], "Full scene: grayscale at 1,000 pixels wide")))
    figures = [make_figure(
        panels, 2, 2, "STEP 1/5: Prepare the two full scenes",
    )]
    # __________________________________________
    # DISPLAY STEPS 2-3 OF 5: TEST THE INITIAL SCHEME
    # ==========================================
    # MAIN ITERATION LOOP: Apply the same display layout to both lighting directions
    # The blurred image shows the intensity information used by the initial threshold
    for step, scene in enumerate(scenes, start=2):
        figures.append(make_figure(
            [(scene["blurred"], "Common blurred grayscale input"),
             (scene["masks"]["initial_adaptive"],
              f"Initial adaptive Gaussian: block {INITIAL_BLOCK_SIZE}, C = {INITIAL_C}")],
            1, 2, f"STEP {step}/5: {scene['title']}",
        ))
    # __________________________________________
    # DISPLAY STEP 4 OF 5: COMPARE THE ADAPTIVE REVISION
    # ==========================================
    # Keep the original, initial mask, and revised mask together for each photograph
    # This figure is also suitable for explaining the observed results in the paper
    panels = []
    for scene in scenes:
        panels.extend(((scene["scene_bgr"], f"{scene['title']}\nOriginal scene at processing size"),
                       (scene["masks"]["initial_adaptive"],
                        f"Initial: block {INITIAL_BLOCK_SIZE}, C = {INITIAL_C}"),
                       (scene["masks"]["revised_adaptive"],
                        f"Revised: block {REVISED_BLOCK_SIZE}, C = {REVISED_C}")))
    figures.append(make_figure(
        panels, 2, 3, "STEP 4/5: Apply one revision to both photographs",
    ))
    # __________________________________________
    # DISPLAY STEP 5 OF 5: EXAMINE THE FINAL MASKS
    # ==========================================
    # The revised adaptive mask is the final result without further processing
    # Cyan marks those same selected pixels on a copy of the color scene
    panels = []
    for scene in scenes:
        panels.extend(((scene["scene_bgr"], scene["title"]),
                       (scene["masks"]["revised_adaptive"], "Final revised adaptive mask"),
                       (scene["overlay_bgr"], "Cyan: selected local regions")))
    figures.append(make_figure(
        panels, 2, 3, "STEP 5/5: Compare the final adaptive masks",
    ))
    return figures
# ---

# __________________________________________
# TERMINAL EXPLANATIONS - FIVE TEACHING STEPS
# ==========================================

# The following functions prepare text from masks that have already been calculated
# There is one explanation for each display step, but no new thresholding passes here

# --- measurement_table()
def measurement_table(scene: SceneResult, names: tuple[str, ...]) -> str:
    """Format a compact table from measurements already calculated.

    Args:
        scene: One scene with its measured mask results.
        names: Mask names to include in table order.

    Returns:
        An indented table with pixel counts, coverage, and connected regions.

    Logic:
        Read measured data directly; do not type expected values into the guide.
    """
    # Build a fixed-width table so its columns remain aligned in the terminal
    # The same calculated values are saved in measurements.csv
    lines = ["    Mask                  White pixels    Image %    Regions"]
    # TABLE LOOP: Read the selected mask names in the requested comparison order
    # The counts come from measure_masks(), not from numbers typed into the paper
    for name in names:
        values = scene["measurements"][name]
        lines.append(f"    {name:<22} {values['white_pixels']:>11,}"
                     f" {values['percent_image_white']:>10.4f}"
                     f" {values['connected_regions']:>10,}")
    return "\n".join(lines)
# ---


# --- build_walkthrough()
def build_walkthrough(scenes: list[SceneResult]) -> GuideSteps:
    """Explain the experiment using its actual images, settings, and counts.

    Args:
        scenes: Both photographs with completed processing and measurements.

    Returns:
        Five lists of paragraphs for the terminal and saved transcript.

    Logic:
        Describe what the methods select and where the results remain limited.
        Keep observations distinct from accuracy and generalization claims.
    """
    # Record both original resolutions and their resized dimensions for Step 1
    # MEASUREMENT LOOP: One set of image dimensions is prepared for each lighting view
    dimensions = []
    for scene in scenes:
        oh, ow = scene["original_bgr"].shape[:2]
        height, width = scene["gray"].shape
        dimensions.append(f"{scene['title']}: original {ow} x {oh} pixels; "
                          f"processed {width} x {height} pixels.")
    # Read the installed library versions during this execution rather than
    # claiming that the versions listed in the assignment were used here
    versions = (f"This run uses Python {sys.version.split()[0]}; "
                f"OpenCV {cv2.__version__}; NumPy {np.__version__}; "
                f"Matplotlib {matplotlib.__version__}.")
    # __________________________________________
    # TEACHING STEP 1 OF 5: PREPARE BOTH FULL SCENES
    # ==========================================
    # Explain grayscale conversion, smoothing, image dimensions, and the
    # difference between real reflected objects, cast shadows, and image noise
    # The text below is for the terminal, not another image-processing pass
    guide: GuideSteps = [[
        "This assignment examines two mugs under different lighting conditions. "
        "One mug is glossy black, and the other is light-colored with raised "
        "flowers. Both sit on a light tabletop in front of a dark background. "
        "The first photograph is lit from the white mug's side. In the second, "
        "the light comes from the black mug's side. The goal is to see whether "
        "the same adaptive thresholding settings still work after that change.",
        *dimensions,
        "In load_and_prepare(), cv2.resize() reduces both photographs to 1,000 "
        "pixels wide while keeping their original proportions. Neither image "
        "is cropped, so the mugs, tabletop, background, and shadows all remain. "
        "The first view shows the original photographs beside their grayscale versions.",
        "OpenCV reads color in BGR order, meaning blue, green, and red. Then "
        "cv2.cvtColor() gives each pixel one brightness value instead of three "
        "color values. The grayscale image uses uint8 values from 0, black, "
        "to 255, white. A 5 x 5 Gaussian blur reduces small brightness "
        "variations before thresholding. With sigmaX=0, OpenCV calculates "
        "sigma from the kernel size. Both adaptive calculations use this same "
        "blurred grayscale input for each photograph.",
        "The blur does not remove the larger shadows or the reflections on the "
        "black mug. Look at its bright patches and the flowers on the white mug. "
        "These are details in the scene, and they also change the brightness "
        "values. Treating all of them as random noise would miss part of the problem.",
        versions,
    ]]
    # __________________________________________
    # TEACHING STEPS 2-3 OF 5: TEST THE INITIAL THRESHOLD
    # ==========================================
    # EXPLANATION LOOP: First explain the photograph lit from the white mug side
    # then use the SAME initial adaptive settings on the black-side photograph
    # Each table describes the initial adaptive mask for one photograph
    # Give the second view its own explanation of the lighting change
    for index, scene in enumerate(scenes):
        # These descriptions introduce the current picture without changing its data
        # Step 2 explains the first attempt; Step 3 checks it on the second photograph
        introduction = (
            "Start with the photograph lit from the white mug's side. The left "
            "panel shows the blurred grayscale input, and the right panel shows "
            "the initial adaptive image. Look at the rims, handles, and raised "
            "flowers to see which details remain visible."
            if index == 0 else
            "Now look at the photograph lit from the black mug's side. The "
            "program uses the same preparation and initial thresholding settings "
            "as in Step 2. Compare the right panel with the previous result, "
            "particularly around the black mug's reflections and the tabletop shadows."
        )
        observation = (
            "Some of the mug boundaries are visible, although several areas "
            "remain thin or disconnected. The black mug's bright reflections "
            "interrupt parts of its outline. The white mug has a different "
            "problem: parts of its boundary are close in brightness to the tabletop."
            if index == 0 else
            "Changing the light affects which parts of the mugs appear in the "
            "binary image. The same settings still pick up some boundaries, "
            "but they do not separate both mugs completely from their surroundings. "
            "The next step revises the settings and checks both photographs again."
        )
        # Explain the method in Step 2 and recall its settings briefly in Step 3
        # The second photograph tests the same scheme without changing its parameters
        method_explanation = (
            "Adaptive thresholding calculates a separate cutoff for each pixel "
            "using the brightness of its neighbors. Here, "
            "ADAPTIVE_THRESH_GAUSSIAN_C calculates a weighted local average "
            "and subtracts C. The initial settings are blockSize=31 and C=5, "
            "so the program examines a 31 x 31 window and subtracts 5 from "
            "that average. THRESH_BINARY_INV makes pixels at or below their "
            "threshold white (255), while brighter pixels become black (0)."
            if index == 0 else
            "The settings remain ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, "
            "blockSize=31, and C=5. Each pixel is still compared with its "
            "weighted local average minus 5. Values at or below that cutoff "
            "become white (255); brighter values become black (0)."
        )
        # Relate the white pixels to the current scene before showing its measured counts
        selection_explanation = (
            "A white pixel does not necessarily belong to a mug. It only means "
            "that the pixel met its local threshold. For example, a shadow on "
            "the tabletop can be selected along with a dark part of a handle. "
            "The table counts those selected pixels and their connected regions."
            if index == 0 else
            "The black mug can still contain bright reflections, while the "
            "tabletop contains dark shadows. This is why changing the light "
            "does not make every selected region part of a mug. The table "
            "describes the pixels selected in this second photograph."
        )
        guide.append([
            introduction,
            method_explanation,
            selection_explanation,
            measurement_table(scene, ("initial_adaptive",)),
            observation,
        ])
    # __________________________________________
    # TEACHING STEP 4 OF 5: REVISE THE SETTINGS
    # ==========================================
    # Describe the 101 x 101/C=10 revision and the results on BOTH photographs
    # Also state that fewer connected regions do not confirm accurate segmentation
    guide.append([
        "The initial results leave several boundaries thin or disconnected. "
        "For the revision, the window increases to 101 x 101 and C changes "
        "to 10. Both photographs use these new settings. The program starts "
        "again from each blurred grayscale image, so the revised result is "
        "calculated independently of the initial binary image.",
        "The larger window includes a wider area when calculating the local "
        "average. Increasing C lowers the threshold, which selects fewer white "
        "pixels if that average stays the same. However, the window also changes "
        "here, so its average can change too. This comparison shows their "
        "combined effect; it cannot tell us how much each setting contributed.",
        scenes[0]["title"] + ".\n" + measurement_table(
            scenes[0], ("initial_adaptive", "revised_adaptive")),
        scenes[1]["title"] + ".\n" + measurement_table(
            scenes[1], ("initial_adaptive", "revised_adaptive")),
        "Read across each row of the figure to compare the original photograph, "
        "initial result, and revised result. Several white regions become "
        "wider and more continuous, making parts of the rims and handles "
        "easier to follow. At the same time, more of the shadows and the dark "
        "backdrop are selected. The improvement is not the same throughout the images.",
        "The tables show more white pixels and fewer connected regions in both "
        "revised images. Some smaller regions may have disappeared, while others "
        "may have joined together. Those changes also occur in the background, "
        "so the numbers alone do not show whether the mugs were separated more accurately.",
    ])
    # __________________________________________
    # TEACHING STEP 5 OF 5: EXAMINE THE RESULTS AND LIMITATIONS
    # ==========================================
    # Relate the revised masks to the original mugs, backdrop, and cast shadows
    # The final images are direct adaptive outputs and have no later processing
    guide.append([
        "The final comparison brings both lighting directions together. Each "
        "row shows the color photograph, the revised adaptive image, and a "
        "cyan overlay. The revised adaptive image is the final result. The "
        "overlay simply marks those same selected pixels on the photograph.",
        "Look at where the cyan areas fall. Some follow the mugs' rims and "
        "handles, but others include shadows on the tabletop and bands near "
        "the dark backdrop. The boundaries are easier to follow in some areas, "
        "although neither photograph gives a complete separation of both mugs.",
        "The black mug remains difficult because its glossy surface reflects "
        "light and objects around it. Those bright patches still belong to the "
        "mug. Meanwhile, parts of the white mug have brightness values close to "
        "the tabletop. Even the space inside a handle contains background that "
        "can look similar to the handle itself. The raised flowers create "
        "additional brightness changes. A local threshold cannot tell what "
        "produced all of these differences.",
        "In measure_masks(), np.count_nonzero() counts the white pixels. Image % "
        "shows how much of the full processed image they cover. Connected "
        "regions are groups of white pixels that touch horizontally, vertically, "
        "or diagonally. These measurements help describe the result, but they "
        "cannot tell whether the selected pixels actually belong to either mug. "
        "Without manually labeled reference masks, segmentation accuracy cannot "
        "be calculated.",
        "Another consideration is that the photographs have different dimensions "
        "and framing. Resizing them to the same width does not make the scenes "
        "identical, so differences between their measurements cannot be "
        "attributed to illumination alone. Both photographs were also examined "
        "when choosing the revision. This shows how the settings work on these "
        "two images; it does not establish how they will work on a new photograph.",
        "For these photographs, the revised settings make several boundaries "
        "more continuous, but they also include more background. That is the "
        "remaining problem with separating the mugs using brightness alone.",
    ])
    # All five lists contain terminal paragraphs, not five new processing passes
    # format_step() uses these same paragraphs for the live and saved explanations
    return guide
# ---

# __________________________________________
# TERMINAL FORMATTING AND SAVED RESULTS
# ==========================================

# --- style_text()
def style_text(message: str, style: str = "", *, stream: TextIO | None = None) -> str:
    """Add color when the destination supports terminal formatting.

    Args:
        message: Text to format.
        style: Name in TEXT_STYLES, or an empty string for plain output.
        stream: Output stream checked for terminal support.

    Returns:
        The message with optional color codes and an immediate reset.
    """
    # Check the actual output destination because redirected text should stay plain
    output = sys.stdout if stream is None else stream
    # DISPLAY DECISION: Leave messages unchanged for files, inactive color styles
    # NO_COLOR, or a dumb terminal that cannot interpret ANSI escape codes
    if (not style or not output.isatty() or os.environ.get("NO_COLOR")
            or os.environ.get("TERM", "").lower() == "dumb"):
        return message
    # Add color only for a supported terminal and reset it after this message
    # Unknown style names leave the original text unchanged
    code = TEXT_STYLES.get(style, "")
    return f"{code}{message}{TEXT_RESET}" if code else message
# ---


# --- format_step()
def format_step(step: int, paragraphs: list[str], *, color: bool = False) -> str:
    """Format one teaching step for the terminal and saved transcript.

    Args:
        step: Teaching step from 1 through 5.
        paragraphs: Explanations and measurement tables for that step.
        color: Request supported terminal colors.

    Returns:
        One complete step with its heading, text, and matching figure names.

    Logic:
        Wrap prose while preserving indented measurement tables.
        The transcript and live guide use the same explanatory text.
    """
    # StringIO collects the complete formatted step before the guide prints or saves it
    result = io.StringIO()
    rule = style_text("=" * 88, "rule" if color else "")
    result.write(f"\n{rule}\n")
    result.write(style_text(f"STEP {step}/5: {STAGE_TITLES[step - 1]}",
                            "heading" if color else "") + "\n")
    result.write(rule + "\n\n")
    # OUTER LOOP: Read each paragraph belonging to the current teaching step
    # The stored order matches the corresponding figure and its explanation
    for paragraph in paragraphs:
        # INNER LOOP: Preserve line breaks inserted for the numerical tables and matrix
        # Lines starting with four spaces stay aligned rather than being rewrapped
        for line in paragraph.splitlines():
            wrapped = (line if line.startswith("    ") else textwrap.fill(
                line, width=88, break_long_words=False, break_on_hyphens=False,
            ))
            # Apply optional terminal color only AFTER wrapping the line to its width
            result.write(style_text(wrapped, "info" if color else "") + "\n")
        result.write("\n")
    # FIGURE LIST LOOP: Each of the five steps has one matching view
    # The printed paths refer to the saved files, not new figures created here
    for index in STAGE_FIGURES[step - 1]:
        result.write(f"Saved teaching view: figures/{FIGURE_NAMES[index]}\n")
    return result.getvalue()
# ---


# --- save_results()
def save_results(output_directory: Path, scenes: list[SceneResult],
                 figures: list[Figure], walkthrough: GuideSteps) -> None:
    """Save all derived images, figures, measurements, and explanations.

    Args:
        output_directory: Destination selected by the command-line options.
        scenes: Both complete processing result sets.
        figures: Five teaching figures in their declared order.
        walkthrough: The complete five-step explanation.

    Raises:
        OSError: If an output image or other file cannot be written.

    Logic:
        Save before opening any guide window. Each photograph has its own
        image subfolder, while one CSV and transcript cover the experiment.
    """
    # __________________________________________
    # PREPARE THE OUTPUT FOLDERS
    # ==========================================
    # Keep derived files in mod_images/ so the original JPEGs remain unchanged
    # parents=True creates missing folders and exist_ok=True permits a repeat run
    output_directory.mkdir(parents=True, exist_ok=True)
    figure_directory = output_directory / "figures"
    figure_directory.mkdir(exist_ok=True)
    # __________________________________________
    # SAVE THE PROCESSED IMAGES AND COLLECT MEASUREMENTS
    # ==========================================
    # OUTER LOOP: Save one set of arrays in each illumination-specific subfolder
    # The source photographs remain in org_images/ and are never overwritten
    rows = []
    for scene in scenes:
        scene_directory = output_directory / scene["stem"]
        scene_directory.mkdir(exist_ok=True)
        # Include the resized color, grayscale, blurred image, all masks, and the overlay
        # The color overlays are display results; binary PNGs retain their 0/255 values
        images = {"resized_color": scene["scene_bgr"], "grayscale": scene["gray"],
                  "blurred": scene["blurred"], **scene["masks"],
                  "final_overlay": scene["overlay_bgr"]}
        # PNG preserves the binary values without introducing JPEG artifacts
        # INNER SAVE LOOP: Write each calculated array as a separate PNG image
        # str(path) gives imwrite() a filename; the extension selects PNG encoding
        for name, image in images.items():
            path = scene_directory / f"{name}.png"
            # Error check: imwrite() returns False if OpenCV cannot write this image
            # Raise the filename instead of claiming that the complete run was saved
            if not cv2.imwrite(str(path), image):
                raise OSError(f"Could not save the output image: {path}")
        height, width = scene["gray"].shape
        # MEASUREMENT LOOP: Append one CSV row for each adaptive mask
        # Keep image dimensions and adaptive settings beside the measured values
        for name, values in scene["measurements"].items():
            rows.append({"scene": scene["stem"], "mask": name,
                         "width": width, "height": height,
                         "block_size": (INITIAL_BLOCK_SIZE if name == "initial_adaptive"
                                        else REVISED_BLOCK_SIZE),
                         "constant_c": INITIAL_C if name == "initial_adaptive" else REVISED_C,
                         **values})
    # __________________________________________
    # SAVE ALL FIVE TEACHING FIGURES
    # ==========================================
    # FIGURE LOOP: zip() assigns the matching filename to each Matplotlib figure
    # savefig() saves the titles and panels; DPI affects the figure, not mask pixels
    for figure, name in zip(figures, FIGURE_NAMES):
        figure.savefig(figure_directory / name, dpi=FIGURE_DPI)
    # __________________________________________
    # SAVE THE MEASUREMENT TABLE
    # ==========================================
    # newline="" prevents extra blank CSV rows on systems with newline translation
    # Use the fields already calculated for the first row as the common column names
    with (output_directory / "measurements.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        # TABLE LOOP: writerows() writes every row using the same CSV column order
        writer.writerows(rows)
    # __________________________________________
    # SAVE THE COMPLETE TERMINAL EXPLANATION
    # ==========================================
    # All five explanations are saved before the first window is opened
    # Quitting with Q during the live walkthrough does not discard this file
    with (output_directory / "terminal_output.txt").open("w", encoding="utf-8") as stream:
        stream.write("CSC515 Module 6 - Adaptive Thresholding Under Changing Illumination\n")
        # EXPLANATION LOOP: Write Steps 1 through 5 with the same text used live
        # The saved transcript contains no ANSI color codes
        for step, paragraphs in enumerate(walkthrough, start=1):
            stream.write(format_step(step, paragraphs))
# ---

# __________________________________________
# TEACHING CONTROLS - WINDOWS AND TERMINAL INPUT
# ==========================================

# On macOS, the input reader waits for text while the main thread updates the figures
# The reader only sends C/Q through the queue and never calls Matplotlib itself

# --- wait_for_guide_command()
def wait_for_guide_command(figure: Figure, final_step: bool = False) -> str:
    """Read C or Q while keeping the current figure responsive.

    Args:
        figure: Current Matplotlib figure.
        final_step: True when only Q is accepted at the last view.

    Returns:
        The accepted uppercase command C or Q.

    Logic:
        A reader thread handles terminal input. Only the main thread processes
        figure events, matching the Module 5 desktop walkthrough.
    """
    # The queue transfers terminal input to the main thread without touching figures
    # The main thread remains responsible for all Matplotlib window events
    commands: queue.Queue[str] = queue.Queue()
    # The last view accepts Q only because there is no next view
    prompt = ("Enter Q to finish, then press Enter: " if final_step else
              "Enter C to continue or Q to quit, then press Enter: ")

    # --- read_command()
    def read_command() -> None:
        """Pass one terminal command to the main thread without drawing figures.

        End of input or an unreadable stream is treated as Q. Reading through
        stdin avoids invoking a desktop input hook in the worker thread.
        """
        try:
            # Read the terminal line without invoking a Matplotlib input hook
            # readline() waits for Enter and upper() accepts lowercase and uppercase C/Q
            line = sys.stdin.readline()
            commands.put(line.strip().upper() if line else "Q")
        except OSError:
            # An unreadable terminal stream is treated as Q to stop the guide safely
            commands.put("Q")
    # ---

    # VALIDATION LOOP: Keep asking until C or Q is entered for the current view
    # Rejected commands must not open the next image or close the current one
    while True:
        print(style_text(prompt, "prompt"), end="", flush=True)
        # The reader thread waits for text while the figure event loop stays responsive
        threading.Thread(target=read_command, daemon=True).start()
        # WAIT LOOP: Process just this figure's events for 50 milliseconds at a time
        # Using the current canvas avoids opening later figures before their turn
        while commands.empty():
            figure.canvas.start_event_loop(0.05)
        command = commands.get()
        # COMMAND DECISION: Q stops at any view, but C continues only before the last
        if command == "Q" or (command == "C" and not final_step):
            return command
        # Otherwise the entered command is invalid, so show the choices again
        print(style_text("Please enter Q." if final_step else "Please enter C or Q.",
                         "example"), flush=True)
# ---


# --- run_walkthrough()
def run_walkthrough(walkthrough: GuideSteps, figures: list[Figure],
                    no_show: bool, no_pause: bool) -> None:
    """Print five explanations and present their five matching figures.

    Args:
        walkthrough: Five completed teaching explanations.
        figures: Five figures already saved to disk.
        no_show: Print without opening desktop windows.
        no_pause: Display without waiting for terminal commands.

    Logic:
        Each step shows one figure. The last view compares the revised masks
        with the original scenes and their selected pixels. Q ends the
        walkthrough without deleting or changing any saved results.
    """
    # MAIN ITERATION LOOP: Print all five steps with the same text saved to the transcript
    # The figures were built earlier, so no image-processing operation runs here
    for step, paragraphs in enumerate(walkthrough, start=1):
        print(format_step(step, paragraphs, color=True), flush=True)
        # DISPLAY DECISION: --no-show prints the explanations but skips desktop windows
        # Continue with the next step so the complete guide is still printed
        if no_show:
            continue
        # DISPLAY LOOP: Use the mapping in STAGE_FIGURES to select the saved views
        # One figure belongs to each explanation in the five-step guide
        for index in STAGE_FIGURES[step - 1]:
            figure = figures[index]
            figure.show()
            figure.canvas.start_event_loop(0.05)
            # INTERACTIVE DECISION: Ask for C/Q only when terminal pauses are enabled
            if not no_pause:
                command = wait_for_guide_command(figure, final_step=index == len(figures) - 1)
                # Q closes the open figures and stops the guide without deleting files
                if command == "Q":
                    plt.close("all")
                    return
                # C closes only the current window before continuing to the next view
                plt.close(figure)
    # OTHERWISE: --no-pause leaves opened desktop views available until they are closed
    # Do not request terminal input in this mode
    if not no_show and no_pause:
        plt.show()
    plt.close("all")
# ---

# _________________________________________________________
# MAIN FUNCTION - Interface of the program (entry point)
# =======================================================

# --- main()
def main() -> int:
    """Process both photographs, save their results, and present the guide.

    Returns:
        0 for completion or Q, 1 for an input/output or OpenCV error, and 130
        when the user interrupts the program with Ctrl+C.

    Logic:
        Keep image processing separate from measurement and display. Save all
        results before opening the first window so the full experiment remains
        available even when the walkthrough is stopped early.
    """
    # Read display options before loading either photograph
    args = parse_arguments()
    # A noninteractive Agg backend can save the Matplotlib figures without a desktop
    if args.no_show:
        plt.switch_backend("Agg")
    # Disable automatic windows so every result can be built and saved first
    plt.ioff()
    try:
        scenes = []
        # __________________________________________
        # IMAGE CALCULATIONS FOR BOTH ILLUMINATION DIRECTIONS
        # ==========================================
        # ASSIGNMENT REQUIREMENT: Use one adaptive scheme for the two lighting directions
        # MAIN PROCESSING LOOP: Prepare each full photograph and calculate both
        # adaptive masks from its blurred grayscale input
        # No method uses the other photograph's pixels as input
        for stem, title in SCENES:
            # PHASE 1: Resize, convert to grayscale, and apply the same Gaussian blur
            scene = load_and_prepare(stem, title)
            # PHASE 2: Calculate the initial and revised adaptive thresholds independently
            # Both photographs receive the same neighborhood and C at each stage
            masks = threshold_image(scene["blurred"])
            scene["masks"] = masks
            # PHASE 3: Count selected pixels and connected regions in each stored mask
            # Measurements describe the masks without claiming object-recognition accuracy
            scene["measurements"] = measure_masks(masks)
            # PHASE 4: Blend the final adaptive selection with the color scene for display
            # The overlay marks the revised mask without changing its binary pixels
            scene["overlay_bgr"] = make_overlay(scene["scene_bgr"], masks["revised_adaptive"])
            # Keep this photograph's results so the later figures can compare both
            scenes.append(scene)
        # __________________________________________
        # BUILD THE FIVE FIGURES AND FIVE EXPLANATIONS
        # ==========================================
        # Draw the teaching views from stored arrays, not new threshold calculations
        # The guide describes the real masks and their measured limitations
        figures = build_figures(scenes)
        walkthrough = build_walkthrough(scenes)
        # __________________________________________
        # SAVE ALL RESULTS BEFORE OPENING ANY TEACHING VIEWS
        # ==========================================
        # Save PNGs, the CSV, and the full terminal explanation before C/Q navigation
        save_results(args.output_dir, scenes, figures, walkthrough)
        print(style_text("CSC515 Module 6 - Adaptive Thresholding Under Changing Illumination",
                         "heading"))
        print(style_text("All images, measurements, and explanations were saved before the guide.",
                         "success"))
        # __________________________________________
        # PRESENT THE FIVE TEACHING STEPS
        # ==========================================
        # The figures and text are already saved, so leaving early does not lose them
        run_walkthrough(walkthrough, figures, args.no_show, args.no_pause)
        print(style_text(f"\nSaved results: {args.output_dir.resolve()}", "success"))
        return 0
    except (OSError, cv2.error) as error:
        # Error check: Report a failed image read, operation, or output write
        # Show the underlying error instead of printing a success message
        print(style_text(f"The program could not finish: {error}", "error", stream=sys.stderr),
              file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Ctrl+C stops the walkthrough with status 130 and preserves saved files
        print("\nThe walkthrough was stopped.", file=sys.stderr)
        return 130
    finally:
        # CLEANUP: Close Matplotlib figures after normal completion or an error
        plt.close("all")
# ---


# __________________________________________
# MODULE INITIALIZATION
# ==========================================

# Initialize and start the program
if __name__ == "__main__":
    raise SystemExit(main())

# __________________________________________
# END OF FILE
# ==========================================
