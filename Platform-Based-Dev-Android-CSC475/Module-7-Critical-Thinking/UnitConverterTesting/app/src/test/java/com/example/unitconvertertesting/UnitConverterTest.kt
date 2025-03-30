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

import org.hamcrest.MatcherAssert.assertThat
import org.hamcrest.Matchers.`is`
import org.hamcrest.Matchers.closeTo
// import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * Unit tests for the UnitConverter class
 * uses JUnit to define test cases and Hamcrest matchers
 */
class UnitConverterTest {
    // Delta value for floating-point precision
    private val delta = 0.01

    // ------------------ Temperature Conversion Tests -----------------------------------

    /**
     * Test: 0°C should return 32°F
     */
    @Test
    fun celsiusToFahrenheit_zeroCelsius_returnsThirtyTwoFahrenheit() {
        val result = UnitConverter.celsiusToFahrenheit(0.0)
        // val result = UnitConverter.celsiusToFahrenheit(10.0) // test code
        // JUnit assertion: Checks that the result equals 32.0 within the delta value
        // assertEquals(32.0, result, delta)

        // Hamcrest assertion - matcher: more readable way to verify that result is close to 32.0
        // The closeTo matcher checks that the actual value is within the range of delta
        // of the expected value.
        assertThat(result, `is`(closeTo(32.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 100°C should return 212°F
     */
    @Test
    fun celsiusToFahrenheit_hundredCelsius_returns212Fahrenheit() {
        val result = UnitConverter.celsiusToFahrenheit(100.0)
        // JUnit assertion to verify that 100°C is converted to 212°F
        // assertEquals(212.0, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(212.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 32°F should return 0°C
     */
    @Test
    fun fahrenheitToCelsius_thirtyTwoFahrenheit_returnsZeroCelsius() {
        val result = UnitConverter.fahrenheitToCelsius(32.0)
        // JUnit assertion verifies that the conversion of 32°F returns 0°C
        // assertEquals(0.0, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(0.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 212°F should return 100°C
     */
    @Test
    fun fahrenheitToCelsius_212Fahrenheit_returns100Celsius() {
        val result = UnitConverter.fahrenheitToCelsius(212.0)
        // JUnit assertion verifies that the conversion of 212°F returns 100°C
        // assertEquals(100.0, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(100.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: -40°C should return -40°F (special case where both meet)
     */
    @Test
    fun celsiusToFahrenheit_negativeForty_returnsNegativeForty() {
        val result = UnitConverter.celsiusToFahrenheit(-40.0)
        // Hamcrest assert verifies the case where Celsius and Fahrenheit  meet
        assertThat(result, `is`(closeTo(-40.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: -40°F should return -40°C (special case where both meet)
     */
    @Test
    fun fahrenheitToCelsius_negativeForty_returnsNegativeForty() {
        val result = UnitConverter.fahrenheitToCelsius(-40.0)
        // Hamcrest assert verifies the case where Celsius and Fahrenheit meet
        assertThat(result, `is`(closeTo(-40.0, delta)))
    }

    // ------------------ Length Conversion Tests -------------------------------------------------

    /**
     * Test: 1 meter should return approximately 3.28084 feet
     */
    @Test
    fun metersToFeet_oneMeter_returns3Point28Feet() {
        val result = UnitConverter.metersToFeet(1.0)
        // JUnit assertion verifies that the conversion of 1 meter returns approximately 3.28084
        // assertEquals(3.28084, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(3.28084, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 3.28084 feet should return approximately 1 meter
     */
    @Test
    fun feetToMeters_3Point28Feet_returnsOneMeter() {
        val result = UnitConverter.feetToMeters(3.28084)
        // JUnit assertion verifies that the conversion of 3.28084 feet returns 1 meter
        // assertEquals(1.0, result, delta)

        // Hamcrest asserts
        assertThat(result, `is`(closeTo(1.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 1 kilometer should return approximately 0.621371 miles.
     */
    @Test
    fun kilometersToMiles_oneKilometer_returns0Point62Miles() {
        val result = UnitConverter.kilometersToMiles(1.0)
        // JUnit assertion verifies that 1 kilometer returns approximately 0.621371 miles
        // assertEquals(0.621371, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(0.621371, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test:  1 mile should return approximately 1.609344 kilometers
     */
    @Test
    fun milesToKilometers_oneMile_returns1Point61Kilometers() {
        val result = UnitConverter.milesToKilometers(1.0)
        // JUnit assertion verifies that 1 mile returns approximately 1.609344 kilometers
        // assertEquals(1.609344, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(1.609344, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 0 meters should return 0 feet
     */
    @Test
    fun metersToFeet_zeroMeters_returnsZeroFeet() {
        val result = UnitConverter.metersToFeet(0.0)
        // Hamcrest assert verifies that 0 meters converts to 0 feet
        assertThat(result, `is`(closeTo(0.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 1000 meters should return approximately 3280.84 feet
     */
    @Test
    fun metersToFeet_largeValue_returnsCorrectValue() {
        val result = UnitConverter.metersToFeet(1000.0)
        // Hamcrest asserts verifies the conversion of a large value
        assertThat(result, `is`(closeTo(3280.84, delta)))
    }

    // ------------------ Weight Conversion Tests ------------------------------------------------

    /**
     * Test: 1 kilogram should return approximately 2.20462 pounds
     */
    @Test
    fun kilogramsToPounds_oneKilogram_returns2Point20Pounds() {
        val result = UnitConverter.kilogramsToPounds(1.0)
        // JUnit assertion verifies that 1 kilogram returns approximately 2.20462 pounds
        // assertEquals(2.20462, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(2.20462, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 1 pound should return approximately 0.453592 kilograms
     */
    @Test
    fun poundsToKilograms_onePound_returns0Point45Kilograms() {
        val result = UnitConverter.poundsToKilograms(1.0)
        // JUnit assertion verifies that 1 pound returns approximately 0.453592 kilograms
        // assertEquals(0.453592, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(0.453592, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 0.5 kilograms should return approximately 1.10231 pounds
     */
    @Test
    fun kilogramsToPounds_decimalValue_returnsCorrectValue() {
        val result = UnitConverter.kilogramsToPounds(0.5)
        // Hamcrest assert verifies the conversion of a decimal value
        assertThat(result, `is`(closeTo(1.10231, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: Converting 0.5 pounds should return approximately 0.226796 kilograms.
     */
    @Test
    fun poundsToKilograms_decimalValue_returnsCorrectValue() {
        val result = UnitConverter.poundsToKilograms(0.5)
        // Hamcrest assert verifies the conversion of a decimal value
        assertThat(result, `is`(closeTo(0.226796, delta)))
    }

    // ------------------ General Conversion Function Tests ---------------------------------------

    /**
     * Test: 0.0 degrees Celsius should return 32.0 degrees Fahrenheit
     */
    @Test
    fun convert_celsiusToFahrenheit_returnsCorrectValue() {
        val result = UnitConverter.convert(0.0, "Celsius", "Fahrenheit")

        // JUnit assertion
        // assertEquals(32.0, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(32.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 1.0 meters should return approximately 3.28084 feet
     */
    @Test
    fun convert_metersToFeet_returnsCorrectValue() {
        val result = UnitConverter.convert(1.0, "Meters", "Feet")

        // JUnit assertion
        // assertEquals(3.28084, result, delta)

        // Hamcrest assert for more expressive assertion
        assertThat(result, `is`(closeTo(3.28084, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 1.0 kilograms should return approximately 2.20462 pounds
     */
    @Test
    fun convert_kilogramsToPounds_returnsCorrectValue() {
        val result = UnitConverter.convert(1.0, "Kilograms", "Pounds")

        // JUnit assertion
        // assertEquals(2.20462, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(2.20462, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: 5.0 degrees Celsius should return 41.0 degrees Fahrenheit
     */
    @Test
    fun convert_sameUnits_returnsOriginalValue() {
        val result = UnitConverter.convert(5.0, "Meters", "Meters")

        // JUnit assertion 
        // assertEquals(5.0, result, delta)

        // Hamcrest assert
        assertThat(result, `is`(closeTo(5.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: same temperature units should return the original value
     */
    @Test
    fun convert_sameTemperatureUnits_returnsOriginalValue() {
        val result = UnitConverter.convert(25.0, "Celsius", "Celsius")
        // Hamcrest assert verifies that same unit conversion returns original value
        assertThat(result, `is`(closeTo(25.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: same weight units should return the original value
     */
    @Test
    fun convert_sameWeightUnits_returnsOriginalValue() {
        val result = UnitConverter.convert(5.0, "Kilograms", "Kilograms")
        // Hamcrest assert verifies that same unit conversion returns original value
        assertThat(result, `is`(closeTo(5.0, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: temperature from Celsius to Fahrenheit and back should return original value
     */
    @Test
    fun convert_bidirectionalTemperatureConversion_returnsOriginalValue() {
        val celsius = 25.0
        val fahrenheit = UnitConverter.celsiusToFahrenheit(celsius)
        val backToCelsius = UnitConverter.fahrenheitToCelsius(fahrenheit)
        // Hamcrest assert verifies that same unit conversion returns original value
        assertThat(backToCelsius, `is`(closeTo(celsius, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: length from meters to feet and back should return original value
     */
    @Test
    fun convert_bidirectionalLengthConversion_returnsOriginalValue() {
        val meters = 10.0
        val feet = UnitConverter.metersToFeet(meters)
        val backToMeters = UnitConverter.feetToMeters(feet)
        // Hamcrest assert verifies that same unit conversion returns original value
        assertThat(backToMeters, `is`(closeTo(meters, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: weight from kilograms to pounds and back should return original value.
     */
    @Test
    fun convert_bidirectionalWeightConversion_returnsOriginalValue() {
        val kilograms = 5.0
        val pounds = UnitConverter.kilogramsToPounds(kilograms)
        val backToKilograms = UnitConverter.poundsToKilograms(pounds)
        // Hamcrest assert verifies that same unit conversion returns original value
        assertThat(backToKilograms, `is`(closeTo(kilograms, delta)))
    }

    //-----------------------------------------------------------------

    /**
     * Test: incompatible units should throw IllegalArgumentException.
     */
    @Test(expected = IllegalArgumentException::class)
    fun convert_incompatibleUnits_throwsException() {
        UnitConverter.convert(1.0, "Celsius", "Kilograms")
    }

    //-----------------------------------------------------------------

    /**
     * Test: invalid unit should throw IllegalArgumentException.
     */
    @Test(expected = IllegalArgumentException::class)
    fun convert_invalidUnit_throwsException() {
        UnitConverter.convert(1.0, "InvalidUnit", "Meters")
    }

    //-----------------------------------------------------------------

}
