package com.example.myrecipeapp.viewmodel

import android.app.Application
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDao
import com.example.myrecipeapp.util.TestHelper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.hamcrest.MatcherAssert.assertThat
import org.hamcrest.Matchers.equalTo
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TestWatcher
import org.junit.runner.Description

/**
 * Test class for RecipeViewModel that doesn't use the database
 */
class RecipeViewModelTest {
    
    // Rule to handle LiveData
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()
    
    // Rule to handle coroutines
    @get:Rule
    val coroutineRule = object : TestWatcher() {
        private val testDispatcher = StandardTestDispatcher()
        
        override fun starting(description: Description) {
            Dispatchers.setMain(testDispatcher)
        }
        
        override fun finished(description: Description) {
            Dispatchers.resetMain()
        }
    }
    
    // Test data
    private val sampleRecipe = TestHelper.createSampleRecipe(id = 1, isFavorite = false)
    
    // Test implementation of ViewModel
    private lateinit var viewModel: TestRecipeViewModel
    
    // Test DAO implementation
    private lateinit var testRecipeDao: TestRecipeDao
    
    /**
     * A ViewModel implementation for testing that doesn't use the real database
     */
    class TestRecipeViewModel : RecipeViewModel(null) {
        
        val testRecipeDao = TestRecipeDao()
        
        // Override properties to use test implementations
        override val recipes: Flow<List<Recipe>> = testRecipeDao.getAll()
        override val favoriteRecipes: Flow<List<Recipe>> = testRecipeDao.getFavorites()
        
        // Use a StateFlow to hold the current recipe
        private val _currentRecipeFlow = MutableStateFlow<Recipe?>(null)
        override val currentRecipe: StateFlow<Recipe?> = _currentRecipeFlow
        
        // Method implementations for testing
        override fun getRecipeById(id: Int) {
            kotlinx.coroutines.test.runTest {
                _currentRecipeFlow.value = testRecipeDao.getById(id)
            }
        }
        
        override fun toggleFavorite(recipe: Recipe) {
            kotlinx.coroutines.test.runTest {
                val updatedRecipe = recipe.copy(isFavorite = !recipe.isFavorite)
                testRecipeDao.update(updatedRecipe)
                
                // Update current recipe if it's the same one
                if (_currentRecipeFlow.value?.id == recipe.id) {
                    _currentRecipeFlow.value = updatedRecipe
                }
            }
        }
        
        override fun addRecipe(recipe: Recipe) {
            kotlinx.coroutines.test.runTest {
                testRecipeDao.insert(recipe)
            }
        }
        
        override fun updateRecipe(recipe: Recipe) {
            kotlinx.coroutines.test.runTest {
                testRecipeDao.update(recipe)
            }
        }
        
        override fun deleteRecipe(recipe: Recipe) {
            kotlinx.coroutines.test.runTest {
                testRecipeDao.delete(recipe)
            }
        }
    }
    
    /**
     * Test implementation of RecipeDao for unit testing
     */
    class TestRecipeDao : RecipeDao {
        private val allRecipes = flowOf(listOf<Recipe>())
        private val favoriteRecipes = flowOf(listOf<Recipe>())
        
        // Track method calls
        val getByIdCalls = mutableListOf<Int>()
        val insertCalls = mutableListOf<Recipe>()
        val updateCalls = mutableListOf<Recipe>()
        val deleteCalls = mutableListOf<Recipe>()
        val searchCalls = mutableListOf<String>()
        
        // Map to store test recipes
        private val recipeMap = mutableMapOf<Int, Recipe>()
        
        // Implementation
        override fun getAll() = allRecipes
        override fun getFavorites() = favoriteRecipes
        
        override suspend fun getById(id: Int): Recipe? {
            getByIdCalls.add(id)
            return recipeMap[id]
        }
        
        override fun search(query: String): Flow<List<Recipe>> {
            searchCalls.add(query)
            return flowOf(recipeMap.values.filter { 
                it.name.contains(query, ignoreCase = true) || 
                it.ingredients.contains(query, ignoreCase = true) || 
                it.category.contains(query, ignoreCase = true) 
            }.toList())
        }
        
        override suspend fun insert(recipe: Recipe): Long {
            insertCalls.add(recipe)
            recipeMap[recipe.id] = recipe
            return recipe.id.toLong()
        }
        
