/*
 Program Name: 3D Rotating Cube Orthographic Projection 
 Author: Alejandro (Alex) Ricciardi
 Date: 09/15/2024
    
 Program Description: 
    This program displays a 3D rotating cube in WebGL,
    and implement an interactive viewer with orthographic projection
    Users can rotate the cube along the X, Y, and Z axes, stop the rotation, 
    and reset all parameters using buttons, Additionally, the users can resize the cube using a slider.
    Furthermore, the users can control the interactive viewer depth, radius, theta angle, and phi angle with sliders.
*/

"use strict";

/**
 * Initializes and handles the 3D cube with orthographic projection.
 * This function sets up WebGL, manages user interactions, and renders the rotating cube.
 */
var cubeOrthoView = function() {

    // ================================================================================
    /*-------------------- 
    |   Initialization   |
    ---------------------*/

    // Declare variables for WebGL context, canvas, and the number of vertices
    var canvas;  // Canvas element where WebGL will render the cube
    var gl;      // WebGL rendering context

    var numPositions = 36;  // Number of vertices (6 faces * 2 triangles per face * 3 vertices per triangle)

    var cubeSize = 0.5;  // Initial size of the cube

    // Arrays to store the cube's vertex positions and colors
    var positionsArray = [];
    var colorsArray = [];

    var vertices;  // Array to store cube vertices

    // Store initial values to reset the cube
    const initialValues = {
        angleX: 0, // rotation angles around the x-axis
        angleY: 0, // rotation angles around the y-axis
        angleZ: 0, // rotation angles around the z-axis
        radius: 1, // Determines the distance of the camera (eye) from the origin. 
        theta: 0, // Camera Spherical coordinates
        phi: 0, // Camera Spherical coordinates
        // Depth
        near: -1, // view near clipping plane (along the negative z-axis).
        far: 1, // view far clipping plane (along the positive z-axis).
        // boundaries of the viewing volume for orthographic projection, the view cube. 
        // the view cube dictates how the cube is clipped out of the view
        left: -1.0, // view cube left side
        right: 1.0, // view cube right  side
        top: 1.0, // view cube top side 
        bottom: -1.0 // view cube bottom side
    };

    // ================================================================================
    /*--------------------
     |   Configuration   |
     ---------------------*/

    // ------------------------------ vertices position ----------------------------

    /**
     * Generates the vertices of the cube based on the current size (cubeSize).
     * Updates the `vertices` array with the new vertex positions for the cube.
     */
    function generateVertices() {
        vertices = [
            vec4(-cubeSize, -cubeSize,  cubeSize, 1.0),  // Front-bottom-left vertex
            vec4(-cubeSize,  cubeSize,  cubeSize, 1.0),  // Front-top-left vertex
            vec4(cubeSize, cubeSize,  cubeSize, 1.0),    // Front-top-right vertex
            vec4(cubeSize, -cubeSize,  cubeSize, 1.0),   // Front-bottom-right vertex
            vec4(-cubeSize, -cubeSize,  -cubeSize, 1.0), // Back-bottom-left vertex
            vec4(-cubeSize, cubeSize,  -cubeSize, 1.0),  // Back-top-left vertex
            vec4(cubeSize, cubeSize,  -cubeSize, 1.0),   // Back-top-right vertex
            vec4(cubeSize, -cubeSize,  -cubeSize, 1.0),  // Back-bottom-right vertex
        ];
    }

    generateVertices(); // Initial generation of cube vertices

    // ------------------------------ vertices colors ----------------------------

    // Colors for the cube's vertices
    var vertexColors = [
        vec4(0.0, 0.0, 0.0, 1.0),  // black
        vec4(1.0, 0.0, 0.0, 1.0),  // red
        vec4(1.0, 1.0, 0.0, 1.0),  // yellow
        vec4(0.0, 1.0, 0.0, 1.0),  // green
        vec4(0.0, 0.0, 1.0, 1.0),  // blue
        vec4(1.0, 0.0, 1.0, 1.0),  // magenta
        vec4(0.0, 1.0, 1.0, 1.0),  // cyan
        vec4(1.0, 1.0, 1.0, 1.0),  // white
    ];

    // ----------------------------------- Viewport ---------------------------------

    // Projection parameters for the orthographic view
    var near = -1;
    var far = 1;
    var radius = 1;  
    var theta = 0.0; 
    var phi = 0.0;   

    // Orthographic projection bounds
    var left = -1.0, right = 1.0, top = 1.0, bottom = -1.0;

    // Rotation angles for each axis
    var angleX = 0, angleY = 0, angleZ = 0; 
    var currentAxis = null; // Track the current axis of rotation
    var stopRotation = false; // Boolean to stop/start rotation

    // Variables for matrix transformations
    var modelViewMatrix, projectionMatrix;
    var modelViewMatrixLoc, projectionMatrixLoc;
    var eye; // Viewer position
    const at = vec3(0.0, 0.0, 0.0); // Center of the scene
    const up = vec3(0.0, 1.0, 0.0); // Up direction

    // ----------------------------------- Cube ---------------------------------

    /**
     * Creates two triangles from a quadrilateral and assigns colors to each vertex.
     * This is used to form the six faces of the cube.
     *
     * @param {number} a - Index of the first vertex of the quad
     * @param {number} b - Index of the second vertex of the quad
     * @param {number} c - Index of the third vertex of the quad
     * @param {number} d - Index of the fourth vertex of the quad
     */
    function quad(a, b, c, d) {
        positionsArray.push(vertices[a]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[b]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[c]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[a]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[c]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[d]);
        colorsArray.push(vertexColors[a]);
    }

    // ----------------------------------------------------------------------------
    
    /**
     * Defines the cube's six faces using the `quad` function.
     * Resets and fills the `positionsArray` and `colorsArray` with vertex data.
     */
    function colorCube() {
        positionsArray = []; // Reset positions array
        colorsArray = [];    // Reset colors array
        quad(1, 0, 3, 2); // Front face
        quad(2, 3, 7, 6); // Right face
        quad(3, 0, 4, 7); // Bottom face
        quad(6, 5, 1, 2); // Top face
        quad(4, 5, 6, 7); // Back face
        quad(5, 4, 0, 1); // Left face
    }


    // ================================================================================
    /*------------------------- 
    |  WebGL Initialization   |
    --------------------------*/

    /**
     * Initializes WebGL, sets up shaders, and event listeners.
     * This function runs when the page is loaded and runs the WebGL context
     */
    window.onload = function init() {

        // ----------------------------------- canvas ---------------------------------
        // Get the canvas element and initialize WebGL context
        canvas = document.getElementById("gl-canvas");
        gl = canvas.getContext('webgl2');
        if (!gl) alert("WebGL 2.0 isn't available");

        // ----------------------------------- Viewport ---------------------------------
        // Set the viewport and clear color
        gl.viewport(0, 0, canvas.width, canvas.height);
        gl.clearColor(0.0, 0.0, 0.0, 1.0);
        gl.enable(gl.DEPTH_TEST);  // Enable depth testing for proper 3D rendering

        // ----------------------------------- shaders ---------------------------------
        // Load and compile shaders
        var program = initShaders(gl, "vertex-shader", "fragment-shader");
        gl.useProgram(program);  // Use the compiled shader program

        colorCube();  // Generate the cube's faces and colors

        // ----------------------------------- buffers ---------------------------------
        //------- Set up color buffer
        var cBufferId = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, cBufferId);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW);

        var colorLoc = gl.getAttribLocation(program, "aColor");
        gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(colorLoc);

        //------ Set up position buffer
        var vBufferId = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

        var positionLoc = gl.getAttribLocation(program, "aPosition");
        gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionLoc);

        // ----------------------------------- Model and projection matrces ---------------------------------
        // Get uniform locations for the model-view and projection matrices
        modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix");
        projectionMatrixLoc = gl.getUniformLocation(program, "uProjectionMatrix");

        // ----------------------------------- Event listeners ---------------------------------
        //--- View
        // Event listeners for sliders to adjust projection and rotation parameters
        document.getElementById("depthSlider").onchange = function(event) {
            far = event.target.value / 2;
            near = -event.target.value / 2;
        };
        document.getElementById("radiusSlider").onchange = function(event) {
            radius = event.target.value;
        };
        document.getElementById("thetaSlider").onchange = function(event) {
            theta = event.target.value * Math.PI / 180.0; // coverts to radian
        };
        document.getElementById("phiSlider").onchange = function(event) {
            phi = event.target.value * Math.PI / 180.0; // coverts to radian
        };

       //--- Size
        document.getElementById("sizeSlider").onchange = function(event) {
            cubeSize = event.target.value;  // Update cube size
            generateVertices();  // Re-generate cube vertices based on the new size
            colorCube();  // Re-create cube with updated vertices

            // Re-buffer the updated position data
            gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);
        };

        //--- rotation buttons
        document.getElementById("rotateXBtn").onclick = function() {
            currentAxis = 'x';  // Set rotation axis to X
            stopRotation = false;  // Resume rotation
        };
        document.getElementById("rotateYBtn").onclick = function() {
            currentAxis = 'y';  // Set rotation axis to Y
            stopRotation = false;
        };
        document.getElementById("rotateZBtn").onclick = function() {
            currentAxis = 'z';  // Set rotation axis to Z
            stopRotation = false;
        };
        document.getElementById("stopBtn").onclick = function() {
            stopRotation = true;  // Stop rotation
        };

        //--- Reset
        document.getElementById("resetBtn").onclick = function() {
            // Reset angles, radius, and projection parameters
            angleX = initialValues.angleX; // rotation angles around the x-axis
            angleY = initialValues.angleY; // rotation angles around the y-axis
            angleZ = initialValues.angleZ; // rotation angles around the z-axis
            radius = initialValues.radius; // Determines the distance of the camera (eye) from the origin. 
            theta = initialValues.theta; // Camera Spherical coordinates positive z-axis
            phi = initialValues.phi; // Camera Spherical coordinates positive x-axis
            near = initialValues.near; // view near clipping plane (along the negative z-axis).
            far = initialValues.far; // view far clipping plane (along the positive z-axis).

            // Reset cube size
            cubeSize = 0.5;  // Default cube size
            generateVertices();
            colorCube();

            // ----------------------------------- Re-buff ---------------------------------
            // Re-buffer the updated position data
            gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

            // Reset slider values
            document.getElementById("depthSlider").value = 2;
            document.getElementById("radiusSlider").value = 1;
            document.getElementById("thetaSlider").value = 0;
            document.getElementById("phiSlider").value = 0;
            document.getElementById("sizeSlider").value = 0.5;  // Reset size slider

            // Resume rotation and clear the active axis
            stopRotation = false;
            currentAxis = null;
        };

        //----- Start the render loop -------
        render();
    }

    /**
     * Handles the rendering of the cube.
     * Recursive function - creates an animation 
     * It is responsible for continuously redrawing the cube
     * It updates the model-view and projection matrices, applies rotation transformations
     * and renders the cube to the canvas.
     */
    var render = function() {
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);  // Clear the canvas

        // Calculate the viewer's eye position using spherical coordinates
        eye = vec3(radius * Math.sin(phi), radius * Math.sin(theta), radius * Math.cos(phi));
        modelViewMatrix = lookAt(eye, at, up);  // Create the model-view matrix

        // Perform rotation around the active axis
        if (!stopRotation) {
            if (currentAxis === 'x') {
                angleX += 1;
                modelViewMatrix = mult(modelViewMatrix, rotateX(angleX));  // Rotate around X-axis
            } else if (currentAxis === 'y') {
                angleY += 1;
                modelViewMatrix = mult(modelViewMatrix, rotateY(angleY));  // Rotate around Y-axis
            } else if (currentAxis === 'z') {
                angleZ += 1;
                modelViewMatrix = mult(modelViewMatrix, rotateZ(angleZ));  // Rotate around Z-axis
            }
        }

        // Create the orthographic projection matrix
        projectionMatrix = ortho(left, right, bottom, top, near, far);

        // Send the matrices to the shader
        gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
        gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));

        // Draw the cube (6 faces * 2 triangles per face * 3 vertices per triangle = 36 vertices)
        gl.drawArrays(gl.TRIANGLES, 0, numPositions);
        
        // recursion case
        // Request the next frame for continuous animation
        requestAnimationFrame(render);
    }

}();

// Create the perspective projection matrix
projectionMatrix = mat4.perspective(fieldOfView, aspectRatio, near, far);

// Send the matrices to the shader
gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));