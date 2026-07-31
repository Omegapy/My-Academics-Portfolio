-----------------------------------------------------------------------------------------------------------------------------
# Portfolio Project  
Program Name: Custom Queue ADT and Quicksort

Grade:  300/300 A

-----------------------------------------------------------------------------------------------------------------------------

CSC400 – Data Structures and Algorithms - Java Course  
Professor: Hubert Pensado  
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 10/06/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-22  

-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:  

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

Program Description:  

This program implements in Java a generic Linked-list queue and sorts the queue using a quicksort algorithm.  
The queue stores Person objects representing a person's first name, last name, and age.   
The Person objects in the queue can be sorted by last name or age.  

Quicksort algorithm notes:  

-	The quicksort algorithm implements a Hoare partition to partition the queue. Meaning that the head node of the linked-list queue is picked as the pivot.  
  
-	Additionally, a queue ADT sort is expected to be stable, preserving the relative (entry) order of elements with equal values.  

-	To partition a linked-list, the element needs to be traversed element by element. Dividing the list into three parts (left, equal, and right) helps simplify the recursion of traversing the list element by element and preserving elements with equal values in order of entry. This also avoids moving elements around in memory, as is required in array-based implementations of quicksort.  

-------------------------------------------------------------------------
----------------------------------------------------

#### Project Map
- Project Report.pdf  
	- Project Explanation 
	- Results and test scenarios for the Final Program  
	- Screenshots Final Program 
- README.md – Markdown file, program information 
- Lessons Learned Reflection.doc – Lesson learned in CSC400 Data Structures and Algorithms - Java Course    
- Milestone-1 – contains Module 2 and Module 4 programs (Program 1 and 2)  
- Milestone-2 – contains Module 5 and Module 6 programs (Program 3 and 4)  
- Final-Program – contains the final program’s Java code source files   
       - Person.java - The Person class.
       - MyQueue.java – The MyQueue<T> Class
       - MyQuickSort.java – The MyQuickSort Class
       - Main.java - The Main class.  

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


