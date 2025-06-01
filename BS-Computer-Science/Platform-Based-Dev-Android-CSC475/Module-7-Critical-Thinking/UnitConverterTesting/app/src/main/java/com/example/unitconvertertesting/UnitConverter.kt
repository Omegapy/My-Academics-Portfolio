/*==================================================================================================
    Program Name: Unit Converter Testing App
    Author: Alexander Ricciardi
    Date: 03/30/2025

    Requirement:
         Jetpack Compose (2.7.x)
         Kotlin (2.0.21)
         Jetpack Compose (composeBom = "2024.09.00"): UI
         JUnit (4): Unit Tests
         Hamcrest (1.3): Unit Tests Hamcrest assertions


    Program Description:
         The program is a small Android app that allows a user to convert
            -	Temperatures from Celsius to Fahrenheit, and vice versa.
            -	Length from meters to feet and from kilometers to miles,
                and vice versa.
            -	Weight from kilograms to pounds, and vice versa.
        The app code also provides unit tests using the Android Testing Framework to test
        conversion calculations accuracy.
        The main purpose of this project is to demonstrate the implementation of unit tests
        within Android Studio using JUnit and Hamcrest.
==================================================================================================*/
package com.example.unitconvertertesting

/**
 * Singleton object for performing unit conversions
 * Implements conversion logic for temperature, length, and weight.
 */
object UnitConverter {

    // ------------------ Temperature Conversions -------------------------------------------------

    /**
     * Temperature from Celsius to Fahrenheit
     * Formula: (Celsius * 9/5) + 32
     *
     * @param celsius
     * @return Temperature in Fahrenheit
     */
    fun celsiusToFahrenheit(celsius: Double): Double {
        return celsius * 9 / 5 + 32
    }

    //-----------------------------------------------------------------

    /**
     * Temperature from Fahrenheit to Celsius.
     * Formula: (Fahrenheit - 32) * 5/9
     *
     * @param fahrenheit
     * @return Temperature in Celsius
     */
    fun fahrenheitToCelsius(fahrenheit: Double): Double {
        return (fahrenheit - 32) * 5 / 9
    }

    // ------------------ Length Conversions -----------------------------------------------------

    /**
     * Length from meters to feet.
     * 1 meter is approximately equal to 3.28084 feet
     *
     * @param meters
     * @return Length in feet
     */
    fun metersToFeet(meters: Double): Double {
        return meters * 3.28084
    }

    //-----------------------------------------------------------------

    /**
     * Length from feet to meters
     * 1 foot is approximately equal to 1/3.28084 meters
     *
     * @param feet
     * @return Length in meters
     */
    fun feetToMeters(feet: Double): Double {
        return feet / 3.28084
    }

    //-----------------------------------------------------------------

    /**
     * Distance from kilometers to miles.
     * 1 kilometer is approximately equal to 0.621371 miles
     *
     * @param kilometers
     * @return Distance in miles.
     */
    fun kilometersToMiles(kilometers: Double): Double {
        return kilometers * 0.621371
    }

    //-----------------------------------------------------------------

    /**
     * Distance from miles to kilometers
     * 1 mile is approximately equal to 1/0.621371 kilometers
     *
     * @param miles
     * @return Distance in kilometers
     */
    fun milesToKilometers(miles: Double): Double {
        return miles / 0.621371
    }

    // ------------------ Weight Conversions ---------------------------------------------------

    /**
     * Weight from kilograms to pounds.
     * 1 kilogram is approximately equal to 2.20462 pounds
     *
     * @param kilograms
     * @return Weight in pounds.
     */
    fun kilogramsToPounds(kilograms: Double): Double {
        return kilograms * 2.20462
    }

    //-----------------------------------------------------------------

    /**
     * Weight from pounds to kilograms
     * 1 pound is approximately equal to 1/2.20462 kilograms
     *
     * @param pounds
     * @return Weight in kilograms.
     */
    fun poundsToKilograms(pounds: Double): Double {
        return pounds / 2.20462
    }

    // ------------------ General Conversion Function --------------------------------------------

    /**
     * Determining which specific conversion to apply
     * based on the source and target unit strings  and perform the conversion
     *
     * @param value  value to be converted
     * @param sourceUnit unit of the input value
     * @param targetUnit unit to convert the value into
     * @return converted value
     * @throws IllegalArgumentException if the conversion is not supported
     */
    fun convert(value: Double, sourceUnit: String, targetUnit: String): Double {
        return when {
            // Temperature conversions
            sourceUnit == "Celsius" && targetUnit == "Fahrenheit" -> celsiusToFahrenheit(value)
            sourceUnit == "Fahrenheit" && targetUnit == "Celsius" -> fahrenheitToCelsius(value)

            // Length conversions
            sourceUnit == "Meters" && targetUnit == "Feet" -> metersToFeet(value)
            sourceUnit == "Feet" && targetUnit == "Meters" -> feetToMeters(value)
            sourceUnit == "Kilometers" && targetUnit == "Miles" -> kilometersToMiles(value)
            sourceUnit == "Miles" && targetUnit == "Kilometers" -> milesToKilometers(value)

            // Weight conversions
            sourceUnit == "Kilograms" && targetUnit == "Pounds" -> kilogramsToPounds(value)
            sourceUnit == "Pounds" && targetUnit == "Kilograms" -> poundsToKilograms(value)

            // If both units are the same, simply return the original value.
            sourceUnit == targetUnit -> value

            // For any unsupported conversion pairs, throw an exception.
            else -> throw IllegalArgumentException("Conversion from $sourceUnit to $targetUnit is not supported")
        }
    }
}
