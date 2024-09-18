/*
    Program Name: Custom Deque
    Author: Alejandro (Alex) Ricciardi
    Date: 09/22/2024
    
    Program Description: 
    The program is a custom double-ended queue (deque) implementation using Java's LinkedList.
*/

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
		// --- Iterate and display elements from head
		System.out.println("\nIterating from head:");
		iteratorFromHead = customDeque.iterator();
		while (iteratorFromHead.hasNext()) {
			System.out.print(iteratorFromHead.next() + " ");
		}

		// ------------------------------------------------------------
		// --- Iterate and display elements from tail
		System.out.println("\n\nIterating from tail:");
		iteratorFromTail = customDeque.iterator(false);
		while (iteratorFromTail.hasNext()) {
			System.out.print(iteratorFromTail.next() + " ");
		}

		// ------------------------------------------------------------
	}
}
