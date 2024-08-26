import pygame
import globals

class HealthBarHUD:
    def __init__(self, health):
        self.health = health

    _shield_surf = None
    _shield_surf_rect = None
    _background_surf = None
    _background_surf_rect = None
    _health_bar_surf = None
    _health_bar_surf_rect = None
    LEFT_OFFSET = 0

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health
        self.draw()

    def decrease_health(self, amount):
        self.health -= amount

    def draw(self):
        try:
            self._shield_surf = pygame.image.load('sprites/assets/healthbar/health-shield.png')
            self._shield_surf_rect = self._shield_surf.get_rect() 
            self._shield_surf_rect.x = 15
            self._shield_surf_rect.y = 15
            self._background_surf = pygame.image.load('sprites/assets/healthbar/health-bar-background.png')
            self._background_surf_rect = self._background_surf.get_rect()
            self._background_surf_rect.x = 36
            self._background_surf_rect.y = 23     

            if (self.health <= 100):
                self.LEFT_OFFSET = (100 - self.health)
                self._health_bar_surf = pygame.image.load('sprites/assets/healthbar/health-bar-inner-100-80.png')
            if (self.health <= 80):
                self.LEFT_OFFSET = (80 - self.health)
                self._health_bar_surf = pygame.image.load('sprites/assets/healthbar/health-bar-inner-80-60.png')
            if (self.health <= 60):
                self.LEFT_OFFSET = (60 - self.health)
                self._health_bar_surf = pygame.image.load('sprites/assets/healthbar/health-bar-inner-60-40.png')
            if (self.health <= 40):
                self.LEFT_OFFSET = (40 - self.health)
                self._health_bar_surf = pygame.image.load('sprites/assets/healthbar/health-bar-inner-40-0.png')
            
            self._health_bar_surf_rect = self._health_bar_surf.get_rect()
            self._health_bar_surf_rect.x = 53 - self.LEFT_OFFSET
            self._health_bar_surf_rect.y = 27
            
            globals.SCREEN.blit(self._background_surf, self._background_surf_rect)    
            globals.SCREEN.blit(self._health_bar_surf, self._health_bar_surf_rect)   
            globals.SCREEN.blit(self._shield_surf, self._shield_surf_rect) 
        except Exception as e:
            print(f"Error drawing health bar: {e}")

    def __str__(self):
        return f"Health: {self.health}"
