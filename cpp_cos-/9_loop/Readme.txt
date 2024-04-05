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
9_loops
----------------

Complete the following programs; when finished take a screen capture of the output from your running program and package it with your .cpp file. 
Submit a zipped folder with your work.

1. Hotel Occupancy

Write a program that calculates the occupancy rate for a hotel; 
the program should start by asking the user for the number of floors in the hotel.  
A for loop should then iterate once for each floor.  In each iteration, 
the loop should ask the user for the number of rooms on the floor and how many of them are occupied.  After all the iterations, 
the program should display how many rooms the hotel has, how many of them are occupied, how many are unoccupied, 
and the percentage of rooms that are occupied. 
The percentage may be calculated by dividing the number of occupied rooms by the total number of rooms.

NOTE: It is traditional that no hotel have a 13th floor!  The loop should skip the entire 13th iteration.

INPUT VALIDATION:  
Do not accept values less than 13 for the number of floors.  
Do not accept a number less than 10 or greater than 24 for the number of rooms per floor.

2.  Random Number Guessing Game

Write a program that generates a random number between 1 and 100 and asks the user to guess what the number is.  
If the user's guess is higher than the random number, the program should display "Too high, try again."  
If the user's guess is lower than the random number the program should display "Too low, try again."  
The program should use a do-while loop that repeats until the user guesses the number correctly.  
The program should also employ a while loop that keeps track of the number of guesses made by the user and, 
once the user guesses the number correctly, displays the number of guesses the user made.
