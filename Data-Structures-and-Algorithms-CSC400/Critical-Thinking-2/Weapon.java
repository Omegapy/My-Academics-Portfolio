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
 * Represents a weapon item in the RPG game. Extends the Item class.
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 08/25/2024
 */
public class Weapon extends Item {
	private String id = "W";
	private String type;
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
	public Weapon(double price, String type, int attackPower) {
		super(price);
		this.attackPower = attackPower;
		this.type = type;
		id = id + numItems;
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	// ----------------------------------------------------------------------------------------------

	/**
	 * Gets the type of the weapon
	 *
	 * @return the type of the weapon
	 */
	public String getType() {
		return type;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Gets the id of the weapon item.
	 *
	 * @return the id of the weapon
	 */
	public String getId() {
		return id;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Gets the attack power of the weapon.
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
		return "Weapon [ID: " + id + ", type: " + type + ", attackPower = " + attackPower + ", price = " + getPrice()
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
		Weapon objT = (Weapon) obj;
		// Compare all fields except the ID
		return (this.getType() == objT.getType() && this.getAttackPower() == objT.getAttackPower());
	}

}