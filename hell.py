import pygame
import copy

from board import Board
from pieces import Piece
from utils import utils

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
            print("piece : " + str(piece.x) + " " + str(piece.y))
            print("Coups valide : ")
            for coup in self._coups_possibles(piece):
                # Évalue seulement les coups valides
                if self.board._est_coup_valide(piece, coup, self.board):
                    print("target : " + str(coup[0]) + " " + str(coup[1]))
                    
                    nouveau_plateau = self._simuler_coup(piece, coup)
                    score = self._minimax(nouveau_plateau, profondeur=5, est_maximisant=False)
                    
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (piece, coup)
            
            print()
        
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
        
        print("palteau de simulation")
        return nouveau_plateau
    
    def _simuler_coup_with_board(self, piece, coup, plateau):
        """Crée une VRAIE copie du plateau"""
        nouveau_plateau = Board(None, plateau.SCREEN_WIDTH, plateau.SCREEN_HEIGHT)
        nouveau_plateau.pieces = [
            Piece(p.x, p.y, p.radius, p.color, p.owner)
            for p in plateau.pieces
        ]
        
        for p in nouveau_plateau.pieces:
            if p.x == piece.x and p.y == piece.y:
                p.move(coup[0], coup[1])
                break
        
        return nouveau_plateau
    
    def _evaluer_plateau(self, plateau):
        """Évalue l'avantage de l'IA"""
        score = 0 
         
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
                        # print("horizontal")
                        # print( joueur + " : " + str(p1.x) + " " + str(p1.y) + " " + str(p2.x) + " " + str(p2.y) + " " + str(p3.x) + " " + str(p3.y))
                        
                        return True
                    
                    # Alignement vertical (même x)
                    if p1.x == p2.x == p3.x:
                        # print("vertical")
                        # print(joueur + " : " + str(p1.x) + " " + str(p1.y) + " " + str(p2.x) + " " + str(p2.y) + " " + str(p3.x) + " " + str(p3.y))
                        return True
                    
                    # Alignement diagonal (même pente)
                    dx1 = p2.x - p1.x
                    dy1 = p2.y - p1.y
                    dx2 = p3.x - p1.x
                    dy2 = p3.y - p1.y
                    
                    if dx1 * dy2 == dx2 * dy1:  # Évite la division par zéro
                        # print("oblique")
                        # print(joueur + " : " + str(p1.x) + " " + str(p1.y) + " " + str(p2.x) + " " + str(p2.y) + " " + str(p3.x) + " " + str(p3.y))
                        return True
        
        return False
    
    def _minimax(self, plateau, profondeur, est_maximisant):
        if profondeur == 0 or self._a_trois_alignes(plateau, 'player1') or self._a_trois_alignes(plateau, 'player2'):
            return self._evaluer_plateau(plateau)
        
        if est_maximisant:
            best = -float('inf')
            for piece in [p for p in plateau.pieces if p.owner == self.player_name]:
                for coup in self._coups_possibles(piece):
                    if self.board._est_coup_valide(piece, coup, plateau):
                        new_board = self._simuler_coup_with_board(piece, coup, plateau)
                        best = max(best, self._minimax(new_board, profondeur-1, False))
            return best
        else:
            best = float('inf')
            adversaire = 'player1' if self.player_name == 'player2' else 'player2'
            for piece in [p for p in plateau.pieces if p.owner == adversaire]:
                for coup in self._coups_possibles(piece):
                    if self.board._est_coup_valide(piece, coup, plateau):
                        new_board = self._simuler_coup_with_board(piece, coup, plateau)
                        best = min(best, self._minimax(new_board, profondeur-1, True))
            return best
    
    def _absolute_to_relative(self, x, y):
        """Convertit des coordonnées absolues en relatives (0-1)"""
        x_rel = round((x - self.board.border_x) / self.board.border_size, 2)
        y_rel = round((y - self.board.border_y) / self.board.border_size, 2)
        return (x_rel, y_rel)
    
    def choisir_placement(self, number_of_piece, number_of_piece_adverse):
        """Choisit la meilleure position pour placer une pièce"""
        print("number_of_piece : " + str(number_of_piece))
        print("number_of_piece_adverse : " + str(number_of_piece_adverse))
        print()
        
        # positions_possibles = [
        #     (0, 0), (0.5, 0), (1, 0),
        #     (0, 0.5), (0.5, 0.5), (1, 0.5),
        #     (0, 1), (0.5, 1), (1, 1)
        # ]
        
        positions_possibles = [
            (0, 0), (0.5, 0), (1, 0),
            (0, 0.5),   (1, 0.5),
            (0, 1), (0.5, 1), (1, 1)
        ]
        
        
        # Filtrer les positions interdites et occupées
        positions_valides = []
        for pos_rel in positions_possibles:
            x, y = utils.relative_to_absolute(pos_rel[0], pos_rel[1],
                                            self.board.border_x,
                                            self.board.border_y,
                                            self.board.border_size)
            if (not any(p.x == x and p.y == y for p in self.board.pieces) and
                not self.board.is_position_forbidden((x, y))):
                positions_valides.append((x, y))
        
        if not positions_valides:
            return None
        
        # Prioriser le centre si disponible
        # if (number_of_piece >= 1) : 
        #     centre_x, centre_y = utils.relative_to_absolute(0.5, 0.5,
        #                                                 self.board.border_x,
        #                                                 self.board.border_y,
        #                                                 self.board.border_size)
        #     if (centre_x, centre_y) in positions_valides:
        #         return (centre_x, centre_y)
        
        # Choisir la meilleure position selon l'évaluation
        meilleur_score = -float('inf')
        meilleure_position = None
        
        for pos in positions_valides:
            pos_rel = self._absolute_to_relative(pos[0], pos[1])
            score = self._evaluer_position(pos_rel, number_of_piece, number_of_piece_adverse)
            
            if score > meilleur_score:
                meilleur_score = score
                meilleure_position = pos
        
        return meilleure_position
    
    def _evaluer_position(self, pos_rel, number_of_piece, number_of_piece_adverse):
        """Évalue l'avantage d'une position (en coordonnées relatives)"""
        score = 0
                
        adversaire = 'player1' if self.player_name == 'player2' else 'player2'
        pieces_adverses = [p for p in self.board.pieces if p.owner == adversaire]
        
        if number_of_piece_adverse >= 2: 
            print("tapenana")
            score = self.compter_score(score, pieces_adverses, pos_rel, 150)
            
        pieces_joueur = [p for p in self.board.pieces if p.owner == self.player_name]
        if number_of_piece >= 2:
            print("plus grand que 2, mitady 3 eme alignement")
            score = self.compter_score(score, pieces_joueur, pos_rel, 100)
        
        if (number_of_piece >= 1) :
            if pos_rel == (0.5, 0.5):
                score += 3
             
        elif pos_rel in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            score += 1
             
        elif pos_rel in [(0.5, 0), (0, 0.5), (0.5, 1), (1, 0.5)]:
            score += 2
        
        return score
    
    def compter_score(self, score_actuelle, pieces, pos_rel, score_a_ajouter):
        for i in range(len(pieces)):
            for j in range(i+1, len(pieces)):
                p1 = pieces[i]
                p2 = pieces[j]
                    
                p1_rel = self._absolute_to_relative(p1.x, p1.y)
                p2_rel = self._absolute_to_relative(p2.x, p2.y)
                    
                if self._sont_alignes(p1_rel, p2_rel, pos_rel):
                    score_actuelle += score_a_ajouter 
            
        return score_actuelle
            
    def _sont_alignes(self, p1, p2, p3):
        """Vérifie si 3 positions relatives sont alignées"""
        # Horizontal
        if p1[1] == p2[1] == p3[1]:
            return True
        
        # Vertical
        if p1[0] == p2[0] == p3[0]:
            return True
        
        # Diagonal
        dx1 = p2[0] - p1[0]
        dy1 = p2[1] - p1[1]
        dx2 = p3[0] - p1[0]
        dy2 = p3[1] - p1[1]
        
        return dx1 * dy2 == dx2 * dy1