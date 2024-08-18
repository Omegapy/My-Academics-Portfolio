/*
    Program Name: RPG Bag
    Author: Alejandro (Alex) Ricciardi
    Date: 08/18/2024
    
    Program Description: 
    The program is an implementation of a Bag Abstract Data Structure (Bag ADT) 
    using a Linked list structure.
    [element | next] -> [element | next] -> [element | next] -> null.
    The Bag class represents the inventory of an RPG video game player. 
    The Bag allows for the storage and management of game items such as Potions, Armor, and Weapons. 
    The Bag ADT is implemented as a generic class that can store any item object type.
*/

/*-------------------
 |     Packages     |
 -------------------*/
package rpgBag; // Program Folder

/**
 * Represents an armor item in the RPG game. Extends the Item class.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/18/2024
 */
public class Armor extends Item {
	private int defenseRating; // Defense rating of the armor

	// ==============================================================================================
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs an Armor with the specified price and defense rating.
	 *
	 * @param price         the price of the armor
	 * @param defenseRating the defense rating of the armor
	 */
	public Armor(double price, int defenseRating) {
		super(price);
		this.defenseRating = defenseRating;
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Returns the defense rating of the armor.
	 *
	 * @return the defense rating of the armor
	 */
	public int getDefenseRating() {
		return defenseRating;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Returns a string representation of the Armor.
	 *
	 * @return a string representation of the Armor
	 */
	@Override
	public String toString() {
		return "Armor [defenseRating=" + defenseRating + ", price=" + getPrice() + "]";
	}

	// ----------------------------------------------------------------------------------------------

}