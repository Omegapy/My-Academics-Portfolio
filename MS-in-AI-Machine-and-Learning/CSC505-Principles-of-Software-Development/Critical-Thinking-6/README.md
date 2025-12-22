# Critical Thinking 6
Program Name: Critical Thinking Assignment 6 – Root Solver

Data:  12/21/2025  
Grade: 

---

CSC505 Principal of Software Development – Python Programming   
Professor: Dr. Joseph Issa  
Winter A (25WA) – 2025   
Student: Alexander (Alex) Ricciardi

---

**Program Description:**

Part of Assignement Step 3: Write Your Python Implementation
  - Translate your lowest-level refined design into working Python code.
    - Use functions or classes to reflect the structure of your stepwise breakdown.
    - Keep your code modular and clearly commented.
    - The final script should demonstrate correct functionality for your selected problem.

Root Solver is a small python script that solves for the roots of a transcendental equation (e.g., using Newton-Raphson or bisection method for equations like cos(x) - x = 0).

---

Requirements:  
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

---

**Assignment Directions:**  

In modern software engineering, stepwise refinement (also known as top-down design) is a key strategy for breaking down complex problems into manageable parts. In this assignment, you will apply this approach to one of three program options and demonstrate your ability to define and refine procedural abstractions across multiple levels.

Instructions:  
- Step 1: Select Your Problem Domain
  - Choose one of the following program types to develop (choose the problem that most aligns with your interests or background):
    - Check Writer: Convert a numeric dollar amount into written words (e.g., 123.45 → "One hundred twenty-three dollars and forty-five cents").
    - Root Solver: Solve for the roots of a transcendental equation (e.g., using Newton-Raphson or bisection method for equations like cos(x) - x = 0).
    - Task Scheduler: Implement a basic task scheduling algorithm (e.g., First-Come-First-Serve or Round-Robin) to simulate how an operating system schedules tasks.
- Step 2: Apply Stepwise Refinement
  - Break your solution into three levels of procedural abstraction:
    - High-level overview of the system in plain language (e.g., "Convert number to words in proper check-writing format.")
    - Mid-level refinement, where major functions and logic blocks are outlined (e.g., “Split dollars and cents,” “Convert three-digit numbers,” “Assemble output.”)
    - Low-level refinement, showing the individual steps or functions to be implemented (e.g., “Convert hundreds place,” “Handle rounding,” “Add ‘and’ between sections.”)
  - Use a UML Activity Diagram or hierarchical structure chart to visually represent the breakdown across refinement levels.
  - Tools: Use one of the following for diagrams:
  - UMLetLinks to an external site.
  - GliffyLinks to an external site.
  - Microsoft Visio (if available)
- Step 3: Write Your Python Implementation
  - Translate your lowest-level refined design into working Python code.
    - Use functions or classes to reflect the structure of your stepwise breakdown.
    - Keep your code modular and clearly commented.
    - The final script should demonstrate correct functionality for your selected problem.
- Step 4: Submit Your Work
  - Submit all of the following in a zipped folder:
    - Your Python script (.py)
    - A screenshot of your script running successfully with example input/output
    - Your UML diagram(s) in .png or .pdf format
    - (Optional) A brief README.txt file that outlines your design logic and any assumptions made.
  - References:
    - Include at least two credible references beyond the course textbook. These can include:
      - Python documentation
      - Articles on procedural abstraction or top-down design
      - Research papers or tutorials related to your selected program

The CSU Global Library (available in the left hand navigation menu) is a great place to find these references.  
All references should be APA 7 format according to the CSU Global Writing Center.
 
---

UML Activity Diagram

<img width="1591" height="2560" alt="Root Solver Activity Diagram" src="https://github.com/user-attachments/assets/ae495c6a-343f-4cd0-b5c4-852cc1a55124" />
 
---

**Articles and tutorials used**
 
