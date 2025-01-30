import pygame
from pygame.locals import *
import math
from config import *
import random

class player(pygame.sprite.Sprite):
    def __init__(self,game,png,init_pos,**kwargs):
        self.exist = True
        self.asdf = True
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
        self.damage = 0

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
                    if self.com in DODGE_DICT:
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
        if self.game.mouse_pressed[0]:
            if mode == 1:
                random_rect = rect.copy()
                random_rect.move_ip(random.randint(-30,30),random.randint(-30,30))
                sim_bullet(self.game,"asset/player_mode1_bullet.png",random_rect.center, (286*PLAYER_BULLET_RADIO,37*PLAYER_BULLET_RADIO),self.groups,4,speed=40)
class sim_bullet(pygame.sprite.Sprite):
    def __init__(self, game, png, init_pos, scale, groups,damage,**kwargs):
        self.exist = True
        self.asdf = True
        self.damage = damage
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
        self.groups = groups
        pygame.sprite.Sprite.__init__(self,groups)

        targeting(self)

        self.velocity = [self.arg_dict["speed"]*math.cos(math.radians(self.arg_dict["direction"])),-self.arg_dict["speed"]*math.sin(math.radians(self.arg_dict["direction"]))]
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(png),scale),self.arg_dict["direction"]).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=init_pos)

    def update(self, *args, **kwargs):
        self.move()
        if get_hit(self):
            self.hit()
    def move(self):
        self.rect[0] += self.velocity[0]
        self.rect[1] += self.velocity[1]
        if rect_in_game_area_x(self.rect) == False or rect_in_game_area_y(self.rect) == False:
            self.exist = False
    def explosion(self):
        self.exist = False
        fx_wave(self.game,self.rect.center,20,100,0.3,BLUE)
    def hit(self):
        match self.arg_dict["hit_function"]:
            case "explosion":
                self.explosion()
            case "invincible":
                pass
def targeting(self):
    if self.game.main_enemy_sprite.has(self):
        self.target = self.game.main_teammate_sprite
    elif self.game.main_teammate_sprite.has(self):
        self.target = self.game.main_enemy_sprite
        
def rect_in_game_area_x(rect):
    if rect.center[0] > b + 100 or rect.center[0] < -100:
        return False
    else:
        return True
def rect_in_game_area_y(rect):
    if rect.center[1] > h + 100 or rect.center[1] < -100:
        return False
    else:
        return True

def get_hit(self,**kwarg):
    return pygame.sprite.spritecollide(self, self.target,False)

class sim_enemy(pygame.sprite.Sprite):
    def __init__(self,game,png,init_pos,scale,**kwargs):
        self.exist = True
        self.asdf = True
        self.image = pygame.transform.scale(pygame.image.load(png),scale).convert()
        self.image.set_colorkey(BLACK)
        self.game = game
        self.time = 0
        self.arg_dict = {
            "direction":270,
            "speed":1,
            "shooting":False,
            "health":20,
            "moving":"straight_line",
            "sines":False,
            "shooting":True,
            "shooting_method":"",
            "bullet":None,
            "bullet_arg":None,
            "shooting_rate":ENEMY_SHOOTING_RATE,
            "type":"sim_enemy"
        }
        for i,val in kwargs.items():
            self.arg_dict[i] = val
        self._layer = ENEMY_LAYER 
        self.groups = [game.all_sprite,game.main_sprite,game.main_enemy_sprite]
        pygame.sprite.Sprite.__init__(self,self.groups)

        targeting(self)

        self.velocity = [self.arg_dict["speed"]*math.cos(math.radians(self.arg_dict["direction"])),-self.arg_dict["speed"]*math.sin(math.radians(self.arg_dict["direction"]))]
        self.i_image = pygame.transform.rotate(self.image,self.arg_dict["direction"])
        self.image = self.i_image
        self.rect = self.image.get_rect(center=init_pos)
        self.health = self.arg_dict["health"]
    def update(self, *args, **kwargs):
        self.move()
        if get_hit(self):
            self.hit()
        if self.arg_dict["shooting"]:
            self.shooting_mth()
        self.sp_action()
        self.time += 1
        #pygame.draw.rect(self.game.bg,BLUE,self.rect,2)
    def move(self):
        self.rect[0] += self.velocity[0]
        self.rect[1] += self.velocity[1]
        if self.arg_dict["moving"] == "sine_curve":
            self.rect[0] += self.arg_dict["sines"][0]*math.sin(self.time*self.arg_dict["sines"][1])

        if rect_in_game_area_y(self.rect) == False:
            self.exist = False
    def hit(self):
        for i in get_hit(self):
            self.health += -i.damage
            if self.health <= 0:
                self.exist = False
                fx_wave(self.game,self.rect.center,50,250,0.5,RED)
    def shooting(self):
            match self.arg_dict["bullet"]:
                case "sim_bullet":
                    sim_bullet(self.game,"asset/enemy_bullet.png",self.rect.center, (256*ENEMY_BULLET_RADIO,100*ENEMY_BULLET_RADIO),self.groups,3,**self.arg_dict["bullet_arg"])
                case "lazer":
                    sim_bullet(self.game,"asset/enemy_bullet.png",self.rect.center, (8192*ENEMY_BULLET_RADIO,100*ENEMY_BULLET_RADIO),self.groups,1,**self.arg_dict["bullet_arg"])
    def sp_action(self):
        if self.arg_dict["type"] == "sine_enemy":
            self.image = pygame.transform.rotate(self.i_image,6.28*self.arg_dict["sines"][0]*math.sin(self.time*self.arg_dict["sines"][1]))
    def shooting_mth(self):
        if self.time%(round(FPS/self.arg_dict["shooting_rate"])) == 0:
            match self.arg_dict["shooting_method"]:
                case "":
                    self.shooting()
                case "poly":
                    for i in range(self.arg_dict["shooting_method_c1"][0]):
                        self.arg_dict["bullet_arg"]["direction"] = self.arg_dict["shooting_method_c1"][1]+i*self.arg_dict["shooting_method_c1"][2]
                        self.shooting()


