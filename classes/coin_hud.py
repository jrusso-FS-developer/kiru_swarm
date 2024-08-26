import pygame
import globals

class CoinHUD:
    def __init__(self):
        self.coins = 0
        self.font = pygame.font.Font(None, 36)
        self.set()

    # variables
    coins: int = 0
    font: pygame.font.Font = None

    _surf: pygame.Surface = None
    _rect: pygame.Rect = None
    _text_surf: pygame.Surface = None
    _text_rect: pygame.Rect = None

    def set(self):
        self.coins = 0
        self._surf = pygame.image.load('sprites/items/coin/coin_small.png')
        self._rect = self._surf.get_rect()
        self.set_position(1120, 15)

    def add_coins(self, amount):
        self.coins += amount

    def remove_coins(self, amount):
        self.coins -= amount

    def get_x(self):
        return self._rect.x
    
    def get_y(self):
        return self._rect.y

    def get_position(self):
        return (self._rect.x, self._rect.y)

    def set_position(self, x, y):
        self._rect.x = x if x != None else self._rect.x
        self._rect.y = y if y != None else self._rect.y   

    def draw(self):
        self.font = pygame.font.Font('fonts/Roboto-Bold.ttf', 36)
        self._text_surf = self.font.render(f'{self.coins} x ', True, (252, 186, 3))
        self._text_rect = self._text_surf.get_rect()
        self._text_rect.x = self.get_x() - self._text_rect.width
        self._text_rect.y = 20

        globals.SCREEN.blit(self._text_surf, self._text_rect)
        globals.SCREEN.blit(self._surf, self.get_position())