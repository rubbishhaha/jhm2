import pygame
import sys
from pygame.locals import *
import math
import pygame.docs
import pygame.docs.generated
import pygame.docs.generated._images
from setting import *
import random

class player(pygame.sprite.Sprite):
    def __init__(self,game,png,init_pos,**kwargs):
        self.exist = True
        self.init_image = pygame.transform.scale(pygame.image.load(png),[30,30]).convert()
        self.init_image.set_alpha(PLAYER_TRANSPARENT_CONSTANT)
        self.image = self.init_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(topleft=init_pos)
        self.init_rect = self.rect
        self.game = game
        self.arg = kwargs
        self._layer = PLAYER_LAYER 
        self.groups = [game.all_sprite,game.main_sprite,game.main_teammate_sprite]
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.velocity = [0,0]
        self.rotat = 0
        self.speed = 0
        self.dodge_cd = 0
        self.weapon_mode = 1

        sim_enemy(self.game,"asset/sim_enemy.png",(300,300),(50,50))
    def update(self, *args, **kwargs):
        self.move()
        self.rotat = self.rotation(self.velocity[0],self.velocity[1],self.rotat,self.speed)
        self.image_process()
        self.shoot(self.rect,self.weapon_mode)

    def image_process(self):
        self.image , self.rect = self.animation(self.init_image,self.rotat,self.init_rect,self.rect,self.speed)

        #pygame.draw.rect(self.game.bg, BLUE, self.rect, 2)
        pygame.draw.circle(self.game.bg, GREEN, self.rect.center, 5, 3)
    def move(self):
        self.com = ""
        if self.game.command[K_w]:
            self.com += "w"
            self.velocity[1] += -PLAYER_SPEED if self.velocity[1] > -PLAYER_MAXIMUM_SPEED and self.speed < PLAYER_MAXIMUM_SPEED else 0
        if self.game.command[K_a]:
            self.com += "a"
            self.velocity[0] += -PLAYER_SPEED if self.velocity[0] > -PLAYER_MAXIMUM_SPEED and self.speed < PLAYER_MAXIMUM_SPEED else 0
        if self.game.command[K_s]:
            if len(self.com) < 2:
                self.com += "s" 
            self.velocity[1] += PLAYER_SPEED if self.velocity[1] < PLAYER_MAXIMUM_SPEED and self.speed < PLAYER_MAXIMUM_SPEED else 0
        if self.game.command[K_d]:
            if len(self.com) < 2:
                self.com += "d"
            self.velocity[0] += PLAYER_SPEED if self.velocity[0] < PLAYER_MAXIMUM_SPEED and self.speed < PLAYER_MAXIMUM_SPEED else 0
        if self.game.command[K_SPACE]:
            if self.dodge_cd == 0:
                if self.com == "":
                    self.velocity[0] = PLAYER_DODGE_SPEED*math.cos(math.radians(self.r2))
                    self.velocity[1] = -PLAYER_DODGE_SPEED*math.sin(math.radians(self.r2))
                else:
                    self.velocity = DODGE_DICT[self.com]
                self.dodge_cd = 10
        if self.dodge_cd > 0:
            self.dodge_cd += -1
        self.velocity = [i*0.8 if abs(i) > 0.1 else 0 for i in self.velocity]
        self.rect[0] += round(self.velocity[0])
        self.rect[1] += round(self.velocity[1])
        if self.rect.center[0] < 5:
            self.rect.centerx = 5
        elif self.rect.center[0] > b-5:
            self.rect.centerx = b-5
        if self.rect.center[1] < 5:
            self.rect.centery = 5
        elif self.rect.center[1] > h-5:
            self.rect.centery = h-5
        self.speed = math.sqrt(math.pow(self.velocity[0],2) + math.pow(self.velocity[1],2))
    def rotation(self,vx,vy,r,s):
        if vx == 0:
            if vy == 0:
                self.r2 = r
            else:
                self.r2 = 270 if vy > 0 else 90
        elif vy == 0:
            self.r2 = 0 if vx > 0 else 180
        else:
            self.r2 = math.degrees(math.atan2(vx,vy)) - 90 # if vx >= 0 else -90 + math.degrees(math.atan2(vy,vx))

        if abs(self.r2-r) < abs(self.r2-r-360) and abs(self.r2-r) < abs(self.r2-r+360):
            self.a2 = self.r2-r
        elif abs(self.r2-r-360) > abs(self.r2-r+360):
            self.a2 = self.r2-r+360
        else:
            self.a2 = self.r2-r-360

        self.a1 = r + round(self.a2*s/PLAYER_ROTATION_CONSTANT)
        #print(self.velocity, self.a1, self.r2, self.dodge_cd)

        while self.a1 > 360 or self.a1 < 0:
            self.a1 = self.a1-360 if self.a1 > 360 else self.a1 + 360
        return self.a1
    
    def animation(self,image,r,rect,nr,s):
        self.a4_Im = pygame.transform.scale(image,(rect[2]*(1+s*MOVE_ANIMATION_IMAGE_SCALE_CONSTANT),rect[3]*(1-s*MOVE_ANIMATION_IMAGE_SCALE_CONSTANT)))
        self.a4_Im = pygame.transform.rotate(self.a4_Im,r)
        self.a5_rect = self.a4_Im.get_rect(topleft=nr.topleft)
        return self.a4_Im, self.a5_rect
    def shoot(self,rect,mode):
        if mode == 1:
            random_rect = rect.copy()
            random_rect.move_ip(random.randint(-30,30),random.randint(-30,30))
            sim_bullet(self.game,"asset/player_mode1_bullet.png",random_rect.center, (286*PLAYER_BULLET_RADIO,37*PLAYER_BULLET_RADIO),self.groups,speed=40)
