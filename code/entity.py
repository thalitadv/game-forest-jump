#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import pygame.image


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = None
        self.rect = pygame.Rect(position[0], position[1], 32, 32)
        self.speed = 0

    @abstractmethod
    def move(self, ):
        pass