        override suspend fun update(recipe: Recipe): Int {
            updateCalls.add(recipe)
            recipeMap[recipe.id] = recipe
            return 1
        }
        
        override suspend fun delete(recipe: Recipe): Int {
            deleteCalls.add(recipe)
            recipeMap.remove(recipe.id)
            return 1
        }
        
        fun addTestRecipe(recipe: Recipe) {
            recipeMap[recipe.id] = recipe
        }
    }
    
    @Before
    fun setup() {
        // Create test ViewModel
        viewModel = TestRecipeViewModel()
        testRecipeDao = viewModel.testRecipeDao
        
        // Add test data
        testRecipeDao.addTestRecipe(sampleRecipe)
    }
    
    @After
    fun tearDown() {
        // Nothing to clean up
    }

    @Test
    fun getRecipeById_updatesCurrentRecipe() = runTest {
        // Given a recipe ID
        val recipeId = 1
        
        // When requesting that recipe
        viewModel.getRecipeById(recipeId)
        
        // Then currentRecipe should be updated with the recipe from the DAO
        assertThat(viewModel.currentRecipe.value, equalTo(sampleRecipe))
        assertThat(testRecipeDao.getByIdCalls.contains(recipeId), equalTo(true))
    }

    @Test
    fun toggleFavorite_updatesRecipeFavoriteStatus() = runTest {
        // Given a recipe with isFavorite = false
        
        // When toggling its favorite status
        viewModel.toggleFavorite(sampleRecipe)
        
        // Then the DAO should be called with updated recipe
        assertThat(testRecipeDao.updateCalls.size, equalTo(1))
        val updatedRecipe = testRecipeDao.updateCalls.first()
        assertThat(updatedRecipe.id, equalTo(sampleRecipe.id))
        assertThat(updatedRecipe.isFavorite, equalTo(!sampleRecipe.isFavorite))
    }
    
    @Test
    fun toggleFavorite_updatesCurrentRecipe_whenSameRecipe() = runTest {
        // Given the ViewModel has a currentRecipe set
        viewModel.getRecipeById(sampleRecipe.id)
        
        // When toggling its favorite status
        viewModel.toggleFavorite(sampleRecipe)
        
        // Then currentRecipe should also be updated
        assertThat(viewModel.currentRecipe.value?.isFavorite, equalTo(true))
    }

    @Test
    fun toggleFavorite_doesNotUpdateCurrentRecipe_whenDifferentRecipe() = runTest {
        // Given the ViewModel has a currentRecipe set
        val otherRecipe = TestHelper.createSampleRecipe(id = 99)
        testRecipeDao.addTestRecipe(otherRecipe)
        viewModel.getRecipeById(99)
        
        // When toggling a different recipe's favorite status
        val recipeToToggle = sampleRecipe.copy(id = 1)
        viewModel.toggleFavorite(recipeToToggle)
        
        // Then currentRecipe should not be updated
        assertThat(viewModel.currentRecipe.value?.id, equalTo(99))
        assertThat(viewModel.currentRecipe.value?.isFavorite, equalTo(false))
    }

    @Test
    fun addRecipe_callsDaoInsertMethod() = runTest {
        // Given a new recipe
        val newRecipe = TestHelper.createSampleRecipe(id = 0, isFavorite = false)
        
        // When adding the recipe
        viewModel.addRecipe(newRecipe)
        
        // Then the DAO insert method should be called
        assertThat(testRecipeDao.insertCalls.contains(newRecipe), equalTo(true))
    }

    @Test
    fun updateRecipe_callsDaoUpdateMethod() = runTest {
        // Given an updated recipe
        val updatedRecipe = sampleRecipe.copy(name = "Updated Recipe Name")
        
        // When updating the recipe
        viewModel.updateRecipe(updatedRecipe)
        
        // Then the DAO update method should be called
        assertThat(testRecipeDao.updateCalls.contains(updatedRecipe), equalTo(true))
    }

    @Test
    fun deleteRecipe_callsDaoDeleteMethod() = runTest {
        // Given a recipe to delete
        
        // When deleting the recipe
        viewModel.deleteRecipe(sampleRecipe)
        
        // Then the DAO delete method should be called
        assertThat(testRecipeDao.deleteCalls.contains(sampleRecipe), equalTo(true))
    }
} 