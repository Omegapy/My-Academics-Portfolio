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
   This file defines the Category enum class for recipe categorization
   provide categories for recipes
*/


package com.example.myrecipeapp.model

/**
 * Enum for meal categories from TheMealDB.
 */
enum class Category(val displayName: String, val description: String) {
    BEEF("Beef", "Beef-based dishes including steaks, mince, and strips"),
    BREAKFAST("Breakfast", "Morning meals and brunch dishes"),
    CHICKEN("Chicken", "Poultry dishes featuring chicken as the main ingredient"),
    DESSERT("Dessert", "Sweet dishes served after main meals"),
    GOAT("Goat", "Recipes featuring goat meat"),
    LAMB("Lamb", "Dishes made with lamb or mutton"),
    MISCELLANEOUS("Miscellaneous", "Recipes that don't fit into other categories"),
    PASTA("Pasta", "Dishes based on pasta, noodles, and similar foods"),
    PORK("Pork", "Pork-based recipes and dishes"),
    SEAFOOD("Seafood", "Fish and shellfish recipes"),
    SIDE("Side", "Accompaniments and side dishes"),
    STARTER("Starter", "Appetizers and first courses"),
    VEGAN("Vegan", "Plant-based recipes without animal products"),
    VEGETARIAN("Vegetarian", "Dishes without meat but may include dairy or eggs"),
    UNKNOWN("Unknown", "Category not specified");
    
    companion object {
        /**
         * Returns a Category from a string name, ignoring case
         * Returns UNKNOWN if no match is found or if input is null
         */
        fun fromString(categoryName: String?): Category {
            if (categoryName == null || categoryName.isBlank()) return UNKNOWN
            
            return values().find { 
                it.name.equals(categoryName.trim(), ignoreCase = true) || 
                it.displayName.equals(categoryName.trim(), ignoreCase = true) 
            } ?: UNKNOWN
        }
    }
} 
