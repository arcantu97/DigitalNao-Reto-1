

document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById("canvas");
    var canvasContext = canvas.getContext("2d");
    var x = canvas.width / 2;
    var y = canvas.height - 30;
    var dx = 2;
    var dy = -2;
    const ballRadius = 10;
    const paddleHeight = 9;
    const paddleWidth = 75;
    let paddleX = (canvas.width - paddleWidth) / 2;
    let rightPressed = false;
    let leftPressed = false;
    var brickRowCount = 3;
    var brickColumnCount = 8;
    var brickWidth = 69;
    var brickHeight = 20;
    var brickPadding = 10;
    var brickOffsetTop = 30;
    var brickOffsetLeft = 30;
    var bricks = [];
    var score = 0;
    let attempts = 3;
    const fps = 120;
    
    for (let column = 0; column < brickColumnCount; column++) {
        bricks[column] = [];
        for (let row = 0; row < brickRowCount; row++) {
            bricks[column][row] = { x: 0, y: 0, status: 1 };
        }
    }

    document.addEventListener("mousemove", mouseHandler, false);
    document.addEventListener("keydown", keyDownHandler, false);
    document.addEventListener("keyup", keyUpHandler, false);
    function keyDownHandler(e) {
        if (e.key == "Right" || e.key == "ArrowRight") {
            rightPressed = true;
        }
        else if (e.key == "Left" || e.key == "ArrowLeft") {
            leftPressed = true;
        }
    }

    function keyUpHandler(e) {
        if (e.key == "Right" || e.key == "ArrowRight") {
            rightPressed = false;
        }
        else if (e.key == "Left" || e.key == "ArrowLeft") {
            leftPressed = false;
        }
    }

    function mouseHandler(e) {
        const relativeX = e.clientX - canvas.offsetLeft;
        if (relativeX > 0 && relativeX < canvas.width) {
            paddleX = relativeX - paddleWidth / 2;
        }
    }


    function draw_ball() {
        canvasContext.beginPath();
        canvasContext.arc(x, y, ballRadius, 0, Math.PI * 2);
        canvasContext.fillStyle = "white";
        canvasContext.fill();
        canvasContext.closePath();
    }

    function draw_paddle() {
        canvasContext.beginPath();
        canvasContext.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
        canvasContext.fillStyle = "red";
        canvasContext.fill();
        canvasContext.closePath();
    }

    function draw_bricks() {
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                if (bricks[c][r].status === 1) {
                    const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                    const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                    bricks[c][r].x = brickX;
                    bricks[c][r].y = brickY;
                    canvasContext.beginPath();
                    canvasContext.rect(brickX, brickY, brickWidth, brickHeight);
                    canvasContext.fillStyle = "#0095DD";
                    canvasContext.fill();
                    canvasContext.closePath();
                }
            }
        }
    }


    function draw_collision() {
        for (let c = 0; c < brickColumnCount; c++) {
            for (let r = 0; r < brickRowCount; r++) {
                const b = bricks[c][r];
                if (b.status === 1) {
                    if (
                        x > b.x &&
                        x < b.x + brickWidth &&
                        y > b.y &&
                        y < b.y + brickHeight
                    ) {
                        dy = -dy;
                        b.status = 0;
                        score++;
                        if (score === brickRowCount * brickColumnCount) {
                            alert("Ganaste!");
                            document.location.reload();
                            clearInterval(interval); // Needed for Chrome to end game
                        }
                    }
                }
            }
        }
    }

    function draw_score() {
        canvasContext.font = "20px Arial";
        canvasContext.fillStyle = "green";
        canvasContext.fillText(`Score: ${score}`, 8, 20);
    }

    function draw_attemps() {
        canvasContext.font = "20px Arial";
        canvasContext.fillStyle = "white";
        canvasContext.fillText(`Attemps: ${attempts}`, canvas.width - 185, 20);
    }



    function draw_area() {
        canvasContext.clearRect(0, 0, canvas.width, canvas.height);
        draw_bricks();
        draw_ball();
        draw_paddle();
        draw_collision();
        draw_score();
        draw_attemps();

        // Efecto de mover la bola en la posición opuesta  
        if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
            dx = -dx;
        }
        if (y + dy < ballRadius) {
            dy = -dy;
        }
        else if (y + dy > canvas.height - ballRadius) {
            if (x > paddleX && x < paddleX + paddleWidth) {
                dy = -dy;
            }
            else {
                attempts--;
                if (!attempts) {
                    alert("GAME OVER");
                    document.location.reload();
                }
                else {
                    x = canvas.width / 2;
                    y = canvas.height - 30;
                    dx = 3;
                    dy = -3;
                    paddleX = (canvas.width - paddleWidth) / 2;
                }
            }
        }

        if (rightPressed && paddleX < canvas.width - paddleWidth) {
            paddleX += 7;
        }
        else if (leftPressed && paddleX > 0) {
            paddleX -= 7;
        }

        x += dx;
        y += dy;
        requestAnimationFrame(draw_area);
    }

    draw_area();

});

