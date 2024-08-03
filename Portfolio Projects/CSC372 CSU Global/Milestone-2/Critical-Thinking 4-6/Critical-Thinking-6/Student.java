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

/**
 * Creates a student object with rollno, name, and address.
 *
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/21/2024
 */
public class Student {
    /** The student's roll number. */
    public int rollno;
    /** The student's name. */
    public String name;
    /** The student's address. */
    public String address;

    // ==============================================================================================
    /*------------------
    |    Constructs    |
    -------------------*/

    /**
     * Construct, creates a new Student object.
     *
     * @param rollno  the student's roll number
     * @param name    the student's name
     * @param address the student's address
     */
    public Student(int rollno, String name, String address) {
        this.rollno = rollno;
        this.name = name;
        this.address = address;
    }

    // ==============================================================================================
    /*-----------------------------------
     |   Object String Representation   |
     -----------------------------------*/

    /**
     * Sets a string representation of the Student object.
     *
     * @return A string containing the student's roll number, name, and address.
     */
    @Override
    public String toString() {
        return "Roll No: " + rollno + ", Name: " + name + ", Address: " + address;
    }

    // ---------------------------------------------------------------------------------------------------------
}

