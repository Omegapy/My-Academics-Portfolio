# Foundations of Computer Vision – CSC515 

---

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omega.py)      

Created date: 09/14/2026  

---

Project Description:    
This repository is a collection of assignments from CSC525 – Foundations of Computer Vision - CSU Global.  

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
[![TensorFlow 2.21.0](https://img.shields.io/badge/TensorFlow-2.21.0-FF6F00?style=flat\&logo=tensorflow\&logoColor=white)](https://www.tensorflow.org/)
[![PyTorch 2.13.0](https://img.shields.io/badge/PyTorch-2.13.0-EE4C2C?style=flat\&logo=pytorch\&logoColor=white)](https://pytorch.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat\&logo=numpy\&logoColor=white)](https://numpy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat\&logo=pandas\&logoColor=white)](https://pandas.pydata.org/)

---

#### Project Map  

- Critical Thinking Module 2
- Portfolio Milestone Module 3
- Discussions

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


