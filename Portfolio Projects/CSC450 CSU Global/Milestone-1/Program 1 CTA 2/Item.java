/*
    Program Name: RPG Bag V2
    Author: Alejandro (Alex) Ricciardi
    Date: 08/25/2024
    
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
 * Represents a generic item in the RPG game. This class is the base class for
 * all item types, such as Potion, Armor, and Weapon.
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 08/25/2024
 */
public abstract class Item {
	protected static int numItems = 0;
	private double price; // Price of the item

	// ==============================================================================================
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs an Item with the specified price.
	 *
	 * @param price the price of the item
	 */
	protected Item(double price) {
		numItems++;
		this.price = price;
	}

	// ==============================================================================================
	/*------------------------
	 |  Getters Not Abstract |
	 ------------------------*/

	/**
	 * Returns the price of the item.
	 *
	 * @return the price of the item
	 */
	protected double getPrice() {
		return this.price;
	}

	// ==============================================================================================
	/*-------------------------
	 |  Setters Not Abstract  |
	 -------------------------*/

	/**
	 * Sets a new price for the item.
	 *
	 * @param price the new price to set
	 */
	protected void setPrice(double price) {
		this.price = price;
	}

	// ==============================================================================================
	/*---------------------
	 |  Abstract Methods  |
	 ---------------------*/

	/**
	 * Checks if this Potion is equal to another object. Override the Java Object
	 * class equal method
	 *
	 * @param obj the object to compare to
	 */
	@Override
	public abstract boolean equals(Object obj);

	// ----------------------------------------------------------------------------------------------

	/**
	 * Gets the assigned item type
	 */
	protected abstract String getId();

	// ----------------------------------------------------------------------------------------------

	/**
	 * Gets the assigned item type
	 */
	protected abstract String getType();

	// ----------------------------------------------------------------------------------------------

}
