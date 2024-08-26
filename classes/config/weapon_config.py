from enum import Enum

class WeaponBlock:
    def __init__(self, 
                 NAME, 
                 ANIMATION_FRAMES,
                 DAMAGE, 
                 RANGE, 
                 STUN_TIME,
                 SOUND_PATH, 
                 IMAGE_PATH,
                 ATTACK_BOTTOM_OFFSET,
                 CROUCH_ATTACK_BOTTOM_OFFSET):
        self.NAME = NAME
        self.ANIMATION_FRAMES = ANIMATION_FRAMES
        self.DAMAGE = DAMAGE
        self.RANGE = RANGE
        self.STUN_TIME = STUN_TIME
        self.SOUND_PATH = SOUND_PATH
        self.IMAGE_PATH = IMAGE_PATH
        self.ATTACK_BOTTOM_OFFSET = ATTACK_BOTTOM_OFFSET
        self.CROUCH_ATTACK_BOTTOM_OFFSET = CROUCH_ATTACK_BOTTOM_OFFSET
        self.selected = False

    NAME: str = ''
    ANIMATION_FRAMES: int = 0
    DAMAGE: int = 0
    RANGE: int = 0
    STUN_TIME: int = 0
    SOUND_PATH: str = ''
    IMAGE_PATH: str = ''
    ATTACK_BOTTOM_OFFSET: int = 0
    CROUCH_ATTACK_BOTTOM_OFFSET: int = 0
    selected: bool = False

class WeaponConfig:
    SAMURAI = WeaponBlock('samurai',  # NAME
                          24, # ANIMATION_FRAMES
                          80, # DAMAGE
                          75, # RANGE
                          10, # STUN_TIME
                          'sounds/character/player/ninja-boy/weapons/samurai', # SOUND_PATH
                          'sprites/characters/player/ninja-boy/weapons/samurai', # IMAGE_PATH
                          0, # ATTACK_BOTTOM_OFFSET
                          0 # CROUCH_ATTACK_BOTTOM_OFFSET
                          )
    CHUCKS = WeaponBlock('chucks', # NAME
                          24, # ANIMATION_FRAMES
                          50, # DAMAGE
                          75, # RANGE
                          160, # STUN_TIME
                          'sounds/character/player/ninja-boy/weapons/chucks', # SOUND_PATH
                          'sprites/characters/player/ninja-boy/weapons/chucks', # IMAGE_PATH
                          3, # ATTACK_BOTTOM_OFFSET
                          12 # CROUCH_ATTACK_BOTTOM_OFFSET
                          )