import pygame
import pygame.freetype
import pygame.mixer
import random
import math as m

from .players import Player
from .enemies import Enemy, BasicEnemySpawner
from .bullets import Bullet
from .entities import EntityGroup
from .staticwindows import Scoreboard, MainTitle, RetryWindow
from .events import ENEMY_SPAWN, TALLY_UP

class Game:
    def __init__(self, width: int, height: int):
        self.width, self.height = self.size = (width, height)
        pygame.init()
        pygame.freetype.init()
        pygame.mixer.init()
        self.font = pygame.freetype.SysFont("DejaVu Sans", 12)
        self.window = pygame.display.set_mode(self.size, flags=pygame.SCALED)

        self.bgmusic = pygame.mixer.Sound("media/third.wav")
        
        self.player = Player()
        
        self.enemies = BasicEnemySpawner((16, 16), 0xff7700)
        self.scoreboard = Scoreboard(self.font, 240, 32)
        self.title_screen = MainTitle(self.width, self.height)
        self.retry_window = RetryWindow(240, 64)

        # Creating, at once, all screens in the game: Title, Retry, and playground
        self.retry_window.set_text("Retry? Press R", 0xffffff, center="center", size=12)
        self.retry_window.move_to((120, 160))
        self.title_screen.set_text(" SHMUP", 0xff68b2f9, center="upper")
        self.title_screen.set_text("Press ANY button", 0xffffffff, center="lower", size=16)

        # Begin the game at state 0, main screen
        self.state = 0
        self.scoreboard.render_score()
        pygame.time.set_timer(ENEMY_SPAWN, 500)

    def setup_game(self):
        self.scoreboard.clean_score()
        self.player.alive = True
        self.enemies.empty()
        self.player.move_to(self.width / 2, self.height * 4 / 5)
        self.player.empty()
        self.bgmusic.play(loops=-1)
        self.state = 1
        
    def mainloop(self):
        self.running = True
        self.timer = pygame.time.Clock()
        while self.running:
            dt = self.timer.tick()
            self.process_events()
            self.update_logic(dt)
            self.render()
        pygame.quit()

    def process_events(self):
        events = pygame.event.get()
        if self.state == 0:
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    self.state = 1
                    self.setup_game()
                    self.player.alive = True
                    self.scoreboard.clean_score()
          
        elif self.state == 1:
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == ENEMY_SPAWN:
                    if (self.player.alive):
                        self.enemies.spawn(
                            (random.randint(0, self.width-32), -self.height / 5))
                elif event.type == TALLY_UP:
                    self.scoreboard.update_score(1)
                elif event.type == pygame.KEYDOWN:
                    pass
        elif self.state == 2:
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.setup_game()

                    
    def update_logic(self, dt):
        keys = pygame.key.get_pressed()

        # Title screen
        # TODO
        if self.state == 0:
            pass
        # Main logic of the game, while the player is alive
        elif self.state == 1:
            if (self.player.alive):
                rect = self.window.get_rect() # Window region clamp
                self.enemies.update(dt, rect, self.player)
                self.player.update(dt, keys, rect, self.enemies)
                return
            # TODO: Reset state
            self.state = 2
            self.bgmusic.stop()
            self.retry_window.set_bg(self.window.copy())
        # Restart screen
        # TODO
        elif self.state == 2:
            pass
        
    def render(self):
        self.window.fill(0x000000)
        if self.state == 0:
            self.title_screen.render_to(self.window)
            
        elif self.state == 1:
            self.player.draw(self.window)
            self.enemies.draw(self.window)
            # Score
            self.scoreboard.render_score()
            self.scoreboard.render_to(self.window)

        elif self.state == 2:
            self.retry_window.draw_retry(self.window)
            
        pygame.display.flip()
        
    def quit(self):
        self.running = False
