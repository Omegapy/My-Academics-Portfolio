# Foundation of Operating Systems – CSC507 

---

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omega.py)      

created date: 05/10/2026  

---

Project Description:    
This repository is a collection of assignments from CSC507 – Foundation of Operating Systems at Colorado State University Global - CSU Global.  

**CSC507 - Foundation of Operating Systems**.   
This course will introduce you to the ins and outs of Computer Operating Systems. You will learn how and why operating systems evolved from the simple batch systems in the early days, to the advanced and varied systems we use today. You will understand the essential elements of operating systems, including processors, memory, and file management. This course will use both theory and practical application of the information learned.

**Course Learning Outcomes:**     
1. Identify factors that can affect the lower bound of a solution.
2. Discuss the use of abstract data types in software development.
3. Create an application that demonstrates optimal performance.
4. Implement a recursive solution to solve a specific problem.
5. Develop an application that makes use of appropriate data structures.
6. Evaluate the Big-O runtime of an algorithm.

---

Foundation of Operating Systems CSC507   
Professor: Dr. Joseph Issa  
Spring C (26SC) – 2026   
Student: Alexander (Alex) Ricciardi   

Final grade: 

---

My Links:

<a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" align="left" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></a>
<a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" align="left" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></a>

[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/@AngryOwl-AI)
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)

<a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></a>
<a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></a><br>
   
---

Requirements:  
- Linux OS - Ubuntu Desktop 24.04.1 LTS
- Windows 11
- Python

---

#### Project Map  

