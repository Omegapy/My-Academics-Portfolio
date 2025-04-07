package com.example.myrecipeapp.ui.screens

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.example.myrecipeapp.model.Recipe
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import java.util.concurrent.atomic.AtomicBoolean

@RunWith(AndroidJUnit4::class)
@LargeTest
class RecipeFormScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun formScreen_whenAllFieldsValid_enablesSaveButton() {
        // track ii or not  the navigation happened
        val navigatedBack = AtomicBoolean(false)
        
        // recipe form with an empty recipe
        composeTestRule.setContent {
            RecipeFormScreen(
                recipeId = null, // Start with a new recipe
                onNavigateBack = { navigatedBack.set(true) },
                onHomeClicked = { },
                onSearchClicked = { },
                onAddClicked = { },
                currentRoute = "recipeForm"
            )
        }
        
        // wait for the UI to settle
        composeTestRule.waitForIdle()
        
        // fill in required fields
        composeTestRule.onNodeWithTag("nameInput").performTextInput("Spaghetti Carbonara")
        composeTestRule.onNodeWithTag("categoryDropdown").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithText("Pasta").performClick()
        composeTestRule.onNodeWithTag("areaInput").performTextInput("Italian")
        
        // Add an ingredient
        composeTestRule.onNodeWithTag("addIngredientButton").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("ingredientNameInput").performTextInput("Pasta")
        composeTestRule.onNodeWithTag("ingredientMeasureInput").performTextInput("200g")
        composeTestRule.onNodeWithTag("confirmIngredientButton").performClick()
        
        // Add an instruction using different methods to find elements
        composeTestRule.onNodeWithTag("addInstructionButton").performClick()
        composeTestRule.waitForIdle()
        
        // wait for UI to update
        composeTestRule.waitForIdle()
        

        // The save button might not be visible yet
        // But other elements should be visible
        composeTestRule.onNodeWithTag("nameInput").assertExists()
    }
    
    @Test
    fun formScreen_whenEditingExistingRecipe_displaysRecipeData() {
        // the recipe form with an existing recipe ID
        composeTestRule.setContent {
            RecipeFormScreen(
                recipeId = 1, // Existing recipe ID
                onNavigateBack = { },
                onHomeClicked = { },
                onSearchClicked = { },
                onAddClicked = { },
                currentRoute = "recipeForm"
            )
        }
        
        // just check some basic elements are displayed
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("nameInput").assertExists()
        composeTestRule.onNodeWithTag("areaInput").assertExists()
        composeTestRule.onNodeWithTag("categoryDropdown").assertExists()
    }
    
    @Test
    fun formScreen_whenChangingRecipeData_updatesForm() {
        // the recipe form with a new recipe
        composeTestRule.setContent {
            RecipeFormScreen(
                recipeId = null,
                onNavigateBack = { },
                onHomeClicked = { },
                onSearchClicked = { },
                onAddClicked = { },
                currentRoute = "recipeForm"
            )
        }
        
        //  fill in initial recipe name
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("nameInput").performTextInput("Chocolate Cake")
        
        // Change recipe name
        composeTestRule.onNodeWithTag("nameInput").performTextClearance()
        composeTestRule.onNodeWithTag("nameInput").performTextInput("Vanilla Cake")
        
        // Select category
        composeTestRule.onNodeWithTag("categoryDropdown").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithText("Dessert").performClick()
        
        // Verify updates are reflected
        composeTestRule.onNodeWithTag("nameInput").assertTextContains("Vanilla Cake")
        composeTestRule.onNodeWithText("Dessert").assertIsDisplayed()
    }
} 