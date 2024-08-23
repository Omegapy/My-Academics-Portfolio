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
 * Main class runs tests on the functionality of the Bag data structure.
 * 
 * @author Alejandro Ricciardi
 * @version 3.0
 * @date 08/25/2024
 */
public class Main {

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

				        *********************
				        *     RPG BAG V2    *
				        *********************
				""";

		// Create two instances of the Bag class
		Bag<Item> bag1 = new Bag<>();
		Bag<Item> bag2 = new Bag<>();

		// ------------------------------------------------------------
		// Create items to be duplicated
		Potion healingPotion = new Potion(10.5, "Healing", 50);
		Potion strengthPotion = new Potion(10.5, "Strength", 50);
		Potion protectionPotion = new Potion(10.5, "Protection", 50);

		// Create Distinct, not use to create duplicate
		Armor ironArmor = new Armor(75.0, "Iron", 50);
		Weapon sword = new Weapon(150.0, "Sword", 40);
		Potion ptotectionPotion = new Potion(10.5, "Protection", 50);

		// ------------------------------------------------------------
		// -- Add items to bag 2
		// Healing potions
		bag1.add(new Potion(10.5, "Healing", 50)); // Distinct new id
		bag1.add(healingPotion); // Duplicate when merge with Bag 2
		bag1.add(healingPotion); // Duplicate in this bag and when merge with Bag 2
		// Strength potions
		bag1.add(new Potion(10.5, "Strength", 50)); // Distinct new id
		bag1.add(strengthPotion); // Duplicate when merge with Bag 2
		// Armor
		bag1.add(ironArmor); // Distinct new id

		// -- Add elements to the second
		// Healing potions
		bag2.add(healingPotion); // Duplicate when merge with Bag
		// Strength potions
		bag2.add(strengthPotion); // Duplicate when merge with Bag 1
		// Protection potions
		bag2.add(ptotectionPotion); // Distinct
		// Weapon
		bag2.add(sword); // Distinct new id

		// ===========================================================
		System.out.println(banner);

		// Print the size of each bag
		System.out.println("Size of Bag 1: " + bag1.size());
		System.out.println("Size of Bag 2: " + bag2.size());

		System.out.println("\nBag 1");
		bag1.printContent();
		System.out.println("\nBag 2");
		bag2.printContent();

		// ===========================================================
		// Merge Bag 2 into Bag 1
		bag1.merge(bag2);
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Merged Bag 1 and Bag 2 into Bag 1\n");
		// Print the size of each bag
		System.out.println("Size of the merged Bag 1: " + bag1.size() + "\n");
		bag1.printContent();

		// ------------------------------------------------------------
		// Test the Bag class'contain method
		System.out.println("\nTesting contains method:");
		System.out.println("Bag contains Healing Potions: " + bag1.contains(healingPotion));
		System.out.println("Bag contains Strength Potions: " + bag1.contains(strengthPotion));
		System.out.println("Bag contains Potection Potions: " + bag1.contains(protectionPotion));
		System.out.println("Bag contains Iron Armors: " + bag1.contains(ironArmor));
		System.out.println("Bag contains Swords: " + bag1.contains(sword));

		// ------------------------------------------------------------
		// Test the count method
		System.out.println("\nTesting count method:");
		System.out.println("Count of Healing Potions: " + bag1.count(healingPotion));
		System.out.println("Count of Strength Potions: " + bag1.count(strengthPotion));
		System.out.println("Count of Potection Potions: " + bag1.count(protectionPotion));
		System.out.println("Count Swors: " + bag1.count(ironArmor));
		System.out.println("Count of Iron Armors: " + bag1.count(ironArmor));

		// ===========================================================
		// Remove a healing potion
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Deleting Healing Potion!\n");
		if (bag1.contains(healingPotion)) {
			if (bag1.remove(healingPotion)) {
				System.out.println("A Healing Potion was removed successfully!");
			} else {
				System.out.println("Failed to remove Healing Potion!");
			}
		} else {
			System.out.println("The Bag does not contain any Healing Potion!");
		}
		// Print the bag contents again
		System.out.println("Count of Healing Potions after removal: " + bag1.count(healingPotion));
		bag1.printContent();
		// Print the size of each bag
		System.out.println("\nSize of Bag 1 after deletion: " + bag1.size());

		// ===========================================================
		// Try to remove a second healing potion
		System.out.println("\n-------------------------------------------------------\n");
		System.out.println("Deleting second Healing Potion!\n");
		if (bag1.contains(healingPotion)) {
			if (bag1.remove(healingPotion)) {
				System.out.println("Another Healing Potion was removed successfully!");
			} else {
				System.out.println("Failed to remove Healing Potion!");
			}
		} else {
			System.out.println("The Bag does not contain any Healing Potion!");
		}
		// Print the bag contents again
		System.out.println("Count of Healing Potions after removal: " + bag1.count(healingPotion));
		bag1.printContent();
		// Print the size of each bag
		System.out.println("Size of Bag 1 after deletion: " + bag1.size());

		// ===========================================================
		// test the contains method after removal
		System.out.println("\nTesting contains method after Healing Potions removal:");

		// ------------------------------------------------------------
		// Test the Bag class'contain method
		System.out.println("\nTesting contains method:");
		System.out.println("Bag contains Healing Potions: " + bag1.contains(healingPotion));
		System.out.println("Bag contains Strength Potions: " + bag1.contains(strengthPotion));
		System.out.println("Bag contains Potection Potions: " + bag1.contains(protectionPotion));
		System.out.println("Bag contains Iron Armors: " + bag1.contains(ironArmor));
		System.out.println("Bag contains Swords: " + bag1.contains(sword));

		// ------------------------------------------------------------
		// Test the count method
		System.out.println("\nTesting count method:");
		System.out.println("Count of Healing Potions: " + bag1.count(healingPotion));
		System.out.println("Count of Strength Potions: " + bag1.count(strengthPotion));
		System.out.println("Count of Potection Potions: " + bag1.count(protectionPotion));
		System.out.println("Count Swors: " + bag1.count(ironArmor));
		System.out.println("Count of Iron Armors: " + bag1.count(ironArmor));

		// ------------------------------------------------------------
		// Create a new bag containing only the distinct elements
		System.out.println("\n-------------------------------------------------------\n");
		Bag<Item> distinctBag = bag1.distinct();
		System.out.println("Distinct Bag Contents\n");
		// Print the size of each bag
		System.out.println("Size of distinct Bag: " + distinctBag.size());
		distinctBag.printContent();

		// ===========================================================
		// test the contains method after duplicate removal
		// items with different ids but the same type are Not duplicates
		// items with the same ids and type are duplicates
		System.out.println("\nTesting contains method after duplicates renoval removal:");

		// ------------------------------------------------------------
		// Test the Bag class'contain method
		System.out.println("\nTesting contains method:");
		System.out.println("Bag contains Healing Potions: " + distinctBag.contains(healingPotion));
		System.out.println("Bag contains Strength Potions: " + distinctBag.contains(strengthPotion));
		System.out.println("Bag contains Potection Potions: " + distinctBag.contains(protectionPotion));
		System.out.println("Bag contains Iron Armors: " + distinctBag.contains(ironArmor));
		System.out.println("Bag contains Swords: " + distinctBag.contains(sword));

		// ------------------------------------------------------------
		// Test the count method
		System.out.println("\nTesting count method:");
		System.out.println("Count of Healing Potions: " + distinctBag.count(healingPotion));
		System.out.println("Count of Strength Potions: " + distinctBag.count(strengthPotion));
		System.out.println("Count of Potection Potions: " + distinctBag.count(protectionPotion));
		System.out.println("Count Swors: " + distinctBag.count(ironArmor));
		System.out.println("Count of Iron Armors: " + distinctBag.count(ironArmor));

	}

	// ----------------------------------------------------------------------------------------------

}
