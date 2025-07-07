import pygame
from code.entity import Entity


class Item(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.frames = self.load_frames_from_folder('./asset/item', 'item_', 4)
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

        self.score_value = 150

    def move(self, *args):
        pass

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def load_frames_from_folder(self, folder_path, prefix, total):
        return [
            pygame.image.load(f"{folder_path}/{prefix}{i}.png").convert_alpha()
            for i in range(1, total + 1)
        ]