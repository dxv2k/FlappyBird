
import pygame 
from pygame.locals import *

# Windows settings 
WINDOWWIDTH = 400
WINDOWHEIGHT = 600

# class GameObject(pygame.sprite.Sprite): 
class GameObject: 
    def __init__(self,
        h,
        w, 
        img, 
        x = 0,
        y = 0
        ): 
        self.height = h 
        self.width = w
        self.surface = img
        # Init coordinate  
        x = 0 
        y = 0 
    
    def update(self): 
        pass 

    def draw(self): 
        pass 

    def rect(self): 
        pass 

    def mask(self): 
        pass 

# BIRD 
BIRDWIDTH = 60 
BIRDHEIGHT = 45 
G = 0.5 # g-force  
SPEEDFLY = -8 
BIRDIMG = pygame.image.load('img/bird.png')


class Bird(GameObject):
    def __init__(self): 
        GameObject.__init__(self,
                BIRDHEIGHT,
                BIRDWIDTH, 
                BIRDIMG)
        self.velocity = 0

    # def draw(self):
    #     DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))

    # def update(self, mouseClick): 

    @property 
    def rect(self): 
        return Rect(self.x, self.y, 
                    self.width, self.height)


    # @property 
    # def mask(self): 


class Pipe(GameObject): 
    def __init__(self): 
        GameObject.__init__(self) 
