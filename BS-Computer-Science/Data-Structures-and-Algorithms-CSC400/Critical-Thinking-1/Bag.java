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

/*---------------------------
|    Imported modules      |
---------------------------*/
import java.util.Iterator;
import java.util.NoSuchElementException;

// @formatter:off
/** 
 * A Bag ADT class. This class implements a bag using a linked list structure to
 * store elements 
 * [element | next] -> [element | next] -> [element | next] -> null.
 *
 * @param <T> the type of elements in this bag, must extend Item
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 08/18/2024
 */
// @formatter:on
public class Bag<T> implements Iterable<T> {
	private Node headNode; // The first node in the bag list
	private int size;

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
			T item = current.item;
			current = current.next;
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
		headNode = null;
		size = 0;
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
	 * Returns an iterator that iterates over the items in the bag.
	 *
	 * @return an iterator that iterates over the items in the bag
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

	// ----------------------------------------------------------------------------------------------

	/**
	 * Prints the contents of the bag.
	 */
	public void printContent() {
		System.out.println("Bag contents:");
		for (T item : this) {
			System.out.println(item);
		}
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
		Node nextNode = headNode;
		headNode = new Node();
		headNode.item = item;
		headNode.next = nextNode;
		size++;
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
			return false;

		if (headNode.item.equals(item)) {
			headNode = headNode.next;
			size--;
			return true;
		}

		while (current.next != null) { // Iterates the linked structure
			if (current.next.item.equals(item)) {
				current.next = current.next.next;
				size--;
				return true;
			}
			current = current.next;
		}
		return false; // Item not found in the bag
	}

	// ----------------------------------------------------------------------------------------------

}
