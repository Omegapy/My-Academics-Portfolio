-----------------------------------------------------------------------------------------------------------------------------
# Portfolio Project  
Program Name: Custom Queue ADT and Quicksort

Grade:  

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

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 


