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
MVVM Architecture: VIEWMODEL
    This file contains the OnlineRecipeViewModel for managing online recipe data and operations
 */

package com.example.myrecipeapp.viewmodel

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.myrecipeapp.model.Ingredient
import com.example.myrecipeapp.model.OnlineRecipe
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDao
import com.example.myrecipeapp.model.RecipeDatabase
import com.example.myrecipeapp.repository.OnlineMealRepository
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import retrofit2.HttpException
import java.io.IOException

/**
 * ViewModel for TheMealDB online recipes
 */
class OnlineRecipeViewModel(application: Application) : AndroidViewModel(application) {
    
    // Repository for online recipes
    private val onlineMealRepository = OnlineMealRepository.getInstance()
    
    // Repository for saving recipes locally
    private val recipeDao: RecipeDao
    
    // Search-related LiveData
    private val _searchResults = MutableLiveData<List<OnlineRecipe>>(emptyList())
    val searchResults: LiveData<List<OnlineRecipe>> = _searchResults
    
    // Pagination and infinite scrolling
    private val _hasMoreResults = MutableLiveData<Boolean>(false)
    val hasMoreResults: LiveData<Boolean> = _hasMoreResults
    
    // Store all loaded meals for pagination
    private var allLoadedMeals = mutableListOf<OnlineRecipe>()
    private var currentPage = 1
    private val pageSize = 10
    
    private val _searchQuery = MutableLiveData<String>("")
    private val _currentSearchType = MutableLiveData<SearchType>(SearchType.NAME)
    
    // Current recipe detail
    private val _currentRecipe = MutableLiveData<OnlineRecipe?>()
    val currentRecipe: LiveData<OnlineRecipe?> = _currentRecipe
    
    // Loading and error states
    private val _isLoading = MutableLiveData<Boolean>(false)
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>(null)
    val error: LiveData<String?> = _error
    
    // Available categories 
    private val _categories = MutableLiveData<List<String>>(emptyList())
    val categories: LiveData<List<String>> = _categories
    
    // Available areas
    private val _areas = MutableLiveData<List<String>>(emptyList())
    val areas: LiveData<List<String>> = _areas
    
    // Random meal
    private val _randomMeal = MutableLiveData<Recipe?>(null)
    
    init {
        recipeDao = RecipeDatabase.getInstance(application).recipeDao()
        loadMetadata()
    }

    //---------------------------------------------------------------

    /**
     * Load categories and areas
     */
    private fun loadMetadata() {
        viewModelScope.launch {
            try {
                // Use repository instead of direct API calls
                val categoryList = onlineMealRepository.getCategories()
                _categories.value = categoryList
                
                val areaList = onlineMealRepository.getAreas()
                _areas.value = areaList
            } catch (e: Exception) {
                _error.value = "Failed to load categories and areas: ${e.message}"
                e.printStackTrace()
            }
        }
    }

    //---------------------------------------------------------------
    
