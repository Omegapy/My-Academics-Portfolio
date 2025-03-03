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

package com.example.todolistapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.example.todolistapp.data.DatabaseInitializer
import com.example.todolistapp.data.TaskRepository
import com.example.todolistapp.model.Task
import com.example.todolistapp.ui.screens.TodoListScreen
import com.example.todolistapp.ui.theme.ToDoListAppTheme

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
 * MainActivity class is main class, the entry point of the application
 * 
 * This activity:
 * - Initializes the database with (fake)) data if the database is empty
 * - Sets up the TaskRepository for data operations
 * - Configures the UI with Jetpack Compose
 */
class MainActivity : ComponentActivity() {

    // Handles task data operations
    private lateinit var repository: TaskRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Initializes database with (fake) data if the database is empty
        val initializer = DatabaseInitializer(this)
        initializer.initializeWithSampleData()

        // Get repository instance for task operations
        repository = TaskRepository(this)

        // Set up the UI with edge-to-edge display and Compose
        enableEdgeToEdge()
        setContent {
            ToDoListAppTheme {
                TodoApp(repository)
            }
        }
    }
}

//-------------------------------------------------------------------------------------------

/**
 * TodoApp Class is the main composable function, it sets up the application UI.
 *
 * - Manages the state of tasks using the repository
 * - Sets up the Scaffold for the UI
 * - Configures the TodoListScreen
 * 
 * @param repository The TaskRepository instance for data operations
 */
@Composable
fun TodoApp(repository: TaskRepository) {
    // State to hold the current list of tasks
    var tasks by remember { mutableStateOf(repository.getTasks()) }
    
    // Function to refresh tasks list from the repository
    val refreshTasks = {
        tasks = repository.getTasks()
    }

    // Main scaffold layout
    Scaffold { innerPadding ->
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            // TodoListScreen for task operations
            TodoListScreen(
                tasks = tasks,
                whenTaskCheckedChange = { task: Task, isCompleted: Boolean ->
                    // Update task completion status and refresh the list
                    repository.updateTaskCompletionStatus(task.id, isCompleted)
                    refreshTasks()
                },
                whenTaskDelete = { taskId: Long ->
                    // Delete task and refresh the list
                    repository.deleteTask(taskId)
                    refreshTasks()
                },
                whenTaskAdd = { task: Task ->
                    // Add new task and refresh the list
                    repository.addTask(task)
                    refreshTasks()
                }
            )
        }
    }
}