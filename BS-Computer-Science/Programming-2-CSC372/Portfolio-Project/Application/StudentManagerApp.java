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
import java.io.IOException;
import java.util.LinkedList;
import java.util.Optional;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/**
 * Main application class for the Student Manager program. This class creates
 * the user interface (GUI).
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 08/04/2024
 */
public class StudentManagerApp extends Application {
    // Instance of StudentManager to handle student data and file operations
    private StudentManager manager = new StudentManager();
    // Text fields for inputting student information
    private TextField nameField, addressField, gpaField;
    // Constant for setting the width of text fields
    final private int FIELD_SIZE = 250;

    // ==============================================================================================
    /*-----------------
     |   Main  GUI    |
     -----------------*/

    /**
     * The main entry point for the JavaFX application. This method sets up the
     * primary stage and creates the main GUI components.
     *
     * @param primaryStage The primary stage for this application.
     */
    @Override
    public void start(Stage primaryStage) {
	primaryStage.setTitle("Student Manager");

	// Initialize file if no students.txt file is found
	checkAndInitializeFile();

	// Icon
	try {
	    Image icon = new Image("logo.png");
	    primaryStage.getIcons().add(icon);
	} catch (Exception e) {
	    System.out.print("Icon image not found.");
	}

	// Main layout container
	VBox mainLayout = new VBox(10);
	mainLayout.setPadding(new Insets(10));

	// Create input fields
	GridPane inputGrid = new GridPane();
	inputGrid.setHgap(10);
	inputGrid.setVgap(10);
	inputGrid.addRow(0, new Label("Name:"), nameField = new TextField());
	inputGrid.addRow(1, new Label("Address:"), addressField = new TextField());
	inputGrid.addRow(2, new Label("GPA:"), gpaField = new TextField());

	// Set preferred widths for input fields
	nameField.setPrefWidth(FIELD_SIZE);
	addressField.setPrefWidth(FIELD_SIZE);
	gpaField.setPrefWidth(FIELD_SIZE);

	// Create buttons for various actions
	Button addButton = new Button("Add Student");
	Button saveButton = new Button("Save Students To File");
	Button searchButton = new Button("Search Students");
	Button viewAllButton = new Button("View All The Students");

	// Set button actions
	addButton.setOnAction(e -> addStudent());
	saveButton.setOnAction(e -> saveToFile());
	searchButton.setOnAction(e -> searchStudents());
	viewAllButton.setOnAction(e -> viewAllStudents());

	// Arrange buttons in vertical boxes
	VBox addSearchButtonsBox = new VBox(10);
	addSearchButtonsBox.getChildren().addAll(addButton, searchButton);

	VBox saveViewButtonsBox = new VBox(10);
	saveViewButtonsBox.getChildren().addAll(saveButton, viewAllButton);

	// Arrange button boxes horizontally
	HBox buttonBox = new HBox(20);
	buttonBox.setAlignment(Pos.CENTER);
	buttonBox.getChildren().addAll(addSearchButtonsBox, saveViewButtonsBox);

	// Add all elements to the main layout
	mainLayout.getChildren().addAll(inputGrid, buttonBox);

	// Set the scene
	Scene scene = new Scene(mainLayout, 380, 200);
	primaryStage.setScene(scene);
	primaryStage.show();
    }

    // ==============================================================================================
    /*-----------------
     |   Initialize   |
     -----------------*/

    /**
     * Checks if the students file exists and initializes it if necessary. If the
     * file doesn't exist, it prompts the user to either create an empty file or
     * populate it with fake data.
     */
    private void checkAndInitializeFile() {
	if (!manager.fileExists()) {
	    // Create an alert dialog to ask the user about file initialization
	    Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
	    alert.setTitle("File Not Found");
	    alert.setHeaderText("students.txt file was not found");
	    alert.setContentText("Do you want to populate it with fake student data?");

	    // Create custom buttons for the alert
	    ButtonType yesButton = new ButtonType("Yes");
	    ButtonType noButton = new ButtonType("No");
	    alert.getButtonTypes().setAll(yesButton, noButton);

	    // Show the alert and wait for user response
	    Optional<ButtonType> result = alert.showAndWait();
	    if (result.isPresent() && result.get() == yesButton) {
		try {
		    // Populate the file with fake data
		    manager.populateWithFakeData();
		    showAlert("Success", "File populated with fake student data.");
		} catch (IOException e) {
		    showAlert("Error", "Failed to populate file: " + e.getMessage());
		}
	    } else {
		try {
		    // Create an empty file
		    manager.createEmptyFile();
		    showAlert("Success", "Empty students.txt file created.");
		} catch (IOException e) {
		    showAlert("Error", "Failed to create file: " + e.getMessage());
		}
	    }
	}

	// Load existing students from the file
	manager.loadExistingStudents();
    }

    // ==============================================================================================
    /*------------------
     |   New Student   |
     ------------------*/

    /**
     * Adds a new student based on the input fields. This method is called when the
     * "Add Student" button is clicked.
     */
    private void addStudent() {
	try {
	    // Get input values from text fields
	    String name = nameField.getText();
	    String address = addressField.getText();
	    double gpa = Double.parseDouble(gpaField.getText());

	    // Create a new Student object
	    Student student = new Student(name, address, gpa);
	    // Add the student to the manager
	    manager.addStudent(student);

	    // Clear input fields after successful addition
	    nameField.clear();
	    addressField.clear();
	    gpaField.clear();

	    showAlert("Success", "Student added successfully!");
	} catch (NumberFormatException e) {
	    showAlert("Error", "Invalid GPA. Please enter a valid number.");
	} catch (IllegalArgumentException e) {
	    showAlert("Error", e.getMessage());
	}
    }

