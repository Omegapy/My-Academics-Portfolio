# Foundations of Computer Vision – CSC515 

---

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omega.py)      

Created date: 09/14/2026  

---

Project Description:    
This repository is a collection of assignments from CSC515 – Foundations of Computer Vision - CSU Global.  

**CSC515 - Foundations of Computer Vision**   

In this Graduate course, students will apply digital image construction and processing. Students will explore topics associated with image formation, image acquisition, and image geometry. Students will be exposed to the techniques required to efficiently analyze images for representation in applicable context scenarios. Students will also apply image processing techniques for filtering and edge detection for image deconstruction

**Course Learning Outcomes:**     

1. Using an image processing model, create an algorithm to solve a specific computer vision problem.
2. Describe and recognize 2D and 3D Shapes, understand transformations.
3. Manage image sizes, convert color images to grayscale images, augment and transform images.
4. Implement an application using appropriate image filters.
5. Compare various image segmentation techniques and understand morphology.
6. Select an appropriate edge detection method to identify edges and corners in an image.

---

Foundations of Computer Vision CSC515   
Professor: Dr. Binbong Li 
Fall C (26FC) – 2026   
Student: Alexander (Alex) Ricciardi   

Final grade: 

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
   
---

Requirements:  

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat\&logo=python\&logoColor=white)](https://www.python.org/downloads/)


---

#### Project Map  

- Critical Thinking Module 5
- Critical Thinking Module 4
- Portfolio Milestone Module 3
- Critical Thinking Module 2
- Portfolio Milestone Module 1
- Discussions

## Critical Thinking Module 5
Directory: [Critical-Thinking-Module-5](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC515-Foundations-of-Computer-Vision/Critical-Thinking-Module-5)   
Title: Morphology Operations for Handwritten Text Enhancement

---
---

**Assignment:**

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

2. A single Python code file.e.

---

**My Program Overview**

[The supplied scan contains a yellow handwritten service note on top of a printed form. The program uses the four visible note corners to separate and straighten the note. A 12-pixel border is trimmed, producing a 769 x 772-pixel image. These coordinates are specific to `org_images/sticky_note.png`; this is not an automatic document detector.

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

---

[Go back to the Project Map](#project-map)

---
---

## Critical Thinking Module 4
Directory: [Critical-Thinking-Module-4](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC515-Foundations-of-Computer-Vision/Critical-Thinking-Module-4)   
Title: Laplacian Filters for Different Kernel Windows

---
---

**Assignment:**

AOption #2: Laplacian Filters for Different Kernel Windows
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

---

**My Program Overview**

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

---

[Go back to the Project Map](#project-map)  

---
---

## Portfolio Milestone Module 3
Directory: [Portfolio-Milestone-Module-3](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC515-Foundations-of-Computer-Vision/Portfolio-Milestone-Module-3)   
Title: Blending Images in OpenCV

---
---

**Assignment:**

This assignment is the second milestone of a broader portfolio project.  

The broader portfolio project that I chose to do is:  

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

**This Portfolio Milestone assignment:**

It is time to think more about your upcoming Portfolio Project. In face and object detection, it is often useful to create a new image by combining two images together. Perhaps you would like to remove a tattoo or create a [deepfake](https://www.proofpoint.com/us/threat-reference/deepfake).

Use a camera to take a picture of yourself facing the frontal. Using an image from the web, create a deepfake by replacing someone else’s likeness with yourself.

---

**My Program**
`Module3_Portfolio_Option2.py` places the face from `org_images/Alex.png` into
`org_images/the_rock.png`. It completes the two-image blending milestone described
above. The three-image face-detection and eye-blurring work belongs to the later
portfolio project.

Image Results:  
<img width="368" height="247" alt="image" src="https://github.com/user-attachments/assets/fb476f29-bd91-46e4-bb3d-575b023bd422" />

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

---

[Go back to the Project Map](#project-map)  


---
---

## Critical Thinking Module 2
Directory: [Critical-Thinking-Module-2](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC515-Foundations-of-Computer-Vision/Critical-Thinking-Module-2)   
Title: Color channel extraction, reconstruction, and red/green swapping

---
---

**Assignment:**

After completing the Required Reading, you should have a good idea of how to use OpenCV for multi-scale representation of images by pixels matrices. Select and take a look at one of the following images:

Image of a Puppy: puppy.jpg
Image of a kitten: kitty.jpg

As both are colored images, each image has three channels, corresponding to the primary colors of red, green, and blue.

Import your selected image (using the link) into OpenCV and write code to extract each of these channels separately to create 2D images. This means that from the n x n x 3 shaped image, you will get 3 matrices of the shape n x n.
Now, write code to merge all these images back into a colored 3D image.
What will the image look like if you exchange the reds with the greens? Write code to merge the 2D images created in step 1 back together, this time swapping out the red channel with the green channel (GRB).
Be sure to display the resulting images for each step. Your submission should be one executable Python file.

---

**My Program Overview**

The program uses the puppy org_images/puppy.jpg to perform color transformation using OPenCV
The program separates Blue, Green, and Red (BGR) color values of the image and creates
another image by swapping the red and green values. 
- Blue → stays Blue
- Green → moves into the Red position
- Red → moves into the Green position

<img width="771" height="203" alt="image" src="https://github.com/user-attachments/assets/e15e3124-ba6c-4185-b440-ca8834a80d8c" />

---

[Go back to the Project Map](#project-map)  

---
---

## Portfolio Milestone Module 1
Directory: [Portfolio-Milestone-Module-1](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC515-Foundations-of-Computer-Vision/Portfolio-Milestone-Module-1)   
Title: Face Detection and Privacy - OpenCV image loading, display, and saving

---
---

**Assignment:**

This assignment is the first milestone of a broader portfolio project.  

The broader portfolio project that I chose to do is:  

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

**This Portfolio Milestone assignment:**

It is time to begin thinking about your Portfolio Project.  In order to complete the Portfolio Project, OpenCV will need to be installed and working properly on your desktop. 

OpenCV (Open-Source Computer Vision Library) is an open-source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in commercial products.

For this milestone assignment, install OpenCV based on your specific operating system.  Then, use OpenCV to complete the following:

1. Write Python code to import one of the following images:
        - brain image
        - numbers image

2. Write Python code to display the image.  

3. Write Python code to write a copy of the image to any directory on your desktop.

---

**My Program**

The program loads org_images/brain_image.jpg, displays it, and saves mod_images/brain_image.png using OpenCV.

OpenCV loads/decodes the JPG into a 3D NumPy array of shape (height, width, 3).
The 3 values correspond to each pixel color's value in BGR (blue, green, red).
The image matrix can be indexed as image[row, column] = [BLUE, GREEN, RED].
[0] = blue, [1] = green, [2] = red
The red, green, and blue color values are stored as unsigned 8-bit integers (uint8), 
which correspond to RGB color values from 0 to 255.


---

[Go back to the Project Map](#project-map)  

----
----

## Discussions 
This repository is a collection of discussion posts from CSC506 – Design and Analysis of Algorithms  
Directory: [Discussions](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC515-Foundations-of-Computer-Vision/Discussions)

---

[Go back to the Project Map](#project-map)


