# imports used
import pygame
from tile import *
from csv import reader
from pygame import mixer

mixer.init()  # initialize mixer for the audio

# constatns
SCALE, FPS = 64, 60
TILE_SIZE = 16
LEVEL_HEIGHT = 20
H, W = LEVEL_HEIGHT * SCALE/2, LEVEL_HEIGHT * SCALE/2

vol = 0.2
music_vol = 0.25

# controlls which level gets loaded
def select_level(lvl_num):
    lvl = {
        'bombs': f'graphics/levels/level{lvl_num}/level{lvl_num}_bombs.csv',
        'cannons': f'graphics/levels/level{lvl_num}/level{lvl_num}_cannons.csv',
        'coins': f'graphics/levels/level{lvl_num}/level{lvl_num}_coins.csv',
        'decor': f'graphics/levels/level{lvl_num}/level{lvl_num}_decor.csv',
        'exit': f'graphics/levels/level{lvl_num}/level{lvl_num}_exit.csv',
        'hearts': f'graphics/levels/level{lvl_num}/level{lvl_num}_hearts.csv',
        'platforms': f'graphics/levels/level{lvl_num}/level{lvl_num}_platforms.csv',
        'saw': f'graphics/levels/level{lvl_num}/level{lvl_num}_saw.csv',
        'start': f'graphics/levels/level{lvl_num}/level{lvl_num}_start.csv',
        'water': f'graphics/levels/level{lvl_num}/level{lvl_num}_water.csv',
        'fire': f'graphics/levels/level{lvl_num}/level{lvl_num}_fire.csv'
    }
    return lvl


# some images loaded
coin_img = pygame.image.load('graphics/tiles/hazards/coin/0.png')
paused_img = pygame.image.load(
    'graphics/menu buttons/Square Buttons/Pause Square Button.png')
up_img = pygame.image.load('graphics/menu buttons/Square Buttons/up_down.png')
down_img = pygame.transform.flip(up_img, True, False)
timer_img = pygame.transform.scale(pygame.image.load(
    'graphics/menu buttons/Square Buttons/timer.png'), (48, 48))

# function to draw text on screen


def draw_text(x, y, col, text, surface, font):
    img = font.render(text, True, col)
    surface.blit(img, (x, y))

# import csv for the level and return the terrain_map of the csv
def import_csv_layout(path):
    terrain_map = []

    with open(path) as level_map:
        level = reader(level_map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))

    return terrain_map

# takes the tileset and cuts the tiles into usable images
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    surface = pygame.transform.scale(
        surface, (int(surface.get_width()*2), int(surface.get_height()*2)))
    x = int(surface.get_size()[0]/32)
    y = int(surface.get_size()[1]/32)
    cut_tiles = []
    for row in range(y):
        for col in range(x):
            xpos = col * 32
            ypos = row * 32
            new_surface = pygame.Surface(
                (32, 32), pygame.SRCALPHA)
            new_surface.fill(pygame.Color(0, 0, 0, 0))
            new_surface.blit(surface, (0, 0), pygame.Rect(
                xpos, ypos, 32, 32))
            cut_tiles.append(new_surface)

    return cut_tiles


# music
pygame.mixer.music.load('audio/music.wav')
pygame.mixer.music.set_volume(music_vol)
pygame.mixer.music.play(-1, 0, 2000)

# audio
explosion = pygame.mixer.Sound('audio/explosion.wav')
explosion.set_volume(vol)
hit = pygame.mixer.Sound('audio/hit.wav')
hit.set_volume(vol)
jump = pygame.mixer.Sound('audio/jump.wav')
jump.set_volume(vol)
nav = pygame.mixer.Sound('audio/menu_nav.wav')
nav.set_volume(vol)
pick_up = pygame.mixer.Sound('audio/pick up.wav')
pick_up.set_volume(vol)
pick_up_2 = pygame.mixer.Sound('audio/pick up 2.wav')
pick_up_2.set_volume(vol)
shoot = pygame.mixer.Sound('audio/shoot.wav')
shoot.set_volume(vol)
next_lvl = pygame.mixer.Sound('audio/win.wav')
next_lvl.set_volume(vol)

# change volume funtions
def change_audio_volume(volume):
    explosion.set_volume(volume)
    hit.set_volume(volume)
    jump.set_volume(volume)
    nav.set_volume(volume)
    pick_up.set_volume(volume)
    pick_up_2.set_volume(volume)
    shoot.set_volume(volume)
    next_lvl.set_volume(volume)


def change_music_volume(volume):
    pygame.mixer.music.set_volume(volume)

# pause game function
# runs a second instance of pygame stopping the first one
def pause(clock, surface, resume_btn, exit_btn, font):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    paused = False  # resume

        surface.fill('black')
        draw_text(W/3, 50, 'white', "PAUSED", surface, font)
        draw_text(W/5, 350, 'white', "Press M to resume...", surface, font)
        surface.blit(paused_img, (W/3, H/5))
        if resume_btn.draw(surface):
            paused = False
        if exit_btn.draw(surface):
            paused = False
            pygame.quit()
            quit()

        clock.tick(60)
        pygame.display.update()
