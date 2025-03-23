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
MVVM Architecture: VIEW
    This file contains the RecipeFormScreen composable used for adding or editing recipes
 */

package com.example.myrecipeapp.ui.screens

import android.content.Context
import android.net.Uri
import android.util.Log
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.border
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusDirection
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.myrecipeapp.R
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.ui.components.AppFooter
import com.example.myrecipeapp.viewmodel.RecipeViewModel
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.util.UUID

/**
 * Save a content URI image to app's internal storage
 * 
 * @param context Application context
 * @param uri Content URI of the selected image
 * @param filename Optional filename (defaults to a random UUID)
 * @return Path to the saved file or null if saving failed
 */
private fun saveImageToInternalStorage(context: Context, uri: Uri, filename: String = UUID.randomUUID().toString()): String? {
    return try {
        // Create file in app's private directory
        val imageFile = File(context.filesDir, "$filename.jpg")
        
        // Copy image data from content URI to file
        context.contentResolver.openInputStream(uri)?.use { inputStream ->
            FileOutputStream(imageFile).use { outputStream ->
                inputStream.copyTo(outputStream)
            }
        }
        
        // Return the file path for storage
        imageFile.absolutePath
    } catch (e: IOException) {
        Log.e("RecipeFormScreen", "Error saving image", e)
        null
    }
}

//--------------------------------------------------------------------------------------------------

