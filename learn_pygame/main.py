# import pygame, sys
# from pygame.locals import * 

# BLACK = (  0,   0,   0)
# WHITE = (255, 255, 255)
# RED   = (255,   0,   0)
# GREEN = (  0, 255,   0)
# BLUE  = (  0,   0, 255)

# pygame.init()

# DISPLAYSURF = pygame.display.set_mode((400,300))
# pygame.display.set_caption('Hello World!')

# while True: 
#     for event in pygame.event.get(): 
#         if event.type == QUIT: 
#             pygame.quit() 
#             sys.exit() 
    
#     # DISPLAYSURF.fill((255,255,255)) # RED 
#     # pygame.draw.rect(DISPLAYSURF,   # surface  
#     #                 (255,0,0),      # Color  
#     #                 (100,80,150,50)) # rect 


#     DISPLAYSURF.fill((255,255,255)) # RED 
#     surface2rect = pygame.Surface((150,50)) # create surface with 150,50
#     surface2rect.fill((0,255,0)) # green color for surface 
#     pygame.draw.rect(surface2rect, 
#                     (255,0,0),
#                     (20,20,50,20))
#     DISPLAYSURF.blit(surface2rect, (100,80)) # blit to draw on another surface 

#     pygame.display.update()

import pygame
FPS = 30 
class Actor(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = pygame.Surface((32, 32))
        self.rect = pygame.display.get_surface().get_rect()
        self.image.fill(pygame.Color('dodgerblue'))

    def update(self, events, dt):
        self.rect.move_ip((1 * dt / 5, 2 * dt / 5))
        if self.rect.x > 500: self.rect.x = 0
        if self.rect.y > 500: self.rect.y = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    sprites = pygame.sprite.Group()
    Actor(sprites)
    clock = pygame.time.Clock()
    dt = 0
    while True:

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        sprites.update(events, dt)

        screen.fill((30, 30, 30))
        sprites.draw(screen)
        pygame.display.update()

        dt = clock.tick(FPS)

if __name__ == '__main__':
    main()


