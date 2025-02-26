from game.scripts.gui.Square import Square
from game.scripts.logic.Move import Move
from game.scripts.Constants import *

import pygame

class GameController:
    
    def __init__(self, renderer):
        self.renderer = renderer                        #private game object
        self.board = renderer.board                     #private board object of game object (initialized in GameRenderer class)
        self.drag = renderer.drag                       #private drag object of game object (initialized in GameRenderer class)
        
    def display(self):
        self.renderer.display_board()                   #first render for game board
        self.renderer.display_last_move()               #second render for last moves
        self.renderer.display_moves()                   #third render for valid moves
        self.renderer.display_pieces()                  #fourth render for pieces
    
    #mouse click handler
    def mouse_click(self, event):
        self.drag.update_pos(event.pos)                                                 #updates mouse coordinates of Drag object
                    
        clicked_row = self.drag.mouse_y // SQUARE_SIZE                                  #gets row number from Drag object's mouse_y
        clicked_col = self.drag.mouse_x // SQUARE_SIZE                                  #gets col number from Drag object's mouse_x
        
        if Square.in_range(clicked_row, clicked_col):                                   #checks if click is within board range
            if self.board.squares[clicked_row][clicked_col].has_piece():                #checks if clicked Square has any piece
                piece = self.board.squares[clicked_row][clicked_col].piece              #gets the piece
                
                if piece.color == self.renderer.next_turn_player:                       #if clicked piece has same color as current player
                    self.board.calc_moves(piece, clicked_row, clicked_col, True)        #calculates valid moves for clicked piece
                    self.drag.initial_pos(event.pos)                                    #sets initial row and col attributes of Drag object
                    self.drag.drag_set(piece)                                           #sets dragging state to True of Drag object
                    
                    self.display()                                                      #displays everything
    
    #mouse movement handler
    def mouse_motion(self, event):
        if self.drag.dragging:                                                          #updates game_surface if board has a dragging state
            self.drag.update_pos(event.pos)
            
            self.display()                                                              #displays everything
            
            self.drag.update_blit(self.renderer.surface)                                #renders the piece being dragged
    
    #mouse release handler
    def mouse_release(self, event):
        if self.drag.dragging:                                                          #updates game_surface if board has a dragging state
            self.drag.update_pos(event.pos)
            final_row = self.drag.mouse_y // SQUARE_SIZE                                #gets row number from Drag object's mouse_y                            
            final_col = self.drag.mouse_x // SQUARE_SIZE                                #gets col number from Drag object's mouse_x
            
            initial = Square(self.drag.initial_row, self.drag.initial_col)              #creates initial and final Square objects
            final = Square(final_row, final_col)
            move = Move(initial, final)                                                 #creates Move object
            
            if self.board.valid_move(self.drag.piece, move):                            #if move is within list of calculated valid moves
                captured = self.board.squares[final_row][final_col].has_piece()         #boolean flag for capturing a piece
                self.board.final_move(self.drag.piece, move)                            #sets the board according to the move
                self.renderer.move_capture_sound(captured)                              #plays capture or move sound
                
                self.display()                                                          #displays everything
                
                #debug print, prints the move made
                print(f'{self.drag.piece.color} {self.drag.piece.name} moved from {chr(initial.col+97)}{ROWS-initial.row} to {chr(final.col+97)}{ROWS-final.row}')
            
            else:                                                                       #plays illegal sound if move made is invalid
                self.renderer.illegal_sound() 
            
            if self.drag.piece.moved == True:
                self.drag.piece.moved = False                                           #sets moved flag of piece to False
                self.renderer.next_turn()                                               #switches to the other color
        
        self.drag.undrag_set()                                                          #sets dragging state to False
    
    #key press handler
    def key_press(self, event):
        #on key press(t)
        if event.key == pygame.K_t:
            self.renderer.config.change_theme()                                         #change theme on key press t
            self.display()                                                              #displays everything
        
        #on key press(r)    
        if event.key == pygame.K_r:
            self.renderer.reset()                                                       #restarts Game object on game_screen
            self.__init__(self.renderer)                                                #reinitializes GameController object