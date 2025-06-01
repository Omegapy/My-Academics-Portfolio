package com.example.myrecipeapp.api

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.example.myrecipeapp.data.api.TheMealDbApiService
import com.example.myrecipeapp.repository.OnlineMealRepository
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import okhttp3.OkHttpClient
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.hamcrest.CoreMatchers.equalTo
import org.hamcrest.CoreMatchers.notNullValue
import org.hamcrest.MatcherAssert.assertThat
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Integration test for TheMealDB API using MockWebServer
 * Tests the Retrofit service, data models (JSON parsing), and repository integration
 */
class TheMealDbApiTest {

    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private lateinit var mockWebServer: MockWebServer
    private lateinit var apiService: TheMealDbApiService
    private lateinit var repository: OnlineMealRepository

    @Before
    fun setup() {
        // Setup MockWebServer
        mockWebServer = MockWebServer()
        mockWebServer.start()

        // Configure Moshi
        val moshi = Moshi.Builder()
            .add(KotlinJsonAdapterFactory())
            .build()

        // configure OkHttp client
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

        // create API service
        apiService = retrofit.create(TheMealDbApiService::class.java)

        // Create custom repository with our API service for testing
        repository = TestOnlineMealRepository(apiService)
    }

    @After
    fun tearDown() {
        mockWebServer.shutdown()
    }

    @Test
    fun searchMealsByName_returnsExpectedMeals() = runBlocking {
        // Prepare mock response
        val mockResponseJson = """
            {
                "meals": [
                    {
                        "idMeal": "52772",
                        "strMeal": "Teriyaki Chicken Casserole",
                        "strCategory": "Chicken",
                        "strArea": "Japanese",
                        "strInstructions": "Preheat oven to 350° F. Spray a 9x13-inch baking pan with non-stick spray.\r\nCombine soy sauce, ½ cup water, brown sugar, ginger and garlic in a small saucepan and cover. Bring to a boil over medium heat. Remove lid and cook for one minute once boiling.\r\nMeanwhile, stir together the corn starch and 2 tablespoons of water in a separate dish until smooth. Once sauce is boiling, add mixture to the saucepan and stir to combine. Cook until the sauce starts to thicken then remove from heat.\r\nPlace the chicken breasts in the prepared pan. Pour one cup of the sauce over top of chicken. Place chicken in oven and bake 35 minutes or until cooked through. Remove from oven and shred chicken in the dish using two forks.\r\n*Meanwhile, steam or cook the vegetables according to package directions.\r\nAdd the cooked vegetables and rice to the casserole dish with the chicken. Add most of the remaining sauce, reserving a bit to drizzle over the top when serving. Gently toss everything together in the casserole dish until combined. Return to oven and cook 15 minutes. Remove from oven and let stand 5 minutes before serving. Drizzle each serving with remaining sauce. Enjoy!",
                        "strMealThumb": "https://www.themealdb.com/images/media/meals/wvpsxx1468256321.jpg",
                        "strTags": "Meat,Casserole",
                        "strYoutube": "https://www.youtube.com/watch?v=4aZr5hZXP_s",
                        "strIngredient1": "soy sauce",
                        "strIngredient2": "water",
                        "strIngredient3": "brown sugar",
                        "strIngredient4": "ground ginger",
                        "strIngredient5": "minced garlic",
                        "strIngredient6": "cornstarch",
                        "strIngredient7": "chicken breasts",
                        "strIngredient8": "stir-fry vegetables",
                        "strIngredient9": "brown rice",
                        "strIngredient10": "",
                        "strIngredient11": "",
                        "strIngredient12": "",
                        "strIngredient13": "",
                        "strIngredient14": "",
                        "strIngredient15": "",
                        "strIngredient16": "",
                        "strIngredient17": "",
                        "strIngredient18": "",
                        "strIngredient19": "",
                        "strIngredient20": "",
                        "strMeasure1": "3/4 cup",
                        "strMeasure2": "1/2 cup",
                        "strMeasure3": "1/4 cup",
                        "strMeasure4": "1/2 teaspoon",
                        "strMeasure5": "1/2 teaspoon",
                        "strMeasure6": "4 Tablespoons",
                        "strMeasure7": "2",
                        "strMeasure8": "1 (12 oz.)",
                        "strMeasure9": "3 cups",
                        "strMeasure10": "",
                        "strMeasure11": "",
                        "strMeasure12": "",
                        "strMeasure13": "",
                        "strMeasure14": "",
                        "strMeasure15": "",
                        "strMeasure16": "",
                        "strMeasure17": "",
                        "strMeasure18": "",
                        "strMeasure19": "",
                        "strMeasure20": "",
                        "strSource": "",
                        "strImageSource": null,
                        "strCreativeCommonsConfirmed": null,
                        "dateModified": null
                    }
                ]
            }
        """.trimIndent()

        // Enqueue the mock response
        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(mockResponseJson)
        )

        // Call the repository method
        val recipes = repository.searchMealsByName("chicken").first()

        // Assert the results
        assertThat(recipes, notNullValue())
        assertThat(recipes.size, equalTo(1))
        
