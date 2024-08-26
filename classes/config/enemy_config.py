from enum import Enum
from typing import List
from classes.config.enums.danger_zone import DangerZone
import globals

from classes.config.enums.sides import Sides

class EnemyBlock:
    def __init__(self,
                 ASSET_PATH: str,
                 ATTACK_ANIMATION_FRAMES: int,
                 ATTACKING_OFFSETS: int,
                 BEGIN_ATTACK_ANIMATION_FRAMES: int,
                 BOUNDARIES: List[int],
                 CEILING: int, 
                 COLLIDABLE_SIDES: List[Sides],
                 DAMAGE: int,
                 DANGER_ZONES: List[Enum],
                 DEADLY_SIDES: List[Sides],
                 DURABILITY: int,
                 FLOOR: int, 
                 HURT_ANIMATION_FRAMES: int,
                 IS_AGGRESSIVE: bool,
                 IS_BOUNDED: bool,
                 IS_FLYABLE: bool,
                 IS_SMOOTH_MOVER: bool,
                 IS_THINKER: bool,
                 IS_WALKABLE: bool,
                 MAIN_ANIMATION_FRAMES: int,
                 MAX_VELOCITY: int,
                 MIN_VELOCITY: int,
                 NAME: str,
                 OFFSETS: int,
                 POINTS_VALUE: int,
                 STILL_IMAGE: str,
                 THINKING_FRAME_RANGE: tuple[int, int],
                 VELOCITY: int):
        self.ATTACK_ANIMATION_FRAMES = ATTACK_ANIMATION_FRAMES
        self.ATTACKING_OFFSETS = ATTACKING_OFFSETS
        self.ASSET_PATH = ASSET_PATH
        self.BEGIN_ATTACK_ANIMATION_FRAMES = BEGIN_ATTACK_ANIMATION_FRAMES
        self.BOUNDARIES = BOUNDARIES
        self.CEILING = CEILING
        self.COLLIDABLE_SIDES = COLLIDABLE_SIDES
        self.DAMAGE = DAMAGE
        self.DANGER_ZONES = DANGER_ZONES
        self.DEADLY_SIDES = DEADLY_SIDES
        self.DURABILITY = DURABILITY
        self.FLOOR = FLOOR
        self.HURT_ANIMATION_FRAMES = HURT_ANIMATION_FRAMES
        self.IS_AGGRESSIVE = IS_AGGRESSIVE
        self.IS_BOUNDED = IS_BOUNDED
        self.IS_FLYABLE = IS_FLYABLE
        self.IS_SMOOTH_MOVER = IS_SMOOTH_MOVER
        self.IS_THINKER = IS_THINKER
        self.IS_WALKABLE = IS_WALKABLE
        self.MAIN_ANIMATION_FRAMES = MAIN_ANIMATION_FRAMES
        self.MAX_VELOCITY = MAX_VELOCITY
        self.MIN_VELOCITY = MIN_VELOCITY
        self.NAME = NAME
        self.OFFSETS = OFFSETS
        self.POINTS_VALUE = POINTS_VALUE
        self.STILL_IMAGE = STILL_IMAGE
        self.THINKING_FRAME_RANGE = THINKING_FRAME_RANGE
        self.VELOCITY = VELOCITY    

        self._top_offset = OFFSETS[0]
        self._right_offset = OFFSETS[1]
        self._bottom_offset = OFFSETS[2]
        self._left_offset = OFFSETS[3]

    # constants
    ASSET_PATH = ''
    ATTACK_ANIMATION_FRAMES: int = 0
    BEGIN_ATTACK_ANIMATION_FRAMES: int = 0
    BOUNDARIES: List[int] = [0, 0]
    CEILING: int = 0
    COLLIDABLE_SIDES: List[Sides]
    DAMAGE: int = 10
    DANGER_ZONES: List[Enum]
    DEADLY_SIDES: List[Sides]
    DURABILITY: int = 20
    FLOOR: int = 0
    HURT_ANIMATION_FRAMES: int = 0
    IS_AGGRESSIVE = False
    IS_BOUNDED = False
    IS_FLYABLE = False
    IS_SMOOTH_MOVER = False
    IS_THINKER = False
    IS_WALKABLE = False
    MAIN_ANIMATION_FRAMES = 11
    MAX_VELOCITY: int = 100
    MIN_VELOCITY: int = 1
    NAME = ''
    STILL_IMAGE = ''
    THINKING_FRAME_RANGE: tuple[int, int] = (0, 0)
    VELOCITY: int = 0

    # offset constants
    ATTACKING_OFFSETS: List[int] = [0, 0, 0, 0]
    OFFSETS: List[int] = [0, 0, 0, 0]
    _bottom_offset:int = 0
    _left_offset:int = 0
    _right_offset:int = 0
    _top_offset:int = 0

    # vars
    _health: int = 100

