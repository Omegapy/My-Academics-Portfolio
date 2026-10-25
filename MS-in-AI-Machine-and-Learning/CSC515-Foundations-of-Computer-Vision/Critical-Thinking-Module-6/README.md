# Critical Thinking Module 6 - Option 2: Adaptive Thresholding Scheme Accounting for Changes in Illumination

**Program:** [Module6_CTA_Option2.py](Module6_CTA_Option2.py)  
**Explanation:** [Word document](Module6_CTA_Option2_Explanation.docx)

**Date:** 10/24/2026
**Grade:** Pending

---

Foundations of Computer Vision CSC515   
Professor: Dr. Bingdong Li 
Fall C (26FC) – 2026   
Student: Alexander (Alex) Ricciardi  

---

## Overview

The program applies an initial and revised adaptive thresholding scheme to both supplied mug photographs. It saves the calculated results and provides a five-step terminal walkthrough. The Word explanation describes the same settings and measurements. It also explains a separate comparison of the intermediate adaptive settings used to assess the revision. The Appendix is reserved for terminal and figure screenshots and is currently empty.

The revised masks contain recognizable local regions around the mugs, reflections, embossed flowers, and shadows. Complete separation of both mugs from the background remains unresolved. The glossy black mug reflects surrounding objects, so some of its internal brightness changes come from reflections as well as shadows.

---

## Assignment:

Option #2: Adaptive Thresholding Scheme Accounting for Changes in Illumination. 
Select two objects, one light and one dark. Put both objects on a flat surface. Illuminate the scene so that light comes from the direction of the light object. Take a picture of the scene.  Develop a suitable adaptive thresholding scheme to segment the image as best as you can. Now, change the direction of illumination by moving your light source so that the illumination is from the direction of the dark object. Again, take a picture of the scene.  Using this image, see whether your algorithm still works. If not, revise the algorithm to make it work.

Next, write a 2-3 page (it can be more than 3 pages if needed) summary of your observed results. Include in your summary, the following:

**Critical Thinking Assignment Deliverables**

1. A single Word document

* Identify your assignment choice in the title page
    * Screenshots of resulting images and terminal output belong in the Appendix. The current document reserves this section for those captures.
    * 2-3 pages in length (the paper can be more than 3 pages if necessary) to explain your Python program in a single Word document Note you can embed or attach images or/and diagrams if any were produced by your program, the Appendix will only hold the terminal output sections, including all images output by the matplotlib library
    * Include at least two scholarly references in addition to the course textbook
    * APA 7 format

2. A single Python code file.

* Original Image 1: [light_white_mug_side.jpeg](org_images/light_white_mug_side.jpeg)
* Original Image 2: [light_black_mug_side.jpeg](org_images/light_black_mug_side.jpeg)


---

## The program

`Module6_CTA_Option2.py` reads both photographs from `org_images/`. Processing uses each full scene. The original photographs are preserved.

Gaussian adaptive thresholding calculates a local threshold from a weighted neighborhood average minus C. With inverse thresholding, values at or below that threshold become white, or 255. The remaining pixels become black, or 0. The adaptive mask therefore selects locally dark regions, including some background and shadow regions (OpenCV, n.d.).

The initial settings are `blockSize=31` and `C=5`. The revision uses `blockSize=101` and `C=10`. Both photographs receive the same revision, calculated from the same blurred grayscale input used by the initial scheme. The wider neighborhood produces more continuous regions around some boundaries, while the larger C requires a stronger local darkness difference for a fixed neighborhood average. Changing both parameters together shows the behavior of the revised scheme, but does not measure each parameter's effect separately.

The revised adaptive mask is the final result. The cyan overlay marks its selected pixels on a copy of the color photograph without changing the mask.

The black mug's glossy surface reflects objects around it like a curved mirror. Its bright and dark reflected patterns create local threshold changes inside the same physical mug. The white mug's embossed flowers also create real image structure. These details should not all be described as random noise. Local brightness alone does not identify which regions belong to a mug, a reflection, or the background.

### Observed measurements

The program calculates white-pixel counts with `np.count_nonzero()` and connected-region counts with `cv2.connectedComponents(..., connectivity=8)`. Eight-connectivity treats white pixels sharing an edge or a corner as connected. The saved measurements describe the masks; they do not measure segmentation accuracy.

