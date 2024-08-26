from enum import Enum
from typing import List, Tuple

from classes.behaviors.glow import GlowBehavior
from classes.collectable_object import CollectableObject

class EFFECT_TYPES(Enum):
    IMMUNITY = 1
    SUPER_STRIKE = 2
    SUPER_JUMP = 3

class PowerUpBlock(CollectableObject, GlowBehavior):
    def __init__(self, 
                 NAME: str, 
                 EFFECT_FRAMES: int,
                 EFFECT_TYPE: EFFECT_TYPES,
                 GLOW_IMAGE_NAME: str,
                 IMAGE_NAME: str,
                 IMAGE_PATH: str,
                 SOUND_NAME: str,
                 SOUND_PATH: str, 
                 OFFSETS: List[int] = [0, 0, 0, 0],
                 POSITION: Tuple[int, int] = (0, 0)): # top, right, bottom, left
        super().__init__(NAME, 0, '', '', IMAGE_NAME, IMAGE_PATH, SOUND_NAME, SOUND_PATH, OFFSETS, POSITION)
        self.NAME = NAME
        self.EFFECT_FRAMES = EFFECT_FRAMES
        self.EFFECT_TYPE = EFFECT_TYPE
        self.GLOW_IMAGE_NAME = GLOW_IMAGE_NAME

    NAME: str = ''
    EFFECT_FRAMES: int = 0
    EFFECT_TYPE: EFFECT_TYPES = None

class PowerUpConfig:
    IMMUNITY = PowerUpBlock(
        'immunity', # NAME
        600, # EFFECT_FRAMES,
        EFFECT_TYPES.IMMUNITY, # EFFECT_TYPE
        'glow-bottle.png', # GLOW_IMAGE_NAME
        'blue-bottle.png', # IMAGE_NAME
        'sprites/assets/power-ups/bottles', # IMAGE_PATH
        'power-up-collect.mp3', # SOUND_NAME
        'sounds/sfx', # SOUND_PATH
        [0, 0, 8, 0], # OFFSETS
        (0, 0) # POSITION
    )