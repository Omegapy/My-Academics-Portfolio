/*
    Program Name: Grocery Price Calculator
    Author: Alejandro (Alex) Ricciardi
    Date: 07/14/2024
    
    Program Description: 
    Grocery Price Calculator is a small JavaFX program that calculates the total sum of user inputed grocery prices.
    It calculates the total cost using recursion. 
*/

/*-------------------
 |     Packages     |
 --------------------*/
package application; // Program Folder

/*---------------------------
|    Imported modules      |
---------------------------*/
import java.util.ArrayList;

// JavaFX imports
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/**
 * GroceryCalculator extends the JafaFx Application class. It is GUI that
 * accepts user grocery item price inputs, validates inputs, and calculates and
 * displays the items' prices sum after 5 items were entered or after the
 * 'Calculate Total' button was selected. The class contains the main method.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/14/2024
 */
public class GroceryCalculator extends Application {

    private ArrayList<TextField> priceFields = new ArrayList<>(); // Stores Prices
    private VBox priceFieldsContainer; // GUI contains instruction label, item price fields, and total button
    private Stage primaryStage; // GUI main stage (window)
    private Scene scene; // GUI contains GUI components
    private static final int INITIAL_HEIGHT = 150; // Initial window height
    private static final int HEIGHT_INCREMENT = 30; // Used to add 30px to the window height
    private int numItemsEntered; // Keeps track of the number of items entered by the user

    // ==============================================================================================
    /*-----------------
    |   Main  GUI    |
    -----------------*/

