import pygame
from os import listdir

SCALE = 64

# regular tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image.fill('grey')

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# inherits tile and places an image on the surface
class WorldTile(Tile):
    def __init__(self, x, y, width, height, surface):
        super().__init__(x, y, width, height)
        self.image = surface

# inherits pygames' sprite class and is animated like the player class
class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        super().__init__()
        self.path = path
        self.animation_list = self.load_images(self.path)
        self.animation_index = 0
        self.image = self.animation_list[self.animation_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1
        self.flip = False

    def animate(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animation_list):
            self.animation_index = 0
        self.image = pygame.transform.flip(
            self.animation_list[int(self.animation_index)], self.flip, False)

    def load_images(self, path):
        img_list = []
        frame_num = len(listdir(path))
        for i in range(frame_num):
            img = pygame.transform.scale2x(
                pygame.image.load(f'{path}/{i}.png'))
            img_list.append(img)
        return img_list

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.animate()
