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

package com.example.unitconvertertesting.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

// Set of Material typography styles to start with
val Typography = Typography(
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)