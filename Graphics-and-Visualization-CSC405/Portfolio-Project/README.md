-----------------------------------------------------------------------------------------------------------------------------
# Portfolio Project
Program Name: Rotating Cube

<p align="left">
<img  src="https://github.com/user-attachments/assets/6baed473-9a62-4fd4-8cd8-703249e82ae2">
</p>

The following video demonstrates the functionality of the program: []()

-----------------------------------------------------------------------------------------------------------------------------

CSC405 – Graphics and Visualization - WebGL Course  
Professor: Dr Marquez   
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 10/06/2024   

-----------------------------------------------------------------------------------------------------------------------------


Requirements:  
- GLES 3
- WebGL 2 (JavaScript)
  
-----------------------------------------------------------------------------------------------------------------------------

Assignment:  

Portfolio Project  
There are three parts to the portfolio project.  

Updates to Milestone from Module 5:  
Based on instructor feedback, please provide updates to your interactive viewer activity from Module 5. Additionally, implement advanced interactivity features. For example, allow users to select and highlight parts of a complex object, switch between visualizations, or toggle between shaders. You will compile the updated source files with screenshots with your final project submission.  

Lessons Learned Reflection:  
Write a two-page summary that discusses the lessons you learned in this course. Reflect on how these lessons can be applied to a real-world problem or a specific real application. How will you use the concepts in this course going forward?  

Final Program (Hidden-Surface Removal Problem):  
Study the Hidden-Surface Removal problem and implement the Painter’s algorithm using WebGL. Provide one paragraph discussing what the Hidden-Surface Removal problem within your lessons learned reflection document.  

Clearly provide the details of your program (provide a 2-paragraph overview), including the screenshots of your working program. Describe the object (primitive) that you are working with. Don’t forget to adequately comment your source code.  

Assemble all of the requirements for this project and submit to Canvas for grading by the due date. As a reminder, there are no late submissions for Module 8, as everything must be submitted by the last day of the term.   

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

Program Version-1:  
[Module-5 Portfolio Milestone](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Module-5-Portfolio-Milestone)  
This program displays a 3D rotating cube in WebGL and implements an interactive viewer with orthographic projection.  
Users can rotate the cube along the X, Y, and Z axes, stop the rotation, and reset all parameters using buttons.  
Additionally, the users can resize the cube using a slider.  
Furthermore, the users can control the interactive viewer depth, radius, theta angle, and phi angle with sliders.  

Program Version-2: [Portfolio-Milestone](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Portfolio-Project/Portfolio-Milestone)   
This program is version 2 of the [Module-5 Portfolio Milestone](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Module-5-Portfolio-Milestone)  
It displays a 3D rotating cube in WebGL.  
It implements an interactive viewer that can be toggled between orthographic and perspective projections.  
It also implements an interactive Blinn-Phong lighting that can be toggled between on and off state.     
Users can rotate the cube along the X, Y, and Z axes, stop the rotation, 
and reset all parameters using buttons. Additionally, users can resize the cube using a slider.  

Program Final Version-3 - Rotating Cube:  
This program is version 3 of  
- [Module-5 Portfolio Milestone](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Module-5-Portfolio-Milestone)  
- and [Portfolio Milestone version 2](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Portfolio-Project/Portfolio-Milestone)   

This program displays a 3D rotating cube in WebGL.  
It implements an interactive viewer that can be toggled between orthographic and perspective projections.  
It also implements an interactive Blinn-Phong lighting that can be toggled between on and off state.  
The program implements the Painter's Algorithm for hidden surface removal.  
Users can rotate the cube along the X, Y, and Z axes, stop the rotation, and reset all parameters using buttons. Additionally, users can resize the cube using a slider.  

The program also implements the Painter's Algorithm for Hidden Surface Removal (HSR).   
The Painter's Algorithm manually sorts the cube’s faces to simulate depth without relying on the WebGL z-buffer to remove hidden surfaces.

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- rotatingCube.html – contains Program Final Version 3 Vertex Shader GLSL and Fragment Shader GLSL  
- rotatingCube.js – Program Final Version 3 contains JavaScript application logic  
- common folder – contains External Script for initializing shaders and performing matrix operations 
- Reflection Portfolio Project.doc – provides an overview and reflection on the program's functionality, as well as a discussion about the Hidden-Surface Removal problem   
- Screenshots – contains the 3D cube screenshots 
- Portfolio-Milestone - contains the Program Version 2 files   
- Lessons Learned Reflection.doc – Essay about the lessons in CSC405 – Graphics and Visualization - WebGL Course    
- README.md – Markdown file, program information  

-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 



