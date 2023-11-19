from observable import Observable
import ast
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
import pickle
import sys
from config import *

def verificar_salto(func):
    """
    Decorador que ajusta la altura del salto del jugador cada vez que recolecta 10 monedas.

    Parámetros:
    func (function): La función a decorar.

    Devuelve:
    function: La función decorada.
    """
    def wrapper(self):
        func(self)  
        if self.contador_monedas == 10:
            print("10 MONEDAS")
            global jump_height
            jump_height -= 5 
            self.contador_monedas = 0  
    return wrapper

class Jugador(Observable):
    """
    Clase que representa al jugador en el juego.
    """
    def __init__(self, x, y, nombre):
        """
        Inicializa un nuevo jugador.

        Parámetros:
        x (int): La posición horizontal inicial del jugador.
        y (int): La posición vertical inicial del jugador.
        nombre (str): El nombre del jugador para cargar las imágenes correspondientes.
        """
        Observable.__init__(self)
        self.reset(x, y, nombre)
        self.contador_monedas = 0

    def update(self, game_over, world, jump_fx):
        """
        Actualiza la posición y el estado del jugador en el juego.

        Parámetros:
        game_over (int): El estado del juego (0: en curso, 1: nivel completado, -1: juego terminado).
        world (World): La instancia del mundo del juego.
        jump_fx (pygame.mixer.Sound): El efecto de sonido para el salto del jugador.

        Devuelve:
        int: El estado actualizado del juego después de la actualización del jugador.
        """
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = jump_height
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1

            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction
                    if platform.move_y != 0:
                        self.rect.y += platform.move_direction * platform.move_y

            self.rect.x += dx
            self.rect.y += dy
        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER !!!', font, blue, (screen_width // 2) - 140, (screen_height // 2))
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over

    @verificar_salto
    def recolectar_moneda(self):
        """
        Método que maneja la recolección de monedas por parte del jugador.

        Este método debe llamarse cuando el jugador recolecta una moneda.
        """
        self.notify_observers("Moneda recolectada")
        self.contador_monedas += 1

    def reset(self, x, y, nombre):
        """
        Restablece las propiedades del jugador a su estado inicial.

        Parámetros:
        x (int): La posición horizontal inicial del jugador.
        y (int): La posición vertical inicial del jugador.
        nombre (str): El nombre del jugador para cargar las imágenes correspondientes.
        """
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5):
            img_right = pygame.image.load(f'img/{nombre}/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