class sim_bullet(pygame.sprite.Sprite):
    def __init__(self, game, png, init_pos, scale, groups,**kwargs):
        self.exist = True
        self.image = pygame.transform.scale(pygame.image.load(png),scale).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=init_pos)
        self.game = game
        self.arg_dict = {
            "direction":90,
            "hit_function": "explosion",
            "speed":10,
            "tracking":False
        }
        for i,val in kwargs.items():
            self.arg_dict[i] = val
        self._layer = FX_LAYER 
        pygame.sprite.Sprite.__init__(self,groups)

        target(self,self.game,self.groups)

        self.velocity = [self.arg_dict["speed"]*math.cos(math.radians(self.arg_dict["direction"])),-self.arg_dict["speed"]*math.sin(math.radians(self.arg_dict["direction"]))]
        self.image = pygame.transform.rotate(self.image,self.arg_dict["direction"])
        self.rect = self.image.get_rect(center=init_pos)

    def update(self, *args, **kwargs):
        self.move()
        self.hit()
    def move(self):
        self.rect[0] += self.velocity[0]
        self.rect[1] += self.velocity[1]
        if rect_in_game_area(self.rect) == False:
            self.kill()
    def hit(self):
        if pygame.sprite.spritecollide(self, self.target,False):
            if self.arg_dict["hit_function"] == "explosion":
                self.explosion()
    
    def explosion(self):
        self.exist = False
        fx_wave(self.game,self.rect.center,20,100,0.2)
        
def rect_in_game_area(rect):
    if rect[0] > b + 100 or rect[0] < -100 or rect[1] > h + 100 or rect[1] < -100:
        return False
    else:
        return True
def target(self,game,group):
    if pygame.sprite.Group.has(self.game.main_teammate_sprite,self):
        self.target = self.game.main_enemy_sprite
    elif pygame.sprite.Group.has(self.game.main_enemy_sprite,self):
        self.target = self.game.main_teammate_sprite

class sim_enemy(pygame.sprite.Sprite):
    def __init__(self,game,png,init_pos,scale,**kwargs):
        self.exist = True
        self.image = pygame.transform.scale(pygame.image.load(png),[30,30]).convert()
        self.image.set_colorkey(BLACK)
        self.game = game
        self.arg_dict = {
            "direction":270,
            "speed":1,
            "shooting":False,
            "health":20
        }
        self._layer = ENEMY_LAYER 
        self.groups = game.all_sprite,game.main_sprite,game.main_enemy_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)
    
        self.velocity = [self.arg_dict["speed"]*math.cos(math.radians(self.arg_dict["direction"])),-self.arg_dict["speed"]*math.sin(math.radians(self.arg_dict["direction"]))]
        self.image = pygame.transform.rotate(self.image,self.arg_dict["direction"])
        self.rect = self.image.get_rect(center=init_pos)
    def update(self, *args, **kwargs):
        self.move()
    def move(self):
        self.rect[0] += self.velocity[0]
        self.rect[1] += self.velocity[1]
        if rect_in_game_area(self.rect) == False:
            self.kill()

class fx_wave(pygame.sprite.Sprite):
    def __init__(self,game,pos,i_s,t_s,t):
        self.game = game
        self.i_image = pygame.image.load("asset/fx_wave.png").convert()
        self.i_image.set_colorkey(BLACK)
        self.i_image.set_alpha(100)
        self.count = 0
        self.frame = t*30
        self._layer = FX_LAYER 
        self.groups = game.sp_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = list(pos)
        self.pos[0] += -i_s/2
        self.pos[1] += -i_s/2
        self.i_s = i_s
        self.scale_speed = (t_s-i_s)/self.frame
    def update(self, *args, **kwargs):
        for i in range(self.count):
            self.game.bg.blit(pygame.transform.scale(self.i_image,(i*self.scale_speed+self.i_s,i*self.scale_speed+self.i_s)),(self.pos[0]-i*self.scale_speed/2,self.pos[1]-i*self.scale_speed/2))
        self.count += 1
        if self.count > self.frame:
            self.kill()
        
        