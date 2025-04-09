package com.example.myrecipeapp.repository

import android.content.Context
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import com.example.myrecipeapp.data.api.TheMealDbApiService
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.model.RecipeDao
import com.example.myrecipeapp.model.RecipeDatabase
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.runBlocking
import okhttp3.OkHttpClient
import okhttp3.mockwebserver.MockWebServer
import org.hamcrest.CoreMatchers.equalTo
import org.hamcrest.CoreMatchers.notNullValue
import org.hamcrest.CoreMatchers.nullValue
import org.hamcrest.MatcherAssert.assertThat
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.shadows.ShadowLog
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import java.util.concurrent.TimeUnit

/**
 * Integration test for CombinedRecipeRepository that tests both local database and network operations
 * Uses Robolectric to run on JVM and MockWebServer to mock network responses
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [30]) // Target Android API level for testing
class CombinedRepositoryTest {

    // JUnit rules
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    // Test components
    private lateinit var mockWebServer: MockWebServer
    private lateinit var apiService: TheMealDbApiService
    private lateinit var recipeDao: RecipeDao
    private lateinit var database: RecipeDatabase
    
    // Repositories
    private lateinit var localRepository: LocalRecipeRepository
    private lateinit var onlineRepository: MockOnlineMealRepository
    private lateinit var combinedRepository: CombinedRecipeRepository

    @Before
    fun setup() {
        // setup Robolectric logging
        ShadowLog.stream = System.out
        
        // Setup in-memory Room database
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = Room.inMemoryDatabaseBuilder(
            context,
            RecipeDatabase::class.java
        ).allowMainThreadQueries() // For simplicity in tests
         .build()
        
        recipeDao = database.recipeDao()
        
        // Setup MockWebServer
        mockWebServer = MockWebServer()
        mockWebServer.start()
        
        // Configure Moshi
        val moshi = Moshi.Builder()
            .add(KotlinJsonAdapterFactory())
            .build()
        
        // Configure OkHttp client
        val okHttpClient = OkHttpClient.Builder()
            .connectTimeout(1, TimeUnit.SECONDS)
            .readTimeout(1, TimeUnit.SECONDS)
            .writeTimeout(1, TimeUnit.SECONDS)
            .build()
        
        // Create Retrofit with MockWebServer URL
        val retrofit = Retrofit.Builder()
            .baseUrl(mockWebServer.url("/"))
            .client(okHttpClient)
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
        
        // Create API service
        apiService = retrofit.create(TheMealDbApiService::class.java)
        
        // Create repositories
        localRepository = LocalRecipeRepository(recipeDao)
        onlineRepository = MockOnlineMealRepository() // Use our mock implementation
        combinedRepository = CombinedRecipeRepository(localRepository, onlineRepository)
    }

    @After
    fun tearDown() {
        // Close database and MockWebServer
        database.close()
        mockWebServer.shutdown()
    }

    @Test
    fun getRecipeByName_whenNotInLocalDb_fetchesFromApiAndCaches() = runBlocking {
        // Prepare mock API response for "Pizza" recipe
        val pizzaRecipe = Recipe(
            id = 53014,
            name = "Pizza Express Margherita",
            category = "Miscellaneous",
            area = "Italian",
            instructions = "Preheat the oven to 230°C. Add the sugar and crumble the fresh yeast into warm water...",
            ingredients = "Plain Flour:150g,Olive Oil:15ml,Salt:1 tsp",
            thumbnailUrl = "https://www.themealdb.com/images/media/meals/x0lk931587671540.jpg",
            tags = "Italian"
        )
        
        // Setup mock repository to return our pizza recipe
        onlineRepository.setPizzaRecipe(pizzaRecipe)
        
        // Verify database is empty initially
        val initialRecipes = localRepository.getAllRecipes().first()
        assertThat("Database should be empty initially", initialRecipes.isEmpty(), equalTo(true))
        
        // Call the repository method - first time should get from API
        val recipe = combinedRepository.getRecipeByName("Pizza").first()
        
        // Verify recipe was found and matches API data
        assertThat("Recipe should be returned", recipe, notNullValue())
        assertThat("Recipe should have correct name", recipe?.name, equalTo("Pizza Express Margherita"))
        assertThat("Recipe should have correct category", recipe?.category, equalTo("Miscellaneous"))
        assertThat("Recipe should have correct area", recipe?.area, equalTo("Italian"))
        
        // Verify recipe was cached in the database
        val cachedRecipes = localRepository.getAllRecipes().first()
        assertThat("Recipe should be cached in database", cachedRecipes.size, equalTo(1))
        assertThat("Cached recipe should match", cachedRecipes[0].name, equalTo("Pizza Express Margherita"))
        
        // Verify API was called
        assertThat("API should have been called", onlineRepository.callCount > 0, equalTo(true))
        
        // Call the repository method again - should use cache
        val cachedRecipe = combinedRepository.getRecipeByName("Pizza").first()
        
        // Verify recipe still found
        assertThat("Recipe should be returned from cache", cachedRecipe, notNullValue())
        assertThat("Cached recipe should have correct name", cachedRecipe?.name, equalTo("Pizza Express Margherita"))
        
        // Verify API call count didn't increase
        assertThat("No additional API calls should be made", onlineRepository.callCount, equalTo(1))
    }

    @Test
    fun getRecipeByName_whenInLocalDb_usesLocalDbOnly() = runBlocking {
        // Prepare a recipe to add to the local database
        val localRecipe = Recipe(
            id = 1,
            name = "Spaghetti Carbonara",
            category = "Pasta",
            area = "Italian",
            instructions = "Boil pasta. Mix eggs, cheese, and pancetta...",
            ingredients = "pasta:200g,eggs:3,cheese:100g,pancetta:150g",
            thumbnailUrl = "https://example.com/carbonara.jpg",
            tags = "pasta,italian"
        )
        
        // Add recipe to local database
        localRepository.addRecipe(localRecipe)
        
        // Verify database has the recipe
        val dbRecipes = localRepository.getAllRecipes().first()
        assertThat("Database should have 1 recipe", dbRecipes.size, equalTo(1))
        
        // Call the repository method - should get from database
        val recipe = combinedRepository.getRecipeByName("Carbonara").first()
        
        // Verify recipe was found and matches local data
        assertThat("Recipe should be returned", recipe, notNullValue())
        assertThat("Recipe should have correct name", recipe?.name, equalTo("Spaghetti Carbonara"))
        
        // Verify no API calls were made
        assertThat("No API calls should be made", onlineRepository.callCount, equalTo(0))
    }

    @Test
    fun getRecipeByName_whenNetworkError_usesLocalDbFallback() = runBlocking {
        // Add a recipe to local database for fallback
        val localRecipe = Recipe(
            id = 1,
            name = "Local Lasagna Recipe",
            category = "Pasta",
            area = "Italian",
            instructions = "Layer pasta, sauce, and cheese...",
            ingredients = "pasta:500g,sauce:300g,cheese:200g",
            thumbnailUrl = "https://example.com/lasagna.jpg",
            tags = "pasta,italian"
        )
        localRepository.addRecipe(localRecipe)
        
        // Configure repository to throw network error
        onlineRepository.setShouldThrowError(true)
        
        // Try to get a recipe that's not in DB by exact name, but contains "Lasagna"
        val recipe = combinedRepository.getRecipeByName("Lasagna").first()
        
        // Should fall back to local recipe that contains "Lasagna" in the name
        assertThat("Should fall back to local recipe", recipe, notNullValue())
        assertThat("Should have correct name", recipe?.name, equalTo("Local Lasagna Recipe"))
    }

    @Test
    fun getRecipeByName_whenNotFoundAnywhere_returnsNull() = runBlocking {
        // Setup mock to return empty list for "NonExistentRecipe"
        onlineRepository.setEmptyResponse("NonExistentRecipe")
        
        // Call the repository method for a recipe that doesn't exist
        val recipe = combinedRepository.getRecipeByName("NonExistentRecipe").first()
        
        // Verify no recipe was found
        assertThat("Recipe should not be found", recipe, nullValue())
        
        // Verify API was called
        assertThat("API should have been called", onlineRepository.callCount > 0, equalTo(true))
    }

    @Test
    fun fetchOnlineRecipes_savesToLocalDatabase() = runBlocking {
        // Configure mock to return Teriyaki recipes
        val teriyakiRecipes = listOf(
            Recipe(
                id = 52772,
                name = "Teriyaki Chicken Casserole",
                category = "Chicken",
                area = "Japanese",
                instructions = "Preheat oven to 350° F...",
                ingredients = "soy sauce:3/4 cup,water:1/2 cup",
                thumbnailUrl = "https://www.themealdb.com/images/media/meals/wvpsxx1468256321.jpg",
                tags = "Meat,Casserole"
            ),
            Recipe(
                id = 52773,
                name = "Honey Teriyaki Salmon",
                category = "Seafood",
                area = "Japanese",
                instructions = "Mix all the ingredients in the Honey Teriyaki Glaze together...",
                ingredients = "Salmon:1 lb,Olive Oil:1 tablespoon",
                thumbnailUrl = "https://www.themealdb.com/images/media/meals/xxyupu1468262513.jpg",
                tags = "Fish,Breakfast,DateNight"
            )
        )
        onlineRepository.setTeriyakiRecipes(teriyakiRecipes)
        
        // Verify database is empty initially
        val initialRecipes = localRepository.getAllRecipes().first()
        assertThat("Database should be empty initially", initialRecipes.isEmpty(), equalTo(true))
        
        // Call the repository method
        val recipes = combinedRepository.fetchOnlineRecipes("Teriyaki")
        
        // Verify recipes were returned
        assertThat("Should return recipes", recipes.size, equalTo(2))
        
        // Verify recipes were cached in the database
        val cachedRecipes = localRepository.getAllRecipes().first()
        assertThat("Recipes should be cached", cachedRecipes.size, equalTo(2))
        
        // Verify API was called
        assertThat("API should have been called", onlineRepository.callCount > 0, equalTo(true))
    }

    /**
     * Mock implementation of OnlineMealRepository that returns predetermined results
     */
    private class MockOnlineMealRepository : OnlineMealRepository() {
        var callCount = 0
        private var pizzaRecipe: Recipe? = null
        private var teriyakiRecipes: List<Recipe> = emptyList()
        private var shouldThrowError = false
        private val emptyQueries = mutableSetOf<String>()
        
        fun setPizzaRecipe(recipe: Recipe) {
            pizzaRecipe = recipe
        }
        
        fun setTeriyakiRecipes(recipes: List<Recipe>) {
            teriyakiRecipes = recipes
        }
        
        fun setShouldThrowError(shouldThrow: Boolean) {
            shouldThrowError = shouldThrow
        }
        
        fun setEmptyResponse(query: String) {
            emptyQueries.add(query)
        }
        
        override fun searchMealsByName(query: String): Flow<List<Recipe>> = flow {
            callCount++
            println("MockOnlineMealRepository: searchMealsByName called with query='$query', count=$callCount")
            
            if (shouldThrowError) {
                throw Exception("Simulated network error")
            }
            
            when {
                query == "Pizza" && pizzaRecipe != null -> {
                    emit(listOf(pizzaRecipe!!))
                }
                query == "Teriyaki" -> {
                    emit(teriyakiRecipes)
                }
                query in emptyQueries -> {
                    emit(emptyList())
                }
                else -> {
                    emit(emptyList())
                }
            }
        }
    }
} 