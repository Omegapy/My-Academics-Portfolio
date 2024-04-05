-----------------------------------------------------------------------------------------------------------------------------	
				              c++ Computer Science – 1
-----------------------------------------------------------------------------------------------------------------------------

This repository is a collection of c++ program assignments from COSC 1030 - Computer Science-1 class at Laramie County Community College.
Related links:
https://www.lccc.wy.edu
https://lccc.wy.edu/pathways/sciTechEngMath/computerScienceProgram/index.aspx

-----------------------------------------------------------------------------------------------------------------------------

COSC 1030 – Computer Science 1
Professor: David Durbin
Fall Semester - 2022
Student: Alejandro (Alex) Ricciardi

-----------------------------------------------------------------------------------------------------------------------------

Requirement:
c++ 11 or later
I used MS Visiual Studio IDE to creat my programs

-----------------------------------------------------------------------------------------------------------------------------
					           Assignements
-----------------------------------------------------------------------------------------------------------------------------


----------------
7_array_vector
----------------

Complete the following programs; 
when finished take a screen capture of the output from your running program and package it with your .cpp file. 
Submit your work in a zipped folder.
Yes, you need to do all four of these. Two are about vectors and two are about arrays. Make sure you use the correct type for each program.

1. Full Moons

Using the data provided below, create a program that stores the dates of the full moons for the rest of 2022 in a integer array.  
Have the user enter the current date.
and return the number of days until the next full moon. Full moon information can be found at THISLinks to an external site. web page.  
If the user enters a date that is past the full moon for the current month the program should move to the next month. 
If the user enters a date after December 18th the program should return an error message.

INPUT VALIDATION:  
Do not accept numbers above 31 as the day for the date in March, May, July, August, October or December 
and do not accept a number above 30 for April, June, September or November.  Do not accept a number below 10 or above 12 for the month.

Hint: 
You don't have to use the date entered by the user! (You do still need the user to enter the date though.) 
If you #include <ctime> you can get the current date from the system clock! Search for ctime and getdate() for c++.

2. Get and Display Names

Ask the user for a first name and store it in a vector of strings. 
Do this 10 times.  After the final name, print the names to the screen in reverse order of entry.  
Then do this with a second set of 10 names using a character array. The amount of space allocated for each name should be at least 15 characters. 
(REMEMBER: The final place in an array holds the null terminator; this is not counted as a character!)

3. Revisiting: RNG and You

Flip a coin 500 times and store the information in a vector. Using a for loop, 
get the number of heads flipped and subtract this from the total size of the vector using size().  
Roll two 6-sided dice 1000 times and record the number of times each combination of numbers (2-12) is rolled.  
Display these to the screen with proper labels and spacing.
(Yes, you can just modify your existing code rather than writing it all from scratch. Make sure you get your numbers correct though.)

4. Driver's License Exam

The local Driver's License Office has asked you to write a program that grades the written section of the drive's license exam.  
The exam has 20 multiple choice questions; the correct answers are below:
1. B   2. D   3. A   4. A   5. C   6. A   7. B   8. A   9. C   10. D  
11. B   12. C   13. D   14. A  15. D   16. C  17. C   18. B   19. D   20. A
Your program should store the correct answers (show above) in an array.  
It should ask the user to enter the student's answers for each of the 20 questions and store the answers in a second array.  
After the student answers have been entered, the program should display a message indicating whether the student passed or failed the exam.  
(At least 15 correct answers are required to pass the exam.)  The program should then display the total number of correctly answered questions, 
and a list showing the question numbers of the questions the student got wrong. 

Input Validation: 
Only accept the letters 'A', 'B', 'C' and 'D' as answers.

Note that there is now a criteria in the grading for your comments in the program.  
You need to start commenting about what things do, 
where variables are being used (especially if you are passing them to functions) and your loops/conditionals. 
Switch statements are conditionals. Purposes of functions. I won't be jumping on you hard over this (yet). 
But I will be leaving comments in the rubric for your submissions, so make sure you check that. 
(If you want a sample, look at the paintJobEstimator_Sample file in module 6.) 
Larger programs with longer and more complex loops or conditionals would need more detailed comments around those items, 
and comments for functions as well. 
Functions should have at least a minimal comment detailing what the purpose of the function is.


Gross Box Office Profit:          $ ###.##
Net Box Office Profit:            $ ###.##
Amount Paid to Distributor:       $ ###.##
When finished, take a screen capture of your output and submit both the screen capture and your .cpp file in a zipped folder.

2. Monthly Payments

The monthly payment on a loan may be calculated with the following formula:
Payment = ((Rate * (1 + Rate) ^ N) / (((1 + Rate) ^ N) - 1)) * L     <- Note that no parenthesis comes after L!

Rate is the monthly interest rate, which is the annual interest rate divided by 12. N is the number of payments, 
and L is the amount of the loan. Write a program that asks for these values and displays a report similar to the following example:

Loan Amount:                       $ 10000.00
Annual Interest Rate:                 12%
Monthly Interest Rate:                 1%
Number of Payments:                   36
Monthly Payment:                   $ 332.14
Interest Paid:                     $ 1957.15
Total Amount Paid:                 $ 11957.15

DO NOT use the same numbers I did!  
When finished, take a screen capture of your output and submit both the screen capture and your .cpp file in a zipped folder.


