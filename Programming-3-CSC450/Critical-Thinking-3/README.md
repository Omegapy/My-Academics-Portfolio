-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 3  
Program Names: Integer Pointers  

Grade:  

-----------------------------------------------------------------------------------------------------------------------------

CSC450 – Programming III – C++/Java Course  
Professor: Reginald Haseltine
Fall D Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
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

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 


