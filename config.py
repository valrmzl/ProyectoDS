"""
Juego con Pygame: "El super juego de Vale, Chris y Sebas"
Archivo con variables, inicialización, funciones, y configuraciones básicas
"""

import pygame
from pygame.locals import *
from pygame import mixer

# Configuración de variables globales
tile_size = 50
jump_height = -15

clock = pygame.time.Clock()
fps = 60

# Configuración de la ventana
screen_width = 1000
screen_height = 1000

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
pygame.display.set_caption("El super juego de Vale, Chris y Sebas")
screen = pygame.display.set_mode((screen_width, screen_height))

# Configuración de fuente y color para el score
font_score = pygame.font.SysFont('Bauhus 93', 30)

# Configuración para el Game Over
font = pygame.font.SysFont('Bauhus 93', 70)

white = (255, 255, 255)
blue = (0, 0, 255)

# Variables del juego
game_over = 0
main_menu = True
player_name = ""
nivel = 1
nivel_maximo = 2
score = 0  # Puntuación de las monedas

# Cargar imágenes
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/pasillo.jpg')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# Cargar efectos de sonido
moneda_fx = pygame.mixer.Sound('img/coin.wav')
moneda_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_fx = pygame.mixer.Sound('img/music.wav')
game_fx.set_volume(0.5)

# Función para mostrar el score en la pantalla
def draw_text(text, font, text_col, x, y):
    """
    Muestra un texto en la pantalla.

    Parámetros:
    text (str): El texto que se mostrará.
    font (pygame.font.Font): La fuente del texto.
    text_col (tuple): El color del texto en formato RGB.
    x (int): La posición horizontal del texto.
    y (int): La posición vertical del texto.
    """
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Clase para representar botones en el juego
class Button():
    def __init__(self, x, y, image):
        """
        Inicializa un botón con una posición y una imagen.

        Parámetros:
        x (int): La posición horizontal del botón.
        y (int): La posición vertical del botón.
        image (pygame.Surface): La imagen del botón.
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        """
        Dibuja el botón en la pantalla y maneja las interacciones del mouse.

        Devuelve:
        bool: True si el botón ha sido clickeado, False de lo contrario.
        """
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

# Crear grupos de sprites
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
moneda_group = pygame.sprite.Group()
