import pygame
import globals

class LifeHUD:
    LEFT = globals.SCREEN_WIDTH // 2 - 350
    _dude_surfs = []
    _folder = ''

    def set_count(self, count):
        globals.player.life_count = count
        self.draw()

    def decrease_count(self, count = 1):
        globals.player.life_count -= count
        self.draw()

    def increase_count(self, count = 1):   
        globals.player.life_count += count
        self.draw()

    def set_folder(self, folder):
        self._folder = folder

    def draw(self):
        self._dude_surfs = []
        for i in range(globals.player.life_count):
            self._dude_surfs.append(pygame.image.load(f'{self._folder}/tiny.png'))
            surf = self._dude_surfs[i]
            rect = surf.get_rect() 
            rect.x = self.LEFT + (i * (rect.width - 8))
            rect.y = 15
            globals.SCREEN.blit(surf, rect)  