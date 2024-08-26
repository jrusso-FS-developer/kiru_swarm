import pygame
from classes.level import Level, LevelConfig
import globals
import os
from pygame.locals import (
    K_ESCAPE
)

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.system('cls' if os.name == 'nt' else 'clear')
    clock = pygame.time.Clock()
    game_running = True
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("The Reaper")
    level_number = 1
    level = Level(level_number)

    def run_game(level_number) -> bool:
        try:
            level.draw()

            pygame.display.flip()
            
            if (globals.game_over):
                # TODO: game over screen
                pass

            if (level.end or globals.restart_level):
                level_number = level_number + 1 if not globals.restart_level else level_number
                if (level_number > len(list(LevelConfig))):
                    return -1
                globals.restart_level = False
                set_level(level_number)
            return level_number
        except Exception as e:
            print(f"Error: {e}")
            pygame.quit()

    def set_level(level_num):
        level.set(level_num)
        pygame.display.flip()

    # game loop
    while game_running:
        # set frame rate
        clock.tick(60)

        # set pressed keys
        globals.pressed_keys = pygame.key.get_pressed()

        # black screen
        globals.SCREEN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    game_running = False
            else:
                pass

        level_number = run_game(level_number)

        if level_number == -1:
            game_running = False
               

    pygame.quit()

if __name__ == "__main__":
    main()