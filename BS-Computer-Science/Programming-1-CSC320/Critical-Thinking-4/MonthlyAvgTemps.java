/*
    Program: Get Monthly Temperatures
    MonthlyAvgTemps class
    
    Description:
    Stores the average temperatures for each month and computes
    the yearly average temperature as well as the highest and lowest monthly averages.
  
    Utilized by: Main class
*/

/**
 * The MonthlyAvgTemps class stores the average temperatures for each month and computes
 * the yearly average temperature as well as the highest and lowest monthly averages.
 * Utilized by the Main class.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 05/19/2024
 */
public class MonthlyAvgTemps {
    private String[] months;  // Stores the names of the months
    private int[] temps;  // Stores the average temperatures of the months
    private int highest,  // Stores the highest temperature
                lowest,  // Stores the lowest temperature
                yearlyAvg,  // Stores the yearly average temperature
                highestMonthIndex,  // Stores the index of the month with the highest temperature
                lowestMonthIndex;  // Stores the index of the month with the lowest temperature
    
    /**
     * Constructor  
     * Initializes a MonthlyAvgTemps object with the provided temperatures.
     * Used by the Main class.
     * 
     * @param temps The average temperatures for each month.
     */
    public MonthlyAvgTemps(int[] temps) {
        this.highest = Integer.MIN_VALUE;  // (MIN_VALUE) smallest possible value that an integer can represent
        this.lowest = Integer.MAX_VALUE;   // (MAX_VALUE) largest possible value that an integer can represent
        this.yearlyAvg = Integer.MIN_VALUE; 
        this.highestMonthIndex = 0;  
        this.lowestMonthIndex = 0; 
        this.months = new String[] {"January", "February", "March", "April", "May", "June",
                                    "July", "August", "September", "October", "November", "December"};
        this.temps = temps;
        // Compute the statistics
        // the yearly average temperature as well as the highest and lowest monthly averages.
        computeStatsValuesIndexes(); 
    }
    
    /*----------------
    |     Getters    |
    ------------------*/

    /**
     * Gets the array of month names.
     * 
     * @return An array of month names.
     */
    public String[] getMonths() {
        return months;
    }

    /**
     * Gets the array of average temperatures.
     * 
     * @return An array of average temperatures.
     */
    public int[] getTemps() {
        return temps;
    }

    /**
     * Gets the highest average temperature value.
     * 
     * @return The highest average temperature.
     */
    public double getHighestTemp() {
        return highest;
    }

    /**
     * Gets the lowest average temperature value.
     * 
     * @return The lowest average temperature.
     */
    public double getLowestTemp() {
        return lowest;
    }

    /**
     * Gets the index of the month with the highest average temperature.
     * 
     * @return The index of the month with the highest average temperature.
     */
    public int getHighestMonthIndex() {
        return highestMonthIndex;
    }

    /**
     * Gets the index of the month with the lowest average temperature.
     * 
     * @return The index of the month with the lowest average temperature.
     */
    public int getLowestMonthIndex() {
        return lowestMonthIndex;
    }

    /**
     * Gets the yearly average temperature.
     * 
     * @return The yearly average temperature.
     */
    public int getYearlyAvg() { 
        return yearlyAvg;
    }
    
    /*-------------------------------
    |     Private Class Methods     |
    ---------------------------------*/

    /**
     * Computes monthly average statistics,
     * including the highest and lowest monthly average temperatures, yearly average temperature,
     * and the indices of the months with the highest and lowest average temperatures.
     */
    private void computeStatsValuesIndexes() {
        int total = 0;  // Stores the sum of all temperatures
        for (int i = 0; i < temps.length; i++) {
            if (temps[i] > highest) {
                highest = temps[i];
                highestMonthIndex = i;
            }
            if (temps[i] < lowest) {
                lowest = temps[i];
                lowestMonthIndex = i;
            }
            total += temps[i];
        }
        yearlyAvg = (Integer)Math.round(total / temps.length); // Calculate the yearly average temperature
    }
}


