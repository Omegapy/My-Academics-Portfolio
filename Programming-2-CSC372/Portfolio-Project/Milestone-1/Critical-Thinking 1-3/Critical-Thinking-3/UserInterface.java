/*
    Program Name: Bank Account GUI
    Author: Alejandro (Alex) Ricciardi
    Date: 06/30/2024
    
    Program Description: 
    The program is a small Java JavaFX application provides a text area for user input and a menu bar with four options:
         - Show Date and Time
         - Saves the content of the text area to a file named "log.txt".
         - Changes the background to a random shade of green.
         - Exit
*/

/*-------------------
 |     Packages     |
 --------------------*/
package application; // Program Folder

/*--------------------------
|    Imported modules      |
---------------------------*/
//--- File manipulation
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
//--- Date and time
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
//--- random
import java.util.Random;

//--- JavaFX
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Label;
import javafx.scene.control.Menu;
import javafx.scene.control.MenuBar;
import javafx.scene.control.MenuItem;
import javafx.scene.control.TextArea;
import javafx.scene.image.Image;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

/**
 * UserInterface class implements the main application window for a JavaFX
 * application. It provides a text area for user input and a menu bar with
 * various options. It also contains the main method
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 06/30/2024
 */
public class UserInterface extends Application {

    private TextArea textArea;
    private BorderPane root;

    Integer priorHue = -1;
    Color priorColor;

    // Create label to be used by the VBox
    Label label = new Label("Write text below:");

    // The following lines, combine with the method changeBackgroundColor(), are to
    // meet the assignment requirement:
    // "It displays the initial random hue each time it's selected for a single
    // execution of the program."
    Random random = new Random();
    // Generates a random initial hue in the green range (100-160, inclusive)
    private Integer initialHue = 100 + random.nextInt(61);
    // Creates an initial color with the initial hue, full saturation, and 80%
    // brightness
    private Color initialColor = Color.hsb(initialHue, 1.0, 0.8);
    // Flag to track if it's the first time changing the background color
    private boolean isInitialHue = true;

    /**
     * The main entry point for all JavaFX applications. It sets up the primary
     * stage with all the UI components.
     *
     * @param primaryStage the primary stage for this application.
     */
    @Override
    public void start(Stage primaryStage) {
	// Creates the main layout container
	root = new BorderPane();

	// Creates a VBox that holds the label and text area
	VBox vbox = new VBox(10); // 10 is the spacing between the different elements
	vbox.setPadding(new Insets(10));

	// Text area
	textArea = new TextArea();
	textArea.setPrefRowCount(10); // Set the (preferred) number of visible text rows to 10

	vbox.getChildren().addAll(label, textArea);

	// Sets the VBox as the center of the BorderPane
	root.setCenter(vbox);

	// Creates and sets the menu bar
	MenuBar menuBar = createDropDownMenu();
	root.setTop(menuBar);

	// Icon
	try {
	    Image icon = new Image("logo.png");
	    primaryStage.getIcons().add(icon);
	} catch (Exception e) {
	    System.out.print("Icon image not found.");
	}

	// Creates the scene and displays it
	Scene scene = new Scene(root, 425, 300);
	primaryStage.setTitle("User Interface");
	primaryStage.setScene(scene);
	primaryStage.show();
    }

    // ==============================================================================================
    /*-------------
     |    Menu    |
     --------------*/

    /**
     * Creates a Menu Bar option drop-down menu that contains the option menu items:
     * - Show Date and Time - Save to file - Change Background Color - Exit
     *
     * @return MenuBar.
     */
    private MenuBar createDropDownMenu() {
	MenuBar menuBar = new MenuBar();
	Menu menu = new Menu("Options");

	// Creates menu items
	MenuItem dateTimeItem = new MenuItem("Show Date and Time");
	dateTimeItem.setOnAction(e -> showDateTime());

	MenuItem saveItem = new MenuItem("Save to File");
	saveItem.setOnAction(e -> saveToFile());

	MenuItem colorItem = new MenuItem("Change Background Color");
	colorItem.setOnAction(e -> changeBackgroundColor());

	MenuItem exitItem = new MenuItem("Exit");
	exitItem.setOnAction(e -> System.exit(0));

	// Adds all items to the menu and the menu to the menu bar
	menu.getItems().addAll(dateTimeItem, saveItem, colorItem, exitItem);
	menuBar.getMenus().add(menu);

	return menuBar;
    }

    // ==============================================================================================
    /*------------------------------
     |   Options Functionalities   |
     ------------------------------*/

