import pygame
import time
import random
pygame.font.init()

x,y = 460,630 # Best Quality
WIN = pygame.display.set_mode((x,y)) # Windows game
pygame.display.set_caption("Space War (Practice).")

# load images
Blue_space_ship = pygame.image.load("Enemy1.PNG")
Blue_space_ship = pygame.transform.scale(Blue_space_ship,(35,35))
Red_space_ship = pygame.image.load("Enemy2.PNG")
Red_space_ship = pygame.transform.scale(Red_space_ship,(20,20))
Yellow_space_ship = pygame.image.load("Enemy3.PNG")
Yellow_space_ship = pygame.transform.scale(Yellow_space_ship,(15,15))
# player ship
player_space_ship = pygame.image.load("SpaceShip.bmp")
player_space_ship = pygame.transform.scale(player_space_ship,(50,50))

# missile ships
Red_space_ship_missile = pygame.image.load("missile2.PNG")
Red_space_ship_missile = pygame.transform.scale(Red_space_ship_missile,(11,11))
Blue_space_ship_missile = pygame.image.load("missile1.PNG")
Blue_space_ship_missile = pygame.transform.scale(Blue_space_ship_missile,(11,11))
Yellow_space_ship_missile = pygame.image.load("missile3.PNG")
Yellow_space_ship_missile = pygame.transform.scale(Yellow_space_ship_missile,(11,11))
# missile player ship
player_space_ship_missile = pygame.image.load("missile.PNG")
player_space_ship_missile = pygame.transform.scale(player_space_ship_missile,(9,9))
player_space_ship_missile_pro = pygame.image.load("missile.PNG")
player_space_ship_missile_pro = pygame.transform.scale(player_space_ship_missile_pro,(15,15))

# BackGround
BG = pygame.image.load("SpaceBackG.PNG")
BG = pygame.transform.scale(BG,(x,y))

class Missile:
    def __init__ (self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self,window):
        window.blit(self.image,(self.x,self.y))
    
    def move(self,vel):
        self.y+= vel
    
    def off_screen(self,height):
        return not(self.y < height and self.y >= 0)

    def collision(self,_object):
        return collide(self,_object)