/**
 * Screen for adding a new recipe or editing an existing one
 * form fields for all recipe properties including ingredients and instructions
 * with editable lists and image selection.
 *
 * @param recipeId ID of the recipe to edit (null when adding a new recipe)
 * @param onNavigateBack Callback for navigating back to previous screen
 * @param onHomeClicked Callback for navigating to home screen
 * @param onSearchClicked Callback for opening search
 * @param onAddClicked Callback for navigating to add recipe screen
 * @param currentRoute Current navigation route
 * @param viewModel ViewModel for accessing and manipulating recipe data
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RecipeFormScreen(
    recipeId: Int? = null,
    onNavigateBack: () -> Unit,
    onHomeClicked: () -> Unit,
    onSearchClicked: () -> Unit,
    onAddClicked: () -> Unit,
    currentRoute: String? = null,
    viewModel: RecipeViewModel = viewModel()
) {
    val isEditMode = recipeId != null
    val focusManager = LocalFocusManager.current
    
    // State for delete confirmation dialog
    var showDeleteConfirmation by remember { mutableStateOf(false) }
    
    // Load recipe data if in edit mode
    LaunchedEffect(recipeId) {
        if (recipeId != null) {
            viewModel.getRecipeById(recipeId)
        }
    }
    
    // Get current recipe being edited (if in edit mode)
    val currentRecipe by viewModel.currentRecipe.collectAsState()
    
    // Form state
    var name by remember { mutableStateOf("") }
    var category by remember { mutableStateOf("") }
    var area by remember { mutableStateOf("") }
    var isFavorite by remember { mutableStateOf(false) }
    var expanded by remember { mutableStateOf(false) }
    
    // Thumbnail image state
    var thumbnailUrl by remember { mutableStateOf("") }
    var selectedImageUri by remember { mutableStateOf<Uri?>(null) }
    val context = LocalContext.current
    
    // Image picker launcher
    val imagePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let {
            selectedImageUri = it
            // Save the image to internal storage and use the persistent path
            val savedImagePath = saveImageToInternalStorage(context, it)
            if (savedImagePath != null) {
                thumbnailUrl = savedImagePath
            } else {
                // If saving fails, use the URI temporarily but show an error
                thumbnailUrl = it.toString()
                Toast.makeText(context, "Error saving image. It may not persist after app restart.", Toast.LENGTH_LONG).show()
            }
        }
    }
    
    // State for editable ingredients list
    val ingredientsList = remember { mutableStateListOf<Pair<String, String>>() }
    var newIngredientName by remember { mutableStateOf("") }
    var newIngredientMeasure by remember { mutableStateOf("") }
    var editingIngredientIndex by remember { mutableStateOf(-1) }
    
    // State for editable instructions list
    val instructionsList = remember { mutableStateListOf<String>() }
    var newInstruction by remember { mutableStateOf("") }
    var editingInstructionIndex by remember { mutableStateOf(-1) }
    
    // State for dialogs
    var showIngredientDialog by remember { mutableStateOf(false) }
    var showInstructionDialog by remember { mutableStateOf(false) }
    
    // Populated categories
    val categories = listOf("Breakfast", "Lunch", "Dinner", "Dessert", "Appetizer", "Side", "Pasta", "Chicken", "Beef", "Vegetarian", "Seafood")

    //--------------------------------------------------------------

    // Populate form fields when currentRecipe changes
    LaunchedEffect(currentRecipe) {
        currentRecipe?.let {
            name = it.name
            category = it.category
            area = it.area
            isFavorite = it.isFavorite
            thumbnailUrl = it.thumbnailUrl
            
            // Parse ingredients
            ingredientsList.clear()
            it.getIngredientsList().forEach { ingredient ->
                ingredientsList.add(Pair(ingredient.name, ingredient.measure ?: ""))
            }
            
            // Parse instructions - split by periods or line breaks
            instructionsList.clear()
            val steps = it.instructions.split("\\. |\\.\n|\\n".toRegex())
                .filter { step -> step.isNotBlank() }
                .map { step -> step.trim() }
            instructionsList.addAll(steps)
        }
    }
    
    // Validation state
    val isValid = name.isNotBlank() && ingredientsList.isNotEmpty() && instructionsList.isNotEmpty()
    
    // Delete confirmation dialog
    if (showDeleteConfirmation && currentRecipe != null) {
        AlertDialog(
            onDismissRequest = { showDeleteConfirmation = false },
            title = { Text("Delete Recipe") },
            text = { Text("Are you sure you want to delete '${currentRecipe?.name}'? This action cannot be undone.") },
            confirmButton = {
                Button(
                    onClick = {
                        currentRecipe?.let { viewModel.deleteRecipe(it) }
                        showDeleteConfirmation = false
                        onNavigateBack()
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color.Red,
                        contentColor = Color.White
                    )
                ) {
                    Text("Delete")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDeleteConfirmation = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    //--------------------------------------------------------------

    // Dialog for adding/editing ingredients
    if (showIngredientDialog) {
        AlertDialog(
            onDismissRequest = { 
                showIngredientDialog = false 
                editingIngredientIndex = -1
                newIngredientName = ""
                newIngredientMeasure = ""
            },
            title = { Text(if (editingIngredientIndex >= 0) "Edit Ingredient" else "Add Ingredient") },
            text = {
                Column {
                    OutlinedTextField(
                        value = newIngredientName,
                        onValueChange = { newIngredientName = it },
                        label = { Text("Ingredient") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(
                            capitalization = KeyboardCapitalization.Words,
                            imeAction = ImeAction.Next
                        ),
                        keyboardActions = KeyboardActions(
                            onNext = { focusManager.moveFocus(FocusDirection.Down) }
                        )
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    OutlinedTextField(
                        value = newIngredientMeasure,
                        onValueChange = { newIngredientMeasure = it },
                        label = { Text("Amount") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(
                            imeAction = ImeAction.Done
                        ),
                        keyboardActions = KeyboardActions(
                            onDone = { focusManager.clearFocus() }
                        )
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        if (newIngredientName.isNotBlank()) {
                            if (editingIngredientIndex >= 0) {
                                ingredientsList[editingIngredientIndex] = Pair(newIngredientName, newIngredientMeasure)
                            } else {
                                ingredientsList.add(Pair(newIngredientName, newIngredientMeasure))
                            }
                            showIngredientDialog = false
                            editingIngredientIndex = -1
                            newIngredientName = ""
                            newIngredientMeasure = ""
                        }
                    },
                    enabled = newIngredientName.isNotBlank()
                ) {
                    Text(if (editingIngredientIndex >= 0) "Update" else "Add")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = { 
                        showIngredientDialog = false 
                        editingIngredientIndex = -1
                        newIngredientName = ""
                        newIngredientMeasure = ""
                    }
                ) {
                    Text("Cancel")
                }
            }
        )
    }

    //--------------------------------------------------------------

    // Dialog for adding/editing instructions
    if (showInstructionDialog) {
        AlertDialog(
            onDismissRequest = { 
                showInstructionDialog = false 
                editingInstructionIndex = -1
                newInstruction = ""
            },
            title = { Text(if (editingInstructionIndex >= 0) "Edit Step" else "Add Step") },
            text = {
                OutlinedTextField(
                    value = newInstruction,
                    onValueChange = { newInstruction = it },
                    label = { Text("Instructions") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(120.dp),
                    keyboardOptions = KeyboardOptions(
                        capitalization = KeyboardCapitalization.Sentences
                    )
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        if (newInstruction.isNotBlank()) {
                            if (editingInstructionIndex >= 0) {
                                instructionsList[editingInstructionIndex] = newInstruction
                            } else {
                                instructionsList.add(newInstruction)
                            }
                            showInstructionDialog = false
                            editingInstructionIndex = -1
                            newInstruction = ""
                        }
                    },
                    enabled = newInstruction.isNotBlank()
                ) {
                    Text(if (editingInstructionIndex >= 0) "Update" else "Add")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = { 
                        showInstructionDialog = false 
                        editingInstructionIndex = -1
                        newInstruction = ""
                    }
                ) {
                    Text("Cancel")
                }
            }
        )
    }

    //--------------------------------------------------------------

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        if (isEditMode) "View and Edit Recipe" else "Add New Recipe", 
                        color = if (isSystemInDarkTheme()) Color.White else Color.Black
                    ) 
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            Icons.Default.ArrowBack, 
                            contentDescription = "Back",
                            tint = if (isSystemInDarkTheme()) Color.White else Color.Black
                        )
                    }
                },
                actions = {
                    // Show delete button only in edit mode
                    if (isEditMode) {
                        IconButton(onClick = { showDeleteConfirmation = true }) {
                            Icon(
                                imageVector = Icons.Default.Delete,
                                contentDescription = "Delete Recipe",
                                tint = Color.Gray
                            )
                        }
                    }
                    
                    IconButton(onClick = { isFavorite = !isFavorite }) {
                        Icon(
                            imageVector = if (isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                            contentDescription = if (isFavorite) "Remove from favorites" else "Add to favorites",
                            tint = if (isFavorite) Color(0xFFE91E63) else Color.Gray
                        )
                    }
                }
            )
        },
        bottomBar = {
            AppFooter(
                onHomeClicked = onHomeClicked,
                onSearchClicked = onSearchClicked,
                onAddClicked = onAddClicked,
                currentRoute = currentRoute
            )
        },
        floatingActionButton = {
            if (isValid) {
                FloatingActionButton(
                    onClick = {
                        // Convert ingredients list to formatted string
                        val ingredientsStr = ingredientsList
                            .filter { it.first.isNotBlank() }
                            .joinToString(",") { "${it.first}:${it.second}" }
                        
                        // Join instructions with periods
                        val instructionsStr = instructionsList
                            .filter { it.isNotBlank() }
                            .joinToString(". ") { 
                                // Ensure each instruction ends with a period
                                val step = it.trim()
                                if (step.endsWith(".")) step else "$step."
                            }
                        
                        val recipe = Recipe(
                            id = currentRecipe?.id ?: 0, // 0 for new recipes, existing ID for edits
                            name = name,
                            category = category,
                            area = area,
                            instructions = instructionsStr,
                            ingredients = ingredientsStr,
                            isFavorite = isFavorite,
                            thumbnailUrl = thumbnailUrl,
                            tags = currentRecipe?.tags ?: "",
                            mealDbId = currentRecipe?.mealDbId ?: ""
                        )
                        
                        if (isEditMode) {
                            viewModel.updateRecipe(recipe)
                        } else {
                            viewModel.addRecipe(recipe)
                        }
                        
                        onNavigateBack()
                    },
                    containerColor = Color.DarkGray
                ) {
                    Text("Save", color = Color.White)
                }
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            // Recipe Name
            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                label = { Text("Recipe Name") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                keyboardOptions = KeyboardOptions(
                    capitalization = KeyboardCapitalization.Words,
                    imeAction = ImeAction.Next
                ),
                keyboardActions = KeyboardActions(
                    onNext = { focusManager.moveFocus(FocusDirection.Down) }
                ),
                isError = name.isBlank()
            )
            
            Spacer(modifier = Modifier.height(16.dp))

            //--------------------------------------------------------------

            // Thumbnail image
            Column(
                modifier = Modifier.fillMaxWidth(),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "Recipe Image",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 8.dp)
                )
                
                Box(
                    modifier = Modifier
                        .size(200.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .border(1.dp, Color.Gray, RoundedCornerShape(8.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    if (selectedImageUri != null) {
                        // Display selected image from device
                        AsyncImage(
                            model = selectedImageUri,
                            contentDescription = "Recipe Thumbnail",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Crop
                        )
                    } else if (thumbnailUrl.isNotEmpty()) {
                        // Display image from URL or local file path
                        val imageModel = if (thumbnailUrl.startsWith("/")) {
                            // Local file path
                            File(thumbnailUrl)
                        } else if (thumbnailUrl.startsWith("content://")) {
                            // Content URI
                            Uri.parse(thumbnailUrl)
                        } else {
                            // Remote URL
                            thumbnailUrl
                        }
                        
                        AsyncImage(
                            model = ImageRequest.Builder(context)
                                .data(imageModel)
                                .crossfade(true)
                                .build(),
                            contentDescription = "Recipe Thumbnail",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Crop,
                            error = androidx.compose.ui.res.painterResource(R.drawable.recipe_app_logo)
                        )
                    } else {
                        // Display default logo
                        AsyncImage(
                            model = ImageRequest.Builder(context)
                                .data(R.drawable.recipe_app_logo)
                                .crossfade(true)
                                .build(),
                            contentDescription = "Default Recipe Image",
                            modifier = Modifier
                                .size(100.dp)
                                .padding(16.dp),
                            contentScale = ContentScale.Fit
                        )
                    }
                }
                
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 8.dp),
                    horizontalArrangement = androidx.compose.foundation.layout.Arrangement.Center
                ) {
                    Button(
                        onClick = { imagePickerLauncher.launch("image/*") },
                        modifier = Modifier.padding(end = 8.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Edit,
                            contentDescription = "Change Image",
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Change Image")
                    }
                    
                    Button(
                        onClick = {
                            thumbnailUrl = ""
                            selectedImageUri = null
                        },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = MaterialTheme.colorScheme.errorContainer,
                            contentColor = MaterialTheme.colorScheme.onErrorContainer
                        )
                    ) {
                        Icon(
                            imageVector = Icons.Default.Delete,
                            contentDescription = "Remove Image",
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Remove Image")
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            Divider()
            Spacer(modifier = Modifier.height(16.dp))

            //--------------------------------------------------------------

            // Category dropdown
            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = !expanded }
            ) {
                OutlinedTextField(
                    value = category,
                    onValueChange = { category = it },
                    readOnly = false,
                    label = { Text("Category") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .menuAnchor(),
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                    keyboardActions = KeyboardActions(
                        onNext = { focusManager.moveFocus(FocusDirection.Down) }
                    )
                )
                
                ExposedDropdownMenu(
                    expanded = expanded,
                    onDismissRequest = { expanded = false }
                ) {
                    categories.forEach { option ->
                        DropdownMenuItem(
                            text = { Text(text = option) },
                            onClick = {
                                category = option
                                expanded = false
                                focusManager.moveFocus(FocusDirection.Down)
                            }
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))

            //--------------------------------------------------------------

            // Area (Cuisine)
            OutlinedTextField(
                value = area,
                onValueChange = { area = it },
                label = { Text("Area/Cuisine") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                keyboardOptions = KeyboardOptions(
                    capitalization = KeyboardCapitalization.Words,
                    imeAction = ImeAction.Next
                ),
                keyboardActions = KeyboardActions(
                    onNext = { focusManager.moveFocus(FocusDirection.Down) }
                )
            )
            
            Spacer(modifier = Modifier.height(16.dp))

            //--------------------------------------------------------------

            // Ingredients Section
            Column(
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Ingredients",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.weight(1f)
                    )
                    Button(
                        onClick = { 
                            showIngredientDialog = true 
                            editingIngredientIndex = -1
                            newIngredientName = ""
                            newIngredientMeasure = ""
                        }
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Add Ingredient")
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Add")
                    }
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                if (ingredientsList.isEmpty()) {
                    Text(
                        text = "No ingredients added yet. Click Add to add ingredients.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.error
                    )
                } else {
                    ingredientsList.forEachIndexed { index, ingredient ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(
                                    modifier = Modifier.weight(1f)
                                ) {
                                    Text(
                                        text = ingredient.first,
                                        style = MaterialTheme.typography.titleSmall
                                    )
                                    if (ingredient.second.isNotBlank()) {
                                        Text(
                                            text = ingredient.second,
                                            style = MaterialTheme.typography.bodyMedium
                                        )
                                    }
                                }
                                
                                IconButton(
                                    onClick = {
                                        editingIngredientIndex = index
                                        newIngredientName = ingredient.first
                                        newIngredientMeasure = ingredient.second
                                        showIngredientDialog = true
                                    }
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Edit,
                                        contentDescription = "Edit Ingredient",
                                        tint = if (isSystemInDarkTheme()) Color.White else Color.DarkGray
                                    )
                                }
                                
                                IconButton(
                                    onClick = { ingredientsList.removeAt(index) }
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Delete,
                                        contentDescription = "Remove Ingredient",
                                        tint = if (isSystemInDarkTheme()) Color.White else Color.DarkGray
                                    )
                                }
                            }
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            Divider()
            Spacer(modifier = Modifier.height(16.dp))

            //--------------------------------------------------------------

            // Instructions Section
            Column(
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Instructions",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.weight(1f)
                    )
                    Button(
                        onClick = { 
                            showInstructionDialog = true 
                            editingInstructionIndex = -1
                            newInstruction = ""
                        }
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Add Step")
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Add Step")
                    }
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                if (instructionsList.isEmpty()) {
                    Text(
                        text = "No instructions added yet. Click Add Step to add cooking steps.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.error
                    )
                } else {
                    instructionsList.forEachIndexed { index, instruction ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "${index + 1}.",
                                    style = MaterialTheme.typography.titleSmall,
                                    modifier = Modifier
                                        .padding(end = 8.dp)
                                        .width(24.dp)
                                )
                                
                                Text(
                                    text = instruction,
                                    style = MaterialTheme.typography.bodyMedium,
                                    modifier = Modifier.weight(1f)
                                )
                                
                                IconButton(
                                    onClick = {
                                        editingInstructionIndex = index
                                        newInstruction = instruction
                                        showInstructionDialog = true
                                    }
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Edit,
                                        contentDescription = "Edit Step",
                                        tint = if (isSystemInDarkTheme()) Color.White else Color.DarkGray
                                    )
                                }
                                
                                IconButton(
                                    onClick = { instructionsList.removeAt(index) }
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Delete,
                                        contentDescription = "Remove Step",
                                        tint = if (isSystemInDarkTheme()) Color.White else Color.DarkGray
                                    )
                                }
                            }
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))

            //--------------------------------------------------------------

            // Favorite checkbox
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(
                    checked = isFavorite,
                    onCheckedChange = { isFavorite = it }
                )
                Text("Add to Favorites")
            }

            //--------------------------------------------------------------
            
            // Extra space at bottom for FAB
            Spacer(modifier = Modifier.height(80.dp))
        }
    }
} 
