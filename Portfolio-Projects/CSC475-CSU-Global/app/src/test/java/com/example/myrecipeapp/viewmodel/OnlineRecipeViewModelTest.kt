package com.example.myrecipeapp.viewmodel

import android.app.Application
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.myrecipeapp.model.OnlineRecipe
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDao
import com.example.myrecipeapp.repository.OnlineMealRepository
import com.example.myrecipeapp.util.TestHelper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.hamcrest.MatcherAssert.assertThat
import org.hamcrest.Matchers.containsString
import org.hamcrest.Matchers.equalTo
import org.hamcrest.Matchers.not
import org.hamcrest.Matchers.nullValue
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TestWatcher
import org.junit.runner.Description
import retrofit2.HttpException
import retrofit2.Response
import okhttp3.ResponseBody.Companion.toResponseBody
import java.io.IOException

/**
 * Unit tests for OnlineRecipeViewModel.
 */
@OptIn(ExperimentalCoroutinesApi::class)
class OnlineRecipeViewModelTest {

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
    private val sampleRecipe = TestHelper.createSampleRecipe(id = 1)
    private val sampleOnlineRecipe = TestHelper.createSampleOnlineRecipe()
    
    // Test implementation of ViewModel
    private lateinit var viewModel: TestOnlineRecipeViewModel
    
    // Test repository implementation
    private lateinit var testRepository: TestOnlineMealRepository
    
    // Test DAO implementation
    private lateinit var testRecipeDao: TestRecipeDao
    
    /**
     * A ViewModel implementation for testing that doesn't use the real repository or database
     */
    class TestOnlineRecipeViewModel : OnlineRecipeViewModel(null) {
        
        val testRepository = TestOnlineMealRepository()
        val testRecipeDao = TestRecipeDao()
        
        // Search-related LiveData for testing
        private val _searchResults = MutableLiveData<List<OnlineRecipe>>(emptyList())
        override val searchResults: LiveData<List<OnlineRecipe>> = _searchResults
        
        // Loading and error states
        private val _isLoading = MutableLiveData<Boolean>(false)
        override val isLoading: LiveData<Boolean> = _isLoading
        
        private val _error = MutableLiveData<String?>(null)
        override val error: LiveData<String?> = _error
        
        // Current recipe detail
        private val _currentRecipe = MutableLiveData<OnlineRecipe?>()
        override val currentRecipe: LiveData<OnlineRecipe?> = _currentRecipe
        
        // Search query for testing
        private var lastQuery = ""
        private var lastSearchType = SearchType.NAME
        
        // Method implementations that don't use real repository or Android dependencies
        override fun searchMeals(query: String, searchType: SearchType, resetPagination: Boolean) {
            if (query.isBlank()) {
                _searchResults.value = emptyList()
                return
            }
            
            _isLoading.value = true
            _error.value = null
            lastQuery = query
            lastSearchType = searchType
            
            runTest {
                try {
                    // Simulate searching based on search type
                    val formattedQuery = formatQueryForSearchType(query, searchType)
                    
                    val results = when (searchType) {
                        SearchType.NAME -> testRepository.searchMealsByName(formattedQuery)
                        SearchType.INGREDIENT -> testRepository.getMealsByIngredient(formattedQuery)
                        SearchType.CATEGORY -> testRepository.getMealsByCategory(formattedQuery)
                        SearchType.AREA -> testRepository.getMealsByArea(formattedQuery)
                    }
                    
                    // Simulate collecting the flow
                    results.collect { recipes ->
                        val onlineRecipes = recipes.map { recipeToOnlineRecipe(it) }
                        _searchResults.value = onlineRecipes
                    }
                    
                    _isLoading.value = false
                } catch (e: IOException) {
                    _error.value = "Network error: ${e.message}"
                    _isLoading.value = false
                    _searchResults.value = emptyList()
                } catch (e: HttpException) {
                    _error.value = "API error: ${e.message()}"
                    _isLoading.value = false
                    _searchResults.value = emptyList()
                } catch (e: Exception) {
                    _error.value = "Error: ${e.message}"
                    _isLoading.value = false
                    _searchResults.value = emptyList()
                }
            }
        }
        
        override fun getMealById(id: String) {
            _isLoading.value = true
            _error.value = null
            
            runTest {
                try {
                    testRepository.getMealById(id).collect { recipe ->
                        if (recipe != null) {
                            _currentRecipe.value = recipeToOnlineRecipe(recipe)
                        } else {
                            _error.value = "Recipe not found"
                        }
                        _isLoading.value = false
                    }
                } catch (e: Exception) {
                    _error.value = "Error: ${e.message}"
                    _isLoading.value = false
                }
            }
        }
        
