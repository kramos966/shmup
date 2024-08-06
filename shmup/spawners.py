import pygame
import pygame.freetype
import math as m

from .entities import EntityGroup
from .color import CKEY

class BaseSpawner(pygame.sprite.Group):
    def __init__(self, sprite_size: tuple | list):
        pygame.sprite.Group.__init__(self)
        self.base_image = pygame.Surface(sprite_size).convert()
        self.base_image.set_colorkey(CKEY)
        self.base_image.fill(CKEY)

    def _draw_sprite(self):
        raise NotImplementedError("This method must be overriden.")

    def spawn(self, *args, **kwargs):
        raise NotImplementedError("This method must be overriden.")
