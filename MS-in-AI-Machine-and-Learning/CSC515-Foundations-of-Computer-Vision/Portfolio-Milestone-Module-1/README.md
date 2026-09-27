# Portfolio Milestone Module 1 - Option #2: Face Detection and Privacy
Project: Face Detection and Privacy - OpenCV image loading, display, and saving

Data:  09/20/2026  
Grade: 100% | A

---

Foundations of Computer Vision CSC515   
Professor: Dr. Binbong Li   
Fall C (26FC) – 2026     
Student: Alexander (Alex) Ricciardi    

---

## Assignment 

This assignment is the first milestone of a broader portfolio project.  

The broader portfolio project tha i choose to do is:  

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

### This Portfolio Milestone asignment:

It is time to begin thinking about your Portfolio Project.  In order to complete the Portfolio Project, OpenCV will need to be installed and working properly on your desktop. 

OpenCV (Open-Source Computer Vision Library) is an open-source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in commercial products.

For this milestone assignment, install OpenCV based on your specific operating system.  Then, use OpenCV to complete the following:

1. Write Python code to import one of the following images:
        - brain image
        - numbers image

2. Write Python code to display the image.  

3. Write Python code to write a copy of the image to any directory on your desktop.

**Submission Guidelines**

- Submission title: **Portfolio Milestone Module 1 - Option #2: Face Detection and Privacy**.
- Submit one executable Python file: [Module1_Portfolio_Option2.py](Module1_Portfolio_Option2.py).
- Include the selected option and instructions for running the code in the file
  header, as clarified by the professor. The script header includes both.
- The professor also permits a Word document with run instructions and screenshots;
  this project uses the executable Python file submission.
- Refer to the rubric below for more details about how you will be graded for this assignment.

---

## Program Requirements

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![OpenCV 4.13.0](https://img.shields.io/badge/OpenCV-4.13.0-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![NumPy 2.5.3](https://img.shields.io/badge/NumPy-2.5.3-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)

---

## The program

The program loads org_images/brain_image.jpg, displays it, and saves mod_images/brain_image.png using OpenCV.

OpenCV loads/decodes the JPG into a 3D NumPy array of shape (height, width, 3).
The 3 values correspond to each pixel color's value in BGR (blue, green, red).
The image matrix can be indexed as image[row, column] = [BLUE, GREEN, RED].
[0] = blue, [1] = green, [2] = red
The red, green, and blue color values are stored as unsigned 8-bit integers (uint8), 
which corresponds to RGB color values from 0 to 255.

Example:
```python
    image = [
            [[255, 0, 0], [0, 255, 0], ...],  # Row 0: blue pixel, green pixel, ... (number of columns - pixel width)
            [[0, 0, 255], [255, 255, 255], ...],  # Row 1: red pixel, white pixel, ... (number of columns - pixel width)
            ... (number of rows - height)
        ]
```

Then the program displays the image in a window. Click the image window and
press any key to continue. The program closes the window and saves the image
as `mod_images/brain_image.png`.

---

### Launch the program

Open a terminal in the folder containing
[Module1_Portfolio_Option2.py](Module1_Portfolio_Option2.py). Install the required
libraries:

```bash
python -m pip install -r requirements.txt
```

Run the program from that same folder:

```bash
python Module1_Portfolio_Option2.py
```

---

**Project Map:**

./
```text
Portfolio-Milestone-Module-1-Option-2/
├── README.md                                       # Project documentation
├── Module1_Portfolio_Option2.py                    # The program
├── Portfolio Module-1_Option-2_Screenshots.pdf     # Terminal output screenshots
├── requirements.txt                                # Required packages
├── org_images/
│   └── brain_image.jpg                             # Original course image
└── mod_images/
    └── brain_image.png                             # Modified course image
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
