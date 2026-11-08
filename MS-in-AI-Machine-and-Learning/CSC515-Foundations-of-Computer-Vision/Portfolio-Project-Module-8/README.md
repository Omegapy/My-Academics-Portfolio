# Portfolio Project Module 8 - Option #2: Face Detection and Privacy

**Program:** [Module8_Portfolio_Option2.py](Module8_Portfolio_Option2.py)  
**Analysis:** [PDF Analysis](Module8_Portfolio_Option2_Analysis.pdf)

**Date:** 11/08/2026. 
**Grade:** Pending

---

## Overview

The goal of this project is to write algorithms for face detection and feature blurring. Select three color images from the web that meet the following requirements:

1. Two images containing human subjects facing primarily to the front and one image with a non-human subject.
2. At least one image of a human subject should contain that person's entire body.
3. At least one image should contain multiple human subjects.
4. At least one image should display a person's face far away.
5. All images should vary in light illumination and color intensity.

---

Foundations of Computer Vision CSC515   
Professor: Dr. Bingdong Li   
Fall C (26FC) – 2026   
Student: Alexander (Alex) Ricciardi  

---

## Assignment 

### Portfolio Project - Option #2: Face Detection and Privacy

To address privacy concerns you may want to use data anonymization. On images, this can be achieved by hiding features that could lead to a person or personal data identification, such as the person's facial features or a license plate number.

The goal of this project is to write algorithms for face detection and feature blurring. Select three color images from the web that meet the following requirements:

1. Two images containing human subjects facing primarily to the front and one image with a non-human subject.
2. At least one image of a human subject should contain that person's entire body.
3. At least one image should contain multiple human subjects.
4. At least one image should display a person's face far away.
5. All images should vary in light illumination and color intensity.

