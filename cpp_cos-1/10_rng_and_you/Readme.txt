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
10_rng_and_you
----------------

Using the random number generation that was covered in class, create the following programs:

1. Flip a coin 50 times 
and get the number of heads flipped and the number of tails flipped.  
Roll two 6-sided dice 50 times and record the number of times each combination of numbers (2-12) is rolled.  
Display these to the screen with proper labels and spacing.  

2. A Battleship game board is 10 x 10. 
The PT Boat holds 2 pegs, the submarine and Frigate hold 3, the Battleship 4 and the Aircraft carrier 5.  
Based on this information, use random numbers to figure out the average number of turns 
it will take to sink all five ships over 5 games of Battleship.

Place your screen captures and .cpp files in a folder, zip that folder and submit it.

Hints:

1. This isn't as complicated as it looks, so don't try to make it more complicated than it is.

2. Get a random number between 0 & 1 (see sample program). Track the number of 0's and number of 1's. Do that 50 times.  
Use a switch statement for the dice. (See week 3's menu template for an example of a switch statement.)

3. 10 * 10 == 100.  2+3+3+4+5 == 17.  Get a random number between 1-100 (0-99, don't forget the computer starts at 0!) 
And if that number is between 1 and 17 (0-16) you hit a ship. Each time you get a new random number is 1 turn. Record number of turns. 
Repeat until you get 17 hits. Repeat that process 5 times.  Take the average.
Yes, it will be a long program. Copy/Paste is your friend (make sure the code works before you copy/paste).

4. Have a good weekend.
5. You can use loops if you want.


Loan Amount:                       $ 10000.00
Annual Interest Rate:                 12%
Monthly Interest Rate:                 1%
Number of Payments:                   36
Monthly Payment:                   $ 332.14
Interest Paid:                     $ 1957.15
Total Amount Paid:                 $ 11957.15

DO NOT use the same numbers I did!  
When finished, take a screen capture of your output and submit both the screen capture and your .cpp file in a zipped folder.

