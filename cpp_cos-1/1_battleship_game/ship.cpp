

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |  BattleShip Game               *         Ship class Definitions       *                                 |
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
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////

	/*////////////////////////
	--------------------------
	|        Headers         |
	--------------------------
	////////////////////////*/

#include "ship.h"

	/*////////////////////////
	--------------------------
	|    Static Varibles     |
	--------------------------
	////////////////////////*/

/*--------------------------------------------------------------------------------
 |                                                                               |
 |  Unitializes static num_ship (number of ships created) from the class Ship.   |
 |  Everytime a ship is created num_ship++ in the class constructors!! wierd!    |
 |                                                                               |
 --------------------------------------------------------------------------------*/
int Ship::num_ships = 0;

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
vector<vector<int>> Ship::position_ship(vector<vector<string>> &game_grid) {

	// utilize by the class ship, its private function position_ship() and std::rnd() funtion
	srand(time(NULL)); // set random seed number = system clock time

	//-- local vector
	vector<vector<int>> ship_coordinates;

	//-- local variables
	int column, row, direction;
	bool ship_at_location;

	// Randomly picks the location and checks if a ship is already at the location
	do {
		ship_at_location = false;
		do { // Randomly picks the first ship's coordinate and checks if a ship at the coordinates
			column = rand() % 9;
			row = rand() % 9;
			// If it is not a ship at the coordinates break, pick coordinates
			if (game_grid[row][column] == " ") {
				break;
			}
		} while (true);
		// Randomly picks the ship's direction
		direction = rand() % 3;
		// If direction == 0 ship to the right
		if (direction == 0 && (row + num_hits) <= 9) {
			for (int i = 0; i < num_hits; i++) { // Set the coordinated of the ship using its lenght
				ship_coordinates.push_back({ row, column });
				row++;
				if (game_grid[row][column] != " ") { // If it is a ship at the coordinate break, do not pic coordinates
					ship_coordinates.clear(); // reset ship_coordinates
					ship_at_location = true;
					break;
				}
			}
		}
		// If direction == 1 ship to the left
		else if (direction == 1 && (row - num_hits) >= 0) {
			for (int i = 0; i < num_hits; i++) { // Set the coordinated of the ship using its lenght
				ship_coordinates.push_back({ row, column });
				row--;
				if (game_grid[row][column] != " ") { // If it is a ship at the coordinate break, do not pick coordinates
					ship_coordinates.clear(); // reset ship_coordinates
					ship_at_location = true;
					break;
				}
			}
		}// If direction == 2 ship down
		else if (direction == 2 && (column + num_hits) <= 9) {
			for (int i = 0; i < num_hits; i++) { // Set the coordinated of the ship using its lenght
				ship_coordinates.push_back({ row, column });
				column++;
				if (game_grid[row][column] != " ") { // If it is a ship at the coordinate break, do not pic coordinates
					ship_coordinates.clear(); // reset ship_coordinates
					ship_at_location = true;
					break;
				}
			}
		}// If direction == 3 ship up
		else if (direction == 2 && (column - num_hits) >= 0) {
			for (int i = 0; i < num_hits; i++) { // Set the coordinated of the ship using its lenght
				ship_coordinates.push_back({ row, column });
				column--;
				if (game_grid[row][column] != " ") { // If it is a ship at the coordinate break, do not pic coordinates
					ship_coordinates.clear(); // reset ship_coordinates
					ship_at_location = true;
					break;
				}
			}
		}
		else { // It is already a ship at first coordinates
			ship_coordinates.clear(); // reset ship_coordinates
			ship_at_location = true;

		}
	} while (ship_at_location);

	// Adds the ship's coordinates and id to the game grid.
	for (int i = 0; i < ship_coordinates.size(); i++) {
		game_grid[ship_coordinates[i][0]][ship_coordinates[i][1]] = to_string(id);
	}

	return ship_coordinates;
} // position_ship()

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
Ship::Ship() {
	/*
		Default constructor is activated when no parameters are passed while creating a ship class object.
		It throws an error, the parameter grid_name need to passed to extiatate a ship object.
	*/
	try {
		throw  "Error Class Constructor";
	}
	catch (const char &error) {
		cout << "***** " << error << " *****\n\n       a ship object can not be null! the parameter grid_name need to passed to extiatate a ship object\n"
			<< "\n       ex : ship(hit_miss_grid) ship; \n\n";
	}

}

/*------------------
 |                 |
 |  Constructor-1  |
 |                 |
 ------------------*/
