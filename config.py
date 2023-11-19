import pygame
from pygame.locals import *
from pygame import mixer

tile_size = 50
jump_height = -15

clock = pygame.time.Clock()
fps = 60

# ventana
screen_width = 1000
screen_height = 1000

pygame.mixer.pre_init(44100, -16, 2, 512) #configuracion default recomendada
mixer.init()
pygame.init()
pygame.display.set_caption("El super juego de Vale, Chris y Sebas")
screen = pygame.display.set_mode((screen_width, screen_height))

#fuente  y color del score
font_score = pygame.font.SysFont('Bauhus 93', 30)

#para el game over
font = pygame.font.SysFont('Bauhus 93', 70)


white = (255,255, 255)
blue = (0,0, 255)

# Variables del juego
game_over = 0
main_menu = True
player_name = ""
nivel = 1
nivel_maximo = 2
score = 0 #el de las monedas

# cargar imagenes
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/pasillo.jpg')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

#cargar musica
moneda_fx = pygame.mixer.Sound('img/coin.wav')
moneda_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_fx = pygame.mixer.Sound('img/music.wav')
game_fx.set_volume(0.5)

#mostrar el score
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw(self):
        action = False
        #posicion mouse
        pos = pygame.mouse.get_pos()
        
        #checar mouse
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
                
        screen.blit(self.image, self.rect)
        
        return action
    
    
blob_group = pygame.sprite.Group() #crea un nuevo grupo vacio para despues poder añadirle enemigos
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
moneda_group = pygame.sprite.Group()
