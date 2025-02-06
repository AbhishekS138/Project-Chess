import sys
import pygame
from game.scripts.Constants import *
from game.scripts.Game import Game
from game.scripts.logic.Drag import Drag
class Main:
    
    def __init__(self): 
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        
        self.gameSurface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.menuSurface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.game = Game()
        self.drag = Drag()
                
    def run(self):  
        #Variables to be used
        _gameSurface = self.gameSurface
        _menuSurface = self.menuSurface
        
        _surface = self.surface
        _game = self.game
        _board = self.game.board
        _drag = self.drag
        
        while True:
            
            _menuSurface.fill((255, 255, 255))
            
            _game.displayBoard(_gameSurface)
            _game.displayPieces(_gameSurface, self.drag)
            
            if _drag.dragging:
                _drag.updateBlit(_gameSurface)
            
            _surface.blit(_gameSurface, (0, 0))
            _surface.blit(_menuSurface, (GAME_WIDTH, 0))
            
            
            for event in pygame.event.get():
                
                #On mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    _drag.updatePos(event.pos)
                    
                    clickedRow = _drag.mouseY // SQUARE_SIZE
                    clickedCol = _drag.mouseX // SQUARE_SIZE
                    
                    #Check if piece is clicked
                    if _board.squares[clickedRow][clickedCol].hasPiece():
                        piece = _board.squares[clickedRow][clickedCol].piece
                        _drag.initialPos(event.pos)
                        _drag.dragSet(piece)
                
                #On mouse movement
                elif event.type == pygame.MOUSEMOTION:
                    if _drag.dragging:
                        _drag.updatePos(event.pos)
                        _game.displayBoard(_gameSurface)
                        _drag.updateBlit(_gameSurface)
                
                #On mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    _drag.undragSet()
                
                #On window close
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
    
main = Main()
main.run()