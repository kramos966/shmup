import pygame
import pygame.freetype
import math as m
import random

from .entities import Entity, EntityGroup
from .color import CKEY

class Bullet(Entity):
    def __init__(self, color: hex, position: pygame.math.Vector2 | list, speed=0.2):
        Entity.__init__(self)
        self.image = pygame.Surface((8, 8)).convert()
        self.image.set_colorkey(CKEY)
        self.image.fill(CKEY)
        pygame.draw.circle(self.image, color, (4, 4), 4)
        pygame.draw.circle(self.image, 0xffffff, (4, 4), 2)
        self.rect = self.image.get_rect()
        self.rect.scale_by_ip(0.5)
        self.speed = speed
        self.direction = pygame.math.Vector2(0, -1)
        self.velocity = self.speed * self.direction
        self.position = pygame.math.Vector2(position)
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def set_direction(self, direction: list | tuple):
        self.direction.x = direction[0]
        self.direction.y = direction[1]
        self.velocity = self.speed * self.direction

    def update(self, dt: int | float, clamp_reg: pygame.rect, colliders: EntityGroup):
        super().update(dt)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        if ((self.position.x > clamp_reg.w) |
            (self.position.x < -8) |
            (self.position.y < -8) |
            (self.position.y > clamp_reg.h)):
            self.kill()

class BulletSpawner(pygame.sprite.Group):
    """Bullet spawner, which creates and holds bullets from
    a single source."""
    
    def __init__(self, size, color):
        pygame.sprite.Group.__init__(self)
        self.base_image = pygame.Surface(size).convert()
        self.base_image.set_colorkey(CKEY)
        self.base_image.fill(CKEY)

    def spawn(self):
        """Spawn bullets according to the currently held pattern."""
        pass

    def set_pattern(self, n_bullets: int, spread_angle: float):
        pass
