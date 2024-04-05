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

Final grade: A   %103.27

-----------------------------------------------------------------------------------------------------------------------------

Map description:
The programs are stored in folders named after the corresponding assignment; folders can contain one or more programs. 
The folder’s names number that precedes the assignment name is a chronologic reference, 
with the number ‘12’ representing the oldest and first assignment.

-----------------------------------------------------------------------------------------------------------------------------

Requirement:
c++ 11 or later
I used MS Visiual Studio IDE to creat my programs

-----------------------------------------------------------------------------------------------------------------------------
					           Assignements
-----------------------------------------------------------------------------------------------------------------------------

----------------------
0_final_project
----------------------	

						Ether's Quest

Requirement:

    MS Windows 10, 64 bit
    c++ 11 or later
    SFML (Simple and Fast Multimedia Library) 
    https://www.sfml-dev.org/
    I used MS Visual Studio IDE to create my program.


Class Final Project Prerequisites:

“Your final project is to create an interactive, text-based Choose Your Own Adventure style game based on a movie, 
book or game of your choice. You may use your own idea if you don't want to base it on an existing property.
 If you aren't sure what I mean by Choose Your Own Adventure, see the "Cat Break" image file in this week's module. 
 (Credit to the author, Fox, for the Choose Your Own Adventure.).”

This project goes substantially beyond the Class Final Project Prerequisites; the project is a small c++ window desktop application.

Project description:

Ether’s Quest is a small story-based “D&D game” based on the Innistrad universe. 
Where Ether journeys to save his younger sister Clarabella. 
Clarabella was abducted by the evil vampire lord, Salt, 
to be offered in sacrifice to the demon Iretrat. In exchange for Clarabella’s soul, 
Iretrat will reanimate Pantra, Salt’s lost love, using Clarabella’s blood. 
The sacrifice must be performed on the first day of the Hunter’s moon, 
at the Skirsdag high temple located in Stensia. 
Ether’s journey to save Clarabella will start at his home in Gavony; 
he will travel through the region of Nephalia , Kessig, and Stensia, 
where he will encounter many dangers. Provided that he survives the journey; 
at Skirsdag high temple, he will have to battle 
and defeat both lord Salt and the demon Iretrat to save Clarabella and complete his quest.

***** For more info see the Readme.txt file in the 0_final_project folder *******

-----------------------------------------------------------------------------------------------------------------------------

----------------------
1_battleship_game
----------------------												 

This is ONE assignment divided into TWO parts!  You only should submit one program for this assignment.

1. Battleship Class

Recreate the battleship game we worked on earlier in the term (see Module 4) 
using a Ship class that creates five objects, one for each type of ship.  

The class should have the following member variables:
shipName: 
Each object should be named to reflect the type of ship it is.
numHits: 
The number of hits the ship can take before sinking.

location: 
This should be an int array or vector and stores where on the 10 by 10 grid the ship is placed. 
Think x,y coordinates like in graphing, only you need to store between 2 and 5 sets per ship. 
Check the Reminder at the end for a way to make this easier. 
Make sure none of the ships are placed overlapping each other!
	
hit: 
This should be an array of Boolean variables initialized as false, 
as the ship is hit in each location set the corresponding variable to true, 
when the entire array is set to true, the ship is sunk.

The Ship class should also have the following functions:
Both a default and overloaded constructor.
Accessor (get) and Mutator (set) functions for each variable.

shipHit: 
This function should be called if a ship is hit, it should display the name of the ship, 
how many times it has been hit or if that was the final hit, that the ship has been sunk.

Your program needs to have the following function but it is NOT part of the Class:

displayShipInfo: 
when called this function should display the number of ships sunk, the number of ships remaining, 
which ships have been sunk (by name), which ships are left (by name), 
and which of the ships that have not been sunk have been hit and how many times they have been hit.

2. Battleship Game

Using the class and function you created above, complete the recreation of the battleship game.  
You may need more functions and will likely need more variables than you have created already.  
Create five objects from your class and either assign them random positions, 
have the user input the positions or hard code the positions yourself, 
the choice is yours.

If you have the user input the positions or assigned them randomly, 
then have the computer attempt to sink your ships with random guesses; if you assigned the ship positions, 
have the user guess until all ships are sunk.

Regardless of how the game is played display a message when all the ships have been sunk indicating the game is over.

Remember: The spaces on a battleship board can be numbered from 1-100 (0-99) starting in the upper left corner. 
Don't allow guesses or random numbers outside this range.  
I recommend placing the ships yourself (hard coded) and having the user guess.


