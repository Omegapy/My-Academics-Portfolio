# -----------------------------------------------------------------------------
# Module Type: executable script
# Author: Alexander Ricciardi (Omega.py)
# Created: 10/04/2026
# -----------------------------------------------------------------------------
# Course: Foundations of Computer Vision CSC515
# Professor: Dr. Bingdong Li
# Term: Fall C (26FC) - 2026
# Assignment: Portfolio Milestone Module 3 - Option #2: Blending Images in OpenCV
# -----------------------------------------------------------------------------
# The Program:
# Load Alex.png and the_rock.png from org_images/. The second photo shows The Rock.
# Crop and align Alex's face,
# compare skin colors and blend the corrected face into The Rock'sphotograph.
# Compare both blending methods with the original baseline in the teaching views.
# Save the selected result and its four-panel comparison in mod_images/.
# Calculate all results first, then open each figure before its explanation.
# Type C in the terminal to continue or Q to quit, then press Enter.
# Terminal colors separate headings, code, examples, and status messages.
# -----------------------------------------------------------------------------
# Requirements:
# - Python 3.12
# - OpenCV 4.13.0 (opencv-contrib-python==4.13.0.92)
# - NumPy 2.5.3; Matplotlib 3.11.2
#
# Run from this folder:
#    python Module3_Portfolio_Option2.py
#
# Contents Overview:
# - load_bgr_image() / save_bgr_image_as_png()
#   - Read original BGR images and write a separate PNG with an error check.
# - validate_alex_and_the_rock_images()
#   - Keep the manually measured coordinates tied to the original photograph sizes.
# - get_alex_to_the_rock_transform()
#   - Map three reference points from Alex's cropped face to The Rock'sface.
# - align_alex_face_and_build_baseline_mask()
#   - Crop and align Alex's face, then prepare the original baseline mask.
# - create_ellipse_mask() / create_alex_face_blend_alpha()
#   - Select oval patches and calculate a gradual transition inside the face boundary.
# - prepare_alex_and_the_rock_masks()
#   - Keep coverage, face selection, skin samples, and color correction strength separate.
# - match_alex_skin_to_the_rock()
#   - Move Alex's sampled skin colors toward The Rock'swhile protecting facial detail.
# - alpha_blend_foreground_with_background()
#   - Mix Alex's prepared face and The Rock'sphotograph using a weight for each pixel.
# - clone_alex_face_into_the_rock()
#   - Match boundary colors with normal cloning and restore the unchanged exterior.
# - create_alex_on_the_rock_results()
#   - Calculate the baseline and both corrected results once, using the same originals.
# - show_bgr_image() / save_alex_the_rock_comparison()
#   - Use the same display rules for photographs in saved panels and teaching views.
# - sample_alex_and_the_rock_lab_colors()
#   - Collect the skin-color samples and shared graph intervals used in Step 6.
# - style_text() / print_wrapped() / print_banner() / print_face_blending_guide_step()
#   - Explain the processing code with color accents and named variables.
# - build_face_blending_guide_figure()
#   - Show the matching image comparisons and Lab plots for each teaching stage.
# - wait_for_guide_command() / run_face_blending_guide()
#   - Read C or Q in the terminal while the teaching pictures stay responsive.
# - main()
#   - Calculate and save results, then present the guided walkthrough.
# -----------------------------------------------------------------------------

"""Create a fake image by replacing a face with another face using OpenCV.

The original first image org_images/the_rock.png is an image of Dwayne "The Rock" Johnson.
The second original image org_images/Alex.png is an image of Alex (me).
The program replaces The Rock'sface with Alex's face using OpenCV.

Step 1: Load the two original images.
Step 2: Crop and align Alex's face.
Step 3: Prepare the mask for Alex's face.
Step 4: Prepare the mask for The Rock'sface.
Step 5: Prepare the mask for the transition area.
Step 6: Correct the skin color of Alex's face.
Step 7: Blend the corrected face with The Rock'sface.
Step 8: Clone the face to match boundary colors.
Step 9: Create the final result.
Step 10: Save the final result.
Step 11: Save the comparison.
Step 12: Execute the program and display the results in a guide.

"""

# __________________________________________
# IMPORTS
# ==========================================

# Handle files.
import os  # use for terminal color preferences
from pathlib import Path  # use for path manipulation

# Let the program wait for typing while Matplotlib
# continues updating the pictures. They do not take part in the image calculations.
from queue import Queue  # pass the terminal response back to the walkthrough
import shutil  # use for reading terminal dimensions
import sys  # use for terminal input, output, and the program's exit status
import textwrap  # use for wrapping long lines of text
from threading import Thread  # wait for input while the picture windows stay responsive
from typing import TextIO  # use for type hints

# Core Imports
# OpenCV performs the image operations, and NumPy stores and calculates the arrays.
# Matplotlib displays the teaching views. FigureCanvasAgg renders the saved comparison
# directly to a PNG, while pyplot manages the windows shown during the walkthrough.
import cv2  # use for opencv
import matplotlib  # use for matplotlib
import matplotlib.pyplot as plt  # use for plotting
from matplotlib.backends.backend_agg import FigureCanvasAgg  # use for creating figures
from matplotlib.figure import Figure  # use for creating figures
import numpy as np  # use for array operations

# __________________________________________
# PATHS AND FACE COORDINATES
# ==========================================

# ----------------------
# File paths
# ______________________

ASSIGNMENT_DIRECTORY = Path(__file__).resolve().parent
ALEX_IMAGE_PATH = ASSIGNMENT_DIRECTORY / "org_images" / "Alex.png"
THE_ROCK_IMAGE_PATH = ASSIGNMENT_DIRECTORY / "org_images" / "the_rock.png"
OUTPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "mod_images"
# ALEX_ON_THE_ROCK_RESULT_PATH is the full-size face replacement. ALEX_THE_ROCK_COMPARISON_PATH is a
# separate
# picture containing four panels. Neither path points to an original photograph.
ALEX_ON_THE_ROCK_RESULT_PATH = OUTPUT_DIRECTORY / "alex_on_the_rock.png"
ALEX_THE_ROCK_COMPARISON_PATH = OUTPUT_DIRECTORY / "face_blending_comparison.png"

# ----------------------
# Faces coordinates
# ______________________

# Manual coordinates are measured in pixels in each original photograph.
# Left, top, right, bottom. Right and bottom limits are exclusive.
# x increases toward the right; y increases downward. OpenCV points use [x, y],
# while NumPy image slices use [row, column], which is [y, x]. Keeping that order
# clear matters when the crop and the eye/mouth points are used together.
ALEX_FACE_CROP_BOUNDS = (240, 500, 1230, 1770)
# Image-left eye, image-right eye, mouth center. Left means the viewer's left.
# Each array has three rows and two columns. Matching rows name the same feature
# in the two photographs. float32 supplies the point format used by getAffineTransform().
ALEX_FACE_ALIGNMENT_POINTS = np.float32([[548, 918], [954, 914], [752, 1334]])
THE_ROCK_FACE_ALIGNMENT_POINTS = np.float32([[530, 458], [734, 467], [635, 705]])
# The points trace the outline of Alex's forehead, glasses, cheeks, and beard.
# It uses Alex's original image coordinates, just like ALEX_FACE_ALIGNMENT_POINTS.
# The points form a polygon around the face. int32 stores whole-pixel
# positions for fillPoly(), which fills the inside of that polygon in a mask.
ALEX_BASELINE_FACE_OUTLINE = np.int32(
    [
        [340, 650],
        [450, 550],
        [710, 510],
        [970, 570],
        [1110, 650],
        [1160, 815],
        [1200, 840],
        [1160, 1100],
        [1080, 1470],
        [980, 1600],
        [850, 1680],
        [720, 1710],
        [575, 1630],
        [465, 1490],
        [360, 1230],
        [305, 1090],
        [270, 880],
        [310, 840],
    ]
)


# -----------------------
# Masks kernel and sigma
# _______________________

# -----------------------------------------------------------------------------
# The baseline smooths only its mask, an array of weights. Width and sigma are
# measured in pixels in The Rock'simage.
# -----------------------------------------------------------------------------
ALEX_BASELINE_MASK_KERNEL = (61, 61)  # The size of the Gaussian kernel used to smooth the mask.
# The standard deviation of the Gaussian kernel used to smooth the mask.
ALEX_BASELINE_MASK_SIGMA = 12.0

# -----------------------------------------------------------------------------
# The old outline and Gaussian are used to create the baseline
# -----------------------------------------------------------------------------
ALEX_IMAGE_SIZE = (1536, 2048)  # Width, height of Alex's original photograph.
THE_ROCK_IMAGE_SIZE = (1192, 1370)  # Width, height of The Rock'soriginal photograph.
# Keep a separate copy of Alex's outline for the corrected blends.
# copy() gives the corrected path its own array, so adjusting that outline later
# would leave the baseline outline available for comparison.
ALEX_FINAL_FACE_OUTLINE = ALEX_BASELINE_FACE_OUTLINE.copy()

# -----------------------
# Feather Mask
# _______________________
#
# The feather mask is used to create a smooth transition between Alex's clipped face and The Rock'simage.


# Width controls how far the final blending weights fade from the Alex and The Rock's
# face boundary. It is measured on The Rock'simage grid after Alex is aligned.
ALEX_FACE_MASK_FEATHER_PIXELS = 24.0

# -------------------------
# Skin and Protected Areas
# _________________________

# ------------------------------------
# Skin color samples  
# ------------------------------------ 
# Both lists use The Rock'simage grid. Alex's patches are measured after alignment.
# Small forehead and cheek patches avoid frames, eyebrows, lips, beard, and glare.
ALEX_SKIN_SAMPLE_PATCHES = [
    (535, 346, 20, 16),
    (690, 340, 24, 20),
    (496, 598, 17, 21),
    (778, 608, 20, 28),
]
THE_ROCK_SKIN_SAMPLE_PATCHES = [
    (535, 346, 20, 16),
    (690, 340, 24, 20),
    (496, 590, 17, 21),
    (778, 590, 20, 28),
]

# -----------------------------------------
# Alex protected areas (glasses and beard) 
# -----------------------------------------
# Ellipses (circles) cover Alex's glasses and beard after alignment on The Rock'simage.
# They reduce color changes in those areas without removing any part of the face mask.
ALEX_PROTECTED_FEATURE_PATCHES = [(632, 490, 222, 91), (630, 759, 170, 127)]
# Standard deviation of the Gaussian kernel used to smooth the protected-features mask.
ALEX_FEATURE_MASK_SIGMA = 12.0
# Strength of the color correction around the glasses and beard.
# These areas still get less correction, but enough to reduce the red tint around them.
ALEX_PROTECTED_FEATURE_COLOR_STRENGTH = 0.65

# ------------------------------------  
# The Lab: Color correction 
# ____________________________________  

# The Lab is used to measure and adjust colors. 
#
# It separates lightness (L) from green/red (a) and blue/yellow (b).

# Strength of the color correction applied to the Lab channels.
# A strength of 0 keeps a channel; 1 would apply the whole statistical adjustment.
# The lighter Lab strength is used because the photographs have different lighting.
# I use a stronger adjustment for a because Alex's face was still too red.
# Tuple positions follow the channel order: (L lightness, a green/red, b blue/yellow).
# ALEX_LAB_CORRECTION_STRENGTH sets the amount used.
ALEX_LAB_CORRECTION_STRENGTH = (0.30, 0.95, 0.80)

# MAX_ALEX_LAB_CORRECTION_STRENGTH supplies the upper limits
# checked by match_alex_skin_to_the_rock(), so a changed setting cannot exceed those limits.
MAX_ALEX_LAB_CORRECTION_STRENGTH = (0.50, 1.00, 0.85)

# The Rock'ssampled colors vary less. Let the gain narrow Alex's color spread.
# This also avoids pushing less-red areas of the face too far toward green.
ALEX_TO_THE_ROCK_LAB_GAIN_BOUNDS = (0.25, 1.10)

# The red/green channel needs a larger allowed shift to remove the remaining red tint.
MAX_ALEX_LAB_SHIFT = (12.0, 32.0, 12.0)

# A skin sample needs enough selected pixels for the mean and spread calculations.
# MIN_ALEX_THE_ROCK_SKIN_SAMPLE_PIXELS rejects an empty or very small selection.
MIN_ALEX_THE_ROCK_SKIN_SAMPLE_PIXELS = 64

# ALEX_SKIN_STD_EPSILON marks a
# channel with too little variation to use safely as the divisor when calculating gain.
ALEX_SKIN_STD_EPSILON = 0.5

# Direct comparison favored alpha: normal cloning brightened the forehead and
# lenses too much. The alpha result keeps their detail while reducing the warm cast.
# This string matches a key in the alex_on_the_rock_candidates dictionary returned by
# create_alex_on_the_rock_results().
# Both methods are calculated and displayed; this setting chooses which one is saved
# to ALEX_ON_THE_ROCK_RESULT_PATH. It does not turn off the other comparison.
SELECTED_ALEX_ON_THE_ROCK_METHOD = "alex_on_the_rock_alpha"

#------------------------------------
# Save directory for walkthrough figures
#____________________________________
# Keep a saved copy of each view in the walkthrough folder.
WALKTHROUGH_DIRECTORY = OUTPUT_DIRECTORY / "diagnostics" / "walkthrough"

# ------------------------------------
# Walkthrough Terminal Output
# ___________________________________

# The baseline and corrected blends are separate comparisons from the same inputs.
# The title order matches the numbered cases in print_face_blending_guide_step() and
# build_face_blending_guide_figure().
# A displayed step starts at 1; indexing this tuple uses step - 1 because Python starts at 0.
STAGE_TITLES = (
    "Original photographs and color values",
    "Crop the source face",
    "Align the eyes and mouth",
    "First blend before matching skin colors",
    "Choose the face and skin regions",
    "Match skin colors",
    "Blend the corrected face",
    "Compare with seamless cloning",
    "Inspect the final result",
)