    /**
     * Displays the current date and time in the text area.
     */
    private void showDateTime() {
	LocalDateTime now = LocalDateTime.now();
	// Creates a formatter date-time pattern, ex: April 23th, 2023 and it is 6:44PM
	DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMMM d'[suffix]', yyyy 'and it is' h:mma");
	// Formats the date-time and replaces the [suffix] placeholder
	String formattedDateTime = formatter.format(now).replace("[suffix]", getSuffix(now.getDayOfMonth()));
	textArea.setText("Today is " + formattedDateTime);
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the suffix for a given day of the month.
     *
     * @param day the day of the month
     * @return the suffix (st, nd, rd, or th)
     */
    private String getSuffix(int day) {
	if (day >= 11 && day <= 13) {
	    return "th";
	}
	switch (day % 10) {
	case 1:
	    return "st";
	case 2:
	    return "nd";
	case 3:
	    return "rd";
	default:
	    return "th";
	}
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Saves the content of the text area to a file named "log.txt". If the file
     * exists, it appends the content; otherwise, it creates a new file. It also
     * displays a status message of the file operation using an Alert dialog.
     */
    private void saveToFile() {
	String textContent = "-------------------------------------------------\n" + textArea.getText();
	File file = new File("log.txt"); // Creates a file object
	boolean fileExists = file.exists(); // Returns true if file already exists
	// If the file already exist is opened in append mode, otherwise a new file
	// is created and opened in append mode
	try {
	    FileWriter writer = new FileWriter(file, true); // true is to open file in append mode.
	    writer.write(textContent);
	    writer.write(System.lineSeparator()); // Adds a new line after each new file entry
	    writer.close();
	    // Creates an information alert
	    Alert alert = new Alert(Alert.AlertType.INFORMATION);
	    alert.setTitle("File Save Status");
	    alert.setHeaderText(null);
	    if (fileExists) {
		alert.setContentText("Content appended to log.txt");
	    } else {
		alert.setContentText("New file log.txt created and content saved");
	    }
	    alert.showAndWait();
	} catch (IOException e) {
	    // Creates an error alert if an exception occurs
	    Alert alert = new Alert(Alert.AlertType.ERROR);
	    alert.setTitle("File Save Error");
	    alert.setHeaderText(null);
	    alert.setContentText("Error saving to file: " + e.getMessage());
	    alert.showAndWait();
	}
    }

    // ---------------------------------------------------------------------------------------------------------

    /**
     * Changes the background color of the application to a random shade of green.
     * Displays information about the new color in the text area.
     */
    private void changeBackgroundColor() {

	// Change the font color of the label to white bold
	label.setStyle("-fx-font-weight: bold; -fx-text-fill: white;");

	// First use of the changeBackgroundColor() option
	if (isInitialHue) {
	    // Sets the background color of the root pane
	    root.setStyle("-fx-background-color: " + toHexColorCode(initialColor) + ";"); // FX CSS code
	    // Text
	    String initialColorInfo = String.format(
		    "Initial background color details:\n" + "Initial green hue: %d\n" + "Initial color: %s\n"
			    + "This color uses full saturation and 80%% brightness.",
		    initialHue, toHexColorCode(initialColor));

	    textArea.setText(initialColorInfo);

	    isInitialHue = false;
	    return; // exits method
	} else if (priorHue == -1) {
	    // Generates a random hue in the green range (100-160, inclusive)
	    Integer greenHue = 100 + random.nextInt(61);
	    // Creates a new color with the random hue, full saturation, and 80% brightness
	    Color newColor = Color.hsb(greenHue, 1.0, 0.8);
	    // Sets the background color of the root pane
	    root.setStyle("-fx-background-color: " + toHexColorCode(newColor) + ";"); // FX CSS code
	    // Text
	    String colorChangeInfo = String.format(
		    "Background color change details:\n" + "Initial green hue: %d\n" + "Initial color: %s\n"
			    + "New green hue: %d\n" + "New color: %s\n"
			    + "Both colors use full saturation and 80%% brightness.",
		    initialHue, toHexColorCode(initialColor), greenHue, toHexColorCode(newColor));

	    textArea.setText(colorChangeInfo);
	    //
	    priorHue = greenHue;
	    priorColor = newColor;
	    return; // exits method
	}
	// Generates a random hue in the green range (100-160, inclusive)
	Integer greenHue = 100 + random.nextInt(61);
	// Creates a new color with the random hue, full saturation, and 80% brightness
	Color newColor = Color.hsb(greenHue, 1.0, 0.8);
	// Sets the background color of the root pane
	root.setStyle("-fx-background-color: " + toHexColorCode(newColor) + ";"); // FX CSS code
	// Text
	String colorChangeInfo = String.format(
		"Background color change details:\n" + "Initial hue: %d\n" + "Initial color: %s\n"
			+ "Previous hue: %d\n" + "Previous color: %s\n" + "New hue: %d\n" + "New color: %s\n"
			+ "All colors use full saturation and 80%% brightness.",
		initialHue, toHexColorCode(initialColor), priorHue, toHexColorCode(priorColor), greenHue,
		toHexColorCode(newColor));

	textArea.setText(colorChangeInfo);

	priorHue = greenHue;
	priorColor = newColor;
    }

    /**
     * Converts a Color object to its hexadecimal color code.
     *
     * @param color the Color object to convert
     * @return the hexadecimal color code as a String
     */
    private String toHexColorCode(Color color) {
	return String.format("#%02X%02X%02X", (int) (color.getRed() * 255), (int) (color.getGreen() * 255),
		(int) (color.getBlue() * 255));
    }

    // ==============================================================================================
    /*-----------
    |    Main   |
    -------------*/

    /**
     * The main method is the entry point of the Java application. It launches the
     * application.
     *
     * @param args command line arguments
     */
    public static void main(String[] args) {
	launch(args);
    }

    // ---------------------------------------------------------------------------------------------------------
}