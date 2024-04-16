/*
	Program: Name and Address Information
	Description: Person class stores customers information and displays it
 	Utilized by: Main class
 
*/

/**
 * The Customer class stores persons' information and displays it.
 * 
 * @author Alejandro Ricciardi
 */
public class Person {
	
	// Properties of the Customer class
	private String firstName;
    private String lastName;
    private String streetAddress;
    private String city;
    private String zipCode;

    /**
     * Constructor of the Customer class
     *
     * @param firstName The first name of the person
     * @param lastName The last name of the person
     * @param streetAddress The street address of the person
     * @param city The city where the customer lives
     * @param zipCode The postal zip code of the person's address
     */
    public Person(String firstName, String lastName, String streetAddress, String city, String zipCode) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.streetAddress = streetAddress;
        this.city = city;
        this.zipCode = zipCode;
    }

    /**
     * Displays the person's information to the console.
     */
    public void displayInformation() {
        System.out.println("First Name: " + firstName);
        System.out.println("Last Name: " + lastName);
        System.out.println("Street Address: " + streetAddress);
        System.out.println("City: " + city);
        System.out.println("Zip Code: " + zipCode);
    }
}
