import pygame
from game.scripts.Constants import *

class Drag:
    
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol = 0
        self.finalRow = 0
        self.finalCol = 0
        self.piece = None
        self.dragging = False
    
    #Blit method
    def updateBlit(self, surface):
        #Image to be rendered
        image = pygame.image.load(self.piece.image)
        #Rect to be rendered
        imageRect = (self.mouseX, self.mouseY)
        self.piece.imageRect = image.get_rect(center = imageRect)
        surface.blit(image, self.piece.imageRect)
    
    #Update methods
    def updatePos(self, pos):
        self.mouseX, self.mouseY = pos
        
    def initialPos(self, pos):
        self.initialRow = pos[1] // SQUARE_SIZE
        self.initialCol = pos[0] // SQUARE_SIZE
        
    def dragSet(self, piece):
        self.piece = piece
        self.dragging = True
        
    def undragSet(self):
        self.piece = None
        self.dragging = False