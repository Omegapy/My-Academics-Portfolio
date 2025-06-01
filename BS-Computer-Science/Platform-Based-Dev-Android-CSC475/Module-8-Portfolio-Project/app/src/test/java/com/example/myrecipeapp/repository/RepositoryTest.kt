package com.example.myrecipeapp.repository

import com.example.myrecipeapp.model.Recipe
import org.junit.Test
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Before
import org.junit.runner.RunWith
import org.junit.runners.JUnit4
import java.io.IOException
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

/**
 * repository layer test suite:
 * - Basic CRUD operations
 * - Search and filter functionality
 * - Cache implementation
 * - Error handling and recovery
 * - Concurrency scenarios
 * - Edge cases
 */
@RunWith(JUnit4::class)
class RepositoryTest {
    
    /**
     * repository implementation for testing:
     * - Local data operations
     * - Cache with expiration
     * - Error injection for testing recovery
     * - Simulated network latency
     * - Thread-safety for concurrent operations
     */
    private class EnhancedRepository {
        // Thread safe collections for concurrent access testing
        @Volatile
        private var shouldInjectErrors = false
        
        @Volatile
        private var networkLatencyMs = 0L
        
        private val recipes = mutableListOf<Recipe>()
        
        // cache with expiration time (simulates real repository caching)
        private data class CacheEntry(val recipe: Recipe, val expirationTime: Long)
        private val recipeCache = mutableMapOf<Int, CacheEntry>()
        
        // Track operation statistics for performance testing
        private val cacheHits = AtomicInteger(0)
        private val cacheMisses = AtomicInteger(0)
        
        // Simulate network state
        private var hasNetwork = true
        
        fun setNetworkAvailable(available: Boolean) {
            hasNetwork = available
        }
        
        fun injectErrors(shouldInject: Boolean) {
            shouldInjectErrors = shouldInject
        }
        
        fun setNetworkLatency(latencyMs: Long) {
            networkLatencyMs = latencyMs
        }
        
        fun getCacheStats(): Pair<Int, Int> {
            return Pair(cacheHits.get(), cacheMisses.get())
        }
        
        fun clearCache() {
            recipeCache.clear()
            cacheHits.set(0)
            cacheMisses.set(0)
        }
        
        private fun simulateNetworkLatency() {
            if (networkLatencyMs > 0) {
                Thread.sleep(networkLatencyMs)
            }
        }
        
        private fun simulateErrorIfNeeded() {
            if (shouldInjectErrors) {
                throw IOException("Simulated network error")
            }
        }
        
