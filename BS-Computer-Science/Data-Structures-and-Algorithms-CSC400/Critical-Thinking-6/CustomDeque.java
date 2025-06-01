/*
    Program Name: Custom Deque ADT
    Author: Alejandro (Alex) Ricciardi
    Date: 09/22/2024
    
    Program Description: 
    The program is a custom double-ended queue (deque) implementation using Java's LinkedList. 
    It tests the deque insertion, deletion, and iteration functionalities 
    from both the front and the end.
*/

/*-------------------
 |     Packages     |
 -------------------*/
package customDeque; // Program Folder

/*---------------------------
 |    Imported modules      |
 ---------------------------*/
import java.util.Deque;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.NoSuchElementException;

//@formatter:off
/**
 * A custom implementation of a double-ended queue, a deque 
 * A deque that allows insertion and removal of elements from 
 * both the front and rear ends 
 * This class uses Java's LinkedList to store elements
 * 
 * @author Alejandro Ricciardi
 * @version 3.0
 * @date 09/22/2024
 * 
 * @param <T> The type of elements to be stored in the deque
 */
//@formatter:on
public class CustomDeque<T> {
	// The internal deque to store elements of type T
	private Deque<T> deque;

	// --------------------------------------------------------------------------
	/*------------------
	 |  Inner Classes  |
	 ------------------*/

	//@formatter:off
	/**
	 * This class implements an iterator to traverse the elements of the deque 
	 * The traversal can be set to start from the head or the tail, based on the
	 * constructor argument fromHead
	 * Note that fromHead is set to true by default
	 */
	//@formatter:on
	private class DequeIterator implements Iterator<T> {
		// Internal iterator object, which can iterate either from head or tail
		private Iterator<T> iterator;

		// --------- Constructor

		//@formatter:off
		/**
		 * Constructs a DequeIterator to iterate the deque
		 * 
		 * @param fromHead If true, the iteration starts from the head (front). If
		 *                 false, it starts from the tail (rear) 
		 *                 - Default set to true by the Iterator method -
		 */
		//@formatter:on
		public DequeIterator(boolean fromHead) {
			if (fromHead) {
				this.iterator = deque.iterator(); // Iterate starting from the front
			} else {
				this.iterator = deque.descendingIterator(); // Iterate starting from the back
			}
		}

		// --------- Getters

		/**
		 * Checks if there are more elements in the deque.
		 * 
		 * @return true if there are more elements, false otherwise.
		 */
		@Override
		public boolean hasNext() {
			return iterator.hasNext();
		}

		// --------------------------------------------

		/**
		 * Returns the next element in the iteration.
		 * 
		 * @return The next element in the deque.
		 * @throws NoSuchElementException If no more elements are present.
		 */
		@Override
		public T next() {
			if (!hasNext()) {
				throw new NoSuchElementException(); // Throws exception if no next element exists
			}
			return iterator.next();
		}
		// --------------------------------------------
	}

	// --------------------------------------------------------------------------
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs an empty CustomDeque.
	 */
	public CustomDeque() {
		this.deque = new LinkedList<>(); // Initializes an empty deque using LinkedList
	}

	// --------------------------------------------------------------------------
	/*------------
	 |  Getters  |
	 ------------*/

	// --------- Iterators

	//@formatter:off
	/**
	 * Iterates starting from the front (head) of the deque
	 * fromHead set to true
	 * 
	 * @return An iterator starting from the front of the deque.
	 */
	public Iterator<T> iterator() {
		return new DequeIterator(true); // Default iteration from head
	}
	//@formatter:on

	// --------------------------------------------------------------------------

	//@formatter:off
	/**
	 * Iterates that can start from either the front or the back of the
	 * deque
	 * fromHead needs to be set
	 * 
	 * @param fromHead If true, the iteration starts from the head (front),
	 *                 otherwise from the tail (rear).
	 * @return An iterator starting either from the front or back of the deque.
	 */
	//@formatter:on
	public Iterator<T> iterator(boolean fromHead) {
		return new DequeIterator(fromHead); // Custom iteration direction
	}

	// --------------------------------------------------------------------------

	// ---------

	/**
	 * Checks if the deque is empty.
	 * 
	 * @return true if the deque contains no elements, false otherwise.
	 */
	public boolean isEmpty() {
		return deque.isEmpty(); // Checks whether deque is empty
	}

	// --------------------------------------------------------------------------
	/*------------
	 |  Setters  |
	 ------------*/

	// --------- Removes methods

	/**
	 * Removes and returns the element at the front (head) of the deque.
	 * 
	 * @return The element removed from the front of the deque.
	 * @throws NoSuchElementException If the deque is empty.
	 */
	public T dequeueFront() {
		if (isEmpty()) {
			throw new NoSuchElementException("Deque is empty"); // Exception if deque is empty
		}
		return deque.removeFirst(); // Removes and returns the first element
	}

	// --------------------------------------------------------------------------

	/**
	 * Removes and returns the element at the rear (tail) of the deque.
	 * 
	 * @return The element removed from the rear of the deque.
	 * @throws NoSuchElementException If the deque is empty.
	 */
	public T dequeueRear() {
		if (isEmpty()) {
			throw new NoSuchElementException("Deque is empty"); // Exception if deque is empty
		}
		return deque.removeLast(); // Removes and returns the last element
	}

	// --------------------------------------------------------------------------

	// --------- Insert methods

	/**
	 * Inserts an element at the front (head) of the deque.
	 * 
	 * @param data The element to be added to the front of the deque.
	 */
	public void enqueueFront(T data) {
		deque.addFirst(data); // Adds element to the front
	}

	// --------------------------------------------------------------------------

	/**
	 * Inserts an element at the rear (tail) of the deque.
	 * 
	 * @param data The element to be added to the rear of the deque.
	 */
	public void enqueueRear(T data) {
		deque.addLast(data); // Adds element to the back
	}

	// --------------------------------------------------------------------------
}
