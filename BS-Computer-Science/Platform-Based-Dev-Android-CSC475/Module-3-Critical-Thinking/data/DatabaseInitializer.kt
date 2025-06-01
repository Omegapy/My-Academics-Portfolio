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

package com.example.todolistapp.data

import android.content.Context
import com.example.todolistapp.model.Priority
import com.example.todolistapp.model.Task

/**
 * VIEWMODEL
 * 
 * This code is part of the ViewModel layer in  MVVM
 * - The ViewModel layer prepares and manages data for the View
 * - Mediates between View and Model.
 * - Transforms data from the Model.
 * - Provides data streams to the View.
 *
 */

//-------------------------------------------------------------------------------------------

/**
 * Utility/testing class that initializes the database
 * by adding (fake) tasks if the database is empty.
 * This use for first-time app launches or for testing
 */
class DatabaseInitializer(private val context: Context) {

    private val repository = TaskRepository(context)

    /**
     * Initializes the database with a predefined set of tasks if the database is empty.
     * @return The number of tasks added
     */
    fun initializeWithSampleData(): Int {
        // Check if the database already has tasks
        if (repository.getTasks().isNotEmpty()) {
            return 0 // Database already has data, don't initialize
        }

        // Sample tasks
        val sampleTasks = listOf(
            Task(description = "Complete Android tutorial", priority = Priority.HIGH),
            Task(description = "Buy groceries", priority = Priority.MEDIUM),
            Task(description = "Exercise for 30 minutes", priority = Priority.MEDIUM),
            Task(description = "Call mom", priority = Priority.LOW),
            Task(description = "Finish project presentation", priority = Priority.URGENT),
            Task(description = "Schedule dentist appointment", priority = Priority.LOW),
            Task(description = "Read a chapter of the book", priority = Priority.LOW),
            Task(description = "Backup computer files", priority = Priority.MEDIUM),
            Task(description = "Fix leaking faucet", priority = Priority.MEDIUM),
            Task(description = "Prepare for job interview", priority = Priority.HIGH)
        )

        // Add all sample tasks to the database
        var tasksAdded = 0
        sampleTasks.forEach { task ->
            val id = repository.addTask(task)
            if (id != -1L) {
                tasksAdded++
            }
        }

        return tasksAdded
    }

}
