import pygame
import random
import os
FPS = 60
WIDTH = 500
HEIGHT = 600
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
score = 0

#遊戲初始化 與 創建視窗
pygame.init()
pygame.mixer.init() #音效模組初始化
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Game") #改遊戲名稱
font_name = os.path.join('font.ttf') #引入字體

#載入圖片
background_img = pygame.image.load(os.path.join("img","background.png")).convert() #在當下的pygame資料夾找img資料夾 載入background.png 在轉換成pygame容易讀取的格式
player_img = pygame.image.load(os.path.join("img","player.png")).convert() 
#rock_img = pygame.image.load(os.path.join("img","rock.png")).convert() 
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert() 
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert()) #在字串外加上f可以在字串內用變數 append : list tupple 用的

expl_anim = {} #字典形式
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = [] #代表飛船的爆炸圖片 一樣九張照片

for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
player_mini_image = pygame.transform.scale(player_img, (25,19))
player_mini_image.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_image) #改遊戲小圖片


#加入寶物
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img","shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img","gun.png")).convert()




#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]

pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.2)

gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))



#將文字寫到畫面上的函式
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size) #創建物件
    text_surface = font.render(text, True, WHITE)    #渲染 要寫出來的文字, 是否要用anti-arials 字體較滑順, 文字顏色
    text_rect = text_surface.get_rect() #文字做定位
    text_rect.centerx = x
    text_rect.top = y 
    surf.blit(text_surface, text_rect)

#撞到石頭把他加回來的函式
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

#畫出生命值
def draw_health(surf, hp, x, y):
    if hp < 0 :
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH,BAR_HEIGHT) #畫出外框矩形的設定
    fill_rect = pygame.Rect(x,y, fill, BAR_HEIGHT)#內部血條矩形的設定
    pygame.draw.rect(surf, GREEN, fill_rect) #把矩形畫出來
    pygame.draw.rect(surf, WHITE, outline_rect,2) #第四個參數是外框要幾像素

# 畫出還剩幾條命
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i #小飛船之間間隔三十像素在畫另外一個
        img_rect.y = y
        surf.blit(img,img_rect)
#初始畫面函式 
def draw_init():
    draw_text(screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '<- -> 移動飛船 空白鍵發射子彈', 22,WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲', 18,WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP: #按下鍵盤的東西
                waiting = False
                return False
    show_init = False            




class Player(pygame.sprite.Sprite): #繼承sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #就跟js一樣self此時就可以用sprite裡面的function了
        self.image = pygame.transform.scale(player_img, (50,38)) #重新定義圖片大小
        self.image.set_colorkey(BLACK) #去背 讓黑色變透明
        self.radius = 20
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1 #子彈等級
        self.gun_time = 0 
        
    def update(self):
        now = pygame.time.get_ticks()
        #更新子彈恢復等級時間
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        # 更新 被撞倒後復活時間
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-10
            
        key_pressed = pygame.key.get_pressed() #call此函式會回傳鍵盤上的整串布林值
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        elif key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
            
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            else:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500) #直接丟去畫面外看起來就像消失
    # 吃到閃電的函式
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        # self.image = pygame.Surface((30,40)) #寬, 高
        self.image_ori = random.choice(rock_imgs) #隨機挑一張出來
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85 / 2)
        self.rect.x = random.randrange(0, WIDTH-self.rect.width) #從這段隨機挑一個數
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
        
    def update(self):
        self.rotate() #新增石頭下墜旋轉動畫
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #如果掉下去以後超過視窗範圍就重置
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree %= 360
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree) #因為每次旋轉都會有點失真 所以每次都讓沒有失真過的圖片做旋轉才不會疊加失真
        center = self.rect.center # 取得原先的中心點 防止每次轉動都會定位不同位置
        self.rect = self.image.get_rect() #重新定位
        self.rect.center = center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): # x y 為飛船位置
        pygame.sprite.Sprite.__init__(self) 
        #self.image = pygame.Surface((10,20))
        #self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill() #會去檢查有這個子彈的所有sprite群組如果有這個子彈就移除

#爆炸的圖片物件
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size): # 爆炸中心點 大or小爆炸
        pygame.sprite.Sprite.__init__(self) 
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 #代表更新了第幾張圖片了
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 #至少過多久毫秒會到下一張
        
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            #看是否更新到最後一張圖片了 是的話就要刪掉
            if self.frame == len(expl_anim[self.size]):
                self.kill() 
            else :
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

#創建寶物
class Power(pygame.sprite.Sprite):
    def __init__(self, center): #寶物出現位置
        pygame.sprite.Sprite.__init__(self) 
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill() 

# pygame有內建函式可以幫我們判斷每個子彈跟石頭是否有碰撞 只需要將它們分別放入群組中
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
powers = pygame.sprite.Group()

for i in range(10):
    new_rock()

#播放背景音樂
pygame.mixer.music.play(-1) #傳入的參數代表要播放幾次 -1代表無限次重複播放

#創建一個物件對時間做操控
clock = pygame.time.Clock()


#遊戲迴圈
show_init = True  #初始畫面設定
running = True
while running : 
    if show_init:
        screen.blit(background_img, (0,0))
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0
    
    clock.tick(FPS)

    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #按下鍵盤的東西
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update() #這樣每個物件都會去執行update函式
    #判斷石頭子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) #後面兩個布林值判斷這兩個撞到分別是否要刪掉 並且此函式會回傳一個字典
    
    # count = 0
    # for rock in rocks:
    #     rockx = rock.rect.x
    #     rocky = rock.rect.y
    #     for bullet in bullets:
    #         if bullet.rect.bottom == rocky and bullet.rect.x == rockx or bullet.rect.left == rocky or bullet.rect.right == rocky:
    #             bullet.kill()
    #             count += 1
    #             rock.kill()
    for hit in hits:
        score += hit.radius #根據不同大小的石頭碰撞時獲得不同分數 hits裡面是key value對 key是碰撞到的石頭 value是碰撞到的子彈
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.98:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow) #寶物群組 為了之後判斷寶物飛船是否有碰到=
        new_rock()

    #判斷石頭飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) # 碰撞判斷加入標準為圓形的而非default 矩形的 True代表撞到時石頭是否要消失
    for hit in hits:
        new_rock()
        player.health -= hit.radius*2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide() #死掉之後會有一段緩衝時間才出現 
    #判斷寶物與飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True) 
    for hit in hits:
        if hit.type == 'shield':
            player.health += 5
            shield_sound.play()
            if player.health > 100:
                player.health = 100
        elif hit.type == 'gun':
            gun_sound.play()
            player.gunup()
    if player.lives == 0 and not(death_expl.alive()): # alive 函式 要等到物件已經不存在了才讓他結束遊戲 這樣可以讓爆炸跟消失都播完才結束
        show_init = True
        
    

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0,0)) #將背景圖片帶進來,放在哪
    all_sprites.draw(screen) #將此群組內所有東西畫出
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health,5,10)
    draw_lives(screen, player.lives, player_mini_image, WIDTH-100,15)
    pygame.display.update()
pygame.quit()