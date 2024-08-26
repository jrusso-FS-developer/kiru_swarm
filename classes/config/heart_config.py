from typing import List, Tuple
from classes.collectable_object import CollectableObject


class HeartBlock(CollectableObject):
    def __init__(self,    
                 NAME: str,  
                 ANIMATION_FRAMES: int,
                 ROTATION_FRAMES: int,
                 ANIMATION_IMAGE_NAME: str,
                 IMAGE_NAME: str,
                 IMAGE_PATH: str,
                 SOUND_NAME: str,
                 SOUND_PATH: str, 
                 VALUE: int,
                 OFFSETS: List[int] = [0, 0, 0, 0],
                 POSITION: Tuple[int, int] = (0, 0)): # top, right, bottom, left
        super().__init__(NAME, ANIMATION_FRAMES, ANIMATION_IMAGE_NAME, ANIMATION_IMAGE_NAME, IMAGE_NAME, IMAGE_PATH, SOUND_NAME, SOUND_PATH, OFFSETS, POSITION)
        self.ANIMATION_FRAMES = ANIMATION_FRAMES
        self.ROTATION_FRAMES = ROTATION_FRAMES
        self.VALUE = VALUE
    
    ANIMATION_FRAMES: int = 0
    ROTATION_FRAMES: int = 0
    VALUE: int = 0

class HeartConfig:
    HEART_1 = HeartBlock(
        'health', # NAME
        24, # ANIMATION_FRAMES
        12, # ROTATION_FRAMES
        'heart_throb', # ANIMATION_IMAGE_NAME
        'heart_throb_0.png', # IMAGE_NAME
        'sprites/items/heart', # IMAGE_PATH
        'heart-collect.mp3', # SOUND_NAME
        'sounds/sfx', # SOUND_PATH
        50, # VALUE PERCENT (Adds 50% health to player's health bar)
        [0, 0, 8, 0], # OFFSETS
        (0, 0) # POSITION
    )