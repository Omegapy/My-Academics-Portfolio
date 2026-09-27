# -----------------------------------------------------------------------------
# Module Type: executable script
# Author: Alexander Ricciardi (Omega.py)
# Created: 2026-09-22
# -----------------------------------------------------------------------------
# Course: Foundations of Computer Vision CSC515
# Professor: Dr. Binbong Li
# Term: Fall C (26FC) - 2026
# Assignment: Critical Thinking Module 2
# -----------------------------------------------------------------------------
# The Program:
# The program uses the "org_images/puppy.jpg" image to perform color transformation using OPenCV
# The program separates Blue, Green and Red (BGR) color values of the image and creates
# another image by swapping the red and green values. 
# Blue → stays Blue
# Green → moves into the Red position
# Red → moves into the Green position
# -----------------------------------------------------------------------------
# Requirements:
# - Python 3.12
# - OpenCV 4.13.0 (opencv-contrib-python==4.13.0.92), NumPy 2.5.3
# - term-image 0.7.2 with Pillow 10.4.0; see requirements.txt for package pins.
# - An interactive terminal supporting the iTerm2 inline image protocol.
#   In VS Code, enable terminal.integrated.enableImages in terminal settings.
#
# Run from this folder:
#    python Module2_CTA.py
#
# Contents Overview:
# - load_image()
#   - Decode the supplied JPEG as a BGR pixel array and report unreadable input.
# - create_results()
#   - Extract the three intensity planes and merge the two color results.
# - save_image()
#   - Write a lossless PNG and report a failed write.
# - display_image()
#   - Render a saved PNG with its label and explanation using terminal graphics.
# - get_preview_renderer()
#   - Select PNG rendering and check that terminal pixel dimensions are available.
# - print_transformation_explanation()
#   - Print the code, channel matrix, and an example from the actual image.
# - render_preview_lines() / print_preview_row()
#   - Render aligned image panels without changing the saved image arrays.
# - display_transformation()
#   - Show the explanation followed by the original, inputs, and result.
# - main()
#   - Coordinate image processing, saving, terminal presentation, and error reporting.
# -----------------------------------------------------------------------------

"""Extract the color channels, reconstruct the image, and swap red with green.

OpenCV reads the image into a uint8 array with shape (height, width, 3).
Each pixel has three values in BGR order: blue, green, and red. The values
range from 0 to 255. cv2.split() separates them into three 2D arrays, each
with shape (height, width).

It merges (blue, green, red) to put the original image back together. For the
second merge, it uses (blue, red, green) to exchange red and green. The output
still uses BGR storage. In RGB order, its colors come from the original
(green, red, blue) channels, which is the GRB result in the assignment.
- Blue → stays Blue
- Green → moves into the Red position
- Red → moves into the Green position
"""

# __________________________________________
# IMPORTS
# ==========================================

from pathlib import Path
import os
import shutil
import sys
import textwrap
from typing import TextIO

import cv2
import numpy as np


# __________________________________________
# GLOBAL CONSTANTS
# ==========================================

# This scripts folder is used to find the input and output files.
# The 'org_images' folder contains the original image.
# The 'mod_images' folder contains the modified image.
# This allows the program to be run from either location shown in the README.
ASSIGNMENT_DIRECTORY = Path(__file__).resolve().parent
INPUT_PATH = ASSIGNMENT_DIRECTORY / "org_images" / "puppy.jpg"
OUTPUT_DIRECTORY = ASSIGNMENT_DIRECTORY / "mod_images"

# Each filename has a title, an explanation, and a note about the channel values.
# The program shows the results in this order. A newline in a title adds a subtitle.
RESULT_DESCRIPTIONS = {
    "red_channel.png": (
        "Red channel intensity\nThe original red values, shown as a 2D grayscale image",
        "This image keeps the red value from each pixel of the original picture. "
        "The blue and green values are left out of this result.",
        "Darker pixels have lower red values; brighter pixels have higher red values. "
        "Black represents 0, and white represents 255 in this grayscale display.",
    ),
    "green_channel.png": (
        "Green channel intensity\nThe original green values, shown as a 2D grayscale image",
        "Here, we are looking at the green value from each original pixel. "
        "The result keeps those values without including blue or red.",
        "A dark pixel has a low green value, and a bright pixel has a high green value. "
        "The display goes from black at 0 to white at 255.",
    ),
    "blue_channel.png": (
        "Blue channel intensity\nThe original blue values, shown as a 2D grayscale image",
        "This result shows the blue value at each position in the original image. "
        "The green and red values are not included in this 2D array.",
        "Low blue values appear darker, and high blue values appear brighter. "
        "A value of 0 appears black; a value of 255 appears white.",
    ),
    "reconstructed.png": (
        "Reconstructed original\nPutting the three channels back in their original positions",
        "It put blue, green, and red back together in OpenCV's BGR order. "
        "The result has the same colors and pixel values as the decoded original image.",
        "In the separate channel images below, lower values still appear darker and "
        "higher values appear brighter. The merge puts those values back into a color image.",
    ),
    "red_green_swapped.png": (
        "Red/green swapped (GRB)\nUsing the red values for green, and the green values for red",
        "For this merge, it keeps blue where it was and exchanges red and green. "
        "The colors change, but each pixel stays in the same row and column.",
        "The input channel images still show lower values as darker and higher values "
        "as brighter. Their values stay the same; what changes is where it put them in the merge.",
    ),
}


