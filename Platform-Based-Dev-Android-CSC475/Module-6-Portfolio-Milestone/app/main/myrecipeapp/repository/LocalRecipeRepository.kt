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
         The app allows a user to access meal recipes. The recipes can be stored on the user's device and
          fetched from TheMealDB database using API calls. The UI system includes view, search, add, 
          modify, and favorite recipe functionalities.
==================================================================================================*/

/*
MVVM Architecture: REPOSITORY
    This file implements the Repository interface for local database operations
 */

package com.example.myrecipeapp.repository

import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDao
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.withContext

/**
 * Implementation of RecipeRepository that uses the local Room database
 */
class LocalRecipeRepository(private val recipeDao: RecipeDao) : RecipeRepository {
    
    override fun getAllRecipes(): Flow<List<Recipe>> = recipeDao.getAll()
    
    override suspend fun getRecipe(id: Int): Recipe? = withContext(Dispatchers.IO) {
        recipeDao.getById(id)
    }
    
    override fun searchRecipes(query: String): Flow<List<Recipe>> = recipeDao.search(query)
    
    override fun getFavoriteRecipes(): Flow<List<Recipe>> = recipeDao.getFavorites()
    
    override suspend fun addRecipe(recipe: Recipe): Long = withContext(Dispatchers.IO) {
        recipeDao.insert(recipe)
    }
    
    override suspend fun updateRecipe(recipe: Recipe): Int = withContext(Dispatchers.IO) {
        recipeDao.update(recipe)
    }
    
    override suspend fun deleteRecipe(recipe: Recipe): Int = withContext(Dispatchers.IO) {
        recipeDao.delete(recipe)
    }
    
    override suspend fun fetchOnlineRecipes(query: String): List<Recipe> {
        // This will be implemented in the future to fetch recipes from TheMealDB API
        return emptyList()
    }
    
    companion object {
        // Singleton pattern
        @Volatile
        private var INSTANCE: LocalRecipeRepository? = null
        
        fun getInstance(recipeDao: RecipeDao): LocalRecipeRepository {
            return INSTANCE ?: synchronized(this) {
                val instance = LocalRecipeRepository(recipeDao)
                INSTANCE = instance
                instance
            }
        }
    }
} 
