window.canvas = document.querySelector("canvas");

doAfterRender = function(func) {
    setTimeout(func, 0);
};

drawCanvas = function() {
    var ctx=canvas.getContext("2d");
    ctx.rect(10,0,100,100);
    ctx.fillStyle="red";
    ctx.fill();
};

updateCanvasSize = function() {
  canvas.width  = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  drawCanvas();
};

window.onresize = updateCanvasSize;

updateCanvasSize();