# OpenCV stores one pixel as [B, G, R], so blue is at index 0, green at 1, and red at 2.
# It also uses these indices (0,1,2) to match the selected channel in its colored preview.
CHANNEL_INDICES = {
    "blue_channel.png": 0,
    "green_channel.png": 1,
    "red_channel.png": 2,
}

# These matrices also appear in the terminal above the pictures.
# Printing them without wrapping the text so their rows and columns stay aligned.
TRANSFORMATION_MATRICES = {
    "blue_channel.png": """\
                 [ B ]
B = [1  0  0]  @ [ G ]
                 [ R ]

B = 1*B + 0*G + 0*R
""",
    "green_channel.png": """\
                 [ B ]
G = [0  1  0]  @ [ G ]
                 [ R ]

G = 0*B + 1*G + 0*R
""",
    "red_channel.png": """\
                 [ B ]
R = [0  0  1]  @ [ G ]
                 [ R ]

R = 0*B + 0*G + 1*R
""",
    "reconstructed.png": """\
[B']   [1  0  0]   [B]   [B]
[G'] = [0  1  0] @ [G] = [G]
[R']   [0  0  1]   [R]   [R]
""",
    "red_green_swapped.png": """\
[B']   [1  0  0]   [B]   [B]
[G'] = [0  0  1] @ [G] = [R]
[R']   [0  1  0]   [R]   [G]
""",
}

# These sizes count terminal character cells, not pixels in the original image.
MIN_PANEL_WIDTH = 18
MAX_PANEL_WIDTH = 64
MAX_PREVIEW_HEIGHT = 20
PANEL_SEPARATOR = " | "

# The explanations are in the terminal's normal text color. These accents
# separate headings, code, examples, and channel labels without changing the words.
# ANSI escape codes control text appearance; they do not change any image values.
TEXT_STYLES = {
    "heading": "\033[1;96m",
    "rule": "\033[36m",
    "info": "\033[36m",
    "code": "\033[1;93m",
    "matrix": "\033[96m",
    "example": "\033[93m",
    "success": "\033[1;92m",
    "error": "\033[1;91m",
    "red": "\033[1;91m",
    "green": "\033[1;92m",
    "blue": "\033[1;94m",
}
TEXT_RESET = "\033[0m"


# __________________________________________
# IMAGE INPUT
# ==========================================

# --- load_image()
def load_image(path: Path) -> np.ndarray:
    """Read the JPEG into a BGR pixel array without changing the original file.

    Args:
        path: Location of the original JPEG image.

    Returns:
        A nonempty uint8 array with shape (height, width, 3).
        Each pixel contains blue, green, and red values, in that order.

    Raises:
        FileNotFoundError: There is no file at the given path.
        ValueError: OpenCV could not read any pixels from the file.
        cv2.error: OpenCV encountered another error while reading the image.
    """
    # Error check: Stop with a missing-file error before asking OpenCV to read the image.
    if not path.is_file():
        raise FileNotFoundError(f"Input image does not exist: {path}")

    # cv2.imread() reads the image file and decodes it into a NumPy pixel array in memory.
    # str(path) changes the Path object into the filename string that OpenCV receives.
    # cv2.IMREAD_COLOR requests three channels in BGR order: blue, green, and red.
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    # Error check: A failed read returns None. An empty array has no pixel values.
    # Either result means we cannot continue, so I raise ValueError here.
    if image is None or image.size == 0:
        raise ValueError(f"OpenCV could not read the image: {path}")
    return image
# ---


# __________________________________________
# CHANNEL EXTRACTION AND MERGING
# ==========================================

