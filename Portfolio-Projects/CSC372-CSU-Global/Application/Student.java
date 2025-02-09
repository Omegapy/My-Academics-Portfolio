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

/**
 * Creates student objects. This class stores student data and provides methods
 * for data access and validation. It implements the Comparable interface to be
 * used by the SortSearchUtil class to sort and search students
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/04/2024
 */
public class Student implements Comparable<Student> {
    // The name of the student
    private String name;
    // The address of the student
    private String address;
    // The Grade Point Average (GPA) of the student
    private double gpa;

    // ==============================================================================================
    /*-----------------
     |  Constructors  |
     -----------------*/

    /**
     * Constructs a new Student object.
     *
     * @param name    The name of the student.
     * @param address The address of the student.
     * @param gpa     The GPA of the student.
     * @throws IllegalArgumentException if any of the parameters are invalid.
     */
    public Student(String name, String address, double gpa) {
	setName(name);
	setAddress(address);
	setGPA(gpa);
    }

    // ==============================================================================================
    /*------------
     |  Getters  |
     ------------*/

    /**
     * Gets the name of the student.
     *
     * @return The student's name.
     */
    public String getName() {
	return name;
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Gets the address of the student.
     *
     * @return The student's address.
     */
    public String getAddress() {
	return address;
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Gets the GPA of the student.
     *
     * @return The student's GPA.
     */
    public double getGPA() {
	return gpa;
    }

    // ==============================================================================================
    /*------------
     |  Setters  |
     ------------*/

    /**
     * Sets the name of the student.
     * 
     * @param name The new name to set.
     * @throws IllegalArgumentException if the name is null or empty.
     */
    public void setName(String name) {
	// Check if the name is null or empty (after trimming whitespace)
	if (name == null || name.trim().isEmpty()) {
	    throw new IllegalArgumentException("Name cannot be empty");
	}
	this.name = name;
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the address of the student.
     *
     * @param address The new address to set.
     * @throws IllegalArgumentException if the address is null or empty.
     */
    public void setAddress(String address) {
	// Check if the address is null or empty (after trimming whitespace)
	if (address == null || address.trim().isEmpty()) {
	    throw new IllegalArgumentException("Address cannot be empty");
	}
	this.address = address;
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the GPA of the student.
     *
     * @param gpa The new GPA to set.
     * @throws IllegalArgumentException if the GPA is not between 0.0 and 4.0.
     */
    public void setGPA(double gpa) {
	// Check if the GPA is within the valid range
	if (gpa < 0 || gpa > 4.0) {
	    throw new IllegalArgumentException("GPA must be between 0.0 and 4.0");
	}
	this.gpa = gpa;
    }

    // ==============================================================================================
    /*--------------------------
     |  Special Functionality  |
     --------------------------*/

    /**
     * Compares this student with another student based on their names.
     *
     * @param other The other student to compare with.
     * @return A negative integer, zero, or a positive integer as this student's
     *         name is less than, equal to, or greater than the specified student's
     *         name.
     */
    @Override
    public int compareTo(Student other) {
	return this.name.compareTo(other.name);
    }

    // ==============================================================================================
    /*---------------------
     |  Object To String  |
     ---------------------*/

    // @formatter:off
    /**
     * Returns a string representation of the student. 
     * This method overrides the default toString method from Object class.
     * Example: "Name: Miller Alice, Address: 123 Main St Cheyenne WY 82007, GPA: 1.65"
     * 
     * @return A formatted string containing the student's name, address, and GPA.
     */
    @Override
    public String toString() {
        // Use String.format for consistent formatting
        return String.format("Name: %s, Address: %s, GPA: %.2f", name, address, gpa);
    }
    
    // ---------------------------------------------------------------------------------------------------------

    // @formatter:off
    /**
     * Returns a string representation of the student to be saved in file. 
     * Example: "Miller Alice, 123 Main St Cheyenne WY 82007, 1.65"
     * 
     *
     * @return A formatted string containing the student's name, address, and GPA.
     */
    public String toSaveString() {
        // Use String.format for consistent formatting
        return String.format("%s, %s, %.2f", name, address, gpa);
    }
    
    // ---------------------------------------------------------------------------------------------------------
    
}