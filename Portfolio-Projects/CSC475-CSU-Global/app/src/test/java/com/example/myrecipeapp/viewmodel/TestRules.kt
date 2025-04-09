package com.example.myrecipeapp.viewmodel

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.TestCoroutineDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.setMain
import org.junit.rules.TestRule
import org.junit.rules.TestWatcher
import org.junit.runner.Description
import org.junit.runners.model.Statement

/**
 * Test rules for ViewModel testing.
 * Provides rules for LiveData and Coroutines testing.
 */
object TestRules {
    /**
     * Rule for testing LiveData to execute tasks synchronously.
     */
    val instantTaskExecutorRule = InstantTaskExecutorRule()
    
    /**
     * Rule for setting the main dispatcher to a test dispatcher.
     */
    @OptIn(ExperimentalCoroutinesApi::class)
    class MainCoroutineRule : TestWatcher() {
        private val testDispatcher = TestCoroutineDispatcher()
        
        @OptIn(ExperimentalCoroutinesApi::class)
        override fun starting(description: Description?) {
            Dispatchers.setMain(testDispatcher)
        }
        
        override fun finished(description: Description?) {
            Dispatchers.resetMain()
            testDispatcher.cleanupTestCoroutines()
        }
    }
} 