from typing import Tuple
import pygame
import globals

class GlowBehavior():
    def __init__(self):
        self.setup_glow(self.GLOW_POSITION)

    # CONSTANTS
    GLOW_IMAGE_NAME: str = ''
    GLOW_POSITION: Tuple[int, int] = (0, 0)
    IMAGE_PATH: str = ''

    # variables
    _alpha = 0
    _surf_glow: pygame.Surface = None
    _glow_rect: pygame.Rect = None
    _reverse: bool = False

    def setup_glow(self, _position: Tuple[int, int]):        
        self.GLOW_POSITION = (_position[0] - 8, _position[1] - 10)
        self._surf_glow = pygame.image.load(f'{self.IMAGE_PATH}/{self.GLOW_IMAGE_NAME}')
        self._glow_rect = self._surf_glow.get_rect()
        self.set_glow_position(self.GLOW_POSITION[0], self.GLOW_POSITION[1] - self.get_height())
    
    def get_glow_x(self):
        return self._glow_rect.x
    
    def get_glow_y(self):
        return self._glow_rect.y
    
    def get_glow_position(self) -> Tuple[int, int]: 
        return (self.get_glow_x(), self.get_glow_y())

    def set_glow_position(self, x = None, y = None):
        self._glow_rect.x = x if x != None else self._glow_rect.x
        self._glow_rect.y = y if y != None else self._glow_rect.y

    def glow(self, speed):        
        _new_x = self.GLOW_POSITION[0] - speed if not globals.game_paused and globals.game_moving else self.get_glow_x()
        self.set_glow_position(_new_x)

        if (self._alpha >= 85):
            self._reverse = True
        elif (self._alpha <= 5):
            self._reverse = False

        self._alpha = (self._alpha - self._alpha / 10) if self._reverse else (self._alpha + (90 - self._alpha) / 10)
        self._surf_glow.set_alpha(self._alpha)
        globals.SCREEN.blit(self._surf_glow, self.get_glow_position())