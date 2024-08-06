import pygame
import pygame.freetype
import random
import math as m
from typing import Type

from .entities import Entity, EntityGroup
from .bullets import Bullet, BulletSpawner
from .players import Player
from .color import CKEY
from .misc import sign
from .events import TALLY_UP_EVENT

class Enemy(Entity):
    def __init__(self, position: list | pygame.math.Vector2, bullet_spawner: BulletSpawner):
        Entity.__init__(self)
        self.position = pygame.math.Vector2(position)
        self.speed = 0.08
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = self.direction * self.speed
        self.image = pygame.Surface((16, 16)).convert()
        self.image.set_colorkey(CKEY)
        self.rect = self.image.get_rect()
        self.rect.scale_by_ip(0.8)
        self.shoot_timer = 800
        self.shoot_time = 0
        self.image.fill(CKEY)
        pygame.draw.circle(self.image, 0xaa3333, (8, 8), 8)
        # This enemy turns to a direction given where it spawned and a random time
        self.turn_wait = random.randint(1200, 2000)
        self.turn_timer = 0
        self.turn = -sign(self.position.x - 120)
        self.turn_c = 0

        self.bullet_spawner = bullet_spawner

    def acceleration(self):
        accel = pygame.math.Vector2(0, 0)
        if self.turn_timer > self.turn_wait:
            # FIXME: This is absurd! You can turn by just assigning an initial turn speed
            # and swapping each timer count!!!!!!
            accel.x = self.turn * self.velocity.y * 1 - self.velocity.x
            self.turn_timer = 0
            self.turn_c += 1
            self.turn = -self.turn
        return accel

    def update(self, dt: int | float, clamp_reg: pygame.rect, player: Player):
        self.turn_timer += dt
        super().update(dt)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        #self.clamp(clamp_reg)

        if (self.rect.y > clamp_reg.h):
            self.kill()
        p_bullets = player.bullet_spawner
        collided = pygame.sprite.spritecollide(self, p_bullets, True)
        if (any(collided)):
            self.kill()
            # Send an event to update the score
            pygame.event.post(TALLY_UP_EVENT)
        self.shoot_time += dt

        self.shoot()

    def shoot(self):
        if self.shoot_time >= self.shoot_timer:
            self.shoot_time = 0
            px = self.position.x + 4
            py = self.position.y + 8
            sp = 0.10

            self.bullet_spawner.spawn((px, py), sp)

class BasicEnemySpawner(EntityGroup):
    """Spawner of basic enemies, ships that move to ad fro shooting three bullets."""
    def __init__(self, size: tuple | list, color: int | tuple | list):
        EntityGroup.__init__(self)
        self.base_image = pygame.Surface(size).convert()
        self.bullet_spawner = BulletSpawner((8, 8), 0x00ffaa, 3, m.pi / 12)

    def spawn(self, position):
        enemy = Enemy(position, self.bullet_spawner)
        self.add(enemy)

    def empty(self):
        self.bullet_spawner.empty()
        super().empty()

    def update(self, *args, **kwargs):
        self.bullet_spawner.update(*args, **kwargs)
        super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        self.bullet_spawner.draw(surface)
