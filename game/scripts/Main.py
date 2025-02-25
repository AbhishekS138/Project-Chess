from game.scripts.Constants import *
from game.scripts.Game import Game
from game.scripts.gui.Square import Square
from game.scripts.logic.Move import Move

import sys
import pygame

class Main:
    
    def __init__(self):
        pygame.init()                                               #pygame initialization 
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))     #pygame surface initialization
        pygame.display.set_caption("Chess")                         #surface title initialization
        
        #game surface, overlaid on self.surface
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        #menu surface, overlaid beside game_surface
        self.menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        self.game = Game(self.game_surface)      #game object
    
    #method for everything, called by run.py            
    def run(self):  
        #Variables to be used, set to private since they are only used in Main class (not necessary)
        _game_surface = self.game_surface       #private game surface
        _menu_surface = self.menu_surface       #private menu surface
        _surface = self.surface                 #private main surface
        _game = self.game                       #private game object
        _board = _game.board                    #private board object of game object (initialized in Game class)
        _drag = _game.drag                      #private drag object of game object (initialized in Game class)
        
        #method to call display methods of Game class, everything is rendered on _game_surface
        def display():   
            _game.display_board()              #first render for game board
            _game.display_last_move()          #second render for last moves
            _game.display_moves()              #third render for valid moves
            _game.display_pieces()             #fourth render for pieces
        
        #always True results in a loop running indefinitely
        while True:
            
            _menu_surface.fill((255, 255, 255))
            
            display()                                           #initial display caller
            
            if _drag.dragging:                                  #updates game_surface if board has a dragging state
                _drag.update_blit(_game_surface)
            
            _surface.blit(_game_surface, (0, 0))                #blits game_surface to surface at (0,0)
            _surface.blit(_menu_surface, (GAME_WIDTH, 0))       #blits menu_surface to surface at (width of game surface, 0)
            
            #iterates through all events defined in pygame
            for event in pygame.event.get():
                
                #on mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    _drag.update_pos(event.pos)                                             #updates mouse coordinates of Drag object
                    
                    clicked_row = _drag.mouse_y // SQUARE_SIZE                              #gets row number from Drag object's mouse_y
                    clicked_col = _drag.mouse_x // SQUARE_SIZE                              #gets col number from Drag object's mouse_x
                    
                    if Square.in_range(clicked_row, clicked_col):                           #checks if click is within board range
                        if _board.squares[clicked_row][clicked_col].has_piece():            #checks if clicked Square has any piece
                            piece = _board.squares[clicked_row][clicked_col].piece          #gets the piece
                            
                            if piece.color == _game.next_turn_player:                       #if clicked piece has same color as current player
                                _board.calc_moves(piece, clicked_row, clicked_col, True)    #calculates valid moves for clicked piece
                                _drag.initial_pos(event.pos)                                #sets initial row and col attributes of Drag object
                                _drag.drag_set(piece)                                       #sets dragging state to True of Drag object
                                
                                display()                                                   #displays everything
                
                #on mouse movement
                elif event.type == pygame.MOUSEMOTION:
                    if _drag.dragging:                                                      #updates game_surface if board has a dragging state
                        _drag.update_pos(event.pos)
                        
                        display()                                                           #displays everything
                        
                        _drag.update_blit(_game_surface)                                    #renders the piece being dragged
                
                #On mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if _drag.dragging:                                                      #updates game_surface if board has a dragging state
                        _drag.update_pos(event.pos)
                        final_row = _drag.mouse_y // SQUARE_SIZE                            #gets row number from Drag object's mouse_y                            
                        final_col = _drag.mouse_x // SQUARE_SIZE                            #gets col number from Drag object's mouse_x
                        
                        initial = Square(_drag.initial_row, _drag.initial_col)              #creates initial and final Square objects
                        final = Square(final_row, final_col)
                        move = Move(initial, final)                                         #creates Move object
                        
                        if _board.valid_move(_drag.piece, move):                            #if move is within list of calculated valid moves
                            captured = _board.squares[final_row][final_col].has_piece()     #boolean flag for capturing a piece
                            _board.final_move(_drag.piece, move)                            #sets the board according to the move
                            _game.move_capture_sound(captured)                              #plays capture or move sound
                            
                            display()                                                       #displays everything
                            
                            #debug print, prints the move made
                            print(f'{piece.color} {piece.name} moved from {chr(initial.col+97)}{ROWS-initial.row} to {chr(final.col+97)}{ROWS-final.row}')
                        
                        else:                                                               #plays illegal sound if move made is invalid
                            _game.illegal_sound() 
                        
                        if _drag.piece.moved == True:
                            _drag.piece.moved = False                                       #sets moved flag of piece to False
                            _game.next_turn()                                               #switches to the other color
                    
                    _drag.undrag_set()                                                      #sets dragging state to False
                    
                elif event.type == pygame.KEYDOWN:
                    #on key press(t)
                    if event.key == pygame.K_t:
                        _game.config.change_theme()                                         #change theme on key press t
                        display()                                                           #displays everything
                    
                    #on key press(r)    
                    if event.key == pygame.K_r:
                        _game.reset()                                                       #restarts Game object on game_screen
                        _game = self.game                                                   #resets _game object
                        _board = _game.board                                                #resets _board object
                        _drag = _game.drag                                                  #resets _drag object
        
                
                #On window close
                elif event.type == pygame.QUIT:
                    pygame.quit()                                                           #quits pygame
                    sys.exit()                                                              #closes execution
            
            #updates display property accordingly        
            pygame.display.update()