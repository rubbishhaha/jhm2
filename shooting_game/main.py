import pygame
import sys
from pygame.locals import *
import numpy as np
from setting import *

class game:
    def __init__(self):
        self.bg = pygame.display.set_mode((b,h))
        self.FPS = pygame.time.Clock()
        self.close_window = False
        self.status = "menu"
    def main(self):
        self.event()
        pygame.display.update()
    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.close_window = True
            print(event)
        self.FPS.tick(30)

    def main__init__(self):
        self.main_sprite = pygame.sprite.LayeredUpdates()
        
    def UI(self):
        self.event()


    def UI__init__(self):
        self.UI_sprite = pygame.sprite.LayeredUpdates()

pygame.init()
game_state = game()

while game_state.close_window == False:

    if pygame.key.get_pressed()[K_ESCAPE] == True:
        if game_state.status == "main":
            game_state.status = "menu"
        elif game_state.status == "menu":
            game_state.status = "main"
        
    if game_state.status == "main":
        game_state.main()
    elif game_state.status == "menu":
        game_state.UI()
    
    print(pygame.key.)

pygame.quit()
sys.exit()