/*
    Program Name: RPG Bag
    Author: Alejandro (Alex) Ricciardi
    Date: 08/18/2024
    
    Program Description: 
    The program is an implementation of a Bag Abstract Data Structure (Bag ADT). 
    The Bag class represents the inventory of an RPG video game player. 
    The Bag allows for the storage and management of game items such as Potions, Armor, and Weapons. 
    The Bag ADT is implemented as a generic class that can store any item object type.
*/

/*-------------------
 |     Packages     |
 -------------------*/
package rpgBag; // Program Folder

/**
 * Represents a weapon item in the RPG game. Extends the Item class.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/18/2024
 */
public class Weapon extends Item {
	private int attackPower; // Attack power of the weapon

	// ==============================================================================================
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs a Weapon with the specified price and attack power.
	 *
	 * @param price       the price of the weapon
	 * @param attackPower the attack power of the weapon
	 */
	public Weapon(double price, int attackPower) {
		super(price);
		this.attackPower = attackPower;
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Returns the attack power of the weapon.
	 *
	 * @return the attack power of the weapon
	 */
	public int getAttackPower() {
		return attackPower;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Returns a string representation of the Weapon.
	 *
	 * @return a string representation of the Weapon
	 */
	@Override
	public String toString() {
		return "Weapon [attackPower=" + attackPower + ", price=" + getPrice() + "]";
	}

	// ----------------------------------------------------------------------------------------------

}