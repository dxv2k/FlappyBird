import os 
import math
import random 
import pygame
from pygame.locals import *

import neat 

# Window settings
WINDOW_HEIGHT = 800 
WINDOW_WIDTH = 600 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# FLOOR
FLOOR_POS = 730 

# PIPE 
PIPE_POS = 700 

# FPS 
FPS = 30

# Font  
pygame.font.init() # init font
STAT_FONT = pygame.font.SysFont('comicsans', 80)

# Load textures  
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

# BIRD 
BIRD_INIT_POS_X = 230
BIRD_INIT_POS_Y = 350

"""
    In this game, the bird doesn't move but instead of that 
    objects move
"""

pygame.display.set_caption('Flappy Bird')

# TODO: using abstract GameObj for Bird,Pipe,Floor 
class Object: 
    IMG = None 
    ANIMATION_TIME = 0 
    def __init__(self, x,y): 
        self.x = x
        self.y = y

    def update(self,dt): 
        pass 

    def draw(self): 
        pass 
    
    def rect(self): 
        pass 

    def mask(self): 
        pass 

class Bird:
    """
    Bird class representing the flappy bird
    """
    MAX_ROTATION = 25
    IMGS = bird_images
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # TODO: set threshold that bird can't go out window size  
    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        make the bird move
        :return: None
        """
        self.tick_count += 1

        # for downward acceleration
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        draw the bird
        :param win: pygame window or surface
        :return: None
        """
        self.img_count += 1

        # TODO: Optimize this by implement State Machine 
        # ref: https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/from-user-input-to-animations-using-state-machines-r4155/
        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # tilt the bird
        blitRotateCenter(WINDOW, self.img, (self.x, self.y), self.tilt)

    # TODO: implement @property 
    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        return pygame.mask.from_surface(self.img)

class PipePair: 
    GAP_SPACE = 200 # top and bottom space  
    VELOCITY = 5 # velocity moving toward the bird 
    def __init__(self,x): 
        self.x = x 
        self.height = 0   

        # top pipe and bottom pipe 
        self.top = 0 
        self.bottom = 0 

        # Image for PipePair  
        self.IMG_TOP = pygame.transform.flip(pipe_img, False, True) 
        self.IMG_BOTTOM = pipe_img

        # Contain if the bird already pass this PipePair 
        self.passed = False

        # Random generate height for PipePair
        self.set_height()

    def set_height(self):
        '''
        Random generate height for PipePair
        ''' 
        self.height = random.randrange(50,450)        
        self.top = self.height - self.IMG_TOP.get_height()
        self.bottom = self.height + self.GAP_SPACE 

    def move(self): 
        self.x -= self.VELOCITY
    
    def draw(self,window): 
        # top pipe
        window.blit(self.IMG_TOP, (self.x,self.top))
        # bottom pipe
        window.blit(self.IMG_BOTTOM, (self.x,self.bottom))

    def get_mask(self): 
        ''' 
        return: [top pipe mask, bottom pipe mask]
        ''' 
        return [pygame.mask.from_surface(self.IMG_TOP), 
                pygame.mask.from_surface(self.IMG_BOTTOM)]
    
    def isCollide(self, bird, window): 
        ''' 
        param: bird object, window object 
        return: True/False 
        '''
        bird_mask = bird.get_mask()
        pipe_mask = self.get_mask() 

        # calculate offset 
        # explain: https://gamedev.stackexchange.com/questions/47694/meaning-of-offset-in-pygame-mask-overlap-methods 
        top_offset = (self.x - bird.x, 
                    self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, 
                    self.bottom - round(bird.y))

        # check if coliision 
        top_collision = bird_mask.overlap(pipe_mask[0], 
                                            top_offset) 
        bottom_collision = bird_mask.overlap(pipe_mask[1], 
                                            bottom_offset) 
        if top_collision or bottom_collision: 
            return True 
        return False

class Floor: 
    """ 
    Represents the moving floor of the game
    Explanation of how its work: 
        - Using 2 images of the base 
        - Moving 2 of which continously  
    """ 
    VELOCITY = 5
    WIDTH = base_img.get_width()
    IMG = base_img 

    def __init__(self,y): 
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self): 
        self.x1 -= self.VELOCITY 
        self.x2 -= self.VELOCITY 
        
        # 1st base
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        # 2nd base
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self,window): 
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))

# class Score():
#     def __init__(self):
#         self.score = 0
#         self.addScore = True
    
#     def draw(self,window):
#         font = pygame.font.SysFont('consolas', 40)
#         scoreSuface = font.render(str(self.score), True, (0, 0, 0))
#         textSize = scoreSuface.get_size()
#         # window.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 100))
    
#     def update(self, bird, columns):
#         # collision = False
#         # for i in range(3):
#         #     rectColumn = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
#         #     rectBird = [bird.x, bird.y, bird.width, bird.height]
#         #     if rectCollision(rectBird, rectColumn) == True:
#         #         collision = True
#         #         break
#         # if collision == True:
#         #     if self.addScore == True:
#         #         self.score += 1
#         #     self.addScore = False
#         # else:
#         #     self.addScore = True


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(window,
                birds,
                pipes, 
                floor, 
                score): 
    window.blit(bg_img,(0,0))
    # bird 
    for bird in birds: 
        bird.draw(window)

    # pipes  
    for pipe in pipes: 
        pipe.draw(window)
        
    # floor 
    floor.draw(window)

    # score 
    scoreSuface = STAT_FONT.render(str(score), 
                                    True, 
                                    (255, 255, 255)) # color white 
    textSize = scoreSuface.get_size()
    # window.blit(scoreSuface, (int((WINDOW_WIDTH - textSize[0])/2), 100))
    window.blit(scoreSuface, (WINDOW_WIDTH - scoreSuface.get_width() - 15, 10))

    pygame.display.update()

