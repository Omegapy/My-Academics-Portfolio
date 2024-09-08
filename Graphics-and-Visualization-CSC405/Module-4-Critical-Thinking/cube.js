/*
 Program Name: Rotating 3D Cube 
 Author: Alejandro (Alex) Ricciardi
 Date: 09/08/2024
    
 Program Description: 
    This program creates a simple rotating colored 3D cube using WebGL. 
    The user can rotate the cube along the X, Y, and Z axes and move it up, down, left, and right.
    The user can also pause and restart the rotation while moving the cube.
    This program visits the concepts of transformation in computer graphics, more specifically quaternion rotation and translation. 
*/

"use strict";
// ================================================================================
/*----------------------
|   Global Variables   |
-----------------------*/

// Global variables
var canvas;  // Reference to the HTML canvas element where the cube will be rendered
var gl;      // WebGL context, used to draw and render graphics in the canvas

var numPositions = 36;  // Number of vertices (6 faces * 2 triangles per face * 3 vertices per triangle)
var positions = [];     // Store the cube's vertex positions
var colors = [];        // Store the cube's vertex colors for each face

// Constants for rotation axes
var xAxis = 0;   
var yAxis = 1;   
var zAxis = 2;   
var axis = 0;    // Default rotation axis (initially set to X-axis)

// Control for rotation and animation (pause/restart)
var rotationActive = true;  // Determine if the rotation is active
var animationFrameId;       // Store the requestAnimationFrame ID to control animation (pause/restart)

// Rotation and translation variables
var theta = [0, 0, 0];  // Hold rotation angles for the x, y, and z axes
var thetaLoc;           // Uniform location for the rotation angles in the vertex shader
var translation = [0.0, 0.0];  // Translation offsets for x and y axes (moves the cube)
var translationLoc;     // Uniform location for the translation in the vertex shader


// ================================================================================
/*-------------------
|   Main Function   |
---------------------*/

/**
 * Initializes the WebGL context, shaders, and sets up event listeners for the cube's control.
 */
window.onload = function init() {
    // Get the canvas element by its ID
    canvas = document.getElementById("gl-canvas");

    // ================================================================================
    /*-------------------- 
    |   Initialization   |
    ---------------------*/

    // Initialize the WebGL context for rendering the cube
    gl = canvas.getContext("webgl2");
    if (!gl) {
        alert("WebGL 2.0 isn't available"); // Display an error if WebGL 2.0 is not supported
    }

    // Load and compile the vertex and fragment shaders
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);  // Use the shader program

    // ================================================================================
    /*--------------------
     |   Configuration   |
     ---------------------*/

    // ------------------------------ vertices and colors ----------------------------

    // Define the cube's vertices and colors
    colorCube();

    // ----------------------------------- Viewport ---------------------------------

    // Configure WebGL viewport (visible part of the canvas)
    gl.viewport(0, 0, canvas.width, canvas.height);  // Set the viewport size to match the canvas
    gl.clearColor(0.0, 0.0, 0.0, 1.0);  // Set the background color to black
    // Enable depth testing to handle hidden surfaces behind others
    // without it, when rotating, the facese will overlap
    gl.enable(gl.DEPTH_TEST);  

    // ---------------------------------- Buffers --------------------------------------

    // --- Position buffer
    // Create and bind buffers for vertex positions
    var vBuffer = gl.createBuffer(); // Store the vertex positions in buffer
    // Attaches position buffer to the ARRAY_BUFFER, 
    // which store and manage vertex attribute data (positions, colors, texture coordinates).
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW); // data position to the GPU

    // Link the position buffer to the aPosition attribute in the vertex shader
    var positionLoc = gl.getAttribLocation(program, "aPosition"); // Store and retrives the index location of the aPosition attribute from the compiled shader.
    gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0); // Define the position data format to be processe by WebGL
    gl.enableVertexAttribArray(positionLoc); // Linked point location and aPosition to be used dring rendering

    // --- Color buffer    
    // Create and bind buffers for vertex colors
    var cBuffer = gl.createBuffer(); // Store the colors of the vertices in buffer
    // Attaches color buffer to the ARRAY_BUFFER, 
    // which store and manage vertex attribute data (positions, colors, texture coordinates).
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer); 
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW); // data color to the GPU

    // Link the color buffer to the aColor attribute in the vertex shader
    var colorLoc = gl.getAttribLocation(program, "aColor"); // Store and retrives the location of the aColor attribute from the compiled shader.
    gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0); // Define the colors data format to be processe by WebGL
    gl.enableVertexAttribArray(colorLoc); // Linked point location and color to be used dring rendering

    
    // ---------------------------------- Get Transalation and Rotation  ----------------------

    // Get the uniform locations for the rotation angles and translation in the vertex shader
    // to be use by restart rotation 
    thetaLoc = gl.getUniformLocation(program, "uTheta");
    translationLoc = gl.getUniformLocation(program, "uTranslation");

    // ---------------------------------- Event listeners ----------------------------------

    // --- Rotation buttons
    // Event listeners for rotation buttons (X, Y, Z)
    document.getElementById("xButton").onclick = function () {
        axis = xAxis;  // Set the rotation axis to X
    };
    document.getElementById("yButton").onclick = function () {
        axis = yAxis;  // Set the rotation axis to Y
    };
    document.getElementById("zButton").onclick = function () {
        axis = zAxis;  // Set the rotation axis to Z
    };


    // --- Translation buttons
    // Event listeners for translation buttons (Up, Down, Left, Right)
    document.getElementById("upButton").onclick = function () {
        translation[1] += 0.1; // Move the cube up (increase Y translation)
    };
    document.getElementById("downButton").onclick = function () {
        translation[1] -= 0.1; // Move the cube down (decrease Y translation)
    };
    document.getElementById("rightButton").onclick = function () {
        translation[0] -= 0.1; // Move the cube right (increase X translation)
    };
    document.getElementById("leftButton").onclick = function () {
        translation[0] += 0.1; // Move the cube left (decrease X translation)
    };
   


    // --- Reset button
    // Event listener for reset button to reset rotation and translation
    document.getElementById("resetButton").onclick = function () {
    // Reset rotation angles and translation to the original state
        theta = [0, 0, 0];    // Reset all rotation angles to 0
        translation = [0.0, 0.0]; // Reset translation to the center
            axis = xAxis;  // Reset the rotation axis to X
    };

    // --- Pause and restart rotation buttons
    // Event listener for Stop Rotation button
    document.getElementById("pauseButton").onclick = function () {
        rotationActive = false; // Stop rotation but allow translation
    };
    // Event listener for Restart Rotation button
    document.getElementById("restartButton").onclick = function () {
        if (!rotationActive) {
            rotationActive = true; // Restart rotation
        }
    };

    // ------------------------------------------------------------------------------

    // Start the rendering loop 
    render();
};