# --- create_results()
def create_results(image: np.ndarray) -> dict[str, np.ndarray]:
    """Separate the three channels, reconstruct the original, and create the red/green swap.

    Args:
        image: The uint8 BGR image returned by load_image().

    Returns:
        A dictionary that pairs the five PNG filenames with their image arrays.
        All arrays keep the original height and width. The input image is unchanged.
    """
    # cv2.split() returns three separate 2D arrays in BGR order. Each array keeps
    # one channel's original values and the image's height and width.
    # A channel array is also called a plane. It appears in grayscale when displayed,
    # but it is not a weighted grayscale conversion of the whole color image.
    #
    # We can write one pixel's BGR values as a column vector:
    #
    #                 [ B ]
    #     p_BGR =     [ G ]
    #                 [ R ]
    #
    # Here, B, G, and R are values from 0 to 255. cv2.split() separates the whole
    # image into three 2D matrices, with one matrix for each channel:
    #
    #     Blue  plane:  B = [b_ij]
    #     Green plane:  G = [g_ij]
    #     Red   plane:  R = [r_ij]
    #
    # The row vectors below show how to select one value from a BGR pixel.
    # Each 1 selects a channel, and the 0s leave out the other two. We are selecting
    # color values, not applying a geometric transformation to the image:
    #
    #     B = [1  0  0] [B]      G = [0  1  0] [B]      R = [0  0  1] [B]
    #                   [G]                    [G]                    [G]
    #                   [R]                    [R]                    [R]
    #
    # This selection happens at every (row, column) position in the image.
    blue, green, red = cv2.split(image)

    # cv2.merge() puts the three 2D arrays together along the channel dimension.
    # OpenCV reads the resulting positions as BGR. Putting red where green belongs,
    # and green where red belongs, therefore exchanges those two colors.
    #
    # For this first merge, it keeps blue, green, and red in their original positions.
    # At each pixel, splitting and merging this way is equivalent to using the
    # 3 x 3 identity matrix, which leaves the three values unchanged:
    #
    #     [B']   [1  0  0] [B]   [B]
    #     [G'] = [0  1  0] [G] = [G]
    #     [R']   [0  0  1] [R]   [R]
    #
    # cv2.merge((blue, green, red)) puts the original BGR image back together.
    reconstructed = cv2.merge((blue, green, red))

    # For the second merge, it swaps red and green. This is a channel permutation:
    # blue stays at index 0, while the original red and green values trade places:
    #
    #     [B']   [1  0  0] [B]   [B]
    #     [G'] = [0  0  1] [G] = [R]
    #     [R']   [0  1  0] [R]   [G]
    #
    # The output still uses BGR storage. It fills those positions with the original
    # (blue, red, green) values instead of (blue, green, red). In RGB order, the
    # output colors come from the original (green, red, blue) channels. That is
    # the GRB image requested by the assignment. For example, an original BGR
    # pixel [20, 100, 200] becomes [20, 200, 100].
    #
    # Only the color values change positions within each pixel. The pixel itself
    # does not move, rotate, or scale; its row and column stay the same.
    swapped = cv2.merge((blue, red, green))
    return {
        "red_channel.png": red,
        "green_channel.png": green,
        "blue_channel.png": blue,
        "reconstructed.png": reconstructed,
        "red_green_swapped.png": swapped,
    }
# ---


# __________________________________________
# IMAGE OUTPUT
# ==========================================

# --- save_image()
def save_image(image: np.ndarray, path: Path) -> None:
    """Save a channel or BGR image as a PNG without changing its height or width.

    Args:
        image: One of the channel arrays or merged images from create_results().
        path: Where to save the PNG in this assignment's mod_images folder.

    Raises:
        OSError: OpenCV returned False instead of saving the file.
        cv2.error: OpenCV encountered an error while encoding or writing the image.
    """
    # cv2.imwrite() uses the .png extension to choose PNG encoding. PNG keeps the
    # channel values without losing information. OpenCV treats a three-channel
    # array as BGR when writing it. str(path) supplies the destination filename.
    # Error check: If imwrite() returns False, the image was not saved.
    if not cv2.imwrite(str(path), image):
        raise OSError(f"OpenCV could not write the image: {path}")
# ---


# __________________________________________
# TERMINAL TEXT FORMATTING
# ==========================================

# --- style_text()
def style_text(message: str, style: str = "", *, stream: TextIO | None = None) -> str:
    """Add a text color, then reset it so the next message keeps its own appearance.

    Args:
        message: Text that has already been wrapped or aligned.
        style: Name from TEXT_STYLES, or an empty string for normal terminal text.
        stream: Output receiving the text. The default is the current stdout.

    Returns:
        The same words with color codes around them, or plain text when color is off.
    """
    output = sys.stdout if stream is None else stream
    # A file or pipe should receive readable text, not color codes. NO_COLOR also
    # lets us turn off the accents without changing the program. Check stderr
    # separately so an error does not inherit stdout's color setting.
    if (
        not message
        or not style
        or not output.isatty()
        or os.environ.get("NO_COLOR")
        or os.environ.get("TERM", "").lower() == "dumb"
    ):
        return message
    color = TEXT_STYLES.get(style, "")
    return f"{color}{message}{TEXT_RESET}" if color else message
# ---


# --- get_label_style()
def get_label_style(label: str) -> str:
    """Use the source channel's color for its title; use cyan for the other titles.
    
    Args:
        label: The label for the current step.
        
    Returns:
        The style for the label.
    """
    # split the label into title and subtitle
    title = label.split("\n", 1)[0].lower()
    # Read the title only. During the swap, a subtitle mentions both the source
    # and destination colors, but the input label still names its original channel.
    for channel in ("blue", "green", "red"):
        # Check if the title starts with any of the channel-specific prefixes
        if title.startswith((
            f"{channel} channel",
            f"{channel}-only",
            f"input: {channel} ",
            f"result: 2d {channel} ",
        )):
            return channel
    return "heading"
# ---


