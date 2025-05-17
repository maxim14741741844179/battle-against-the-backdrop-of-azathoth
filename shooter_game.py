#Создай собственный Шутер!
from random import randint, random
from pygame import *
font.init()
font1 = font.Font(None, 36)
lost = 0
font2 = font.Font(None, 36)
kill = 0
font3 = font.Font(None, 80)
font4 = font.Font(None, 36)
mixer.init()
mixer.music.load('kosmicheskie-zvuki-chernaya-dyira-puteshestvie-vo-vremeni-36695.mp3')
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')

win = display.set_mode((700, 500))
display.set_caption('присутствие пустоты')
bg = transform.scale(image.load('2021-06-04_16-40-25.png'), (700, 500))
bg1 = transform.scale(image.load('35b5db0072d511eebecbbaea8797b5f2_upscaled.jfif'), (700, 500))
clock = time.Clock()

finish = False
game = True
menu = True

class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.health = 10
        self.is_parrying = False
        self.parry_duration = 30  
        self.parry_timer = 0  

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x += self.speed
        if self.is_parrying:
            current_time = time.get_ticks()
            if current_time - self.start_time >= 1:
                self.parry_timer -= 1
                self.start_time = current_time
                if self.parry_timer <= 0:
                    self.is_parrying = False
    def fire(self):
        bullet = Bullet('High_Velocity_Bullet.jpg', 10, 20, 10, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        if current_weapon_index == 1:
            bullet = Bullet('High_Velocity_Bullet.jpg', 10, 20, 10, self.rect.left, self.rect.top)
            bullets.add(bullet)
            bullet = Bullet('High_Velocity_Bullet.jpg', 10, 20, 10, self.rect.right, self.rect.top)
            bullets.add(bullet)
    def parry(self):
        if not self.is_parrying:
            self.is_parrying = True
            self.parry_timer = self.parry_duration
class Enemy(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.healthmy = 5 
        self.damage = 2
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
           self.rect.y = -50
           self.rect.x = randint(0, 700 - self.rect.w)
           self.speed = randint(1, 5)
           lost += 1

class Bullet(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.damage = 3
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
class Boss(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.healthb = 10
        self.last_shot_time = time.get_ticks()
        self.shoot_interval = 200
    def shoot(self):
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.last_shot_time = current_time
class Bulletb(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.damage = 3
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()




        
class Weapon:
    def __init__(self, name, fire_rate, dps):
        self.name = name
        self.fire_rate = fire_rate
        self.dps = dps

weapons = [
    Weapon ("Пистолет", 3, 3),         # 2 выстрела в секунду
    Weapon("Дробовик", 2, 2),         # 1 выстрел в секунду
    Weapon("Автомат", 7, 1),          # 5 выстрелов в секунду
    Weapon("Снайперская винтовка", 1, 10)  # Полвыстрела в секунду (один выстрел за два секунды)
]
current_weapon_index = 0
last_shot_time = 0






player = Player('images-no-bg-preview (carve.photos).png', 65, 65, 10, 350, 430)
enemy1 = Enemy('images (8)-no-bg-preview (carve.photos).png', 65, 65, randint(1, 3), randint(0, 635), -50)
enemy2 = Enemy('images (8)-no-bg-preview (carve.photos).png', 65, 65, randint(1, 3), randint(0, 635), -50) 
enemy3 = Enemy('images (8)-no-bg-preview (carve.photos).png', 65, 65, randint(1, 3), randint(0, 635), -50) 
enemy4 = Enemy('images (8)-no-bg-preview (carve.photos).png', 65, 65, randint(1, 3), randint(0, 635), -50)
enemy5 = Enemy('images (8)-no-bg-preview (carve.photos).png', 65, 65, randint(1, 3), randint(0, 635), -50)
start = GameSprite('pngtree-finish-button-in-pixel-art-style-png-image_5683603.png', 200, 100, 0, 250, 300)
boss = Boss('1383287635_1755349320-no-bg-preview (carve.photos).png', 500, 250, 0, 100, 10)


enemies = sprite.Group()
enemies.add(enemy1, enemy2, enemy3, enemy4, enemy5)
bullets = sprite.Group()

winner = font3.render('Ультраборщ', 1, (0, 0, 230))
losers = font3.render('Ультралох', 1, (230, 0, 0))

while game:
    if menu:
        win.blit(bg1, (0, 0))
        start.reset()
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if start.rect.collidepoint(x,y):
                    menu = False
    if finish == False and menu == False:
        win.blit(bg, (0, 0))
        player.update()
        player.reset()
        enemies.update()
        enemies.draw(win)
        bullets.update()
        bullets.draw(win)
        text_lose = font1.render('Ултракасой: ' + str(lost), 1, (230, 0, 0))
        win.blit(text_lose, (50, 50))
        text_kill = font2.render('Ултраубийство: ' + str(kill), 1, (230, 0, 0))
        win.blit(text_kill, (50, 20))
        text_life = font4.render('Ультрахп: ' + str(player.health), 1, (0, 230, 0))
        win.blit(text_life, (50, 80))
        sprites_list1 = sprite.groupcollide(enemies, bullets, False, False)
        for enemy1 in sprites_list1:
            # print(sprites_list1[enemy1])
            for bullet in sprites_list1[enemy1]:
                bullet.damage = current_weapon.dps
                enemy1.healthmy -= bullet.damage
                print(enemy1.healthmy, bullet.damage)  
                # for bullet in bullets:
                bullet.kill()
                if enemy1.healthmy <= 0:
                    enemy1.kill()
                    kill += 1
                    enemy1 = Enemy('images (8)-no-bg-preview (carve.photos).png', 65, 65, randint(1, 5), randint(0, 635), -50)
                    enemies.add(enemy1)
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_i:
                    weapon = weapons[current_weapon_index]
                    
                    current_time = time.get_ticks()
                    if current_time - last_shot_time >= (1000 / weapon.fire_rate):
                        last_shot_time = current_time
                        bullet_dps = current_time
                        current_weapon = weapons[current_weapon_index]
                        player.fire()      
                if e.key == K_o:
                    # print('p')
                    if not player.is_parrying:
                        player.start_time = time.get_ticks()
                    player.parry()
                if e.key == K_1:
                    current_weapon_index = 0
                elif e.key == K_2 and len(weapons) > 1:
                    current_weapon_index = 1
                elif e.key == K_3 and len(weapons) > 2:
                    current_weapon_index = 2
                elif e.key == K_4 and len(weapons) > 3:
                    current_weapon_index = 3
        if kill >= 1:
            boss.reset()
            enemies.empty()
            sprites_list2 = sprite.spritecollide(boss, bullets, False)
            for bullet in sprites_list2:
                bullet.damage = current_weapon.dps
                boss.healthb -= bullet.damage
                print(boss.healthb, bullet.damage)  
                bullet.kill()
            if boss.healthb <= 0:
                finish = True
                win.blit(winner, (200, 200))
        if lost >= 100000000000000000:
            finish = True
            win.blit(losers, (200, 200))
        if player.health <= 0:
            finish = True
            win.blit(losers, (200, 200))
        # if len(sprite.spritecollide(player, enemies, False)) > 0:
        for enemy in sprite.spritecollide(player, enemies, False):
            print('столкнулся')
            if not player.is_parrying:
                print('паррирование')
                player.health -= enemy.damage  
                print(f"Player Health: {player.health}")
            else:
                print("Attack parried!")
            enemy.kill()
            enemy1 = Enemy('images (8)-no-bg-preview (carve.photos).png', 65, 65, randint(1, 5), randint(0, 635), -50)
            enemies.add(enemy1)
    if finish == True and menu == False:
        for e in event.get():
            if e.type == QUIT:
                game = False
    
    clock.tick(60)
    display.update()
