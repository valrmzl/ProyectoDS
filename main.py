import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

# ventana
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("El super juego de Vale, Chris y Sebas")

# Variables del juego
tile_size = 50

# cargar imagenes
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')


# Clase para mostrar mi jugador
class Jugador():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5): #Cargaremos las 4 imagenes para la animación. Izquierda y derecha
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0  # Variables creadas para detectar colisiones
        dy = 0
        walk_cooldown = 5

        # Obtener clics
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
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
                    dy = tile[1].top -self.rect.bottom
                    self.vel_y = 0



        # Actualizar las coordenadas del jugador
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # Dibujar jugador EN LA PLANTALLA
        screen.blit(self.image, self.rect)
        # dibujamos el recatngulo de para el elemento del jugador
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)


class World():
    # constructor
    def __init__(self, data):

        self.tile_list = []
        # cargar imagenes
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    # pero necesito saber donde la voy a poner
                    img_rect = img.get_rect()

                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    # pero necesito saber donde la voy a poner
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemigo(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #dibujamos el rectangulo para cada elemento
            pygame.draw.rect(screen, (255,255,255), tile[1], 2)


# esto es lo que me va a permitir ubicar las cosas que quiero mostrar
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

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
        ##moviendolos derecha e ixquierda
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

# Creación de instancias
jugador = Jugador(100, screen_height - 130)
blob_group = pygame.sprite.Group() #crea un nuevo grupo vacio para despues poder añadirle enemigos
world = World(world_data)

# necesitamos un loop para que la ventana se muestre mucho tiempo
# si no se cerraria
run = True
while run:

    clock.tick(fps)

    # le estoy diciendo en donde quiero que se muestre
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    world.draw()


    blob_group.update()
    blob_group.draw(screen)

    jugador.update()

    for event in pygame.event.get():
        # EL BOTON DE X
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()  # sin esta linea no se veria el fondo

pygame.quit()
