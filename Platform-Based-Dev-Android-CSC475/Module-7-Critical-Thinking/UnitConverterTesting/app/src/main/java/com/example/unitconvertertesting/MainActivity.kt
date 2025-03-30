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

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.example.unitconvertertesting.ui.theme.UnitConverterTestingTheme
import java.text.DecimalFormat

/**
 * The main activity for the add,
 * sets up Jetpack Compose UI
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        // set the activity
        setContent {
            UnitConverterTestingTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    UnitConverterApp(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

//-------------------------------------------------------------------------------------------------

/**
 * The main composable function
 * It displays input fields, dropdowns for unit selection, a convert button,
 * and the result text
 * it also manages the user input and selections
 */
@OptIn(ExperimentalMaterial3Api::class) // for ExposedDropdownMenuBox
@Composable
fun UnitConverterApp(modifier: Modifier = Modifier) {
    // background color
    Surface(
        modifier = modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // --- User and Conversion Variables ---
            var inputValue by remember { mutableStateOf("") }
            var resultValue by remember { mutableStateOf("") }

            var fromUnitExpanded by remember { mutableStateOf(false) }
            var toUnitExpanded by remember { mutableStateOf(false) }

            var selectedFromUnit by remember { mutableStateOf("Celsius") } // Default value
            var selectedToUnit by remember { mutableStateOf("Fahrenheit") } // Default value

            // List of unit categories.
            val unitCategories = listOf("Temperature", "Length", "Weight")
            var selectedCategory by remember { mutableStateOf(unitCategories[0]) }
            var categoryExpanded by remember { mutableStateOf(false) }

            // --- Unit by Conversion ---
            val temperatureUnits = listOf("Celsius", "Fahrenheit")
            val lengthUnits = listOf("Meters", "Feet", "Kilometers", "Miles")
            val weightUnits = listOf("Kilograms", "Pounds")

            // 'From' and 'To'
            // dropdowns based on the currently selected category.
            val currentUnits = when (selectedCategory) {
                "Temperature" -> temperatureUnits
                "Length" -> lengthUnits
                "Weight" -> weightUnits
                else -> temperatureUnits // Default
            }

            // --- UI Elements ---

            Text(
                text = "Unit Converter",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.padding(bottom = 24.dp)
            )

            // --- Category Selection Dropdown ---
            ExposedDropdownMenuBox(
                expanded = categoryExpanded,
                onExpandedChange = { categoryExpanded = it },
                modifier = Modifier.fillMaxWidth()
            ) {
                // TextField acts as the display area for the selected category and the menu
                TextField(
                    value = selectedCategory,
                    onValueChange = {}, // Input
                    readOnly = true,
                    // dropdown arrow icon, changes based on 'expanded' state
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = categoryExpanded) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .menuAnchor(), // This anchors the DropdownMenu
                    label = { Text("Category") } // Label for the dropdown
                )

                // The dropdown menu, appears when 'expanded' is true
                DropdownMenu(
                    expanded = categoryExpanded,
                    onDismissRequest = { categoryExpanded = false }, // Close menu
                    modifier = Modifier.exposedDropdownSize() // size to match the anchor
                ) {
                    // menu item for each category.
                    unitCategories.forEach { category ->
                        DropdownMenuItem(
                            text = { Text(category) },
                            onClick = {
                                // Update the selected category
                                selectedCategory = category
                                // Reset 'From' and 'To' units based on the new category
                                selectedFromUnit = when (category) {
                                    "Temperature" -> temperatureUnits[0]
                                    "Length" -> lengthUnits[0]
                                    "Weight" -> weightUnits[0]
                                    else -> temperatureUnits[0]
                                }
                                selectedToUnit = when (category) {
                                    "Temperature" -> temperatureUnits[1]
                                    "Length" -> lengthUnits[1]
                                    "Weight" -> weightUnits[1]
                                    else -> temperatureUnits[1]
                                }
                                // close the category dropdown
                                categoryExpanded = false
                                // clear previous result
                                resultValue = ""
                            }
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // --- Input Value Field ---
            OutlinedTextField(
                value = inputValue,
                onValueChange = { inputValue = it },
                label = { Text("Value") }, // Label
                // keyboard type for numerical input (allows decimals)
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))

            // --- Unit Selection ('From' and 'To') ---
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                // --- 'From' Dropdown ---
                ExposedDropdownMenuBox(
                    expanded = fromUnitExpanded,
                    onExpandedChange = { fromUnitExpanded = it },
                    modifier = Modifier.weight(1f)
                ) {
                    TextField(
                        value = selectedFromUnit,
                        onValueChange = {},
                        readOnly = true,
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = fromUnitExpanded) },
                        modifier = Modifier.menuAnchor(), // Anchor for the 'From menu
                        label = { Text("From") }
                    )

                    DropdownMenu(
                        expanded = fromUnitExpanded,
                        onDismissRequest = { fromUnitExpanded = false },
                        modifier = Modifier.exposedDropdownSize()
                    ) {
                        // units relevant to the selected category
                        currentUnits.forEach { unit ->
                            DropdownMenuItem(
                                text = { Text(unit) },
                                onClick = {
                                    selectedFromUnit = unit // update selected 'From'
                                    fromUnitExpanded = false // close the dropdown
                                    resultValue = "" // clear previous result
                                }
                            )
                        }
                    }
                }


                Spacer(modifier = Modifier.padding(8.dp))

                // --- 'To' Unit Dropdown ---
                ExposedDropdownMenuBox(
                    expanded = toUnitExpanded,
                    onExpandedChange = { toUnitExpanded = it },
                    modifier = Modifier.weight(1f)
                ) {
                    TextField(
                        value = selectedToUnit,
                        onValueChange = {},
                        readOnly = true,
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = toUnitExpanded) },
                        modifier = Modifier.menuAnchor(),
                        label = { Text("To") }
                    )

                    DropdownMenu(
                        expanded = toUnitExpanded,
                        onDismissRequest = { toUnitExpanded = false },
                        modifier = Modifier.exposedDropdownSize()
                    ) {
                        // units relevant to the selected category
                        currentUnits.forEach { unit ->
                            DropdownMenuItem(
                                text = { Text(unit) },
                                onClick = {
                                    selectedToUnit = unit // update selected 'To' unit
                                    toUnitExpanded = false // close the dropdown
                                    resultValue = "" // clear previous result
                                }
                            )
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // --- Convert Button ---
            Button(
                onClick = {
                    // conversion logic
                    try {
                        // parse the input string to a Double
                        val inputValueDouble = inputValue.toDouble()
                        // conversion function from the UnitConverter object
                        val result = UnitConverter.convert(
                            inputValueDouble,
                            selectedFromUnit,
                            selectedToUnit
                        )
                        // numerical result to a maximum of 4 decimal places
                        val df = DecimalFormat("#.####")
                        resultValue = df.format(result)
                    } catch (e: NumberFormatException) {
                        // if input value is not a valid number
                        resultValue = "Invalid input"
                    } catch (e: IllegalArgumentException) {
                        // if selected units are incompatible or invalid
                        // (thrown by UnitConverter.convert).
                        resultValue = e.message ?: "Conversion not supported"
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Convert")
            }

            Spacer(modifier = Modifier.height(24.dp))

            // --- Result Display ---
            // display the result Text only if resultValue is not empty
            if (resultValue.isNotEmpty()) {
                // display the result or error message
                Text(
                    // only if it is a valid result, not for error messages
                    text = if (resultValue == "Invalid input" || resultValue.startsWith("Conversion")) {
                        resultValue // Show error message directly
                    } else {
                        "Result: $resultValue ${selectedToUnit}" // formatted result with unit
                    } ,
                    style = MaterialTheme.typography.titleLarge
                )
            }
        }
    }
}