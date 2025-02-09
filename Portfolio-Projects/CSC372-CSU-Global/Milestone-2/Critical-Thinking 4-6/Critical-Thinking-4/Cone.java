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

/**
 * The class represents cone shape. This class extends the abstract Shape class
 * and computes the surface area and volume of a cone.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/07/2024
 */
public class Cone extends Shape {

    private double radius, height;

    /**
     * Constructs a Cone with the given radius and height.
     * 
     * @param radius The radius of the base of the cone.
     * @param height The height of the cone.
     */
    public Cone(double radius, double height) {
	this.radius = radius;
	this.height = height;
    }

    /**
     * Calculates the surface area of the cone. Note: The surface area of a shape is
     * different than the area of a shape.
     * 
     * @return The surface area of the cone (πr(r + √(r^2 + h^2))).
     */
    @Override
    public double surfaceArea() {
	// The slant height of a cone (√(r^2 + h^2)))
	double slantHeight = Math.sqrt(radius * radius + height * height);
	return Math.PI * radius * (radius + slantHeight);
    }

    /**
     * Calculates the volume of the cone.
     * 
     * @return The volume of the cone ((1/3)πr^2h).
     */
    @Override
    public double volume() {
	return (1.0 / 3.0) * Math.PI * radius * radius * height;
    }

    /**
     * Returns a string representation of the cone's surface area and volume.
     * 
     * @return A formatted string containing the surface area and volume.
     */
    @Override
    public String toString() {
	return String.format("Surface Area: %.2f\nVolume: %.2f", surfaceArea(), volume());
    }
}