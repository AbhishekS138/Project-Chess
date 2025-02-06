import os

class Piece:
    
    def __init__(self, name, color, value, image = None, imageRect = None):
        self.name = name
        self.color = color
        valueSign = 1 if color == 'white' else -1
        self.value = value * valueSign
        self.image = image
        self.setImage()
        self.imageRect = imageRect
        self.moves = []
        self.moved = False
        
    def setImage(self):
        # Get the absolute path to the assets folder
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets"))

        # Construct the full path to the piece image
        self.image = os.path.join(base_path, f"{self.color}_{self.name}.png")
        
    def addMoves(self, move):
        self.moves.append(move)

class Pawn(Piece):
    
    def __init__(self, color):
        self.direction = -1 if color == 'white' else 1
        
        super().__init__('pawn', color, 1.0)
        
class Knight(Piece):
    
    def __init__(self, color):
        super().__init__('knight', color, 3.0)
       
class Bishop(Piece):
    
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)
        
class Rook(Piece):
    
    def __init__(self, color):
        super().__init__('rook', color, 5.0)
        
class Queen(Piece):
    
    def __init__(self, color):
        super().__init__('queen', color, 9.0)
        
class King(Piece):
    
    def __init__(self, color):
        super().__init__('king', color, 100.0) 