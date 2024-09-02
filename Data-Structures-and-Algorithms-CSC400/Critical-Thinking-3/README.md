-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 3
Name: Asymptotic Analysis Exercises

Grade:  

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

int sum = 0;  
for (int counter = n; counter > 0; counter = counter - 2)  
      sum = sum + counter;  

Exercise 2)    
Suppose your implementation of a particular algorithm appears in Java as follows:  

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

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 


