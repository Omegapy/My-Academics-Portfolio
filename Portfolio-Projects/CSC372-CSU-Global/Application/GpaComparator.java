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
 * Comparator for sorting Student objects based on their names. Implements a
 * descending order comparison (highest to lowest GPA), used by the
 * SortSearchUtil class. This class implements the Comparator interface
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/04/2024
 */
public class GpaComparator implements Comparator<Student> {
    /**
     * Compares two students based on their GPA. This method is called by sorting
     * algorithms to determine the order of students. It implements a descending
     * order, so students with higher GPAs come first.
     *
     * @param s1 The first student to be compared.
     * @param s2 The second student to be compared.
     * @return A negative integer, zero, or a positive integer as the first
     *         student's GPA is greater than, equal to, or less than the second
     *         student's GPA.
     */
    @Override
    public int compare(Student s1, Student s2) {
	// Reverse the comparison to sort in descending order
	return Double.compare(s2.getGPA(), s1.getGPA());
    }
}