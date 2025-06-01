/*
    Program Name: Infix Calculator
    Author: Alejandro (Alex) Ricciardi
    Date: 09/08/2024
    
    Program Description: 
    - The program is an implementation of an Infix calculator that evaluates arithmetic expressions in infix notation.
    - The program converts Infix expressions stored in a text file into Postfix expressions,
      then computes the Postfix expressions and displays the computation results.
    - The program utilizes a Stack Abstract Data Structure (Stack ADT) to manage operators and operands 
      when converting Infix expressions to Postfix form and during evaluation of Postfix expressions.
    - The Stack ADT is a linked list structure or chain using generic types.
      [element | next] -> [element | next] -> [element | next] -> null.
*/

/*-------------------
 |     Packages     |
 -------------------*/
package infixCalculator; // Program Folder

import java.util.EmptyStackException;

/**
 * A Stack ADT class that implements a stack using a linked list structure, a
 * chain, to store elements. Each node contains data and a reference to the next
 * node in the chain.
 *
 * @param <T> the type of elements in this stack
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 09/08/2024
 */
public class LinkedStack<T> {

	private Node top; // The top element in the stack
	private int size; // Number of elements in the stack

	// ==============================================================================================
	/*------------------
	 |  Inner Classes  |
	 ------------------*/

	/**
	 * Inner Node class for linked structure. Each Node object contains an element
	 * of type T and a reference to the next node.
	 */
	private class Node {
		T data; // Data stored in the node
		Node next; // Reference to the next node in the chain

		/**
		 * Constructor to create a node with the given data.
		 *
		 * @param data the element stored in this node
		 */
		public Node(T data) {
			this.data = data;
			this.next = null;
		}
	}

	// ==============================================================================================
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs an empty stack.
	 */
	public LinkedStack() {
		this.top = null;
		this.size = 0;
	}

	// ==============================================================================================
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Retrieves the top element in the stack without removing it .
	 * 
	 * @return the data of the top element in the stack
	 * @throws IllegalStateException if the stack is empty
	 */
	public T peek() throws EmptyStackException {
		if (isEmpty()) {
			throw new EmptyStackException();
		}
		return top.data; // Return the data of the top node
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Checks if the stack is empty.
	 * 
	 * @return true if the stack is empty, false otherwise
	 */
	public boolean isEmpty() {
		return top == null; // Stack is empty if top is null
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Returns the number of elements in the stack.
	 * 
	 * @return the size of the stack
	 */
	public int size() {
		return size;
	}

	// ==============================================================================================
	/*------------
	 |  Setters  |
	 ------------*/

	/**
	 * Adds a new element to the top of the stack.
	 * 
	 * @param newElement the element to add to the stack
	 */
	public void push(T newElement) {
		Node newNode = new Node(newElement); // Create a new node
		newNode.next = top; // Link the new node to the current top
		top = newNode; // Update the top reference to the new node
		size++; // Increment the stack size
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Removes and returns the stack's top element.
	 * 
	 * @return the data of the removed element
	 * @throws IllegalStateException if the stack is empty
	 */
	public T pop() throws EmptyStackException {
		if (isEmpty()) {
			throw new EmptyStackException();
		}
		T topData = top.data; // Retrieve the data of the top node
		top = top.next; // Move the top reference to the next node
		size--; // Decrement the stack size
		return topData; // Return the popped data
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Clears the stack by setting each node to null. This ensures that all nodes
	 * eligible for garbage collection.
	 * 
	 * @return true if all elements were successfully nullified, false otherwise
	 */
	public boolean clear() throws Exception {
		try {
			Node current = top;
			while (current != null) {
				Node temp = current.next; // Keep reference to the next node
				current = null; // Set the current node to null
				current = temp; // Move to the next node
			}
			top = null;
			size = 0;

			return true;
		} catch (Exception e) {
			throw new Exception("An error occure when clearing the stack:\n" + e.getMessage());
		}
	}

	// ----------------------------------------------------------------------------------------------

}
