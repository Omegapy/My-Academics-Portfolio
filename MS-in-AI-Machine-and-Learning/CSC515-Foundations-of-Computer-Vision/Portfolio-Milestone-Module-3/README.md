# Portfolio Milestone Module 3 - Option #2 Blending Images in OpenCV
Project: Crop, align, and blend Alex's face into The RocK's photograph using OpenCV.

Data: 10/04/2026  
Grade: 100% | A

---

Foundations of Computer Vision CSC515   
Professor: Dr. Binbong Li 
Fall C (26FC) – 2026   
Student: Alexander (Alex) Ricciardi  

---

## Assignment 

Portfolio Project - Option #2: Face Detection and Privacy:   

Option #2: Face Detection and Privacy. 
To address privacy concerns you may want to use data anonymization.  On images, this can be achieved by hiding features that could lead to a person or personal data identification, such as the person’s facial features or a license plate number.

The goal of this project is to write algorithms for face detection and feature blurring.  Select three color images from the web that meet the following requirements:

1. Two images containing human subjects facing primarily to the front and one image with a non-human subject.
2. At least one image of a human subject should contain that person’s entire body.
3. At least one image should contain multiple human subjects.
4. At least one image should display a person’s face far away.
5. All images should vary in light illumination and color intensity. 


First, using the appropriate trained [cascade classifier](https://github.com/opencv/opencv/tree/4.x/data/haarcascades), write one algorithm to detect the human faces in the gray scaled versions of the original images.  Put a red boundary box around the detected face in the image in order to see what region the classifier deemed as a human face. If expected results are not achieved on the unprocessed images, apply processing steps before implementing the classifier for optimal results.

After the faces have been successfully detected, you will want to process only the extracted faces before detecting and applying blurring to hide the eyes. Although the [eye classifier](https://github.com/opencv/opencv/tree/4.x/data/haarcascades) is fairly accurate, it is important that all faces are centered, rotated, and scaled so that the eyes are perfectly aligned. If expected results are not achieved, implement more image processing for optimal eye recognition. Now, apply a blurring method to blur the eyes out in the extracted image.

Inspect your results and write a summary describing the techniques you used to detect and blur the eyes out of human faces in images. Reflect on the challenges you faced and how you overcame these challenges.  Furthermore, discuss in your summary, the accuracy of your results for all three images and techniques you used to improve the accuracy after each repeated experiment.

---

### This Portfolio Milestone Assignment - Option #2: Blending Images in OpenCV:

It is time to think more about your upcoming Portfolio Project. In face and object detection, it is often useful to create a new image by combining two images together. Perhaps you would like to remove a tattoo or create a [deepfake](https://www.proofpoint.com/us/threat-reference/deepfake).

Use a camera to take a picture of yourself facing the frontal. Using an image from the web, create a deepfake by replacing someone else’s likeness with yourself.

### CSC515_M03_PM

| Criteria | Meets Expectation | Approaches Expectation | Below Expectation | Limited Evidence | Pts |
|---|---|---|---|---|---:|
| **Requirements** | **75 to >60.0 pts**  **Meets Expectation**  Includes all of the required components, as specified in the assignment. | **60 to >45.0 pts**  **Approaches Expectation**  Includes most of the required components, as specified in the assignment. | **45 to >30.0 pts**  **Below Expectation**  Includes some of the required components, as specified in the assignment. | **30 to >0 pts**  **Limited Evidence**  Includes few of the required components, as specified in the assignment. | **75 pts** |
| **Content** | **50 to >40.0 pts**  **Meets Expectation**  Demonstrates strong or adequate knowledge of the materials; correctly represents knowledge from the readings and sources. | **40 to >30.0 pts**  **Approaches Expectation**  Some significant but not major errors or omissions in demonstration of knowledge. | **30 to >20.0 pts**  **Below Expectation**  Major errors or omissions in demonstration of knowledge. | **20 to >0 pts**  **Limited Evidence**  Fails to demonstrate knowledge of the materials. | **50 pts** |

**Total Points: 125**

---

## Program Requirements

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![OpenCV 4.13.0](https://img.shields.io/badge/OpenCV-4.13.0-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![NumPy 2.5.3](https://img.shields.io/badge/NumPy-2.5.3-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib 3.11.2](https://img.shields.io/badge/Matplotlib-3.11.2-11557C?style=flat&logo=python&logoColor=white)](https://matplotlib.org/)

Use Python 3.12 and the packages pinned in [requirements.txt](requirements.txt):
`opencv-contrib-python==4.13.0.92`, `numpy==2.5.3`, and `matplotlib==3.11.2`.
These versions were checked in the local Python 3.12.13 environment. The `cv2`
import comes from `opencv-contrib-python`; install only one OpenCV distribution.

Open a terminal in the folder containing `Module3_Portfolio_Option2.py`, then
install the required libraries:

```bash
python -m pip install -r requirements.txt
```

Use an interactive terminal and a graphical desktop with a working Matplotlib
GUI backend. Keep both supplied photographs in `org_images/` beside the script,
with their existing filenames and dimensions. No model download is needed.

---

## The program

`Module3_Portfolio_Option2.py` places the face from `org_images/Alex.png` into
`org_images/the_rock.png`. It completes the two-image blending milestone described
above. The three-image face-detection and eye-blurring work belongs to the later
portfolio project.

All program code stays in this one Python script. The processing sections crop and
align the face, prepare masks, match skin colors, and compare the two blending
methods. `create_alex_on_the_rock_results()` collects these results once. The
saving functions and walkthrough use those same arrays, so the explanations
refer to the images from the current run. A shared image-display helper keeps
BGR-to-RGB conversion and panel labels consistent across the saved comparisons
and teaching views.

The names identify which photograph or mask each part uses. `alex_original_image`
and `the_rock_original_image` hold the two originals. `aligned_alex_face` holds
Alex's face after alignment, and `corrected_alex_face` holds it after matching
skin colors. `alex_skin_sample_mask` and `the_rock_skin_sample_mask` select the
patches used to measure each person's skin color. `alex_blend_alpha` sets how
much of Alex's face appears at each pixel.

The constants follow the same naming. `ALEX_FACE_CROP_BOUNDS` selects Alex's crop.
`ALEX_FACE_ALIGNMENT_POINTS` and `THE_ROCK_FACE_ALIGNMENT_POINTS` mark the eyes
and mouth in their original photographs. Settings beginning with
`ALEX_BASELINE_MASK_` belong to the first blend used for comparison.

The script's 12 step banners mark the loading, processing, saving, and display
work. The terminal guide has nine views that group related operations for
explanation. These are two ways of following the same program, so their step
numbers do not match one for one.

### Main functions

| Function | What it does |
| --- | --- |
| `get_alex_to_the_rock_transform()` | Calculates the matrix that maps Alex's cropped eye and mouth points to The Rock's marked points. |
| `align_alex_face_and_build_baseline_mask()` | Crops and aligns Alex's face, then prepares the mask for the uncorrected baseline. |
| `prepare_alex_and_the_rock_masks()` | Builds Alex's face selection and blending weights, both skin-sample masks, and Alex's color-correction strength map. |
| `match_alex_skin_to_the_rock()` | Adjusts Alex's face colors using The Rock's sampled skin as the reference. |
| `alpha_blend_foreground_with_background()` | Combines two images using a weight at each pixel. It also makes face previews on gray. |
| `clone_alex_face_into_the_rock()` | Creates the seamless-cloning comparison from Alex's corrected face and The Rock's original photograph. |
| `create_alex_on_the_rock_results()` | Collects the originals, masks, baseline, and both corrected results. |
| `run_face_blending_guide()` | Displays and saves the nine teaching views, with C/Q controls in the terminal. |

### Processing steps

The program loads both photographs as BGR pixel arrays. Alex's image is 1536 × 2048
pixels, and the destination is 1192 × 1370. The destination's original fourth
channel is fully opaque, so it can be loaded as a three-channel color image.

1. Crop Alex's face using `(left, top, right, bottom) = (240, 500, 1230, 1770)`.
   The right and bottom limits are excluded. This selects a 990 × 1270 region.
2. Align three manually selected reference points: the image-left eye, image-right
   eye, and mouth center. In `(x, y)` order, the original source points
   `(548, 918)`, `(954, 914)`, and `(752, 1334)` map to `(530, 458)`, `(734, 467)`,
   and `(635, 705)`. The program subtracts the crop offset before calculating the
   affine transform, which adjusts the face's position, orientation, and size.
3. Reproduce the original uncorrected blend as a baseline. It keeps the original
   polygon. `ALEX_BASELINE_MASK_KERNEL = (61, 61)` and
   `ALEX_BASELINE_MASK_SIGMA = 12.0` smooth Alex's aligned baseline mask. This
   smooths the blending weights while preserving the photograph's detail. The
   first blend appears alongside the corrected results in the walkthrough.
4. Keep the new masks separate. Coverage identifies pixels that contain only real
   source data after the warp. The binary face mask selects the face for cloning.
   `create_alex_face_blend_alpha()` uses
   `ALEX_FACE_MASK_FEATHER_PIXELS = 24.0` to fade the final blending weights inward
   over 24 destination pixels, with an opaque center. The skin masks select small
   forehead and cheek samples for color measurements; they do not remove pixels
   from the face.
5. Compare those skin samples in CIE Lab. L represents lightness, while a and b
   represent two color directions. The destination is the reference. The program
   adjusts the source mean and spread with gains limited to 0.25–1.10, maximum
   proposed changes of `(12, 32, 12)` Lab units, and correction fractions of
   `(0.30, 0.95, 0.80)` for L, a, and b. Nearly constant samples keep a gain of 1.
   Smooth strength masks reduce correction around the glasses and beard to 65%
   of the channel fractions. Only the strength mask is smoothed; the face is not blurred.
6. Use that same corrected face for two methods. Alpha blending calculates
   `result = alpha * corrected face + (1 - alpha) * destination` in `float32`,
   then rounds and clips the values before returning to `uint8`. Ordinary
   `NORMAL_CLONE` transfers source gradients into the destination boundary colors.
   Its placement uses the mask's bounding rectangle, giving a center of `(624, 574)`.
   The cloned result receives the same final alpha guard. Both methods restore
   every zero-alpha pixel directly from the unmodified destination.
7. Save the selected result and open the nine teaching views. The selected result
   uses **corrected alpha blending**. The four-panel comparison shows both originals,
   the corrected prepared face on gray, and the final edited class exercise.
   BGR is converted to RGB only when displaying the images.

The final files remain [alex_on_the_rock.png](mod_images/alex_on_the_rock.png), at
1192 × 1370 pixels, and
[face_blending_comparison.png](mod_images/face_blending_comparison.png), at
1350 × 1500 pixels. Each run replaces these two derived files and saves each
teaching view when its window opens. The two photographs in `org_images/`
are the required input files.

The configuration section in `Module3_Portfolio_Option2.py` contains the sample
ellipses, face outline, feather width, Lab limits, protected-feature ellipses, and
selected method. Coordinates are specific to these two photographs. The program
rejects unexpectedly resized inputs and does not detect faces automatically.

### Input and calculation checks

`validate_alex_and_the_rock_images()` checks the original dimensions and pixel
type once at the start of processing. Mask preparation checks crop coverage,
face boundaries, and skin-sample placement. Each skin-sample mask must contain
at least `MIN_ALEX_THE_ROCK_SKIN_SAMPLE_PIXELS = 64` selected pixels before color
matching or plotting uses it.

Color matching checks the correction strengths and avoids dividing by a nearly
zero standard deviation. Blending, cloning, and plotting use the prepared
arrays. File reads and writes still report failures, and cloning checks that
the selected region is large enough.

### The result

The [final teaching view](mod_images/diagnostics/walkthrough/stage_09.png) shows
why I kept corrected alpha blending. Its forehead and cheeks are less orange/pink
than the baseline, and the forehead and jaw transitions are less abrupt. The
frames, eyes, lips, and beard hairs remain visible. Normal cloning made the
forehead and lenses noticeably brighter and gave the face a washed-out appearance,
so I did not select it. Both methods used the same alignment, correction, and mask.

The horizontal band of light across the source forehead remains visible. The head
and chin shapes also differ between the photographs. The color adjustment does
not reconstruct lighting or change the affine alignment. The result is an OpenCV
composite for the class exercise, with no deep-learning or recognition-accuracy claim.

### Saved files

Each run saves the selected face composite and the four-panel comparison in
`mod_images/`. The walkthrough also saves each opened teaching view as
`mod_images/diagnostics/walkthrough/stage_01.png` through `stage_09.png`.
The windows show the baseline, both blending methods, masks, and skin-color graphs.

The included PNGs provide saved examples of the final result, comparison, and all
nine teaching views. The [screenshots document](screenshots_module3_portfolio_milestone.docx)
contains the original photographs, result, and screenshots from program execution.

The two final PNGs are replaced on every completed processing run. A teaching-view
PNG is replaced only when its stage opens; quitting early leaves the remaining
saved views as they were. The original photographs are never overwritten.

With the current inputs and settings, the selected skin patches in Alex's
aligned face have an average Lab a value of 33.30. After color correction, that
average is 10.57, compared with 9.36 in The Rock's reference patches. These
measurements use the skin-sample masks, so the background, glasses, and beard
are excluded from the averages.

### Image and method sources

- `Alex.png` is the user's supplied personal photograph. `the_rock.png` is the
  user's supplied web photograph of The Rock. Its original page and license were not provided.
- OpenCV's [Geometric Transformations of Images](https://docs.opencv.org/4.13.0/da/d6e/tutorial_py_geometric_transformations.html)
  explains the three-point affine mapping and the `(width, height)` output order.
- OpenCV's [Arithmetic Operations on Images](https://docs.opencv.org/4.13.0/d0/d86/tutorial_py_image_arithmetics.html)
  explains weighted blending and limiting changes to an image region. This program
  uses a separate alpha value at each pixel instead of one weight for the entire image.
- OpenCV's [Lab conversion documentation](https://docs.opencv.org/4.13.0/de/d25/imgproc_color_conversions.html)
  defines the normalized float input and Lab channel ranges used for color matching.
- OpenCV's [4.13.0 cloning implementation](https://github.com/opencv/opencv/blob/4.13.0/modules/photo/src/seamless_cloning.cpp)
  shows how ordinary cloning places the nonzero mask's bounding rectangle.

---

### Launch the program

From a terminal in the folder containing `Module3_Portfolio_Option2.py`, run:

```bash
python Module3_Portfolio_Option2.py
```

This command applies to macOS, Linux, and Windows PowerShell when `python` selects
the Python installation with the required libraries. If that command is named
`python3` on your system, use `python3` in both the installation and run commands.
The program takes no command-line arguments. It resolves input and output paths
relative to its own file.

The program prints its title and processing messages while it calculates and
saves the outputs. The guided section then starts at
`STEP 1/9: Original photographs and color values` and presents nine views:

1. Alex and The Rock as the source and destination images.
2. Cropping Alex's face and expressing the marked points relative to that crop.
3. Mapping Alex's eyes and mouth to their positions in The Rock's picture, with separate equations for the new x and y positions.
4. The first blend, before matching skin colors, and the mask used to combine the photos.
5. Selecting the face, measuring skin patches, and controlling color changes.
6. Matching skin colors in Lab and comparing the sampled colors in three graphs.
7. Alpha blending with separate blue, green, and red equations and each image's share of the result.
8. Seamless cloning, its placement rectangle, and keeping the original background.
9. Comparing the originals, the first blend, and the two corrected results.

The first figure opens automatically after calculation and saving, followed by its
terminal explanation. In the terminal, type **C** to continue or **Q** to quit,
then press **Enter**. Lowercase letters work too. After stage nine, type **Q**
and press **Enter** to finish.

Previous figures stay open for comparison. Closing a picture only closes that
view; use the terminal to continue or quit. The pictures stay responsive while
the program waits for a response. **Ctrl+C** also cancels the presentation.
The saved results remain available in `mod_images/`.

The controls read complete lines from the terminal, with the same C/Q choices on
Windows, macOS, and Linux. A small input thread lets Matplotlib keep updating
the pictures. There are no OS checks, raw-key readers, or window-close callbacks.

Terminal banners, subtitles, and calculation diagrams use cyan; code and examples use yellow,
saved-result messages use green, errors use red, and the controls use magenta.
Longer explanation paragraphs keep the terminal's normal text color. Color codes
are omitted from redirected output and when `NO_COLOR` is set.

Run the script from an interactive terminal with a desktop Matplotlib backend.
Restart an already-running process to load code changes. No command-line options
are needed; every run opens the guided presentation.

Windows and Linux execution has not been verified for this submission copy.

### Reading the terminal equations

The terminal explains each image-processing step with code examples and
equations. The code examples use the script's function and variable names.
The equations use labels for one pixel, such as `x_in_crop`
and `blue_alex`, to explain calculations that the program applies to whole arrays.

Step 3 shows how a position in Alex's crop maps to The Rock's image:

```text
x_on_rock = m00 * x_in_crop + m01 * y_in_crop + m02
y_on_rock = m10 * x_in_crop + m11 * y_in_crop + m12
```

Here, x is the horizontal position and y is the vertical position, in pixels.
The `m` labels identify entries in the 2-by-3 transformation matrix. The first
digit gives the row and the second gives the column, starting at zero.
`m02` supplies the horizontal shift, and `m12` supplies the vertical shift.

Step 7 shows the three color calculations separately:

```text
weight = foreground_alpha[y, x]
Alex's share = weight
The Rock's share = 1 - weight

blue_result  = weight * blue_alex  + (1 - weight) * blue_the_rock
green_result = weight * green_alex + (1 - weight) * green_the_rock
red_result   = weight * red_alex   + (1 - weight) * red_the_rock
```

The values ending in `_alex` come from Alex's corrected face. Those ending in
`_the_rock` come from The Rock's original photograph at the same position.
One weight applies to all three channels. A weight of 1 uses Alex, 0 keeps
The Rock, and 0.5 mixes equal amounts. The program then rounds and clips the
result to the 0-255 range. In `foreground_alpha[y, x]`, y selects the row and
x selects the column.

---

**Project Map:**

```text
Portfolio-Milestone-Module-3-Option-2/
├── Module3_Portfolio_Option2.py                   Image processing and guided walkthrough
├── README.md                                      Prompt, method, results, and run commands
├── requirements.txt                               Pinned runtime dependencies
├── screenshots_module3_portfolio_milestone.pdf   Photographs, result, and screenshots
├── mod_images/
│   ├── alex_on_the_rock.png                       Final color composite
│   ├── face_blending_comparison.png               Four-panel comparison
│   └── diagnostics/
│       └── walkthrough/
│           ├── stage_01.png                       Original photographs
│           ├── stage_02.png                       Face crop
│           ├── stage_03.png                       Alignment
│           ├── stage_04.png                       Baseline blend
│           ├── stage_05.png                       Masks and skin samples
│           ├── stage_06.png                       Skin-color matching
│           ├── stage_07.png                       Alpha blending
│           ├── stage_08.png                       Seamless cloning
│           └── stage_09.png                       Final comparison
└── org_images/
    ├── Alex.png                                   Original source face
    └── the_rock.png                               Original destination portrait
```

---

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img height="30" src="https://raw.githubusercontent.com/Omegapy/My-Academics-Portfolio/main/assets/branding/code-chronicles-omegapy-shield.gif" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>
