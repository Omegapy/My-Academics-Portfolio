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
MVVM Architecture: MODEL
    This file defines the API service for TheMealDB
    responsible for retrieving data from external sources
*/

package com.example.myrecipeapp.data.api

import com.example.myrecipeapp.BuildConfig
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import retrofit2.http.GET
import retrofit2.http.Query
import java.util.concurrent.TimeUnit

/**
 * Retrofit service interface for TheMealDB API
 */
interface TheMealDbApiService {
    /**
     * Search meal by name
     * www.themealdb.com/api/json/v2/<Your API Key>/search.php?s=Arrabiata
     */
    @GET("search.php")
    suspend fun searchMealsByName(@Query("s") query: String): Response<MealResponse>

    /**
     * List all meals by first letter
     * www.themealdb.com/api/json/v2/<Your API Key>/search.php?f=a
     */
    @GET("search.php")
    suspend fun listMealsByFirstLetter(@Query("f") letter: String): Response<MealResponse>

    /**
     * Lookup full meal details by id
     * www.themealdb.com/api/json/v2/<Your API Key>/lookup.php?i=52772
     */
    @GET("lookup.php")
    suspend fun getMealById(@Query("i") id: String): Response<MealResponse>

    /**
     * Lookup a single random meal
     * www.themealdb.com/api/json/v2/<Your API Key>/random.php
     */
    @GET("random.php")
    suspend fun getRandomMeal(): Response<MealResponse>

    /**
     * List all meal categories
     * www.themealdb.com/api/json/v2/<Your API Key>/categories.php
     */
    @GET("categories.php")
    suspend fun getCategories(): Response<CategoriesResponse>

    /**
     * List all Categories, Area, Ingredients
     * www.themealdb.com/api/json/v2/<Your API Key>/list.php?c=list
     */
    @GET("list.php")
    suspend fun listCategories(@Query("c") list: String = "list"): Response<MealResponse>

    /**
     * List all Areas
     * www.themealdb.com/api/json/v2/<Your API Key>/list.php?a=list
     */
    @GET("list.php")
    suspend fun listAreas(@Query("a") list: String = "list"): Response<MealResponse>

    /**
     * List all Ingredients
     * www.themealdb.com/api/json/v2/<Your API Key>/list.php?i=list
     */
    @GET("list.php")
    suspend fun listIngredients(@Query("i") list: String = "list"): Response<MealResponse>

    /**
     * Filter by main ingredient
     * www.themealdb.com/api/json/v2/65232507/filter.php?i=chicken_breast
     */
    @GET("filter.php")
    suspend fun filterByIngredient(@Query("i") ingredient: String): Response<MealResponse>

    /**
     * Filter by Category
     * www.themealdb.com/api/json/v2/<Your API Key>/filter.php?c=Seafood
     */
    @GET("filter.php")
    suspend fun filterByCategory(@Query("c") category: String): Response<MealResponse>

    /**
     * Filter by Area
     * www.themealdb.com/api/json/v2/<Your API Key>/filter.php?a=Canadian
     */
    @GET("filter.php")
    suspend fun filterByArea(@Query("a") area: String): Response<MealResponse>
}

//----------------------------------------------------------------------------------------------

/**
 * Object for accessing TheMealDB API
 */
object TheMealDbApi {
    // API key in Gradle file
    private const val BASE_URL = "https://www.themealdb.com/api/json/v2/${BuildConfig.MEAL_DB_API_KEY}/"
    
    // Configure Moshi
    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()
    
    // Configure OkHttp client with logging interceptor
    private val httpClient = OkHttpClient.Builder()
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()
    
    // Create Retrofit instance
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(httpClient)
        .addConverterFactory(MoshiConverterFactory.create(moshi))
        .build()
    
    // Create API service
    val apiService: TheMealDbApiService by lazy {
        retrofit.create(TheMealDbApiService::class.java)
    }
} 
