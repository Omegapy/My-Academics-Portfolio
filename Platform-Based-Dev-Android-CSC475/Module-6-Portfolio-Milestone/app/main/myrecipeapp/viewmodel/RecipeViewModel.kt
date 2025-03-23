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
MVVM Architecture: VIEWMODEL
    This file contains the RecipeViewModel which manages UI-related data and business logical
 */

package com.example.myrecipeapp.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDatabase
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel that manages recipe data and operations
 * access to recipes stored in the local database and handles CRUD operations
 */
class RecipeViewModel(application: Application) : AndroidViewModel(application) {
    
    private val database = RecipeDatabase.getInstance(application.applicationContext)
    private val recipeDao = database.recipeDao()
    
    // Public Flow of all recipes
    val recipes: Flow<List<Recipe>> = recipeDao.getAll()
    
    // Public Flow of favorite recipes
    val favoriteRecipes: Flow<List<Recipe>> = recipeDao.getFavorites()
    
    // Private MutableStateFlow for current recipe being edited
    private val _currentRecipe = MutableStateFlow<Recipe?>(null)
    val currentRecipe: StateFlow<Recipe?> = _currentRecipe

    /**
     * Toggles the favorite status of a recipe.
     *
     * @param recipe The recipe to update
     */
    fun toggleFavorite(recipe: Recipe) {
        viewModelScope.launch {
            val updatedRecipe = recipe.copy(isFavorite = !recipe.isFavorite)
            recipeDao.update(updatedRecipe)
            
            // Update the current recipe if it's the same one being toggled
            if (_currentRecipe.value?.id == recipe.id) {
                _currentRecipe.value = updatedRecipe
            }
        }
    }

    //--------------------------------------------------------------------
    
    /**
     * Retrieves a recipe by its ID and updates the currentRecipe state.
     *
     * @param id The ID of the recipe to retrieve
     */
    fun getRecipeById(id: Int) {
        viewModelScope.launch {
            _currentRecipe.value = recipeDao.getById(id)
        }
    }

    //--------------------------------------------------------------------
    
    /**
     * Adds a new recipe to the database.
     *
     * @param recipe The recipe to add
     */
    fun addRecipe(recipe: Recipe) {
        viewModelScope.launch {
            recipeDao.insert(recipe)
        }
    }

    //--------------------------------------------------------------------
    
    /**
     * Updates an existing recipe in the database.
     *
     * @param recipe The recipe with updated information
     */
    fun updateRecipe(recipe: Recipe) {
        viewModelScope.launch {
            recipeDao.update(recipe)
        }
    }
    
    /**
     * Deletes a recipe from the database.
     *
     * @param recipe The recipe to delete
     */
    fun deleteRecipe(recipe: Recipe) {
        viewModelScope.launch {
            recipeDao.delete(recipe)
        }
    }

    //--------------------------------------------------------------------

} 
