package com.example.myrecipeapp.util

import android.app.Application
import android.content.Context
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.example.myrecipeapp.model.RecipeDao
import com.example.myrecipeapp.model.RecipeDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.setMain
import org.junit.Before
import org.junit.Rule
import org.junit.rules.TestWatcher
import org.junit.runner.Description
import org.mockito.Mockito
import org.mockito.MockitoAnnotations

/**
 * test class with common setup for view model tests
 */
@OptIn(ExperimentalCoroutinesApi::class)
abstract class SimpleViewModelTest {

    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    @get:Rule
    val mainDispatcherRule = object : TestWatcher() {
        private val testDispatcher = StandardTestDispatcher()
        
        override fun starting(description: Description) {
            Dispatchers.setMain(testDispatcher)
        }
        
        override fun finished(description: Description) {
            Dispatchers.resetMain()
        }
    }
    
    // Common mocks
    protected lateinit var mockApplication: Application
    protected lateinit var mockContext: Context
    protected lateinit var mockDatabase: RecipeDatabase
    protected lateinit var mockRecipeDao: RecipeDao
    
    @Before
    open fun setup() {
        // Create mocks without using Mockito annotations
        mockApplication = Mockito.mock(Application::class.java)
        mockContext = Mockito.mock(Context::class.java)
        mockDatabase = Mockito.mock(RecipeDatabase::class.java)
        mockRecipeDao = Mockito.mock(RecipeDao::class.java)
        
        // Standard setup
        Mockito.`when`(mockApplication.applicationContext).thenReturn(mockContext)
        Mockito.`when`(mockDatabase.recipeDao()).thenReturn(mockRecipeDao)
    }
} 