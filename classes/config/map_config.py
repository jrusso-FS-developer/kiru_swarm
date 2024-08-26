from decimal import Decimal
import string
from typing import List
from classes.config.coin_config import CoinBlock, CoinConfig
from classes.config.enemy_config import EnemyBlock
from classes.config.heart_config import HeartBlock, HeartConfig
from classes.config.power_up_config import PowerUpBlock, PowerUpConfig
from classes.config.weapon_config import WeaponBlock, WeaponConfig
import globals
from classes.config.obstacle_config import ObstacleBlock, ObstacleConfig
from classes.config.enemy_config import EnemyBlock, EnemyConfig

class MapCoinBlock(CoinBlock):
    def __init__(self, 
                 config: CoinBlock,
                 POSITION: tuple
                 ):
        super().__init__(config.NAME, 
                         config.ANIMATION_FRAMES, 
                         config.ANIMATION_IMAGE_NAME, 
                         config.ANIMATION_IMAGE_NAME_REVERSE, 
                         config.IMAGE_NAME, 
                         config.IMAGE_PATH, 
                         config.SOUND_NAME, 
                         config.SOUND_PATH, 
                         config.VALUE,
                         config.OFFSETS, 
                         POSITION)
        self.POSITION = POSITION

    POSITION: tuple = (0, 0)

class MapHeartBlock(HeartBlock):
    def __init__(self, 
                 config: HeartBlock,
                 POSITION: tuple
                 ):
        super().__init__(config.NAME, 
                         config.ANIMATION_FRAMES,
                         config.ROTATION_FRAMES,
                         config.ANIMATION_IMAGE_NAME,
                         config.IMAGE_NAME,
                         config.IMAGE_PATH,
                         config.SOUND_NAME,
                         config.SOUND_PATH,
                         config.VALUE,
                         config.OFFSETS, 
                         POSITION)
        self.POSITION = POSITION

    POSITION: tuple = (0, 0)

class MapObstacleBlock(ObstacleBlock):
    def __init__(self, config:ObstacleBlock,
                 start_x:int, start_bottom:int):
        super().__init__(config.name, 
                        config.blocker,
                        config.right_offset, 
                        config.left_offset, 
                        config.top_offset, 
                        config.image_path, 
                        config.image_animation_path, 
                        config.image_secondary_animation_path, 
                        config.is_climable, 
                        config.is_landable, 
                        config.is_deadly_on_contact,
                        config.is_deadly_on_primary_animation,
                        config.is_deadly_on_secondary_animation,
                        config.animation_frames,
                        config.secondary_animation_frames,
                        config._animation_pause_timer,
                        config.secondary_animation_pause_timer,
                        config._hold_animation,
                        config.DEADLY_SIDES,
                        config.COLLIDABLE_SIDES)
        
        self._x = start_x
        self._bottom = start_bottom

    _x = 0
    _bottom = 0

class MapEnemyBlock(EnemyBlock):
    def __init__(self, 
                 config: EnemyBlock,
                 x, y):
        super().__init__(
                 config.ASSET_PATH,
                 config.ATTACK_ANIMATION_FRAMES,
                 config.ATTACKING_OFFSETS,
                 config.BEGIN_ATTACK_ANIMATION_FRAMES,
                 config.BOUNDARIES,
                 config.CEILING, 
                 config.COLLIDABLE_SIDES,
                 config.DAMAGE,
                 config.DANGER_ZONES,
                 config.DEADLY_SIDES,
                 config.DURABILITY,
                 config.FLOOR, 
                 config.HURT_ANIMATION_FRAMES,
                 config.IS_AGGRESSIVE,
                 config.IS_BOUNDED,
                 config.IS_FLYABLE,
                 config.IS_SMOOTH_MOVER,
                 config.IS_THINKER,
                 config.IS_WALKABLE,
                 config.MAIN_ANIMATION_FRAMES,
                 config.MAX_VELOCITY,
                 config.MIN_VELOCITY,
                 config.NAME,
                 config.OFFSETS,
                 config.POINTS_VALUE,
                 config.STILL_IMAGE,
                 config.THINKING_FRAME_RANGE,
                 config.VELOCITY)
        self._initial_x = x
        self._initial_y = y

    _initial_x = 0
    _initial_y = 0

class MapWeaponBlock(WeaponBlock):
    def __init__(self, 
                 config: WeaponBlock,
                 POSITION: tuple[Decimal, Decimal] = (0, 0)):
        super().__init__(config.NAME, 
                         config.ANIMATION_FRAMES,
                         config.DAMAGE, 
                         config.RANGE, 
                         config.STUN_TIME,
                         config.SOUND_PATH, 
                         config.IMAGE_PATH,
                         config.ATTACK_BOTTOM_OFFSET,
                         config.CROUCH_ATTACK_BOTTOM_OFFSET)
        self.POSITION = POSITION
    
    POSITION: tuple[Decimal, Decimal] = (0, 0)

