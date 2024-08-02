import pygame

ENEMY_SPAWN = pygame.event.custom_type()
TALLY_UP = pygame.event.custom_type()
TALLY_UP_EVENT = pygame.event.EventType(TALLY_UP, score=1)
