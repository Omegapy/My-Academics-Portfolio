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
    This file defines the Recipe (objects) data model for recipes
 */

package com.example.myrecipeapp.model

import android.os.Parcelable
import androidx.room.Entity
import androidx.room.Ignore
import androidx.room.PrimaryKey
import kotlinx.parcelize.Parcelize

/**
 * Data class representing a recipe/meal.
 * Annotated with Room annotations for database persistence.
 * Implements Parcelable for passing between components.
 * 
 * Structure is based on TheMealDB API response format.
 */
@Parcelize
@Entity(tableName = "meals")
data class Recipe(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    /**
     * The name of the meal/recipe
     */
    val name: String,
    
    /**
     * The category string (mapped to enum in getCategoryEnum())
     */
    val category: String,
    
    /**
     * The region or country the meal originates from (e.g., Italian, Mexican)
     */
    val area: String,
    
    /**
     * Step-by-step instructions for preparing the meal
     */
    val instructions: String,
    
    /**
     * Ingredients and their measurements, stored as a formatted string
     * Format: "ingredient1:measure1,ingredient2:measure2,..."
     */
    val ingredients: String,
    
    /**
     * URL to the meal's thumbnail image
     */
    val thumbnailUrl: String = "",
    
    /**
     * YouTube video URL for the recipe, if available
     */
    val youtubeUrl: String = "",
    
    /**
     * Tags associated with the recipe (e.g., "Soup", "Spicy")
     */
    val tags: String = "",
    
    /**
     * Original source URL of the recipe
     */
    val source: String = "",
    
    /**
     * Flag to mark favorite recipes
     */
    val isFavorite: Boolean = false,
    
    /**
     * ID from TheMealDB API, if the recipe was fetched from there
     */
    val mealDbId: String = ""
) : Parcelable {
    
    /**
     * Returns the Category enum for this recipe
     */
    @Ignore
    fun getCategoryEnum(): Category {
        return Category.fromString(category)
    }
    
    /**
     * Returns a list of Ingredient objects parsed from the ingredients string
     * Includes error handling for malformed strings
     */
    @Ignore
    fun getIngredientsList(): List<Ingredient> {
        if (ingredients.isEmpty()) return emptyList()
        
        return try {
            ingredients.split(",").mapNotNull { pair ->
                try {
                    Ingredient.fromString(pair)
                } catch (e: Exception) {
                    // Log error but don't crash on malformed ingredient
                    println("Error parsing ingredient: $pair, ${e.message}")
                    null
                }
            }
        } catch (e: Exception) {
            // Handle any parsing errors
            println("Error parsing ingredients: ${e.message}")
            emptyList()
        }
    }
    
    /**
     * Returns a formatted string of ingredients for display
     */
    @Ignore
    fun getFormattedIngredients(): String {
        return getIngredientsList().joinToString("\n") { ingredient ->
            "• ${ingredient.getFormattedIngredient()}"
        }
    }
    
    /**
     * Get the list of tags as a string list
     */
    @Ignore
    fun getTagsList(): List<String> {
        if (tags.isEmpty()) return emptyList()
        return tags.split(",").map { it.trim() }
    }
    
    companion object {
        /**
         * Creates a Recipe object from a list of ingredients
         */
        fun fromIngredients(
            id: Int = 0,
            name: String,
            category: String,
            area: String,
            instructions: String,
            ingredientsList: List<Ingredient>,
            thumbnailUrl: String = "",
            youtubeUrl: String = "",
            tags: String = "",
            source: String = "",
            isFavorite: Boolean = false,
            mealDbId: String = ""
        ): Recipe {
            val ingredients = ingredientsList
                .filter { it.name.isNotBlank() && it.measure?.isNotBlank() ?: false }
                .joinToString(",") { "${it.name}:${it.measure}" }
            
            return Recipe(
                id = id,
                name = name,
                category = category,
                area = area,
                instructions = instructions,
                ingredients = ingredients,
                thumbnailUrl = thumbnailUrl,
                youtubeUrl = youtubeUrl,
                tags = tags,
                source = source,
                isFavorite = isFavorite,
                mealDbId = mealDbId
            )
        }
        
        /**
         * Creates a Recipe object from a Category enum and a list of ingredients
         */
        fun fromCategoryAndIngredients(
            id: Int = 0,
            name: String,
            category: Category,
            area: String,
            instructions: String,
            ingredientsList: List<Ingredient>,
            thumbnailUrl: String = "",
            youtubeUrl: String = "",
            tags: String = "",
            source: String = "",
            isFavorite: Boolean = false,
            mealDbId: String = ""
        ): Recipe {
            return fromIngredients(
                id = id,
                name = name,
                category = category.displayName,
                area = area,
                instructions = instructions,
                ingredientsList = ingredientsList,
                thumbnailUrl = thumbnailUrl,
                youtubeUrl = youtubeUrl,
                tags = tags,
                source = source,
                isFavorite = isFavorite,
                mealDbId = mealDbId
            )
        }
    }
} 