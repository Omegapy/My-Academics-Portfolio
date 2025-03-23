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
    This file contains data transfer objects (DTOs) for TheMealDB API
*/

package com.example.myrecipeapp.data.api

import com.example.myrecipeapp.model.Ingredient
import com.example.myrecipeapp.model.OnlineRecipe
import com.example.myrecipeapp.model.Recipe
import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

/**
 * Data class for Json TheMealDB API
 */
@JsonClass(generateAdapter = true)
data class MealResponse(
    @Json(name = "meals") val meals: List<MealDto>?
)

//----------------------------------------------------------------------------------------------

/**
 * Data class that matches TheMealDB meal structure
 */
@JsonClass(generateAdapter = true)
data class MealDto(
    @Json(name = "idMeal") val id: String = "",
    @Json(name = "strMeal") val name: String = "",
    @Json(name = "strDrinkAlternate") val drinkAlternate: String? = null,
    @Json(name = "strCategory") val category: String = "",
    @Json(name = "strArea") val area: String = "",
    @Json(name = "strInstructions") val instructions: String = "",
    @Json(name = "strMealThumb") val thumbnailUrl: String = "",
    @Json(name = "strTags") val tags: String? = null,
    @Json(name = "strYoutube") val youtubeUrl: String? = null,
    @Json(name = "strSource") val source: String? = null,
    @Json(name = "strImageSource") val imageSource: String? = null,
    @Json(name = "strCreativeCommonsConfirmed") val creativeCommonsConfirmed: String? = null,
    @Json(name = "dateModified") val dateModified: String? = null,
    
    // Ingredients
    @Json(name = "strIngredient1") val ingredient1: String? = null,
    @Json(name = "strIngredient2") val ingredient2: String? = null,
    @Json(name = "strIngredient3") val ingredient3: String? = null,
    @Json(name = "strIngredient4") val ingredient4: String? = null,
    @Json(name = "strIngredient5") val ingredient5: String? = null,
    @Json(name = "strIngredient6") val ingredient6: String? = null,
    @Json(name = "strIngredient7") val ingredient7: String? = null,
    @Json(name = "strIngredient8") val ingredient8: String? = null,
    @Json(name = "strIngredient9") val ingredient9: String? = null,
    @Json(name = "strIngredient10") val ingredient10: String? = null,
    @Json(name = "strIngredient11") val ingredient11: String? = null,
    @Json(name = "strIngredient12") val ingredient12: String? = null,
    @Json(name = "strIngredient13") val ingredient13: String? = null,
    @Json(name = "strIngredient14") val ingredient14: String? = null,
    @Json(name = "strIngredient15") val ingredient15: String? = null,
    @Json(name = "strIngredient16") val ingredient16: String? = null,
    @Json(name = "strIngredient17") val ingredient17: String? = null,
    @Json(name = "strIngredient18") val ingredient18: String? = null,
    @Json(name = "strIngredient19") val ingredient19: String? = null,
    @Json(name = "strIngredient20") val ingredient20: String? = null,
    
    // Measurements
    @Json(name = "strMeasure1") val measure1: String? = null,
    @Json(name = "strMeasure2") val measure2: String? = null,
    @Json(name = "strMeasure3") val measure3: String? = null,
    @Json(name = "strMeasure4") val measure4: String? = null,
    @Json(name = "strMeasure5") val measure5: String? = null,
    @Json(name = "strMeasure6") val measure6: String? = null,
    @Json(name = "strMeasure7") val measure7: String? = null,
    @Json(name = "strMeasure8") val measure8: String? = null,
    @Json(name = "strMeasure9") val measure9: String? = null,
    @Json(name = "strMeasure10") val measure10: String? = null,
    @Json(name = "strMeasure11") val measure11: String? = null,
    @Json(name = "strMeasure12") val measure12: String? = null,
    @Json(name = "strMeasure13") val measure13: String? = null,
    @Json(name = "strMeasure14") val measure14: String? = null,
    @Json(name = "strMeasure15") val measure15: String? = null,
    @Json(name = "strMeasure16") val measure16: String? = null,
    @Json(name = "strMeasure17") val measure17: String? = null,
    @Json(name = "strMeasure18") val measure18: String? = null,
    @Json(name = "strMeasure19") val measure19: String? = null,
    @Json(name = "strMeasure20") val measure20: String? = null
) {
    /**
     * Converts this DTO to a Recipe object
     */
    fun toRecipe(): Recipe {
        // string in the format "ingredient1:measure1,ingredient2:measure2,..."
        val ingredients = buildString {
            val pairs = listOf(
                ingredient1 to measure1, ingredient2 to measure2, ingredient3 to measure3,
                ingredient4 to measure4, ingredient5 to measure5, ingredient6 to measure6,
                ingredient7 to measure7, ingredient8 to measure8, ingredient9 to measure9,
                ingredient10 to measure10, ingredient11 to measure11, ingredient12 to measure12,
                ingredient13 to measure13, ingredient14 to measure14, ingredient15 to measure15,
                ingredient16 to measure16, ingredient17 to measure17, ingredient18 to measure18,
                ingredient19 to measure19, ingredient20 to measure20
            ).filter { (ingredient, _) -> 
                !ingredient.isNullOrBlank() 
            }
            
            pairs.forEachIndexed { index, (ingredient, measure) ->
                if (index > 0) append(",")
                append("${ingredient}:${measure ?: ""}")
            }
        }
        
        return Recipe(
            id = 0, // Will be assigned by Room
            name = name,
            category = category,
            area = area,
            instructions = instructions,
            ingredients = ingredients,
            thumbnailUrl = thumbnailUrl,
            youtubeUrl = youtubeUrl ?: "",
            tags = tags ?: "",
            source = source ?: "",
            isFavorite = false,
            mealDbId = id
        )
    }
    
    /**
     * Converts this DTO to an OnlineRecipe object
     */
    fun toOnlineRecipe(): OnlineRecipe {
        // Extract ingredients and measurements
        val ingredients = mutableListOf<Ingredient>()
        
        // Process all 20 possible ingredients
        val ingredientFields = listOf(
            ingredient1 to measure1,
            ingredient2 to measure2,
            ingredient3 to measure3,
            ingredient4 to measure4,
            ingredient5 to measure5,
            ingredient6 to measure6,
            ingredient7 to measure7,
            ingredient8 to measure8,
            ingredient9 to measure9,
            ingredient10 to measure10,
            ingredient11 to measure11,
            ingredient12 to measure12,
            ingredient13 to measure13,
            ingredient14 to measure14,
            ingredient15 to measure15,
            ingredient16 to measure16,
            ingredient17 to measure17,
            ingredient18 to measure18,
            ingredient19 to measure19,
            ingredient20 to measure20
        )
        
        // Add ingredients to the list
        for ((ingredient, measure) in ingredientFields) {
            if (!ingredient.isNullOrBlank()) {
                ingredients.add(Ingredient(
                    name = ingredient,
                    measure = measure?.takeIf { it.isNotBlank() }
                ))
            }
        }
        
        return OnlineRecipe(
            id = id,
            name = name,
            category = category,
            area = area,
            instructions = instructions,
            thumbnailUrl = thumbnailUrl,
            tags = tags ?: "",
            youtubeUrl = youtubeUrl,
            source = source,
            imageSource = imageSource,
            ingredients = ingredients,
            mealDbId = id
        )
    }
}

//----------------------------------------------------------------------------------------------

/**
 * Data class for categories (list of categories) response
 */
@JsonClass(generateAdapter = true)
data class CategoriesResponse(
    @Json(name = "categories") val categories: List<CategoryDto>?
)

//----------------------------------------------------------------------------------------------

/**
 * Data class for a category (single)
 */
@JsonClass(generateAdapter = true)
data class CategoryDto(
    @Json(name = "idCategory") val id: String,
    @Json(name = "strCategory") val name: String,
    @Json(name = "strCategoryThumb") val thumbnailUrl: String,
    @Json(name = "strCategoryDescription") val description: String
) 
