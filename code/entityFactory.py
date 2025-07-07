#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from code.Item import Item
from code.background import Background
from code.const import WIN_WIDTH, WIN_HEIGHT
from code.enemy import Enemy
from code.player import Player
from code.platform import Platform
from code.win import Win

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
                patrol_range = kwargs.get('patrol_range', 100)
                return Enemy('enemy2', position, patrol_range)
            case 'platform':
                return Platform(position)
            case 'item':
                return Item('item', position)
            case 'win':
                return Win('win', position)