// Overloaded constructor-1
Ship::Ship(vector<vector<string>> &game_grid) {

	ship_name = "Carrier";
	num_hits = 5;
	id = num_ships;
	location = position_ship(game_grid);
	// Static
	num_ships++;
}

/*------------------
 |                 |
 |  Constructor-2  |
 |                 |
 ------------------*/
// Overloaded constructor-2
Ship::Ship(vector<vector<string>> &game_grid, string ship_name) {

	// Matches the name with hit points
	if (ship_name == "Carrier") {
		num_hits = 5;
	}
	else if (ship_name == "Battleship") {
		num_hits = 4;
	}
	else if (ship_name == "Cruiser") {
		num_hits = 3;
	}
	else if (ship_name == "Submarine") {
		num_hits = 3;
	}
	else if (ship_name == "Destroyer") {
		num_hits = 2;
	}
	else { // no matched ship name
		try {
			throw  "Error Class Constructor";
		}
		catch (const char &error) {
			cout << "***** " << error << "*****\n\n       The ship name is invalid!\n       To enter your own ship names you need to also define their num_hits\n"
				<< "       ex: Ship(hit_miss_grid, \"Cruise Missile Ship\", 3) ship; \n\n";
		}
	}

	this->ship_name = ship_name;
	id = num_ships;
	location = position_ship(game_grid);
	// Static
	num_ships++;
} // Construct-2

/*------------------
 |                 |
 |  Constructor-3  |
 |                 |
 ------------------*/
// Overloaded constructor-3
Ship::Ship(vector<vector<string>> &game_grid, string ship_name, int num_hits) {

	// Limits the size of the ship to 7 and not less than 2
	if (num_hits > 7 || num_hits < 2) { // Displays and exits program if num_hits > 7 or < 2
		try {
			throw  "Error Class Constructor";
		}
		catch (const char &error) {
			cout << "***** " << error << "*****\n\n       The number of num_hits is invalid!\n       It shoud be no nore than 7 and not less than 2.\n\n";
		}
	}
	this->ship_name = ship_name;
	this->num_hits = num_hits;
	id = num_ships;
	location = position_ship(game_grid);
	// Static
	num_ships++;
}

		/*////////////////////////
		--------------------------
		|       Accessors        |
		--------------------------
		////////////////////////*/


string Ship::get_name() { // returns ship name
	return ship_name;
}

int Ship::get_num_hits() { // returns how many times the ship can be before sinking
	return num_hits;
}

int Ship::get_hit() { // returns how many times the ship was hit
	return hit;
}

bool Ship::get_sunk() { // returns true or false ship was sunked
	return sunk;
}

vector<vector<int>> Ship::get_location() { // returns the location of the ship
	return location;
}

// static
int Ship::get_num_ships() { // returns the number of ships created
	return num_ships;
}

int Ship::get_id() { // returns the ship's id
	return id;
}

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
void Ship::set_name(string ship_name) {

	this->ship_name = ship_name;
}
/*---------------------------------------------------------------------------
 |                                                                          |
 | Changes the ship size, how many times the ship can be before sinking.    |
 | Limits the size of the ship to 7 and not less than 2.                    |
 | it will display an error message and exit program with a code error -3.  |
 |                                                                          |
 ---------------------------------------------------------------------------*/
void Ship::set_num_hits(int num_hits) {

	// Limits the size of the ship to 7 and not less than 2
	if (num_hits > 7 || num_hits < 2) { // Displays and exits program if num_hits > 7 or < 2
		try {
			throw  "Error Class Constructor";
		}
		catch (const char &error) {
			cout << "***** " << error << "*****\n\n       The number of num_hits is invalid!\n       It shoud be no nore than 7 and not less than 2.\n\n";
		}
	}
	this->num_hits = num_hits;
}
/*---------------------------------------------------
 |                                                  |
 |  Changes how many times the ship was it.         |
 |  If hit = num_hits changes the sunked to true    |
 |                                                  |
 ---------------------------------------------------*/
void Ship::add_hit() {

	hit++;
	if (hit == num_hits) { sunk = true; }
}

/*------------------------------------------------------------------------
 |                                                                       |
 |  Changes the sunked variable.                                         |
 |  Resets the hit variable to match the sunked false or true values.    |
 |                                                                       |
 ------------------------------------------------------------------------*/
void Ship::set_sunked(bool sunk) {

	this->sunk = sunk;
	// Resets the hit variable to match the sunked false or true values.
	(sunk) ? hit = num_hits : hit = 0;
}
