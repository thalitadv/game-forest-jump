import pygame
from code.entity import Entity

class Win(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.image = pygame.image.load('./asset/maps/win.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.dead = False

    def move(self, *args):
        pass