class Ship:
    COOLMISSILE = 30
    def __init__(self,x,y,health =100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.missile_image = None
        self.missilePro_image = None
        self.missiles = list()
        self.cool_down_conter = 0
    
    def draw(self,window,width=50,height=50):
        #pygame.draw.rect(window,(255,0,0),(self.x,self.y,width,height))
        window.blit(self.ship_image,(self.x,self.y))
        for missile in self.missiles:
            missile.draw(window)

    def move_missile(self,vel,_obj):
        self.coolmissile()
        for missile in self.missiles:
            missile.move(vel)
            if missile.off_screen(y):# HEIGHT
                self.missiles.remove(missile)
            elif missile.collision(_obj):
                _obj.health -= 10
                self.missiles.remove(missile)

    def coolmissile(self):
        if self.cool_down_conter >= self.COOLMISSILE:
            self.cool_down_conter = 0
        elif self.cool_down_conter > 0:
            self.cool_down_conter += 1

    def shoot(self):
        if self.cool_down_conter == 0 :
            missile = Missile(self.x+20,self.y,self.missile_image)
            self.missiles.append(missile)
            self.cool_down_conter = 1
    
    def shoot1(self):
        if self.cool_down_conter == 0 :
            missile = Missile(self.x+8,self.y,self.missile_image)
            self.missiles.append(missile)
            self.cool_down_conter = 1        
    
    def shoot2(self):
        if self.cool_down_conter == 0 :
            missile = Missile(self.x+32,self.y,self.missile_image)
            self.missiles.append(missile)
            self.cool_down_conter = 1

    def shootPro(self):
        if self.cool_down_conter == 0 :
            missile = Missile(self.x+16,self.y,self.missilePro_image)
            self.missiles.append(missile)
            self.cool_down_conter = 1


    def get_width(self):
        return self.ship_image.get_width()
    
    def get_height(self):
        return self.ship_image.get_height()

class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_image = player_space_ship
        self.missile_image = player_space_ship_missile
        self.missilePro_image = player_space_ship_missile_pro
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

    def move_missile(self,vel,objs):
        self.coolmissile()
        for missile in self.missiles:
            missile.move(vel)
            if missile.off_screen(y):# HEIGHT
                self.missiles.remove(missile)
            else:
                for obj in objs:
                    if missile.collision(obj):
                        objs.remove(obj)
                        self.missiles.remove(missile)
    def draw(self,window):
        super().draw(window)
        self.health_charge(window)
    def health_charge(self,window):
        pygame.draw.rect(window,(255,55,55),(self.x , \
            self.y + self.ship_image.get_height()+10,\
                self.ship_image.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x , \
            self.y + self.ship_image.get_height()+10,\
                self.ship_image.get_width() *(self.health/self.max_health),10))     

class Enemy(Ship):
    Color_Ship_Strnger={
        "red":(Red_space_ship,Red_space_ship_missile),
        "yellow":(Yellow_space_ship,Yellow_space_ship_missile),
        "blue": (Blue_space_ship,Blue_space_ship_missile)
    }
    def __init__(self,x,y,color,health = 100):
        super().__init__(x,y,health)
        self.ship_image,self.missile_image = self.Color_Ship_Strnger[color]
        self.ship_image,self.missilePro_image = self.Color_Ship_Strnger[color]
        self.mask = pygame.mask.from_surface(self.ship_image)
    
    def move(self,vel):
        self.y+= vel
    def shoot(self):
        if self.cool_down_conter == 0 :
            missile = Missile(self.x+5,self.y,self.missile_image)
            self.missiles.append(missile)
            self.cool_down_conter = 1

def collide(_object1,_object2): # contact
    offset_x = _object2.x - _object1.x
    offset_y = _object2.y - _object1.y
    return _object1.mask.overlap(_object2.mask,(offset_x,offset_y)) != None

def main(): # NEW
    run = True
    Fps = 60
    level = 0
    lives = 5
    _missile =12
    main_font = pygame.font.SysFont('courier',20)
    lost_font = pygame.font.SysFont("courier",40)
    enemies = list()
    wave_length = 5
    enemy_velocity =1
    player_velocity = 10
    missile_velocity = 12
    missilePro_velocity = 15 
    player = Player(300,500)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG,(0,0))
        # text
        for i in range(255):
            lives_label = main_font.render(f"Lives: {lives}",1,(0,255,i))
            level_label = main_font.render(f"Level: {level}",2,(255,i,0))
            missilePro_label = main_font.render(f"Missile: {_missile}",3,(i,0,255))
            
        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label,(x - level_label.get_width()-10,10)) 
        WIN.blit(missilePro_label,(10,y- missilePro_label.get_width()+100)) 
        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_labeel = lost_font.render("YOU LOST!!!",5,(255,255,255))
            WIN.blit(lost_labeel,(x/2-lost_labeel.get_width()/2,350))
        pygame.display.update()

    while run:
        clock.tick(Fps)
        redraw_window()
        if _missile <=0 :
            missilePro_velocity = missile_velocity
            
            

        if lives <=0 or player.health <=0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > Fps*3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for j in range(wave_length):
                enemy = Enemy(random.randrange(50,x-50),\
                    random.randrange(-1500,-100),random.choice(["red","blue","yellow"]))#-1500*level/5
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0: # left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity+ player.get_width() < x: # right
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0: # up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + 10 < y: # down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_q]:
            player.shoot1()
        if keys[pygame.K_e]:
            player.shoot2()
        if keys[pygame.K_f]:
            player.shootPro()

        for enemy in enemies[ : ]:
            enemy.move(enemy_velocity)
            enemy.move_missile(missile_velocity, player)
            
            if random.randrange(0,2*60) == 1:
               enemy.shoot() 
            
            # if collide(enemy,player):
            #     player.health -=10
            #     enemies.remove(enemy)
            # elif enemy.y + enemy.get_height() > y:
            #     lives -= 1
            #     enemies.remove(enemy)
                    
            if keys[pygame.K_f]:
                _missile = _missile

            
        player.move_missile(-missile_velocity, enemies)

        redraw_window()

def Main_menu():
    Text_font = pygame.font.SysFont("Courier",25)
    run = True
    while run:
        WIN.blit(BG,(0,0))
        Text_font_label = Text_font.render("Press the Space to Start...",12,(0,55,255))
        WIN.blit(Text_font_label,(x/2 - Text_font_label.get_width()/2 , y/2 - Text_font_label.get_height()/2))
        pygame.display.update()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            if i.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

Main_menu()
