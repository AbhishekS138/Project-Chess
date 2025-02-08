import pygame
from game.scripts.Constants import *
from game.scripts.gui.Board import Board
from game.scripts.logic.Drag import Drag

class Game:
    
    def __init__(self):
        self.board = Board()
        self.drag = Drag()
    
    #display methods
    
    #display board
    def display_board(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = LIGHT_GREEN
                else:
                    color = DARK_GREEN

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
        if self.drag.dragging:
            piece = self.drag.piece
            
            for move in piece.moves:
                color = DEEP_RED if (move.final.row + move.final.col) % 2 == 0 else LIGHT_RED
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)