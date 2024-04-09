# Game

# 資料夾說明

* 太空遊戲:
  * 遊戲說明:玩家需要操作只能左右移動的飛船躲避或者發射子彈將從上方降落的隕石擊碎,過程中玩家可以吃到閃電來增強子彈射擊效果五秒或者吃到盾牌回復血量
  * 用python與其模組pygame,結合pygame模組的函式以及物件導向概念做出
  * 遊戲畫面:
    * 初始畫面: ![image](https://github.com/nickchen111/Game/blob/main/Space%20Game/img/%E5%A4%AA%E7%A9%BA%E9%81%8A%E6%88%B2%E9%96%8B%E5%A7%8B%E7%95%AB%E9%9D%A2.png=100x200)
 
* 貪吃蛇遊戲:
  * 遊戲說明: 玩家需要用上下左右鍵操作貪吃蛇去吃到畫面中隨機出現的果實,並且每次吃了果實尾巴就會變長分數就會增加 如果咬到自己遊戲就結束了
  * 結合HTML與CSS做出遊戲畫面,再利用Javascript物件導向概念做出果實、蛇身等物件
  * 技術細節:
    * 需考量果實每次出現地點不能在貪吃蛇身體上 利用 do while迴圈判斷
    * 利用canvas做出遊戲畫面
    * 需debug玩家如果同時在0.1內按了兩次方向鍵有可能導致的bug處理 利用暫時取消事件監聽功能的方式
* 彈跳球遊戲:
  * 遊戲說明: 玩家需要用滑鼠操作一個會隨滑鼠X座標移動的版子在有限空間內去控制不斷撞到物體而反彈的球撞到所有在空間內的方塊,越快撞完的人獲勝
  * 結合HTML與CSS做出遊戲畫面,再利用Javascript物件導向概念做出磚塊物件
  * 技術細節:
    * 在判斷是否所有磚塊被消除的程式碼中,不去真的將陣列中的磚塊物件刪除 而是用一個變數count計算被撞擊的磚塊再利用visible屬性去讓磚塊消失 以此來優化時間複雜度
    * 利用canvas做出遊戲畫面
# English Version
* Space Game:
  * Game Description: Players need to operate a spaceship that can only move left or right to dodge or shoot bullets to destroy meteors descending from above. During the game, players      can pick up lightning to enhance bullet shooting effects for five seconds or pick up shields to restore health.
  * Developed using Python and its module Pygame, combining Pygame module functions and object-oriented concepts to create the space game.
    
* Snake Game:
  * Game Description: Players need to use the arrow keys to control a snake to eat randomly appearing fruits on the screen. Each time the snake eats a fruit, its tail grows longer and      the score increases. If the snake bites itself, the game ends.
  * Created the game interface using HTML and CSS, then utilized JavaScript's object-oriented concepts to create objects such as fruits and snake body segments.
  * Technical Details:
    * Need to consider that fruits cannot appear on the snake's body. Use a do-while loop for checking.
    * Implemented the game interface using canvas.
    * Addressed a bug where if players pressed two direction keys within 0.1 seconds, it could cause unexpected behavior by temporarily disabling event listening.

* Bouncing Ball Game:
  * Game Description: Players need to control a paddle that moves horizontally with the mouse to bounce a ball continuously hitting objects within a limited space, aiming to hit all t      -he bricks in the space. The faster player who clears all bricks wins.
  * Created the game interface using HTML and CSS, then utilized JavaScript's object-oriented concepts to create bricks objects.
  * Technical Details:
    * In the code for checking if all bricks have been eliminated, instead of deleting bricks objects from the array, a variable "count" is used to track the number of hit bricks. The
      "visible" attribute is then used to make bricks disappear, optimizing time complexity.
    * Utilized canvas for creating the game interface.
