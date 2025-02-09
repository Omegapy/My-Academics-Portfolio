/*
    Program Name: Students Manager
    Author: Alejandro (Alex) Ricciardi
    Date: 008/042024
    
    Program Description: 
    The Students Manager is a small Java application that utilizes JavaFX GUI 
    allowing the user to add, view, search, and sort students data: 
        - Student data management (name, address, GPA)
        - File-based storage
        - Sorting by name or GPA
        - Search functionality
        - Basic data validation
*/

/*-------------------
 |     Packages     |
 --------------------*/
package application; // Program Folder

/*---------------------------
 |    Imported modules      |
 ---------------------------*/
import java.util.Comparator;
import java.util.LinkedList;

/**
 * Utility class for sorting and searching students. Provides methods for
 * selection sort and binary search on a LinkedList of Student objects.
 * 
 * @author Alejandro Ricciardi
 * @version 1.1
 * @since 08/04/2024
 */
public class SortSearchUtil {

    /**
     * Sorts the given LinkedList of students using the selection sort algorithm.
     *
     * @param students   The LinkedList of students to be sorted.
     * @param comparator The Comparator used to determine the order of the students.
     */
    public static void selectionSort(LinkedList<Student> students, Comparator<Student> comparator) {
	int n = students.size();
	Student temp;

	// Iterate through the list
	for (int i = 0; i < n - 1; i++) {
	    int minIndex = i;

	    // Find the minimum element in the unsorted portion
	    for (int j = i + 1; j < n; j++) {
		if (comparator.compare(students.get(j), students.get(minIndex)) < 0) {
		    minIndex = j;
		}
	    }

	    // Swap the found minimum element with the first element of the unsorted portion
	    if (minIndex != i) {
		temp = students.get(i);
		students.set(i, students.get(minIndex));
		students.set(minIndex, temp);
	    }
	}
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Performs a binary search on the sorted LinkedList of students to find a
     * student by name.
     *
     * @param students    The sorted LinkedList of students to search.
     * @param studentName The name of the student to search for.
     * @return The index of the found student, or -1 if not found.
     */
    public static int binarySearchByName(LinkedList<Student> students, String studentName) {
	int mid;
	int comparison;
	int left = 0;
	int right = students.size() - 1;

	// Create a comparator for comparing student names
	Comparator<Student> comparator = new NameComparator();

	// Create a temporary student object with the target name for comparison
	Student studentTarget = new Student(studentName, "tempAddress", 0.0);
	System.out.println("Searching for: " + studentTarget.getName());

	// Perform binary search
	while (left <= right) {
	    // Calculate the middle index
	    mid = left + (right - left) / 2;
	    System.out.println("Comparing with: " + students.get(mid).getName());

	    // Compare the middle student with the target student
	    comparison = comparator.compare(students.get(mid), studentTarget);

	    if (comparison == 0) {
		return mid; // Student found
	    } else if (comparison < 0) {
		left = mid + 1; // Search the right half
	    } else {
		right = mid - 1; // Search the left half
	    }
	}

	return -1; // Student not found
    }

    // ---------------------------------------------------------------------------------------------------------
}