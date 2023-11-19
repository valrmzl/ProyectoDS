# main.py
import pygame
from game import Game

# Inicializar pygame y crear una instancia del juego
pygame.init()
game = Game()

# Bucle principal
while game.is_running():
    game.handle_events()
    game.update()
    game.draw()

# Finalizar pygame al salir del bucle
pygame.quit()
