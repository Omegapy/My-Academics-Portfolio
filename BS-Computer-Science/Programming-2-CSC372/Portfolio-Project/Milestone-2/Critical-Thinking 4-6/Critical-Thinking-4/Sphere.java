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
 * The class represents a sphere shape. This class extends the abstract Shape
 * class and computes the surface area and volume of a sphere.
 * 
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/07/2024
 */
public class Sphere extends Shape {

    private double radius;

    /**
     * Constructs a Sphere with the given radius.
     * 
     * @param radius The radius of the sphere.
     */
    public Sphere(double radius) {
	this.radius = radius;
    }

    /**
     * Calculates the surface area of the sphere. Note: The surface area of a shape
     * is different than the area of a shape.
     * 
     * @return The surface area of the sphere (4πr^2).
     */
    @Override
    public double surfaceArea() {
	return 4 * Math.PI * radius * radius;
    }

    /**
     * Calculates the volume of the sphere.
     * 
     * @return The volume of the sphere ((4/3)πr^3).
     */
    @Override
    public double volume() {
	return (4.0 / 3.0) * Math.PI * Math.pow(radius, 3);
    }

    /**
     * Returns a string representation of the sphere's surface area and volume.
     * 
     * @return A formatted string containing the surface area and volume.
     */
    @Override
    public String toString() {
	return String.format("Surface Area: %.2f\nVolume: %.2f", surfaceArea(), volume());
    }
}