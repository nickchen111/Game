const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
// getContext method 會回傳一個canvas的drawing context
//drawing context 可以用來在 canvas內畫圖

//去計算蛇的身體每格多長
const unit = 20;
const row = canvas.height / unit; // 320/20 = 16
const column = canvas.width / unit; // 320/20 = 16

//開始做蛇
let snake = []; // array 中的每個元素都是一個物件 此物件工作室儲存身體的x y座標
function createSnake() {
  snake[0] = {
    x: 80,
    y: 0,
  };

  snake[1] = {
    x: 60,
    y: 0,
  };

  snake[2] = {
    x: 40,
    y: 0,
  };

  snake[3] = {
    x: 20,
    y: 0,
  };
}

//做果實
class Fruit {
  constructor() {
    this.x = Math.floor(Math.random() * column) * unit;
    this.y = Math.floor(Math.random() * row) * unit;
  }
  // instacne method
  drawFruit() {
    ctx.fillStyle = "yellow";
    ctx.fillRect(this.x, this.y, unit, unit);
  }

  pickLocation() {
    //不能跟蛇當下位置重疊
    let overlapping = false;
    let new_x;
    let new_y;

    do {
      new_x = Math.floor(Math.random() * column) * unit;
      new_y = Math.floor(Math.random() * row) * unit;
      for (let i = 0; i < snake.length; i++) {
        if (new_x == snake[i].x && new_y == snake[i].y) {
          overlapping = true;
          break;
        } else overlapping = false;
      }
    } while (overlapping);

    this.x = new_x;
    this.y = new_y;
  }
}

//初始設定 蛇 果實
createSnake();
let myFruit = new Fruit();

window.addEventListener("keydown", changeDirection);
let d = "Right";

function changeDirection(e) {
  if (e.key == "ArrowLeft" && d != "Right") {
    d = "Left";
  } else if (e.key == "ArrowRight" && d != "Left") {
    d = "Right";
  } else if (e.key == "ArrowUp" && d != "Down") {
    d = "Up";
  } else if (e.key == "ArrowDown" && d != "Up") {
    d = "Down";
  }

  //特殊狀況需處理 假設 draw d = right 我0.1s內快速按 up left 就可以180度迴轉 導致遊戲結束
  //所以每次按上下左右 在下一楨被畫出來之前 不接受任何的keydown事件
  window.removeEventListener("keydown", changeDirection);
}

let highestScore;
loadHighestScore();
let score = 0;
document.getElementById("myScore").innerHTML = "遊戲分數:" + score;
document.getElementById("myScore2").innerHTML = "最高分數:" + highestScore;

function draw() {
  //每次畫圖之前 確認蛇有沒有咬到自己
  for (let i = 1; i < snake.length; i++) {
    if (snake[i].x == snake[0].x && snake[i].y == snake[0].y) {
      clearInterval(myGame);
      alert("遊戲結束");
      return;
    }
  }

  //做每一步之前先將畫布reset
  // chatgpt 建議語法 ctx.clearRect(0, 0, canvas.width, canvas.height); // 清除 canvas
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  myFruit.drawFruit();

  //畫出蛇
  for (let i = 0; i < snake.length; i++) {
    //放置貪吃蛇撞牆後的狀態程式碼 每一格格子都會去做下列判斷
    if (snake[i].x >= canvas.width) {
      snake[i].x = 0;
    }
    if (snake[i].x < 0) {
      snake[i].x = canvas.width - unit;
    }
    if (snake[i].y >= canvas.height) {
      snake[i].y = 0;
    }
    if (snake[i].y < 0) {
      snake[i].y = canvas.height - unit;
    }

    if (i == 0) {
      ctx.fillStyle = "lightgreen"; //蛇頭
    } else {
      ctx.fillStyle = "lightblue"; // 設定填滿顏色
    }

    ctx.strokeStyle = "white"; //設定外框顏色

    // x, y, width, height
    ctx.fillRect(snake[i].x, snake[i].y, unit, unit); // 設定要畫出的實心長方形
    ctx.strokeRect(snake[i].x, snake[i].y, unit, unit); // 畫出帶有框的長方形
  }

  //以目前d變數方向決定蛇的下一楨要放在哪個座標
  let snakeX = snake[0].x;
  let snakeY = snake[0].y;
  if (d == "Left") {
    snakeX -= unit;
  } else if (d == "Up") {
    snakeY -= unit;
  } else if (d == "Down") {
    snakeY += unit;
  } else if (d == "Right") {
    snakeX += unit;
  }

  let newHead = {
    x: snakeX,
    y: snakeY,
  };

  // 再來邏輯是如果有吃到果實 我就不pop尾巴 但是還是執行unshift增加頭 沒吃到就是兩個都執行
  //確認 1. 蛇是否有吃到果實 2. 吃到要加分  3.變換果實位置
  if (newHead.x == myFruit.x && newHead.y == myFruit.y) {
    //概念是我還是同一個物件 不過用了一些判斷讓此物件內的x, y 更改數值 這樣一來每次執行的情況就會根據是否有吃果實而不同
    myFruit.pickLocation();
    score++;
    setHigherScore(score);
    document.getElementById("myScore").innerHTML = "遊戲分數:" + score;
  } else {
    snake.pop();
  }
  snake.unshift(newHead);
  window.addEventListener("keydown", changeDirection);
}

//設定蛇每過幾秒就要執行移動的function

let myGame = setInterval(draw, 100); // 要執行的function, 秒數

function loadHighestScore() {
  if (localStorage.getItem("highestScore") == null) {
    highestScore = 0;
  } else highestScore = Number(localStorage.getItem("highestScore"));
}

function setHigherScore(score) {
  if (score > highestScore) {
    localStorage.setItem("highestScore", score);
    highestScore = score;
    document.getElementById("myScore2").innerHTML = "最高分數:" + highestScore;
  }
}
