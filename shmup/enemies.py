import pygame
import pygame.freetype
import random
import math as m

from .entities import Entity, EntityGroup
from .bullets import Bullet
from .color import CKEY
from .misc import sign
from .events import TALLY_UP_EVENT

class Enemy(Entity):
    def __init__(self, position: list | pygame.math.Vector2):
        Entity.__init__(self)
        self.position = pygame.math.Vector2(position)
        self.speed = 0.08
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = self.direction * self.speed
        self.image = pygame.Surface((16, 16)).convert()
        self.image.set_colorkey(CKEY)
        self.rect = self.image.get_rect()
        #self.rect.scale_by_ip(0.8)
        self.shoot_timer = 800
        self.shoot_time = 0
        self.image.fill(CKEY)
        pygame.draw.circle(self.image, 0xaa3333, (8, 8), 8)
        self.turn_wait = random.randint(1200, 2000)
        self.turn_timer = 0
        self.turn = -sign(self.position.x - 120)
        self.turn_c = 0

    def acceleration(self):
        accel = pygame.math.Vector2(0, 0)
        if self.turn_timer > self.turn_wait:
            accel.x = self.turn * self.velocity.y * 1 - self.velocity.x
            self.turn_timer = 0
            self.turn_c += 1
            self.turn = -self.turn
        return accel

    def update(self, dt: int | float, clamp_reg: pygame.rect, p_bullets: EntityGroup,
               e_bullets: EntityGroup):
        self.turn_timer += dt
        super().update(dt)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        #self.clamp(clamp_reg)

        if (self.rect.y > clamp_reg.h):
            self.kill()
        collided = pygame.sprite.spritecollide(self, p_bullets, True)
        if (any(collided)):
            self.kill()
            # Send an event to update the score
            pygame.event.post(TALLY_UP_EVENT)
        self.shoot_time += dt
        self.shoot(e_bullets)

    def shoot(self, e_bullets: EntityGroup):
        if self.shoot_time >= self.shoot_timer:
            self.shoot_time = 0
            px = self.position.x + 4
            py = self.position.y + 8
            sp = -0.1
            bullet = Bullet(0xaaff77, (px, py), sp)
            e_bullets.add(bullet)
            
            direction = [m.sin(m.pi / 10), -m.cos(m.pi / 10)]
            bullet2 = Bullet(0xaaff77, (px, py), sp) 
            bullet2.set_direction(direction)
            e_bullets.add(bullet2)
            
            direction[0] = -direction[0]
            bullet3 = Bullet(0xaaff77, (px, py), sp)
            bullet3.set_direction(direction)
            e_bullets.add(bullet3)
