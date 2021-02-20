from singleton import SingletonMeta

class GameObject(): 
    # value: str = None 
    __metaclass__ = SingletonMeta

    def __init__(self, 
        w = None,
        h = None,
        x = None,
        y = None,
        speed = None,
        surface = None
    ): 
        self.width = w 
        self.height = h
        self.x = x  
        self.y = y  
        self.speed = speed 
        self.suface = surface

    def update(self): 
        pass 

    def draw(self): 
        pass 


    

