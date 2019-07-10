function drawPoint(pointStatus, ctx, i, j) {
    switch (pointStatus) {
        case "spawn":
            ctx.fillStyle = "blue";
            ctx.fillRect(scale * i, scale * j, scale, scale);
            break;
        case "food":
            ctx.fillStyle = "red";
            ctx.fillRect(scale * i, scale * j, scale, scale);
            break;
        case "obstacle":
            ctx.fillStyle = "aqua";
            ctx.fillRect(scale * i, scale * j, scale, scale);
            break;
        case "antUp":
            ctx.drawImage(imgUp, scale * i, scale * j);
            break;
        case "antRight":
            ctx.drawImage(antRight, scale * i, scale * j);
            break;
        case "antDown":
            ctx.drawImage(antDown, scale * i, scale * j);
            break;
        case "antLeft":
            ctx.drawImage(antLeft, scale * i, scale * j);
            break;
        default:
            ctx.fillStyle = "white";
            ctx.fillRect(scale * i, scale * j, scale, scale);
    }
}

function draw(e) {
    var data = JSON.parse(e.data);
    matrix = data['matrix'];
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < 100; i++) {
        for (var j = 0; j < 100; j++) {
            drawPoint(matrix[i][j], ctx, i, j);
            //ctx.fillStyle = matrix[i][j];
            //ctx.fillRect(5*i,5*j,5,5);   
        }
    }
}

function drawMatrix() {
    matrixSocket.send(JSON.stringify({ 'counter': 1 }));
    ctx2.drawImage(img, 30, 30);
}

setInterval(drawMatrix, 100);