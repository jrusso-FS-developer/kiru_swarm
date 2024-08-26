import math
from typing import List
import pygame
import gc
from Box2D import (b2PolygonShape, b2CircleShape)

from classes.heart import Heart
from classes.power_up import PowerUp
from classes.weapon import Weapon
import globals

from classes.coin import Coin
from classes.debugger import Debugger
from classes.enemy import Enemy
from classes.game_timer import GameTimer
from classes.obstacle import Obstacle
from classes.background import Background
from classes.config.level_config import LevelBlock, LevelConfig, Theme
from classes.map import Map
from classes.player import Player

class Level(LevelBlock):
    def __init__(self, level_number):
        self.set(level_number)

    # variables
    name = ''
    length = 0
    backdroppath = ''
    end = False
    background = None
    theme = None
    screen_center = (0, 0)
    map:Map = None

    _coins:List[Coin] = []
    _enemies:List[Enemy] = []
    _final_width: int = 0
    _ground_scroll: int = 0
    _ground_surf: pygame.Surface = None
    _ground_surf_rect: pygame.Rect = None
    _ground_tile_count: int = 0
    _hearts: List[Heart] = []
    _music_paused: bool = False
    _obstacles: List[Obstacle] = []
    _power_ups: List[PowerUp] = []
    _timer: GameTimer = None
    _time_display_sur: pygame.Surface = None
    _time_display_surf_rect: pygame.Rect = None
    _timer_font: pygame.font.Font = None
    _timer_bg_surf: pygame.Surface = None
    _timer_bg_surf_rect: pygame.Rect = None
    _weapons: List[Weapon] = []

    def set(self, level_number):
        # clear physics world
        for body in list(globals.physics_world.bodies):
            globals.physics_world.DestroyBody(body)

        config: LevelBlock = list(LevelConfig)[level_number - 1].value
        super().__init__(config.name, config.theme, config.map_config, config.backdroppath, config.foregroundpaths, config.midgroundpaths, config.music_path)
        self.screen_center = globals.screen_center
        self.end = False 
        if (globals.player == None):  
            globals.player = Player()
        self._timer_font = pygame.font.Font('fonts/ds_digib.ttf', 72)
        self._ground_scroll = 0

        # create map instance
        if (self.map):
            del self.map
            gc.collect()
        self.map = None
        self.map = Map(config.map_config)
        self.GROUND_TILE = self.map.GROUND_TILE
        self.length = self.map.LENGTH

        # set coins
        self._coins = []
        for coin in self.map.COIN_CONFIGS:
            self._coins.append(Coin(coin))

        # set enemies
        self._enemies = []
        for enemy in self.map.ENEMY_CONFIGS:
            self._enemies.append(Enemy(enemy))

        # set hearts
        self._hearts = []
        for heart in self.map.HEART_CONFIGS:
            self._hearts.append(Heart(heart))

        # set obstacles
        self._obstacles = []
        for obstacle in self.map.OBSTACLE_CONFIGS:
            self._obstacles.append(Obstacle(obstacle))

        # set power ups
        self._power_ups = []
        for power_up in self.map.POWER_UP_CONFIGS:
            self._power_ups.append(PowerUp(power_up))

        # set weapons
        self._weapons = []
        for weapon in self.map.WEAPON_CONFIGS:
            self._weapons.append(Weapon(weapon))

        # create background instance 
        globals.game_moving = False  
        globals.game_paused = False  
        if (self.background):
            del self.background
            gc.collect()
        self.background = None
        self.background = Background(0, 0, self)

        # set the ground image tile to the map
        self._ground_surf = pygame.image.load(self.map.GROUND_TILE)
        self._ground_surf_rect = self._ground_surf.get_rect()
        self._ground_surf_rect.center = self.screen_center
        self._ground_tile_count = math.ceil(self.length / self._ground_surf_rect.width * 6)

        # play music
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(.4)
        pygame.mixer.music.play(5)
        self._music_paused = False

        pygame.font.init()  # Initialize the font module

        # set timer
        self._timer = GameTimer()      

    def draw(self):          
        # pause music if game is paused       
        if (globals.game_paused and not self._music_paused):
            pygame.mixer.music.pause()
            self._music_paused = True
        elif (not globals.game_paused and self._music_paused):
            pygame.mixer.music.unpause()
            self._music_paused = False

        if (globals.player.is_dying):
            pygame.mixer.music.stop()
        
        if self.theme == Theme.DAY:
            globals.SCREEN.fill((42, 48, 51))
        elif self.theme == Theme.NIGHT:
            globals.SCREEN.fill((46, 49, 51))
        else:
            globals.SCREEN.fill((0, 0, 0))  
        self.background.draw()

        # move the ground
        self._ground_surf_rect.top = globals.GROUND 
        if (not globals.game_paused and globals.game_moving and not globals.player.is_dying):
            self._ground_scroll += globals.ground_scroll_speed  
            pygame.mixer.music.set_volume(.25)
        else:
            self._ground_scroll += 0

        for i in range(self._ground_tile_count):
            globals.SCREEN.blit(self._ground_surf, (i * self._ground_surf_rect.width - self._ground_scroll, self._ground_surf_rect.y))

        # now start the timer
        if not globals.game_paused and globals.game_moving:
            if not self._timer.started:
                self._timer.start()

        # remove dead enemies
        for enemy in self._enemies:
            if (enemy.is_dead):
                self._enemies.remove(enemy)
                del enemy
                gc.collect()

        # remove collected coins
        for coin in self._coins:
            if (coin.collected and coin.delete):
                self._coins.remove(coin)
                del coin
                gc.collect()

        # remove collected hearts
        for heart in self._hearts:
            if (heart.collected and heart.delete):
                self._hearts.remove(heart)
                del heart
                gc.collect()

        # remove collected power ups
        for power_up in self._power_ups:
            if (power_up.collected and power_up.delete):
                self._power_ups.remove(power_up)
                del power_up
                gc.collect()

        # draw power ups
        for power_up in self._power_ups:
            power_up.draw(self._ground_scroll)

        # remove collected weapons
        for weapon in self._weapons:
            if (weapon.collected and weapon.delete):
                self._weapons.remove(weapon)
                del weapon
                gc.collect()  

        # draw obstacles
        for obstacle in self._obstacles:
            obstacle.draw(self._ground_scroll)  

        # draw coins
        for coin in self._coins:
            coin.draw_obj(self._ground_scroll)

        # draw hearts
        for heart in self._hearts:
            heart.draw(self._ground_scroll)

        # draw weapons
        for weapon in self._weapons:
            weapon.draw(self._ground_scroll)

        # draw enemies
        for enemy in self._enemies:
            enemy.draw(self._obstacles) 
            
        # manage key presses
        globals.player.draw(self._obstacles, globals.ground_scroll_speed) 

        # add player to screen
        globals.SCREEN.blit(globals.player.surf, globals.player._rect)

        # update timer if player is not dying
        if (not globals.player.is_dying):
            self._timer.draw()
                 
        self._time_display_surf = self._timer_font.render(self._timer.display(), True, (1, 255, 9))
        self._timer_font.set_bold(True)
        self._time_display_surf_rect = self._time_display_surf.get_rect()
        self._final_width = self._time_display_surf_rect.width if self._final_width == 0 else self._final_width
        self._time_display_surf_rect.center = (globals.SCREEN_WIDTH // 2 - self._final_width // 2, 2)
        globals.SCREEN.blit(self._time_display_surf, self._time_display_surf_rect.center)     

        # keep this around for debugging the raycast which checks for obstacles between player and enemy
        # self.debug_ray_cast()

    def debug_ray_cast(self):
        # Define a color for the fixture outlines
        outline_color = (255, 0, 0)  # Red

        # Iterate over all bodies in the world
        for body in globals.physics_world.bodies:

            # Iterate over all fixtures of the body
            for fixture in body.fixtures:
                # Check the shape of the fixture
                if isinstance(fixture.shape, b2PolygonShape):
                    # Transform the vertices from local coordinates to world coordinates
                    vertices = [(body.transform * v) * globals.PPM for v in fixture.shape.vertices]
                    # Convert the vertices from world coordinates to screen coordinates
                    vertices = [(v[0], (globals.SCREEN_HEIGHT - v[1])) for v in vertices]
                    # Reverse the y-coordinate to fix the mirror effect
                    vertices = [(v[0], globals.SCREEN_HEIGHT - v[1]) for v in vertices]
                    # If it's a polygon shape, draw a polygon
                    pygame.draw.polygon(globals.SCREEN, outline_color, vertices, 1)  # The last argument is the line width

                elif isinstance(fixture.shape, b2CircleShape):
                    # If it's a circle shape, draw a circle
                    center = body.transform * fixture.shape.pos * globals.PPM
                    # Reverse the y-coordinate to fix the mirror effect
                    center = (center[0], globals.SCREEN_HEIGHT - center[1])
                    radius = fixture.shape.radius * globals.PPM
                    pygame.draw.circle(globals.SCREEN, outline_color, center, radius, 1)