    // ==============================================================================================
    /*-----------------------
     |  Save All Students   |
     -----------------------*/

    /**
     * Saves all students to the file. This method is called when the "Save Students
     * To File" button is clicked.
     */
    private void saveToFile() {
	try {
	    // Get a copy of newly added students before saving
	    LinkedList<Student> newStudents = new LinkedList<>(manager.getNewlyAddedStudents());

	    // Sort and save all students to file
	    manager.sortAndSaveToFile();
	    // showAlert("Success", "Students saved to file successfully!");

	    // If there are newly added students, display them
	    if (!newStudents.isEmpty()) {
		showStudents("Newly Successfully Added Students", newStudents);
	    }

	} catch (IOException e) {
	    showAlert("Error", "Failed to save to file: " + e.getMessage());
	}
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Displays all students in a new window. This method is called when the "View
     * All The Students" button is clicked.
     */
    private void viewAllStudents() {
	// Get a copy of all students
	LinkedList<Student> students = new LinkedList<>(manager.getStudents());
	// Display students in a new window
	showStudents("All Students", students);
    }

    // ==============================================================================================
    /*-------------------
    |  Search Student   |
    --------------------*/

    /**
     * Opens a new window for searching students. This method is called when the
     * "Search Students" button is clicked.
     */
    private void searchStudents() {
	// Create a new stage for the search window
	Stage searchStage = new Stage();
	searchStage.setTitle("Search Students");

	// Create layout for the search window
	VBox layout = new VBox(10);
	layout.setPadding(new Insets(10));

	// Create search input field
	TextField searchField = new TextField();
	searchField.setPromptText("Enter student name to search");

	// Create search button
	Button searchButton = new Button("Search");
	searchButton.setOnAction(e -> searchStudentByName(searchField.getText()));

	// Add components to the layout
	layout.getChildren().addAll(new Label("Search by name:"), searchField, searchButton);

	// Set the scene for the search window
	Scene scene = new Scene(layout, 300, 150);
	searchStage.setScene(scene);
	searchStage.show();
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Performs a search for students based on a given name. This method is called
     * when the search button in the search window is clicked.
     *
     * @param studentName The name to search for.
     */
    private void searchStudentByName(String studentName) {
	LinkedList<Student> searchResults = new LinkedList<>();

	// Perform binary search to find the student
	int indexResults = SortSearchUtil.binarySearchByName(manager.getStudents(), studentName);

	if (indexResults != -1) {
	    // If student is found, add to search results and display
	    searchResults.add(manager.getStudents().get(indexResults));
	    showStudents("Search Results", searchResults);
	} else {
	    // If student is not found, show alert
	    showAlert("Not Found", "No student found with the name: " + studentName);
	}
    }

    // ==============================================================================================
    /*--------------------------
     |  Display Students List  |
     --------------------------*/

    // @formatter:off
    /**
     * Updates the ListView with the current list of students. 
     * Utilized by the showStudents() method
     *
     * @param listView The ListView to update.
     * @param students The current list of students.
     */
    private void updateListView(ListView<String> listView, LinkedList<Student> students) {
        // Clear existing items in the ListView
        listView.getItems().clear();
        // Add each student to the ListView
        for (Student student : students) {
            listView.getItems().add(student.toString());
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------
 
    // @formatter:off
    /**
     * Displays a list of students in a new window.
     * Utilized by the SaveToFile(), ViewAllStudents(), and SearchStudentByName() methods
     *
     * @param title    The title of the window.
     * @param students The list of students to display.
     */
    private void showStudents(String title, LinkedList<Student> students) {
        // Create a new stage for displaying students
        Stage stage = new Stage();
        stage.setTitle(title);

        // Create a ListView to display students
        ListView<String> studentListView = new ListView<>();
        for (Student student : students) {
            studentListView.getItems().add(student.toString());
        }

        // Create buttons for sorting
        Button sortByNameBtn = new Button("Sort by Name (A-Z)");
        Button sortByGPABtn = new Button("Sort by GPA (Highest to Lowest)");

        // Arrange sorting buttons horizontally
        HBox buttonBox = new HBox(10);
        buttonBox.getChildren().addAll(sortByNameBtn, sortByGPABtn);
        buttonBox.setAlignment(Pos.CENTER);

        // Create main layout for the window
        VBox layout = new VBox(10);
        layout.setPadding(new Insets(10));
        layout.getChildren().addAll(new Label(title + ":"), studentListView, buttonBox);

        // Set actions for sorting buttons
        sortByNameBtn.setOnAction(e -> {
            SortSearchUtil.selectionSort(students, new NameComparator());
            updateListView(studentListView, students);
        });

        sortByGPABtn.setOnAction(e -> {
            SortSearchUtil.selectionSort(students, new GpaComparator());
            updateListView(studentListView, students);
        });

        // Set the scene for the window
        Scene scene = new Scene(layout, 450, 350);
        stage.setScene(scene);
        stage.show();
    }
    
    // ==============================================================================================
    /*-----------------
     |  Alert Dialogs |
     -----------------*/

    /**
     * Displays an alert dialog with the given title and message.
     *
     * @param title   The title of the alert.
     * @param message The message to display in the alert.
     */
    private void showAlert(String title, String message) {
        // Create and configure the alert dialog
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
    
    // ==============================================================================================
    /*----------------
     |  Main Method  |
     ----------------*/

    /**
     * The main method that launches the JavaFX application.
     *
     * @param args Command line arguments (not used).
     */
    public static void main(String[] args) {
        launch(args);
    }
    
    // ---------------------------------------------------------------------------------------------------------
    
}