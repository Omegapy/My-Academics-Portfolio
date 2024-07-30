/*
        Program Name: Sort Students
        Author: Alejandro (Alex) Ricciardi
        Date: 07/21/2024

        Program Description:
        The Sort Students program sorts a list of students, allowing users to view
        and sort students by first name or roll number.
        The program uses selection sort to sort the students
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

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.image.Image;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/**
 * Sorts Students and displays results.
 * Extends JavaFX's Application class.
 * Contains the main method.
 *
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/21/2024
 */
public class SortStudents extends Application {

    private ArrayList<Student> students = new ArrayList<>();
    private ListView<Student> studentListView; // JavaFX pane for lists

    // ==============================================================================================
    /*---------------------------
     |    Data Initialization   |
     -------------------------- */

    /**
     * Initializes the list of students with sample data.
     */
    private void initializeStudents() {

        students.add(new Student(110, "Julia Roberts", "159 Walnut St"));
        students.add(new Student(102, "Alice Johnson", "123 Main St"));
        students.add(new Student(106, "George Clooney", "147 Birch St"));
        students.add(new Student(101, "Charlie Brown", "789 Oak St"));
        students.add(new Student(105, "Diana Ross", "321 Pine St"));
        students.add(new Student(103, "Bob Smith", "456 Elm St"));
        students.add(new Student(107, "Fiona Apple", "987 Cedar St"));
        students.add(new Student(108, "Ian McKellen", "369 Ash St"));
        students.add(new Student(109, "Hannah Montana", "258 Spruce St"));
        students.add(new Student(104, "Edward Norton", "654 Maple St"));
    }

    // ==============================================================================================
    /*------------
     |    GUI    |
     ------------*/

    /**
     * The start method is called when the application is launched.
     * It sets up the JavaFX GUI components and functionality of the application.
     *
     * @param primaryStage The primary stage for this application.
     */
    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Student Manager");

        // Initialize student data
        initializeStudents();

        // Create UI components
        studentListView = new ListView<>();
        updateListView();

        // Icon
        try {
            Image icon = new Image("logo.png");
            primaryStage.getIcons().add(icon);
        } catch (Exception e) {
            System.out.print("Icon image not found.");
        }

        // Buttons to sort students
        Button btnSortByName = new Button("Sort by First Name");
        Button btnSortByRollNo = new Button("Sort by Roll No");

        // Set up layout
        HBox hbButtons = new HBox(10);
        hbButtons.getChildren().addAll(btnSortByName, btnSortByRollNo);

        VBox vbox = new VBox(10);
        vbox.getChildren().addAll(hbButtons, studentListView);
        vbox.setPadding(new Insets(10));

        // Set up event handlers
        btnSortByName.setOnAction(e -> {
            System.out.println("-----------------------------------------------------");
            System.out.println("               Sorted by First Name");
            System.out.println("-----------------------------------------------------");
            SortingUtil.selectionSort(students, new SortingUtil.NameComparator());
            updateListView();
        });
        btnSortByRollNo.setOnAction(e -> {
            System.out.println("-----------------------------------------------------");
            System.out.println("               Sorted by Roll No");
            System.out.println("-----------------------------------------------------");
            SortingUtil.selectionSort(students, new SortingUtil.RollNoComparator());
            updateListView();
        });

        // Create scene and show stage
        Scene scene = new Scene(vbox, 400, 300);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Updates the ListView with the current list of students.
     */
    private void updateListView() {
        studentListView.getItems().clear();
        studentListView.getItems().addAll(students);
    }

    // ==============================================================================================
    /*--------------------
     |    Main Method    |
     --------------------*/

    /**
     * The main entry point for the application.
     *
     * @param args Command line arguments (not used in this application).
     */
    public static void main(String[] args) {
        launch(args);
    }

    // ---------------------------------------------------------------------------------------------------------
}