# # TODO: move gameloop from main to here 
# def gameLoop(window, 
#             bird, 
#             pipe, 
#             score
# ): 
#     while True: 

def main(): 
    # Game time 
    clock = pygame.time.Clock()

    # Game Object 
    bird = Bird(230,350) 
    floor = Floor(695)
    # pipe = PipePair(700)
    pipes = [PipePair(600)] 

    score = 0  
    # Main loop
    # TODO: update() with dt   
    while True: 
        clock.tick(FPS)
        # Event handler 
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit()
                sys.quit()
            if event.type == MOUSEBUTTONDOWN: 
                bird.jump()

        # respawn pipe and incr score  
        remove_pipe = []
        add_pipe = False  
        for pipe in pipes: 
            if pipe.isCollide(bird,WINDOW): 
                # TODO: terminate the bird if collided 
                print("[INFO] Bird collide with Pipe")
                pass 
            # check if pipe is off screen 
            if pipe.x + pipe.IMG_TOP.get_width() < 0: 
                remove_pipe.append(pipe) 
            # pipe.move() 
            if not pipe.passed and pipe.x < bird.x: 
                pipe.passed = True
                add_pipe = True
            pipe.move() 

        if add_pipe: 
            score += 1 
            pipes.append(PipePair(600))
            print('[INFO] Score: ',score)
        for pipe in remove_pipe: 
            pipes.remove(pipe)
        # if pipe.isCollide(bird,WINDOW): 
        #     print("[INFO] Bird collide with Pipe")

        # TODO: update GameObject with delta_time
        bird.move()
        floor.move()
        draw_window(WINDOW,bird,pipes,floor,score)

def eval_genomes(genomes, config): 
    # Game time 
    clock = pygame.time.Clock()

    # Game Object 
    floor = Floor(FLOOR_POS)
    pipes = [PipePair(PIPE_POS)] 
    score = 0  

    # Bird and its genome, neural nets management  
    birds = [] # holding bird object  
    neural_net = [] # holding neural net
    ge = [] # genome object 

    for gen_id, genome in genomes: 
        genome.fitness = 0 # set fitness level
        neural = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_net.append(neural)
        birds.append(Bird(BIRD_INIT_POS_X,BIRD_INIT_POS_Y)) 
        ge.append(genome)

    run = True # flag
    while True: 
        clock.tick(FPS)
        # Event handler 
        for event in pygame.event.get():
            if event.type == QUIT: 
                run = False 
                pygame.quit()
                sys.quit()
        # if multiple pipe appear, decide which one to feed to neural net 
        pipe_ind = 0
        if len(birds) > 0:
            if ((len(pipes) > 1) 
                and (birds[0].x > pipes[0].x + pipes[0].IMG_TOP.get_width())):  # determine whether to use the first or second
                pipe_ind = 1                                                                 # pipe on the screen for neural network input

        # decide if bird should jump 
        for idx, bird in enumerate(birds): 
            ge[idx].fitness += 0.1 # reward for every survived frame 
            bird.move()
            # send bird location to neural net 
            output = neural_net[birds.index(bird)].activate((
                                bird.y, # bird is not moving so given y-axis  
                                abs(bird.y - pipes[pipe_ind].height), # distance to top pipe  
                                abs(bird.y - pipes[pipe_ind].bottom)))  # distance to bottom pipe 
            if output[0] > 0.5: 
                bird.jump() 

        # update floor 
        floor.move() 

        # respawn pipe and collisiion detection  
        remove_pipe = []
        add_pipe = False  
        for pipe in pipes: 
            pipe.move() 
            # check if any collision  
            for idx, bird in enumerate(birds): 
                # If bird collide with any pipe
                # remove bird and its genome, neural from list 
                if pipe.isCollide(bird,WINDOW):  
                    ge[birds.index(bird)].fitness = -1
                    neural_net.pop(birds.index(bird)) # eliminate bird from neural net  
                    ge.pop(birds.index(bird)) # eliminate bird from genome  
                    birds.pop(birds.index(bird)) # remove bird object   
                    
            # check if pipe is off screen 
            if pipe.x + pipe.IMG_TOP.get_width() < 0: 
                remove_pipe.append(pipe) 
            if not pipe.passed and pipe.x < bird.x: 
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # encourage bird to jump through pipe by giving more reward than sual 
            for genome in ge:
                genome.fitness += 5
            pipes.append(PipePair(PIPE_POS))

        for pipe in remove_pipe: 
            pipes.remove(pipe)

        for bird in birds:
            # check if bird outside the screen 
            # if outside consider it as defective bird 
            if ((bird.y + bird.img.get_height() - 10 >= FLOOR_POS) or 
                (bird.y < 0)):
                # or (bird.y < -50):
                neural_net.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WINDOW,birds,pipes,floor,score)

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = population.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

# if __name__ == '__main__':
#     main()

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    # config_path = os.path.join(local_dir, '../config/config-feedforward.txt')
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