- [Portfolio Milestone Module 2](#portfolio-milestone-module-2)
- [Critical Thinking Module 2](#critical-thinking-module-2)
- [Critical Thinking Module 1](#critical-thinking-module-1)
- [Discussions](#discussions)

---
---

## Portfolio Milestone Module 2
Directory: [Portfolio-Milestone-Module-2](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC-507-Foundation-of-Operating-Systems/Portfolio-Milestone-Module-2)   

---
---

**Assignment:**

**This assignment is a Portfolio Milestone for Module 2.**

Portfolio Milestone Project: Bash and Python Scripting

Using Python Programming language
In your Linux installation, use Bash, or a Linux Shell of your choice, to do the following:

1. Generate a random number: echo $RANDOM
2. Output a random number into a file called file1.txt: echo $RANDOM > file1.txt
3. Append another random number to the end of this file: echo $RANDOM >> file1.txt
4. Remove file1.txt: rm file1.txt
5. Create a script called numbers.sh, that does this one thousand (1000) times, using the “for” loop.
6. Make the script executable: chmod +x numbers.sh
7. Run the script: ./numbers.sh

If you are not familiar with Linux Shell scripting, review the following videos:

Simpson, S. (2025, July 1). Learning bash scriptingLinks to an external site. [Video]. LinkedIn Learning. 

Simpson, S. (2025, July 1). Working with while and until loopsLinks to an external site. [Video]. LinkedIn Learning.

You should now have a file called file1.txt containing 1,000 lines, with each line being a random number.

Create a Python program to perform this task, to create file2.txt. You should now have 2 files: file1.txt & file2.txt, each containing 1,000 lines, with each line being a random number.

Do a word and line count on these programs, scripts, and text files (feel free to create a new folder(s) to store these, if you prefer a certain level of organization.)

wc *

Take a screenshot of the files and their word/line counts and submit to the instructor.

### For context

**Portfolio Project** Working with Big Data using Multithreading
The goal of this project is to use the concepts taught in this course to develop an efficient way of working with Big Data.

You should have 2 files in your Linux system: hugefile1.txt and hugefile2.txt, with one billion lines in each one. If you do not, please go back to the Module 7 Portfolio Reminder and complete the steps there.

Create a program, using a programming language of your choice, to produce a new file: totalfile.txt, by taking the numbers from each line of the two files and adding them. So, each line in file #3 is the sum of the corresponding line in hugefile1.txt and hugefile2.txt.

For example, if the first 5 lines of your files look as follows:

$ head -5 hugefile*txt

==> hugefile1.txt <==

4131

29929

6483

7659

25003

==> hugefile1.txt <==

8866

19171

11029

4889

27069

then the first 5 lines of totalfile.txt look like this:

$ head -5 totalfile.txt

12997

49100

17512

12548

52072
Because the files of such large sizes cannot be read into memory in their entirety at the same time, you need to use concurrency. Reading the files one line at a time will take a long time, so use what you have learned in this course to optimize this process. Be sure to record the amount of time it takes for each version of your program to complete this task.

Optimize the program by using threads, so that you benefit from multiple cores in your CPU. Create a multithreaded program, where each thread works on the next chunk of the file.

Now, break up hugefile1.txt and hugefile2.txt into 10 files each, and run your process on all 10 sets in parallel. How do the run times compare to the original process?

Explain your methods and results in detail. What conclusions can you make about the different methods of optimizing large file processing? How has the information that you learned in this course helped you to accomplish this task?

Your paper should be 2-3 pages in length and conform to CSU Global Writing Center. Include at least 3 references in addition to the course textbook. The CSU Global Library is a good place to find these references. You can access the Writing Center and Library by clicking on the links in the course navigation panel.

**Portfolio Reminder Module 8**

From the previous you should have 2 files in your Linux system: file1.txt and file2.txt, with one million lines in each one. Use them to create 2 files with one billion lines each: hugefile1.txt and hugefile2.txt. Your script might look as follows:

#!/bin/bash
for i in {1..1000}
do
  cat file1.txt >> hugefile1.txt
  cat file2.txt >> hugefile2.txt
done

Run this script, then verify that you now have 2 files with one billion lines each:

wc -l hugefile*txt

---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking Module 2
Directory: [Critical-Thinking-Module-2](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC-507-Foundation-of-Operating-Systems/Critical-Thinking-Module-2)   
Title: Critical Thinking Module 2 - Process Management

---
---

**Assignment:**

Compare and Contrast Process Management Utilities of Linux OS with Windows OS
Process management utilities in the Linux OS involve using shell commands to perform various tasks related to controlling, monitoring, and interacting with running processes. In contrast, Windows OS offers the Task Manager, a graphical tool that provides an overview of running processes, system performance, and resource usage.

Perform at least five tasks on each OS using these two process management utilities. In your Critical Thinking Assignment, prepare a summary to describe the results, including screenshots, in your paper. Compare their ease of use and ability to intervene in a process.

**Grading Criteria**  
- Your paper should be 2-3 pages in length, not including the cover page and references page.
- Your paper must be formatted according to APA guidelines in the CSU Global Writing Center (available in the left-hand navigation panel).
- Your claims should be supported by evidence.  Include at least 3 credible references. The CSU Global Library (available in the left-hand navigation panel) is a good place to find these references.
- All references must be cited in the text and listed on the references page, according to APA formatting.

---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking Module 1
Directory: [Critical-Thinking-Module-1](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC-507-Foundation-of-Operating-Systems/Critical-Thinking-Module-1)   
Title: Critical Thinking Module 1 - Linux Shell Commands

---
---

**Assignment:**

Perform Shell Commands to Understand Elements of Computers
In your Linux computer, use shell commands to determine the specifications of the four main structural components of your computer. The four components to investigate are the following:

- Processor
- Main memory
- I/O modules
- Storage devices (e.g., hard drives, solid-state drives)

Explain the commands you use and provide descriptions of the results. Additionally, include screenshots of the results in your paper.

Note: To complete this assignment, you need to set up a Linux OS on your computer. To do this, follow the instructions in Module 1: Portfolio Reminder.

**Grading Criteria**  
- Your paper should be 2-3 pages in length, not including the cover page and references page.
- Your paper must be formatted according to APA guidelines in the CSU Global Writing Center (available in the left-hand navigation panel).
- Your claims should be supported by evidence.  Include at least 3 credible references. The CSU Global Library (available in the left-hand navigation panel) is a good place to find these references.
- All references must be cited in the text and listed on the references page, according to APA formatting.

---

[Go back to the Project Map](#project-map)  

----
----

## Discussions 
This repository is a collection of discussion posts from CSC506 – Design and Analysis of Algorithms  
Directory: [Discussions]([...])

---

[Go back to the Project Map](#project-map)