******** Please Read ********

This programm will only run on Window OS.

Rules for BattleShip (a Milton Bradley Game)
https://www.cs.nmsu.edu/~bdu/TA/487/brules.htm

Game:
The computer randmonly positions 5 ships on a 10 by 10 grid.
The user has to find all the ships in the grid, and sink them to win the game.

-----------------------------------------------------------------------------------------------------------------------------

----------------------
2_file_information
----------------------												 

You need to submit the entire project FOLDER for both assignments!

1. Fortune Teller

Using the "FORTUNES.txt" file in the modules tab, 
create a program that reads the fortunes from the text file into either a vector or an array (strings or characters).  
Display a prompt for the user to enter the number of their birth month (1 == January, 2 == February, etc.), and then generate a random fortune, 
as being the current fortune for people born in the named month.

Example:
Enter the number of your birth month: 8
Fortune for people born in August: "If it looks back at you from the plate, don't eat it."

INPUT VALIDATION:
Make sure that the program can find the file and read the contents prior to importing the information.
Do not accept numbers less than 1 or greater than 12 for the birth month.


2. Driver's License Exam Re-visit

Using the file "correctanswers.txt" populate the correct answers array for the drivers license exam program.  
Create a text file with the student answers, one letter per line (see the correct answers file for an example).  
Import the student answers from your text file into the program.  After the student answers have been imported, 
the program should compare the student answers to the correct answers and display a message indicating whether the student passed or failed the exam.  
(At least 15 correct answers are required to pass the exam.) Additionally, the total number of correctly answered questions,
and a list showing the question numbers of the questions the student got wrong should all be written to a new text file.

Turn in your .cpp file, student answers file, and final report text file as your submission; you do NOT need to turn in a screen capture.

NOTE:
You do not need an output text file for the first program. You do not need a screen capture for the second program.
When working with output files, some times you need to create the file yourself before the IDE can find it.  
Also the text files need to be in the same folder as your project. 
If you forget to include the correctanswer.txt or FORTUNES.txt files I have copies of those, 
but if you don't submit your student answer text file your program will not work.

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

-----------------------------------------------------------------------------------------------------------------------------

---------------------------------------
4_us_presidents_sorting_searching_pt-2
---------------------------------------

President of the United States Information Dump

Using the link below to an external site. website, record information on past U.S. 
Presidents into a set of arrays (you may also use vectors, but they are more difficult to sort).
https://www.whitehouse.gov/about-the-white-house/presidents/

- potus_Last_Name (string): The President's last name. <- This is what you will sort by.
- potus_First_Name (string): The President's first name. <- Do NOT sort by this. 
  DO remember to include this when displaying the names. 
  If a middle initial is needed it should go here. (George H. W. Bush vs. George W. Bush)
- potus_Terms (int): The number of terms the President served.
- potus_FirstYear (int): The year the President started serving his term in office.  <- Note that this is NOT the same as the year the President was elected. 
  President Biden was elected in 2020, but his term started in 2021. (<- Most recent example.)

All of this information should be hard coded, there should be no user input up to this point.

You will need to have options for the user to do the following:

Display the list of Presidents, in order, first to most recent, in groups of 10.  i.e. Display Washington through Tyler, 
pause for user to hit a key, then display Polk through Garfield, etc. Yes, you need to list Cleveland twice.
Sort the list of names in Alphabetical order and display it in groups of 10 Presidents at a time. Again, 
display 1 through 10, wait for key press, then 11 through 20, etc. (i.e. Quincy-Adams should be sorted as a 'Q' not as an 'A'.)
Show only Presidents who served 1 term.
Show only Presidents who served 2 or more terms. (Yes, we had one 4 term President. (Yes, you should know that by now if you are from the U.S.))
Show a list of the Presidents and the year they started serving their term. Again, you need to show Cleveland twice.
You need to use functions for each of these options. At least one function for each one. That's five different functions just for the displays, 
plus those you'll need for the sorting and the searching.

Display a menu of the options that the user can choose from. Have the program clear the screen and return to the menu after each option is done.

--Don't forget an option to exit the program.

Note: 
There should be no input from the user other than their menu choices. All the Presidential data should be hard coded.

Hint: 
You can clear the screen by simply printing endl 30-50 times. Use a loop.
Input Validation: 
Do not accept options not included in the menu. (A, B, C or 1, 2, 3 etc.)
Screen Capture: 
Screen capture should show the first 20 presidents from the default display.

