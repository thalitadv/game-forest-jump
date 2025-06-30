#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.const import WIN_WIDTH, COLOR_TITLE, MENU_OPTION, COLOR_OPTION


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/bgmenu.jpg')
        self.rect = self.surf.get_rect()

    def run(self, ):
        pygame.mixer_music.load('./asset/sound/menu.mp3')
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(80, "Memories", COLOR_TITLE, ((WIN_WIDTH / 2), 70))
            self.menu_text(80, "Of Sun", COLOR_TITLE, ((WIN_WIDTH / 2), 120))

            for i in range(len(MENU_OPTION)):
                self.menu_text(25, MENU_OPTION[i], COLOR_OPTION, ((WIN_WIDTH / 2), 200 + 25 * i))

            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Close window
                    quit() # End pygame

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


