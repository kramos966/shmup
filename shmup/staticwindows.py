import pygame
import pygame.freetype
import random
import math as m

class Background(pygame.sprite.Sprite):
    def __init__(self, bg: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.rect = bg.get_rect()
        self.image = bg.convert()

class StaticWindow(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = self.size = (width, height)
        self.image = pygame.Surface(self.size).convert()
        self.rect = self.image.get_rect()

    def render_to(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        
    def set_text(self, text: str, color, center: list | tuple | str, size=36):
        self.font.size = size
        text, rect = self.font.render(text, fgcolor=color)
        # Center text on screen
        if type(center) == str:
            if center == "center":
                rect.center = (self.width // 2, self.height // 2)
            elif center == "upper":
                rect.center = (self.width // 2, self.height // 3)
            elif center == "lower":
                rect.center = (self.width // 2, self.height * 2 // 3)
        self.image.blit(text, rect)
        
class Scoreboard(StaticWindow):
    def __init__(self, font, width, height):
        StaticWindow.__init__(self, width, height)
        self.tally = 0
        self.font = font

    def update_score(self, new_scores):
        self.tally += new_scores

    def clean_score(self):
        self.tally = 0
      
    def render_score(self):
        self.image.fill(0x000000)
        pygame.draw.line(self.image, 0xffffff, (0, self.height - 1), (self.width, self.height - 1))
        self.text = self.font.render_to(self.image, (140, 10), f"Score = {str(self.tally)}",
                                        fgcolor=0xffffff)

class MainTitle(StaticWindow):
    def __init__(self, width, height):
        StaticWindow.__init__(self, width, height)
        self.font = pygame.freetype.SysFont("DejaVu Sans", 36, bold=True)
        self.image.fill(0x000000)

class RetryWindow(StaticWindow):
    def __init__(self, width, height):
        StaticWindow.__init__(self, width, height)
        self.font = pygame.freetype.SysFont("DejaVu Sans", 12, bold=False)

    def set_bg(self, bg: pygame.Surface):
        self.bg = bg

    def draw_retry(self, surface: pygame.Surface):
        surface.blit(self.bg, (0, 0))
        super().render_to(surface)

    def move_to(self, center):
        self.rect.center = center
