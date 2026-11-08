#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Module Type: executable script
# Author: Alexander Ricciardi (Omega.py)
# Created: 2026-10-28
# -----------------------------------------------------------------------------
# Course: Foundations of Computer Vision CSC515
# Professor: Dr. Bingdong Li
# Term: Fall C (26FC) - 2026
# Assignment: Portfolio Project Module 8 - Option #2: Face Detection and Privacy
# -----------------------------------------------------------------------------
# The Program
# Read a human portrait, a full-body group photograph, and a photograph of a cat
# Compare human-face Haar cascades on grayscale versions of all three photographs
# Keep the initial detections, including extra boxes, beside the revised results
# Extract faces from the original color images and estimate an initial eye pair
# Rotate, scale, and center each face before running the eye classifier again
# Compare two Gaussian blur strengths and return the eye regions to the full scene
# Save the images, measurements, and seven teaching stages in mod_images/
# Enter C to close the current view and continue, or Q to quit, then press Enter
# All results are saved before the first view; --no-show runs without windows
# -----------------------------------------------------------------------------
# Requirements
# - Python 3.12 or later; verified with Python 3.12.13
# - OpenCV 4.13.0 (opencv-contrib-python==4.13.0.92)
# - NumPy 2.5.3 and Matplotlib 3.11.2
# - Keep the three supplied original photographs in org_images/
# - Install dependencies with python -m pip install -r requirements.txt
#
# Run from this folder
#    python Module8_Portfolio_Option2.py
#    python Module8_Portfolio_Option2.py --no-show
#
# Dependencies
# - cv2, numpy, matplotlib, and matplotlib.pyplot
# - argparse, csv, hashlib, io, json, math, os, pathlib, queue, sys, textwrap
# - threading, time, and typing
#
# Contents Overview
# - parse_arguments() / load_cascades() / load_and_prepare()
#   - Check options, pretrained classifiers, and unchanged source photographs
# - detect_faces() / run_face_experiments()
#   - Preserve six face-detection experiments without using reference annotations
# - detect_eye_candidates() / select_eye_pair() / find_eye_pair() / align_face()
#   - Work inside extracted faces and keep the two eye-detection stages separate
# - blur_eyes() / restore_eye_regions() / process_faces()
#   - Blur accepted eye regions and preserve all pixels outside their masks
# - match_face_boxes() / measure_results()
#   - Compare calculated results with separately marked visual reference locations
# - build_figures() / build_walkthrough() / save_results()
#   - Present stored results and retain the complete experiment before display
# - wait_for_guide_command() / run_walkthrough() / main()
#   - Present the C/Q guide and coordinate the program
# -----------------------------------------------------------------------------

"""Detect human faces and obscure their eyes in three web photographs.

The cat is the nonhuman example, not a subject whose eyes should be located with
an animal classifier. All three images enter the same human-face detector. The
reference labels never suppress detections or supply missing eye coordinates.

This is a small development experiment. The images were inspected while choosing
settings, and the visual reference marks are approximate, not an expert-labeled
benchmark. Eye coverage, eye-center localization, and face detection are measured
separately. Blurring the eyes does not establish that a person is anonymous.

Methods: OpenCV 4.13.0 cascade and geometric-transformation tutorials. Source
links, image credits, and links to the accompanying APA paper are in README.md.
"""

# ____________________________________________________________________________________
# ====================================================================================
# IMAGE REPRESENTATIONS AND PROCESSING
#
# original_bgr: untouched uint8 color photograph, with blue, green, and red channels
# gray: original-resolution grayscale photograph with one intensity value per pixel
# detection_gray: grayscale input for one particular face experiment
# face_box: (x, y, width, height) in the ORIGINAL photograph
# crop_bgr: clean face region extracted from original_bgr, not a red-box display
# normalized_bgr: aspect-preserving face resize used for the provisional eye search
# aligned_bgr: 320 x 320 face after rotation, uniform scaling, and translation
# aligned_mask / scene_mask: uint8 treatment masks, with selected pixels at 255
# NumPy selects pixels with [y, x]; OpenCV boxes start with x, then y
#
# original color --> grayscale --> six face experiments --> selected face boxes
# original color + selected boxes --> clean crops --> provisional eye pair
# clean crop + eye pair --> aligned face --> NEW eye detection --> eye blur
# aligned blur + inverse transform --> original-size eye treatment --> final scene
#
# REFERENCE ANNOTATIONS ARE USED ONLY AFTER THESE CALCULATIONS
# They measure errors but never place, align, or blur an eye
# Displaying a figure does not repeat any face or eye detection
# ====================================================================================

# __________________________________________
# IMPORTS
# ==========================================

import argparse  # For paths, --help, and the display controls
import csv  # For the face, eye, and processing measurements
import hashlib  # For checking the exact source images and loaded XML files
import io  # For collecting the saved terminal explanations
import json  # For source records, settings, boxes, and transformation matrices
import math  # For the eye-line angle and Gaussian kernel size
import os  # For checking terminal color preferences
from pathlib import Path  # For paths relative to this script
import queue  # For passing terminal commands to the main thread
import sys  # For the installed Python version and exit status
import textwrap  # For readable terminal paragraphs
import threading  # For input without blocking Matplotlib events
import time  # For recording elapsed detector time
from typing import Any, TextIO  # For result dictionaries and output streams

import cv2  # Computer Vision Library
import matplotlib  # For the installed version and backend information
import matplotlib.pyplot as plt  # For the teaching figures and desktop windows
import numpy as np  # For images, coordinates, and pixel measurements
from matplotlib.axes import Axes  # For figure-panel type hints
from matplotlib.figure import Figure  # For figure type hints

# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

# Keep the input and output folders next to this Python file
# The program can run from another terminal folder without losing the image paths
ASSIGNMENT_DIRECTORY = Path(__file__).resolve().parent
INPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "org_images"
OUTPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "mod_images"
FIGURE_DPI = 130
# These sizes control saved figure previews and the separate eye searches
# Changing a display size does not resize the final original photograph
DISPLAY_MAX_EDGE = 1000
EYE_SEARCH_EDGE = 300
ALIGNED_EDGE = 320
# The eye targets are positions in the aligned canvas, not image annotations
# The two target positions place the eyes on the same horizontal line
# Both points are measured on the 320 by 320 aligned face
TARGET_EYES = np.array([[96.0, 121.6], [224.0, 121.6]], dtype=np.float64)
FACE_IOU_THRESHOLD = 0.50
# The reference measurements use one minimum overlap and one eye center tolerance
# These values help evaluate the results and do not guide the detector
EYE_ERROR_FRACTION = 0.10
EYE_ERROR_MINIMUM = 2.0
INITIAL_EYE_PADDING = 0.35
EYE_PADDING = 0.60
WEAK_SIGMA_FRACTION = 0.10
FINAL_SIGMA_FRACTION = 0.45

# Keep one fixed final configuration for all images, including the cat
# These are development choices, not settings selected separately for each input
# Each dictionary holds the settings for one face detection experiment
# The same six settings are tested on each original photograph
# A smaller maximum edge is used only in the experiments that request it
EXPERIMENTS = (
    {"name": "01_default_native", "cascade": "face_default", "preprocessing": "gray",
     "max_edge": None, "scale_factor": 1.1, "min_neighbors": 5, "min_size": 24},
    {"name": "02_alt_native", "cascade": "face_alt", "preprocessing": "gray",
     "max_edge": None, "scale_factor": 1.1, "min_neighbors": 5, "min_size": 24},
    {"name": "03_alt_scaled", "cascade": "face_alt", "preprocessing": "gray",
     "max_edge": 1000, "scale_factor": 1.1, "min_neighbors": 5, "min_size": 24},
    {"name": "04_alt_equalized", "cascade": "face_alt", "preprocessing": "equalized",
     "max_edge": 1000, "scale_factor": 1.1, "min_neighbors": 5, "min_size": 24},
    {"name": "05_alt_clahe", "cascade": "face_alt", "preprocessing": "clahe",
     "max_edge": 1000, "scale_factor": 1.1, "min_neighbors": 5, "min_size": 24},
    {"name": "06_alt_stricter", "cascade": "face_alt", "preprocessing": "gray",
     "max_edge": 1000, "scale_factor": 1.1, "min_neighbors": 7, "min_size": 24},
)
# Use the third experiment for extracting faces after the comparison
# Keep the earlier and later experiments so the results can still be examined
FINAL_EXPERIMENT = "03_alt_scaled"
# These names select the trained XML files supplied with OpenCV
# Face classifiers and eye classifiers are loaded separately
CASCADE_FILES = {
    "face_default": "haarcascade_frontalface_default.xml",
    "face_alt": "haarcascade_frontalface_alt.xml",
    "eye": "haarcascade_eye.xml",
    "eyeglasses": "haarcascade_eye_tree_eyeglasses.xml",
}

# Read original files from the earlier image-selection package without redownloading
# Hash checks prevent the reference coordinates from silently scoring another image
# Record the exact photographs used for the assignment
# Their dimensions and SHA256 values stop a different file from being used by mistake
SOURCES = (
    {"stem": "eileen_collins", "file": "eileen_collins.jpg", "title": "Human portrait",
     "width": 2615, "height": 3269,
     "sha256": "752846bd7bc6496b66ee4aebf1799635b676ba15b2c06adb6cf7be6da1eb91bb",
     "credit": "NASA; Commons also credits Robert Markowitz",
     "source": "https://images.nasa.gov/details/S99-00858",
     "role": "Front-facing person, indoor lighting, and a close face"},
    {"stem": "sts133_arrival", "file": "sts133_arrival.jpg", "title": "Full-body group",
     "width": 3000, "height": 1996,
     "sha256": "d833243b9d7bdc0081636703c2ee6b652fc45fb8e5c96887e3ab81d7abeabf28",
     "credit": "NASA/Kim Shiflett",
     "source": "https://images.nasa.gov/details/KSC-2011-1515",
     "role": "Six front-facing people, entire bodies, small faces, and outdoor light"},
    {"stem": "chelsea", "file": "chelsea.png", "title": "Cat: nonhuman example",
     "width": 451, "height": 300,
     "sha256": "596aa1e7cb875eb79f437e310381d26b338a81c2da23439704a73c4651e8c4bb",
     "credit": "Stefan van der Walt; CC0",
     "source": "https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.chelsea",
     "role": "Nonhuman subject, brown fur, and softer shading"},
)

# These approximate visual marks were placed on the unchanged source photographs
# Face boxes follow the visible face from forehead to chin, excluding most hair
# Eye centers mark the visible opening; eye_regions cover the visible lids and opening
# Faces and eyes are numbered from IMAGE LEFT to IMAGE RIGHT, not by a person's side
# Neither detect_faces(), process_faces(), nor find_eye_pair() reads this reference set
# These marks describe the visible faces and eyes in the original photographs
# They are used after processing to measure errors rather than to find the eyes
REFERENCE_ANNOTATIONS = {
    "eileen_collins": [
        {"id": "P1", "box": [875, 580, 515, 530],
         "eyes": [[1013, 711], [1237, 729]],
         "eye_regions": [[959, 690, 105, 48], [1180, 712, 109, 48]]},
    ],
    "sts133_arrival": [
        {"id": "G1", "box": [533, 747, 101, 112],
         "eyes": [[558, 795], [595, 788]],
         "eye_regions": [[550, 789, 19, 10], [587, 782, 20, 10]]},
        {"id": "G2", "box": [816, 711, 102, 113],
         "eyes": [[845, 737], [889, 740]],
         "eye_regions": [[835, 732, 21, 10], [880, 735, 20, 10]]},
        {"id": "G3", "box": [1305, 708, 113, 120],
         "eyes": [[1337, 749], [1376, 742]],
         "eye_regions": [[1327, 744, 21, 10], [1366, 737, 21, 10]]},
        {"id": "G4", "box": [1753, 700, 116, 139],
         "eyes": [[1783, 751], [1824, 756]],
         "eye_regions": [[1773, 746, 21, 10], [1814, 751, 21, 10]]},
        {"id": "G5", "box": [2116, 712, 116, 124],
         "eyes": [[2147, 759], [2187, 756]],
         "eye_regions": [[2138, 754, 22, 11], [2176, 751, 22, 11]]},
        {"id": "G6", "box": [2440, 712, 117, 135],
         "eyes": [[2472, 769], [2512, 765]],
         "eye_regions": [[2462, 764, 21, 10], [2502, 760, 21, 10]]},
    ],
    "chelsea": [],
}

# Keep the seven terminal explanations in the same order as the saved figures
STAGE_TITLES = (
    "Examine the three photographs", "Detect faces with the initial settings",
    "Compare the revisions", "Extract faces and estimate eye positions",
    "Align faces and find the eyes again", "Blur the eyes and restore the scenes",
    "Review the results and their limits",
)
TEXT_RESET = "\033[0m"
TEXT_STYLES = {"heading": "\033[1;38;5;191m", "rule": "\033[38;5;191m",
               "info": "\033[36m", "success": "\033[1;92m",
               "error": "\033[1;91m", "prompt": "\033[1;95m"}
