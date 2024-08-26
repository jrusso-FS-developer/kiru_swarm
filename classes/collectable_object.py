import pygame
import globals

from typing import List, Tuple

class CollectableObject():
    def __init__(self,
                 NAME: str,
                 ANIMATION_FRAMES: int,
                 ANIMATION_IMAGE_NAME: str,
                 ANIMATION_IMAGE_NAME_REVERSE: str,
                 IMAGE_NAME: str,
                 IMAGE_PATH: str,
                 SOUND_NAME: str,
                 SOUND_PATH: str,
                 OFFSETS: List[int] = [0, 0, 0, 0],                 
                 POSITION: Tuple[int, int] = (0, 0)):
        self.NAME = NAME
        self.ANIMATION_FRAMES = ANIMATION_FRAMES
        self.ANIMATION_IMAGE_NAME = ANIMATION_IMAGE_NAME
        self.ANIMATION_IMAGE_NAME_REVERSE = ANIMATION_IMAGE_NAME_REVERSE
        self.IMAGE_NAME = IMAGE_NAME
        self.IMAGE_PATH = IMAGE_PATH
        self.SOUND_NAME = SOUND_NAME
        self.SOUND_PATH = SOUND_PATH
        self.OFFSETS = OFFSETS
        self.POSITION = POSITION

        # offsets
        self._top_offset = OFFSETS[0]
        self._right_offset = OFFSETS[1]
        self._bottom_offset = OFFSETS[2]
        self._left_offset = OFFSETS[3]

    # constants
    ANIMATION_FRAMES: int = 0
    IMAGE_NAME: str = ''
    IMAGE_PATH: str = ''
    NAME: str = ''
    SOUND_NAME: str = ''
    SOUND_PATH: str = ''
    OFFSETS: List[int] = [0, 0, 0, 0]
    POSITION: Tuple[int, int] = (0, 0)

    # variables
    collected: bool = False
    collected_player_method = None
    delete: bool = False
    mask: pygame.mask.Mask = None

    _alpha = 255
    _animation_frame: int = 0
    _collected_sound: pygame.mixer.Sound = None
    _debugger_message: str = ''
    _float: int = 0
    _rect: pygame.Rect = None
    _rotation_frame: int = 0
    _surf: pygame.Surface = None
    _text_rect: pygame.Rect = None
    _text_surf: pygame.Surface = None

    # offsets
    _left_offset: int = 0
    _right_offset: int = 0
    _top_offset: int = 0
    _bottom_offset: int = 0

    def setup_collectable(self):
        self._surf = pygame.image.load(f'{self.IMAGE_PATH}/{self.IMAGE_NAME}')
        self._rect = self._surf.get_rect()
        self.mask = pygame.mask.from_surface(self._surf)   
        globals.SCREEN.blit(self._surf, self.get_position())
        self.set_position(self.POSITION[0], self.POSITION[1] - self.get_height())
        self._float = self.get_position()[1] - 160

        # set sound
        self._collected_sound = pygame.mixer.Sound(f'{self.SOUND_PATH}/{self.SOUND_NAME}')
        self._text_float = self.get_position()[1] - 160

        self._text_surf = pygame.font.Font('fonts/Roboto-Bold.ttf', 24).render(self.NAME.lower(), True, (255, 255, 255))
        self._text_rect = self._text_surf.get_rect()

    def get_top(self):
        return self._rect.y + self._top_offset
    
    def get_bottom(self):
        return self._rect.bottom - self._bottom_offset
    
    def get_x(self):
        return self._rect.x
    
    def get_y(self):
        return self._rect.y

    def get_x_center(self):
        return self._rect.x + self._rect.width / 2
    
    def get_y_center(self):
        return self._rect.y + self._rect.height / 2
    
    def get_width(self):
        return self._rect.width - self._left_offset - self._right_offset
    
    def get_height(self):
        return self._rect.height - self._top_offset - self._bottom_offset
    
    def get_left(self):
        return self._rect.x + self._left_offset
    
    def get_right(self):    
        return self._rect.x + self.get_width() - self._right_offset
    
    def get_center_position(self) -> Tuple[int, int]: 
        return (self.get_x_center(), self.get_y_center())
    
    def get_position(self) -> Tuple[int, int]: 
        return (self.get_x(), self.get_y())

    def set_position(self, x = None, y = None):
        self._rect.x = x if x != None else self._rect.x
        self._rect.y = y if y != None else self._rect.y

    def animate(self):
        if (self._animation_frame < self.ANIMATION_FRAMES):
            if (not self.collected):
                self._surf = pygame.image.load(f'{self.IMAGE_PATH}/{self.ANIMATION_IMAGE_NAME}_{self._animation_frame}.png')
            else:
                self._surf = pygame.image.load(f'{self.IMAGE_PATH}/{self.ANIMATION_IMAGE_NAME_REVERSE}_{self._animation_frame}.png')
            self._animation_frame += 1
        else:
            self._animation_frame = 0

    def check_for_collision(self):        
        if self.mask.overlap(globals.player.mask, (globals.player.get_x() - self.get_x(), globals.player.get_y() - self.get_y())): 
            self.collected = True
            self._collected_sound.play()
            self.collected_player_method(self)

    def draw_obj(self, speed):
        self.animate()
        _new_x = self.POSITION[0] - speed if not globals.game_paused and globals.game_moving else self.get_x()
        self.set_position(_new_x)

        if (not self.collected):
            self.check_for_collision()
        else:
            _divisor = 4
            if (self.get_position()[1] > self._float + 3.1):
                self.set_position(None, self.get_y() - int((self.get_y() - self._float) / _divisor))
            else:
                self.set_position(None, self._float)  
                self._alpha = self._alpha / _divisor            
                if (self._alpha > 10):
                    self._surf.set_alpha(self._alpha)
                    self._text_surf.set_alpha(self._alpha)
                else:
                    self._surf.set_alpha(5)
                    self._text_surf.set_alpha(5)
                    self.delete = True
            
            globals.SCREEN.blit(self._text_surf, (self.get_position()[0] + 40, self.get_position()[1]))

        globals.SCREEN.blit(self._surf, self.get_position())