import pygame 

class Piece:
    def __init__(self, x, y, radius, color, owner):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.owner = owner
        
        self.selected = False
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    
    def draw(self, screen, outline_color): 
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius) 
        pygame.draw.circle(screen, outline_color, (self.x, self.y), self.radius, 2)
         
        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius // 2, 2)
    
    def is_clicked(self, pos):
        """Vérifie si le pion a été cliqué"""
        return self.rect.collidepoint(pos)
    
    def move(self, new_x, new_y):
        """Déplace le pion à une nouvelle position"""
        self.x = new_x
        self.y = new_y
        
        self.rect.center = (new_x, new_y)
        self.rect = pygame.Rect(new_x - self.radius, new_y - self.radius, 
                              self.radius * 2, self.radius * 2)
    