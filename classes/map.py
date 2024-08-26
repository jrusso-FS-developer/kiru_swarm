from typing import List
from classes.config.map_config import MapBlock, MapConfig, MapObstacleBlock
from classes.config.obstacle_config import ObstacleBlock
from classes.obstacle import Obstacle


class Map(MapBlock):
    def __init__(self, config: MapBlock):
        super().__init__(config.NAME, 
                         config.LENGTH, 
                         config.COIN_CONFIGS, 
                         config.ENEMY_CONFIGS, 
                         config.HEART_CONFIGS,
                         config.OBSTACLE_CONFIGS, 
                         config.WEAPON_CONFIGS,
                         config.POWER_UP_CONFIGS,
                         config.GROUND_TILE)