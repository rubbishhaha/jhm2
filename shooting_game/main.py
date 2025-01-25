import pygame
from pygame.locals import *
from config import *
from sprite import *

class game:
    def __init__(self):
        self.bg = pygame.display.set_mode((b,h))
        self.FPS = pygame.time.Clock()
        self.close_window = False
        self.status = "menu"
        self.bg_image = pygame.transform.scale(pygame.image.load("asset/bg.png"),(b,h))
        self.time = 0
        pygame.display.set_caption("cnmb nigger")

        self.UI_sprite = pygame.sprite.LayeredUpdates()
        self.main_sprite = pygame.sprite.LayeredUpdates()
        self.all_sprite = pygame.sprite.LayeredUpdates()
        self.main_enemy_sprite = pygame.sprite.Group()
        self.main_teammate_sprite = pygame.sprite.Group()
        self.sp_sprite = pygame.sprite.LayeredUpdates()

        self.player = player(self,"asset/player.png",(0,0))

    def main(self):
        self.event()
        self.draw()
        self.update()
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
    def update(self):
        self.main_sprite.update()
        self.sp_sprite.update()
        self.sprite_exist()
        self.enemy_spawn()
        self.time += 1
    def enemy_spawn(self):
        if self.time%(ENEMY_SPAWN_RATE*FPS) == 0:
            self.a1 = random.randint(0,2)
            if self.a1 == 0:
                sim_enemy(self,"asset/sim_enemy.png",(random.randint(0,600),-49),(100,100),health=150,speed=1),
            elif self.a1 == 1:
                sim_enemy(self,"asset/sim_enemy.png",(random.randint(0,600),-49),(30,30),health=20,moving="sine_curve",sines=[8,0.2],speed=4),
            elif self.a1 == 2:
                sim_enemy(self,"asset/sim_enemy.png",(random.randint(0,600),-49),(50,50),health=70,speed=2,shooting=True,bullet="sim_bullet")

    def sprite_exist(self):
        for sprite in self.all_sprite:
            if sprite.asdf == False:
                sprite.kill()
            if sprite.exist == False:
                sprite.asdf = False
    def draw(self):
        self.bg.blit(self.bg_image, (0, 0,600,600))
        self.main_sprite.draw(self.bg)
    def main_run__init__(self):
        pass
    def UI(self):
        pass
    def UI__init__(self):
        pass
    def ESC_get_pressed(self):
        if self.status == "main":
            self.status = "menu"
            self.UI__init__()
        elif self.status == "menu":
            self.status = "main"
            self.main_run__init__()

pygame.init()
game_state = game()

while game_state.close_window == False:
    game_state.main()
    if game_state.status == "main":
        game_state.main_run()
    elif game_state.status == "menu":
        game_state.UI()
    

pygame.quit()