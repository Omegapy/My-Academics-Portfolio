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
 * Represents a potion item in the RPG game. Extends the Item class with
 * additional properties specific to potions.
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 08/25/2024
 */
public class Potion extends Item {
	private String id = "P";
	private String type; // Type of potion (e.g., healing, mana, stamina)
	private int effect; // The effect strength of the potion

	// ==============================================================================================
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs a Potion with the specified price, type, and effect.
	 *
	 * @param price  the price of the potion
	 * @param type   the type of the potion
	 * @param effect the effect strength of the potion
	 */
	public Potion(double price, String type, int effect) {
		super(price);
		this.type = type;
		this.effect = effect;
		id = id + numItems;
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Gets the id of the potion item.
	 *
	 * @return the id of the potion
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
	 * Returns the effect strength of the potion.
	 *
	 * @return the effect strength of the potion
	 */
	public int getEffect() {
		return effect;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Returns a string representation of the Potion.
	 *
	 * @return a string representation of the Potion
	 */
	@Override
	public String toString() {
		return "Potion [ID: " + id + ", type: " + type + ", effect = " + effect + ", price = " + getPrice() + "]";
	}

	// ----------------------------------------------------------------------------------------------

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
		Potion objT = (Potion) obj;
		// Compare all fields except the ID
		return (this.getType() == objT.getType() && this.getEffect() == objT.getEffect());
	}

	// ----------------------------------------------------------------------------------------------
}