# --- print_program_banner()
def print_program_banner(title: str, subtitle: str) -> None:
    """Put the existing program title and description inside a startup banner.

    Args:
        title: Program heading, kept in its original wording.
        subtitle: Existing description of the operations shown during the run.
    """
    # Calculate the width of the terminal window
    width = max(1, min(118, shutil.get_terminal_size().columns - 2))
    print()
    # Very narrow terminals need the full width for text rather than box edges.
    if width < 8:
        print(style_text("=" * width, "rule"))
        print_wrapped(title, style="heading")
        print_wrapped(subtitle)
        print(style_text("=" * width, "rule"))
        print(flush=True)
        return
    # Calculate the width of the inner part of the banner
    inner_width = width - 4
    # Create the border and empty row strings
    border = "+" + "=" * (width - 2) + "+"
    empty_row = "|" + " " * (width - 2) + "|"
    # Print the top border and empty row
    print(style_text(border, "rule"))
    print(style_text(empty_row, "rule"))
    # Wrap and center plain text first. Color codes are not visible characters
    # and must not count toward the banner's width.
    for message, style in ((title, "heading"), (subtitle, "")):
        # Wrap and center the title and subtitle
        for line in textwrap.wrap(message, width=inner_width):
            print(
                style_text("|", "rule") + " "
                + style_text(line.center(inner_width), style) + " "
                + style_text("|", "rule")
            )
        # Print the bottom border and empty row
        print(style_text(empty_row, "rule"))
    print(style_text(border, "rule"))
    # Print a flush to ensure everything is displayed
    print(flush=True)
# ---


# __________________________________________
# TERMINAL DISPLAY
# ==========================================

# --- display_image()
def display_image(path: Path, label: str, explanation: str) -> None:
    """Show one saved PNG in the terminal with its label and explanation.

    Args:
        path: Saved PNG to display. Reading the file handles its color order.
        label: Title for the image, with a subtitle on a new line when needed.
        explanation: Short explanation printed above the picture.

    Raises:
        OSError: The terminal cannot show inline images, or drawing the image fails.
        ValueError: The display library cannot read or size the PNG preview.
    """
    # Error check: The images need an interactive terminal. Redirecting the output
    # to a file or pipe would not show the pictures there.
    if not sys.stdout.isatty():
        raise OSError("Image previews require an interactive terminal; run without redirection.")
    # Try to load the preview renderer
    from term_image.exceptions import TermImageError
    renderer = get_preview_renderer()
    # Print a blank line for spacing
    print()
    # Split the label into title and subtitle
    title, _, subtitle = label.partition("\n")
    # Print the title with appropriate styling
    print_wrapped(title, style=get_label_style(label), space_after=0)
    # Print the subtitle if it exists
    if subtitle:
        print_wrapped(subtitle, space_after=0)
    print()
    # Print the explanation
    print_wrapped(explanation)
    # Print the filename
    print_wrapped(f"File: {path.name}", style="info")
    # Get terminal size
    columns, lines = shutil.get_terminal_size()
    # Leave room for the text around the preview. These limits use terminal cells.
    # The library accounts for each cell's width and height to keep the image proportions.
    frame = (max(1, min(64, columns - 2)), max(1, min(24, lines - 7)))
    try:
        # from_file() reads the saved PNG through Pillow. This avoids passing a BGR
        # array to a display that expects RGB. The with block releases the image
        # resources when we finish using them.
        with renderer.from_file(str(path)) as preview:
            # With no separate width or height, set_size() fits the picture inside
            # the frame without stretching it. Only the preview changes size;
            # the saved PNG keeps its original resolution.
            preview.set_size(frame_size=frame)
            # method="whole" sends the complete PNG through the inline image protocol.
            # The terminal shows image pixels instead of replacing each character
            # cell with one or two solid colors.
            preview.draw(h_align="left", pad_height=1, method="whole")
    except TermImageError as exc:
        raise OSError(f"Could not display {path.name}: {exc}") from exc
# ---


# --- get_preview_renderer()
def get_preview_renderer() -> type:
    """Select PNG display after checking whether this terminal can show the images.

    Raises:
        OSError: Inline images are unavailable, or the terminal does not report
            the pixel size of its character cells.
    """
    # Wait until the display is needed before checking the terminal.
    # Term-Image 0.7.2 does not include VS Code or its related terminals in its
    # built-in list, so the code below checks those terminals separately.
    from term_image.image import ITerm2Image
    from term_image.utils import get_cell_size, get_terminal_name_version, query_terminal

    terminal_name, _ = get_terminal_name_version()
    if terminal_name == "vscode":
        # VS Code's image addon reports support with device-attribute code 4.
        # Check this terminal session, since enabling images may require opening
        # a new one. Otherwise, the comparison could contain empty picture panels.
        response = query_terminal(b"\033[c", more=lambda data: not data.endswith(b"c"))
        attributes = (response or b"").removeprefix(b"\033[?").removesuffix(b"c").split(b";")
        if b"4" not in attributes:
            raise OSError(
                "Enable terminal.integrated.enableImages in Antigravity/VS Code, "
                "then open a new terminal. Inline images also require GPU acceleration."
            )
        # Antigravity reports its terminal name as vscode. Inline image support
        # in that terminal requires terminal.integrated.enableImages.
        # It applies this support override only to terminals with that reported name.
        ITerm2Image.forced_support = True
    elif not ITerm2Image.is_supported():
        raise OSError(
            "Sharp previews need an inline-image terminal. Use Antigravity/VS Code "
            "with terminal.integrated.enableImages enabled, or iTerm2/WezTerm."
        )

    # The library needs the actual pixel size of a terminal cell. Without it, the
    # fallback is only 1 x 2 pixels per cell, which makes the preview look blocky
    # even when the terminal supports image graphics.
    if get_cell_size() is None:
        raise OSError("The terminal did not report pixel dimensions for image rendering.")
    return ITerm2Image
