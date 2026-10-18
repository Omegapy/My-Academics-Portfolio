# Critical Thinking Module 5 - Option 2: Morphology Operations for Handwritten Text Enhancement

**Program:** [Module5_CTA_Option2.py](Module5_CTA_Option2.py)  
**Explanation:** [Word document](Module5_CTA_Option2_Explanation.docx)

**Date:** 10/18/2026  
**Grade:** 

---

Foundations of Computer Vision CSC515   
Professor: Dr. Bingdong Li 
Fall C (26FC) – 2026   
Student: Alexander (Alex) Ricciardi  

---


## Assignment:

Option #2: Morphology Operations for Handwritten Text Enhancement  
Many companies have thousands of documents to process, analyze, and transform in order to carry out day-to-day operations. Some of these documents might contain handwritten text. Handwritten text can be found in handwritten notes, memos, whiteboards, medical records, historical documents, text input by stylus, etc. Therefore, a complete Optical Character Recognition (OCR) solution has to include support for recognizing handwritten text in images.

Handwriting recognition (HWR), also known as Handwritten Text Recognition (HTR), is the ability of a computer to receive and interpret intelligible handwritten input. A handwriting recognition system handles formatting, performs correct segmentation into characters, and finds the most plausible words. Due to the variety of handwriting styles, orientations, character sizes, and distortions, handwriting recognition is a challenging problem. Thus, to reduce the rejection rates during the matching stage, handwritten text has to be enhanced prior to matching. Enhancement can be achieved using morphological image processing.

Acquire a scanned input image of cursive handwritten text on a sticky note. In OpenCV, write algorithms to process the image using morphological operations (dilation, erosion, opening, and closing).

Next, write a 2-3 page (it can be more than 3 pages if needed) summary of your observed results. Include in your summary, the following:

1. Describe in detail what enhancements did each morphological operation make on the image and how beneficial these enhancements are for handwriting recognition.
2. Did the enhancement also result in data loss of other features? Explain.
3. Research morphological operations for handwriting enhancements and include whether your results were similar with the findings in these. Be sure to cite them in your summary using correct APA styling.

**Submission Guidelines**

- Your submission should be one executable Python script and one summary of 2-3 pages in length.
- Include at least two scholarly references in addition to the course textbook. The textbook is Dey, S. (2025). Image processing and computer vision masterclass with Python: Learn advanced image processing techniques, computer vision fundamentals, and applications (2nd ed.). BPB Publications.
- All references must be cited in the text and listed on the references page, in APA 7 format.

**Critical Thinking Assignment Deliverables**

1. A single Word document

* Identify your assignment choice in the title page
    * Screenshots of resulting images and terminal output in an Appendix section. 
    * 2-3 pages in length (the paper can be more than 3 pages if necessary) to explain your Python program in a single Word document Note you can embed or attach images or/and diagrams if any were produced by your program, the Appendix will only hold the terminal output sections, including all images output by the matplotlib library
    * Include at least two scholarly references in addition to the course textbook
    * APA 7 format

2. A single Python code file.

---

## Program Requirements

Python 3.12 or later, OpenCV, NumPy, and Matplotlib. The program was checked with Python 3.12.13, OpenCV 4.13.0 (`opencv-contrib-python==4.13.0.92`), NumPy 2.5.3, and Matplotlib 3.11.2. The included [requirements.txt](requirements.txt) pins these three packages. The script also uses the Python standard library and does not need an OCR engine.

The `cv2` import is provided by `opencv-contrib-python`, which includes OpenCV's main modules. Install only one OpenCV distribution in the selected Python environment. A desktop display and working Matplotlib GUI backend are needed for interactive windows; `--no-show` saves results without opening windows.

---

## The Program

The supplied scan contains a yellow handwritten service note on top of a printed form. The program uses the four visible note corners to separate and straighten the note. A 12-pixel border is trimmed, producing a 769 x 772-pixel image. These coordinates are specific to `org_images/sticky_note.png`; this is not an automatic document detector.

Images - Original and Outputs:  
<img width="599" height="484" alt="image" src="https://github.com/user-attachments/assets/32c404aa-5975-4b3c-8778-b630961319f2" />

Grayscale conversion gives each pixel one brightness value. Inverse Otsu thresholding then separates dark writing from the lighter paper. The selected threshold is 162. The array used for morphology contains white handwriting, with a value of 255, on black background, with a value of 0. The original scan is not changed, and no artificial noise is added.

Dilation, erosion, opening, and closing all start from this same binary image. Each operation uses a 3 x 3 elliptical structuring element and one iteration. At this size, OpenCV's ellipse contains five active positions:

```text
0 1 0
1 1 1
0 1 0
```

Dilation expands the foreground. Erosion reduces it. Opening performs erosion followed by dilation, while closing performs dilation followed by erosion. The four comparisons are independent; the program does not pass the result of one comparison into the next.

### Observed Results

| Operation | Foreground pixels | Added | Removed | Change from input | Connected regions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Binary input | 35,968 | 0 | 0 | 0.00% | 87 |
| Dilation | 48,006 | 12,038 | 0 | +33.47% | 82 |
| Erosion | 24,162 | 0 | 11,806 | -32.82% | 83 |
| Opening | 35,672 | 0 | 296 | -0.82% | 81 |
| Closing | 36,250 | 282 | 0 | +0.78% | 86 |

A connected region is a group of foreground pixels linked horizontally, vertically, or diagonally. It can contain several letters or only a small mark. These counts describe the image; they are not character counts or recognition scores.

