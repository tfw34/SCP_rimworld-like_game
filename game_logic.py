import pygame
from pygame.locals import *
import json
import time
import datetime
import os
import menu_logic
import __main__

from OpenGL.GL import *
from OpenGL.GLU import *

config = open("config/config.json")
config = json.load(config)
squares = config["settings"]["game"]["n_tiles"]

def load_current_save(filename): # used to load save to render_logic
    menu_logic.selected_file = filename
    menu_logic.set_menu(5)

def new_game(squares=squares):
    """Generates a new game, and saves its map. New game will then be loaded in the menu
    Squares: size of the map

    """
    print("generating new game")
    date = str(datetime.date.today())
    date.replace(" ", "_")
    st_map = [[0] * squares] * squares
    et_map = [[0] * squares] * squares
    directories = os.listdir(os.getcwd() + "\\save")

    f_map = open("save\\" + str(date) + str(int(time.time())) + ".sav", "w")
    write_data = [str(squares) + "\n", str(st_map) + "\n", str(et_map) + "\n"]
    print("writing data")
    f_map.writelines(write_data)
    print("finished writing data")
    f_map.close()

def change_to_opengl(): # sets the graphics to opengl rather than pygame. MUST RUN BEFORE LOADGAME AT LEAST ONCE.
    menu_logic.set_menu(5)
    res = __main__.resolution
    vsync_conf = config["settings"]["video_conf"]["vsync"] # gets settings for vsync
    if __main__.fullscreen == True:
        __main__.screen = pygame.display.set_mode((res[0], res[1]), DOUBLEBUF | OPENGL | FULLSCREEN, vsync=vsync_conf)
    else:
        __main__.screen = pygame.display.set_mode((res[0], res[1]), DOUBLEBUF | OPENGL, vsync=vsync_conf)
    gluPerspective(45, (res[0] / res[1]), 0.1, 100.0)


def load_game(filename): # Must run change_to_opengl() before this function
    menu_logic.set_menu(5) # sets the menu to in_game
    print("loading " + filename)

    try:
        save = open(os.getcwd() + "\\save\\" + filename, "r").readlines()
    except FileNotFoundError:
        print("Failed to open file")
        return 0
    map_n_squares = save[0]
    st_map = save[1]
    et_map = save[2]
    return [map_n_squares, st_map, et_map]
