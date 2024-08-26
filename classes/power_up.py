import globals

from classes.config.map_config import MapPowerUpBlock

class PowerUp(MapPowerUpBlock):
    def __init__(self, config: MapPowerUpBlock):
        super().__init__(config, 
                         config.POSITION)
        self.set()

    def set(self):
        self.setup_collectable() 
        self.setup_glow(self.POSITION)
        self.collected_player_method = globals.player.collect_power_up

    def draw(self, speed):
        self.draw_obj(speed)
        
        if not self.collected:
            self.glow(speed)