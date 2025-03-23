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
    This file defines the RecipeDatabase data model for recipes
*/

package com.example.myrecipeapp.model

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

/**
 * Room database for storing recipe data in SQLite
 */
@Database(entities = [Recipe::class], version = 1, exportSchema = false)
@TypeConverters(Converters::class)
abstract class RecipeDatabase : RoomDatabase() {
    
    /**
     * Access to the RecipeDao interface for database operations
     * 
     * @return RecipeDao instance for performing CRUD operations on Recipe entities
     */
    abstract fun recipeDao(): RecipeDao
    
    companion object {
        @Volatile
        private var INSTANCE: RecipeDatabase? = null

        //-----------------------------------------------------------------------------

        /**
         * Gets the singleton instance of RecipeDatabase.
         * If the instance doesn't exist, creates a new database instance
         * Also checks if the database is empty and prepopulates it with sample data if needed
         * This only happens once when the app is first launched or if the database is cleared
         *
         * @param context The application context used to create the database
         * @return The singleton RecipeDatabase instance
         */
        fun getInstance(context: Context): RecipeDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    RecipeDatabase::class.java,
                    "recipe_database"
                )
                .fallbackToDestructiveMigration()
                .build()
                
                INSTANCE = instance
                
                // Prepopulate the database if it's empty
                CoroutineScope(Dispatchers.IO).launch {
                    val dao = instance.recipeDao()
                    val recipeCount = dao.getAll().first().isEmpty()
                    if (recipeCount) {
                        prepopulateDatabase(dao)
                    }
                }
                
                instance
            }
        }

        //-----------------------------------------------------------------------------
        
        /**
         * Prepopulates the database with sample recipes.
         * This function is called only once when the database is first created and empty
         * Adds three recipes (Corba, Spaghetti Carbonara, and Chicken Enchilada Casserole)
         * to give users sample data to explore when they first launch the app
         *
         * @param recipeDao The RecipeDao instance used to insert the sample recipes
         */
        private suspend fun prepopulateDatabase(recipeDao: RecipeDao) {
            val sampleRecipes = listOf(
                Recipe(
                    name = "Corba",
                    category = "Side",
                    area = "Turkish",
                    instructions = "Pick through your lentils for any foreign debris, rinse them 2 or 3 times, drain, and set aside. In a large pot over medium-high heat, warm the oil. Add the onions and cook until they are translucent. Add the carrots and cook for another 3 minutes. Add the tomato paste and stir it around for around 1 minute. Now add the cumin, paprika, mint, thyme, black pepper, and red pepper as quickly as you can and stir for 10 seconds to bloom the spices. Immediately add the tomatoes, lentils, broth, and salt. Bring the soup to a (gentle) boil, then turn the heat down to low and let the soup simmer for 30 minutes. Serve with lemon wedges and fresh herbs.",
                    ingredients = "Red Lentils:1 cup,Onion:1 large,Carrot:1 large,Tomato Puree:1 tablespoon,Cumin:2 teaspoons,Paprika:1 teaspoon,Mint:1/2 teaspoon,Thyme:1/2 teaspoon,Black Pepper:1/4 teaspoon,Red Pepper Flakes:1/4 teaspoon,Vegetable Stock:4 cups,Water:1 cup,Salt:1 teaspoon",
                    thumbnailUrl = "https://www.themealdb.com/images/media/meals/58oia61564916529.jpg",
                    tags = "Soup",
                    mealDbId = "52977"
                ),
                Recipe(
                    name = "Spaghetti Carbonara",
                    category = "Pasta",
                    area = "Italian",
                    instructions = "Bring a large pot of water to a boil. Add a generous pinch of salt. Cook spaghetti according to package instructions. Meanwhile, in a large bowl, whisk eggs and cheese until well-combined. In a large skillet over medium heat, cook bacon until crispy. Add garlic and cook until fragrant, about 1 minute. Transfer spaghetti directly to skillet using tongs, along with about 1/2 cup pasta water. Remove from heat. Quickly add egg mixture to pasta, stirring constantly until creamy. Add more pasta water if needed. Season with black pepper and serve immediately with extra cheese.",
                    ingredients = "Spaghetti:350g,Pancetta:200g,Eggs:4 large,Parmesan Cheese:100g,Garlic:2 cloves,Black Pepper:to taste",
                    thumbnailUrl = "https://www.themealdb.com/images/media/meals/llcbn01574260722.jpg",
                    tags = "Pasta,Italian",
                    isFavorite = true,
                    mealDbId = "52982"
                ),
                Recipe(
                    name = "Chicken Enchilada Casserole",
                    category = "Chicken",
                    area = "Mexican",
                    instructions = "Cut each chicken breast in about 3 pieces, so that it cooks faster and put it in a small pot. Pour Enchilada sauce over it and cook covered on low to medium heat until chicken is cooked through, about 20 minutes. No water is needed, the chicken will cook in the Enchilada sauce. Make sure you stir occasionally so that it doesn't stick to the bottom. Remove chicken from the pot and shred with two forks. Preheat oven to 375 F degrees. Start layering the casserole. Start with about ¼ cup of the leftover Enchilada sauce over the bottom of a baking dish. I used a longer baking dish, so that I can put 2 corn tortillas across. Place 2 tortillas on the bottom, top with ⅓ of the chicken and ⅓ of the remaining sauce. Sprinkle with ⅓ of the cheese and repeat starting with 2 more tortillas, then chicken, sauce, cheese. Repeat with last layer with the remaining ingredients. Bake for 20 to 30 minutes uncovered, until bubbly and cheese has melted and started to brown on top. Serve warm.",
                    ingredients = "Enchilada Sauce:14 oz,Chicken Breasts:2,Corn Tortillas:6,Cheddar Cheese:2 cups",
                    thumbnailUrl = "https://www.themealdb.com/images/media/meals/qtuwxu1468233098.jpg",
                    tags = "Casserole,Cheasy,Meat",
                    mealDbId = "52765"
                )
            )
            
            for (recipe in sampleRecipes) {
                recipeDao.insert(recipe)
            }
        }
    }
} 
