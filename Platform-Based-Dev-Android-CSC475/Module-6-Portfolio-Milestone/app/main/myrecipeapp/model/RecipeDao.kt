/*==================================================================================================
    Program Name: My Photo Gallery App
    Author: Alexander Ricciardi
    Date: 03/17/2025

    Requirement:
         Jetpack Compose (2.7.x)
         Kotlin (2.0.21)
         AndroidX Core KTX (1.15.0): Kotlin extensions for core Android functionality
         Navigation Compose (2.7.7): Navigation between screens 
         Material 3: Material Design 3 components and theming system
         Room (2.6.1): Local database for storing recipes with SQLite abstraction
         Lifecycle Components (2.8.7): ViewModel and LiveData for MVVM architecture
         Retrofit (2.9.0): Type-safe HTTP client for API 
         Moshi (1.15.0): JSON parser for API 
         OkHttp (4.12.0): HTTP client and logging 
         Coil (2.5.0): Image loading library 
         Compose Runtime LiveData (1.6.2)
          Gson (2.10.1): JSON serialization/deserialization library
         Activity Compose (1.10.1): Compose integration with Activity
         Compose BOM: Bill of materials for consistent Compose dependencies

    Program Description:
         The app allows a user to access meal recipes. The recipes can be stored on the user\'s device and 
          fetched from TheMealDB database using API calls. The UI system includes view, search, add, 
          modify, and favorite recipe functionalities.
==================================================================================================*/

/*
MVVM Architecture: MODEL
    This file defines the RecipeDao data model for recipes
 */

package com.example.myrecipeapp.model

// Import Room annotations
import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

/**
 * Data Access Object (DAO) for Recipe objects
 * methods to interact with the recipes in the database
 */
@Dao
interface RecipeDao {

    /**
     * Retrieves all recipes from the database.
     *
     * @return Flow of all recipes for reactive updates
     */
    @Query("SELECT * FROM meals")
    fun getAll(): Flow<List<Recipe>>

    //------------------------------------------------------

    /**
     * Retrieves a specific recipe by its ID.
     *
     * @param id The unique identifier of the recipe
     * @return The recipe with the specified ID, or null if not found
     */
    @Query("SELECT * FROM meals WHERE id = :id")
    suspend fun getById(id: Int): Recipe?

    //------------------------------------------------------

    /**
     * Retrieves all recipes marked as favorites.
     *
     * @return Flow of favorite recipes for reactive updates
     */
    @Query("SELECT * FROM meals WHERE isFavorite = 1")
    fun getFavorites(): Flow<List<Recipe>>

    //------------------------------------------------------

    /**
     * Searches for recipes matching the query string in name, ingredients, or category.
     *
     * @param query The search term to match
     * @return Flow of recipes matching the query for reactive updates
     */
    @Query("SELECT * FROM meals WHERE name LIKE '%' || :query || '%' OR ingredients LIKE '%' || :query || '%' OR category LIKE '%' || :query || '%'")
    fun search(query: String): Flow<List<Recipe>>

    //------------------------------------------------------

    /**
     * Inserts a new recipe into the database.
     * If a recipe with the same ID already exists, it will be replaced.
     *
     * @param recipe The recipe to insert
     * @return The new row ID for the inserted recipe
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(recipe: Recipe): Long

    //------------------------------------------------------

    /**
     * Updates an existing recipe in the database.
     *
     * @param recipe The recipe with updated information
     * @return The number of recipes updated (should be 1 if successful)
     */
    @Update
    suspend fun update(recipe: Recipe): Int

    //------------------------------------------------------

    /**
     * Deletes a recipe from the database.
     *
     * @param recipe The recipe to delete
     * @return The number of recipes deleted (should be 1 if successful)
     */
    @Delete
    suspend fun delete(recipe: Recipe): Int

    //------------------------------------------------------
} 

