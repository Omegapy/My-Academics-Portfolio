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

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

/**
 * dark color scheme for the application
 */
private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)

/**
 * light color scheme for the application.
 */
private val LightColorScheme = lightColorScheme(
    primary = Purple40,
    secondary = PurpleGrey40,
    tertiary = Pink40
)

/**
 * the main theme composable
 *
 * @param darkTheme
 * @param dynamicColor to use Monet-style dynamic theming based on the user's wallpaper
 * (available on Android 12 and later)
 * @param content the UI content
 */
@Composable
fun UnitConverterTestingTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    //dynamic color is available on Android 12+ (API level 31+)
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    // color scheme based on dynamic color availability and dark theme preference
    val colorScheme = when {
        // Condition 1: use dynamic color if requested AND available on the device (Android 12+)
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current // Get the current Android context
            // dynamic dark or light scheme based on the darkTheme flag
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        // Condition 2: if dynamic color is not used/available, use the predefined dark scheme if darkTheme is true
        darkTheme -> DarkColorScheme

        // Condition 3: otherwise (light theme without dynamic color), use the predefined light scheme
        else -> LightColorScheme
    }

    // the chosen color scheme and the app's typography (defined in Type.kt)
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}