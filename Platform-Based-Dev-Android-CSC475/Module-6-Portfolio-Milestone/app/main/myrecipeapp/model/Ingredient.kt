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
MVVM Architecture: MODEL
    This file defines the Ingredient data model used in recipes
    core data entity
*/

package com.example.myrecipeapp.model

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

/**
 * Data class for recipe ingredient with measurement
 */
@Parcelize
data class Ingredient(
    /**
     * The name of the ingredient (e.g., "Flour", "Chicken")
     */
    val name: String,
    
    /**
     * The amount/measurement of the ingredient (e.g., "2 cups", "500g")
     */
    val measure: String?,
    
    /**
     * Optional URL to the ingredient's image (from TheMealDB)
     */
    val imageUrl: String? = null
) : Parcelable {
    
    /**
     * Returns a formatted string representation of this ingredient
     * @param measureFirst If true, returns "measure name", otherwise "name: measure"
     */
    fun getFormattedIngredient(measureFirst: Boolean = true): String {
        return when {
            measure.isNullOrBlank() -> name
            measureFirst -> "$measure $name"
            else -> "$name: $measure"
        }
    }
    //--------------------------------------------------------------------
    companion object {
        /**
         * Ingredient from a string in the format "name:measure"
         */
        fun fromString(ingredientString: String?): Ingredient? {
            if (ingredientString.isNullOrBlank()) return null
            
            val parts = ingredientString.split(":")
            return if (parts.size == 2) {
                Ingredient(
                    name = parts[0].trim(),
                    measure = parts[1].trim()
                )
            } else null
        }
    }
} 
