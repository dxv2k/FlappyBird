from object import GameObject

# BIRD 
BIRDWIDTH = 60 
BIRDHEIGHT = 45 
G = 0.5 # g-force  
SPEEDFLY = -8 

BIRDIMG = pygame.image.load('img/bird.png')

class Bird(GameObject):
    def __init__(self):
        super().__init__(self, 
                        h=BIRDHEIGHT, 
                        w=BIRDWIDTH, 
                        x=(WINDOWWIDTH - self.width)/2, 
                        y=(WINDOWHEIGHT - self.height)/2,
                        surface=BIRDIMG) 
        self.speed = 0

    #     self.width = BIRDWIDTH
    #     self.height = BIRDHEIGHT
    #     self.x = (WINDOWWIDTH - self.width)/2
    #     self.y = (WINDOWHEIGHT- self.height)/2
    #     self.suface = BIRDIMG

    def draw(self):
        DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))

    def update(self, mouseClick): 
        # y = y0 + v0*t + 0.5*g*t^2 
        # v = v0 + g*t
        self.y += self.speed + 0.5*G 
        self.speed += G
        if mouseClick: 
            self.speed = SPEEDFLY



