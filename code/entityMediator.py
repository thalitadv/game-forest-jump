import pygame

from code.const import WIN_HEIGHT
from code.entity import Entity
from code.enemy import Enemy
from code.player import Player


class EntityMediator:
    @staticmethod
    def __rects_intersect(r1: pygame.Rect, r2: pygame.Rect) -> bool:
        # Manual rectangle collision check
        return (
                r1.right >= r2.left and
                r1.left <= r2.right and
                r1.bottom >= r2.top and
                r1.top <= r2.bottom
        )

    @staticmethod
    def __verify_collision_window(ent: Entity):
        # Check if player fell below screen
        if isinstance(ent, Player):
            if ent.rect.top > WIN_HEIGHT:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        # Check collision between Player and Enemy and apply damage
        valid_interaction = False

        if isinstance(ent1, Enemy) and isinstance(ent2, Player):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, Enemy):
            valid_interaction = True

        if valid_interaction:
            # Check actual rectangle collision
            if (ent1.rect.right >= ent2.rect.left and
                ent1.rect.left <= ent2.rect.right and
                ent1.rect.bottom >= ent2.rect.top and
                ent1.rect.top <= ent2.rect.bottom):

                if hasattr(ent1, 'attacking') and ent1.attacking:
                    if hasattr(ent2, 'take_damage'):
                        ent2.take_damage(ent1.damage, attacker=ent1)

                if hasattr(ent2, 'attacking') and ent2.attacking:
                    if hasattr(ent1, 'take_damage'):
                        ent1.take_damage(ent2.damage, attacker=ent2)


    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if hasattr(enemy, 'last_attacker') and isinstance(enemy.last_attacker, Player):
            enemy.last_attacker.score += enemy.score

    @staticmethod
    def __verify_collision_terrain(entity: Entity, collidable_rects: list[pygame.Rect]):
        if isinstance(entity, Player):
            # Apply gravity
            entity.vertical_speed += entity.gravity

            future_rect = entity.rect.copy()
            future_rect.y += entity.vertical_speed

            collided = False
            for rect in collidable_rects:
                if future_rect.colliderect(rect):
                    if entity.vertical_speed > 0:  # caindo
                        entity.rect.bottom = rect.top
                        entity.vertical_speed = 0
                        entity.is_jumping = False
                    elif entity.vertical_speed < 0:  # subindo
                        entity.rect.top = rect.bottom
                        entity.vertical_speed = 0

                    collided = True
                    break

            if not collided:
                entity.rect.y += entity.vertical_speed

    @staticmethod
    def verify_collision(entity_list: list[Entity], collidable_rects: list[pygame.Rect]):
        for i in range(len(entity_list)):
            entity = entity_list[i]

            EntityMediator.__verify_collision_window(entity)

            if isinstance(entity, Player):
                EntityMediator.__verify_collision_terrain(entity, collidable_rects)

            for j in range(i + 1, len(entity_list)):
                EntityMediator.__verify_collision_entity(entity, entity_list[j])

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)

    @staticmethod
    def verify_collision_platforms(player, platforms):
        for platform in platforms:
            # Update drop status
            platform.update()

            if platform.rect.colliderect(player.rect):
                if player.vertical_speed > 0 and player.rect.bottom <= platform.rect.top + 10:
                    player.rect.bottom = platform.rect.top
                    player.vertical_speed = 0
                    player.is_jumping = False
                    platform.start_fall()
            else:
                # If the player left the platform without activating the drop
                if not platform.falling:
                    platform.fall_timer = None