    /**
     * Search for meals using the repository
     */
    fun searchMeals(query: String, searchType: SearchType, resetPagination: Boolean = false) {
        if (query.isBlank()) {
            _searchResults.value = emptyList()
            return
        }
        
        _isLoading.value = true
        _error.value = null
        _searchQuery.value = query
        _currentSearchType.value = searchType
        
        Log.d("OnlineRecipeViewModel", "Searching for $searchType with query: '$query'")
        
        if (resetPagination) {
            currentPage = 1
            allLoadedMeals.clear()
        }
        
        viewModelScope.launch {
            try {
                val formattedQuery = formatQueryForSearchType(query, searchType)
                Log.d("OnlineRecipeViewModel", "Formatted query: '$formattedQuery'")
                
                val recipes = when (searchType) {
                    SearchType.NAME -> onlineMealRepository.searchMealsByName(formattedQuery)
                    SearchType.INGREDIENT -> onlineMealRepository.getMealsByIngredient(formattedQuery)
                    SearchType.CATEGORY -> onlineMealRepository.getMealsByCategory(formattedQuery)
                    SearchType.AREA -> onlineMealRepository.getMealsByArea(formattedQuery)
                }

                //--------------------------------------------
                
                // Collect the flow result
                recipes.collectLatest { recipeList ->
                    if (recipeList.isNotEmpty()) {
                        Log.d("OnlineRecipeViewModel", "Search returned ${recipeList.size} results")
                        
                        // Convert results to OnlineRecipe objects
                        val allMeals = recipeList.mapNotNull { recipe ->
                            try {
                                // Convert Recipe to OnlineRecipe
                                recipeToOnlineRecipe(recipe)
                            } catch (e: Exception) {
                                Log.e("OnlineRecipeViewModel", "Error converting recipe: ${e.message}")
                                null
                            }
                        }
                        
                        allLoadedMeals = allMeals.toMutableList()
                        
                        // Display only first page initially
                        val initialResults = allLoadedMeals.take(pageSize)
                        _searchResults.postValue(initialResults)
                        
                        // Check if there are more results to load
                        _hasMoreResults.postValue(allLoadedMeals.size > pageSize)
                    } else {
                        Log.d("OnlineRecipeViewModel", "Search returned null or empty results")
                        _searchResults.postValue(emptyList())
                        _hasMoreResults.postValue(false)
                        
                        val errorMessage = when (searchType) {
                            SearchType.NAME -> "No recipes found with name: '$formattedQuery'"
                            SearchType.INGREDIENT -> "No recipes found with ingredient: '${formattedQuery.replace("_", " ")}'"
                            SearchType.CATEGORY -> "No recipes found in category: '$formattedQuery'"
                            SearchType.AREA -> "No recipes found from: '$formattedQuery'"
                        }
                        _error.postValue(errorMessage)
                    }
                    _isLoading.postValue(false)
                }
            } catch (e: IOException) {
                Log.e("OnlineRecipeViewModel", "Network error", e)
                _error.postValue("Network error: ${e.message}")
                _isLoading.postValue(false)
                _searchResults.postValue(emptyList())
            } catch (e: HttpException) {
                Log.e("OnlineRecipeViewModel", "API error: ${e.code()}, ${e.message()}")
                _error.postValue("API error: ${e.message()}")
                _isLoading.postValue(false)
                _searchResults.postValue(emptyList())
            } catch (e: Exception) {
                Log.e("OnlineRecipeViewModel", "Exception searching TheMealDB", e)
                _error.postValue("Error: ${e.message}")
                _isLoading.postValue(false)
                _searchResults.postValue(emptyList())
            }
        }
    }

    //---------------------------------------------------------------

    /**
     * Load more results for infinite scrolling
     */
    fun loadMoreResults(searchType: SearchType) {
        if (!_hasMoreResults.value!!) return
        
        currentPage++
        val nextPageStart = (currentPage - 1) * pageSize
        val nextPageEnd = currentPage * pageSize
        
        if (nextPageStart >= allLoadedMeals.size) {
            _hasMoreResults.value = false
            return
        }
        
        val nextPageItems = allLoadedMeals.subList(
            nextPageStart,
            minOf(nextPageEnd, allLoadedMeals.size)
        )
        
        // Append to existing results
        val currentResults = _searchResults.value ?: emptyList()
        _searchResults.value = currentResults + nextPageItems
        
        // Check if we've shown all items
        _hasMoreResults.value = allLoadedMeals.size > nextPageEnd
    }

    //---------------------------------------------------------------
    
    /**
     * Get meal details by ID
     */
    fun getMealById(id: String) {
        _isLoading.value = true
        _error.value = null
        
        viewModelScope.launch {
            try {
                onlineMealRepository.getMealById(id).collectLatest { recipe ->
                    if (recipe != null) {
                        // Convert Recipe to OnlineRecipe
                        _currentRecipe.postValue(recipeToOnlineRecipe(recipe))
                    } else {
                        _error.postValue("Recipe not found")
                    }
                    _isLoading.postValue(false)
                }
            } catch (e: IOException) {
                _error.postValue("Network error: ${e.message}")
                _isLoading.postValue(false)
            } catch (e: HttpException) {
                _error.postValue("HTTP error: ${e.code()}")
                _isLoading.postValue(false)
            } catch (e: Exception) {
                _error.postValue("Error: ${e.message}")
                _isLoading.postValue(false)
            }
        }
    }

    //---------------------------------------------------------------
    
    fun clearSearch() {
        _searchQuery.value = ""
        _searchResults.value = emptyList()
    }

    //---------------------------------------------------------------

    /**
     * Saves the current online recipe to the local database collection
     */
    fun saveRecipeToCollection() {
        currentRecipe.value?.let { onlineRecipe ->
            viewModelScope.launch {
                // Convert OnlineRecipe to Recipe
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
                
                // Save to local database
                recipeDao.insert(localRecipe)
            }
        }
    }

    //---------------------------------------------------------------
    
    /**
     * Get a random meal from the repository
     */
    fun getRandomMeal() {
        _isLoading.value = true
        _error.value = null
        
        viewModelScope.launch {
            try {
                onlineMealRepository.getRandomMeal().collectLatest { recipe ->
                    _randomMeal.postValue(recipe)
                    _isLoading.postValue(false)
                }
            } catch (e: Exception) {
                _error.postValue("Failed to load random meal: ${e.message}")
                _isLoading.postValue(false)
            }
        }
    }

