import pygame 
from pygame.locals import * 

import os
import sys 
import random 

# Windows settings 
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# FPS and Clock 
FPS = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('img/background.png')

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

class Bird: 
    MAX_ROTATE = 25 
    IMGS = bird_images 
    def __init__(self,x,y,width=60,height=45):
        self.width = width
        self.height = height
        self.x = x 
        self.y = y 
        self.rotate = 0 # Current rotation degree  
        self.speed = 0
        self.tick_count = 0
        # self.suface = BIRDIMG

    # def draw(self):
    #     DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))

    # def update(self, mouseClick): 
    #     # y = y0 + v0*t + 0.5*g*t^2 
    #     # v = v0 + g*t
    #     self.y += self.speed + 0.5*G 
    #     self.speed += G
    #     if mouseClick: 
    #         self.speed = SPEEDFLY

    # @property
    # def rect(self): 
    #     return Rect()