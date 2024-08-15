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
 * Main class runs tests on the functionality of the Bag data structure.
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 08/18/2024
 */
public class Main {

	// ==============================================================================================
	/*------------------
	 |  Class Methods  |
	 ------------------*/

	/**
	 * Prints the contents of the bag.
	 *
	 * @param bag the bag to print
	 */
	private static void printBagContents(Bag<Item> bag) {
		System.out.println("Bag contents:");
		for (Item item : bag) {
			System.out.println(item);
		}
	}

	// ==============================================================================================
	/*----------------
	 |  Main Method  |
	 ----------------*/
	/**
	 * Entry point for the program. Runs tests on the functionality of the Bag data
	 * structure.
	 *
	 * @param args command line arguments (not used)
	 */
	public static void main(String[] args) {
		String banner = """

				        *******************
				        *     RPG BAG     *
				        *******************
				""";

		// Create an instance of the Bag class
		Bag<Item> bag = new Bag<>();

		// ------------------------------------------------------------
		// Create items
		Potion healingPotion = new Potion(10.5, "Healing", 50);
		Potion strengthPotion = new Potion(10.5, "Strength", 50);
		Potion protectionPotion = new Potion(10.5, "Protection", 50);
		Armor ironArmor = new Armor(75.0, 50);
		Weapon sword = new Weapon(150.0, 40);

		// Add elements to the bag
		bag.add(healingPotion);
		bag.add(healingPotion); // Add another healing potion
		bag.add(strengthPotion);
		bag.add(strengthPotion); // Add another strength potion
		bag.add(ironArmor);
		bag.add(sword);
		// --- No protection potion added to bag

		// ------------------------------------------------------------
		System.out.println(banner);

		// Print the bag content
		printBagContents(bag);

		// ------------------------------------------------------------
		// Test the Bag class'contain method
		System.out.println("\nTesting contains method:");
		System.out.println("Bag contains Healing Potion: " + bag.contains(healingPotion));
		System.out.println("Bag contains Strength Potion: " + bag.contains(strengthPotion));
		System.out.println("Bag contains Iron Armor: " + bag.contains(ironArmor));
		System.out.println("Bag contains Potection Potion: " + bag.contains(protectionPotion));

		// ------------------------------------------------------------
		// Test the count method
		System.out.println("\nTesting count method:");
		System.out.println("Count of Healing Potions: " + bag.count(healingPotion));
		System.out.println("Count of Strength Potions: " + bag.count(strengthPotion));
		System.out.println("Count of Iron Armor: " + bag.count(ironArmor));
		System.out.println("Count of Potection Potion: " + bag.count(protectionPotion));

		// ------------------------------------------------------------
		// Change price of healing potion
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Changing Healing Potion from 10.5 to 12.0\n");
		healingPotion.setPrice(12.0);
		System.out.println("The Price of the Healing Potions was changed successfully!\n");
		System.out.println("Count of Healing Potions: " + bag.count(healingPotion));
		System.out.println("Healing Potion price: " + healingPotion.getPrice());

		// ------------------------------------------------------------
		// Remove a healing potion
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Deleting Healing Potion!\n");
		if (bag.contains(healingPotion)) {
			if (bag.remove(healingPotion)) {
				System.out.println("A Healing Potion was removed successfully!");
			} else {
				System.out.println("Failed to remove Healing Potion!");
			}
		} else {
			System.out.println("The Bag does not contain any Healing Potion!");
		}
		// Print the bag contents again
		System.out.println("Count of Healing Potions after removal: " + bag.count(healingPotion) + "\n");
		printBagContents(bag);

		// Try to remove another healing potion
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Deleting Healing Potion!\n");
		if (bag.contains(healingPotion)) {
			if (bag.remove(healingPotion)) {
				System.out.println("Another Healing Potion was removed successfully!");
			} else {
				System.out.println("Failed to remove Healing Potion!");
			}
		} else {
			System.out.println("The Bag does not contain any Healing Potion!");
		}
		// Print the bag contents again
		System.out.println("Count of Healing Potions after removal: " + bag.count(healingPotion) + "\n");
		printBagContents(bag);

		// Try to remove a non-existent healing potion
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Deleting Healing Potion!\n");
		if (bag.contains(healingPotion)) {
			if (bag.remove(healingPotion)) {
				System.out.println("Another Healing Potion was removed successfully!");
			} else {
				System.out.println("Failed to remove Healing Potion!");
			}
		} else {
			System.out.println("The Bag does not contain any Healing Potion!");
		}
		System.out.println("Count of Healing Potions: " + bag.count(healingPotion) + "\n");
		// Print the bag contents again
		printBagContents(bag);

		// ------------------------------------------------------------
		// Print the items count again
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Printing the items count again:\n");
		System.out.println("Count of Healing Potions: " + bag.count(healingPotion));
		System.out.println("Count of Strength Potions: " + bag.count(strengthPotion));
		System.out.println("Count of Iron Armor: " + bag.count(ironArmor));
		System.out.println("Count of Potection Potion: " + bag.count(protectionPotion));
	}

	// ----------------------------------------------------------------------------------------------

}
