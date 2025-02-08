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
        
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.game = Game()
        self.drag = Drag()
                
    def run(self):  
        #Variables to be used
        _game_surface = self.game_surface
        _menu_surface = self.menu_surface
        
        _surface = self.surface
        _game = self.game
        _board = _game.board
        _drag = _game.drag
        
        while True:
            
            _menu_surface.fill((255, 255, 255))
            
            #Display methods
            _game.display_board(_game_surface)
            _game.display_moves(_game_surface)
            _game.display_pieces(_game_surface)
            
            if _drag.dragging:
                _drag.update_blit(_game_surface)
            
            _surface.blit(_game_surface, (0, 0))
            _surface.blit(_menu_surface, (GAME_WIDTH, 0))
            
            
            for event in pygame.event.get():
                
                #On mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    _drag.updatePos(event.pos)
                    
                    clicked_row = _drag.mouse_y // SQUARE_SIZE
                    clicked_col = _drag.mouse_x // SQUARE_SIZE
                    
                    #Check if piece is clicked
                    if _board.squares[clicked_row][clicked_col].has_piece():
                        piece = _board.squares[clicked_row][clicked_col].piece
                        _board.calc_moves(piece, clicked_row, clicked_col)
                        _drag.initialPos(event.pos)
                        _drag.dragSet(piece)
                        
                        #Display methods
                        _game.display_board(_game_surface)
                        _game.display_moves(_game_surface)
                        _game.display_pieces(_game_surface)
                
                #On mouse movement
                elif event.type == pygame.MOUSEMOTION:
                    if _drag.dragging:
                        _drag.updatePos(event.pos)
                        
                        #Display methods
                        _game.display_board(_game_surface)
                        _game.display_moves(_game_surface)
                        _drag.update_blit(_game_surface)
                
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