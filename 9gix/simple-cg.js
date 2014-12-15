
var aVertPos, uMVMatrix, uPMatrix;
var MVMatrix, PMatrix;


function init(){
    var canvas = document.getElementById('simple-cg');
    var gl = initWebGL(canvas);
    gl.clearColor(0.0, 1.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    initViewport(gl, canvas);
    initShaders(gl);
    initMatrices(canvas);
    
    var square = createSquare(gl);
    draw(gl, square);
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

    shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    gl.useProgram(shaderProgram);


    aVertPos = gl.getAttribLocation(shaderProgram, "aVertPos");
    gl.enableVertexAttribArray(aVertPos);

    uMVMatrix = gl.getUniformLocation(shaderProgram, "uMVMatrix");

    uPMatrix = gl.getUniformLocation(shaderProgram, "uPMatrix");

}

function initMatrices(canvas){
    MVMatrix = mat4.create();
    mat4.translate(MVMatrix, MVMatrix, [0, 0, -3.333]);

    PMatrix = mat4.create();
    mat4.perspective(PMatrix, Math.PI / 4, canvas.width / canvas.height, 1, 10000);
}

function draw(gl, obj){
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    gl.bindBuffer(gl.ARRAY_BUFFER, obj.buffer);

    gl.vertexAttribPointer(aVertPos, obj.vertSize, gl.FLOAT, false, 0, 0);
    gl.uniformMatrix4fv(uMVMatrix, false, MVMatrix);
    gl.uniformMatrix4fv(uPMatrix, false, PMatrix);

    gl.drawArrays(obj.primtype, 0, obj.nVerts);
}

function getFragmentShader(gl){
    return loadShaderFromDOM(gl, "shader-fs");
}

function getVertexShader(gl){
    return loadShaderFromDOM(gl, "shader-vs");
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
    var verts = [
         .5,  .5,  0.0,
        -.5,  .5,  0.0,
         .5, -.5,  0.0,
        -.5, -.5,  0.0
    ];
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(verts), gl.STATIC_DRAW);
    
    var square = {
        buffer:vertexBuffer,
        vertSize:3,
        nVerts:4,
        primtype:gl.TRIANGLE_STRIP
    };
    return square;
}