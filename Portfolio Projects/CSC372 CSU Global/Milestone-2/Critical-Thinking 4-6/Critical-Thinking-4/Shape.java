/*
    Program Abstract Class Shape
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
 * An abstract class that represents a geometric shape. This class defines the
 * interface for all shapes such as spheres, cones, and cylinders.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 07/07/2024
 */
public abstract class Shape {

    /**
     * Calculates the surface area of the shape.
     * 
     * @return The surface area as a double value.
     */
    public abstract double surfaceArea();

    /**
     * Calculates the volume of the shape.
     * 
     * @return The volume as a double value.
     */
    public abstract double volume();
}