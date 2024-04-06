#all imports

import pygame
from settings import *
from tile import *
from world_objects import *
from player import Player
from healthbar import *
from pygame import mixer

mixer.init()    #intiialize mixer


class World(pygame.sprite.Sprite):
    def __init__(self, level_data, player_num):
        super().__init__()
        # level data will be a dictionary containing the links to the csv
        # that has the various objects in the world
        self.saw_fire_bullet_timer = 0
        self.bomb_timer = 0
        self.bullets = pygame.sprite.Group()
        self.p_num = player_num
        
        # all the sprites
        #bombs
        bombs_sprites = import_csv_layout(level_data['bombs'])
        self.bomb_sprites = self.create_tile_group(bombs_sprites, 'bombs')

        #cannons
        cannons_sprites = import_csv_layout(level_data['cannons'])
        self.cannons_sprites = self.create_tile_group(
            cannons_sprites, 'cannons')

        #coins
        coins_sprites = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_sprites, 'coins')

        #decor
        decor_sprites = import_csv_layout(level_data['decor'])
        self.decor_sprites = self.create_tile_group(decor_sprites, 'decor')

        #exits
        exit_sprites = import_csv_layout(level_data['exit'])
        self.exit_sprites = self.create_tile_group(exit_sprites, 'exit')

        #hearts
        hearts_sprites = import_csv_layout(level_data['hearts'])
        self.hearts_sprites = self.create_tile_group(hearts_sprites, 'hearts')

        #platforms
        platforms = import_csv_layout(level_data['platforms'])
        self.platform_sprites = self.create_tile_group(platforms, 'platforms')

        #saws
        saw_sprites = import_csv_layout(level_data['saw'])
        self.saw_sprites = self.create_tile_group(saw_sprites, 'saw')

        #water
        water_sprites = import_csv_layout(level_data['water'])
        self.water_sprites = self.create_tile_group(water_sprites, 'water')

        #fire
        fire_sprites = import_csv_layout(level_data['fire'])
        self.fire_sprites = self.create_tile_group(fire_sprites, 'fire')

        # start position and player
        start_pos = import_csv_layout(level_data['start'])
        self.player = self.create_tile_group(start_pos, 'start')
        self.p = pygame.sprite.GroupSingle()

        for p in self.player:
            self.p.add(p)

    #this iterates throught the csv file and places a tile image in the respective positions
    #it then returns the group of tiles that were requested e.g 'platforms' or 'bombs'
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':   #if not empty space, add an object at that position
                    x = col_index * 32
                    y = row_index * 32

                    if type == 'platforms':
                        terrain_list = import_cut_graphics(
                            'graphics/tiles/Assets_City.png')
                        tile_surface = terrain_list[int(value)]
                        sprite_group.add(
                            WorldTile(x, y, SCALE, SCALE, tile_surface))

                    if type == 'bombs':
                        sprite_group.add(Bomb(x, y-32))

                    if type == 'cannons':
                        sprite_group.add(Cannon(x, y-32))

                    if type == 'coins':
                        sprite_group.add(Coin(x, y-32))

                    if type == 'water':
                        sprite_group.add(Water(x, y))

                    if type == 'hearts':
                        sprite_group.add(Heart(x, y-32))

                    if type == 'decor':
                        terrain_list = import_cut_graphics(
                            'graphics/tiles/Assets_City.png')
                        tile_surface = terrain_list[int(value)]
                        sprite_group.add(
                            Decor(x, y, SCALE, SCALE, tile_surface))

                    if type == 'exit':
                        sprite_group.add(Exit(x, y-32))

                    if type == "fire":
                        sprite_group.add(Fire(x, y))

                    if type == "saw":
                        sprite_group.add(Saw(x, y-32))

                    if type == "start":
                        sprite_group.add(Player(x, y, self.p_num))

        return sprite_group

    #all game logic run here
    def game_logic(self, player):

        #coin collections
        for sprite in self.coins_sprites:
            if sprite.rect.colliderect(player.rect):
                player.score += 10
                sprite.kill()
                pick_up.play()

        #heart collection
        for sprite in self.hearts_sprites:
            if sprite.rect.colliderect(player.rect):
                player.health += 25
                if player.health >= 100:
                    player.health = 100
                sprite.kill()
                pick_up_2.play()

        #player interaction with bombs
        for sprite in self.bomb_sprites:
            if sprite.rect.colliderect(player.rect):
                if sprite.exploded == False:
                    player.health -= 30
                sprite.animation_list = sprite.load_images(
                    'graphics/tiles/hazards/bomb/explosion')
                sprite.exploded = True
                explosion.play()

        #player interaction with water
        for sprite in self.water_sprites:
            if sprite.rect.colliderect(player.rect):
                player.health = 0

        #player interaction with saws
        for sprite in self.saw_sprites:
            if sprite.rect.colliderect(player.rect):
                self.saw_fire_bullet_timer += 1
                if self.saw_fire_bullet_timer >= 50:
                    player.health -= 10
                    self.saw_fire_bullet_timer = 0
                    hit.play()

        #player interaction with fire
        for sprite in self.fire_sprites:
            if sprite.rect.colliderect(player.rect):
                self.saw_fire_bullet_timer += 1
                if self.saw_fire_bullet_timer >= 50:
                    player.health -= 10
                    self.saw_fire_bullet_timer = 0
                    hit.play()

        #player interaction with exits
        for sprite in self.exit_sprites:
            if sprite.rect.colliderect(player.rect):
                player.next_level = True
                next_lvl.play()

        #player interaction with cannons
        for sprite in self.cannons_sprites:
            if sprite.attack_rect.colliderect(player.rect):
                self.saw_fire_bullet_timer += 1
                if self.saw_fire_bullet_timer >= 50:
                    b = Bullet(sprite.rect.x-20, sprite.rect.y+19)
                    self.bullets.add(b)
                    self.saw_fire_bullet_timer = 0
                    shoot.play()

        #player and world interaction with bullets
        for b in self.bullets:
            if b.rect.colliderect(player.rect):
                b.kill()
                player.health -= 10
                hit.play()
            if b.rect.x <= 0:
                b.kill()

        for p in self.platform_sprites:
            for b in self.bullets:
                if b.rect.colliderect(p.rect):
                    b.kill()

    #runs the entire level
    def run(self, surface, font):
        #draw an update all sprites
        self.saw_sprites.draw(surface)
        self.saw_sprites.update()

        for b in self.bullets:
            b.draw(surface)
            b.update()

        self.platform_sprites.draw(surface)
        self.platform_sprites.update()

        self.bomb_sprites.draw(surface)
        self.bomb_sprites.update()

        self.cannons_sprites.draw(surface)

        self.coins_sprites.draw(surface)
        self.coins_sprites.update()

        self.hearts_sprites.draw(surface)
        self.hearts_sprites.update()

        self.water_sprites.draw(surface)
        self.water_sprites.update()

        self.exit_sprites.draw(surface)
        self.exit_sprites.update()

        self.fire_sprites.draw(surface)
        self.fire_sprites.update()

        self.decor_sprites.draw(surface)
        self.decor_sprites.update()

        #load and update player and UI and run game logic
        self.player.draw(surface)
        for p in self.player:
            self.game_logic(p)
            HealthBar(30, 30, p.health, 100).draw(p.health, surface)
            surface.blit(pygame.transform.scale2x(coin_img), (22, 47))
            draw_text(60, 51, 'gold', str(p.score), surface, font)
            if p.alive is False:
                p.kill()
            self.cannons_sprites.update(p)

        self.player.update(self.platform_sprites)
        