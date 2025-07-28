import pygame


pygame.init()

hit_sound = pygame.mixer.Sound('sounds/hit.wav')
hurt_sound = pygame.mixer.Sound('sounds/hurt.wav')

class Rect:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.wave = 0
        self.color = 'yellow'
        self.size = size
        
        self.global_life = 20
        self.life = self.global_life
        self.active = False
        
        self.x_to_draw = size * x
        self.y_to_draw = size * y
        
    def draw(self, sc):
        pygame.draw.rect(sc, self.color, (self.x_to_draw + (self.size // 2) - (self.wave // 2),
                                                      self.y_to_draw + (self.size // 2) - (self.wave // 2),
                                                      self.wave, self.wave))
        pygame.draw.rect(sc, 'white', (self.x_to_draw, self.y_to_draw, self.size, self.size), 2)
        
    def tick(self, mistakes):
        if self.active:
            if self.wave + 20 >= self.size:
                self.wave = self.size - 20
                self.color = 'green'
                self.life -= 1
                
            elif self.wave + 20 >= 0:
                self.wave += 4
        
            if self.life <= 0:
                if self.color != 'red':
                    mistakes += 1
                    print(mistakes)
                self.color = 'red'
                self.wave -= 7
                
                
        if self.wave <= 0:
            self.active = False
            self.life = self.global_life
            self.color = 'yellow'
            self.wave = 0
        return mistakes
            
    def click(self):
        if self.color == 'green':
            hit_sound.play()
            self.wave = 0
            self.active = False
            
        elif self.color == 'yellow':
            if self.wave > 0:
                self.wave = self.size - 20
                self.life = 0
                hurt_sound.play()
        
            
            
        
        