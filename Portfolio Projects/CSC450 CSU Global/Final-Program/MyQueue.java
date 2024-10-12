/*
    Program Name: Custom Queue ADT and QuickSort
    Author: Alejandro (Alex) Ricciardi
    Date: 10/06/2024
    
    Program Description: 
    This program implements in Java a generic Linked-list queue and sorts the queue using a quicksort algorithm. 
    The queue stores Person objects representing a person first name, last name, and age.
    the Person objects in the queue can be sorted by last name or age.     
*/

/*-------------------
 |     Packages     |
 -------------------*/
package nameAgeQueue;

/**
 * Generic queue ADT (Abstract Data Type) using a linked-list.
 * 
 * @author Alejandro Ricciardi
 * @version 2.0
 * @date 10/06/2024
 *
 * @param <T> the type of elements held in this queue
 */
public class MyQueue<T> {

	private Node<T> front;
	private Node<T> rear;
	private int size;

	// --------------------------------------------------------------------------
	/*------------------
	 |  Inner Classes  |
	 ------------------*/

	/**
	 * Represents a node in the queue. Each node holds the data and a reference to
	 * the next node in the linked-list. The last node next node reference is null.
	 *
	 * @param <T> the type of data held in the node - default generic
	 */
	@SuppressWarnings("hiding")
	public class Node<T> {
		T data; // Data stored in the node
		Node<T> next; // Reference to the next node in the queue

		/**
		 * Constructs a node with data. The next node reference is initialized to null.
		 *
		 * @param data the data held in this node
		 */
		public Node(T data) {
			this.data = data; // the node's data
			this.next = null; // Next node is initially null
		}
	}

	// --------------------------------------------------------------------------
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs an empty queue.
	 */
	public MyQueue() {
		this.front = null;
		this.rear = null;
		this.size = 0;
	}

	// --------------------------------------------------------------------------
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Gets the element at the front of the queue without removing it.
	 *
	 * @return the element at the front of the queue, or null if the queue is empty
	 */
	public T peek() {
		if (isEmpty()) { // If the queue is empty, return null
			System.out.println("Queue is empty. No elements to show.");
			return null;
		}
		return front.data;
	}

	// --------------------------------------------------------------------------

	/**
	 * Checks if the queue is empty.
	 *
	 * @return true if the queue is empty, false otherwise
	 */
	public boolean isEmpty() {
		return size == 0;
	}

	// --------------------------------------------------------------------------

	/**
	 * Gets the number of elements in the queue.
	 *
	 * @return the size of the queue
	 */
	public int getSize() {
		return size;
	}

	// --------------------------------------------------------------------------

	/**
	 * Gets the front node (head) of the queue.
	 *
	 * @return the front node of the queue, or null if the queue is empty
	 */
	public Node<T> getFront() {
		return front;
	}

	// --------------------------------------------------------------------------
	/*------------
	 |  Setters  |
	 ------------*/

	/**
	 * Adds an element to the rear of the queue.
	 *
	 * @param data the element to be added to the queue
	 */
	public void enqueue(T data) {
		Node<T> newNode = new Node<>(data);
		if (rear == null) {
			front = rear = newNode; // Both front and rear to the new node
		} else {
			rear.next = newNode; // Link the new node to the end of the queue
			rear = newNode; // Update the rear to the new node
		}
		size++;
		System.out.println(data + " added to the queue.");
	}

	// --------------------------------------------------------------------------

	/**
	 * Removes and returns the element at the front of the queue.
	 *
	 * @return the element at the front of the queue, or {@code null} if the queue
	 *         is empty
	 */
	public T dequeue() {
		if (isEmpty()) { // If the queue is empty, return null
			System.out.println("Queue is empty. No elements to remove.");
			return null;
		}
		T removedData = front.data; // Get the data of the front node
		front = front.next; // Move the front to the next node
		if (front == null) {
			rear = null; // Set rear to null If front is null
		}
		size--;
		System.out.println(removedData + " removed from the queue.");
		return removedData;
	}

	// --------------------------------------------------------------------------

	/**
	 * Sets the front node of the queue.
	 *
	 * @param front the new front node of the queue
	 */
	public void setFront(Node<T> front) {
		this.front = front;
	}

	// --------------------------------------------------------------------------
	// --- Print

	/**
	 * Prints the elements of the queue in order from front to rear. If the queue is
	 * empty, it prints a message saying that the queue is empty.
	 */
	public void printQueue() {
		if (isEmpty()) {
			System.out.println("Queue is empty.");
			return;
		}
		Node<T> current = front; // Start from the front of the queue
		while (current != null) { // Traverse the queue
			System.out.println(current.data); // Print the data of the current node
			current = current.next; // Move to the next node
		}
	}

	// --------------------------------------------------------------------------
}
