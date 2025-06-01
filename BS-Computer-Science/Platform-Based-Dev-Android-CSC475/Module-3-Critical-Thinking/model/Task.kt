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

package com.example.todolistapp.model

/**
 * MODEL
 * 
 * This code is part of the Model layer in MVVM
 * - It defines the core data structures of the application
 * - Holds application data
 * - Does not directly talk to the View
 * - Exposes data to the ViewModel via Observables
 *
 */

//-------------------------------------------------------------------------------------------

/**
 * Priority enum, the different priority levels for tasks
 * - URGENT
 * - HIGH
 * - MEDIUM
 * - LOW
 *
 */
enum class Priority {
    HIGH,
    MEDIUM,
    LOW,
    URGENT
}

//-------------------------------------------------------------------------------------------

/**
 * Task class is a data class representing a single task object:
 *
 * - unique identifier
 * - task description
 * - priority level
 * - completion status
 * 
 * @property id Unique identifier
 * @property description  description
 * @property priority Priority level
 * @property isCompleted Boolean indicating if the task is completed or not
 */
data class Task(
    val id: Long = 0,
    val description: String,
    val priority: Priority,
    val isCompleted: Boolean = false
)