| Measurement | Light from the white mug's side | Light from the black mug's side |
| --- | ---: | ---: |
| Original image, width × height | 2,134 × 1,765 | 2,222 × 1,543 |
| Processed image, width × height | 1,000 × 827 | 1,000 × 694 |
| Initial adaptive white pixels | 66,762 | 66,728 |
| Revised adaptive white pixels | 96,910 | 93,428 |
| Initial adaptive image coverage | 8.0728% | 9.6150% |
| Revised adaptive image coverage | 11.7183% | 13.4622% |
| Initial adaptive connected regions | 380 | 301 |
| Revised adaptive connected regions | 150 | 149 |

The revision produces fewer connected regions, while some boundaries become wider and some regions join. A smaller region count does not establish better segmentation. The photographs also differ in framing and image height, so their count differences cannot be attributed only to illumination. Both photographs were examined during development; neither is a held-out test image.

## Program requirements

Use Python 3.12 with OpenCV, NumPy, and Matplotlib. The included `requirements.txt` pins the reference versions below. Only these three third-party libraries are needed; the remaining imports are part of Python's standard library.

| Component | Reference version |
| --- | --- |
| Python | 3.12.13 |
| OpenCV | 4.13.0 |
| OpenCV package | `opencv-contrib-python==4.13.0.92` |
| NumPy | 2.5.3 |
| Matplotlib | 3.11.2 |

The `opencv-contrib-python` package supplies the `cv2` import. Install only one OpenCV distribution in your environment. A working Matplotlib desktop backend is needed for the interactive windows; `--no-show` saves all results without a graphical display. The script prints the actual installed versions whenever it runs.

## How to run the program

Open a terminal in the folder containing `Module6_CTA_Option2.py`. If needed, install the dependencies into your chosen Python environment:

```bash
python -m pip install -r requirements.txt
```

Run the interactive walkthrough:

```bash
python Module6_CTA_Option2.py
```

If your system names its Python 3 interpreter `python3`, use that command in place of `python` throughout these instructions.

Keep both supplied photographs in `org_images/` beside the script, with their original filenames. Input and default output paths are resolved relative to the script, so the assignment folder can be moved as a unit.

### Terminal controls and options

On an interactive terminal with a working Matplotlib desktop backend, the guide presents one view at a time. Type `C` and press Enter to close the current view and continue. Type `Q` and press Enter to quit. Invalid commands prompt again.

Each of the five steps has one view. Use `C` between views. The final comparison accepts `Q` to finish. Closing a picture closes that view; use the terminal to continue or quit.

All calculated images, measurements, figures, and the complete explanation are saved before the first view. Quitting the walkthrough leaves the saved results available. Normal completion or `Q` returns status 0. **Ctrl+C** closes the figures and returns status 130. An input/output or OpenCV failure is reported in the terminal and returns status 1.

| Option | Behavior |
| --- | --- |
| `--no-show` | Save all results and print the five explanations without opening windows or waiting for C/Q input. |
| `--no-pause` | Show the figures without C/Q pauses. The final display remains open until its windows are closed. |
| `--output-dir PATH` | Save results to another folder. A relative path is resolved from the terminal's current folder. Input paths remain beside the script. |
| `--help` | Show the available command-line options. |

From the same folder, generate results without desktop windows, display without terminal pauses, or choose a separate output folder:

```bash
python Module6_CTA_Option2.py --no-show
python Module6_CTA_Option2.py --no-pause
python Module6_CTA_Option2.py --no-show --output-dir ./my_results
```

The default output folder is `mod_images/` beside the script. Running the program again replaces its matching generated output files in the selected destination. The original JPEGs in `org_images/` are preserved. Each run saves twelve processed images, five teaching figures, a four-row measurement CSV, and the complete five-step transcript.

## Files map

The map uses the original assignment folder name. All files shown are included; `mod_images/` contains saved example results that can be regenerated.

