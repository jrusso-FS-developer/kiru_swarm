import pygame
import globals

class Score:
    def __init__(self, score):
        self._score = score
        self._point_scored_sound = pygame.mixer.Sound('sounds/sfx/point-scored.mp3')
        self._point_scored_sound.set_volume(.5)

    _score = 0
    _surf = None
    _point_scored_sound: pygame.mixer.Sound = None
    _rect = None

    def add_points(self, points):
        self._score += points
        self._point_scored_sound.play()
        self.draw()

    def get_score(self):
        return self._score
    
    def set_score(self, score):
        self._score = score
        self.draw()

    def draw(self):
        self._surf = pygame.image.load('sprites/assets/score_background.png')
        self._rect = self._surf.get_rect()
        self._rect.x = globals.SCREEN.get_width() - self._rect.width - 20
        self._rect.y = 12
        font = pygame.font.Font('fonts/Unkempt-Bold.ttf', 28)
        text_surf = font.render(f"score: {self._score}", True, (255, 255, 255))
        globals.SCREEN.blit(self._surf, self._rect)
        globals.SCREEN.blit(text_surf, (self._rect.x + 15, self._rect.y + 8))