    //---------------------------------------------------------------

    /**
     * Helper function to convert Recipe to OnlineRecipe
     */
    private fun recipeToOnlineRecipe(recipe: Recipe): OnlineRecipe {
        val ingredientPairs = recipe.ingredients.split(",")
            .filter { it.isNotBlank() }
            .map { pair ->
                val parts = pair.split(":")
                val name = parts[0].trim()
                val measure = if (parts.size > 1) parts[1].trim() else ""
                Ingredient(name, measure)
            }
        
        return OnlineRecipe(
            id = recipe.mealDbId.ifBlank { recipe.id.toString() }, // Use mealDbId or convert local id to string
            name = recipe.name,
            mealDbId = recipe.mealDbId,
            category = recipe.category,
            area = recipe.area,
            instructions = recipe.instructions,
            thumbnailUrl = recipe.thumbnailUrl,
            youtubeUrl = recipe.youtubeUrl,
            tags = recipe.tags,
            source = recipe.source,
            imageSource = null, // No equivalent in Recipe, set to null
            ingredients = ingredientPairs
        )
    }

    //---------------------------------------------------------------
    
    /**
     * Format a search query based on the search type
     *
     * @param query The original user query
     * @param searchType The type of search (NAME, CATEGORY, INGREDIENT, or AREA)
     * @return The formatted query string optimized for TheMealDB API
     */
    private fun formatQueryForSearchType(query: String, searchType: SearchType): String {
        return when (searchType) {
            SearchType.NAME -> query.trim()
            SearchType.CATEGORY -> {
                // TheMealDB API requires exact category names
                val normalizedCategory = query.trim().replaceFirstChar { 
                    if (it.isLowerCase()) it.titlecase(java.util.Locale.getDefault()) else it.toString() 
                }
                
                // Convert common terms to official TheMealDB categories
                when (normalizedCategory.lowercase()) {
                    "breakfast" -> "Breakfast"
                    "chicken", "poultry" -> "Chicken"
                    "dessert", "sweets", "cake", "cakes" -> "Dessert"
                    "goat" -> "Goat"
                    "lamb" -> "Lamb"
                    "pasta", "noodles" -> "Pasta"
                    "pork" -> "Pork"
                    "seafood", "fish" -> "Seafood"
                    "side", "sides", "side dish" -> "Side"
                    "starter", "starters", "appetizer", "appetizers" -> "Starter"
                    "vegan" -> "Vegan"
                    "vegetarian", "veggie" -> "Vegetarian"
                    "beef", "steak" -> "Beef"
                    "miscellaneous", "misc" -> "Miscellaneous"
                    else -> normalizedCategory  // Use normalized version for other categories
                }
            }
            SearchType.INGREDIENT -> query.trim().replace(" ", "_").lowercase()
            SearchType.AREA -> {
                // TheMealDB API is very particular about area names
                // First capitalize correctly
                val capitalizedArea = query.trim().replaceFirstChar { 
                    if (it.isLowerCase()) it.titlecase(java.util.Locale.getDefault()) else it.toString() 
                }
                
                // Then handle special cases
                when (capitalizedArea.lowercase()) {
                    "us", "usa", "united states", "american" -> "American"
                    "uk", "united kingdom", "england", "british", "great britain" -> "British"
                    "italy", "italian" -> "Italian"
                    "france", "french" -> "French"
                    "china", "chinese" -> "Chinese"
                    "india", "indian" -> "Indian"
                    "japan", "japanese" -> "Japanese"
                    "mexico", "mexican" -> "Mexican"
                    "spain", "spanish" -> "Spanish"
                    "thailand", "thai" -> "Thai"
                    "vietnam", "vietnamese" -> "Vietnamese"
                    "greece", "greek" -> "Greek"
                    "morocco", "moroccan" -> "Moroccan"
                    "russia", "russian" -> "Russian"
                    "egypt", "egyptian" -> "Egyptian"
                    "ireland", "irish" -> "Irish"
                    "canada", "canadian" -> "Canadian"
                    "netherlands", "dutch" -> "Dutch"
                    "turkey", "turkish" -> "Turkish"
                    "portugal", "portuguese" -> "Portuguese"
                    else -> capitalizedArea // Use capitalized version for other countries
                }
            }
        }
    }
    
    enum class SearchType {
        NAME, INGREDIENT, CATEGORY, AREA
    }
} 
