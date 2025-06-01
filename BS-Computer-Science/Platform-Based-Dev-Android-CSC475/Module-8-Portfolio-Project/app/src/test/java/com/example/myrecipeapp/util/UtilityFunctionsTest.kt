package com.example.myrecipeapp.util

import com.example.myrecipeapp.model.Category
import com.example.myrecipeapp.model.Converters
import com.example.myrecipeapp.model.Ingredient
import com.example.myrecipeapp.model.Recipe
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.junit.runners.Parameterized
import org.junit.runners.Parameterized.Parameters
import java.util.Arrays

/**
 * Unit tests for utility functions in the recipe app
 * 
 * Tests various formatting, conversion, and utility functions across:
 * - Ingredient formatting
 * - String conversions
 * - Category conversions
 * - Recipe filtering
 */
class UtilityFunctionsTest {

    // Test helper methods
    private fun createTestRecipe(): Recipe {
        return Recipe(
            id = 1,
            name = "Test Recipe",
            category = "Dessert",
            area = "American",
            instructions = "Test instructions",
            ingredients = "sugar:1 cup,flour:2 cups,eggs:3",
            thumbnailUrl = "http://example.com/img.jpg",
            tags = "sweet,dessert,easy"
        )
    }

    // Sample ingredients for tests
    private val sampleIngredient1 = Ingredient("Flour", "2 cups")
    private val sampleIngredient2 = Ingredient("Sugar", "1 cup")
    private val sampleIngredient3 = Ingredient("Salt", "1 tsp")
    private val sampleIngredientNoMeasure = Ingredient("Vanilla", null)
    private val sampleIngredientEmptyMeasure = Ingredient("Cinnamon", "")

    //region Ingredient Formatting Tests

    @Test
    fun testIngredientFormattedOutput() {
        // Test standard formatting with measure first (default)
        assertEquals("2 cups Flour", sampleIngredient1.getFormattedIngredient())
        
        // Test with name first
        assertEquals("Flour: 2 cups", sampleIngredient1.getFormattedIngredient(measureFirst = false))
        
        // Test with null or empty measure
        assertEquals("Vanilla", sampleIngredientNoMeasure.getFormattedIngredient())
        assertEquals("Cinnamon", sampleIngredientEmptyMeasure.getFormattedIngredient())
    }

    @Test
    fun testIngredientFromString() {
        // Valid strings
        val result1 = Ingredient.fromString("Flour:2 cups")
        assertNotNull("Should parse valid ingredient string", result1)
        assertEquals("Flour", result1?.name)
        assertEquals("2 cups", result1?.measure)
        
        // Null or empty string
        assertNull("Should handle null string", Ingredient.fromString(null))
        assertNull("Should handle empty string", Ingredient.fromString(""))
        
        // malformed string (no colon)
        assertNull("Should handle malformed string", Ingredient.fromString("Flour 2 cups"))
    }

    //end region

    //region Recipe Ingredient List Tests

    @Test
    fun testRecipeGetIngredientsList() {
        val recipe = createTestRecipe()
        val ingredients = recipe.getIngredientsList()
        
        assertEquals("Should parse 3 ingredients", 3, ingredients.size)
        assertEquals("sugar", ingredients[0].name)
        assertEquals("1 cup", ingredients[0].measure)
        assertEquals("flour", ingredients[1].name)
        assertEquals("2 cups", ingredients[1].measure)
    }

    @Test
    fun testRecipeGetFormattedIngredients() {
        val recipe = createTestRecipe()
        val formatted = recipe.getFormattedIngredients()
        
        assertTrue("Should contain first ingredient", formatted.contains("• 1 cup sugar"))
        assertTrue("Should contain second ingredient", formatted.contains("• 2 cups flour"))
        assertTrue("Should contain third ingredient", formatted.contains("• 3 eggs"))
        assertTrue("Should use bullet points", formatted.contains("•"))
        assertTrue("Should separate with newlines", formatted.contains("\n"))
    }

    @Test
    fun testRecipeEmptyIngredients() {
        val emptyRecipe = Recipe(
            id = 1,
            name = "Empty Recipe",
            category = "Other",
            area = "Unknown",
            instructions = "No instructions",
            ingredients = "",
            thumbnailUrl = ""
        )
        
        val ingredients = emptyRecipe.getIngredientsList()
        assertTrue("Should return empty list for empty ingredients", ingredients.isEmpty())
        
        val formatted = emptyRecipe.getFormattedIngredients()
        assertEquals("Should return empty string for empty ingredients", "", formatted)
    }

    //end region

    //region Converter Tests

    @Test
    fun testStringListConverter() {
        val converters = Converters()
        
        // Convert list to string
        val testList = listOf("one", "two", "three")
        val result = converters.fromStringList(testList)
        assertEquals("one,two,three", result)
        
        // Convert string back to list
        val resultList = converters.toStringList(result)
        assertEquals(testList, resultList)
        
        // Edge cases
        assertEquals("", converters.fromStringList(null))
        assertEquals("", converters.fromStringList(emptyList()))
        assertTrue(converters.toStringList("").isEmpty())
    }

    @Test
    fun testCategoryConverter() {
        val converters = Converters()
        
        // Convert Category to string
        val category = Category.DESSERT
        val result = converters.fromCategory(category)
        assertEquals("Dessert", result)
        
        // Convert string back to Category
        val resultCategory = converters.toCategory(result)
        assertEquals(Category.DESSERT, resultCategory)
        
        // Edge case - null category should return UNKNOWN
        assertEquals(Category.UNKNOWN.displayName, converters.fromCategory(null))
        
        // Unknown category string should return UNKNOWN
        assertEquals(Category.UNKNOWN, converters.toCategory("InvalidCategory"))
    }

    //endregion

    // Simple parameterized tests for JUnit 4

    @Test
    fun testIngredientFormatWithMultipleScenarios() {
        // Measure first - default
        assertEquals("2 cups Flour", Ingredient("Flour", "2 cups").getFormattedIngredient(true))
        
        // Name first
        assertEquals("Flour: 2 cups", Ingredient("Flour", "2 cups").getFormattedIngredient(false))
        
        // Null measure
        assertEquals("Salt", Ingredient("Salt", null).getFormattedIngredient(true))
        
        // Empty measure
        assertEquals("Pepper", Ingredient("Pepper", "").getFormattedIngredient(false))
    }
    
    @Test
    fun testValidIngredientStrings() {
        // Test multiple valid ingredient strings
        val testStrings = listOf("flour:2 cups", "sugar:1 tsp", "salt:pinch")
        
        testStrings.forEach { ingredientStr ->
            val result = Ingredient.fromString(ingredientStr)
            assertNotNull("Should parse valid ingredient string: $ingredientStr", result)
            val parts = ingredientStr.split(":")
            assertEquals(parts[0], result?.name)
            assertEquals(parts[1], result?.measure)
        }
    }
    
    @Test
    fun testInvalidIngredientStrings() {
        // test multiple invalid ingredient strings
        val testStrings = listOf<String?>(null, "", " ", "malformed", "no:colon:here")
        
        testStrings.forEach { ingredientStr ->
            val result = Ingredient.fromString(ingredientStr)
            assertNull("Should reject invalid ingredient string: $ingredientStr", result)
        }
    }
} 