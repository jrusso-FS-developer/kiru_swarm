from enum import Enum
from typing import List, Tuple

from classes.collectable_object import CollectableObject

class CoinBlock(CollectableObject):
    def __init__(self, 
                 NAME: str,
                 ANIMATION_FRAMES: int,
                 ANIMATION_IMAGE_NAME: str,
                 ANIMATION_IMAGE_NAME_REVERSE: str,
                 IMAGE_NAME: str,
                 IMAGE_PATH: str,
                 SOUND_NAME: str,
                 SOUND_PATH: str, 
                 VALUE: int,
                 OFFSETS: List[int] = [0, 0, 0, 0],
                 POSITION: Tuple[int, int] = (0, 0)):
        super().__init__(NAME, 
                         ANIMATION_FRAMES, 
                         ANIMATION_IMAGE_NAME, 
                         ANIMATION_IMAGE_NAME_REVERSE, 
                         IMAGE_NAME, 
                         IMAGE_PATH, 
                         SOUND_NAME, 
                         SOUND_PATH, 
                         OFFSETS, 
                         POSITION)
        self.NAME = NAME
        self.VALUE = VALUE

    NAME: str = ''
    VALUE: int = 0

class CoinConfig:
    COIN_1 = CoinBlock(
        '+ 1', # NAME
        11, # ANIMATION_FRAMES
        'rotation', # ANIMATION_IMAGE_NAME
        'rotation_rapid', # ANIMATION_IMAGE_NAME_REVERSE
        'rotation_0.png', # IMAGE_NAME
        'sprites/items/coin/1', # IMAGE_PATH
        'coin-collect.mp3', # SOUND_NAME
        'sounds/sfx', # SOUND_PATH
        1, # VALUE
        [0, 0, 8, 0], # OFFSETS
        (0, 0) # POSITION
    )