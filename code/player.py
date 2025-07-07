#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from code.const import ENTITY_SPEED, WIN_WIDTH, ENTITY_COOLDOWN, ENTITY_RANGE
from code.entity import Entity

class Player(Entity):
    def __init__(self, name: str, position: tuple,):
        super().__init__(name, position)

        # Attack properties
        self.attacking = False
        self.attack_duration = 300
        self.last_attack_time = 0
        self.attack_range = ENTITY_RANGE[name]
        self.attack_cooldown = ENTITY_COOLDOWN[name]

        # Move
        self.speed = ENTITY_SPEED[name]
        self.is_jumping = False
        self.jump_velocity = -8
        self.gravity = 0.5
        self.vertical_speed = 0

        self.last_jump_time = 0
        self.jump_cooldown = 800

        self.score = 0

        self.animation_speed = {
            'idle': 0.1,
            'run': 0.1,
            'jump': 0.1,
            'attack': 0.2,
            'hurt': 0.1,
            'dead': 0.1
        }

        # Load animations
        self.animations = {
            'idle': self.load_frames_from_folder('./asset/player', 'idle_', 4),
            'run': self.load_frames_from_folder('./asset/player', 'run_', 6),
            'jump': self.load_frames_from_folder('./asset/player', 'jump_', 8),
            'attack': self.load_frames_from_folder('./asset/player', 'attack_', 4),
            'hurt': self.load_frames_from_folder('./asset/player', 'hurt_', 4),
            'dead': self.load_frames_from_folder('./asset/player', 'hurt_', 4)
        }
        self.image = self.animations['idle'][0]

    def load_frames_from_folder(self, folder_path, prefix, total):
        frames = []
        return [
            pygame.image.load(f"{folder_path}/{prefix}{i}.png").convert_alpha()
            for i in range(1, total + 1)
        ]

    def update_animation(self):
        valid_states = ['idle', 'run', 'jump', 'attack', 'hurt', 'dead']
        if self.state not in valid_states:
            self.state = 'idle'

        speed = self.animation_speed.get(self.state, 0.1)
        self.frame_index += speed

        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0
            if self.state == 'attack':
                self.attacking = False
                self.state = 'idle'
            elif self.state == 'hurt':
                self.state = 'idle'
            elif self.state == 'dead':
                self.dead = True
                return

        frame = self.animations[self.state][int(self.frame_index)]
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    def attack(self):
        pressed_key = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if pressed_key[pygame.K_LCTRL] and not self.attacking and now - self.last_attack_time >= self.attack_cooldown:
            self.attacking = True
            self.attack_timer = now
            self.last_attack_time = now
            self.frame_index = 0
            self.state = 'attack'
            print("CTRL pressionado")

        if self.attacking and now - self.last_attack_time >= self.attack_duration:
            self.attacking = False
            self.state = 'idle'

    def move(self, collidable_rects):
        self.attack()
        now = pygame.time.get_ticks()

        if self.state == 'hurt':
            if now - self.hurt_time < self.hurt_duration:
                self.update_animation()
                return
            else:
                self.state = 'idle'

        pressed_key = pygame.key.get_pressed()
        dx = 0
        moving = False

        if pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_a]:
            dx -= ENTITY_SPEED['player']
            self.facing_left = True
            moving = True
        if pressed_key[pygame.K_RIGHT] or pressed_key[pygame.K_d]:
            dx += ENTITY_SPEED['player']
            self.facing_left = False
            moving = True

        if not self.attacking and not self.is_jumping:
            self.state = 'run' if moving else 'idle'

        if not self.is_jumping and pressed_key[pygame.K_SPACE] and now - self.last_jump_time >= self.jump_cooldown:
            self.is_jumping = True
            self.vertical_speed = self.jump_velocity
            self.last_jump_time = now
            if not self.attacking:
                self.state = 'jump'

        # Horizontal collisions
        future_rect = self.rect.copy()
        future_rect.x += dx

        if future_rect.left < 0:
            dx = 0 - self.rect.left
            self.rect.left = 0
        elif future_rect.right > 1776:
            dx = WIN_WIDTH - self.rect.right
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

        self.update_animation()

