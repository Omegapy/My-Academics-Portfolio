-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 3
Name: Asymptotic Analysis Exercises

Grade:  60/60 A

-----------------------------------------------------------------------------------------------------------------------------

CSC400 – Data Structures and Algorithms - Java Course  
Professor: Hubert Pensado  
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 09/01/2024   

-----------------------------------------------------------------------------------------------------------------------------

Project Description:  
This documentation is part of the Critical Thinking 3 Assignment from CSC400: Data Structures and Algorithms at Colorado State University Global. It consists of a series of exercises designed
to demonstrate the principles of asymptotic analysis. Asymptotic analysis uses the Big-Oh notation.

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

Complete the following exercises. For each exercise, show your work and all the steps taken to determine the Big-Oh for each problem. Partial points cannot be awarded without showing work.  

Exercise 1)  
What is the Big-Oh of the following computation?
<pre>
int sum = 0;  
for (int counter = n; counter > 0; counter = counter - 2)  
      sum = sum + counter;  
</pre>
Exercise 2)    
Suppose your implementation of a particular algorithm appears in Java as follows:  
<pre>
for (int pass = 1; pass <= n; pass++)  
{  
	for(int index  = 0; index < n; index++)  
	{  
		for(int count = 1; count < 10; count++)  
		{  
			. . .   

		} //end for  
	} // end for  
} //end for  
</pre>
The algorithm involves an array of "n" items. The previous code shows only the repetition in the algorithm, but it does not show the computations that occur within the loops.Those computations, however, are independent of "n." What is the order of the algorithm?   
   
Exercise 3)  
Consider two programs, A and B. Program A requires 1000 x n^2 operations and Program B requires 2n operaitons. For which values of n will Program A execute faster than Program B?

Exercise 4)  
Consider an array of length "n" containing unique integers in random order and in the range 1 to n + 1. For example an array of length 5 would contain 5 unique integers selected randomly from the integers 1 through 6. Thus the array might contain 3 6 5 1 4. Of the integers 1 through 6, notice that 2 was not selected and is not in the array. Write Java code that finds the integer that does not appear in such an array. Explain the Big-Oh in your code.

⚠️ My notes:
- Each exercise starts on a new page.  
- 𝑔(𝑛) is the number of primitive operations.  
- The summation properties of a constant.   

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


