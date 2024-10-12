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
 * Represents an armor item in the RPG game. Extends the Item class.
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 08/25/2024
 */
public class Armor extends Item {
	private String id = "A";
	private String type;
	private int defenseRating;

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
	public Armor(double price, String type, int defenseRating) {
		super(price);
		this.defenseRating = defenseRating;
		this.type = type;
		id = id + numItems;
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Gets the id of the armor item.
	 *
	 * @return the id of the armor
	 */
	public String getId() {
		return id;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Gets the type of the potion.
	 *
	 * @return the type of the potion
	 */
	public String getType() {
		return type;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Gets the defense rating of the armor.
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
		return "Armor [ID: " + id + ", type: " + type + ", defenseRating = " + defenseRating + ", price = " + getPrice()
				+ "]";
	}

	// ---------------------------------------------------------------------------------------------

	/**
	 * Checks if this Potion is equal to another object. Ignores the id in the
	 * comparison. Override the Java Object class equal method.
	 *
	 * @param obj the object to compare to
	 * @return true if the objects are equal, false otherwise
	 */
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null || getClass() != obj.getClass())
			return false;
		Armor objT = (Armor) obj;
		// Compare all fields except the ID
		return (this.getType() == objT.getType() && this.getDefenseRating() == objT.getDefenseRating());
	}

	// ---------------------------------------------------------------------------------------------

}