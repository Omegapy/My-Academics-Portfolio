/*==================================================================================================
    Program Name: To Do List App
    Author: Alexander Ricciardi
    Date: 03/02/2025

    Requirement:
        Kotlin
        Jetpack Compose
        SQLite
        Minimum SDK: 24
        Target SDK: 35

    Program Description:
        The app is a small program that allows the user to manage a to do list
        The app uses the Model-View-ViewModel (MVVM) architecture
        The app uses Jetpack Compose to generate its UI
        The user can add, delete, and complete tasks
        The tasks are prioritize by relevance
        The tasks can be display sorted by priority
        The app use SQLite to store task data
==================================================================================================*/

package com.example.todolistapp.data.database

import android.content.ContentValues
import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import com.example.todolistapp.model.Priority
import com.example.todolistapp.model.Task

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
 * The TaskDatabase class manages the task data (CRUD) at the SQL database level
 * by implementing the SQLiteOpenHelper class functionality (methods).
 *
 * - Creates and upgrading the database schema
 * - Provides methods for CRUD operations on tasks
 * - Translates between database records and Task objects
 * 
 * @param context to access the database
 */
class TaskDatabase(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        // Database metadata
        private const val DATABASE_NAME = "tasks.db"
        private const val DATABASE_VERSION = 1

        // Table name
        private const val TABLE_TASKS = "tasks"

        // Column names
        private const val KEY_ID = "id"
        private const val KEY_DESCRIPTION = "description"
        private const val KEY_PRIORITY = "priority"
        private const val KEY_IS_COMPLETED = "is_completed"
    }

    //--------------------- Methods ---------

    /**
     * Called the first time the app is launch to create the database
     * tasks table with columns
     * 
     * @param db The database instance
     */
    override fun onCreate(db: SQLiteDatabase) {
        // Create the tasks table with columns for id, description, priority, and completion status
        val createTableQuery = """
            CREATE TABLE $TABLE_TASKS (
                $KEY_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                $KEY_DESCRIPTION TEXT NOT NULL,
                $KEY_PRIORITY TEXT NOT NULL,
                $KEY_IS_COMPLETED INTEGER NOT NULL DEFAULT 0
            )
        """.trimIndent()

        db.execSQL(createTableQuery)
    }

    //---------------------------------------------

    /**
     * Updates tables
     * 'Drops' the existing table and creates a new one
     * 
     * @param db The database instance
     * @param oldVersion The old database version
     * @param newVersion The new database version
     */
    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // Drop old table if it exists and create a new one
        db.execSQL("DROP TABLE IF EXISTS $TABLE_TASKS")
        onCreate(db)
    }

    //---------------------------------------------

    /**
     * Inserts a new task
     * 
     * @param task The task to insert
     * @return The ID of the newly inserted task, or -1 if the insertion failed
     */
    fun insertTask(task: Task): Long {
        val db = writableDatabase

        // values for insertion
        val values = ContentValues().apply {
            put(KEY_DESCRIPTION, task.description)
            put(KEY_PRIORITY, task.priority.name)
            put(KEY_IS_COMPLETED, if (task.isCompleted) 1 else 0)
        }

        // Insert and get the new row ID
        val id = db.insert(TABLE_TASKS, null, values)
        db.close()

        return id
    }

    //---------------------------------------------

    /**
     * RGets all the tasks from the database
     * 
     * @return A list of all tasks
     */
    fun getAllTasks(): List<Task> {
        val taskList = mutableListOf<Task>()
        val selectQuery = "SELECT * FROM $TABLE_TASKS"

        val db = readableDatabase
        val cursor = db.rawQuery(selectQuery, null)

        // Process the cursor and convert each row to a Task object
        cursor?.use {
            if (it.moveToFirst()) {
                do {
                    val task = cursorToTask(it)
                    taskList.add(task)
                } while (it.moveToNext())
            }
        }

        return taskList
    }

    //---------------------------------------------

    /**
     * Gets a specific task by ID
     * 
     * @param id The ID of the task
     * @return The task with the specified ID, or null if not found
     */
    fun getTask(id: Long): Task? {
        val db = readableDatabase

        // Query for a task with the specified ID
        val cursor = db.query(
            TABLE_TASKS,
            null,
            "$KEY_ID = ?",
            arrayOf(id.toString()),
            null,
            null,
            null
        )

        var task: Task? = null

        // Convert the cursor to a Task object if a row is found
        cursor?.use {
            if (it.moveToFirst()) {
                task = cursorToTask(it)
            }
        }

        return task
    }

    //---------------------------------------------

    /**
     * Updates an existing task
     * 
     * @param task The updated task
     * @return The number of rows affected
     */
    fun updateTask(task: Task): Int {
        val db = writableDatabase

        // Prepare values for update
        val values = ContentValues().apply {
            put(KEY_DESCRIPTION, task.description)
            put(KEY_PRIORITY, task.priority.name)
            put(KEY_IS_COMPLETED, if (task.isCompleted) 1 else 0)
        }

        //---------------------------------------------

        // Update the row and get the number of rows affected
        val rowsAffected = db.update(
            TABLE_TASKS,
            values,
            "$KEY_ID = ?",
            arrayOf(task.id.toString())
        )

        db.close()
        return rowsAffected
    }

    //---------------------------------------------

    /**
     * Deletes a task
     * 
     * @param taskId The ID
     * @return The number of rows affected
     */
    fun deleteTask(taskId: Long): Int {
        val db = writableDatabase

        // Delete the row and get the number of rows affected
        val rowsAffected = db.delete(
            TABLE_TASKS,
            "$KEY_ID = ?",
            arrayOf(taskId.toString())
        )

        db.close()
        return rowsAffected
    }

    //---------------------------------------------

    /**
     * Deletes all completed tasks
     * 
     * @return The number of rows affected
     */
    fun deleteCompletedTasks(): Int {
        val db = writableDatabase

        // Delete all tasks where is_completed = 1
        val rowsAffected = db.delete(
            TABLE_TASKS,
            "$KEY_IS_COMPLETED = ?",
            arrayOf("1")
        )

        db.close()
        return rowsAffected
    }

    //---------------------------------------------

    /**
     * Gets tasks filtered by completion state
     * 
     * @param isCompleted gets completed or active tasks
     * @return A list of tasks with the completion state
     */
    fun getTasksByCompletionStatus(isCompleted: Boolean): List<Task> {
        val taskList = mutableListOf<Task>()
        val db = readableDatabase

        // Query for tasks with the specified completion states
        val cursor = db.query(
            TABLE_TASKS,
            null,
            "$KEY_IS_COMPLETED = ?",
            arrayOf(if (isCompleted) "1" else "0"),
            null,
            null,
            null
        )

        // Process the cursor and convert each row to a Task object
        cursor?.use {
            if (it.moveToFirst()) {
                do {
                    val task = cursorToTask(it)
                    taskList.add(task)
                } while (it.moveToNext())
            }
        }

        return taskList
    }

    //---------------------------------------------

    /**
     * Gets tasks by priority
     * 
     * @param priority The priority
     * @return A list of tasks with the priority
     */
    fun getTasksByPriority(priority: Priority): List<Task> {
        val taskList = mutableListOf<Task>()
        val db = readableDatabase

        // Query for tasks with the priority
        val cursor = db.query(
            TABLE_TASKS,
            null,
            "$KEY_PRIORITY = ?",
            arrayOf(priority.name),
            null,
            null,
            null
        )

        //---------------------------------------------

        // Process the cursor and convert each row to a Task object
        cursor?.use {
            if (it.moveToFirst()) {
                do {
                    val task = cursorToTask(it)
                    taskList.add(task)
                } while (it.moveToNext())
            }
        }

        return taskList
    }

    //---------------------------------------------

    /**
     * Helper method to convert a database cursor to a Task object.
     * 
     * @param cursor The cursor positioned at the row to convert
     * @return A Task object with data from the cursor
     */
    private fun cursorToTask(cursor: Cursor): Task {
        // Get column indices safely to avoid crashes if schema changes
        val idIndex = cursor.getColumnIndex(KEY_ID)
        val descriptionIndex = cursor.getColumnIndex(KEY_DESCRIPTION)
        val priorityIndex = cursor.getColumnIndex(KEY_PRIORITY)
        val isCompletedIndex = cursor.getColumnIndex(KEY_IS_COMPLETED)

        // Create and return a Task object with data from the cursor
        return Task(
            id = if (idIndex >= 0) cursor.getLong(idIndex) else 0,
            description = if (descriptionIndex >= 0) cursor.getString(descriptionIndex) else "",
            priority = if (priorityIndex >= 0) Priority.valueOf(cursor.getString(priorityIndex)) else Priority.MEDIUM,
            isCompleted = if (isCompletedIndex >= 0) cursor.getInt(isCompletedIndex) == 1 else false
        )
    }

    //---------------------------------------------
}