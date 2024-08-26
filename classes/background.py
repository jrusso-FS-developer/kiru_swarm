import gc
import math
import pygame
from classes.debugger import Debugger
import globals

class ImageBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        self.set(x, y, path)

    def set(self, x, y, path):
        super(ImageBlock, self).__init__()
        self.surf = pygame.image.load(path)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        self.set(x, y, level)

    # game vars   
    FLASHY_FRAMES_MAX = 5
         
    end = False    
    pygame.font.init()  # Initialize the font module
    font = pygame.font.Font('fonts/Unkempt-Bold.ttf', 42)
    text_surf = None
    text_begin_surf = None
    screen_center = (0, 0)
    length = 0
    moving = False
    
    _tile_count_backdrop = 0
    _tile_count_foreground = 0
    _scroll = 0
    _scroll_foreground_multiplier = 3.5
    _scroll_midground_multiplier = 2.25
    _intro_timer = 240
    _title_alpha = 255
    _begin_alpha = 255
    _flashy_frames = FLASHY_FRAMES_MAX
    _flashy_count = 0
    _game_paused = False
    _header_surf: pygame.Surface = None
    _header_bg_surf_rect: pygame.Rect = None

    def set(self, x, y, level):
        super(Background, self).__init__()
        self._scroll = 0
        self.set_images(x, y, level)
        self._tile_count_backdrop = math.ceil(level.length / self.surf_backdrop_rect.width)
        self._tile_count_foreground = math.ceil(level.length / self.surf_backdrop_rect.width * self._scroll_foreground_multiplier)
        self._tile_count_midground = math.ceil(level.length / self.surf_backdrop_rect.width * self._scroll_midground_multiplier)
        self.level = level
        self.text_begin_surf = self.font.render(f'begin!!!', True, (255, 255, 255), None)  
        self.text_surf = self.font.render(f'Level: "{level.name}" ', True, (255, 255, 255), None)  
        self.text_begin_bg_surf = pygame.image.load('sprites/backgrounds/begin_bg.png')  
        self.text_begin_bg_surf_rect = self.text_begin_bg_surf.get_rect()
        self.text_begin_surf_rect = self.text_begin_surf.get_rect()
        self.text_surf_rect = self.text_surf.get_rect()
        self.screen_center = globals.screen_center
        self._intro_timer = 380
        self._title_alpha = 0
        self._begin_alpha = 0
        self._flashy_frames = self.FLASHY_FRAMES_MAX
        self._flashy_count = 0

        # set the HUD background
        self._header_bg_surf = pygame.Surface((globals.SCREEN_WIDTH, 75))
        self._header_bg_surf_rect = self._header_bg_surf.get_rect()
        self._header_bg_surf_rect.center = (0, 0)
        self._header_bg_surf.set_alpha(80)

        pygame.draw.rect(self._header_bg_surf, (0, 0, 0), self._header_bg_surf_rect)

    def set_images(self, x, y, level):
        # backgrop
        self.surf_backdrop = pygame.image.load(level.backdroppath)
        self.surf_backdrop_rect = self.surf_backdrop.get_rect()
        self.surf_backdrop_rect.x = x
        self.surf_backdrop_rect.y = y

        # foreground
        self.surf_foreground = []
        for i in range(len(level.foregroundpaths)):
            self.surf_foreground.append(ImageBlock(x, y, level.foregroundpaths[i]))

        # midground
        self.surf_midground = []
        for i in range(len(level.midgroundpaths)):
            self.surf_midground.append(ImageBlock(x, y, level.midgroundpaths[i]))

    def draw(self):
        fi = 0
        mi = 0
        scroll = self._scroll if globals.game_moving and not globals.player.is_dying else 0

        for i in range(self._tile_count_backdrop):
            globals.SCREEN.blit(self.surf_backdrop, (i * self.surf_backdrop_rect.width + scroll, 0))
        for i in range(self._tile_count_midground):
            surf_midground = self.surf_midground[mi]
            globals.SCREEN.blit(surf_midground.surf, (i * surf_midground.rect.width + (scroll * self._scroll_midground_multiplier), -150))
            mi = mi + 1 if mi < (len(self.surf_midground) - 1) else 0
        for i in range(self._tile_count_foreground):
            surf_foreground = self.surf_foreground[fi]
            # globals.screen.blit(surf_foreground.surf, (i * surf_foreground.rect.width + (scroll * self._scroll_foreground_multiplier), 150))
            fi = fi + 1 if fi < (len(self.surf_foreground) - 1) else 0
            
        globals.SCREEN.blit(self._header_bg_surf, self._header_bg_surf_rect.center)

        if (not globals.game_paused):
            if (globals.game_moving):    
                self._scroll -= globals.bg_scroll_speed
                self.length = globals.SCREEN.get_width() - self._scroll

                if self._scroll > -10:
                    self.text_begin_bg_surf_rect.center = (self.screen_center[0] - self.text_begin_bg_surf_rect.width / 2, self.screen_center[1] - self.text_begin_bg_surf_rect.height - 45)
                    self.text_begin_surf_rect.center = (self.screen_center[0] - self.text_begin_surf_rect.width / 2, self.screen_center[1] - self.text_begin_surf_rect.height - 80)
                    self.text_begin_bg_surf.set_alpha(255)
                    globals.SCREEN.blit(self.text_begin_bg_surf, self.text_begin_bg_surf_rect.center)
                    globals.SCREEN.blit(self.text_begin_surf, self.text_begin_surf_rect.center)

                if self.level:
                    if self.length >= self.level.length:
                        globals.game_moving = False
                        self.level.end = True                    
                        del self.level
                        gc.collect()
            
            if (self._intro_timer > 0):
                self._intro_timer -= 1.25

                if (self._intro_timer > 220):
                    self._title_alpha = self._title_alpha + 8 if self._title_alpha < 255 else 255
                    self.text_bg_surf = pygame.image.load('sprites/backgrounds/title_bg.png') if self._flashy_frames < 2 else pygame.image.load('sprites/backgrounds/title_bg_flashy.png') 
                    if self._flashy_frames > 0:
                        self._flashy_frames -= 1
                    else: 
                        self._flashy_count += 1
                        self._flashy_frames = self.FLASHY_FRAMES_MAX - self._flashy_count
                elif (self._intro_timer <= 220 and self._intro_timer > 0):
                    if self._intro_timer > 200:
                        self._flashy_frames = self.FLASHY_FRAMES_MAX
                    self._title_alpha = self._title_alpha - 8 if self._title_alpha > 0 else 0
                    self.text_bg_surf = pygame.image.load('sprites/backgrounds/title_bg.png') if self._flashy_frames > 2 else pygame.image.load('sprites/backgrounds/title_bg_flashy.png') 
                    if self._flashy_frames > 0:
                        self._flashy_frames -= 1
                    else: 
                        self._flashy_count += 1
                        self._flashy_frames = self.FLASHY_FRAMES_MAX - self._flashy_count

                self.text_bg_surf_rect = self.text_bg_surf.get_rect()

                self.text_bg_surf_rect.center = (self.screen_center[0] - self.text_bg_surf_rect.width / 2, self.screen_center[1] - self.text_bg_surf_rect.height -10)
                self.text_surf_rect.center = (self.screen_center[0] - self.text_surf_rect.width / 2, self.screen_center[1] - self.text_surf_rect.height - 80)
                self.text_bg_surf.set_alpha(self._title_alpha)
                self.text_surf.set_alpha(self._title_alpha)
                globals.SCREEN.blit(self.text_bg_surf, self.text_bg_surf_rect.center)
                globals.SCREEN.blit(self.text_surf, self.text_surf_rect.center)
            else:
                globals.game_moving = True