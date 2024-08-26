from decimal import Decimal
import pygame
from Box2D import (b2World)


# global game constants
DEBUG_MODE: bool = False
EDGE_THRESHOLD: int = 240
GAME_LIFE_COUNT: int = 3
GROUND: int = 700
MIN_BG_SCROLL_SPEED: Decimal = .18
MIN_GROUND_SCROLL_SPEED: int = 1
MUSIC_PATH: str = 'sounds/music'
PPM: Decimal = 1.16
SCREEN_HEIGHT: int = 800
SCREEN_WIDTH: int = 1400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# global game variables
bg_scroll_speed: Decimal = MIN_BG_SCROLL_SPEED
ground_scroll_speed: int = MIN_GROUND_SCROLL_SPEED
game_paused: bool = False
game_moving: bool = False
game_over: bool = False
debug: bool = True
player = None
pressed_keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
restart_level: bool = False
screen_center: tuple[Decimal, Decimal] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# create 2d physics world
physics_world = b2World()