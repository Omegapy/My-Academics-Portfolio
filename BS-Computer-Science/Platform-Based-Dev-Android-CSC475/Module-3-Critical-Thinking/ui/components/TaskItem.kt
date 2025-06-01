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

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.todolistapp.model.Priority
import com.example.todolistapp.model.Task

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
 * TaskItem composable function that displays a single task in the to do list.
 *
 * - Displays the task description
 * - Displays the task priority
 * - checkbox to mark tasks as completed
 * - delete button to remove tasks
 * - indicating completed tasks with strikethrough text
 * 
 * @param task The task to display
 * @param whenChecked when the task's completion status changes
 * @param whenDelete when the task is deleted
 */
@Composable
fun TaskItem(
    task: Task,
    whenChecked: (Boolean) -> Unit,
    whenDelete: () -> Unit
) {
    // priority background colors
    val priorityColor = when (task.priority) {
        Priority.LOW -> Color(0xFF4CAF50)      // Green
        Priority.MEDIUM -> Color(0xFFE6A700)   // Yellow
        Priority.HIGH -> Color(0xFFD97700)     // Darker
        Priority.URGENT -> Color(0xFFF44336)   // Red
    }
    
    // text colors
    val textColor = when (task.priority) {
        Priority.MEDIUM -> Color(0xFF5D4200)  // Darker brown
        Priority.HIGH -> Color(0xFF7A4100)    // Darker brown
        else -> priorityColor
    }
    
    // Card for the task item with elevation and rounded corners
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Priority indicator - colored circle showing task priority
            Box(
                modifier = Modifier
                    .size(24.dp)
                    .clip(CircleShape)
                    .background(priorityColor)
            )
            
            Spacer(modifier = Modifier.width(12.dp))
            
            // Checkbox for marking task as completed
            Checkbox(
                checked = task.isCompleted,
                onCheckedChange = whenChecked,
                colors = CheckboxDefaults.colors(
                    checkedColor = MaterialTheme.colorScheme.primary,
                    uncheckedColor = MaterialTheme.colorScheme.outline
                )
            )
            
            Spacer(modifier = Modifier.width(8.dp))
            
            // Task description and priority text
            Column(
                modifier = Modifier.weight(1f)
            ) {
                // Task description with strikethrough if completed
                Text(
                    text = task.description,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = if (task.isCompleted) FontWeight.Normal else FontWeight.Medium,
                    textDecoration = if (task.isCompleted) TextDecoration.LineThrough else TextDecoration.None,
                    color = if (task.isCompleted) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurface,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                // Convert priority enum to properly capitalized text
                val priorityText = task.priority.name.lowercase().capitalize()
                
                // Priority text label
                Text(
                    text = priorityText,
                    color = textColor,
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.SemiBold
                )
            }
            
            // Delete button
            IconButton(
                onClick = whenDelete,
                modifier = Modifier.size(40.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Delete,
                    contentDescription = "Delete Task",
                    tint = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}

//-------------------------------------------------------------------------------------------

/**
 * Capitalize the first letter of a string.
 * 
 * @return String first letter capitalized
 */
private fun String.capitalize(): String {
    return this.replaceFirstChar { it.uppercase() }
}