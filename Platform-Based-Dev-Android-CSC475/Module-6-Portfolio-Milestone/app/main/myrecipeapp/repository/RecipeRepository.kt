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

    MVVM Architecture: REPOSITORY
    This file defines the Repository interface that serves as a mediator between data sources and ViewModels.
    Part of the Repository layer in the MVVM architecture, providing a clean API for data operations.
==================================================================================================*/

package com.example.myrecipeapp.repository

import com.example.myrecipeapp.model.Recipe
import kotlinx.coroutines.flow.Flow

/**
 * Repository interface defining operations for managing recipe data.
 * This abstraction allows for easy swapping of data sources (local database, remote API, etc.)
 */
interface RecipeRepository {
    /**
     * Gets all recipes from the data source.
     */
    fun getAllRecipes(): Flow<List<Recipe>>
    
    /**
     * Gets a specific recipe by ID.
     */
    suspend fun getRecipe(id: Int): Recipe?
    
    /**
     * Searches for recipes matching the given query string.
     * The search will look for matches in name, ingredients, and category.
     */
    fun searchRecipes(query: String): Flow<List<Recipe>>
    
    /**
     * Gets all recipes marked as favorites.
     */
    fun getFavoriteRecipes(): Flow<List<Recipe>>
    
    /**
     * Adds a new recipe to the data source.
     * @return ID of the newly added recipe
     */
    suspend fun addRecipe(recipe: Recipe): Long
    
    /**
     * Updates an existing recipe in the data source.
     * @return Number of recipes updated (should be 1 if successful)
     */
    suspend fun updateRecipe(recipe: Recipe): Int
    
    /**
     * Deletes a recipe from the data source.
     * @return Number of recipes deleted (should be 1 if successful)
     */
    suspend fun deleteRecipe(recipe: Recipe): Int
    
    /**
     * Fetches recipes from an online source (future implementation for TheMealDB API).
     * @return List of recipes from the online source
     */
    suspend fun fetchOnlineRecipes(query: String): List<Recipe> = emptyList()
} 
