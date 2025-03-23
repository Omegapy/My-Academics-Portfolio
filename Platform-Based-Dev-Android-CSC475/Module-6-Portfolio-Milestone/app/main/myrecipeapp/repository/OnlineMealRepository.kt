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
MVVM Architecture: REPOSITORY
    This file contains the repository implementation for fetching recipes from TheMealDB API
    mediates between the API data source and ViewModels
*/

package com.example.myrecipeapp.repository

import com.example.myrecipeapp.data.api.TheMealDbApi
import com.example.myrecipeapp.model.Recipe
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.withContext

/**
 * Repository for fetching recipes from TheMealDB API
 */
class OnlineMealRepository {
    private val apiService = TheMealDbApi.apiService

    /**
     * Search for meals by name
     */
    fun searchMealsByName(query: String): Flow<List<Recipe>> = flow {
        try {
            val response = apiService.searchMealsByName(query)
            if (response.isSuccessful) {
                val recipes = response.body()?.meals?.map { it.toRecipe() } ?: emptyList()
                emit(recipes)
            } else {
                emit(emptyList())
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emit(emptyList())
        }
    }.flowOn(Dispatchers.IO)

    //-------------------------------------------------------------------------------------

    /**
     * Get random meal
     */
    fun getRandomMeal(): Flow<Recipe?> = flow {
        try {
            val response = apiService.getRandomMeal()
            if (response.isSuccessful) {
                val recipes = response.body()?.meals?.map { it.toRecipe() } ?: emptyList()
                emit(recipes.firstOrNull())
            } else {
                emit(null)
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emit(null)
        }
    }.flowOn(Dispatchers.IO)

    //-------------------------------------------------------------------------------------

    /**
     * Get meals by first letter
     * not implemented yet
     */
    fun getMealsByFirstLetter(letter: String): Flow<List<Recipe>> = flow {
        try {
            val response = apiService.listMealsByFirstLetter(letter)
            if (response.isSuccessful) {
                val recipes = response.body()?.meals?.map { it.toRecipe() } ?: emptyList()
                emit(recipes)
            } else {
                emit(emptyList())
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emit(emptyList())
        }
    }.flowOn(Dispatchers.IO)

    //-------------------------------------------------------------------------------------

    /**
     * Get meal by ID
     */
    fun getMealById(id: String): Flow<Recipe?> = flow {
        try {
            val response = apiService.getMealById(id)
            if (response.isSuccessful) {
                val recipes = response.body()?.meals?.map { it.toRecipe() } ?: emptyList()
                emit(recipes.firstOrNull())
            } else {
                emit(null)
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emit(null)
        }
    }.flowOn(Dispatchers.IO)

    //-------------------------------------------------------------------------------------

    /**
     * Filter meals by category
     */
    fun getMealsByCategory(category: String): Flow<List<Recipe>> = flow {
        try {
            val response = apiService.filterByCategory(category)
            if (response.isSuccessful) {
                val recipes = response.body()?.meals?.map { it.toRecipe() } ?: emptyList()
                emit(recipes)
            } else {
                emit(emptyList())
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emit(emptyList())
        }
    }.flowOn(Dispatchers.IO)

    //-------------------------------------------------------------------------------------

    /**
     * Filter meals by area/region
     */
    fun getMealsByArea(area: String): Flow<List<Recipe>> = flow {
        try {
            val response = apiService.filterByArea(area)
            if (response.isSuccessful) {
                val recipes = response.body()?.meals?.map { it.toRecipe() } ?: emptyList()
                emit(recipes)
            } else {
                emit(emptyList())
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emit(emptyList())
        }
    }.flowOn(Dispatchers.IO)

    //-------------------------------------------------------------------------------------

    /**
     * Filter meals by main ingredient
     */
    fun getMealsByIngredient(ingredient: String): Flow<List<Recipe>> = flow {
        try {
            val response = apiService.filterByIngredient(ingredient)
            if (response.isSuccessful) {
                val recipes = response.body()?.meals?.map { it.toRecipe() } ?: emptyList()
                emit(recipes)
            } else {
                emit(emptyList())
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emit(emptyList())
        }
    }.flowOn(Dispatchers.IO)

    //-------------------------------------------------------------------------------------

    /**
     * Get all available categories
     */
    suspend fun getCategories(): List<String> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.listCategories()
            if (response.isSuccessful) {
                response.body()?.meals?.mapNotNull { 
                    it.category.takeIf { it.isNotBlank() } 
                }?.distinct() ?: emptyList()
            } else {
                emptyList()
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    //-------------------------------------------------------------------------------------

    /**
     * Get all available areas
     */
    suspend fun getAreas(): List<String> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.listAreas()
            if (response.isSuccessful) {
                response.body()?.meals?.mapNotNull { 
                    it.area.takeIf { it.isNotBlank() } 
                }?.distinct() ?: emptyList()
            } else {
                emptyList()
            }
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    //-------------------------------------------------------------------------------------

    companion object {
        @Volatile
        private var instance: OnlineMealRepository? = null

        fun getInstance(): OnlineMealRepository =
            instance ?: synchronized(this) {
                instance ?: OnlineMealRepository().also { instance = it }
            }
    }

    //-------------------------------------------------------------------------------------
} 
