# Critical Thinking Module 4 - Option 2 Laplacian Filters for Different Kernel Windows

**Program:** [Module4_CTA_Option2.py](Module4_CTA_Option2.py)

**Date:** 10/06/2026  
**Grade:** 100% | A  

---

Foundations of Computer Vision CSC515   
Professor: Dr. Bingdong Li 
Fall C (26FC) – 2026   
Student: Alexander (Alex) Ricciardi  

---

## Assignment:

Option #2: Laplacian Filters for Different Kernel Windows
Image filtering involves the application of window operations that perform useful functions, such as noise removal and image enhancement. Compare the effects of Laplacian and Gaussian filters on an image for different kernel windows.

This [image](org_images/Mod4CT2.jpg). In OpenCV, write algorithms for this image to do the following:

1. Apply a Gaussian, a Laplacian, and a Gaussian with Laplacian filter using a 3x3 kernel. For Gaussian, think about how to select a good value of sigma for optimal results.
2. Apply a Gaussian, a Laplacian, and a Gaussian with Laplacian filter using a 5x5 kernel. For gaussian, use the same value of sigma you selected in the above step.
3. Apply a Gaussian, a Laplacian, and a Gaussian with Laplacian filter using a 7x7 kernel. For gaussian, use the same value of sigma you selected in the above step.
4. Output your filter results as 3 x 3 side-by-side subplots to make comparisons easy to inspect visually. That is, your subplot should have 3 rows (1 for each kernel size) and 3 columns (1 for each filter type). Be sure to include row and column labels.

Next, write a 2-3 page summary of your output results. Include in your summary, the following:

- Which filter type (Gaussian, Laplacian, or Gaussian with Laplacian) is preferred for better edge detection and why
- Provide two references of support for your answer and cite them in your summary using correct APA styling.
- Which filter (include kernel size and sigma, if applicable) performed the best visually? Include details like
- whether there were image features better preserved and/or better enhanced. Are these preservations and enhancements of image features important for edge detection? Why or why not?
- Are your results in line with the preferred method? Discuss why or why not?

**Submission Guidelines**

- Your submission should be one executable Python script and one summary of 2-3 pages in length.
- Include at least two scholarly references in addition to the course textbook. The course textbook is Dey, S. (2025). Image processing and computer vision masterclass with Python: Learn advanced image processing techniques, computer vision fundamentals, and applications (2nd ed.). BPB Publications.
- All references must be cited in the text and listed on the references page, in APA 7 format.

**Critical Thinking Assignment Deliverables**

1. A single Word document

* Identify your assignment choice in the title page
    * Screenshots of resulting images in an Appendix section. 
    * 2-3 pages in length (the paper can be more than 3 pages if necessary) to explain your Python program in a single Word document Note you can embed or attach images or/and diagrams if any were produced by your program, the Appendix will only hold the terminal output sections, including all images output by the matplotlib library
    * Include at least two scholarly references in addition to the course textbook
    * APA 7 format

2. A single Python code file.

<<<<<<< HEAD

=======
>>>>>>> 4aa25cca7bad1138efd94399c92f459f429e9866
---

