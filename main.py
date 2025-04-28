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

last_move_time = 0
ia_move_delay = 1

running = True
while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                game.handle_click(event.pos)
                last_move_time = current_time 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f: 
                game.toggle_forbidden_mode()
    
    # Faire jouer l'IA si c'est son tour et que le délai est écoulé
    if (not game.initialization_phase and game.current_player == 'player2' and not game.game_over 
        and current_time - last_move_time >= ia_move_delay):
        game.tour_ia()
        last_move_time = current_time
    
    screen.fill((240, 217, 181)) 
    game.draw()
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()