import pygame
import globals

class Debugger:
    @staticmethod
    def print(message):
        _title_message = 'The Reaper v1.0 Debug Mode: ON'
        _prefix = 'DEBUG: '

        if globals.debug and len(message) > 0:
            pygame.font.init()            
            debugger_message_font = pygame.font.Font('fonts/Roboto-Medium.ttf', 12)
            title_message_font = pygame.font.Font('fonts/Roboto-Bold.ttf', 12)
            title_message_surf = title_message_font.render(_title_message, True, (255, 255, 255), None)  
            debug_message_surf = debugger_message_font.render(f'{_prefix}{message}', True, (255, 255, 255), None)  
            debug_message_surf_rect = debug_message_surf.get_rect()
            title_message_surf_rect = title_message_surf.get_rect()

            # Create a new surface of the same size as the rectangle
            surf_bg = pygame.Surface((350, 100))

            surf_bg_rect = surf_bg.get_rect()
            surf_bg_rect.x = globals.SCREEN_WIDTH - 530
            surf_bg_rect.y = globals.GROUND
            
            title_message_surf_rect.center = surf_bg_rect.center   # Center the text surface within the background surface
            title_message_surf_rect.x += 20
            title_message_surf_rect.y += 10
            debug_message_surf_rect.center = title_message_surf_rect.center   # Center the text surface within the background surface
            debug_message_surf_rect.y += 20

            # Set the alpha of the surface
            surf_bg.set_alpha(160)

            pygame.draw.rect(surf_bg, (0, 0, 0), surf_bg_rect)
            globals.SCREEN.blit(surf_bg, surf_bg_rect.center)
            globals.SCREEN.blit(title_message_surf, title_message_surf_rect.center)
            globals.SCREEN.blit(debug_message_surf, debug_message_surf_rect.center)