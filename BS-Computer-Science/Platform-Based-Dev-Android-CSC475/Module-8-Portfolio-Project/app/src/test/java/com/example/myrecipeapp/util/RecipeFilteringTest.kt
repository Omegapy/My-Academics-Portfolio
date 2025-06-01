package com.example.myrecipeapp.util

import com.example.myrecipeapp.model.Category
import com.example.myrecipeapp.model.Recipe
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test

/**
 * Unit tests for recipe filtering functionality
 * 
 * Tests filtering operations on collections:
 * - Filtering by keyword
 * - Filtering by category
 * - Filtering by favorite status
 * - Filtering by ingredients
 */
class RecipeFilteringTest {

    // Test data
    private lateinit var testRecipes: List<Recipe>
    
    @Before
    fun setup() {
        // Create a test dataset for filtering operations
        testRecipes = listOf(
            Recipe(
                id = 1,
                name = "Chocolate Cake",
                category = Category.DESSERT.displayName,
                area = "American",
                instructions = "Mix and bake at 350F",
                ingredients = "flour:2 cups,sugar:1 cup,cocoa:1/2 cup,eggs:2",
                thumbnailUrl = "http://example.com/cake.jpg",
                tags = "dessert,sweet,chocolate",
                isFavorite = true
            ),
            Recipe(
                id = 2,
                name = "Chicken Pasta",
                category = Category.PASTA.displayName,
                area = "Italian",
                instructions = "Boil pasta, add sauce",
                ingredients = "pasta:8 oz,chicken:2 cups,tomato:1 cup,basil:2 tbsp",
                thumbnailUrl = "http://example.com/pasta.jpg",
                tags = "dinner,pasta,chicken",
                isFavorite = false
            ),
            Recipe(
                id = 3,
                name = "Chocolate Mousse",
                category = Category.DESSERT.displayName,
                area = "French",
                instructions = "Mix and chill for 2 hours",
                ingredients = "chocolate:200g,cream:1 cup,eggs:3",
                thumbnailUrl = "http://example.com/mousse.jpg",
                tags = "dessert,chocolate,french",
                isFavorite = true
            ),
            Recipe(
                id = 4,
                name = "Caesar Salad",
                category = Category.SIDE.displayName,
                area = "Italian",
                instructions = "Toss and serve",
                ingredients = "lettuce:1 head,croutons:1 cup,dressing:1/2 cup,chicken:1 cup", 
                thumbnailUrl = "http://example.com/salad.jpg",
                tags = "healthy,salad,lunch",
                isFavorite = false
            )
        )
    }
    
    /**
     * Filter recipes by keyword in name, instructions, or ingredients
     */
    private fun filterRecipesByKeyword(recipes: List<Recipe>, keyword: String): List<Recipe> {
        if (keyword.isBlank()) return recipes
        
        val lowercaseKeyword = keyword.lowercase()
        return recipes.filter { recipe ->
            recipe.name.lowercase().contains(lowercaseKeyword) ||
            recipe.instructions.lowercase().contains(lowercaseKeyword) ||
            recipe.ingredients.lowercase().contains(lowercaseKeyword)
        }
    }
    
    /**
     * Filter recipes by category
     */
    private fun filterRecipesByCategory(recipes: List<Recipe>, category: Category?): List<Recipe> {
        if (category == null || category == Category.UNKNOWN) return recipes
        
        return recipes.filter { recipe ->
            recipe.category == category.displayName
        }
    }
    
    /**
     * Filter recipes by favorite status
     */
    private fun filterFavoriteRecipes(recipes: List<Recipe>): List<Recipe> {
        return recipes.filter { it.isFavorite }
    }
    
    /**
     * Filter recipes that contain all specified ingredients
     */
    private fun filterRecipesByIngredients(recipes: List<Recipe>, ingredients: List<String>): List<Recipe> {
        if (ingredients.isEmpty()) return recipes
        
        val lowercaseIngredients = ingredients.map { it.lowercase() }
        
        return recipes.filter { recipe ->
            // Simple ingredient matching - just check if the ingredients string contains each keyword
            // In a real implementation, parse the ingredients properly
            val lowerIngredients = recipe.ingredients.lowercase()
            lowercaseIngredients.all { ingredient -> 
                lowerIngredients.contains(ingredient)
            }
        }
    }
    
    @Test
    fun testFilterByKeyword() {
        // Filter by "chocolate" - should match 2 recipes
        val chocolateResults = filterRecipesByKeyword(testRecipes, "chocolate")
        assertEquals("Should find 2 chocolate recipes", 2, chocolateResults.size)
        assertTrue("Should include Chocolate Cake", chocolateResults.any { it.name == "Chocolate Cake" })
        assertTrue("Should include Chocolate Mousse", chocolateResults.any { it.name == "Chocolate Mousse" })
        
        // Filter by "chicken" - should match 2 recipes 
        val chickenResults = filterRecipesByKeyword(testRecipes, "chicken")
        assertEquals("Should find 2 chicken recipes", 2, chickenResults.size)
        
        // Filter by "bake" - should match 1 recipe in instructions
        val bakeResults = filterRecipesByKeyword(testRecipes, "bake")
        assertEquals("Should find 1 recipe with baking", 1, bakeResults.size)
        assertEquals("Should be the cake recipe", "Chocolate Cake", bakeResults[0].name)
        
        // Empty keyword returns all recipes
        val allResults = filterRecipesByKeyword(testRecipes, "")
        assertEquals("Empty keyword should return all recipes", testRecipes.size, allResults.size)
        
        // No match should return empty list
        val noResults = filterRecipesByKeyword(testRecipes, "sushi")
        assertTrue("Non-matching keyword should return empty list", noResults.isEmpty())
    }
    