        val recipe = recipes[0]
        assertThat(recipe.name, equalTo("Teriyaki Chicken Casserole"))
        assertThat(recipe.category, equalTo("Chicken"))
        assertThat(recipe.area, equalTo("Japanese"))
        assertThat(recipe.mealDbId, equalTo("52772"))
        assertThat(recipe.thumbnailUrl, equalTo("https://www.themealdb.com/images/media/meals/wvpsxx1468256321.jpg"))
        
        // Verify ingredients were parsed correctly
        assertThat(recipe.ingredients.contains("soy sauce"), equalTo(true))
        assertThat(recipe.ingredients.contains("water"), equalTo(true))
        assertThat(recipe.ingredients.contains("brown sugar"), equalTo(true))
        
        // verify request was made to the correct endpoint
        val request = mockWebServer.takeRequest()
        assertThat(request.path, equalTo("/search.php?s=chicken"))
    }

    @Test
    fun getMealById_returnsExpectedMeal() = runBlocking {
        // Prepare mock response
        val mockResponseJson = """
            {
                "meals": [
                    {
                        "idMeal": "52772",
                        "strMeal": "Teriyaki Chicken Casserole",
                        "strCategory": "Chicken",
                        "strArea": "Japanese",
                        "strInstructions": "Preheat oven to 350° F...",
                        "strMealThumb": "https://www.themealdb.com/images/media/meals/wvpsxx1468256321.jpg",
                        "strTags": "Meat,Casserole",
                        "strYoutube": "https://www.youtube.com/watch?v=4aZr5hZXP_s",
                        "strIngredient1": "soy sauce",
                        "strIngredient2": "water",
                        "strMeasure1": "3/4 cup",
                        "strMeasure2": "1/2 cup"
                    }
                ]
            }
        """.trimIndent()

        // Enqueue the mock response
        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(mockResponseJson)
        )

        // Call the repository method
        val recipe = repository.getMealById("52772").first()

        // Assert the results
        assertThat(recipe, notNullValue())
        assertThat(recipe?.name, equalTo("Teriyaki Chicken Casserole"))
        assertThat(recipe?.mealDbId, equalTo("52772"))

        // Verify request was made to the correct endpoint
        val request = mockWebServer.takeRequest()
        assertThat(request.path, equalTo("/lookup.php?i=52772"))
    }

    @Test
    fun searchMealsByName_emptyResponse_returnsEmptyList() = runBlocking {
        // Prepare empty response
        val mockResponseJson = """
            {
                "meals": null
            }
        """.trimIndent()

        // Enqueue the mock response
        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(mockResponseJson)
        )

        // Call the repository method
        val recipes = repository.searchMealsByName("nonexistent").first()

        // Assert the results
        assertThat(recipes.isEmpty(), equalTo(true))

        // Verify request was made to the correct endpoint
        val request = mockWebServer.takeRequest()
        assertThat(request.path, equalTo("/search.php?s=nonexistent"))
    }

    @Test
    fun searchMealsByName_serverError_returnsEmptyList() = runBlocking {
        // Enqueue a server error response
        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(500)
                .setBody("Internal Server Error")
        )

        // Call the repository method
        val recipes = repository.searchMealsByName("chicken").first()

        // Assert the results - should handle the error and return empty list
        assertThat(recipes.isEmpty(), equalTo(true))
    }

    @Test
    fun searchMealsByName_networkError_returnsEmptyList() = runBlocking {
        // Simulate a network error by shutting down the server
        mockWebServer.shutdown()

        // Call the repository method
        val recipes = repository.searchMealsByName("chicken").first()

        // assert the results - should handle the error and return empty list
        assertThat(recipes.isEmpty(), equalTo(true))
    }

    @Test
    fun getRandomMeal_returnsExpectedMeal() = runBlocking {
        // Prepare mock response
        val mockResponseJson = """
            {
                "meals": [
                    {
                        "idMeal": "52771",
                        "strMeal": "Spicy Arrabiata Penne",
                        "strCategory": "Vegetarian",
                        "strArea": "Italian",
                        "strInstructions": "Bring a large pot of water to a boil...",
                        "strMealThumb": "https://www.themealdb.com/images/media/meals/ustsqw1468250014.jpg",
                        "strTags": "Pasta,Curry",
                        "strYoutube": "https://www.youtube.com/watch?v=1IszT_guI08",
                        "strIngredient1": "penne rigate",
                        "strIngredient2": "olive oil",
                        "strMeasure1": "1 pound",
                        "strMeasure2": "1/4 cup"
                    }
                ]
            }
        """.trimIndent()

        // Enqueue the mock response
        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(mockResponseJson)
        )

        // Call the repository method
        val recipe = repository.getRandomMeal().first()

        // Assert the results
        assertThat(recipe, notNullValue())
        assertThat(recipe?.name, equalTo("Spicy Arrabiata Penne"))
        assertThat(recipe?.category, equalTo("Vegetarian"))
        assertThat(recipe?.area, equalTo("Italian"))

        // Verify request was made to the correct endpoint
        val request = mockWebServer.takeRequest()
        assertThat(request.path, equalTo("/random.php"))
    }

    /**
     * Custom repository for testing that allows injecting the API service
     */
    private class TestOnlineMealRepository(private val testApiService: TheMealDbApiService) : OnlineMealRepository() {
        init {
            // Override the protected apiService property
            val field = this::class.java.superclass.getDeclaredField("apiService")
            field.isAccessible = true
            field.set(this, testApiService)
        }
    }
} 