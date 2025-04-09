# main.py
import pygame
from game_manager import GameManager

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fanorona Telo")

game = GameManager(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                game.handle_click(event.pos)
    
    screen.fill((240, 217, 181)) 
    game.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()