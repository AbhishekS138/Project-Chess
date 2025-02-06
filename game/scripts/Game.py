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
    def displayBoard(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = LIGHT_GREEN
                else:
                    color = DARK_GREEN

                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                
                pygame.draw.rect(surface, color, rect)
                
    #display pieces
    def displayPieces(self, surface, drag):
        for row in range(ROWS):
            for col in range(COLS):
                
                #Check for piece
                if self.board.squares[row][col].hasPiece():
                    piece = self.board.squares[row][col].piece
                    
                    #Piece's image to be rendered
                    if piece is not drag.piece:
                        image = pygame.image.load(piece.image)
                        imageRect = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.imageRect = image.get_rect(center = imageRect)
                        surface.blit(image, piece.imageRect)