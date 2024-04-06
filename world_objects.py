from tile import *
import pygame

#inherits animated tile but the images used for the tile are changed from the default
class Bomb(AnimatedTile):
    def __init__(self, x, y):
        super().__init__(x, y, path='graphics/tiles/hazards/bomb/idle')
        self.exploded = False

    def update(self):
        if self.exploded:
            self.animate()
            if self.animation_index >= 4:
                self.kill()

#inherits animated tile but the images used for the tile are changed from the default
class Cannon(AnimatedTile):
    def __init__(self, x, y):
        super().__init__(x, y, path='graphics/tiles/hazards/cannon/shoot')
        self.attack_rect = pygame.Rect(self.rect.left-256, y+32, 256, 32)

    #only animate if the target is within range
    def update(self, target):
        if self.attack_rect.colliderect(target.rect):
            self.animate()
        else:
            self.image = self.animation_list[0]


#inherits animated tile but the images used for the tile are changed from the default
class Coin(AnimatedTile):
    def __init__(self, x, y):
        super().__init__(x, y, path='graphics/tiles/hazards/coin')

#no animation needed here
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale2x(
            pygame.image.load('graphics/tiles/hazards/sign.png'))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


#inherits animated tile but the images used for the tile are changed from the default
class Heart(AnimatedTile):
    def __init__(self, x, y):
        super().__init__(x, y, path='graphics/tiles/hazards/heart')


#inherits animated tile but the images used for the tile are changed from the default
class Saw(AnimatedTile):
    def __init__(self, x, y):
        super().__init__(x, y, path='graphics/tiles/hazards/saw')

#no animation needed here
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale2x(
            pygame.image.load('graphics/tiles/hazards/water.png'))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


#inherits animated tile but the images used for the tile are changed from the default
class Fire(AnimatedTile):
    def __init__(self, x, y):
        super().__init__(x, y, path='graphics/tiles/hazards/fire')

#no animation needed here
class Decor(WorldTile):
    def __init__(self, x, y, width, height, surface):
        super().__init__(x, y, width, height, surface)

#no animation needed here
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale2x(
            pygame.image.load('graphics/tiles/hazards/bullet.png'))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = -3 #speed of the bullet

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        #update the bullet's position
        self.rect.x += self.speed