# These names describe the dictionaries holding each scene and face result
# They are type hints and do not change how the data is processed
SceneResult = dict[str, Any]
FaceResult = dict[str, Any]
View = dict[str, Any]

# __________________________________________
# PROGRAM OPTIONS AND IMAGE PREPARATION
# ==========================================

# --- parse_arguments()
def parse_arguments() -> argparse.Namespace:
    """Read input/output paths and the familiar Module 6 display options.

    Returns:
        Paths, --no-show, and --no-pause. None changes the detector settings.
    """
    # ArgumentParser collects the options typed after the script name
    # The display settings leave the actual face and eye detection unchanged
    parser = argparse.ArgumentParser(
        description="Compare human-face detection, face alignment, and eye blurring.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # The input option can point to another folder containing the same original files
    # The output option selects where the measured results and PNG files are saved
    parser.add_argument("--input-dir", type=Path, default=INPUT_DIRECTORY,
                        help="Folder containing the three supplied original images.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIRECTORY,
                        help="Folder for derived images and measurements.")
    parser.add_argument("--no-show", action="store_true",
                        help="Save and explain without opening windows.")
    parser.add_argument("--no-pause", action="store_true",
                        help="Show figures without waiting for C/Q commands.")
    return parser.parse_args()
# ---


# --- check_output_directory()
def check_output_directory(input_directory: Path, output_directory: Path) -> None:
    """Reject overlapping input/output trees and existing links into source data.

    Raises:
        ValueError: If outputs could overwrite originals or follow a symbolic link.
    """
    # Resolve both paths before checking them so relative paths are compared correctly
    source = input_directory.resolve()
    destination = output_directory.resolve()
    # Error check: Neither directory may contain the other
    # A scene output named after an input must never replace that original image
    # ERROR CHECK Prevent output files from ending up inside the original image folder
    # Also reject the reverse situation where the source folder is inside the output
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Input and output folders must be separate, non-overlapping folders")
    if output_directory.is_symlink():
        # A symbolic link can point to a folder somewhere else on the computer
        # Reject it here so a saved image cannot follow that link into the source files
        raise ValueError(f"The output folder must not be a symbolic link: {output_directory}")
    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f"The output destination is not a folder: {destination}")
        # The any check examines the existing output tree for a symbolic link
        # One link is enough to reject that destination
        if any(path.is_symlink() for path in destination.rglob("*")):
            raise ValueError("Remove symbolic links from the selected output folder before running")
# ---


