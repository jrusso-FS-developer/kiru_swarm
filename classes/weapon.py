import pygame
import globals

from classes.config.map_config import MapWeaponBlock

class Weapon(MapWeaponBlock):
    def __init__(self, config: MapWeaponBlock, selected = False, collected: bool = False):
        super().__init__(config,
                         config.POSITION)
        self.set(selected, collected)
        
    # variables
    collected: bool = False
    collect_sound: pygame.mixer.Sound = None
    hit_sound: pygame.mixer.Sound = None
    woosh_sound: pygame.mixer.Sound = None
    selected: bool = False

    _alpha = 255
    _animation_frame: int = 0
    delete: bool = False
    _float: int = 0
    _mask: pygame.mask.Mask = None
    _surf: pygame.Surface = None
    _rect: pygame.Rect = None

    def get_x(self):
        return self._rect.x

    def get_y(self):
        return self._rect.y
    
    def get_height(self):
        return self._rect.height
    
    def get_position(self):
        return (self._rect.x, self._rect.y)

    def set_position(self, x = None, y = None):
        self._rect.x = x if x != None else self._rect.x
        self._rect.y = y if y != None else self._rect.y

    def set(self, selected, collected):
        self.selected = selected
        self.collected = collected
        self.woosh_sound = pygame.mixer.Sound(f'{self.SOUND_PATH}/woosh.mp3')
        self.hit_sound = pygame.mixer.Sound(f'{self.SOUND_PATH}/hit.mp3')
        self.collect_sound = pygame.mixer.Sound(f'{self.SOUND_PATH}/collect.mp3')
        self.woosh_sound.set_volume(.35)
        self.hit_sound.set_volume(.70)
        self._animation_frame: int = 0

        self._surf = pygame.image.load(f'{self.IMAGE_PATH}/inventory.png')
        self._rect = self._surf.get_rect()
        self._mask = pygame.mask.from_surface(self._surf) 

        self.set_position(self.POSITION[0], self.POSITION[1] - self.get_height())
        self._float = self.get_position()[1] - 160

    def play_hit(self):
        self.hit_sound.play()
    
    def play_woosh(self):
        self.woosh_sound.play()

    def animate(self):
        if (self._animation_frame < self.ANIMATION_FRAMES):
            self._surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/spinning_{self._animation_frame}.png')
            self._animation_frame += 1
        else:
            self._animation_frame = 0
            self._surf = pygame.image.load(f'{self.IMAGE_PATH}/animations/spinning_{self._animation_frame}.png')

    def check_for_collision(self):        
        if self._mask.overlap(globals.player.mask, (globals.player.get_x() - self.get_x(), globals.player.get_y() - self.get_y())): 
            self.collected = True
            self.collect_sound.play()
            globals.player.collect_weapon(self)

    def draw(self, speed):
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
                else:
                    self._surf.set_alpha(5)
                    self.delete = True

        globals.SCREEN.blit(self._surf, self._rect)