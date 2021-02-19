import pygame, sys
from pygame.locals import * 

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World!')

while True: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit() 
    
    # DISPLAYSURF.fill((255,255,255)) # RED 
    # pygame.draw.rect(DISPLAYSURF,   # surface  
    #                 (255,0,0),      # Color  
    #                 (100,80,150,50)) # rect 


    DISPLAYSURF.fill((255,255,255)) # RED 
    surface2rect = pygame.Surface((150,50)) # create surface with 150,50
    surface2rect.fill((0,255,0)) # green color for surface 
    pygame.draw.rect(surface2rect, 
                    (255,0,0),
                    (20,20,50,20))
    DISPLAYSURF.blit(surface2rect, (100,80)) # blit to draw on another surface 

    pygame.display.update()
