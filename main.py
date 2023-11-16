import ast
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
import pickle #libreria que ayuda a importar la data de cada nivel en python


pygame.mixer.pre_init(44100, -16, 2, 512) #configuracion default recomendada
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

# ventana
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("El super juego de Vale, Chris y Sebas")

#fuente  y color del score
font_score = pygame.font.SysFont('Bauhus 93', 30)
#para el game over
font = pygame.font.SysFont('Bauhus 93', 70)
white = (255,255, 255)
blue = (0,0, 255)
# Variables del juego
tile_size = 50
game_over = 0
main_menu = True

nivel = 2
nivel_maximo = 2
score = 0 #el de las monedas

# cargar imagenes
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
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


#funcion para reinciar el nivel
def reiniciar_nivel(level):
    jugador.reset(100, screen_height-130)
    #todos mis grupos tambien deben de estar vacios
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    #cargar el nivel desde data y crear el mudno

    if path.exists(f'nivel{nivel}_data'):
        with open(f'nivel{nivel}_data', 'r') as file:
            world_data_str = file.read()
            world_data = ast.literal_eval(world_data_str)

    # Ahora puedes crear el objeto World con los datos cargados
    world = World(world_data)

    return world

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

# Clase para mostrar mi jugador
class Jugador():
    def __init__(self, x, y):
       self.reset(x,y)

    def update(self, game_over):
        dx = 0  # Variables creadas para detectar colisiones
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
        
            # Obtener clics
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
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
                        dy = tile[1].top -self.rect.bottom
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
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
            
        return game_over

    def reset(self,x,y):
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
                if tile == 4:   #Plataformas horizontales
                    plataforma = Plataforma(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(plataforma)
                if tile == 5:   #Plataformas verticales
                    plataforma = Plataforma(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(plataforma)
                if tile == 6:
                    lava =  Lava(col_count * tile_size, row_count * tile_size + int(tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    moneda = Moneda(col_count * tile_size + (tile_size // 2), row_count * tile_size - (tile_size//2))
                    moneda_group.add(moneda)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size//2))
                    exit_group.add(exit)
                
                    
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #dibujamos el rectangulo para cada elemento
            pygame.draw.rect(screen, (255,255,255), tile[1], 2)




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
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img =  pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #para que quede centrada en el bloque
 


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img =  pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

# Creación de instancias
jugador = Jugador(100, screen_height - 130)

blob_group = pygame.sprite.Group() #crea un nuevo grupo vacio para despues poder añadirle enemigos
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
moneda_group = pygame.sprite.Group()

# una moneda para donde se muestra el score
moneda_score = Moneda(tile_size // 2, tile_size//2 )
moneda_group.add(moneda_score)
#cargar el nivel desde data y crear el mudno

with open(f'nivel{nivel}_data', 'r') as file:
    world_data_str = file.read()
    world_data = ast.literal_eval(world_data_str)

# Ahora puedes crear el objeto World con los datos cargados
world = World(world_data)


#botones
restart_button = Button(screen_width//2-50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 250, screen_height // 2, exit_img)

# necesitamos un loop para que la ventana se muestre mucho tiempo
# sino se cerraria
run = True
while run:

    clock.tick(fps)

    # le estoy diciendo en donde quiero que se muestre
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_group.update()
            #actualizar el score de las monedas
            #pero primero vemos si hubo una colision
            if pygame.sprite.spritecollide(jugador, moneda_group,True): #el arguento de true aqui hace que desaparezca
                score += 1
                moneda_fx.play()
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
            
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        moneda_group.draw(screen)

        game_over = jugador.update(game_over)
        
        #si el jugador murio
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reiniciar_nivel(nivel)
                game_over = 0
                score = 0
        #si el juagdor avanza de nivel
        if game_over == 1:
            #resetear y siguiente nivel
            nivel +=1
            #y checar que aun no sea el ultimo nivel
            #estar seguro del nivel
            if nivel <= nivel_maximo:
                world_data = []
                world = reiniciar_nivel(nivel)
                game_over = 0 
                
            else:
                draw_text('YOU WIN!! :D  ', font, blue, (screen_width//2)-140, (screen_height//2))
                #restart 
                if restart_button.draw():
                    nivel = 1
                    world_data = []
                    world = reiniciar_nivel(nivel)
                    game_over = 0 
                    score = 0
                    
                    
                
            

            

    for event in pygame.event.get():
        # EL BOTON DE X
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()  # sin esta linea no se veria el fondo

pygame.quit()
