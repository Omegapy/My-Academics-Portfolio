/*
 Program Name: Sierpinski Gasket Vertex 2D
    Author: Alejandro (Alex) Ricciardi
    Date: 08/25/2024
    
    Program Description: 
    The program is a very simple WebGL application that generates and displays a 2D animation 
    of the Sierpinski Gasket being rendered.
    pPosition uses points to generate the fractal.
    tPosition uses triangles to generate the fractal.

    To render Points
    in gasket.js 
    - comment out "gl.drawArrays(gl.POINTS, 0, currentVertex);" and comment "gl.drawArrays(gl.TRIANGLES, 0, currentVertex);"
    - comment out "initPoints(initVertices);" and comment below "initTriangles(initVertices[0], initVertices[1], initVertices[2], numTimesToSubdivide);"
    in gasket.js 
    - comment out "vec4 aPosition = pPosition;" and comment "vec4 aPosition = tPosition;"

    To render Traingles
    in gasket.js comment 
    - comment out "gl.drawArrays(gl.TRIANGLES, 0, currentVertex);" and comment "gl.drawArrays(gl.POINTS, 0, currentVertex);"
    - out "gl.drawArrays(gl.TRIANGLES, 0, currentVertex);" and comment "gl.drawArrays(gl.POINTS, 0, currentVertex);"
    in gasket.js 
    - comment out "vec4 aPosition = tPosition;" and comment "vec4 aPosition = pPosition;"
*/

"use strict";

/** @type {WebGLRenderingContext} */
var gl;

var positions = [];

var positionsP = []; // Store Points Positions
// var numPositions = 5000; // Number of points to be generated 
var numPositions = 20000; 

var positionsT = []; // Store Tringles Positions
var numTimesToSubdivide = 5; // Number of recursive subdivisions of the triangles

/**
 * Initializes the WebGL context and generates the Sierpinski Gasket points.
 * Sets the graphics pipeline.
 *
 * @function
 * @name init
 */
window.onload = function init() {
    var canvas = document.getElementById("gl-canvas"); // Sets the HTML canvas
    // Initializes the WebGL 2.0 context, allowing the use of the WebGL API 
    // to draw graphics on the canvas element. 
    // gl is the interface provides the OpenGL ES 3.0 rendering context
    // drawing surface of an HTML <canvas> element.
    gl = canvas.getContext('webgl2');
    if (!gl) alert( "WebGL 2.0 isn't available" );

    // ================================================================================
    /*-----------------------
     |   Initialize Gasket  |
     -----------------------*/

    // ------- Initializes Points --------

    // Corners of our gasket with three positions, a triangle.
    var initVertices = [
        vec2(-1, -1),
        vec2(0,  1),
        vec2( 1, -1)
    ];

    // ------- Initializes Points --------
    initPoints(initVertices); // <------ to draw points comment out and comment below "initTriangles(initVertices[0], initVertices[1], initVertices[2], numTimesToSubdivide);"

    // ------- Initializes Triangle --------
    // initTriangles(initVertices[0], initVertices[1], initVertices[2], numTimesToSubdivide); // <------ to draw points comment out and comment above "initPoints(initVertices);""

    // ================================================================================
    /*----------------------
     |   Configure WebGL   |
     ----------------------*/

    // Set viewpoint and background
    gl.viewport(0, 0, canvas.width, canvas.height); // Set the viewport size
    gl.clearColor(0.0, 0.0, 0.0, 1.0); // Set the background color to black
    // gl.clearColor(1.0, 1.0, 1.0, 1.0); // Set the background color to white

    // Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    // Load the data into the GPU
    var bufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, bufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);

    // ------- Configure Points -----
    // Associate our shader variables with our data buffer
    var positionLocP = gl.getAttribLocation(program, "pPosition");
    gl.vertexAttribPointer(positionLocP, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLocP);

    // ------- Configure Triangles -----
    // Associate our shader variables with our data buffer
    var positionLocT = gl.getAttribLocation(program, "tPosition");
    gl.vertexAttribPointer(positionLocT, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLocT);

    render();
};

// ================================================================================

/**
 * Clears the canvas and renders the Sierpinski Gasket points.
 * Recursive function - creates an animation of the Gasket being rendered.
 * 
 * @function
 * @name render
 */
var currentVertex = 0; // Track the current point being rendered
function render() {
    
    // Clear the canvas before each frame
    gl.clear(gl.COLOR_BUFFER_BIT);

    // ----- Draw Points -----
    // Render points in the array from index 0 up to the current point's index
    gl.drawArrays(gl.POINTS, 0, currentVertex); // <------ to draw points comment out and comment below "gl.drawArrays(gl.TRIANGLES, 0, currentVertex);"

    // ----- Draw Triangles -----
    // gl.drawArrays(gl.TRIANGLES, 0, currentVertex); // <------ to draw triangles comment out and comment above "gl.drawArrays(gl.POINTS, 0, currentVertex);"
    
    // Increment the current point index
    // ---- Recursion Base case ---- currentVertex == positions.length
    if (currentVertex < positions.length) { 
        // ---- Recursive case ----
        currentVertex++;
        // ---- Recursive call ----
        setTimeout(render, 10); // 10 milliseconds delay between each point
    }
}


function initPoints(vertices) {
    // Add the initial position to the array of points
    var u = add(vertices[0], vertices[1]);
    var v = add(vertices[0], vertices[2]);
    var p = mult(0.25, add( u, v )); // Computed point position inside the gasket
    positionsP.push(p);

    // Compute new positions to generate the gasket
    // Each new point is located midway between the last point
    // The new point is randomly picked
    for ( var i = 0; positionsP.length < numPositions; ++i ) {
        var j = Math.floor(3 * Math.random()); // Vertex index picked randomly 

        // Calculate the midpoint
        p = add(positionsP[i], vertices[j]); 
        p = mult(0.5, p);
        positionsP.push(p);
    }

    positions = positionsP;
}

// ================================================================================

/**
 * Adds a single triangle to the position buffer.
 * 
 * @function
 * @name triangle
 * @param {vec2} a - The first vertex of the triangle
 * @param {vec2} b - The second vertex of the triangle
 * @param {vec2} c - The third vertex of the triangle
 */
function triangle(a, b, c) {
    positionsT.push(a, b, c);
}


/**
 * Subdivides a triangle into smaller triangles 
 * 
 * @function
 * @name initTriangles
 * @param {vec2} a - The first vertex of the triangle
 * @param {vec2} b - The second vertex of the triangle
 * @param {vec2} c - The third vertex of the triangle
 * @param {number} count - The number of subdivisions remaining
 */
function initTriangles(a, b, c, count) {

    // ---- Base case ----
    if ( count === 0 ) {
        triangle(a, b, c);
    }
    else {
        
        // ---- Recursive case ----
        // bisect the sides
        var ab = mix( a, b, 0.5 );
        var ac = mix( a, c, 0.5 );
        var bc = mix( b, c, 0.5 );

        --count;

        // ---- Recursive call ----
        // three new triangles
        initTriangles( a, ab, ac, count );
        initTriangles( c, ac, bc, count );
        initTriangles( b, bc, ab, count );
    }

    positions = positionsT;
}





