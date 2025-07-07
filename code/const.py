import pygame

# C
C_TITLE = (10, 18, 3)
C_OPTION = (255, 255, 255)
C_SELECTED = (0, 39, 40)
C_SCORE = (255, 255, 255)

# E
EVENT_LEVEL_END = pygame.USEREVENT + 1

ENTITY_COOLDOWN = {
    'player': 1000,
    'enemy1': 450,
    'enemy2': 400
}

ENTITY_DAMAGE = {
    'player': 20,
    'enemy1': 10,
    'enemy2': 12,
    'item': 0,
    'win': 0
}

ENTITY_SCORE = {
    'enemy1': 100,
    'enemy2': 125,
    'player': 0,
    'item': 150,
    'win': 0
}

ENTITY_HEALTH = {
    'player': 100,
    'enemy1': 600,
    'enemy2': 500,
    'item': 1,
    'win': 1
}

ENTITY_RANGE = {
    'player': 80,
    'enemy1': 30,
    'enemy2': 40
}

ENTITY_SPEED = {
    'player': 2,
    'enemy1': 1,
    'enemy2': 1
}

# M
MENU_OPTION = ('NEW GAME',
               'SCORE',
               'EXIT')

# w
WIN_WIDTH = 600
WIN_HEIGHT = 400

# S
SCORE_POS = {
    'Title': (WIN_WIDTH / 2, 50),
    'EnterName': (WIN_WIDTH / 2, 80),
    'Label': (WIN_WIDTH / 2, 90),
    'Name': (WIN_WIDTH / 2, 110),
    0: (WIN_WIDTH / 2, 110),
    1: (WIN_WIDTH / 2, 130),
    2: (WIN_WIDTH / 2, 150),
    3: (WIN_WIDTH / 2, 170),
    4: (WIN_WIDTH / 2, 190),
    5: (WIN_WIDTH / 2, 210),
    6: (WIN_WIDTH / 2, 230),
    7: (WIN_WIDTH / 2, 250),
    8: (WIN_WIDTH / 2, 270),
    9: (WIN_WIDTH / 2, 290),
}