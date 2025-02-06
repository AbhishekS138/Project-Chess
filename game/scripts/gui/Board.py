from game.scripts.Constants import *
from game.scripts.gui.Square import Square
from game.scripts.gui.Piece import *

class Board:
    
    def __init__(self):
        self.squares = [[Square(row, col) for row in range(ROWS)] for col in range(COLS)]
        self._addPiece('white')
        self._addPiece('black')
        
    def _addPiece(self, color):
        rowPawn, rowKing = (6, 7) if color == 'white' else (1, 0)
        
        #Pawn Placement
        for col in range(COLS):
            self.squares[rowPawn][col] = Square(rowPawn, col, Pawn(color))
            
        #Rook Placement
        self.squares[rowKing][0] = Square(rowKing, 0, Rook(color))
        self.squares[rowKing][7] = Square(rowKing, 7, Rook(color))
        
        #Knight Placement
        self.squares[rowKing][1] = Square(rowKing, 1, Knight(color))
        self.squares[rowKing][6] = Square(rowKing, 6, Knight(color))
        
        #Bishop Placement
        self.squares[rowKing][2] = Square(rowKing, 2, Bishop(color))
        self.squares[rowKing][5] = Square(rowKing, 5, Bishop(color))
        
        #Queen Placement
        self.squares[rowKing][3] = Square(rowKing, 3, Queen(color))
        
        #King Placement
        self.squares[rowKing][4] = Square(rowKing, 4, King(color))