import pygame
import pygame.freetype
import math as m
import random

from .entities import Entity, EntityGroup
from .spawners import BaseSpawner
from .color import CKEY

class Bullet(Entity):
    def __init__(self, image: pygame.Surface, position: pygame.math.Vector2 | list,
                 speed = 0.2, direction = (0, 1)):
        Entity.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.scale_by_ip(0.5)
        self.speed = speed
        self.direction = pygame.math.Vector2(0, -1)
        self.velocity = self.speed * self.direction
        self.position = pygame.math.Vector2(position)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.set_direction(direction)

    def set_direction(self, direction: list | tuple):
        self.direction.x = direction[0]
        self.direction.y = direction[1]
        self.velocity = self.speed * self.direction

    def update(self, dt: int | float, clamp_reg: pygame.rect, entity: Entity):
        super().update(dt)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        if ((self.position.x > clamp_reg.w) |
            (self.position.x < -8) |
            (self.position.y < -8) |
            (self.position.y > clamp_reg.h)):
            self.kill()

class BulletSpawner(BaseSpawner):
    """Bullet spawner, which creates and holds bullets from
    a single source."""
    
    def __init__(self, size: tuple | list, color: int | tuple | list, n_bullets = 1,
                 spread_angle = 0.0):
        BaseSpawner.__init__(self, size)
        self._draw_sprite(color)
        self.n_bullets = n_bullets
        self.spread_angle = spread_angle #TODO: Write on a paper what you intend to do...
        self.set_pattern(n_bullets, spread_angle)

    def _draw_sprite(self, color):
        pygame.draw.circle(self.base_image, color, (4, 4), 4)
        pygame.draw.circle(self.base_image, 0xffffff, (4, 4), 2)

    def spawn(self, position: pygame.math.Vector2 | list | tuple, speed: float):
        """Spawn bullets according to the currently held pattern at the given position."""
        # FIXME: Only bullets emanating from a single point...
        # Spawn bullets from position
        for direction in self.directions:
            bullet = Bullet(self.base_image, position, speed = speed, direction = direction)
            self.add(bullet)

    def set_pattern(self, n_bullets: int, spread_angle: float):
        if n_bullets > 1:
            delta_alpha = spread_angle / (n_bullets - 1)
        else:
            delta_alpha = 1
        self.directions = []
        for i in range(n_bullets):
            angle = -.5 * spread_angle + i * delta_alpha
            self.directions.append(pygame.math.Vector2(m.sin(angle), m.cos(angle)))
            
                              
