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