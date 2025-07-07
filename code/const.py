import pygame

# C
C_TITLE = (10, 18, 3)
C_OPTION = (255, 255, 255)
C_SELECTED = (0, 39, 40)
C_TEST = (255, 255, 255)

# E
EVENT_ENEMY = pygame.USEREVENT + 1

ENTITY_COOLDOWN = {
    'player': 500,
    'enemy1': 45,
    'enemy2': 60
}

ENTITY_DAMAGE = {
    'player': 20,
    'enemy1': 10,
    'enemy2': 12
}

ENTITY_SCORE = {
    'enemy1': 100,
    'enemy2': 125,
    'player': 0
}

ENTITY_HEALTH = {
    'player': 100,
    'enemy1': 2000,
    'enemy2': 60
}

ENTITY_RANGE = {
    'player': 80,
    'enemy1': 30,
    'enemy2': 40
}

ENTITY_SPEED = {
    'background0': 0,
    'background1': 1,
    'background2': 0,
    'player': 2,
    'enemy1': 1
}


# M
MENU_OPTION = ('NEW GAME',
               'SCORE',
               'EXIT')

# S
SPAWN_TIME = 4000

# w
WIN_WIDTH = 600
WIN_HEIGHT = 400