# main.py
import pygame
import time
from game_manager import GameManager

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fanorona Telo")

game = GameManager(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
clock = pygame.time.Clock()

# Variable pour suivre le temps du dernier coup
last_move_time = 0
ia_move_delay = 1  # Délai en secondes

running = True
while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                game.handle_click(event.pos)
                last_move_time = current_time  # Mettre à jour le temps du dernier coup
    
    # Faire jouer l'IA si c'est son tour et que le délai est écoulé
    if (not game.initialization_phase and game.current_player == 'player2' and not game.game_over 
        and current_time - last_move_time >= ia_move_delay):
        game.tour_ia()
        last_move_time = current_time  # Réinitialiser le timer
    
    screen.fill((240, 217, 181)) 
    game.draw()
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()