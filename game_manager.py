import pygame
from board import Board
from pieces import Piece

class GameManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.board = Board(screen, width, height)
        self.selected_piece = None
        self.current_player = 'player1'
    
    def handle_click(self, pos):
        """Gère les clics de souris"""
        if not self.selected_piece:
            # Phase de sélection
            for piece in self.board.pieces:
                if piece.owner == self.current_player and piece.is_clicked(pos):
                    self.selected_piece = piece
                    piece.selected = True
                    break
        else:
            # Phase de déplacement
            self._try_move_piece(pos)
    
    def _try_move_piece(self, pos):
        """Tente de déplacer le pion sélectionné"""
        target_pos = self._get_nearest_valid_position(pos)
        
        if not target_pos:
            self.selected_piece.selected = False
            self.selected_piece = None
            return
            
        if self._is_valid_move(self.selected_piece, target_pos):
            self.selected_piece.move(target_pos[0], target_pos[1])
            self.selected_piece.selected = False
            self.selected_piece = None
            self._switch_player()
        else:
            self.selected_piece.selected = False
            self.selected_piece = None
    
    def _get_nearest_valid_position(self, pos):
        """Trouve la position valide la plus proche du clic"""
        valid_positions = self.board.get_valid_positions()
        if not valid_positions:
            return None
        
        min_dist = float('inf')
        nearest_pos = None
        for vpos in valid_positions:
            dist = (vpos[0] - pos[0])**2 + (vpos[1] - pos[1])**2
            
            print("dist : " + str(dist))

            if dist < min_dist:
                min_dist = dist
                nearest_pos = vpos
                
                print("min_dist : " + str(min_dist))
                print("nearest_pos : " + str(nearest_pos))
                
        if min_dist <= (self.board.piece_radius * 2)**2:
            return nearest_pos
        return None
    
    def _is_valid_move(self, piece, target_pos):
        """Vérifie si le mouvement est valide"""
        # Case cible occupée?
        for p in self.board.pieces:
            if p.x == target_pos[0] and p.y == target_pos[1]:
                return False
                
        # Distance valide?
        step = self.board.border_size // 2
        dx = abs(piece.x - target_pos[0])
        dy = abs(piece.y - target_pos[1])
        
        return (dx == step and dy == 0) or (dy == step and dx == 0) or (dx == step and dy == step)
    
    def _switch_player(self):
        """Change le tour de joueur"""
        self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
    
    def draw(self):
        """Dessine le plateau et les pions"""
        self.board.draw_board()