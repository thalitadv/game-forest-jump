#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import pygame.image

from code.const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = None
        self.rect = pygame.Rect(position[0], position[1], 32, 32)
        self.speed = 0
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]

        self.animations: dict[str, list[pygame.Surface]] = {}
        self.frame_index = 0
        self.facing_left = False
        self.image: pygame.Surface

        self.dead:bool = False

        self.state = 'idle'
        self.hurt_time = 0
        self.hurt_duration = 300

    @abstractmethod
    def move(self, ):
        pass

    def take_damage(self, amount, attacker=None):
        if self.dead:
            return

        self.health -= amount

        if attacker:
            self.last_attacker = attacker

        from code.enemy import Enemy
        from code.player import Player
        if isinstance(self, Player) and isinstance(attacker, Enemy):
            self.score = max(0, self.score - 10)


        if self.health <= 0:
            self.dead = True
        else:
            self.state = 'hurt'
            self.hurt_time = pygame.time.get_ticks()

        self.frame_index = 0

    def die(self):
        self.dead = True

