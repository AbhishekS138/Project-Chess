from game.scripts.Constants import *
from game.scripts.gui.Square import Square
from game.scripts.gui.Piece import *
from game.scripts.logic.Move import Move
from game.scripts.config.Config import Config

import pygame

class Board:
    
    #Initialize board with double dimensional square list
    def __init__(self):
        self.squares = [[Square(row, col) for row in range(ROWS)] for col in range(COLS)]
        self.last_move = None
        self._add_piece('white')
        self._add_piece('black')
        self.config = Config()
    
    #Add piece of a color to any square of the board
    def _add_piece(self, color):
        row_pawn, row_king = (6, 7) if color == 'white' else (1, 0)
        
        #Pawn Placement
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            
        #Rook Placement
        self.squares[row_king][0] = Square(row_king, 0, Rook(color))
        self.squares[row_king][7] = Square(row_king, 7, Rook(color))
        
        #Knight Placement
        self.squares[row_king][1] = Square(row_king, 1, Knight(color))
        self.squares[row_king][6] = Square(row_king, 6, Knight(color))
        
        #Bishop Placement
        self.squares[row_king][2] = Square(row_king, 2, Bishop(color))
        self.squares[row_king][5] = Square(row_king, 5, Bishop(color))
        
        #Queen Placement
        self.squares[row_king][3] = Square(row_king, 3, Queen(color))
        
        #King Placement
        self.squares[row_king][4] = Square(row_king, 4, King(color))
    
    def final_move(self, piece, move):
        initial = move.initial
        final = move.final
        
        #game board piece update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        #pawn promotion
        if isinstance(piece, Pawn):
            self.promotion(piece, final)
        
        #castling
        if isinstance(piece, King):
            if abs(initial.col - final.col) == 2:
                difference = final.col - initial.col
                rook = piece.left_rook if difference < 0 else piece.right_rook
                if isinstance(rook, Rook):
                    self.final_move(rook, rook.moves[-1])
        
        #move set to true
        piece.moved = True
        piece.first_move = True
        #clear list of valid moves since no more valid moves are possible until next turn
        piece.clear_moves()
        #set last move to true (for rendering purposes)
        self.last_move = move
        
        print(f'{piece.color} {piece.name} moved from [{ROWS-initial.row}, {chr(initial.col+97)}] to [{ROWS-final.row}, {chr(final.col+97)}]')
    
    def valid_move(self, piece, move):
        return move in piece.moves
    
    def promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.config.promote_sound.play()
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    #defining castling move squares of rooks and king 
    def castle_moves(self, king, rook, rook_col):
        row = 0 if king.color == 'black' else 7
        left_col = 1 if rook_col == 0 else 5
        right_col = 4 if rook_col == 0 else 7
        
        for i in range(left_col, right_col):
            #a piece is blocking the castle
                if self.squares[row][i].has_piece():
                    break
                                
        if i == right_col - 1:
            king.left_rook = rook if rook_col == 0 else None
            king.right_rook = rook if rook_col == 7 else None
                                    
            #rook move
            initial = Square(row, rook_col)
            final = Square(row, 3) if rook_col == 0 else Square(row, 5)
            move = Move(initial, final)
            rook.add_move(move)
                                    
            #king move
            initial = Square(row, 4)
            final = Square(row, 2) if rook_col == 0 else Square(row, 6)
            move = Move(initial, final)
            king.add_move(move)
    
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
        
        def fixed_step_moves(possible_moves):
            
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
                
            #Castling        
            if isinstance(piece, King):
                if not piece.first_move:
                    left_rook = self.squares[row][0].piece
                    right_rook = self.squares[row][7].piece

                    #queen-side castling
                    if isinstance(left_rook, Rook):
                        if not left_rook.first_move:
                            self.castle_moves(piece, left_rook, 0)                    
                    #king-side castling
                    if isinstance(right_rook, Rook):
                        if not right_rook.first_move:
                            self.castle_moves(piece, right_rook, 7)
        
        def variable_step_moves(possible_moves):
            
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
            fixed_step_moves([
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
            variable_step_moves([
                (-1, -1),   #up-left
                (-1, 1),    #up-right
                (1, -1),    #down-left
                (1, 1)      #down-right
            ])  
        
        elif isinstance(piece, Rook):
            variable_step_moves([
                (-1, 0),     #up
                (1, 0),      #down
                (0, -1),     #left
                (0, 1)      #right
            ])    
        
        elif isinstance(piece, Queen):
            variable_step_moves([
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
            fixed_step_moves([
                (row+1, col),
                (row+1, col+1),
                (row+1, col-1),
                (row-1, col),
                (row-1, col+1),
                (row-1, col-1),
                (row, col-1),
                (row, col+1)
            ])