
from  observable import Observable
import ast
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
import pickle #libreria que ayuda a importar la data de cada nivel en python
import sys
from entidades import Moneda,Enemigo,Plataforma,Lava,Exit

class World():
    def __init__(self, data,GameObjectFactory):
        self.tile_list = []
        self.create_objects(data,GameObjectFactory)

    def create_objects(self, data,GameObjectFactory):
        tile_size = 50
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile in [1, 2]:
                    self.create_tile(tile, col_count, row_count)
                elif tile == 3:
                    GameObjectFactory.create_object("enemigo", col_count * tile_size, row_count * tile_size + 15)
                elif tile == 4:
                    GameObjectFactory.create_object("plataforma", col_count * tile_size, row_count * tile_size, 1, 0)
                elif tile == 5:
                    GameObjectFactory.create_object("plataforma", col_count * tile_size, row_count * tile_size, 0, 1)
                elif tile == 6:
                    GameObjectFactory.create_object("lava", col_count * tile_size, row_count * tile_size + int(tile_size // 2))
                elif tile == 7:
                    GameObjectFactory.create_object("moneda", col_count * tile_size + (tile_size // 2), row_count * tile_size - (tile_size//2))
                elif tile == 8:
                    GameObjectFactory.create_object("exit", col_count * tile_size, row_count * tile_size - (tile_size//2))

                col_count += 1
            row_count += 1
    def create_tile(self, tile_type, x, y):
        tile_size = 50
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        img = pygame.transform.scale(dirt_img if tile_type == 1 else grass_img, (tile_size, tile_size))
        img_rect = img.get_rect()
        img_rect.x = x * tile_size
        img_rect.y = y * tile_size
        tile_instance = (img, img_rect)
        self.tile_list.append(tile_instance)


    def draw(self,screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
