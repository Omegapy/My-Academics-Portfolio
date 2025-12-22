# Principles of Software Development – CSC505 

---

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omega.py)      

created date: 11/10/2025  

---

Project Description:    
This repository is a collection of assignments from CSC505 – Principles of Software Development at Colorado State University Global - CSU Global.  

---

Principles of Software Development CSC505  
Professor: Joseph Issa  
Winter A (25WA) – 2025   
Student: Alexander (Alex) Ricciardi   

Final grade: 

---

My Links:   

<i><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></i>
<i><a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></i>
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
<i><a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></i>
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)
<i><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></i>
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)  
   
---

Requirements:  
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

---

#### Project Map  

- [Critical Thinking 6](#critical-thinking-6)
- [Critical Thinking 5](#critical-thinking-5)
- [Critical Thinking 4](#critical-thinking-4)
- [Critical Thinking 3](#critical-thinking-3)
- [Critical Thinking 2](#critical-thinking-2)
- [Critical Thinking 1](#critical-thinking-1)
- [Discussions](#discussions)

---
---

## Critical Thinking 6
Directory: [Critical-Thinking-6](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC505-Principles-of-Software-Development/Critical-Thinking-6)   
Title: Critical Thinking Assignment 6 – PHTRS

---
---

#### Assignment Description:  

The department of public works for a large city has decided to develop a web-based pothole tracking and repair system (PHTRS). A description follows:

Citizens can log onto a website and report the location and severity of potholes. As potholes are reported, they are logged within a "public works department repair system" and are assigned an identifying number. Potholes are stored by street address, size (on a scale of 1 to 10), location (e.g., middle of road, curb), district (determined from the address), and repair priority (determined from pothole size).

Work order data are associated with each pothole and include:

- Pothole location and size
- Repair crew identifying number
- Number of people on the crew
- Equipment assigned
- Hours applied to repair
- Hole status (work in progress, repaired, temporary repair, not repaired)
- Amount of filler material used
- Cost of repair (calculated based on time, labor, equipment, and materials)

A damage file is also maintained to record citizen-reported damages caused by potholes. This file includes:

- Citizen’s name, address, and phone number
- Type of damage (e.g., tire, alignment, body)
- Dollar amount of damage

PHTRS is an online system, and all interactions and queries are performed interactively through digital interfaces.

**Interface Examples and Assumptions:**

- Citizen Portal Interface: A web form with fields for street address, pothole size (slider or dropdown), pothole location (radio buttons), and optional image upload. Citizens may also have a dashboard to track the status of previously submitted reports or submit damage claims.
- Admin Interface: A secure login-based dashboard that allows authorized public works employees to view reported potholes, filter by district or priority, assign work crews, and update repair status.
- Repair Crew Mobile Interface: A tablet-optimized or mobile-responsive page allowing crews to log hours, update pothole repair status, and enter filler material used.
- Damage Claims Form: An online claims submission form that routes to the department's claims processing system with required fields for contact information, damage description, and evidence upload.
 
**Instructions:**

- Draw a UML Use Case Diagram
- Create a UML Use Case diagram that represents all major actors and their interactions with the PHTRS system. You’ll need to make assumptions about how users interact with the system based on the interfaces described above. Your diagram should include:
    - Actors such as Citizen, Public Works Admin, and Repair Crew
    - Use cases such as Report Pothole, Submit Damage Claim, Assign Repair Crew, Update Repair Status, and Generate Reports
- Use one of the following tools to create your diagram:
    - UMLetLinks to an external site.
    - GliffyLinks to an external site.
    - Microsoft Visio (if you already have access)
- Export your diagram as .png or .pdf.
- Write a Python Summary Script that:
    - Defines the actors and use cases shown in your diagram
    - Prints out each actor and a brief description of their associated use cases
    - Outputs a short textual summary of your diagram structure
Submission Requirements
- Submit the following in a zipped folder:
    - Your Python script (phtrs_summary.py)
    - A screenshot of successful script execution
    - Your UML diagram in .png or .pdf format
    - (Optional) A brief README.txt outlining your design assumptions
- Reference Requirements
Include at least two credible references in addition to the course textbook. Use the CSU Global Library (available in the left hand navigation menu) or professional sources on software design, UML, and civic technology systems. Format references in APA 7 according to the CSU Global Writing Center.
---

PHTRS - Use Case Diagram
<img width="2183" height="2809" alt="PHTRS - Use Case Diagram" src="https://github.com/user-attachments/assets/22edd637-4dbb-4476-97b2-5d16d9efa4c0" />

---

#### Program Description:  
Write a Python Script: developer_builder.py    
The program is a small python script that runs in the console program.  
It creates Developer objects listing desire developer personality traits (Resilience, Awareness Pragmatism).   

---

[Go back to the Project Map](#project-map)

---
---

## Critical Thinking 5
Directory: [Critical-Thinking-5](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC505-Principles-of-Software-Development/Critical-Thinking-5)   
Title: Critical Thinking Assignment 5 – PHTRS

---
---

#### Assignment Description:  

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

#### Program Description:  
Part of Assignment Step 3: Write Your Python Implementation
  - Translate your lowest-level refined design into working Python code.
    - Use functions or classes to reflect the structure of your stepwise breakdown.
    - Keep your code modular and clearly commented.
    - The final script should demonstrate correct functionality for your selected problem.   

---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking 4
Directory: [Critical-Thinking-4](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC505-Principles-of-Software-Development/Critical-Thinking-4)   
Title: Critical Thinking Assignment 4 – Developer Traits

---
---

#### Assignment Description:  

For this assignment, you will identify three personality traits commonly found in high-performing developers based on your professional experience or observations. You will then represent these traits using a UML diagram and simulate their construction in a Python program using the Builder Design Pattern for inspiration.

**Instructions:**

**Identify Developer Traits:**  
- Choose three personality traits that you believe are essential for modern software developers.  
- These can include traits such as curiosity, adaptability, empathy, persistence, communication, or collaboration. Write a brief explanation of each trait and why it's important for team-based software development.   

**Create a UML Diagram:**  
- Model these traits using a UML class diagram, applying the structure of the Builder Design Pattern as shown on OODesign.com. Your UML diagram should:
    - Include a Developer class with each trait as an attribute
    - Include a Developer Builder (or similar) class that constructs the developer object
    - Clearly show class relationships (e.g., composition, method calls)
    - Use one of the following UML tools to create the diagram:
        - UMLetLinks to an external site.
        - GliffyLinks to an external site.
        - Microsoft Visio (optional, if already available)
**Export your diagram as a .png or .pdf file.**  
**Write a Python Script:**
- Develop a Python program (developer_builder.py) that:
    - Defines a Developer class with attributes for each selected trait
    - Uses a builder or fluent interface to construct the developer object
    - Prints a formatted output including:
        - The trait names
        - A brief description of each trait
        - The number of traits represented
Example output:  
Building your ideal developer...
Trait: Curiosity – Drives exploration of new tools and techniques
Trait: Empathy – Enhances team communication and user understanding
Trait: Adaptability – Enables flexibility in changing environments
Total traits included: 3

**Prepare Your Submission:**  
Submit the following in a zipped folder:   
Your Python script file (developer_builder.py)  
A screenshot of the script running successfully  
Your UML diagram (as .png or .pdf)  

---

Builder Design Pattern - Developer Builder 
<img width="2260" height="1853" alt="Builder Design Pattern - Developer Builder" src="https://github.com/user-attachments/assets/d81c8c39-e6f3-488c-a39a-ad06d1c8237a" />

---

#### Program Description:  
Write a Python Script: developer_builder.py    
The program is a small python script that runs in the console program.  
It creates Developer objects listing desire developer personality traits (Resilience, Awareness Pragmatism).   

---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking 3
Directory: [Critical-Thinking-3](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC505-Principles-of-Software-Development/Critical-Thinking-3)   
Title: Critical Thinking Assignment 3 – Mobile App Prototype

---
---

#### Assignment Description:  

You’ve been approached to create an initial prototype for a mobile app that allows users to manage shopping lists on their personal devices. Your task is to create a preliminary architectural design, paper prototype sketches, and a Python summary script that outlines the structure and flow of your design.  
This assignment focuses on the early stages of mobile app development, including UX planning, system architecture, and process flow.  

**Step 1**: Architectural Design Diagram  
Begin by creating a preliminary architecture for your mobile app. Use a diagramming tool (UML or otherwise) to represent key components and interactions. 

Your design should include:  
User interface layer (e.g., Home, Add Item, Edit List, View List, Settings)  
Data layer (e.g., local storage or lightweight cloud sync)  
Controller or logic layer (handles list management, sorting, item removal, etc.)  
Optional extensions (e.g., reminder notifications, sharing lists)  

Recommended Diagram Types:    
UML Component Diagram   
UML Class Diagram   
UML Activity Diagram (to show app behavior)   

Use one of the following tools to create your diagram:  
UMLetLinks to an external site.  
GliffyLinks to an external site.  
Microsoft Visio (if available)  
Export your diagram as .png or .pdf.  

**Step 2**: Paper Prototype Screens  
Sketch a paper prototype of your mobile app showing key screens (hand-drawn or digitally   sketched). 

At a minimum, include:  
Home screen  
Add Item screen  
View List screen  
Edit/Delete Items screen  
Settings/About screen  

Label each screen clearly and show navigation flow between screens (e.g., arrows or numbered steps).  

You may use tools like:    
Pen and paper + phone photo  
Figma (free design tool)  
PowerPoint / Google Slides mockups  
Gliffy / Visio UI stencils  

Tip: The goal is not high-fidelity design, but to simulate how a user would move through the app and what they’d see.

**Step 3**: Python Script to Describe Prototype  

Create a Python script (shopping_list_prototype.py) that:  
Defines the screen names  
Prints the total number of screens  
Prints the navigation flow (e.g., "Home → Add Item → Save → View List")  
Optionally includes descriptions of what each screen does  
Sample Output:

Screens: Home, Add Item, View List, Edit Item, Settings  
Total Screens: 5  
Flow:  
Home → Add Item  
Add Item → View List  
View List → Edit Item  
Home → Settings  

Keep the code simple and use lists or dictionaries to model screens and navigation.

**Step 4**: Submit Your Work  
Submit a zipped folder containing:

Your Python script (shopping_list_prototype.py)  
A screenshot of the script running successfully  
Your architecture diagram (.png or .pdf)  
Your paper prototype screens (images or .pdf)  
(Optional) README.txt with additional notes or assumptions  

References:  

Include at least two credible references in addition to the course textbook. These can include articles, tutorials, mobile UX design guides, or prototyping best practices. Cite all sources using APA 7 format according to the CSU Global Writing Center.  

Good starting points:  
CSU Global Library (available in the left hand navigation menu)  
Nielsen Norman GroupLinks to an external site.  
Mobile design tool documentation (e.g., Figma, Google Material Design)  
 
---

The Mobile App component diagram:  
<img width="2465" height="1399" alt="Mobile App component diagram" src="https://github.com/user-attachments/assets/c848578a-ad2b-4564-b7cf-c8ec82e2cdeb" />

---

The Mobile Shopping APP UI Prototype:  
<img width="3100" height="2940" alt="Mobile Shopping APP UI Prototype" src="https://github.com/user-attachments/assets/a102dc34-edae-429b-b566-7fc878d8eef4" />

---

#### Program Description:  
The program is a small console program that summarizes a mobile shopping app UI flow.  
The script lists screens, counts, descriptions, and navigation screen UI flow paths.

---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking 2
Directory: [Critical-Thinking-2](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC505-Principles-of-Software-Development/Critical-Thinking-2)   
Title: Critical Thinking Assignment 2 – Development and Design Model

---
---

#### Assignment Description:  

Consider the traditional Waterfall Model, which includes sequential stages: communication, planning, modeling, construction, and deployment (Adapted from Pressman, 2020, p. 26). While foundational, this model has limitations in today's fast-changing software environments.  
<img width="850" height="229" alt="image" src="https://github.com/user-attachments/assets/37c00a7e-06bc-4fb9-95d8-b38e9ce41b61" />  
The Waterfall Model includes: Communication (project initiation, requirement gathering), planning (estimating, scheduling, tracking), modeling (analysis, design), construction (code, test, peer validation), and deployment (delivery, support, feedback, TAM).  
(Adapted from Pressman, 2020, p. 26)


For this assignment, you will evaluate the Waterfall Model’s shortcomings and design a modernized version called the YourLastName Adaptive Model. You will visualize it with a UML-style diagram and simulate user interaction using a Python script.

**Instructions:**

Evaluate the Waterfall Model:  
- Briefly identify at least three limitations of the traditional Waterfall Model (e.g., lack of flexibility, late testing, poor adaptability to change).

Design the YourLastName Adaptive Model:
- Using your findings, design a modernized process model. You may integrate principles from Agile, DevOps, or Spiral methodologies.   
Your model should still include major phases, but with added adaptability or feedback loops.

Create a UML Diagram:  
Create a visual diagram of your model using one of the following tools
- UMLetLinks to an external site.
- GliffyLinks to an external site.
- Microsoft Visio (optional, if already available)
Export your diagram as a .png or .pdf.

Develop a Python Script:  
Implement a script named yourlastname_model.py that:  
- Prompts the user for each phase name and a short description.
- Outputs a well-formatted summary of the model’s phases and structure.

Example output:
Phase 1: Discovery - Understand user needs and priorities  
Phase 2: Iterative Design - Develop, test, and refine features  

Gather Your Submission:  
Submit the following in a zipped folder:
- Python source file (.py)
- Screenshot of successful program execution
- UML diagram (.png or .pdf)   

---

Program Description:  
The program is part of the Develop a Python Script section of the assignment, it is a console program that:  
    1. Prompts users for how many phases their model has  
    2. Prompts users for the name and a short description of each phase in their model  
    3. Prints a well formatted summary:  

    Phase 1: Discovery - Understand user needs and priorities
    Phase 2: Iterative Design - Develop, test, and refine features


---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking 1
Directory: [Critical-Thinking-1](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC505-Principles-of-Software-Development/Critical-Thinking-1)   
Title: Critical Thinking Assignment 1 – Sales Analysis

---
---

Assignment Description:  

For this assignment, you will write a simple Python prototype and then create a short developer report, simulating the kind of deliverable expected by a technical team lead or project manager in a modern software development environment. Whether you’re working independently or as part of a team, understanding the challenges of software development and communicating technical work clearly are essential skills for success.  

To get familiar with Python programming and integrated development tools used in the field, begin by writing a Python script with a practical, real-world purpose. Then, create a brief developer-facing report reflecting on key aspects of your experience and how they relate to broader software development challenges.  


Part 1: Python Script Development  
Write a Python script that performs a useful or realistic task. You may choose one of the following or propose your own idea:  

A command-line tip calculator.  
A script that reads and analyzes a CSV file (e.g., grades, sales).  
A simple to-do list or task tracker.  
A basic simulation (e.g., mock CPU/memory monitor using random values).  
A log parser that searches for keywords in a sample file.  
Use any modern IDE of your choice (e.g., VS Code, PyCharm, Replit).  


Part 2: Developer Report (Professional Documentation)  
After completing your script, prepare a developer report answering the following   stakeholder-facing questions based on your experience:  

What was the purpose or intended use case of your script?  
What tools or libraries did you use, and why?  
What challenges did you encounter during development?  
How would you expand or improve this prototype in future iterations?  
What lessons did you learn that apply to broader software development work?  
Keep your responses brief and professional (1–3 sentences per question). This report simulates what you might send as part of an internal project handoff or sprint demo.   


Part 3: Submission Requirements  
Submit the following in a zipped folder:  

Your Python source file (.py).  
A screenshot of your program running successfully.  
Your completed developer report (.txt, .md, or .pdf).  

---

#### Program Description:  
Console-based application that loads Omega.py sales CSV data, computes metrics, and computes sales analytics.

---

[Go back to the Project Map](#project-map)  

----
----

## Discussions 
This repository is a collection of discussion posts from CSC505 – Principles of Software Development   
Directory: [Discussions](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC505-Principles-of-Software-Development/Discussions)

---

[Go back to the Project Map](#project-map)


