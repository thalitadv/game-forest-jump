#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code import player
from code.const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.level import Level
from code.menu import Menu
from code.score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        player_score = [0]
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                player.score =  [0] # [Player]
                level = Level(self.window, 'Level1',  menu_return, player_score)
                level_return = level.run(player_score)
                if level_return:
                    level = Level(self.window, 'Level2', menu_return, player_score)
                    level_return = level.run(player_score)
                    if level_return:
                        score.save(player_score)
            elif menu_return == MENU_OPTION[1]:
                score.show()
            elif menu_return == MENU_OPTION[4]:
                pygame.quit()  # Close window
                quit()  # End pygame
            else:
                pass

