-----------------------------------------------------------------------------------------------------------------------------
# Module-2 Critical Thinking
Program Name: Sierpinski Gasket Vertex 2D

Grade:  103/105 A

<p align="left">
<img  src="https://github.com/user-attachments/assets/0580aefe-6c5b-4f8d-967a-f101b18307db">
</p>

-----------------------------------------------------------------------------------------------------------------------------

CSC405 – Graphics and Visualization - WebGL Course  
Professor: Dr Marquez   
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 08/25/2024   

-----------------------------------------------------------------------------------------------------------------------------


Requirements:  
- GLES 3
- WebGL 2 (JavaScript)
  
-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:  

Critical Thinking Assignment (105 Points)
Sierpinski Gasket
Ensure you have a working WebGL or OpenGL setup. If you haven't already, install any necessary tools, libraries, or frameworks required to run either program. Understand how the Sierpinski Gasket is generated using WebGL/OpenGL. Pay close attention to how primitives and attributes are utilized in the code. 

Check out these two resources for information:  
https://www.cse.unr.edu/~fredh/class/480/text-icg-2ed/Chap-02/ch-02-6up.pdfL  
http://web.cse.ohio-state.edu/~machiraju.1/teaching/CSE5542/Lectures/pdf/cse5542-machiraju-week-3.pdf  

Create a simple WebGL/OpenGL program that renders the Sierpinski Gasket using a vertex shader and a fragment shader.

As you witness the Sierpinski Gasket being rendered, what do you observe? How do the primitives and attributes influence the final output? What patterns emerge as the gasket is generated? How does changing attributes affect the appearance of the fractal?

In your submission include the following:

Your code
Screen images of your image being rendered
2-3 paragraph reflection

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

The program is a very simple WebGL application that generates and displays a 2D animation of the Sierpinski Gasket being rendered.   
pPosition uses points to generate the fractal.  
tPosition uses triangles to generate the fractal.  

To render Points  
- in gasket.js    
    • comment out "gl.drawArrays(gl.POINTS, 0, currentVertex);" and comment "gl.drawArrays(gl.TRIANGLES, 0, currentVertex);"    
    • comment out "initPoints(initVertices);" and comment below "initTriangles(initVertices[0], initVertices[1], initVertices[2], numTimesToSubdivide);"  
- in gasket.js   
    • comment out "vec4 aPosition = pPosition;" and comment "vec4 aPosition = tPosition;"

To render Triangles  
- in gasket.js comment  
    • comment out "gl.drawArrays(gl.TRIANGLES, 0, currentVertex);" and comment "gl.drawArrays(gl.POINTS, 0, currentVertex);"  
    • out "gl.drawArrays(gl.TRIANGLES, 0, currentVertex);" and comment "gl.drawArrays(gl.POINTS, 0, currentVertex);"  
- in gasket.js  
    • comment out "vec4 aPosition = tPosition;" and comment "vec4 aPosition = pPosition;"

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- gasket.html – contains Vertex Shader GLSL and Fragment Shader GLSL  
- gasket.js – contains JavaScript application logic  
- common folder – contains External Script for initializing shaders and performing matrix operations 
- Reflection Module 2 CT – provides an overview and reflection on the program's functionality, including testing scenarios and output screenshots.
- Screenshots – contains the fractal rendering screenshots 
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





