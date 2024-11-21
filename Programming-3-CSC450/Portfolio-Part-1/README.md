-----------------------------------------------------------------------------------------------------------------------------
# Portfolio Part-1  
Program Names: User Input to File in Reverse  

Grade:  

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
-	The simple C++ console application is in file PF1-Thread Counting Synchronization.cpp  
-	The program follows the following SEI CERT C/C++ Coding Standard:
-	CON50-CPP. Do not destroy a mutex while it is locked
-	CON51-CPP. Ensure actively held locks are released on exceptional conditions
- -CON52-CPP. Prevent data races when accessing bit-fields from multiple threads  
- -CON54-CPP. Wrap functions that can spuriously wake up in a loop  
- -CON55-CPP. Preserve thread safety and liveness when using condition variables  
- -ERR50-CPP. Do not abruptly terminate the program  
- -ERR51-CPP. Handle all exceptions  
- -ERR55-CPP. Honor Exception Specifications  
- -STR50-CPP. Guarantee that storage for strings has sufficient space  
- -STR51-CPP. Do not attempt to create a std::string from a null pointer  
- -STR52-CPP. Use valid references, pointers, and iterators t reference elements of a basic_string  

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- Document.pdf  
	- Program Explanation 
	- Results and test scenarios   
	- Screenshots  
- README.md – Markdown file, program information    
- PF1-Thread Counting Synchronization.cpp – Thread Counting Synchronization    

-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 


