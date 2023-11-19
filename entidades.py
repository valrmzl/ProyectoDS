from  observable import Observable
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
from config import tile_size


class Enemigo(pygame.sprite.Sprite): #por default ya tiene un  metodo de update esto que estamos importando
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        ##moviendolos derecha e izquierda
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
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

    def update(self):
        ##moviendolos derecha e izquierda
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img =  pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

class Moneda(pygame.sprite.Sprite, Observable):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        Observable.__init__(self) #COMPORTAMIENTO
        img =  pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #para que quede centrada en el bloque
    
    def recolectar(self):
        self.notify_observers("Moneda recolectada")
        self.kill()


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img =  pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        