// ================================================================================

/**
 * Defines the vertices and colors for each face of the cube.
 * Each face is created using two triangles.
 */
function colorCube() {
    // Define the six faces of the cube, each face is made up of -- two triangles --
    // A quad represent a quadrilateral, which is a four-sided polygon, a rectangle for example
    // in this program the quat a square represent 2 triangles making a face fhe cube
    quad(1, 0, 3, 2, vec4(1.0, 0.0, 0.0, 1));  // Front face - Red
    quad(2, 3, 7, 6, vec4(0.0, 1.0, 0.0, 1.0));  // Right face - Green
    quad(3, 0, 4, 7, vec4(0.0, 0.0, 1.0, 1.0));  // Bottom face - Blue
    quad(6, 5, 1, 2, vec4(1.0, 1.0, 0.0, 1.0));  // Top face - Yellow
    quad(4, 5, 6, 7, vec4(1.0, 0.0, 1.0, 1.0));  // Back face - Pink
    quad(5, 4, 0, 1, vec4(0.0, 1.0, 1.0, 1.0));  // Left face - Cyan
}

// ================================================================================

/**
 * Creates two triangles from a quad (4 vertices) and assigns colors to each face.
 * A quad is a quadrilateral, which is a four-sided polygon, a rectangle for example
 * in this program the quat a square represent 2 triangles making a face fhe cube.
 * 
 * @param {number} a - Index of the first vertex of the quad
 * @param {number} b - Index of the second vertex of the quad
 * @param {number} c - Index of the third vertex of the quad
 * @param {number} d - Index of the fourth vertex of the quad
 * @param {Array} color - The color assigned to the face of the cube
 */
function quad(a, b, c, d, color) {
    // Vertices for the cube (x, y, z, w)
    var vertices = [
    vec4(-0.25, -0.25, 0.25, 1.0),
    vec4(-0.25, 0.25, 0.25, 1.0),
    vec4(0.25, 0.25, 0.25, 1.0),
    vec4(0.25, -0.25, 0.25, 1.0),
    vec4(-0.25, -0.25, -0.25, 1.0),
    vec4(-0.25, 0.25, -0.25, 1.0),
    vec4(0.25, 0.25, -0.25, 1.0),
    vec4(0.25, -0.25, -0.25, 1.0),
    ];

    // Indices to define the two triangles for each face
    var indices = [a, b, c, a, c, d];

    // Push the vertices and colors for each triangle into the buffers
    for (var i = 0; i < indices.length; ++i) {
        positions.push(vertices[indices[i]]);  // Add vertex position
        colors.push(color);  // Add color to the face
    }
}

// ================================================================================

/**
 * Handles the rendering of the cube.
 * Recursive function - creates an animation 
 */
function render() {
    // Clear the canvas and the depth buffer
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Even if rotation is paused, translation should still occur
    if (rotationActive) {
    // Increment the rotation angle for the selected axis
    theta[axis] += 2.0;
    }

    // Send the updated rotation angles and translation values to the vertex shader
    gl.uniform3fv(thetaLoc, theta);
    gl.uniform2fv(translationLoc, translation);

    // Draw the cube (6 faces * 2 triangles per face * 3 vertices per triangle = 36 vertices)
    gl.drawArrays(gl.TRIANGLES, 0, numPositions);

    // recursion case
    // Request another frame for continuous rendering (animation)
    animationFrameId = requestAnimationFrame(render);
}
