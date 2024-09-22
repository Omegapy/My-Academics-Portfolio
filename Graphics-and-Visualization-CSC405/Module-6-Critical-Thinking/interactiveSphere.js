/*
 Program Name: Interactive Recursively Approximated Sphere 
 Author: Alejandro (Alex) Ricciardi
 Date: 09/22/2024

 Program Description:
 This program displays an interactive 3D approximated sphere in WebGL.
 The sphere is created by recursively subdividing a tetrahedron.
 Users can control the sphere's radius, rotation (theta and phi angles), 
 and the number of subdivisions using sliders. The program also supports 
 pausing and resuming the rotation.
 The Blinn-Phon model is implemented in the scene.
 The model view with the light components are the one experiencing the rotation, not the sphere.
*/

"use strict";

/**
 * Initializes and runs the program
 * Sets up WebGL, manages user interactions, and renders the rotating sphere, and lighthing.
 */
var interactiveSphere = function() {

    // ----------------------------------------------------------------------
    /*------------------------------ 
    |   Variables Initialization   |
    -------------------------------*/
    // ----------------------------------------------------------------------
    
    // Declare variables for WebGL context, canvas, and shader program
    var canvas; // The HTML canvas where WebGL will render the sphere
    var gl;     // The WebGL context, used to interact with the WebGL API and control rendering
    var program;  // The shader program, which contains the vertex and fragment shaders for rendering
    
    // ------------------------------ Shapes: Sphere-tetrahedron-triangle-vertex  ----------------------------

    // Number of recursive subdivisions of the tetrahedron
    var numTimesToSubdivide = 3;

    // Variables for tracking indices and storing vertex data
    var index = 0;
    var positionsArray = [];  // Store the vertices of the triangles forming the sphere
    var normalsArray = [];    // Store the normals for each vertex

    // Vertices of the initial tetrahedron
    // The variables va, vb, vc, and vd represent the four vertices of a tetrahedron 
    // a tetrahedron is a 3D shape composed of four triangular faces
    var va = vec4(0.0, 0.0, -1.0, 1);     // Vertex A at the back of the tetrahedron
    var vb = vec4(0.0, 0.942809, 0.333333, 1);   // Vertex B at the top of the tetrahedron
    var vc = vec4(-0.816497, -0.471405, 0.333333, 1);   // Vertex C at the lower-left corner
    var vd = vec4(0.816497, -0.471405, 0.333333, 1);    // Vertex C at the lower-left corner

    // ------------------- Pojection - Model view - Transformations - Camera ------------------

    // Parameters for orthographic projection
    var near = -10;  // The near clipping plane
    var far = 10;    // The far clipping plane
    var radius = 1.5;   // Initial radius (distance of the camera from the origin)
    var theta = 0.0;    // Initial horizontal rotation angle
    var phi = 0.0;      // Initial vertical rotation angle

    // Boundaries for the orthographic projection (view volume)
    // the view volume (objects outside this won't be visible)
    var left = -3.0; 
    var right = 3.0;
    var top_bound = 3.0;
    var bottom = -3.0;

    // Matrices for model-view and projection transformations
    var modelViewMatrix, projectionMatrix;
    var modelViewMatrixLoc, projectionMatrixLoc;
    var nMatrix, nMatrixLoc;  // Normal matrix for lighting

    // Camera and view parameters
    var eye;  // Camera position
    var at = vec3(0.0, 0.0, 0.0);  // Look-at point (center of the sphere)
    var up = vec3(0.0, 1.0, 0.0);  // Up direction

    var vBuffer, nBuffer;  // Buffers for storing vertex and normal data
    var colorIndex = 0;     // Index to cycle through material colors

    var rotationPaused = false;  // Control flag for pausing/resuming rotation

    // ------------------------------ Light ----------------------------

    // Arrays to hold lighting properties for each triangle
    var ambientProducts = []; // Store the ambient lighting component for each triangle
    var diffuseProducts = []; // Store the diffuse lighting component for each triangle
    var specularProducts = []; // Store the specular lighting component for each triangle

    // Light source properties
    var lightPosition = vec4(1.0, 1.0, 1.0, 0.0);  // Directional light (w == 0.0)
    var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0);   // Ambient light color
    var lightDiffuse = vec4(1.0, 1.0, 1.0, 1.0);   // Diffuse light color
    var lightSpecular = vec4(1.0, 1.0, 1.0, 1.0);  // Specular light color

    // Shininess coefficient for specular reflection
    var materialShininess = 50.0;

    // Arrays of material properties for ambient, diffuse, and specular lighting
    var materialAmbientArray = [
        vec4(0.0, 0.0, 0.4, 1.0),  // Blue
        vec4(0.4, 0.0, 0.0, 1.0),  // Red
        vec4(0.0, 0.4, 0.0, 1.0),  // Green
        vec4(0.4, 0.4, 0.0, 1.0)   // Yellow
    ];
    var materialDiffuseArray = [
        vec4(0.0, 1.0, 1.0, 1.0),  // Cyan
        vec4(1.0, 0.0, 0.0, 1.0),  // Red
        vec4(0.0, 1.0, 0.0, 1.0),  // Green
        vec4(1.0, 1.0, 0.0, 1.0)   // Yellow
    ];
    var materialSpecularArray = [
        vec4(1.0, 1.0, 1.0, 1.0),  // White (for shininess)
        vec4(1.0, 1.0, 1.0, 1.0),
        vec4(1.0, 1.0, 1.0, 1.0),
        vec4(1.0, 1.0, 1.0, 1.0)
    ];


    // ----------------------------------------------------------------------
    /*---------------
    |   Functions   |
    ----------------*/
    // ----------------------------------------------------------------------

    // ------------------------------ Triangle ----------------------------
    /**
     * Creates a triangle from three vertices and compute its normal
     * Adds the vertex positions and normals to the respective arrays, and also
     * calculates lighting properties for each triangle
     * 
     * @param {vec4} a - First vertex of the triangle
     * @param {vec4} b - Second vertex of the triangle
     * @param {vec4} c - Third vertex of the triangle
     */
    function triangle(a, b, c) {
        // Compute the normal vector for the triangle
        var t1 = subtract(b, a);  // Vector from a to b
        var t2 = subtract(c, a);  // Vector from a to c
        var normal = normalize(cross(t2, t1));  // Normal vector (perpendicular to the surface)

        // Store normals for each vertex
        // a normal (or normal vector) is a vector that is perpendicular to the shape, here triangles. 
        // Normals detremine direction of the shape facing a light, it determines how the light interacts with surfaces 
        normalsArray.push(vec4(normal[0], normal[1], normal[2], 0.0)); // Normal for the first vertex of the triangle
        normalsArray.push(vec4(normal[0], normal[1], normal[2], 0.0)); // Normal for the second vertex of the triangle
        normalsArray.push(vec4(normal[0], normal[1], normal[2], 0.0)); // Normal for the third vertex of the triangle

        // Store positions for each vertex
        positionsArray.push(a);
        positionsArray.push(b);
        positionsArray.push(c);

        // Compute the lighting products (ambient, diffuse, specular) for this triangle
        // The lighting products are computed by combining the light's properties (ambient, diffuse, specular)
        // with the material properties of the object (stored in arrays for each color)
        // These products will determine how the surface reflects different types of light
        var ambientProduct = mult(lightAmbient, materialAmbientArray[colorIndex]);
        var diffuseProduct = mult(lightDiffuse, materialDiffuseArray[colorIndex]);
        var specularProduct = mult(lightSpecular, materialSpecularArray[colorIndex]);

        // Store the lighting properties for each triangle
        ambientProducts.push(ambientProduct);
        diffuseProducts.push(diffuseProduct);
        specularProducts.push(specularProduct);

        // Cycle through material colors
        colorIndex = (colorIndex + 1) % 4;

        index += 3;  // Increment the vertex index counter
    }

    // ------------------------------ Triangle subdivisions ----------------------------

    /**
     * Recursively subdivides a triangle into smaller triangles, normalizing the 
     * midpoints. This will create a sphere
     *
     * @param {vec4} a - First vertex of the triangle
     * @param {vec4} b - Second vertex of the triangle
     * @param {vec4} c - Third vertex of the triangle
     * @param {number} count - Number of recursive subdivisions to perform
     */
    function divideTriangle(a, b, c, count) {
        //---- Base case: if count reaches zero, stop recursion and draw the triangle ----
        if (count > 0) { 
            // ---- Recursive case: Subdivide the triangle into smaller triangles ----
            // Compute midpoints of each edge
            var ab = mix(a, b, 0.5);
            var ac = mix(a, c, 0.5);
            var bc = mix(b, c, 0.5);

            // Normalize midpoints to project them onto the sphere surface
            ab = normalize(ab, true);
            ac = normalize(ac, true);
            bc = normalize(bc, true);

            //--- Recursive call: Subdivide the new smaller triangles
            divideTriangle(a, ab, ac, count - 1);
            divideTriangle(ab, b, bc, count - 1);
            divideTriangle(bc, c, ac, count - 1);
            divideTriangle(ab, bc, ac, count - 1);
        } else { 
            //---- Base case: create the final triangle ----
            triangle(a, b, c);
        }
    }

    // ------------------------------ tetrahedron division to triangles ----------------------
    /**
     * Takes the four vertices of a tetrahedron and subdivides its faces recursively
     * to approximate a sphere shape.
     * A tetrahedron is a 3D shape composed of four triangular faces. 
     * 
     *
     * The more subdivisions (n), the smoother the resulting sphere becomes. 
     * Each triangular face of the tetrahedron is divided into smaller triangles.
     * 
     * @param {vec4} a - First vertex of the tetrahedron
     * @param {vec4} b - Second vertex of the tetrahedron
     * @param {vec4} c - Third vertex of the tetrahedron
     * @param {vec4} d - Fourth vertex of the tetrahedron
     * @param {number} n - Number of recursive subdivisions to perform
     */
    function tetrahedron(a, b, c, d, n) {
        // Subdivide the first triangular face (a, b, c) of the tetrahedron
        divideTriangle(a, b, c, n);

        // Subdivide the second triangular face (d, c, b)
        divideTriangle(d, c, b, n);

        // Subdivide the third triangular face (a, d, b)
        divideTriangle(a, d, b, n);

        // Subdivide the fourth triangular face (a, c, d)
        divideTriangle(a, c, d, n);
    }


    // ------------------------------ Webgl-geometry-Initialization  ----------------------------
    /**
     * Initializes the WebGL canvas, shaders, and sets up the sphere geometry
     * Binds the buffers for vertex positions and normals, and sets up event 
     * listeners for user interactions through sliders and buttons
     */
    window.onload = function init() {
        canvas = document.getElementById("gl-canvas");  // Get the WebGL canvas

        // Initialize WebGL 2.0 context
        gl = canvas.getContext('webgl2');
        if (!gl) alert("WebGL 2.0 isn't available");

        // Configure WebGL viewport and clear color
        gl.viewport(0, 0, canvas.width, canvas.height);
        gl.clearColor(0.2, 0.2, 0.2, 1.0);
        gl.enable(gl.DEPTH_TEST);  // Enable depth testing for 3D rendering

        // Initialize shaders and create the shader program
        program = initShaders(gl, "vertex-shader", "fragment-shader");
        if (!program) {
            console.error("Shader program failed to initialize.");
            return;
        }
        gl.useProgram(program);

        // Create the sphere by subdividing a tetrahedron
        tetrahedron(va, vb, vc, vd, numTimesToSubdivide);

        // Create and bind the normal buffer
        nBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW);

        // Bind the normal data to the shader's `aNormal` attribute
        var normalLoc = gl.getAttribLocation(program, "aNormal");
        gl.vertexAttribPointer(normalLoc, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(normalLoc);

        // Create and bind the position buffer
        vBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

        // Bind the vertex positions to the shader's `aPosition` attribute
        var positionLoc = gl.getAttribLocation(program, "aPosition");
        gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionLoc);

        // Get uniform locations for the model-view and projection matrices
        modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix");
        projectionMatrixLoc = gl.getUniformLocation(program, "uProjectionMatrix");
        nMatrixLoc = gl.getUniformLocation(program, "uNormalMatrix");

        // Set light position and shininess in the shader
        gl.uniform4fv(gl.getUniformLocation(program, "uLightPosition"), flatten(lightPosition));
        gl.uniform1f(gl.getUniformLocation(program, "uShininess"), materialShininess);

        // Event listeners for sliders to control radius, theta, phi, and subdivisions
        document.getElementById("radiusSlider").oninput = function(event) {
            radius = parseFloat(event.target.value);  // Update camera radius
        };
        document.getElementById("thetaSlider").oninput = function(event) {
            theta = parseFloat(event.target.value) * Math.PI / 180.0;  // Convert degrees to radians for theta
        };
        document.getElementById("phiSlider").oninput = function(event) {
            phi = parseFloat(event.target.value) * Math.PI / 180.0;  // Convert degrees to radians for phi
        };
        document.getElementById("subdivisionSlider").oninput = function(event) {
            numTimesToSubdivide = parseInt(event.target.value);  // Update the number of subdivisions based on slider input
            
            // Reset buffers and arrays to prepare for re-generating the sphere
            index = 0;                          // Reset the index for tracking vertices
            positionsArray = [];                // Clear the array storing vertex positions
            normalsArray = [];                  // Clear the array storing vertex normals
            ambientProducts = [];               // Clear the array storing ambient lighting products
            diffuseProducts = [];               // Clear the array storing diffuse lighting products
            specularProducts = [];              // Clear the array storing specular lighting products
            colorIndex = 0;                     // Reset color index (if color is determined by face or subdivision)
            
            // Re-generate the tetrahedron with the updated number of subdivisions
            tetrahedron(va, vb, vc, vd, numTimesToSubdivide);
        
            // Upload the new vertex positions to the GPU
            gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);
        
            // Upload the new vertex normals to the GPU
            gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW);
        };
        

        // Event listeners for pausing rotation
        document.getElementById("Pause").onclick = function() {
            rotationPaused = true;  // Pause rotation
        };
        // Event listeners for resuming rotation
        document.getElementById("Resume").onclick = function() {
            rotationPaused = false;  // Resume rotation
        };

        render();  // Start the rendering loop
    };

    // ------------------------------ Rendering  ----------------------------
    /**
     * Recursively renders the scene by clearing the canvas, updating the camera position, 
     * computing projection and model-view matrices, and drawing the sphere.
     * The function is called repeatedly to create a continuous rendering loop, 
     * updating the rotation and lighting properties for each frame.
     */
    function render() {
        // Clear the canvas and depth buffer to prepare for new frame rendering
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        // Update theta and phi angles for horizontal and vertical rotation (if rotation is not paused)
        // This means that the camera is rotation not the sphere
        if (!rotationPaused) {
            theta += 0.01;  // Rotate around the x-axis relative the angle (theta)
            // phi += 0.005;  // Uncomment to enable vertical rotation (phi) - Rotate around the xz-plane

        }


        // Compute the camera's position using spherical coordinates. 
        // The camera's position (eye) is determined by `theta` (horizontal angle), `phi` (vertical angle),
        // and the distance from the origin (`radius`).
        eye = vec3(
            radius * Math.sin(theta) * Math.cos(phi),  // X-coordinate of the camera position
            radius * Math.sin(theta) * Math.sin(phi),  // Y-coordinate of the camera position
            radius * Math.cos(theta)                   // Z-coordinate of the camera position
        );

        // Adjust the size of the orthographic projection view volume based on the radius of the sphere
        var viewSize = 1.5 * radius;
        left = -viewSize;
        right = viewSize;
        bottom = -viewSize;
        top_bound = viewSize;
        near = -7 * radius;  // Set near clipping plane based on the radius
        far = 10 * radius;   // Set far clipping plane based on the radius


        // Compute the model-view matrix using the camera's position (eye), the point to look at (at),
        // and the up direction (up). This matrix transforms object coordinates to camera (eye) coordinates.
        modelViewMatrix = lookAt(eye, at, up);

        // Compute the orthographic projection matrix (view volume) based on the updated view size
        projectionMatrix = ortho(left, right, bottom, top_bound, near, far);

        // Compute the normal matrix for transforming normals, which is the transpose of the inverse of the model-view matrix
        nMatrix = normalMatrix(modelViewMatrix, true);

        // Pass the computed model-view, projection, and normal matrices to the vertex shader
        gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
        gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));
        gl.uniformMatrix3fv(nMatrixLoc, false, flatten(nMatrix));

       
        // Loop through all the triangles of the sphere and render each one.
        // Each triangle has its own ambient, diffuse, and specular lighting properties,
        // which are passed to the shader before rendering the triangle.
        for (var i = 0; i < index; i += 3) {
            var loc = i / 3;  // Calculate the current triangle index
            
            // Pass the ambient lighting product for the current triangle to the shader
            gl.uniform4fv(gl.getUniformLocation(program, "uAmbientProduct"), flatten(ambientProducts[loc]));

            // Pass the diffuse lighting product for the current triangle to the shader
            gl.uniform4fv(gl.getUniformLocation(program, "uDiffuseProduct"), flatten(diffuseProducts[loc]));

            // Pass the specular lighting product for the current triangle to the shader
            gl.uniform4fv(gl.getUniformLocation(program, "uSpecularProduct"), flatten(specularProducts[loc]));

            // Draw the current triangle using the vertex positions and lighting properties
            gl.drawArrays(gl.TRIANGLES, i, 3);
        }

        //--- Recusive call 
        requestAnimationFrame(render);
    }

}();