First, using the appropriate trained [cascade classifier](https://github.com/opencv/opencv/tree/4.x/data/haarcascades), write one algorithm to detect the human faces in the gray scaled versions of the original images. Put a red boundary box around the detected face in the image in order to see what region the classifier deemed as a human face. If expected results are not achieved on the unprocessed images, apply processing steps before implementing the classifier for optimal results.

After the faces have been successfully detected, you will want to process only the extracted faces before detecting and applying blurring to hide the eyes. Although the [eye classifier](https://github.com/opencv/opencv/tree/4.x/data/haarcascades) is fairly accurate, it is important that all faces are centered, rotated, and scaled so that the eyes are perfectly aligned. If expected results are not achieved, implement more image processing for optimal eye recognition. Now, apply a blurring method to blur the eyes out in the extracted image.

Inspect your results and write a summary describing the techniques you used to detect and blur the eyes out of human faces in images. Reflect on the challenges you faced and how you overcame these challenges. Furthermore, discuss in your summary, the accuracy of your results for all three images and techniques you used to improve the accuracy after each repeated experiment.

### Submission guidelines

- Your submission should be one executable Python script and one summary of 2-3 pages in length; note that it can be longer up to 5 pages.
- Your paper must be formatted according to APA 7 guidelines.

---

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![OpenCV 4.13.0](https://img.shields.io/badge/OpenCV-4.13.0-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![NumPy 2.5.3](https://img.shields.io/badge/NumPy-2.5.3-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib 3.11.2](https://img.shields.io/badge/Matplotlib-3.11.2-11557C?style=flat&logo=python&logoColor=white)](https://matplotlib.org/)

---

## Run the program

Keep `Module8_Portfolio_Option2.py` beside `org_images/`. All application logic is in that one Python file. The photographs, JSON records, CSV tables, and generated PNGs are supporting data, not additional scripts.

Open a terminal in the folder containing `Module8_Portfolio_Option2.py`. Install the dependencies, then run the program:

```bash
python -m pip install -r requirements.txt
python Module8_Portfolio_Option2.py
```

If your Python installation uses `python3`, substitute it for `python` in these commands.

To calculate and save the complete experiment without opening windows:

```bash
python Module8_Portfolio_Option2.py --no-show
```

Enter **C**, then Enter, to close a view and continue. Enter **Q**, then Enter, to quit. The last view accepts Q. Closing an intermediate window also continues; closing the last window finishes. `--no-pause` opens the views without waiting for terminal commands. `--output-dir` selects another output folder. `--input-dir` selects another folder containing the same three original files.

All results are saved before the first interactive view. Quitting does not discard the measurements or images. The default input and output folders are beside the script. Explicit relative `--input-dir` and `--output-dir` paths are relative to the terminal's current directory. An output directory cannot overlap the inputs. Repeated runs overwrite generated files with the same names in `mod_images/`; use `--output-dir another_results` to save a separate run. The original photographs are read only.

The program requires Python 3.12 or later and was checked with Python 3.12.13, OpenCV 4.13.0 (`opencv-contrib-python==4.13.0.92`), NumPy 2.5.3, and Matplotlib 3.11.2. These three library versions are pinned in [requirements.txt](requirements.txt). `cv2` is the import name provided by `opencv-contrib-python`; install only one OpenCV distribution in the environment you choose. Interactive views require a graphical Matplotlib backend. Use `--no-show` when no desktop display is available. The XML models are loaded from `cv2.data.haarcascades`, which comes with OpenCV. No GPU, network connection, scikit-image installation, or additional Python program is needed to run this package.

---

## What the script does

The first experiment detects face candidates on the original-resolution grayscale images without enhancement. The script retains six common experiments across all three images: the default face cascade, the alternate cascade at native resolution, the alternate cascade on an aspect-preserving 1,000-pixel maximum-edge input, global equalization, CLAHE, and a stricter grouping parameter. Returned face candidates are shown with red boxes, including incorrect candidates.

The selected configuration is `03_alt_scaled`. Boxes are mapped back to the original photographs, and clean face crops are extracted there. A provisional eye pair supplies a rotation angle, uniform scale, and translation. The face is transformed onto a 320 x 320 canvas with target eye centers at (96, 121.6) and (224, 121.6). The eye classifier runs again on that aligned face. Unsuccessful eye attempts remain in the output record.

The first eye search uses `haarcascade_eye.xml`. When a plausible pair is not found, the program tries equalization, `haarcascade_eye_tree_eyeglasses.xml`, and bounded split-region searches. The split searches also change search-scale spacing and grouping support; their effect is not attributed to the region alone. No missing eye is replaced with a manually supplied coordinate.

A Gaussian blur is applied within padded eye regions. The initial comparison uses a 35% margin and sigma equal to 10% of eye-box size. The final version uses a 60% margin and sigma equal to 45% of eye-box size, with a two-pixel minimum sigma. Both padding and strength change, so the comparison is not an isolated blur-strength experiment. The stronger treatment intentionally removes considerable detail inside the padded region.

An inverse transformation returns the treated pixels and their mask to the original scene. Pixels outside the mask are checked for exact equality with the original. The cat enters the same human-face detector. There is no condition that identifies its filename and forces zero detections or skips its results.

### Original Process and Final Output Images

<p><img width="550" height="202" alt="image" src="https://github.com/user-attachments/assets/b04a7b99-b08f-4539-8860-7c10a47fd5a0" /></p>
<p><img width="578" height="212" alt="image" src="https://github.com/user-attachments/assets/9d050bca-b76a-4c4e-ae7d-ddb71ee334a1" /></p>
<p><img width="928" height="338" alt="image" src="https://github.com/user-attachments/assets/a1dd7136-aee4-47b1-986e-6f0cdb7d4299" /></p>
<p><img width="574" height="594" alt="image" src="https://github.com/user-attachments/assets/765af173-b359-46d8-8a19-6411f0780f6a" /></p>

---

## Project map

The map lists the included files under the original assignment name. Additional generated files are described in the output table above.

```text
./ 
├── Module8_Portfolio_Option2.py               # Main - Python script.
├── Module8_Portforlio_Option2_Analysis.pdf    # Analysis of the program
├── README.md                                  # Project Documentation - this file
├── requirements.txt                           # Required packages to run the program
├── mod_images/                                # Modified - processed Images
│   ├── experiment_results.json
│   ├── eye_measurements.csv
│   ├── face_measurements.csv
│   ├── processing_summary.csv
│   ├── reference_annotations.json
│   ├── terminal_output.txt
│   ├── chelsea/                       
│   │   ├── final_eye_blurred.png
│   │   ├── final_treatment_mask.png
│   │   ├── initial_treatment_mask.png
│   │   ├── reference_annotations.png
│   │   └── selected_face_boxes.png
│   ├── eileen_collins/
│   │   ├── final_eye_blurred.png
│   │   ├── final_treatment_mask.png
│   │   ├── initial_treatment_mask.png
│   │   ├── reference_annotations.png
│   │   ├── selected_face_boxes.png
│   │   └── faces/
│   │       └── face_01/
│   │           ├── aligned_bgr.png
│   │           ├── blurred_bgr.png
│   │           ├── crop_bgr.png
│   │           ├── final_selected_eyes.png
│   │           ├── normalized_bgr.png
│   │           └── weak_blur_bgr.png
│   ├── figures/
│   │   ├── 01_originals.png
│   │   ├── 02_grayscale.png
│   │   ├── 03_initial_faces.png
│   │   ├── 04_reference_marks.png
│   │   ├── 05_comparison_chelsea.png
│   │   ├── 05_comparison_eileen_collins.png
│   │   ├── 05_comparison_sts133_arrival.png
│   │   ├── 06_extracted_faces.png
│   │   ├── 07_alignment.png
│   │   ├── 08_blur_strengths.png
│   │   ├── 09_privacy_scenes.png
│   │   └── 10_final_comparison.png
│   └── sts133_arrival/
│       ├── final_eye_blurred.png
│       ├── final_treatment_mask.png
│       ├── initial_treatment_mask.png
│       ├── reference_annotations.png
│       ├── selected_face_boxes.png
│       └── faces/
│           ├── face_01/
│           │   ├── aligned_bgr.png
│           │   ├── blurred_bgr.png
│           │   ├── crop_bgr.png
│           │   ├── final_selected_eyes.png
│           │   ├── normalized_bgr.png
│           │   └── weak_blur_bgr.png
│           ├── face_02/
│           │   ├── aligned_bgr.png
│           │   ├── blurred_bgr.png
│           │   ├── crop_bgr.png
│           │   ├── final_selected_eyes.png
│           │   ├── normalized_bgr.png
│           │   └── weak_blur_bgr.png
│           ├── face_03/
│           │   ├── aligned_bgr.png
│           │   ├── blurred_bgr.png
│           │   ├── crop_bgr.png
│           │   ├── final_selected_eyes.png
│           │   ├── normalized_bgr.png
│           │   └── weak_blur_bgr.png
│           ├── face_04/
│           │   ├── aligned_bgr.png
│           │   ├── blurred_bgr.png
│           │   ├── crop_bgr.png
│           │   ├── final_selected_eyes.png
│           │   ├── normalized_bgr.png
│           │   └── weak_blur_bgr.png
│           ├── face_05/
│           │   ├── aligned_bgr.png
│           │   ├── blurred_bgr.png
│           │   ├── crop_bgr.png
│           │   ├── final_selected_eyes.png
│           │   ├── normalized_bgr.png
│           │   └── weak_blur_bgr.png
│           └── face_06/
│               ├── aligned_bgr.png
│               ├── blurred_bgr.png
│               ├── crop_bgr.png
│               ├── final_selected_eyes.png
│               ├── normalized_bgr.png
│               └── weak_blur_bgr.png
└── org_images/                                           # Orignal Images
    ├── chelsea.png
    ├── eileen_collins.jpg
    └── sts133_arrival.jpg
```

---

## Photographs and requirements

| File | Dimensions | Assignment requirements |
| --- | --- | --- |
| `org_images/eileen_collins.jpg` | 2,615 x 3,269 | Primarily front-facing human portrait; close face; indoor lighting |
| `org_images/sts133_arrival.jpg` | 3,000 x 1,996 | Six primarily frontal people; full bodies including feet; small faces in a wide outdoor scene |
| `org_images/chelsea.png` | 451 x 300 | Cat with no people; nonhuman case with different colors and shading |

The photographs have not been cropped or recolored. Their source hashes are checked before processing. The wide group scene supplies the distant-face example through small apparent face size; the physical camera distance is unknown. Brightness differences are not a controlled lighting-only experiment because the scenes and subjects also differ.

### Image credits

- **Human portrait:** NASA, image S99-00858, October 30, 1998. The Commons record also credits Robert Markowitz. [NASA source](https://images.nasa.gov/details/S99-00858) and [Commons description and public-domain record](https://commons.wikimedia.org/wiki/File:Commander_Eileen_Collins_-_GPN-2000-001177.jpg).
- **Full-body group:** NASA/Kim Shiflett, image KSC-2011-1515, February 20, 2011. [NASA source](https://images.nasa.gov/details/KSC-2011-1515) and [Commons description and public-domain record](https://commons.wikimedia.org/wiki/File:STS-133_crew_arrival.jpg).
- **Cat:** Chelsea, photographed by Stefan van der Walt, CC0. [scikit-image source and attribution](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.chelsea). The PNG was acquired directly and is included; scikit-image is not a runtime dependency.

Source URLs, credits, dimensions, and SHA-256 values are embedded in the script's `SOURCES` constant and retained in [mod_images/experiment_results.json](mod_images/experiment_results.json). The credit links above provide the reuse records. NASA's [media guidance](https://www.nasa.gov/nasa-brand-center/images-and-media/) provides additional source-use context. Credits identify the supplied source records; the program does not identify people from their faces.

## Measurements and interpretation

The fixed visual reference set contains seven face boxes, fourteen eye centers, and fourteen visible eye regions, marked from the unchanged source photographs. They are approximate annotations for this small assignment, not expert-adjudicated labels. They are embedded in a clearly separated evaluation section of the single script. Detection, alignment, pair selection, and blurring do not read them.

Face boxes are matched one-to-one with intersection-over-union of at least 0.50. The script reports true positives, false positives, false negatives, precision, recall, and F1. Undefined values are saved as JSON null, blank CSV fields, and N/A in the terminal. In particular, face recall on the cat image is N/A because it has no reference human faces.

Eye-center localization uses a separate fixed rule: Euclidean error no greater than 10% of reference inter-eye distance, with a two-pixel minimum, measured in original-image pixels. This tests a window center against an approximate eye-opening center. It is stricter than asking whether the returned region overlaps an eye. The program also reports blur-mask coverage and independently measured residual eye-line tilt. A mathematically exact control-point transformation does not prove perfectly aligned actual eyes.

**Observed results are recorded in the implementation-results section below and in the included measurements.** These images were used to choose settings. Results are development-set measurements, not estimates for unseen faces. Eye blurring leaves other identifying details, including the rest of the face and clothing. It is not a guarantee of anonymization.

---

## Output files

`mod_images/` is generated automatically. A complete execution saves:

| Location | Contents |
| --- | --- |
| `figures/` | Twelve Matplotlib views covering seven teaching stages |
| `face_measurements.csv` | Eighteen rows: three images times six face experiments |
| `eye_measurements.csv` | Per-reference-face center errors, tolerance, alignment angles, attempts, and initial/final coverage |
| `processing_summary.csv` | Per-image face and eye results, changed pixels, and preservation checks |
| `experiment_results.json` | Runtime versions, XML hashes, settings, boxes, attempts, matrices, matching, references, and measurements |
| `reference_annotations.json` | The visual reference coordinates used for scoring |
| `terminal_output.txt` | The complete seven-stage explanation, with no terminal color codes |
| `<scene>/experiments/` | Each detector input and its red-box preview |
| `<scene>/faces/face_XX/` | Clean/normalized/aligned crops, candidate overlays, weaker/final blur, and masks |
| `<scene>/final_eye_blurred.png` | Clean original-size final photograph |
| `<scene>/final_treatment_mask.png` | Original-size binary mask used to reconstruct the final photograph |
| `<scene>/reference_annotations.png` | Original-size reference marks for review |

Face-box previews have a maximum edge of 1,000 pixels to avoid duplicating large photographs in every comparison. Their rectangles are retained at full precision in detector/original coordinates in JSON. The clean final privacy images remain at original resolution and use lossless PNG encoding.

The included results contain all twelve teaching figures, the three measurement tables, the experiment and reference JSON records, the teaching transcript, and each scene's final photograph, initial/final treatment masks, reference overlay, and selected-face preview. For the seven detected faces, they also include the original and normalized crops, aligned faces, initial/final blur, and selected-eye previews. Repeated full-scene experiment inputs, individual experiment previews, candidate-eye overlays, grayscale files, and intermediate face masks are recreated at runtime. The comparison figures and JSON retain the settings and findings from those experiments.

---

## Implementation results

Results from the included experiment records, aggregated across the three photographs:

| Face experiment | Correct faces | Extra boxes | Missed faces |
| --- | ---: | ---: | ---: |
| `01_default_native` | 7 | 9 | 0 |
| `02_alt_native` | 7 | 0 | 0 |
| `03_alt_scaled` | 7 | 0 | 0 |
| `04_alt_equalized` | 5 | 0 | 2 |
| `05_alt_clahe` | 7 | 0 | 0 |
| `06_alt_stricter` | 6 | 0 | 1 |

The selected configuration found all seven reference human faces with no extra boxes. It returned no human-face candidates for the cat. All seven detected human faces received eye treatment. The initial masks fully covered 12 of the 14 marked eye regions; the wider final masks covered all 14. All pixels outside the final treatment masks remained exactly unchanged, including the entire cat photograph.

The strict eye-center check passed **6 of 14 centers**, and both centers met that tolerance on **2 of 7 faces**. These localization errors remain in the results; they are not replaced with the stronger coverage score. Reference eye-line tilt after alignment ranged from approximately -1.77 to +2.05 degrees, so actual eye locations are not claimed to be perfectly horizontal.

The included experiment record reports Python 3.12.13, OpenCV 4.13.0, NumPy 2.5.3, and Matplotlib 3.11.2 on macOS. Each execution records its actual runtime versions and settings in `mod_images/experiment_results.json`. Timings can differ across machines and runs.

---

## Sources for the implementation

- [OpenCV 4.13.0: Cascade Classifier](https://docs.opencv.org/4.13.0/db/d28/tutorial_cascade_classifier.html)
- [OpenCV 4.13.0: Geometric Transformations](https://docs.opencv.org/4.13.0/da/d6e/tutorial_py_geometric_transformations.html)
- [OpenCV 4.13.0: Histogram Equalization and CLAHE](https://docs.opencv.org/4.13.0/d5/daf/tutorial_py_histogram_equalization.html)
- [OpenCV 4.13.0: Smoothing Images](https://docs.opencv.org/4.13.0/d4/d13/tutorial_py_filtering.html)

The course book reference is Dey, S. (2025), *Image processing and computer vision masterclass with Python: Learn advanced image processing techniques, computer vision fundamentals, and applications* (2nd ed.), BPB Publications. This implementation does not attribute its eye-alignment procedure to that classification chapter.

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
 


