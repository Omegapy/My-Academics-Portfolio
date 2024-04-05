
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////
	/*-------------------------------*****************************************----------------------------------
	 |                                *                                      *                                 |
	 |                                *		        Heater's Quest           *                                 |
	 |                                *                                      *                                 |
	 ---------------------------------****************************************----------------------------------*/
	 //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*
	COSC 1030 – Computer Science 1
	Professor: David Durbin
	Student : Alejandro (Alex) Ricciardi
	Due date : 11 / 29 / 2022
	Classes and Objects

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

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*-------------------------------*****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		          Headers                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <cctype> // toupper()
// Console Input & Output Header file, Window OS only
#include <conio.h> // getch()
// Console Window size header file, Window OS only
//#define _WIN32_WINNT 0x0500
//#include<windows.h> // MoveWindow(), SetConsoleTextAttribute()

#include "ship.h"

using namespace std;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *	              Classes                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
//////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*---------------------------------------------------------------------------------------------------------------

Class Ship: please see ship.h and ship.cpp
	Stores ship data.
	Randomly picks the location of the ship.
			Can takes the arguments:
				hit_miss, ship_name, num_hits (num_hits "ship size",
				(can not be more than 7 and not less than 2)
				Note: not passing the argument hit_miss will generate an error.
			Methods:
				Accessors: get_ship_name(), get_num_hits(), get_hit(), get_sunked(), get_location(),
				get_num_ships(), and get_id().
				Mutators: set_ship_name(), set_num_hits(), add_hit(), and set_sunk().
						  No set_location(), set_num_ships(), and set_id() methods are available.

---------------------------------------------------------------------------------------------------------------*/


//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *	        Function Declaration         *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

 /*---------------------------------------
  |                                      |
  |  Clears the console screen.          |
  |  Utilized by press_key_to_continue() |
  |                                      |
  ---------------------------------------*/
void clear(int num_lines); 

/*-----------------------------------
 |                                  |
 |  Waits for a key to be pressed.  |
 |                                  |
 -----------------------------------*/
void press_key_to_continue(int num_lines);

/*---------------------------------------------------------------------------------------
 |                                                                                      |
 |  Sets size of the Console's window                                                   |
 | and position the console in desktop screen utilizing the variable position_console   |
 | Takes the console with width, lenght and position as arguments.                      |
 | position_console values:                                                             |
 | "center", "left_center", "right_center",                                             |
 | "top_left", "top_center", "top_right",                                               |
 | "bottom_left", "bottom_center", "bottom_right".                                      |
 |                                                                                      |
 ---------------------------------------------------------------------------------------*/
void console_size(int screen_width, int screen_lenght, string position_console);

/*--------------------------------------------------------
 |                                                       |
 |  Displays the game banner, utilized by display_grid() |
 |                                                       |
 --------------------------------------------------------*/
void display_banner();

/*--------------------------------------------------------
 |                                                       |
 |  Displays a line of '-'. Utilized by display_grid().  |
 |                                                       |
 --------------------------------------------------------*/
void line();

/*----------------------------------
 |                                 |
 |  Displays the battleship grid.  |
 |                                 |
 ----------------------------------*/
void display_grid(vector<vector<string>> &game_grid, bool &cheat);

/*--------------------------------------------------------
 |                                                       |
 |  Builds a fleet of 5 ships. Returns a fleet vector.   |
 |                                                       |
 --------------------------------------------------------*/
vector<Ship> build_fleet(vector<vector<string>> &fleet);

/*----------------------------------------------------------------------------------------
 |                                                                                       |
 | Accepts and validates user coordinates inputs. Return validated coordinates inputs.   |
 |                                                                                       |
 ----------------------------------------------------------------------------------------*/
vector<int> user_input_coordinates(vector<vector<string>>& game_grid, vector<Ship>& fleet);

/*-----------------------------------
 |                                  |
 |  Displays the fleet information  |
 |                                  |
 -----------------------------------*/
void display_fleet_info(vector<Ship>& fleet); // displayShipInfo()



//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		          Program                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main() {

	/*////////////////////////
	--------------------------
	|      Main Variables    |
	--------------------------
	////////////////////////*/

	//-- Variable
	char ch_menu; // Utilized by _getch() and the menu switch
	int ship_id, num_of_ship_sunk = 0, rounds = 0; // Rounds counts the number of time it took the player to sink all the ships.
	string hit_info;
	bool cheat = false;

	//-- Vectors
	vector <vector<string>> game_grid;
	vector <int> user_coor;

	/*////////////////////////
	--------------------------
	|   Main Game Instance   |
	--------------------------
	////////////////////////*/

	do { // Play the games until until user quits 

		// Sets screen size
		console_size(225, 755, "center");
		
		do { // Displays menu until user presses a valid key

			//-- Banner
			cout << "\n                                            ****************\n                                            *  BattleShip  *\n                                            ****************\n\n";
			cout << "    In this game you are trying to sink the ship randomly position by the computer!\n\n";

			// menu list
			cout << "    Please choose from the following the menu:\n"
				<< "      Press P - To play the game -\n"
				<< "      Press Q - To quit the game -\n"
				<< "      Press C - Mode cheat on/off - Cheat mode is ";
			if (cheat) { cout << "on, you are officially a cheater!\n"; } else { cout << "off.\n"; } // Check if the cheat mode is on or of and diplays result.

			// Waits for user to press a key
			ch_menu = _getch();

			if (toupper(ch_menu) == 'Q') { // Exit program
				return 0;
			}
			else if (toupper(ch_menu) == 'P') { // Play the game
				break;
			}
			else if (toupper(ch_menu) == 'C') { // Changes cheat to on/off
				cheat = !cheat;
				clear(2);
			}
			else { // Invalid input
				cout << "\n\n   ----- Invalid input, please enter a valid input ------\n";
				press_key_to_continue(2);
			}

		} while (true);

		//************************************ Play the game

		// Creates a grid
		vector <vector<string>> game_grid = {
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "},
			{ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "}
		};

		// Creates a fleet 
		vector<Ship> fleet = build_fleet(game_grid);

		clear(2);
		console_size(500, 1000, "center");
		display_grid(game_grid, cheat);


		do { // Loops until all the ships are sunk
			
			// Gets user inputs
			user_coor = user_input_coordinates(game_grid, fleet);

			if (game_grid[user_coor[0]][user_coor[1]] == " ") { // It is a miss
				game_grid[user_coor[0]][user_coor[1]] = "o";
				rounds++;
				hit_info = "It is a miss!\n";
			}
			else if (game_grid[user_coor[0]][user_coor[1]] == "o" || game_grid[user_coor[0]][user_coor[1]] == "x") {
				rounds++;
				hit_info = "You all ready called those coordinates.\n";
			}
			else { // It is a hit
				rounds++;
				ship_id = atoi(game_grid[user_coor[0]][user_coor[1]].c_str());
				for (Ship &ship : fleet) { // Iterates trough the ships fleet
					if (ship.get_id() == ship_id) { // Finds the ship that was hit
						ship.add_hit();
						game_grid[user_coor[0]][user_coor[1]] = "x";
						hit_info = "It is a hit!! The name of the ship hit is " + ship.get_name() + ", and the ship was hit " + to_string(ship.get_hit()) + " times.\n";
						if (ship.get_sunk()) { // Finds if the ship sunk
							hit_info += "     And the ship " + ship.get_name() + " has sunk!\n";
							num_of_ship_sunk++;
						}
					}
				}
				
			}

			// If it is the first resize the console window
			if (rounds == 1) { console_size(625, 1000, "center"); }
			clear(5);
			display_grid(game_grid, cheat);
			display_fleet_info(fleet);
			cout << "     " << hit_info << "\n";
			
			if (num_of_ship_sunk == fleet.size()) {
				cout << "\n   --- Congratulation! You sunk all the ships in the fleet! in " << rounds <<  " rounds ---";
				press_key_to_continue(2);
				break; // Exits loop, play the game
			}

		} while (true);
	
	} while (true);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		         Functions               *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////


/*---------------------------------------
 |                                      |
 |  Clears the console screen.          |
 |  Utilized by press_key_to_continue() |
 |                                      |
 ---------------------------------------*/
void clear(int num_lines) {

	for (int i = 0; i < num_lines; i++) {
		cout << "\n";
	}
	cout << endl; // will flush the output buffer and insert a new line.
}

/*-----------------------------------
 |                                  |
 |  Waits for a key to be pressed.  |
 |                                  |
 -----------------------------------*/
void press_key_to_continue(int num_lines) {

	 // -- Local variables
	 // Press key to continue variable
	char ch;

	cout << "\n    -- Press any key to continue -- \n";
	ch = _getch();
	clear(num_lines);
}

/*--------------------------------------------------------
 |                                                       |
 |  Displays the game banner, utilized by display_grid() |
 |                                                       |
 --------------------------------------------------------*/
void display_banner() {

	cout << "\n                                                   ****************\n                                                   *  BattleShip  *\n                                                   ****************\n\n";
}

/*--------------------------------------------------------
 |                                                       |
 |  Displays a line of '-'. Utilized by display_grid().  |
 |                                                       |
 --------------------------------------------------------*/
void line() {

	cout << "                               ";
	for (int i = 0; i < 10; i++) {
		cout << "-----";
	}
	cout << "---------\n";
}

/*----------------------------------
 |                                 |
 |  Displays the battleship grid.  |
 |                                 |
 ----------------------------------*/
void display_grid(vector<vector<string>> &game_grid, bool &cheat) {

	//*** Local array
	// Grid column letters designation array
	char column_letters[10] = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J' };
	
	// Gets hold of the console inforfation and stores it in the variable hConsole
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);

	// Game banner
	display_banner();

	// Displays grid
	for (int i = 0; i < game_grid.size(); i++) { // Displays rows
		line();
		// Checks if the row is not 10 (i+1) and displays the amount of spaces needed before the row number
		if (i != 9) { 
			cout << "                            ";
		}
		else { // If row number is 10 (i+1)
			cout << "                           ";
		}
		// Displays the row number designation
		cout << i + 1 << " |";
		// Displays hit or miss if any
		for (int j = 0; j < game_grid[i].size(); j++) { // Displays columns
			if (game_grid[i][j] != " ") { // if the location is not empthy
				if (game_grid[i][j] == "o") { // if the location is a miss
					SetConsoleTextAttribute(hConsole, 10); // Changes font color to bright green
					cout << "  o";
					SetConsoleTextAttribute(hConsole, 7); // Reverts font color back to white
					cout << "  |";
				}
				else if (game_grid[i][j] == "x") { // if the location is a hit
					SetConsoleTextAttribute(hConsole, 14); // Changes font color to bright yellow
					cout << "  x";
					SetConsoleTextAttribute(hConsole, 7); // Reverts font color back to white
					cout << "  |";
				}
				else { // The location has a ship not hit
					if (cheat) { // if mode cheat is true it will display ships
						cout << "  " << game_grid[i][j] << "  |";
					}
					else { // if mode cheat is false it will not display ships
						cout << "     |"; // Hides the ship
					}
				}
			} // if
			else { // the location is empty 
				cout << "  " << game_grid[i][j] << "  |";
			}
		} // for loop disply hit miss
		cout << "\n";
	}
	line();
	cout << "                             ";
	// Displays the column letters designation
	for (int i = 0; i < game_grid[0].size(); i++) {
		cout << "     " << column_letters[i];
	}
	cout << "\n" << endl; // Note: endl insert a new line and also flushes the buffer

} // display_grid()

/*-----------------------------------
 |                                  |
 |  Displays the fleet information  |
 |                                  |
 -----------------------------------*/
void display_fleet_info(vector<Ship> &fleet) { // displayShipInfo()

	//--- Local variable
	int num_sunk = 0;

	//--- Local vector
	vector<string> ships_sunk, ships_not_sunk;
	vector<vector<string>> ships_hit;

	//************ Build data
	for (Ship &ship : fleet) { // Iterates trough the ships fleet
		if (ship.get_sunk()) { // Finds sunk ships
			num_sunk++;
			ships_sunk.push_back(ship.get_name());
		}
		else if (ship.get_hit() == 0) { // Finds not hit ship
			ships_not_sunk.push_back(ship.get_name());
		}
		else { // Hit but not sunk ships
			ships_hit.push_back({ship.get_name(), to_string(ship.get_hit())});
			ships_not_sunk.push_back(ship.get_name());
		}
	}
	
	// Displays fleet general info
	cout << "    Number of ship sunk: " << num_sunk << "    Number of ship remaining: " << fleet[0].get_num_ships() - num_sunk << "\n";
	
	// Diplays sunk ships
	if (num_sunk != 0) { // Will not displays the following info if no ship was sunk
		cout << "    Names of the sunk ships: ";
		for (int i = 0; i < ships_sunk.size(); i++) {
			if (i != ships_sunk.size() - 1) { // Check if the ship is the last in the list
				cout << ships_sunk[i] << ", ";
			}
			else if (ships_sunk.size() == 1) { // If it is the only ship in the list
				cout << ships_sunk[i] << "\n";
			}
			else { // last ship in the list
				cout << "and " << ships_sunk[i] << ".\n";
			}
		}
	}
	// Diplays remaining ships
	cout << "    Names of the remaining ships: ";
	for (int i = 0; i < ships_not_sunk.size(); i++) {
		if (i != ships_not_sunk.size() - 1) { // Check if the ship is the last in the list
			cout << ships_not_sunk[i] << ", ";
		}
		else if (ships_not_sunk.size() == 1) { // If it is the only ship in the list
			cout << ships_not_sunk[i] << ".\n";
		}
		else { // last ship in the list
			cout << "and " << ships_not_sunk[i] << ".\n";
		}
	}
	// Diplays hit ships
	if (!ships_hit.empty()) { // Will not displays the following info if no ship was hit
		cout << "    Name of the hit ships: ";
		for (int i = 0; i < ships_hit.size(); i++) {
			if (i != ships_hit.size() - 1) { // Check if the ship is the last in the list
				cout << ships_hit[i][0] << ", it was hit " << ships_hit[i][1] << "; ";
			}
			else if (ships_hit.size() == 1) { // If it is the only ship in the list
				cout << " the " << ships_hit[i][0] << ", it was hit " << ships_hit[i][1] << " times.\n";
			}
			else { // last ship in the list
				cout << "and the " << ships_hit[i][0] << ", it was hit " << ships_hit[i][1] << " times.\n";
			}
		}
	}
	cout << "\n";
} // display_fleet info()

/*--------------------------------------------------------
 |                                                       |
 |  Builds a fleet of 5 ships. Returns a fleet vector.   |
 |                                                       |
 --------------------------------------------------------*/
vector<Ship> build_fleet(vector<vector<string>> &game_grid) {

	//-- Local vector
	vector<Ship> fleet;

	// Creates ships
	Ship ship_1(game_grid, "Carrier");
	Ship ship_2(game_grid, "Battleship");
	Ship ship_3(game_grid, "Cruiser");
	Ship ship_4(game_grid, "Submarine");
	Ship ship_5(game_grid, "Destroyer");

	// Stores ships in vector
	fleet.push_back(ship_1);
	fleet.push_back(ship_2);
	fleet.push_back(ship_3);
	fleet.push_back(ship_4);
	fleet.push_back(ship_5);

	return fleet;

}

/*----------------------------------------------------------------------------------------
 |                                                                                       |
 | Accepts and validates user coordinates inputs. Return validated coordinates inputs.   |
 |                                                                                       |
 ----------------------------------------------------------------------------------------*/
vector<int> user_input_coordinates(vector<vector<string>> &game_grid, vector<Ship> &fleet) {
	 
	//--- Local variables
	string input_coord;
	bool valid_input;
	int input_row;

	// Local vector
	vector<int> input_coordinates;

	//--- Local array
	char column_letters[10] = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J' };

	do { // Loops until user enters valid column number
		
		cout << "     Please enter a row and a column: ";
		cin >> input_coord;

		// Check if the inputed coordinates are valid, the size of the input can not be less then 2 or larger than 3 (ex:10B)
		if (input_coord.size() > 3 || input_coord.size() < 2) {
			valid_input = false;
		}
		else if (input_coord.size() == 3) { // if row 10 or bigger was entered 
			input_row = (atoi(input_coord.substr(0, 2).c_str()))- 1; // convert the string type to an int type and subtract 1. 
			if (input_row >= 0 && input_row < 10) { // Checks if inputer integer is between 1-1=0 and 10-1=9
				input_coordinates.push_back(input_row);
				valid_input = true;
			}
			else {
				valid_input = false;
			}
		}
		else {
			input_row = (input_coord[0] - '0') - 1; // convert the char type to an int type and subtract 1.

			if (input_row >= 0 && input_row < 10) { // Checks if inputer integer is between 1-1=0 and 10-1=9
				input_coordinates.push_back(input_row);
				valid_input = true;
			}
			else {
				valid_input = false;
			}
		}
		
		if (valid_input) { // if the inputed row is a valid input 
			valid_input = false;
			for (int i = 0; i < sizeof(column_letters); i++) { // loops trough possible valid letters input
				if (column_letters[i] == toupper(input_coord.back())) { // Checks if the entered letter is valid
					input_coordinates.push_back(i);
					valid_input = true;
					break; // Exist for loop
				}
			}
		}
		if (valid_input) { break; } // Exits loops skip error mesage
		cout << "\n      --- The entered input is not a valid input. ---\n      --- The row should be a number between 1 and 10 and the column a letter between A and J --\n";
	} while (true);

	return input_coordinates;

} // user_input coordinates

/*---------------------------------------------------------------------------------------
 |                                                                                      |
 |  Sets size of the Console's window                                                   |
 | and position the console in desktop screen utilizing the variable position_console   |
 | Takes the console with width, lenght and position as arguments.                      |
 | position_console values:                                                             |
 | "center", "left_center", "right_center",                                             |
 | "top_left", "top_center", "top_right",                                               |
 | "bottom_left", "bottom_center", "bottom_right".                                      |
 |                                                                                      |
 ---------------------------------------------------------------------------------------*/
void console_size(int console_width, int console_lenght, string position_console) {
	/*
		Sets size of the Console's window
		and position the console in desktop screen utilizing the variable position_console
		Takes the console with width, lenght and position as arguments.

		position_console values:
		"center", "left_center", "right_center",
		"top_left", "top_center", "top_right",
		"bottom_left", "bottom_center", "bottom_right".
	*/

	//-- Local variables
	int console_position_left = 0,
		console_position_top = 0;

	// Creats a structure type rectangle coordinates, upper-left and lower-right corners
	RECT desktop;
	// Gets the desktop screen data 
	HWND my_desktop = GetDesktopWindow();
	// Stores the size of monitor screen to the variable desktop
	GetWindowRect(my_desktop, &desktop);
	/*
		The top left corner of the monitor has the coordinates (0, 0)
		and the bottom right corner has the coordinates (desktop.right, desktop.bottom).
		Note that the desktop.right = monitor lenght
		and the desktop.bottom = monitor width.
	*/
	// Checks if the wanted console lenght is bigger than the monitor screen lenght, 'desktop.right'
	if (desktop.right < console_lenght) { console_lenght = floor(desktop.right); }
	// Checks if the wanted console width is bigger than the monitor screen width, 'desktop.bottom'
	if (desktop.bottom < console_width) { console_width = floor(desktop.bottom); }

	// Checks if the wanted console's width or lenght are NOT the same as the width or lenght of the desktop screen
	// if true initializes the console's coordinates to the wanted console position
	// else console_position_left = 0, console_position_top = 0.
	if (console_lenght != desktop.right || console_width != desktop.bottom) {
		// Checks the wanted position and computes the related coordinates	
		if (position_console == "center") {
			console_position_left = round((desktop.right - console_lenght) / 2);
			console_position_top = round((desktop.bottom - console_width) / 2);
		}
		else if (position_console == "left_center") {
			console_position_left = 10;
			console_position_top = round((desktop.bottom - console_width) / 2);
		}
		else if (position_console == "right_center") {
			console_position_left = round((desktop.right - console_lenght) - 10);
			console_position_top = round((desktop.bottom - console_width) / 2);
		}
		else if (position_console == "top_left") {
			console_position_left = 10;
			console_position_top = 10;
		}
		else if (position_console == "top_center") {
			console_position_left = round((desktop.right - console_lenght) / 2);
			console_position_top = 10;
		}
		else if (position_console == "top_right") {
			console_position_left = round((desktop.right - console_lenght) - 10);
			console_position_top = 10;
		}
		else if (position_console == "bottom_left") {
			console_position_left = 10;
			console_position_top = round((desktop.bottom - console_width) - 40);
		}
		else if (position_console == "bottom_center") {
			console_position_left = round((desktop.right - console_lenght) / 2);
			console_position_top = round((desktop.bottom - console_width) - 40);
		}
		else if (position_console == "bottom_right") {
			console_position_left = round((desktop.right - console_lenght) - 10);
			console_position_top = round((desktop.bottom - console_width) - 40);
		}
	}

	// Gets the existing console screen data
	HWND my_console = GetConsoleWindow();
	// Initializes the console to the wanted size and its position to the center of the screen monitor 
	MoveWindow(my_console, console_position_left, console_position_top, console_lenght, console_width, TRUE);
} // console_size()