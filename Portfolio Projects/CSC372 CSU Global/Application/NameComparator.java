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

/**
 * Comparator for sorting Student objects based on their names. Implements an
 * ascending order comparison (A to Z), used by the SortSearchUtil class. This class implements the Comparator
 * interface.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/04/2024
 */
public class NameComparator implements Comparator<Student> {
    /**
     * Compares two students based on their names. This method is called by sorting
     * algorithms to determine the order of students. It implements an ascending
     * order, so students are sorted alphabetically by name.
     *
     * @param s1 The first student to be compared.
     * @param s2 The second student to be compared.
     * @return A negative integer, zero, or a positive integer as the first
     *         student's name is less than, equal to, or greater than the second
     *         student's name.
     */
    @Override
    public int compare(Student s1, Student s2) {
	// Use the built-in String compareTo method for lexicographic comparison
	// This naturally implements an ascending (A to Z) order
	return s1.getName().compareTo(s2.getName());
    }
}