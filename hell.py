import pygame
import copy

from board import Board
from pieces import Piece

class devil:
    def __init__(self, GameManager, board, player_color):
        self.board = board  
        self.player_name = player_color
        self.GameManager = GameManager
    
    def choisir_coup(self):
        """Trouve le meilleur coup avec MinMax"""
        meilleur_coup = None
        meilleur_score = -float('inf')
        
        for piece in [p for p in self.board.pieces if p.owner == self.player_name]:
            for coup in self._coups_possibles(piece):
                # Évalue seulement les coups valides
                if self.GameManager._is_valid_move(piece, coup):
                    print("Coups valide : ")
                    print("piece : " + str(piece.x) + " " + str(piece.y))
                    print("target : " + str(coup[0]) + " " + str(coup[1]))
                    print()
                    
                    nouveau_plateau = self._simuler_coup(piece, coup)
                    score = self._minimax(nouveau_plateau, profondeur=6, est_maximisant=True)
                    
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (piece, coup)
        
        return meilleur_coup
    
    def _coups_possibles(self, piece):
        """Retourne toutes les positions potentielles autour de la pièce"""
        pas = self.board.border_size // 2
        
        directions = [
            (pas, 0), (-pas, 0),  # Horizontal
            (0, pas), (0, -pas),   # Vertical
            (pas, pas), (-pas, -pas),  # Diagonales
            (pas, -pas), (-pas, pas)
        ]
        
        result = []
        
        for dx, dy in directions:                        
            result.append((piece.x  + dx, piece.y + dy)) 
        
        return result 
    
    def _simuler_coup(self, piece, coup):
        """Crée une copie légère du plateau"""
        nouveau_plateau = Board(None, self.board.SCREEN_WIDTH, self.board.SCREEN_HEIGHT)
        nouveau_plateau.pieces = [
            Piece(p.x, p.y, p.radius, p.color, p.owner)
            for p in self.board.pieces
        ]
        
        for p in nouveau_plateau.pieces:
            if p.x == piece.x and p.y == piece.y:
                p.move(coup[0], coup[1])
                break
        
        return nouveau_plateau
    
    def _evaluer_plateau(self, plateau):
        """Évalue l'avantage de l'IA"""
        score = 0
        pions_ia = len([p for p in plateau.pieces if p.owner == self.player_name])
        pions_adversaire = len(plateau.pieces) - pions_ia
        score += (pions_ia - pions_adversaire) * 10
        
        # Bonus pour les alignements
        if self._a_trois_alignes(plateau, self.player_name):
            score += 100
        if self._a_trois_alignes(plateau, 'player1' if self.player_name == 'player2' else 'player2'):
            score -= 100
            
        return score
    
    def _a_trois_alignes(self, plateau, joueur):
        """Vérifie si un joueur a 3 pions alignés (horizontal, vertical ou diagonal)"""
        pieces = [p for p in plateau.pieces if p.owner == joueur]
        
        # Pas besoin de vérifier si moins de 3 pions
        if len(pieces) < 3:
            return False
        
        # Vérifie toutes les combinaisons possibles de 3 pions
        for i in range(len(pieces)):
            for j in range(i+1, len(pieces)):
                for k in range(j+1, len(pieces)):
                    p1, p2, p3 = pieces[i], pieces[j], pieces[k]
                    
                    # Alignement horizontal (même y)
                    if p1.y == p2.y == p3.y:
                        return True
                    
                    # Alignement vertical (même x)
                    if p1.x == p2.x == p3.x:
                        return True
                    
                    # Alignement diagonal (même pente)
                    dx1 = p2.x - p1.x
                    dy1 = p2.y - p1.y
                    dx2 = p3.x - p1.x
                    dy2 = p3.y - p1.y
                    
                    if dx1 * dy2 == dx2 * dy1:  # Évite la division par zéro
                        return True
        
        return False
    
    def _minimax(self, plateau, profondeur, est_maximisant):
        """Algorithme MinMax"""
        if profondeur == 0:
            return self._evaluer_plateau(plateau)
        
        if est_maximisant:
            best = -float('inf')
            for piece in [p for p in plateau.pieces if p.owner == self.player_name]:
                for coup in self._coups_possibles(piece):
                    if self._est_coup_valide(piece, coup, plateau):
                        new_board = self._simuler_coup(piece, coup)
                        best = max(best, self._minimax(new_board, profondeur-1, False))
            return best
        else:
            best = float('inf')
            adversaire = 'player1' if self.player_name == 'player2' else 'player2'
            for piece in [p for p in plateau.pieces if p.owner == adversaire]:
                for coup in self._coups_possibles(piece):
                    if self._est_coup_valide(piece, coup, plateau):
                        new_board = self._simuler_coup(piece, coup)
                        best = min(best, self._minimax(new_board, profondeur-1, True))
            return best
    
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
                    return False
            
            # 4. Vérifie les pièces intermédiaires (pour horizontaux/verticaux)
            if dx != step or dy != step:  # Si ce n'est pas une diagonale
                mid_x = piece.x + (target_pos[0] - piece.x) // 2
                mid_y = piece.y + (target_pos[1] - piece.y) // 2
                if any(p.x == mid_x and p.y == mid_y for p in board.pieces):
                    return False
            
            return True
        
    def _absolute_to_relative(self, x, y):
        """Convertit des coordonnées absolues en relatives (0-1)"""
        x_rel = round((x - self.board.border_x) / self.board.border_size, 2)
        y_rel = round((y - self.board.border_y) / self.board.border_size, 2)
        return (x_rel, y_rel)