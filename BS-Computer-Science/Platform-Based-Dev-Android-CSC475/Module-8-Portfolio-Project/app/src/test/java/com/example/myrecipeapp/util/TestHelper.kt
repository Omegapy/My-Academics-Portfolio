package com.example.myrecipeapp.util

import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.OnlineRecipe
import com.example.myrecipeapp.model.Ingredient

/**
 * Test helper utility class for common test
 */
object TestHelper {
    
    /**
     * Creates a sample Recipe instance for testing
     * 
     * @param id Optional ID to assign to the recipe
     * @param isFavorite Whether the recipe should be marked as favorite
     * @return Recipe instance
     */
    fun createSampleRecipe(id: Int = 1, isFavorite: Boolean = false): Recipe {
        // Create ingredients string in the format "ingredient1:measure1,ingredient2:measure2"
        val ingredientsStr = "ingredient1:100g,ingredient2:2tbsp"
        
        return Recipe(
            id = id,
            name = "Test Recipe $id",
            category = "Test Category",
            area = "Test Area",
            instructions = "Test instructions for recipe $id.",
            ingredients = ingredientsStr,
            thumbnailUrl = "https://example.com/image$id.jpg",
            isFavorite = isFavorite,
            tags = "test, sample",
            mealDbId = if (id > 0) "meal_$id" else ""
        )
    }
    
    /**
     * Creates a sample OnlineRecipe instance for testing.
     * 
     * @param id Optional ID to assign to the recipe
     * @return A sample OnlineRecipe instance
     */
    fun createSampleOnlineRecipe(id: String = "12345"): OnlineRecipe {
        val ingredients = listOf(
            Ingredient("ingredient1", "100g"),
            Ingredient("ingredient2", "2tbsp")
        )
        
        return OnlineRecipe(
            id = id,
            name = "Online Recipe $id",
            category = "Test Category",
            area = "Test Area",
            instructions = "Test instructions for online recipe $id.",
            thumbnailUrl = "https://example.com/image$id.jpg",
            tags = "test, online, sample",
            youtubeUrl = "https://youtube.com/watch?v=$id",
            source = "Test Source",
            imageSource = "api",
            ingredients = ingredients,
            mealDbId = id
        )
    }
} 