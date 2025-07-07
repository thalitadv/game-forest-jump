import pygame

class Camera:
    def __init__(self, width, height, width_total, height_total):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.width_total = width_total
        self.height_total = height_total

        self.deadzone_top = height // 3
        self.deadzone_bottom = 2 * height // 3

    def update(self, target):
        self.offset.x = target.rect.centerx - self.width // 2
        self.offset.x = max(0, min(self.offset.x, self.width_total - self.width))

        target_y = target.rect.centery

        if target_y <self.offset.y + self.deadzone_top:
            self.offset.y = target_y - self.deadzone_top
        elif target_y > self.offset.y + self.deadzone_bottom:
            self.offset.y = target_y - self.deadzone_bottom

        self.offset.y = max(0, min(self.offset.y, self.height_total - self.height))

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)