Note: 
Make sure the information you are displaying is accurate. 
Yes, there are Presidents I am not that fond of either, but that is no excuse for getting the information wrong.

Warning: 
The instructor just so happens to have his undergrad degree in U.S. History and will notice wild inaccuracies.

*** Please read  ***

This programm will only run on Window OS
It is important to note that:
Not all the Presidents served full terms.
Also, the US has/had 46 presidents but only 45 individuals served as Presidents
this is due to President Grover Cleveland who served 2 nonconsecutive terms, i.e., he is the 22sd and 24th President

Ter completion types:
- Full Term - the President completed a full term.
- Unfinished Term - the President did not complete a full term (passed away, assassinated, resigned).
- Partial Term - the President was the vice president and became the President after the elected President did not finish his term.

I utilized some of the information from the following website 
https://historyinpieces.com/research/presidential-inauguration-dates

-----------------------------------------------------------------------------------------------------------------------------

--------------------------
5_functions_madlib
--------------------------

This is make - up work and is worth up to 40 points.It is NOT required.
Points will be earned entirely at the instructor's determination of program quality.

Write a program that gets words or phrases(as strings) from the user.
You will use the variables this data is stored in to insert and replace words or phrases in the lyrics of a song or parts of a poem.
The song or poem is of your own choice.It should be school friendly, if you need me to explain that, email / message me.

You should get at least two, but no more than five, of each of the following from the user :

nouns(things)
verbs(actions)
adjectives(description words)

You will need a function to get each of these different types of words. (That brings our total function count so far to 4; these three plus main.)

