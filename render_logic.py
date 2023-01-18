import menu_logic
import __main__
import json
import game_logic
import menu_logic
import pygame
from PIL import Image
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

config = open("config/config.json")
config = json.load(config)
squares = config["settings"]["game"]["n_tiles"]

concrete01 = Image.open("assets/Textures/concrete02.jpg")
res = config["settings"]["video_conf"]["resolution"]

def draw_rect(corner1, corner2, colour=(25, 120, 90), tex=None):
    glColor3f(colour[0], colour[1], colour[2])
    glBegin(GL_QUADS)
    glVertex3f(corner1[0], corner1[1],  corner1[2])
    glVertex3f(corner1[0] + corner2[0],  corner1[1], corner1[2])
    glVertex3f(corner1[0] + corner2[0], corner1[1] + corner2[1], corner1[2])
    glVertex3f(corner1[0],  corner1[1] + corner2[1], corner1[2])
    if tex != None:
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D()
    glEnd()

def draw_line(xyz1, xyz2, colour=(255, 255, 255)):
    glColor3f(colour[0], colour[1], colour[2])
    glBegin(GL_LINES)
    glVertex3f(xyz1[0], xyz1[1], xyz1[2])
    glVertex3f(xyz2[0], xyz2[1], xyz2[2])
    glEnd()

def convert_pos_to_opengl(x, y):
    mouse_x = (x / res[0]) * 2 - 1
    mouse_y = -(y / res[1]) * 2 + 1
    return mouse_x, mouse_y

def draw_map(filedata):
    squares = int(filedata[0])
    # BACKGROUND
    draw_rect([squares, -squares, 0], [-squares, squares, 0], colour=[0.62, 0.75, 0.6])

    # GRID
    for y in range(-squares, squares):
        draw_line([-squares, y, 0], [squares, y, 0], colour=(0, 0, 0))
    for x in range(-squares, squares):
        draw_line([x, -squares, 0], [x, squares, 0], colour=(0, 0, 0))


def render_game(filedata):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_pos = glGetFloatv(GL_MODELVIEW_MATRIX)  # gets the x, y, z and where the camera is looking at
    scroll_pos = __main__.scroll_zoom
    previous_scroll_pos = __main__.previous_scroll
    mouse_pos = pygame.mouse.get_pos()
    draw_map(filedata)
    # menu_logict  = menu_logic.button(__main__.screen, "New Game", (-60, 60), (200, 100), (255, 255, 255), (200, 200, 200), (200, 200, 200), action=game_logic.new_game)

    res = __main__.resolution
    movement_scale_box = config["settings"]["game"]["movement_box"] # details the factor bounds of how far the mouse has to go to move
    # This box is calculated by (resolution(x and y) / movement_scale_box)
    x_box, y_box = int(res[0] / movement_scale_box), int(res[1] / movement_scale_box) # returns the start x, y of the box
    # print(x_box, y_box)
    translate_camera = [0, 0]
    keys = pygame.key.get_pressed()
    if mouse_pos[0] < x_box or keys[pygame.K_a] == True:
        translate_camera[0] += 0.5
    if mouse_pos[1] < y_box or keys[pygame.K_s] == True:
        translate_camera[1] += 0.5
    if mouse_pos[0] > res[0] - x_box or keys[pygame.K_d] == True:
        translate_camera[0] -= 0.5
    if mouse_pos[1] > res[1] - y_box or keys[pygame.K_w] == True:
        translate_camera[1] -= 0.5

    zoom = False
    if scroll_pos - previous_scroll_pos < 0: # Allows the camera to zoom in/out
        if camera_pos[3][2] < 59:  # [3][2] is z axis
            zoom = True
    if scroll_pos - previous_scroll_pos > 0:
        if camera_pos[3][2] > 1:
            zoom = True
    if zoom == True:
        glTranslatef(translate_camera[0], translate_camera[1], scroll_pos - previous_scroll_pos)
    else:
        glTranslatef(translate_camera[0], translate_camera[1], 0)

    # -camera[3][0] * 1.901 makes the rect travel at the same speed as the camera, idk why its this specific number but it works so whatever
    # draw_rect([-camera_pos[3][0] * 1.901 + -(translate_camera[0]) - 2, -camera_pos[3][1] + -translate_camera[1] + -1.62, camera_pos[3][2] - 1.6], [0.5, 0.5], colour=(0, 0, 255))
    # -1.62 is an offset that can be removed if needed, same with 1.6, and -2
    print(mouse_pos)
    print([-camera_pos[3][0] * 1.901 + -(translate_camera[0]) - 2, -camera_pos[3][1] + -translate_camera[1] + -1.62])
    positional_data = [mouse_pos, camera_pos, translate_camera]
    draw_button([-camera_pos[3][0] * 1.901 + -(translate_camera[0]) - 2, -camera_pos[3][1] + -translate_camera[1] + -1.62, camera_pos[3][2] - 1.6], [0.5, 0.5], colour1=(0.4, 0.4, 0.4), colour2=[0.7,0.7,0.7], positional_data=positional_data)
def matrix_sub(matrixa, matrixb): # minuses one matrix from another. makes coordinate offset easier
    matrixa[0], matrixa[1], matrixa[2] = matrixa[0] - matrixb[0], matrixa[1] - matrixb[1], matrixa[2] - matrixb[2]
    return matrixa

def draw_button(xyz, wh, colour1, colour2, positional_data):
    mp = positional_data[0]
    camera_pos = positional_data[1][3]
    translate_camera = positional_data[2]
    # if int(mp[0] / -(-camera_pos[3][0] * 1.901 + -(translate_camera[0]) - 2)):
    draw_rect(matrix_sub(xyz, [0.05, -0.05, 0]), [wh[0] + 0.01, wh[1] + 0.01, xyz[2]], colour2)
    draw_rect(xyz, [wh[0], wh[1], xyz[2]], colour1)