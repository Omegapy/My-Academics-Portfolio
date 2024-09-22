-----------------------------------------------------------------------------------------------------------------------------
# Module-6 Critical Thinking
Program Name: Interactive Recursively Approximated Sphere

<p align="left">
<img  src="https://github.com/user-attachments/assets/7a9e8c33-dc66-4970-851b-10a03b197252">
</p>

The following video demonstrates the animation of the Rotating Colored Cube: [Interactive Recursively Approximated Sphere](https://youtu.be/Rp3mV8I62QE)

-----------------------------------------------------------------------------------------------------------------------------

CSC405 – Graphics and Visualization - WebGL Course  
Professor: Dr Marquez   
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 09/22/2024   

-----------------------------------------------------------------------------------------------------------------------------


Requirements:  
- GLES 3
- WebGL 2 (JavaScript)
  
-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:  

Approximating a Sphere Recursively  
This week’s discussion has provided an introduction to Lightning and Shading, particularly with respect to reflection and Vector Computations. In this assignment, you will briefly discuss a sphere object (in one paragraph), which is used as an example curved surface to illustrate shading calculations. Then use the code snippet starting in section 6.6 to design an interactive approximated and recursively subdivided sphere, using WebGL. Finally, complete a two paragraph reflection on what you did and how it went.  

In your program:  

Include screenshots your working program  
Submit all the source files of your working program  
Submit a Word document with your discussion and reflection (approximately 3 paragraphs)    

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

This program displays an interactive 3D approximated sphere in WebGL.  
 The sphere is created by recursively subdividing a tetrahedron.  
 Users can control the sphere's radius, rotation (theta and phi angles), 
 and the number of subdivisions using sliders. The program also supports 
 pausing and resuming the rotation.  
 The Blinn-Phon model is implemented in the scene.  
 The model view with the light components are the one experiencing the rotation, not the sphere.  

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- interactiveSphere.html – contains Vertex Shader GLSL and Fragment Shader GLSL  
- interactiveSphere.js – contains JavaScript application logic  
- common folder – contains External Script for initializing shaders and performing matrix operations 
- Reflection Module 6 CT.doc – provides an overview and reflection on the program's functionality  
- Sphere Object Discuss Module 6 CT.doc – provides a brief discussion on a sphere object, which is used as an example curved surface to illustrate shading calculations  
- Screenshots – contains the 3d cube screenshots 
- README.md – Markdown file, program information  

-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 



