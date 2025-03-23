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
MVVM Architecture: APPLICATION
    This file contains the Application class which initializes app-wide components and dependencies
 */

package com.example.myrecipeapp

import android.app.Application
import androidx.appcompat.app.AppCompatDelegate
import com.example.myrecipeapp.model.RecipeDatabase
import com.example.myrecipeapp.repository.LocalRecipeRepository
import com.example.myrecipeapp.repository.RecipeRepository

/**
 * Application class for the My Recipe App
 * initializes the database and repository
 */
class RecipeApplication : Application() {
    
    // The repository that will be used throughout the app
    lateinit var repository: RecipeRepository
        private set
    
    override fun onCreate() {
        super.onCreate()
        
        // Set app to follow system dark mode setting
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM)
        
        // Initialize the database
        val database = RecipeDatabase.getInstance(this)
        
        // Initialize the repository with the DAO from the database
        repository = LocalRecipeRepository.getInstance(database.recipeDao())
    }
} 
