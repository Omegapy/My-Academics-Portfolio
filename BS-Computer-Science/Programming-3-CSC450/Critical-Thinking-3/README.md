-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 3  
Program Names: Integer Pointers  

Grade: 93% A-

-----------------------------------------------------------------------------------------------------------------------------

CSC450 – Programming III – C++/Java Course  
Professor: Reginald Haseltine
Fall D Semester (24FD) – 2024  
Student: Alexander Ricciardi  
Date: 10/27/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- C++23  

-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:    

Integer Pointers Program  
Demonstrate an understanding of basic C++ programming concepts by completing the following:  
•	Program: Create a C++ program that asks the user to enter three integer values as input. Store the values into three different variables. For each variable, create an integer pointer to dynamic memory. Display the contents of the variables and pointers. In your program, be sure to use the new operator and delete operators to management memory.  

Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and your GIT repository in a single document.

-----------------------------------------------------------------------------------------------------------------------------

Programs Descriptions:  

The program is a small procedural C++ program that prompts a user to enter three integer values,
validates the input values as integers and stores the values using raw pointers.

Note:
- The standard integer is typically 4 bytes, it is platform-dependent.
- The Program accepts whitespaces to be entered before and/or after the integer value.
- The program follows the following SEI CERT C/C++ Coding Standard:
    - EXP34-C. Do not dereference null pointers
    - EXP53-CPP. Do not read uninitialized memory
    - ERR50-CPP. Do not abruptly terminate the program
    - ERR51-CPP. Handle all exceptions
    - ERR56-CPP. Guarantee exception safety
    - ERR57-CPP. Do not leak resources when handling exceptions
    - MEM50-CPP. Do not access freed memory
    - MEM51-CPP. Properly deallocate dynamically allocated resources
    - MEM57-CPP. Avoid using default operator new for over-aligned types
    - INT50-CPP. Do not cast to an out-of-range enumeration value
    - STR50-CPP. Guarantee that storage for strings has sufficient space
      for character data and the null terminator
  

⚠️ My notes:  
- The simple C++ console application is in file CTA-3-integerPointers.cpp
- It is best practice to utilize smart pointers like ‘std::unique_ptr’ or ‘std::shared_ptr’ which automatically manage memory. However, to demonstrate the use of the new and delete operators to manage memory as required by the assignment, the program uses regular raw pointers. 
- Instead of using ‘std::cin’ and ‘int’ to capture and store user inputs, the program uses ‘std::getline’ and ‘std::string’. This allows the program to have more control and flexibility over input validation. For example, the program allows whitespaces to be entered before and/or after the integer value.
- Integer can be negative. The standard integer size, in C++, is typically 4 bytes and is platform-dependent.
- The program follows the following SEI CERT C/C++ Coding Standard:
     - EXP34-C. Do not dereference null pointers
     - EXP53-CPP. Do not read uninitialized memory
     - ERR50-CPP. Do not abruptly terminate the program
     - ERR51-CPP. Handle all exceptions
     - ERR56-CPP. Guarantee exception safety
     - ERR57-CPP. Do not leak resources when handling exceptions
     - MEM50-CPP. Do not access freed memory
     - MEM51-CPP. Properly deallocate dynamically allocated resources
     - MEM57-CPP. Avoid using default operator new for over-aligned types
     - INT50-CPP. Do not cast to an out-of-range enumeration value
     - STR50-CPP. Guarantee that storage for strings has sufficient space
       for character data and the null terminator

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- Document.pdf  
	- Program Explanation 
	- Results and test scenarios   
	- Screenshots  
- README.md – Markdown file, program information   
- CTA-3-integerPointers.cpp – The Integer Pointers Program  

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


