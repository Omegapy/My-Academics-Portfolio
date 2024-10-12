-----------------------------------------------------------------------------------------------------------------------------
# Portfolio Projects 
-----------------------------------------------------------------------------------------------------------------------------

 <img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"> Alejandro (Alex) Ricciardi (Omegapy)   

-----------------------------------------------------------------------------------------------------------------------------

Projects Description:  
This repository is a collection of Portfolio Projects from Colorado State University Global (CSU Global)  
and Laramie County Community College (LCCC), showcasing my educational journey, and achievements.

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- [Python](https://www.python.org/)
- [Jupyter Notebook](https://jupyter.org/)    
- [c++](https://isocpp.org/std/the-standard)
- [java](https://www.java.com/en/)
- [WebGL](https://get.webgl.org/)  

-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)    

Related links:  
[CSU Global](https://csuglobal.edu/)   

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- [CSC400 Data Structures and Algorithms Java](#csc400-data-structures-and-algorithms-java)
- [CSC405 Graphics and Visualization WebGL](#csc405-graphics-and-visualization-webgl)
- [CSC372 Computer Programming 2 Java](#csc372-computer-programming-2-java)
- [CSC320 Programming 1 Java](#csc320-programming-1-java)
- [ITS320 Basic Programming Python](#its320-basic-programming-python)
- [CSC300 Operating Systems and Architecture](#csc300-operating-systems-and-architecture)  
- [COSC1030 Computer Science 1](#cosc1030-computer-science-1)
- [ENG102 Composition 2](#eng102-composition-2)
- [HUM101 Critical Reasoning](#hum101-critical-reasoning)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## CSC400 Data Structures and Algorithms Java
Directory: [CSC400 CSU Global]()   
Portfolio Assignment Option 1: Person Class 
Program Name: Custom Queue ADT and Quicksort  
Fall B (24FB) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 10/06/2024
   
Grade:  100% A

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Description:  
This program implements in Java a generic Linked-list queue and sorts the queue using a quicksort algorithm.  
The queue stores Person objects representing a person's first name, last name, and age.   
The Person objects in the queue can be sorted by last name or age.  

Quicksort algorithm notes:  
-	The quicksort algorithm implements a Hoare partition to partition the queue. Meaning that the head node of the linked-list queue is picked as the pivot.  
-	Additionally, a queue ADT sort is expected to be stable, preserving the relative (entry) order of elements with equal values.  
-	To partition a linked-list, the element needs to be traversed element by element. Dividing the list into three parts (left, equal, and right) helps simplify the recursion of traversing the list element by element and preserving elements with equal values in order of entry. This also avoids moving elements around in memory, as is required in array-based implementations of quicksort.  

       
-------------------------------------------------------------------------------------------

Assignment Directions:  
Option #1: Person Class

Your Portfolio Project for CSC400 consists of the following:  
- Milestone 1 (due in Module 5): Java source code (with corrections if necessary) for programs created in Module 2 and Module 4.  
- Milestone 2 (due in Module 7): Java source code (with corrections if necessary) for programs created in Module 5 and Module 6.  
- Lessons Learned Reflection  
- Final Program  

Lessons Learned Reflection:  
Write a 2-page summary that outlines the lessons you have learned in this programming course. Reflect on how these lessons can be applied towards more effective coding.

Final Program:  
Write a program that creates a Person class that contains strings that represent the first and last name of a person and their age. You will need to create a Queue class that will store each person in the queue and can sort the queue based on last name or age.  

Prompt the user of the program to add five people to the queue. Your program should provide the contents of the queue and then sort the queue using the quick sort in two ways

1.	Descending order by last name  
2.	Descending order by age  

Assemble your Lessons Learned Reflection, your source code, and screenshots of the application executing and results into a single document. Submit your completed Portfolio Project by the posted due date.  

⚠️ My notes:   
-	No corrections were needed for the programs in Milestones 1 and 2.  
-	The Milestones 1 programs’ files can be found in the directory Milestones-1.  
-	The Milestones 2 programs’ files can be found in the directory Milestones-2.  
-	The final program’s Java code source files can be found in the folder Final-Program.  
-	Screenshots for the final program can be found in the Screenshots folder.  
-	I used the generic data type in my implementations of the queue and Quick Sort in my final program.
  
----------------------------------------------------------------------------------------------------------------------------- 

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## CSC405 Graphics and Visualization WebGL
Directory: [CSC405 CSU Global](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/CSC405%20CSU%20Global)   
Portfolio Assignment 
Program Name: Projection Lighting and Painter's Algorithm of a 3D Rotating Cube - WebGL    
Fall B (24FB) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 10/06/2024
   
Grade:  A

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

<p align="left">
<img  src="https://github.com/user-attachments/assets/6baed473-9a62-4fd4-8cd8-703249e82ae2">
</p>

The following video demonstrates the functionality of the program: [Projection Lighting and Painter's Algorithm of a 3D Rotating Cube - WebGL](https://www.youtube.com/watch?v=tczs3bjaGtQ)

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
       
-------------------------------------------------------------------------------------------

Assignment Directions:  Portfolio Project  
There are three parts to the portfolio project.  

Updates to Milestone from Module 5:  
Based on instructor feedback, please provide updates to your interactive viewer activity from Module 5. Additionally, implement advanced interactivity features. For example, allow users to select and highlight parts of a complex object, switch between visualizations, or toggle between shaders. You will compile the updated source files with screenshots with your final project submission.  

Lessons Learned Reflection:  
Write a two-page summary that discusses the lessons you learned in this course. Reflect on how these lessons can be applied to a real-world problem or a specific real application. How will you use the concepts in this course going forward?  

Final Program (Hidden-Surface Removal Problem):  
Study the Hidden-Surface Removal problem and implement the Painter’s algorithm using WebGL. Provide one paragraph discussing what the Hidden-Surface Removal problem within your lessons learned reflection document.  

Clearly provide the details of your program (provide a 2-paragraph overview), including the screenshots of your working program. Describe the object (primitive) that you are working with. Don’t forget to adequately comment your source code.  

Assemble all of the requirements for this project and submit to Canvas for grading by the due date. As a reminder, there are no late submissions for Module 8, as everything must be submitted by the last day of the term. 

Project Map:  
- rotatingCube.html – contains Program Final Version 3 Vertex Shader GLSL and Fragment Shader GLSL  
- rotatingCube.js – Program Final Version 3 contains JavaScript application logic  
- common folder – contains External Script for initializing shaders and performing matrix operations 
- Reflection Portfolio Project.doc – provides an overview and reflection on the program's functionality, as well as a discussion about the Hidden-Surface Removal problem   
- Screenshots – contains the 3D cube screenshots 
- Portfolio-Milestone - contains the Program Version 2 files   
- Lessons Learned Reflection.doc – Essay about the lessons in CSC405 – Graphics and Visualization - WebGL Course    
- README.md – Markdown file, program information  

----------------------------------------------------------------------------------------------------------------------------- 

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## CSC372 Computer Programming 2 Java
Directory: [CSC372 CSU Global](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/CSC372%20CSU%20Global)   
Portfolio Assignment Option 1 
Program Name: Students Manager   
Spring D (24SD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 08/04/2024
   
Grade:  100% A

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Description:  
The Students Manager is a small Java application that utilizes JavaFX GUI  allowing the user to add, view, search, and sort students' data:    
        - Student data management (name, address, GPA)    
        - File-based storage    
        - Sorting by name or GPA    
        - Search functionality     
        - Basic data validation      
       
-------------------------------------------------------------------------------------------

Assignment Directions:  
student data. Student data are private fields in a student class including:  
•	String name  
•	String address  
•	double GPA  
Each student object is stored in a linked list.   
After the user completes the data entry, output the contents of the linked list in ascending sorted order by name to a regular text file that can be opened and viewed using a simple plain-text editor such as notepad.
Validate numeric data for Grade Point Average (GPA).   
Compile your Lessons Learned Reflection, source code, screenshots of the application executing, and results into a single document.   
Format your document in MS Word, according to APA guidelines in the CSU Global Writing Center, particularly in developing your Lessons Learned Reflection. Support your reflection with a minimum of three references, as noted above. Include both a cover page and a reference page with your Portfolio Project.   

⚠️ Program Notes:    
-	I got permission from Dr. Cooper to use the JavaFX library to display the program outputs.  
-	Added my own icon to the window frame – logo.png.  
-	Added search functionality (not an assignment requirement).  
-	Added read file functionality (not an assignment requirement).  
-	Added the option to add fake data to the file for troubleshooting purposes (not an assignment requirement).  
-	Implemented my own selection sort and binary search algorithms.  
-	Created a UML class diagram.  
-	For the source code please see the following: Student.java, StudentManager.java, NameComparator.java, GpaComparator.java, SortSearchUtil.java, StudentManagerApp.java    

Project Map:  
-	Project Report.pdf: A pdf file (this file) containing an overview of the assignment and the Students Manager program.  
-	README.md: A markdown file containing information about the project, intended to be viewed on GitHub.   
-	Lessons Learned and Reflection.doc: A Word document containing a summary and reflections on the lessons I have learned in this programming course.   
-	Milestone-1: Directory containing the Portfolio Milestone assignment from Module 4.  
-	Milestone-2: Directory containing the Portfolio Milestone assignment from Module 7.  
-	Application: A folder containing the source code, Java code files for the Students Manager program.  

----------------------------------------------------------------------------------------------------------------------------- 

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## CSC320 Programming 1 Java
Directory: [CSC320 CSU Global](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/CSC320%20CSU%20Global)   
Portfolio Assignment Option 2 
Program Name: Home Inventory Manager   
Spring B Semester (24SB) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 06/09/2024
   
Grade:  100% A

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Description:  
The program manages a home inventory.  
It provides functionality for adding, removing, updating, and displaying home data.  
The program interacts with the user through a menu-driven interface and stores the home data in a file.   

-------------------------------------------------------------------------------------------

Assignment Directions:  
Portfolio Project – Home Inventory Manager Option2  
Your Portfolio Project for CSC320 will consist of three components:  

•	Program corrections: Make the appropriate corrections to all the programming assignments submitted as Critical Thinking assignments from Modules 1-6. You will need to submit the programs along with the carefully outlined corrections needed in order for programs to run correctly.  
•	Lessons learned reflection: Create a 2-3-page summary that outlines the lessons learned in this Programming I course.  
•	Final program: Create a final program that meets the requirements outlined below.  

Final Program Requirements  
Create a home inventory class that will be used by a national builder to maintain an inventory of available houses in the country. The following attributes should be present in your home class:  

•	private int square_feet  
•	private string address  
•	private string city  
•	private string state  
•	private int zip_code  
•	private string Model_name  
•	private string sale_status (sold, available, or under contract)  

Your program should have appropriate methods such as:  

•	constructor  
•	add a new home  
•	remove a home  
•	update home attributes  
All methods should include try..catch constructs. Except as noted, all methods should return a success or failure message (failure message defined in "catch").  

1.	Create an additional class to call your home class (e.g., Main or HomeInventory). Include a try..catch construct and print it to the console.  
2.	Call home class with parameterized constructor (e.g., "square_feet, address, city, state, zip_code, Model_name, sale_status").  
o	Then, call the method to list the values. Loop through the array and print to the screen    
3.	Call the remove home method to clear the variables:  
o	Print the return value.  
4.	Add a new home.  
o	Print the return value.  
o	Call the list method and print the new home information to the screen.  
5.	Update the home (change the sale status).  
o	Print the return value.  
o	Call the listing method and print the information to the screen.  
6.	Display a message asking if the user wants to print the information to a file (Y or N).  
o	Use a scanner to capture the response. If "Y", print the file to a predefined location (e.g., C:\Temp\Home.txt). Note: you may want to create a method to print the information in the main class.  
o	If "N", indicate that a file will not be printed.  

Your final program submission materials must include your source code and screenshots of the application executing the application and the results.  
Compile your Module 1-6 programs with corrections, lessons learned reflection, and final program course code and application screenshots.  

⚠️ My notes:  
-	I got permission from Professor Pensado for the program to manipulate a file.  
-	The program utilizes BufferedReader and BufferedWriter classes to read and write a file, the program also uses the ArrayList class the access and modify the homes’ data.  
-	In the HomeInventory class the functionalities of methods getHomeByAddress, removeHomeByAddress, and updateHomeByAddress are not implemented in version 1 of the program. However, they are available for future versions of the program.  
-	The program handles exceptions by passing them from the Home class to the HomeInventory class, and then to the Main class, where the exceptions and errors are displayed to the user.  
-	For the source code please see Main.java, InputValidation. Java, Home.java, and HomeInventory.java files. 

----------------------------------------------------------------------------------------------------------------------------- 

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 Basic Programming Python
Directory: [IT320 CSU Global](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/IT320%20CSU%20Global)   
Portfolio Assignment Option 2  
File: Home Inventory Mannager.py  
Winter Semester (24WD) – 2024  
Date: 04/07/2024  

Grade:  300/300 A

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
To manage a home inventory system with functionality to add, update, remove, and display homes data.

-------------------------------------------------------------------------------------------

Assignment Directions:  
Option #2: Program Corrections, Lessons Learned, and Home Inventory Program  
Create a home inventory class that will be used by a National Builder to maintain an inventory of available houses in the country.    
The following attributes should be present in your home class:  

- private int squarefeet  
- private string address  
- private string city  
- private string state  
- private int zipcode  
- private string Modelname  
- private string salestatus (sold, available, under contract)  

Your program should have appropriate methods such as:

- Constructor   
- add a new home  
- remove a home
- update home attributes  
At the end of your program, be sure that it allows the user to output all home inventory to a text file.

-------------------------------------------------------------------------------------------

Pseudocode:
1. Import necessary modules (os) to manipulate file  
2. Create banner  
3. Define the HomeInventory
    - Define a dictionary to store the home data  
      The dictionary needs to be private to meet the attributes private requirements of the assignment  
    - Constructor (init): Initialize the HomeInventory object with the provided filename  
    - Destructor (del): Perform cleanup when the HomeInventory object is destroyed  
    - Getters: Methods to retrieve home data attributes  
    - Setters: Methods to add, remove, and update homes in the inventory  
    - Class Information Methods: Implement str and repr for string representation of the class  
4. Define display functions
    - display_home_data_using_home_id: Display the home data for a specific home using its ID  
    - display_homes: Display a range of homes from the inventory file  
5. Define menu functions   
    - get_valid_input: Prompt the user for input and validate it based on data type  
    - menus: Display the menus to handle user input and to manipulate the home data  
6. Define the main function  
    - Create a HomeInventory object  
    - Display class HomeInventory information  
    - Start the user interface menu  
-------------------------------------------------------------------------------------------

Program Inputs:
    - User input for adding, updating, and removing homes  
    - User input for displaying home information  
    - User input for navigating the menu options  
    
-------------------------------------------------------------------------------------------

Program Inputs: User input for home details, menu choices, and file name.  
Program Outputs: Display of home inventory, updated inventory file, and user prompts. 

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## CSC300 Operating Systems and Architecture
Directory: [CSC300 CSU Global](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/CSC300%20CSU%20Global)  
File: Solutions for a Business Enterprise-Wide Upgrade.pdf  
Spring Semester - 2023  
Date: 04/07/2024  

Grade: 350/350 A+

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  
Portfolio Project (350 Points)
Choose one of the following two assignments to complete this week. Do not do both assignments. 
Identify your assignment choice in the title of your submission.

Option #1: Propose an Enterprise-wide Upgrade Solution for an Organization  
Assume you are a consultant for a local business that has asked you to propose   
an enterprise-wide upgrade solution that includes operating systems, mass storage,   
virtualization and security. The company currently has a mix of operating systems, including several legacy machines.   
The company does not currently use virtual machines but is strongly considering them.   
The company's core business is software testing but it is considering offering a storage solution.  

Your proposal should address the following concerns and questions presented by stakeholders.  

Are there benefits in upgrading their corporate Operating Systems from Windows 8.1 to Windows 10?  
Is there a way to prevent deadlocks from occurring? If they cannot be prevented, is it possible to recover from deadlocks?  
Considering the Windows and Linux operating systems, which OS would be preferred for NAS and why?  
Your paper should also meet the following requirements:

Be 8-10-pages in length.
Include at least three references from the readings or outside sources. 
You can cite the course material and at least one additional credible or scholarly source must also be included to support your analysis and positions.   
The CSU Global LibraryLinks to an external site. is a good place to find your sources.  
Follow APA guidelines in the CSU Global Writing Center.  
Option #2: Upgrade an OS that Uses a Many-to-Many Model or Many-to-One Model  
Currently, OS/2, Windows NT, and Windows 2000 are used in the labs for testing; each uses a one-to-one relationship model.   
Is there a benefit in upgrading to an OS that uses a many-to-many model or a many-to-one model?  
If so, expound on the advantages and which OS would be suitable.

What solution would you recommend for Mass Storage?  
Is RAID a viable option for Mass Storage? If so, which level do you recommend, and why?  
What VM solutions are available, and would it be advantageous to use (VMM) Virtual Machine Manager?  
What storage Virtualization solution would you recommend?  
What software and hardware components would you recommend for network security?  
Would Linux be considered more secure than Windows, and are the file systems similar?  

Your paper should also meet the following requirements:  
Be 8-10-pages in length.  
Include at least three references from the readings or outside sources.   
You can cite the course material and at least one additional credible or scholarly source must also be included to support your analysis and positions.   
The CSU Global LibraryLinks to an external site. is a good place to find your sources.  
Follow APA guidelines in the CSU Global Writing Center.	

-------------------------------------------------------------------------------------------

Essay Summary:  

Title: Portfolio: Solutions for a Business Enterprise-Wide Upgrade  
The portfolio essay presents solutions for a company's enterprise-wide upgrade, focusing on operating systems, mass storage, virtualization,   
and security. The key points are:  
1. Upgrading to a single corporate operating system (Windows 10) for a more uniform environment, improved security, better support, and enhanced compatibility.  
2. Implementing virtualization to optimize cost and hardware resources, improve security and isolation, facilitate software testing, and support legacy applications.  
3. Recommending a Linux-based Network-Attached Storage (NAS) solution for its cost benefits, flexibility, and advanced features compared to a Windows-based NAS.  
4. Implementing strategies to prevent, avoid, and recover from deadlocks while balancing the company's needs and the trade-offs associated with these strategies.  
5. Employing various security measures, such as antivirus/antimalware software, firewalls, intrusion detection   
and prevention systems, patch management, penetration testing, security awareness training, access controls, encryption, and Systems Event Management (SIEM).  
The essay concludes that implementing these suggestions could significantly improve the company's efficiency, security, and competitiveness,   
as well as create opportunities for exploring new business ventures.

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## COSC1030 Computer Science 1
Directory: [COSC 1030 LCCC](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/COSC%201030%20LCCC)   
Portfolio Assignment  
Fall Semester – 2022  
Date: 04/07/2024  

Final grade: 100% A

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
create an interactive, text-based Choose Your Own Adventure style game in c++.  

-------------------------------------------------------------------------------------------

Class Final Project Prerequisites:
Your final project is to create an interactive, text-based Choose Your Own Adventure style game based on a movie, 
book or game of your choice. You may use your own idea if you don't want to base it on an existing property.
 If you aren't sure what I mean by Choose Your Own Adventure, see the "Cat Break" image file in this week's module. 
 (Credit to the author, Fox, for the Choose Your Own Adventure.)

Note: This project goes substantially beyond the Class Final Project Prerequisites; the project is a small c++ window desktop application.

-----------------------------------------------------------------------------------------------------------------------------

Project description:  
Ethers Quest is a small story-based D&D game based on the Innistrad universe. 
Where Ether journeys to save his younger sister Clarabella. 
Clarabella was abducted by the evil vampire lord, Salt, 
to be offered in sacrifice to the demon Iretrat. In exchange for Clarabellas soul, 
Iretrat will reanimate Pantra, Salts lost love, using Clarabellas blood. 
The sacrifice must be performed on the first day of the Hunters moon, 
at the Skirsdag high temple located in Stensia. 
Ethers journey to save Clarabella will start at his home in Gavony. 


he will travel through the region of Nephalia , Kessig, and Stensia, 
where he will encounter many dangers. Provided that he survives the journey; 
at Skirsdag high temple, he will have to battle  
and defeat both lord Salt and the demon Iretrat to save Clarabella and complete his quest.

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ENG102 Composition 2
Folder: [Eng 1020 CSU Global](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/CSC300%20CSU%20Global)  
File: Navigating the AI Revolution.pdf  
Winter Semester (24WD) – 2024   
Date: 04/07/2024  

Grade: 329/354 B+

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  
Portfolio Project (350 Points)
Argumentative Essay
For your Portfolio Project (due in Module 8) you will write an argumentative essay based on a topic in your major field of study.  
You will submit the topic for approval in Module 2, and continue to write and revise until the due date.  
If you critically read the assigned readings and lecture content, enthusiastically participate in the module discussions,  
submit your best work for the Critical Thinking assignments, and thoughtfully reflect on your instructor feedback,  
you will find that the work for your final portfolio project is the natural progression of your work during the course.  
Based on this cumulative approach, it should represent your strongest work.

Requirements  
Your essay must:

Be persuasive. You need to make a clear argument, articulated in your thesis statement, and supported throughout the body of the essay.  
Be directed at a specific audience.  
Have a thesis statement that includes your overall argument and maps out the points you make in the body of the paper.  
Support the thesis with research from credible sources.  
Demonstrate your ability to synthesize and analyze information from multiple sources in order to develop your own insights into the topic.  
Summarize and respond to counterarguments.  
Include proper in-text citations and references citations in APA format.  
Guidance
Length: 3-4 pages, not including the title page or references page, which you are required to include.
Support: 6 or more credible print sources cited in the paper and included on the references page.   
The sources should be from roughly the last five to seven years.  
Voice: Third-person. APA format does allow for limited use of first-person pronouns when describing your work,   
but it is unlikely you will need to use the first person in this project.  	

-------------------------------------------------------------------------------------------

Essay Summary:  

Title: Navigating the AI Revolution: Promoting Innovation and Mitigating Risks  
The essay explores the potential risks and benefits of AI development   
and proposes solutions to mitigate risks while promoting innovation. Key points include:  

1. Risks of unchecked AI development: Misuse, loss of control, and existential threats.    
Severe restrictions proposed by some organizations are myopic and impractical. 
 
2. Solutions:  
a. Ethical AI: Integrate ethical principles into AI systems through Constitutional AI (CAI) and AI Ethical Reasoning (AIER).   
b. AI Reasoning: Train AI to reason efficiently and align with human values and ethical principles.   
C. Government Regulations: Establish a government agency to license and test AI models, implement precision regulation,   
and gradually increase oversight while permitting innovation.    

3. Importance of a balanced approach combining ethical AI development, government regulation, and proactive management of societal impacts.

4. The need for collaboration among government agencies, international organizations,   
and industry self-regulation to ensure AI's safe and beneficial implementation.

5. Urgency of action due to the rapid pace of AI advancement, emphasizing the importance of research on AI Ethical Reasoning.  

The essay concludes that by integrating ethical principles, fostering a culture of safety and ethics among AI developers,   
and establishing appropriate government regulations and agencies, society can responsibly navigate the AI revolution.

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## HUM101 Critical Reasoning
Folder: [HUM101 CSU Global](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Portfolio%20Projects/HUM101%20CSU%20Global)  
File: Aristotle's Ethical Deliberation and Virtue: Principles for Ethical AI.pdf  
Spring Semester (24SD) – 2024   
Date: 08/04/2024  

Grade: 94% B

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  
Option #1: Applying Philosophy to a Modern-Day Issue  
In this option, you will complete the following:  

Select a key idea from one of our five philosophers covered in weeks 1-5.  
Apply that key idea to a modern-day context.  
Demonstrate how that key idea helps the reader understand your perspective on the modern-day context.  
For example, you may choose to discuss Plato’s concept of how knowledge changes perspective, and you may apply that idea to a modern-day novel, film, news story, or even a magazine advertisement.  

The choice of what you apply the tool to is your own. By that, you may choose whatever text, or artifact that communicates a message, to apply the tool.  

Imagine, for example, you watched Bill and Ted’s Excellent Adventure, that film we talked about in our discussion of Plato. You might want to talk about how that film does or does not successfully apply the concepts of Plato to teach the audience about a larger idea.

Note: You may debate whether the text you choose does or does not meet the standards of your chosen philosopher’s ideas.

Remember, too, that you’ve likely done a lot of work on the key themes and examples in our weekly handouts. You can mine ideas and sources from there and from any feedback from your peers.

You have also done a good bit of work on your thesis and/or body paragraphs with your Portfolio Milestone Assignments from weeks 2, 4, and 6. Again, you are encouraged to revisit that work and comments from your Instructor on that work to outline and revise your ideas for the final portfolio project.

Hint: While you are putting together your final discussion presentation in Week 8 discussion, you will also get a chance to review your key ideas and quotes from the class, so be sure to leverage that step in locating key elements of your final paper’s body paragraphs and/or ideas to inform the final thesis, introduction, and conclusion.

Your paper must be two to three pages, 12-point font, double-spaced. That means no 1.5 page papers, and no papers longer than 3 pages. The length of the paper is designed to help you boil down the key ideas into a focused thesis with 3-7 body paragraphs and a conclusion. We are focusing on quality, not quantity. For more on the academic writing process for the final portfolio, review the Week 8 Lecture. 

Include at least two references - one from a philosopher and at least one from a credible outside source. The CSU Global Library is a good place to find these references. To quickly access the Library, click on the tabs in the Course Navigation Panel.  	

-------------------------------------------------------------------------------------------

Essay Summary:  

Title: Aristotle's Ethical Deliberation and Virtue: Principles for Ethical AI   
The paper draws connections between ancient philosophy and modern technology, suggesting that Aristotle's Ethical Deliberation and Virtue concepts could guide the development of ethically aligned AI systems.

Key points include:  

1. Introduction:  
The paper discusses the potential of AI to transform society and the ethical questions this raises.  
2. Aristotle's Ethical Deliberation:  
It explores Aristotle's concept of ethical deliberation as a process of reaching good results through means other than deduction.  
3. Application to AI:  
The paper suggests incorporating Aristotle's principles into AI model training to ensure ethical outputs.  
4. Aristotle's Concept of Virtue:  
It discusses Aristotle's idea of ethical virtue as a mean between extremes and how this could be applied to AI development.  
5. Challenges:  
The paper acknowledges difficulties in implementing these concepts in AI, such as translating abstract ethical principles into machine-processable forms.  
6. Conclusion:  
It argues for the relevance of Aristotelian ethics in developing ethical AI systems, emphasizing the need to embed these principles into AI design.  

[Go back to the Project Map](#project-map)