# --- load_cascades()
def load_cascades() -> tuple[dict[str, cv2.CascadeClassifier], dict[str, Any]]:
    """Load OpenCV's pretrained XML classifiers and record their exact file hashes.

    Returns:
        Classifiers used for calculation and metadata used for the saved record.

    Raises:
        OSError: If an XML file is missing or OpenCV cannot load it.
    """
    # Keep the loaded models and their file information in separate dictionaries
    classifiers = {}
    metadata = {}
    # MAIN ITERATION LOOP Load each face and eye classifier listed in the model table
    # Each turn gets its own filename and stores one working classifier
    for name, filename in CASCADE_FILES.items():
        path = Path(cv2.data.haarcascades) / filename
        if not path.is_file():
            raise OSError(f"Could not find the pretrained classifier: {path}")
        # CascadeClassifier reads a trained XML file without training a new model
        # An empty classifier means the XML model was not loaded successfully
        classifier = cv2.CascadeClassifier(str(path))
        # empty() checks model loading, not whether a later image contains a face
        if classifier.empty():
            raise OSError(f"Could not load the pretrained classifier: {path}")
        classifiers[name] = classifier
        # Save the SHA256 of the actual XML model so a later run can identify its version
        metadata[name] = {"file": filename,
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    return classifiers, metadata
# ---


# --- load_and_prepare()
def load_and_prepare(source: dict[str, Any], input_directory: Path) -> SceneResult:
    """Read one unchanged photograph and retain its native-resolution grayscale image.

    Args:
        source: Filename, dimensions, and identity from SOURCES.
        input_directory: Folder containing the original photographs.

    Returns:
        Original color and grayscale arrays plus measured image information.

    Raises:
        OSError: If the photograph cannot be read.
        ValueError: If its bytes, dimensions, or representation differ from the source.
    """
    # Build the path to one original photograph and read its file fingerprint
    # The hash comparison happens before any image processing
    path = input_directory / source["file"]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != source["sha256"]:
        raise ValueError(f"Input hash differs from the supplied photograph: {path}")
    # Read the photograph in color using the OpenCV BGR channel order
    # An unreadable image must stop here rather than enter the face detector
    original = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if original is None:
        raise OSError(f"Could not decode the input image: {path}")
    # NumPy stores image height before width even though rectangles use x before y
    # Check both dimensions against the expected source photograph
    height, width = original.shape[:2]
    if (width, height) != (source["width"], source["height"]):
        raise ValueError(f"Unexpected image dimensions: {path}")
    if original.ndim != 3 or original.shape[2] != 3 or original.dtype != np.uint8:
        raise ValueError(f"Expected a three-channel uint8 color photograph: {path}")
    # Do not blur or resize this baseline before the first detection experiment
    # cvtColor() combines BGR channels into one intensity value from 0 through 255
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    # Store the untouched color image and its separate grayscale copy
    # The mean and standard deviation describe brightness across the whole scene
    return {**source, "original_bgr": original, "gray": gray,
            "gray_mean": float(gray.mean()), "gray_std": float(gray.std()),
            "input_sha256": digest, "experiments": [], "faces": []}
# ---


# --- prepare_contrast()
def prepare_contrast(gray: np.ndarray, method: str) -> np.ndarray:
    """Apply one declared contrast choice without changing the stored grayscale input.

    Logic:
        Global equalization redistributes intensities over the whole image.
        CLAHE limits local contrast amplification in an 8 x 8 tile grid.
    """
    # Use the requested contrast method without changing the stored grayscale array
    # The plain gray choice returns its own copy for this experiment
    if method == "gray":
        return gray.copy()
    # Global equalization changes the distribution of gray values across the whole image
    if method == "equalized":
        return cv2.equalizeHist(gray)
    # CLAHE works in smaller image areas and limits how much local contrast grows
    # The tile grid is eight by eight and the contrast limit is two
    if method == "clahe":
        return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    raise ValueError(f"Unknown contrast method: {method}")
# ---

# __________________________________________
# FACE DETECTION - BASELINE AND REVISIONS
# ==========================================

# --- detect_faces()
def detect_faces(gray: np.ndarray, settings: dict[str, Any],
                 classifier: cv2.CascadeClassifier) -> dict[str, Any]:
    """Run one face experiment and map returned rectangles to the original image.

    Args:
        gray: Native-resolution uint8 grayscale image.
        settings: One common experiment configuration from EXPERIMENTS.
        classifier: Already-loaded face cascade.

    Returns:
        The actual detector input, both coordinate sets, settings, and timing.

    Logic:
        Keep actual horizontal and vertical resize factors. Whole-pixel rounding
        can make them slightly different even when aspect ratio is preserved.
        No reference count, filename, or annotation enters this calculation.
    """
    # Read the original height and width before preparing the detector input
    # The working image may be smaller but the original shape is kept for the boxes
    height, width = gray.shape
    work = gray
    edge = settings["max_edge"]
    # RESIZE DECISION Only reduce an image when this experiment sets a size limit
    # Use the longer image edge to calculate one common scaling value
    if edge is not None and max(height, width) > edge:
        scale = edge / max(height, width)
        # INTER AREA is used for reducing the image while keeping its proportions
        # Whole pixel rounding can still make the two final resize ratios slightly different
        work = cv2.resize(gray, (round(width * scale), round(height * scale)),
                          interpolation=cv2.INTER_AREA)
    # Apply contrast to the detector copy after any requested resize
    # Calculate separate horizontal and vertical ratios for returning the boxes
    work = prepare_contrast(work, settings["preprocessing"])
    sy, sx = height / work.shape[0], width / work.shape[1]
    started = time.perf_counter()
    # scaleFactor controls the spacing of scales searched by the cascade
    # minNeighbors controls grouped candidate support, not a confidence percentage
    # minSize is measured in the detector input, which may be smaller than the original
    # The cascade searches the grayscale input for face shaped intensity patterns
    # It returns rectangles in the working image rather than the original scene
    rectangles = classifier.detectMultiScale(
        work, scaleFactor=settings["scale_factor"],
        minNeighbors=settings["min_neighbors"],
        minSize=(settings["min_size"], settings["min_size"]),
    )
    elapsed = time.perf_counter() - started
    # Convert each returned rectangle into ordinary Python integers and sort the boxes
    # This keeps their saved order consistent across the later comparisons
    detector_boxes = sorted([list(map(int, box)) for box in rectangles])
    boxes = []
    # BOX CONVERSION LOOP Visit every face rectangle returned by the classifier
    # Multiply its position and size by the two ratios to recover original coordinates
    for x, y, w, h in detector_boxes:
        ox, oy = round(x * sx), round(y * sy)
        # Limit each mapped width and height to the remaining original image area
        # This avoids a box extending past the right or bottom image boundary
        boxes.append([ox, oy, min(round(w * sx), width - ox),
                      min(round(h * sy), height - oy)])
    return {**settings, "detector_gray": work, "detector_boxes": detector_boxes,
            "boxes": boxes, "detector_width": work.shape[1],
            "detector_height": work.shape[0], "original_per_detector_x": sx,
            "original_per_detector_y": sy, "elapsed_seconds": elapsed}
# ---


# --- run_face_experiments()
def run_face_experiments(scene: SceneResult,
                         classifiers: dict[str, cv2.CascadeClassifier]) -> None:
    """Retain every experiment, including settings that produce worse results."""
    # MAIN ITERATION LOOP Run all six face experiments on the current photograph
    # Keep every experiment even when it returns extra boxes or misses a face
    for settings in EXPERIMENTS:
        print(f"  {scene['title']}: {settings['name']}", flush=True)
        result = detect_faces(scene["gray"], settings, classifiers[settings["cascade"]])
        scene["experiments"].append(result)
    # Find the one experiment selected for the remaining face processing
    # The choice uses its fixed name and not the measured reference accuracy
    scene["selected"] = next(result for result in scene["experiments"]
                             if result["name"] == FINAL_EXPERIMENT)
# ---

# __________________________________________
# EXTRACT FACES AND ESTIMATE THE EYE PAIR
# ==========================================

# --- rectangle_iou()
def rectangle_iou(first: list[int], second: list[int]) -> float:
    # Separate each rectangle into its left position top position width and height
    # This calculation uses the area of the two rectangles rather than their centers
    """Calculate intersection-over-union for half-open (x, y, width, height) boxes."""
    ax, ay, aw, ah = first
    bx, by, bw, bh = second
    # Find the width and height shared by both rectangles
    # A missing overlap becomes zero instead of a negative area
    overlap = max(0, min(ax + aw, bx + bw) - max(ax, bx)) * max(
        0, min(ay + ah, by + bh) - max(ay, by))
    # The union is the combined area after counting the overlap only once
    # Dividing overlap by union gives a value between zero and one
    union = aw * ah + bw * bh - overlap
    return overlap / union if union else 0.0
# ---


# --- extract_face()
def extract_face(original: np.ndarray, box: list[int]) -> tuple[np.ndarray, np.ndarray]:
    """Extract a clean original-resolution face and resize a separate eye-search copy.

    Logic:
        The face box is already in original coordinates. Upsampling gives the
        cascade a different sampling grid; it does not recover missing detail.
    """
    # The detected box already uses coordinates from the original photograph
    # NumPy slices use the vertical position first and the horizontal position second
    x, y, width, height = box
    crop = original[y:y + height, x:x + width].copy()
    if crop.size == 0:
        raise ValueError(f"The detected face produced an empty crop: {box}")
    # Size the separate search copy so its longest side is 300 pixels
    # An enlarged small face still has the same original image detail
    scale = EYE_SEARCH_EDGE / max(width, height)
    # Use linear interpolation for enlargement and area interpolation for reduction
    interpolation = cv2.INTER_LINEAR if scale > 1 else cv2.INTER_AREA
    normalized = cv2.resize(crop, (round(width * scale), round(height * scale)),
                            interpolation=interpolation)
    return crop, normalized
# ---


# --- detect_eye_candidates()
def detect_eye_candidates(image: np.ndarray, classifier: cv2.CascadeClassifier,
                          contrast: str, split: bool = False) -> list[list[int]]:
    """Search only an extracted face, with an optional separate search for each half.

    Args:
        image: Normalized or aligned BGR face crop.
        classifier: An eye cascade, not a face or animal cascade.
        contrast: gray, equalized, or clahe.
        split: Search the upper image-left and image-right halves separately.

    Returns:
        Actual eye-cascade rectangles expressed in the input face coordinates.

    Logic:
        A narrower region can change cascade grouping and prevent a nearby brow
        candidate from competing with the other eye. It does not create an eye.
    """
    # Convert this extracted color face to grayscale before searching for eyes
    # Use the contrast choice supplied for the current attempt
    gray = prepare_contrast(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), contrast)
    height, width = gray.shape
    # SEARCH DECISION A split attempt examines left and right portions separately
    # The ordinary search instead examines the upper part as one region
    if split:
        regions = [(0, round(0.125 * height), width // 2, round(0.64 * height)),
                   (width // 2, round(0.125 * height), width, round(0.64 * height))]
    else:
        # The complete upper search excludes much of the mouth and lower face
        regions = [(0, 0, width, round(0.70 * height))]
    candidates = []
    # SEARCH REGION LOOP Examine each search area defined for the current attempt
    # A split attempt runs this loop twice while a regular attempt runs once
    for x0, y0, x1, y1 in regions:
        # A split search uses a finer scale step and lower grouping requirement
        # Record this combined revision rather than attributing it to one parameter
        # The eye cascade receives only the pixels inside the current search area
        # The split search also uses smaller scale steps and a lower grouping requirement
        boxes = classifier.detectMultiScale(
            gray[y0:y1, x0:x1], scaleFactor=1.03 if split else 1.05,
            minNeighbors=2 if split else 3,
            minSize=(max(12, int(0.075 * width if split else 0.09 * width)),) * 2,
            maxSize=(int((0.38 if split else 0.32) * width),) * 2,
        )
        # CANDIDATE LOOP Put each returned eye box back in full face coordinates
        # Add the region offset because the cascade searched only part of the face
        for x, y, w, h in boxes:
            candidates.append([int(x + x0), int(y + y0), int(w), int(h)])
    return sorted(candidates)
# ---


# --- select_eye_pair()
def select_eye_pair(candidates: list[list[int]], shape: tuple[int, ...]) -> list[list[int]]:
    """Choose two distinct, plausibly spaced eyes without reading reference labels.

    Returns:
        Two rectangles in image-left/image-right order, or an empty list.

    Logic:
        Remove strongly overlapping proposals, then check height, spacing,
        midpoint, and relative size. Geometry is a heuristic, not recognition
        proof. The evaluation still checks every accepted pair independently.
    """
    # Use the face dimensions to check whether two candidates look like an eye pair
    # The checks are based on geometry and do not use the marked reference eyes
    height, width = shape[:2]
    distinct = []
    # Keep the larger region when two proposals overlap strongly
    # Preserve the unfiltered candidates separately in the recorded attempt
    # FILTER LOOP Visit larger eye candidates before smaller overlapping candidates
    # Keep a candidate only when it does not overlap strongly with one already chosen
    for candidate in sorted(candidates, key=lambda b: (-b[2] * b[3], b[0], b[1])):
        # The all check compares the current candidate with every box already kept
        # An overlap of forty percent or more makes it a duplicate proposal
        if all(rectangle_iou(candidate, other) < 0.40 for other in distinct):
            distinct.append(candidate)
    distinct.sort()
    # Start without a selected pair and keep the lowest accepted geometry score
    # A smaller score means the two boxes better match the expected eye arrangement
    best_pair = []
    best_score = float("inf")
    # OUTER LOOP Treat each distinct candidate as a possible left eye
    # enumerate also gives its position in the candidate list
    for index, left in enumerate(distinct):
        # INNER LOOP Pair that candidate only with boxes farther right in the list
        # This avoids testing the same two boxes in both directions
        for right in distinct[index + 1:]:
            lx, ly = left[0] + left[2] / 2, left[1] + left[3] / 2
            rx, ry = right[0] + right[2] / 2, right[1] + right[3] / 2
            # Measure the distance between the centers and their difference in height
            # Eyes should have a useful separation without one sitting far below the other
            spacing, vertical = rx - lx, abs(ry - ly)
            # Compare the candidate areas so one box is not much larger than the other
            area_ratio = min(left[2] * left[3], right[2] * right[3]) / max(
                left[2] * left[3], right[2] * right[3])
            # GEOMETRY CHECK Reject pairs outside the upper face or on the same half
            # Also check the spacing vertical difference midpoint and relative eye sizes
            if not (0.18 * height <= ly <= 0.58 * height
                    and 0.18 * height <= ry <= 0.58 * height
                    and lx < width / 2 < rx
                    and 0.26 * width <= spacing <= 0.65 * width
                    and vertical <= 0.15 * height
                    and 0.32 * width <= (lx + rx) / 2 <= 0.68 * width
                    and area_ratio >= 0.45):
                continue
            # Calculate the score only after the pair passes all the geometry checks
            # Smaller vertical offsets and more centered eye pairs receive lower scores
            score = (vertical / height + abs((lx + rx) / (2 * width) - 0.5)
                     + 0.2 * abs(spacing / width - 0.4)
                     + 0.1 * abs(left[2] - right[2]) / width)
            # Replace the saved pair only when this candidate has a better score
            if score < best_score:
                best_score, best_pair = score, [left, right]
    return best_pair
# ---


# --- find_eye_pair()
def find_eye_pair(image: np.ndarray, classifiers: dict[str, cv2.CascadeClassifier]
                  ) -> tuple[list[list[int]], list[dict[str, Any]]]:
    """Try a bounded sequence of eye searches and retain each attempted result.

    Logic:
        Start with ordinary grayscale. Change contrast and then the eye cascade
        only when no plausible pair is found. Split-region attempts come last.
        Stop on a geometric pair, not on a reference count or evaluation score.
    """
    # Keep a record of each attempted search even if no eye pair is accepted
    attempts = []
    # Try ordinary gray first and then change contrast or the eye classifier
    # The split searches are tried last when the earlier attempts fail
    choices = (("eye", "gray", False), ("eye", "equalized", False),
               ("eyeglasses", "gray", False), ("eyeglasses", "equalized", False),
               ("eye", "gray", True), ("eyeglasses", "gray", True),
               ("eye", "clahe", True))
    # MAIN ITERATION LOOP Try one model and contrast combination at a time
    # The current choice also tells the search whether to split the face
    for model, contrast, split in choices:
        # Run the classifier and then look for two boxes with reasonable eye geometry
        candidates = detect_eye_candidates(image, classifiers[model], contrast, split)
        pair = select_eye_pair(candidates, image.shape)
        # Save the actual candidates settings and selected pair from this attempt
        # Unsuccessful searches stay in the results for later inspection
        attempts.append({"cascade": model, "preprocessing": contrast, "split": split,
                         "scale_factor": 1.03 if split else 1.05,
                         "min_neighbors": 2 if split else 3,
                         "candidates": candidates, "pair": pair})
        # Stop the search as soon as one plausible pair is accepted
        # If none of the choices works return an empty pair rather than guessing
        if pair:
            return pair, attempts
    return [], attempts
# ---

# __________________________________________
# ALIGN FACES AND BLUR THE DETECTED EYES
# ==========================================

# --- transform_points()
def transform_points(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    # Turn the supplied points into a two column NumPy array
    # The matrix rotates scales and moves each point without changing its point order
    """Apply a 2 x 3 affine matrix to points stored as an N x 2 array."""
    values = np.asarray(points, dtype=np.float64).reshape(-1, 2)
    return values @ matrix[:, :2].T + matrix[:, 2]
# ---


# --- align_face()
def align_face(crop: np.ndarray, normalized: np.ndarray,
               pair: list[list[int]]) -> dict[str, Any]:
    """Rotate, uniformly scale, and translate the original crop from its eye estimates.

    Returns:
        Aligned pixels, valid-source mask, forward/inverse matrices, and controls.

    Logic:
        theta = atan2(right_y - left_y, right_x - left_x)
        scale = target_eye_distance / measured_eye_distance
        OpenCV's positive rotation removes a downward-sloping image eye line.
        Translation moves the eye midpoint to the target midpoint.
    """
    # CENTER LOOP Build one center for each provisional eye rectangle
    # A rectangle center is its starting position plus half its width or height
    points = np.array([[x + w / 2, y + h / 2] for x, y, w, h in pair], dtype=float)
    # The first eye search used a resized face so return these centers to crop pixels
    # The two dimensions are scaled separately to account for whole pixel rounding
    points[:, 0] *= crop.shape[1] / normalized.shape[1]
    points[:, 1] *= crop.shape[0] / normalized.shape[0]
    # Subtract the left eye center from the right eye center
    # The resulting two values describe the eye line direction and separation
    difference = points[1] - points[0]
    distance = float(np.linalg.norm(difference))
    # ERROR CHECK Both eyes need different centers to calculate a valid scale
    if distance <= 0:
        raise ValueError("The provisional eyes must have different centers")
    # atan2 calculates the eye line angle from its horizontal and vertical difference
    # The new scale makes the eye separation match the target separation
    angle = math.degrees(math.atan2(difference[1], difference[0]))
    scale = float(np.linalg.norm(TARGET_EYES[1] - TARGET_EYES[0]) / distance)
    # The midpoint is halfway between the two provisional eye centers
    # It becomes the center used to rotate and scale the face
    midpoint = points.mean(axis=0)
    # getRotationMatrix2D creates the two by three matrix for rotation and scaling
    # Adjust the translation so the measured eye midpoint reaches the target midpoint
    matrix = cv2.getRotationMatrix2D(tuple(midpoint), angle, scale)
    matrix[:, 2] += TARGET_EYES.mean(axis=0) - midpoint
    # Warp from original crop pixels rather than enlarging the normalized image again
    # Reflection fills display borders; a separate validity mask excludes those pixels
    aligned = cv2.warpAffine(crop, matrix, (ALIGNED_EDGE, ALIGNED_EDGE),
                             flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    # Transform a white mask with the same matrix used for the face
    # It marks pixels that really came from the original crop rather than border filling
    valid = cv2.warpAffine(np.full(crop.shape[:2], 255, np.uint8), matrix,
                          (ALIGNED_EDGE, ALIGNED_EDGE), flags=cv2.INTER_NEAREST,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    # The inverse matrix will be used later to move the blurred eyes back to the crop
    inverse = cv2.invertAffineTransform(matrix)
    # Map the estimated eye centers through the matrix and compare them with the targets
    # This checks the transform calculations rather than actual eye recognition accuracy
    residual = float(np.max(np.linalg.norm(transform_points(points, matrix) - TARGET_EYES,
                                           axis=1)))
    if not np.isfinite(matrix).all() or residual > 0.001:
        raise ValueError("The eye-alignment transform failed its control-point check")
    # Keep the aligned face the valid pixel mask and both transformations
    # These values are needed to detect the eyes again and restore the original scene
    return {"aligned_bgr": aligned, "valid_mask": valid, "matrix": matrix.tolist(),
            "inverse_matrix": inverse.tolist(), "angle_degrees": angle, "scale": scale,
            "provisional_centers_crop": points.tolist(), "control_residual_px": residual}
# ---


# --- blur_eyes()
def blur_eyes(aligned: np.ndarray, pair: list[list[int]], valid_mask: np.ndarray,
              sigma_fraction: float, padding_fraction: float = EYE_PADDING
              ) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]]]:
    """Apply Gaussian blur inside padded, detected eye regions of an aligned face.

    Returns:
        A clean blurred face, the treatment mask, and each kernel/region setting.

    Logic:
        Padding includes visible lids and reduces the chance of leaving an eye
        corner untouched. Sigma follows the detected eye size. This visual
        treatment is not a measured guarantee against person identification.
    """
    # Copy the aligned face so the returned blur does not overwrite its input
    # Start a black mask where white will later identify the changed eye regions
    output = aligned.copy()
    mask = np.zeros(aligned.shape[:2], np.uint8)
    height, width = mask.shape
    treatments = []
    # EYE TREATMENT LOOP Process the two detected eye rectangles one at a time
    # Each rectangle gets its own blur size and padded treatment area
    for x, y, w, h in pair:
        # Calculate extra space around the eye using a fraction of its box dimensions
        # The wider final padding helps include eyelids and corners of the eyes
        mx, my = math.ceil(padding_fraction * w), math.ceil(padding_fraction * h)
        # Clamp the padded region so it stays within the 320 by 320 aligned face
        x0, y0 = max(0, x - mx), max(0, y - my)
        x1, y1 = min(width, x + w + mx), min(height, y + h + my)
        # Use the larger eye box dimension to select the Gaussian spread
        # The minimum sigma of two pixels also applies to small detected eyes
        sigma = max(2.0, sigma_fraction * max(w, h))
        # Three sigma on each side gives a positive odd Gaussian kernel
        # Calculate an odd kernel wide enough to include three sigma on each side
        # An odd kernel has one center pixel for the Gaussian weights
        kernel = 2 * math.ceil(3 * sigma) + 1
        # Blur only the padded area from the untouched aligned face
        # This keeps other face details outside that area unchanged
        region = aligned[y0:y1, x0:x1]
        blurred = cv2.GaussianBlur(region, (kernel, kernel), sigmaX=sigma, sigmaY=sigma,
                                   borderType=cv2.BORDER_REFLECT_101)
        # Limit the replacement to pixels that came from the original crop
        # Set the same positions to white in the treatment mask
        selected = valid_mask[y0:y1, x0:x1] > 0
        output[y0:y1, x0:x1][selected] = blurred[selected]
        mask[y0:y1, x0:x1][selected] = 255
        # Save each eye box padded region kernel and sigma for the result record
        treatments.append({"eye_box": [x, y, w, h], "region": [x0, y0, x1 - x0, y1 - y0],
                           "kernel": kernel, "sigma": sigma,
                           "padding_fraction": padding_fraction})
    return output, mask, treatments
# ---


# --- restore_eye_regions()
def restore_eye_regions(crop: np.ndarray, blurred: np.ndarray, mask: np.ndarray,
                        inverse: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Map the aligned treatment back to the crop and keep all other pixels exact.

    Logic:
        Interpolate color but use nearest-neighbor interpolation for the binary
        mask. Compositing through that mask prevents whole-face resampling.
    """
    # Read the dimensions of the clean original face crop for the return transform
    height, width = crop.shape[:2]
    # Use the inverse matrix to bring blurred color pixels back to the crop size
    # Linear interpolation estimates the returned color values between pixels
    returned = cv2.warpAffine(blurred, inverse, (width, height), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REFLECT_101)
    # Transform the binary mask separately using nearest neighbor interpolation
    # This keeps the mask values as selected or unselected pixels
    returned_mask = cv2.warpAffine(mask, inverse, (width, height), flags=cv2.INTER_NEAREST,
                                  borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    # Start from the original face and replace only positions selected by the mask
    # The rest of the crop stays equal to its original pixel values
    output = crop.copy()
    output[returned_mask > 0] = returned[returned_mask > 0]
    return output, returned_mask
# ---


# --- process_faces()
def process_faces(scene: SceneResult, classifiers: dict[str, cv2.CascadeClassifier]) -> None:
    """Process every selected face candidate without using a reference label.

    Logic:
        A missing pair remains unresolved. There is no hardcoded cat exception,
        manual-coordinate fallback, or claim that a failed pair was detected.
    """
    # Keep a clean copy of the entire photograph and begin with empty scene masks
    # The weak mask is saved for comparison with the wider final treatment
    original = scene["original_bgr"]
    final = original.copy()
    scene_mask = np.zeros(original.shape[:2], np.uint8)
    weak_scene_mask = np.zeros(original.shape[:2], np.uint8)
    # MAIN ITERATION LOOP Process each selected face box in the current photograph
    # The face number starts at one and is used when saving its individual files
    for number, box in enumerate(scene["selected"]["boxes"], start=1):
        # Extract a clean original face crop and a separate smaller eye search copy
        crop, normalized = extract_face(original, box)
        # Look for a provisional eye pair before rotating the face
        # Without a pair the program does not invent positions to complete the alignment
        pair, attempts = find_eye_pair(normalized, classifiers)
        # Start the face record with its crop and initial search attempts
        # The unresolved status remains unless later processing finds and blurs the eyes
        face: FaceResult = {"number": number, "box": box, "crop_bgr": crop,
                            "normalized_bgr": normalized, "provisional_pair": pair,
                            "provisional_attempts": attempts,
                            "status": "unresolved_provisional_pair"}
        # PROCESSING DECISION Continue with alignment only when a plausible pair exists
        if pair:
            # Rotate scale and center the original crop using the provisional eye centers
            face.update(align_face(crop, normalized, pair))
            # Run a new eye search after alignment instead of reusing the original detections
            # The final eye boxes belong to the aligned face coordinate system
            final_pair, final_attempts = find_eye_pair(face["aligned_bgr"], classifiers)
            face.update({"final_pair": final_pair, "final_attempts": final_attempts,
                         "status": "unresolved_aligned_pair"})
            # TREATMENT DECISION Only blur when the second eye search also found a pair
            if final_pair:
                # The first blur has a smaller margin and weaker Gaussian spread
                # Keep its result to compare how much eye detail is still visible
                weak, weak_mask, weak_settings = blur_eyes(
                    face["aligned_bgr"], final_pair, face["valid_mask"],
                    WEAK_SIGMA_FRACTION, INITIAL_EYE_PADDING)
                # Apply the stronger Gaussian blur with the wider final treatment area
                strong, mask, strong_settings = blur_eyes(
                    face["aligned_bgr"], final_pair, face["valid_mask"], FINAL_SIGMA_FRACTION)
                # Return both masks to the original face coordinates
                # Use the stronger restored image as the final treatment
                restored, restored_mask = restore_eye_regions(
                    crop, strong, mask, np.array(face["inverse_matrix"]))
                _, weak_restored_mask = restore_eye_regions(
                    crop, weak, weak_mask, np.array(face["inverse_matrix"]))
                # Locate this face crop inside the complete original photograph
                x, y, w, h = box
                # Mark the original scene pixels selected by the weaker treatment mask
                weak_scene_mask[y:y + h, x:x + w][weak_restored_mask > 0] = 255
                # Copy only the stronger blurred eye pixels into their original scene positions
                # The final scene mask records exactly where a replacement was allowed
                selected = restored_mask > 0
                final[y:y + h, x:x + w][selected] = restored[selected]
                scene_mask[y:y + h, x:x + w][selected] = 255
                # CENTER LOOP Read the two final eye boxes and calculate their centers
                # These centers are on the aligned face before returning to the photograph
                centers = np.array([[a + c / 2, b + d / 2]
                                    for a, b, c, d in final_pair])
                # Undo the face alignment and add the crop offset to get original image positions
                original_centers = transform_points(centers, np.array(face["inverse_matrix"]))
                original_centers += np.array([x, y])
                # Keep both blur versions the restored mask and the final eye locations
                # Mark this face as treated only after the whole eye process succeeds
                face.update({"weak_blur_bgr": weak, "blurred_bgr": strong,
                             "aligned_mask": mask, "weak_aligned_mask": weak_mask,
                             "restored_bgr": restored,
                             "restored_mask": restored_mask, "weak_settings": weak_settings,
                             "blur_settings": strong_settings,
                             "final_centers_original": original_centers.tolist(),
                             "status": "eyes_blurred"})
        # Keep the face record even when one of its eye searches failed
        scene["faces"].append(face)
    # This also checks the zero-detection case without a special rule for an animal
    # Select every scene pixel outside the final treatment mask
    # Compare those pixels with the original photograph to check exact preservation
    outside = scene_mask == 0
    unchanged = bool(np.array_equal(final[outside], original[outside]))
    if not unchanged:
        raise ValueError("Pixels outside the eye-treatment mask changed")
    # Store the final image and masks along with the number of changed pixels
    # Treatment pixels count the mask while changed pixels compare actual colors
    scene.update({"final_bgr": final, "scene_mask": scene_mask,
                  "weak_scene_mask": weak_scene_mask,
                  "outside_mask_unchanged": unchanged,
                  "changed_pixels": int(np.count_nonzero(np.any(final != original, axis=2))),
                  "treatment_pixels": int(np.count_nonzero(scene_mask))})
# ---

# __________________________________________
# MEASUREMENTS - REFERENCES DO NOT DRIVE DETECTION
# ==========================================

# --- match_face_boxes()
def match_face_boxes(detected: list[list[int]], reference: list[list[int]],
                     threshold: float = FACE_IOU_THRESHOLD) -> dict[str, Any]:
    """Match boxes one-to-one, maximizing match count before total overlap.

    Logic:
        There are at most six reference faces in an image. A small table of
        reference subsets finds the best assignment without another library.
        Two overlapping detections cannot both count as the same reference face.
    """
    # Start with an empty matching state and no accumulated overlap
    # A state uses bits to remember which reference faces have already been matched
    states: dict[int, tuple[float, list[dict[str, Any]]]] = {0: (0.0, [])}
    # OUTER LOOP Take one detected face box at a time
    # The matching keeps track of which reference faces are already assigned
    for detection_index, box in enumerate(detected):
        # Copy the existing states so leaving this detection unmatched remains an option
        next_states = dict(states)
        # MIDDLE LOOP Examine each possible set of previously matched reference faces
        # The bit mask tells the program which reference positions are already used
        for used, (total_overlap, pairs) in states.items():
            # INNER LOOP Compare this detection against every reference face in the image
            # Only a reference that is still free can form another valid match
            for reference_index, target in enumerate(reference):
                # Calculate the intersection over union between the two face boxes
                overlap = rectangle_iou(box, target)
                # MATCHING DECISION Skip a reference already used in this state
                # Also skip boxes whose overlap is below the required threshold
                if used & (1 << reference_index) or overlap < threshold:
                    continue
                # Set the bit for the newly matched reference face
                # Add this overlap to the score already earned by the current matching state
                new_used = used | (1 << reference_index)
                score = total_overlap + overlap
                # Keep this assignment when it improves the total overlap for the same state
                # The detection and reference indexes identify the two boxes that were paired
                if new_used not in next_states or score > next_states[new_used][0]:
                    entry = {"detection": detection_index, "reference": reference_index,
                             "iou": overlap}
                    next_states[new_used] = (score, pairs + [entry])
        # Carry the updated matching possibilities into the next detected face
        states = next_states
    # Choose the state with the most matched reference faces
    # Use the summed overlap to break a tie between equally complete matches
    used = max(states, key=lambda mask: (mask.bit_count(), states[mask][0]))
    matches = states[used][1]
    # COLLECTION LOOP Gather the detection numbers and reference numbers used in the matches
    # The two sets make it possible to find extra detections and missed faces
    matched_detections = {entry["detection"] for entry in matches}
    matched_references = {entry["reference"] for entry in matches}
    # Return the matched pairs and the indexes that were not matched
    # Extra detections become false positives and missed references become false negatives
    return {"matches": matches,
            "unmatched_detections": [i for i in range(len(detected))
                                     if i not in matched_detections],
            "unmatched_references": [i for i in range(len(reference))
                                     if i not in matched_references]}
# ---


# --- detection_metrics()
def detection_metrics(true_positive: int, false_positive: int,
                      false_negative: int) -> dict[str, int | float | None]:
    """Calculate precision, recall, and F1 without inventing zero-denominator scores."""
    # Calculate each metric denominator before dividing
    # An empty denominator gives an undefined result rather than a made up accuracy
    precision_denominator = true_positive + false_positive
    recall_denominator = true_positive + false_negative
    f1_denominator = 2 * true_positive + false_positive + false_negative
    # Precision measures how many detected boxes matched a reference
    # Recall measures how many reference faces were found and F1 combines both
    return {"tp": true_positive, "fp": false_positive, "fn": false_negative,
            "precision": true_positive / precision_denominator if precision_denominator else None,
            "recall": true_positive / recall_denominator if recall_denominator else None,
            "f1": 2 * true_positive / f1_denominator if f1_denominator else None}
# ---


# --- measure_results()
def measure_results(scene: SceneResult) -> None:
    """Score stored face boxes, eye centers, alignment, and original-size blur coverage.

    Logic:
        Reference marks enter here, after all detection and image treatment.
        Eye-center error is measured in original pixels. Its tolerance is the
        larger of two pixels and 10% of reference inter-eye distance.
        Coverage measures a treatment mask, not resistance to identification.
    """
    # Read the fixed visual reference marks only after detection and eye processing
    # The cat has an empty reference list because the assignment looks for human faces
    references = REFERENCE_ANNOTATIONS[scene["stem"]]
    # EXPERIMENT MEASUREMENT LOOP Score each of the six saved face experiments
    # These measurements compare detector boxes with the same reference marks
    for experiment in scene["experiments"]:
        # Collect only the reference face boxes and find one to one matches
        # Store the match details and counts for the later figures and CSV table
        match = match_face_boxes(experiment["boxes"], [item["box"] for item in references])
        experiment["matching"] = match
        experiment["metrics"] = detection_metrics(
            len(match["matches"]), len(match["unmatched_detections"]),
            len(match["unmatched_references"]))
    # The selected face experiment is used for the remaining eye measurements
    selected = scene["selected"]
    # INDEX LOOP Make it easy to find a matched detection by its reference number
    # Only reference faces actually matched by the selected detector appear here
    by_reference = {entry["reference"]: entry for entry in selected["matching"]["matches"]}
    eye_rows = []
    # REFERENCE FACE LOOP Examine each visually marked human face
    # A missed face still gets a measurement row with its eye coverage results
    for index, reference in enumerate(references):
        # Measure the distance between the two marked reference eye centers
        # Use ten percent of that distance or at least two pixels as the center tolerance
        eye_points = np.array(reference["eyes"], dtype=float)
        separation = float(np.linalg.norm(eye_points[1] - eye_points[0]))
        tolerance = max(EYE_ERROR_MINIMUM, EYE_ERROR_FRACTION * separation)
        # Start the row with missing values because a reference face may not be detected
        # The later checks fill these fields only when matching data exists
        row: dict[str, Any] = {
            "scene": scene["stem"], "reference_face": reference["id"],
            "detection_number": None, "face_iou": None, "status": "face_not_detected",
            "center_tolerance_px": tolerance, "left_center_error_px": None,
            "right_center_error_px": None, "left_center_correct": False,
            "right_center_correct": False, "reference_roll_before_deg": None,
            "reference_roll_after_deg": None, "provisional_attempts": 0,
            "final_attempts": 0,
        }
        # Measure actual treatment in the original scene, including when a face was missed
        # EYE REGION LOOP Read the marked left eye and right eye areas separately
        # zip pairs the side name with its corresponding reference rectangle
        for side, region in zip(("left", "right"), reference["eye_regions"]):
            x, y, w, h = region
            # Slice the actual final scene mask where the marked eye region is located
            # Count the selected pixels and divide by the total pixels in that region
            patch = scene["scene_mask"][y:y + h, x:x + w]
            row[f"{side}_region_coverage"] = float(np.count_nonzero(patch) / patch.size)
            # Repeat the same coverage measurement for the weaker initial blur
            # This makes the change in covered eye area visible in the results
            initial_patch = scene["weak_scene_mask"][y:y + h, x:x + w]
            row[f"{side}_initial_region_coverage"] = float(
                np.count_nonzero(initial_patch) / initial_patch.size)
        # MATCH DECISION Fill in detection details only if this reference face was found
        # Use the matching index to locate the corresponding processed face record
        if index in by_reference:
            match = by_reference[index]
            face = scene["faces"][match["detection"]]
            row.update({"detection_number": face["number"], "face_iou": match["iou"],
                        "status": face["status"],
                        "provisional_attempts": len(face["provisional_attempts"]),
                        "final_attempts": len(face.get("final_attempts", []))})
            # ALIGNMENT CHECK If this face has a matrix measure the reference eye line
            # This tests actual marked eyes instead of only the provisional control points
            if "matrix" in face:
                delta = eye_points[1] - eye_points[0]
                # Subtract the face crop position to express the marked eyes in crop coordinates
                # Then apply the saved matrix to see their positions on the aligned face
                transformed = transform_points(eye_points - np.array(face["box"][:2]),
                                               np.array(face["matrix"]))
                aligned_delta = transformed[1] - transformed[0]
                row["reference_roll_before_deg"] = math.degrees(math.atan2(delta[1], delta[0]))
                row["reference_roll_after_deg"] = math.degrees(
                    math.atan2(aligned_delta[1], aligned_delta[0]))
            # CENTER CHECK Only calculate eye errors when final eye centers were returned
            if "final_centers_original" in face:
                # Sort the two detected centers into image left and image right order
                # Compare each center with its corresponding visual reference position
                predicted = np.array(sorted(face["final_centers_original"]))
                # Euclidean distance measures the straight line error in original image pixels
                errors = np.linalg.norm(predicted - eye_points, axis=1)
                # CENTER MEASUREMENT LOOP Record the error of each detected eye separately
                # An eye passes this check only when its center is within the fixed tolerance
                for side, error in zip(("left", "right"), errors):
                    row[f"{side}_center_error_px"] = float(error)
                    row[f"{side}_center_correct"] = bool(error <= tolerance)
        # Both centers must pass before the complete eye pair counts as correct
        # The two marked eye regions must also each have full mask coverage
        row["both_centers_correct"] = row["left_center_correct"] and row["right_center_correct"]
        row["both_regions_covered"] = (row["left_region_coverage"] == 1.0
                                       and row["right_region_coverage"] == 1.0)
        # Append the row even if the reference face or one of its eyes was missed
        eye_rows.append(row)
    # COUNT LOOP Total the final detected centers from the actual face records
    # Count how many reference centers passed without changing any detections
    detected_centers = sum(len(face.get("final_centers_original", [])) for face in scene["faces"])
    correct_centers = sum(int(row["left_center_correct"]) + int(row["right_center_correct"])
                          for row in eye_rows)
    # Keep the per face measurements and a separate summary for this photograph
    scene["eye_rows"] = eye_rows
    # Combine face accuracy eye localization and blur coverage in one saved summary
    # A fully covered eye region does not necessarily have a correctly placed eye center
    scene["summary"] = {
        "scene": scene["stem"], "reference_faces": len(references),
        "selected_face_candidates": len(selected["boxes"]), **selected["metrics"],
        "faces_with_eye_treatment": sum(
            face["status"] == "eyes_blurred" for face in scene["faces"]),
        "unresolved_face_candidates": sum(
            face["status"] != "eyes_blurred" for face in scene["faces"]),
        "selected_eye_centers": detected_centers, "correct_eye_centers": correct_centers,
        "incorrect_eye_centers": detected_centers - correct_centers,
        "unmatched_reference_eye_centers": 2 * len(references) - correct_centers,
        "pairs_with_both_centers_correct": sum(row["both_centers_correct"] for row in eye_rows),
        "initial_fully_covered_reference_eyes": sum(
            int(row["left_initial_region_coverage"] == 1.0)
            + int(row["right_initial_region_coverage"] == 1.0) for row in eye_rows),
        "fully_covered_reference_eyes": sum(int(row["left_region_coverage"] == 1.0)
                                             + int(row["right_region_coverage"] == 1.0)
                                             for row in eye_rows),
        "reference_faces_with_both_eye_regions_covered": sum(
            row["both_regions_covered"] for row in eye_rows),
        "changed_pixels": scene["changed_pixels"], "treatment_pixels": scene["treatment_pixels"],
        "outside_mask_unchanged": scene["outside_mask_unchanged"],
    }
# ---

# __________________________________________
# TEACHING FIGURES - DISPLAY STORED RESULTS
# ==========================================

# --- display_size()
def display_size(image: np.ndarray, max_edge: int = DISPLAY_MAX_EDGE) -> np.ndarray:
    """Reduce a display copy without changing a detector input or saved privacy image."""
    # Read the height and width of the image requested for a teaching panel
    # Only the display copy is resized and the stored result remains unchanged
    height, width = image.shape[:2]
    if max(height, width) <= max_edge:
        return image.copy()
    # Use the longer edge to calculate the preview size while keeping the proportions
    scale = max_edge / max(height, width)
    return cv2.resize(image, (round(width * scale), round(height * scale)),
                      interpolation=cv2.INTER_AREA)
# ---


# --- draw_boxes()
def draw_boxes(image: np.ndarray, boxes: list[list[int]], labels: bool = True) -> np.ndarray:
    """Draw red boundaries on a color copy, never on pixels used for feature processing."""
    # Make a copy before adding the red detection boxes
    # The clean image is still used when extracting faces and applying the blur
    output = image.copy()
    thickness = max(2, round(min(image.shape[:2]) / 500))
    # DRAWING LOOP Visit every face box and give it a number starting at one
    # The number matches the face folders created when results are saved
    for number, (x, y, w, h) in enumerate(boxes, start=1):
        # OpenCV uses BGR, so (0, 0, 255) is red rather than blue
        cv2.rectangle(output, (x, y), (x + w - 1, y + h - 1), (0, 0, 255), thickness)
        # DRAWING DECISION Show face numbers only when this view requests labels
        if labels:
            cv2.putText(output, str(number), (x, max(15, y - 6)),
                        cv2.FONT_HERSHEY_SIMPLEX, max(0.45, thickness * 0.28),
                        (0, 0, 255), max(1, thickness // 2), cv2.LINE_AA)
    return output
# ---


# --- reference_overlay()
def reference_overlay(scene: SceneResult) -> np.ndarray:
    """Draw separately marked reference regions for inspection, not for detection."""
    # Get the independent visual marks for this particular photograph
    references = REFERENCE_ANNOTATIONS[scene["stem"]]
    # Draw the manually marked reference boxes on a separate display copy
    # The detector never reads this overlay as an input image
    output = draw_boxes(scene["original_bgr"], [item["box"] for item in references])
    thickness = max(1, round(min(output.shape[:2]) / 800))
    # OUTER DRAWING LOOP Visit each marked reference face in the current scene
    for reference in references:
        # INNER DRAWING LOOP Draw both visible eye regions for this reference face
        # Their rectangles can be compared with the actual blur coverage
        for x, y, w, h in reference["eye_regions"]:
            cv2.rectangle(output, (x, y), (x + w - 1, y + h - 1), (0, 0, 255), thickness)
        # CENTER DRAWING LOOP Add a small cross at each marked eye center
        # These crosses show the positions used for the center error measurements
        for x, y in reference["eyes"]:
            cv2.drawMarker(output, (x, y), (0, 0, 255), cv2.MARKER_CROSS,
                           markerSize=5 * thickness, thickness=thickness)
    return output
# ---


# --- display_image()
def display_image(axis: Axes, image: np.ndarray, title: str) -> None:
    """Show a calculated array with the correct color order and a short label."""
    # DISPLAY DECISION A color image has three dimensions including its channels
    # Reverse BGR to RGB only for the Matplotlib panel
    if image.ndim == 3:
        # Matplotlib expects RGB; only this display conversion reverses the channels
        axis.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:
        # A one channel image uses the gray color map without smoothing its pixels
        axis.imshow(image, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    axis.set_title(title, fontsize=10, pad=8)
    axis.set_axis_off()
# ---


# --- make_figure()
def make_figure(panels: list[tuple[np.ndarray, str]], rows: int, columns: int,
                title: str, size: tuple[float, float] | None = None) -> Figure:
    """Arrange stored images under a teaching title without recalculating results."""
    # Create the requested grid of figure panels without processing the images again
    # The layout changes only how the images are arranged in the teaching figure
    figure, axes = plt.subplots(rows, columns,
                                figsize=size or (5 * columns, 4.8 * rows),
                                squeeze=False, layout="constrained")
    figure.get_layout_engine().set(w_pad=0.12, h_pad=0.16, hspace=0.10, wspace=0.04)
    # PANEL SETUP LOOP Hide the axes on every empty panel before filling the figure
    for axis in axes.flat:
        axis.set_axis_off()
    # DISPLAY LOOP Match each panel with its stored image and its title
    # zip stops when either the panel positions or the input images run out
    for axis, (image, panel_title) in zip(axes.flat, panels):
        display_image(axis, image, panel_title)
    figure.suptitle(title, fontsize=15, fontweight="bold")
    return figure
# ---


# --- build_figures()
def build_figures(scenes: list[SceneResult]) -> list[View]:
    """Build seven teaching stages, including multiple views where a comparison needs them.

    Logic:
        Each view has a stage, filename, and caption. The terminal guide uses
        that same mapping. All figures are saved before a window is displayed.
    """
    # Keep the teaching views in a list so their saved filenames match the terminal guide
    views: list[View] = []

    # --- add_view()
    # This small helper adds one completed figure and its step information to the list
    # It is used by every display step so the figures share the same structure
    def add_view(stage: int, filename: str, caption: str, panels: list[tuple[np.ndarray, str]],
                 rows: int = 1, columns: int = 3,
                 size: tuple[float, float] | None = None) -> None:
        """Keep one figure paired with its stage and explanation."""
        # Build the figure from stored image panels and remember where to save it
        figure = make_figure(panels, rows, columns, f"STEP {stage}/7: {caption}", size)
        views.append({"stage": stage, "filename": filename, "caption": caption, "figure": figure})
    # ---

    # __________________________________________
    # DISPLAY STEP 1: THE COMPLETE INPUT SCENES
    # ==========================================
    # DISPLAY STEP 1 Compare the unchanged photographs and their original dimensions
    # The panel list is built by reading one photograph at a time
    add_view(1, "01_originals.png", "Examine the three original photographs",
             [(display_size(s["original_bgr"]),
               f"{s['title']}\n{s['width']} x {s['height']} pixels") for s in scenes])
    # Create the matching grayscale view and show whole image brightness measurements
    add_view(1, "02_grayscale.png", "Read brightness before detecting faces",
             [(display_size(s["gray"]),
               f"{s['title']}\nMean {s['gray_mean']:.1f}; standard deviation {s['gray_std']:.1f}")
              for s in scenes])
    # __________________________________________
    # DISPLAY STEP 2: BASELINE AND INDEPENDENT REFERENCES
    # ==========================================
    # DISPLAY STEP 2 Show the first cascade results including the incorrect boxes
    add_view(2, "03_initial_faces.png", "Initial face candidates at native resolution",
             [(display_size(draw_boxes(s["original_bgr"], s["experiments"][0]["boxes"])),
               f"{s['title']}\n{len(s['experiments'][0]['boxes'])} candidates") for s in scenes])
    # Show the separately marked faces and eyes beside the detection results
    # These reference drawings are only for checking what the algorithms returned
    add_view(2, "04_reference_marks.png", "Visual reference marks, not detector outputs",
             [(display_size(reference_overlay(s)),
               f"{s['title']}\nReferences are used only for measurement") for s in scenes])
    # __________________________________________
    # DISPLAY STEP 3: RETAIN THE REVISIONS, INCLUDING MISSES
    # ==========================================
    # OUTER COMPARISON LOOP Build a separate six experiment figure for each photograph
    for scene in scenes:
        panels = []
        # INNER COMPARISON LOOP Add one panel for every saved face experiment
        # Show true positives false positives and missed faces beside its red boxes
        for experiment in scene["experiments"]:
            metrics = experiment["metrics"]
            panels.append((display_size(draw_boxes(scene["original_bgr"], experiment["boxes"])),
                           f"{experiment['name']}\nTP {metrics['tp']}; FP {metrics['fp']}; "
                           f"FN {metrics['fn']}"))
        # Use two rows of three panels so all six detector settings can be compared
        add_view(3, f"05_comparison_{scene['stem']}.png", f"Compare {scene['title'].lower()}",
                 panels, 2, 3)
    # __________________________________________
    # DISPLAY STEPS 4-6: SHOW EVERY SELECTED FACE
    # ==========================================
    # Start three panel collections for extracted faces aligned faces and blur strengths
    extracted, aligned, blurred = [], [], []
    # OUTER FACE DISPLAY LOOP Read the processed face records scene by scene
    for scene in scenes:
        # INNER FACE DISPLAY LOOP Build the three teaching comparisons for each face
        # Keep a face in these panels even if an eye search was not successful
        for face in scene["faces"]:
            name = f"{scene['title']}: face {face['number']}"
            # Resize the clean search crop to a common size for side by side display
            # This preview size is separate from the original crop used for treatment
            crop_display = cv2.resize(face["normalized_bgr"], (ALIGNED_EDGE, ALIGNED_EDGE))
            eye_display = draw_boxes(face["normalized_bgr"], face["provisional_pair"], False)
            eye_display = cv2.resize(eye_display, (ALIGNED_EDGE, ALIGNED_EDGE))
            # Draw the provisional eye boxes before making the alignment comparison
            extracted.append((np.hstack((crop_display, eye_display)),
                              f"{name}\nClean crop | provisional pair; "
                              f"{len(face['provisional_attempts'])} attempt(s)"))
            # Use the original preview when a face has no aligned result to display
            # Do not invent a completed alignment for an unresolved eye pair
            aligned_face = face.get("aligned_bgr", crop_display)
            final_eyes = draw_boxes(aligned_face, face.get("final_pair", []), False)
            angle = face.get("angle_degrees")
            angle_text = f"{angle:.2f} degrees" if angle is not None else "unresolved"
            aligned.append((np.hstack((eye_display, final_eyes)),
                            f"{name}\nBefore | aligned/new eye search; rotation {angle_text}"))
            # Show the aligned face next to the weaker and stronger Gaussian versions
            # An unresolved face still shows its available image without a false blur claim
            weak = face.get("weak_blur_bgr", aligned_face)
            strong = face.get("blurred_bgr", aligned_face)
            blurred.append((np.hstack((aligned_face, weak, strong)),
                            f"{name}\nAligned | weaker blur | final blur; {face['status']}"))
    # DISPLAY DECISION Only create face detail figures when at least one face was found
    # The group and portrait faces appear in the same ordered panel lists
    if extracted:
        rows = math.ceil(len(extracted) / 2)
        add_view(4, "06_extracted_faces.png", "Extract clean faces and estimate eye positions",
                 extracted, rows, 2, (16, 3.4 * rows))
        add_view(5, "07_alignment.png", "Rotate, scale, center, then detect eyes again",
                 aligned, rows, 2, (16, 3.4 * rows))
        add_view(6, "08_blur_strengths.png", "Compare eye treatment on aligned faces",
                 blurred, rows, 2, (18, 2.8 * rows))
    # Each clean full-scene output retains its original dimensions
    # Show each final photograph after the treated eyes have been returned to the scene
    # The saved final photograph itself stays at its original resolution
    add_view(6, "09_privacy_scenes.png", "Return only the treated eye regions to the scenes",
             [(display_size(s["final_bgr"]), f"{s['title']}\n"
               f"{s['summary']['faces_with_eye_treatment']} face(s) treated") for s in scenes])
    # Keep the original and final photographs together for the last comparison
    panels = []
    # FINAL DISPLAY LOOP Add two panels per scene with its original and treated image
    # The printed pixel count comes from the measured difference between the two
    for scene in scenes:
        panels.extend([(display_size(scene["original_bgr"]), f"{scene['title']}: original"),
                       (display_size(scene["final_bgr"]),
                        f"Final output; {scene['changed_pixels']:,} changed pixels")])
    # Use one row per photograph in the final comparison figure
    add_view(7, "10_final_comparison.png", "Compare final outputs with the untouched originals",
             panels, 3, 2, (13, 15))
    return views
# ---

# __________________________________________
# TERMINAL EXPLANATIONS - SEVEN TEACHING STEPS
# ==========================================

# --- format_number()
def format_number(value: float | int | None, decimals: int = 3) -> str:
    """Show undefined measurements as N/A rather than silently replacing them with zero."""
    return "N/A" if value is None else f"{value:.{decimals}f}"
# ---


# --- measurement_table()
def measurement_table(scene: SceneResult) -> str:
    """Format the six measured face experiments without typing results into the text."""
    # Start the terminal table with a fixed header for the six face experiments
    lines = ["    Experiment               TP   FP   FN   Precision   Recall       F1"]
    # TABLE LOOP Read each saved experiment and place its measured values in one row
    # Spacing in the formatted text keeps the terminal columns aligned
    for experiment in scene["experiments"]:
        m = experiment["metrics"]
        lines.append(f"    {experiment['name']:<24} {m['tp']:>3} {m['fp']:>4} {m['fn']:>4}"
                     f" {format_number(m['precision']):>11} {format_number(m['recall']):>8}"
                     f" {format_number(m['f1']):>8}")
    return "\n".join(lines)
# ---


# --- build_walkthrough()
def build_walkthrough(scenes: list[SceneResult], runtime: dict[str, Any]) -> list[list[str]]:
    """Explain the actual images, parameters, comparisons, and measured limitations.

    Logic:
        Counts come from the current run. A revision may improve a result,
        leave it unchanged, or make it worse. Keep those outcomes visible.
    """
    # DIMENSION LOOP Read the actual width height and brightness values for all scenes
    # The guide uses measured values from this run instead of typed example numbers
    dimensions = [f"{s['title']}: {s['width']} x {s['height']} pixels. "
                  f"Grayscale mean {s['gray_mean']:.2f}; standard deviation {s['gray_std']:.2f}."
                  for s in scenes]
    # TOTALS LOOP Add each selected result across the three photographs
    # The final teaching step uses these totals to describe the whole experiment
    totals = {name: sum(int(s["summary"][name]) for s in scenes) for name in (
        "reference_faces", "tp", "fp", "fn", "faces_with_eye_treatment",
        "unresolved_face_candidates", "selected_eye_centers", "correct_eye_centers",
        "fully_covered_reference_eyes", "initial_fully_covered_reference_eyes",
        "pairs_with_both_centers_correct")}
    # Keep the first experiment measurements separate from the selected results
    # This makes the baseline errors visible in the early teaching steps
    initial = [s["experiments"][0]["metrics"] for s in scenes]
    # BASELINE TOTALS LOOP Count the matched extra and missed faces across the scenes
    initial_totals = {name: sum(m[name] for m in initial) for name in ("tp", "fp", "fn")}
    # Build the explanations in seven groups with one group for each teaching step
    # Each paragraph describes settings images or counts already calculated by the script
    guide = [[
        "This assignment uses three color photographs from the web. The portrait shows "
        "one primarily front-facing person under indoor lighting. The outdoor photograph "
        "shows a group from head to feet. Its faces occupy a much smaller part of the "
        "scene, so that photograph also supplies the multiple-person and distant-face cases. "
        "The third photograph contains a cat, which supplies the nonhuman example.",
        "Look at the complete photographs before looking at the detections. No original "
        "has been cropped or recolored. The program checks each file's SHA-256, a fingerprint "
        "of its bytes, so the reference coordinates cannot silently be applied to a different "
        "version of the photograph. The source credits are kept with the results.",
        *dimensions,
        "OpenCV reads the color channels in BGR order: blue, green, and red. cvtColor() "
        "converts them into one uint8 intensity value per pixel, from 0 to 255. The first "
        "face experiment uses this original-resolution grayscale image without smoothing "
        "or contrast adjustment. Matplotlib converts display copies to RGB. Reducing a "
        "teaching view does not change the detector input.",
        "The images have visibly different illumination and colors, but they also show "
        "different subjects and backgrounds. Their brightness statistics describe the "
        "whole scenes. Those numbers do not isolate the effect of lighting alone, and "
        "the actual distance between the camera and each person is not known.",
        f"This run uses Python {runtime['python']}; OpenCV {runtime['opencv']}; "
        f"NumPy {runtime['numpy']}; Matplotlib {runtime['matplotlib']}. "
        f"Platform: {runtime['platform']}. Processing uses one OpenCV worker thread.",
    ], [
        "The initial classifier is haarcascade_frontalface_default.xml. This is a pretrained "
        "Haar cascade, not a person-identification model. It examines intensity patterns "
        "at different positions and sizes. A returned box is a face candidate, not proof "
        "that the enclosed region is a human face.",
        "The baseline uses scaleFactor=1.1, minNeighbors=5, and minSize=(24, 24). "
        "scaleFactor sets the spacing between search scales. minNeighbors sets the "
        "support required when nearby candidates are grouped. minSize excludes smaller "
        "search windows. None of these settings is a calibrated probability of correctness.",
        "Look at the red boxes and compare them with the original scenes. All returned "
        "candidates remain visible, including background mistakes and duplicate boxes. "
        "The separate reference view shows approximate visual annotations made from the "
        "original photographs. Those marks never enter the detector or choose an eye pair.",
        "A detected face is matched to at most one reference face. Intersection-over-union "
        "divides the overlapping area by the combined area of the boxes. Here, a match "
        "requires at least 0.50. The matching routine first maximizes the number of valid "
        "one-to-one matches, then their total overlap. An extra box is a false positive, "
        "and an unmatched reference face is a false negative.",
        f"Across the three baseline images, this run produced {initial_totals['tp']} "
        f"matched faces, {initial_totals['fp']} extra boxes, and {initial_totals['fn']} "
        "missed reference faces. Read the tables in the next step to see where they occurred.",
    ], [
        "Each revision starts from the stored original grayscale image. The second "
        "experiment changes only the face model to haarcascade_frontalface_alt.xml. "
        "The third retains that model but caps the longer scene edge at 1,000 pixels, "
        "preserving its proportions. This changes the sampling grid and the effective "
        "original-image size represented by the 24-pixel minimum search window.",
        "The fourth experiment applies global histogram equalization to the scaled "
        "input. The fifth instead uses CLAHE with clipLimit=2.0 and an 8 x 8 tile grid. "
        "Both are compared with the plain scaled image, not chained together. The sixth "
        "returns to plain grayscale and increases minNeighbors from 5 to 7. A stricter "
        "setting can remove a false positive, but it can also remove a real face.",
        *[s["title"] + ".\n" + measurement_table(s) for s in scenes],
        "Precision is TP/(TP+FP), recall is TP/(TP+FN), and F1 is "
        "2TP/(2TP+FP+FN). N/A means the denominator is zero. The cat has no reference "
        "human faces, so its recall is N/A, not 100%. A count of zero is a correct "
        "outcome on this one negative image, not a population-wide specificity estimate.",
        f"The selected configuration is {FINAL_EXPERIMENT} for all three photographs. "
        "It was chosen during development and is fixed in the script. The program does "
        "not pick a different model for each image or use an expected face count to "
        "suppress mistakes. Contrast changes and the stricter setting remain in the "
        "record even when their results are worse.",
    ], [
        "The red boxes were drawn on display copies. Face extraction uses the untouched "
        "original color photographs instead. The selected detector boxes are mapped back "
        "with the actual horizontal and vertical resize factors, then used to slice the "
        "original arrays. NumPy uses [y, x], while each OpenCV rectangle is (x, y, width, height).",
        "A separate face copy is resized to a maximum edge of 300 pixels for the provisional "
        "eye search. Enlarging a small face changes how the cascade samples it; it does "
        "not restore detail that the camera did not record. The clean original crop is "
        "kept for the later geometric transformation.",
        "The first eye search uses haarcascade_eye.xml on the upper 70% of the crop. "
        "Overlapping proposals are filtered, and candidate pairs are checked for plausible "
        "spacing, height, size, and placement on opposite sides of the face. These checks "
        "can reject a nose or brow proposal, but they do not establish that a pair is correct.",
        "When no pair passes, the program tries equalization and the eye-tree-eyeglasses "
        "cascade. The last attempts search the upper left and right halves separately "
        "with a finer scale step and lower grouping requirement. That last revision changes "
        "more than one setting, so its effect cannot be attributed to the region alone. "
        "Every attempted candidate list is saved. A missing pair remains unresolved.",
    ], [
        "A first eye estimate is needed before the face can be oriented. align_face() "
        "calculates the angle between those centers with atan2(), then uses their distance "
        "to calculate one uniform scale. The translation moves their midpoint to the "
        "center of the target eye line. This performs rotation, scaling, and centering; "
        "it is more than a square resize.",
        "The common canvas is 320 x 320 pixels. Its target eye centers are (96, 121.6) "
        "and (224, 121.6), which puts them at 30% and 70% of the width and 38% of the "
        "height. warpAffine() samples the original crop using the calculated matrix. "
        "Reflected pixels can fill the display border, but a separate validity mask "
        "prevents those artificial border pixels from becoming treatment data.",
        "Now look at the eye boxes on the aligned faces. They come from a new cascade "
        "search after the transformation. They are not the original boxes moved into "
        "place. The provisional estimates, final detections, transformation matrix, "
        "inverse matrix, and all retry settings are retained separately.",
        "The two estimated control points map to their targets within a small numerical "
        "tolerance. That checks the transformation mathematics, not the true eye locations. "
        "The program also transforms the independent reference eye marks and measures "
        "their remaining tilt. Approximate cascade-window centers can leave real eyes "
        "slightly misaligned even when the control-point check passes.",
    ], [
        "The eye treatment starts from each aligned color crop. The first margin is 35% "
        "of the detected eye-box width and height. The final margin increases to 60% "
        "on every face to cover more of the eye boundaries. Gaussian blur replaces "
        "pixels only within those padded regions. The comparison also shows a "
        "weaker sigma of 10% of the eye-box size beside a stronger final sigma of 45%. "
        "The minimum sigma is 2 pixels. The actual odd kernel and sigma are saved for each eye. "
        "Both padding and strength change, so this comparison does not isolate blur strength.",
        "Look for remaining eye detail in the weaker version before examining the final "
        "one. The final blur is deliberately strong, which also removes some surrounding "
        "detail inside the padded regions. A less visible seam would not necessarily mean "
        "better privacy. These pictures show the treatment; they are not a re-identification test.",
        "The inverse transformation maps the blurred pixels and their binary mask back "
        "to the original crop. Color uses linear interpolation, while the mask uses "
        "nearest-neighbor interpolation. Only pixels selected by that mask are replaced "
        "in the full scene. The program checks exact equality outside the mask rather "
        "than trusting that the two images look similar.",
        *[f"{s['title']}: {s['summary']['faces_with_eye_treatment']} face(s) received eye "
          f"treatment; {s['changed_pixels']:,} pixels changed; "
          f"outside-mask pixels unchanged: {s['outside_mask_unchanged']}." for s in scenes],
        "There is no animal-specific branch that forces the cat to remain unchanged. "
        "It enters the same human-face pipeline. When the selected detector returns "
        "no face candidates, the treatment mask is empty and the original decoded "
        "pixels remain unchanged. Any false face detection would still be reported.",
    ], [
        f"The selected face experiment matched {totals['tp']} of {totals['reference_faces']} "
        f"reference faces, with {totals['fp']} extra boxes and {totals['fn']} misses. "
        f"Eye processing produced {totals['selected_eye_centers']} final eye centers on "
        f"{totals['faces_with_eye_treatment']} face candidates. "
        f"Unresolved face candidates: {totals['unresolved_face_candidates']}.",
        f"Under the fixed eye-center rule, {totals['correct_eye_centers']} of "
        f"{2 * totals['reference_faces']} reference eyes were localized within tolerance. "
        f"Both centers met that rule on {totals['pairs_with_both_centers_correct']} faces. "
        "The tolerance is 10% of the reference eye separation, with a two-pixel minimum, "
        "measured in the original image. A cascade window is an eye region, not an exact "
        "pupil landmark. Narrow or partly closed eyes make that distinction important.",
        f"The initial mask fully covered {totals['initial_fully_covered_reference_eyes']} "
        f"reference eye regions. The final treatment mask fully covered "
        f"{totals['fully_covered_reference_eyes']} "
        f"of {2 * totals['reference_faces']} marked eye regions. Coverage and center accuracy "
        "answer different questions. A padded blur can cover an eye even when the center "
        "of its detection window falls outside the localization tolerance. Neither count "
        "alone proves that the person cannot be identified.",
        "The reference marks are approximate visual annotations, not an independently "
        "audited benchmark. Inspect the saved reference overlays, especially the small "
        "eyes in the group image. The CSV reports each eye's error, tolerance, coverage, "
        "and remaining alignment angle rather than hiding the weaker measurements "
        "inside an overall success label.",
        "All three photographs were used during development. The program demonstrates "
        "what these settings do on this small set, not how accurately they will process "
        "a new population of faces. Eye blurring also leaves other identifying details, "
        "including the rest of the face, clothing, and name patches. The saved outputs "
        "are an assignment demonstration, not a guarantee of anonymization.",
        "All images, tables, detector attempts, reference marks, and this explanation "
        "were saved before the first interactive view. The APA summary is a separate "
        "assignment deliverable and is not generated by this script.",
    ]]
    # Return the complete guide so it can be saved before any windows open
    return guide
# ---

# __________________________________________
# TERMINAL FORMATTING AND SAVED RESULTS
# ==========================================

# --- style_text()
def style_text(message: str, style: str = "", *, stream: TextIO | None = None) -> str:
    """Add terminal color only when the actual output destination supports it."""
    # Check the actual output destination before adding any terminal color
    # A saved transcript and a redirected terminal need ordinary readable text
    output = sys.stdout if stream is None else stream
    if (not style or not output.isatty() or os.environ.get("NO_COLOR")
            or os.environ.get("TERM", "").lower() == "dumb"):
        return message
    # Look up the selected terminal color and add the reset code after the text
    code = TEXT_STYLES.get(style, "")
    return f"{code}{message}{TEXT_RESET}" if code else message
# ---


# --- format_step()
def format_step(step: int, paragraphs: list[str], views: list[View],
                color: bool = False) -> str:
    """Format one step for both the terminal and the plain-text transcript."""
    # Use StringIO to collect one complete explanation before printing or saving it
    # This gives the live terminal and saved transcript the same text layout
    output = io.StringIO()
    rule = style_text("=" * 88, "rule" if color else "")
    output.write(f"\n{rule}\n")
    output.write(style_text(f"STEP {step}/7: {STAGE_TITLES[step - 1]}",
                            "heading" if color else "") + "\n")
    output.write(rule + "\n\n")
    # OUTER EXPLANATION LOOP Read every paragraph for the current teaching step
    # Keep each paragraph in the order used by the figures and the assignment
    for paragraph in paragraphs:
        # INNER EXPLANATION LOOP Read each existing line within that paragraph
        # Measurement tables already contain separate lines for their rows
        for line in paragraph.splitlines():
            # Leave an indented table row alone so its numbers stay in columns
            # Wrap ordinary text to the selected terminal width
            wrapped = line if line.startswith("    ") else textwrap.fill(
                line, width=88, break_long_words=False, break_on_hyphens=False)
            output.write(style_text(wrapped, "info" if color else "") + "\n")
        output.write("\n")
    # FIGURE LIST LOOP Find every saved view that belongs to this teaching step
    # Print its filename so the student can open the same image afterward
    for view in views:
        if view["stage"] == step:
            output.write(f"Saved teaching view: figures/{view['filename']}\n")
    return output.getvalue()
# ---


# --- save_image()
def save_image(path: Path, image: np.ndarray) -> None:
    """Write a PNG and report a failed write instead of claiming completion."""
    # Create missing parent folders before attempting to save this PNG image
    path.parent.mkdir(parents=True, exist_ok=True)
    # ERROR CHECK imwrite reports whether OpenCV wrote the image successfully
    # A failed write stops the program instead of reporting a completed experiment
    if not cv2.imwrite(str(path), image):
        raise OSError(f"Could not save the output image: {path}")
# ---


# --- metadata_only()
def metadata_only(value: Any) -> Any:
    """Keep numerical records in JSON while saving image arrays separately as PNGs."""
    # JSON cannot directly store the full NumPy image arrays
    # Keep numbers and other small records while each image is saved as a PNG
    if isinstance(value, dict):
        # DICTIONARY LOOP Copy every nonimage entry and check its nested values as well
        return {key: metadata_only(item) for key, item in value.items()
                if not isinstance(item, np.ndarray)}
    # LIST LOOP Visit nested lists and tuples and remove image arrays inside them
    if isinstance(value, (list, tuple)):
        return [metadata_only(item) for item in value]
    # Convert NumPy number types to ordinary Python values that JSON can save
    if isinstance(value, np.generic):
        return value.item()
    return value
# ---


# --- save_table()
def save_table(path: Path, rows: list[dict[str, Any]]) -> None:
    """Save an inspectable CSV using the already-calculated field order."""
    # A scene without reference faces can produce no eye measurement rows
    # Write a short explanation rather than an empty file without any information
    if not rows:
        path.write_text("No reference rows for this run\n", encoding="utf-8")
        return
    # Use the first measurement row to select the CSV column names
    # The writer keeps the same field order for every later row
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
# ---


# --- save_results()
def save_results(output: Path, scenes: list[SceneResult], views: list[View],
                 guide: list[list[str]], runtime: dict[str, Any],
                 model_metadata: dict[str, Any]) -> None:
    """Save the complete experiment before opening the first teaching view.

    Logic:
        Original-size privacy PNGs retain pixel equality outside the mask.
        Full-scene box previews use at most 1,000 pixels on the longer edge;
        JSON retains every rectangle in both detector and original coordinates.
    """
    # Create the output folder and its figures subfolder before writing any results
    # The three original photographs remain in their separate input folder
    output.mkdir(parents=True, exist_ok=True)
    figure_directory = output / "figures"
    figure_directory.mkdir(exist_ok=True)
    # Collect face and eye measurements while saving the individual scene images
    face_rows = []
    eye_rows = []
    # OUTER SAVE LOOP Create a separate result folder for each source photograph
    # Save the complete final image and the treatment masks at original resolution
    for scene in scenes:
        destination = output / scene["stem"]
        destination.mkdir(exist_ok=True)
        # Save the grayscale input reference marks and final treatment for this scene
        # The selected red face boxes are another display file and not the clean final image
        save_image(destination / "original_grayscale.png", scene["gray"])
        save_image(destination / "reference_annotations.png", reference_overlay(scene))
        save_image(destination / "final_eye_blurred.png", scene["final_bgr"])
        save_image(destination / "final_treatment_mask.png", scene["scene_mask"])
        save_image(destination / "initial_treatment_mask.png", scene["weak_scene_mask"])
        save_image(destination / "selected_face_boxes.png",
                   draw_boxes(scene["original_bgr"], scene["selected"]["boxes"]))
        # EXPERIMENT SAVE LOOP Keep each of the six detector inputs and its red box preview
        # Add one CSV measurement row for each experiment in the current photograph
        for experiment in scene["experiments"]:
            # Give each experiment its own folder so the different settings stay separate
            folder = destination / "experiments" / experiment["name"]
            save_image(folder / "detector_input.png", experiment["detector_gray"])
            save_image(folder / "face_boxes_preview.png", display_size(
                draw_boxes(scene["original_bgr"], experiment["boxes"])))
            # Record the exact cascade preprocessing and timing beside each accuracy count
            # The measured numbers come from the experiment records calculated earlier
            face_rows.append({"scene": scene["stem"], "experiment": experiment["name"],
                              "cascade": CASCADE_FILES[experiment["cascade"]],
                              "preprocessing": experiment["preprocessing"],
                              "detector_width": experiment["detector_width"],
                              "detector_height": experiment["detector_height"],
                              "scale_factor": experiment["scale_factor"],
                              "min_neighbors": experiment["min_neighbors"],
                              "min_size": experiment["min_size"], **experiment["metrics"],
                              "elapsed_seconds": experiment["elapsed_seconds"]})
        # FACE SAVE LOOP Create a separate folder for every selected detected face
        # This includes faces where a provisional or final eye search was unresolved
        for face in scene["faces"]:
            # Use two digits in the face number so saved folders remain in reading order
            folder = destination / "faces" / f"face_{face['number']:02d}"
            image_names = ("crop_bgr", "normalized_bgr", "aligned_bgr", "valid_mask",
                           "weak_blur_bgr", "blurred_bgr", "aligned_mask", "weak_aligned_mask",
                           "restored_bgr",
                           "restored_mask")
            # IMAGE SAVE LOOP Check each possible face image by its result dictionary name
            # Some images only exist if the eye alignment and treatment succeeded
            for name in image_names:
                # SAVE DECISION Write only the images that were actually created for this face
                if name in face:
                    save_image(folder / f"{name}.png", face[name])
            # SEARCH PHASE LOOP Save both provisional and aligned eye search attempts
            # The two phases use different face images and must remain separate
            for phase, image_key in (("provisional", "normalized_bgr"), ("final", "aligned_bgr")):
                # ATTEMPT LOOP Save the raw eye candidates returned by every search attempt
                # The numbered previews show failed attempts as well as successful ones
                for index, attempt in enumerate(face.get(f"{phase}_attempts", []), start=1):
                    # Draw candidate boxes only on a copy of the search image for that attempt
                    save_image(folder / f"{phase}_{index:02d}_candidates.png",
                               draw_boxes(face[image_key], attempt["candidates"], False))
            # Save the selected final eye boxes when the aligned search was performed
            if "final_pair" in face:
                save_image(folder / "final_selected_eyes.png",
                           draw_boxes(face["aligned_bgr"], face["final_pair"], False))
        # Collect this scene eye measurements for the combined CSV file
        eye_rows.extend(scene["eye_rows"])
    # Save all figures while they are still hidden
    # FIGURE SAVE LOOP Write each teaching figure while its window is still hidden
    # The figures use stored arrays and do not repeat the face or eye calculations
    for view in views:
        view["figure"].savefig(figure_directory / view["filename"], dpi=FIGURE_DPI)
    # Save the face eye and per scene measurements in three separate CSV files
    # CSV tables make the individual errors and experiment settings easy to inspect
    save_table(output / "face_measurements.csv", face_rows)
    save_table(output / "eye_measurements.csv", eye_rows)
    save_table(output / "processing_summary.csv", [s["summary"] for s in scenes])
    # The JSON record stores the runtime model details settings and measurements
    # It also keeps the reference annotations clearly separate from detection results
    record = {
        "assignment": "CSC515 Module 8 Option 2", "runtime": runtime,
        "models": model_metadata, "selected_experiment": FINAL_EXPERIMENT,
        "face_iou_threshold": FACE_IOU_THRESHOLD,
        "eye_error_fraction": EYE_ERROR_FRACTION, "eye_error_minimum_px": EYE_ERROR_MINIMUM,
        "target_eye_centers": TARGET_EYES.tolist(),
        "annotation_note": "Approximate visual marks from originals, not expert benchmark labels",
        "reference_annotations": REFERENCE_ANNOTATIONS,
        # Remove large image arrays from the scene records before writing JSON
        "scene_results": metadata_only(scenes),
        # VIEW RECORD LOOP Save the figure filenames stages and captions without Figure objects
        "views": [{k: v for k, v in view.items() if k != "figure"} for view in views],
    }
    # Write the experiment and reference records with readable JSON indentation
    # Keep the actual image pixels in their PNG files instead
    (output / "experiment_results.json").write_text(
        json.dumps(record, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (output / "reference_annotations.json").write_text(
        json.dumps(REFERENCE_ANNOTATIONS, indent=2) + "\n", encoding="utf-8")
    # Write the seven teaching explanations to a text file before opening windows
    with (output / "terminal_output.txt").open("w", encoding="utf-8") as stream:
        stream.write("CSC515 Module 8 - Face Detection and Privacy\n")
        # TRANSCRIPT LOOP Write each step using the same formatter used by the terminal
        # The saved explanation does not include terminal color codes
        for step, paragraphs in enumerate(guide, start=1):
            stream.write(format_step(step, paragraphs, views))
# ---

# __________________________________________
# TEACHING CONTROLS - WINDOWS AND TERMINAL INPUT
# ==========================================

# --- wait_for_guide_command()
def wait_for_guide_command(figure: Figure, commands: queue.Queue[str],
                           final_view: bool = False) -> str:
    """Read C/Q while the main thread keeps the displayed figure responsive.

    Logic:
        One persistent input reader serves the whole walkthrough. Closing a
        window does not leave a second reader competing for later terminal input.
        Closing an intermediate window continues; closing the last window quits.
    """
    # The final figure asks for Q because there is no next view to continue to
    prompt = ("Enter Q to finish, then press Enter: " if final_view else
              "Enter C to continue or Q to quit, then press Enter: ")
    # COMMAND VALIDATION LOOP Keep reading until the user gives a valid instruction
    # C advances intermediate views while Q ends the walkthrough
    while True:
        print(style_text(prompt, "prompt"), end="", flush=True)
        # WAIT LOOP Let the current figure process its events while terminal input is pending
        # The queue remains empty until the reader thread sends a command
        while commands.empty():
            # A closed window counts as continue except when it is the last view
            if not plt.fignum_exists(figure.number):
                print("\nThe figure was closed.", flush=True)
                return "Q" if final_view else "C"
            # Run a short figure event interval to keep the window responsive
            figure.canvas.start_event_loop(0.05)
        # Get the command that the terminal reader placed in the shared queue
        command = commands.get()
        # COMMAND DECISION Return only an allowed command for this view
        # Invalid text prints the available choices and repeats the loop
        if command == "Q" or (command == "C" and not final_view):
            return command
        print("Please enter Q." if final_view else "Please enter C or Q.", flush=True)
# ---


# --- run_walkthrough()
def run_walkthrough(guide: list[list[str]], views: list[View],
                    no_show: bool, no_pause: bool) -> None:
    """Present the saved explanations and figures without repeating image calculations."""
    # Use one shared queue for all teaching views to transfer terminal commands
    # Only the main thread will open or update the Matplotlib figures
    commands: queue.Queue[str] = queue.Queue()

    # --- read_commands()
    def read_commands() -> None:
        """Transfer terminal lines to the main thread without touching Matplotlib."""
        # INPUT READER LOOP Read terminal lines until the user quits or input ends
        # This loop runs in a separate thread while the main thread displays figures
        while True:
            try:
                # Read one line and wait for Enter without drawing or updating a figure
                line = sys.stdin.readline()
            except OSError:
                commands.put("Q")
                return
            if not line:
                commands.put("Q")
                return
            # Remove extra spaces and accept lowercase as well as uppercase input
            command = line.strip().upper()
            commands.put(command)
            if command == "Q":
                return
    # ---

    # DISPLAY DECISION First check whether actual desktop figures were requested
    # The Agg backend can save figures but cannot open an interactive window
    if not no_show:
        # Error check: Agg can save images but cannot open an interactive desktop window
        if views and views[0]["figure"].canvas.required_interactive_framework is None:
            raise ValueError("No interactive Matplotlib backend is available; use --no-show")
        if not no_pause:
            # Start the terminal reader once when the user wants C and Q pauses
            threading.Thread(target=read_commands, daemon=True).start()
    # OUTER WALKTHROUGH LOOP Print each of the seven explanations in order
    # The figures were built and saved earlier so no detector runs here
    for step, paragraphs in enumerate(guide, start=1):
        print(format_step(step, paragraphs, views, color=True), flush=True)
        # NO SHOW DECISION Print the explanation but skip all desktop figures
        if no_show:
            continue
        # INNER WALKTHROUGH LOOP Visit the complete list of saved teaching views
        # Only views with the current step number are displayed now
        for index, view in enumerate(views):
            # Skip any view assigned to a different explanation step
            if view["stage"] != step:
                continue
            figure = view["figure"]
            print(f"View {index + 1}/{len(views)}: {view['caption']}", flush=True)
            # Open the current figure and give its window a short interval for events
            figure.show()
            figure.canvas.start_event_loop(0.05)
            # When pauses are enabled wait for C or Q before closing the current figure
            # Q stops the guide but does not remove files already saved on disk
            if not no_pause:
                command = wait_for_guide_command(figure, commands, index == len(views) - 1)
                plt.close(figure)
                if command == "Q":
                    plt.close("all")
                    return
    # The no pause option leaves the figures open until their windows are closed
    if not no_show and no_pause:
        plt.show()
    plt.close("all")
# ---

# _________________________________________________________
# MAIN FUNCTION - Interface of the program (entry point)
# =======================================================

# --- main()
def main() -> int:
    """Calculate, measure, save, and explain the three-image face-privacy experiment.

    Returns:
        0 for completion or Q, 1 for a processing/input/output error, and 130
        when the user interrupts the program with Ctrl+C.

    Logic:
        Finish calculations before evaluation. Finish saving before display.
        Preserve the unsuccessful experiments rather than replacing their results.
    """
    # Read the optional command line settings before loading any image
    args = parse_arguments()
    # Use the noninteractive Agg backend when figures should only be saved to disk
    if args.no_show:
        plt.switch_backend("Agg")
    # Disable automatic figure windows so the complete experiment can be saved first
    plt.ioff()
    # One worker limits thread overhead and makes repeated runs easier to compare
    # Use one OpenCV processing thread for a consistent small assignment run
    cv2.setNumThreads(1)
    # Keep file reading processing and saving inside the same error handling section
    try:
        # Check the folder arrangement before loading any image or model
        # Read the pretrained face and eye classifiers once for all three photographs
        check_output_directory(args.input_dir, args.output_dir)
        classifiers, model_metadata = load_cascades()
        # Record the installed library versions for the actual program execution
        # These details help explain differences when running on another computer
        runtime = {"python": sys.version.split()[0], "opencv": cv2.__version__,
                   "numpy": np.__version__, "matplotlib": matplotlib.__version__,
                   "platform": sys.platform, "matplotlib_backend": matplotlib.get_backend(),
                   "opencv_threads": cv2.getNumThreads()}
        # Start an empty collection for the three source photographs
        scenes = []
        print(style_text("CSC515 Module 8 - Face Detection and Privacy", "heading"), flush=True)
        print("Read the original photographs and calculate the six face experiments.", flush=True)
        # __________________________________________
        # CALCULATE THE THREE SCENES BEFORE LOOKING AT REFERENCE LABELS
        # ==========================================
        # MAIN PROCESSING LOOP Read and process the three photographs in source order
        # Each photograph uses the same face experiments and eye processing procedure
        for source in SOURCES:
            # PHASE 1 Check the original file and prepare its grayscale image
            scene = load_and_prepare(source, args.input_dir)
            # PHASE 2 Run every face detector experiment and select the declared result
            run_face_experiments(scene, classifiers)
            # PHASE 3 Extract each detected face then align and blur accepted eye regions
            process_faces(scene, classifiers)
            # Keep the complete scene result for the later measurement and display steps
            scenes.append(scene)
        # __________________________________________
        # MEASURE THE STORED RESULTS AND PREPARE THE EXPLANATIONS
        # ==========================================
        # MEASUREMENT LOOP Compare every stored scene with its visual reference marks
        # This happens after processing so those marks never select faces or eyes
        for scene in scenes:
            measure_results(scene)
        # Build the comparison figures and terminal explanations from the stored results
        views = build_figures(scenes)
        guide = build_walkthrough(scenes, runtime)
        # __________________________________________
        # SAVE THE COMPLETE EXPERIMENT BEFORE C/Q NAVIGATION
        # ==========================================
        # Save the final images masks tables JSON records and all teaching figures first
        save_results(args.output_dir, scenes, views, guide, runtime, model_metadata)
        print(style_text("All images, measurements, and explanations were saved before the guide.",
                          "success"), flush=True)
        # Present the seven step guide only after its results are already on disk
        run_walkthrough(guide, views, args.no_show, args.no_pause)
        print(style_text(f"\nSaved results: {args.output_dir.resolve()}", "success"), flush=True)
        return 0
    # ERROR CHECK Report a failed input model image operation or output write
    # Return a failure status without printing a completion message
    except (OSError, ValueError, cv2.error) as error:
        print(style_text(f"The program could not finish: {error}", "error", stream=sys.stderr),
              file=sys.stderr, flush=True)
        return 1
    # Ctrl C stops the walkthrough and returns the usual interruption status
    except KeyboardInterrupt:
        print("\nThe walkthrough was stopped. Previously saved files remain available.",
              file=sys.stderr)
        return 130
    # CLEANUP Close any Matplotlib figures even if the program ended with an error
    finally:
        plt.close("all")
# ---

# __________________________________________
# MODULE INITIALIZATION
# ==========================================

# Initialize and start the program
# Start main only when this file is executed as a Python program
# Importing its definitions into another script does not run the experiment
if __name__ == "__main__":
    raise SystemExit(main())

# __________________________________________
# END OF FILE
# ==========================================
