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

----------------------
3_creating_your_Class
----------------------												 

1. Date Class

Design a class called Date.  The class should store a date as three (3) integers: month, day, and year.
There should be member functions to print (display) the date in the following formats:

11/01/16
November 1, 2016
1 November, 2016

Demonstrate this class by writing a complete program implementing it.

HINT:
You will need a way to convert the integer for the month into the month name. Think arrays or vectors.

Input Validation:
Do not accept values for the day greater than 31 or less than 1.
Do not accept values for the month greater than 12 or less than 1.


2. Car Class

Write a class named Car that has the following member variables:

yearModel: An int to hold the model year.
type: A string to hold the type of car (sports car, SUV, van, sedan, etc).
make: A string to hold the make of the car. (Jeep Wrangler, Ford Mustang, etc.)
speed: an int to hold the current speed of the car.

In addition, the class should have the following constructor and other member functions:

Constructor:
The constructor should accept the car's model year and make as parameters.
These values should be assigned to the object's yearModel and make member variables.
The constructor should also assign 0 to the speed member variable.

Accessors:
Appropriate accessor functions to get the values stored in an object's yearModel, type, make and speed member variables.

accelerate:
the accelerate function should add 5 to the speed member variable each time the function is called.

brake:
The brake function should subtract 5 from the speed member variable each time the function is called.

Demonstrate the class in a program that creates a Car object, and then calls the accelerate function five times.

After each call to the accelerate function, get the current speed of the car and display it.
Then, call the break function five times. After each call to the break function, get and display the current speed of the car.

Validation check: Do not have the car going at a negative speed at any time.

*** Please read  ***
This programm will only run on Window OS
