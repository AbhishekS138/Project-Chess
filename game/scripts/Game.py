import pygame
from game.scripts.Constants import *
from game.scripts.gui.Board import Board
from game.scripts.logic.Drag import Drag
from game.scripts.config.Config import Config

class Game:
    
    def __init__(self):
        self.next_turn_player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.drag = Drag()
        self.config = Config()
    
    #display methods
    
    #display board
    def display_board(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)               
                pygame.draw.rect(surface, color, rect)
                
    #display pieces
    def display_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                
                #Check for piece
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    #Piece's image to be rendered
                    if piece is not self.drag.piece:
                        image = pygame.image.load(piece.image)
                        image_rect = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.image_rect = image.get_rect(center = image_rect)
                        surface.blit(image, piece.image_rect)
                        
    #display moves
    def display_moves(self, surface):
        theme = self.config.theme
        
        if self.drag.dragging:
            piece = self.drag.piece
            
            for move in piece.moves:
                if self.board.squares[move.final.row][move.final.col].has_enemy(piece.color):
                    color = theme.enemies.light if (move.final.row + move.final.col) % 2 == 0 else theme.enemies.dark
                    rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(surface, color, rect)
                else:
                    color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                    center_x = move.final.col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = move.final.row * SQUARE_SIZE + SQUARE_SIZE // 2
                    radius = SQUARE_SIZE // 6
                    pygame.draw.circle(surface, color, (center_x, center_y), radius)
    
    def display_last_move(self, surface):
        theme = self.config.theme
        
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)
    
    #other methods
    def next_turn(self):
        self.next_turn_player = 'black' if self.next_turn_player == 'white' else 'white'
        
    def change_theme(self):
        self.config.change_theme()