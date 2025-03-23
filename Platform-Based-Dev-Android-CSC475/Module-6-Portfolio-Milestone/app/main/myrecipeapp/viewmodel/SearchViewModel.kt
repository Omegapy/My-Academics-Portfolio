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
MVVM Architecture: VIEWMODEL
    This file contains the SearchViewModel which manages search functionality and results
*/

package com.example.myrecipeapp.viewmodel

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDatabase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * ViewModel for handling search operations across different recipe sources
 */
class SearchViewModel(application: Application) : AndroidViewModel(application) {
    
    private val database = RecipeDatabase.getInstance(application.applicationContext)
    private val recipeDao = database.recipeDao()
    
    // Store search results
    private val _searchResults = MutableStateFlow<List<Recipe>>(emptyList())
    val searchResults: StateFlow<List<Recipe>> = _searchResults
    
    // Loading state
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading
    
    // Error state
    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error

    //---------------------------------------------------------------------------------------------

    /**
     * Search for recipes based on source type and search parameters
     */
    fun searchRecipes(sourceType: String, searchType: String, query: String) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            try {
                Log.d("SearchViewModel", "Searching: $sourceType, $searchType, query: $query")
                
                when (sourceType) {
                    "my_recipes" -> {
                        // Search local database
                        when (searchType) {
                            "Name" -> {
                                val recipes = withContext(Dispatchers.IO) {
                                    recipeDao.getAll().first()
                                }
                                val filtered = recipes.filter { 
                                    it.name.contains(query, ignoreCase = true) 
                                }
                                Log.d("SearchViewModel", "Found ${filtered.size} recipes by name")
                                _searchResults.value = filtered
                            }
                            "First Letter" -> {
                                if (query.isNotEmpty()) {
                                    val firstChar = query.first().toString()
                                    val recipes = withContext(Dispatchers.IO) {
                                        recipeDao.getAll().first()
                                    }

                                    //-----------------------------------------------------------------------
                                    
                                    // For "First Letter" search, only match recipes where name starts with the query's first character
                                    Log.d("SearchViewModel", "First Letter search with character: $firstChar")
                                    val filtered = recipes.filter { 
                                        it.name.startsWith(firstChar, ignoreCase = true) 
                                    }
                                    Log.d("SearchViewModel", "Found ${filtered.size} recipes starting with '$firstChar'")
                                    _searchResults.value = filtered
                                }
                            }
                            "ID" -> {
                                val id = query.toIntOrNull()
                                if (id != null) {
                                    val recipe = withContext(Dispatchers.IO) {
                                        recipeDao.getById(id)
                                    }
                                    _searchResults.value = listOfNotNull(recipe)
                                } else {
                                    _searchResults.value = emptyList()
                                }
                            }
                            "Category" -> {
                                val recipes = withContext(Dispatchers.IO) {
                                    recipeDao.getAll().first()
                                }

                                //-----------------------------------------------------------------------

                                // For "Category" search, we want to filter where the category STARTS WITH the query
                                Log.d("SearchViewModel", "Category search with query: $query")
                                val filtered = recipes.filter { 
                                    it.category.startsWith(query, ignoreCase = true) 
                                }
                                Log.d("SearchViewModel", "Found ${filtered.size} recipes where category starts with '$query'")
                                _searchResults.value = filtered
                            }
                            "Main Ingredient" -> {
                                val recipes = withContext(Dispatchers.IO) {
                                    recipeDao.getAll().first()
                                }

                                //-----------------------------------------------------------------------

                                // More detailed debugging for ingredient search
                                Log.d("SearchViewModel", "Ingredient search with query: '$query'")
                                Log.d("SearchViewModel", "Found ${recipes.size} total recipes to search through")
                                
                                val filtered = recipes.filter { recipe ->
                                    // Try using the built-in method first
                                    try {
                                        val ingredientsList = recipe.getIngredientsList()
                                        val matchesWithMethod = ingredientsList.any { ingredient ->
                                            ingredient.name.contains(query, ignoreCase = true)
                                        }
                                        
                                        if (matchesWithMethod) {
                                            Log.d("SearchViewModel", "Recipe '${recipe.name}' matches using getIngredientsList()")
                                            return@filter true
                                        }
                                    } catch (e: Exception) {
                                        Log.e("SearchViewModel", "Error using getIngredientsList() for '${recipe.name}': ${e.message}")
                                        // Continue with manual parsing as fallback
                                    }

                                    //-----------------------------------------------------------------------
                                    
                                    // Manual parsing as backup method
                                    try {
                                        // Log the raw ingredients string for debugging
                                        Log.d("SearchViewModel", "Recipe '${recipe.name}' ingredients: '${recipe.ingredients}'")
                                        
                                        // Split ingredients string and check if any ingredient name contains the query
                                        val ingredientsList = recipe.ingredients.split(",")
                                        Log.d("SearchViewModel", "Split into ${ingredientsList.size} ingredients: $ingredientsList")
                                        
                                        val matches = ingredientsList.any { ingredient ->
                                            try {
                                                val parts = ingredient.split(":")
                                                if (parts.isNotEmpty()) {
                                                    val ingredientName = parts[0].trim()
                                                    val doesMatch = ingredientName.contains(query, ignoreCase = true)
                                                    Log.d("SearchViewModel", "Checking if '$ingredientName' contains '$query': $doesMatch")
                                                    doesMatch
                                                } else {
                                                    Log.d("SearchViewModel", "Empty parts after splitting '$ingredient' by colon")
                                                    false
                                                }
                                            } catch (e: Exception) {
                                                Log.e("SearchViewModel", "Error processing ingredient '$ingredient': ${e.message}")
                                                false
                                            }
                                        }
                                        
                                        Log.d("SearchViewModel", "Recipe '${recipe.name}' matches: $matches")
                                        matches
                                    } catch (e: Exception) {
                                        Log.e("SearchViewModel", "Error in manual parsing for '${recipe.name}': ${e.message}")
                                        false
                                    }
                                }
                                
                                Log.d("SearchViewModel", "Found ${filtered.size} recipes containing ingredient '$query'")
                                _searchResults.value = filtered
                            }
                            "Area" -> {
                                val recipes = withContext(Dispatchers.IO) {
                                    recipeDao.getAll().first()
                                }

                                //-----------------------------------------------------------------------
                                
                                // For "Area" search, we want to filter where the area STARTS WITH the query
                                Log.d("SearchViewModel", "Area search with query: $query")
                                val filtered = recipes.filter { 
                                    it.area.startsWith(query, ignoreCase = true) 
                                }
                                Log.d("SearchViewModel", "Found ${filtered.size} recipes where area starts with '$query'")
                                _searchResults.value = filtered
                            }
                            "Random Meals" -> {
                                // Pick 5 random recipes
                                val recipes = withContext(Dispatchers.IO) {
                                    recipeDao.getAll().first()
                                }
                                _searchResults.value = recipes.shuffled().take(5)
                            }
                            else -> {
                                // Default search by name
                                val recipes = withContext(Dispatchers.IO) {
                                    recipeDao.search(query).first()
                                }
                                Log.d("SearchViewModel", "Default search found ${recipes.size} recipes")
                                _searchResults.value = recipes
                            }
                        }
                    }

                    //-----------------------------------------------------------------------

                    "favorite_recipes" -> {
                        // Search favorites
                        when (searchType) {
                            "Name" -> {
                                val favorites = withContext(Dispatchers.IO) {
                                    recipeDao.getFavorites().first()
                                }
                                _searchResults.value = favorites.filter { 
                                    it.name.contains(query, ignoreCase = true) 
                                }
                            }
                            "First Letter" -> {
                                if (query.isNotEmpty()) {
                                    val firstChar = query.first().toString()
                                    val favorites = withContext(Dispatchers.IO) {
                                        recipeDao.getFavorites().first()
                                    }
                                    _searchResults.value = favorites.filter { 
                                        it.name.startsWith(firstChar, ignoreCase = true) 
                                    }
                                }
                            }
                            "ID" -> {
                                val id = query.toIntOrNull()
                                if (id != null) {
                                    val recipe = withContext(Dispatchers.IO) {
                                        recipeDao.getById(id)
                                    }
                                    if (recipe != null && recipe.isFavorite) {
                                        _searchResults.value = listOf(recipe)
                                    } else {
                                        _searchResults.value = emptyList()
                                    }
                                } else {
                                    _searchResults.value = emptyList()
                                }
                            }
                            "Category" -> {
                                val favorites = withContext(Dispatchers.IO) {
                                    recipeDao.getFavorites().first()
                                }

                                //-----------------------------------------------------------------------

                                // For "Category" search, we want to filter where the category STARTS WITH the query
                                Log.d("SearchViewModel", "Category search in favorites with query: $query")
                                val filtered = favorites.filter { 
                                    it.category.startsWith(query, ignoreCase = true) 
                                }
                                Log.d("SearchViewModel", "Found ${filtered.size} favorite recipes where category starts with '$query'")
                                _searchResults.value = filtered
                            }
                            "Main Ingredient" -> {
                                val favorites = withContext(Dispatchers.IO) {
                                    recipeDao.getFavorites().first()
                                }

                                //-----------------------------------------------------------------------
                                
                                // More detailed debugging for ingredient search
                                Log.d("SearchViewModel", "Favorite ingredient search with query: '$query'")
                                Log.d("SearchViewModel", "Found ${favorites.size} total favorite recipes to search through")
                                
                                val filtered = favorites.filter { recipe ->
                                    // Try using the built-in method first
                                    try {
                                        val ingredientsList = recipe.getIngredientsList()
                                        val matchesWithMethod = ingredientsList.any { ingredient ->
                                            ingredient.name.contains(query, ignoreCase = true)
                                        }
                                        
                                        if (matchesWithMethod) {
                                            Log.d("SearchViewModel", "Favorite '${recipe.name}' matches using getIngredientsList()")
                                            return@filter true
                                        }
                                    } catch (e: Exception) {
                                        Log.e("SearchViewModel", "Error using getIngredientsList() for favorite '${recipe.name}': ${e.message}")
                                        // Continue with manual parsing as fallback
                                    }

                                    //-----------------------------------------------------------------------
                                    
                                    // Manual parsing as backup method
                                    try {
                                        // Log the raw ingredients string for debugging
                                        Log.d("SearchViewModel", "Favorite '${recipe.name}' ingredients: '${recipe.ingredients}'")
                                        
                                        // Split ingredients string and check if any ingredient name contains the query
                                        val ingredientsList = recipe.ingredients.split(",")
                                        
                                        val matches = ingredientsList.any { ingredient ->
                                            try {
                                                val parts = ingredient.split(":")
                                                if (parts.isNotEmpty()) {
                                                    val ingredientName = parts[0].trim()
                                                    val doesMatch = ingredientName.contains(query, ignoreCase = true)
                                                    doesMatch
                                                } else {
                                                    false
                                                }
                                            } catch (e: Exception) {
                                                Log.e("SearchViewModel", "Error processing favorite ingredient '$ingredient': ${e.message}")
                                                false
                                            }
                                        }
                                        
                                        matches
                                    } catch (e: Exception) {
                                        Log.e("SearchViewModel", "Error in manual parsing for favorite '${recipe.name}': ${e.message}")
                                        false
                                    }
                                }
                                
                                Log.d("SearchViewModel", "Found ${filtered.size} favorite recipes containing ingredient '$query'")
                                _searchResults.value = filtered
                            }
                            "Area" -> {
                                val favorites = withContext(Dispatchers.IO) {
                                    recipeDao.getFavorites().first()
                                }

                                //-----------------------------------------------------------------------
                                
                                // For "Area" search, we want to filter where the area STARTS WITH the query
                                Log.d("SearchViewModel", "Area search in favorites with query: $query")
                                val filtered = favorites.filter { 
                                    it.area.startsWith(query, ignoreCase = true) 
                                }
                                Log.d("SearchViewModel", "Found ${filtered.size} favorite recipes where area starts with '$query'")
                                _searchResults.value = filtered
                            }
                            "Random Meals" -> {
                                // Pick 5 random favorite recipes
                                val favorites = withContext(Dispatchers.IO) {
                                    recipeDao.getFavorites().first()
                                }
                                _searchResults.value = favorites.shuffled().take(5)
                            }
                            else -> {
                                // Default search all favorites
                                val favorites = withContext(Dispatchers.IO) {
                                    recipeDao.getFavorites().first()
                                }
                                _searchResults.value = favorites 
                            }
                        }
                    }

                    //-----------------------------------------------------------------------

                    "mealdb" -> {
                        // Initialize the API service
                        val apiService = com.example.myrecipeapp.data.api.TheMealDbApi.apiService
                        
                        try {
                            Log.d("SearchViewModel", "Searching TheMealDB with type: $searchType, query: $query")
                            
                            // Convert our search type to match TheMealDB API expectations
                            val response = when (searchType) {
                                "Name" -> apiService.searchMealsByName(query)
                                "Category" -> apiService.filterByCategory(query)
                                "Main Ingredient" -> apiService.filterByIngredient(query)
                                "Area" -> apiService.filterByArea(query)
                                else -> apiService.searchMealsByName(query) // Default to name search
                            }
                            
                            if (response.isSuccessful) {
                                // Convert API results to Recipe objects using the toRecipe() extension function
                                val meals = response.body()?.meals?.map { mealDto ->
                                    mealDto.toRecipe()
                                } ?: emptyList()
                                
                                Log.d("SearchViewModel", "Found ${meals.size} meals from TheMealDB")
                                _searchResults.value = meals
                            } else {
                                Log.e("SearchViewModel", "API error: ${response.code()}")
                                _error.value = "Error searching TheMealDB: ${response.code()}"
                                _searchResults.value = emptyList()
                            }
                        } catch (e: Exception) {
                            Log.e("SearchViewModel", "Exception searching TheMealDB", e)
                            _error.value = "Error accessing TheMealDB: ${e.message}"
                            _searchResults.value = emptyList()
                        }
                    }
                    else -> {
                        // Default to searching all recipes
                        val recipes = withContext(Dispatchers.IO) {
                            recipeDao.search(query).first()
                        }
                        _searchResults.value = recipes
                    }
                }
            } catch (e: Exception) {
                Log.e("SearchViewModel", "Error searching recipes", e)
                _error.value = "Error searching recipes: ${e.message}"
                _searchResults.value = emptyList()
            } finally {
                _isLoading.value = false
            }
        }
    }

    //----------------------------------------------------------------------------------------------

    // Clear search results
    fun clearResults() {
        _searchResults.value = emptyList()
        _error.value = null
    }
    
    // Toggle favorite status of a recipe
    fun toggleFavorite(recipe: Recipe) {
        viewModelScope.launch {
            val updatedRecipe = recipe.copy(isFavorite = !recipe.isFavorite)
            withContext(Dispatchers.IO) {
                recipeDao.update(updatedRecipe)
            }
            
            // Update the list to reflect the change
            _searchResults.value = _searchResults.value.map { 
                if (it.id == recipe.id) updatedRecipe else it 
            }
        }
    }

    /**
     * Get a list of available categories in the database for a specific source type
     */
    fun getAvailableCategories(sourceType: String) = viewModelScope.launch {
        try {
            val categoriesSet = mutableSetOf<String>()
            
            when (sourceType) {
                "my_recipes" -> {
                    val recipes = withContext(Dispatchers.IO) {
                        recipeDao.getAll().first()
                    }
                    recipes.forEach { recipe ->
                        if (recipe.category.isNotBlank()) {
                            categoriesSet.add(recipe.category)
                        }
                    }
                }
                "favorite_recipes" -> {
                    val recipes = withContext(Dispatchers.IO) {
                        recipeDao.getFavorites().first()
                    }
                    recipes.forEach { recipe ->
                        if (recipe.category.isNotBlank()) {
                            categoriesSet.add(recipe.category)
                        }
                    }
                }
                // For mealdb, we could fetch categories from the API if needed
                // or use predefined categories
            }
            
            _availableCategories.value = categoriesSet.toList().sorted()
            
        } catch (e: Exception) {
            Log.e("SearchViewModel", "Error fetching categories: ${e.message}")
            _availableCategories.value = emptyList()
        }
    }
    
    // Available categories for UI display
    private val _availableCategories = MutableStateFlow<List<String>>(emptyList())
    val availableCategories: StateFlow<List<String>> = _availableCategories
} 
