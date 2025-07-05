#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from code.const import ENTITY_SPEED, WIN_WIDTH
from code.entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple,):
        super().__init__(name, position)

        # Load animation spritesheets
        self.animations = {
            'idle': self.load_frames_from_folder('./asset/player', 'idle_', 4),
            'run': self.load_frames_from_folder('./asset/player', 'run_', 6),
            'jump': self.load_frames_from_folder('./asset/player', 'jump_', 8)
        }

        # Initial state
        self.state = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.facing_left = False
        self.image = self.animations[self.state][int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=position)

        # Jump
        self.is_jumping = False
        self.jump_velocity = -8
        self.gravity = 0.5
        self.vertical_speed = 0

    def load_frames_from_folder(self, folder_path, prefix, total):
        frames = []
        for i in range(1, total + 1):
            path = f"{folder_path}/{prefix}{i}.png"
            image = pygame.image.load(path).convert_alpha()
            frames.append(image)
        return frames

    def update_animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0

        frame = self.animations[self.state][int(self.frame_index)]

        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame


    def move(self, collidable_rects):
        pressed_key = pygame.key.get_pressed()
        dx, dy = 0, 0
        moving = False

        if pressed_key[pygame.K_LEFT]:
            dx -= ENTITY_SPEED['player']
            self.state = 'run'
            self.facing_left = True
            moving = True
        if pressed_key[pygame.K_RIGHT]:
            dx += ENTITY_SPEED['player']
            self.state = 'run'
            self.facing_left = False
            moving = True

        if not moving and not self.is_jumping:
            self.state = 'idle'

        if not self.is_jumping and pressed_key[pygame.K_SPACE]:
            self.is_jumping = True
            self.vertical_speed = self.jump_velocity
            self.state = 'jump'

        # Gravity
        self.vertical_speed += self.gravity
        dy += self.vertical_speed

        future_rect = self.rect.copy()
        future_rect.x += dx

        if future_rect.left < 0:
            dx = 0 - self.rect.left  # Ajusta dx para não passar do limite
            self.rect.left = 0

            # Limite direito
        elif future_rect.right > WIN_WIDTH:
            dx = WIN_WIDTH - self.rect.right  # Ajusta dx para não passar do limite
            self.rect.right = WIN_WIDTH

        for rect in collidable_rects:
            if future_rect.colliderect(rect):
                if dx > 0:
                    self.rect.right = rect.left
                elif dx < 0:
                    self.rect.left = rect.right
                dx = 0
                break

        self.rect.x += dx

        future_rect = self.rect.copy()
        future_rect.y += dy

        for rect in collidable_rects:
            if future_rect.colliderect(rect):
                if dy > 0:
                    self.rect.bottom = rect.top
                    self.vertical_speed = 0
                    self.is_jumping = False
                elif dy < 0:
                    self.rect.top = rect.bottom
                    self.vertical_speed = 0
                dy = 0
                break

        self.rect.y += dy

        self.update_animation()