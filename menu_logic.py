import os

import pygame
import __main__
import tkinter as tk
import game_logic

root = tk.Tk()

mixer = pygame.mixer
mixer.init()
click02 = mixer.music.load('assets/Audio/UI/menu_click_02.mp3')


def set_menu(menu): # sets the var of which menu is present to (menu)
    for x in range(0, len(__main__.in_menu)):
        __main__.in_menu[x] = False
    __main__.in_menu[menu] = True

def load_assets(path):
    images = [] # stores all .jpg, .png, etc
    video = []  # stores all .gif, .mp4, .mov files
    sound = []  # stores .wav and .mp3
    fonts = []  # stores all font files
    data = []   # stores .txt, .json, etc, etc
    path_files = os.listdir(path)
    for x in path_files:
        if x[-4::] == ".txt" or x[-5::] == ".json":
            data.append(path + "\\" + x)
        if x[-4::] == ".mp3" or x[-4::] == ".wav":
            sound.append(path + "\\" + x)
        if x[-4::] == ".mov" or x[-4::] == ".mp4" or x[-4::] == ".gif":
            video.append(path + "\\" + x)
        if x[-4::] == ".jpg" or x[-4::] == ".png":
            images.append(path + "\\" + x)
    return [images, video, sound, fonts, data]

def button(screen, msg, xy, wh, colour1, colour2, text_colour=(0, 0, 0), submsg="", button_num=0, file_path="", clickable=True, action=None, img_path=None, click_sound="assets/Audio/UI/menu_click_01.mp3", touch_sound=""):
    """:param click_sound: path to soundfile that plays when button is clicked
    :param touch_sound: path to soundfile that plays when button is hovered over"""
    mouse = __main__.mouse_pos
    click = __main__.click
    if xy[0] + wh[0] > mouse[0] > xy[0] and xy[1] + wh[1] > mouse[1] > xy[1]:
        pygame.draw.rect(screen, colour1, (xy[0], xy[1], wh[0], wh[1])) # draws the rect when hovered over
        pygame.draw.rect(screen, colour2, (xy[0] + 3, xy[1] + 3, wh[0] - 3, wh[1] - 3))
        if click[0]:
            if click_sound != "": # if path is not specificed to nothing, play the sound
                mixer.music.load(click_sound)
                mixer.music.play()
            if action != None:
                if file_path != "": # if the filepath param is not empty, load it to the function. Primarily used in load_game_sc()
                    print("Loading ", file_path)
                    return action(file_path)
                else:
                    action()
    else:
        pygame.draw.rect(screen, colour2, (xy[0], xy[1], wh[0], wh[1])) # draws rect when not hovered over
        pygame.draw.rect(screen, colour1, (xy[0] + 3, xy[1] + 3, wh[0] - 3, wh[1] - 3))
        # temp = colour1
        # colour1 = colour2
        # colour2 = temp
        # pygame.draw.rect(screen, colour2, (xy[0], xy[1], wh[0], wh[1]))  # draws rect when not hovered over
        # pygame.draw.rect(screen, colour1, (xy[0] + 3, xy[1] + 3, wh[0] - 3, wh[1] - 3))
    font = pygame.font.Font('freesansbold.ttf', 32)
    screen.blit(font.render(msg, True, text_colour), (xy[0] + 10, xy[1] + 10))
    if submsg != "":
        font = pygame.font.Font('freesansbold.ttf', 25)
        screen.blit(font.render(submsg, True, colour2), (xy[0] + 10, xy[1] + 40))

def text_box(screen, xy, wh, text, colour, text_colour, sub_text="", text_colour2=(255, 255, 255)):
    pygame.draw.rect(screen, colour, (xy[0], xy[1], wh[0], wh[1]))  # draws the rect when hovered over
    font = pygame.font.Font('freesansbold.ttf', 32)
    screen.blit(font.render(text, True, text_colour), (xy[0] + 10, xy[1] + 10))
    if sub_text != "":
        font = pygame.font.Font('freesansbold.ttf', 25)
        screen.blit(font.render(sub_text, True, text_colour2), (xy[0] + 10, xy[1] + 40))

def main_menu():
    screen = __main__.screen
    config = __main__.config
    set_menu(0)
    button_data = config["element_data"]["main_menu"]
    new_game_bt  = button(screen, "New Game", button_data["new_game"], (200, 100), (255, 255, 255), (200, 200, 200), (0, 0, 0), action=game_logic.new_game)
    load_game_bt = button(screen, "Load Game", button_data["load_game"], (200, 100), (255, 255, 255), (200, 200, 200), (0, 0, 0), action=load_game_sc)
    settings_bt  = button(screen, "Settings", button_data["settings"], (200, 100), (255, 255, 255), (200, 200, 200), (0, 0, 0), action=settings)
    exit_bt      = button(screen, "Exit", button_data["exit"], (200, 100), (255, 255, 255), (200, 200, 200), (0, 0, 0), action=exit)

def apply_changes(): # Applies changes to settings()
    root.destroy()

# def toggle_fullscreen():


def settings(): # Not finished yet
    set_menu(1)
    current_settings = __main__.config["settings"]

    root.title('Game Settings')
    root.geometry('600x400')
    root.lift()
    fullscreen_bool = __main__.config["settings"]["video_conf"]["fullscreen"]
    fullscreen_text = ""
    if fullscreen_bool == True:
        fullscreen_text = "On"
    else:
        fullscreen_text = "Off"


    # tk.Label(root, str(fullscreen_text)).place(x=150, y=10)
    fullscreen = tk.Button(root, text="fullscreen").place(x=150, y=30)
    tk.Label(root, text="SFX Volume").place(x=30, y=10)
    tk.Label(root, text="Music Volume").place(x=100, y=10)
    sfx, music = tk.DoubleVar(), tk.DoubleVar()
    sfx.set(current_settings["audio"]["sfx_vol"])
    music.set(current_settings["audio"]["music_vol"])
    sfx_volume = tk.Scale(root, from_=0, to=100, resolution=1, variable=sfx)
    music_volume = tk.Scale(root, from_=0, to=100, resolution=1, variable=music)
    music_volume.place(x=100, y=30)
    sfx_volume.place(x=30, y=30)

    tk.Button(root, text="Apply", command=apply_changes).place(x=200, y=350)
    root.mainloop()

def load_game_sc(): # Logic for load_game menu.
    set_menu(3)
    screen = __main__.screen
    back_button = button(screen, "Back", [300, 100], [250, 100], (255, 255, 255), (200, 200, 200), (0, 0, 0), action=main_menu)
    load_saves = os.listdir(os.getcwd() + "\\save")
    chosen_file = ""
    if len(load_saves) == 0:
        # def text_box(screen, xy, wh, text, colour, text_colour, sub_text="", text_colour2=(255, 255, 255)):
        text_box(screen, [750, 100], [300, 100], "No Saves Found", (255, 255, 255), (0, 0, 0))
    for x in range(0, len(load_saves)):
        file_size = str(int(((os.stat(os.getcwd() + "\\save\\" + load_saves[x]).st_size) / 1000) / 1000)) + "mb"
        if x < 7:
            save = button(screen, load_saves[x], [300, 210 + (110 * x)], [500, 100], (255, 255, 255), (200, 200, 200), (0, 0, 0), submsg=file_size, action=game_logic.write_current_save, file_path=load_saves[x])
        if x > 7:
            save = button(screen, load_saves[x], [300 + 600, 210 + (110 * (x - 8))], [500, 100], (255, 255, 255), (200, 200, 200), (0, 0, 0), submsg=file_size, action=game_logic.write_current_save, file_path=load_saves[x])