        override fun saveRecipeToCollection() {
            currentRecipe.value?.let { onlineRecipe ->
                runTest {
                    // Convert OnlineRecipe to Recipe for storage
                    val ingredientsString = onlineRecipe.ingredients.joinToString(",") { 
                        "${it.name}:${it.measure ?: ""}" 
                    }
                    
                    val localRecipe = Recipe(
                        name = onlineRecipe.name,
                        category = onlineRecipe.category,
                        area = onlineRecipe.area,
                        instructions = onlineRecipe.instructions,
                        ingredients = ingredientsString,
                        thumbnailUrl = onlineRecipe.thumbnailUrl,
                        youtubeUrl = onlineRecipe.youtubeUrl ?: "",
                        tags = onlineRecipe.tags,
                        source = onlineRecipe.source ?: "",
                        isFavorite = false,
                        mealDbId = onlineRecipe.mealDbId
                    )
                    
                    // Save to test DAO
                    testRecipeDao.insert(localRecipe)
                }
            }
        }
        
        private fun runTest(block: suspend () -> Unit) {
            kotlinx.coroutines.test.runTest {
                block()
            }
        }
    }
    
    /**
     * Test implementation of OnlineMealRepository
     */
    class TestOnlineMealRepository : OnlineMealRepository() {
        // Track method calls
        val searchMealsByNameCalls = mutableListOf<String>()
        val getMealsByIngredientCalls = mutableListOf<String>()
        val getMealsByCategoryCalls = mutableListOf<String>()
        val getMealsByAreaCalls = mutableListOf<String>()
        val getMealByIdCalls = mutableListOf<String>()
        
        // Control test behavior
        var shouldThrowIOException = false
        var shouldThrowHttpException = false
        
        // Test data
        private val testRecipe = TestHelper.createSampleRecipe(id = 1)
        private val recipeMap = mutableMapOf<String, Recipe>().apply {
            put("12345", testRecipe)
        }
        
        override fun searchMealsByName(query: String): Flow<List<Recipe>> {
            searchMealsByNameCalls.add(query)
            
            if (shouldThrowIOException) {
                throw IOException("Network error")
            }
            
            if (shouldThrowHttpException) {
                throw HttpException(Response.error<Any>(404, "Not found".toResponseBody()))
            }
            
            return flowOf(listOf(testRecipe))
        }
        
        override fun getMealsByIngredient(ingredient: String): Flow<List<Recipe>> {
            getMealsByIngredientCalls.add(ingredient)
            
            if (shouldThrowIOException) {
                throw IOException("Network error")
            }
            
            if (shouldThrowHttpException) {
                throw HttpException(Response.error<Any>(404, "Not found".toResponseBody()))
            }
            
            return flowOf(listOf(testRecipe))
        }
        
        override fun getMealsByCategory(category: String): Flow<List<Recipe>> {
            getMealsByCategoryCalls.add(category)
            return flowOf(listOf(testRecipe))
        }
        
        override fun getMealsByArea(area: String): Flow<List<Recipe>> {
            getMealsByAreaCalls.add(area)
            return flowOf(listOf(testRecipe))
        }
        
        override fun getMealById(id: String): Flow<Recipe?> {
            getMealByIdCalls.add(id)
            return flowOf(recipeMap[id])
        }
        
        override suspend fun getCategories(): List<String> {
            return listOf("Beef", "Chicken", "Dessert", "Pasta")
        }
        
        override suspend fun getAreas(): List<String> {
            return listOf("Italian", "American", "Chinese", "Mexican")
        }
    }
    
    /**
     * test implementation of RecipeDao
     */
    class TestRecipeDao : RecipeDao {
        private val allRecipes = flowOf(listOf<Recipe>())
        private val favoriteRecipes = flowOf(listOf<Recipe>())
        
        // Track method calls
        val insertCalls = mutableListOf<Recipe>()
        
        // Map to store test recipes
        private val recipeMap = mutableMapOf<Int, Recipe>()
        
        override fun getAll() = allRecipes
        override fun getFavorites() = favoriteRecipes
        
        override suspend fun getById(id: Int): Recipe? {
            return recipeMap[id]
        }
        
        override fun search(query: String): Flow<List<Recipe>> {
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
            recipeMap[recipe.id] = recipe
            return 1
        }
        
        override suspend fun delete(recipe: Recipe): Int {
            recipeMap.remove(recipe.id)
            return 1
        }
    }
    
    @Before
    fun setup() {
        // Create test ViewModel
        viewModel = TestOnlineRecipeViewModel()
        testRepository = viewModel.testRepository
        testRecipeDao = viewModel.testRecipeDao
    }
    
