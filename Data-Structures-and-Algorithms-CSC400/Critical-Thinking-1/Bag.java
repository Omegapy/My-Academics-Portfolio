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

/*---------------------------
|    Imported modules      |
---------------------------*/
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * A Bag ADT class. This class implements a bag using a linked list structure to
 * store elements. [element | next] -> [element | next] -> [element | next] ->
 * null.
 *
 * @param <T> the type of elements in this bag, must extend Item
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 08/18/2024
 */
public class Bag<T> implements Iterable<T> {
	private Node headNode; // The first node in the bag list
	private int size; // Number of nodes in the bag

	// ==============================================================================================
	/*------------------
	 |  Inner Classes  |
	 ------------------*/
	/**
	 * Private inner class that creates a node in the linked structure. Each node
	 * contains an item and a reference to the next node.
	 */
	private class Node {
		T item; // The item stored in the node
		Node next; // Reference to the next node
	}

	// ==========================================================================

	/**
	 * Private inner class that implements the Iterator interface.
	 */
	private class BagIterator implements Iterator<T> {
		private Node current = headNode; // Start from the first (head) node

		/**
		 * Checks if there are more elements to iterate over.
		 *
		 * @return true if there are more elements, false otherwise
		 */
		public boolean hasNext() {
			return current != null;
		}

		// ----------------------------------------------------------------------------------------------

		/**
		 * Returns the next element in the iteration.
		 *
		 * @return the next element in the iteration
		 * @throws NoSuchElementException if there are no more elements
		 */
		public T next() {
			if (!hasNext())
				throw new NoSuchElementException();
			T item = current.item; // Get the item from the current node
			current = current.next; // Move to the next node
			return item;
		}
	}

	// ==============================================================================================
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs an empty bag.
	 */
	public Bag() {
		headNode = null; // Initialize the first (head) node in the bag to null (empty bag)
		size = 0; // Initialize size of the bag to 0
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Returns the number of items in this bag.
	 *
	 * @return the number of items in this bag
	 */
	public int size() {
		return size;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Checks if this bag is empty.
	 *
	 * @return true if this bag contains no items, false otherwise
	 */
	public boolean isEmpty() {
		return size == 0;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Returns an iterator that iterates over the items in this bag.
	 *
	 * @return an iterator that iterates over the items in this bag
	 */
	public Iterator<T> iterator() {
		return new BagIterator();
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Checks if this bag contains the specified item.
	 *
	 * @param item the item to check for
	 * @return true if the bag contains the item, false otherwise
	 */
	public boolean contains(T item) {
		for (T t : this) {
			if (t.equals(item)) {
				return true;
			}
		}
		return false;
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Counts the number of specific item is in the bag.
	 *
	 * @param item the item to count
	 * @return the number of occurrences of the item in the bag
	 */
	public int count(T item) {
		int count = 0;
		for (T t : this) {
			if (t.equals(item)) {
				count++;
			}
		}
		return count;
	}

	// ==============================================================================================
	/*------------
	 |  Setters  |
	 ------------*/

	/**
	 * Adds the specified item to this bag. This operation runs in constant time
	 * O(1).
	 *
	 * @param item the item to add to the bag
	 */
	public void add(T item) {
		Node nextNode = headNode; // Save the current head node becoming the next node in the added node
		headNode = new Node(); // Create a new node and make it the head node
		headNode.item = item; // Set the item of the new node
		headNode.next = nextNode; // Link the new node to the old head node
		size++; // Increment the size of the bag
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Removes one occurrence of the specified item from the bag if it exists. This
	 * operation runs in linear time O(n) in the worst case.
	 *
	 * @param item the item to remove
	 * @return true if the item was found and removed, false otherwise
	 */
	public boolean remove(T item) {
		Node current = headNode;

		if (headNode == null)
			return false; // If the bag is empty, return false

		if (headNode.item.equals(item)) { // If the item is in the first node
			headNode = headNode.next; // Make the next node the new head node
			size--; // Decrement the size
			return true;
		}

		while (current.next != null) { // Iterates the linked structure
			if (current.next.item.equals(item)) { // If the next node contains the item
				current.next = current.next.next; // Remove the next node from the chain
				size--; // Decrement the size
				return true;
			}
			current = current.next; // Move to the next node
		}
		return false; // Item not found in the bag
	}

	// ----------------------------------------------------------------------------------------------

}
