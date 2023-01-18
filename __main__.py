

import OpenGL
import pygame
from pygame.locals import *
import random
import sys
import os
import json
import menu_logic
import render_logic
import game_logic
from OpenGL.GLU import *
from OpenGL.GL import *



config = open("config/config.json")
config = json.load(config)

current_location = os.getcwd()
# set up from config
resolution = config["settings"]["video_conf"]["resolution"].split("x") # returns array with [x, y]
resolution[0], resolution[1] = int(resolution[0]), int(resolution[1]) # sets resolution to ints in array
fullscreen = config["settings"]["video_conf"]["fullscreen"] # returns a boolean

menu_bg = config["element_data"]["main_menu"]["bg_colour"]
menu_image = "assets/UI/main_menu.jpg"

# CLEANUP FROM PREVIOUS RUN
for x in os.listdir(current_location):
    if x[-4::] == ".tmp":
        print("DEL " + x)
        os.remove(current_location + "\\" + x)

pygame.init()
clock = pygame.time.Clock()
# end setup

if fullscreen == True: # creates the screen
    screen = pygame.display.set_mode((resolution[0], resolution[1]), FULLSCREEN)
else:
    screen = pygame.display.set_mode((resolution[0], resolution[1]))


pygame.display.set_caption('SCP site design')
logo = pygame.image.load(current_location + "\\assets\\UI\\SCP_logo02.png")
menu_image = pygame.image.load("assets/UI/main_menu02.jpg").convert()
menu_image = pygame.transform.scale(menu_image, (resolution[0] - 400, resolution[1] + 200))

pygame.display.set_icon(logo)
# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((menu_bg[0], menu_bg[1], menu_bg[2]))

# represents which menu the user is in
# index 0 is main_menu, 1 is settigs, 2 is in_game, 3 is load_game, 4 is new game, 5 is a transition to change graphics(see change_to_opengl() in game_logic)
# 5 is run only once, as it is used to change the graphics, then sets menu to 2
in_menu = [True, False, False, False, False, False]
scroll_zoom = 0
previous_scroll = 0
camera_x, camera_y, camera_z = 0, 0, -2

click_counter = 0
while True:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if config["settings"]["debug"]["debug_keys"]:
                if event.key == pygame.K_ESCAPE:
                    exit()
        if event.type == pygame.MOUSEWHEEL:
            scroll_zoom += event.y
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == True:
        click_counter += 1 # counts how long a click has been held down for
    else:
        click_counter = 0
    if in_menu[0] == True:
        screen.blit(menu_image, (400, 0))
        menu_logic.main_menu()
    if in_menu[1] == True:
        menu_logic.settings()
    if in_menu[3] == True:
        menu_logic.load_game_sc()
    if in_menu[4] == True:
        game_logic.new_game() # creates a new file
    if in_menu[2] == True: # Do all opengl rendering and game logic here.
        render_logic.render_game(loaded_game)
        pygame.display.flip()
        pygame.time.wait(10)
        previous_scroll = scroll_zoom
    if in_menu[5] == True: # sets the graphics to opengl, and loads the file that needs to be read
        game_logic.change_to_opengl()

        loaded_game = game_logic.load_game(menu_logic.selected_file)
        menu_logic.set_menu(2) # starts rendering process
    if in_menu[2] == False: # If not in opengl, then render pygame
        pygame.display.update()
        clock.tick(60)