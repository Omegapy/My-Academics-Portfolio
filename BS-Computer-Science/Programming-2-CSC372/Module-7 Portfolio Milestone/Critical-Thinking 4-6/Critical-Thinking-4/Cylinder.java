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
 * The class represents a cylinder shape. This class extends the abstract Shape
 * class and computes surface area and volume of a cylinder.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/07/2024
 */
public class Cylinder extends Shape {

    private double radius, height;

    /**
     * Constructs a Cylinder with the given radius and height.
     * 
     * @param radius The radius of the base of the cylinder.
     * @param height The height of the cylinder.
     */
    public Cylinder(double radius, double height) {
	this.radius = radius;
	this.height = height;
    }

    /**
     * Calculates the surface area of the cylinder. Note: The surface area of a
     * shape is different than the area of a shape.
     * 
     * @return The surface area of the cylinder (2πr(r + h)).
     */
    @Override
    public double surfaceArea() {
	return 2 * Math.PI * radius * (radius + height);
    }

    /**
     * Calculates the volume of the cylinder.
     * 
     * @return The volume of the cylinder (πr^2h).
     */
    @Override
    public double volume() {
	return Math.PI * radius * radius * height;
    }

    /**
     * Returns a string representation of the cylinder's surface area and volume.
     * 
     * @return A formatted string containing the surface area and volume.
     */
    @Override
    public String toString() {
	return String.format("Surface Area: %.2f\nVolume: %.2f", surfaceArea(), volume());
    }
}