import pygame
from game.scripts.Constants import *

class Drag:
    
    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.initial_row = 0
        self.initial_col = 0
        self.final_row = 0
        self.final_col = 0
        self.piece = None
        self.dragging = False
    
    #Blit method
    def update_blit(self, surface):
        #Image to be rendered
        image = pygame.image.load(self.piece.image)
        #Rect to be rendered
        image_rect = (self.mouse_x, self.mouse_y)
        self.piece.image_rect = image.get_rect(center = image_rect)
        surface.blit(image, self.piece.image_rect)
    
    #Update methods
    def update_pos(self, pos):
        self.mouse_x, self.mouse_y = pos
        
    def initial_pos(self, pos):
        self.initial_row = pos[1] // SQUARE_SIZE
        self.initial_col = pos[0] // SQUARE_SIZE
        
    def drag_set(self, piece):
        self.piece = piece
        self.dragging = True
        
    def undrag_set(self):
        self.piece = None
        self.dragging = False