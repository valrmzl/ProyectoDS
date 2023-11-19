import ast
import pygame
from os import path
from pygame.locals import *
from pygame import mixer
import pickle #libreria que ayuda a importar la data de cada nivel en python
import sys
from  observable import Observable
from jugador import Jugador
from entidades import Moneda,Enemigo,Lava,Plataforma,Exit
from world import World
from config import *
from game import * 

#funcion para reinciar el nivel
def reiniciar_nivel(nivel):
    global player_name
    jugador.reset(100, screen_height-130,player_name)
    #todos mis grupos tambien deben de estar vacios
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()
    #cargar el nivel desde data y crear el mudno

    if path.exists(f'nivel{nivel}_data'):
        with open(f'nivel{nivel}_data', 'r') as file:
            world_data_str = file.read()
            world_data = ast.literal_eval(world_data_str)

    # Ahora puedes crear el objeto World con los datos cargados
    world = World(world_data,GameObjectFactory)

    return world

world = World(world_data,GameObjectFactory)

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
    #screen.blit(sun_img, (100, 100))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
           
            player_selection = PlayerSelection()
            player_selection.mostrar_seleccion()
            player_name = player_selection.seleccionado
            jugador = Jugador(100, screen_height - 130, player_name)
            moneda_score.add_observer(jugador)
            main_menu = False
    else:
        world.draw(screen)

        if game_over == 0:
            blob_group.update()
            platform_group.update()
           
            
            #actualizar el score de las monedas
            #pero primero vemos si hubo una colision
            if pygame.sprite.spritecollide(jugador, moneda_group,True): #el arguento de true aqui hace que desaparezca
                score += 1
                #moneda_fx.play()
                jugador.recolectar_moneda()
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
            
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        moneda_group.draw(screen)

        game_over = jugador.update(game_over, world, jump_fx)
        
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