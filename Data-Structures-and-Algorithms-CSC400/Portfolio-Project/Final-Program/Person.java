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
 * The class represents an individual with a first name, last name, and age.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 10/06/2024
 */
public class Person {

	private String firstName;
	private String lastName;
	private int age;

	// --------------------------------------------------------------------------
	/*-----------------
	 |  Constructors  |
	 -----------------*/

	/**
	 * Constructs
	 *
	 * @param firstName must be non-null and non-empty
	 * @param lastName  must be non-null and non-empty
	 * @param age       must be non-negative
	 * @throws IllegalArgumentException if the first name or last name are null or
	 *                                  empty, or if the age is negative
	 */
	public Person(String firstName, String lastName, int age) throws IllegalArgumentException {
		// Validate first name and last name (non-null and non-empty)
		if (firstName == null || firstName.trim().isEmpty()) {
			throw new IllegalArgumentException("First name cannot be empty.");
		}
		if (lastName == null || lastName.trim().isEmpty()) {
			throw new IllegalArgumentException("Last name cannot be empty.");
		}
		// Validate age (non-negative)
		if (age < 0) {
			throw new IllegalArgumentException("Age cannot be negative.");
		}

		this.firstName = firstName.trim();
		this.lastName = lastName.trim();
		this.age = age;
	}

	// --------------------------------------------------------------------------
	/*------------
	 |  Getters  |
	 ------------*/

	/**
	 * Gets the first name of the person.
	 *
	 * @return the first name of the person
	 */
	public String getFirstName() {
		return firstName;
	}

	// --------------------------------------------------------------------------

	/**
	 * Gets the last name of the person.
	 *
	 * @return the last name of the person
	 */
	public String getLastName() {
		return lastName;
	}

	// --------------------------------------------------------------------------

	/**
	 * Gets the age of the person.
	 *
	 * @return the age of the person
	 */
	public int getAge() {
		return age;
	}

	// --------------------------------------------------------------------------
	// --- Print

	/**
	 * Gets a string representation of the person, including their first name, last
	 * name, and age.
	 *
	 * @return a string in the format "firstName lastName, Age: age"
	 */
	@Override
	public String toString() {
		return firstName + " " + lastName + ", Age: " + age;
	}

	// --------------------------------------------------------------------------
}
