from  observable import Observable
import ast
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
import pickle #libreria que ayuda a importar la data de cada nivel en python
import sys
from config import *


def verificar_salto(func):
    def wrapper(self):
        func(self)  
        if self.contador_monedas == 10:
            print("10 MONEDAS")
            global jump_height
            jump_height -= 5 
            self.contador_monedas = 0  
    return wrapper


# Clase para mostrar mi jugador
class Jugador(Observable):
    def __init__(self, x, y, nombre):
       Observable.__init__(self)  # Agregar esta línea para inicializar la clase base
       self.reset(x,y,nombre)
       self.contador_monedas = 0

    def update(self, game_over, world, jump_fx):
        dx = 0  # Variables creadas para detectar colisiones
        dy = 0
        walk_cooldown = 5
        col_thresh = 20
        

        if game_over == 0:
            # Obtener clics
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = jump_height
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5  # Le restamos 5 pixeles a la posición
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            #Si no se toca ninguna tecla regresaremos a la imagen original
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #Manejo de animación
            if self.counter > walk_cooldown:    #Neceario para la velocidad de caminata
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Agregar gravedad
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Detectar colisiones
            self.in_air = True
            for tile in world.tile_list:
                #checar en x y y de manera separada
                #en x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y , self.width, self.height):
                    dx = 0 # para que deje de moverse 
                #en y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy , self.width, self.height):
                    #checar si abajo del ground ie jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom -self.rect.top
                        self.vel_y = 0
                    #checar si abajo del ground ie falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #colision con los enemigos
            if pygame.sprite.spritecollide(self, blob_group,False):
                game_over = -1
                #game_over_fx.play()
            #colision con lava
            if pygame.sprite.spritecollide(self, lava_group,False):
                game_over = -1
                #game_over_fx.play()
                #print(game_over)
            #colision de cambio de nivel y de salida
            if pygame.sprite.spritecollide(self, exit_group,False):
                game_over = 1

            #Colisión con plataformas
            for platform in platform_group:
                #Colisión en dirección x
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y , self.width, self.height):
                    dx = 0
                #Colisión en dirección y
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #Revisar plataformas por debajo
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #Revisar plataformas por encima
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    #Moverse con la plataforma
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction
                    if platform.move_y != 0:
                        self.rect.y += platform.move_direction * platform.move_y
                
            # Actualizar las coordenadas del jugador
            self.rect.x += dx
            self.rect.y += dy
        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER !!!', font, blue, (screen_width//2)-140, (screen_height//2))
            if self.rect.y > 200:
                self.rect.y -= 5

        # Dibujar jugador EN LA PLANTALLA
        screen.blit(self.image, self.rect)
        # dibujamos el recatngulo de para el elemento del jugador
        # pygame.draw.rect(screen, (255,255,255), self.rect, 2)
            
        return game_over

    @verificar_salto
    def recolectar_moneda(self):
        print("sonidooo")
        #moneda_fx.play()
        self.notify_observers("Moneda recolectada")
        self.contador_monedas += 1
        

    def reset(self,x,y,nombre):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5): #Cargaremos las 4 imagenes para la animación. Izquierda y derecha
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
        