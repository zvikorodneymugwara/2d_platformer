# the imports used

from tile import Tile
from settings import SCALE, W, jump
import pygame
from os import listdir
from pygame import mixer

mixer.init()  # initialize mixer


class Player(Tile):
    def __init__(self, x, y, player_num):
        super().__init__(x, y, SCALE, SCALE)
        self.direction = pygame.math.Vector2()  # x and y direction vectors
        self.speed = 5
        self.in_air = False
        self.jump_height = -19
        self.gravity = 1
        self.player_num = player_num
        self.on_ground = True
        self.flip = False
        self.animations = ['walk', 'idle', 'move']
        self.animation_speed = 0.06
        self.animation_index = 0
        self.animation_list = self.load_images(
            f'graphics/char {self.player_num}/{self.animations[1]}')
        self.image = self.animation_list[self.animation_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.score = 0
        self.alive = True
        self.next_level = False

    def animate(self):
        # increase the animation index at the rate of the animation speed
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animation_list):
            self.animation_index = 0
        self.image = pygame.transform.flip(
            self.animation_list[int(self.animation_index)], self.flip, False)

    # controlls which animation is being shown
    def update_animation(self):
        if self.direction.x != 0:
            self.animation_list = self.load_images(
                f'graphics/char {self.player_num}/{self.animations[0]}')
        else:
            self.animation_list = self.load_images(
                f'graphics/char {self.player_num}/{self.animations[1]}')

    # loads the images in the path for the animation and scales them
    def load_images(self, path):
        img_list = []
        frame_num = len(listdir(path))
        for i in range(frame_num):
            img = pygame.transform.scale(
                pygame.image.load(f'{path}/{i}.png'), (SCALE/1.4, SCALE/1.4))
            img_list.append(img)
        return img_list

    # player controls
    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.in_air is False:
            self.direction.y = self.jump_height
            jump.play()
            if self.direction.y < 0:
                self.in_air = True
                self.on_ground = False

        if keys[pygame.K_a] and self.rect.left > 0:
            self.direction.x = -1
            self.flip = True
        elif keys[pygame.K_d] and self.rect.right < W:
            self.direction.x = 1
            self.flip = False
        else:
            self.direction.x = 0

    # hotizontal collision
    def horizonal_movement(self, tiles):
        self.rect.x += self.speed * self.direction.x
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = tile.rect.right
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left

    # vertical collision
    def vertical_movement(self, tiles):
        self.apply_gravity()
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.direction.y = 0
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

        if self.on_ground:
            self.in_air = False

    def update(self, world):
        # parameter world controlls collision with platforms of the world
        self.controls()
        self.horizonal_movement(world)
        self.vertical_movement(world)
        self.animate()
        self.update_animation()
        if self.health <= 0:
            self.alive = False

#function that loads the player
def load_player(map):
    p = Player(0, 0, 3)
    for i, j in enumerate(map):
        for k, l in enumerate(j):
            if l == 'P':
                p = Player(k*SCALE, i*SCALE, 3)
    return p
