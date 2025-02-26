from game.scripts.Constants import *
from game.scripts.GameRenderer import GameRenderer
from game.scripts.GameController import GameController

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
        self.renderer = GameRenderer(self.game_surface)             #game renderer object
        self.controller = GameController(self.renderer)             #game controller object
    
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
            
            
# from game.scripts.Constants import *
# from game.scripts.GameRenderer import GameRenderer
# from game.scripts.gui.Square import Square
# from game.scripts.logic.Move import Move

# import sys
# import pygame

# class Main:
    
#     def __init__(self):
#         pygame.init()                                               #pygame initialization 
#         self.surface = pygame.display.set_mode((WIDTH, HEIGHT))     #pygame surface initialization
#         pygame.display.set_caption("Chess")                         #surface title initialization
        
#         #game surface, overlaid on self.surface
#         self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
#         #menu surface, overlaid beside game_surface
#         self.menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
#         self.game_renderer = GameRenderer(self.game_surface)        #game renderer object
    
#     #method for everything, called by run.py            
#     def run(self):  
#         #Variables to be used, set to private since they are only used in Main class (not necessary)
#         game_surface = self.game_surface                #private game surface
#         menu_surface = self.menu_surface                #private menu surface
#         surface = self.surface                          #private main surface
#         game_renderer = self.game_renderer              #private game object
#         board = game_renderer.board                     #private board object of game object (initialized in Game class)
#         drag = game_renderer.drag                       #private drag object of game object (initialized in Game class)
        
#         #method to call display methods of Game class, everything is rendered on _game_surface
#         def display():   
#             game_renderer.display_board()               #first render for game board
#             game_renderer.display_last_move()           #second render for last moves
#             game_renderer.display_moves()               #third render for valid moves
#             game_renderer.display_pieces()              #fourth render for pieces
        
#         #always True results in a loop running indefinitely
#         while True:
            
#             menu_surface.fill((255, 255, 255))
            
#             display()                                           #initial display caller
            
#             if drag.dragging:                                   #updates game_surface if board has a dragging state
#                 drag.update_blit(game_surface)
            
#             surface.blit(game_surface, (0, 0))                  #blits game_surface to surface at (0,0)
#             surface.blit(menu_surface, (GAME_WIDTH, 0))         #blits menu_surface to surface at (width of game surface, 0)
            
#             #iterates through all events defined in pygame
#             for event in pygame.event.get():
                
#                 #on mouse click
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     drag.update_pos(event.pos)                                              #updates mouse coordinates of Drag object
                    
#                     clicked_row = drag.mouse_y // SQUARE_SIZE                               #gets row number from Drag object's mouse_y
#                     clicked_col = drag.mouse_x // SQUARE_SIZE                               #gets col number from Drag object's mouse_x
                    
#                     if Square.in_range(clicked_row, clicked_col):                           #checks if click is within board range
#                         if board.squares[clicked_row][clicked_col].has_piece():             #checks if clicked Square has any piece
#                             piece = board.squares[clicked_row][clicked_col].piece           #gets the piece
                            
#                             if piece.color == game_renderer.next_turn_player:               #if clicked piece has same color as current player
#                                 board.calc_moves(piece, clicked_row, clicked_col, True)     #calculates valid moves for clicked piece
#                                 drag.initial_pos(event.pos)                                 #sets initial row and col attributes of Drag object
#                                 drag.drag_set(piece)                                        #sets dragging state to True of Drag object
                                
#                                 display()                                                   #displays everything
                
#                 #on mouse movement
#                 elif event.type == pygame.MOUSEMOTION:
#                     if drag.dragging:                                                       #updates game_surface if board has a dragging state
#                         drag.update_pos(event.pos)
                        
#                         display()                                                           #displays everything
                        
#                         drag.update_blit(game_surface)                                      #renders the piece being dragged
                
#                 #On mouse release
#                 elif event.type == pygame.MOUSEBUTTONUP:
#                     if drag.dragging:                                                       #updates game_surface if board has a dragging state
#                         drag.update_pos(event.pos)
#                         final_row = drag.mouse_y // SQUARE_SIZE                             #gets row number from Drag object's mouse_y                            
#                         final_col = drag.mouse_x // SQUARE_SIZE                             #gets col number from Drag object's mouse_x
                        
#                         initial = Square(drag.initial_row, drag.initial_col)                #creates initial and final Square objects
#                         final = Square(final_row, final_col)
#                         move = Move(initial, final)                                             #creates Move object
                        
#                         if board.valid_move(drag.piece, move):                              #if move is within list of calculated valid moves
#                             captured = board.squares[final_row][final_col].has_piece()      #boolean flag for capturing a piece
#                             board.final_move(drag.piece, move)                              #sets the board according to the move
#                             game_renderer.move_capture_sound(captured)                      #plays capture or move sound
                            
#                             display()                                                       #displays everything
                            
#                             #debug print, prints the move made
#                             print(f'{piece.color} {piece.name} moved from {chr(initial.col+97)}{ROWS-initial.row} to {chr(final.col+97)}{ROWS-final.row}')
                        
#                         else:                                                               #plays illegal sound if move made is invalid
#                             game_renderer.illegal_sound() 
                        
#                         if drag.piece.moved == True:
#                             drag.piece.moved = False                                        #sets moved flag of piece to False
#                             game_renderer.next_turn()                                       #switches to the other color
                    
#                     drag.undrag_set()                                                       #sets dragging state to False
                    
#                 elif event.type == pygame.KEYDOWN:
#                     #on key press(t)
#                     if event.key == pygame.K_t:
#                         game_renderer.config.change_theme()                                 #change theme on key press t
#                         display()                                                           #displays everything
                    
#                     #on key press(r)    
#                     if event.key == pygame.K_r:
#                         game_renderer.reset()                                               #restarts Game object on game_screen
#                         game_renderer = self.game_renderer                                  #resets _game object
#                         board = game_renderer.board                                         #resets _board object
#                         drag = game_renderer.drag                                           #resets _drag object
        
                
#                 #On window close
#                 elif event.type == pygame.QUIT:
#                     pygame.quit()                                                           #quits pygame
#                     sys.exit()                                                              #closes execution
            
#             #updates display property accordingly        
#             pygame.display.update()