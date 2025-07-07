#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

import pytmx
from pytmx.util_pygame import load_pygame

from code.Item import Item
from code.const import C_OPTION, WIN_HEIGHT
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.camera import Camera
from code.entityMediator import EntityMediator
from code.player import Player


class Level:
    def __init__(self, window, name, menu_return, player_score: list[int]):
        global collision_layer_name
        self.window = window
        self.name = name
        self.platforms = []

        # Load Tiled map
        self.tmx_data = load_pygame(f'asset/maps/{name.lower()}.tmx')
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        # Initializing entities
        self.entity_list: list[Entity] = []
        player = EntityFactory.get_entity('player')
        player.score = player_score[0]
        self.entity_list.append(player)

        if self.name == 'Level1':
            self.entity_list.append(EntityFactory.get_entity('enemy1', (330, 285), patrol_range=80))
            self.entity_list.append(EntityFactory.get_entity('enemy1', (1210, 240), patrol_range=180))
            self.entity_list.append(EntityFactory.get_entity('enemy1', (1680, 205), patrol_range=80))

            self.platforms.append(EntityFactory.get_entity('platform', (485, 250)))
            self.platforms.append(EntityFactory.get_entity('platform', (630, 280)))
            self.platforms.append(EntityFactory.get_entity('platform', (920, 250)))
            self.platforms.append(EntityFactory.get_entity('platform', (1520, 210)))
            self.platforms.append(EntityFactory.get_entity('platform', (1460, 210)))

            self.entity_list.append(EntityFactory.get_entity('item', (510, 200)))
            self.entity_list.append(EntityFactory.get_entity('item', (860, 160)))
            self.entity_list.append(EntityFactory.get_entity('item', (1220, 200)))
            self.entity_list.append(EntityFactory.get_entity('item', (1600, 180)))

            self.entity_list.append(EntityFactory.get_entity('win', (1670, 210)))

        elif self.name == 'Level2':
            self.entity_list.append(EntityFactory.get_entity('enemy1', (550, 255), patrol_range=130))
            self.entity_list.append(EntityFactory.get_entity('enemy1', (1020, 210), patrol_range=150))
            self.entity_list.append(EntityFactory.get_entity('enemy1', (1020, 210), patrol_range=130))
            self.entity_list.append(EntityFactory.get_entity('enemy1', (995, 63), patrol_range=100))
            self.entity_list.append(EntityFactory.get_entity('enemy1', (570, 45), patrol_range=170))
            self.entity_list.append(EntityFactory.get_entity('enemy1', (570, 45), patrol_range=170))

            self.entity_list.append(EntityFactory.get_entity('enemy2', (550, 160), patrol_range=100))
            self.entity_list.append(EntityFactory.get_entity('enemy2', (1020, 170), patrol_range=100))
            self.entity_list.append(EntityFactory.get_entity('enemy2', (580, 15), patrol_range=80))
            self.entity_list.append(EntityFactory.get_entity('enemy2', (550, 15), patrol_range=80))

            self.platforms.append(EntityFactory.get_entity('platform', (220, 290)))
            self.platforms.append(EntityFactory.get_entity('platform', (750, 240)))
            self.platforms.append(EntityFactory.get_entity('platform', (1250, 280)))
            self.platforms.append(EntityFactory.get_entity('platform', (1420, 195)))
            self.platforms.append(EntityFactory.get_entity('platform', (1420, 110)))
            self.platforms.append(EntityFactory.get_entity('platform', (800, 80)))

            self.entity_list.append(EntityFactory.get_entity('item', (150, 230)))
            self.entity_list.append(EntityFactory.get_entity('item', (325, 210)))
            self.entity_list.append(EntityFactory.get_entity('item', (560, 220)))
            self.entity_list.append(EntityFactory.get_entity('item', (1000, 170)))
            self.entity_list.append(EntityFactory.get_entity('item', (1340, 270)))
            self.entity_list.append(EntityFactory.get_entity('item', (1450, 160)))
            self.entity_list.append(EntityFactory.get_entity('item', (1220, 75)))
            self.entity_list.append(EntityFactory.get_entity('item', (820, 30)))
            self.entity_list.append(EntityFactory.get_entity('item', (700, 30)))
            self.entity_list.append(EntityFactory.get_entity('item', (600, 30)))
            self.entity_list.append(EntityFactory.get_entity('item', (500, 30)))
            self.entity_list.append(EntityFactory.get_entity('item', (200, 30)))

            self.entity_list.append(EntityFactory.get_entity('win', (78, 78)))


        map_width = self.tmx_data.width * self.tile_width
        map_height = self.tmx_data.height * self.tile_height
        self.camera = Camera(self.window.get_width(), self.window.get_height(), map_width, map_height)

        # Define the player
        self.player = None
        for ent in self.entity_list:
            if ent.name == 'player':
                self.player = ent
                break

        # Colliders
        if self.name == 'Level1':
            collision_layer_name = 'Camada de Blocos 5'
        elif self.name == 'Level2':
            collision_layer_name = 'Camada de Blocos 4'

        # Colliders
        self.collidable_rects = []
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles') and layer.name == collision_layer_name:
                for x, y, _ in layer.tiles():
                    rect = pygame.Rect(x * self.tile_width, y * self.tile_height,
                                       self.tile_width, self.tile_height)
                    self.collidable_rects.append(rect)

    def make_map(self):
        temp_surface = pygame.Surface((self.tmx_data.width * self.tmx_data.tilewidth,
                                       self.tmx_data.height * self.tmx_data.tileheight))

        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, surf in layer.tiles():
                    temp_surface.blit(surf, (x * self.tile_width, y * self.tile_height))
        return temp_surface

    def run(self, player_score: list[int]):
        pygame.mixer_music.load('./asset/sound/level1.ogg')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.camera.update(self.player)

            # Draw Tiled map layers
            for layer in self.tmx_data.visible_layers:
                if hasattr(layer, 'tiles'):
                    for x, y, surf in layer.tiles():
                        draw_pos = (x * self.tile_width - self.camera.offset.x,
                                    y * self.tile_height - self.camera.offset.y)
                        self.window.blit(surf, draw_pos)

            for platform in self.platforms:
                platform.update()
                platform.draw(self.window, self.camera)

            EntityMediator.verify_collision_platforms(self.player, self.platforms)

            for ent in self.entity_list:
                draw_rect = self.camera.apply(ent.rect)
                if ent.name == 'player':
                    self.level_text(14, f'Health: {ent.health} | Score: {ent.score}', C_OPTION, (50, 25))

                if hasattr(ent, 'image'):
                    self.window.blit(ent.image, draw_rect)
                elif hasattr(ent, 'surf') and ent.surf:
                    self.window.blit(ent.surf, draw_rect)

                if ent == self.player:
                    ent.move(self.collidable_rects)
                else:
                    ent.move(self.player)

                if hasattr(ent, 'update'):
                    ent.update()

            EntityMediator.verify_collision(
                self.entity_list,
                self.collidable_rects,
            )
            # Removes mortal entities
            EntityMediator.verify_health(self.entity_list)

            found_player = any(isinstance(ent, Player) for ent in self.entity_list)
            if not found_player:
                self.show_game_over()
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for ent in self.entity_list:
                if ent.name == 'win' and self.player.rect.colliderect(ent.rect):
                    for ent in self.entity_list:
                        if isinstance(ent, Player):
                            player_score[0] = ent.score
                    return 'Level2'

            # Printed text
            self.level_text(14, f'{self.name} = Timeout: {self.timeout / 1000 :.1f}s', C_OPTION, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps() :.0f}', C_OPTION, (10, WIN_HEIGHT - 40))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_OPTION, (10, WIN_HEIGHT - 25))
            pygame.display.flip()

    def show_game_over(self):
        gameover_image = pygame.image.load('./asset/gameover.png').convert_alpha()
        self.window.blit(gameover_image, (0,0))
        pygame.display.flip()

        pygame.time.delay(1500)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
            text_font: Font = pygame.font.Font("InknutAntiqua-Medium.ttf", text_size)
            text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
            text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
            self.window.blit(source=text_surf, dest=text_rect)



