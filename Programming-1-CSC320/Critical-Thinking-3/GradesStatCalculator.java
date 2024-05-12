/*
	Program: Capture Grade Statistics Using For-loop
	GradesStatCalculator class
	Description: provides methods to compute grades statistics
 	Utilized by: Main class
 
*/

/**
 * The GradesStatCalculator class provides methods to compute grade statistics
 * such as maximum, minimum, and average from an array of doubles.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 05/12/2024
 */
public class GradesStatCalculator {
	
	/**
     * Finds the maximum value in an array of doubles.
     * 
     * @param array Array of double values.
     * @return The maximum value found in the array.
     */
    public static double findMaximum(Double[] array) {
        double max = Double.MIN_VALUE;  // (MIN_VALUE) smallest possible value that a double can represent
        for (double value : array) {
            if (value > max) {
                max = value;
            }
        }
        return max;
    }

    /**
     * Finds the minimum value in an array of doubles.
     * 
     * @param array Array of double values.
     * @return The minimum value found in the array.
     */
    public static double findMinimum(Double[] array) {
        double min = Double.MAX_VALUE;  // (MAX_VALUE) largest possible value that a double can represent
        for (double value : array) {
            if (value < min) {
                min = value;
            }
        }
        return min;
    }

    /**
     * Calculates the average value of an array of doubles.
     * 
     * @param array Array of double values.
     * @return The average value calculated from the array.
     */
    public static double findAverage(Double[] array) {
        double sum = 0;
        for (double value : array) {
            sum += value;
        }
        return sum / array.length;
    }
}
