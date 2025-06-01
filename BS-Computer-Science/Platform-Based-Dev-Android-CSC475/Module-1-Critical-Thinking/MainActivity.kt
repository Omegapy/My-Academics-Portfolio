/*==================================================================================================
    Program Name: Simple Hello Android App
    Author: Alexander Ricciardi
    Date: 02/14/2025

    Requirement: Kotlin

    Program Description:
    This is a simple Hello Android Application written in Kotlin.
    It displays a simple animation where a TextView ("Hello Android!") bounces around within
    the screen's boundaries.
    It also provides a toggle button allowing the user to stop and restart the text animation.

    Note:
    The program uses a background thread to run a text animation within an infinite loop.
    This loop updates the TextView's position and, upon hitting a screen boundary the text bounces
    and changes color. This ‘hands-on’ animation approach is implemented for learning purposes,
    it is generally better and good practice to use Android API’s built‑in animation classes
    (like those in AnimationUtils).

    This file contains the main Kotlin source code dictating the logic
    for the bouncing text background animation thread and the toggle button.
==================================================================================================*/

package com.example.helloandriod

import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

// MainActivity extends AppCompatActivity,
// a compatibility class that provided support for older Android versions
class MainActivity : AppCompatActivity() {

    // @Volatile ensures that isAnimating' updates are visible to all threads
    // Controls the animation loop, it if should keep running
    @Volatile
    private var isAnimating = true

    // Background animation thread.
    // It is nullable because it is only created when the animation is running
    private var animationThread: Thread? = null

    // The following variables store the state of the animation so that if it is stopped and
    // then restarted, the animation resumes from the same position, velocity, and color
    private var currentX: Float = 0f      // Current x-coordinate of the TextView
    private var currentY: Float = 0f      // Current y-coordinate of the TextView
    private var currentVx: Float = 5f     // Horizontal velocity (pixels per frame)
    private var currentVy: Float = 5f     // Vertical velocity (pixels per frame)
    private var currentHue: Float = 0f    // Current hue value for the TextView's color (HSV model)

    // onCreate creates the Activity.
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Set content view, the UI from the activity_main.xml layout file
        setContentView(R.layout.activity_main)

        // Layout's views attribute from activity_main.xml layout file
        val container = findViewById<View>(R.id.main)      // The root container (ConstraintLayout)
        val textView = findViewById<TextView>(R.id.bouncingText) // The TextView that will bounce
        // Button to start/stop the animation
        val toggleButton = findViewById<Button>(R.id.toggleButton)

        // Apply window insets to the container to avoid overlap with system UI
        // (such as status bar, navigation bar)
        ViewCompat.setOnApplyWindowInsetsListener(container) { v, insets ->
            // Obtain the insets corresponding to the system bars
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            // Set padding on the container so content is not obscured by system bars
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets  // Return the insets.
        }

        // (Runnable) The container that ensures that the layout has been measured and is ready
        container.post {
            // Initialize the starting position for the animation using the TextView
            currentX = textView.x
            currentY = textView.y
            isAnimating = true
            startAnimationThread() // start the background animation thread
        }

        // Toggle button to start or stop the animation
        toggleButton.setOnClickListener {
            if (isAnimating) {
                isAnimating = false
                animationThread?.interrupt()  // Interrupt the animation thread
                // Update button text (From "Stop Animation" to "Start Animation").
                toggleButton.text = getString(R.string.toggle_button_state1)
            } else {
                // If animation is stopped, start (or restart) it:
                isAnimating = true
                // Update button text (From "Start Animation" to "Stop Animation")
                toggleButton.text = getString(R.string.toggle_button_state2)
                startAnimationThread()    // Start a new animation thread.
            }
        }
    }

    //-------------------------------------------------------------------------------------------

    /**
     * Creates and starts a new background thread that continuously updates the TextView's position
     * and color after bouncing
     */
    private fun startAnimationThread() {
        // TextView attributes from activity_main.xml layout file
        val container = findViewById<View>(R.id.main)
        val textView = findViewById<TextView>(R.id.bouncingText)

        // Dimensions of the container and the TextView.
        val containerWidth = container.width
        val containerHeight = container.height
        val textViewWidth = textView.width
        val textViewHeight = textView.height

        // Computes the maximum allowed x and y coordinates from screen size
        val maxX = containerWidth - textViewWidth
        val maxY = containerHeight - textViewHeight

        // Initialize local variables using the stored velocities and colors
        var x = currentX      // Current x position
        var y = currentY      // Current y position
        var vx = currentVx    // Current x velocity
        var vy = currentVy    // Current y velocity
        var hue = currentHue  // Current color hue

        //--- Create the background animation thread
        animationThread = Thread {
            // The animation loop continues as long as isAnimating is true
            // and the thread is not interrupted.
            while (isAnimating && !Thread.currentThread().isInterrupted()) {
                // Update the position of the TextView by adding the velocity
                x += vx
                y += vy

                // Variable to track whether the TextView has hit a boundary (bounced)
                var bounced = false

                // Check horizontal boundaries:
                if (x < 0) {
                    // If the TextView goes past the left edge:
                    x = 0f       // Clamp position to the edge.
                    vx = -vx     // Reverse the horizontal velocity.
                    bounced = true
                } else if (x > maxX) {
                    // If the TextView goes past the right edge:
                    x = maxX.toFloat() // Clamp to right edge
                    vx = -vx           // Reverse horizontal velocity
                    bounced = true
                }

                // Check vertical boundaries:
                if (y < 0) {
                    // If the TextView goes above the top edge:
                    y = 0f      // Clamp to the top
                    vy = -vy    // Reverse the vertical velocity
                    bounced = true
                } else if (y > maxY) {
                    // If the TextView goes below the bottom edge:
                    y = maxY.toFloat() // Clamp to the bottom
                    vy = -vy           // Reverse vertical velocity
                    bounced = true
                }

                // If a bounce occurred, update the hue and calculate a new dark color
                var newColor: Int? = null
                if (bounced) {
                    hue += 30f  // Increment the hue
                    if (hue > 360f) hue -= 360f  // hue value need to stay within 0-360
                    // Saturation is 1 and Value (brightness) is set to 0.4 creating a dark color
                    newColor = Color.HSVToColor(floatArrayOf(hue, 1f, 0.4f))
                }

                // Save the updated animation state
                // This is done so the animation can resume
                // from the same position, velocity, and color
                currentX = x
                currentY = y
                currentVx = vx
                currentVy = vy
                currentHue = hue

                // (Runnable) the main thread to update the UI
                // UI updates must occur on the main thread
                runOnUiThread {
                    textView.x = x
                    textView.y = y
                    newColor?.let { textView.setTextColor(it) }
                }

                // Sleep for approximately 16ms for approximately matching 60 frames per second
                try { //
                    Thread.sleep(16)
                } catch (e: InterruptedException) {
                    // If the thread is interrupted when sleeping, restore the interrupted status
                    // and break out of the animation loop to end the thread.
                    Thread.currentThread().interrupt()
                    break
                }
            }
        }
        // Start the animation thread.
        animationThread?.start()
    }

    //-------------------------------------------------------------------------------------------

    // When the activity is destroyed, ensure that the background thread (stop the animation)
    // is stopped and destroyed
    override fun onDestroy() {
        isAnimating = false
        animationThread?.interrupt()   // Interrupt the animation thread
        super.onDestroy()              // Destroy
    }

    //-------------------------------------------------------------------------------------------
}
