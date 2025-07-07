import random
import pygame

class Platform:
    def __init__(self, position):
        self.image = pygame.image.load('./asset/maps/platform.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 32))
        self.rect = self.image.get_rect(topleft=position)
        self.original_pos = position

        self.fall_timer = None
        self.falling = False
        self.gravity = 0.5
        self.fall_speed = 2

        self.fall_delay = 500
        self.fall_duration = 3000

        self.return_timer = None
        self.tremble_offset = 0

    def start_fall(self):
        if self.fall_timer is None and not self.falling:
            self.fall_timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        if self.fall_timer and not self.falling:
            elapsed = now - self.fall_timer
            if elapsed >= self.fall_delay:
                self.falling = True
                self.fall_timer = None
                self.return_timer = now
            else:
                tremble = random.randint(-2, 2)
                self.tremble_offset = tremble
        else:
            self.tremble_offset = 0

        if self.falling:
            self.rect.y += self.fall_speed

            if self.return_timer and now - self.return_timer > self.fall_duration:
                self.reset()

    def reset(self):
        self.rect.topleft = self.original_pos
        self.fall_timer = None
        self.falling = False
        self.return_timer = None
        self.tremble_offset = 0

    def draw(self, window, camera):
        draw_rect = self.rect.move(self.tremble_offset - camera.offset.x, -camera.offset.y)
        window.blit(self.image, draw_rect)