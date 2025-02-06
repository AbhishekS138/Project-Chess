import sys
import pygame
from game.scripts.Constants import *
from game.scripts.Game import Game

class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        
        self.gameScreen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.menuScreen = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.game = Game()
                
    def run(self):
        while True:
            #Variables to be used
            _screen = self.screen
            _game = self.game
            _gameScreen = self.gameScreen
            _menuScreen = self.menuScreen
            
            _menuScreen.fill((255, 255, 255))
            
            _game.displayBoard(_gameScreen)
            _game.displayPieces(_gameScreen)
            _screen.blit(_gameScreen, (0, 0))
            _screen.blit(_menuScreen, (GAME_WIDTH, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
    
main = Main()
main.run()