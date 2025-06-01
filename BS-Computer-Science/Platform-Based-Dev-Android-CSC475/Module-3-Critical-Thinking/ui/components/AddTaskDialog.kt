/*==================================================================================================
    Program Name: To Do List App
    Author: Alexander Ricciardi
    Date: 03/02/2025

    Requirement:
        Kotlin 2.0.0
        Jetpack Compose 2024.04.01
        SQLite
        Minimum SDK: 24
        Target SDK: 35

    Program Description:
       The program is a small Android application that allows the user to manage a to do list
            •	The app uses the Model-View-ViewModel (MVVM) architecture
            •	The app uses Jetpack Compose to generate its UI
            •	The user can add, delete, and complete tasks
            •	The tasks are prioritized by relevance
            •	The tasks can be displayed sorted by priority
            •	The app uses SQLite to store task data
==================================================================================================*/

package com.example.todolistapp.ui.components


import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.DialogProperties
import com.example.todolistapp.model.Priority

/**
 * VIEW
 *
 * This code is part of the View layer in MVVM
 * - It handles UI
 * - Informs the ViewModel about user actions.
 * - Observes ViewModel for data updates.
 * - Contains no business logic.
 *
 */

//-------------------------------------------------------------------------------------------

/**
 * AddTaskDialog is a composable function that displays a dialog for adding a new task
 *
 * - Collects task description input from the user
 * - Allows selection of task priority
 * - Validates user input
 * - Buttons to confirm or cancel the operation
 * 
 * @param whenDismiss when the dialog is dismissed
 * @param whenTaskAdd when a new task is added with description and priority
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddTaskDialog(
    whenDismiss: () -> Unit,
    whenTaskAdd: (String, Priority) -> Unit
) {
    // State variables for the dialog
    var taskDescription by remember { mutableStateOf("") }
    var selectedPriority by remember { mutableStateOf(Priority.MEDIUM) }
    var isDescriptionError by remember { mutableStateOf(false) }
    
    AlertDialog(
        onDismissRequest = whenDismiss,
        properties = DialogProperties(dismissOnClickOutside = true),
        title = { 
            Text(
                "Add New Task",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
        },
        text = {
            Column(
                modifier = Modifier.padding(top = 8.dp)
            ) {
                // Task description input field
                OutlinedTextField(
                    value = taskDescription,
                    onValueChange = { 
                        taskDescription = it
                        isDescriptionError = it.isBlank()
                    },
                    label = { Text("Task Description") },
                    isError = isDescriptionError,
                    supportingText = {
                        if (isDescriptionError) {
                            Text(
                                text = "Description cannot be empty",
                                color = MaterialTheme.colorScheme.error
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                
                Spacer(modifier = Modifier.height(20.dp))
                
                // Priority selection section
                Text(
                    text = "Priority:",
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Medium
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                // Priority selector component
                PrioritySelector(
                    selectedPriority = selectedPriority,
                    whenPrioritySelected = { selectedPriority = it }
                )
            }
        },
        confirmButton = {
            // Add task button with validation
            Button(
                onClick = {
                    if (taskDescription.isNotBlank()) {
                        whenTaskAdd(taskDescription, selectedPriority)
                    } else {
                        isDescriptionError = true
                    }
                },
                shape = RoundedCornerShape(8.dp)
            ) {
                Text("Add Task")
            }
        },
        dismissButton = {
            // Cancel button
            TextButton(onClick = whenDismiss) {
                Text("Cancel")
            }
        }
    )
}

//-------------------------------------------------------------------------------------------

/**
 * PrioritySelector composable function that displays a row of priority options that can be selected
 * 
 * allows users to select a priority levels
 * (LOW, MEDIUM, HIGH, URGENT).
 * 
 * @param selectedPriority selected priority
 * @param whenPrioritySelected when a priority is selected
 */
@Composable
fun PrioritySelector(
    selectedPriority: Priority,
    whenPrioritySelected: (Priority) -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // priority level
        Priority.values().forEach { priority ->
            val isSelected = priority == selectedPriority
            
            //  background colors priority level
            val priorityColor = when (priority) {
                Priority.LOW -> Color(0xFF4CAF50)      // Green
                Priority.MEDIUM -> Color(0xFFE6A700)   // Yellow
                Priority.HIGH -> Color(0xFFD97700)     // Darker orange
                Priority.URGENT -> Color(0xFFF44336)   // Red
            }
            
            // text colors
            val textColor = when (priority) {
                Priority.MEDIUM -> if (isSelected) Color(0xFF5D4200) else Color(0xFF8B6000)
                Priority.HIGH -> if (isSelected) Color(0xFF7A4100) else Color(0xFF9C5200)  // Darker brown
                else -> priorityColor
            }
            
            // Calculate equal weight for each priority
            val weight = 1f / Priority.values().size
            
            // Priority selection chip
            Card(
                modifier = Modifier
                    .weight(weight)
                    .padding(horizontal = 4.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .clickable { whenPrioritySelected(priority) },
                colors = CardDefaults.cardColors(
                    containerColor = if (isSelected) priorityColor.copy(alpha = 0.3f) else MaterialTheme.colorScheme.surface
                ),
                border = BorderStroke(
                    width = if (isSelected) 2.dp else 1.dp,
                    color = if (isSelected) priorityColor else MaterialTheme.colorScheme.outline.copy(alpha = 0.5f)
                )
            ) {
                // Priority text capitalization first letter
                Text(
                    text = priority.name.lowercase().capitalize(),
                    color = textColor,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                    modifier = Modifier
                        .padding(vertical = 8.dp)
                        .align(Alignment.CenterHorizontally)
                )
            }
        }
    }
}

//-------------------------------------------------------------------------------------------

/**
 * Function to capitalize the first letter of a string.
 * priority level text.
 * 
 * @return String to capalized first letter
 */
private fun String.capitalize(): String {
    return this.replaceFirstChar { it.uppercase() }
} 