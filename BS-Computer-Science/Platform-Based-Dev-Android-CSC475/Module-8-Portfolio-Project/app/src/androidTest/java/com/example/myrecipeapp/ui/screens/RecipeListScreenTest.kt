package com.example.myrecipeapp.ui.screens

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.example.myrecipeapp.model.Recipe
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import java.util.concurrent.atomic.AtomicInteger

@RunWith(AndroidJUnit4::class)
@LargeTest
class RecipeListScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    // Not use for now
    // Helper function to create sample recipes
    private fun createSampleRecipes(): List<Recipe> {
        return listOf(
            Recipe(
                id = 1,
                name = "Spaghetti Carbonara",
                category = "Pasta",
                area = "Italian",
                instructions = "Boil pasta...",
                ingredients = "pasta:200g,eggs:3,cheese:100g,pancetta:150g",
                thumbnailUrl = "https://example.com/carbonara.jpg",
                tags = "pasta,italian",
                isFavorite = true,
                mealDbId = ""
            ),
            Recipe(
                id = 2,
                name = "Chocolate Cake",
                category = "Dessert",
                area = "American",
                instructions = "Mix ingredients...",
                ingredients = "flour:2 cups,sugar:1 cup,chocolate:200g,eggs:3",
                thumbnailUrl = "https://example.com/cake.jpg",
                tags = "dessert,chocolate,sweet",
                isFavorite = false,
                mealDbId = ""
            ),
            Recipe(
                id = 3,
                name = "Caesar Salad",
                category = "Side",
                area = "Italian",
                instructions = "Toss ingredients...",
                ingredients = "lettuce:1 head,croutons:1 cup,dressing:1/2 cup",
                thumbnailUrl = "https://example.com/salad.jpg",
                tags = "salad,healthy",
                isFavorite = false,
                mealDbId = ""
            )
        )
    }

    @Test
    fun recipeList_displaysAllRecipes() {
        // mock ViewModel to test the UI
        // test  UI elements exist
        composeTestRule.setContent {
            RecipeListScreen(
                title = "My Recipes",
                searchType = "all",
                onRecipeClicked = {},
                onMenuClicked = {},
                onHomeClicked = {},
                onSearchClicked = {},
                onAddClicked = {},
                onMyRecipesClicked = {},
                onFavoritesClicked = {},
                onMealDbClicked = {},
                currentRoute = "recipeList"
            )
        }
        
        // verify the loading indicator exists (even if hidden)
        composeTestRule.onNodeWithTag("loadingIndicator").assertExists()
        
        // verify add recipe button exists
        composeTestRule.onNodeWithTag("addRecipeButton").assertExists()
    }

    @Test
    fun recipeList_clickAddRecipe_triggersCallback() {
        var addRecipeClicked = false
        
        composeTestRule.setContent {
            RecipeListScreen(
                title = "My Recipes",
                searchType = "all",
                onRecipeClicked = {},
                onMenuClicked = {},
                onHomeClicked = {},
                onSearchClicked = {},
                onAddClicked = { addRecipeClicked = true },
                onMyRecipesClicked = {},
                onFavoritesClicked = {},
                onMealDbClicked = {},
                currentRoute = "recipeList"
            )
        }
        
        // click on add recipe button
        composeTestRule.onNodeWithTag("addRecipeButton").performClick()
        
        // Verify callback was triggered
        assert(addRecipeClicked) { "Add recipe button was clicked but callback wasn't triggered" }
    }

    @Test
    fun recipeList_searchQueryUpdatesUI() {
        composeTestRule.setContent {
            RecipeListScreen(
                title = "Search Recipes",
                searchType = "search",
                initialQuery = "pasta",
                onRecipeClicked = {},
                onMenuClicked = {},
                onHomeClicked = {},
                onSearchClicked = {},
                onAddClicked = {},
                onMyRecipesClicked = {},
                onFavoritesClicked = {},
                onMealDbClicked = {},
                currentRoute = "search"
            )
        }
        
        // verify search field has query
        composeTestRule.onNode(hasText("pasta")).assertExists()
    }

    @Test
    fun recipeList_titleIsDisplayed() {
        val testTitle = "Custom Recipe Title"
        
        composeTestRule.setContent {
            RecipeListScreen(
                title = testTitle,
                searchType = "all",
                onRecipeClicked = {},
                onMenuClicked = {},
                onHomeClicked = {},
                onSearchClicked = {},
                onAddClicked = {},
                onMyRecipesClicked = {},
                onFavoritesClicked = {},
                onMealDbClicked = {},
                currentRoute = "recipeList"
            )
        }
        
        // Verify title is displayed
        composeTestRule.onNodeWithText(testTitle).assertExists()
    }
} 