# ---



# __________________________________________
# EXPLANATIONS AND SIDE-BY-SIDE COMPARISONS
# ==========================================

# display_image() is still available when we need to show a single saved PNG.
# main() uses display_transformation() to show the original, the inputs, and the result.

# --- print_wrapped()
def print_wrapped(message: str, *, style: str = "", space_after: int = 1) -> None:
    """Fit the explanation text to the terminal width; print matrices separately.
    
    Args:
        message (str): The text to wrap.
        style (str, optional): The style to apply to the text.
        space_after (int, optional): The number of blank lines to leave after the text.
        
    Returns:
        None
    """
    # the width of the terminal is used to wrap the text
    width = max(1, min(118, shutil.get_terminal_size().columns - 2))
    # the message is split into paragraphs
    paragraphs = message.split("\n")  
    for index, paragraph in enumerate(paragraphs):
        # A blank line separates paragraphs, not every wrapped line. This keeps
        # a paragraph together while giving the next explanation its own space.
        if index and paragraph and paragraphs[index - 1]:
            print()
        wrapped = textwrap.fill(paragraph, width=width) if paragraph else ""
        print(style_text(wrapped, style))
    # Headings can use space_after=0 to keep their subtitles close. Ordinary
    # explanations leave one blank line before the next block of text.
    print("\n" * max(0, space_after), end="", flush=True)
# ---


# --- print_transformation_explanation()
def print_transformation_explanation(
    filename: str, image: np.ndarray, result: np.ndarray, step: int
) -> None:
    """Explain the operation with its code, matrix, and a pixel from the loaded image.

    Args:
        filename: One of the five result filenames from create_results().
        image: The original image decoded into BGR values, without any changes.
        result: The image array for this operation at its original resolution.
        step: Which comparison to show, numbered from 1 to 5.
        
    Returns:
        None
    """
    # Get the label, explanation, and intensity note for the current filename
    label, explanation, intensity_note = RESULT_DESCRIPTIONS[filename]
    # the width of the terminal is used to wrap the text
    width = max(1, min(118, shutil.get_terminal_size().columns - 2))
    # print the rule
    print("\n" + style_text("=" * width, "rule"))
    # get the title and subtitle
    title, _, subtitle = label.partition("\n")
    # print the title and subtitle
    print_wrapped(f"STEP {step}/5: {title}", style=get_label_style(label), space_after=0)
    # print the subtitle if it exists
    if subtitle:
        print_wrapped(subtitle, space_after=0)
    print(style_text("=" * width, "rule"))
    print()
    print_wrapped(explanation)
    print_wrapped(intensity_note)

    # Use the center pixel from the loaded image so the example matches the
    # picture we are looking at. Converting its uint8 values to Python integers
    # makes the arithmetic easier to read in the terminal.
    row, column = image.shape[0] // 2, image.shape[1] // 2
    b, g, r = (int(value) for value in image[row, column])
    sample = [b, g, r]

    # If the filename is in CHANNEL_INDICES, it means we are looking at a channel extraction step
    if filename in CHANNEL_INDICES:
        channel_index = CHANNEL_INDICES[filename]
        channel_name = ("blue", "green", "red")[channel_index]
        channel_symbol = ("B", "G", "R")[channel_index]
        # print the code for splitting the image
        print_wrapped("Code: blue, green, red = cv2.split(image)", style="code")
        print_wrapped(
            f"This is the {channel_name} array returned by cv2.split(). In the matrix "
            f"below, the 1 selects {channel_symbol}, and the two 0s leave out the other "
            "channels. Each pixel now has one value instead of three, so the result "
            "is a 2D matrix. The grayscale display shows how much of this channel "
            "was present: 0 is none, and 255 is the highest value in this 8-bit image."
        )
        print_wrapped(
            "Reading the three pictures from left to right:\n"
            "Original color image | Selected channel in its own color | 2D grayscale result.\n"
            "The middle picture is a visual aid. It keeps the selected channel and sets "
            "the other two to zero in a separate preview array. It is not an extra "
            "processing step, and it does not convert that preview to get the grayscale "
            "result. The result on the right comes directly from cv2.split()."
        )
    elif filename == "reconstructed.png":
        # print the code for merging the image
        print_wrapped("Code: reconstructed = cv2.merge((blue, green, red))", style="code")
        # print the explanation for merging the image
        print_wrapped(
            "Put each 2D channel array back into its original position: blue into B, "
            "green into G, and red into R. Splitting and merging in this order is "
            "equivalent to the identity matrix below. Every pixel keeps its original "
            "three values, so the reconstructed picture matches the decoded original."
        )
        print_wrapped(
            "Reading the five pictures from left to right:\n"
            "Original | Blue channel input | Green channel input | Red channel input | Result.\n"
            "The three middle pictures are the actual 2D arrays used by cv2.merge(). "
            "They are shown in output order: B, G, R. Each subtitle explains where "
            "that channel's values go in the reconstructed image."
        )
    else:
        # print the code for swapping the channels
        print_wrapped("Code: swapped = cv2.merge((blue, red, green))", style="code")
        # print the explanation for swapping the channels
        print_wrapped(
            "This permutation matrix rearranges the channels. Blue stays where it was. "
            "The original red values become the output's green values, and the original "
            "green values become its red values. The output still uses BGR storage, "
            "but its values come from the original channels as [B, R, G]. In RGB order, "
            "those same output colors are [G, R, B], the GRB result in the assignment."
        )
        print_wrapped(
            "Reading the five pictures from left to right:\n"
            "Original | Blue channel input | Red channel input | Green channel input | Result.\n"
            "The three input arrays keep their original values. Their titles and subtitles "
            "show where those values go: blue to blue, red to green, and green to red. "
            "The B, G, and R slots are the output's blue, green, and red positions."
        )

    # print the matrix
    print_wrapped("The matrix for one pixel (@ means matrix multiplication):", style="heading")
    print(style_text(TRANSFORMATION_MATRICES[filename].rstrip(), "matrix"))
    print()
    # print the note about the prime mark
    if filename not in CHANNEL_INDICES:
        print_wrapped("The prime mark (') identifies an output value; it is not a derivative.")
    print_wrapped(
        "The matrix describes what happens to the color values. The code uses "
        "cv2.split() and cv2.merge() rather than multiplying each pixel by a matrix. "
        "The pixel's row and column do not change."
    )

    # print the example from the center pixel
    print_wrapped(
        f"Example from the center pixel: image[{row}, {column}] = {sample} in BGR order.",
        style="example", space_after=0,
    )
    # If the filename is in CHANNEL_INDICES, it means we are looking at a channel extraction step
    if filename in CHANNEL_INDICES:
        weights = [int(index == channel_index) for index in range(3)]
        expression = " + ".join(f"{weight}*{value}" for weight, value in zip(weights, sample))
        print_wrapped(
            f"Selected channel value: {expression} = {int(result[row, column])}.",
            style="example",
        )
    else:
        output_sample = [int(value) for value in result[row, column]]
        print_wrapped(f"The output pixel is {output_sample} in BGR order.", style="example")
    # print the shape and data type
    print_wrapped(
        f"Array shape: {image.shape} -> {result.shape}. Data type: {result.dtype}.", style="info",
    )
    # print the saved result
    print_wrapped(f"Saved result: {OUTPUT_DIRECTORY / filename}", style="success")
    print(flush=True)