Dilation makes the writing heavier but also joins some nearby letters and enlarges small background marks. Erosion removes small marks and thins the writing, but it breaks the thin connection near the curved stroke in the model label. Opening removes three tiny isolated marks in the upper-right background while retaining most of the original stroke shape. Closing changes fewer pixels than opening, but it joins the S and e in Set. That separation exists in the input, so filling it is not evidence that damaged handwriting was repaired.

For this note, opening gives the most useful small-mark cleanup among the four operations. Most improvement in background contrast comes from thresholding before morphology. A handwriting recognizer was not evaluated, and the script does not claim an increase in OCR accuracy. The Word document compares these observations with the course textbook and two scholarly studies.

### Saved Images and Teaching Views

All results are saved before the terminal walkthrough begins. The six numbered steps explain preparation, dilation, erosion, opening, closing, and the full comparison. The final step also includes close-ups of the thin stroke and the space between S and e.

The displayed binary and morphology images and their saved PNGs show white handwriting (255) on a black background (0), matching the arrays used for the calculations. No display inversion is applied. `binary.png` and `binary_foreground.png` contain the same binary input, also retained in `morphology_arrays.npz`.

The eight labeled Matplotlib views are in `mod_images/figures/`. The individual full-resolution results, measurements, arrays, and complete terminal explanation are in `mod_images/`. These files are already included in this package. Running the script again replaces the generated files in the chosen output folder, not the original scan.

The Word explanation includes the discussion, references, and an appendix with screenshots. The individual image files are also included in `mod_images/`.

---

## How to Run the Program

Open a terminal in the folder containing `Module5_CTA_Option2.py`. Keep
`org_images/sticky_note.png` in its included subfolder. Install the dependencies
in your selected Python environment, then run the program:

```bash
python -m pip install -r requirements.txt
python Module5_CTA_Option2.py
```

If your Python 3 command is `python3`, use it in place of `python` in these commands.

On an interactive terminal with a working Matplotlib desktop backend, one image
window opens at a time. Type `C` to close the current view and open the next,
or `Q` to quit, then press Enter. Invalid commands prompt again. Step 6 shows
the full comparison, followed by the two close-ups, each after another `C`.
Only the final close-up accepts `Q` alone. All images, arrays, measurements,
and the complete explanation are saved before the first step, so quitting
leaves the full set of saved results available.

Closing a picture closes only that view; use the terminal to continue or quit.
`Q` closes the remaining figures and prints the result location. A normal
completion or `Q` returns exit status 0. **Ctrl+C** stops the program, closes
the figures, and returns status 130. An input/output or OpenCV failure is
reported in the terminal and returns status 1.

Terminal headings, explanations, tables, saved-file messages, and prompts use
color when the terminal supports it. Redirected output and the saved transcript
remain plain text. Setting `NO_COLOR=1` or `TERM=dumb` disables terminal colors.

To generate the complete results and explanation without opening windows or
waiting for input:

```bash
python Module5_CTA_Option2.py --no-show
```

For a windowed run without terminal pauses:

```bash
python Module5_CTA_Option2.py --no-pause
```

Close the Matplotlib windows to finish a `--no-pause` run. The display controls
change presentation only; each run calculates and saves the same four
morphological results and all eight teaching figures. `--no-show` prints all
six explanations without windows or C/Q prompts. `--no-pause` opens all eight
views and prints the explanations, then waits for the windows to close.

### Optional arguments

| Argument | Meaning | Default |
| --- | --- | --- |
| `--output-dir PATH` | Select the result folder. | Script-local `mod_images` |
| `--no-show` | Save all results and teaching figures, and print their explanations without windows or pauses. | Off |
| `--no-pause` | Show figures and print explanations without C/Q pauses. | Off |
| `--help` | Show command-line help. | — |

For example, keep another run separate from the included results:

```bash
python Module5_CTA_Option2.py --no-show --output-dir mod_images_separate_run
```

The input is always the supplied `org_images/sticky_note.png`. Default input
and output paths are resolved from the script, so the program can be launched
from another working directory when the interpreter and script paths are
specified correctly. An explicit relative `--output-dir` path is resolved from
the shell's current directory. Each run replaces the named generated files in
its selected output folder, including all eight PNGs in its `figures/`
subfolder. Select a different output folder to retain a separate run.

---

## Files Map

```text
CTA_Module-5/
├── Module5_CTA_Option2.py
├── Module5_CTA_Option2_Explanation.pdf
├── README.md
├── requirements.txt
├── mod_images/
│   ├── binary.png
│   ├── binary_foreground.png
│   ├── closing.png
│   ├── dilation.png
│   ├── erosion.png
│   ├── grayscale.png
│   ├── measurements.csv
│   ├── morphology_arrays.npz
│   ├── note_rectified.png
│   ├── opening.png
│   ├── terminal_output.txt
│   └── figures/
│       ├── 01_preparation.png
│       ├── 02_dilation.png
│       ├── 03_erosion.png
│       ├── 04_opening.png
│       ├── 05_closing.png
│       ├── 06_morphology_comparison.png
│       ├── 07_stroke_detail.png
│       └── 08_gap_detail.png
└── org_images/
    └── sticky_note.png
```

The supplied sticky-note scan is retained unchanged in `org_images/`. The Word document contains the research citations and references. The saved images, measurements, arrays, and terminal explanation are included in `mod_images/`.

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
 