```text
CTA_Module-6/
├── Module6_CTA_Option2.py
├── Module6_CTA_Option2_Explanation.docx
├── README.md
├── requirements.txt
├── mod_images/
│   ├── measurements.csv
│   ├── terminal_output.txt
│   ├── figures/
│   │   ├── 01_preparation.png
│   │   ├── 02_white_side_thresholding.png
│   │   ├── 03_black_side_thresholding.png
│   │   ├── 04_adaptive_revision.png
│   │   └── 05_final_comparison.png
│   ├── light_black_mug_side/
│   │   ├── blurred.png
│   │   ├── final_overlay.png
│   │   ├── grayscale.png
│   │   ├── initial_adaptive.png
│   │   ├── resized_color.png
│   │   └── revised_adaptive.png
│   └── light_white_mug_side/
│       ├── blurred.png
│       ├── final_overlay.png
│       ├── grayscale.png
│       ├── initial_adaptive.png
│       ├── resized_color.png
│       └── revised_adaptive.png
└── org_images/
    ├── light_black_mug_side.jpeg
   └── light_white_mug_side.jpeg

```

| File or folder | Contents |
| --- | --- |
| [Module6_CTA_Option2.py](Module6_CTA_Option2.py) | Single executable script for adaptive thresholding, measurement, saving, and the terminal walkthrough. |
| [Module6_CTA_Option2_Explanation.docx](Module6_CTA_Option2_Explanation.docx) | Program explanation, observed results, research comparison, references, and the empty Appendix. |
| [README.md](README.md) | Assignment, rubric, methods, run instructions, and file map. |
| [org_images/light_white_mug_side.jpeg](org_images/light_white_mug_side.jpeg) | Original photograph illuminated from the white mug's side. |
| [org_images/light_black_mug_side.jpeg](org_images/light_black_mug_side.jpeg) | Original photograph illuminated from the black mug's side. |
| [requirer_reading/Chapter-3_126-141pp.pdf](requirer_reading/Chapter-3_126-141pp.pdf) | Supplied course textbook excerpt used for the explanation. |
| [mod_images/light_white_mug_side/](mod_images/light_white_mug_side/) | Six calculated images for white-side illumination. |
| [mod_images/light_black_mug_side/](mod_images/light_black_mug_side/) | The same six calculated images for black-side illumination. |
| [mod_images/measurements.csv](mod_images/measurements.csv) | Dimensions, adaptive settings, white-pixel counts, coverage, and connected regions for each mask. |
| [mod_images/terminal_output.txt](mod_images/terminal_output.txt) | Complete five-step explanation, actual runtime versions, measurement tables, and figure filenames. |
| [mod_images/figures/](mod_images/figures/) | Five saved Matplotlib views, listed below. |

Each scene folder contains `resized_color.png`, `grayscale.png`, `blurred.png`, `initial_adaptive.png`, `revised_adaptive.png`, and `final_overlay.png`.

| Step | Saved figure | What it shows |
| --- | --- | --- |
| 1 | [01_preparation.png](mod_images/figures/01_preparation.png) | Both original photographs and their full grayscale scenes. |
| 2 | [02_white_side_thresholding.png](mod_images/figures/02_white_side_thresholding.png) | Blurred input and initial adaptive mask for white-side illumination. |
| 3 | [03_black_side_thresholding.png](mod_images/figures/03_black_side_thresholding.png) | The same comparison for black-side illumination. |
| 4 | [04_adaptive_revision.png](mod_images/figures/04_adaptive_revision.png) | Color scenes, initial adaptive masks, and revised adaptive masks for both photographs. |
| 5 | [05_final_comparison.png](mod_images/figures/05_final_comparison.png) | Color scenes, revised adaptive masks, and cyan overlays. |

## References

Bradley, D., & Roth, G. (2007). Adaptive thresholding using the integral image. *Journal of Graphics Tools, 12*(2), 13–21. [https://doi.org/10.1080/2151237X.2007.10129236](https://doi.org/10.1080/2151237X.2007.10129236)

Dey, S. (2025). *Image processing and computer vision masterclass with Python: Learn advanced image processing techniques, computer vision fundamentals, and applications* (2nd ed.). BPB Publications.

OpenCV. (n.d.). *Image thresholding*. OpenCV 4.13.0 documentation. [https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html)

Sauvola, J., & Pietikäinen, M. (2000). Adaptive document image binarization. *Pattern Recognition, 33*(2), 225–236. [https://doi.org/10.1016/S0031-3203(99)00055-2](https://doi.org/10.1016/S0031-3203(99)00055-2)

---

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img width="27" height="27" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53" alt="Code Chronicles logo"></a><a href="https://www.alexomegapy.com"><img height="30" src="https://img.shields.io/badge/Code%20Chronicles%20%7C%20Omegapy-0D1117?style=for-the-badge" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>
 
