/*
    Program Name: Custom Deque ADT
    Author: Alejandro (Alex) Ricciardi
    Date: 09/22/2024
    
    Program Description: 
    The program is a custom double-ended queue (deque) implementation using Java's LinkedList. 
    It tests the deque insertion, deletion, and iteration functionalities 
    from both the front and the end.

/*-------------------
 |     Packages     |
 -------------------*/
package customDeque; // Program Folder

/*---------------------------
 |    Imported modules      |
 ---------------------------*/
import java.util.Iterator;
import java.util.Random;

/**
 * Tests the iterating functionality of the CostumeDeque class. It adds random
 * integers to the deque and then iterates through them from both the front
 * (head) and the rear (tail).
 * 
 * @author Alejandro (Alex) Ricciardi
 * @version 1.0
 * @date 09/22/2024
 */
class TestCustomDeque {

	/**
	 * Program entry point. It creates an instance of CustomDeque, creates and
	 * enqueues random integers into it from both the front and rear, and test =s
	 * the deque iterating functionality from both the head and the tail.
	 * 
	 * @param args Command-line arguments (not used).
	 */
	public static void main(String[] args) {
		String banner = """

				        ***************************************
				        *     Test Iteranation Custom Deque   *
				        ***************************************
				""";

		CustomDeque<Integer> customDeque = new CustomDeque<Integer>(); // Instances a CustomDeque to hold Integer
																		// elements
		Iterator<Integer> iteratorFromHead; // Iterator for traversing deque from the head (front)
		Iterator<Integer> iteratorFromTail; // Iterator for traversing deque from the tail (rear)
		int randomInt; // Store random integer values

		System.out.println(banner);

		// ------------------------------------------------------------
		// --- Generate ten random integers and add them to the deque
		Random rand = new Random();
		System.out.println("Enqueuing elements:");
		for (int i = 0; i < 10; i++) {
			randomInt = rand.nextInt(100); // Random integer between 0 and 99
			// Randomly assign integer to the head or to the tail of the deque
			if (rand.nextBoolean()) { // Front
				customDeque.enqueueFront(randomInt);
				System.out.println("Enqueued " + randomInt + " at front.");
			} else { // Rear
				customDeque.enqueueRear(randomInt);
				System.out.println("Enqueued " + randomInt + " at rear.");
			}
		}

		// ------------------------------------------------------------
		// --- Display elements after initial enqueuing
		displayElements(customDeque, "Initial elements (iterating from head):", true);
		displayElements(customDeque, "Initial elements (iterating from tail):", false);

		// ------------------------------------------------------------
		// --- Test 1: Deleting elements from the front and rear (tail)
		System.out.println("\n\n------------------------------------------------------------");
		System.out.println("Test 1: Deleting elements from front and rear");

		displayElements(customDeque, "Initial elements (iterating from head) before deleting:", true);
		customDeque.dequeueFront();
		displayElements(customDeque, "Elements after deleting from front (from head):", true);
		System.out.println();
		displayElements(customDeque, "Initial elements (iterating from tail) before deleting:", false);
		customDeque.dequeueRear();
		displayElements(customDeque, "Elements after deleting from rear (from tail):", false);

		// ------------------------------------------------------------
		// --- Test 2: Adding elements to the front and rear
		System.out.println("\n\n------------------------------------------------------------");
		System.out.println("Test 2: Adding elements to front and rear");

		displayElements(customDeque, "Initial elements (iterating from head) before adding 50 to head:", true);
		customDeque.enqueueFront(50);
		displayElements(customDeque, "Elements after adding 50 to front (from head):", true);
		System.out.println();
		displayElements(customDeque, "Initial elements (iterating from tail) before adding 99 to tail:", false);
		customDeque.enqueueRear(99);
		displayElements(customDeque, "Elements after adding 99 to rear (from tail):", false);

		// ------------------------------------------------------------
		// --- Test 3: Testing hasNext() and next() functionality from the head
		System.out.println("\n\n------------------------------------------------------------");
		System.out.println("Test 3: Testing hasNext() and next() functionality (from head)\n");

		iteratorFromHead = customDeque.iterator(); // Iterator from the head
		System.out.println("Iterating and displaying using next():");

		while (iteratorFromHead.hasNext()) {
			System.out.print(iteratorFromHead.next() + " ");
		}

		System.out.println("\nTesting hasNext() trying after iterating from head: " + iteratorFromHead.hasNext());

		// ------------------------------------------------------------
		// --- Test 4: Testing hasNext() and next() from the tail
		System.out.println("\n------------------------------------------------------------");
		System.out.println("Test 4: Testing hasNext() and next() functionality (from tail)\n");

		iteratorFromTail = customDeque.iterator(false); // Iterator from the tail
		System.out.println("Iterating and displaying using next():");

		while (iteratorFromTail.hasNext()) {
			System.out.print(iteratorFromTail.next() + " ");
		}

		System.out.println("\nTesting hasNext() trying after iterating from tail: " + iteratorFromTail.hasNext());

		// ------------------------------------------------------------
	}

	// ================================================================
	/*-------------------
	 |  Helper Methods  |
	 -------------------*/

	/**
	 * Displays deque elements using an iterator.
	 * 
	 * @param deque        The deque to iterate over.
	 * @param message      Message to display before showing the elements.
	 * @param iterateFront If true, iterate from front; if false, iterate from rear.
	 */
	private static void displayElements(CustomDeque<Integer> deque, String message, boolean iterateFront) {
		System.out.println("\n" + message);
		Iterator<Integer> iterator = deque.iterator(iterateFront);
		while (iterator.hasNext()) {
			System.out.print(iterator.next() + " ");
		}
	}

	// ------------------------------------------------------------
}