class MapPowerUpBlock(PowerUpBlock):
    def __init__(self, 
                 config: PowerUpBlock,
                 POSITION: tuple[Decimal, Decimal] = (0, 0)):
        super().__init__(config.NAME, 
                         config.EFFECT_FRAMES,
                         config.EFFECT_TYPE,
                         config.GLOW_IMAGE_NAME,
                         config.IMAGE_NAME,
                         config.IMAGE_PATH,
                         config.SOUND_NAME,
                         config.SOUND_PATH,
                         config.OFFSETS,
                         POSITION)


class MapBlock:
    def __init__(self, 
                 NAME, 
                 LENGTH,
                 COIN_CONFIGS,
                 ENEMY_CONFIGS, 
                 HEART_CONFIGS,
                 OBSTACLE_CONFIGS, 
                 WEAPON_CONFIGS,
                 POWER_UP_CONFIGS,
                 GROUND_TILE):
        self.NAME = NAME
        self.LENGTH = LENGTH
        self.COIN_CONFIGS = COIN_CONFIGS
        self.ENEMY_CONFIGS = ENEMY_CONFIGS
        self.HEART_CONFIGS = HEART_CONFIGS
        self.OBSTACLE_CONFIGS = OBSTACLE_CONFIGS
        self.WEAPON_CONFIGS = WEAPON_CONFIGS
        self.POWER_UP_CONFIGS = POWER_UP_CONFIGS
        self.GROUND_TILE = GROUND_TILE
            
    NAME: str = ''
    COIN_CONFIGS:List[MapCoinBlock] = []
    ENEMY_CONFIGS:List[MapEnemyBlock] = []
    HEART_CONFIGS:List[MapHeartBlock] = []
    LENGTH: int = 0
    OBSTACLE_CONFIGS:List[MapObstacleBlock] = []
    WEAPON_CONFIGS:List[MapWeaponBlock] = []
    GROUND_TILE: str = ''

class MapConfig:
    Level1Map = MapBlock('Level1Map', # NAME
                         3800, # LENGTH in px
                        [MapCoinBlock(CoinConfig.COIN_1, (2100, globals.GROUND - 300)),
                         MapCoinBlock(CoinConfig.COIN_1, (2165, globals.GROUND - 300)),
                         MapCoinBlock(CoinConfig.COIN_1, (2230, globals.GROUND - 300)),
                         MapCoinBlock(CoinConfig.COIN_1, (2100, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (2165, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (2230, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (2800, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (2865, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (2930, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (2995, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (3060, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (3125, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (3190, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (3255, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (3320, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (3380, globals.GROUND - 10)),
                         MapCoinBlock(CoinConfig.COIN_1, (3445, globals.GROUND - 10))], # COIN_CONFIGS
                        [MapEnemyBlock(EnemyConfig.BUMBLE, 800, 375),
                         MapEnemyBlock(EnemyConfig.PORKY_PINE, 1300, globals.GROUND)], # ENEMY_CONFIGS,
                         [MapHeartBlock(HeartConfig.HEART_1, (3445, globals.GROUND - 210))], # HEART_CONFIGS
                         [MapObstacleBlock(ObstacleConfig.TRASHCAN, # config
                                            1100, # x
                                            globals.GROUND + 5, # bottom
                                           ), 
                          MapObstacleBlock(ObstacleConfig.DONOTENTER_SIGN, 
                                            1390, # x
                                            globals.GROUND + 5, # bottom
                                           ),
                          MapObstacleBlock(ObstacleConfig.ARROWRIGHT_SIGN, 
                                            1460, # x
                                            globals.GROUND + 5, # bottom
                                           ),
                          MapObstacleBlock(ObstacleConfig.PLATFORM_MEDIUM, 
                                            1650, # x
                                            globals.GROUND - 110, # bottom
                                           ),
                          MapObstacleBlock(ObstacleConfig.PLATFORM_SMALL, 
                                            2100, # x
                                            globals.GROUND - 180, # bottom
                                           ),
                          MapObstacleBlock(ObstacleConfig.PLATFORM_SMALL, 
                                            2400, # x
                                            globals.GROUND, # bottom
                                           ),
                          MapObstacleBlock(ObstacleConfig.PLATFORM_MEDIUM, 
                                            2800, # x
                                            globals.GROUND - 110, # bottom
                                           ),
                          MapObstacleBlock(ObstacleConfig.PLATFORM_MEDIUM, 
                                            3160, # x
                                            globals.GROUND - 110, # bottom
                                           )],
                        [MapWeaponBlock(WeaponConfig.CHUCKS,
                                        (3600, globals.GROUND - 30))], # WEAPON_CONFIGS
                        [MapPowerUpBlock(PowerUpConfig.IMMUNITY,
                                         (1950, globals.GROUND -212))], # POWER_UP_CONFIGS
                        'sprites/assets/city_ground_tile_day.png')