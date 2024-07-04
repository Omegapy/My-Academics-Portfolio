/*
    Program Name: Abstract Class Shape
    Author: Alejandro (Alex) Ricciardi
    Date: 07/07/2024
    
    Program Description: 
    The program is a small Java program that calculates the surface area and volume of Sphere, Cone, and Cylinder shaped objects.
    It uses JavaFX to create a simple GUI that displays the surface area and volume of these shapes.
*/

/*-------------------
 |     Packages     |
 --------------------*/
package application; // Program Folder

/*--------------------------
|    Imported modules      |
---------------------------*/
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.image.Image;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/**
 * A small JavaFX GUI that displays information about different shapes. This
 * class creates a user interface to show the surface area and volume of a
 * sphere, a cylinder, and a cone. Note: The surface area of a shape is
 * different than the area of a shape.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/07/2024
 */
public class ShapeArray extends Application {

    /**
     * The main entry point for all JavaFX applications. This method sets up the
     * user interface and displays the shape information.
     * 
     * @param primaryStage The primary stage for this application.
     */
    @Override
    public void start(Stage primaryStage) {
	// Create an array of shapes and instansies shapes objects.
	Shape[] shapeArray = new Shape[3];
	shapeArray[0] = new Sphere(5.00);
	shapeArray[1] = new Cone(7.00, 6.00);
	shapeArray[2] = new Cylinder(3.00, 7.00);

	// Create labels for each shape
	Label[] labelArray = new Label[3];
	labelArray[0] = new Label(" Sphere");
	labelArray[1] = new Label(" Cone");
	labelArray[2] = new Label(" Cylinder");

	// Add bold to the labels texts
	for (Label label : labelArray) {
	    label.setStyle("-fx-font-weight: bold; -fx-font-size: 12px;");
	}

	// Create text areas to display shape information
	TextArea[] textArray = new TextArea[3];
	for (int i = 0; i < textArray.length; i++) {
	    textArray[i] = new TextArea(shapeArray[i].toString());
	    textArray[i].setEditable(false);
	}

	// Create a VBox to hold the labels and text areas
	VBox displayBox = new VBox(5);
	for (int i = 0; i < textArray.length; i++) {
	    displayBox.getChildren().addAll(labelArray[i], textArray[i]);
	}

	// Create the root VBox and add the display box to it
	VBox root = new VBox();
	root.setAlignment(Pos.CENTER);
	root.getChildren().addAll(displayBox);
	root.setPadding(new Insets(20));

	// Icon
	try {
	    Image icon = new Image("logo.png");
	    primaryStage.getIcons().add(icon);
	} catch (Exception e) {
	    System.out.print("Icon image not found.");
	}

	// Create the scene and set it on the stage
	Scene scene = new Scene(root, 250, 250);
	primaryStage.setTitle("Shapes");
	primaryStage.setScene(scene);
	primaryStage.show();
    }

    // ==============================================================================================
    /*----------
    |   Main   |
    -----------*/

    /**
     * The main method is the entry point of the Java application. It launches the
     * application
     * 
     * @param args Command line arguments (not used).
     */
    public static void main(String[] args) {
	launch(args);
    }
}