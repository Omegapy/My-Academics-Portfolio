-----------------------------------------------------------------------------------------------------------------------------
# Module-4 Critical Thinking
Program Name: Rotating 3D Cube

Grade:  105/105 A

<p align="left">
<img  src="https://github.com/user-attachments/assets/705d0aaa-7ced-47b5-bd99-e6dcc5064dad">
</p>

The following video demonstrates the animation of the Rotating Colored Cube: [3D Rotating Cube](https://www.youtube.com/watch?v=peIjP2O0FTU)

-----------------------------------------------------------------------------------------------------------------------------

CSC405 – Graphics and Visualization - WebGL Course  
Professor: Dr Marquez   
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 09/08/2024   

-----------------------------------------------------------------------------------------------------------------------------


Requirements:  
- GLES 3
- WebGL 2 (JavaScript)
  
-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:  

Critical Thinking Assignment (105 Points)  
Colored Cube  
Familiarize yourself with the concepts of vertices, shaders, buffers, and transformations in WebGL/OpenGL. Understand how vertices define the shape of an object, shaders control the appearance, buffers hold data, and transformations position and orient objects.  

Create a WebGL/OpenGL Program that produces a Colored Cube. Write the vertex and fragment shaders. The vertex shader should handle the vertex positions and transformations, while the fragment shader should define the colors.  

Set up a render loop that continuously updates and redraws the scene. Inside the loop, apply transformations, update uniform values, and issue draw calls. Inside the render loop, issue draw calls to render the cube. Ensure the shaders are correctly receiving vertex and color data.  

Run the program and observe the colored cube on the screen. Debug any issues that may arise, such as incorrect transformations or shader errors.  

Document the steps you took to create the colored cube. Explain the role of shaders, buffers, and transformations in achieving the final result. Reflect on what you've learned through this exercise. This should be approximately 3 paragraphs in length.  

In your submission:  

Include screenshots your working program  
Submit all the source files of your working program  
Submit a Word document with the documentation and reflection  

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

This program creates a simple rotating colored 3D cube using WebGL.   
The user can rotate the cube along the X, Y, and Z axes and move it up, down, left, and right.  
The user can also pause and restart the rotation while still moving the cube.   
This program visits the concepts of transformation in computer graphics, more specifically quaternion rotation and translation.  

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- cube.html – contains Vertex Shader GLSL and Fragment Shader GLSL  
- cube.js – contains JavaScript application logic  
- common folder – contains External Script for initializing shaders and performing matrix operations 
- Reflection Module 4 CT – provides an overview and reflection on the program's functionality, including testing scenarios and output screenshots.
- Screenshots – contains the 3d cube screenshots 
- README.md – Markdown file, program information  

-----------------------------------------------------------------------------------------------------------------------------

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





