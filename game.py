import ast
import pygame
from os import path
from pygame.locals import *
import sys
from entidades import Moneda, Enemigo, Lava, Plataforma, Exit
from world import World
from config import *



class PlayerSelection:
    """
    Clase que maneja la selección del jugador al inicio del juego.
    """
    def __init__(self):
        """
        Inicializa una nueva instancia de PlayerSelection.
        """
        self.seleccionado = None

    def mostrar_seleccion(self):
        """
        Muestra la pantalla de selección del jugador y espera hasta que el jugador haya seleccionado un personaje.
        """
        sebas_img = pygame.image.load('img/Sebas/guy1.png')
        vale_img = pygame.image.load('img/Vale/guy1.png')
        chris_img = pygame.image.load('img/Chris/guy1.png')

        sebas_btn = Button(screen_width // 4 - 50, screen_height // 2, sebas_img)
        vale_btn = Button(screen_width // 2 - 50, screen_height // 2, vale_img)
        chris_btn = Button(3 * screen_width // 4 - 50, screen_height // 2, chris_img)

        seleccion_realizada = False

        while not seleccion_realizada:
            clock.tick(fps)
            screen.blit(bg_img, (0, 0))
            draw_text('SELECT YOUR PLAYER', font, white, screen_width // 2 - 200, screen_height // 4)

            if sebas_btn.draw():
                self.seleccionado = "Sebas"
                print("Sebas selected")
                seleccion_realizada = True
            if vale_btn.draw():
                self.seleccionado = "Vale"
                seleccion_realizada = True
            if chris_btn.draw():
                self.seleccionado = "Chris"
                seleccion_realizada = True

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

# una moneda para donde se muestra el score
moneda_score = Moneda(tile_size // 2, tile_size//2)
moneda_group.add(moneda_score)

# cargar el nivel desde data y crear el mundo
with open(f'nivel{nivel}_data', 'r') as file:
    world_data_str = file.read()
    world_data = ast.literal_eval(world_data_str)

row_count = len(world_data)
col_count = len(world_data[0])

# Factory method
class GameObjectFactory:
    """
    Clase que implementa un método de fábrica para crear objetos del juego.
    """
    @staticmethod
    def create_object(object_type, x, y, *args):
        """
        Crea un objeto del juego según el tipo especificado.

        Parámetros:
        object_type (str): El tipo de objeto a crear ("moneda", "enemigo", "plataforma", "lava", "exit", etc.).
        x (int): La posición horizontal del objeto.
        y (int): La posición vertical del objeto.
        args: Argumentos adicionales específicos para ciertos tipos de objetos.

        Devuelve:
        pygame.sprite.Sprite: El objeto del juego creado.
        """
        if object_type == "moneda":
            objeto = Moneda(x, y)
            moneda_group.add(objeto)
        elif object_type == "enemigo":
            objeto = Enemigo(x, y)
            blob_group.add(objeto)
        elif object_type == "plataforma":
            objeto = Plataforma(x, y, *args)
            platform_group.add(objeto)
        elif object_type == "lava":
            objeto = Lava(x, y)
            lava_group.add(objeto)
        elif object_type == "exit":
            objeto = Exit(x, y)
            exit_group.add(objeto)
        # Agrega más tipos según sea necesario
        else:
            raise ValueError(f"Tipo de objeto no válido: {object_type}")
        return objeto