    /**
     * The main entry point for the JavaFX application. Sets stage, scene, root
     * VBox, instruction Label, price fields container VBox, and total button.
     * 
     * @param primaryStage the primary stage
     */
    @Override
    public void start(Stage primaryStage) {
	this.primaryStage = primaryStage;
	primaryStage.setTitle("Grocery Calculator");

	// Icon
	try {
	    Image icon = new Image("logo.png");
	    primaryStage.getIcons().add(icon);
	} catch (Exception e) {
	    System.out.print("Icon image not found.");
	}

	// Main container
	VBox root = createMainLayout();

	scene = new Scene(root, 300, INITIAL_HEIGHT);
	primaryStage.setScene(scene);
	primaryStage.show();

	addNewPriceField(); // Recursive, adds item fields
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Creates and returns the main layout.
     * 
     * @return VBox containing the main layout, root
     */
    private VBox createMainLayout() {
	VBox root = new VBox(10);
	root.setPadding(new Insets(20));
	Label instLabel = new Label("Enter the prices of items\n(press Enter to add more):");
	root.getChildren().add(instLabel);

	// Contains the the price fields
	priceFieldsContainer = new VBox(5);
	root.getChildren().add(priceFieldsContainer);
	// Button
	Button calculateButton = new Button("Calculate Total");
	// Base case-1 for the recursive addNewItemField() method
	calculateButton.setOnAction(e -> calculateTotal(this.priceFields.size())); // Calculates total if clicked
	root.getChildren().add(calculateButton);

	return root;
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Recursive Method. Adds a new text item price field after the enter key is
     * pressed. Until the 'Calculate Total" button is clicked or the user entered 5
     * items. Adjusts the window size.
     */
    private void addNewPriceField() {
	TextField itemField = new TextField();
	itemField.setPromptText("Price of item #" + (priceFields.size() + 1));
	priceFields.add(itemField);
	priceFieldsContainer.getChildren().add(itemField);

	// ---- Base case-1: 'Calculate Total' button selected ----
	// The 'Calculate Total' button event listener is found in the
	// createMainLayout() method.

	// ---- Base case-2: 5 items prices were entered ----
	// This was implemented to meet the assignment requirements
	if (numItemsEntered == 5) {
	    numItemsEntered = 0;
	    calculateTotal(this.priceFields.size());
	}

	// ---- Recursive case ----
	// Listens for 'enter' key is pressed to add new item field
	itemField.setOnKeyPressed(event -> {
	    if (event.getCode() == KeyCode.ENTER) { // Enter key pressed
		if (validatePrice(itemField)) { // Validates input
		    if (itemField == priceFields.get(priceFields.size() - 1)) {
			numItemsEntered++;
			// ---- Recursive call ----
			addNewPriceField();
		    }
		}
	    }
	});

	// -- This code is run if the Recursive case is not meet.
	// Adjusts window height to accommodate new price fields
	int newHeight = INITIAL_HEIGHT + (priceFields.size() * HEIGHT_INCREMENT);
	primaryStage.setHeight(newHeight);

	// Focuses cursor on the new field
	itemField.requestFocus();
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Displays the total price of all items.
     * 
     * @param total the total price to display
     */
    private void showTotal(double total) {
	Alert alert = new Alert(Alert.AlertType.INFORMATION);
	alert.setTitle("Total Price");
	alert.setHeaderText(null);
	alert.setContentText(String.format("The total price of your groceries is: $%.2f", total));
	alert.setOnCloseRequest(e -> resetMainWindow());
	alert.showAndWait();
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Resets the main window to its initial state. Clears all price fields and
     * resets the window size.
     */
    private void resetMainWindow() {
	priceFields.clear();
	VBox newRoot = createMainLayout();
	scene.setRoot(newRoot);
	primaryStage.setHeight(INITIAL_HEIGHT);
	addNewPriceField(); // Add the first item field after reset
    }

    // ==============================================================================================
    /*-----------------------
     |   Input Validation   |
     -----------------------*/

    /**
     * Validates user input to match currency format (e.g., 12.99) If the input is
     * invalid, it sets a red border on the price field and shows an error alert.
     * 
     * @param priceField The TextField to validate
     * @return true if the price is valid or the field is empty, false otherwise
     */
    private boolean validatePrice(TextField priceField) {
	String input = priceField.getText();
	// Invalid input: using Regex, doesn't match currency format (e.g., 12.99)
	if (!input.matches("\\d+(\\.\\d{1,2})?")) {
	    priceField.setStyle("-fx-border-color: red;"); // Highlights price field in red
	    invalidInputAlert("Invalid Input", "Please enter a valid price (e.g., 12.99).", () -> {
		priceField.clear(); // Clears the invalid input
		priceField.setStyle(""); // Resets the field style
		priceField.requestFocus(); // Sets the cursor focus back to the price field that generated the error
	    });
	    return false;
	} else {
	    priceField.setStyle(""); // Resets style if valid
	    return true;
	}
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Displays an the invalid input alert window.
     * 
     * @param title         The title of the alert dialog
     * @param content       The main message content of the alert dialog
     * @param onCloseAction A Runnable to be executed when the alert is closed with
     *                      OK button
     */
    private void invalidInputAlert(String title, String content, Runnable onCloseAction) {
	Alert alert = new Alert(Alert.AlertType.ERROR);
	alert.setTitle(title);
	alert.setHeaderText(null);
	alert.setContentText(content);

	// Show the alert and wait for it to be closed
	alert.showAndWait().ifPresent(response -> {
	    if (response == ButtonType.OK) {
		// Execute the provided action only if OK was clicked
		onCloseAction.run();
	    }
	});
    }

    // ==============================================================================================
    /*-------------------
     |   Calculations   |
     --------------------*/

    /**
     * Calculates the total price of all items Displays the result in a information
     * window.
     */
    private void calculateTotal(int numItems) {
	int index = numItems - 1;
	double total = sumPrices(index);

	// The last text field input was entered without using the enter key and the
	// input was invalid
	if (total == -1.00) {
	    return;
	}

	showTotal(total);
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Recursive method. It calculates the sum of all prices entered.
     * 
     * @param index the current index in the price fields list
     * @return the sum of all prices from the current index to the end of the list
     */
    private double sumPrices(int index) {
	// Initialized to 0.00 in case the "Calculate Total" is clicked and the last
	// price field is empty
	double price = 0.00;

	// ---- Base case: The last item in the list was computed ----
	if (index == -1) {
	    return 0.00; // the sum of the item prices is computed recursively this adds 0.00 to the sum
	}

	// ---- Recursive case ----
	if (!priceFields.get(index).getText().isEmpty()) { // Checks if the last price is empty
	    if (validatePrice(priceFields.get(index))) { // Validates input
		price = Double.parseDouble(priceFields.get(index).getText());
	    } else { // An invalid input was entered and the ‘Calculate Total’ button was clicked
		     // (The 'enter' key was not pressed)
		return -1;
	    }
	}
	--index;
	// ---- Recursive call ----
	// the sum of the item prices is computed recursively
	return price + sumPrices(index);
    }

    // ==============================================================================================
    /*-------------------
     |   Main  Method   |
     -------------------*/

    /**
     * The main method that launches the JavaFX application.
     * 
     * @param args command line arguments (not used)
     */
    public static void main(String[] args) {
	launch(args);
    }
}