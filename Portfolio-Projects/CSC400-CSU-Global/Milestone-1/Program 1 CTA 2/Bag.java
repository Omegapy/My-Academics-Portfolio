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

import java.util.HashSet;
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
 * @version 3.0
 * @date 08/25/2024
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
	 * Creates a node in the linked structure. Each node contains an item and a
	 * reference to the next node.
	 */
	private class Node {
		T item; // The item stored in the node
		Node next; // Reference to the next node
	}

	// ==========================================================================

	/**
	 * Implements the Iterator interface.
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
	 * Gets one occurrence of an item type from the bag. For instance, if an healing
	 * potion object type is given, it will get the first occurrence of an healing
	 * potion object type it encounter. This operation runs in linear time O(n) in
	 * the worst case.
	 *
	 * 
	 * @param item the item to get from the bag
	 * @return the item if found, null otherwise
	 */
	public T get(T item) {
		for (T currentItem : this) {
			if (currentItem.equals(item)) {
				return currentItem;
			}
		}
		return null; // Item not found in the bag
	}

	/**
	 * Gets the number of items in this bag.
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
	 * Gets the iterator that iterates over the items in the bag. Used by for-each
	 * loop
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
	 * Gets the number of specific item is in the bag.
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

	// ----------------------------------------------------------------------------------------------

	/**
	 * Returns a new bag containing only distinct elements. Note that elements can
	 * be of the same type but have different ids (for example) making them distinct
	 * elements.
	 * 
	 * This method uses an HasSet to remove duplicate, as it not allows duplicated.
	 * 
	 * @return a new bag with distinct elements
	 */
	public Bag<T> distinct() {
		Bag<T> bagWithNoDuplicate = new Bag<>();
		HashSet<T> elementsSet = new HashSet<>();
		for (T item : this) {
			// Sets do not allow, thus no duplicate can be added to a set
			if (elementsSet.add(item)) { // Returns true if the element was added to the set
				bagWithNoDuplicate.add(item);
			}
		}
		return bagWithNoDuplicate;
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
	 * Removes one occurrence of an item type from the bag. For instance, if an
	 * healing potion object type is given, it will remove the first occurrence of
	 * an healing potion object type it encounter. This operation runs in linear
	 * time O(n) in the worst case.
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

	/**
	 * Merges the elements of another bag into the current bag.
	 * 
	 * @param otherBag the bag to merge into this one
	 */
	public void merge(Bag<T> otherBag) {
		for (T item : otherBag) {
			this.add(item);
		}
	}

	// ----------------------------------------------------------------------------------------------
}