class fx_wave(pygame.sprite.Sprite):
    def __init__(self,game,pos,i_s,t_s,t,color):
        self.game = game
        self.exist = True
        self.asdf = True
        self._age = pygame.image.load("asset/fx_wave.png").convert()
        self._age.set_colorkey(BLACK)
        self._age.fill(color, special_flags=pygame.BLEND_RGBA_MIN)
        self.image = pygame.transform.scale(self._age, (0,0))
        self.time = 0
        self.frame = t*30
        self._layer = FX_LAYER 
        self.groups = game.all_sprite,game.main_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.rect = pygame.rect.Rect(0,0,i_s,i_s)
        self.rect.center = pos
        self.i_s = i_s
        self.scale_speed = (t_s-i_s)/self.frame
    def update(self, *args, **kwargs):
        self.image = pygame.transform.scale(self._age,(self.time*self.scale_speed+self.i_s,self.time*self.scale_speed+self.i_s))
        self.image.set_alpha(255*(1-self.time/self.frame))
        self.rect[0] -= self.scale_speed/2
        self.rect[1] -= self.scale_speed/2
        #self.game.bg.blit(self.image,self.rect)
        #pygame.draw.rect(self.game.bg, BLUE, self.rect, 2)
        self.time += 1
        if self.time > self.frame:
            self.exist = False

class option(pygame.sprite.Sprite):
    def __init__(self,game,rect,image,func,value,image_no=-1,apppear_method=None):
        self.game = game
        self.rect = pygame.rect.Rect(rect)
        self.r_rect = self.rect.copy()
        if image_no != -1:
            self.image = pygame.Surface((self.rect[2],self.rect[3])).convert()
            self.a = pygame.image.load(image)
            self.image.blit(self.a,(0,0),(167*image_no,0,self.rect[2],self.rect[3]))
        else:
            self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(BLACK)
        self.r_image = self.image
        match apppear_method:
            case None:
                self.appear_time = 0
            case "boom":
                self.appear_time = OPTION_APPEAR_TIME
                self.appear_method = "boom"
                self.image = pygame.Surface((0,0))
        self.func = func
        self.value = value
        self._layer = FX_LAYER 
        self.groups = game.all_sprite,game.UI_sprite
        self.grown = False
        self.g_x = (OPTION_GROW_RATIO-1)*self.r_rect[2]
        self.g_Y = (OPTION_GROW_RATIO-1)*self.r_rect[3]
        pygame.sprite.Sprite.__init__(self,self.groups)
    def update(self, *args, **kwargs):
        match self.mouse_get_pressed():
            case 0:
                self.de_grow()
            case 1:
                self.grow()
            case 2:
                self.execute()
        if self.appear_time > 0:
            self.cg_in()
    def mouse_get_pressed(self):
        if self.r_rect.collidepoint(self.game.mouse_codr):
            if self.game.mouse_pressed[0]:
                return 2
            else:
                return 1
        else:
            return 0
    def grow(self):
        self.n_x = math.floor(self.g_x-self.rect[2]+self.r_rect[2])/2
        self.n_y = math.floor(self.g_x-self.rect[3]+self.r_rect[3])/2
        if self.n_x <= 1:
            self.n_x = 0
            self.rect = pygame.Rect(self.r_rect[0]-self.g_x/2,self.r_rect[1]-self.g_Y/2,self.r_rect[2]+self.g_x,self.r_rect[3]+self.g_Y)
        if self.n_y <= 1:
            self.n_y = 0
        self.rect = pygame.rect.Rect(self.rect[0]-self.n_x/2,self.rect[1]-self.n_y/2,self.rect[2]+self.n_x,self.rect[3]+self.n_y)
        self.image = pygame.transform.scale(self.r_image,(self.rect[2],self.rect[3]))
        
    def de_grow(self):
        self.n_x = math.floor(-self.rect[2]+self.r_rect[2])/2
        self.n_y = math.floor(-self.rect[3]+self.r_rect[3])/2
        if self.n_x >= -1:
            self.n_x = 0
            self.rect = self.r_rect
        if self.n_y >= -1:
            self.n_y = 0
        self.rect = pygame.rect.Rect(self.rect[0]-self.n_x/2,self.rect[1]-self.n_y/2,self.rect[2]+self.n_x,self.rect[3]+self.n_y)
        self.image = pygame.transform.scale(self.r_image,(self.rect[2],self.rect[3]))
    def execute(self):
        match self.func:
            case 0:
                self.game.status = self.value
            case 1:
                self.game.status = self.value
                self.game.main__term__()
                self.game.main__init__()
    def cg_in(self):
        match self.appear_method:
            case "boom":
                self.a1 = (OPTION_APPEAR_TIME-self.appear_time)/OPTION_APPEAR_TIME
                self.image = pygame.transform.scale(self.r_image,(self.r_rect[2]*self.a1,self.r_rect[3]*self.a1))
                self.appear_time += -1
    
        