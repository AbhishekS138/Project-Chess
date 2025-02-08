from game.scripts.Constants import *
from game.scripts.gui.Square import Square
from game.scripts.gui.Piece import *
from game.scripts.logic.Move import Move

class Board:
    
    #Initialize board with double dimensional square list
    def __init__(self):
        self.squares = [[Square(row, col) for row in range(ROWS)] for col in range(COLS)]
        self._add_piece('white')
        self._add_piece('black')
        
    #Calculate valid moves for each piece
    def calc_moves(self, piece, row, col):
        
        def pawn_moves():
            #steps
            steps = 1 if piece.moved else 2
            
            #Forward
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))
            for possible_move_row in range(start, end, piece.direction):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        
                        move = Move(initial, final)
                        piece.add_move(move)
                    #Blocked
                    else:
                        break
                #Not in range
                else:
                    break
            
            #Diagonal
            possible_move_row = row + piece.direction
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def adjacent_step_moves(possible_moves):
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        
                        #Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        #Create move
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def linear_moves(possible_moves):
            
            for possible_move in possible_moves:
                row_line, col_line = possible_move
                possible_move_row = row + row_line
                possible_move_col = col + col_line
                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        move = Move(initial, final)
                        
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)
                        
                        if self.squares[possible_move_row][possible_move_col].has_team(piece.color):
                            break
                            
                        if self.squares[possible_move_row][possible_move_col].has_enemy(piece.color):
                            piece.add_move(move)
                            break
                            
                    else:
                        break
                    
                    possible_move_row += row_line
                    possible_move_col += col_line
        
        if isinstance(piece, Pawn):
            pawn_moves()    
        
        elif isinstance(piece, Knight):
            adjacent_step_moves([
                (row+2, col-1),
                (row+2, col+1),
                (row-2, col-1),
                (row-2, col+1),
                (row-1, col-2),
                (row-1, col+2),
                (row+1, col-2),
                (row+1, col+2)
            ])
        
        elif isinstance(piece, Bishop):
            linear_moves([
                (-1, -1),   #up-left
                (-1, 1),    #up-right
                (1, -1),    #down-left
                (1, 1)      #down-right
            ])  
        
        elif isinstance(piece, Rook):
            linear_moves([
                (-1, 0),     #up
                (1, 0),      #down
                (0, -1),     #left
                (0, 1)      #right
            ])    
        
        elif isinstance(piece, Queen):
            linear_moves([
                (-1, -1),   #up-left
                (-1, 1),    #up-right
                (1, -1),    #down-left
                (1, 1),     #down-right
                (-1, 0),     #up
                (1, 0),      #down
                (0, -1),     #left
                (0, 1)      #right
            ])    
        
        elif isinstance(piece, King):
            adjacent_step_moves([
                (row+1, col),
                (row+1, col+1),
                (row+1, col-1),
                (row-1, col),
                (row-1, col+1),
                (row-1, col-1),
                (row, col-1),
                (row, col+1)
            ])    
        
    
    #Add piece of a color to any square of the board
    def _add_piece(self, color):
        row_pawn, row_king = (6, 7) if color == 'white' else (1, 0)
        
        #Pawn Placement
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        self.squares[5][6] = Square(5, 6, Pawn(color))
            
        #Rook Placement
        self.squares[row_king][0] = Square(row_king, 0, Rook(color))
        self.squares[row_king][7] = Square(row_king, 7, Rook(color))
        self.squares[3][7] = Square(3, 7, Rook(color))
        
        #Knight Placement
        self.squares[row_king][1] = Square(row_king, 1, Knight(color))
        self.squares[row_king][6] = Square(row_king, 6, Knight(color))
        self.squares[4][6] = Square(4, 6, Knight(color))
        
        #Bishop Placement
        self.squares[row_king][2] = Square(row_king, 2, Bishop(color))
        self.squares[row_king][5] = Square(row_king, 5, Bishop(color))
        self.squares[4][4] = Square(4, 4, Bishop(color))
        
        #Queen Placement
        self.squares[row_king][3] = Square(row_king, 3, Queen(color))
        self.squares[3][3] = Square(3, 3, Queen(color))
        
        #King Placement
        self.squares[row_king][4] = Square(row_king, 4, King(color))
        self.squares[5][2] = Square(5, 2, King(color))