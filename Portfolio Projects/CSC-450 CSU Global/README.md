-----------------------------------------------------------------------------------------------------------------------------
# Portfolio Project
Program Names: 
- Thread Counting Synchronization (C++)
- Thread Counting Synchronization (Java)

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omegapy)  

Grade:  100% A

-----------------------------------------------------------------------------------------------------------------------------

CSC450 – Programming III – C++/Java Course  
Professor: Reginald Haseltine  
Fall D (24FD) – 2024  
Student: Alexander (Alex) Ricciardi  
Date: 12/01/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-21  
- C++  

-----------------------------------------------------------------------------------------------------------------------------

The Assignment Directions:  

The assignment has two parts:

-----------------------------------------------------------------------------------------------------------------------------

Part-1:  

Requirements:  
- C++17

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

Part-2:

Requirements:  
- Java Se 21  

Portfolio Project Part II 
Concurrency Concepts
For your Portfolio Project, you will demonstrate an understanding of the various concepts discussed in each module.  For the second part of your Portfolio Project, you will create a Java application that will exhibit concurrency concepts.  Your application should create two threads that will act as counters. One thread should count up to 20. Once thread one reaches 20, then a second thread should be used to count down to 0.  For your created code, please provide a detailed analysis of appropriate concepts that could impact your application.  Specifically, please address:  
•	Performance issues with concurrency  
•	Vulnerabilities exhibited with use of strings  
•	Security of the data types exhibited.  
Submit the following components to your GIT repository in a single   document:  
•	Word document with appropriate screenshots of your program executing, program analysis responses, and source code in the Word file.  
•	Submit your .java source code file(s).  If more than 1 file, submit a zip file.  
•	Provide a detailed comparison between the performance implementations between the Java and C++ versions of your applications.  Which implementation may be considered less vulnerable to security threats and why? Your detailed comparison should be 3-4 pages in length. Any citations should be formatted according to guidelines in the CSU Global Writing Center (located in the course navigation menu).  

To receive full credit for the packaging requirements for your Module 8 Portfolio Project assignment you must:  
1) Put your Java source code in .java text files. Note that I execute all your programs to check them out.  
2) In a Word or PDF "documentation and analysis" file, labeled as such, put a copy of your Java source code and execution output screen snapshots. This week this regular documentation file must also include a detailed analysis write-up of the important concepts of concurrency with Java to cover in detail performance issues, string vulnerabilities, and security of data types.  
3) Some positive evidence that you've definitely stored your source code in a GitHub repository on GitHub.com.  
4) Include a separate 3-4 page APA Edition 7 paper comparing the performance and security differences between C++ and Java multi-threaded programs. Here's the link to the school's Writing Center for APA Edition 7 requirements -> https://csuglobal.libguides.com/writingcenterLinks to an external site.  
5) Put all 4 of the above files into a single .zip file, and submit ONLY that .zip file for grading. Do not submit any additional separate files.  
 
 -----------------------------------------------------------------------------------------------------------------------------

Programs Descriptions:  

This program demonstrates the use of threads and how to synchronize them using ReentrantLocks and Conditions.  
Thread 1 counts up from 0 to a maximum count, while Thread 2 waits until Thread 1 completes, and then counts down from the maximum count to 0.    

⚠️ My notes:  
- The simple Java console application is in the file ThreadCountingSynchronization.java
- The program follows the following SEI CERT Oracle Coding Standards for Java:
       - STR00-J. Don't form strings containing partial characters from variable-width encodings
       - STR01-J. Do not assume that a Java char fully represents a Unicode code point
       - ERR00-J. Do not suppress or ignore checked exceptions  
       - ERR01-J. Do not allow exceptions to expose sensitive information  
       - ERR03-J. Restore prior object state on method failure  
       - ERR09-J. Do not allow untrusted code to terminate the JVM  
       - LCK00-J. Use private final lock objects to synchronize classes that may interact with untrusted code  
       - LCK08-J. Ensure actively held locks are released on exceptional conditions  
       - THI02-J. Notify all waiting threads rather than a single thread  
       - THI03-J. Always invoke wait() and await() methods inside a loop  
       - TSM00-J. Do not override thread-safe methods with methods that are not thread-safe  

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map  
- Portfolio-Part-1 – Directory for Thread Counting Synchronization (C++)  
- Portfolio-Part-2 – Directory for Thread Counting Synchronization (Java)

-----------------------------------------------------------------------------------------------------------------------------

My Links:   
<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    <span><a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></span>    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)  





