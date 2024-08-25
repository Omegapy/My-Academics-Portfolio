-----------------------------------------------------------------------------------------------------------------------------
# Module-2 Critical Thinking
Program Name: Sierpinski Gasket Vertex 2D

Grade:  

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

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 





