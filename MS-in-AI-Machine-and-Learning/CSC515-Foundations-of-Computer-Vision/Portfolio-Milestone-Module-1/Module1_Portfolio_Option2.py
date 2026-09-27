# -----------------------------------------------------------------------------
# Module Type: executable script
# Author: Alexander Ricciardi (Omega.py)
# Created: 2026-09-2016
# -----------------------------------------------------------------------------
# Course: Foundations of Computer Vision CSC515
# Professor: Dr. Binbong Li
# Term: Fall C (26FC) - 2026
# Assignment: Portfolio Milestone Module 1 - Option #2: Face Detection and Privacy
# -----------------------------------------------------------------------------
# The Program:
# Using OpenCV, the program loads org_images/brain_image.jpg and displays it.
# The user clicks the image window and presses any key to continue.
# The program closes the window, saves mod_images/brain_image.png, and terminates.
# -----------------------------------------------------------------------------
# Requirements:
# - Python 3.12
#
# Run from this folder:
#    python Module1_Portfolio_Option2.py
#
# Dependencies:
# - cv2 4.13.0 (OpenCV; opencv-contrib-python==4.13.0.92)
# - NumPy 2.5.3
# - pathlib and sys (Python standard library)
#
# Contents Overview:
# - print_message()
#   - Prints the given message with the assigned color.
# - print_banner_tritle_description()
#   - Prints the assignment title and description with colored borders.
# - load_image()
#   - Loads an image file and decodes it into a NumPy array.
# - display_image()
#   - Displays the image in a window until the user presses a key in it.
# - save_image_as_png()
#   - Saves the BGR pixel array into a given image file name with a given file extension.
# - main()
#   - Main function that ties everything together.
# -----------------------------------------------------------------------------

"""Load org_images/brain_image.jpg, display it, and save mod_images/brain_image.png.

    OpenCV loads/decodes the JPG into a 3D NumPy array of shape (height, width, 3).
    The 3 values correspond to each pixel color's value in BGR (blue, green, red).
    The image matrix can be indexed as image[row, column] = [BLUE, GREEN, RED].
            [0] = blue, [1] = green, [2] = red
    The red, green, and blue color values are stored as unsigned 8-bit integers (uint8), 
    which corresponds to RGB color values from 0 to 255.

    Example:
        image = [
            [[255, 0, 0], [0, 255, 0], ...],  # Row 0: blue pixel, green pixel, ... (number of columns - pixel width)
            [[0, 0, 255], [255, 255, 255], ...],  # Row 1: red pixel, white pixel, ... (number of columns - pixel width)
            ... (number of rows - height)
        ]

    Then the program displays the image in a window. After the user presses a key
    in that window, it closes the window and saves mod_images/brain_image.png.
"""

# __________________________________________
# IMPORTS
# ==========================================

from pathlib import Path
import sys

import cv2
import numpy as np


# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

# Resolve image folders from the script so the launch directory does not affect the paths.
ASSIGNMENT_DIRECTORY = Path(__file__).resolve().parent
INPUT_PATH = ASSIGNMENT_DIRECTORY / "org_images" / "brain_image.jpg"
OUTPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "mod_images"
PROGRAM_DESCRIPTION = """This program loads org_images/brain_image.jpg, displays it,
and saves mod_images/brain_image.png.

OpenCV decodes the JPG into a 3D NumPy array in RAM with shape
(height, width, 3). Each pixel stores three color values in BGR order:
    image[row, column] = [BLUE, GREEN, RED]
    [0] = blue, [1] = green, [2] = red
The values are unsigned 8-bit integers (uint8), ranging from 0 to 255.

Example:
    image = [
        [[255, 0, 0], [0, 255, 0]],      # Row 0: blue pixel, green pixel
        [[0, 0, 255], [255, 255, 255]]   # Row 1: red pixel, white pixel
    ]
    print(image[0][0][0]) # Blue value -> 255
    print(image[0][0][1]) # Green value -> 0
    print(image[0][0][2]) # Red value -> 0
    print(image[0][0])    # First pixel -> [255, 0, 0] (blue)
    print(image[0])       # First row -> [[255, 0, 0], [0, 255, 0]]
    print(image)          # Full 2x2x3 array:
    # [[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]]
"""
WINDOW_TITLE = "Brain Image"

# ANSI colors for terminal outputs
COLOR_CYAN = "\033[1;36m"
COLOR_YELLOW = "\033[1;33m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[1;31m"
COLOR_RESET = "\033[0m"


# __________________________________________
# TERMINAL INTERFACE
# ==========================================

# --- print_message()
def print_message(message: str, color: str = "") -> None:
    """Print a message with the assigned color.

    Args:
        message: Text to display
    """
    # COLOR_RESET colors text back to default
    # Flushes = True empties the output buffer and writes the output to
    # the terminal immediately
    # This is implemented because the program may pause while waiting for the
    # user to close the OpenCV window
    # If not the user may not see the text until the OpenCV window is closed
    print(f"{color}{message}{COLOR_RESET}", flush=True)
