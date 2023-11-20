from observable import Observable
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
from config import tile_size

class Enemigo(pygame.sprite.Sprite):
    """
    Clase que representa a un enemigo en el juego.
    """
    def __init__(self, x, y)-> None:
        """
        Inicializa un nuevo enemigo.

        Parámetros:
        x (int): La posición horizontal inicial del enemigo.
        y (int): La posición vertical inicial del enemigo.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self)-> None:
        """
        Actualiza la posición del enemigo.

        Mueve al enemigo hacia la derecha e izquierda en un patrón predefinido.
        """
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Plataforma(pygame.sprite.Sprite):
    """
    Clase que representa una plataforma en el juego.
    """
    def __init__(self, x, y, move_x, move_y)-> None:
        """
        Inicializa una nueva plataforma.

        Parámetros:
        x (int): La posición horizontal inicial de la plataforma.
        y (int): La posición vertical inicial de la plataforma.
        move_x (int): La distancia horizontal que la plataforma se moverá.
        move_y (int): La distancia vertical que la plataforma se moverá.
        """
        pygame.sprite.Sprite.__init__(self)
        img =  pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self)-> None:
        """
        Actualiza la posición de la plataforma.

        Mueve la plataforma hacia la derecha e izquierda en un patrón predefinido.
        """
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    """
    Clase que representa una superficie de lava en el juego.
    """
    def __init__(self, x, y):
        """
        Inicializa una nueva superficie de lava.

        Parámetros:
        x (int): La posición horizontal inicial de la lava.
        y (int): La posición vertical inicial de la lava.
        """
        pygame.sprite.Sprite.__init__(self)
        img =  pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

class Moneda(pygame.sprite.Sprite, Observable):
    """
    Clase que representa una moneda en el juego.
    """
    def __init__(self, x, y)-> None:
        """
        Inicializa una nueva moneda.

        Parámetros:
        x (int): La posición horizontal inicial de la moneda.
        y (int): La posición vertical inicial de la moneda.
        """
        pygame.sprite.Sprite.__init__(self)
        Observable.__init__(self)
        img =  pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def recolectar(self)-> None:
        """
        Recolecta la moneda y notifica a los observadores.

        Este método debe llamarse cuando el jugador recolecta la moneda.
        """
        self.notify_observers("Moneda recolectada")
        self.kill()

class Exit(pygame.sprite.Sprite):
    """
    Clase que representa la salida en el juego.
    """
    def __init__(self, x, y)-> None:
        """
        Inicializa una nueva salida.

        Parámetros:
        x (int): La posición horizontal inicial de la salida.
        y (int): La posición vertical inicial de la salida.
        """
        pygame.sprite.Sprite.__init__(self)
        img =  pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
