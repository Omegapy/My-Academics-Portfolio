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
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;
import java.util.Random;

/**
 * Manages student objects and handles file operations. This class is
 * responsible for adding, storing, and retrieving student data, as well as
 * reading from and writing to a file.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/04/2024
 */
public class StudentManager {
    // LinkedList to store all students, including those loaded from file and newly
    // added
    private LinkedList<Student> allStudents;
    // LinkedList to store only newly added students
    private LinkedList<Student> newlyAddedStudents;
    // Constant for the file name where student data is stored
    private static final String FILE_NAME = "students.txt";

    // ==============================================================================================
    /*-----------------
     |  Constructors  |
     -----------------*/

    /**
     * Constructs a new StudentManager object. Initializes the lists for all
     * students and newly added students, and load existing file.
     * 
     */
    public StudentManager() {
	// Initialize both LinkedLists
	allStudents = new LinkedList<>();
	newlyAddedStudents = new LinkedList<>();
	// Load existing students from file, if any.
	loadExistingStudents();
    }

    // ==============================================================================================
    /*------------
     |  Getters  |
     ------------*/

    /**
     * Gets a list of newly added students.
     *
     * @return list of the newly added students.
     */
    public LinkedList<Student> getNewlyAddedStudents() {
	// Return a reference to the newlyAddedStudents list
	return newlyAddedStudents;
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Gets a list of all students.
     *
     * @return list containing all students.
     */
    public LinkedList<Student> getStudents() {
	// Return a reference to the allStudents list
	return allStudents;
    }

    // ==============================================================================================
    /*-----------------------------
     |  Initialize and Load File  |
     -----------------------------*/

    /**
     * Checks if the students file exists.
     *
     * @return true if the file exists, false otherwise.
     */
    public boolean fileExists() {
	// Check if the file exists in the current directory
	return new File(FILE_NAME).exists();
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Creates an empty students file.
     *
     * @throws IOException if an I/O error occurs.
     */
    public void createEmptyFile() throws IOException {
	// Create a new empty file with the specified FILE_NAME
	new File(FILE_NAME).createNewFile();
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Populates the file with fake student data. This method creates 5 students
     * with random data and saves them to the file sorted by name.
     *
     * @throws IOException if an I/O error occurs.
     */
    public void populateWithFakeData() throws IOException {
	Random random = new Random();
	Student student;
	double gpa;
	// Fake Data
	String[] names = { "Miller Alice", "Taylor Bob", "Garcia Charlie", "Lorato David", "Thui Emma" };
	String[] addresses = { "123 Main St Cheyenne WY 82007", "456 Elm St Cheyenne WY 82007",
		"789 Oak St Cheyenne WY 82007", "321 Pine St Cheyenne WY 82007", "654 Maple St Cheyenne WY 82007" };

	// Create and add students to allStudents
	for (int i = 0; i < 5; i++) {
	    // Generate a random GPA between 0.0 and 4.0
	    gpa = 0.0 + (random.nextDouble() * 4.0);
	    // Create a new Student object with fake data
	    student = new Student(names[i], addresses[i], gpa);
	    // Add the student to the allStudents list
	    allStudents.add(student);
	}

	// Sort the students by name
	SortSearchUtil.selectionSort(allStudents, new NameComparator());

	// Save sorted students to file
	try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME))) {
	    for (Student studentToSave : allStudents) {
		// Write each student's data to the file
		writer.write(studentToSave.toSaveString());
		writer.newLine();
	    }
	}
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Loads existing students from the file into the allStudents list.
     */
    public void loadExistingStudents() {
	String address;
	String name;
	double gpa;
	String line;
	String[] parts;

	// Clear the existing allStudents list before loading
	allStudents.clear();

	try (BufferedReader reader = new BufferedReader(new FileReader(FILE_NAME))) {
	    while ((line = reader.readLine()) != null) {
		// Split each line into parts: name, address, GPA
		parts = line.split(", ");
		if (parts.length == 3) {
		    name = parts[0];
		    address = parts[1];
		    gpa = Double.parseDouble(parts[2]);
		    // Create a new Student object and add it to allStudents
		    allStudents.add(new Student(name, address, gpa));
		}
	    }
	} catch (IOException e) {
	    // Print error message if file reading fails
	    System.err.println("Error reading from file: " + e.getMessage());
	}
    }

    // ==============================================================================================
    /*-----------------
    |   Add Student   |
    -----------------*/

    /**
     * Adds a new student to both allStudents and newlyAddedStudents lists.
     *
     * @param student The student to add.
     */
    public void addStudent(Student student) {
	// Add the student to both lists
	allStudents.add(student);
	newlyAddedStudents.add(student);
    }

    // ==============================================================================================
    /*------------------
    |   Sort and Save  |
    -------------------*/

    /**
     * Sorts all students and saves them to the file. Clears the newlyAddedStudents
     * list after saving.
     *
     * @throws IOException if an I/O error occurs.
     */
    public void sortAndSaveToFile() throws IOException {
	// Sort all students by name
	SortSearchUtil.selectionSort(allStudents, new NameComparator());

	try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME))) {
	    for (Student student : allStudents) {
		// Write each student's data to the file
		writer.write(student.toSaveString());
		writer.newLine();
	    }
	}

	// Clear the newlyAddedStudents list after saving
	newlyAddedStudents.clear();
    }

    // ---------------------------------------------------------------------------------------------------------

}