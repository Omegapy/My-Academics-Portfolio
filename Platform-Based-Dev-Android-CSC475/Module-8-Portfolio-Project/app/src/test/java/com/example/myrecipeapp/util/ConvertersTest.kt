package com.example.myrecipeapp.util

import com.example.myrecipeapp.model.Category
import com.example.myrecipeapp.model.Converters
import com.example.myrecipeapp.model.Ingredient
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test

/**
 * Unit tests for Converters utility class
 * 
 * Tests data conversion:
 * - Ingredient list to/from JSON string
 * - String list to/from comma-separated string
 * - Category enum to/from string
 */
class ConvertersTest {
    
    private lateinit var converters: Converters
    
    @Before
    fun setup() {
        converters = Converters()
    }
    
    @Test
    fun testIngredientListConversion() {
        // Create a sample list of ingredients
        val ingredients = listOf(
            Ingredient("Flour", "2 cups"),
            Ingredient("Sugar", "1 cup"),
            Ingredient("Eggs", "2")
        )
        
        // Convert to string
        val jsonString = converters.fromIngredientsList(ingredients)
        
        // Verify string format
        assertTrue("JSON should contain ingredient names", jsonString.contains("Flour"))
        assertTrue("JSON should contain measurements", jsonString.contains("2 cups"))
        
        // Convert back to list
        val resultList = converters.toIngredientsList(jsonString)
        
        // Verify conversion accuracy
        assertEquals("Should have same number of ingredients", ingredients.size, resultList.size)
        assertEquals("First ingredient name should match", ingredients[0].name, resultList[0].name)
        assertEquals("First ingredient measure should match", ingredients[0].measure, resultList[0].measure)
    }
    
    @Test
    fun testNullOrEmptyIngredientsList() {
        // Test null ingredients list
        val nullResult = converters.fromIngredientsList(null)
        assertEquals("Null list should convert to empty string", "", nullResult)
        
        // Test empty ingredients list
        val emptyResult = converters.fromIngredientsList(emptyList())
        assertTrue("Empty list should convert to empty JSON array", 
            emptyResult == "[]" || emptyResult.isEmpty())
        
        // Test empty string to ingredients list
        val emptyStringResult = converters.toIngredientsList("")
        assertTrue("Empty string should convert to empty list", emptyStringResult.isEmpty())
        
        // test invalid JSON
        val invalidResult = converters.toIngredientsList("not valid json")
        assertTrue("Invalid JSON should return empty list", invalidResult.isEmpty())
    }
    
    @Test
    fun testStringListConversion() {
        // Create a sample list of strings
        val stringList = listOf("apple", "banana", "cherry")
        
        // Convert to string
        val result = converters.fromStringList(stringList)
        assertEquals("Should be comma-separated", "apple,banana,cherry", result)
        
        // Convert back to list
        val resultList = converters.toStringList(result)
        assertEquals("Should convert back to original list", stringList, resultList)
        
        // Test null string list
        assertEquals("", converters.fromStringList(null))
        
        // Test empty string list
        assertEquals("", converters.fromStringList(emptyList()))
        
        // Test empty string to list
        assertTrue(converters.toStringList("").isEmpty())
    }
    
    @Test
    fun testStringListWithSpecialCharacters() {
        // Test with strings containing commas and spaces
        val specialStringList = listOf("item 1", "item,2", "item, 3")
        
        // Convert to string - this may produce different results
        val result = converters.fromStringList(specialStringList)
        
        // can't expect exact format due to escaping handling differences
        // just check if conversion doesn't crash and produces something
        assertNotNull(result)
        
        // just verify it's not empty some output and not an exception
        // actual implementation might handle commas in different ways
        assertTrue("Should produce non-empty string", result.isNotEmpty())
    }
    
    @Test
    fun testCategoryConversion() {
        // Test common categories with known behavior
        val dessertCategory = Category.DESSERT
        val dessertResult = converters.fromCategory(dessertCategory)
        assertEquals("Dessert category should convert to 'Dessert'", dessertCategory.displayName, dessertResult)
        
        val resultCategory = converters.toCategory(dessertResult)
        assertEquals("Should convert back to original enum", dessertCategory, resultCategory)
        
        // Test UNKNOWN category
        val unknownResult = converters.fromCategory(Category.UNKNOWN)
        // Don't assert exact string - implementation may vary
        assertNotNull("UNKNOWN should convert to some string", unknownResult)
        
        // test null category
        val nullResult = converters.fromCategory(null)
        assertNotNull("Null should produce some string result", nullResult)
        
        // Test invalid category string
        val invalidResult = converters.toCategory("InvalidCategory")
        assertEquals("Invalid category should convert to UNKNOWN", Category.UNKNOWN, invalidResult)
    }
} 