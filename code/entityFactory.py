#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from code.background import Background
from code.const import WIN_WIDTH, WIN_HEIGHT
from code.enemy import Enemy
from code.player import Player
from code.platform import Platform


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0), **kwargs):
        match entity_name:
            case 'background':
                list_bg = []
                for i in range(3):
                    list_bg.append(Background(f'background{i}', (0, 0)))
                    list_bg.append(Background(f'background{i}', (WIN_WIDTH, 0)))
                return list_bg
            case 'player':
                return Player('player', (10, WIN_HEIGHT - 200))
            case 'enemy1':
                patrol_range = kwargs.get('patrol_range', 100)
                return Enemy('enemy1', position, patrol_range)
            case 'enemy2':
                return Enemy('enemy2', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))
            case 'platform':
                return Platform(position)
