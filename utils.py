# from game_manager import GameManager

class utils:
    @staticmethod
    def relative_to_absolute(x_rel, y_rel, border_x, border_y, border_size):
        """Convertit des coordonnées relatives (0-1) en absolues (pixels)"""
        x = border_x + int(x_rel * border_size)
        y = border_y + int(y_rel * border_size)
        return (x, y)
    
    @staticmethod
    def absolute_to_relative(x, y, board):
        x_rel = (x - board.border_x) / board.border_size
        y_rel = (y - board.border_y) / board.border_size
        return (round(x_rel, 2), round(y_rel, 2))
     
    @staticmethod
    def _check_win_condition(self):
        """Vérifie si le joueur actuel a gagné""" 
        player_pieces = [p for p in self.board.pieces if p.owner == self.current_player]
         
        for i in range(len(player_pieces)):
            for j in range(i+1, len(player_pieces)):
                for k in range(j+1, len(player_pieces)):
                    if self._are_aligned(player_pieces[i], player_pieces[j], player_pieces[k]):
                        self.game_over = True 
                        self.winner = self.current_player
                        return True
        return False
    
    @staticmethod
    def _are_aligned(self, p1, p2, p3):
        """Vérifie si 3 pions sont alignés""" 
        # Horizontal
        if p1.y == p2.y == p3.y:
            return True
        
        # Vertical
        if p1.x == p2.x == p3.x:
            return True
            
        dx1 = p2.x - p1.x
        dy1 = p2.y - p1.y
        dx2 = p3.x - p1.x
        dy2 = p3.y - p1.y
        
        return dx1 * dy2 == dx2 * dy1