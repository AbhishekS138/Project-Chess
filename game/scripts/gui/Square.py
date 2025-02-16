from game.scripts.gui.Piece import *

class Square:
    
    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece
        
    def __eq__(self, value):
        return self.row == value.row and self.col == value.col
    
    def has_piece(self):
        return self.piece != None
    
    def is_empty(self):
        return not self.has_piece()
    
    def has_team(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_enemy(self, color):
        return self.has_piece() and self.piece.color != color

    def is_empty_or_enemy(self, color):
        return self.is_empty() or self.has_enemy(color)
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        
        return True