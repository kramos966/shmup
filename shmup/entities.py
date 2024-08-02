import pygame
import pygame.freetype
import random
import math as m

class EntityGroup(pygame.sprite.Group):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Group.__init__(self, *args, **kwargs)

class Entity(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.position = pygame.math.Vector2(0, 0) # Should be Vector2
        self._time = 0
        self.velocity = pygame.math.Vector2(0, 0)

    def clamp(self, clamp_reg):
        _, _, w, h = self.rect
        self.position.x = max(-w, min(self.position.x, clamp_reg.w))
        self.position.y = max(-h, min(self.position.y, clamp_reg.h))
        self.rect.center = self.position.x, self.position.y

    def acceleration(self):
        return pygame.math.Vector2(0, 0)

    def update(self, dt: int):
        """Basic update function.
        - dt: time interval
        - f: callable as a function of time and position, f(t, position)
        """
        self._time += dt
        # Simple Euler integration method. Maybe RK4 is still fast enough...
        dv = self.acceleration() * dt
        self.velocity += dv
        self.position += self.velocity * dt
        
