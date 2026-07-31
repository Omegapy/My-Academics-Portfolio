-----------------------------------------------------------------------------------------------------------------------------
# Portfolio Part-1  
Program Names: Thread Counting Synchronization    

Grade:  100% A

-----------------------------------------------------------------------------------------------------------------------------

CSC450 – Programming III – C++/Java Course  
Professor: Reginald Haseltine
Fall D Semester (24FD) – 2024  
Student: Alexander (Alex) Ricciardi  
Date: 11/24/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- C++17  

-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:    

Portfolio Project: Part 1  
For your Portfolio Project, you will demonstrate an understanding of the various concepts discussed in each module. For the first part of your Portfolio Project, you will create a C++ application that will exhibit concurrency concepts. Your application should create two threads that will act as counters. One thread should count up to 20. Once thread one reaches 20, then a second thread should be used to count down to 0. For your created code, provide a detailed analysis of appropriate concepts that could impact your application. Specifically, address:  
•	Performance issues with concurrency  
•	Vulnerabilities exhibited with use of strings  
•	Security of the data types exhibited.  
Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and your GIT repository in a single document.  

To receive full credit for the packaging requirements for your Critical Thinking and Portfolio assignments you must:
1) Put your C++ source code in .cpp text files. Note that I execute all your programs to check them out.  
2) In a Word or PDF "documentation" file, labeled as such, put a copy of your C++ source code and execution output screen snapshots.  
3) Some positive evidence that you've definitely stored your source code in a GitHub repository on GitHub.com.  
4) Include a detailed analysis paper in APA Edition 7 format of the important concepts of concurrency with C++ to cover in detail performance issues, string vulnerabilities, and security of data types. Here's a link to the school's Writing Center where you can find the relevant APA Edition 7 requirements you need to follow -> https://csuglobal.libguides.com/writingcenterLinks to an external site.  
5) Put all your files into a single .zip file, and submit ONLY that .zip file for grading. Do not submit any additional separate files.  

-----------------------------------------------------------------------------------------------------------------------------

Programs Descriptions:  

This program demonstrates the use of threads and how to synchronize them using mutexes and condition variables.  
Thread 1 counts up from 0 to a maximum count, while Thread 2 waits until Thread 1 completes, and then counts down from the maximum count to 0.  
  

⚠️ My notes:  
- The simple C++ console application is in file PF1-Thread Counting Synchronization.cpp  
- The program follows the following SEI CERT C/C++ Coding Standard:
	- CON50-CPP. Do not destroy a mutex while it is locked
	  CON51-CPP. Ensure actively held locks are released on exceptional conditions
	- CON52-CPP. Prevent data races when accessing bit-fields from multiple threads
	- CON54-CPP. Wrap functions that can spuriously wake up in a loop
	- CON55-CPP. Preserve thread safety and liveness when using condition variables
	- ERR50-CPP. Do not abruptly terminate the program
	- ERR51-CPP. Handle all exceptions
	- ERR55-CPP. Honor Exception Specifications
	- STR50-CPP. Guarantee that storage for strings has sufficient space
	- STR51-CPP. Do not attempt to create a std::string from a null pointer
	- STR52-CPP. Use valid references, pointers, and iterators t reference elements of a basic_string  

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- Document.pdf  
	- Program Explanation 
	- Results and test scenarios   
	- Screenshots
- PF-Analysis-Part-1.doc - Program Analysis
- README.md – Markdown file, program information    
- PF1-Thread Counting Synchronization.cpp – Thread Counting Synchronization    

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


