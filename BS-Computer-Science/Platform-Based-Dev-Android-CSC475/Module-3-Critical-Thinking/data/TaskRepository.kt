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
import com.example.todolistapp.data.database.TaskDatabase
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
 * Repository class provides data access to the ViewModel (API)
 * This class abstracts the  SQLite database from the rest of the app.
 */
class TaskRepository(private val context: Context) {
    private val database = TaskDatabase(context)


    //------------------------------------------------------------------

    //-----------------------------
    //       Getters
    //-----------------------------

    /**
     * Gets all tasks from the database.
     * @return List of all tasks
     */
    fun getTasks(): List<Task> {
        return database.getAllTasks()
    }


    //------------------------------------------------------------------

    /**
     * Gets a specific task by its ID.
     * @param id ID of the task to retrieve
     * @return task with the specified ID, or null if not found
     */
    fun getTaskById(id: Long): Task? {
        return database.getTask(id)
    }

    //------------------------------------------------------------------

    /**
     * Gets tasks filtered by priority.
     * @param priority priority to filter
     * @return List of tasks
     */
    fun getTasksByPriority(priority: Priority): List<Task> {
        return database.getTasksByPriority(priority)
    }

    //------------------------------------------------------------------

    /**
     * Gets all completed tasks.
     * @return List of completed tasks
     */
    fun getCompletedTasks(): List<Task> {
        return database.getTasksByCompletionStatus(true)
    }

    //------------------------------------------------------------------

    /**
     * Gets all active (not completed) tasks.
     * @return List of active tasks
     */
    fun getActiveTasks(): List<Task> {
        return database.getTasksByCompletionStatus(false)
    }

    //------------------------------------------------------------------

    //-----------------------------
    //       Modifiers
    //-----------------------------

    /**
     * Adds a new task to the database
     * @param task task to add
     * @return ID of the newly inserted task, or -1 if the insertion failed
     */
    fun addTask(task: Task): Long {
        return database.insertTask(task)
    }

    //------------------------------------------------------------------

    /**
     * Deletes a task from the database.
     * @param taskId ID of the task to delete
     * @return number of rows affected
     */
    fun deleteTask(taskId: Long): Int {
        return database.deleteTask(taskId)
    }

    //------------------------------------------------------------------

    /**
     * Deletes all completed tasks.
     * @return number of tasks deleted
     */
    fun deleteCompletedTasks(): Int {
        return database.deleteCompletedTasks()
    }

    //------------------------------------------------------------------

    /**
     * Updates the completion status of a task.
     * @param taskId ID of the task to update
     * @param isCompleted new completion status
     * @return number of rows affected
     */
    fun updateTaskCompletionStatus(taskId: Long, isCompleted: Boolean): Int {
        val task = database.getTask(taskId) ?: return 0
        val updatedTask = task.copy(isCompleted = isCompleted)
        return database.updateTask(updatedTask)
    }

    //------------------------------------------------------------------
    // To be implemented in future versions

    /**
     * Updates an existing task in the database.
     * @param task task with updated values
     * @return number of rows affected
     */
    fun updateTask(task: Task): Int {
        return database.updateTask(task)
    }

    //------------------------------------------------------------------
    // To be implemented in future versions

    /**
     * Updates the priority of a task.
     * @param taskId ID of the task to update
     * @param priority new priority
     * @return number of rows affected
     */
    fun updateTaskPriority(taskId: Long, priority: Priority): Int {
        val task = database.getTask(taskId) ?: return 0
        val updatedTask = task.copy(priority = priority)
        return database.updateTask(updatedTask)
    }

    //------------------------------------------------------------------
}