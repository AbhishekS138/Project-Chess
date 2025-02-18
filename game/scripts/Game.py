from game.scripts.Constants import *
from game.scripts.gui.Board import Board
from game.scripts.logic.Drag import Drag
from game.scripts.config.Config import Config

import pygame
class Game:
    
    def __init__(self, surface):
        self.surface = surface                      #game surface on which everything is to be rendered
        self.next_turn_player = 'white'             #turn based variable for players, default set to white (white moves first)
        self.board = Board()                        #Board object
        self.drag = Drag()                          #Drag object
        self.config = Config()                      #Config object
        self.config.game_start_sound.play()         #play game start sound on Game object initialization
    
    #DISPLAY METHODS
    
    #rectangle display method
    def draw_rect(self, scheme, row, col):
        
        #color is initialized as defined by the current scheme
        color = scheme.light if (row + col) % 2 == 0 else scheme.dark
        
        #pygame rect object, with parameters(x-axis starting point, y-axis starting point, x-axis rect size, y-axis rect size)
        rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        
        #pygame draw method, to render rect of color on surface
        pygame.draw.rect(self.surface, color, rect)
    
    #display board
    def display_board(self):
        theme = self.config.theme           #current theme of the board
        
        for row in range(ROWS):
            for col in range(COLS):
                self.draw_rect(theme.bg, row, col)  #rendering all squares with the bg colors of theme
                
                #col labels
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light           #opposite colors of squares are used
                    label = self.config.font.render(str(ROWS - row), True, color)       #loads 8 - row number, to be rendered
                    #position of label, 5 pixels away on x-axis, 5 pixels down from left corner of current square, on y-axis
                    label_pos = (5, 5 + row * SQUARE_SIZE)
                    self.surface.blit(label, label_pos)                                 #blits label at label_pos
                
                #row labels
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light   #opposite colors of squares are used
                    label = self.config.font.render(str(chr(col + 97)), True, color)    #loads col number + 97(a), to be rendered
                    #position of label, 15 pixels away from right corner of current square, on x-axis, 20 pixels up on y-axis
                    label_pos = (col * SQUARE_SIZE + SQUARE_SIZE - 15, HEIGHT - 20)
                    self.surface.blit(label, label_pos)                                 #blits label at label_pos
                
    #display pieces
    def display_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                
                #Check for piece
                if self.board.squares[row][col].has_piece():            #checks if the particular square has a piece
                    piece = self.board.squares[row][col].piece          #assigns said piece to piece variable
                    
                    #Piece's image to be rendered
                    if piece is not self.drag.piece:                    #if piece is not being dragged
                        image = pygame.image.load(piece.image)
                        #piece image is to be rendered at the center of the square
                        image_rect = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.image_rect = image.get_rect(center = image_rect)
                        self.surface.blit(image, piece.image_rect)
                        
    #display moves
    def display_moves(self):
        theme = self.config.theme
        
        if self.drag.dragging:
            piece = self.drag.piece         #piece being dragged
            
            for move in piece.moves:        #all moves in moves list of piece
                #checks if final square of move has enemy piece
                if self.board.squares[move.final.row][move.final.col].has_enemy(piece.color):
                    self.draw_rect(theme.enemies, move.final.row, move.final.col)   #rendering all squares with the enemies colors of theme
                else:
                    #draws a circle of color at center of all empty squares of move, with a radius of 1/6th of square size
                    color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                    center_x = move.final.col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = move.final.row * SQUARE_SIZE + SQUARE_SIZE // 2
                    radius = SQUARE_SIZE // 6
                    pygame.draw.circle(self.surface, color, (center_x, center_y), radius)
    
    def display_last_move(self):
        theme = self.config.theme
        
        #checks if Board object has any last moves
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            #renders 2 squares in the list [initial, final] with the trace colors of theme
            for pos in [initial, final]:
                self.draw_rect(theme.trace, pos.row, pos.col)       #rendering all squares with the trace colors of theme
                    
    #OTHER METHODS
    #method to switch next turn player
    def next_turn(self):
        self.next_turn_player = 'black' if self.next_turn_player == 'white' else 'white'
        
    #method to change themes
    def change_theme(self):
        self.config.change_theme()
        
    #method to reset Game object with same game surface
    def reset(self):
        self.__init__(self.surface)
    
    #method to play capture sound if captured exists, else plays move sound
    def move_capture_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_self_sound.play()
            
    #method to play illegal move sound
    def illegal_sound(self):
        self.config.illegal_sound.play()