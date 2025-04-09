package com.example.myrecipeapp.database

import android.content.Context
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import com.example.myrecipeapp.model.Category
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDao
import com.example.myrecipeapp.model.RecipeDatabase
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.hamcrest.CoreMatchers.equalTo
import org.hamcrest.CoreMatchers.notNullValue
import org.hamcrest.CoreMatchers.nullValue
import org.hamcrest.MatcherAssert.assertThat
import org.hamcrest.Matchers.hasSize
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

/**
 * Integration tests for Room database operations
 * Uses Robolectric to test Room database integration on JVM without a device
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [30]) // Target Android API level for testing
class RecipeDatabaseTest {

    private lateinit var recipeDao: RecipeDao
    private lateinit var database: RecipeDatabase

    @Before
    fun createDb() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        
        // Create an in-memory database for testing
        database = Room.inMemoryDatabaseBuilder(
            context,
            RecipeDatabase::class.java
        ).allowMainThreadQueries() // For simplicity in tests, allow queries on main thread
         .build()
        
        recipeDao = database.recipeDao()
    }

    @After
    fun closeDb() {
        database.close()
    }

    // Helper function to create test recipes
    private fun createTestRecipe(
        id: Int = 0,
        name: String = "Test Recipe",
        category: String = Category.DESSERT.displayName,
        isFavorite: Boolean = false
    ): Recipe {
        return Recipe(
            id = id,
            name = name,
            category = category,
            area = "Test Area",
            instructions = "Test instructions for making this recipe.",
            ingredients = "ingredient1:1 cup,ingredient2:2 tbsp",
            thumbnailUrl = "https://example.com/image.jpg",
            tags = "test,sample",
            isFavorite = isFavorite
        )
    }

    @Test
    fun insertAndRetrieveRecipe() = runBlocking {
        // create a test recipe
        val recipe = createTestRecipe(name = "Test Pie")
        
        // Insert recipe to the database
        val id = recipeDao.insert(recipe)
        
        // Retrieve recipe by ID
        val retrievedRecipe = recipeDao.getById(id.toInt())
        
        // Verify recipe was retrieved successfully
        assertThat(retrievedRecipe, notNullValue())
        assertThat(retrievedRecipe?.name, equalTo("Test Pie"))
        assertThat(retrievedRecipe?.category, equalTo(Category.DESSERT.displayName))
    }

    @Test
    fun getAllRecipes() = runBlocking {
        // insert multiple recipes
        val recipe1 = createTestRecipe(name = "Chocolate Cake")
        val recipe2 = createTestRecipe(name = "Apple Pie")
        val recipe3 = createTestRecipe(name = "Chicken Curry", category = Category.CHICKEN.displayName)
        
        recipeDao.insert(recipe1)
        recipeDao.insert(recipe2)
        recipeDao.insert(recipe3)
        
        // Get all recipes
        val allRecipes = recipeDao.getAll().first()
        
        // Verify all recipes were retrieved
        assertThat(allRecipes, hasSize(3))
        
        // Verify recipe names are correct
        val recipeNames = allRecipes.map { it.name }.toSet()
        assertThat(recipeNames.contains("Chocolate Cake"), equalTo(true))
        assertThat(recipeNames.contains("Apple Pie"), equalTo(true))
        assertThat(recipeNames.contains("Chicken Curry"), equalTo(true))
    }

    @Test
    fun updateRecipe() = runBlocking {
        // Insert a recipe
        val recipe = createTestRecipe(name = "Original Recipe")
        val id = recipeDao.insert(recipe).toInt()
        
        // Retrieve the recipe
        val retrievedRecipe = recipeDao.getById(id)
        
        // Update the recipe
        val updatedRecipe = retrievedRecipe?.copy(
            name = "Updated Recipe",
            instructions = "Updated instructions",
            isFavorite = true
        )
        
        if (updatedRecipe != null) {
            recipeDao.update(updatedRecipe)
        }
        
        // Retrieve the updated recipe
        val retrievedUpdatedRecipe = recipeDao.getById(id)
        
        // Verify the recipe was updated
        assertThat(retrievedUpdatedRecipe, notNullValue())
        assertThat(retrievedUpdatedRecipe?.name, equalTo("Updated Recipe"))
        assertThat(retrievedUpdatedRecipe?.instructions, equalTo("Updated instructions"))
        assertThat(retrievedUpdatedRecipe?.isFavorite, equalTo(true))
    }

    @Test
    fun deleteRecipe() = runBlocking {
        // Insert a recipe
        val recipe = createTestRecipe()
        val id = recipeDao.insert(recipe).toInt()
        
        // Retrieve the recipe
        val retrievedRecipe = recipeDao.getById(id)
        
        // Delete the recipe
        retrievedRecipe?.let { recipeDao.delete(it) }
        
        // Try to retrieve the deleted recipe
        val deletedRecipe = recipeDao.getById(id)
        
        // Verify the recipe was deleted
        assertThat(deletedRecipe, nullValue())
    }

    @Test
    fun getFavoriteRecipes() = runBlocking {
        // Insert recipes with different favorite status
        val favRecipe1 = createTestRecipe(name = "Favorite Recipe 1", isFavorite = true)
        val favRecipe2 = createTestRecipe(name = "Favorite Recipe 2", isFavorite = true)
        val nonFavRecipe = createTestRecipe(name = "Non-favorite Recipe", isFavorite = false)
        
        recipeDao.insert(favRecipe1)
        recipeDao.insert(favRecipe2)
        recipeDao.insert(nonFavRecipe)
        
        // get favorite recipes
        val favorites = recipeDao.getFavorites().first()
        
        // Verify only favorite recipes are returned
        assertThat(favorites, hasSize(2))
        assertThat(favorites.all { it.isFavorite }, equalTo(true))
        
        // Verify favorite recipe names
        val favoriteNames = favorites.map { it.name }.toSet()
        assertThat(favoriteNames.contains("Favorite Recipe 1"), equalTo(true))
        assertThat(favoriteNames.contains("Favorite Recipe 2"), equalTo(true))
        assertThat(favoriteNames.contains("Non-favorite Recipe"), equalTo(false))
    }

    @Test
    fun searchRecipes() = runBlocking {
        // Insert recipes with different names and ingredients
        val chocolateCake = createTestRecipe(
            name = "Chocolate Cake"
        ).copy(ingredients = "flour:2 cups,sugar:1 cup,chocolate:200g,eggs:2")
        
        val chocolateMousse = createTestRecipe(
            name = "Chocolate Mousse"
        ).copy(ingredients = "chocolate:150g,cream:1 cup,egg whites:4")
        
        val strawberryPie = createTestRecipe(
            name = "Strawberry Pie"
        ).copy(ingredients = "flour:1.5 cups,sugar:0.5 cup,strawberries:500g,butter:100g")
        
        recipeDao.insert(chocolateCake)
        recipeDao.insert(chocolateMousse)
        recipeDao.insert(strawberryPie)
        
        // Search for chocolate recipes
        val chocolateResults = recipeDao.search("chocolate").first()
        
        // Verify chocolate recipes are returned
        assertThat(chocolateResults, hasSize(2))
        
        // Search for strawberry recipes
        val strawberryResults = recipeDao.search("strawberry").first()
        
        // Verify strawberry recipes are returned
        assertThat(strawberryResults, hasSize(1))
        assertThat(strawberryResults[0].name, equalTo("Strawberry Pie"))
        
        // Search for cream in ingredients
        val creamResults = recipeDao.search("cream").first()
        
        // verify recipes with cream are returned
        assertThat(creamResults, hasSize(1))
        assertThat(creamResults[0].name, equalTo("Chocolate Mousse"))
        
        // Search for non-existent recipe
        val noResults = recipeDao.search("nonexistent").first()
        
        // Verify no recipes are returned
        assertThat(noResults, hasSize(0))
    }

    @Test
    fun searchByCategory() = runBlocking {
        // Insert recipes with different categories
        val dessertRecipe = createTestRecipe(
            name = "Dessert Recipe", 
            category = Category.DESSERT.displayName
        )
        val pastaRecipe = createTestRecipe(
            name = "Pasta Recipe", 
            category = Category.PASTA.displayName
        )
        val chickenRecipe = createTestRecipe(
            name = "Chicken Recipe", 
            category = Category.CHICKEN.displayName
        )
        
        recipeDao.insert(dessertRecipe)
        recipeDao.insert(pastaRecipe)
        recipeDao.insert(chickenRecipe)
        
        // Search for dessert category
        val dessertResults = recipeDao.search("Dessert").first()
        
        // Verify dessert recipes are returned
        assertThat(dessertResults, hasSize(1))
        assertThat(dessertResults[0].category, equalTo(Category.DESSERT.displayName))
        
        // Search for pasta category
        val pastaResults = recipeDao.search("Pasta").first()
        
        // Verify pasta recipes are returned
        assertThat(pastaResults, hasSize(1))
        assertThat(pastaResults[0].name, equalTo("Pasta Recipe"))
    }
} 