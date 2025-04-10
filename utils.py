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