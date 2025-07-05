#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

import pytmx
from pytmx.util_pygame import load_pygame

from code.const import COLOR_OPTION, WIN_HEIGHT, EVENT_ENEMY, SPAWN_TIME
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.camera import Camera


class Level:
    def __init__(self, window, name):
        self.timeout = 20000  # 20 seconds
        self.window = window
        self.name = name

        # Load Tiled map
        self.tmx_data = load_pygame(f'asset/maps/level1.tmx')
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        self.entity_list: list[Entity] = []
       # self.entity_list.extend(EntityFactory.get_entity('background'))
        self.entity_list.append(EntityFactory.get_entity('player'))
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

        map_width = self.tmx_data.width * self.tile_width
        map_height = self.tmx_data.height * self.tile_height
        self.camera = Camera(self.window.get_width(), self.window.get_height(),  map_width, map_height)

        self.player = None
        for ent in self.entity_list:
            if ent.name == 'player':
                self.player = ent
                break

        self.collidable_rects = []
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles') and layer.name == 'Camada de Blocos 5':
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

    def run(self):
        pygame.mixer_music.load('./asset/sound/menu.mp3')
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

            for ent in self.entity_list:
                draw_rect = self.camera.apply(ent.rect)

                if hasattr(ent, 'image'):
                    self.window.blit(ent.image, draw_rect)
                elif hasattr(ent, 'surf') and ent.surf:
                    self.window.blit(ent.surf, draw_rect)

                if ent == self.player:
                    ent.move(self.collidable_rects)
                else:
                    ent.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                   # choice = random.choice(('enemy1', 'enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(('enemy1')))

            # Printed text
            self.level_text(14, f'{self.name} = Timeout: {self.timeout / 1000 :.1f}s', COLOR_OPTION, (10,5))
            self.level_text(14, f'fps: {clock.get_fps() :.0f}', COLOR_OPTION, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', COLOR_OPTION, (10, WIN_HEIGHT - 20))
            pygame.display.flip()

            pygame.draw.rect(self.window, (255, 0, 0), self.camera.apply(self.player.rect), 1)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
            text_font: Font = pygame.font.Font("InknutAntiqua-Medium.ttf", text_size)
            text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
            text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
            self.window.blit(source=text_surf, dest=text_rect)



