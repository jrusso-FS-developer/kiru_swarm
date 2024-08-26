import pygame
import globals

class Halo:
    def __init__(self):
        self.set()

    #variables
    _animation_frame_count: int = 12 
    _animation_frame: int = 0 
    _folder: str = 'sprites/assets/halo/animations'
    _rect: pygame.Rect = None
    _surf: pygame.Surface = None

    def set_position(self, x = None, y = None):
        self._rect.x = x if x != None else self._rect.x
        self._rect.y = y if y != None else self._rect.y        

    def set(self):
        self._surf = pygame.image.load(f'{self._folder}/spin_0.png')
        self._rect = self._surf.get_rect()

    def draw(self):
        self._surf = pygame.image.load(f'{self._folder}/spin_{self._animation_frame}.png')

        if (self._animation_frame < self._animation_frame_count - 1):
            self._animation_frame += 1
        else:
            self._animation_frame = 0

        globals.SCREEN.blit(self._surf, self._rect)