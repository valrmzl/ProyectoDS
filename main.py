print("Hola proyecto de diseño de software")


import pygame
from pygame.locals import *

pygame.init()

#ventana
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("El super juego de Vale, Chris y Sebas")

tile_size = 200
# cargar imagenes
sun_img= pygame.image.load('img/sun.png')
bg_img= pygame.image.load('img/sky.png')

#funcion para ver la cudricula
def cuadricula():
    for line in range(0,6):
        pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (screen_width, line*tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_height))

class World():
    #constructor
    def __init__(self, data) -> None:

        self.title_list = []
        #cargar imagenes
        dirt_img= pygame.image.load('img/dirt.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile ==1:
                    img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    #pero necesito saber donde la voy a poner
                    img_rect = img.get_rect()
                    img_rect.x = col_count* tile_size
                    img_rect.y = row_count* tile_size
                col_count +=1 
            row_count +=1



#esto es lo que me va a permitir ubicar las cosas que quiero mostrar
world_data = [
[1,1,1,1,1],
[1,0,0,0,1],
[1,0,0,0,1],
[1,0,0,0,1],
[1,1,1,1,1]
]

#necesitamos un loop para que la ventana se muestre mucho tiempo
# si no se cerraria
run = True
while run:
    #le estoy diciendo en donde quiero que se muestre
    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,10))
    cuadricula()
    for event in pygame.event.get():
        #EL BOTON DE X
        if event.type == pygame.QUIT:
            run = False

        pygame.display.update() #sin esta linea no se veria el fondo

pygame.quit()