import pygame

class displayer :
    @staticmethod
    def _display_win_message(Game_manager, board):
        """Affiche un message de victoire stylisé"""
        if not Game_manager.game_over or not Game_manager.winner:
            return
        
        # Création d'une surface semi-transparente pour le fond
        overlay = pygame.Surface((board.SCREEN_WIDTH, board.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Noir semi-transparent
        
        # Affichage de l'overlay
        Game_manager.screen.blit(overlay, (0, 0))
        
        # Configuration du texte
        font_large = pygame.font.Font(None, 30)
        font_small = pygame.font.Font(None, 25)
        
        # Texte principal
        winner_text = f"Le joueur {Game_manager.winner} a gagné !"
        text_surf = font_large.render(winner_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=((board.SCREEN_WIDTH // 3 ) + 50, board.SCREEN_HEIGHT//3))
        Game_manager.screen.blit(text_surf, text_rect)
        
        # Texte secondaire
        restart_text = "Cliquez pour rejouer"
        restart_surf = font_small.render(restart_text, True, (200, 200, 200))
        restart_rect = restart_surf.get_rect(center=((board.SCREEN_WIDTH // 3 ) + 50, board.SCREEN_HEIGHT//3 + 50))
        Game_manager.screen.blit(restart_surf, restart_rect)
        
        pygame.display.flip()