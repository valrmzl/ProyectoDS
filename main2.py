import ast
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
import pickle
import sys
from observable import Observable
from jugador import Jugador
from entidades import Moneda, Enemigo, Lava, Plataforma, Exit
from world import World
from config import *
from game import *

# Función para reiniciar el nivel
def reiniciar_nivel(nivel):
    """
    Reinicia el nivel del juego.

    Parámetros:
    nivel (int): El número del nivel a reiniciar.

    Devuelve:
    World: Una nueva instancia del mundo con el nivel reiniciado.
    """
    global player_name
    jugador.reset(100, screen_height-130, player_name)
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()

    # Cargar el nivel desde data y crear el mundo
    if path.exists(f'nivel{nivel}_data'):
        with open(f'nivel{nivel}_data', 'r') as file:
            world_data_str = file.read()
            world_data = ast.literal_eval(world_data_str)

    world = World(world_data, GameObjectFactory)

    return world

world = World(world_data, GameObjectFactory)

# Botones
restart_button = Button(screen_width//2-50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 250, screen_height // 2, exit_img)

# Bucle principal del juego
run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            player_selection = PlayerSelection()
            player_selection.mostrar_seleccion()
            player_name = player_selection.seleccionado
            jugador = Jugador(100, screen_height - 130, player_name)
            moneda_score.add_observer(jugador)
            main_menu = False
    else:
        world.draw(screen)

        if game_over == 0:
            blob_group.update()
            platform_group.update()

            if pygame.sprite.spritecollide(jugador, moneda_group, True):
                score += 1
                jugador.recolectar_moneda()
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        moneda_group.draw(screen)

        game_over = jugador.update(game_over, world, jump_fx)

        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reiniciar_nivel(nivel)
                game_over = 0
                score = 0

        if game_over == 1:
            nivel += 1
            if nivel <= nivel_maximo:
                world_data = []
                world = reiniciar_nivel(nivel)
                game_over = 0
            else:
                draw_text('YOU WIN!! :D  ', font, blue, (screen_width//2)-140, (screen_height//2))
                if restart_button.draw():
                    nivel = 1
                    world_data = []
                    world = reiniciar_nivel(nivel)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