- Encyclopaedia Britannica’s entry on Transcendental function was used to learn/support the written definition/background for transcendental equations in the program documentation (EncyclopaediaBritannica, 2025).
- MIT OpenCourseWare’s Nonlinear equations notes were used to leran/support the numerical method.descriptions and stopping conditions for bisection and Newton-Raphson in the design narrative (MIT OpenCourseWare, 2012).
- OpenStax’s discussion of the Intermediate Value Theorem was used to help/learn/support/justify the bisection precondition requiring a sign change on ([a,b]) (Gilbert & Herman, 2016).
- Python’s official `math` module documentation was used to leran ho to use math functions/constants and to check the allowed-expression whitelist (Python Software Foundation, n.d.).
- IBM Documentation on activity diagrams and control nodes was used to learn about activity-diagram concepts (decisions, merges, loops) for the assignment diagrams (IBM, n.d.; IBM, n.d.).
- The OMG UML 2.5.1 specification was used as a notation reference for UML activity-diagram elements (Object Management Group, 2017).
- Pressman & Maxim (2020) [Textbook] and Wirth (1971) were used to learr about the stepwise refinement (top-down design) (Pressman & Maxim, 2020; Wirth, 1971).
- University of Malta’s structure chart reference was used to learn about the hierarchical structure chart terminology and decomposition approach (University of Malta, n.d.).
- SciPy’s documentation for `optimize.newton` and `optimize.root_scalar` was used learn about what the expected solver behavior and terminology should be (SciPy Developers, n.d.; SciPy Developers, n.d.).
- Weisstein’s Transcendental equation entry was used as an additional reference for terminology and examples in the documentation (Weisstein, n.d.).
- Ricciardi’s UML activity diagrams and multithreading concepts article was used as a template/reference tp creat the UML activity diagrams (Ricciardi, 2025).

---

**References**: 

Encyclopaedia Britannica. (2025, December 12). *Transcendental function*. Encyclopaedia Britannica. https://www.britannica.com/science/transcendental-function

IBM. (n.d.). *Activity diagrams*. IBM Documentation. https://www.ibm.com/docs/en/rational-soft-arch/9.6.1?topic=diagrams-activity

IBM. (n.d.). *Control nodes in activity diagrams*. IBM Documentation. https://www.ibm.com/docs/en/dma?topic=diagrams-control-nodes

MIT OpenCourseWare. (2012). Chapter 4: Nonlinear equations (18.330 Introduction to Numerical Analysis) [PDF]. MIT. https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/5b325bfa56a599794c7196de926844b0_MIT18_330S12_Chapter4.pdf

Object Management Group. (2017). *Unified Modeling Language (UML)® specification (Version 2.5.1)*. OMG. https://www.omg.org/spec/UML/2.5.1/About-UML

Gilbert, S., and Herman, E. (2016). 2.4 Continuity: The Intermediate Value Theorem. In Calculus, Volume 1. OpenStax. https://openstax.org/books/calculus-volume-1/pages/2-4-continuity

Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A practitioner’s approach (9th ed.). McGraw Hill Education.

Python Software Foundation. (n.d.). *math — Mathematical functions. Python 3 documentation*. Python.org.  https://docs.python.org/3/library/math.html

Ricciardi, A. (2025, January 18). *UML activity diagrams and multithreading concepts*. Omega.py. https://www.alexomegapy.com/post/uml-activity-diagrams-and-multithreading-concepts

SciPy Developers. (n.d.). *scipy.optimize.newton*. SciPy documentation. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html

SciPy Developers. (n.d.). *scipy.optimize.root_scalar*. SciPy documentation https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html

University of Malta. (n.d.). Structure Charts: Elements and Definitions [PDF]. UM. https://staff.um.edu.mt/ecac1/files/sc_definitions.pdf

Weisstein, E. W. (n.d.). *Transcendental equation*. In MathWorld—A Wolfram Web Resource. https://mathworld.wolfram.com/TranscendentalEquation.html

Wirth, N. (1971). Program Development by Stepwise Refinement. Communications of the ACM, 14(4), 221–227. https://doi.org/10.1145/362575.362577

---

**Assumptions**

- The user inputs an equation as a single expression in terms of `x` (for example, `cos(x)-x`).
- The equation uses only the supported operators and math functions/constants  within a  program’s safe-expression whitelist (e.g., `+ - * / **`, `sin`, `cos`, `exp`, `log`, `sqrt`, `abs`, `pi`, `e`, `pow`).
- The program needs to solve for real-valued roots only (no complex roots).
- For the bisection method, the user needs t o provide an interval ([a, b]) where the function is continuous and a sign change exists (`f(a) * f(b) < 0`).
- For the Newton-Raphson** method, the user provides a reasonable initial guess `x0`; convergence is not guaranteed for all equations/guesses and the solver may fail safely if the derivative is too small or values become non-finite.
- Tolerance and iteration limits are chosen by the user to balance accuracy and runtime; results are numerical approximations, not exact symbolic solutions.

---

**Project Map:**

- root_solver.py - Main Root Solver console Python script 
- Screeshoots Module 6.pdf - Console output screenshots showing the program running successfully
- Root Solver Activity Diagram.png - UML Activity Diagram for the Root Solver program
- README.md - This document -> program overview, references, assumptions
- utilities/ - Utilities module -> utility banner/menu functions and user input validation functions

---

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

