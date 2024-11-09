-----------------------------------------------------------------------------------------------------------------------------
# Programming-3 (c++, Java) – CSC450  
-----------------------------------------------------------------------------------------------------------------------------

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omegapy)      

created date: 10/04/2024  

-----------------------------------------------------------------------------------------------------------------------------

Projects Description:    
This repository is a collection of c++ and Java programs from CSC450 – Programming-3 Course at Colorado State University Global - CSU Global.  

-----------------------------------------------------------------------------------------------------------------------------

CSC450 – Programming III – C++/Java Course    
Professor: Reginald Haseltine  
Fall D (24FD) – 2024   
Student: Alejandro (Alex) Ricciardi   

Final grade:  

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-21  
- c++  

-----------------------------------------------------------------------------------------------------------------------------
My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)    

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map  

- [Critical Thinking 5](#critical-thinking-5)
- [Critical Thinking 3](#critical-thinking-3) 
- [Critical Thinking 2](#critical-thinking-2) 
- [Critical Thinking 1](#critical-thinking-1)   
- [Discussions](#discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 5  
Directory: [Critical-Thinking-5](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Programming-3-CSC450/Critical-Thinking-5)  

Programs Names: User Input to File in Reverse   

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

This program prompts the user to enter a string (sentence) and appends it to the "CSC450_CT5_mod5.txt" file without deleting existing data.
The program also validates the user input, trimming leading and trailing whitespaces from inputted text.
It then reverses each line of "CSC450_CT5_mod5.txt" by reversing the characters in each line while maintaining the order of the lines, and stores the reversed content in "CSC450-mod5-reverse.txt"
  

⚠️ My notes:  
- The simple C++ console application is in file CTA-5-Input-to-file.cpp  
- The program follows the following SEI CERT C/C++ Coding Standard:  
     - STR50-CPP. Guarantee that storage for strings has sufficient space for character data and the null terminator  
     - STR52-CPP. Use valid references, pointers, and iterators to reference elements of a basic_string  
     - STR53-CPP. Range check element access  
     - FIO50-CPP. Do not alternately input and output from a file stream without an intervening positioning call  
     - FIO51-CPP. Close files when they are no longer needed  
     - ERR50-CPP. Do not abruptly terminate the program  
     - ERR51-CPP. Handle all exceptions  
     - ERR56-CPP. Guarantee exception safety  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)
-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 3  
Directory: [Critical-Thinking-3](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Programming-3-CSC450/Critical-Thinking-3)  

Programs Names: Integer Pointers   

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

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

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)


-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 2  
Directory: [Critical-Thinking-2](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Programming-3-CSC450/Critical-Thinking-2)  

Programs Names: Two String Input Concatenated  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

The program takes two strings inputted by the user, concatenates them, 
and prints the resulting concatenated string. 
The input strings and their concatenation are safely handled using C++'s ‘std::string’ class, 
which automatically manages memory, preventing buffer overflows.
The program also uses ‘std::getline’ for string inputs, ensuring strings with spaces are fully captured. 
The program repeats the process three times, accepting two string inputs and concatenating them 
to test if varying string lengths are handled securely. 

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Critical Thinking 1  
Directory: [Critical-Thinking-1](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Programming-3-CSC450/Critical-Thinking-1)  

Programs Names:     
   Secure Person Management System – CT1-Person.cpp  
   Correct Syntax Corrected CSC450_CT1_mod1-1 - CSC450_CT1_mod1-1.cpp  
   Correct Syntax Corrected CSC450_CT1_mod1-2 - CSC450_CT1_mod1-2.cpp

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

1. Secure Person Management System  
This program is a small procedural C++ application that manages an array of Person objects.   
It tests and implements secure coding practices to mitigate vulnerabilities such as:  
	- Buffer overflows  
	- Integer overflows  
	- Incorrect type conversions   
	- Null pointer dereferencing  

Note: Visual Studio 2022 IDE will give a warning when using ‘strncpy’,  
and you'll need to add the line ‘#define _CRT_SECURE_NO_WARNINGS‘ to compile the program.  
Another alternative is using ‘td::string’ or ‘strncpy_s’ for a safer implementation.  
However, to showcase the vulnerability of buffer overflow when using a char array, this program uses ‘strncpy’.  

2. Correct Syntax Corrected CSC450_CT1_mod1-1  
This programm showcases the correct code syntaxes for the given C++ program, CSC450_CT1_mod1-1.cpp.

3. Correct Syntax Corrected CSC450_CT1_mod1-2  
This programm showcases the correct code syntaxes for the given C++ program, CSC450_CT1_mod1-2.cpp.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Discussions 
This repository is a collection of discussion posts from CSC450 – Programming-3   
Directory: [Discussions](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Programming-3-CSC450/Discussions)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)

