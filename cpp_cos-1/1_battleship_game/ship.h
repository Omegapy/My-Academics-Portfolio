

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |  BattleShip Game               *         Ship class Declaration       *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

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

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

			/*////////////////////////
			--------------------------
			|        Headers         |
			--------------------------
			////////////////////////*/

#pragma once

// Console Input & Output Header file, Window OS only
#include <conio.h> // getch()
// Console Window size header file, Window OS only
#define _WIN32_WINNT 0x0500
#include<windows.h> // MoveWindow(), SetConsoleTextAttribute()

#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <cctype> // toupper()

using namespace std;

			/*/////////////////////////
			--------------------------
			|          Class         |
			--------------------------
			////////////////////////*/


class Ship {

			/*////////////////////////
			--------------------------
			|       Variables        |
			--------------------------
			////////////////////////*/



	// Variables
	string ship_name;
	int num_hits, hit = 0, id; // ship id
	bool sunk = false;
	// static initialized in ship.cpp 
	static int num_ships; // Keeps track of the num ber of ship created

	//-- Private vector
	vector<vector<int>> location;

			/*////////////////////////
			--------------------------
			|    Private Function    |
			--------------------------
			////////////////////////*/

	/*---------------------------------------------
	 |                                            |
	 |  Randomly picks the location of the ship.  |
	 |  returns the coordinates of the ship.      |
	 |                                            |
	 ---------------------------------------------*/
	vector<vector<int>> position_ship(vector<vector<string>> &game_grid);

public:

			/*////////////////////////
			--------------------------
			|      Constructors      |
			--------------------------
			////////////////////////*/

	/*------------------
	 |                 |
	 |     Default     |
	 |                 |
	 ------------------*/
	Ship();

	/*------------------
	 |                 |
	 |  Constructor-1  |
	 |                 |
	 ------------------*/
	Ship(vector<vector<string>> &game_grid);

	/*------------------
	 |                 |
	 |  Constructor-2  |
	 |                 |
	 ------------------*/
	Ship(vector<vector<string>> &game_grid, string ship_name);

	/*------------------
	 |                 |
	 |  Constructor-3  |
	 |                 |
	 ------------------*/
	Ship(vector<vector<string>> &game_grid, string ship_name, int num_hits);

			/*////////////////////////
			--------------------------
			|       Accessors        |
			--------------------------
			////////////////////////*/

	string get_name(); // returns ship name


	int get_num_hits(); // returns how many times the ship can be before sinking

	int get_hit(); // returns how many times the ship was hit

	bool get_sunk();// returns true or false ship was sunked

	vector<vector<int>> get_location(); // returns the location of the ship

	int get_num_ships(); // returns the number of ships created

	int get_id(); // returns the ship's id

			/*////////////////////////
			--------------------------
			|        Mutators        |
			--------------------------
			////////////////////////*/

	/*-------------------------
	 |                        |
	 | Changes the ship name  |
	 |                        |
	 -------------------------*/
	void set_name(string ship_name);

	/*---------------------------------------------------------------------------
	 |                                                                          |
	 | Changes the ship size, how many times the ship can be before sinking.    |
	 | Limits the size of the ship to 7 and not less than 2.                    |
	 | it will display an error message and exit program with a code error -3.  |
	 |                                                                          |
	 ---------------------------------------------------------------------------*/
	void set_num_hits(int num_hits);

	/*---------------------------------------------------
	 |                                                  |
	 |  Changes how many times the ship was it.         |
	 |  If hit = num_hits changes the sunked to true    |
	 |                                                  |
	 ---------------------------------------------------*/
	void add_hit();

	/*------------------------------------------------------------------------
	 |                                                                       |
	 |  Changes the sunked variable.                                         |
	 |  Resets the hit variable to match the sunked false or true values.    |
	 |                                                                       |
	 ------------------------------------------------------------------------*/
	void set_sunked(bool sunk);
};