    @Test
    fun testFilterByCategory() {
        // filter by DESSERT category
        val dessertResults = filterRecipesByCategory(testRecipes, Category.DESSERT)
        assertEquals("Should find 2 dessert recipes", 2, dessertResults.size)
        assertTrue("All results should be desserts", 
            dessertResults.all { it.category == Category.DESSERT.displayName })
        
        // Filter by PASTA category
        val pastaResults = filterRecipesByCategory(testRecipes, Category.PASTA)
        assertEquals("Should find 1 pasta recipe", 1, pastaResults.size)
        assertEquals("Should be the pasta recipe", "Chicken Pasta", pastaResults[0].name)
        
        // Filter by SIDE category
        val sideResults = filterRecipesByCategory(testRecipes, Category.SIDE)
        assertEquals("Should find 1 side dish recipe", 1, sideResults.size)
        assertEquals("Should be the salad recipe", "Caesar Salad", sideResults[0].name)
        
        // Filter by UNKNOWN category - should return all
        val allResults = filterRecipesByCategory(testRecipes, Category.UNKNOWN)
        assertEquals("UNKNOWN category should return all recipes", testRecipes.size, allResults.size)
        
        // Filter by null category - should return all
        val nullResults = filterRecipesByCategory(testRecipes, null)
        assertEquals("Null category should return all recipes", testRecipes.size, nullResults.size)
    }
    
    @Test
    fun testFilterFavorites() {
        // Filter favorites
        val favorites = filterFavoriteRecipes(testRecipes)
        assertEquals("Should find 2 favorite recipes", 2, favorites.size)
        assertTrue("All results should be favorites", favorites.all { it.isFavorite })
        assertTrue("Should include Chocolate Cake", favorites.any { it.name == "Chocolate Cake" })
        assertTrue("Should include Chocolate Mousse", favorites.any { it.name == "Chocolate Mousse" })
        
        // Test with no favorites
        val noFavorites = filterFavoriteRecipes(emptyList())
        assertTrue("Empty list should return empty favorites", noFavorites.isEmpty())
        
        // test with all non-favorites
        val nonFavorites = filterFavoriteRecipes(testRecipes.filter { !it.isFavorite })
        assertTrue("List with no favorites should return empty", nonFavorites.isEmpty())
    }
    
    @Test
    fun testFilterByIngredients() {
        // Simple cases that should match
        val chocolateResults = filterRecipesByIngredients(testRecipes, listOf("chocolate"))
        // Only the mousse has "chocolate" in ingredients string
        assertEquals("Should match recipes with chocolate", 1, chocolateResults.size)
        assertEquals("Should find the chocolate mousse recipe", "Chocolate Mousse", chocolateResults[0].name)
        
        // Filter by "chicken" 
        val chickenResults = filterRecipesByIngredients(testRecipes, listOf("chicken"))
        assertEquals("Should find recipes with chicken", 2, chickenResults.size)
        
        // Empty ingredients list returns all recipes
        val allResults = filterRecipesByIngredients(testRecipes, emptyList())
        assertEquals("Empty ingredients should return all recipes", testRecipes.size, allResults.size)
        
        // No match should return empty list
        val noResults = filterRecipesByIngredients(testRecipes, listOf("beef", "rice"))
        assertTrue("Non-matching ingredients should return empty list", noResults.isEmpty())
    }
    
    @Test
    fun testCombinedFilters() {
        // Combine category + favorite filters
        val dessertFavorites = filterFavoriteRecipes(filterRecipesByCategory(testRecipes, Category.DESSERT))
        assertEquals("Should find 2 favorite desserts", 2, dessertFavorites.size)
        
        // combine keyword + favorite filters (keyword in name)
        val chocolateFavorites = filterFavoriteRecipes(filterRecipesByKeyword(testRecipes, "chocolate"))
        assertEquals("Should find 2 favorite chocolate recipes", 2, chocolateFavorites.size)
        
        // Combine category + ingredient filters
        // look for desserts with cream
        val dessertWithCream = filterRecipesByIngredients(
            filterRecipesByCategory(testRecipes, Category.DESSERT),
            listOf("cream")
        )
        assertEquals("Should find 1 dessert with cream", 1, dessertWithCream.size)
        assertEquals("Should be the mousse recipe", "Chocolate Mousse", dessertWithCream[0].name)
    }
} 