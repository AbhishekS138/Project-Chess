import pygame
import os

from game.scripts.config.Sound import Sound
from game.scripts.config.Theme import Theme
from game.scripts.Constants import *

class Config:
    
    def __init__(self):
        self.themes = []
        self.add_theme()
        self.index = 0
        self.theme = self.themes[self.index]
        
        # base_sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/sounds"))
        # self.move_self_sound = Sound(os.path.join(base_sound_path, "move_self.ogg"))
        # self.capture_sound = Sound(os.path.join(base_sound_path, "capture.ogg")) 
    
    def change_theme(self):
        self.index += 1
        self.index %= len(self.themes)
        self.theme = self.themes[self.index]
    
    def add_theme(self):
        green = Theme(GREEN_LIGHT, GREEN_DARK, GREEN_TRACE_LIGHT, GREEN_TRACE_DARK, GREEN_MOVE_LIGHT, GREEN_MOVE_DARK, LIGHT_RED, DARK_RED)
        brown = Theme(BROWN_LIGHT, BROWN_DARK, BROWN_TRACE_LIGHT, BROWN_TRACE_DARK, BROWN_MOVE_LIGHT, BROWN_MOVE_DARK, LIGHT_RED, DARK_RED)
        blue = Theme(BLUE_LIGHT, BLUE_DARK, BLUE_TRACE_LIGHT, BLUE_TRACE_DARK, BLUE_MOVE_LIGHT, BLUE_MOVE_DARK, LIGHT_RED, DARK_RED) 
        gray = Theme(GRAY_LIGHT, GRAY_DARK, GRAY_TRACE_LIGHT, GRAY_TRACE_DARK, GRAY_MOVE_LIGHT, GRAY_MOVE_DARK, LIGHT_RED, DARK_RED)
        
        self.themes = [green, brown, blue, gray]