You will need to use a function to display the lyrics of the song as well as the name of the artist you most prefer to have sing it.
There can be lyrical differences between different artists.Include a URL to the lyrics as a comment in this function. (This brings our function count to 5.)
(Places like genius.com, azlyrics.com, songlyrics.com are best for this.
	Wikipedia is a 100 % no go.I will hit you with the Wikipedia penalty if you use it.
	Yes, even including a link to Wikipedia as a comment will invoke that penalty.)
	Pass the data you have gotten from the user to another function that displays your madlib.
	Examples of the output are below. (This brings our function count to 6. This is the minimum number of functions you need to get credit.)
	Separate the original lyrics from the madlib using a line of symbols of your choice. (*&# _ - etc.)

	Song / Poem Requirements :

School friendly.
Songs must be at least 1 verse plus the chorus.
Poems should be somewhat recognizable even after the minimum of 6 items have be injected. "Somewhat" is being left to your determination.
Do not use a haiku.
Do not expect any rhyme scheme from whatever you pick to be preserved.

*** Please read ***
This programm will only run on Window OS
Song :
"Come Fly With Me"
Frank Sinatra Lyrics
I had it the sound track just for fun

lyrics from azlyrics.com
https ://www.azlyrics.com/lyrics/franksinatra/comeflywithme.html

-----------------------------------------------------------------------------------------------------------------------------

--------------------------
6_sorting_searching_pt-1
--------------------------

1. Sales

A small yard supply store has recently started selling new items. 
Write a program that lets the owner track which items are selling well and which ones are not. 
The items are as follows: clock radios, grills, umbrellas, patio furniture, holiday decorations, candy bars, garden gnomes and pet supplies.
The program should use two parallel arrays; 
an array of strings that holds the product names and an array of integers that holds the number of items sold during the past month for each type.  

The names should be stored in the array at the time the name array is created. Simply initialize the array with those items.  
The program should prompt the user to enter the number of items sold for each type.  
Once the sales data has been entered, the program should produce a report that displays sales for each item type, 
total sales, and the names of the highest selling and lowest selling products.
Yes, I am well aware that grills will not sell as well as candy bars. This assignment is not designed to reflect reality. 
*If you wish to use vectors in place of the arrays you may, be aware that vectors are much more difficult to sort.

INPUT VALIDATION: 
Do not accept negative values for the number of items sold.

Output Example:

	My Lawn Co. Sales Figures:

	--------------------------------

	Clock Radios:              30 units sold
	Grills:                     7 units sold
	Umbrellas:                 12 units sold
	Patio Furniture:           10 sets sold
	Holiday Decorations:       28 units sold
	Candy Bars:               132 units sold
	Garden Gnomes:             17 units sold
	Pet Supplies:              39 units sold

	--------------------------------

	Total Items Sold: 275 Units Sold

	--------------------------------

	Highest Selling Product: Candy Bars
	Lowest Selling Product:  Grills

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

-----------------------------------------------------------------------------------------------------------------------------

----------------
8_functions
----------------

Complete the following programs; take screen captures of your output, package them with your .cpp source files and submit in a zipped folder.

1. Celsius Temperature Table

The formula to convert a temperature from Fahrenheit to Celsius is:
C = (F - 32) * 5/9   < With F being the Fahrenheit temp and C being the Celsius temp.>
Write a function called Celsius that accepts the Fahrenheit temperature as an argument. 
 The function should return the temperature after it has been converted to Celsius.  
Demonstrate the function by putting it in a loop that displays first the Fahrenheit temperature 
and then the Celsius equivalent temperature every 6 degrees between 32 degrees Fahrenheit and 92 degrees Fahrenheit.  
Use proper headings and spacing to make the output easy to read.

2. Winning Sales Division

Write a program that determines which of a company's eight divisions 
(Northeast, Southeast, NorthCentral, SouthCentral, NorthPlains, SouthPlains, Northwest, Southwest) 
had the greatest sales for a quarter. The program should include the following two functions, both of which will be called by main.
double getSales( ) is passed the name of a division; 
it will ask the user for a division's quarterly sales figure, validate that input, then return it. 
This function should be called once for each division.
void findHighest( ) is passed all eight sales totals.  
It will determine which is the largest and print the name of the corresponding sales division and sales figure.

INPUT VALIDATION: 
Do not accept values lower than $0.01 for the sales figure.

3. Paint Job Estimator

A painting contractor has determined that for every 115 square feet of wall space, 1 gallon of paint and 6 hours of labor will be required.  
The company charges $54.00 per hour for labor.  
Write a modular program that allows the user to enter the number of rooms to be painted, the price of paint per gallon, 
and then the square footage of each room.  The program should then display the following information properly spaced and labelled:

- The number of gallons of paint required.
- The total hours of labor needed. (This is a union job, so assume they'll be taking breaks and not working more than 10 hours per day. 
Divide up into working days if necessary.)
- The total cost of the paint.
- The labor charges.
-The total cost of the paint job.

INPUT VALIDATION: 
Do not accept a value lower than 1 for the number of rooms; all rooms must have at least 85 square feet of wall space to be painted. 
The average cost of the paint is $32.50 per gallon, do not accept values lower 75% of that price or greater than 1.25 times that price. 

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

-----------------------------------------------------------------------------------------------------------------------------

----------------
11_conditionals
----------------

This is a two part assignment: Part 1 consists of creating a flowchart diagram; part 2 will be writing a program to match that diagram.

Part 1:  Create a flowchart using the tools in the Useful Resources module of how you should dress based on the following weather conditions: 
Temperature over 80 degrees Fahrenheit (temp>80); 
Temperature over 50 degrees Fahrenheit (temp<80 &&temp>50); 
Temperature below 32 degrees Fahrenheit (temp<32); Raining (note that if the temperature is below 32 degrees Fahrenheit 
and it is raining then we consider that to be snowing). 
The check for rain can be a simple yes or no ('y' or 'n').

Part 2: Based on your flowchart, create a C++ program that follows the same process. 
You will need to use conditional statements for this program. 

When the program is complete, run the program 2 times with different criteria, 
take screen captures of BOTH sets of results! (You should be asking the user for the temperature and whether or not it is raining.)

Package your screen captures, flowchart and .cpp file into a zipped folder and turn that in.

-----------------------------------------------------------------------------------------------------------------------------

----------------
12_math
----------------

1. Box Office

A movie theater only keeps a percentage of the revenue earned from ticket sales, the rest of the money goes to the movie distributor.  
Write a program that calculates the theater's gross (overall amount earned) 
and net (amount after the distributor's cut) box office profit for one night.  
The program should ask for the name of the movie and how many adult tickets and child tickets were sold.  
Adult tickets cost $12.00 each; seniors and children tickets cost $9.00 each. Students and Military with valid ID are $10.00 each.  
The theater keeps 20% of the ticket sales, the remainder goes to the distributor.  
Have the program display the information in the same format as the example below:

Movie Name:                     " Movie Name "
Adult Tickets Sold:                 ##
Senior/Child Tickets Sold:          ##
Student/Military Tickets Sold:      ##
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

-----------------------------------------------------------------------------------------------------------------------------