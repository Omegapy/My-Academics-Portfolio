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
    This file defines the OnlineRecipe data model for recipes fetched from external API sources.
    Part of the Model layer in MVVM architecture, representing data from TheMealDB API.
==================================================================================================*/

package com.example.myrecipeapp.model

import android.os.Parcelable
import kotlinx.parcelize.Parcelize
import com.example.myrecipeapp.data.api.MealDto

/**
 * Data class representing an online recipe from TheMealDB API
 */
@Parcelize
data class OnlineRecipe(
    val id: String,
    val name: String,
    val category: String,
    val area: String,
    val instructions: String,
    val thumbnailUrl: String,
    val tags: String,
    val youtubeUrl: String?,
    val source: String?,
    val imageSource: String?,
    val ingredients: List<Ingredient>,
    val mealDbId: String
) : Parcelable {
    
    /**
     * Returns a list of ingredients from this recipe
     */
    fun getIngredientsList(): List<Ingredient> {
        return ingredients
    }
    
    companion object {
        /**
         * Creates an OnlineRecipe from a MealDto
         */
        fun fromMealDto(mealDto: MealDto): OnlineRecipe {
            // Extract ingredients and measurements
            val ingredients = mutableListOf<Ingredient>()
            
            // Process all 20 possible ingredients
            val ingredientFields = listOf(
                mealDto.ingredient1 to mealDto.measure1,
                mealDto.ingredient2 to mealDto.measure2,
                mealDto.ingredient3 to mealDto.measure3,
                mealDto.ingredient4 to mealDto.measure4,
                mealDto.ingredient5 to mealDto.measure5,
                mealDto.ingredient6 to mealDto.measure6,
                mealDto.ingredient7 to mealDto.measure7,
                mealDto.ingredient8 to mealDto.measure8,
                mealDto.ingredient9 to mealDto.measure9,
                mealDto.ingredient10 to mealDto.measure10,
                mealDto.ingredient11 to mealDto.measure11,
                mealDto.ingredient12 to mealDto.measure12,
                mealDto.ingredient13 to mealDto.measure13,
                mealDto.ingredient14 to mealDto.measure14,
                mealDto.ingredient15 to mealDto.measure15,
                mealDto.ingredient16 to mealDto.measure16,
                mealDto.ingredient17 to mealDto.measure17,
                mealDto.ingredient18 to mealDto.measure18,
                mealDto.ingredient19 to mealDto.measure19,
                mealDto.ingredient20 to mealDto.measure20
            )
            
            // Add valid ingredients to the list
            for ((ingredient, measure) in ingredientFields) {
                if (!ingredient.isNullOrBlank()) {
                    ingredients.add(Ingredient(
                        name = ingredient,
                        measure = measure?.takeIf { it.isNotBlank() }
                    ))
                }
            }
            
            return OnlineRecipe(
                id = mealDto.id,
                name = mealDto.name,
                category = mealDto.category,
                area = mealDto.area,
                instructions = mealDto.instructions,
                thumbnailUrl = mealDto.thumbnailUrl,
                tags = mealDto.tags ?: "",
                youtubeUrl = mealDto.youtubeUrl,
                source = mealDto.source,
                imageSource = mealDto.imageSource,
                ingredients = ingredients,
                mealDbId = mealDto.id
            )
        }
    }
} 