# ANSI terminal text colors
TEXT_STYLES = {
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
TEXT_RESET = "\033[0m"
NEXT_PROMPT = "Enter C to continue or Q to quit, then press Enter."
EXIT_PROMPT = "Enter Q to quit, then press Enter."


# __________________________________________
# IMAGE INPUT AND OUTPUT
# ==========================================


# --- load_bgr_image()
def load_bgr_image(image_path: Path) -> np.ndarray:
    """Read a photograph as a nonempty uint8 BGR array.

    Args:
        image_path: Original image filename.

    Returns:
        Color pixels with shape (height, width, 3) and values from 0 to 255.

    Raises:
        FileNotFoundError: The input path is not a file.
        ValueError: The image cannot be decoded.
        cv2.error: OpenCV reports a reading error.
    """
    # Error check: Stop before processing when the expected input is missing.
    if not image_path.is_file():
        raise FileNotFoundError(f"Input image does not exist: {image_path}")
    # imread() decodes a file into a NumPy pixel array; str(image_path) supplies its filename.
    # IMREAD_COLOR requests three BGR channels. The Rock'soriginal alpha is
    # entirely opaque, so dropping that fourth channel does not change its appearance.
    #
    # Each photograph becomes a grid of pixels with three values at each position:
    #
    #     bgr_image[row, column] = [B, G, R]
    #     bgr_image.shape        = (height, width, 3)
    #
    # B, G, and R hold blue, green, and red intensities from 0 to 255. The last
    # dimension stores colors; it does not represent depth in a 3D scene.
    # Reading the file creates this array in memory. The file itself stays unchanged.
    bgr_image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    # Error check: A failed decode returns None; an empty array contains no image pixels.
    if bgr_image is None or bgr_image.size == 0:
        raise ValueError(f"OpenCV could not read the image: {image_path}")
    return bgr_image


# ---


# --- save_bgr_image_as_png()
def save_bgr_image_as_png(bgr_image: np.ndarray, image_path: Path) -> None:
    """Write BGR pixels to a PNG, reporting directory or write failures.

    Args:
        bgr_image: Processed uint8 BGR image.
        image_path: Output filename, separate from the originals.

    Raises:
        OSError: The directory cannot be created or the image cannot be written.
        cv2.error: OpenCV reports an encoding error.
    """
    # parents=True creates missing folders; exist_ok=True permits repeat runs.
    # image_path.parent is the folder containing the new image, not the image filename.
    # Creating that folder first lets imwrite() focus on writing the pixel array.
    image_path.parent.mkdir(parents=True, exist_ok=True)
    # imwrite() encodes BGR pixels as PNG because the filename ends in .png.
    # PNG stores the resulting color values without JPEG-style compression loss.
    # The array keeps its height and width. Reusing the same output filename replaces
    # that derived result on the next run; the input paths are not written here.
    # Error check: False means the write failed, so do not report a saved result.
    if not cv2.imwrite(str(image_path), bgr_image):
        raise OSError(f"OpenCV could not write the image: {image_path}")


# ---


# __________________________________________
# FACE ALIGNMENT
# ==========================================


# --- validate_alex_and_the_rock_images()
def validate_alex_and_the_rock_images(
    alex_original_image: np.ndarray, the_rock_original_image: np.ndarray
) -> None:
    """Reject resized inputs because the manual coordinates belong to the original sizes.

    Args:
        alex_original_image: Alex's decoded BGR photograph.
        the_rock_original_image: The Rock'sdecoded BGR photograph.

    Raises:
        ValueError: An image has a different size, channel count, or pixel data type.
    """
    # The settings store (width, height), while original_image.shape reports (height, width, 3).
    # original_image_size[1] and original_image_size[0] put the expected dimensions in array order
    # for this comparison.
    # A resized photograph would move the marked eyes and mouth away from the stored
    # coordinates. Stopping here gives a useful explanation before an incorrect crop.
    for person_name, original_image, original_image_size in [
        ("Alex", alex_original_image, ALEX_IMAGE_SIZE),
        ("The RocK", the_rock_original_image, THE_ROCK_IMAGE_SIZE),
    ]:
        if original_image.dtype != np.uint8 or original_image.shape != (
            original_image_size[1],
            original_image_size[0],
            3,
        ):
            raise ValueError(
                f"{person_name} needs its original {original_image_size[0]} x "
                f"{original_image_size[1]} uint8 BGR image. "
                "Use the supplied photograph without resizing it."
            )


# ---


# ________________________________________________
# Step 2: Crop and align Alex's face.
# ------------------------------------------------


# --- get_alex_to_the_rock_transform()
def get_alex_to_the_rock_transform() -> np.ndarray:
    """Calculate the matrix that puts Alex's eyes and mouth at The Rock'smarked points.

    Returns:
        A 2x3 affine transformation matrix (np.ndarray) that maps coordinates from
        Alex's face (specifically, the cropped face region) to The Rock'sface coordinates.
        This matrix is used by `cv2.warpAffine` to align and overlay Alex's face onto
        The Rock'sface in the final composite image.

    """
    # Subtract the crop's (left, top) offset because the cropped image starts at (0, 0).
    # A point marked in the full photograph needs a new address inside the crop:
    #
    #     [x_in_crop]   [x_in_Alex]   [left]
    #     [y_in_crop] = [y_in_Alex] - [top ]
    #
    # ALEX_FACE_ALIGNMENT_POINTS has one [x, y] row for each eye and the mouth. NumPy subtracts
    # ALEX_FACE_CROP_BOUNDS[:2], which holds [left, top], from all three rows. The marked
    # features stay in place; only the starting point for their coordinates changes.
    alex_crop_alignment_points = ALEX_FACE_ALIGNMENT_POINTS - np.float32(ALEX_FACE_CROP_BOUNDS[:2])
    # cv2.getAffineTransform() uses three matching point pairs to calculate a 2-by-3
    # matrix. Here, the eyes and mouth guide the face's size, angle, and position.
    # The points must not lie on one straight line. The mapping can also include shear.
    #
    # The returned matrix describes where a point in Alex's crop belongs in The Rock'simage:
    #
    #     [x_on_rock]   [m00  m01  m02]   [x_in_crop]
    #     [y_on_rock] = [m10  m11  m12] @ [y_in_crop]
    #                                     [    1    ]
    #
    # @ denotes matrix multiplication.
    # m00 through m12 are the six values in the returned alex_to_the_rock_matrix. The first
    # two columns control size, angle, and shear; the last column moves the face.
    # The 1 makes that movement part of the multiplication. This matrix acts on
    # pixel positions. It does not mix the blue, green, and red channels.
    return cv2.getAffineTransform(alex_crop_alignment_points, THE_ROCK_FACE_ALIGNMENT_POINTS)


# ---


# --- align_alex_face_and_build_baseline_mask()
def align_alex_face_and_build_baseline_mask(
    alex_original_image: np.ndarray,
    the_rock_original_image: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Reproduce the original, uncorrected face preparation for the baseline.

    The baseline is the first blend before skin-color matching. Its mask tells
    the program where to use Alex and where to keep The Rock'sphotograph.

    Args:
        alex_original_image: Original Alex portrait in uint8 BGR format.
        the_rock_original_image: Original photograph of The Rock in uint8 BGR format.

    Returns:
        Alex's aligned BGR face and float32 alpha mask at The Rock'simage dimensions.
        The face canvas is black outside the warped crop; alex_baseline_alpha excludes those pixels.

    Raises:
        ValueError: Alex's crop or The Rock'smarked face region is unusable.
        cv2.error: OpenCV cannot transform the supplied arrays.

    Logic:
        1. Extract Alex's crop and translate the manual outline into crop coordinates.
        2. Warp the face and its mask with the same affine transform.
        3. Feather the mask inward, keeping its center opaque and its exterior zero.
    """
    alex_crop_left, alex_crop_top, alex_crop_right, alex_crop_bottom = ALEX_FACE_CROP_BOUNDS
    # Error check: These coordinates require the supplied photographs at their original sizes.
    if not (
        0 <= alex_crop_left < alex_crop_right <= alex_original_image.shape[1]
        and 0 <= alex_crop_top < alex_crop_bottom <= alex_original_image.shape[0]
    ):
        raise ValueError("Alex's image does not contain the configured face crop.")
    the_rock_height, the_rock_width = the_rock_original_image.shape[:2]
    if np.any(THE_ROCK_FACE_ALIGNMENT_POINTS < 0) or np.any(
        THE_ROCK_FACE_ALIGNMENT_POINTS >= [the_rock_width, the_rock_height]
    ):
        raise ValueError("The Rock'simage does not contain the marked eye and mouth points.")
    # Array slices use rows before columns. No operation below changes Alex's crop directly.
    #
    #     alex_original_image[alex_crop_top:alex_crop_bottom, alex_crop_left:alex_crop_right]
    #                rows        columns
    #
    # The slice includes top and left but stops before bottom and right. It keeps
    # all three BGR values, so alex_face_crop has shape:
    #
    #     (alex_crop_bottom - alex_crop_top, alex_crop_right - alex_crop_left, 3)
    #
    # Cropping selects existing pixels. The resize, turn, and movement happen later
    # in warpAffine(), after the program has calculated the matching-point matrix.
    alex_face_crop = alex_original_image[
        alex_crop_top:alex_crop_bottom, alex_crop_left:alex_crop_right
    ]
    alex_baseline_crop_outline = ALEX_BASELINE_FACE_OUTLINE - np.int32(
        [alex_crop_left, alex_crop_top]
    )
    alex_baseline_crop_mask = np.zeros(alex_face_crop.shape[:2], dtype=np.float32)
    # fillPoly() writes 1 inside the selected outline and leaves the exterior at 0.
    # alex_baseline_crop_mask is a separate 2D array with one selection value per pixel:
    #
    #     alex_baseline_crop_mask[y, x] = 1  -> inside Alex's face outline
    #     alex_baseline_crop_mask[y, x] = 0  -> outside that outline
    #
    # The program warps this mask with the same matrix as the face. This keeps
    # the selection lined up with the eyes, cheeks, and beard after alignment.
    cv2.fillPoly(alex_baseline_crop_mask, [alex_baseline_crop_outline], 1.0)
    alex_to_the_rock_matrix = get_alex_to_the_rock_transform()
    # warpAffine() expects output size as (width, height). INTER_LINEAR interpolates
    # between nearby pixels; BORDER_CONSTANT fills positions outside the crop with zero.
    aligned_alex_face = cv2.warpAffine(
        alex_face_crop,
        alex_to_the_rock_matrix,
        (the_rock_width, the_rock_height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    alex_aligned_baseline_mask = cv2.warpAffine(
        alex_baseline_crop_mask,
        alex_to_the_rock_matrix,
        (the_rock_width, the_rock_height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    # cv2.GaussianBlur() averages nearby mask values to make a gradual transition
    # around the face. It smooths the selection map, not the photograph. ALEX_BASELINE_MASK_KERNEL
    # sets the neighborhood size; ALEX_BASELINE_MASK_SIGMA controls the spread of the averaging.
    # A Gaussian filter gives nearby mask values more influence than distant ones.
    # Its result contains fractions near the boundary, making a gradual mix possible.
    #
    #     alex_aligned_baseline_mask -> alex_softened_baseline_mask -> alex_baseline_alpha ->
    # alex_baseline_alpha in create_alex_on_the_rock_results()
    #
    # alex_baseline_alpha is the share taken from Alex: 1 uses Alex, 0 uses The RocK, and a value
    # between them mixes both pictures. No Gaussian filter is applied to the face pixels.
    alex_softened_baseline_mask = cv2.GaussianBlur(
        alex_aligned_baseline_mask, ALEX_BASELINE_MASK_KERNEL, sigmaX=ALEX_BASELINE_MASK_SIGMA
    )
    # Keep that transition inside the selected face. This rescaling makes lower
    # weights zero, so the black area outside Alex's crop cannot enter the blend.
    alex_baseline_alpha = np.clip(2.0 * alex_softened_baseline_mask - 1.0, 0.0, 1.0)
    # Gaussian arithmetic can leave the interior just below 1; keep it exactly opaque.
    alex_baseline_alpha[alex_baseline_alpha > 1.0 - 1e-6] = 1.0
    alex_baseline_alpha[alex_aligned_baseline_mask < 1.0] = 0.0
    # Error check: A misplaced mask must not silently produce an unchanged portrait.
    if not np.any(alex_baseline_alpha == 1.0):
        raise ValueError("The aligned face mask has no opaque interior.")
    return aligned_alex_face, alex_baseline_alpha


# ---


# __________________________________________
# FACE MASKS AND SKIN SAMPLES
# ==========================================


# --- create_ellipse_mask()
def create_ellipse_mask(mask_shape: tuple[int, int], ellipse_patches: list[tuple]) -> np.ndarray:
    """Make a binary uint8 mask from the ellipses on a (height, width) grid.

    Args:
        mask_shape: Height and width of the grid shared by the aligned images.
        ellipse_patches: Ellipses given as (center x, center y, horizontal radius, vertical radius).

    Returns:
        One 2D array with 255 inside the ellipses and 0 elsewhere.
    """
    # Starting with zeros leaves every position unselected. Each ellipse adds a
    # selected patch to this same mask, so the result contains all the listed patches.
    # A radius measures center to edge; the horizontal and vertical radii can differ.
    # The continuous oval is described by:
    #
    #     ((column - ellipse_center_x) / radius_x)^2 + ((row - ellipse_center_y) / radius_y)^2 <= 1
    #
    # OpenCV draws that oval on the integer pixel grid. In this mask, 255 means
    # selected; it does not mean the corresponding skin pixel has a white color.
    ellipse_selection_mask = np.zeros(mask_shape, dtype=np.uint8)
    for ellipse_center_x, ellipse_center_y, radius_x, radius_y in ellipse_patches:
        if (
            radius_x <= 0
            or radius_y <= 0
            or ellipse_center_x - radius_x < 0
            or ellipse_center_y - radius_y < 0
            or ellipse_center_x + radius_x >= mask_shape[1]
            or ellipse_center_y + radius_y >= mask_shape[0]
        ):
            raise ValueError("A reviewed skin or feature ellipse falls outside the image.")
        # ellipse() receives a center, two radii, rotation, and start/end angles.
        # A full 360 degrees and thickness=-1 fill the ellipse with the value 255.
        cv2.ellipse(
            ellipse_selection_mask,
            (ellipse_center_x, ellipse_center_y),
            (radius_x, radius_y),
            0,
            0,
            360,
            255,
            -1,
        )
    return ellipse_selection_mask


# ---


# --- create_alex_face_blend_alpha()
def create_alex_face_blend_alpha(
    alex_face_selection_mask: np.ndarray, alex_crop_coverage: np.ndarray, alex_feather_width: float
) -> np.ndarray:
    """Soften a binary face selection inward, using only fully covered pixels from Alex's crop.

    Args:
        alex_face_selection_mask: Nonempty uint8 selection containing only 0 and 255.
        alex_crop_coverage: Float coverage from the same linear warp used for Alex's crop.
        alex_feather_width: Transition width in The Rock'simage pixels, measured inward from the
            boundary.

    Returns:
        A float32 alpha array with an opaque interior and an exactly zero exterior.

    Raises:
        ValueError: Selection, coverage, or transition width cannot produce a valid face.
    """
    # Mask preparation supplies a binary selection and coverage on the same image grid.
    # Check the adjustable fade width and keep selected pixels away from black warp padding.
    if not np.isfinite(alex_feather_width) or alex_feather_width <= 0:
        raise ValueError("Alex's face-mask feather width must be finite and greater than zero.")
    if np.any(alex_crop_coverage[alex_face_selection_mask > 0] < 1.0):
        raise ValueError("The face mask must stay inside fully covered source pixels.")
    if np.any(alex_face_selection_mask[[0, -1], :]) or np.any(alex_face_selection_mask[:, [0, -1]]):
        raise ValueError("The face selection needs an empty border around the image.")
    # distanceTransform() measures distance from each selected pixel to a zero pixel.
    # DIST_L2 uses Euclidean distance; DIST_MASK_PRECISE avoids a chamfer approximation.
    alex_face_edge_distance = cv2.distanceTransform(
        alex_face_selection_mask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE
    )
    # The outermost selected pixel has distance 1. Starting its weight at zero
    # keeps the blend inside the face outline, away from the black warp padding.
    # alex_edge_fraction*alex_edge_fraction*(3 - 2*alex_edge_fraction) gives a smooth transition
    # from the portrait to Alex's face.
    #
    #     alex_edge_fraction     = clip((alex_face_edge_distance - 1) / alex_feather_width, 0, 1)
    #     alex_blend_alpha = alex_edge_fraction * alex_edge_fraction * (3 - 2 * alex_edge_fraction)
    #
    # alex_face_edge_distance measures how far a selected pixel is from the outside of the mask.
    # Subtracting 1 starts the outermost selected pixels at zero. Dividing by alex_feather_width
    # spreads the transition across ALEX_FACE_MASK_FEATHER_PIXELS. clip() keeps alex_edge_fraction
    # between 0 and 1.
    # The curve starts and ends gently: alex_edge_fraction=0 keeps The Rock and alex_edge_fraction=1
    # uses Alex fully.
    # This creates blending weights. The aligned photograph keeps its existing detail.
    alex_edge_fraction = np.clip((alex_face_edge_distance - 1.0) / alex_feather_width, 0.0, 1.0)
    alex_blend_alpha = (
        alex_edge_fraction * alex_edge_fraction * (3.0 - 2.0 * alex_edge_fraction)
    ).astype(np.float32)
    alex_blend_alpha[alex_face_selection_mask == 0] = 0.0
    if not np.any(alex_blend_alpha == 1.0):
        raise ValueError("The face mask is too small for an opaque interior at this width.")
    return alex_blend_alpha


# ---


# --- prepare_alex_and_the_rock_masks()
def prepare_alex_and_the_rock_masks(
    alex_original_image: np.ndarray, the_rock_original_image: np.ndarray
) -> dict[str, np.ndarray]:
    """Keep warp coverage, face selection, blending weights, and skin samples separate.

    Args:
        alex_original_image: Original Alex photograph; its dimensions are checked before alignment.
        the_rock_original_image: Original photograph of The RocK, used here for its grid dimensions.

    Returns:
        Arrays named alex_crop_coverage, alex_face_selection_mask, alex_blend_alpha,
            alex_skin_sample_mask, the_rock_skin_sample_mask, and alex_color_strength.
        All use The Rock'simage grid. Skin masks select statistics; alex_color_strength controls
        how much color changes at each pixel. Neither changes the face selection.

    Raises:
        ValueError: A face selection, skin sample, or transition setting is unusable.
    """
    # create_alex_on_the_rock_results() validates the original photographs before preparation.
    alex_crop_left, alex_crop_top, alex_crop_right, alex_crop_bottom = ALEX_FACE_CROP_BOUNDS
    alex_crop_shape = (alex_crop_bottom - alex_crop_top, alex_crop_right - alex_crop_left)
    alex_to_the_rock_matrix = get_alex_to_the_rock_transform()
    the_rock_canvas_size = (the_rock_original_image.shape[1], the_rock_original_image.shape[0])
    # Warping an all-ones crop with the image's interpolation shows how much of
    # Alex's crop contributes. Coverage below 1 includes some black border padding.
    alex_crop_coverage = cv2.warpAffine(
        np.ones(alex_crop_shape, np.float32),
        alex_to_the_rock_matrix,
        the_rock_canvas_size,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    # __________________________________________
    # STEP 3: PREPARE THE MASK FOR ALEX'S FACE.
    # ==========================================

    alex_crop_face_mask = np.zeros(alex_crop_shape, np.uint8)
    cv2.fillPoly(
        alex_crop_face_mask,
        [ALEX_FINAL_FACE_OUTLINE - np.int32([alex_crop_left, alex_crop_top])],
        255,
    )
    # INTER_NEAREST picks an existing mask value, so the clone mask stays binary.
    # The coverage check below rejects any selected pixel with incomplete image support.
    alex_face_selection_mask = cv2.warpAffine(
        alex_crop_face_mask,
        alex_to_the_rock_matrix,
        the_rock_canvas_size,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    # __________________________________________
    # STEP 5: PREPARE THE MASK FOR THE TRANSITION AREA.
    # ==========================================

    alex_blend_alpha = create_alex_face_blend_alpha(
        alex_face_selection_mask, alex_crop_coverage, ALEX_FACE_MASK_FEATHER_PIXELS
    )
    
    # These arrays share The Rock'spixel grid, but each answers a different question:
    #
    #     alex_crop_coverage       Does this position contain pixels from Alex's crop?
    #     alex_face_selection_mask Is this position inside the selected face? (0 or 255)
    #     alex_blend_alpha         How much of Alex appears here? (0 to 1)
    #     alex_skin_sample_mask    Is this Alex skin pixel included in the color sample?
    #     the_rock_skin_sample_mask Is this The Rock skin pixel included in the reference?
    #     alex_color_strength      How much color adjustment is allowed here? (0 to 1)
    #
    # The skin masks select forehead and cheek measurements. They do not cut out
    # the glasses, lips, or beard from the finished picture. alex_color_strength reduces
    # the adjustment around the protected features while the face selection stays the same.
    
    # __________________________________________
    # STEP 3 (CONTINUED): SELECT ALEX'S SKIN SAMPLES.
    # ==========================================

    alex_skin_sample_mask = create_ellipse_mask(alex_blend_alpha.shape, ALEX_SKIN_SAMPLE_PATCHES)

    # __________________________________________
    # STEP 4: PREPARE THE MASK FOR THE Rock'sFACE.
    # ==========================================

    the_rock_skin_sample_mask = create_ellipse_mask(
        alex_blend_alpha.shape, THE_ROCK_SKIN_SAMPLE_PATCHES
    )
    # Check sample counts once here, before either color matching or plotting uses them.
    # create_ellipse_mask() already supplies binary uint8 masks on the requested grid.
    for person_name, skin_sample_mask in [
        ("Alex", alex_skin_sample_mask),
        ("The RocK", the_rock_skin_sample_mask),
    ]:
        if np.count_nonzero(skin_sample_mask) < MIN_ALEX_THE_ROCK_SKIN_SAMPLE_PIXELS:
            raise ValueError(
                f"{person_name}'s skin sample needs at least "
                f"{MIN_ALEX_THE_ROCK_SKIN_SAMPLE_PIXELS} pixels."
            )
    if np.any(alex_blend_alpha[alex_skin_sample_mask > 0] != 1.0):
        raise ValueError("Alex's skin samples must stay inside the opaque face interior.")
    alex_feature_protection_mask = (
        create_ellipse_mask(alex_blend_alpha.shape, ALEX_PROTECTED_FEATURE_PATCHES).astype(
            np.float32
        )
        / 255.0
    )
    
    # Only the strength mask is blurred. The photograph, frames, and beard texture
    # keep their detail. A (0, 0) kernel lets OpenCV choose its size from sigma.
    # alex_feature_protection_mask is near 1 around the glasses and beard and near 0 away from them.
    # After smoothing, the following expression makes the change gradual:
    #
    #     alex_color_strength = 1 - (1 - ALEX_PROTECTED_FEATURE_COLOR_STRENGTH) *
    #                           alex_feature_protection_mask
    #
    # At alex_feature_protection_mask=1, alex_color_strength equals
    # ALEX_PROTECTED_FEATURE_COLOR_STRENGTH. At alex_feature_protection_mask=0, it equals 1.
    # The Lab channel strengths still apply afterward, so 1 means the full planned
    # adjustment, not an unrestricted color change.
    
    alex_feature_protection_mask = cv2.GaussianBlur(
        alex_feature_protection_mask, (0, 0), sigmaX=ALEX_FEATURE_MASK_SIGMA
    )
    
    alex_color_strength = (
        1.0 - (1.0 - ALEX_PROTECTED_FEATURE_COLOR_STRENGTH) * alex_feature_protection_mask
    ).astype(np.float32)
    
    alex_color_strength[alex_face_selection_mask == 0] = 0.0
    # Check if Alex's skin samples include pixels outside the correction region.
    if np.any(alex_color_strength[alex_skin_sample_mask > 0] == 0):
        raise ValueError("Alex's skin samples include pixels outside the correction region.")
    return {
        "alex_crop_coverage": alex_crop_coverage,
        "alex_face_selection_mask": alex_face_selection_mask,
        "alex_blend_alpha": alex_blend_alpha,
        "alex_skin_sample_mask": alex_skin_sample_mask,
        "the_rock_skin_sample_mask": the_rock_skin_sample_mask,
        "alex_color_strength": alex_color_strength,
    }


# ---


# __________________________________________
# SKIN COLOR CORRECTION
# ==========================================

# ________________________________________________
# Step 6: Correct the skin color of Alex's face.
# ------------------------------------------------


# --- match_alex_skin_to_the_rock()
def match_alex_skin_to_the_rock(
    aligned_alex_face: np.ndarray,
    the_rock_original_image: np.ndarray,
    alex_skin_sample_mask: np.ndarray,
    the_rock_skin_sample_mask: np.ndarray,
    alex_color_strength: np.ndarray,
    alex_channel_strengths: tuple[float, float, float] = ALEX_LAB_CORRECTION_STRENGTH,
) -> np.ndarray:
    """Adjust Alex's skin colors toward The Rock'susing float Lab values.

    Args:
        aligned_alex_face: Alex's aligned uint8 BGR face, before blending.
            Black padding is not included in the skin samples.
        the_rock_original_image: The Rock'sunmodified uint8 BGR photograph with the same
            dimensions.
        alex_skin_sample_mask: Binary 0/255 mask of selected skin on Alex's aligned face.
        the_rock_skin_sample_mask: Separate binary mask of selected skin on The Rock'sface.
        alex_color_strength: Finite 0-1 strength map that reduces changes around protected features.
        alex_channel_strengths: L, a, and b correction fractions, limited by
            MAX_ALEX_LAB_CORRECTION_STRENGTH.

    Returns:
        A corrected uint8 BGR copy, ready for either blending method.

    Related Equation:
        alex_target_lab = (alex_lab - alex_skin_mean) * alex_to_the_rock_lab_gain +
            the_rock_skin_mean
        alex_corrected_lab = alex_lab + alex_color_strength * alex_channel_strength *
            bounded(alex_target_lab - alex_lab)

    Equation Relationship:
        The gain is The Rock'scolor spread divided by Alex's, limited by
            ALEX_TO_THE_ROCK_LAB_GAIN_BOUNDS.
        This changes color statistics without smoothing the detail in Alex's face.

    Raises:
        ValueError: Correction strengths have invalid values or channel count.
    """
    # Convert the three channel settings to a NumPy vector so multiplication can
    # apply the L, a, and b strengths across every pixel in the Lab image.
    # The workflow supplies images and sample masks on the same grid. Check the
    # adjustable correction strengths here before applying them to Alex's face.
    alex_channel_strength = np.asarray(alex_channel_strengths, np.float32)
    if (
        not np.all(np.isfinite(alex_color_strength))
        or np.any(alex_color_strength < 0)
        or np.any(alex_color_strength > 1)
        or alex_channel_strength.shape != (3,)
        or not np.all(np.isfinite(alex_channel_strength))
        or np.any(alex_channel_strength < 0)
        or np.any(alex_channel_strength > np.asarray(MAX_ALEX_LAB_CORRECTION_STRENGTH, np.float32))
    ):
        raise ValueError(
            "Color matching needs three finite, bounded channel strengths and a 0-1 strength map."
        )
    
    # Zero means no correction, including no rounding from a BGR/Lab conversion.
    if not np.any(alex_channel_strength):
        return aligned_alex_face.copy()
    
    # Float cvtColor() expects BGR values from 0 to 1. Its Lab result has L in 0-100
    # and signed a/b values, unlike the offset channels in an 8-bit Lab image.
    #
    #     BGR pixel / 255 -> cv2.cvtColor(..., COLOR_BGR2Lab) -> [L, a, b]
    #
    # L describes lightness. The a channel runs from green toward red, and b runs
    # from blue toward yellow. Lab conversion calculates a different description
    # of each color; it does more than rearrange BGR channels. The pixel positions
    # and the (height, width, 3) array shape stay the same.
    
    alex_lab = cv2.cvtColor(aligned_alex_face.astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab)
    the_rock_lab = cv2.cvtColor(
        the_rock_original_image.astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab
    )

    # The photographs have different skin colors and lighting. I measure small
    # skin patches rather than the whole picture, which would include the background,
    # glasses, and beard. Boolean indexing keeps only pixels selected by each mask.
    #
    #     alex_lab[alex_skin_sample_mask > 0] -> alex_skin_values
    #
    # Each selected skin pixel contributes one [L, a, b] row. mean(axis=0) averages
    # down those rows, giving three channel averages. std(axis=0) gives three values
    # describing how much the sampled colors vary around those averages.
    #
    alex_skin_values = alex_lab[alex_skin_sample_mask > 0] 
    the_rock_skin_values = the_rock_lab[the_rock_skin_sample_mask > 0] 
    alex_skin_mean, alex_skin_std = alex_skin_values.mean(axis=0), alex_skin_values.std(axis=0) 
    the_rock_skin_mean = the_rock_skin_values.mean(axis=0) 
    the_rock_skin_std = the_rock_skin_values.std(axis=0) 
    
    # A uniform patch has too little spread to divide safely. Keep gain 1
    # in that channel and allow only the bounded mean adjustment.
    
    # Check if Alex's skin std is stable.
    alex_skin_std_is_stable = alex_skin_std > ALEX_SKIN_STD_EPSILON
    
    # Set the initial gain to 1 for all channels.
    alex_to_the_rock_lab_gain = np.ones(3, np.float32)

    # Divide the Rock'sskin std by Alex's skin std to get the gain.
    # Only do this for channels where the std is stable.
    np.divide(
        the_rock_skin_std,
        alex_skin_std,
        out=alex_to_the_rock_lab_gain,
        where=alex_skin_std_is_stable,
    )

    # Clip the gain to the allowed range.
    alex_to_the_rock_lab_gain = np.clip(
        alex_to_the_rock_lab_gain, *ALEX_TO_THE_ROCK_LAB_GAIN_BOUNDS
    )

    # Subtracting Alex's mean centers his colors around zero. The gain adjusts
    # their spread, and The Rock'smean moves them toward his skin colors.
    # Limits on gain, shift, and strength keep this adjustment conservative.
    #
    # For each Lab channel, the calculation follows the same steps:
    #
    #     centered color = alex_lab - alex_skin_mean
    #     alex_target_lab         = centered color * alex_to_the_rock_lab_gain + the_rock_skin_mean
    #     alex_lab_shift          = alex_target_lab - alex_lab, limited by MAX_ALEX_LAB_SHIFT
    #     alex_corrected_lab    = alex_lab + alex_color_strength * alex_channel_strength *
    #                           alex_lab_shift
    #
    # alex_to_the_rock_lab_gain comes from the two samples' standard deviations. A gain below 1
    # brings colors closer together; a gain above 1 spreads them farther apart.
    # alex_channel_strength
    # sets a separate amount for L, a, and b. alex_color_strength varies by pixel, reducing
    # changes near the glasses and beard. Both multiply the proposed shift, so the
    # program can adjust skin color without replacing every pixel with one flat color.

    # Calculate the target Lab color for Alex.
    alex_target_lab = (alex_lab - alex_skin_mean) * alex_to_the_rock_lab_gain + the_rock_skin_mean
    # Calculate the shift needed to move Alex's colors to the target.
    alex_lab_shift = np.clip(
        alex_target_lab - alex_lab, -np.array(MAX_ALEX_LAB_SHIFT), MAX_ALEX_LAB_SHIFT
    )
    # Apply the shift to Alex's colors.
    alex_corrected_lab = (
        alex_lab + alex_color_strength[..., None] * alex_channel_strength * alex_lab_shift
    ).astype(np.float32)
    alex_correction_region = alex_color_strength > 0
    # Limit the adjusted Lab values before converting them back to BGR. alex_correction_region
    # remembers where correction was allowed, so other pixels can be copied from
    # the aligned face without any rounding introduced by the color conversions.
    alex_bounded_lab = np.clip(alex_corrected_lab, [0, -127, -127], [100, 127, 127]).astype(
        np.float32
    )
    # OpenCV's float Lab-to-BGR conversion already limits out-of-gamut values to
    # 0-1. Multiply by 255 below to return to the original color range.
    alex_corrected_bgr_float = cv2.cvtColor(alex_bounded_lab, cv2.COLOR_Lab2BGR)
    corrected_alex_face = np.clip(np.rint(alex_corrected_bgr_float * 255.0), 0, 255).astype(
        np.uint8
    )
    # ~alex_correction_region reverses the Boolean selection: it identifies the positions where
    # correction was zero. Assigning those pixels back keeps their values exact.
    corrected_alex_face[~alex_correction_region] = aligned_alex_face[~alex_correction_region]
    return corrected_alex_face


# ---


# __________________________________________
# TWO BLENDING METHODS
# ==========================================

# _______________________________________________________
# Step 7: Blend the corrected face with The Rock'sface.
# -------------------------------------------------------


# --- alpha_blend_foreground_with_background()
def alpha_blend_foreground_with_background(
    foreground_image: np.ndarray,
    background_image: np.ndarray,
    foreground_alpha: np.ndarray,
) -> np.ndarray:
    """Blend the face locally while keeping the background where foreground_alpha is zero.

    Args:
        foreground_image: Alex's aligned face, corrected face, or cloned result in uint8 BGR.
        background_image: The Rock'sphotograph, or gray for a preview, with the same shape.
        foreground_alpha: Finite float mask with shape (height, width), bounded to [0, 1].

    Returns:
        A new uint8 BGR image, with values rounded and clipped to [0, 255].

    Related Equation:
        blended_bgr_image = foreground_alpha * foreground_image + (1 - foreground_alpha) *
            background_image

    Equation Relationship:
        This function evaluates the weighted sum independently for each pixel and channel.
    """
    # The workflow supplies matching uint8 images and alpha weights already bounded to 0-1.
    # Add a singleton channel axis so each pixel's weight applies to B, G, and R.
    # float32 avoids uint8 overflow and retains fractional values during the calculation.
    #
    # At one position, let weight = foreground_alpha[y, x]. The same weight mixes all three colors:
    #
    #     [B_result]            [B_Alex]                [B_The_RocK]
    #     [G_result] = weight * [G_Alex] + (1-weight) * [G_The_RocK]
    #     [R_result]            [R_Alex]                [R_The_RocK]
    #
    # Here, Alex refers to foreground_image and The Rock to background_image in
    # the final alpha blend. The same function also places face previews on gray
    # and blends the cloned result back into The Rock'spicture.
    #
    # foreground_alpha starts with shape (height, width). Adding np.newaxis makes foreground_weights
    # (height, width, 1), allowing NumPy to use each weight across the three BGR
    # channels. This is broadcasting; it avoids writing a separate loop per channel.
    # At weight=1, the blended_bgr_image uses Alex. At weight=0, it keeps The RocK. At weight=0.5,
    # each picture contributes half of its color values before the result is rounded.
    
    foreground_weights = foreground_alpha.astype(np.float32)[..., np.newaxis]
    blended_bgr_float = foreground_weights * foreground_image.astype(np.float32) + (
        1.0 - foreground_weights
    ) * background_image.astype(np.float32)
    # rint() rounds to the nearest integer; clip() bounds values before conversion to uint8.
    blended_bgr_image = np.clip(np.rint(blended_bgr_float), 0, 255).astype(np.uint8)
    # Restore these values explicitly, so exterior preservation does not depend on
    # floating-point rounding. This same guard also applies to the cloned candidate.
    blended_bgr_image[foreground_alpha == 0] = background_image[foreground_alpha == 0]
    return blended_bgr_image


# ---


# ________________________________________________
# Step 8: Clone the face to match boundary colors.
# ------------------------------------------------


# --- clone_alex_face_into_the_rock()
def clone_alex_face_into_the_rock(
    corrected_alex_face: np.ndarray,
    the_rock_original_image: np.ndarray,
    alex_face_selection_mask: np.ndarray,
    alex_blend_alpha: np.ndarray,
) -> tuple[np.ndarray, tuple[int, int]]:
    """Clone the corrected face in place, then blend its edge against the original portrait.

    Args:
        corrected_alex_face: Alex's aligned BGR face after skin-color matching, before blending.
        the_rock_original_image: The Rock'soriginal BGR photograph. Both images must be same-size
            uint8.
        alex_face_selection_mask: Nonempty binary uint8 face selection, with an empty image border.
        alex_blend_alpha: Final inward feather; its support must stay inside the hard selection.

    Returns:
        Guarded normal-clone candidate and its center in The Rock'simage, in (x, y) order.

    Raises:
        ValueError: The selected face region is too small for normal cloning.
        cv2.error: OpenCV cannot solve the clone for the supplied region.
    """
    # Mask preparation checks the selection's border and creates its contained alpha weights.
    # Color matching supplies a corrected uint8 face on The Rock'simage grid.
    # boundingRect() returns the nonzero mask's x, y, width, and height. Ordinary
    # NORMAL_CLONE places that rectangle around the center, not the full canvas.
    #
    #     center_x = alex_clone_x + alex_clone_width // 2
    #     center_y = alex_clone_y + alex_clone_height // 2
    #
    # x and y locate the mask's upper-left corner. Adding half its width and height
    # places the center inside that same rectangle. // keeps the center in whole pixels.
    # The face is already aligned, so this center keeps it at that location.
    alex_clone_x, alex_clone_y, alex_clone_width, alex_clone_height = cv2.boundingRect(
        alex_face_selection_mask
    )
    if alex_clone_width < 5 or alex_clone_height < 5:
        raise ValueError("The clone region must be at least five pixels wide and high.")
    alex_clone_center = (
        alex_clone_x + alex_clone_width // 2,
        alex_clone_y + alex_clone_height // 2,
    )
    # cv2.seamlessClone() uses the selected face's gradients, the color changes
    # between nearby pixels, while matching The Rock'scolors at the selected boundary.
    # NORMAL_CLONE selects this method. The center places the mask's rectangle;
    # passing a mask copy keeps the recorded selection available for comparison.
    #
    #     corrected_alex_face -> color changes between neighboring face pixels
    #     the_rock_original_image      -> colors around the selected face boundary
    #                         -> alex_on_the_rock_clone
    #
    # OpenCV solves for face colors using both inputs. Unlike alpha blending, this
    # is not a fixed share of the two original colors at each pixel. It can change
    # the face's brightness, which is why the program displays both methods for comparison.
    alex_on_the_rock_clone = cv2.seamlessClone(
        corrected_alex_face,
        the_rock_original_image,
        alex_face_selection_mask.copy(),
        alex_clone_center,
        cv2.NORMAL_CLONE,
    )
    # Here the foreground is the cloned result. Using Alex again would bring the
    # warm colors back into the interior and undo this method's adjustment.
    return (
        alpha_blend_foreground_with_background(
            alex_on_the_rock_clone, the_rock_original_image, alex_blend_alpha
        ),
        alex_clone_center,
    )


# ---


# __________________________________________
# PROCESSING WORKFLOW
# ==========================================


# --- create_alex_on_the_rock_results()
def create_alex_on_the_rock_results(
    alex_original_image: np.ndarray, the_rock_original_image: np.ndarray
) -> dict:
    """Calculate the baseline and both corrected blends from the same two photographs.

    Args:
        alex_original_image, the_rock_original_image: Original uint8 BGR images at the configured
            dimensions.

    Returns:
        A dictionary containing the originals, aligned face, masks, corrected face,
        baseline, two candidates, and cloning center.

    Logic:
        Crop and align -> reproduce alex_on_the_rock_baseline -> prepare face_masks -> match skin
            colors
        -> compare alpha blending with normal cloning. Presentation reads these
        results later, so the saved images and explanations use the same calculation.
    """
    validate_alex_and_the_rock_images(alex_original_image, the_rock_original_image)
    # The original arrays feed separate comparison paths:
    #
    #     alex_original_image -> aligned_alex_face -> alex_on_the_rock_baseline
    #                          |
    #                          +-> corrected_alex_face -> alex_on_the_rock_alpha
    #                                                +-> alex_on_the_rock_clone
    #
    # Every blend also uses the_rock_original_image. The baseline keeps its original mask;
    # the corrected results use the masks from prepare_alex_and_the_rock_masks(). Color matching
    # starts with aligned_alex_face, so it never measures an already-blended picture.
    aligned_alex_face, alex_baseline_alpha = align_alex_face_and_build_baseline_mask(
        alex_original_image, the_rock_original_image
    )
    alex_on_the_rock_baseline = alpha_blend_foreground_with_background(
        aligned_alex_face, the_rock_original_image, alex_baseline_alpha
    )
    face_masks = prepare_alex_and_the_rock_masks(alex_original_image, the_rock_original_image)
    corrected_alex_face = match_alex_skin_to_the_rock(
        aligned_alex_face,
        the_rock_original_image,
        face_masks["alex_skin_sample_mask"],
        face_masks["the_rock_skin_sample_mask"],
        face_masks["alex_color_strength"],
    )
    # Both methods receive Alex's corrected face and The Rock'soriginal photograph.
    # Keeping their inputs the same makes it possible to compare how each method blends the edge.
    alex_on_the_rock_clone, alex_clone_center = clone_alex_face_into_the_rock(
        corrected_alex_face,
        the_rock_original_image,
        face_masks["alex_face_selection_mask"],
        face_masks["alex_blend_alpha"],
    )
    alex_on_the_rock_candidates = {
        "alex_on_the_rock_alpha": alpha_blend_foreground_with_background(
            corrected_alex_face, the_rock_original_image, face_masks["alex_blend_alpha"]
        ),
        "alex_on_the_rock_clone": alex_on_the_rock_clone,
    }
    return {
        "alex_original_image": alex_original_image,
        "the_rock_original_image": the_rock_original_image,
        "aligned_alex_face": aligned_alex_face,
        "alex_baseline_alpha": alex_baseline_alpha,
        "alex_on_the_rock_baseline": alex_on_the_rock_baseline,
        "face_masks": face_masks,
        "corrected_alex_face": corrected_alex_face,
        "alex_clone_center": alex_clone_center,
        "alex_on_the_rock_candidates": alex_on_the_rock_candidates,
    }


# ---


# __________________________________________
# IMAGE DISPLAY AND SAVED COMPARISON
# ==========================================


# --- show_bgr_image()
def show_bgr_image(axis, bgr_image: np.ndarray, title: str, coordinates: bool = False) -> None:
    """Show a photograph with the correct colors and optional pixel coordinates.

    OpenCV stores BGR values; Matplotlib expects RGB. The display conversion
    produces a separate array and leaves the processing image unchanged.

    Args:
        axis: The Matplotlib panel that receives this picture.
        bgr_image: A uint8 BGR photograph or prepared preview.
        title: The label and any subtitle, separated by newline characters.
        coordinates: Whether to show pixel positions along the panel's edges.
    """
    # At each position, cvtColor() presents [B, G, R] as [R, G, B] for imshow().
    # It keeps the pixel in the same location. Supplying BGR directly to Matplotlib
    # would make the displayed red and blue colors appear exchanged.
    axis.imshow(cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB))
    axis.set_title(title, fontsize=10)
    if coordinates:
        # Coordinate labels help relate the crop and marked points to the code.
        # The x direction follows columns; the y direction follows image rows.
        axis.set_xlabel("x / column (pixels)", fontsize=9)
        axis.set_ylabel("y / row (pixels)", fontsize=9)
        axis.tick_params(labelsize=8)
    else:
        # Blending comparisons emphasize appearance, so those panels hide the axes.
        # This removes plot markings, not pixels from the photograph.
        axis.axis("off")


# ---


# --- save_alex_the_rock_comparison()
def save_alex_the_rock_comparison(face_blending_results: dict) -> None:
    """Save the original photographs, corrected face preview, and selected result together.

    Args:
        face_blending_results: The image and mask arrays already calculated by
            create_alex_on_the_rock_results().

    The comparison is a separate presentation image. Its panel sizes do not set
    the resolution of the full-size face replacement saved by save_bgr_image_as_png().
    """
    # Gray makes the selected face easier to see. This preview is a separate array;
    # both blending methods use the corrected face's actual colors as their input.
    # np.full_like() creates an equally sized array filled with [224, 224, 224].
    # Equal B, G, and R values make a neutral gray background behind the face preview.
    corrected_alex_preview = alpha_blend_foreground_with_background(
        face_blending_results["corrected_alex_face"],
        np.full_like(face_blending_results["the_rock_original_image"], 224),
        face_blending_results["face_masks"]["alex_blend_alpha"],
    )
    # The list order becomes the reading order of the 2-by-2 figure:
    #
    #     Alex original          | The Rock original
    #     Corrected face on gray | Selected face replacement
    #
    # Each tuple keeps a title with its image array, so the two stay paired in the loop.
    panels = [
        (
            "Alex: original photograph\nThe face used for the replacement",
            face_blending_results["alex_original_image"],
        ),
        (
            "The RocK: original photograph\nThe picture receiving Alex's face",
            face_blending_results["the_rock_original_image"],
        ),
        (
            "Prepared face\nAlex aligned with colors adjusted\nGray is left out of the blend",
            corrected_alex_preview,
        ),
        (
            "Selected result\nAlex's face blended into The Rock'spicture",
            face_blending_results["alex_on_the_rock_candidates"][SELECTED_ALEX_ON_THE_ROCK_METHOD],
        ),
    ]
    # An Agg canvas renders directly to a file. It does not create a desktop window.
    # Constrained layout leaves room for the labels, keeping them clear of the pictures.
    figure = Figure(figsize=(9, 10), layout="constrained")
    FigureCanvasAgg(figure)
    axes = figure.subplots(2, 2)
    try:
        # axes.flat visits each panel from left to right, then moves to the next row.
        # zip() pairs those panels with the titles and images in the same order.
        for axis, (title, pixels) in zip(axes.flat, panels):
            show_bgr_image(axis, pixels, title)
        ALEX_THE_ROCK_COMPARISON_PATH.parent.mkdir(parents=True, exist_ok=True)
        # figsize is measured in inches; dpi is pixels per inch. This 9-by-10-inch
        # figure saved at 150 dpi creates a 1350-by-1500-pixel comparison image.
        figure.savefig(ALEX_THE_ROCK_COMPARISON_PATH, dpi=150)
    finally:
        # The file has its own figure, which is no longer needed after saving or a failure.
        plt.close(figure)


# ---


# __________________________________________
# GUIDED TRANSFORMATION WALKTHROUGH
# ==========================================


# --- sample_alex_and_the_rock_lab_colors()
def sample_alex_and_the_rock_lab_colors(face_blending_results: dict) -> dict:
    """Measure the plotted skin populations in float Lab with shared channel bins.

    Args:
        face_blending_results: The completed results, including both face versions and the skin
            masks.

    Returns:
        Three N-by-3 sample arrays and three common bin-edge arrays. Corrected
        samples use Alex's original skin mask; The Rock'ssamples use his own skin mask.
        L is in 0-100 lightness units; a/b are signed color coordinates.
    """
    # The three groups correspond to Alex before correction, Alex after correction,
    # and The RocK. Reusing Alex's mask selects the same locations before and after;
    # otherwise a different patch could make the graph suggest a misleading change.
    face_masks = face_blending_results["face_masks"]
    skin_color_samples = {}
    for label, image_key, mask_key in [
        ("Source", "aligned_alex_face", "alex_skin_sample_mask"),
        ("Corrected", "corrected_alex_face", "alex_skin_sample_mask"),
        ("Reference", "the_rock_original_image", "the_rock_skin_sample_mask"),
    ]:
        # Normalize BGR to 0-1 for OpenCV's floating-point Lab representation.
        # Boolean indexing excludes warp padding and all unselected background.
        sampled_person_lab = cv2.cvtColor(
            face_blending_results[image_key].astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab
        )
        skin_color_samples[label] = sampled_person_lab[face_masks[mask_key] > 0]
        # Each selected pixel contributes one [L, a, b] row. Mask preparation already
        # checks that both skin selections have enough pixels for matching and plotting.
    # A histogram groups nearby values into intervals called bins. Each Lab channel
    # gets one common set of intervals spanning all three groups. Sharing them makes
    # the positions of the plotted distributions directly comparable.
    lab_channel_bins = []
    for channel in range(3):
        low = min(float(values[:, channel].min()) for values in skin_color_samples.values())
        high = max(float(values[:, channel].max()) for values in skin_color_samples.values())
        # The same 24 bins cover all populations, including a constant-color sample.
        # linspace() returns 25 interval edges, leaving 24 spaces between them.
        # Extending low and high by 0.5 also gives nonzero width if every value is equal.
        lab_channel_bins.append(np.linspace(low - 0.5, high + 0.5, 25))
    return {"samples": skin_color_samples, "bins": lab_channel_bins}


# ---


# --- style_text()
def style_text(message: str, style: str = "", *, stream: TextIO | None = None) -> str:
    """Add a terminal color and reset it after the message.

    Args:
        message: Text that has already been wrapped or aligned.
        style: A name from TEXT_STYLES; an empty string keeps normal text.
        stream: Destination used to check color support; defaults to stdout.

    Returns:
        The same words with color codes, or plain text when color is disabled.
    """
    output = sys.stdout if stream is None else stream
    # stdout is the normal terminal output. An error may use stderr instead.
    # isatty() asks whether this particular output goes to a terminal, so redirecting
    # a transcript to a file does not fill that file with text-color escape codes.
    # A file or pipe receives plain text. NO_COLOR and a basic "dumb" terminal
    # also disable the accents. Check the actual stream, including stderr for errors.
    if (
        not message
        or not style
        or not output.isatty()
        or os.environ.get("NO_COLOR")
        or os.environ.get("TERM", "").lower() == "dumb"
    ):
        return message
    color = TEXT_STYLES.get(style, "")
    # The final string has three parts: a style code, the message, and a reset code.
    # Only the terminal interprets those codes; the message's words stay the same.
    return f"{color}{message}{TEXT_RESET}" if color else message


# ---


# --- print_wrapped()
def print_wrapped(
    message: str,
    style: str = "",
    *,
    stream: TextIO | None = None,
) -> None:
    """Fit prose to the terminal, then add its color; keep code and matrices separate.

    Args:
        message: One or more explanation lines, with intentional newlines kept.
        style: A TEXT_STYLES name, or an empty string for the terminal's normal text.
        stream: An output such as stderr; omitted for normal stdout text.
    """
    output = sys.stdout if stream is None else stream
    # Leave a small margin at the terminal's right edge, and cap paragraphs at 100
    # characters for readability. max(1, ...) keeps the width valid in a narrow terminal.
    width = max(1, min(100, shutil.get_terminal_size().columns - 2))
    # Wrap prose without clearing the terminal, so the reader can scroll back.
    # Keep filenames and paths intact rather than splitting them at a hyphen.
    # split("\n") keeps intentional paragraph breaks. fill() wraps each paragraph
    # at word boundaries, and join() puts those paragraphs back in their original order.
    wrapped = "\n".join(
        textwrap.fill(line, width, break_long_words=False, break_on_hyphens=False) if line else ""
        for line in message.split("\n")
    )
    # Apply color after wrapping so invisible escape codes do not affect line width.
    # flush=True sends the text immediately, so an explanation or prompt is visible
    # before the program waits for the next response.
    print(style_text(wrapped, style, stream=output), file=output, flush=True)


# ---


# --- print_banner()
def print_banner(title: str) -> None:
    """Separate the program or step heading from its explanation with a cyan banner."""
    # The heading and its two rules use the same available width as the body text.
    # Repeating '=' creates a visible break between steps without clearing earlier
    # explanations, so the reader can scroll back to compare them.
    width = max(1, min(100, shutil.get_terminal_size().columns - 2))
    print("\n" + style_text("=" * width, "rule"))
    print_wrapped(title, style="heading")
    print(style_text("=" * width, "rule"), flush=True)


# ---


# --- print_face_blending_guide_step()
def print_face_blending_guide_step(step: int) -> None:
    """Explain each view with its purpose, code, calculation, and picture-reading guide.

    The diagrams use the same variables as the processing functions. They explain
    the calculations already completed; printing them does not transform an image.

    Args:
        step: The teaching view to explain, numbered from 1 through 9.
    """
    # The validated image sizes supply the dimensions printed in each explanation.
    # These tuples describe arrays that already exist; calculating a shape here
    # does not allocate, resize, or crop an image.
    alex_shape = (ALEX_IMAGE_SIZE[1], ALEX_IMAGE_SIZE[0], 3)
    the_rock_shape = (THE_ROCK_IMAGE_SIZE[1], THE_ROCK_IMAGE_SIZE[0], 3)
    alex_crop_left, alex_crop_top, alex_crop_right, alex_crop_bottom = ALEX_FACE_CROP_BOUNDS
    alex_crop_shape = (alex_crop_bottom - alex_crop_top, alex_crop_right - alex_crop_left, 3)
    example = ""

    # Each case supplies the same reading sequence: purpose, code, a diagram,
    # an explanation of the symbols, and a guide to the pictures. Some steps add
    # a small example when it helps explain a coordinate or blending weight.
    if step == 1:
        # Establish the BGR storage order before introducing transformations.
        subtitle = "Load the two photographs and identify their pixel arrays"
        paragraphs = [
            "alex_original_image holds Alex's photograph, which supplies the replacement face. "
            "the_rock_original_image holds The Rock'sphotograph, which receives that face. "
            "Loading "
            "either file creates an array in memory and leaves the original file unchanged.",
            "An image array is a grid of pixels. Each pixel stores blue, green, and red "
            "values in BGR order. image[row, column] selects one pixel; its three entries "
            "describe color, not depth. OpenCV uses BGR, while Matplotlib expects RGB. "
            "The display conversion puts those same values in the order Matplotlib needs.",
            "Left: Alex's original photograph. Right: The Rock'soriginal photograph. "
            "Both pictures show the inputs before cropping, color matching, or blending.",
        ]
        code = [
            "Code in main():",
            "  alex_original_image = load_bgr_image(ALEX_IMAGE_PATH)",
            "  the_rock_original_image = load_bgr_image(THE_ROCK_IMAGE_PATH)",
            "Code in show_bgr_image():",
            "  cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)",
        ]
        diagram_title = "The color-order matrix for one pixel:"
        diagram = [
            "[R_display]   [0  0  1] [B_image]",
            "[G_display] = [0  1  0] [G_image]",
            "[B_display]   [1  0  0] [R_image]",
        ]
        diagram_note = (
            "Each 1 selects a value for the display. This matrix describes BGR-to-RGB "
            "reordering; the program uses cvtColor() to do it. The pixel stays at the "
            "same row and column. The processing arrays keep their BGR order."
        )
        array_note = (
            f"Array shapes: alex_original_image {alex_shape}; "
            f"the_rock_original_image {the_rock_shape}. "
            "Both use uint8 BGR values from 0 to 255."
        )
    elif step == 2:
        # Keep the crop operation separate from the change in point coordinates.
        subtitle = "Keep Alex's face and measure its marked points from the crop's corner"
        paragraphs = [
            "Cropping selects the rectangle around Alex's face. ALEX_FACE_CROP_BOUNDS stores "
            "left, top, right, and bottom. The slice below keeps those rows and columns, "
            "including all three color channels. It selects pixels without resizing them.",
            "Array indexing uses rows before columns, so top:bottom comes before "
            "left:right. The right and bottom limits are excluded. The marked eyes and "
            "mouth originally use coordinates from the full photograph. After cropping, "
            "the upper-left corner of the crop becomes the new coordinate starting point.",
            "Left: Alex's photograph with the crop rectangle. Right: the extracted face. "
            "Matching marker colors identify the same eyes and mouth in both pictures. "
            "The markers are display annotations; they are not painted into the face pixels.",
        ]
        code = [
            "Code in align_alex_face_and_build_baseline_mask():",
            "  alex_crop_left, alex_crop_top, alex_crop_right, alex_crop_bottom = "
            "ALEX_FACE_CROP_BOUNDS",
            "  alex_face_crop = alex_original_image[alex_crop_top:alex_crop_bottom, "
            "alex_crop_left:alex_crop_right]",
            "Code in get_alex_to_the_rock_transform():",
            "  alex_crop_alignment_points = ALEX_FACE_ALIGNMENT_POINTS - "
            "np.float32(ALEX_FACE_CROP_BOUNDS[:2])",
        ]
        diagram_title = "The coordinate change for each marked point:"
        diagram = [
            "[x_in_crop]   [x_in_Alex]   [alex_crop_left]",
            "[y_in_crop] = [y_in_Alex] - [alex_crop_top ]",
            "",
            "ALEX_FACE_ALIGNMENT_POINTS - crop corner -> alex_crop_alignment_points",
        ]
        diagram_note = (
            "ALEX_FACE_CROP_BOUNDS[:2] selects left and top. Subtracting them gives the same "
            "feature a new address inside the crop. NumPy applies that subtraction to "
            "each of the three [x, y] rows in ALEX_FACE_ALIGNMENT_POINTS."
        )
        example = (
            "ALEX_FACE_ALIGNMENT_POINTS[0] marks the viewer's left eye in Alex's full photo. "
            "alex_crop_alignment_points[0] marks that same eye inside the crop."
        )
        array_note = (
            f"Array shape: alex_original_image {alex_shape} -> alex_face_crop {alex_crop_shape}. "
            "The crop keeps uint8 BGR pixels."
        )
    elif step == 3:
        # Connect the marked features to the matrix that actually positions the face.
        subtitle = "Fit Alex's eyes and mouth to their positions in The Rock'spicture"
        paragraphs = [
            "The faces have different sizes and positions. The program uses the two eye "
            "centers and the mouth center as matching points. alex_crop_alignment_points holds "
            "Alex's positions inside the crop. THE_ROCK_FACE_ALIGNMENT_POINTS holds the positions "
            "where those features should land in The Rock'sphotograph.",
            "getAffineTransform() calculates a 2-by-3 matrix from the three point pairs. "
            "This affine transform can resize, turn, move, stretch, or slant the crop. "
            "warpAffine() applies that mapping to the face pixels. INTER_LINEAR estimates "
            "colors when a mapped position falls between existing pixels. The face mask "
            "receives the same transform so it stays lined up with the face.",
            "Left: Alex's crop with its marked points. Middle: the aligned face. "
            "Right: The Rock'starget points. Matching marker colors identify the same "
            "eye or mouth. Black around the aligned face is empty space outside Alex's "
            "crop; the blending mask later excludes it.",
        ]
        code = [
            "Code in get_alex_to_the_rock_transform():",
            "  cv2.getAffineTransform(alex_crop_alignment_points, "
            "THE_ROCK_FACE_ALIGNMENT_POINTS)",
            "Code in align_alex_face_and_build_baseline_mask():",
            "  alex_to_the_rock_matrix = get_alex_to_the_rock_transform()",
            "  aligned_alex_face = cv2.warpAffine(",
            "      alex_face_crop, alex_to_the_rock_matrix, (the_rock_width, the_rock_height),",
            "      flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,",
            "      borderValue=0)",
        ]
        diagram_title = "Calculate the pixel's position in The Rock's image:"
        diagram = [
            "Alex's cropped face: (x_in_crop, y_in_crop)",
            "The Rock's image: (x_on_rock, y_on_rock)",
            "",
            "x_on_rock = m00 * x_in_crop + m01 * y_in_crop + m02",
            "y_on_rock = m10 * x_in_crop + m11 * y_in_crop + m12",
        ]
        diagram_note = (
            "x is the horizontal position; y is the vertical position, in pixels. "
            "The first equation calculates the new x position, and the second calculates y. "
            "m00 through m12 label the six entries in alex_to_the_rock_matrix. "
            "The first digit identifies the row and the second identifies the column, "
            "starting at zero. The first two columns control size, angle, and shear. "
            "m02 shifts the horizontal position; m12 shifts the vertical position. "
            "These equations expand matrix multiplication by [x_in_crop, y_in_crop, 1]. "
            "The final 1 makes the shifts contribute as m02 * 1 and m12 * 1. "
            "This changes pixel positions; it does not rearrange BGR channels."
        )
        array_note = (
            f"Array shape: alex_face_crop {alex_crop_shape} -> aligned_alex_face "
            f"{the_rock_shape}. OpenCV receives the output size as (width, height)."
        )
    elif step == 4:
        # Introduce the baseline and alpha before discussing the improved masks.
        subtitle = "Make the first blend before adjusting Alex's skin colors"
        paragraphs = [
            "The baseline is the first blended picture, kept as a starting result for "
            "comparison. It combines the aligned face with The Rock'sphotograph before "
            "skin-color matching. Later results start from the same original photographs.",
            "A mask is a separate image that selects part of a photograph. Here it follows "
            "Alex's face and leaves out the room. A sharp selection could leave a pasted "
            "edge. GaussianBlur() averages nearby mask values to make a gradual transition. "
            "ALEX_BASELINE_MASK_KERNEL sets the neighborhood size; ALEX_BASELINE_MASK_SIGMA "
            "controls how widely nearby "
            "values contribute. The filter smooths the mask while the face keeps its detail.",
            "Left: the aligned face before color matching, shown on gray. Middle: the "
            "first blending mask. Yellow uses Alex, purple keeps The RocK, and the colors "
            "between them mix both photographs. Right: the first blend made with that mask. "
            "Gray is only the face preview's background.",
        ]
        code = [
            "Code in align_alex_face_and_build_baseline_mask():",
            "  alex_softened_baseline_mask = cv2.GaussianBlur(",
            "      alex_aligned_baseline_mask, ALEX_BASELINE_MASK_KERNEL, "
            "sigmaX=ALEX_BASELINE_MASK_SIGMA)",
            "  alex_baseline_alpha = np.clip(2.0 * alex_softened_baseline_mask - 1.0, 0.0, " "1.0)",
            "Code in create_alex_on_the_rock_results():",
            "  aligned_alex_face, alex_baseline_alpha = "
            "align_alex_face_and_build_baseline_mask(alex_original_image, "
            "the_rock_original_image)",
            "  alex_on_the_rock_baseline = "
            "alpha_blend_foreground_with_background(aligned_alex_face, "
            "the_rock_original_image, alex_baseline_alpha)",
        ]
        diagram_title = "How the mask becomes a blending weight:"
        diagram = [
            "alex_aligned_baseline_mask -> GaussianBlur -> alex_softened_baseline_mask -> "
            "alex_baseline_alpha",
            "                                                |",
            "                           returned as alex_baseline_alpha",
            "",
            "alex_baseline_alpha = 0          0 < alex_baseline_alpha < 1          "
            "alex_baseline_alpha = 1",
            "The Rock           mix both photos        Alex",
        ]
        diagram_note = (
            "Rescaling the softened mask fades the selection inward. The program also "
            "sets alex_baseline_alpha to zero where alex_aligned_baseline_mask is below 1, "
            "excluding partially covered "
            "edge pixels. This keeps the black space outside Alex's crop out of the blend. "
            "An opaque interior means alex_baseline_alpha is exactly 1 there."
        )
        array_note = (
            f"Array shapes: face and baseline {the_rock_shape}; alex_baseline_alpha "
            f"{the_rock_shape[:2]}. The mask holds one float32 weight per pixel."
        )
    elif step == 5:
        # Distinguish selection, opacity, and color correction; all are 2D maps.
        subtitle = "Separate the face selection, skin samples, and amount of color change"
        paragraphs = [
            "These maps have different jobs. alex_crop_coverage records how much of Alex's crop "
            "contributes at each aligned position. alex_face_selection_mask selects the face "
            "with 0 or 255. "
            "alex_blend_alpha controls how much of that face appears in the blend. Its center uses "
            "Alex fully, while its edge gradually mixes with The RocK.",
            "The skin masks select small forehead and cheek patches for color measurements. "
            "Glasses, lips, and beard are excluded from those samples because they do not "
            "represent skin color. They still appear in the replacement. alex_color_strength is "
            "another map: it reduces the color adjustment near the glasses and beard.",
            "Top row, left to right: real crop coverage, face selection, and blending "
            "weights. Bottom row: Alex's sampled skin, The Rock'ssampled skin, and color "
            "adjustment strength. Gray around the samples makes the small patches easier "
            "to see; it is not included in the measurements.",
        ]
        code = [
            "Code in prepare_alex_and_the_rock_masks():",
            "  alex_blend_alpha = create_alex_face_blend_alpha(alex_face_selection_mask, "
            "alex_crop_coverage, ALEX_FACE_MASK_FEATHER_PIXELS)",
            "  alex_skin_sample_mask = create_ellipse_mask(alex_blend_alpha.shape, "
            "ALEX_SKIN_SAMPLE_PATCHES)",
            "  the_rock_skin_sample_mask = create_ellipse_mask(alex_blend_alpha.shape, "
            "THE_ROCK_SKIN_SAMPLE_PATCHES)",
            "Code in create_alex_face_blend_alpha():",
            "  alex_edge_fraction = np.clip((alex_face_edge_distance - 1.0) / "
            "alex_feather_width, 0.0, 1.0)",
            "  alex_blend_alpha = (alex_edge_fraction * alex_edge_fraction * (3.0 - 2.0 * "
            "alex_edge_fraction)).astype(np.float32)",
        ]
        diagram_title = "One position, three different decisions:"
        diagram = [
            "alex_face_selection_mask[y, x]       -> select the replacement face: 0 or 255",
            "alex_blend_alpha[y, x]      -> decide Alex's share in the blend: 0 to 1",
            "alex_color_strength[y, x] -> control the planned color adjustment: 0 to 1",
            "",
            "alex_face_edge_distance from the mask's outside -> alex_edge_fraction -> "
            "alex_blend_alpha",
        ]
        diagram_note = (
            "distanceTransform() measures distance to the mask's outside. Subtracting 1 "
            "starts the outermost selected pixels at zero. Dividing by "
            "ALEX_FACE_MASK_FEATHER_PIXELS "
            "sets the transition width. The "
            "alex_edge_fraction*alex_edge_fraction*(3-2*alex_edge_fraction) curve starts and "
            "ends gently, "
            "avoiding a sudden change in the blending weight."
        )
        example = (
            "A position can have alex_blend_alpha=1 and alex_color_strength below 1. The blend "
            "uses "
            "Alex's face fully there, while the color adjustment remains reduced."
        )
        array_note = (
            f"Each map has shape {the_rock_shape[:2]}. Binary masks use uint8 "
            "values 0 and 255; alex_crop_coverage, alex_blend_alpha, and "
            "alex_color_strength use float32 fractions."
        )
    elif step == 6:
        # Explain the sampled statistics before interpreting the skin-color graphs.
        subtitle = "Bring Alex's sampled skin colors closer to The Rock'scolors"
        paragraphs = [
            "The photographs have different lighting and skin colors. The program measures "
            "the selected patches and adjusts Alex's colors toward The RocK's. CIE Lab "
            "separates lightness, L, from the green/red direction, a, and the blue/yellow "
            "direction, b. This allows a stronger color adjustment with less change to "
            "lightness. Dividing BGR values by 255 supplies the 0-to-1 input range needed "
            "for OpenCV's floating-point Lab conversion.",
            "alex_skin_mean and the_rock_skin_mean each contain three averages: one for "
            "L, a, and b. Their standard deviations describe how much the samples vary. "
            "alex_to_the_rock_lab_gain adjusts that spread. The program limits gain and the "
            "proposed shift, "
            "then applies the channel strengths and the correction map. The stronger "
            "adjustment for a reduces Alex's red tint. Allowing a narrower color spread "
            "also keeps less-red areas from being pushed too far toward green.",
            "Top row: Alex's sampled colors before adjustment, the same patches after "
            "adjustment, and The Rock'sreference samples. The graphs below compare L, a, "
            "and b. A higher line means more sampled colors are concentrated near that "
            "value. Each graph uses shared bins and density, so the area under each "
            "distribution is 1 even when the sample counts differ. The graphs show the "
            "adjustment; drawing them does not change the image.",
        ]
        code = [
            "Code in match_alex_skin_to_the_rock():",
            "  alex_lab = cv2.cvtColor(",
            "      aligned_alex_face.astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab)",
            "  the_rock_lab = cv2.cvtColor(",
            "      the_rock_original_image.astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab)",
            "  alex_skin_values = alex_lab[alex_skin_sample_mask > 0]",
            "  the_rock_skin_values = the_rock_lab[the_rock_skin_sample_mask > 0]",
        ]
        diagram_title = "The adjustment, applied separately to L, a, and b:"
        diagram = [
            "alex_to_the_rock_lab_gain = the_rock_skin_std / alex_skin_std, limited by "
            "ALEX_TO_THE_ROCK_LAB_GAIN_BOUNDS",
            "alex_target_lab = (alex_lab - alex_skin_mean) * alex_to_the_rock_lab_gain + "
            "the_rock_skin_mean",
            "alex_lab_shift = alex_target_lab - alex_lab, limited by MAX_ALEX_LAB_SHIFT",
            "alex_corrected_lab = alex_lab + alex_color_strength * alex_channel_strength "
            "* alex_lab_shift",
        ]
        diagram_note = (
            "Subtracting Alex's mean centers his sampled colors around zero. Multiplying "
            "by alex_to_the_rock_lab_gain changes their spread, and adding The Rock'smean "
            "moves the center "
            "toward his skin colors. A nearly uniform sample keeps alex_to_the_rock_lab_gain at "
            "1 to avoid "
            "dividing by a very small spread. alex_channel_strength holds the three channel "
            "amounts. alex_color_strength "
            "supplies a separate amount at each pixel. The displayed equation summarizes "
            "that operation; the code uses alex_color_strength[..., None] so its value applies "
            "to all three channels. The adjustment changes colors without blurring the face."
        )
        example = (
            "alex_lab[alex_skin_sample_mask > 0] keeps one [L, a, b] row per selected "
            "skin pixel. mean(axis=0) averages down those rows, keeping one mean "
            "for each of the three channels."
        )
        array_note = (
            f"Face shape stays {the_rock_shape}. uint8 BGR -> float32 Lab -> "
            "uint8 BGR. Skin samples have shape (selected pixel count, 3)."
        )
    elif step == 7:
        # Show the same weight applied to B, G, and R at one aligned pixel position.
        subtitle = "Mix the corrected face with The Rock using one weight per pixel"
        paragraphs = [
            "Alpha blending combines corrected_alex_face with the_rock_original_image. The center "
            "of the selected face uses Alex, the outside keeps The RocK, and the edge mixes "
            "both. Changing the share gradually makes the replacement meet the surrounding "
            "photograph without a sharp pasted edge.",
            "Inside alpha_blend_foreground_with_background(), foreground_image receives Alex's "
            "corrected face and "
            "background_image receives The Rock's photograph. foreground_alpha is the blending "
            "mask. "
            "Adding np.newaxis makes each weight apply to blue, green, and red together. "
            "float32 keeps fractions during the calculation. np.rint() rounds the result "
            "and np.clip() keeps values between 0 and 255 before conversion to uint8.",
            "Left: Alex's corrected face on gray. Middle: The Rock's original photograph. "
            "Right: the alpha-blended result. Gray is only a preview background. The "
            "calculation uses Alex's face colors and The Rock's original pixels.",
        ]
        code = [
            "Code in create_alex_on_the_rock_results():",
            "  alpha_blend_foreground_with_background(corrected_alex_face, "
            "the_rock_original_image, face_masks[\"alex_blend_alpha\"])",
            "Code in alpha_blend_foreground_with_background():",
            "  foreground_weights = foreground_alpha.astype(np.float32)[..., np.newaxis]",
            "  blended_bgr_float = (foreground_weights * foreground_image.astype(np.float32)",
            "             + (1.0 - foreground_weights) * background_image.astype(np.float32))",
            "  blended_bgr_image = np.clip(np.rint(blended_bgr_float), 0, " "255).astype(np.uint8)",
        ]
        diagram_title = "Mix the blue, green, and red values at one pixel:"
        diagram = [
            "weight = foreground_alpha[y, x]",
            "Alex's share = weight",
            "The Rock's share = 1 - weight",
            "",
            "blue_result  = weight * blue_alex  + (1 - weight) * blue_the_rock",
            "green_result = weight * green_alex + (1 - weight) * green_the_rock",
            "red_result   = weight * red_alex   + (1 - weight) * red_the_rock",
        ]
        diagram_note = (
            "Each equation mixes one color channel at the same pixel position in both images. "
            "The names ending in _alex represent values from Alex's corrected face; "
            "those ending in _the_rock represent values from The Rock's original photograph. "
            "In foreground_alpha[y, x], y selects the row and x selects the column. "
            "The weight is Alex's share, from 0 to 1. The remaining share comes from The Rock. "
            "The same weight applies to blue, green, and red. It does not move the pixel "
            "or exchange channels. The program then rounds and clips these results to 0-255. "
            "Where foreground_alpha is zero, it also copies The Rock's original pixels "
            "directly into the result to keep the background exact."
        )
        example = (
            "At foreground_alpha[y, x]=0.5, Alex contributes half and The Rock contributes half. "
            "At 1, the result uses Alex fully. At 0, it keeps The RocK."
        )
        array_note = (
            f"Images: {the_rock_shape}. foreground_alpha: {the_rock_shape[:2]}. "
            f"foreground_weights: {the_rock_shape[:2] + (1,)}. The result returns to uint8 BGR."
        )
    elif step == 8:
        # Use a flow diagram because seamless cloning is not a single blending matrix.
        subtitle = "Compare a blend based on neighboring color changes and boundary colors"
        paragraphs = [
            "Seamless cloning combines the same corrected face with The Rock in a different "
            "way. It uses gradients, meaning color changes between neighboring face pixels, "
            "and fits them to The Rock'scolors at the selected boundary. This can reduce "
            "a seam, but it can also change the brightness of the replacement face.",
            "boundingRect(alex_face_selection_mask) finds the smallest rectangle around the "
            "selected face. "
            "It returns alex_clone_x, alex_clone_y, alex_clone_width, and alex_clone_height. "
            "The center of that rectangle tells "
            "seamlessClone() where to place it. NORMAL_CLONE selects the cloning method. "
            "The face was already aligned, so the center keeps it at its existing position.",
            "Left: Alex's corrected face. Middle: The Rock with the placement rectangle "
            "and center marked. Right: the cloned result. Compare the forehead, lenses, "
            "and beard with the alpha blend from Step 7. Both methods receive the same "
            "corrected face and original photograph.",
        ]
        code = [
            "Code in clone_alex_face_into_the_rock():",
            "  alex_clone_x, alex_clone_y, alex_clone_width, alex_clone_height = "
            "cv2.boundingRect(alex_face_selection_mask)",
            "  alex_clone_center = (alex_clone_x + alex_clone_width // 2, alex_clone_y + "
            "alex_clone_height // 2)",
            "  alex_on_the_rock_clone = cv2.seamlessClone(",
            "      corrected_alex_face, the_rock_original_image, "
            "alex_face_selection_mask.copy(), alex_clone_center,",
            "      cv2.NORMAL_CLONE)",
            "  return alpha_blend_foreground_with_background(alex_on_the_rock_clone, "
            "the_rock_original_image, alex_blend_alpha), alex_clone_center",
        ]
        diagram_title = "How the cloning inputs contribute:"
        diagram = [
            "corrected_alex_face -> neighboring color changes -+",
            "the_rock_original_image -----> colors at the face boundary +-> "
            "alex_on_the_rock_clone",
            "",
            "alex_on_the_rock_clone + the_rock_original_image + alex_blend_alpha -> "
            "alpha_blend_foreground_with_background() -> final clone result",
        ]
        diagram_note = (
            "The arrows show the inputs OpenCV uses to solve for the cloned face colors. "
            "It is not a fixed weighted sum of the two original images. After cloning, "
            "alpha_blend_foreground_with_background() applies the gradual edge and restores the "
            "original pixels outside "
            "the mask. Its foreground is alex_on_the_rock_clone here, so this last step keeps "
            "the cloning "
            "result instead of replacing it with Alex's pre-cloning colors."
        )
        array_note = (
            f"Both corrected methods produce {the_rock_shape} uint8 BGR images. "
            "alex_face_selection_mask is a 2D uint8 selection; alex_clone_center "
            "stores an (x, y) position."
        )
    elif step == 9:
        # End with the method choice, visible limitations, and the saved output files.
        subtitle = "Inspect the comparison and the saved face replacement"
        paragraphs = [
            "The selected result uses skin-color matching followed by alpha blending. "
            "Normal cloning made the forehead and lenses too bright in this comparison. "
            "The alpha result keeps more of that detail while reducing the red tint. "
            "The earlier baseline remains visible so the effect of the changes is easier "
            "to judge.",
            "The band of light on Alex's forehead and the different head and chin shapes "
            "remain visible. Matching skin colors does not recreate the lighting or the "
            "three-dimensional shape of a face. This milestone uses manually chosen points. "
            "Automatic face detection and eye blurring belong to the later portfolio project.",
            "Top row: Alex, The RocK, and the corrected face on gray. Bottom row: the first "
            "blend before color matching, the selected alpha blend, and the seamless-cloning "
            "comparison. Check the skin color, the face boundary, and the detail around the "
            "glasses and beard. The surrounding photograph should stay the same.",
        ]
        code = [
            "Code in main():",
            "  save_bgr_image_as_png(",
            "      face_blending_results[\"alex_on_the_rock_candidates\"][",
            "          SELECTED_ALEX_ON_THE_ROCK_METHOD],",
            "      ALEX_ON_THE_ROCK_RESULT_PATH)",
            "  save_alex_the_rock_comparison(face_blending_results)",
        ]
        diagram_title = "The comparison paths from the same two photographs:"
        diagram = [
            "aligned_alex_face   + alex_baseline_alpha -> alex_on_the_rock_baseline",
            "corrected_alex_face + face_masks[\"alex_blend_alpha\"] -> "
            "alex_on_the_rock_alpha (selected)",
            "corrected_alex_face + face_masks[\"alex_face_selection_mask\"]  -> "
            "alex_on_the_rock_clone",
            "",
            "Each path also uses the_rock_original_image.",
        ]
        diagram_note = (
            "The baseline uses its original Gaussian mask. Both corrected methods use "
            "the same color-adjusted face; the clone also receives the final alpha edge. "
            "SELECTED_ALEX_ON_THE_ROCK_METHOD chooses the saved replacement. "
            "ALEX_ON_THE_ROCK_RESULT_PATH holds that image, "
            "and ALEX_THE_ROCK_COMPARISON_PATH holds the four-panel comparison. Saving these "
            "derived "
            "files leaves both photographs in org_images unchanged."
        )
        array_note = (
            f"Saved replacement: {the_rock_shape}, uint8 BGR. Display panels convert "
            "a copy to RGB; they do not change the saved face-replacement pixels."
        )
    else:
        raise ValueError(f"Unknown walkthrough stage: {step}")

    print_banner(f"STEP {step}/{len(STAGE_TITLES)}: {STAGE_TITLES[step - 1]}")
    # Introduce the purpose in cyan, then explain the code and picture in normal text.
    print_wrapped(subtitle, style="info")
    print_wrapped("\n" + paragraphs[0])
    print()
    for line in code:
        # Keep variable names and code aligned. Color accents separate code references
        # from explanations of what those variables hold.
        print(style_text("  " + line, "code"))
    for paragraph in paragraphs[1:-1]:
        # The middle paragraphs explain the code; the last paragraph is reserved
        # for the picture-reading guide printed below the calculation.
        print_wrapped("\n" + paragraph)
    print_wrapped("\n" + diagram_title, style="heading")
    # Print diagrams without wrapping so matrix rows and columns stay lined up.
    print(style_text("\n".join("  " + line for line in diagram), "matrix"))
    print_wrapped("\n" + diagram_note)
    if example:
        # An empty example means this step's diagram already explains the operation.
        print_wrapped("\nExample: " + example, style="example")
    print_wrapped("\nReading the pictures:", style="heading")
    print_wrapped(paragraphs[-1])
    print_wrapped("\n" + array_note, style="info")
    print_wrapped(
        f"Saved teaching view: {WALKTHROUGH_DIRECTORY / f'stage_{step:02d}.png'}", style="success"
    )
    # run_face_blending_guide() saves the figure before calling this function, so the
    # path refers to the view for the step that was just presented.
    print(flush=True)


# ---


# --- build_face_blending_guide_figure()
def build_face_blending_guide_figure(step: int, face_blending_results: dict) -> Figure:
    """Create a stage view from already-calculated arrays, before its explanation.

    Image arrays remain BGR uint8. Scalar panels carry explicit scales; neutral
    sample/face previews are separate arrays. Coordinate annotations are artists,
    so no marker or rectangle changes a processing pixel.

    Args:
        step: The numbered teaching view, matching the terminal explanation.
        face_blending_results: Original and processed arrays returned by
            create_alex_on_the_rock_results().

    Returns:
        A Matplotlib figure that run_face_blending_guide() saves and then displays.
    """
    face_masks = face_blending_results["face_masks"]
    # The layout follows how much each step needs to compare. Steps 1 and 2 have
    # two panels; steps 5, 6, and 9 need two rows of three. The other steps have one
    # row of three. squeeze=False keeps axes as a 2D array even with only one row.
    count = 2 if step <= 2 else (6 if step in (5, 6, 9) else 3)
    rows, columns = (2, 3) if count == 6 else (1, count)
    figure, axes = plt.subplots(
        rows, columns, figsize=(12, 7.4), squeeze=False, layout="constrained"
    )
    axes = axes.ravel()
    # ravel() gives the panels a simple reading-order index:
    #
    #     [0] [1] [2]
    #     [3] [4] [5]  <- present only in the six-panel views
    #
    # This changes the container of plot panels, not the image arrays shown in them.
    try:
        # The window title identifies the open view; the suptitle is printed inside
        # the figure and also appears in its saved PNG. Navigation stays in the terminal.
        figure.canvas.manager.set_window_title(f"CSC515 walkthrough - Step {step}/9")
        figure.suptitle(f"STEP {step}/9: {STAGE_TITLES[step-1]}", fontsize=14)
        figure.supxlabel("")

        # --- show_mask_values()
        def show_mask_values(
            index: int, values: np.ndarray, title: str, maximum: float, unit: str
        ) -> None:
            """Keep scalar mask values separate from photographs and label their scale."""
            # A scalar panel has one number per pixel. viridis turns low values purple
            # and high values yellow for display. vmin and vmax fix the scale at 0..1
            # for weights or 0..255 for a binary selection. These colors belong to the
            # visualization; they are not colors that the mask adds to the face.
            view = axes[index].imshow(values, vmin=0, vmax=maximum, cmap="viridis")
            axes[index].set_title(title, fontsize=10)
            axes[index].axis("off")
            figure.colorbar(view, ax=axes[index], shrink=0.7, label=unit)

        # ---

        # --- preview_alex_face_on_gray()
        def preview_alex_face_on_gray(
            alex_face_key: str, alex_preview_alpha: np.ndarray
        ) -> np.ndarray:
            """Make a preview-only copy; neutral gray never enters either compositor."""
            # alex_face_key selects an already aligned face from face_blending_results. A same-sized
            # gray
            # array supplies the preview background, and alex_preview_alpha reveals the selected
            # face. The stored face and the original photograph remain unchanged.
            return alpha_blend_foreground_with_background(
                face_blending_results[alex_face_key],
                np.full_like(face_blending_results["the_rock_original_image"], 224),
                alex_preview_alpha,
            )

        # ---

        # --- show_alex_or_the_rock_skin_samples()
        def show_alex_or_the_rock_skin_samples(
            index: int, person_image_key: str, person_skin_mask_key: str, title: str
        ) -> None:
            """Show actual sampled colors on gray, cropped to their common face region."""
            # Begin with a separate gray image, then copy only the selected BGR pixels.
            # The 2D Boolean mask chooses complete three-channel pixels from
            # face_blending_results[person_image_key].
            # This makes the measured patches visible without showing the rest of the face.
            skin_sample_preview = np.full_like(face_blending_results[person_image_key], 224)
            selected_skin_pixels = face_masks[person_skin_mask_key] > 0
            skin_sample_preview[selected_skin_pixels] = face_blending_results[person_image_key][
                selected_skin_pixels
            ]
            # A common crop preserves sample positions and makes small patches readable.
            alex_face_x, alex_face_y, alex_face_width, alex_face_height = cv2.boundingRect(
                face_masks["alex_face_selection_mask"]
            )
            show_bgr_image(
                axes[index],
                skin_sample_preview[
                    alex_face_y : alex_face_y + alex_face_height,
                    alex_face_x : alex_face_x + alex_face_width,
                ],
                title + "\nGray is outside the skin samples",
            )

        # ---

        # --- show_face_alignment_points()
        def show_face_alignment_points(index: int, points: np.ndarray) -> None:
            """Overlay matching point markers in the current panel's coordinate system."""
            # The same point order and colors are used in every panel: left eye, right
            # eye, then mouth. *point unpacks [x, y] into the two plot coordinates.
            # plot() draws a marker over the image without changing the NumPy array.
            for point, color, name in zip(
                points, ("cyan", "yellow", "magenta"), ("Left eye", "Right eye", "Mouth")
            ):
                axes[index].plot(
                    *point, marker="+", color=color, markersize=12, markeredgewidth=2, label=name
                )
            axes[index].legend(fontsize=8, loc="upper right")

        # ---

        alex_crop_left, alex_crop_top, alex_crop_right, alex_crop_bottom = ALEX_FACE_CROP_BOUNDS
        # Only the crop and alignment views need this slice. It is a display of
        # the same crop used by align_alex_face_and_build_baseline_mask(), taken from the unchanged
        # original.
        if step in (2, 3):
            alex_face_crop = face_blending_results["alex_original_image"][
                alex_crop_top:alex_crop_bottom, alex_crop_left:alex_crop_right
            ]
        if step == 1:
            # Start with the original arrays, before any processing, as a visual reference.
            show_bgr_image(
                axes[0],
                face_blending_results["alex_original_image"],
                "Original source: Alex\nThe face used for the replacement",
            )
            show_bgr_image(
                axes[1],
                face_blending_results["the_rock_original_image"],
                "Original destination: The RocK\nThe picture receiving Alex's face",
            )
        elif step == 2:
            # The rectangle's corner is (left, top); its size comes from subtracting
            # opposite bounds. Its unfilled center leaves the original photograph visible.
            show_bgr_image(
                axes[0],
                face_blending_results["alex_original_image"],
                "Alex's original photograph\n"
                "Rectangle selects the face; markers guide alignment",
                True,
            )
            axes[0].add_patch(
                matplotlib.patches.Rectangle(
                    (alex_crop_left, alex_crop_top),
                    alex_crop_right - alex_crop_left,
                    alex_crop_bottom - alex_crop_top,
                    fill=False,
                    edgecolor="lime",
                    linewidth=2,
                )
            )
            show_face_alignment_points(0, ALEX_FACE_ALIGNMENT_POINTS)
            show_bgr_image(
                axes[1],
                alex_face_crop,
                "Alex's face crop\nSame face pixels measured from the crop's corner",
                True,
            )
            show_face_alignment_points(
                1, ALEX_FACE_ALIGNMENT_POINTS - np.float32([alex_crop_left, alex_crop_top])
            )
        elif step == 3:
            # Show the crop, aligned face, and target photograph together so the
            # marker positions can be compared before and after the affine mapping.
            show_bgr_image(
                axes[0],
                alex_face_crop,
                "Face crop before alignment\nMarkers identify Alex's eyes and mouth",
                True,
            )
            show_face_alignment_points(
                0, ALEX_FACE_ALIGNMENT_POINTS - np.float32([alex_crop_left, alex_crop_top])
            )
            show_bgr_image(
                axes[1],
                face_blending_results["aligned_alex_face"],
                "Face after alignment\nSized and positioned for The Rock'spicture\n"
                "Black is outside the original crop",
                True,
            )
            alex_crop_alignment_points = ALEX_FACE_ALIGNMENT_POINTS - np.float32(
                [alex_crop_left, alex_crop_top]
            )
            # Each point is stored as a row here. Adding a column of ones gives:
            #
            #     P = [x_left_eye   y_left_eye   1]
            #         [x_right_eye  y_right_eye  1]
            #         [x_mouth      y_mouth      1]
            #
            # P has shape (3, 3). The affine matrix M has shape (2, 3), so P @ M.T
            # gives three transformed [x, y] rows. .T transposes M for row-based
            # multiplication; this is the same mapping used to align the face pixels.
            show_face_alignment_points(
                1,
                np.column_stack((alex_crop_alignment_points, np.ones(3)))
                @ get_alex_to_the_rock_transform().T,
            )
            show_bgr_image(
                axes[2],
                face_blending_results["the_rock_original_image"],
                "The RocK: alignment targets\n" "Where Alex's eye and mouth points should land",
                True,
            )
            show_face_alignment_points(2, THE_ROCK_FACE_ALIGNMENT_POINTS)
        elif step == 4:
            # All three panels come from the baseline path. Keeping its mask and
            # result together makes the starting blend clear before the corrected versions.
            show_bgr_image(
                axes[0],
                preview_alex_face_on_gray(
                    "aligned_alex_face", face_blending_results["alex_baseline_alpha"]
                ),
                "Uncorrected face\nAlex aligned before matching skin colors\n"
                "Gray is left out of the blend",
            )
            show_mask_values(
                1,
                face_blending_results["alex_baseline_alpha"],
                "Original baseline alpha\nYellow uses Alex; purple uses The RocK\n"
                "Colors between them mix both photos",
                1,
                "Share taken from Alex",
            )
            show_bgr_image(
                axes[2],
                face_blending_results["alex_on_the_rock_baseline"],
                "Uncorrected baseline\nFirst blend before matching skin colors",
            )
        elif step == 5:
            # The top row explains where the face can appear. The bottom row shows
            # which skin is measured and where the color correction is reduced.
            show_mask_values(
                0,
                face_masks["alex_crop_coverage"],
                "Source coverage\nYellow contains pixels from Alex's crop",
                1,
                "Amount of real source data",
            )
            show_mask_values(
                1,
                face_masks["alex_face_selection_mask"],
                "Face selection\nYellow selects pixels for replacement",
                255,
                "0 keeps The Rock / 255 selects Alex",
            )
            show_mask_values(
                2,
                face_masks["alex_blend_alpha"],
                "Final blending mask (alpha)\n" "Full Alex face in center; gradual mix at edge",
                1,
                "Share taken from Alex",
            )
            show_alex_or_the_rock_skin_samples(
                3,
                "aligned_alex_face",
                "alex_skin_sample_mask",
                "Alex's sampled skin\nSmall patches used to compare colors",
            )
            show_alex_or_the_rock_skin_samples(
                4,
                "the_rock_original_image",
                "the_rock_skin_sample_mask",
                "The Rock'ssampled skin\nReference patches for color matching",
            )
            show_mask_values(
                5,
                face_masks["alex_color_strength"],
                "Color adjustment strength\n" "Less change near glasses and beard",
                1,
                "Fraction of planned color change",
            )
        elif step == 6:
            # The sample previews show the measured colors, and the graphs summarize
            # their distributions. Rendering either representation leaves the samples intact.
            show_alex_or_the_rock_skin_samples(
                0,
                "aligned_alex_face",
                "alex_skin_sample_mask",
                "Alex's skin before adjustment\nOriginal colors from selected patches",
            )
            show_alex_or_the_rock_skin_samples(
                1,
                "corrected_alex_face",
                "alex_skin_sample_mask",
                "Alex's skin after adjustment\nSame patches after matching colors",
            )
            show_alex_or_the_rock_skin_samples(
                2,
                "the_rock_original_image",
                "the_rock_skin_sample_mask",
                "The Rock'ssampled skin\nColors used as the reference",
            )
            graph = sample_alex_and_the_rock_lab_colors(face_blending_results)
            graph_titles = (
                "L: lightness\nHow light or dark the samples are",
                "a: green / red\nWhere samples fall between green and red",
                "b: blue / yellow\nWhere samples fall between blue and yellow",
            )
            graph_labels = {
                "Source": "Alex before",
                "Corrected": "Alex after",
                "Reference": "The RocK",
            }
            for channel, label in enumerate(graph_titles):
                axis = axes[channel + 3]
                for (name, values), color in zip(
                    graph["samples"].items(), ("#0072B2", "#D55E00", "#009E73")
                ):
                    # Density = count / (population size * bin width). Its area is 1,
                    # allowing comparison of the differently sized skin populations.
                    # counts[k] is the number of sampled pixels in interval k.
                    # np.diff(edges) gives each interval's width. Dividing by both
                    # sample count and width makes height represent concentration:
                    #
                    #     density[k] = counts[k] / (sample_count * bin_width[k])
                    #
                    # A taller section means values are packed more closely together.
                    # stairs() draws that constant height across each interval.
                    counts, edges = np.histogram(values[:, channel], bins=graph["bins"][channel])
                    density = counts / (len(values) * np.diff(edges))
                    axis.stairs(density, edges, label=graph_labels[name], color=color)
                axis.set_title(label, fontsize=11)
                axis.set_xlabel(
                    "Lightness (Lab units)" if channel == 0 else "Color (Lab units)", fontsize=9
                )
                axis.set_ylabel("Sample concentration (density)", fontsize=9)
                axis.legend(fontsize=8)
                axis.tick_params(labelsize=8)
        elif step in (7, 8):
            # These steps share the same corrected face and original photograph.
            # Only the result panel changes method. Step 8 also marks clone placement.
            show_bgr_image(
                axes[0],
                preview_alex_face_on_gray("corrected_alex_face", face_masks["alex_blend_alpha"]),
                "Corrected face\nAlex after matching skin colors\n" "Gray is left out of the blend",
            )
            show_bgr_image(
                axes[1],
                face_blending_results["the_rock_original_image"],
                (
                    "The RocK: original photograph\nThe unchanged picture receiving the face"
                    if step == 7
                    else "The RocK: clone placement\n"
                    "Rectangle and center show where the face goes"
                ),
                step == 8,
            )
            if step == 8:
                alex_face_x, alex_face_y, alex_face_width, alex_face_height = cv2.boundingRect(
                    face_masks["alex_face_selection_mask"]
                )
                axes[1].add_patch(
                    matplotlib.patches.Rectangle(
                        (alex_face_x, alex_face_y),
                        alex_face_width,
                        alex_face_height,
                        fill=False,
                        edgecolor="cyan",
                        linewidth=2,
                    )
                )
                axes[1].plot(
                    *face_blending_results["alex_clone_center"], "+", color="magenta", markersize=14
                )
            key = "alex_on_the_rock_alpha" if step == 7 else "alex_on_the_rock_clone"
            show_bgr_image(
                axes[2],
                face_blending_results["alex_on_the_rock_candidates"][key],
                (
                    "Corrected alpha result\nFace replaced with a gradual mix at the edge"
                    if step == 7
                    else "Normal clone result\n" "Matched boundary colors with background kept"
                ),
            )
        elif step == 9:
            # The final grid keeps the originals above the three results, making
            # it possible to compare both the inputs and the changes between methods.
            panels = [
                (
                    face_blending_results["alex_original_image"],
                    "Alex\nOriginal photograph supplying the face",
                ),
                (
                    face_blending_results["the_rock_original_image"],
                    "The RocK\nOriginal photograph receiving the face",
                ),
                (
                    preview_alex_face_on_gray(
                        "corrected_alex_face", face_masks["alex_blend_alpha"]
                    ),
                    "Corrected face\nAligned and adjusted before blending",
                ),
                (
                    face_blending_results["alex_on_the_rock_baseline"],
                    "Uncorrected baseline\nFirst blend before matching skin colors",
                ),
                (
                    face_blending_results["alex_on_the_rock_candidates"]["alex_on_the_rock_alpha"],
                    "SELECTED: corrected alpha\nMixes both photos at the face edge",
                ),
                (
                    face_blending_results["alex_on_the_rock_candidates"]["alex_on_the_rock_clone"],
                    "Normal cloning comparison\nUses The Rock'scolors at the face boundary",
                ),
            ]
            for index, (pixels, title) in enumerate(panels):
                show_bgr_image(axes[index], pixels, title)
        else:
            raise ValueError(f"Unknown walkthrough stage: {step}")
        return figure
    except BaseException:
        # CLEANUP: Even a failed panel or interrupted draw owns only this figure.
        # Re-raise the error after closing it so main() can explain why the run stopped.
        plt.close(figure)
        raise


# ---


# __________________________________________
# TERMINAL AND FIGURE CONTROLS
# ==========================================


# --- wait_for_guide_command()
def wait_for_guide_command(final_step: bool = False) -> str:
    """Wait for C to continue or Q to quit, without freezing the picture windows.

    The reader types a letter and presses Enter. Reading a complete line uses
    the same terminal input on Windows, macOS, and Linux without checking the OS.

    Args:
        final_step: Whether the last view is already displayed, leaving only Q to quit.

    Returns:
        Lowercase "c" to advance or "q" to finish the walkthrough.
    """
    # The input reader and the window display do two different jobs. Queue passes
    # the response safely from the input thread back to the main thread:
    #
    #     Terminal line -> read_input() -> commands.put()
    #                                      |
    #     Window updates <- plt.pause()    +-> commands.get() -> next step or quit
    #
    # While the queue is empty, the main thread keeps Matplotlib responsive.
    commands: Queue[str] = Queue()
    prompt = EXIT_PROMPT if final_step else NEXT_PROMPT

    # --- read_input()
    def read_input() -> None:
        """Read one terminal response and pass it back to the walkthrough."""
        try:
            # readline() waits for the submitted line, including its trailing newline.
            # strip() removes surrounding whitespace, and lower() accepts C/Q or c/q.
            # An empty string from readline() means input has ended, so use Q.
            # A submitted blank line is "\n" instead and is handled by the prompt loop.
            line = sys.stdin.readline()
            command = line.strip().lower() if line else "q"
        except OSError:
            # If the terminal input ends, finish with the results already saved.
            command = "q"
        commands.put(command)
        # The reader is finished once its one response is in the queue. Any further
        # prompt starts another reader; this function never changes a figure or image.

    # ---

    while True:
        print_wrapped(prompt, style="prompt")
        # readline() waits here in a separate thread. Only the main thread works
        # with Matplotlib, so the reader can still move and inspect the pictures.
        # daemon=True means this waiting reader does not keep Python running after
        # the main program has ended. The regular C/Q flow consumes its response first.
        Thread(target=read_input, daemon=True).start()
        while commands.empty():
            # pause() services window events briefly, rather than leaving the main
            # thread blocked on terminal input or repeatedly checking without a wait.
            plt.pause(0.1)
        command = commands.get()
        # On the last view, C has nowhere further to go. Other responses simply
        # show the choices again; they do not advance or rerun image processing.
        if command == "q" or (command == "c" and not final_step):
            return command
        print_wrapped("Please use one of the choices shown above.", style="info")


# ---


# --- run_face_blending_guide()
def run_face_blending_guide(face_blending_results: dict) -> None:
    """Show and save each teaching view, then wait for the reader's terminal response.

    All image transformations have already completed. Earlier views stay open
    for comparison while C opens the next view. Q finishes the presentation.

    Args:
        face_blending_results: The complete results dictionary, shared by all nine teaching views.
    """
    # The same sequence is used for each step:
    #
    #     build figure -> save its PNG -> show picture -> explain -> wait for C or Q
    #
    # Saving first gives every displayed view a file the reader can inspect later.
    # This folder holds presentation images, separate from the full-size replacement.
    WALKTHROUGH_DIRECTORY.mkdir(parents=True, exist_ok=True)
    # Refresh the pictures without repeatedly bringing them in front of the terminal.
    # rc_context() applies this display preference only during the walkthrough and
    # restores the previous setting afterward. It does not change image pixel values.
    with plt.rc_context({"figure.raise_window": False}):
        try:
            for step in range(1, len(STAGE_TITLES) + 1):
                print_wrapped(f"Opening step {step}/{len(STAGE_TITLES)}...", style="info")
                figure = build_face_blending_guide_figure(step, face_blending_results)
                figure.savefig(WALKTHROUGH_DIRECTORY / f"stage_{step:02d}.png", dpi=120)
                # block=False allows execution to continue to the explanation and
                # prompt while earlier figures remain available for comparison.
                plt.show(block=False)
                # Give Matplotlib time to draw the picture before its explanation.
                plt.pause(0.1)
                print_face_blending_guide_step(step)
                # The reader controls progression. This call returns only after
                # receiving one of the choices allowed at the current step.
                if wait_for_guide_command(final_step=step == len(STAGE_TITLES)) == "q":
                    break
        finally:
            # Close the presentation's windows when the reader quits or presses Ctrl+C.
            plt.close("all")


# ---


# __________________________________________
# MAIN FUNCTION - ENTRY POINT
# ==========================================


# --- main()
def main() -> int:
    """Load the photographs, save the final images, and present the nine teaching stages.

    Returns:
        Zero on success, one after an input/save/display failure, or 130 on Ctrl+C.

    Logic:
        Load and process the photos,
        save the result and comparison, then open the guided walkthrough.
    """
    # This function coordinates the assignment. The processing functions explain
    # and perform the individual OpenCV operations; main() connects their results
    # to the saved files and the presentation:
    #
    #     load_bgr_image() -> create_alex_on_the_rock_results() -> save_bgr_image_as_png() /
    # save_alex_the_rock_comparison()
    #                                      -> run_face_blending_guide()
    #
    # outputs_saved becomes True only after both final files have been written.
    # It lets the messages explain what is still available if the reader stops early.
    outputs_saved = False
    print_banner("CSC515 - Portfolio Milestone Module 3\n" "Option #2: Blending Images in OpenCV")
    print_wrapped("The program places Alex's face into The Rock'sphotograph.", style="info")
    try:
        
        # __________________________________________
        # STEP 1: LOAD THE TWO ORIGINAL IMAGES.
        # ==========================================

        # Load both originals once. Their file paths identify the photos; the returned
        # arrays hold the BGR pixels used by all later calculations and comparisons.
        alex_original_image = load_bgr_image(ALEX_IMAGE_PATH)
        the_rock_original_image = load_bgr_image(THE_ROCK_IMAGE_PATH)
        print_wrapped(
            "\nCropping keeps the part of Alex's photograph that contains the face. "
            "An affine transform then maps Alex's eyes and mouth onto The Rock's"
            "matching points, adjusting the face's size, angle, and position. "
            "These coordinates were chosen manually for the supplied photographs."
        )

        # __________________________________________
        # STEP 9: CREATE THE FINAL RESULT.
        # ==========================================

        face_blending_results = create_alex_on_the_rock_results(
            alex_original_image, the_rock_original_image
        )
        # face_blending_results keeps the originals, masks, aligned face, and both corrected methods
        # together. The walkthrough reuses them, so pressing C never recalculates a blend.
        print_wrapped(
            "\nA blending mask tells the program how much of Alex and The Rock to use "
            "at each position. The center uses Alex's face, and the edge gradually mixes "
            "with The Rock'sphotograph. Separate skin masks select small forehead and "
            "cheek patches to compare their colors. Color matching moves Alex's skin "
            "colors toward The RocK's, with less change near the glasses and beard."
        )
        print_wrapped(
            "\nBoth methods use the corrected face and The Rock'soriginal photograph. "
            "Alpha blending mixes their colors using one weight per pixel. Normal cloning "
            "uses changes between neighboring pixels and The Rock'scolors at the boundary. "
            "Keeping the original blend provides a starting result for the comparison."
        )

        # __________________________________________
        # STEP 10: SAVE THE FINAL RESULT.
        # ==========================================

        # Choose the already-calculated candidate using SELECTED_ALEX_ON_THE_ROCK_METHOD. The
        # four-panel
        # comparison also reads that same candidate, keeping the two saved outputs consistent.
        save_bgr_image_as_png(
            face_blending_results["alex_on_the_rock_candidates"][SELECTED_ALEX_ON_THE_ROCK_METHOD],
            ALEX_ON_THE_ROCK_RESULT_PATH,
        )

        # __________________________________________
        # STEP 11: SAVE THE COMPARISON.
        # ==========================================

        save_alex_the_rock_comparison(face_blending_results)
        outputs_saved = True
        print_wrapped(
            f"Saved full-resolution result: {ALEX_ON_THE_ROCK_RESULT_PATH}\n"
            f"Saved comparison: {ALEX_THE_ROCK_COMPARISON_PATH}",
            style="success",
        )
        # __________________________________________
        # STEP 12: EXECUTE THE PROGRAM AND DISPLAY THE RESULTS IN A GUIDE.
        # ==========================================

        run_face_blending_guide(face_blending_results)
    except KeyboardInterrupt:
        # Ctrl+C is a reader-requested cancellation. Explain whether the final files
        # were saved, then return 130 so the launching terminal can recognize an interruption.
        print_wrapped("\nWalkthrough cancelled. Remaining stages were not presented.", style="info")
        if outputs_saved:
            print_wrapped(
                "The result and comparison were already saved " "in mod_images/.", style="success"
            )
        else:
            print_wrapped("Processing stopped before all final outputs were saved.", style="error")
        return 130
    except (OSError, ValueError, RuntimeError, ImportError, cv2.error) as error:
        # Keep the underlying error message, such as a missing photo or failed image write.
        # stderr separates errors from the normal explanation stream. Returning 1 reports
        # that the run did not finish successfully without discarding any files already saved.
        print_wrapped(
            f"The face-blending run could not finish: {error}", style="error", stream=sys.stderr
        )
        if outputs_saved:
            print_wrapped(
                "The saved result and comparison remain available " "in mod_images/.",
                style="info",
                stream=sys.stderr,
            )
        return 1
    print_wrapped("The result and comparison are saved in mod_images/.", style="success")
    # Reaching this point means the normal run finished. Zero is the success status
    # returned to the terminal by sys.exit() in the initialization block below.
    return 0


# ---


# __________________________________________
# MODULE INITIALIZATION
# ==========================================

# Python sets __name__ to "__main__" when this file is launched as the program.
# The guard starts the assignment in that case. Importing its functions elsewhere
# leaves the walkthrough unopened and does not write any results by itself.
# sys.exit() passes main()'s status back to the terminal that launched the script.
if __name__ == "__main__":
    sys.exit(main())


# __________________________________________
# END OF FILE
# ==========================================
