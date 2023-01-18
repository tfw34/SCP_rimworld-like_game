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
res = config["settings"]["video_conf"]["resolution"].split("x")
res[0], res[1] = int(res[0]), int(res[1])

def draw_rect(corner1, corner2, colour=(0.2, 0.75, 0.5)):
    glColor3f(colour[0], colour[1], colour[2])
    glBegin(GL_QUADS)
    glVertex3f(corner1[0], corner1[1],  corner1[2])
    glVertex3f(corner1[0] + corner2[0],  corner1[1], corner1[2])
    glVertex3f(corner1[0] + corner2[0], corner1[1] + corner2[1], corner1[2])
    glVertex3f(corner1[0],  corner1[1] + corner2[1], corner1[2])
    glEnd()

def draw_line(xyz1, xyz2, colour=(255, 255, 255)):
    glColor3f(colour[0], colour[1], colour[2])
    glBegin(GL_LINES)
    glVertex3f(xyz1[0], xyz1[1], xyz1[2])
    glVertex3f(xyz2[0], xyz2[1], xyz2[2])
    glEnd()

def convert_pos_to_opengl(x, y):
    return (x / res[0]) * 2 - 1, -(y / res[1]) * 2 + 1

def convert_pos_to_pygame(x, y):
    return (x * res[0]) / 2 + 1, -(y * res[1]) / 2 - 1

def draw_map(filedata):
    # draw_rect([-0.5, -0.5, -1], [1, 1])
    squares = int(filedata[0])
    # BACKGROUND
    # draw_rect([squares, -squares, -1], [-squares, squares, -1], colour=[0.62, 0.75, 0.6])
    draw_rect([-0.5, -0.5, -1], [0.5, 0.5])
    # for y in range(-squares, squares):
    #     draw_line([-squares, y, -1], [squares, y, 0], colour=(1, 1, 1))
    # for x in range(-squares, squares):
    #     draw_line([x, -squares, -1], [x, squares, 0], colour=(1, 1, 1))

def render_game(filedata):
    camera_pos = glGetFloatv(GL_MODELVIEW_MATRIX)  # gets the x, y, z and where the camera is looking at
    scroll_pos = __main__.scroll_zoom
    previous_scroll_pos = __main__.previous_scroll
    mouse_pos = __main__.mouse_pos
    mouse_x, mouse_y = convert_pos_to_opengl(mouse_pos[0], mouse_pos[1])
    # menu_logict  = menu_logic.button(__main__.screen, "New Game", (-60, 60), (200, 100), (255, 255, 255), (200, 200, 200), (200, 200, 200), action=game_logic.new_game)

    res = __main__.resolution
    movement_scale_box = config["settings"]["game"]["movement_box"] # details the factor bounds of how far the mouse has to go to move
    # This box is calculated by (resolution(x and y) / movement_scale_box)
    x_box, y_box = int(res[0] / movement_scale_box), int(res[1] / movement_scale_box) # returns the start x, y of the box
    # print(x_box, y_box)

    camera_x, camera_y, camera_z = __main__.camera_x, __main__.camera_y, __main__.camera_z # Gets the camera pos from __main__
    # gluLookAt(camera_x, camera_y, camera_z, camera_x, camera_y, camera_z, 0, 1, 0)
    # camera_x, camera_y, camera_z = camera_pos[3][0], camera_pos[3][1], camera_pos[3][2]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] == True: # moves the camera
        camera_x += 0.1
    if keys[pygame.K_s] == True:
        camera_y -= 0.1
    if keys[pygame.K_d] == True:
        camera_x -= 0.1
    if keys[pygame.K_w] == True:
        camera_y += 0.1

    if scroll_pos - previous_scroll_pos < 0: # Allows the camera to zoom in/out
        if camera_pos[3][2] < 59:  # [3][2] is z axis
            # glTranslatef(0, 0, scroll_pos - previous_scroll_pos)
            camera_z -= 0.1
    if scroll_pos - previous_scroll_pos > 0:
        if camera_pos[3][2] > 1:
            # glTranslatef(0, 0, (scroll_pos - previous_scroll_pos) * 2)
            camera_z += 0.1
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # print(camera_x, camera_y, camera_z, "|", mouse_x, mouse_y)
    gluLookAt(camera_x, camera_y, camera_z, camera_x, camera_y, 0, 0, 1, 0)
    draw_map(filedata)
    positional_data = [[mouse_x, mouse_y], [camera_x, camera_y, camera_z]]

    draw_button([camera_x + 0.74, camera_y - 1.05, camera_z + 1], [0.3, 0.3], colour1=(1, 1, 1), colour2=(0.7, 0.7, 0.7), positional_data=positional_data)

    __main__.camera_x, __main__.camera_y, __main__.camera_z = camera_x, camera_y, camera_z # updates the __main__ pos data
def matrix_sub(matrixa, matrixb): # minuses one matrix from another. makes coordinate offset easier
    matrixa[0], matrixa[1], matrixa[2] = matrixa[0] - matrixb[0], matrixa[1] - matrixb[1], matrixa[2] - matrixb[2]
    return matrixa

def draw_button(xyz, wh, colour1, colour2, positional_data, click_sound="assets/Audio/UI/menu_click_01.mp3"):
    mouse = convert_pos_to_opengl(__main__.mouse_pos[0], __main__.mouse_pos[1])
    click_time = __main__.click_counter # counts how long a click has been held
    mp = positional_data[0]
    camera_pos = positional_data[1]
    # if int(mp[0] / -(-camera_pos[3][0] * 1.901 + -(translate_camera[0]) - 2)):
    if xyz[0] + wh[0] - 0.04 > -mouse[0] > xyz[0] - 0.05 and xyz[1] + wh[1] + 0.01 > mouse[1] > xyz[1]:
        if click_time > 0 and click_time < 2: # Used instead of pygame.get_mouse() as it counts how long the mouse has been clicked(this stops the button being "pressed" more than once)
            print("CLICK!")
            pygame.mixer.music.load(click_sound)
            pygame.mixer.music.play()
        draw_rect(matrix_sub(xyz, [0.05, -0.05, 0]), [wh[0] + 0.01, wh[1] + 0.01, xyz[2]], colour1)
        draw_rect(xyz, [wh[0], wh[1], xyz[2]], colour2)
    else:
        draw_rect(matrix_sub(xyz, [0.05, -0.05, 0]), [wh[0] + 0.01, wh[1] + 0.01, xyz[2]], colour2)
        draw_rect(xyz, [wh[0], wh[1], xyz[2]], colour1)