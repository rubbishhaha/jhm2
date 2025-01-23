import pygame
import sys
from pygame.locals import *
import numpy as np
from setting import *
from sprite import *

class game:
    def __init__(self):
        self.bg = pygame.display.set_mode((b,h))
        self.FPS = pygame.time.Clock()
        self.close_window = False
        self.status = "menu"
        self.bg_image = pygame.transform.scale(pygame.image.load("asset/bg.png"),(b,h))

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
        self.FPS.tick(30)
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
        for sprite in self.all_sprite:
            if sprite.exist == False:
                sprite.kill()
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
sys.exit()