# ---


# --- render_preview_lines()
def render_preview_lines(image: np.ndarray, width: int, height: int) -> list[str]:
    """Prepare a PNG preview as terminal rows without stretching the picture.

    Only the temporary preview is resized. The image array stays unchanged.
    width and height limit the display size in terminal cells, not source pixels.

    Args:
        image: The image data (numpy array) in BGR order.
        width: The desired width of the preview in terminal cells.
        height: The desired height of the preview in terminal cells.
        
    Returns:
        A list of strings representing the terminal rows of the image preview.
    """
    # term-image already uses Pillow, so it is part of the program's dependencies.
    # Importing these here keeps terminal setup separate from image processing.
    from PIL import Image
    from term_image.exceptions import TermImageError
    renderer = get_preview_renderer()

    # Pillow can read a 2D channel array directly, but it expects RGB for a color image.
    # It creates an RGB copy for the preview so it displays OpenCV's BGR values correctly.
    # This display-only conversion is separate from the assignment's red/green swap.
    display_array = image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    try:
        with Image.fromarray(display_array) as pil_image:
            with renderer(pil_image) as preview:
                preview.set_size(frame_size=(width, height))
                # <1 keeps the image left aligned without horizontal padding. .^1 sets
                # vertical alignment within a minimum height of one terminal row.
                # +L sends PNG strips at the terminal's actual pixel resolution.
                # Each strip is one text row high, but it contains many image pixels.
                # Padding is added on the left to center it. print_preview_row() positions
                # each strip because terminals do not all move the cursor the same way.
                # API: https://term-image.readthedocs.io/en/stable/guide/formatting.html
                padding = " " * ((width - preview.rendered_width) // 2)
                return [padding + line for line in format(preview, "<1.^1+L").splitlines()]
    except TermImageError as exc:
        raise OSError(f"Could not render a comparison preview: {exc}") from exc
# ---


# --- print_preview_row()
def print_preview_row(panels: list[tuple[str, np.ndarray]]) -> None:
    """Show the pictures with titles and subtitles, side by side when there is room.

    Each panel pairs its label with an image array. The first label line is the
    title; any remaining lines form its subtitle. A narrow terminal shows the
    panels separately, keeping the same order and explanations.

    Args:
        panels: A list of tuples, where each tuple contains a label string and an
                image array (numpy array in BGR order).
    
    Returns:
        None
    """
    if not panels:
        return
    
    # Get terminal size
    columns, lines = shutil.get_terminal_size()
    available_width = max(1, columns - 2)
    gap = PANEL_SEPARATOR
    minimum_width = len(panels) * MIN_PANEL_WIDTH + (len(panels) - 1) * len(gap)

    # Show one picture at a time when the terminal is too narrow for this row.
    # This is easier to read than shrinking all the pictures into tiny panels.
    if len(panels) > 1 and available_width < minimum_width:
        for panel in panels:
            print_preview_row([panel])
        return
    
    # Calculate the width of each panel
    panel_width = max(
        1, min(MAX_PANEL_WIDTH, (available_width - (len(panels) - 1) * len(gap)) // len(panels))
    )
    # Wrap titles and subtitles separately. The newline needs to stay a real break,
    # and a longer title should not push only its own subtitle below the others.
    labels = [
        textwrap.wrap(label.split("\n", 1)[0], width=panel_width) or [""]
        for label, _ in panels
    ]
    # Wrap subtitles
    subtitles = [
        [
            line
            # Iterate over each paragraph in the subtitle
            for paragraph in label.split("\n")[1:]
            # Wrap each paragraph and add to the list
            for line in (textwrap.wrap(paragraph, width=panel_width) or [""])
        ]
        for label, _ in panels
    ]
    label_height = max(len(label_lines) for label_lines in labels)
    subtitle_height = max(len(subtitle_lines) for subtitle_lines in subtitles)
    # Leave room for the added text above the images. This changes only preview
    # sizing; the five saved PNGs keep their original dimensions and pixel values.
    subtitle_gap = 1 if subtitle_height else 0
    panel_height = max(
        1, min(MAX_PREVIEW_HEIGHT, lines - label_height - subtitle_height - subtitle_gap - 4)
    )
    # Render the preview rows
    rendered = [render_preview_lines(array, panel_width, panel_height) for _, array in panels]

    # These labels are plain text, with no color escape codes, so center() can align
    # them. Print all titles first, then all subtitles, to keep the columns lined up.
    # Add color only after centering each label. The spacing calculation above
    # still uses plain text, so the image columns do not shift when color is on.
    for text_group in (labels, subtitles):
        if text_group is subtitles and subtitle_gap:
            print()
        # Print each line of the labels
        for line_index in range(max(len(text_lines) for text_lines in text_group)):
            # Join the text groups with the gap
            print(style_text(gap, "rule").join(
                style_text(
                    (text_lines[line_index] if line_index < len(text_lines) else "").center(
                        panel_width
                    ),
                    get_label_style(panels[index][0]) if text_group is labels else "",
                )
                # Iterate over each panel in the text group
                for index, text_lines in enumerate(text_group)
            ))
    # Print a rule at the bottom
    print(style_text(gap.join("-" * panel_width for _ in panels), "rule"))

    # Terminals do not move the cursor consistently after an inline PNG.
    # CSI n G moves it to a specific column, counting from 1. I set that position
    # before each picture and separator so one image does not overwrite another.
    for line_index in range(max(len(preview_lines) for preview_lines in rendered)):
        for panel_index, preview_lines in enumerate(rendered):
            column = 1 + panel_index * (panel_width + len(gap))
            if panel_index:
                print(f"\033[{column - len(gap)}G{style_text(gap, 'rule')}", end="")
            preview_line = preview_lines[line_index] if line_index < len(preview_lines) else ""
            print(f"\033[{column}G{preview_line}", end="")
        print()
    print(flush=True)
# ---


# --- display_transformation()
def display_transformation(
    image: np.ndarray, results: dict[str, np.ndarray], filename: str, step: int
) -> None:
    """Show the explanation, then compare the original image, the inputs, and the result.

    Each comparison starts from the same decoded original image. The colored
    single-channel previews are labeled as visual aids, not additional saved results.
    A wide terminal shows the pictures in one row. With less room, the original,
    input group, and result appear below one another in the same reading order.
    
    Args:
        image: The original image data (numpy array) in BGR order.
        results: A dictionary of results, where keys are filenames and values are image arrays.
        filename: The filename of the current image.
        step: The current step number.
    
    Returns:
        None
    """
    if not sys.stdout.isatty():
        raise OSError("Image previews require an interactive terminal; run without redirection.")
    # Get the preview renderer
    get_preview_renderer()

    # Get the result from the results dictionary
    result = results[filename]
    # Print the explanation for the transformation
    print_transformation_explanation(filename, image, result, step)
    # Create the original panel
    original_panel = ("Original color image\nThe same source for each comparison", image)
    # Check if the filename is in the channel indices
    if filename in CHANNEL_INDICES:
        # Get the channel index
        channel_index = CHANNEL_INDICES[filename]
        # Get the channel name
        channel_name = ("Blue", "Green", "Red")[channel_index]
        # Makes a separate array to show the selected channel in its own color.
        # For example, the red-only preview contains [0, 0, R] at each BGR pixel.
        # The actual result stays a 2D array. This preview does not overwrite it.
        colored_channel = np.zeros_like(image)
        colored_channel[:, :, channel_index] = result
        inputs = [(
            f"{channel_name}-only color view (visual aid)\nOther two channels set to 0",
            colored_channel,
        )]
        # Create the result panel
        result_panel = (
            f"Result: 2D {channel_name.lower()} intensity\n"
            f"Original {channel_name.lower()} values shown in grayscale",
            result,
        )
    else:
        # The middle pictures show the actual input channel arrays and where their
        # values go. Swapping channels changes those destinations, not the input arrays.
        order = (
            ("blue", "green", "red")
            if filename == "reconstructed.png"
            else ("blue", "red", "green")
        )
        # Create the input panels
        inputs = [
            (
                f"Input: {channel.upper()} -> {slot} slot\n"
                f"Original {channel} values become output {output_channel}",
                results[f"{channel}_channel.png"],
            )
            # Iterate over each channel in the order
            for channel, slot, output_channel in zip(
                order, ("B", "G", "R"), ("blue", "green", "red")
            )
        ]
        # Create the result label
        result_label = (
            "Result: reconstructed colors\nOriginal BGR values put back together"
            if filename == "reconstructed.png"
            else "Result: red/green swapped\nRed and green exchanged; blue unchanged"
        )
        # Create the result panel
        result_panel = (result_label, result)

    # Combine the panels
    panels = [original_panel, *inputs, result_panel]
    # Calculate the required number of columns
    required_columns = len(panels) * MIN_PANEL_WIDTH + (len(panels) - 1) * len(PANEL_SEPARATOR) + 2
    # Check if the terminal is wide enough to display the panels in a row
    if shutil.get_terminal_size().columns >= required_columns:
        # Print the panels in a row
        print_preview_row(panels)
    else:
        # Print the wrapped explanation
        print_wrapped(
            f"The pictures are shown in groups because this terminal is narrow. "
            f"Widen it to at least {required_columns} columns to see the original, "
            "all inputs, and the result side by side."
        )
        print_preview_row([original_panel])
        print_preview_row(inputs)
        print_preview_row([result_panel])
# ---


# __________________________________________
# MAIN FUNCTION - ENTRY POINT
# ==========================================

# --- main()
def main() -> int:
    """Run the program and return 0 after all five comparisons have been displayed.

    Logic:
        Load -> split -> merge -> save five PNGs -> display the five results.
        It saves all results first so they remain available if terminal display fails.
        Errors are printed to stderr, and a failed run returns a nonzero exit status.
    """
    print_program_banner(
        "CSC515 - Critical Thinking Module 2: Color channel transformation",
        "Extracting blue, green, and red; reconstructing the image; swapping red and green.",
    )
    try:
        image = load_image(INPUT_PATH)
        print_wrapped(
            f"Input image: {INPUT_PATH}\nDecoded array: {image.shape}, {image.dtype} (BGR)",
            style="info",
        )
        results = create_results(image)

        # mkdir() creates this assignment's output folder. parents=True also creates
        # missing parent folders. exist_ok=True lets us run the program again when
        # the folder already exists.
        OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        for filename, result in results.items():
            save_image(result, OUTPUT_DIRECTORY / filename)
    except (OSError, ValueError, cv2.error) as exc:
        print(
            style_text(f"Image processing failed: {exc}", "error", stream=sys.stderr),
            file=sys.stderr,
        )
        return 1

    print_wrapped(f"Saved five PNGs to: {OUTPUT_DIRECTORY}", style="success")
    try:
        # Explain the array's rows, columns, and channels before the five comparisons.
        height, width, channels = image.shape
        print_wrapped(
            f"The image has {height} rows, {width} columns, and {channels} color channels. "
            "image[row, column] gives the three values [B, G, R] for one pixel. "
            "The third array dimension stores color values, not spatial depth. "
            "We are working with a regular color picture, not creating a 3D model."
        )
        print_wrapped(
            "All five results come from the same original image. It separates or rearranges "
            "its color channels without moving the pixels. The code, matrix, and "
            "explanation appear above each comparison so we can connect the operation "
            "to what happens in the pictures."
        )
        print_wrapped(
            "Each picture has a title and a subtitle explaining what it shows. "
            "The terminal previews use PNG graphics at the terminal's pixel resolution. "
            "Only the previews are resized to fit; the five saved PNGs keep their "
            "original dimensions and pixel values. Scroll back to compare the text and pictures."
        )
        for step, filename in enumerate(RESULT_DESCRIPTIONS, start=1):
            display_transformation(image, results, filename, step)
    except (OSError, ValueError, ImportError, cv2.error) as exc:
        print(
            style_text(
                f"Terminal display failed: {exc}\nSaved PNGs remain in {OUTPUT_DIRECTORY}.",
                "error", stream=sys.stderr,
            ),
            file=sys.stderr,
        )
        return 1

    print_wrapped(
        "\nFinished. All five results are saved, and their comparisons have been displayed.",
        style="success",
    )
    return 0
# ---


# __________________________________________
# MODULE INITIALIZATION
# ==========================================

if __name__ == "__main__":
    # report the program execution success or failure to the OS.
    sys.exit(main())


# __________________________________________
# END OF FILE
# ==========================================
