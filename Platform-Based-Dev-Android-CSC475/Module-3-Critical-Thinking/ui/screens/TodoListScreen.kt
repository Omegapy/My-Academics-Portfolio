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

package com.example.todolistapp.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Done
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.todolistapp.model.Priority
import com.example.todolistapp.model.Task
import com.example.todolistapp.ui.components.AddTaskDialog
import com.example.todolistapp.ui.components.TaskItem

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
 * TodoListScreen Composable function render the main screen of the application
 * It displays the list of tasks
 *
 * - Displays the list of tasks
 * - UI
 *   For adding new tasks
 *   Task operations (checking, deleting)
 *   Sorting functionality
 *
 * @param tasks The list of tasks
 * @param whenTaskCheckedChange when a task's completion status changes
 * @param whenTaskDelete when a task is deleted
 * @param whenTaskAdd when a new task is added
 */
@OptIn(ExperimentalMaterial3Api::class) // lastest version of material design
@Composable
fun TodoListScreen(
    tasks: List<Task>,
    whenTaskCheckedChange: (Task, Boolean) -> Unit,
    whenTaskDelete: (Long) -> Unit,
    whenTaskAdd: (Task) -> Unit
) {
    // add task dialog
    var showAddTaskDialog by remember { mutableStateOf(false) }
    
    // the dropdown menu
    var showMenu by remember { mutableStateOf(false) }
    
    // tracks if tasks should be sorted by priority
    var sortedTasks by remember { mutableStateOf(tasks) }
    var isSortedByPriority by remember { mutableStateOf(false) }

    //------------  Embedded Function ------------------
    
    /**
     * Updates the sorted tasks list
     * tasks are sorted by priority (URGENT > HIGH > MEDIUM > LOW)
     * if sorting is disabled, the original task order is used from database
     */
    fun updateSortedTasks() {
        sortedTasks = if (isSortedByPriority) {
            // Sort by priority: URGENT > HIGH > MEDIUM > LOW
            tasks.sortedWith(
                compareByDescending<Task> { 
                    when (it.priority) {
                        Priority.URGENT -> 3
                        Priority.HIGH -> 2
                        Priority.MEDIUM -> 1
                        Priority.LOW -> 0
                    }
                }
            )
        } else {
            // Use original order
            tasks
        }
    }

    //------------ Sort ------------------
    
    // Update sorted tasks when the original tasks list changes
    if (!isSortedByPriority) {
        sortedTasks = tasks
    } else {
        updateSortedTasks()
    }

    //------------ Scaffold  ------------------
    
    // Main scaffold layout with top app bar and floating action button
    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { 
                    Text(
                        "My To Do List",
                        fontWeight = FontWeight.Bold
                    )
                },
                //------------ Dropdown Menu three dots ------------------
                actions = {
                    Box {
                        // Menu button (three dots)
                        IconButton(onClick = { showMenu = true }) {
                            Icon(
                                imageVector = Icons.Default.MoreVert,
                                contentDescription = "Menu Options"
                            )
                        }
                        
                        // Dropdown menu with task management options
                        DropdownMenu(
                            expanded = showMenu,
                            onDismissRequest = { showMenu = false }
                        ) {
                            // Sort by priority option
                            DropdownMenuItem(
                                text = { 
                                    Text(
                                        if (isSortedByPriority) "Reset sort order" else "Sort by priority"
                                    ) 
                                },
                                leadingIcon = { 
                                    Icon(
                                        imageVector = Icons.AutoMirrored.Filled.List,
                                        contentDescription = "Sort"
                                    )
                                },
                                onClick = { 
                                    // Toggle sort by priority
                                    isSortedByPriority = !isSortedByPriority
                                    updateSortedTasks()
                                    showMenu = false
                                }
                            )

                            // Clear completed tasks option
                            DropdownMenuItem(
                                text = { Text("Clear completed") },
                                leadingIcon = { 
                                    Icon(
                                        imageVector = Icons.Default.Done,
                                        contentDescription = "Clear completed"
                                    )
                                },
                                onClick = { 
                                    // Remove all completed tasks
                                    tasks.filter { it.isCompleted }.forEach { whenTaskDelete(it.id) }
                                    showMenu = false
                                }
                            )
                            
                            // Delete all tasks option
                            DropdownMenuItem(
                                text = { Text("Delete all") },
                                leadingIcon = { 
                                    Icon(
                                        imageVector = Icons.Default.Delete,
                                        contentDescription = "Delete all"
                                    )
                                },
                                onClick = { 
                                    // Remove all tasks
                                    tasks.forEach { whenTaskDelete(it.id) }
                                    showMenu = false
                                }
                            )
                        }
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        //------------ Add tacks button [+] ------------------
        floatingActionButton = {
            // Add task button
            FloatingActionButton(
                onClick = { showAddTaskDialog = true },
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                Icon(
                    imageVector = Icons.Default.Add,
                    contentDescription = "Add Task",
                    tint = Color.White
                )
            }
        }
    ) { innerPadding ->
        // Main content area
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            color = MaterialTheme.colorScheme.background
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 16.dp)
            ) {
                // Display empty when no tasks are available
                if (sortedTasks.isEmpty()) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .align(Alignment.Center),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "No tasks yet!",
                            style = MaterialTheme.typography.titleLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = FontWeight.Medium
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "Add a task using the + button",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            textAlign = TextAlign.Center
                        )
                    }
                } else {
                    // Display the list of tasks using LazyColumn
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(vertical = 8.dp)
                    ) {
                        items(sortedTasks) { task ->
                            TaskItem(
                                task = task,
                                whenChecked = { isChecked ->
                                    whenTaskCheckedChange(task, isChecked)
                                },
                                whenDelete = {
                                    whenTaskDelete(task.id)
                                }
                            )
                        }
                    }
                }
            }
            //------------ add task dialog ------------------
            // Show add task dialog when the add button is clicked
            if (showAddTaskDialog) {
                AddTaskDialog(
                    whenDismiss = { showAddTaskDialog = false },
                    whenTaskAdd = { description, priority ->
                        val newTask = Task(
                            description = description,
                            priority = priority
                        )
                        whenTaskAdd(newTask)
                        showAddTaskDialog = false
                    }
                )
            }
        }
    }
} 