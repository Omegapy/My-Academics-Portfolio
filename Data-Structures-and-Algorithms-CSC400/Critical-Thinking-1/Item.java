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
 * Represents a generic item in the RPG game. This class is the base class for
 * all item types, such as Potion, Armor, and Weapon.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/18/2024
 */
public class Item {
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
	public Item(double price) {
		this.price = price;
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Returns the price of the item.
	 *
	 * @return the price of the item
	 */
	public double getPrice() {
		return price;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Returns a string representation of the Item.
	 *
	 * @return a string representation of the Item
	 */
	@Override
	public String toString() {
		return "Item [price=" + price + "]";
	}

	// ==============================================================================================
	/*------------
	 |  Setters  |
	 ------------*/

	/**
	 * Sets a new price for the item.
	 *
	 * @param price the new price to set
	 */
	public void setPrice(double price) {
		this.price = price;
	}

	// ----------------------------------------------------------------------------------------------

}
