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
        
        # print("radius piece : " + str(self.piece_radius))
        self.pieces = []
        self.forbidden_positions = [] 
        
        # self.initialize_pieces()
    
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
    
        for pos in self.forbidden_positions:
            pygame.draw.circle(
                self.screen, 
                (0, 0, 0),  # Noir pur
                pos,
                self.piece_radius // 2  # Plus petit qu'une pièce normale
            )
            
    def  initialize_pieces(self):
        piece_positions = [
            (0, 0, self.BLACK, 'player1'),
            (0.5, 1, self.BLACK, 'player1'), 
            (1, 0, self.BLACK, 'player1'),
            
            (0, 0.5, self.WHITE, 'player2'),
            (0.5, 0, self.WHITE, 'player2'),
            (1, 0.5, self.WHITE, 'player2')
        ]
        
        for x_rel, y_rel, color, owner in piece_positions:             
            x, y = utils.relative_to_absolute(x_rel, y_rel, self.border_x, self.border_y, self.border_size)
            
            # print("self.border_size : " + str(self.border_size))
            # print("x : " + str(x))
            # print("y : " + str(y))
            
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
    
    def _place_piece(self, pos, owner):
        """Place une pièce sur le plateau"""
        color = self.BLACK if owner == 'player1' else self.WHITE
        piece = Piece(pos[0], pos[1], self.piece_radius, color, owner)
        self.pieces.append(piece)
    
    def _is_valid_initial_position(self, pos):
        """Vérifie si la position est vide"""
        return not any(p.x == pos[0] and p.y == pos[1] for p in self.pieces)
    
    def add_forbidden_position(self, pos):
        """Ajoute une position interdite"""
        if pos not in self.forbidden_positions:
            self.forbidden_positions.append(pos)
    
    def is_position_forbidden(self, pos):
        """Vérifie si une position est interdite"""
        return pos in self.forbidden_positions
    
    def _est_coup_valide(self, piece, target_pos, board):
        """Vérifie si le mouvement est valide""" 

        # Pas en dehors de la table
        if not (board.border_x <= target_pos[0] <= board.border_x + board.border_size and
        board.border_y <= target_pos[1] <= board.border_y + board.border_size):
            return False
            
        # 1. Vérifie que la case cible est vide
        for p in board.pieces:
            if p.x == target_pos[0] and p.y == target_pos[1]:
                # print("Case non vide")
                return False
            
        step = board.border_size // 2
        dx = abs(piece.x - target_pos[0])
        dy = abs(piece.y - target_pos[1])
            
        # 2. Vérifie que le déplacement est d'une case
        if not ((dx == step and dy == 0) or  # Horizontal
                (dy == step and dx == 0) or  # Vertical
                (dx == step and dy == step)):  # Diagonal
            # print("Mouvement interdite")
            return False
            
        # 3. Vérifie les diagonales interdites (en coordonnées relatives)
        piece_rel = utils.absolute_to_relative(piece.x, piece.y, self)
        target_rel = utils.absolute_to_relative(target_pos[0], target_pos[1], self)
            
        forbidden_diagonals = {
                (0.5, 0): [(1, 0.5), (0, 0.5)],    # (150,0) → (300,150), (0,150)
                (0, 0.5): [(0.5, 0), (0.5, 1)],    # (0,150) → (150,0), (150,300)
                (0.5, 1): [(0, 0.5), (1, 0.5)],    # (150,300) → (0,150), (300,150)
                (1, 0.5): [(0.5, 0), (0.5, 1)]     # (300,150) → (150,0), (150,300)
        }
            
        if piece_rel in forbidden_diagonals:
            if target_rel in forbidden_diagonals[piece_rel]: 
                return False
            
        # 4. Vérifie les pièces intermédiaires (pour horizontaux/verticaux)
        if dx != step or dy != step:  # Si ce n'est pas une diagonale
            mid_x = piece.x + (target_pos[0] - piece.x) // 2
            mid_y = piece.y + (target_pos[1] - piece.y) // 2
            if any(p.x == mid_x and p.y == mid_y for p in board.pieces):
                return False
            
        return True