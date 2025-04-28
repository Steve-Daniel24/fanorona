from board import Board
from pieces import Piece
from utils import utils

from game_win import displayer

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
        # Le code existant pour le jeu normal
        else:
            if not self.selected_piece:
                for piece in self.board.pieces:
                    if piece.owner == self.current_player and piece.is_clicked(pos):
                        self.selected_piece = piece
                        piece.selected = True
                        break
            else:
                self._try_move_piece(pos)
    
    def toggle_forbidden_mode(self):
        """Active/désactive le mode ajout de points noirs"""
        self.adding_forbidden = not self.adding_forbidden
        
    def tour_ia(self):
        coup = self.ai_player_one.choisir_coup()
        
        if coup:
            piece, (x, y) = coup
            piece.move(x, y)
            self._check_win_condition("player2")
            self._switch_player()
    
    def _handle_initialization_click(self, pos):
        """Gère le placement pendant l'initialisation"""
        if self.adding_forbidden: 
            return
        
        target_pos = self._get_nearest_valid_position(pos)
        x_rel = round((target_pos[0] - self.board.border_x) / self.board.border_size, 2)
        y_rel = round((target_pos[1] - self.board.border_y) / self.board.border_size, 2)
        
        # Vérification explicite du centre (coordonnées relatives et absolues)
        if (x_rel == 0.5 and y_rel == 0.5) or \
        (pos[0] == self.board.border_x + self.board.border_size//2 and 
            pos[1] == self.board.border_y + self.board.border_size//2) :
            # if self.pieces_placed['player1'] == 0: 
                return
        
        if target_pos and self.board._is_valid_initial_position(target_pos):
            # Vérifie aussi que la position n'est pas un point noir
            if not self.board.is_position_forbidden(target_pos):
                self.board._place_piece(target_pos, 'player1')
                self.pieces_placed['player1'] += 1
                
                self._check_win_condition(self.current_player)
                
                if self._check_initialization_complete():
                    return
                
                self.current_player = 'player2'
                placement = self.ai_player_one.choisir_placement(self.pieces_placed['player2'], self.pieces_placed['player1'])
                
                if placement:
                    self.board._place_piece(placement, 'player2')
                    self.pieces_placed['player2'] += 1
                    
                    self._check_win_condition(self.current_player)
                    
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
        
        if self.board._est_coup_valide(self.selected_piece, target_pos, self.board):
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
    
    def _switch_player(self):
        """Change le tour de joueur"""
        self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
    
    def draw(self):
        """Dessine le plateau et les pions"""
        self.board.draw_board()
        
        if self.game_over:
            displayer.displayer._display_win_message(self, self.board)
    
    def _check_win_condition(self, player):
        """Vérifie si le joueur actuel a gagné""" 
        player_pieces = [p for p in self.board.pieces if p.owner == player]
        
        for i in range(len(player_pieces)):
            for j in range(i+1, len(player_pieces)):
                for k in range(j+1, len(player_pieces)):
                    if utils._are_aligned(player_pieces[i], player_pieces[j], player_pieces[k]):
                        self.game_over = True 
                        self.winner = player
                        
                        print(f"Le joueur {player} a gagné avec l'alignement :")
                        print(f"- {player_pieces[i].x}, {player_pieces[i].y}")
                        print(f"- {player_pieces[j].x}, {player_pieces[j].y}")
                        print(f"- {player_pieces[k].x}, {player_pieces[k].y}")
                        return True
        
        return False