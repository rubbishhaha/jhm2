import pygame
import sys
from pygame.locals import *
from config import *
from sprite import *

class game:
    def __init__(self):
        self.bg = pygame.display.set_mode((b,h))
        self.FPS = pygame.time.Clock()
        self.close_window = False
        self.status = "ui"
        self.free_random = 0
        pygame.display.set_caption("simple shooting game")

        self.UI_sprite = pygame.sprite.LayeredUpdates()
        self.main_sprite = pygame.sprite.LayeredUpdates()
        self.all_sprite = pygame.sprite.LayeredUpdates()
        self.main_enemy_sprite = pygame.sprite.Group()
        self.main_teammate_sprite = pygame.sprite.Group()
    
    def main__init__(self):
        self.bg_image = pygame.transform.scale(pygame.image.load("asset/bg.png"),(b,h))
        self.player = player(self,"asset/player.png",(300,400))
        self.time = 0
        self.free_random = 0
    def main__term__(self):
        self.main_sprite.empty()
        self.all_sprite.empty()
        self.main_enemy_sprite.empty()
        self.main_teammate_sprite.empty()
    def main(self):
        self.event()
        self.main_draw()
        self.main_update()
        self.FPS.tick(FPS)
        pygame.display.update()
    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.close_window = True
            elif event.type == pygame.KEYDOWN:
                if event.key==K_ESCAPE:
                    self.ESC_get_pressed()
        self.command = pygame.key.get_pressed()
        self.mouse_codr = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()
    def main_update(self):
        self.main_sprite.update()
        self.sprite_exist()
        self.enemy_spawn()
        self.time += 1
    def enemy_spawn(self):
        enemy_spawner.continous_spawning_checking()
        if self.time%(round(FPS/ENEMY_SPAWN_RATE)) == 0:
            self.a1 = random.randint(0,5)
            match self.a1:
                case 0:
                    sim_enemy(self,"asset/heavy_enemy.png",(random.randint(0,b),-49),(100,100),health=100,speed=1,type="heavy_enemy"),
                case 1:
                    sim_enemy(self,"asset/sine_enemy.png",(random.randint(0,b),-49),(30,30),health=20,moving="sine_curve",sines=[8,0.2],speed=4,type="sine_enemy"),
                case 2:
                    sim_enemy(self,"asset/shooting_enemy.png",(random.randint(0,b),-49),(50,50),health=50,speed=2,shooting=True,bullet="sim_bullet",bullet_arg={"speed":10,"direction":270},type="shooting_enemy")
                case 3:
                    enemy_spawner.sine_enemy_team(self)
                case 4:
                    enemy_spawner.plain_trapper(self)
                case 5:
                    enemy_spawner.shotgun_shooter(self)

    def sprite_exist(self):
        for sprite in self.main_sprite:
            if sprite.asdf == False:
                sprite.kill()
            if sprite.exist == False:
                sprite.asdf = False
    def main_draw(self):
        self.bg.blit(self.bg_image, (0, 0,600,600))
        self.main_sprite.draw(self.bg)
    def UI_draw(self):
        if self.bluring_time > 0:
            self.bluring_factor = self.bluring_time/OPTION_APPEAR_TIME
            self.bg_image = pygame.transform.smoothscale(pygame.transform.smoothscale(self.bg_image_copy,((b-BACKGROUND_BLUR_RATE)*self.bluring_factor,(h-BACKGROUND_BLUR_RATE)*self.bluring_factor)),(b,h))
            self.bluring_time += -1
        self.bg.blit(self.bg_image, (0, 0,600,600))
        self.UI_sprite.draw(self.bg)
    def UI(self):
        self.event()
        self.UI_draw()
        self.UI_update()
        self.FPS.tick(FPS)
        pygame.display.update()
    def UI__init__(self):
        self.bg_image = pygame.transform.scale(pygame.image.load("asset/bg.png"),(b,h))
        self.bg_image.blit(pygame.image.load("asset/shoot_only.png"),(40,200))
        option(self,[180,400,167,91],"asset/option_spreadsheet.png",0,"main",image_no=2)
        self.bluring_time = 0
    def UI__term__(self):
        self.UI_sprite.empty()
        self.bg_image = pygame.transform.scale(pygame.image.load("asset/bg.png"),(b,h))
    def UI_update(self):
        self.UI_sprite.update()
    def menu__init__(self):
        self.bg_image_copy = self.bg.copy()
        self.bluring_time = OPTION_APPEAR_TIME
        option(self,[13,255,167,91],"asset/option_spreadsheet.png",0,"ui",image_no=0,apppear_method="boom")
        option(self,[180,255,167,91],"asset/option_spreadsheet.png",1,"main",image_no=1,apppear_method="boom")
        option(self,[347,255,167,91],"asset/option_spreadsheet.png",0,"main",image_no=2,apppear_method="boom")

    def ESC_get_pressed(self):
        if self.status == "main":
            self.status = "menu"
        elif self.status == "menu":
            self.status = "main"
        if self.status == "ui":
            self.close_window = True

class enemy_spawner():
    def continous_spawning_checking():
        for u in spawn_list:
            u[4] += 1
            if u[4] >= u[3]:
                if type(u[1][-1]) == dict:
                    u[0](*u[1][:-1],**u[1][-1])
                else:
                    u[0](*u[1])
                u[4] = 0
                u[2] += -1
                if u[2] <= 0:
                    spawn_list.remove(u)
    def continous_spawning_appending(func,data,time,num):
        spawn_list.append([func,data,num,time,0])

    def sine_enemy_team(self):
        self.free_random = random.randint(0,b)
        enemy_spawner.continous_spawning_appending(sim_enemy,[self,"asset/sine_enemy.png",(self.free_random,-49),(30,30),{"health":20,"moving":"sine_curve","sines":[8,0.07],"speed":4,"type":"sine_enemy"}],3,10)
    def plain_trapper(self):
        sim_enemy(self,"asset/trapper_enemy.png",(random.randint(0,b),-49),(70,70),health=30,speed=3,shooting=True,shooting_method="poly",shooting_method_c1=[2,0,180],bullet="lazer",bullet_arg={"speed":80,"hit_function":"invincible"},shooting_rate=15,type="shooting_enemy")
    def shotgun_shooter(self):
        sim_enemy(self,"asset/shooting_enemy.png",(random.randint(0,b),-49),(70,70),health=30,speed=2,shooting=True,shooting_method="poly",shooting_method_c1=[36,0,65],bullet="sim_bullet",bullet_arg={"speed":10,"hit_function":"explosion"},shooting_rate=0.5,type="shooting_enemy")

pygame.init()
game_state = game()

while game_state.close_window == False:
    game_state.UI__init__()
    while game_state.status == "ui" and game_state.close_window == False:
        game_state.UI()
    game_state.UI__term__()
    game_state.main__init__()
    while game_state.status == "main" and game_state.close_window == False:
        game_state.main()
        if game_state.status == "menu":
            game_state.menu__init__()
            while game_state.status == "menu" and game_state.close_window == False:
                game_state.UI()
            game_state.UI__term__()
    game_state.main__term__()


pygame.quit()
sys.exit()

# ui init, ui run, ui destroy, main init, main run, esc init,esc run , esc destroy, main destroy