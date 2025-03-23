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

    MVVM Architecture: MODEL
    This file contains type converters for Room database.
    Part of the Model layer in MVVM architecture, handling data type conversions for database storage.
==================================================================================================*/

/*
MVVM Architecture: MODEL
    This file contains type converters for Room database
    handles data type conversions for database storage
 */

package com.example.myrecipeapp.model

import androidx.room.TypeConverter
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

/**
 * Type converters for Room database
 * conversion between complex data types and their string representations
 * Used by RecipeDatabase (@TypeConverters(Converters::class))
 */
class Converters {
    private val gson = Gson()
    
    /**
     * Converts a list of Ingredient objects to a JSON string for storage
     */
    @TypeConverter
    fun fromIngredientsList(ingredients: List<Ingredient>?): String {
        if (ingredients == null) return ""
        return gson.toJson(ingredients)
    }
    
    /**
     * Converts a JSON string back to a list of Ingredient objects
     */
    @TypeConverter
    fun toIngredientsList(ingredientsString: String): List<Ingredient> {
        if (ingredientsString.isEmpty()) return emptyList()
        val type = object : TypeToken<List<Ingredient>>() {}.type
        return try {
            gson.fromJson(ingredientsString, type)
        } catch (e: Exception) {
            emptyList() // Return empty list on parsing error
        }
    }
    
    /**
     * Converts a list of strings to a comma-separated string
     */
    @TypeConverter
    fun fromStringList(list: List<String>?): String {
        return list?.joinToString(",") ?: ""
    }
    
    /**
     * Converts a comma-separated string back to a list of strings
     */
    @TypeConverter
    fun toStringList(string: String): List<String> {
        if (string.isEmpty()) return emptyList()
        return string.split(",").map { it.trim() }
    }
    
    /**
     * Converts a Category enum to its name string
     */
    @TypeConverter
    fun fromCategory(category: Category?): String {
        return category?.displayName ?: Category.UNKNOWN.displayName
    }
    
    /**
     * Converts a string back to a Category enum
     */
    @TypeConverter
    fun toCategory(categoryString: String): Category {
        return Category.fromString(categoryString)
    }
} 
