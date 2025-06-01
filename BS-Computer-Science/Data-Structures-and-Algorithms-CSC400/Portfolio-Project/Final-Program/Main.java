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

import java.util.Comparator;
import java.util.LinkedList;
import java.util.Scanner;
import java.util.regex.Pattern;

/**
 * Tests MyQueue and MyQuickSort classes with a queue of Person objects.
 *
 * @author
 * @version 1.0
 * @date 10/06/2024
 */
public class Main {
	/**
	 * Test the queue and the quick sort. It prompts the user to enter data for five
	 * Person objects, adds them to the queue, sorts the queue based on last name
	 * and age, and displays the contents of the queue.
	 *
	 * @param args command-line arguments (not used)
	 */
	public static void main(String[] args) {
		String banner = """

				    ***************************************
				    *   Test Custom Queue and QuickSort   *
				    ***************************************
				""";

		MyQueue<Person> personQueue = new MyQueue<>(); // Queue to store Person objects
		Person person;

		int count = 0; // count people entered

		Scanner scanner = new Scanner(System.in); // Scanner for user input
		String firstName, lastName, ageInput;
		int age;

		// Regex pattern to match integers
		Pattern integerPattern = Pattern.compile("^\\d+$");

		System.out.println(banner);

		// --------------------------------------------------------------------------
		System.out.println("\n--------------------------------------------------------------------------\n");
		personQueue.printQueue();
		System.out.println("Number of elements in the queue: " + personQueue.getSize());

		// --------------------------------------------------------------------------

		// Prompt user to add five people to the queue
		System.out.println("\n--------------------------------------------------------------------------\n");
		System.out.println("Please enter details for five people.");
		while (count < 5) {
			try {
				System.out.println("\nPerson " + (count + 1));

				// Prompt for first name
				System.out.print("First Name: ");
				firstName = scanner.nextLine().trim();

				// Prompt for last name
				System.out.print("Last Name: ");
				lastName = scanner.nextLine().trim();

				// Prompt for age and validate it is an integer
				while (true) {
					System.out.print("Age: ");
					ageInput = scanner.nextLine().trim();
					// Use regex to ensure age is an integer
					if (integerPattern.matcher(ageInput).matches()) {
						age = Integer.parseInt(ageInput);
						break;
					} else {
						System.out.println("Invalid input. Please enter a valid integer for age.");
					}
				}

				// Create a new Person object and add it to the queue
				person = new Person(firstName, lastName, age);
				personQueue.enqueue(person); // Enqueue the Person
				count++;
			} catch (IllegalArgumentException e) {
				// Handle exceptions from the Person class (invalid input)
				System.out.println("Error: " + e.getMessage());
				System.out.println("Please re-enter the details for this person.");
			} catch (Exception e) {
				// Handle any other unexpected exceptions
				System.out.println("An unexpected error occurred: " + e.getMessage());
				System.out.println("Please re-enter the details for this person.");
			} // While loop
		}

		// --------------------------------------------------------------------------

		// Display the contents of the queue
		System.out.println("\n--------------------------------------------------------------------------\n");
		System.out.println("Queue Contents:\n");
		personQueue.printQueue();
		System.out.println("\nNumber of elements in the queue: " + personQueue.getSize());

		// --------------------------------------------------------------------------

		// Sort and display the queue elements by age in descending order
		sortByAge(personQueue);

		// --------------------------------------------------------------------------

		// Sort and display the elements queue by last name in descending order
		sortByLastName(personQueue);

		// --------------------------------------------------------------------------

		// Dequeue an element and redisplay the queue
		System.out.println("\n--------------------------------------------------------------------------\n");
		System.out.println("Dequeueing one person from the queue...\n");
		Person dequeuedPerson = personQueue.dequeue();
		if (dequeuedPerson != null) {
			System.out.println("Dequeued: " + dequeuedPerson);
		}
		System.out.println("\nQueue Contents after dequeue:\n");
		personQueue.printQueue();
		System.out.println("\nNumber of elements in the queue: " + personQueue.getSize());
		System.out.println("\nNote: The first element in the queue was removed based on the FIFO principle.");

		// --------------------------------------------------------------------------

		// Sort and display the queue elements by age in descending order
		sortByAge(personQueue);

		// --------------------------------------------------------------------------

		// Dequeue an element and redisplay the queue
		System.out.println("\n--------------------------------------------------------------------------\n");
		System.out.println("Dequeueing one person.\n");
		dequeuedPerson = personQueue.dequeue();
		if (dequeuedPerson != null) {
			System.out.println("Dequeued: " + dequeuedPerson);
		}
		System.out.println("\nQueue Contents after dequeue:\n");
		personQueue.printQueue();
		System.out.println("\nNumber of elements in the queue: " + personQueue.getSize());
		System.out.println("\nNote: The first element in the queue was removed based on the FIFO principle.");

		// --------------------------------------------------------------------------

		// Sort and display the queue elements by last name in descending order
		sortByLastName(personQueue);

		// --------------------------------------------------------------------------

		// Close the scanner
		scanner.close();
	}

	// --------------------------------------------------------------------------

	/**
	 * Sorts the queue elements by age in descending order and display them.
	 *
	 * @param personQueue the queue of Person objects to be sorted
	 */
	private static void sortByAge(MyQueue<Person> personQueue) {
		LinkedList<Person> sortedByAge;
		// Sort the queue elements by age in descending order
		System.out.println("\n--------------------------------------------------------------------------\n");
		System.out.println("Sorting queue elements by age in descending order:");
		sortedByAge = MyQuickSort.quickSort(personQueue, new Comparator<Person>() {
			@Override
			public int compare(Person p2, Person p1) {
				return Integer.compare(p1.getAge(), p2.getAge());
			}
		});
		System.out.println();
		printLinkedList(sortedByAge);
		System.out.println(
				"\nNote: The sort does not modify the queue,\n it returns a sorted LinkedList of the queue elements.");
	}

	// --------------------------------------------------------------------------

	/**
	 * Sorts the queue elements by last name in descending order and display them.
	 *
	 * @param personQueue the queue of Person objects to be sorted
	 */
	private static void sortByLastName(MyQueue<Person> personQueue) {
		LinkedList<Person> sortedByLastName;
		// Sort the elements queue by last name in descending order
		System.out.println("\n--------------------------------------------------------------------------\n");
		System.out.println("Sorting queue elements by last name in descending order:");
		sortedByLastName = MyQuickSort.quickSort(personQueue, new Comparator<Person>() {
			@Override
			public int compare(Person p1, Person p2) {
				return p2.getLastName().compareTo(p1.getLastName());
			}
		});
		System.out.println();
		printLinkedList(sortedByLastName);
		System.out.println(
				"\nNote: The sort does not modify the queue,\n it returns a sorted LinkedList of the queue elements.");
	}

	// --------------------------------------------------------------------------

	/**
	 * Print a LinkedList of Person objects.
	 *
	 * @param list the LinkedList to print
	 */
	private static void printLinkedList(LinkedList<Person> list) {
		if (list == null || list.isEmpty()) {
			System.out.println("List is empty.");
			return;
		}
		for (Person person : list) {
			System.out.println(person);
		}
	}

	// --------------------------------------------------------------------------
}
