import pygame
import pygame.freetype
import random
import math as m

from .entities import Entity, EntityGroup
from .bullets import Bullet
from .color import CKEY

class Player(Entity):
    def __init__(self, bullets):
        Entity.__init__(self)
        self.image = pygame.Surface((16, 32)).convert()
        self.image.set_colorkey(CKEY)
        self.image.fill(0xffffff)
        self.rect = self.image.get_rect()
        self.rect.scale_by_ip(0.5)
        print(self.rect.width)
        self.speed = 1e-1
        self.position = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(0, 0)
        self.bullets = bullets
        self.bullet_cooldown = 200 # ms
        self.bullet_shoot_time = self.bullet_cooldown + 1
        self.alive = False
        
    def update(self, dt: int, keys: dict, clamp_reg: pygame.rect, enemies: EntityGroup,
               bullets: EntityGroup):
        self.bullet_shoot_time += dt
        self.direction.x = self.direction.y = 0
        if keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_DOWN]:
            self.direction.y = 1
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        if keys[pygame.K_x]:
            if self.bullet_shoot_time > self.bullet_cooldown:
                self.shoot()
                self.bullet_shoot_time = 0
        self.velocity = self.speed * self.direction

        super().update(dt)
        # Clamp position inside area
        self.clamp(clamp_reg)

        # Kill player if it collides with enemies
        collision_list = pygame.sprite.spritecollide(self, enemies, False)
        if (any(collision_list)):
            self.alive = False
        bullet_collision = pygame.sprite.spritecollide(self, bullets, True)
        if (any(bullet_collision)):
            self.alive = False
        
    def move_to(self, x: float, y: float):
        self.position.x = x
        self.position.y = y
        # self.rect.x = x
        # self.rect.y = y
        self.rect.center = (x, y)

    def shoot(self) -> None:
        position = pygame.math.Vector2(self.position)
        position.y -= self.rect.h / 2
        bullet = Bullet(0x9F2B68, position)
        self.bullets.add(bullet)
