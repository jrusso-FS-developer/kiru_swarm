import pygame
import globals

from classes.config.map_config import MapCoinBlock


class Coin(MapCoinBlock):
    def __init__(self, 
                 config: MapCoinBlock):
        super().__init__(config,
                         config.POSITION)
        self.set()

    def set(self):  
        self.setup_collectable() 
        self.collected_player_method = globals.player.collect_coin