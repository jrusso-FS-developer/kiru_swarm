import pygame
import globals

from classes.config.map_config import MapHeartBlock

class Heart(MapHeartBlock):
    def __init__(self, config: MapHeartBlock):
        super().__init__(config,
                         config.POSITION)
        self.set()

    def set(self):
        self.setup_collectable() 
        self.collected_player_method = globals.player.collect_heart

    def rotate(self):
        if (self._rotation_frame < self.ROTATION_FRAMES):
            self._surf = pygame.image.load(f'{self.IMAGE_PATH}/heart_rotation_{self._rotation_frame}.png')
            self._rotation_frame += 1
        else:
            self._rotation_frame = 0

    def draw(self, speed):
        self.draw_obj(speed)
        
        if self.collected:
            self.rotate()
            _divisor = 4
            if (self.get_position()[1] > self._float + 3.1):
                self.set_position(None, self.get_y() - int((self.get_y() - self._float) / _divisor))
            else:
                self.set_position(None, self._float)  
                self._alpha = self._alpha / _divisor            
                if (self._alpha > 10):
                    self._surf.set_alpha(self._alpha)
                else:
                    self._surf.set_alpha(5)
                    self.delete = True