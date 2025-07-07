#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.const import ENTITY_SPEED, ENTITY_RANGE, ENTITY_COOLDOWN, ENTITY_HEALTH, ENTITY_DAMAGE
from code.entity import Entity

class Enemy(Entity):
    def __init__(self, name: str, position: tuple, patrol_range: int = 100):
        super().__init__(name, position)

        self.speed = ENTITY_SPEED[name]
        self.health = ENTITY_HEALTH[name]
        self.range = ENTITY_RANGE[name]
        self.damage = ENTITY_DAMAGE[name]
        self.cooldown = ENTITY_COOLDOWN[name]
        self.hurt_duration = 300

        self.cooldown_timer = 0

        self.facing_left = True
        self.patrol_range = patrol_range
        self.start_x = position[0]

        self.state = 'run'
        self.frame_index = 0
        self.animation_speed = {
            'run': 0.1,
            'attack': 0.15,
            'hurt': 0.1,
        }
        if name == "enemy1":
            self.animations = {
                'run': self.load_frames_from_folder('./asset/enemy1', 'enemy1Run_', 8),
                'attack': self.load_frames_from_folder('./asset/enemy1', 'enemy1Attack_', 5),
                'hurt': self.load_frames_from_folder('./asset/enemy1', 'enemy1Hurt_', 5),
            }
        else:
            self.animations = {
                'run': self.load_frames_from_folder('./asset/enemy2', 'enemy2Run_', 8),
                'attack': self.load_frames_from_folder('./asset/enemy2', 'enemy2Attack_', 8),
                'hurt': self.load_frames_from_folder('./asset/enemy2', 'enemy2Hurt_', 5),
            }


        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=position)

    def load_frames_from_folder(self, folder_path, prefix, total):
            return [
                pygame.image.load(f"{folder_path}/{prefix}{i}.png").convert_alpha()
                for i in range(1, total + 1)
            ]

    def update_animation(self):
        valid_states = ['run', 'attack', 'hurt']
        if self.state not in valid_states:
            self.state = 'run'

        speed = self.animation_speed.get(self.state, 0.1)
        self.frame_index += speed

        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0
            if self.state == 'attack':
                self.state = 'run'
            elif self.state == 'hurt':
                self.state = 'run'

        frame = self.animations[self.state][int(self.frame_index)]
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    def move(self, player=None):
        now = pygame.time.get_ticks()

        # If you are hurt, just animate hurt and stop
        if self.state == 'hurt':
            if now - self.hurt_time < self.hurt_duration:
                self.update_animation()
                return
            else:
                self.state = 'run'  # run again after the hurt

        #If attacking, animate attack
        if self.state == 'attack':
            self.update_animation()
            if self.frame_index >= len(self.animations['attack']):
                self.frame_index = 0
                self.state = 'run'
            return

        # Decreases attack cooldown
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        if self.name == 'enemy2' and player:
            range_visual = 150
            range_ataque = self.range

            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance <= range_visual:
                if distance > range_ataque:
                    direction_x = 1 if dx > 0 else -1
                    direction_y = 1 if dy > 0 else -1
                    self.rect.x += direction_x * self.speed
                    self.rect.y += direction_y * self.speed
                    self.facing_left = dx < 0
                else:
                    if self.cooldown_timer == 0:
                        self.state = 'attack'
                        self.frame_index = 0
                        player.take_damage(self.damage, attacker=self)
                        self.cooldown_timer = self.cooldown
                self.update_animation()
                return

        # Patrol movement
        if self.facing_left:
            self.rect.x -= self.speed
            if self.rect.x <= self.start_x - self.patrol_range:
                self.facing_left = False
        else:
            self.rect.x += self.speed
            if self.rect.x >= self.start_x + self.patrol_range:
                self.facing_left = True


        # Checks if it can attack the player
        if player:
            distance_x = abs(self.rect.centerx - player.rect.centerx)
            distance_y = abs(self.rect.centery - player.rect.centery)

            if distance_x < self.range and distance_y < 40 and self.cooldown_timer == 0:
                self.state = 'attack'
                self.frame_index = 0
                player.take_damage(self.damage, attacker=self)
                self.cooldown_timer = self.cooldown

        # Updates animation according to current state
        self.update_animation()