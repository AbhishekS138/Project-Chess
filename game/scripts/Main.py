from game.scripts.Constants import *
from game.scripts.GameRenderer import GameRenderer
from game.scripts.GameController import GameController

import sys
import pygame

class Main:
    
    def __init__(self):
        pygame.init()                                                       #pygame initialization 
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))             #pygame surface initialization
        pygame.display.set_caption("Chess")                                 #surface title initialization
        
        #game surface, overlaid on self.surface
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        #menu surface, overlaid beside game_surface
        self.menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.renderer = GameRenderer(self.game_surface)                     #game renderer object
        self.controller = GameController(self.renderer)                     #game controller object
    
    #method for everything, called by run.py            
    def run(self):
        
        #always True results in a loop running indefinitely
        while True:
            
            self.menu_surface.fill((255, 255, 255))
            self.controller.display()                                       #initial display caller
            
            if self.controller.drag.dragging:                               #updates game_surface if board has a dragging state
                self.controller.drag.update_blit(self.game_surface)
            
            self.surface.blit(self.game_surface, (0, 0))                    #blits game_surface to surface at (0,0)
            self.surface.blit(self.menu_surface, (GAME_WIDTH, 0))           #blits menu_surface to surface at (width of game surface, 0)
            
            #iterates through all events defined in pygame
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:                    #mouse click handler
                    self.controller.mouse_click(event)
                elif event.type == pygame.MOUSEMOTION:                      #mouse movement handler
                    self.controller.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONUP:                    #mouse release handler
                    self.controller.mouse_release(event)
                elif event.type == pygame.KEYDOWN:                          #key press handler
                    self.controller.key_press(event)
                elif event.type == pygame.QUIT:
                    pygame.quit()                                           #quits pygame
                    sys.exit()                                              #exits the system
            
            #updates display property accordingly  
            pygame.display.update()