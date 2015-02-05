"use strict";
var simpleCG = function(){
    var aVertPosition, aVertColor, uMVMatrix, uPMatrix;
    var MVMatrix, PMatrix, rotationAxis;
    var fragmentShaderScriptId, vertexShaderScriptId;
    var texture, useTexture, aTexCoord, uSampler, textureSource;
    useTexture = true;
    textureSource = "images/box.jpg";

    if (useTexture){
        fragmentShaderScriptId = "shader-fs-texture";
        vertexShaderScriptId = "shader-vs-texture";       
    } else {
        fragmentShaderScriptId = "shader-fs";
        vertexShaderScriptId = "shader-vs";    
    }


    function init(){
        var canvas = document.getElementById('simple-cg');
        var gl = initWebGL(canvas);

        initViewport(gl, canvas);
        initShaders(gl);
        initMatrices(canvas);
        if (useTexture){
            initTexture(gl);
        }
        
        var cube = createCube(gl);
        run(gl, cube);
    }

    var duration = 5000; // ms
    var currentTime = Date.now();
    function animate() {
        var now = Date.now();
        var delta = now - currentTime;
        currentTime = now;
        var fract = delta / duration;
        var angle = Math.PI * 2 * fract;
        mat4.rotate(MVMatrix, MVMatrix, angle, rotationAxis);
    }

    function run(gl, cube) {
        requestAnimationFrame(
            function() {
                run(gl, cube);
            });
        draw(gl, cube);
        animate();
    }


    function initMatrices(canvas){
        MVMatrix = mat4.create();
        mat4.translate(MVMatrix, MVMatrix, [0, 0, -8]);

        PMatrix = mat4.create();
        mat4.perspective(PMatrix, Math.PI / 4, canvas.width / canvas.height, 1, 10000);

        rotationAxis = vec3.create();
        vec3.normalize(rotationAxis, [1, 1, 1]);
    }

    function initWebGL(canvas){
        return canvas.getContext("webgl");
    }

    function initViewport(gl, canvas){
        gl.viewport(0,0,canvas.width, canvas.height);
    }

    function initShaders(gl){
        var fragmentShader = getFragmentShader(gl);
        var vertexShader = getVertexShader(gl);

        var shaderProgram = gl.createProgram();
        gl.attachShader(shaderProgram, vertexShader);
        gl.attachShader(shaderProgram, fragmentShader);
        gl.linkProgram(shaderProgram);

        gl.useProgram(shaderProgram);


        aVertPosition = gl.getAttribLocation(shaderProgram, "aVertPosition");
        gl.enableVertexAttribArray(aVertPosition);

        if (useTexture){
            aTexCoord = gl.getAttribLocation(shaderProgram, "aTexCoord");
            gl.enableVertexAttribArray(aTexCoord);
        } else {
            aVertColor = gl.getAttribLocation(shaderProgram, "aVertColor");
            gl.enableVertexAttribArray(aVertColor);
        }

        uMVMatrix = gl.getUniformLocation(shaderProgram, "uMVMatrix");
        uPMatrix = gl.getUniformLocation(shaderProgram, "uPMatrix");

        uSampler = gl.getUniformLocation(shaderProgram, "uSampler");

    }

    function getFragmentShader(gl){
        return loadShaderFromDOM(gl, fragmentShaderScriptId);
    }

    function getVertexShader(gl){
        return loadShaderFromDOM(gl, vertexShaderScriptId);
    }

    function loadShaderFromDOM(gl, id) {
        var shaderScript, source, currentChild, shader;

        shaderScript = document.getElementById(id);

        if (!shaderScript) {
            return null;
        }

        source = "";
        currentChild = shaderScript.firstChild;

        while(currentChild) {
            if (currentChild.nodeType == currentChild.TEXT_NODE) {
                source += currentChild.textContent;
            }

            currentChild = currentChild.nextSibling;
        }

        shader = createShader(gl, source, shaderScript.type);
        return shader;
    }

    function createShader(gl, source, type){
        var shader;
        if (type == "x-shader/x-fragment") {
            shader = gl.createShader(gl.FRAGMENT_SHADER);
        } else if (type == "x-shader/x-vertex") {
            shader = gl.createShader(gl.VERTEX_SHADER);
        } else {
            // Unknown shader type
            return null;
        }

        gl.shaderSource(shader, source);
        
        // Compile the shader program
        gl.compileShader(shader);  
        
        // See if it compiled successfully
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {  
            alert("Error compiling the shaders: " + gl.getShaderInfoLog(shader));  
            return null;  
        }
        
      return shader;
    }


    // Create the vertex data for a square to be drawn
    function createSquare(gl) {
        var vertexBuffer;
        vertexBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);

        var verts = new Float32Array([
             .5,  .5,  0.0,
            -.5,  .5,  0.0,
             .5, -.5,  0.0,
            -.5, -.5,  0.0
        ]);
        gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);

        var square = {
            buffer:vertexBuffer,
            vertSize:3,
            nVerts:4,
            primtype:gl.TRIANGLE_STRIP
        };
        return square;
    }

    function createCube(gl){
        // Vertices Position
        var verts = [
           // Front face
           -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
           -1.0,  1.0,  1.0,

           // Back face
           -1.0, -1.0, -1.0,
           -1.0,  1.0, -1.0,
            1.0,  1.0, -1.0,
            1.0, -1.0, -1.0,

           // Top face
           -1.0,  1.0, -1.0,
           -1.0,  1.0,  1.0,
            1.0,  1.0,  1.0,
            1.0,  1.0, -1.0,

           // Bottom face
           -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0,  1.0,
           -1.0, -1.0,  1.0,

           // Right face
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            1.0,  1.0,  1.0,
            1.0, -1.0,  1.0,

           // Left face
           -1.0, -1.0, -1.0,
           -1.0, -1.0,  1.0,
           -1.0,  1.0,  1.0,
           -1.0,  1.0, -1.0
        ];

        var vertexBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);   
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(verts), gl.STATIC_DRAW);
        
        if (useTexture){
            // Texture Coordinate
            var texCoords = [
                // Front
                0.0, 0.0,
                1.0, 0.0,
                1.0, 1.0,
                0.0, 1.0,

                // Back
                1.0, 0.0,
                1.0, 1.0,
                0.0, 1.0,
                0.0, 0.0,

                // Top
                0.0, 1.0,
                0.0, 0.0,
                1.0, 0.0,
                1.0, 1.0,

                // Bottom
                1.0, 1.0,
                0.0, 1.0,
                0.0, 0.0,
                1.0, 0.0,

                // Right
                1.0, 0.0,
                1.0, 1.0,
                0.0, 1.0,
                0.0, 0.0,

                // Left
                0.0, 0.0,
                1.0, 0.0,
                1.0, 1.0,
                0.0, 1.0,
            ];
            var texCoordBuffer = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
            gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(texCoords), gl.STATIC_DRAW);
        
        } else {

            // Vertices Color
            var faceColors = [
                [1.0, 0.0, 0.0, 1.0], // front color
                [0.0, 1.0, 0.0, 1.0], // back color
                [0.0, 0.0, 1.0, 1.0], // top color
                [1.0, 1.0, 0.0, 1.0], // bottom color
                [0.0, 1.0, 1.0, 1.0], // right color
                [1.0, 0.0, 1.0, 1.0], // left color
            ]

            var vertexColors = [];
            for (var i in faceColors){
                var color = faceColors[i];
                for (var j = 0; j < 4; j++){
                    vertexColors = vertexColors.concat(color);
                }
            }

            var colorBuffer = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
            gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertexColors), gl.STATIC_DRAW);

        }

        // Element Array
        var cubeIndices = [
            0, 1, 2,        0, 2, 3,        // Front
            4, 5, 6,        4, 6, 7,        // Back
            8, 9, 10,       8, 10, 11,      // Top
            12, 13, 14,     12, 14, 15,     // Bottom
            16, 17, 18,     16, 18, 19,     // Right
            20, 21, 22,     20, 22, 23,     // Left
        ];
        var cubeIndexBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, cubeIndexBuffer);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(cubeIndices), gl.STATIC_DRAW);

        var cube = {
            buffer: vertexBuffer,
            colorBuffer: colorBuffer,
            texCoordBuffer: texCoordBuffer,
            indices: cubeIndexBuffer,
            vertSize: 3,
            nVerts: 24,
            colorSize: 4,
            texCoordSize: 2,
            nColor: 24,
            nIndices: 36,
            primtype: gl.TRIANGLES,
        };

        return cube;
    }

    function draw(gl, obj){
        gl.clearColor(0.0, 0.0, 0.0, 1.0);
        gl.enable(gl.DEPTH_TEST);
        gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);

        gl.bindBuffer(gl.ARRAY_BUFFER, obj.buffer);
        gl.vertexAttribPointer(aVertPosition, obj.vertSize, gl.FLOAT, false, 0, 0);

        if (useTexture){
            gl.bindBuffer(gl.ARRAY_BUFFER, obj.texCoordBuffer);
            gl.vertexAttribPointer(aTexCoord, obj.texCoordSize, gl.FLOAT, false, 0, 0);
        } else {
            gl.bindBuffer(gl.ARRAY_BUFFER, obj.colorBuffer);
            gl.vertexAttribPointer(aVertColor, obj.colorSize, gl.FLOAT, false, 0, 0);
        }

        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, obj.indices);

        gl.uniformMatrix4fv(uMVMatrix, false, MVMatrix);
        gl.uniformMatrix4fv(uPMatrix, false, PMatrix);

        if (useTexture){
            gl.activeTexture(gl.TEXTURE0);
            gl.bindTexture(gl.TEXTURE_2D, texture);
            gl.uniform1i(uSampler, 0);
        }
        gl.drawElements(obj.primtype, obj.nIndices, gl.UNSIGNED_SHORT, 0);
    }

    function handleTextureLoaded(gl, texture){
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texture.image);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
        //gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); //Prevents s-coordinate wrapping (repeating).
        //gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); //Prevents t-coordinate wrapping (repeating).
        gl.generateMipmap(gl.TEXTURE_2D);
        gl.bindTexture(gl.TEXTURE_2D, null);
    }

    function initTexture(gl){
        texture = gl.createTexture();
        texture.image = new Image();
        texture.image.onload = function(){
            handleTextureLoaded(gl, texture);
        }
        texture.image.src = textureSource;
    }
    
    return {
        init: init,
    };
};