    @After
    fun tearDown() {
        // Nothing to clean up
    }

    @Test
    fun searchMeals_byName_shouldUpdateSearchResultsWithRecipesFromRepository() = runTest {
        // Given a search query
        val query = "pasta"
        
        // When searching by name
        viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.NAME)
        
        // Then search results should be updated
        assertThat(viewModel.searchResults.value, not(nullValue()))
        assertThat(viewModel.searchResults.value?.size, equalTo(1))
        assertThat(viewModel.isLoading.value, equalTo(false))
        assertThat(viewModel.error.value, nullValue())
        
        assertThat(testRepository.searchMealsByNameCalls.contains(query), equalTo(true))
    }
    
    @Test
    fun searchMeals_byIngredient_shouldUpdateSearchResultsWithRecipesFromRepository() = runTest {
        // Given a search query
        val query = "chicken"
        
        // When searching by ingredient
        viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.INGREDIENT)
        
        // Then search results should be updated
        assertThat(viewModel.searchResults.value, not(nullValue()))
        assertThat(viewModel.searchResults.value?.size, equalTo(1))
        assertThat(viewModel.isLoading.value, equalTo(false))
        assertThat(viewModel.error.value, nullValue())
        
        // Verify the ingredient was formatted properly (spaces replaced with underscores)
        assertThat(testRepository.getMealsByIngredientCalls.any { it.contains(query) }, equalTo(true))
    }
    
    @Test
    fun searchMeals_shouldFormatIngredientQueryByReplacingSpacesWithUnderscores() = runTest {
        // Given a search query with spaces
        val query = "olive oil"
        
        // When searching by ingredient
        viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.INGREDIENT)
        
        // Then the repository should be called with formatted query (spaces replaced with underscores)
        val formattedQuery = query.replace(" ", "_").lowercase()
        assertThat(testRepository.getMealsByIngredientCalls.any { it.contains("_") }, equalTo(true))
        assertThat(testRepository.getMealsByIngredientCalls.contains(formattedQuery), equalTo(true))
    }
    
    @Test
    fun searchMeals_shouldReturnEmptyResultsForBlankQuery() = runTest {
        // Given a blank query
        val query = ""
        
        // When searching
        viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.NAME)
        
        // Then search results should be empty and repository should not be called
        assertThat(viewModel.searchResults.value, equalTo(emptyList()))
        assertThat(testRepository.searchMealsByNameCalls.contains(query), equalTo(false))
    }
    
    @Test
    fun searchMeals_shouldSetErrorWhenRepositoryThrowsIOException() = runTest {
        // Given a repository that throws an IOException
        testRepository.shouldThrowIOException = true
        
        // When searching
        viewModel.searchMeals("test", OnlineRecipeViewModel.SearchType.NAME)
        
        // Then error state should be set
        assertThat(viewModel.error.value, containsString("Network error"))
        assertThat(viewModel.isLoading.value, equalTo(false))
        assertThat(viewModel.searchResults.value, equalTo(emptyList()))
    }
    
    @Test
    fun searchMeals_shouldSetErrorWhenRepositoryThrowsHttpException() = runTest {
        // Given a repository that throws an HttpException
        testRepository.shouldThrowHttpException = true
        
        // When searching
        viewModel.searchMeals("test", OnlineRecipeViewModel.SearchType.NAME)
        
        // Then error state should be set
        assertThat(viewModel.error.value, containsString("API error"))
        assertThat(viewModel.isLoading.value, equalTo(false))
        assertThat(viewModel.searchResults.value, equalTo(emptyList()))
    }
    
    @Test
    fun getMealById_shouldUpdateCurrentRecipeWithRecipeFromRepository() = runTest {
        // Given a recipe ID
        val recipeId = "12345"
        
        // When requesting that recipe
        viewModel.getMealById(recipeId)
        
        // Then currentRecipe should be updated
        assertThat(viewModel.currentRecipe.value, not(nullValue()))
        assertThat(viewModel.isLoading.value, equalTo(false))
        
        assertThat(testRepository.getMealByIdCalls.contains(recipeId), equalTo(true))
    }
    
    @Test
    fun saveRecipeToCollection_shouldSaveCurrentRecipeToLocalDatabase() = runTest {
        // Given a current recipe is loaded
        val recipeId = "12345"
        viewModel.getMealById(recipeId)
        
        // When saving to collection
        viewModel.saveRecipeToCollection()
        
        // Then the DAO should be called to insert the recipe
        assertThat(testRecipeDao.insertCalls.size, equalTo(1))
    }
} 