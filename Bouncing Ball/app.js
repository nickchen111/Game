const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
// const unit = 50;
// const column = canvas.width / unit; // 1000 / 20 = 50
// const row = canvas.height / unit; // 600/ 20 = 30;
let circle_x = 160;
let circle_y = 60;
let radius = 20;
let xSpeed = 20;
let ySpeed = 20;
let ground_x = 100;
let ground_y = 500;
let ground_height = 5;
let brickArray = [];
let count = 0;

//求min到max隨機的數字 小技巧
function getRandomArbitrary(min, max) {
  return min + Math.floor(Math.random() * (max - min));
}

//監聽滑鼠移動軌跡
canvas.addEventListener("mousemove", (e) => {
  ground_x = e.clientX;
});

//生成可以被撞擊的物件
class Brick {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.width = 50;
    this.height = 50;
    brickArray.push(this);
    this.visible = true;
  }

  drawBrick() {
    ctx.fillStyle = "lightgreen";
    ctx.fillRect(this.x, this.y, this.width, this.height);
  }
  touchingBall(ballX, ballY) {
    return (
      ballX >= this.x - radius &&
      ballX <= this.x + radius + this.width &&
      ballY <= this.y + radius + this.height &&
      ballY >= this.y - radius
    );
  }
}
//製作所有的brick 寬度限制 0 <= x <= 950 高度 0 <= y <= 550
for (let i = 0; i < 10; i++) {
  new Brick(getRandomArbitrary(0, 950), getRandomArbitrary(0, 550));
}

//生成圓
function drawCircle() {
  //確認球是否有打到磚塊
  brickArray.forEach((brick, index) => {
    if (brick.visible && brick.touchingBall(circle_x, circle_y)) {
      brick.visible = false;
      count += 1;
      //改變x y 方向速度 將brick從brickArray 移除
      //從下方與上方撞擊
      if (circle_y >= brick.y + brick.height || circle_y <= brick.y) {
        ySpeed = -ySpeed;
      }
      //從左方與右方
      else if (circle_x <= brick.x || circle_x >= brick.x + brick.width) {
        xSpeed = -xSpeed;
      }

      // brickArray.splice(index, 1); // 從這個index開始刪掉一個值
      // if (brickArray.length == 0) {
      //   alert("遊戲結束");
      //   clearInterval(game);
      // }
      if (count == 10) {
        alert("遊戲結束");
        clearInterval(game);
      }
    }
  });
  //確認球 是否打到橘色地板
  if (
    circle_x + radius >= ground_x &&
    circle_x - radius <= ground_x + 200 &&
    circle_y + radius >= ground_y &&
    circle_y - radius <= ground_y + 5
  ) {
    //給他施加彈力
    if (ySpeed > 0) {
      circle_y -= 40;
    } else {
      circle_y += 40;
    }
    ySpeed = -ySpeed;
  }
  //確認球有無打到邊界
  if (circle_x < 0 || circle_x >= canvas.width - radius) {
    xSpeed = -xSpeed;
  } else if (circle_y >= canvas.height - radius || circle_y < radius) {
    ySpeed = -ySpeed;
  }

  //更動圓的座標 製造移動感
  circle_x += xSpeed;
  circle_y += ySpeed;
  //畫出黑色背景
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 畫出所有的brick
  brickArray.forEach((brick) => {
    if (brick.visible) brick.drawBrick();
  });

  //畫出可控制的地板
  ctx.fillStyle = "orange";
  ctx.fillRect(ground_x, ground_y, 200, ground_height);

  // 畫出圓球 x, y, radius, startangle, endangle , xy為圓心
  ctx.beginPath();
  ctx.arc(circle_x, circle_y, radius, 0, 2 * Math.PI);
  ctx.stroke();
  ctx.fillStyle = "yellow";
  ctx.fill();
}
let game = setInterval(drawCircle, 25);