# ---


# --- print_banner_tritle_description()
def print_banner_tritle_description() -> None:
    """Print the assignment title and description with colored borders."""
    # border: "==== ... ==="
    border = "=" * 64
    # Print the title and subtitle
    print_message(
        f"\n{border}\n"
        "CSC515 - Portfolio Milestone Module 1\n" # Title
        "Option #2: Face Detection and Privacy\n" # Subtitle
        f"{border}",
        COLOR_CYAN,
    )
    # Print  description
    print_message(PROGRAM_DESCRIPTION)
    print_message(f"{border}\n", COLOR_CYAN)
# ---


# __________________________________________
# IMAGE INPUT AND OUTPUT
# ==========================================

# --- load_image()
def load_image(path: Path) -> np.ndarray:
    """Load an image file and decode/store it in RAM as a NumPy array

    Args:
        path: The path to the image file.

    Returns:
        The image as a NumPy array.

    Raises:
        FileNotFoundError: The input is not an existing file.
        ValueError: OpenCV cannot decode a nonempty image from the file.
        cv2.error: OpenCV encounters another image-reading error.
    """
    # Error check: 
    # If the input path does not exist, raise FileNotFoundError.
    if not path.is_file():
        raise FileNotFoundError(f"Input image does not exist: {path}")
    # cv2.imread() loads the image from the file and decodes the JPG image into
    # a NumPy pixel array in memory.
    # str(path) is used to convert the Path object to a string.
    # cv2.IMREAD_COLOR tells OpenCV to load the image as a 3-channel BGR color image
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    # Error check: 
    # if the image cannot be read, it will return None.
    if image is None or image.size == 0:
        raise ValueError(f"OpenCV could not read the image: {path}")
    return image
# ---


# --- save_image_as_png()
def save_image_as_png(image: np.ndarray, directory: Path) -> Path:
    """Save/encode a BGR pixel array into a given image file name with a given file extention

    Args:
        image: The BGR pixel array returned by load_image()

    Returns:
        The path of the new PNG file.

    Raises:
        OSError: The directory cannot be created or the image cannot be written.
        cv2.error: OpenCV reports an image-encoding or writing error.
    """
    # Create the output directory if it does not exist.
    directory.mkdir(parents=True, exist_ok=True)
    # Create an output filename if none exists
    output = directory / "brain_image.png"
    # cv2.imwrite() encodes from BGR pixel array to provided file format (file extension)
    # and saves the image
    # using the path and the file extension
    # here, the .png extension selects PNG encoding
    if not cv2.imwrite(str(output), image):
        # Error check: 
        # If the image cannot be written, it will return False.
        raise OSError(f"OpenCV could not write the image: {output}")
    return output
# ---


# __________________________________________
# IMAGE DISPLAY
# ==========================================

# --- display_image()
def display_image(image: np.ndarray) -> None:
    """Display a BGR image until the user presses a key in its window.

    Args:
        image: The BGR pixel array returned by load_image()

    Raises:
        cv2.error: The window cannot be created
    """
    # try-finally allows cv2.destroyAllWindows() to be called even if an
    # unexpected error occurs while the window is open.
    try:
        # display image in a window
        cv2.imshow(WINDOW_TITLE, image)
        # move the window to a given position on screen
        cv2.moveWindow(WINDOW_TITLE, 50, 10)
        # waitKey(0) waits for any keyboard key press.
        # Loops until a key is pressed.
        cv2.waitKey(0)
    finally:
        # Destroy all windows.
        cv2.destroyAllWindows()
# ---


# __________________________________________
# MAIN FUNCTION - ENTRY POINT
# ==========================================

# --- main()
def main() -> int:
    """Run program."""
    #Display title and description
    print_banner_tritle_description()
    # try-except catches and handles errors
    try:
        # --- Step 1: Load image ---
        print_message("Loading image...", COLOR_CYAN)
        image = load_image(INPUT_PATH)
        print_message(f"Loaded: {INPUT_PATH}\n", COLOR_GREEN)

        # --- Step 2: Display image ---
        print_message("Displaying image...", COLOR_CYAN)
        print_message(
            "Click on the image window if needed.\n"
            "Then press any key to save the image into PNG format and exit the program.\n",
            COLOR_YELLOW,
        )
        display_image(image)

        # --- Step 3: Save image ---
        print_message("Saving copy...", COLOR_CYAN)
        output = save_image_as_png(image, OUTPUT_DIRECTORY)
    # Catch errors and display error message
    except (OSError, ValueError, cv2.error) as error:
        print_message(f"Image workflow failed: {error}", COLOR_RED)
        return 1
    # Display completion message and exit program no error occured 
    print_message(f"Saved copy: {output}\nThank you for using this program!\n", COLOR_GREEN)
    return 0
# ---


# __________________________________________
# MODULE INITIALIZATION
# ==========================================

if __name__ == "__main__":
    sys.exit(main())


# __________________________________________
# END OF FILE
# ==========================================