        fun addRecipe(recipe: Recipe): Result<Long> {
            return try {
                simulateErrorIfNeeded()
                synchronized(recipes) {
                    recipes.add(recipe)
                    // Cache the recipe with 10-minute expiration
                    val expirationTime = System.currentTimeMillis() + (10 * 60 * 1000)
                    recipeCache[recipe.id] = CacheEntry(recipe, expirationTime)
                    Result.success(recipe.id.toLong())
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun addRecipes(recipeList: List<Recipe>): Result<Int> {
            return try {
                simulateErrorIfNeeded()
                synchronized(recipes) {
                    var added = 0
                    for (recipe in recipeList) {
                        recipes.add(recipe)
                        // Cache each recipe with 10-minute expiration
                        val expirationTime = System.currentTimeMillis() + (10 * 60 * 1000)
                        recipeCache[recipe.id] = CacheEntry(recipe, expirationTime)
                        added++
                    }
                    Result.success(added)
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun getRecipeById(id: Int): Result<Recipe?> {
            return try {
                // check cache first with expiration check
                val cachedEntry = recipeCache[id]
                if (cachedEntry != null && System.currentTimeMillis() < cachedEntry.expirationTime) {
                    cacheHits.incrementAndGet()
                    return Result.success(cachedEntry.recipe)
                }
                
                cacheMisses.incrementAndGet()
                
                // Not in cache or expired, get from "database"
                simulateNetworkLatency() // Simulate DB query time
                simulateErrorIfNeeded()
                
                val recipe = synchronized(recipes) {
                    recipes.find { it.id == id }
                }
                
                // add to cache if found with a new expiration time
                if (recipe != null) {
                    val expirationTime = System.currentTimeMillis() + (10 * 60 * 1000)
                    recipeCache[id] = CacheEntry(recipe, expirationTime)
                }
                
                Result.success(recipe)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun getAllRecipes(): Result<List<Recipe>> {
            return try {
                simulateNetworkLatency()
                simulateErrorIfNeeded()
                Result.success(synchronized(recipes) { recipes.toList() })
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun searchRecipes(query: String, limit: Int = Int.MAX_VALUE): Result<List<Recipe>> {
            if (query.isBlank()) {
                return Result.success(emptyList())
            }
            
            return try {
                simulateNetworkLatency()
                simulateErrorIfNeeded()
                
                val results = synchronized(recipes) {
                    recipes.filter { recipe ->
                        recipe.name.contains(query, ignoreCase = true) || 
                        recipe.ingredients.contains(query, ignoreCase = true) ||
                        recipe.category.contains(query, ignoreCase = true) ||
                        recipe.instructions.contains(query, ignoreCase = true)
                    }.take(limit)
                }
                
                Result.success(results)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun getFavoriteRecipes(): Result<List<Recipe>> {
            return try {
                simulateNetworkLatency()
                simulateErrorIfNeeded()
                
                Result.success(synchronized(recipes) {
                    recipes.filter { it.isFavorite }
                })
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun updateRecipe(recipe: Recipe): Result<Boolean> {
            return try {
                simulateNetworkLatency()
                simulateErrorIfNeeded()
                
                synchronized(recipes) {
                    val index = recipes.indexOfFirst { it.id == recipe.id }
                    if (index == -1) return Result.success(false)
                    
                    recipes[index] = recipe
                    // Update cache
                    val expirationTime = System.currentTimeMillis() + (10 * 60 * 1000)
                    recipeCache[recipe.id] = CacheEntry(recipe, expirationTime)
                    Result.success(true)
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun deleteRecipe(id: Int): Result<Boolean> {
            return try {
                simulateNetworkLatency()
                simulateErrorIfNeeded()
                
                synchronized(recipes) {
                    val index = recipes.indexOfFirst { it.id == id }
                    if (index == -1) return Result.success(false)
                    
                    recipes.removeAt(index)
                    // Remove from cache
                    recipeCache.remove(id)
                    Result.success(true)
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
        
        fun searchOnlineRecipes(query: String): Result<List<Recipe>> {
            // Simulate online search with fallback to local
            if (!hasNetwork) {
                // Fallback to local search when offline
                return searchRecipes(query)
            }
            
            return try {
                simulateNetworkLatency()
                simulateErrorIfNeeded()
                
                val searchResult = searchRecipes(query)
                if (searchResult.isSuccess) {
                    // transform to simulate online results
                    Result.success(searchResult.getOrNull()?.map { 
                        it.copy(name = "Online: ${it.name}")
                    } ?: emptyList())
                } else {
                    searchResult
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }
    
    private lateinit var repository: EnhancedRepository
    
    // test data generation
    private fun createTestRecipes(count: Int): List<Recipe> {
        val categories = listOf("Appetizer", "Main Course", "Dessert", "Breakfast", "Snack")
        val areas = listOf("Italian", "Mexican", "American", "Chinese", "Indian", "French")
        
        return (1..count).map { i ->
            Recipe(
                id = i,
                name = "Recipe $i",
                category = categories[i % categories.size],
                area = areas[i % areas.size],
                instructions = "Step 1: Do something. Step 2: Do something else for recipe $i.",
                ingredients = "Ingredient ${i}:${i}0g,Ingredient ${i+1}:${i*5}g",
                thumbnailUrl = "http://example.com/image$i.jpg",
                isFavorite = i % 3 == 0 // Every third recipe is a favorite
            )
        }
    }
    
    @Before
    fun setUp() {
        repository = EnhancedRepository()
    }
    
    @Test
    fun testBasicCRUDOperations() {
        // Arrange
        val recipe = Recipe(
            id = 1,
            name = "Test Recipe",
            category = "Test",
            area = "Test Area",
            instructions = "Test instructions",
            ingredients = "Test:1cup",
            thumbnailUrl = "http://example.com/test.jpg",
            isFavorite = false
        )
        
        // Act & Assert - Create
        val addResult = repository.addRecipe(recipe)
        assertTrue(addResult.isSuccess)
        assertEquals(1L, addResult.getOrNull())
        
        // Act & Assert - Read
        val getResult = repository.getRecipeById(1)
        assertTrue(getResult.isSuccess)
        assertEquals(recipe, getResult.getOrNull())
        
        // Act & Assert - Update
        val updatedRecipe = recipe.copy(name = "Updated Recipe", isFavorite = true)
        val updateResult = repository.updateRecipe(updatedRecipe)
        assertTrue(updateResult.isSuccess)
        assertTrue(updateResult.getOrNull() == true)
        
        val getUpdatedResult = repository.getRecipeById(1)
        assertEquals("Updated Recipe", getUpdatedResult.getOrNull()?.name)
        assertTrue(getUpdatedResult.getOrNull()?.isFavorite == true)
        
        // Act & Assert - Delete
        val deleteResult = repository.deleteRecipe(1)
        assertTrue(deleteResult.isSuccess)
        assertTrue(deleteResult.getOrNull() == true)
        
        val getAfterDeleteResult = repository.getRecipeById(1)
        assertNull(getAfterDeleteResult.getOrNull())
    }
    
    @Test
    fun testBulkOperations() {
        // Arrange
        val testRecipes = createTestRecipes(10)
        
        // Act - Add multiple recipes at once
        val addResult = repository.addRecipes(testRecipes)
        
        // Assert
        assertTrue(addResult.isSuccess)
        assertEquals(10, addResult.getOrNull())
        
        // Act - Get all recipes
        val getAllResult = repository.getAllRecipes()
        
        // Assert
        assertTrue(getAllResult.isSuccess)
        assertEquals(10, getAllResult.getOrNull()?.size)
        
        // Act - Get all favorites (every third recipe)
        val getFavoritesResult = repository.getFavoriteRecipes()
        
        // Assert
        assertTrue(getFavoritesResult.isSuccess)
        assertEquals(3, getFavoritesResult.getOrNull()?.size) // Recipes 3, 6, 9 are favorites
    }
    
    @Test
    fun testSearchFiltering() {
        // Arrange - Add 5 recipes
        val testRecipes = createTestRecipes(5)
        repository.addRecipes(testRecipes)
        
        // Set a small network latency
        repository.setNetworkLatency(5L)
        
        // Act - Search by name (should match all)
        val nameSearchResult = repository.searchRecipes("Recipe")
        
        // Assert
        assertTrue("Name search should succeed", nameSearchResult.isSuccess)
        val nameResults = nameSearchResult.getOrNull() ?: emptyList()
        assertTrue("Name search should return results", nameResults.isNotEmpty())
        
        // Act - Search by category (should match some)
        val categorySearchResult = repository.searchRecipes("Dessert")
        
        // Assert
        assertTrue("Category search should succeed", categorySearchResult.isSuccess)
        
        // Act - Search with no matches
        val noMatchResult = repository.searchRecipes("NonExistentTerm")
        
        // Assert
        assertTrue("No match search should succeed", noMatchResult.isSuccess)
        val noMatches = noMatchResult.getOrNull() ?: emptyList()
        assertEquals("No match search should return empty list", 0, noMatches.size)
        
        // reset latency for other tests
        repository.setNetworkLatency(0L)
    }
    
    @Test
    fun testPagination() {
        // Arrange
        repository.addRecipes(createTestRecipes(50))
        
        // Act - Get first page (10 recipes)
        val page1Result = repository.searchRecipes("Recipe", 10)
        
        // Assert
        assertTrue(page1Result.isSuccess)
        assertEquals(10, page1Result.getOrNull()?.size)
    }
    
    @Test
    fun testErrorHandling() {
        // Arrange - Add a recipe
        val recipe = Recipe(
            id = 1, name = "Test", category = "Test", area = "Test",
            instructions = "Test", ingredients = "Test:1cup", isFavorite = false
        )
        repository.addRecipe(recipe)
        
        // Inject errors
        repository.injectErrors(true)
        
        // Try to perform an operation that should fail
        val errorResult = repository.getAllRecipes()
        
        // Verify operation failed
        assertTrue(errorResult.isFailure)
        
        // disable error injection
        repository.injectErrors(false)
        
        // Verify operations work again
        val successResult = repository.getAllRecipes()
        assertTrue(successResult.isSuccess)
    }
    
    @Test
    fun testCaching() {
        // Arrange - Add a recipe and clear stats
        repository.clearCache()
        val recipe = Recipe(
            id = 1, name = "Cache Test", category = "Test", area = "Test",
            instructions = "Test", ingredients = "Test:1cup", isFavorite = false
        )
        repository.addRecipe(recipe)
        
        // Act - First access
        repository.getRecipeById(1)
        
        // Get initial stats to compare
        val (initialHits, initialMisses) = repository.getCacheStats()
        
        // Act - Second access (should be cache hit)
        repository.getRecipeById(1)
        
        // Get final stats
        val (finalHits, finalMisses) = repository.getCacheStats()
        
        // Assert - cache hits should have increased
        assertTrue("Cache hits should increase", finalHits > initialHits)
    }
    
    @Test
    fun testConcurrency() {
        // repository handle concurrent operations safely
        val recipeCount = 100
        val threadCount = 10
        val executor = Executors.newFixedThreadPool(threadCount)
        val latch = CountDownLatch(threadCount)
        
        // Add base data
        repository.addRecipes(createTestRecipes(recipeCount))
        
        // Have multiple threads read and write concurrently
        repeat(threadCount) { threadIndex ->
            executor.submit {
                try {
                    // Each thread does different operations based on its index
                    when (threadIndex % 3) {
                        0 -> {
                            // Add new recipes
                            val newRecipes = (1..10).map { i ->
                                Recipe(
                                    id = recipeCount + threadIndex * 10 + i,
                                    name = "Thread $threadIndex Recipe $i",
                                    category = "Test",
                                    area = "Test",
                                    instructions = "Test",
                                    ingredients = "Test:1cup",
                                    isFavorite = false
                                )
                            }
                            repository.addRecipes(newRecipes)
                        }
                        1 -> {
                            // Read existing recipes
                            for (i in 1..20) {
                                repository.getRecipeById(i)
                            }
                        }
                        2 -> {
                            // Update recipes
                            for (i in 1..5) {
                                val getResult = repository.getRecipeById(i)
                                if (getResult.isSuccess) {
                                    val recipe = getResult.getOrNull()
                                    if (recipe != null) {
                                        repository.updateRecipe(recipe.copy(
                                            name = "Updated by thread $threadIndex"
                                        ))
                                    }
                                }
                            }
                        }
                    }
                } finally {
                    latch.countDown()
                }
            }
        }
        
        // wait for all threads to complete
        latch.await(10, TimeUnit.SECONDS)
        
        // Verify repository is still in consistent state
        val allRecipes = repository.getAllRecipes()
        assertTrue(allRecipes.isSuccess)
        assertTrue((allRecipes.getOrNull()?.size ?: 0) > recipeCount)
    }
    
    @Test
    fun testEdgeCases() {
        // Test empty repository
        val emptyResult = repository.getAllRecipes()
        assertTrue(emptyResult.isSuccess)
        assertTrue(emptyResult.getOrNull()?.isEmpty() == true)
        
        // Test null/blank search
        val blankSearchResult = repository.searchRecipes("")
        assertTrue(blankSearchResult.isSuccess)
        assertTrue(blankSearchResult.getOrNull()?.isEmpty() == true)
        
        // Test non-existent IDs
        val nonExistentResult = repository.getRecipeById(999)
        assertTrue(nonExistentResult.isSuccess)
        assertNull(nonExistentResult.getOrNull())
        
        // Test deleting non-existent item
        val deleteResult = repository.deleteRecipe(999)
        assertTrue(deleteResult.isSuccess)
        assertFalse(deleteResult.getOrNull() == true)
    }
    
    @Test
    fun testOfflineFallback() {
        // Arrange
        val testRecipes = createTestRecipes(5)
        repository.addRecipes(testRecipes)
        
        // Act - Online search
        val onlineResult = repository.searchOnlineRecipes("Recipe")
        
        // Switch to offline
        repository.setNetworkAvailable(false)
        
        // Act - Offline search (should fall back to local)
        val offlineResult = repository.searchOnlineRecipes("Recipe")
        
        // Assert
        assertTrue(onlineResult.isSuccess)
        assertTrue(offlineResult.isSuccess)
        
        // Online results should have "Online:" prefix
        val onlineRecipes = onlineResult.getOrNull() ?: emptyList()
        val offlineRecipes = offlineResult.getOrNull() ?: emptyList()
        
        assertTrue(onlineRecipes.isNotEmpty())
        assertTrue(offlineRecipes.isNotEmpty())
        
        // Verify formats
        for (recipe in onlineRecipes) {
            assertTrue(recipe.name.startsWith("Online:"))
        }
        
        for (recipe in offlineRecipes) {
            assertFalse(recipe.name.startsWith("Online:"))
        }
    }
} 