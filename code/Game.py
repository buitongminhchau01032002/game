import pygame
import random


list=['dir/car.png', 'dir/bird.png', 'dir/enemy.png','dir/computer.png','dir/ramen.png','dir/bullet.png','dir/player.png']
width=500
height=600
score= 0
score1= 0
shield=0
list_e=["dir/regularExplosion00.png","dir/regularExplosion01.png","dir/regularExplosion02.png","dir/regularExplosion03.png","dir/regularExplosion04.png","dir/regularExplosion05.png","dir/regularExplosion06.png","dir/regularExplosion07.png","dir/regularExplosion08.png"]
#EXplosion
ex_ani = {}
ex_ani["lg"]=[]
ex_ani["mi"]=[]
ex_ani["player"]=[]
for i in range(9):
    ex_e = pygame.image.load(list_e[i])
    ex_e2 = pygame.transform.scale(ex_e, (120,120))
    ex_ani["lg"].append(ex_e2)
    ex_e3 = pygame.transform.scale(ex_e, (30,30))
    ex_ani["mi"].append(ex_e3)
    ex_e4 = pygame.transform.scale(ex_e, (300,300))
    ex_ani["player"].append(ex_e4)


class Land(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("dir/landing.png")
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x= 0
        self.rect.y = height-10
#PLAYER, ĐẠN VÀ KẺ ĐỊCH
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image= pygame.image.load("dir/tank.png")
        self.rect= self.image.get_rect()
        self.radius= 25
        #pygame.draw.circle(self.image, (0,0,0), self.rect.center, self.radius)
        self.rect.centerx= self.rect.width/2  
        self.rect.bottom= height-22
        self.speedx=0

    def update(self):
        self.speedx= 0
        keystate= pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx-=11
        if keystate[pygame.K_RIGHT]:
            self.speedx+=11
        if self.rect.right>width:
            self.rect.right=width
        if self.rect.left<0:
            self.rect.left=0
        self.rect.x+=self.speedx

    def shoot(self):
        bullet= Bullet((self.rect.centerx-1.5, self.rect.top), self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
    def powerup(self):
        power= Power((self.rect.centerx-1.5, self.rect.top), self.rect.top)
        all_sprites.add(power)
        Powerup.add(power)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        i= random.randrange(7)
        self.image = pygame.image.load(list[i])
        self.image_orig= self.image.copy()
        self.rect = self.image.get_rect()       
        self.radius = 15

        #pygame.draw.circle(self.image, (0,0,0) , self.rect.center , self.radius)
        self.rect.x = random.randrange(width-20)
        self.rect.y = random.randrange(-100,-70)
        self.speedy= random.randrange(2,12)
        self.speedx= random.randrange(-2,3)
        self.rot = 0
        self.rot_speed = random.randrange(-20,20)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now- self.last_update>50:
            self.last_update = now
            self.rot= (self.rot+ self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.y> height:
            self.rect.x = random.randrange(width-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy= random.randrange(2,12)
            self.speedx= random.randrange(-2,3)
           

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("dir/bullet2.png")
        self.image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.center = x
        self.speed=-23
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            pass

class Power(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("dir/bullet2.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.center = x
        self.speed=-23
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            pass

class explosion_effect(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = ex_ani[self.size][0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update> self.frame_rate:
            self.last_update = now
            self.frame+=1
            if self.frame == len(ex_ani[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = ex_ani[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
gameover = pygame.image.load("dir/gameover.png")
def show_gameover_screen():
    screen.blit(gameover, (0,0))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#MÀN HÌNH CHÍNH
pygame.init()     

pygame.mixer.init()
hurt = pygame.mixer.Sound("dir/augh.ogg")
firesound = pygame.mixer.Sound("dir/laser.ogg")
explosion0 = pygame.mixer.Sound("dir/explosion0.ogg")
explosion0.set_volume(0.3)
explosion = pygame.mixer.Sound("dir/explosion.ogg")
explosion1 = pygame.mixer.Sound("dir/explosion1.ogg")
heart = pygame.image.load("dir/heart.png")
back= pygame.image.load("dir/land.png")

screen= pygame.display.set_mode((width,height))
pygame.display.set_caption("Tank1204")
#CÁC ĐỐI TƯỢNG
'''all_sprites = pygame.sprite.Group()
enemy = pygame.sprite.Group()
bullets = pygame.sprite.Group()
land = pygame.sprite.Group()
landing = Land()
all_sprites.add(landing)
land.add(landing)
Powerup = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(12):
    e = Enemy()
    enemy.add(e)
    all_sprites.add(e)'''

#
game_over = True
done= False
clock=pygame.time.Clock()
#score
fontname = pygame.font.match_font("arial")
def drawscore( surf, text, size, x, y):
    font = pygame.font.Font(fontname, size)
    textsurface= font.render(text,True, (0,0,0))
    textrect = textsurface.get_rect()
    textrect.midtop= (x, y)
    surf.blit(textsurface , textrect)

#VÒNG LẶP GAME
while not done:
    if game_over:
        show_gameover_screen()
        game_over = False
        
        score = 0
        score1 = 0
        shield = 0

        all_sprites = pygame.sprite.Group()
        enemy = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        land = pygame.sprite.Group()
        landing = Land()
        all_sprites.add(landing)
        land.add(landing)
        Powerup = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(17):
            e = Enemy()
            enemy.add(e)
            all_sprites.add(e)
    score+=1/40
    screen.blit(back, (0,0))
    #player.shoot()
    
    #CONTROL
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            done = True
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key== pygame.K_SPACE:
                player.shoot()
                firesound.play()
    
    all_sprites.update()
    #vA CHẠM GIỮA ĐẠN VÀ ÊNMY
    hits =  pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
        score1+=1
        e = Enemy()
        enemy.add(e)
        all_sprites.add(e)
        explosion.play()
        expl = explosion_effect(hit.rect.center, "lg")
        all_sprites.add(expl)
    #Vachajp enemy vaf mawjt ddaats
    hits = pygame.sprite.spritecollide(landing, enemy, True)
    for hit in hits:
        expl = explosion_effect(hit.rect.center, "mi")
        all_sprites.add(expl)
        explosion0.play()
        e = Enemy()
        enemy.add(e)
        all_sprites.add(e)
    
    #VA CHẠM GIỮA PLAYER VÀ ENEMY
    hits = pygame.sprite.spritecollide(player, enemy, True, pygame.sprite.collide_circle)
    for hit in hits:
        shield+=50
        explosion0.play()
        e = Enemy()
        enemy.add(e)
        all_sprites.add(e)
        hurt.play()
        if shield>100:
            explosion1.play()
            expl = explosion_effect(hit.rect.center, "player")
            all_sprites.add(expl)
            player.kill()

        expl = explosion_effect(hit.rect.center, "mi")
        all_sprites.add(expl)
    
    all_sprites.draw(screen)
    #thanh máu
    if shield==0:
        screen.blit(heart ,(10, height-50))
        screen.blit(heart ,(10, height-80))
        screen.blit(heart ,(10, height-110))
    elif shield==50:
        screen.blit(heart ,(10, height-40))
        screen.blit(heart ,(10, height-80))
    elif shield==100:
        screen.blit(heart ,(10, height-40))
    elif shield>100:
        shield+=50
        if shield==3500:
            game_over = True



    drawscore(screen, "Survive:"+str(round(score))+"s", 20,50,5)
    drawscore(screen, "SCORE:"+str(score1), 20, 450, 5)
    
    clock.tick(40)
    pygame.display.flip()

pygame.quit()