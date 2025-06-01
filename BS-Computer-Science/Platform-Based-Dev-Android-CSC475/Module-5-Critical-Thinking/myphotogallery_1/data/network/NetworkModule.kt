/*==================================================================================================
    Program Name: My Photo Gallery App
    Author: Alexander Ricciardi
    Date: 03/16/2025

    Requirement:
        Jetpack Compose (2.7.x): UI
        Retrofit (2.9.0): API communication
        OkHttp (4.11.0): HTTP client
        Gson (1.6.0): JSON serialization/deserialization
        Coil (2.50): For asynchronous image loading with Compose integration
        Kotlin Coroutines (1.7.3):
        Navigation Compose (2.7.7): navigation between screens
        Material 3: Material Design components and theming

    Program Description:
    The program is a small Android application that allows a user to browse images from pexels.com
    (a website that provides free stock photos).
        •	When launched, the home page of the app displays
            a browsable list of curated professional photographs selected by Pexels.
        •	Search for specific images using keywords.
        •	View detailed information about each photograph, including photographer credits.
        •	The app User Interface (UI) follows Material Design principles.
==================================================================================================*/

/* Part of MVVM Architecture: MODEL */

package com.example.myphotogallery_1.data.network

import com.example.myphotogallery_1.data.api.PexelsApiService
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 *  Povides Pexels API service and network-related dependencies for the application.
 * 
 * This singleton object configures and initializes the networking components
 */
object NetworkModule {
    
    /**
     * Base URL for the Pexels API.
     * All API requests will be made to endpoints relative to this URL.
     * 
     * MVVM Component: MODEL - Configuration constant
     */
    private const val BASE_URL = "https://api.pexels.com/"
    
    /**
     * Pexels API key
     */
    const val API_KEY = "3ig3SveXZZFVCvugK5KFGFtX2jacR9mW6LwP9gTA8SpU5e2mI9fjF7RO"
    
    /**
     * Create and configure an OkHttpClient object
     * 
     * This client is used by Retrofit to perform
     * the actual HTTP requests
     * 
     * @return OkHttpClient object
     */
    private fun createOkHttpClient(): OkHttpClient {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        
        return OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    //-------------------------------------------------------------------------------------------
    
    /**
     * Create and configure a Retrofit oject
     * 
     * Sets up the Retrofit client with the base URL, HTTP client, and
     * JSON converter for serializing/deserializing requests and responses
     * 
     * @return Retrofit object
     */
    private fun createRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(createOkHttpClient())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    //-------------------------------------------------------------------------------------------
    
    /**
     * Provides an instance of the PexelsApiService interface
     * Creates a Retrofit implementation of the PexelsApiService interface
     */
    val pexelsApiService: PexelsApiService by lazy {
        createRetrofit().create(PexelsApiService::class.java)
    }

    //-------------------------------------------------------------------------------------------
} 