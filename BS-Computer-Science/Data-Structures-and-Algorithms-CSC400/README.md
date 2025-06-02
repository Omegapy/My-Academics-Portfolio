-----------------------------------------------------------------------------------------------------------------------------
# Data Structures and Algorithms (Java) – CSC400
-----------------------------------------------------------------------------------------------------------------------------

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alejandro (Alex) Ricciardi (Omegapy)  

created date: 08/12/2024  

-----------------------------------------------------------------------------------------------------------------------------

Projects Description:    
This repository is a collection of Java programs and assignments from CSC400 – Data Structures and Algorithms Course  
at Colorado State University Global - CSU Global.  

-----------------------------------------------------------------------------------------------------------------------------

CSC400 – Data Structures and Algorithms Course   
Professor: Herbert Pensado  
Fall B (24FB) – 2024   
Student: Alejandro (Alex) Ricciardi   

Final grade: 100% A

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-22

-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    <span><a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></span>    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)      

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map

- [Portfolio Project](#portfolio-project)
- [Critical Thinking 5](#critical-thinking-5)
- [Critical Thinking 4](#critical-thinking-4) 
- [Critical Thinking 3](#critical-thinking-3) 
- [Critical Thinking 2](#critical-thinking-2) 
- [Critical Thinking 1](#critical-thinking-1) 
- [Discussions](#discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Portfolio Project
Directory: [Portfolio-Project](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Data-Structures-and-Algorithms-CSC400/Portfolio-Project)  
Program Name: Custom Queue ADT and Quicksort  

-------------------------------------------------------------------------------------------

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


Program Description:  
This program implements in Java a generic Linked-list queue and sorts the queue using a quicksort algorithm.  
The queue stores Person objects representing a person's first name, last name, and age.   
The Person objects in the queue can be sorted by last name or age.  

Quicksort algorithm notes:  

-	The quicksort algorithm implements a Hoare partition to partition the queue. Meaning that the head node of the linked-list queue is picked as the pivot.  
  
-	Additionally, a queue ADT sort is expected to be stable, preserving the relative (entry) order of elements with equal values.  

-	To partition a linked-list, the element needs to be traversed element by element. Dividing the list into three parts (left, equal, and right) helps simplify the recursion of traversing the list element by element and preserving elements with equal values in order of entry. This also avoids moving elements around in memory, as is required in array-based implementations of quicksort.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 5
Directory: [Critical-Thinking-5](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Data-Structures-and-Algorithms-CSC400/Critical-Thinking-5)  
Program Name: MSD RadixSort

-------------------------------------------------------------------------------------------

Program Description:  
MSD RadixSort is an implementation of a Most Significant Digit (MSD) radix sort in Java, which sorts an array of lowercase strings in alphabetical order by examining each character from left to right. The program uses recursion to sort subarrays (buckets) based on character positions. 

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 4
Directory: [Critical-Thinking-4](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Data-Structures-and-Algorithms-CSC400/Critical-Thinking-4)  
Program Name: Infix Calculator

-------------------------------------------------------------------------------------------

Program Description: 
-	The program is an implementation of an Infix calculator that evaluates arithmetic expressions in infix notation.  
-	The program converts Infix expressions stored in a text file into Postfix expressions, then computes the Postfix expressions and displays the computation results.  
-	The program utilizes a Stack Abstract Data Structure (Stack ADT) to manage operators and operands when converting Infix expressions to Postfix form and during the evaluation of Postfix expressions.
-	The Stack ADT is a linked list structure or chain using generic types.   
[element | next] -> [element | next] -> [element | next] -> null.   

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 3
Directory: [Critical-Thinking-3](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Data-Structures-and-Algorithms-CSC400/Critical-Thinking-3)  
Name: Asymptotic Analysis Exercises

-------------------------------------------------------------------------------------------

Project Description:  
This documentation is part of the Critical Thinking 3 Assignment from CSC400: Data Structures and Algorithms at Colorado State University Global. It consists of a series of exercises designed to demonstrate the principles of asymptotic analysis. Asymptotic analysis uses the Big-Oh notation.

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 2
Directory: [Critical-Thinking-2](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Data-Structures-and-Algorithms-CSC400/Critical-Thinking-2)  
Program Name: RPG Bag

-------------------------------------------------------------------------------------------

Program Description: 
The Program is version 2 of the [Critical Thinking 1](#critical-thinking-1) program with added functionalities, such as merge and duplicate removal.  
The program is a simple implementation of a Bag Abstract Data Structure (Bag ADT) in Java.  
The Bag class represents the inventory of an RPG video game player. 
The Bag allows for the storage and management of game items such as Potions, Armor, and Weapons.  
The Bag ADT is implemented as a generic class that can store any item object type.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 1
Directory: [Critical-Thinking-1](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Data-Structures-and-Algorithms-CSC400/Critical-Thinking-1)  
Program Name: RPG Bag

-------------------------------------------------------------------------------------------

Program Description:   
The program is a simple implementation of a Bag Abstract Data Structure (Bag ADT) in Java.  
The Bag class represents the inventory of an RPG video game player. 
The Bag allows for the storage and management of game items such as Potions, Armor, and Weapons.  
The Bag ADT is implemented as a generic class that can store any item object type.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Discussions 
This repository is a collection of discussion posts from CSC400 - Data Structures and Algorithms    
Directory: [Discussionshttps://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Data-Structures-and-Algorithms-CSC400/Discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

