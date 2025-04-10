import pygame
from pieces import Piece

from utils import utils

class Board:
    
    def __init__(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
        # CONSTANTES
        self.screen = screen
        
        self.BROWN = (139, 69, 19)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BACKGROUND = (240, 217, 181)
        
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
        self.margin = 10
                
        self.border_size = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 4 * self.margin
        # Position pour centrer le carré
        self.border_x = (SCREEN_WIDTH - self.border_size) // 2
        self.border_y = (SCREEN_HEIGHT - self.border_size) // 2
        
        # Constantes pour les pions
        self.piece_radius = self.border_size // 24
        
        print("radius piece : " + str(self.piece_radius))
        self.pieces = []
        
        self.initialize_pieces()
    
    def draw_board(self): 
        self.screen.fill(self.BACKGROUND)
        
        pygame.draw.rect(
            self.screen, 
            self.BROWN, 
            (self.border_x, self.border_y, self.border_size + 2, self.border_size + 2),
            3
        )
        
        center_x = self.border_x + self.border_size // 2
        center_y = self.border_y + self.border_size // 2
        
        # Ligne verticale centrale
        pygame.draw.line(
            self.screen, 
            self.BROWN,
            (center_x, self.border_y),
            (center_x, self.border_y + self.border_size),
            2
        )
        
        # Ligne horizontale centrale
        pygame.draw.line(
            self.screen,
            self.BROWN,
            (self.border_x, center_y),
            (self.border_x + self.border_size, center_y),
            2
        )
        
        # Diagonale de gauche à droite
        pygame.draw.line(
            self.screen, 
            self.BROWN,
            (self.border_x, self.border_y),
            (self.border_x + self.border_size, self.border_y + self.border_size),
            2
        )
        
        # Diagonale de droite à gauche
        pygame.draw.line(
            self.screen,
            self.BROWN,
            (self.border_x + self.border_size, self.border_y),
            (self.border_x, self.border_y + self.border_size),
            2
        )
        
        for piece in self.pieces:
            piece.draw(self.screen, self.BROWN)
    
    def initialize_pieces(self):
        piece_positions = [
            (0, 0, self.BLACK, 'player1'),
            (0.5, 0, self.WHITE, 'player2'), 
            (1, 0, self.BLACK, 'player1'),
            
            (0, 1, self.WHITE, 'player2'),
            (0.5, 1, self.BLACK, 'player1'),
            (1, 1, self.WHITE, 'player2')
        ]
        
        for x_rel, y_rel, color, owner in piece_positions:             
            x, y = utils.relative_to_absolute(x_rel, y_rel, self.border_x, self.border_y, self.border_size)
            
            print("self.border_size : " + str(self.border_size))
            print("x : " + str(x))
            print("y : " + str(y))
            
            piece = Piece(x, y, self.piece_radius, color, owner)
            self.pieces.append(piece)
    
    def get_valid_positions(self):
        """Retourne toutes les positions valides sur le plateau"""
        positions = []
        step = self.border_size // 2
        for i in range(3):
            for j in range(3):
                x = self.border_x + j * step
                y = self.border_y + i * step
                
                positions.append((x, y)) 
        return positions