/*
        Program Name: Sort Students
        Author: Alejandro (Alex) Ricciardi
        Date: 07/21/2024

        Program Description:
        The Sort Students program sorts a list of students, allowing users to view
        and sort students by first name or roll number.
        The program uses selection sort to sort the students.
*/

/*-------------------
 |     Packages     |
 -------------------*/
package omegapy.sortingsearchingstudents; // Program Folder

/*---------------------------
 |    Imported modules      |
 ---------------------------*/
import java.util.ArrayList;
import java.util.Comparator;

/**
 * Utility class providing sorting algorithms for Student objects.
 *
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/21/2024
 */
public class SortingUtil {

    // ==============================================================================================
    /*-----------------------
     |    Inner Classes     |
     ---------------------- */

    /**
     * The class implement the Comparator Interface to compares student names (first + last Name).
     */
    public static class NameComparator implements Comparator<Student> {
        /**
         * Compares two Student objects names.
         *
         * @param s1 the first Student to be compared.
         * @param s2 the second Student to be compared.
         * @return a negative integer, zero, or a positive integer as the first argument
         *         is less than, equal to, or greater than the second.
         */
        @Override
        public int compare(Student s1, Student s2) {
            return s1.name.compareTo(s2.name);
        }
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * The class implement the Comparator Interface to compares student roll numbers.
     */
    public static class RollNoComparator implements Comparator<Student> {
        /**
         * Compares two Student objects roll numbers.
         *
         * @param s1 the first Student to be compared.
         * @param s2 the second Student to be compared.
         * @return a negative integer, zero, or a positive integer as the first argument
         *         is less than, equal to, or greater than the second.
         */
        @Override
        public int compare(Student s1, Student s2) {
            return Integer.compare(s1.rollno, s2.rollno);
        }
    }

    // ==============================================================================================
    /*-----------------------
     |    Sort Algorithms   |
     ---------------------- */

    /**
     * Sorts an ArrayList of Student objects using the selection sort algorithm.
     *
     * @param students   The ArrayList of Student objects to be sorted.
     * @param comparator The Comparator used compare students.
     */
    public static void selectionSort(ArrayList<Student> students, Comparator<Student> comparator) {
        int n = students.size();
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;
            // Find the minimum element in the unsorted part of the list
            for (int j = i + 1; j < n; j++) {
                if (comparator.compare(students.get(j), students.get(minIndex)) < 0) {
                    minIndex = j;
                }
            }
            // Swap the found minimum element with the first element of the unsorted part
            if (minIndex != i) {
                Student temp = students.get(i);
                students.set(i, students.get(minIndex));
                students.set(minIndex, temp);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------------------
}
