import pygame

class Sound:
    
    #initialize a path and a sound file for the Sound object
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)
    
    #method to play the sound file of the Sound object 
    def play(self):
        pygame.mixer.Sound.play(self.sound)
        
    #exclude the pygame.mixer.Sound object during deepcopy.
    def __getstate__(self):
        state = self.__dict__.copy()
        del state["sound"]                          #remove unpicklable object
        return state

    #reload the sound object after deepcopy.
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.sound = pygame.mixer.Sound(self.path)  #reload sound from path