class EnemyConfig:
    # Bumble's actively deadly sides change depending on which direction he's facing.  
    # This is handled in the enemy class.
    BUMBLE: EnemyBlock = EnemyBlock(
        'sprites/characters/enemies/bumble', # ASSET_PATH
        5, # ATTACK_ANIMATION_FRAMES
        [5, 10, 50, 10], # ATTACKING_OFFSETS
        5, # BEGIN_ATTACK_ANIMATION_FRAMES
        [180, 180], # BOUNDARIES
        50, # CEILING
        [Sides.BOTTOM, Sides.LEFT, Sides.RIGHT, Sides.TOP], # COLLIDABLE_SIDES
        25, # DAMAGE
        [DangerZone.BOTTOM_LEFT, DangerZone.BOTTOM_RIGHT], # DANGER_ZONES
        [Sides.BOTTOM], # DEADLY_SIDES
        .50, # DURABILITY
        globals.GROUND, # FLOOR
        24, # HURT_ANIMATION_FRAMES
        True, # IS_AGGRESSIVE
        True, # IS_BOUNDED
        True, # IS_FLYABLE
        True, # IS_SMOOTH_MOVER
        True, # IS_THINKER
        False, # IS_WALKABLE
        23, # MAIN_ANIMATION_FRAMES
        35, # MAX_VELOCITY
        1, # MIN_VELOCITY
        'Bumble', # NAME
        [5, 10, 10, 10], # OFFSETS [top, right, bottom, left]
        100, # POINTS_VALUE
        'bumble.png', # STILL_IMAGE
        (180, 300), # THINKING_FRAME_RANGE
        15 # VELOCITY
        )
    PORKY_PINE: EnemyBlock = EnemyBlock(
        'sprites/characters/enemies/porky-pine', # ASSET_PATH
        23, # ATTACK_ANIMATION_FRAMES
        [5, 5, 1, 5], # ATTACKING_OFFSETS
        0, # BEGIN_ATTACK_ANIMATION_FRAMES
        [0, 0], # BOUNDARIES
        50, # CEILING
        [Sides.BOTTOM, Sides.LEFT, Sides.RIGHT, Sides.TOP], # COLLIDABLE_SIDES
        20, # DAMAGE
        [DangerZone.TOP_LEFT, DangerZone.TOP_RIGHT, DangerZone.BOTTOM_LEFT, DangerZone.BOTTOM_RIGHT], # DANGER_ZONES
        [Sides.BOTTOM, Sides.TOP, Sides.LEFT, Sides.RIGHT], # DEADLY_SIDES
        .20, # DURABILITY
        globals.GROUND, # FLOOR
        0, # HURT_ANIMATION_FRAMES
        False, # IS_AGGRESSIVE
        False, # IS_BOUNDED
        False, # IS_FLYABLE
        False, # IS_SMOOTH_MOVER
        True, # IS_THINKER
        True, # IS_WALKABLE
        23, # MAIN_ANIMATION_FRAMES
        5, # MAX_VELOCITY
        1, # MIN_VELOCITY
        'Porky-Pine', # NAME
        [5, 5, 5, 5], # OFFSETS [top, right, bottom, left]
        60, # POINTS_VALUE
        'porky_pine.png', # STILL_IMAGE
        (60, 120), # THINKING_FRAME_RANGE
        5 # VELOCITY
        )