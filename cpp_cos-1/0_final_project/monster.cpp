//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *       Monster class definitions      *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

  The Monster class create objects with the states:  
  string name, int health, int armore, and int strength


*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

	/*////////////////////////
	--------------------------
	|        Headers         |
	--------------------------
	////////////////////////*/


#include "monster.h"


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
Monster::Monster() {
	// empty
}

/*------------------
 |                 |
 |  Constructor-1  |
 |                 |
 ------------------*/
Monster::Monster(string name, int health, int armore, int strength) {

	this->name = name;
	this->health = health;
	this->armor = armore;
	this->strength = strength;
}

	/*////////////////////////
	--------------------------
	|       Accessors        |
	--------------------------
	////////////////////////*/

string Monster::get_name() {
	return name;
}

int Monster::get_health() {
	return health;
}

int Monster::get_armor() {
	return armor;
}

int Monster::get_strength() {
	return strength;
}

	/*////////////////////////
	--------------------------
	|        Mutators        |
	--------------------------
	////////////////////////*/

void Monster::set_name(string name) {
	this->name = name;
}

void Monster::set_health(int health) {
	this->health = health;
}

void Monster::set_armore(int armore) {
	this->armor = armore;
}

void Monster::set_strength(int strength) {
	this->strength = strength;
}