## Program Requirements

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![OpenCV 4.13.0](https://img.shields.io/badge/OpenCV-4.13.0-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![NumPy 2.5.3](https://img.shields.io/badge/NumPy-2.5.3-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib 3.11.2](https://img.shields.io/badge/Matplotlib-3.11.2-11557C?style=flat&logo=python&logoColor=white)](https://matplotlib.org/)


---

## The Program

[Module4_CTA_Option2.py](Module4_CTA_Option2.py) compares Gaussian smoothing,
Laplacian filtering, and Gaussian followed by Laplacian on the supplied noisy
portrait. Each method runs with 3 × 3, 5 × 5, and 7 × 7 windows. All three rows
start from the same grayscale image and use Gaussian sigma **1.0 pixel**.

Image Results:  
<img width="314" height="253" alt="image" src="https://github.com/user-attachments/assets/109d9722-565f-48ec-a169-98521ebdf16c" />

I use the Laplacian to examine rapid changes in brightness that may mark object
boundaries. Noise can produce strong responses too. The comparison shows whether
smoothing first makes the hair outline, collar, and crossed arms easier to follow
without losing too much detail.

The program saves the original/grayscale reference and the required 3 × 3
comparison, then presents five teaching views. Each view is saved and opened before its
terminal explanation. Earlier windows stay open for comparison.

| Stage | Teaching view |
| --- | --- |
| 1 | Original photograph beside the grayscale filtering input. |
| 2 | Gaussian results for 3 × 3, 5 × 5, and 7 × 7. |
| 3 | Direct Laplacian responses for the same three apertures. |
| 4 | Gaussian images above their corresponding Gaussian-then-Laplacian responses. |
| 5 | Required 3 × 3 comparison of all nine results. |

The terminal starts with a course and assignment banner, followed by calculation
and save messages. Each `STEP n/5` explanation includes its purpose, code,
calculation or matrix, and a guide to reading the pictures. Cyan identifies
banners, subtitles, and matrices; yellow identifies code and examples; green
marks saved results; red marks errors; and magenta marks prompts. Longer prose
keeps the terminal's normal color. Redirected output and `NO_COLOR` use plain
text. Code and matrix alignment are preserved, and earlier explanations stay
in the terminal for scrolling back.

The explanations use first person for my choices and connect each code excerpt
to its result. Steps 2 and 3 work through the same real 3 × 3 neighborhood. At
row 83, column 125, the Gaussian weighted sum is 193.256451 and the normalized
Laplacian sum is -17.500000; both match OpenCV. Step 5 explains RMS as response
strength and states why I prefer the 5 × 5 combined result for this photograph.

All nine calculated arrays and the 13 core result files are saved before the
walkthrough. Teaching views are saved as each stage is presented, under
`mod_images/diagnostics/walkthrough/`. Pressing C only advances the presentation;
it does not recalculate a filter.

The source is decoded as BGR `uint8`, then converted to grayscale `float64`
without resizing or changing the 0–255 intensity scale. Gaussian smoothing keeps
fractional averages; `CV_64F` preserves positive and negative Laplacian responses.
All filters use `BORDER_REFLECT_101` to handle neighborhoods at the image boundary.

The Laplacian uses coefficient-normalization factors of 1/4, 1/64, and 1/1024 for
the respective apertures. In the combined method, both stages use the row's
window size. The combined interior support is therefore 5 × 5, 9 × 9, or 13 × 13.
The API parameters and derivative normalization follow the
[OpenCV 4.13.0 filtering documentation](https://docs.opencv.org/4.13.0/d4/d86/group__imgproc__filter.html).

Gaussian panels use the common intensity range 0–255. All six derivative panels
use the same maximum response and the mapping
`sqrt(abs(response) / shared_maximum)`. Individual PNGs use the same mapping as
the comparison figure. These display copies show response strength; the `.npz`
file retains the signed values. The program does not threshold responses or
select zero crossings to produce a final edge map.

### Input and written analysis

The input is the assignment-supplied
[Mod4CT2.jpg](org_images/Mod4CT2.jpg), already stored locally. It is 250 × 166
pixels; no download is needed. Its Git blob is
`d04fde764976613ae3381505848ac75cd8a48a01`. The program never writes to this input
and rejects output paths that refer to it, including symbolic and hard links.
The image is used as course-provided material; no separate redistribution license
was supplied.

[Module4_CTA_Option2_ Explanation.docx](Module4_CTA_Option2_%20Explanation.docx)
contains the written analysis, title page, references, code excerpts, figures,
and appendix screenshots.

For this photograph, the report selects **Gaussian followed by Laplacian with
5 × 5 windows and sigma 1.0** as a useful visual balance between reducing
background clutter and keeping the hair outline, collar, sleeves, and crossed
arms recognizable. The 5 × 5 and 7 × 7 Gaussian results differ by a mean absolute
value of 0.134188 intensity levels. In the fixed right-background sample, the
5 × 5 direct Laplacian RMS is 8.5802; smoothing first reduces it to 2.9419. These
measurements describe responses, not detection accuracy. No clean reference
photograph or labeled edge map was provided.

---

## How to Run the Program

Use Python 3.12. The program was checked with Python 3.12.13, OpenCV 4.13.0
(`opencv-contrib-python==4.13.0.92`), NumPy 2.5.3, and Matplotlib 3.11.2.
The script uses these three packages and the Python standard library.
The `opencv-contrib-python` package provides the `cv2` import; install only one
OpenCV distribution in the selected Python environment.

Open a terminal in the folder containing `Module4_CTA_Option2.py`. Keep
`org_images/Mod4CT2.jpg` beside the program in the shown subfolder. Install the
pinned dependencies from [requirements.txt](requirements.txt), then run:

```bash
python -m pip install -r requirements.txt
python Module4_CTA_Option2.py
```

If your system uses `python3` for Python 3.12, substitute it for `python` in
these commands. A desktop Matplotlib backend is needed for the windowed views.

On an interactive terminal with a working Matplotlib desktop backend, type `C`
to continue or `Q` to quit, then press Enter. Invalid commands prompt again.
Quitting stops the walkthrough; the core results have already been saved. At the
last stage, only `Q` is accepted. It closes the figures and prints the result
location. A normal completion or Q returns exit status 0.

Closing a picture closes only that view; use the terminal to continue or quit.
The input reader runs separately while the main thread processes window events.
The walkthrough does not repeatedly raise windows over the terminal. **Ctrl+C**
cancels, closes the figures, explains whether the core files were already saved,
and returns status 130. A read, write, or display failure returns status 1 and
reports the underlying error.

To generate the complete results and explanation without opening windows:

```bash
python Module4_CTA_Option2.py --no-show
```

For a windowed run without terminal pauses:

```bash
python Module4_CTA_Option2.py --no-pause
```

Close the Matplotlib windows to finish a `--no-pause` run. The display controls
change presentation only; each run calculates and saves the same nine arrays
for its selected image and sigma. `--no-show` saves and explains all five teaching
views without waiting for C/Q. `--no-pause` opens all five views, then waits for
the windows to close.

### Optional arguments

| Argument | Meaning | Default |
| --- | --- | --- |
| `--image PATH` | Use a different input image. | Script-local `org_images/Mod4CT2.jpg` |
| `--output-dir PATH` | Select the result folder. | Script-local `mod_images` |
| `--sigma NUMBER` | Use one finite, positive sigma for all three rows. | `1.0` |
| `--no-show` | Save core results and all five teaching views, and print their explanations without windows or pauses. | Off |
| `--no-pause` | Show figures and print explanations without C/Q pauses. | Off |
| `--help` | Show command-line help. | — |

For example, keep an alternate experiment separate from the report's default run:

```bash
python Module4_CTA_Option2.py --no-show --sigma 1.2 --output-dir mod_images_sigma_1_2
```

Default paths are resolved from the script, so the program can be launched from
another working directory. Explicit relative paths are resolved from the shell's
current directory. Each run replaces the 13 named core result files in its selected
output folder. Each visited teaching stage also replaces its own PNG. An early
quit leaves later stages unpresented; older teaching PNGs can still exist from a
previous run. Select a different output folder to retain a separate experiment.
The image-specific interpretation in the report applies to the supplied image
with sigma 1.0; custom inputs and other sigma values need their own assessment.

---

## Saved results


The default output folder is [mod_images](mod_images). A full run writes 13 core
files plus five teaching PNGs, for 18 generated files:

| File | Contents |
| --- | --- |
| `01_source_reference.png` | Original photograph and grayscale input. |
| `02_filter_comparison_3x3.png` | Labeled three-row, three-column comparison. |
| `gaussian_3x3.png`, `gaussian_5x5.png`, `gaussian_7x7.png` | Gaussian display images. |
| `laplacian_3x3.png`, `laplacian_5x5.png`, `laplacian_7x7.png` | Absolute Laplacian display images. |
| `gaussian_laplacian_3x3.png`, `gaussian_laplacian_5x5.png`, `gaussian_laplacian_7x7.png` | Combined-filter display images. |
| `filter_arrays.npz` | Grayscale input, nine `float64` results, sigma, shared derivative display limit, and display gamma. |
| `terminal_output.txt` | Complete five-step explanation without ANSI color codes, saved even if the presentation is stopped early. |
| `diagnostics/walkthrough/stage_01.png` through `stage_05.png` | Five labeled teaching views matching the terminal stages. |

The included results illustrate the default input and sigma 1.0. The saved
transcript shows its input and output paths relative to this folder. A new run
writes the paths used on the recipient's machine.

---

## Files Map

```text
CTA_Module-4/
├── Module4_CTA_Option2.py
├── Module4_CTA_Option2_ Explanation.pdf
├── README.md
├── requirements.txt
├── mod_images/
│   ├── 01_source_reference.png
│   ├── 02_filter_comparison_3x3.png
│   ├── filter_arrays.npz
│   ├── gaussian_3x3.png
│   ├── gaussian_5x5.png
│   ├── gaussian_7x7.png
│   ├── gaussian_laplacian_3x3.png
│   ├── gaussian_laplacian_5x5.png
│   ├── gaussian_laplacian_7x7.png
│   ├── laplacian_3x3.png
│   ├── laplacian_5x5.png
│   ├── laplacian_7x7.png
│   ├── terminal_output.txt
│   └── diagnostics/
│       └── walkthrough/
│           ├── stage_01.png
│           ├── stage_02.png
│           ├── stage_03.png
│           ├── stage_04.png
│           └── stage_05.png
└── org_images/
    └── Mod4CT2.jpg
```

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
 
