import pygame
import time

from board import Board
from pieces import Piece
from utils import utils

from hell import devil

class GameManager:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.board = Board(screen, width, height)
        self.selected_piece = None
        self.current_player = 'player1'
        
        self.game_over = False
        self.winner = None
         
        self.ai_player_one = devil(self, self.board, player_color='player2')
        
        self.initialization_phase = True
        self.pieces_placed = {'player1': 0, 'player2': 0}  
        self.total_pieces_to_place = 3 
        
        self.adding_forbidden = False 
    
    def toggle_forbidden_mode(self):
        """Active/désactive le mode ajout de points noirs"""
        self.adding_forbidden = not self.adding_forbidden
    
    def handle_click(self, pos):
        """Gère les clics de souris"""
        # ajout de point noir
        if self.adding_forbidden:
            target_pos = self._get_nearest_valid_position(pos)
            if target_pos:
                self.board.add_forbidden_position(target_pos)
            return
        # initialisation des pieces
        elif self.initialization_phase:
            self._handle_initialization_click(pos)
        else:
            # Le code existant pour le jeu normal
            if not self.selected_piece:
                for piece in self.board.pieces:
                    if piece.owner == self.current_player and piece.is_clicked(pos):
                        self.selected_piece = piece
                        piece.selected = True
                        break
            else:
                self._try_move_piece(pos)
    
    def tour_ia(self):
        coup = self.ai_player_one.choisir_coup()
        
        if coup:
            piece, (x, y) = coup
            piece.move(x, y)
            self._check_win_condition("player2")
            self._switch_player()
    
    def _handle_initialization_click(self, pos):
        """Gère le placement pendant l'initialisation"""
        if self.adding_forbidden:  # Ne pas placer de pièces en mode point noir
            return
                    
        target_pos = self._get_nearest_valid_position(pos)
        if target_pos and self.board._is_valid_initial_position(target_pos):
            # Vérifie aussi que la position n'est pas interdite
            if not self.board.is_position_forbidden(target_pos):
                self.board._place_piece(target_pos, 'player1')
                self.pieces_placed['player1'] += 1
                
                if self._check_initialization_complete():
                    return
                
                self.current_player = 'player2'
                placement = self.ai_player_one.choisir_placement()
                if placement:  # S'assurer que l'IA a trouvé une position valide
                    self.board._place_piece(placement, 'player2')
                    self.pieces_placed['player2'] += 1
                    
                    if self._check_initialization_complete():
                        return
                    self._switch_player() 
    
    def _check_initialization_complete(self):
        """Vérifie si tous les pions sont placés"""
        if (self.pieces_placed['player1'] >= self.total_pieces_to_place and
            self.pieces_placed['player2'] >= self.total_pieces_to_place):
            self.initialization_phase = False
            self._switch_player()
            return True
        return False
    
    def _try_move_piece(self, pos):
        """Tente de déplacer le pion sélectionné"""
        target_pos = self._get_nearest_valid_position(pos)
        
        if not target_pos:
            self.selected_piece.selected = False
            self.selected_piece = None
            return
            
        if self._is_valid_move(self.selected_piece, target_pos):
            self.selected_piece.move(target_pos[0], target_pos[1])
            
            if self._check_win_condition(self.current_player):
                print(f"Le joueur {self.current_player} a gagné !")
                return
            
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
            
            if dist < min_dist:
                min_dist = dist
                nearest_pos = vpos
        
        if min_dist <= (self.board.piece_radius * 2)**2:
            return nearest_pos
        return None
    
    def _is_valid_move(self, piece, target_pos):
        """Vérifie si le mouvement est valide"""
        # Vérifie si la position est interdite
        if self.board.is_position_forbidden(target_pos):
            return False

        # Pas en dehors de la table
        if not (self.board.border_x <= target_pos[0] <= self.board.border_x + self.board.border_size and
        self.board.border_y <= target_pos[1] <= self.board.border_y + self.board.border_size):
            return False

        # 1. Vérifie que la case cible est vide
        for p in self.board.pieces:
            if p.x == target_pos[0] and p.y == target_pos[1]:
                # print("Case non vide")
                return False
        
        step = self.board.border_size // 2
        dx = abs(piece.x - target_pos[0])
        dy = abs(piece.y - target_pos[1])
        
        # 2. Vérifie que le déplacement est d'une case
        if not ((dx == step and dy == 0) or  # Horizontal
                (dy == step and dx == 0) or  # Vertical
                (dx == step and dy == step)):  # Diagonal
            # print("Mouvement interdite")
            return False
        
        # 3. Vérifie les diagonales interdites (en coordonnées relatives)
        piece_rel = self._absolute_to_relative(piece.x, piece.y)
        target_rel = self._absolute_to_relative(target_pos[0], target_pos[1])
        
        forbidden_diagonals = {
            (0.5, 0): [(1, 0.5), (0, 0.5)],    # (150,0) → (300,150), (0,150)
            (0, 0.5): [(0.5, 0), (0.5, 1)],    # (0,150) → (150,0), (150,300)
            (0.5, 1): [(0, 0.5), (1, 0.5)],    # (150,300) → (0,150), (300,150)
            (1, 0.5): [(0.5, 0), (0.5, 1)]     # (300,150) → (150,0), (150,300)
        }
        
        if piece_rel in forbidden_diagonals:
            if target_rel in forbidden_diagonals[piece_rel]:
                # print("piece_rel" + str(piece_rel))
                # print("target_rel : " + str(target_rel))
                
                # print("")
                return False
        
        # 4. Vérifie les pièces intermédiaires (pour horizontaux/verticaux)
        if dx != step or dy != step:  # Si ce n'est pas une diagonale
            mid_x = piece.x + (target_pos[0] - piece.x) // 2
            mid_y = piece.y + (target_pos[1] - piece.y) // 2
            if any(p.x == mid_x and p.y == mid_y for p in self.board.pieces):
                return False
        
        return True
    
    def _absolute_to_relative(self, x, y):
        """Convertit des coordonnées absolues en relatives (0-1)"""
        x_rel = round((x - self.board.border_x) / self.board.border_size, 2)
        y_rel = round((y - self.board.border_y) / self.board.border_size, 2)
        return (x_rel, y_rel)
    
    def _switch_player(self):
        """Change le tour de joueur"""
        self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
    
    def draw(self):
        """Dessine le plateau et les pions"""
        self.board.draw_board()
    
    def _check_win_condition(self, player):
        """Vérifie si le joueur actuel a gagné""" 
        player_pieces = [p for p in self.board.pieces if p.owner == player]
         
        for i in range(len(player_pieces)):
            for j in range(i+1, len(player_pieces)):
                for k in range(j+1, len(player_pieces)):
                    if self._are_aligned(player_pieces[i], player_pieces[j], player_pieces[k]):
                        self.game_over = True 
                        self.winner = self.current_player
                        return True
        return False
    
    def _are_aligned(self, p1, p2, p3):
        """Vérifie si 3 pions sont alignés""" 
        # Horizontal
        if p1.y == p2.y == p3.y:
            return True
        
        # Vertical
        if p1.x == p2.x == p3.x:
            return True
        
        # Alignement diagonal (même pente)
        # On évite la division par zéro en utilisant la multiplication
        dx1 = p2.x - p1.x
        dy1 = p2.y - p1.y
        dx2 = p3.x - p1.x
        dy2 = p3.y - p1.y
        
        return dx1 * dy2 == dx2 * dy1